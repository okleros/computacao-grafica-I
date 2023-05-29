import pygame, numpy as np
from math import floor, sin, cos, pi, isnan
from copy import deepcopy

# Define the Color class
class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
        self.r = min(max(r, 0), 255)
        self.g = min(max(g, 0), 255)
        self.b = min(max(b, 0), 255)
        self.a = min(max(a, 0), 255)

    def __repr__(self) -> str:
        return f"[{self.r}, {self.g}, {self.b}, {self.a}]"

    def __mul__(self, scalar: float):
        p = Color(self.r * scalar, self.g * scalar, self.b * scalar, self.a * scalar)

        return p

    def __rmul__(self, scalar: float):
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

LCI = 0XFA
COL = 0XFB
TEX = 0XFC

def normalize(screen, p: tuple) -> tuple:
    x = p[0]
    y = p[1]

    if not (0 <= x < len(screen)) or not (0 <= y < len(screen[0])):
        return -1

    return (int(x), int(y))

def setpixel(screen, p: tuple, color: Color) -> None:
    p = normalize(screen, p)

    if p == -1:
        return

    pygame_color = pygame.Color(int(color.r), int(color.g), int(color.b), int(color.a))
    screen[p[0]][p[1]] = pygame_color

def getpixel(surf, p: tuple) -> Color:
    p = normalize(surf, p)

    if p == -1:
        return -1

    pygame_color = pygame.Color(surf[p[0], p[1]] << 8 | 0xff)
    return Color(pygame_color.r, pygame_color.g, pygame_color.b, pygame_color.a)

def getpixelTex(tex, p: tuple) -> Color:
    x = p[0] % 1
    y = p[1] % 1

    x = floor(x * (len(tex)))
    y = floor(y * (len(tex[0])))

    pygame_color = pygame.Color(tex[x, y] << 8 | 0xFF)

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
GREY = Color(0xB0, 0xB0, 0xB0)
NEON_GREEN = Color(57, 255, 20)
NEON_RED = Color(255, 49, 49)
NEON_YELLOW = Color(255, 240, 31)
NEON_ORANGE = Color(255, 95, 31)
ORANGE = Color(255, 165, 0)
MAGENTA_DARK = Color(118, 0, 169)
CREAM = Color(255, 253, 208)
PINK = Color(255, 203, 209)
VIOLET = Color(79, 47, 79)

def DDA(screen, pi: tuple, pf: tuple, color: Color) -> None:
    xi = pi[0]
    yi = pi[1]
    xf = pf[0]
    yf = pf[1]

    dx = xf - xi
    dy = yf - yi

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        setpixel(screen, pi, color)
        return

    stepx = dx / steps
    stepy = dy / steps

    for i in range(round(steps) + 1):
        x = round(xi + i * stepx)
        y = round(yi + i * stepy)

        setpixel(screen, (x, y), color)

def DDAAA(screen, pi: tuple, pf: tuple, color: Color) -> None:
    xi = pi[0]
    yi = pi[1]
    xf = pf[0]
    yf = pf[1]

    dx = xf - xi
    dy = yf - yi

    steps = max(abs(dx), abs(dy))

    if steps == 0:
        setpixel(screen, pi, color)
        return

    stepx = dx / steps
    stepy = dy / steps

    for i in range(int(steps) + 1):
        x = xi + i * stepx
        y = yi + i * stepy

        if abs(stepx) == 1:
            yd = y - floor(y)

            setpixel(screen, (round(x), floor(y)), round((1 - yd) * color))
            setpixel(screen, (round(x), floor(y + 1)), round(yd * color))
        else:
            xd = x - floor(x)

            setpixel(screen, (floor(x), round(y)), round((1 - xd) * color))
            setpixel(screen, (floor(x + 1), round(y)), round(xd * color))

def bresenham(screen, p1, p2, color) -> None:
    x1 = round(p1[0])
    x2 = round(p2[0])
    y1 = round(p1[1])
    y2 = round(p2[1])

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    err = dx - dy

    while True:
        setpixel(screen, (x1, y1), color)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

