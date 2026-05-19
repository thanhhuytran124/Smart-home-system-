
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
class FaceRecognizer:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='detector.tflite')
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map = {}
    def _crop_face(self, img_bgr):
        """Dùng MediaPipe detect & crop khuôn mặt. Trả về ảnh gray 200x200 hoặc None."""
        rgb_img  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
        result   = self.detector.detect(mp_image)
        if not result.detections:
            return None
        det  = max(result.detections, key=lambda d: d.bounding_box.width * d.bounding_box.height)
        bbox = det.bounding_box
        x, y, w, h = max(0, bbox.origin_x), max(0, bbox.origin_y), bbox.width, bbox.height
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        face = gray[y:y + h, x:x + w]
        if face.size == 0:
            return None
        return cv2.resize(face, (200, 200))
    def train(self, dataset_path):
        """Phát hiện khuôn mặt trong từng ảnh, crop, rồi train LBPH."""
        faces      = []
        labels     = []
        current_id = 0
        if not os.path.exists(dataset_path):
            print(f"[ERROR] Path {dataset_path} does not exist!")
            return
        print("[INFO] Training AI on your dataset...")
        for person_name in sorted(os.listdir(dataset_path)):
            person_dir = os.path.join(dataset_path, person_name)
            if not os.path.isdir(person_dir):
                continue
            self.label_map[current_id] = person_name
            count_ok = 0
            count_skip = 0
            for image_name in os.listdir(person_dir):
                img_path = os.path.join(person_dir, image_name)
                img      = cv2.imread(img_path)
                if img is None:
                    count_skip += 1
                    continue
                face = self._crop_face(img)
                if face is None:
                    print(f"  [SKIP] Khong tim thay khuon mat: {image_name}")
                    count_skip += 1
                    continue
                faces.append(face)
                labels.append(current_id)
                count_ok += 1
            print(f"  [{person_name}] OK: {count_ok} | Skip: {count_skip}")
            current_id += 1
        if len(faces) > 0:
            self.recognizer.train(faces, np.array(labels))
            print(f"[INFO] Success! Loaded {len(self.label_map)} people, total {len(faces)} face samples.")
        else:
            print("[ERROR] No usable face images found in dataset folders.")
    def identify_faces(self, frame):
        """Detects and returns names + coordinates."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)
        results_list = []
        if detection_result.detections:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                x, y, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                face_roi = gray[max(0,y):y+h, max(0,x):x+w]
                if face_roi.size == 0: continue
                face_roi = cv2.resize(face_roi, (200, 200))
                label_id, confidence = self.recognizer.predict(face_roi)
                name = self.label_map.get(label_id, "Unknown") if confidence < 75 else "Unknown"
                results_list.append({
                    "name": name,
                    "box": (x, y, w, h),
                    "confidence": round(confidence, 2)
                })
        return results_list
if __name__ == "__main__":
    if not os.path.exists('detector.tflite'):
        print("[ERROR] Khong tim thay 'detector.tflite' trong thu muc hien tai.")
        print("Tai ve tu: https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite")
        print("Sau do doi ten thanh 'detector.tflite' va dat cung thu muc voi AI_module.py")
        exit(1)
    recognizer = FaceRecognizer()
    recognizer.train('face_dataset/')
    CAMERA_URL = 0
    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        print(f"[ERROR] Khong mo duoc camera (source={CAMERA_URL}).")
        exit(1)
    print("[INFO] Nhan 'q' de thoat.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Khong doc duoc frame tu camera.")
            break
        identities = recognizer.identify_faces(frame)
        for person in identities:
            x, y, w, h = person["box"]
            name       = person["name"]
            conf       = person["confidence"]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{name} ({conf})", (x, max(20, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow("IoT Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
