import cv2
import numpy as np
from HandDetectionModule import MediapipeLandmark

# parameters
width = 1280
height = 720
paddleWidth = 150
paddleHeight = 20
paddleColor = (75, 153, 242)
lives = 3
deltaX = 10
deltaY = -10
xPos = 640
yPos = 400
level = 1
ball = True
ballRadius = 8
highScore = 0
bgColor = (30, 79, 24)
scoreColor = (149, 129, 252)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FPS, 30)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('Classic Pong Game', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Classic Pong Game', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

prevVal = 683
myScore = 0
handData = MediapipeLandmark(1)

while True:
    _, frame = camera.read()
    val = handData.Coordinates(frame)
    background = np.zeros([720, 1366, 3], dtype=np.uint8)
    background[:, :] = bgColor
    frameResize = cv2.resize(frame, (144, 81))
    frameResize = cv2.flip(frameResize, 1)
    background[639:720, 1222:1366] = frameResize
    if val == 0:
        val = prevVal
    else:
        prevVal = val
    cv2.rectangle(background, (1366 - (val - paddleWidth // 2), 720 - paddleHeight),
                  (1366 - (val + paddleWidth // 2), 720), paddleColor, -1)
    paddleRightCorner = (1366 - (val - paddleWidth // 2), 720 - paddleHeight)
    paddleLeftCorner = (1366 - (val + paddleWidth // 2), 720 - paddleHeight)
    if ball:
        cv2.circle(background, (xPos, yPos), ballRadius, (255, 255, 255), -1)
        xPos += deltaX
        yPos += deltaY
    if xPos >= 1360 or xPos <= 5:
        deltaX = -deltaX
    if yPos <= 10:
        deltaY = -deltaY
    if paddleRightCorner[0] >= xPos >= paddleLeftCorner[0]:
        if 695 <= yPos <= 710:
            deltaY = -deltaY
            myScore += 1
            if myScore % 5 == 0 and myScore >= 5:
                level += 1
                if deltaX < 0:
                    deltaX -= 2
                else:
                    deltaX += 2
                if deltaY < 0:
                    deltaY -= 1
                else:
                    deltaY += 1
    cv2.putText(background, 'Lives: ' + str(lives), (1200, 35), cv2.FONT_HERSHEY_PLAIN, 2, scoreColor, 2)
    cv2.putText(background, 'Level: ' + str(level), (1200, 68), cv2.FONT_HERSHEY_PLAIN, 2, scoreColor, 2)
    cv2.putText(background, 'Score: ' + str(myScore), (1200, 101), cv2.FONT_HERSHEY_PLAIN, 2, scoreColor, 2)
    if yPos >= 720:
        lives -= 1
        temp = cv2.blur(background, (15, 15))
        cv2.putText(temp, 'You Lost a Life !', (300, 360), cv2.FONT_HERSHEY_DUPLEX, 3, (185, 89, 200), 3, 1)
        cv2.imshow('Classic Pong Game', temp)
        cv2.waitKey(2000)
        xPos = 640
        yPos = 400
        if deltaY > 0:
            deltaY = -deltaY
    if lives == 0:
        ball = False
        deltaX = 10
        deltaY = -10
        level = 0
        background = cv2.blur(background, (20, 20))
        cv2.waitKey(1000)
        for i in range(0, 720, 10):
            background[i:i + 10, :] = (24, 34, 255)
            cv2.imshow('Classic Pong Game', background)
            cv2.waitKey(10)
        cv2.putText(background, 'GAME OVER', (400, 360), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 255), 2)
        cv2.putText(background, 'Your Score: ' + str(myScore), (420, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 35), 2)
        if myScore > highScore:
            highScore = myScore
        cv2.putText(background, 'HIGH SCORE: ' + str(highScore), (420, 480), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 56), 2)
        cv2.putText(background, 'Press q twice to exit or game restarts in 5 seconds', (300, 550),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Classic Pong Game', background)
        cv2.waitKey(5000)
        ball = True
        myScore = 0
        lives = 3
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.imshow('Classic Pong Game', background)
camera.release()
cv2.destroyAllWindows()