def senoid(screen, color: Color) -> None:
    xant = 0
    yant = (HEIGHT / 2) + (100 * sin(xant * 0.05))

    for x in range(1, WIDTH):
        y = int(HEIGHT / 2 + 100 * sin(x * 0.05))
        bresenham(screen, (xant, yant), (x, y), color)

        xant = x
        yant = y

def circle(screen, c: tuple, r: float, color: Color) -> None:
    def plot(c: tuple, p: tuple, color: Color) -> None:
        xp = p[0]
        yp = p[1]
        xc = c[0]
        yc = c[1]

        setpixel(screen, (xc + xp, yc + yp), color)
        update()
        setpixel(screen, (xc - xp, yc + yp), color)
        update()
        setpixel(screen, (xc + xp, yc - yp), color)
        update()
        setpixel(screen, (xc - xp, yc - yp), color)
        update()
        setpixel(screen, (xc + yp, yc + xp), color)
        update()
        setpixel(screen, (xc - yp, yc + xp), color)
        update()
        setpixel(screen, (xc + yp, yc - xp), color)
        update()
        setpixel(screen, (xc - yp, yc - xp), color)
        update()

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

def ellipse(screen, center: tuple, a: int, b: int, color: Color) -> None:
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
        setpixel(screen, (x + xc, y + yc), color)
        update()
        setpixel(screen, (-x + xc, y + yc), color)
        update()
        setpixel(screen, (x + xc, -y + yc), color)
        update()
        setpixel(screen, (-x + xc, -y + yc), color)
        update()

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
        setpixel(screen, (x + center[0], y + center[1]), color)
        update()
        setpixel(screen, (-x + center[0], y + center[1]), color)
        update()
        setpixel(screen, (x + center[0], -y + center[1]), color)
        update()
        setpixel(screen, (-x + center[0], -y + center[1]), color)
        update()

        y += 1
        p += da * y + a2

        if p >= 0:
            x -= 1
            p -= db * x

