from auxfunc import *

import pygame
from pygame.locals import *

pygame.init()
width = 640
height = 480

# Load the base image
base_image = pygame.image.load("res/background3.png")

# Define the size of the tiles
tile_width = 128
tile_height = 128

# Create the screen surface
screen = pygame.display.set_mode((width, height))

# Run the main loop to display the tiled image
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the tiled image
    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            screen.blit(base_image, (x, y), pygame.Rect(x, y, tile_width, tile_height))
            pygame.display.update()

    pygame.display.update()

pygame.quit()
