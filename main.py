import pygame, numpy as np
from collections import deque
from math import floor, ceil, sin, cos, pi
from numbers import Number as number
from time import sleep

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

WIDTH = 700
HEIGHT = 700

CENTER = (WIDTH / 2, HEIGHT / 2)

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

    if not (0 <= x < WIDTH) or not (0 <= y < HEIGHT):
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

def getpixelTex(p: tuple, surf: pygame.surface) -> Color:
    x = p[0] % 1
    y = p[1] % 1

    x = round(x * (surf.get_width() - 1))
    y = round(y * (surf.get_height() - 1))

    pygame_color = surf.get_at((x, y))

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
GREY = Color(0x51, 0x51, 0x51)

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

        setpixel((xc + xp, yc + yp), color)
        setpixel((xc - xp, yc + yp), color)
        setpixel((xc + xp, yc - yp), color)
        setpixel((xc - xp, yc - yp), color)
        setpixel((xc + yp, yc + xp), color)
        setpixel((xc - yp, yc + xp), color)
        setpixel((xc + yp, yc - xp), color)
        setpixel((xc - yp, yc - xp), color)

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

def ellipse(center: tuple, a: int, b: int, color: Color) -> None:
    # Compute the initial values for x and y along the major axis
    x = 0
    y = b

    xc = center[0]
    yc = center[1]

    a2 = a ** 2
    b2 = b ** 2

    da = 2 * a2
    db = 2 * b2

    # Compute the error term for each step along the major axis
    p = b2 - a2 * b + 0.25 * a2

    # Step along the major axis and plot the corresponding points
    while b2 * x <= a2 * y:
        setpixel((x + xc, y + yc), color)
        setpixel((-x + xc, y + yc), color)
        setpixel((x + xc, -y + yc), color)
        setpixel((-x + xc, -y + yc), color)

        x += 1
        p += db * x + b2

        if p >= 0:
            y -= 1
            p -= da * y

    # Compute the initial values for x and y along the minor axis
    x = a
    y = 0

    # Compute the error term for each step along the minor axis
    p = a2 - b2 * a + 0.25 * b2

    # Step along the minor axis and plot the corresponding points
    while a2 * y <= b2 * x:
        setpixel((x + center[0], y + center[1]), color)
        setpixel((-x + center[0], y + center[1]), color)
        setpixel((x + center[0], -y + center[1]), color)
        setpixel((-x + center[0], -y + center[1]), color)

        y += 1
        p += da * y + a2

        if p >= 0:
            x -= 1
            p -= db * x

