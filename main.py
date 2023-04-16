import pygame
from collections import deque
from math import floor, ceil, sin, cos
from numbers import Number as number

# Define the Color class
class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
        self.r = min(max(r, 0), 255)
        self.g = min(max(g, 0), 255)
        self.b = min(max(b, 0), 255)
        self.a = min(max(a, 0), 255)

    def __repr__(self) -> str:
        return f"[{self.r}, {self.g}, {self.b}, {self.a}]"

    def __mul__(self, scalar: number):
        p = Color(self.r * scalar, self.g * scalar, self.b * scalar, self.a * scalar)

        return p

    def __rmul__(self, scalar: number):
        p = Color(self.r * scalar, self.g * scalar, self.b * scalar, self.a * scalar)

        return p

    def __round__(self):
        p = Color(round(self.r), round(self.g), round(self.b), round(self.a))

        return p

    def __floor__(self):
        p = Color(floor(self.r), floor(self.g), floor(self.b), round(self.a))

        return p
    
    def __eq__(self, other):
        if self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a:
            return True

        return False

WIDTH = HEIGHT = 700

# Initialize Pygame and create the screen
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption for the window
pygame.display.set_caption("Computer Graphics is fun!")

def normalize(p: tuple) -> tuple:
    x = min(max(p[0], 0), WIDTH - 1)
    y = min(max(p[1], 0), HEIGHT - 1)

    return (x, y)

def setpixel(p: tuple, color: Color) -> None:
    p = normalize(p)

    pygame_color = pygame.Color(color.r, color.g, color.b, color.a)
    screen.set_at(p, pygame_color)

def getpixel(p: tuple) -> Color:
    p = normalize(p)

    pygame_color = screen.get_at(p)
    return Color(pygame_color.r, pygame_color.g, pygame_color.b, pygame_color.a)

# Default useful color macros
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW = Color(255, 255, 0)

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

# bresenham currently not working for angled lines over 45 degrees
def bresenham(pi: tuple, pf: tuple, color: Color) -> None:
    trocou = False

    xi = pi[0]
    xf = pf[0]
    yi = pi[1]
    yf = pf[1]

    dx = xf - xi
    dy = yf - yi

    if dy > dx:
        aux = dx
        dx = dy
        dy = aux
        aux = xi
        xi = yi
        yi = aux

        trocou = True

    dx2 = 2 * dx
    dy2 = 2 * dy

    p  = - dx + dy2

    x = round(xi)
    y = round(yi)

    print(x, y)

    for i in range(round(abs(dx)) + 1):
        if trocou:
            setpixel((x, y), color)

        else:
            setpixel((y, x), color)

        x += 1

        if p > 0:
            y += 1

            p = p - dx2 + dy2

        else:
            p += dy2

def senoid(color: Color) -> None:
    xant = 0
    yant = (HEIGHT / 2) + (100 * sin(xant * 0.05))

    for x in range(1, WIDTH):
        y = HEIGHT / 2 + 100 * sin(x * 0.05)
        DDAAA((xant, yant), (x, y), color)

        xant = x
        yant = y

class Polygon:
    __vertices = None

    def __init__(self) -> None:
        self.__vertices = []

    def __repr__(self) -> list:
        return self.__vertices

    def addVertex(self, vertex: tuple) -> None:
        self.__vertices.append(vertex)

    def removeVertex(self, index: int) -> None:
        self.__vertices.remove(index)

    def insertVertex(self, vertex: tuple, index: int) -> None:
        self.__vertices.insert(index, vertex)

    def getVertices(self) -> None:
        for i in range(len(self.__vertices)):
            print(f"[{self.__vertices[0]}, {self.__vertices[1]}]\n")

    def draw(self, color: Color) -> None:
        x = self.__vertices[0][0]
        y = self.__vertices[0][1]

        for i in range(1, len(self.__vertices)):
            prox = self.__vertices[i][0]
            proy = self.__vertices[i][1]

            DDA((x, y), (prox, proy), color)

            x = prox
            y = proy

        DDA((x, y), (self.__vertices[0][0], self.__vertices[0][1]), color)

def floodFill(p: tuple, color: Color) -> None:
    p = normalize(p)
    
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


def main():
    pol = Polygon()

    pol.addVertex((100, 200))
    pol.addVertex((WIDTH / 2, 50))
    pol.addVertex((WIDTH - 100, 200))
    pol.addVertex((WIDTH - 180, HEIGHT - 180))
    pol.addVertex((180, HEIGHT - 180))

    pol.draw(YELLOW)
    senoid(RED)

    setpixel((-5, -5), GREEN)
    setpixel((800, 800), MAGENTA)

    pygame.display.flip()

    floodFill((int(WIDTH / 2), int(HEIGHT / 2) + 150), CYAN)
    floodFill((int(WIDTH / 2), int(HEIGHT)), MAGENTA)

    # Update the screen
    pygame.display.flip()

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.png")
                running = False
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()