from auxfunc import *
import os
from os.path import join, isfile
from random import randint, random, choice
from time import sleep
from copy import deepcopy

pygame.init()
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

#print(screen_width, screen_height)

WIDTH = 384
HEIGHT = 384
SIDEBAR_OFFSET = 100

screen = pygame.display.set_mode((WIDTH + SIDEBAR_OFFSET, HEIGHT))
pygame.display.set_caption("Space Invaders")

os.environ['SDL_VIDEO_CENTERED'] = '1'
window_pos_x = (screen_width - WIDTH) // 2
window_pos_y = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_pos_x},{window_pos_y}"

FPS = 30

def load_sound(name):
	return pygame.mixer.Sound(join("music", name))

pygame.mixer.music.set_volume(0.07)
music = pygame.mixer.music.load(join("music", "BgMusic.ogg"))

pygame.mixer.music.play(-1)

bullet_sound = load_sound("shotfired.ogg")
bomb_sound = load_sound("bomb.wav")
dead_sound = load_sound("dead_sound.wav")
enemy_death_sound = load_sound("enemy_death_sound.wav")
laser_sound = load_sound("laser.wav")

bullet_sound.set_volume(0.07)
bomb_sound.set_volume(0.3)
dead_sound.set_volume(0.3)
enemy_death_sound.set_volume(0.06)


def load_textures():
	path = "res"

	images = [f for f in os.listdir(path) if isfile(join(path, f))]

	all_images = {}

	for image in images:
		img = pygame.image.load(join(path, image)).convert()
		all_images[image.replace(".png", "")] = img

	return all_images
	
TEXTURES = load_textures()

POWERUPS = ["t_bomb", "t_laser", "t_freeze", "t_ship_speed", "t_damage", "t_more_bullets"]
ENEMIES = ["easy", "medium", "hard", "expert"]

DEFAULT_VIEW = [[0, 0], [WIDTH - 1, 0], [WIDTH - 1, HEIGHT - 1], [0, HEIGHT - 1]]
SIDEBAR_VIEW = [[WIDTH - 1, 0], [WIDTH - 1 + SIDEBAR_OFFSET, 0], [WIDTH - 1 + SIDEBAR_OFFSET, HEIGHT - 1], [WIDTH - 1, HEIGHT - 1]]
DV = Polygon(DEFAULT_VIEW)
SV = Polygon(SIDEBAR_VIEW)

class Bullet(Rectangle):
	def __init__(self, p, damage):
		x =  p[0]
		y =  p[1]

		self.damage = min(damage, 4)
		self.colors = [NEON_GREEN * 1.5, NEON_YELLOW * 1.5, NEON_ORANGE * 1.5, NEON_RED * 1.5]
		
		super().__init__(x, y, 1, 6)
		self.setColor(self.colors[round(self.damage - 1)])

class Player(Rectangle):
	def __init__(self):
		super().__init__(WIDTH / 2, HEIGHT - 30, 16, 16)
		self.setTexture(TEXTURES["ship"])
		self.health = 3
		self.crosshair = False

class Enemy(Rectangle):
	def __init__(self, health, player):
		super().__init__(randint(int(max(player.center()[0] - 200, 30)), int(min(player.center()[0] + 200, WIDTH - 30))), -14, 14, 14)
		self.health = min(health, 4)
		self.setTexture(TEXTURES[ENEMIES[int(self.health) - 1]])

class PowerUp(Rectangle):
	def __init__(self, p, type_pu):
		super().__init__(p[0], p[1], 16, 16)
		self.setTexture(TEXTURES[POWERUPS[type_pu]])
		self.type_pu = type_pu

def collided(polygon1, polygon2):
	vert1 = polygon1.getVertices()
	vert2 = polygon2.getVertices()

	min_x1 = min(v[0] for v in vert1)
	max_x1 = max(v[0] for v in vert1)
	min_y1 = min(v[1] for v in vert1)
	max_y1 = max(v[1] for v in vert1)

	min_x2 = min(v[0] for v in vert2)
	max_x2 = max(v[0] for v in vert2)
	min_y2 = min(v[1] for v in vert2)
	max_y2 = max(v[1] for v in vert2)

	return (min_x1 <= max_x2 and max_x1 >= min_x2) and (min_y1 <= max_y2 and max_y1 >= min_y2)

