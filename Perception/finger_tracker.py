import cv2 as cv
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()

def get_index_finger_position(frame):
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            lm = handlms[8]
            h, w, _ = frame.shape
            return (int(lm.x * w), int(lm.y * h))