from auxfunc import *
import os, sys
from os.path import join, isfile
from random import randint, random, choice
from time import sleep
from copy import deepcopy

pygame.init()
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

WIDTH = 384
HEIGHT = 384
SIDEBAR_OFFSET = 100

screen0 = pygame.display.set_mode((WIDTH + SIDEBAR_OFFSET, HEIGHT))
pygame.display.set_caption("Space Invaders")
screen = pygame.PixelArray(screen0)

os.environ['SDL_VIDEO_CENTERED'] = '1'
window_pos_x = (screen_width - WIDTH) // 2
window_pos_y = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_pos_x},{window_pos_y}"

FPS = 30

def load_sound(name):
	return pygame.mixer.Sound(join("music", name))

pygame.mixer.music.set_volume(0.07)
music = pygame.mixer.music.load(join("music", "BgMusic.wav"))

bullet_sound = load_sound("shotfired.wav")
bomb_sound = load_sound("bomb.wav")
dead_sound = load_sound("dead_sound.wav")
enemy_death_sound = load_sound("enemy_death_sound.wav")
laser_sound = load_sound("laser.wav")

bullet_sound.set_volume(0.07)
bomb_sound.set_volume(0.3)
dead_sound.set_volume(0.3)
enemy_death_sound.set_volume(0.06)

def load_font():
	path = "font"

	letters = [f for f in os.listdir(path) if isfile(join(path, f))]

	all_letters = {}

	for letter in letters:
		lt = pygame.image.load(join(path, letter)).convert()
		all_letters[letter.replace(".png", "")] = lt

	return all_letters

def load_textures():
	path = "res"

	images = [f for f in os.listdir(path) if isfile(join(path, f))]

	all_images = {}

	for image in images:
		img = pygame.image.load(join(path, image)).convert()
		all_images[image.replace(".png", "")] = img

	return all_images
	
TEXTURES = load_textures()
FONT = load_font()

pygame.display.set_icon(TEXTURES["easy"])

POWERUPS = ["t_bomb", "t_laser", "t_freeze", "t_ship_speed", "t_damage", "t_more_bullets", "t_health"]
ENEMIES = ["easy", "medium", "hard", "hard1", "hard2", "hard3", "hard4", "hard5", "expert"]

DEFAULT_VIEW = [[0, 0], [WIDTH - 1, 0], [WIDTH - 1, HEIGHT - 10], [0, HEIGHT - 10]]
SIDEBAR_VIEW = [[WIDTH - 1, 0], [WIDTH - 1 + SIDEBAR_OFFSET, 0], [WIDTH - 1 + SIDEBAR_OFFSET, HEIGHT - 1], [WIDTH - 1, HEIGHT - 1]]
DV = Polygon(DEFAULT_VIEW)
SV = Polygon(SIDEBAR_VIEW)


def write(screen, dest: tuple, text: str, size: int) -> None:
	text_length = len(text)

	if size == 16:
		for i in range(text_length):
			screen[dest[0] + i * size:dest[0] + i * size + size, dest[1]:dest[1] + size] = pygame.PixelArray(FONT[str(ord(text[i]))])

	else:
		for i in range(text_length):
			k = Rectangle(dest[0] + i * size, dest[1], size, size)
			k.setTexture(FONT[str(ord(text[i]))])
			k.scanline(screen, TEX)

class Bullet(Rectangle):
	def __init__(self, p, damage):
		x =  p[0]
		y =  p[1]

		self.damage = min(damage, 9)
		self.colors = [GREEN * 1.5, NEON_GREEN * 1.5, YELLOW * 1.5, NEON_YELLOW * 1.5, ORANGE * 1.5, NEON_ORANGE * 1.5, RED * 1.5, NEON_RED * 1.5, WHITE]
		
		super().__init__(x, y, 1, 4)
		self.setColor(self.colors[round(self.damage - 1)])

