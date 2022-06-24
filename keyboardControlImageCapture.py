import keyboardPressManipulating as kp
from djitellopy import tello
import time
import cv2
import numpy as np
import pygame

kp.init()
pygame.display.set_caption("Camera")
screen = pygame.display.set_mode((1280, 720))
me = tello.Tello()
me.connect()
print(me.get_battery())
running = True
global img

me.streamon()

def getKeyboardInput():
    leftright, forwardbackward, updown, yarnvelocity = 0, 0, 0, 0

    speed = 100

    if kp.getKey("a"):
        leftright = -speed
    elif kp.getKey("d"):
        leftright = speed

    if kp.getKey("UP"):
        updown = speed
    elif kp.getKey("DOWN"):
        updown = -speed

    if kp.getKey("w"):
        forwardbackward = speed
    elif kp.getKey("s"):
        forwardbackward = -speed

    if kp.getKey("e"):
        yarnvelocity = speed
    elif kp.getKey("q"):
        yarnvelocity = -speed
    if kp.getKey("x"):
        me.land()
        time.sleep(3)
    if kp.getKey("z"):
        me.takeoff()

    if kp.getKey('p'):
        cv2.imwrite(f'resources/images/{time.time()}.png',img)
        time.sleep(0.5)

    return [leftright, forwardbackward, updown, yarnvelocity]

def showbattery(img, me):
    if me.get_battery() < 30:
        cv2.putText(img, f'LOW BATTERY\\n: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
    else:
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


def imgInGame(img, running):
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame[::-1])
    screen.blit(frame, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


# me.takeoff()


while running:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])
    img = me.get_frame_read().frame
    showbattery(img, me)
    imgInGame(img, running)