class Polygon:
    def __init__(self, ver: list = []) -> None:
        self.__vertices = ver
        self.__clipped = None
        self.__color = None
        self.__tex = None
        self.__center = self.center()

    def __repr__(self) -> list:
        return str(self.__vertices)

    def clip(self, clipping_polygon):
        subject_polygon = self.__vertices
        
        def compute_intersection(edge_1, edge_2):
                trocou = False

                x1, y1 = edge_1[0]
                x2, y2 = edge_1[1]

                x3, y3 = edge_2[0][:2]
                x4, y4 = edge_2[1][:2]

                x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
                y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

                if y3 > y4:
                    x3, y3, x4, y4 = x4, y4, x3, y3
                    trocou = True

                if y3 == y4:
                    t = (x - x4) / (x3 - x4)

                else:
                    t = (y - y4) / (y3 - y4)

                if not trocou and y3 != y4:
                    return [x, y, lerpColor(edge_2[0][2], edge_2[1][2], t), [lerp(edge_2[0][3][0], edge_2[1][3][0], t), lerp(edge_2[0][3][1], edge_2[1][3][1], 1 - t)]]

                else:
                    return [x, y, lerpColor(edge_2[0][2], edge_2[1][2], t), [lerp(edge_2[0][3][0], edge_2[1][3][0], 1 - t), lerp(edge_2[0][3][1], edge_2[1][3][1], t)]]

        def inside(point, edge):
            x, y = point[:2]
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            return (x2 - x1) * (y - y1) > (y2 - y1) * (x - x1)

        def clip_polygon(input_polygon, clip_edge):
            output_polygon = []
            s = input_polygon[-1]

            for e in input_polygon:
                if inside(e, clip_edge):
                    if not inside(s, clip_edge):
                        output_polygon.append(compute_intersection(clip_edge, [s, e]))
                    output_polygon.append(e)

                elif inside(s, clip_edge):
                    output_polygon.append(compute_intersection(clip_edge, [s, e]))
                s = e

            self.__clipped = output_polygon
            return output_polygon

        clipped_polygon = subject_polygon

        for clip_edge in zip(clipping_polygon, clipping_polygon[1:] + [clipping_polygon[0]]):
            if clipped_polygon:
                clipped_polygon = clip_polygon(clipped_polygon, clip_edge)
            
            else:
                clipped_polygon = []

        return clipped_polygon

    def center(self) -> tuple:
        xsum = ysum = 0

        num = len(self.__vertices)

        for i in range(num):
            xsum += self.__vertices[i][0]
            ysum += self.__vertices[i][1]

        x = xsum / num
        y = ysum / num

        self.__center = [x, y]

        return self.__center

    def copy(self):
        return deepcopy(self)

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
        self.translate([amt, 0])

    def moveY(self, amt: int = 0) -> None:
        self.translate([0, amt])
    
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
        vxi = v[0][0]
        vyi = v[0][1]
        vxf = v[1][0]
        vyf = v[1][1]

        wxi = w[0][0]
        wxf = w[1][0]
        wyi = w[0][1]
        wyf = w[1][1]

        a = (vxf - vxi) / (wxf - wxi)
        b = (vyf - vyi) / (wyf - wyi)

        M = np.array([[a, 0, vxi - a * wxi],
                      [0, b, vyi - b * wyi],
                      [0, 0,             1]])

        self.transform(M)

        return self.__vertices

    def draw(self, screen, color: Color) -> None:
        if self.__clipped is not None:
            ver = self.__clipped

        else:
            ver = self.__vertices

        if not ver:
            return

        x = ver[0][0]
        y = ver[0][1]

        for i in range(1, len(ver)):
            prox = ver[i][0]
            proy = ver[i][1]

            bresenham(screen, (x, y), (prox, proy), color)

            x = prox
            y = proy

        bresenham(screen, (x, y), (ver[0][0], ver[0][1]), color)

    def scanline(self, screen, arg: int) -> None:
        if arg == LCI:
            self.__scanlineLerp(screen)

        elif arg == COL:
            self.__scanlineColor(screen)

        elif arg == TEX:
            self.__scanlineTex(screen)

        else:
            raise ValueError("The arguments for scanline should be LCI for color interpolation, COL for color or TEX for texture.")

    def __scanlineColor(self, screen) -> None:
        if self.__color is None:
            raise Exception("There is no color currently assigned to this Polygon, use Polygon.setColor(color) to assign a color and then try again")

        if self.__clipped is not None:
            ver = self.__clipped
        else:
            ver = self.__vertices

        if not ver:
            return

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
                    setpixel(screen, (pixel, y), self.__color)

    def __scanlineLerp(self, screen) -> None:
        if self.__clipped is not None:
            ver = self.__clipped
        else:
            ver = self.__vertices

        if not ver:
            return

        poly = [ver[i][1] for i in range(len(ver))]

        ymin = min(poly)
        ymax = max(poly)

        for y in range(int(ymin), int(ymax) + 1):            
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

                k = 0

                colori = itx[i][1]
                colorf = itx[i + 1][1]
                
                passos = abs(itx[i][0] - itx[i + 1][0])

                for pixel in range(round(itx[i][0]), round(itx[i + 1][0]), passo):
                    t = k / passos

                    setpixel(screen, (pixel, y), lerpColor(colori, colorf, t))
                    k += 1

    def __scanlineTex(self, screen) -> None:
        if self.__tex is None:
            raise Exception("There is no texture currently assigned to this Polygon, use Polygon.setTexture(tex) to assign a texture and then try again")
        
        if self.__clipped is not None:
            ver = self.__clipped
        else:
            ver = self.__vertices

        if not ver:
            return

        poly = [ver[i][1] for i in range(len(ver))]

        ymin = min(poly)
        ymax = max(poly)

        for y in range(round(ymin), round(ymax) + 1):
            itx = []
            pi = ver[0]
            passo = 1

            for p in range(1, len(ver)):
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

                    setpixel(screen, (pixel, y), getpixelTex(self.__tex, (tx, ty)))
                    k += 1

    def setTexture(self, tex: pygame.surface) -> None:
        self.__tex = pygame.PixelArray(tex)

    def setColor(self, color: Color) -> None:
        self.__color = color

    def getColor(self) -> Color:
        return self.__color