class Player(Rectangle):
	def __init__(self):
		super().__init__(WIDTH / 2, HEIGHT - 30, 16, 16)
		self.setTexture(TEXTURES["ship"])
		self.health = 3
		self.crosshair = False
		self.setColor(NEON_GREEN)

class Enemy(Rectangle):
	def __init__(self, health, player):
		super().__init__(randint(int(max(player.center()[0] - 200, 30)), int(min(player.center()[0] + 200, WIDTH - 30))), -14, 14, 14)
		self.health = min(health, 9)
		self.setTexture(TEXTURES[ENEMIES[int(self.health) - 1]])
		self.setColor(NEON_RED)

class PowerUp(Rectangle):
	def __init__(self, p, type_pu):
		super().__init__(p[0], p[1], 14, 14)
		if type_pu != 6:
			self.setTexture(TEXTURES[POWERUPS[type_pu]])
		
		self.type_pu = type_pu
		self.setColor(CYAN)

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

def tela_inicial(screen):
	# Definição do polígono do botão
	polygon_botao = Polygon([
		[(WIDTH + SIDEBAR_OFFSET) // 2 - 70, HEIGHT // 2 + 15, MAGENTA, [0, 0]],
		[(WIDTH + SIDEBAR_OFFSET) // 2 + 70, HEIGHT // 2 + 15, PINK, [1, 0]],
		[(WIDTH + SIDEBAR_OFFSET) // 2 + 70, HEIGHT // 2 + 65, BLACK, [1, 1]],
		[(WIDTH + SIDEBAR_OFFSET) // 2 - 70, HEIGHT // 2 + 65, BLUE, [0, 1]]])

	# Definição do polígono do nome do jogo
	polygon_titulo = Polygon(
		[[15, 15, MAGENTA_DARK, [0, 0]],
		[WIDTH + SIDEBAR_OFFSET - 15, 15, VIOLET, [1, 0]],
		[WIDTH + SIDEBAR_OFFSET - 15, HEIGHT / 4 - 10, BLUE, [1, 1]],
		[15, HEIGHT / 4 - 10, PINK, [0, 1]]])

	# Definição do polígono da tela de jogo
	polygon_tela = Polygon([
		[0, 0, MAGENTA_DARK, [0, 0]],
		[WIDTH + SIDEBAR_OFFSET, 0, VIOLET, [3, 0]],
		[WIDTH + SIDEBAR_OFFSET, HEIGHT, BLUE, [3, 3]], 
		[0, HEIGHT, PINK, [0, 3]]])

	# poligono para desenhar a bandeira do Brasil
	b1 = Polygon([
		[(WIDTH + SIDEBAR_OFFSET) / 2 + 150, HEIGHT / 2 + 40, RED, [0, 0]], 
		[(WIDTH + SIDEBAR_OFFSET) / 2 + 150, HEIGHT / 2 + 48, RED, [1, 0]],
		[(WIDTH + SIDEBAR_OFFSET) / 2 + 161, HEIGHT / 2 + 48, RED, [1, 1]], 
		[(WIDTH + SIDEBAR_OFFSET) / 2 + 161, HEIGHT / 2 + 40, RED, [0, 1]]])

	# Pega os vertices do polygono_botao para, futuramente, verificar cursor
	poly_botao = polygon_botao.getVertices()
	# Loop da tela inicial
	# desenha e coloca textura na tela
	clear(screen, pygame.PixelArray(TEXTURES["background"]))
	pygame.display.flip()

	# Tentativa de desenhar saturno
	raio=40
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30), raio, YELLOW)
	floodFill(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30), NEON_ORANGE)
	ellipse(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30), raio + 10, raio + 5, CREAM)
	ellipse(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30),raio + 13,raio + 2, CREAM)
	ellipse(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30), raio + 12,raio + 6, CREAM)
	ellipse(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30),raio + 13,raio + 7, CREAM)
	ellipse(screen, ((WIDTH + SIDEBAR_OFFSET) / 4 - 40,  HEIGHT / 2 - 30),raio + 15,raio + 9, CREAM)
	pygame.display.flip()

	# tentativa de desenhar a Lua
	raio=60
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 150,  HEIGHT / 2 + 110), raio, WHITE * 0.05)
	update()
	floodFill(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 150,  HEIGHT / 2 + 110), GREY)
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 160,  HEIGHT / 2 + 80), raio - 43, BLACK)
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 125,  HEIGHT / 2 + 110), raio - 38, BLACK)
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 170,  HEIGHT / 2 + 120), raio - 45, BLACK)
	circle(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 150,  HEIGHT / 2 + 145),raio -  49, BLACK)
	pygame.display.flip()
	
	# desenhando a bandeira do Brasil
	b1.draw(screen, WHITE * 0.5)
	b1.setTexture(TEXTURES["b6"])
	bresenham(screen, ((WIDTH + SIDEBAR_OFFSET) / 2 + 150,  HEIGHT / 2 + 60), ((WIDTH + SIDEBAR_OFFSET) / 2 + 150, HEIGHT / 2 + 40), WHITE * 0.5)
	pygame.display.flip()
	b1.scanline(screen, TEX)
	pygame.display.flip()
	
	DDAAA(screen, ((WIDTH + SIDEBAR_OFFSET) * 3 / 4 + 15, HEIGHT * 1/4 + 30), ((WIDTH + SIDEBAR_OFFSET) * 3 / 4 + 57, HEIGHT * 1 / 4 + 47), WHITE)
	DDAAA(screen, ((WIDTH + SIDEBAR_OFFSET) * 1 / 4 - 30, HEIGHT * 3 / 4 + 20), ((WIDTH + SIDEBAR_OFFSET) * 1 / 4 + 5, HEIGHT * 3 / 4 - 20), WHITE)
	pygame.display.flip()


	# desenha o poligono onde vai ficar o nome do jogo
	polygon_titulo.scanline(screen, LCI)
	# escrever o Nome do Jogo
	write(screen,[int(WIDTH / 2 - 130), int(HEIGHT / 8 - 8)], "Space Invaders", 26)
	pygame.display.flip()

	# Desenha e Colore o Polygono_botao
	polygon_botao.scanline(screen, LCI)
	# Escreve o texto do botão iniciar
	write(screen, [int(WIDTH / 2 - 5), int(HEIGHT / 2 + 35)], "Iniciar", 16)
	pygame.display.flip()

	rodando = True
	while rodando:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				update()
				pygame.image.save(screen0, "./output.png")
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				mouse_x, mouse_y = event.pos
				# Verifica se o botão foi pressionado
				if (mouse_x >= poly_botao[0][0] and mouse_x <= poly_botao[1][0] and mouse_y >= poly_botao[0][1] and mouse_y <= poly_botao[2][1]):
					main(screen)
			
