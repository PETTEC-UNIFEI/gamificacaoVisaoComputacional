import cv2
import mediapipe as mp
from config import WIDTH, HEIGHT, MODEL_PATH

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

with open(MODEL_PATH, "rb") as f:
    model_data = f.read()

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_buffer=model_data),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

SMOOTHING_ALPHA = 0.4  # 0 = sem suavização, 1 = ignora leituras novas
smooth_x, smooth_y = None, None

def get_frame_and_finger():
    global smooth_x, smooth_y

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

        if smooth_x is None:
            smooth_x, smooth_y = dedo_x, dedo_y
        else:
            smooth_x = SMOOTHING_ALPHA * dedo_x + (1 - SMOOTHING_ALPHA) * smooth_x
            smooth_y = SMOOTHING_ALPHA * dedo_y + (1 - SMOOTHING_ALPHA) * smooth_y

        dedo_x, dedo_y = int(smooth_x), int(smooth_y)
    else:
        smooth_x, smooth_y = None, None

    return frame, dedo_x, dedo_y

def release_camera():
    cap.release()