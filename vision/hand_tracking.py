import cv2
import mediapipe as mp
from config import WIDTH, HEIGHT, MODEL_PATH

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

def get_frame_and_finger():
    ret, frame = cap.read()
    if not ret:
        return None, None, None

    frame = cv2.flip(frame, 1)

    # detecção
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = detector.detect(mp_image)

    dedo_x, dedo_y = None, None

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            h, w, _ = frame.shape
            dedo_x = int(hand_landmarks[8].x * WIDTH)
            dedo_y = int(hand_landmarks[8].y * HEIGHT)

    return frame, dedo_x, dedo_y

def release_camera():
    cap.release()