class Polygon:
    def __init__(self, ver: list = []) -> None:
        self.__vertices = ver
        self.__color = None
        self.__tex = None
        self.__center = self.center()

    def center(self) -> tuple:
        xsum = ysum = 0

        num = len(self.__vertices)

        for i in range(num):
            xsum += self.__vertices[i][0]
            ysum += self.__vertices[i][1]

        x = xsum / num
        y = ysum / num

        return [x, y]

    def __repr__(self) -> list:
        return str(self.__vertices)

    def addVertex(self, vertex: tuple) -> None:
        self.__vertices.append(vertex)
        self.__center = self.center()

    def removeVertex(self, index: int) -> None:
        self.__vertices.remove(index)
        self.__center = self.center()

    def insertVertex(self, vertex: tuple, index: int) -> None:
        self.__vertices.insert(index, vertex)
        self.__center = self.center()

    def getVertices(self) -> list:
        return self.__vertices

    def getCenter(self) -> tuple:
        return self.__center

    def rows(self) -> int:
        return len(self.__vertices)

    def columns(self) -> int:
        return len(self.__vertices[0])

    def moveX(self, amt: int = 0) -> None:
        for i in range(len(self.__vertices)):
            self.__vertices[i][0] += amt

    def moveY(self, amt: int = 0) -> None:
        for i in range(len(self.__vertices)):
            self.__vertices[i][1] += amt
    
    def translate(self, p: tuple) -> None:
        tx = p[0]
        ty = p[1]

        points = self.__vertices

        R = np.array([[1, 0, tx],
                      [0, 1, ty],
                      [0, 0,  1]])

        for i in range(len(points)):
            P = np.array([points[i][0:2] + [1]]).transpose()

            M = (R @ P).transpose()

            self.__vertices[i][0] = M[0][0]
            self.__vertices[i][1] = M[0][1]

    def scale(self, scale: int, p: tuple = None) -> None:
        if p is None:
            p = self.center()

        self.translate([-p[0], -p[1]])

        sx = scale[0]
        sy = scale[1]

        points = self.__vertices

        R = np.array([[sx, 0, 0],
                      [0, sy, 0],
                      [0, 0, 1]])

        for i in range(len(points)):
            P = np.array([points[i][0:2] + [1]]).transpose()

            M = (R @ P).transpose()

            self.__vertices[i][0] = M[0][0]
            self.__vertices[i][1] = M[0][1]

        self.translate(p)

    def rotate(self, deg: float, p: tuple = None) -> None:
        if p is None:
            p = self.center()

        self.translate([-p[0], -p[1]])
        
        deg = deg * pi / 180

        R = np.array([[cos(deg), -sin(deg), 0],
                      [sin(deg),  cos(deg), 0],
                      [       0,         0, 1]])

        for i in range(len(self.__vertices)):
            
            P = np.array([self.__vertices[i][0:2] + [1]]).transpose()

            M = (R @ P).transpose()

            self.__vertices[i][0] = M[0][0]
            self.__vertices[i][1] = M[0][1]

        self.translate(p)

    def transform(self, M: np.array) -> None:
        for i in range(len(self.__vertices)):
            
            P = np.array([self.__vertices[i][0:2] + [1]]).transpose()

            T = (M @ P).transpose()

            self.__vertices[i][0] = T[0][0]
            self.__vertices[i][1] = T[0][1]

    def mapToWindow(self, w: tuple, v: tuple) -> None:
        vw = v[0]
        vh = v[1]

        wxi = w[0][0]
        wxf = w[1][0]
        wyi = w[0][1]
        wyf = w[1][1]

        M = np.array([[vw / (wxf - wxi), 0, (1 - wxi * vw / (wxf - wxi))],
                   [0, vh / (wyf - wyi), (1 - wyi * vh / (wyf - wyi))],
                   [0,                0,                            1]])

        self.transform(M)

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

    def scanline(self, arg: int) -> None:
        if arg == LCI:
            self.__scanlineLerp()

        elif arg == COL:
            self.__scanlineColor()

        elif arg == TEX:
            self.__scanlineTex()

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
                xi = intersec(y, (pi, pf))[0]

                if xi >= 0:
                    itx.append(xi)

                pi = pf

            pf = ver[0]
            xi = intersec(y, (pi, pf))[0]

            if xi >= 0:
                itx.append(xi)

            for i in range(0, len(itx), 2):
                try:
                    if itx[i] > itx[i + 1]:
                        itx[i], itx[i + 1] = itx[i + 1], itx[i]

                except:
                    continue

                for pixel in range(round(itx[i]) + 1, round(itx[i + 1])):
                    setpixel((pixel, y), self.__color)

    def __scanlineLerp(self) -> None:
        ver = self.__vertices
        poly = [ver[i][1] for i in range(len(ver))]

        ymin = min(poly)
        ymax = max(poly)

        for y in range(int(ymin), int(ymax)):            
            pi = ver[0]
            itx = []

            for p in range(1, self.rows()):
                pf = ver[p]
                xi = intersec(y, (pi, pf))

                if xi[0] >= 0:
                    itx.append(xi)

                pi = pf

            pf = ver[0]
            xi = intersec(y, (pi, pf))

            if xi[0] >= 0:
                itx.append(xi)

            for i in range(0, len(itx), 2):
                passo = 1
                
                try:
                    if itx[i][0] > itx[i + 1][0]:
                        passo = -1
                except:
                    break
                    #itx.append(itx[0])
                    #passo = 1

                k = 0

                colori = itx[i][1]
                colorf = itx[i + 1][1]
                
                passos = abs(itx[i][0] - itx[i + 1][0])

                for pixel in range(round(itx[i][0]), round(itx[i + 1][0]), passo):
                    t = k / passos

                    setpixel((pixel, y), lerpColor(colori, colorf, t))
                    k += 1

    def __scanlineTex(self) -> None:
        ver = self.__vertices
        poly = [ver[i][1] for i in range(len(ver))]

        ymin = min(poly)
        ymax = max(poly)

        for y in range(int(ymin), int(ymax)):
            itx = []
            pi = ver[0]
            passo = 1

            for p in range(1, self.rows()):
                pf = ver[p]
                xi = intersec(y, (pi, pf))

                if xi[0] >= 0:
                    itx.append(xi)

                pi = pf

            pf = ver[0]
            xi = intersec(y, (pi, pf))

            if xi[0] >= 0:
                itx.append(xi)

            for i in range(0, len(itx), 2):
                try:
                    if itx[i][0] > itx[i + 1][0]:
                        passo = -1

                except:
                    continue

                k = 0
                passos = abs(itx[i][0] - itx[i + 1][0])

                for pixel in range(round(itx[i][0]), round(itx[i + 1][0]), passo):
                    t = k / passos

                    tx = lerp(itx[i][2][0], itx[i + 1][2][0], t)
                    ty = lerp(itx[i][2][1], itx[i + 1][2][1], t)

                    setpixel((pixel, y), getpixelTex((tx, ty), self.__tex))
                    k += 1

    def setTexture(self, tex: pygame.surface) -> None:
        self.__tex = tex

    def setColor(self, color: Color) -> None:
        self.__color = color

