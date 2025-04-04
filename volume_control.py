import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75)
Draw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def control_volume():
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
            x2, y2 = landmarkList[20][1], landmarkList[20][2]
            distance = math.hypot(x2 - x1, y2 - y1)
            vol_level = np.interp(distance, [15, 220], [-65.25, 0])
            volume.SetMasterVolumeLevel(vol_level, None)

        cv2.imshow('Volume Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
