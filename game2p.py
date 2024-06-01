import cv2
import numpy as np
import random
from HandDetectionModule2P import MediapipeLandmark

# parameters
width = 1280
height = 720
paddleWidth = 200
paddleHeight = 20
paddleColor = (75, 153, 242)
deltaxInitial = random.choice([-10, 10])
deltayInitial = random.randint(-10, 10)
DeltaX = deltaxInitial
DeltaY = deltayInitial
xPos = 640
yPos = 400
rounds = 1
ball = True
BallRadius = 8
P1Score = 0
P2Score = 0
bgColor = (30, 79, 24)
scoreColor = (149, 129, 252)

""" Method to increase ball speed"""


def increaseBallSpeed(deltaX, deltaY):
    if abs(deltaX) < 25:
        if deltaX > 0:
            deltaX += 5
        else:
            deltaX -= 5

    if abs(deltaY) < 20:
        if deltaY > 0:
            deltaY += 2
        else:
            deltaY -= 2
    return deltaX, deltaY


# Start webcam livestream capture and set dimensions
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FPS, 30)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('Classic Pong Game 2P', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Classic Pong Game 2P', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

prevVal_L = 400
prevVal_R = 400

handData = MediapipeLandmark()

run = True
# game loop
while run:
    # start the camera recording
    _, frame = camera.read()

    # get the hand coordinates from HandDetectionModule
    right_hand_coordinates, left_hand_coordinates = handData.Coordinates(frame)
    # print(right_hand_coordinates)

    background = cv2.imread('redblue.png')
    # Resize the background image to match the desired dimensions (720x1366)
    background = cv2.resize(background, (1366, 720))
    frameresize = cv2.resize(frame, (144, 81))
    frameresize = cv2.flip(frameresize, 1)

    # Overlay the resized frame on the resized background
    background[639:720, 1222:1366] = frameresize

    # invert the y-coordinates so 0 is down and max is up
    val_R = right_hand_coordinates
    val_L = left_hand_coordinates

    # Update the coordinates of the paddle if there's a new input from handdetection module
    if val_L == 720:
        val_L = prevVal_L
    else:
        prevVal_L = val_L

    if val_R == 720:
        val_R = prevVal_R
    else:
        prevVal_R = val_R

    # Paddle for right player
    cv2.rectangle(background, (1366 - paddleHeight, 720 - (val_R + paddleWidth // 2)),
                  (1366, 720 - (val_R - paddleWidth // 2)), paddleColor, -1)
    RightPaddLeUpperCorner = (1366 - paddleHeight, 720 - (val_R + paddleWidth // 2))
    RightPaddleLowerCorner = (1366 - paddleHeight, 720 - (val_R - paddleWidth // 2))

    # Paddle for left player
    cv2.rectangle(background, (paddleHeight, 720 - (val_L + paddleWidth // 2)), (0, 720 - (val_L - paddleWidth // 2)),
                  paddleColor, -1)
    LeftPaddleUpperCorner = (paddleHeight, 720 - (val_L + paddleWidth // 2))
    LeftPaddleLowerCorner = (paddleHeight, 720 - (val_L - paddleWidth // 2))

    # Displays the scores
    cv2.putText(background, 'P1 Score: ' + str(P1Score), (150, 35), cv2.FONT_HERSHEY_PLAIN, 1, scoreColor, 2)
    cv2.putText(background, 'P2 Score: ' + str(P2Score), (1000, 35), cv2.FONT_HERSHEY_PLAIN, 1, scoreColor, 2)
    cv2.putText(background, 'Round: ' + str(rounds), (575, 35), cv2.FONT_HERSHEY_PLAIN, 1, scoreColor, 2)

    # Creates the ball and initiates its movement
    if ball == True:
        cv2.circle(background, (xPos, yPos), BallRadius, (255, 255, 255), -1)
        yPos += DeltaY
        xPos += DeltaX

    # Checks collision with paddle as ball aproaches the left or right edges
    if xPos >= 1330 and xPos <= 1355:
        if (yPos >= RightPaddLeUpperCorner[1]) and (yPos <= RightPaddleLowerCorner[1]):
            DeltaX = -DeltaX
            DeltaX, DeltaY = increaseBallSpeed(DeltaX, DeltaY)

    if xPos <= 25 and xPos >= 0:
        if (yPos >= LeftPaddleUpperCorner[1]) and (yPos <= LeftPaddleLowerCorner[1]):
            DeltaX = -DeltaX
            DeltaX, DeltaY = increaseBallSpeed(DeltaX, DeltaY)

    # If ball collides with upper or lower edge, reflect along the invert the deltay
    if yPos >= 695 or yPos <= 10:
        DeltaY = -DeltaY

    if xPos >= 1390:
        P1Score += 1
        temp = cv2.blur(background, (15, 15))
        cv2.putText(temp, 'P1 Scores a Point !', (300, 360), cv2.FONT_HERSHEY_DUPLEX, 3, (185, 89, 200), 3, 1)
        cv2.imshow('Classic Pong Game 2P', temp)
        cv2.waitKey(2000)
        rounds += 1
        xPos = 640
        yPos = 400
        DeltaX = deltaxInitial
        DeltaY = deltayInitial

    if xPos <= -30:
        rounds += 1
        P2Score += 1
        temp = cv2.blur(background, (15, 15))
        cv2.putText(temp, 'P2 Scores a Point !', (300, 360), cv2.FONT_HERSHEY_DUPLEX, 3, (185, 89, 200), 3, 1)
        cv2.imshow('Classic Pong Game 2P', temp)
        cv2.waitKey(2000)
        xPos = 640
        yPos = 400
        DeltaX = deltaxInitial
        DeltaY = deltayInitial

    # sets the winning rules for the game
    if P1Score + P2Score == 3:
        ball = False
        background = cv2.blur(background, (20, 20))
        cv2.waitKey(1000)
        for i in range(0, 720, 10):
            background[i:i + 10, :] = (24, 34, 255)
            cv2.imshow('Classic Pong Game 2P', background)
            cv2.waitKey(10)
        cv2.putText(background, 'GAME OVER', (400, 360), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 255), 2)
        if P1Score > P2Score:
            cv2.putText(background, 'P1 WINS !!', (420, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 35), 2)

        else:
            cv2.putText(background, 'P2 WINS !!', (420, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 35), 2)
        cv2.putText(background, 'Press q twice to exit or game restarts in 5 seconds', (300, 550),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Classic Pong Game 2P', background)
        cv2.waitKey(5000)
        ball = True
        P1Score = 0
        P2Score = 0
        rounds = 0
    if cv2.waitKey(1) & 0xff == ord('q'):
        run = False
    cv2.imshow('Classic Pong Game 2P', background)
camera.release()
cv2.destroyAllWindows()