def intersec(scan: int, seg: tuple) -> int:
    trocou = False

    xi = seg[0][0]
    yi = seg[0][1]

    txi = seg[0][3][0]
    tyi = seg[0][3][1]

    xf = seg[1][0]
    yf = seg[1][1]

    txf = seg[1][3][0]
    tyf = seg[1][3][1]

    colori = seg[0][2]
    colorf = seg[1][2]

    y = scan

    # Se o segmento é horizontal, não há intersecção
    if yi == yf:
        return [-1, -1, -1]

    # Troca os pontos para garantir que o ponto inicial está acima do final
    if yi > yf:
        xi, xf, yi, yf = xf, xi, yf, yi
        trocou = True

    t = (y - yi) / (yf - yi)

    if t >= 0 and t < 1:
        x = lerp(xi, xf, t)

        if trocou:
            tx = lerp(txf, txi, t)
            ty = lerp(tyf, tyi, t)

            return [x, lerpColor(colorf, colori, t), [tx, ty]]
        else:
            tx = lerp(txi, txf, t)
            ty = lerp(tyi, tyf, t)

            return [x, lerpColor(colori, colorf, t), [tx, ty]]

    else:
        return [-1, -1, -1]

lerp = lambda a, b, t: (1 - t) * a + t * b

lerpColor = lambda c1, c2, t: round(Color(lerp(c1.r, c2.r, t), lerp(c1.g, c2.g, t), lerp(c1.b, c2.b, t)))

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
    j = [[-1, -1], [2, 1]]
    v = [150, 100]
    v2 = [75, 50]

    p1 = Polygon([[300, 300, CYAN, [0, 0]], [WIDTH - 300, 300, MAGENTA, [1, 0]], [WIDTH - 300, HEIGHT - 300, YELLOW, [1, 1]], [300, HEIGHT - 300, WHITE, [0, 1]]])
    p2 = Polygon([[WIDTH / 2, 0, RED, [2, 0]], [WIDTH, HEIGHT, GREEN, [4, 4]], [0, HEIGHT, BLUE, [0, 4]]])
    p3 = Polygon([[-0.5, -0.5, RED, [0, 0]], [0.5, -0.5, GREEN, [1, 0]], [0.5, 0.5, BLUE, [1, 1]], [-0.5, 0.5, YELLOW, [0, 1]]])
    p4 = Polygon([[-0.5, -0.5, RED, [0, 0]], [0.5, -0.5, GREEN, [1, 0]], [0.5, 0.5, BLUE, [1, 1]], [-0.5, 0.5, YELLOW, [0, 1]]])

    sam = pygame.image.load("res/Sam_3.png").convert()
    dice = pygame.image.load("res/6545910.png").convert()

    p1.setTexture(dice)
    p1.setColor(YELLOW)
    p3.setColor(BROWN)
    p3.setTexture(sam)
    p4.setTexture(dice)

    p3.mapToWindow(j, v)
    p4.mapToWindow(j, v2)

    i = 0
    running = True
    while running:
        clear()
        #p1.scale([1.1, 1.1])
        #p3.scale([1.1, 1.1])
        p1.rotate(5)
        #p3.rotate(5)
        #p4.rotate(5)
        p1.scanline(COL)
        #p3.scanline(TEX)
        #p4.scanline(TEX)
        #p1.draw(GREEN)
        #p3.draw(MAGENTA)
        update()
        #sleep(0.02)
        #i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.png")
                running = False

    # Run the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.png")
                running = False

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
