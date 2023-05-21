from auxfunc import *
import os
from os.path import join, isfile
from random import randint, random, choice
from time import sleep
from copy import deepcopy

pygame.init()
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

#print(screen_width, screen_height)

WIDTH = 320
HEIGHT = 320

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

os.environ['SDL_VIDEO_CENTERED'] = '1'
window_pos_x = (screen_width - WIDTH) // 2
window_pos_y = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_pos_x},{window_pos_y}"

FPS = 30

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
		self.scale([1 + 0.01 * self.health, 1 + 0.01 * self.health])


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

	for i in range(WIDTH // width + 1):
		for j in range(HEIGHT // height + 1):
			pos = [i * width, (j * height)]
			tiles.append(pos)

	return [tiles, bg]

def main(screen):
	background, bg_img = get_background(TEXTURES["background3"])
	j = [[0, 0], [WIDTH, HEIGHT]]
	v = [[0, 0], [WIDTH, HEIGHT]]

	enemy_spawn_chance = 2
	bullet_dmg = 1
	bullets_ps = 3
	enemy_health = 1
	enemies_killed = 1
	player_xvel = 4
	bullets_ao = 1
	enemy_yvel = 1
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
		if random() < 0.67:
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
		player = Player()

		player.translate([-8, -(HEIGHT / 2 - 20)])

		x = 0
		running = True
		while x < 144 and running:
			clear(screen, [background, bg_img])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			keyspressed = pygame.key.get_pressed()
			if keyspressed[pygame.K_ESCAPE]:
				pygame.quit()
				quit()

			v[1][0] += 0.03
			v[1][1] += 0.03
			v[0][0] -= 0.03
			v[0][1] -= 0.03

			player.mapToWindow(j, v)
			player.rotate(5)
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

		pygame.quit()
		quit()

	while running:
		clock.tick(FPS)
		if froze:
			clear(screen)
		
		else:
			clear(screen, [background, bg_img])

		if random() <= 0.01 * enemy_spawn_chance and len(enemies) < 5:
			enemies.append(Enemy(enemy_health, player))
		
		keyspressed = pygame.key.get_pressed()

		if (keyspressed[pygame.K_a] or keyspressed[pygame.K_LEFT]) and player.getVertices()[0][0] - 20 >= 0:
			player.moveX(-player_xvel)
		
		if (keyspressed[pygame.K_d] or keyspressed[pygame.K_RIGHT]) and player.getVertices()[1][0] + 20 < WIDTH:
			player.moveX(player_xvel)
		
		if keyspressed[pygame.K_ESCAPE]:
			running = False
		
		if keyspressed[pygame.K_SPACE]:
			bullets_ps += 1
			bullets_ps = min(bullets_ps, FPS / 2)

		if c % (FPS // min(bullets_ps, FPS)) == 0 and not player.crosshair:
			bullets.append(Bullet([player.center()[0], player.center()[1] - 16], bullet_dmg))

		i = 0
		while i < len(enemies) and player.crosshair:
			enemy = enemies[i]
			
			if player.crosshair and enemy.getVertices()[0][0] - player_xvel // 3 < player.center()[0] < enemy.getVertices()[1][0] + player_xvel // 3:
				enemies.pop(i)
				enemies_killed += 1

				if enemies_killed % 20 == 0:
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
				enemies.pop(i)
				enemies_killed += 1

				if enemies_killed % 20 == 0:
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
					enemies.clear()

					enemies_killed += qt_enemy

					if enemies_killed % 20 == 0:
						if not froze:
							enemy_yvel += 0.2
						
						enemy_health += 0.5
						enemy_spawn_chance += 1
				
				elif type_pu == 1:
					if player.crosshair:
						crosshair_count = 0
					
					else:
						player.crosshair = True
						player_xvel += 5
						crosshair_count = 0
				
				elif type_pu == 2:
					if freeze_count != 0:
						freeze_count = 0

					else:
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

		# for bullet in bullets:
		# 	if bullet.getVertices()[0][1] < 0:
		# 		bullets.remove(bullet)
		# 		continue

		# 	for e_bullet in e_bullets:
		# 		if collided(e_bullet, bullet):
		# 			bullets.remove(bullet)
		# 			e_bullets.remove(e_bullet)

		# 		if collided(e_bullet, player):
		# 			player.health -= 1
					
		# 			if player.health == 0:
		# 				zoomIn(player)

		# 	for enemy in enemies:
		# 		if player.crosshair:
		# 			print(enemy.getVertices()[0][0], centre, enemy.getVertices()[1][0])
	
		# 		if player.crosshair and enemy.getVertices()[0][0] < centre < enemy.getVertices()[1][0]:
		# 			enemy.health = 0
		# 			continue

		# 		elif collided(enemy, bullet):					
		# 			bullets.remove(bullet)
		# 			enemy.health -= bullet.damage
				
		# 		if enemy.health <= 0:
		# 			enemies_killed += 1
		# 			enemies.remove(enemy)
					# if random() < 0.5:
					# 	k = random()
						
					# 	if k < 1:
					# 		type_pu = 4
					# 	elif k < 0.05:
					# 		type_pu = 2
					# 	elif k < 0.31:
					# 		type_pu = 3
					# 	elif k < 0.40:
					# 		type_pu = 1
					# 	else:
					# 		type_pu = 0
						
					# 	powerups.append(PowerUp(enemy.getVertices()[0], type_pu))

		# 			if enemies_killed % 20 == 0:
		# 				enemy_spawn_chance += 0.5
		# 				enemy_yvel += 0.3
		# 				enemy_health += 0.5
					
		# 			continue

		# 		if collided(enemy, player) or enemy.getVertices()[0][1] > HEIGHT:
		# 			enemies.remove(enemy)
		# 			player.health -= 1
					
		# 			if player.health == 0:
		# 				zoomIn(player)

		# for powerup in powerups:
		# 	# POWERUPS = ["t_increase_bullets", "t_ship_vel", "t_bomb", "t_double_bullets"]
		# 	if collided(powerup, player):
		# 		if powerup.type_pu == 0:
		# 			bullets_ps += 1
		# 			bullets_ps = min(bullets_ps, FPS // 3)
		# 			print(bullets_ps)
		# 		elif powerup.type_pu == 1:
		# 			player_xvel += 1
		# 		elif powerup.type_pu == 2:
		# 			enemies = []
		# 		elif powerup.type_pu == 3:
		# 			bullet_dmg += 0.5
		# 			print(bullet_dmg)
		# 		else:
		# 			player.crosshair = True
		# 			player_xvel += 5
		# 			crosshair_count = 0

		# 		powerups.remove(powerup)

		# 	if powerup.getVertices()[0][1] > HEIGHT:
		# 		powerups.remove(powerup)

		if player.crosshair:
			bresenham(screen, player.center(), [player.center()[0], 0], NEON_RED)
			crosshair_count += 1
			
			if crosshair_count % (5 * FPS) == 0:
				player.crosshair = False
				player_xvel -= 5

		if froze:
			freeze_count += 1

			if freeze_count % (5 * FPS) == 0:
				enemy_yvel += prev_vel
				freeze_count = 0
				froze = False

		#player.mapToWindow(j, v)
		#player.clip(DEFAULT_VIEW)
		player.scanline(screen, TEX)

		for powerup in powerups:
			powerup.moveY(1.2 * enemy_yvel)
			#powerup.mapToWindow(j, v)
			#powerup.clip(DEFAULT_VIEW)		
			powerup.scanline(screen, TEX)
		
		for enemy in enemies:
			enemy.moveY(enemy_yvel)
			if random() < 0.01:
				enemy.moveX(choice([-3 * enemy_yvel, 3 * enemy_yvel]))
			#enemy.mapToWindow(j, v)
			#enemy.clip(DEFAULT_VIEW)		
			enemy.scanline(screen, TEX)

#		print(len(powerups))
		for bullet in bullets:
			bullet.moveY(-5)
			#bullet.mapToWindow(j, v)
			#bullet.clip(DEFAULT_VIEW)		
			bullet.draw(screen, bullet.getColor())

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.flip()
				pygame.image.save(screen, "./output2.png")
				running = False

		update()

		c = (c + 1) % FPS

		#print(f"powerups = {len(powerups)}, enemies = {len(enemies)}, bullets = {len(bullets)}, bullet_dmg = {bullet_dmg}")
		print(clock.get_fps())

	pygame.quit()
	quit()

if __name__ == "__main__":
	main(screen)