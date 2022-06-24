import pygame
import cv2
import numpy as np


def init():
    pygame.init()
    win = pygame.display.set_mode((480, 480))


def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans


def main():
    if getKey("LEFT"):
        print("left pressed")


if __name__ == '__main__':
    init()
    cap = cv2.VideoCapture(0)
    while True:
        main()
        _, img = cap.read()
        cv2.imshow('cam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

