from auxfunc import *
from color import Color

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