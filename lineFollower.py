import cv2
import numpy as np
from djitellopy import tello


cap = cv2.VideoCapture(0)
hsvVals = [35,0,136,140,75,255]
sensors = 3
theshold = 0.3
width, heigth = 480, 360

senstivity = 3
weights = [-25, -15, 0, 15, 25]
fSpeed = 15

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamon()
# me.takeoff()


def thesholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def getCoutours(imgThres, img):
    cx = 0
    contours, hieracrhy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        cv2.drawContours(img, contours, -1, (255, 0, 255), 7)
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv2.drawContours(img, contours, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    return cx


def getSensorOutput(imgThres, sensors):
    imgs = np.hsplit(imgThres, sensors)
    totalPixels = (img.shape[1] // sensors) * img.shape[0]
    senOut = []
    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > theshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
        cv2.imshow(str(x), im)
    print(senOut)
    return senOut


def sendCommands(senOut, cx):
    global curve
    lr = (cx - width // 2) // senstivity
    lr = int(np.clip(lr, -10, 10))
    if lr < 2 and lr > -2: lr = 0

    ##rotation
    if senOut == [1, 0, 0]: curve = weights[0]
    elif senOut == [1, 1, 0]: curve = weights[1]
    elif senOut == [0, 1, 0]: curve = weights[2]
    elif senOut == [0, 1, 1]: curve = weights[3]
    elif senOut == [0, 0, 1]: curve = weights[4]


    elif senOut == [0, 0, 0]: curve = weights[2]
    elif senOut == [1, 1, 1]: curve = weights[2]
    elif senOut == [1, 0, 1]: curve = weights[2]


    # me.send_rc_control(lr,fSpeed,0,curve)


while True:
    _, img = cap.read()
    # img = me.get_frame_read().frame
    img = cv2.resize(img, (width, heigth))
    img = cv2.flip(img, 0)

    imgThres = thesholding(img)
    cx = getCoutours(imgThres, img)
    senOut = getSensorOutput(imgThres, sensors)
    sendCommands(senOut, cx)
    cv2.imshow('out', img)
    cv2.imshow('path', imgThres)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        me.land()
        break
