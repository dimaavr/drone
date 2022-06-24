import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

cap = cv2.VideoCapture(0)

w, h = 360, 240
forwardbackwardRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0


def findFace(img):
    facesCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facesCascade.detectMultiScale(img_g, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        centerX = x + w // 2
        centerY = y + h // 2
        area = w * h
        cv2.circle(img, (centerX, centerY), 5, (255, 0, 0), cv2.FILLED)
        myFaceListC.append([centerX, centerY])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    forwardbackward = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if forwardbackwardRange[0] < area  and area < forwardbackwardRange[1]:
        forwardbackward = 0
    elif area > forwardbackwardRange[1]:
        forwardbackward = -20
    elif forwardbackwardRange[0] > area and area != 0:
        forwardbackward = 10
    if x == 0:
        speed = 0
        error = 0
    print(speed, forwardbackward)
    print('\n',area)
    me.send_rc_control(0, forwardbackward, 0, speed)
    return error





me.takeoff()
me.send_rc_control(10, 0, 40, 0)
time.sleep(4)
me.send_rc_control(0, 0, 0, 0)

while True:
    # _, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(me, info, w, pid, pError)
    # print("center", info[0], "area", info[1])
    cv2.imshow('cam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.streamoff()
        me.land()
        break
