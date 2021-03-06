from djitellopy import tello
from time import sleep
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamoff()
me.streamon()
sleep(1)
# me.takeoff()


def showbattery(img, me):
    if me.get_battery() < 30:
        cv2.putText(img, f'LOW BATTERY\\n: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)
    else:
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


while True:
    img = me.get_frame_read().frame
    showbattery(img, me)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.streamoff()
        # me.land()
        break

cv2.destroyAllWindows()
