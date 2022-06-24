import keyboardPressManipulating as kp
from djitellopy import tello
from time import sleep

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())


def getKeyboardInput():
    leftright, forwardbackward, updown, yarnvelocity = 0, 0, 0, 0

    speed = 25

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

    if kp.getKey("x"): me.land()
    if kp.getKey("z"): me.takeoff()

    return [leftright, forwardbackward, updown, yarnvelocity]


# me.takeoff()
while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])
    sleep(0.01)
