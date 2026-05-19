from yolobit import *
from machine import Pin, PWM
import time
SERVO_GPIO = pin3.pin
SERVO_CLOSE_DUTY = 51
SERVO_OPEN_DUTY  = 102
AUTO_CLOSE_SECS = 0
class DoorController:
    def __init__(self):
        self.servo = PWM(Pin(SERVO_GPIO), freq=50)
        self._is_open   = False
        self._opened_at = 0
        self.close()
    def open(self):
        self.servo.duty(SERVO_OPEN_DUTY)
        self._is_open   = True
        self._opened_at = time.time()
        print("[Door] Open door - duty:", SERVO_OPEN_DUTY)
    def close(self):
        self.servo.duty(SERVO_CLOSE_DUTY)
        self._is_open   = False
        self._opened_at = 0
        print("[Door] Close door - duty:", SERVO_CLOSE_DUTY)
    def toggle(self):
        self.close() if self._is_open else self.open()
    @property
    def is_open(self):
        return self._is_open
    def check(self):
        self._check_auto_close()
    def door_callback(self, topic, msg):
        cmd = msg.decode().strip().lower()
        print("[Door] Lenh MQTT:", cmd)
        if cmd in ("open", "1") and not self._is_open:
            self.open()
        elif cmd in ("close", "0") and self._is_open:
            self.close()
        elif cmd == "toggle":
            self.toggle()
    def _check_auto_close(self):
        if AUTO_CLOSE_SECS > 0 and self._is_open and self._opened_at:
            if time.time() - self._opened_at >= AUTO_CLOSE_SECS:
                print("[Door] Automatically close door")
                self.close()
door = DoorController()
