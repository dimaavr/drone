import keyboardPressManipulating as kp
from djitellopy import tello
import time
import cv2
import numpy as np
import pygame
import pandas as pd
from pyzbar import pyzbar

kp.init()
pygame.display.set_caption("Camera")
screen = pygame.display.set_mode((1280, 720))
me = tello.Tello()
me.connect()
print(me.get_battery())
running = True
global img

cols = ['NAME', 'AMOUNT', 'COUNTRY']
df_good = pd.DataFrame()

me.streamon()


def getKeyboardInput():
    leftright, forwardbackward, updown, yarnvelocity = 0, 0, 0, 0

    speed = 50

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
        cv2.imwrite(f'resources/images{time.time()}.jpg', img)
        time.sleep(0.5)

    return [leftright, forwardbackward, updown, yarnvelocity]


def showbattery(img, me):
    if me.get_battery() < 30:
        cv2.putText(img, f'LOW BATTERY\\n: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
    else:
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


def imgInGame(img, running):
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame[::-1])
    screen.blit(frame, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            me.streamoff()
            # me.land()
            running = False


def getQr(img):
    all_data = []
    qrcodes = pyzbar.decode(img)  # Создается список найденных кодов
    for qrcode in qrcodes:
        qrcodeData = qrcode.data.decode('utf-8')
        if qrcode.type == 'QRCODE' and 'name=' in qrcodeData:  # проверяем тип кода и проверяем вхождение строки 'name='
            all_data.append(qrcodeData.split('&'))
    return all_data



while running:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])
    img = me.get_frame_read().frame
    showbattery(img, me)

    data = getQr(img)
    am = False
    if data != []:
        if not df_good.empty:
            for i, j in df_good.iterrows():
                if list(j.array) == data[0] and am == False:
                    am = True
            if am == False:
                for cell in data:  # если на изображении больше 1 кода
                    df_good = df_good.append(pd.DataFrame([cell], columns=cols))
                    cv2.imwrite(f'resources/images{time.time()}.png', img)
        else:
            for cell in data:  # если на изображении больше 1 кода
                df_good = df_good.append(pd.DataFrame([cell], columns=cols))
                cv2.imwrite(f'resources/images{time.time()}.png', img)
    df_good.reset_index(drop=True, inplace=True)

    imgInGame(img, running)
    print(df_good)
