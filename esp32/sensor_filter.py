
import time
TEMP_ZONES = [
    (-99, 20, "Lanh"),
    (20,  26, "Thoai mai"),
    (26,  30, "Am"),
    (30,  33, "Nong"),
    (33,  99, "Rat nong"),
]
HUMI_ZONES = [
    (0,   40, "Kho"),
    (40,  65, "Ly tuong"),
    (65,  80, "Am"),
    (80, 101, "Rat am"),
]
LIGHT_ZONES = [
    (0,   20, "Toi"),
    (20,  60, "Trung binh"),
    (60, 101, "Sang"),
]
HYSTERESIS_TEMP   = 0.7
HYSTERESIS_HUMI   = 2.0
HYSTERESIS_LIGHT  = 3.0
MIN_INTERVAL_SECS = 10
HEARTBEAT_SECS    = 300
def _find_zone(value, zones, current=None, hysteresis=0):
    """
    Tìm zone của value, có hysteresis:
    - Nếu đang trong `current` zone: chỉ rời khi value vượt biên thêm `hysteresis`.
    - Nếu chưa có zone: tìm zone theo định nghĩa cứng.
    """
    if current is not None:
        for lo, hi, name in zones:
            if name == current:
                if (lo - hysteresis) <= value < (hi + hysteresis):
                    return current
                break
    for lo, hi, name in zones:
        if lo <= value < hi:
            return name
    return zones[-1][2]
class SensorFilter:
    """Theo dõi zone của 3 cảm biến, báo khi nào nên publish."""
    def __init__(self):
        self.temp_zone  = None
        self.humi_zone  = None
        self.light_zone = None
        self.last_send  = 0
    def should_send(self, temp, humi, light):
        """
        Trả về (send_or_not, reason_string).
        Tự động cập nhật state nội bộ nếu trả về True.
        """
        new_t = _find_zone(temp,  TEMP_ZONES,  self.temp_zone,  HYSTERESIS_TEMP)
        new_h = _find_zone(humi,  HUMI_ZONES,  self.humi_zone,  HYSTERESIS_HUMI)
        new_l = _find_zone(light, LIGHT_ZONES, self.light_zone, HYSTERESIS_LIGHT)
        now       = time.time()
        rate_ok   = (now - self.last_send) >= MIN_INTERVAL_SECS
        heartbeat = (now - self.last_send) >= HEARTBEAT_SECS
        changes = []
        if new_t != self.temp_zone:
            changes.append("Temp:{}->{}".format(self.temp_zone, new_t))
        if new_h != self.humi_zone:
            changes.append("Humi:{}->{}".format(self.humi_zone, new_h))
        if new_l != self.light_zone:
            changes.append("Light:{}->{}".format(self.light_zone, new_l))
        should = (bool(changes) and rate_ok) or heartbeat
        if should:
            self.temp_zone  = new_t
            self.humi_zone  = new_h
            self.light_zone = new_l
            self.last_send  = now
            reason = "Zone change [" + ", ".join(changes) + "]" if changes else "Heartbeat"
            return True, reason
        return False, None
    def current_zones(self):
        """Trả về tuple (temp_zone, humi_zone, light_zone) hiện tại."""
        return (self.temp_zone, self.humi_zone, self.light_zone)
