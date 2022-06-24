import cv2
import numpy
import pygame


def showbattery(img, me):
    if me.get_battery() < 30:
        cv2.putText(img, f'LOW BATTERY\\n: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)
    else:
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
        cv2.putText(img, f'Battery: {me.get_battery()}%', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
