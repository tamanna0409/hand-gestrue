import cv2
import mediapipe as mp
import os
import time
import subprocess

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75)
Draw = mp.solutions.drawing_utils

photo_folder = "photos"
os.makedirs(photo_folder, exist_ok=True)

def capture_photo():
    cap = cv2.VideoCapture(0)
    photo_count = 1
    last_capture_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Process = hands.process(frameRGB)

        landmarkList = []
        if Process.multi_hand_landmarks:
            for handlm in Process.multi_hand_landmarks:
                for _id, landmarks in enumerate(handlm.landmark):
                    height, width, _ = frame.shape
                    x, y = int(landmarks.x * width), int(landmarks.y * height)
                    landmarkList.append([_id, x, y])
                Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

        if len(landmarkList) >= 21:
            index_tip = landmarkList[8][2]
            middle_tip = landmarkList[12][2]
            ring_knuckle = landmarkList[13][2]
            other_fingers_down = all(landmarkList[i][2] > ring_knuckle for i in [16, 20])
            is_index_raised = index_tip < ring_knuckle
            is_middle_raised = middle_tip < ring_knuckle
            current_time = time.time()

            if is_index_raised and is_middle_raised and other_fingers_down and (current_time - last_capture_time > 5):
                photo_path = os.path.join(photo_folder, f"photo_{photo_count}.jpg")
                cv2.imwrite(photo_path, frame)
                if os.name == "nt":
                    os.startfile(photo_path)
                elif os.name == "posix":
                    subprocess.run(["xdg-open", photo_path])
                photo_count += 1
                last_capture_time = current_time

        cv2.imshow('Photo Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