class Rectangle(Polygon):
    def __init__(self, x, y, width, height):
        super().__init__([[x, y, RED, [0, 0]], [x + width, y, NEON_ORANGE, [1, 0]], [x + width, y + height, RED, [1, 1]], [x, y + height, NEON_ORANGE, [0, 1]]])

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

def floodFill(screen, p: tuple, color: Color) -> None:
    def isValid(screen, p: tuple, icolor: Color) -> bool:
        p = normalize(screen, p)

        if (p == -1 or getpixel(screen, p) != icolor):
            return False

        return True

    p = normalize(screen, p)

    if p == -1:
        return

    stack = []

    icolor = getpixel(screen, p)

    stack.append(p)

    while stack:
        pixel = stack.pop()

        x = pixel[0]
        y = pixel[1]

        if isValid(screen, pixel, icolor):
            setpixel(screen, pixel, color)
            update()

            north = (x, y - 1)
            south = (x, y + 1)
            east = (x + 1, y)
            west = (x - 1, y)

            if isValid(screen, north, icolor):
                stack.append(north)

            if isValid(screen, south, icolor):
                stack.append(south)

            if isValid(screen, east, icolor):
                stack.append(east)

            if isValid(screen, west, icolor):
                stack.append(west)

def update():
    pygame.display.flip()

def clear(screen, background = None):
    if background is not None:
        screen[:, :] = background[:, :384]

    else:
        screen[:, :] = 0

def main():
    j = [[0, 0], [WIDTH, HEIGHT]]
    v = [[0, 0], [WIDTH, HEIGHT]]
    j2 = [[0, 0], [1, 1]]
    v2 = [[WIDTH / 2 + 1, 0], [WIDTH - 1, HEIGHT / 2]]

    p1 = Polygon([[300, 300, CYAN, [0, 0]], [WIDTH - 300, 300, MAGENTA, [1, 0]], [WIDTH - 300, HEIGHT - 300, YELLOW, [1, 1]], [300, HEIGHT - 300, WHITE, [0, 1]]])
    p2 = Polygon([[WIDTH / 2, 0, RED, [2, 0]], [WIDTH, HEIGHT, GREEN, [4, 4]], [0, HEIGHT, BLUE, [0, 4]]])
    p3 = Polygon([[0, 0, RED, [0, 0]], [1, 0, GREEN, [1, 0]], [1, 1, BLUE, [1, 1]], [0, 1, YELLOW, [0, 1]]])
    p4 = Polygon([[0, 0, RED, [0, 0]], [1, 0, GREEN, [1, 0]], [1, 1, BLUE, [1, 1]], [0, 1, YELLOW, [0, 1]]])

    #sam = pygame.image.load("res/Sam_3.png").convert_alpha()
    #dice = pygame.image.load("res/6545910.png").convert_alpha()

    #p1.setTexture(dice)
    p1.setColor(YELLOW)

    p4c = p4.copy()
    p4c.mapToWindow(j2, v2)

    clock = pygame.time.Clock()

    i = 0
    running = True
    while running:
        p1.mapToWindow(j, v)
        clear(screen)
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.png")
                running = False
        
        p1.rotate(5)
        p1.draw(screen, CYAN)
        v[1][0] += 0.01
        v[1][1] += 0.01
        v[0][0] -= 0.01
        v[0][1] -= 0.01
        update()

    # Run the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.png")
                running = False

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    #main()
    pass
