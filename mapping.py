import math
import cv2
import keyboardPressManipulating as kp
from djitellopy import tello
from time import sleep
import numpy as np



##params###
forwardSpeed = 16  # cm/s
angularSpeed = 360 / 10  # Deg/s
interval = 0.25
distanceInterval = forwardSpeed * interval
angularInterval = angularSpeed * interval
###########################################
x, y = 500, 500
angle = 0
yaw = 0

kp.init()

me = tello.Tello()
me.connect()
print(me.get_battery())


points = [(0, 0), (0, 0)]


def getKeyboardInput():
    leftright, forwardbackward, updown, yarnvelocity = 0, 0, 0, 0
    global x, y, yaw, angle
    speed = 17
    angularspeed = 50
    distance = 0

    if kp.getKey("a"):
        leftright = -speed
        distance = distanceInterval
        angle = -180
    elif kp.getKey("d"):
        leftright = speed
        distance = -distanceInterval
        angle = 180

    if kp.getKey("UP"):
        updown = speed

    elif kp.getKey("DOWN"):
        updown = -speed

    if kp.getKey("w"):
        forwardbackward = speed
        distance = distanceInterval
        angle = 270
    elif kp.getKey("s"):
        forwardbackward = -speed
        distance = -distanceInterval
        angle = -90

    if kp.getKey("e"):
        yarnvelocity = angularspeed
        yaw += angularInterval

    elif kp.getKey("q"):
        yarnvelocity = -angularspeed
        yaw -= angularInterval

    if kp.getKey("x"):
        me.land()
        sleep(3)
    if kp.getKey("z"):
        me.takeoff()


    sleep(interval)
    angle += yaw
    x += int(distance * math.cos(math.radians(angle)))
    y += int(distance * math.sin(math.radians(angle)))

    return [leftright, forwardbackward, updown, yarnvelocity, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

def showbattery(img, me):
    if me.get_battery() < 30:
        cv2.putText(img, f'LOW BATTERY\\n: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
    else:
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)



# me.takeoff()
while True:
    # img = me.get_frame_read().frame
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])
    imgRoute = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != values[4] or points[-1][1] != values[5]):
        points.append((values[4], values[5]))
    drawPoints(imgRoute, points)
    # showbattery(img, me)
    # imgInGame(img, running)
    cv2.imshow("map", imgRoute)
    cv2.waitKey(1)
