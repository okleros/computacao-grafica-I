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
    x = int(min(max(p[0], 0), WIDTH - 1))
    y = int(min(max(p[1], 0), HEIGHT - 1))

    return (x, y)

def setpixel(p: tuple, color: Color) -> None:
    p = normalize(p)

    pygame_color = pygame.Color(int(color.r), int(color.g), int(color.b), int(color.a))
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

    for i in range(int(steps) + 1):
        x = xi + i * stepx
        y = yi + i * stepy

        if abs(stepx) == 1:
            yd = y - floor(y)

            setpixel((round(x), floor(y)), round((1 - yd) * color))
            setpixel((round(x), floor(y + 1)), round(yd * color))
        else:
            xd = x - floor(x)

            setpixel((floor(x), round(y)), round((1 - xd) * color))
            setpixel((floor(x + 1), round(y)), round(xd * color))

# bresenham currently not working for angled lines over 45 degrees
def bresenhamm(pi: tuple, pf: tuple, color: Color) -> None:
    xi = pi[0]
    xf = pf[0]
    yi = pi[1]
    yf = pf[1]

    dx = abs(xf - xi)
    dy = abs(yf - yi)

    p  = 2 * dy - dx

    dy2 = 2 * dy
    dx2 = 2 * (dy - dx)

    if xi > xf:
        x = xf
        y = yf
        x_end = xi
    
    else:
        x = xi
        y = yi
        x_end = xf

    setpixel((x, y), color)

    while x < x_end:
        x += 1

        if p < 0:
            p += dy2
        
        else:
            y += 1
            p += dx2

        setpixel((x, y), color)

def bresenham(p1, p2, color) -> None:
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    err = dx - dy
    
    while True:
        setpixel((x1, y1), color)
        
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def senoid(color: Color) -> None:
    xant = 0
    yant = (HEIGHT / 2) + (100 * sin(xant * 0.05))

    for x in range(1, WIDTH):
        y = int(HEIGHT / 2 + 100 * sin(x * 0.05))
        bresenham((xant, yant), (x, y), color)

        xant = x
        yant = y

def circle(c: tuple, r: number, color: Color) -> None:
    def plot(c: tuple, p: tuple, color: Color) -> None:
        xp = p[0]
        yp = p[1]
        xc = c[0]
        yc = c[1]

        setpixel((xc + x, yc + y), color)
        setpixel((xc - x, yc + y), color)
        setpixel((xc + x, yc - y), color)
        setpixel((xc - x, yc - y), color)
        setpixel((xc + y, yc + x), color)
        setpixel((xc - y, yc + x), color)
        setpixel((xc + y, yc - x), color)
        setpixel((xc - y, yc - x), color)

    x = 0
    y = r
    p = 3 - 2 * r

    while x < y:
        plot(c, (x, y), color)

        if p < 0:
            p = p + 4 * x + 6

        else:
            p = p + 4 * (x - y) + 10
            y -= 1

        x += 1

    if x == y:
        plot(c, (x, y), color)

# bresenham_ellipse not working
def bresenham_ellipse(center: tuple, a: int, b: int, color: Color) -> None:
    # Compute the initial values for x and y along the major axis
    x = a
    y = 0
    
    # Compute the error term for each step along the major axis
    d1 = b**2 - a**2*b + 0.25*a**2
    
    # Step along the major axis and plot the corresponding points
    while b**2*x > a**2*y:
        setpixel((x + center[0], y + center[1]), color)
        setpixel((-x + center[0], y + center[1]), color)
        setpixel((x + center[0], -y + center[1]), color)
        setpixel((-x + center[0], -y + center[1]), color)
        
        if d1 < 0:
            d1 += b**2*(2*x+3)
        else:
            d1 += b**2*(2*x+3) + a**2*(-2*y+2)
            y += 1
        
        x -= 1
    
    # Compute the initial values for x and y along the minor axis
    x = 0
    y = b
    
    # Compute the error term for each step along the minor axis
    d2 = a**2 - b**2*a + 0.25*b**2
    
    # Step along the minor axis and plot the corresponding points
    while a**2*y > b**2*x:
        setpixel((x + center[0], y + center[1]), color)
        setpixel((-x + center[0], y + center[1]), color)
        setpixel((x + center[0], -y + center[1]), color)
        setpixel((-x + center[0], -y + center[1]), color)
        
        if d2 < 0:
            d2 += a**2*(2*y+3)
        else:
            d2 += a**2*(2*y+3) + b**2*(-2*x+2)
            x += 1
        
        y -= 1

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

            bresenham((x, y), (prox, proy), color)

            x = prox
            y = proy

        bresenham((x, y), (self.__vertices[0][0], self.__vertices[0][1]), color)

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