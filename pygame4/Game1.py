from sys import exit
from time import sleep
import pygame
from threading import Thread
from pygame.locals import *

s = open('space.txt')
pat = int(s.readline().split(':')[1])
checkpoint = 0
spaces = [[], []]
isDown = True
canLeft = True
size = [0, 600 - pat]
ss = s.readline().split(':')[1].split(",")
finish = pygame.Rect(800 - pat - int(ss[0]), 600 - pat - int(ss[1]), pat, pat)
rect = None
win = None


def checkDown():
    global isDown
    global canLeft
    while rect[1] < 600 - pat:
        canMove = True

        sleep(0.5)
        canLeft = False

        if rect[1] < 600 - pat:
            for space in spaces[checkpoint]:
                if rect[1] + pat == space.top and rect[0] == space.left:
                    canMove = False
            if canMove:
                pygame.draw.rect(win, (255, 255, 255), rect)
                drawLines()
                pygame.display.update()
                rect.move_ip(0, pat)
                pygame.draw.rect(win, (100, 100, 100), rect)

                drawLines()
                pygame.display.update()
            else:
                break
    canLeft = True
    isDown = True
    sleep(0.35)


def drawFinish():
    global finish
    pygame.draw.rect(win, (0, 0, 255), finish)


def drawspace():
    global rect
    global checkpoint
    pygame.display.set_caption('第%d關' % (checkpoint+1))
    win.fill((255, 255, 255))
    if rect is None:
        rect = pygame.Rect(size[0], size[1], pat, pat)
    else:
        rect.move_ip(pat - 800, 0)
    pygame.draw.rect(win, (100, 100, 100), rect)
    for space in spaces[checkpoint]:
        pygame.draw.rect(win, (255, 0, 0), space)
    drawFinish()
    drawLines()
    pygame.display.update()


def space():
    # rows = open('space.txt').read().split('\n')
    i = checkpoint
    global finish

    for row in s.readlines():
        row = row.replace('\n', '')
        if row.__contains__(':'):
            continue
        if row.__contains__('='):
            i += 1
            spaces.append(list())
            continue
        row = row.split(",")
        rect_local = pygame.Rect(int(row[0]), 600 - pat - int(row[1]), pat, pat)
        spaces[i].append(rect_local)
    drawspace()


def drawLines():
    for i in range(pat, 800, pat):
        pygame.draw.aaline(win, (0, 0, 0), (i, 0), (i, 600), 2)

    for i in range(pat, 600, pat):
        pygame.draw.aaline(win, (0, 0, 0), (0, i), (800, i), 2)


keys = [K_RIGHT, K_LEFT, K_UP, K_DOWN]


def checkKey(event):
    if keys.__contains__(event.key):
        global isDown
        global canLeft
        global checkpoint

        canMove = True
        if event.key == K_RIGHT and canLeft:
            pygame.draw.rect(win, (255, 255, 255), rect)
            if rect[0] < 800 - pat:
                for space in spaces[checkpoint]:
                    if rect[0] + pat == space.left and rect[1] == space.top:
                        canMove = False
                        break
                if canMove:
                    rect.move_ip(pat, 0)
        elif event.key == K_LEFT and canLeft:
            pygame.draw.rect(win, (255, 255, 255), rect)
            if rect[0] > 0:
                for space in spaces[checkpoint]:
                    if rect[0] - pat == space.left and rect[1] == space.top:
                        canMove = False
                        break
                if canMove:
                    rect.move_ip(-pat, 0)
        elif event.key == K_UP and isDown:
            pygame.draw.rect(win, (255, 255, 255), rect)
            if rect[1] > 0:
                for space in spaces[checkpoint]:
                    if rect[1] - pat == space.top and rect[0] == space.left:
                        canMove = False
                        break
                if canMove:
                    rect.move_ip(0, -pat)
        pygame.draw.rect(win, (100, 100, 100), rect)
        drawLines()
        pygame.display.update()

        # print(rect[1] + 50, spaces[0].top)
        # print('--------------')
        # print(rect[0], spaces[0].left)
        # print("==============")
        if rect[1] < 600 - pat:
            Thread(target=checkDown).start()
            isDown = False
        if rect[0] == finish.left and rect[1] == finish.top:
            if checkpoint == len(spaces) - 2:
                finish_raw_pic = pygame.image.load('./遊戲結束.jpg').convert()
                finish_pic = pygame.transform.scale(finish_raw_pic, win.get_size())
                win.blit(finish_pic, win.get_rect())
                pygame.display.update()
                sleep(1.5)
                pygame.quit()
                exit()
            else:
                checkpoint += 1
                drawspace()
    elif event.key == K_ESCAPE:
        pygame.quit()
        exit()


def main():
    pygame.init()

    global win
    win = pygame.display.set_mode((800, 600))

    space()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                checkKey(event)
