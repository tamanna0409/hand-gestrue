import cv2
import mediapipe as mp
import os

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75)
Draw = mp.solutions.drawing_utils

def open_file_manager():
    cap = cv2.VideoCapture(0)
    file_manager_opened = False

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

        if not file_manager_opened and len(landmarkList) >= 21:
            thumb_tip = landmarkList[4][2]
            index_knuckle = landmarkList[5][2]
            is_thumb_up = thumb_tip < index_knuckle
            is_other_fingers_down = all(landmarkList[i][2] > index_knuckle for i in [8, 12, 16, 20])

            if is_thumb_up and is_other_fingers_down:
                print("Opening File Manager...")
                os.system("explorer" if os.name == "nt" else "xdg-open .")
                file_manager_opened = True

        cv2.imshow('File Manager Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
