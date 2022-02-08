from djitellopy import tello
from time import sleep
import cv2
#
# me = tello.Tello()
# me.connect()
# print(me.get_battery())
#
# me.takeoff()
# me.send_rc_control(0, 30, 10, 0)
# sleep(5)
# me.flip("b")
# sleep(1)
# me.flip("l")
# me.send_rc_control(0, 0, 0, 0)
# sleep(2)
# me.send_rc_control(0, 0, 0, 100)
# sleep(2)
# me.send_rc_control(0, 30, 0, 0)
# sleep(2)
# me.send_rc_control(0, 0, 0, 0)
# me.land()

me = tello.Tello()
me.connect()

print(me.get_battery())

me.streamon()


while True:

    img = me.get_frame_read().frame
    # img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

