import cv2
import mediapipe as mp

class MediapipeLandmark:
    def __init__(self, max_num_hands=2, model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def Coordinates(self, frame):
        val = int()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                val = int(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
        return abs(val)
