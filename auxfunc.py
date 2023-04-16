from color import Color
import pygame
from collections import deque
from math import floor

def setpixel(p: tuple, color: Color) -> None:
    pygame_color = pygame.Color(color.r, color.g, color.b, color.a)
    screen.set_at(p, pygame_color)

def getpixel(p: tuple) -> Color:
    pygame_color = screen.get_at(p)
    return Color(pygame_color.r, pygame_color.g, pygame_color.b, pygame_color.a)

def DDA(pi: tuple, pf: tuple, color: Color) -> None:
    xi = pi[0]
    yi = pi[1]
    xf = pf[0]
    yf = pf[1]

    dx = xf - xi
    dy = yf - yi

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        setpixel(pi, color)
        return
    
    stepx = dx / steps
    stepy = dy / steps

    for i in range(round(steps) + 1):
        x = round(xi + i * stepx)
        y = round(yi + i * stepy)

        setpixel((x, y), color)

def DDAAA(pi: tuple, pf: tuple, color: Color) -> None:
    xi = pi[0]
    yi = pi[1]
    xf = pf[0]
    yf = pf[1]

    dx = xf - xi
    dy = yf - yi

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        setpixel(pi, color)
        return
    
    stepx = dx / steps
    stepy = dy / steps

    for i in range(round(steps) + 1):
        x = xi + i * stepx
        y = yi + i * stepy

        if abs(stepx) == 1:
            yd = y - floor(y)

            setpixel((round(x), floor(y)), round(1 - yd) * color)
            setpixel((round(x), floor(y + 1)), round(yd * color))
        else:
            xd = x - floor(x)

            setpixel((floor(x), round(y)), round((1 - xd) * color))
            setpixel((floor(x + 1), round(y)), round(xd * color))

def floodFill(p: tuple, color: Color) -> None:
    
    def isValid(p: tuple, icolor: Color) -> bool:
        if (p[0] < 0):
            return False

        if (p[1] < 0):
            return False

        if (p[0] > WIDTH - 1):
            return False

        if (p[1] > HEIGHT - 1):
            return False

        if (getpixel(p) != icolor):
            return False

        return True

    stack = deque()

    icolor = getpixel(p)
    #print(p)

    stack.append(p)

    while stack:
        pixel = stack.pop()
        #print(pixel)

        x = pixel[0]
        y = pixel[1]

        if isValid(pixel, icolor):
            setpixel(pixel, color)
            #print("pixel set at ", pixel)

            north = (x, y - 1)
            south = (x, y + 1)
            east = (x + 1, y)
            west = (x - 1, y)

            if isValid(north, icolor):
                stack.append(north)

            if isValid(south, icolor):
                stack.append(south)

            if isValid(east, icolor):
                stack.append(east)

            if isValid(west, icolor):
                stack.append(west)