def main(screen):
	background = pygame.PixelArray(TEXTURES["background6"])

	pygame.mixer.music.play(-1)

	j = [[0, 0], [WIDTH - 1, HEIGHT - 1]]
	v = [[0, 0], [WIDTH - 1, HEIGHT - 1]]

	j2 = [[0, 0], [WIDTH - 1, HEIGHT - 1]]
	v2 = [[WIDTH - 1, HEIGHT - 100], [WIDTH - 1 + 100, HEIGHT - 1]]

	enemy_spawn_chance = 2
	bullet_dmg = 1
	bullets_ps = 2
	enemy_health = 1
	enemies_killed = 0
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
		if len(powerups) < 3 and random() < 0.5 * enemy_health:
			k = random()
			
			if k < 0.01:
				type_pu = 0
			
			elif k < 0.04:
				type_pu = 1
			
			elif k < 0.05:
				type_pu = 2
			
			elif k < 0.15:
				type_pu = choice([3, 6])
			
			elif k < 0.40:
				type_pu = 4
			
			elif k < 0.50:
				type_pu = 5

			else:
				return
			
			powerups.append(PowerUp(enemy.center(), type_pu))

		else:
			return

	def zoomIn():
		pygame.mixer.music.pause()
		dead_sound.play()
		player2 = Player()

		player2.translate([-10, -(HEIGHT / 2 - 20)])

		x = 0
		running = True
		while x < 90 and running:
			clear(screen, background)
			
			write(screen, [WIDTH + 1, 25], f"{enemies_killed:03d}", 16)
			write(screen, [WIDTH + 1, 90], f"{player.health:03d}", 16)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			keyspressed = pygame.key.get_pressed()
			if keyspressed[pygame.K_ESCAPE]:
				pygame.quit()
				quit()

			v[1][0] += 0.08
			v[1][1] += 0.08
			v[0][0] -= 0.08
			v[0][1] -= 0.08

			player2.mapToWindow(j, v)
			player2.rotate(8)
			player2.clip(DEFAULT_VIEW)
			player2.scanline(screen, TEX)
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
			clear(screen, None)
		
		else:
			clear(screen, background)
		
		
		if random() <= 0.01 * enemy_spawn_chance and len(enemies) < 5:
			enemies.append(Enemy(enemy_health, player))
		
		keyspressed = pygame.key.get_pressed()

		if (keyspressed[pygame.K_a] or keyspressed[pygame.K_LEFT]):
			for i in range(player_xvel):
				if player.getVertices()[0][0] - 8 >= 0:
					player.moveX(-1)
		
		if (keyspressed[pygame.K_d] or keyspressed[pygame.K_RIGHT]):
			for i in range(player_xvel):
				if player.getVertices()[1][0] + 8 < WIDTH:
					player.moveX(1)
		
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
					enemy_yvel += 0.1
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
					enemy_yvel += 0.1
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

				if player.health <= 0:
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
					enemies_bombed = enemies.copy()
					enemies.clear()
					
					for enemy in enemies_bombed:
						randomPowerUp(enemy)

					enemies_killed += qt_enemy

					if enemies_killed % 15 == 0:
						if not froze:
							enemy_yvel += 0.1
						
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
				
				elif type_pu == 5:
					bullets_ps += 1
					bullets_ps = min(bullets_ps, FPS // 3)

				else:
					player.health += 1

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


		player.mapToWindow(j, v)
		player.clip(DEFAULT_VIEW)
		player.scanline(screen, TEX)

		for powerup in powerups:
			powerup.moveY(1.2 * enemy_yvel)
			powerup.mapToWindow(j, v)
			powerup.clip(DEFAULT_VIEW)
			
			if powerup.type_pu != 6:
				powerup.scanline(screen, TEX)
			else:
				powerup.scanline(screen, LCI)
		
		for enemy in enemies:
			enemy.moveY(enemy_yvel)
			if random() < 0.01:
				enemy.moveX(choice([-3 * enemy_yvel, 3 * enemy_yvel]))
			
			enemy.mapToWindow(j, v)
			enemy.clip(DEFAULT_VIEW)
			enemy.scanline(screen, TEX)

		for bullet in bullets:
			bullet.moveY(-bullet_yvel)
			bullet.mapToWindow(j, v)
			bullet.clip(DEFAULT_VIEW)
			bullet.draw(screen, bullet.getColor())

		write(screen, [WIDTH + 1, HEIGHT - 20], f"{str(int(clock.get_fps()))[:2]} FPS", 16)
		
		DV.draw(screen, WHITE * 0.8)
		SV.draw(screen, WHITE * 0.8)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.flip()
				pygame.image.save(screen0, "./output2.png")
				running = False

		if froze:
			write(screen, [WIDTH + 1, 5], "SCORE", 16)
			write(screen, [WIDTH + 1, 70], "HEALTH", 16)

		write(screen, [WIDTH + 1, 25], f"{enemies_killed:03d}", 16)
		write(screen, [WIDTH + 1, 90], f"{player.health:03d}", 16)

		update()

		c = (c + 1) % FPS

	pygame.quit()
	quit()

if __name__ == "__main__":
	main(screen)
	#tela_inicial(screen)
