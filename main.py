from auxfunc import *
from os import listdir
from os.path import join, isfile

WIDTH = 240
HEIGHT = 240
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

def load_textures():
	path = "res"

	images = [f for f in listdir(path) if isfile(join(path, f))]

	all_images = {}

	for image in images:
		img = pygame.image.load(join(path, image)).convert()
		all_images[image.replace(".png", "")] = img

	return all_images

def get_background(bg):
	_, _, width, height = bg.get_rect()
	tiles = []

	for i in range(WIDTH // width + 1):
		for j in range(HEIGHT // height + 1):
			pos = [i * width, j * height]
			tiles.append(pos)

	return [tiles, bg]

def main(screen):
	textures = load_textures()
	
	clock = pygame.time.Clock()
	p3 = Polygon([[0, 0, RED, [0, 0]], [1, 0, GREEN, [1, 0]], [1, 1, BLUE, [1, 1]], [0, 1, YELLOW, [0, 1]]])

	background, bg_img = get_background(textures["background"])

	p3.setTexture(textures["ship"])
	p3.setColor(CYAN)

	running = True
	while running:
		clock.tick(FPS)
		clear(screen, [background, bg_img])
		
		keyspressed = pygame.key.get_pressed()

		if keyspressed[pygame.K_w] or keyspressed[pygame.K_UP]:
			p3.moveY(-5)
		if keyspressed[pygame.K_a] or keyspressed[pygame.K_LEFT]:
			p3.moveX(-5)
		if keyspressed[pygame.K_s] or keyspressed[pygame.K_DOWN]:
			p3.moveY(5)
		if keyspressed[pygame.K_d] or keyspressed[pygame.K_RIGHT]:
			p3.moveX(5)
		if keyspressed[pygame.K_k]:
			p3.scale([1.1, 1.1])
		if keyspressed[pygame.K_l]:
			p3.scale([0.9, 0.9])
		if keyspressed[pygame.K_m]:
			p3.translate([-30, -30])
		if keyspressed[pygame.K_ESCAPE]:
			running = False
		if keyspressed[pygame.K_SPACE]:
			print(p3)

		p3.clip([[50, 50], [WIDTH - 1, 50], [WIDTH - 1, HEIGHT - 1], [50, HEIGHT - 1]])
		p3.draw(screen, WHITE)
		for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	                pygame.display.flip()
	                pygame.image.save(screen, "./output2.png")
	                running = False

		update()

	pygame.quit()
	quit()

if __name__ == "__main__":
	main(screen)