def get_background(bg):
	_, _, width, height = bg.get_rect()
	tiles = []

	for i in range(WIDTH // width):
		for j in range(HEIGHT // height + 1):
			pos = [i * width, j * height]
			tiles.append(pos)

	return [tiles, bg]

def main(screen):
	background, bg_img = get_background(TEXTURES["background3"])
	j = [[0, 0], [WIDTH - 1, HEIGHT - 1]]
	v = [[0, 0], [WIDTH - 1, HEIGHT - 1]]

	j2 = [[0, 0], [WIDTH - 1, HEIGHT - 1]]
	v2 = [[WIDTH - 1, HEIGHT - 100], [WIDTH - 1 + 100, HEIGHT - 1]]

	enemy_spawn_chance = 2
	bullet_dmg = 1
	bullets_ps = 1
	enemy_health = 1
	enemies_killed = 1
	player_xvel = 3
	enemy_yvel = 1
	bullet_yvel = 5
	zoom_in = 0
	freeze_count = 0
	
	bullets = []
	e_bullets = []
	enemies = []
	powerups = []

	player = Player()
	
	clock = pygame.time.Clock()

	running = True
	froze = False
	c = 0

	def randomPowerUp(enemy):
		if random() < 0.3 * enemy.health:
			k = random()
			
			if k < 0.01:
				type_pu = 0
			
			elif k < 0.04:
				type_pu = 1
			
			elif k < 0.05:
				type_pu = 2
			
			elif k < 0.15:
				type_pu = 3
			
			elif k < 0.40:
				type_pu = 4
			
			elif k < 0.50:
				type_pu = 5

			else:
				return
			
			powerups.append(PowerUp(enemy.center(), type_pu))

	def zoomIn():
		pygame.mixer.music.pause()
		dead_sound.play()
		player = Player()

		player.translate([-10, -(HEIGHT / 2 - 20)])

		x = 0
		running = True
		while x < 90 and running:
			clear(screen, [background, bg_img], DV, SV)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			keyspressed = pygame.key.get_pressed()
			if keyspressed[pygame.K_ESCAPE]:
				print(enemies_killed)
				pygame.quit()
				quit()

			v[1][0] += 0.08
			v[1][1] += 0.08
			v[0][0] -= 0.08
			v[0][1] -= 0.08

			player.mapToWindow(j, v)
			player.rotate(8)
			player.clip(DEFAULT_VIEW)
			player.scanline(screen, TEX)
			update()

			x += 1

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			keyspressed = pygame.key.get_pressed()
			if keyspressed[pygame.K_ESCAPE]:
				running = False

		print(enemies_killed)
		pygame.quit()
		quit()

	while running:
		clock.tick(FPS)
		if froze:
			clear(screen, None, DV, SV)
		
		else:
			clear(screen, [background, bg_img], DV, SV)

		if random() <= 0.01 * enemy_spawn_chance and len(enemies) < 5:
			enemies.append(Enemy(enemy_health, player))
		
		keyspressed = pygame.key.get_pressed()

		if (keyspressed[pygame.K_a] or keyspressed[pygame.K_LEFT]) and player.getVertices()[0][0] - 8 >= 0:
			player.moveX(-player_xvel)
		
		if (keyspressed[pygame.K_d] or keyspressed[pygame.K_RIGHT]) and player.getVertices()[1][0] + 8 < WIDTH:
			player.moveX(player_xvel)
		
		if keyspressed[pygame.K_ESCAPE]:
			running = False
		
		if keyspressed[pygame.K_SPACE]:
			bullets_ps += 1
			bullets_ps = min(bullets_ps, FPS / 2)

		if c % (FPS // min(bullets_ps, FPS)) == 0 and not player.crosshair:
			bullets.append(Bullet([player.center()[0], player.center()[1] - 16], bullet_dmg))
			bullet_sound.play()

		i = 0
		while i < len(enemies) and player.crosshair:
			enemy = enemies[i]
			
			if player.crosshair and enemy.getVertices()[0][0] - player_xvel // 3 < player.center()[0] < enemy.getVertices()[1][0] + player_xvel // 3:
				enemy_death_sound.play()
				enemies.pop(i)
				enemies_killed += 1

				if enemies_killed % 15 == 0:
					enemy_yvel += 0.2
					enemy_health += 0.5
					enemy_spawn_chance += 1

				randomPowerUp(enemy)
				continue

			i += 1
		
		i = 0
		while i < len(enemies):
			enemy = enemies[i]
			killed = False

			k = 0
			while k < len(bullets):
				bullet = bullets[k]
				if collided(bullet, enemy):
					bullets.pop(k)
					enemy.health -= bullet_dmg

					if enemy.health <= 0:
						killed = True
						break

					continue
				
				if bullet.getVertices()[0][1] < 0:
					bullets.pop(k)
					continue

				k += 1

			if killed:
				enemy_death_sound.play()
				enemies.pop(i)
				enemies_killed += 1

				if enemies_killed % 15 == 0:
					enemy_yvel += 0.2
					enemy_health += 0.5
					enemy_spawn_chance += 1

				randomPowerUp(enemy)
				continue

			i += 1
		
		i = 0
		while i < len(enemies):
			enemy = enemies[i]
			if collided(player, enemy) or enemy.getVertices()[0][1] > HEIGHT:
				player.health -= 1

				if player.health == 0:
					zoomIn()

				enemies.pop(i)
				continue			

			i += 1

		while i < len(bullets):
			bullet = bullets[i]
			if bullet.getVertices()[0][1] < 0:
				bullets.pop(i)
				continue

			i += 1

		i = 0
		while i < len(powerups):
			# POWERUPS = ["t_bomb", "t_laser", "t_freeze", "t_ship_speed", "t_damage", "t_more_bullets"]
			powerup = powerups[i]

			if powerup.getVertices()[0][1] > HEIGHT:
				powerups.pop(i)

				continue

			if collided(powerup, player):
				type_pu = powerup.type_pu
				powerups.pop(i)

				if type_pu == 0:
					qt_enemy = len(enemies)
					bomb_sound.play()
					enemies_bombed = enemies
					enemies.clear()
					
					for enemy in enemies_bombed:
						randomPowerUp(enemy)

					enemies_killed += qt_enemy

					if enemies_killed % 15 == 0:
						if not froze:
							enemy_yvel += 0.2
						
						enemy_health += 0.5
						enemy_spawn_chance += 1
				
				elif type_pu == 1:
					if player.crosshair:
						crosshair_count = 0
						laser_sound.play()
					
					else:
						laser_sound.play()
						player.crosshair = True
						player_xvel += 5
						crosshair_count = 0
				
				elif type_pu == 2:
					if freeze_count != 0:
						freeze_count = 0

					else:
						pygame.mixer.music.pause()
						prev_vel = deepcopy(enemy_yvel)
						enemy_yvel = 0
						freeze_count = 0
						froze = True
				
				elif type_pu == 3:
					player_xvel += 1
				
				elif type_pu == 4:
					bullet_dmg += 0.5
				
				else:
					bullets_ps += 1
					bullets_ps = min(bullets_ps, FPS // 3)

				continue


			i += 1

		if player.crosshair:
			bresenham(screen, player.center(), [player.center()[0], 0], NEON_RED)
			bresenham(screen, [player.center()[0] - 1, player.center()[1]], [player.center()[0] - 1, 0], RED)
			bresenham(screen, [player.center()[0] + 1, player.center()[1]], [player.center()[0] + 1, 0], RED)
			crosshair_count += 1
			
			if crosshair_count % (5 * FPS) == 0:
				player.crosshair = False
				player_xvel -= 5

		if froze:
			freeze_count += 1

			if freeze_count % (5 * FPS) == 0:
				pygame.mixer.music.play(-1)
				enemy_yvel += prev_vel
				freeze_count = 0
				froze = False

		player.scanline(screen, TEX)

		for powerup in powerups:
			powerup.moveY(1.2 * enemy_yvel)
			powerup.clip(DEFAULT_VIEW)
			powerup.scanline(screen, TEX)
		
		for enemy in enemies:
			enemy.moveY(enemy_yvel)
			if random() < 0.01:
				enemy.moveX(choice([-3 * enemy_yvel, 3 * enemy_yvel]))
			
			enemy.clip(DEFAULT_VIEW)
			enemy.scanline(screen, TEX)

		for bullet in bullets:
			bullet.moveY(-bullet_yvel)
			bullet.clip(DEFAULT_VIEW)
			bullet.draw(screen, bullet.getColor())

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.flip()
				pygame.image.save(screen, "./output2.png")
				running = False

		update()

		c = (c + 1) % FPS

	pygame.quit()
	quit()

if __name__ == "__main__":
	main(screen)
