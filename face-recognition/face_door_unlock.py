
import cv2
import time
import serial
import os
from AI_module import FaceRecognizer
SERIAL_PORT = "COM6"
BAUDRATE    = 115200
SER_TIMEOUT = 0.3
AUTHORIZED           = {"Huy", "Nguyen"}
CONFIDENCE_THRESHOLD = 70
COOLDOWN_SECS        = 8
STREAK_REQUIRED      = 3
def send_cmd(ser, cmd, wait=1.0):
    """Gửi lệnh, đợi và trả về dòng response (đã strip "RESP:" prefix)."""
    ser.reset_input_buffer()
    ser.write((cmd + "\n").encode())
    deadline = time.time() + wait
    while time.time() < deadline:
        line = ser.readline().decode(errors="ignore").strip()
        if line.startswith("RESP:"):
            return line[5:]
    return None
def main():
    if not os.path.exists("detector.tflite"):
        print("[ERROR] Thieu 'detector.tflite' — xem huong dan trong AI_module.py")
        return
    print(f"[INIT] Mo Serial {SERIAL_PORT}@{BAUDRATE}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=SER_TIMEOUT)
        time.sleep(2)
    except serial.SerialException as e:
        print(f"[ERROR] Khong mo duoc {SERIAL_PORT}: {e}")
        print("        Kiem tra COM port trong Device Manager.")
        return
    resp = send_cmd(ser, "PING", wait=2.0)
    if resp == "PONG":
        print("[INIT] ESP32 OK (PONG)")
    else:
        print(f"[WARN] Khong nhan duoc PONG (got: {resp}). Van tiep tuc...")
    print("[INIT] Loading face recognizer...")
    recognizer = FaceRecognizer()
    recognizer.train("face_dataset/")
    print(f"[INIT] Authorized: {AUTHORIZED}\n")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Khong mo duoc camera.")
        ser.close()
        return
    last_unlock = 0
    streak_name = None
    streak_cnt  = 0
    print("[INFO] Nhan 'q' de thoat.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        identities = recognizer.identify_faces(frame)
        best = None
        for person in identities:
            x, y, w, h = person["box"]
            name       = person["name"]
            conf       = person["confidence"]
            authorized = name in AUTHORIZED and conf < CONFIDENCE_THRESHOLD
            color      = (0, 255, 0) if authorized else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{name} ({conf})", (x, max(20, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            if authorized and (best is None or conf < best["confidence"]):
                best = person
        now = time.time()
        if best:
            if best["name"] == streak_name:
                streak_cnt += 1
            else:
                streak_name = best["name"]
                streak_cnt  = 1
            cv2.putText(frame, f"Streak: {streak_cnt}/{STREAK_REQUIRED}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if streak_cnt >= STREAK_REQUIRED and (now - last_unlock) > COOLDOWN_SECS:
                print(f"[UNLOCK] {best['name']} (conf={best['confidence']})")
                resp = send_cmd(ser, "DOOR_OPEN")
                print(f"  → ESP32: {resp}")
                if resp and resp.startswith("OK"):
                    last_unlock = now
                    cv2.putText(frame, "UNLOCKED!", (10, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        else:
            streak_name = None
            streak_cnt  = 0
        remaining = max(0, COOLDOWN_SECS - (now - last_unlock))
        if remaining > 0:
            cv2.putText(frame, f"Cooldown: {remaining:.1f}s",
                        (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        cv2.imshow("Face Door Unlock", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
if __name__ == "__main__":
    main()
