import pygame
from polygon import Polygon
from color import Color
from auxfunc import *
from collections import deque

WIDTH = HEIGHT = 700

# Initialize Pygame and create the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption for the window
pygame.display.set_caption("Computer Graphics is fun!")


WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

def main():
    pol = Polygon()

    pol.addVertex((100, 200))
    pol.addVertex((WIDTH / 2, 50))
    pol.addVertex((WIDTH - 100, 200))
    pol.addVertex((WIDTH - 180, HEIGHT - 180))
    pol.addVertex((180, HEIGHT - 180))

    pol.draw(RED)

    pygame.display.flip()

    floodFill((int(WIDTH / 2), int(HEIGHT / 2) + 150), Color(0, 255, 255))
    #floodFill((int(WIDTH / 2), int(HEIGHT - 1)), Color(255, 0, 0))

    # Update the screen
    pygame.display.flip()

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, "./output2.bmp")
                running = False
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()