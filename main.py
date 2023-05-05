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

WIDTH = 512
HEIGHT = 512

LCI = 0XFA
COL = 0XFB
TEX = 0XFC

# Initialize Pygame and create the screen
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption for the window
pygame.display.set_caption("Computer Graphics is fun!")

def normalize(p: tuple) -> tuple:
    x = p[0]
    y = p[1]

    if x not in range(0, WIDTH) or y not in range(0, HEIGHT):
        return -1

    return (int(x), int(y))

def setpixel(p: tuple, color: Color) -> None:
    p = normalize(p)

    if p == -1:
        return

    pygame_color = pygame.Color(int(color.r), int(color.g), int(color.b), int(color.a))
    screen.set_at(p, pygame_color)

def getpixel(p: tuple, surf: pygame.surface = screen) -> Color:
    p = normalize(p)

    if p == -1:
        return -1

    pygame_color = surf.get_at(p)
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
BROWN = Color(150, 75, 0)

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
    def __init__(self, ver: list = []) -> None:
        self.__vertices = ver
        self.__color = None
        self.__tex = None

    def __repr__(self) -> list:
        return self.__vertices

    def addVertex(self, vertex: tuple) -> None:
        self.__vertices.append(vertex)

    def removeVertex(self, index: int) -> None:
        self.__vertices.remove(index)

    def insertVertex(self, vertex: tuple, index: int) -> None:
        self.__vertices.insert(index, vertex)

    def getVertices(self) -> list:
        return self.__vertices

    def rows(self) -> int:
        return len(self.__vertices)

    def columns(self) -> int:
        return len(self.__vertices[0])

    def moveX(self, amt: int = 0):
        for i in range(len(self.__vertices)):
            self.__vertices[i][0] += amt
    
    def moveY(self, amt: int = 0):
        for i in range(len(self.__vertices)):
            self.__vertices[i][1] += amt

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

    def scanline(self, arg: int) -> None:
        if arg == LCI:
            pass
        
        elif arg == COL:
            self.__scanlineColor()
        
        elif arg == TEX:
            pass
        
        else:
            raise ValueError("The arguments for scanline should be LCI for color interpolation, COL for color or TEX for texture.")


        
    def __scanlineColor(self) -> None:
        if self.__color is None:
            raise Exception("There is no color currently assigned to this Polygon, use Polygon.setColor(color) to assign a color and then try again")
        
        ver = self.__vertices
        poly = [ver[i][1] for i in range(len(ver))]

        ymin = min(poly)
        ymax = max(poly)

        for y in range(int(ymin), int(ymax)):
            itx = []
            pi = ver[0]

            for p in range(1, self.rows()):
                pf = ver[p]
                xi = intersec(y, (pi, pf))

                if xi >= 0:
                    itx.append(xi)

                pi = pf

            pf = ver[0]
            xi = intersec(y, (pi, pf))

            if xi >= 0:
                itx.append(xi)

            for i in range(0, len(itx), 2):
                try:
                    if itx[i] > itx[i + 1]:
                        itx[i], itx[i + 1] = itx[i + 1], itx[i]

                except:
                    continue

                for pixel in range(int(itx[i]) + 1, int(itx[i + 1])):
                    setpixel((pixel, y), self.__color)

    def setTexture(self, tex: pygame.surface):
        self.__tex = tex

    def setColor(self, color: Color):
        self.__color = color

def intersec(scan: int, seg: tuple) -> int:
    xi = seg[0][0]
    yi = seg[0][1]
    xf = seg[1][0]
    yf = seg[1][1]
    y = scan

    # Se o segmento é horizontal, não há intersecção
    if yi == yf:
        return -1

    # Troca os pontos para garantir que o ponto inicial está acima do final
    if yi > yf:
        xi, xf, yi, yf = xf, xi, yf, yi

    t = (y - yi) / (yf - yi)

    if t > 0 and t <= 1:
        x = xi + t * (xf - xi)

        return x

    else:
        return -1

def floodFill(p: tuple, color: Color) -> None:
    def isValid(p: tuple, icolor: Color) -> bool:
        p = normalize(p)

        if (p == -1 or getpixel(p) != icolor):
            return False

        return True

    p = normalize(p)
    
    if p == -1:
        return

    stack = deque()

    icolor = getpixel(p)

    stack.append(p)

    while stack:
        pixel = stack.pop()

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

def boundaryFill(p: tuple, bcolor: Color, color: Color) -> None:
    def isValid(p: tuple, bcolor: Color) -> bool:
        p = normalize(p)

        if (p == -1 or getpixel(p) == bcolor):
            return False

        return True

    p = normalize(p)

    if p == -1:
        return
    
    stack = deque()

    stack.append(p)

    while stack:
        pixel = stack.pop()

        x = pixel[0]
        y = pixel[1]

        if isValid(pixel, bcolor):
            setpixel(pixel, color)

            north = (x, y - 1)
            south = (x, y + 1)
            east = (x + 1, y)
            west = (x - 1, y)

            if isValid(north, bcolor):
                stack.append(north)

            if isValid(south, bcolor):
                stack.append(south)

            if isValid(east, bcolor):
                stack.append(east)

            if isValid(west, bcolor):
                stack.append(west)

def update():
    pygame.display.flip()

def clear():
    screen.fill((0, 0, 0))

def main():
    p1 = Polygon([[225, 225, GREEN], [WIDTH - 225, 225, RED], [WIDTH - 225, HEIGHT - 225, WHITE], [225, HEIGHT - 225, 225, BLACK]])
    p2 = Polygon([[225, 225, GREEN], [WIDTH - 225, 225, RED], [WIDTH - 225, HEIGHT - 225, WHITE], [225, HEIGHT - 225, 225, BLACK]])
    p3 = Polygon([[225, 225, GREEN], [WIDTH - 225, 225, RED], [WIDTH - 225, HEIGHT - 225, WHITE], [225, HEIGHT - 225, 225, BLACK]])
    p4 = Polygon([[225, 225, GREEN], [WIDTH - 225, 225, RED], [WIDTH - 225, HEIGHT - 225, WHITE], [225, HEIGHT - 225, 225, BLACK]])

    dice = pygame.image.load("C:\\Users\\gutem\\OneDrive\\Imagens\\Saved Pictures\\6545910.png").convert()

    p1.setColor(RED)
    p2.setColor(GREEN)
    p3.setColor(BLUE)
    p4.setColor(MAGENTA)

    for i in range(200):
        clear()
        
        p1.scanline(COL)
        p2.scanline(COL)
        p3.scanline(COL)
        p4.scanline(COL)
        
        p1.moveX(2)
        p1.moveY(2)
        p2.moveX(-2)
        p2.moveY(2)
        p3.moveX(2)
        p3.moveY(-2)
        p4.moveX(-2)
        p4.moveY(-2)
        
        update()
    
    # Update the screen
    update()

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
