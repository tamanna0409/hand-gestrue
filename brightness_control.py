import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
from math import hypot

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75)
Draw = mp.solutions.drawing_utils

def control_brightness():
    cap = cv2.VideoCapture(0)
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

        if landmarkList:
            x1, y1 = landmarkList[4][1], landmarkList[4][2]
            x2, y2 = landmarkList[8][1], landmarkList[8][2]
            L = hypot(x2 - x1, y2 - y1)
            b_level = np.interp(L, [15, 220], [0, 100])
            sbc.set_brightness(int(b_level))

        cv2.imshow('Brightness Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
