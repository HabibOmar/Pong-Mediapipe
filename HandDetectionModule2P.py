import cv2
import mediapipe as mp

class MediapipeLandmark:
    def __init__(self, max_num_hands=2, model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=model_complexity
        )

    def Coordinates(self, frame):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)

        left_hand_coordinates = int()

        right_hand_coordinates = int()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print(hand_landmarks)
                landmarks = []  # List to store the coordinates of landmarks for each hand
                for landmark in hand_landmarks.landmark:
                    x, y = landmark.x, landmark.y,  # Get the X, Y coordinates
                    landmarks.append((x, y))
                    # print(landmarks)

                # Determine if the hand is on the left or right based on the X-coordinate of the palm landmark (landmark[0])
                if landmarks[0][0] < 0.5:
                    if results.multi_hand_landmarks!=None:
                        left_hand_coordinates = [x[1]for x in landmarks]
                        left_hand_coordinates = [i *720 for i in left_hand_coordinates]
                        left_hand_coordinates = abs(int(left_hand_coordinates[5]))
                else:
                    if results.multi_hand_landmarks!=None:
                        right_hand_coordinates = [x[1] for x in landmarks]
                        right_hand_coordinates = [i *720 for i in right_hand_coordinates]
                        right_hand_coordinates = abs(int(right_hand_coordinates[5]))

        return 720 - left_hand_coordinates, 720 - right_hand_coordinates
