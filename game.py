import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

HEIGHT = 800
WIDTH = 1200
SCORE_WIDTH = 50
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

pygame.init()
FONT = pygame.font.SysFont("DejaVu Sans", 20)
FPS = pygame.time.Clock()

mainDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

os.chdir("./pygame")
bg = pygame.transform.scale(pygame.image.load("./background.png"), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = bg.get_width()
bgMove = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

playerSize = (20, 20)
enemySize = (180, 30)
bonusSize = (180, 200)
player = pygame.image.load("./player.png")
playerRect = player.get_rect()

def createEnemy():
	enemy = pygame.image.load("./enemy.png")
	enemyRect = pygame.Rect(WIDTH - enemySize[0], random.randint(0, HEIGHT - enemySize[1]), *enemySize)
	enemyMove = [random.randint(-8, -4), 0]
	return [enemy, enemyRect, enemyMove]
	
def createBonus():
	bonus = pygame.image.load("./bonus.png")
	bonusRect = pygame.Rect(random.randint(0, WIDTH - bonusSize[1]), 0, *bonusSize)
	bonusMove = [0, random.randint(4, 8)]
	return [bonus, bonusRect, bonusMove]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

playerMoveDown = [0, 4]
playerMoveUp = [0, -4]
playerMoveLeft = [-4, 0]
playerMoveRight = [4, 0]
enemies = []
bonuses = []
score = 0
imageIndex = 0
playing = True

while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == CREATE_ENEMY:
			enemies.append(createEnemy())
		if event.type == CREATE_BONUS:
			bonuses.append(createBonus())
		if(event.type == CHANGE_IMAGE):
			player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[imageIndex]))
			imageIndex += 1
			if imageIndex == len(PLAYER_IMAGES):
				imageIndex = 0
	
	FPS.tick(120)
	keys = pygame.key.get_pressed()
	
	if keys[K_DOWN] and playerRect.bottom < HEIGHT:
		playerRect = playerRect.move(playerMoveDown)
	if keys[K_UP] and playerRect.top > 0:
		playerRect = playerRect.move(playerMoveUp)
	if keys[K_LEFT] and playerRect.left > 0:
		playerRect = playerRect.move(playerMoveLeft)
	if keys[K_RIGHT] and playerRect.right < WIDTH:
		playerRect = playerRect.move(playerMoveRight)
	
	bgX1 -= bgMove
	bgX2 -= bgMove
	
	if bgX1 < -bg.get_width():
		bgX1 = bg.get_width()
	if bgX2 < -bg.get_width():
		bgX2 = bg.get_width()
	
	mainDisplay.blit(bg, (bgX1, 0))
	mainDisplay.blit(bg, (bgX2, 0))
	mainDisplay.blit(player, playerRect)
	mainDisplay.blit(FONT.render(str(score), True , COLOR_BLACK), (WIDTH / 2 - SCORE_WIDTH / 2, 20))
	
	for enemy in enemies:
		enemyRect = enemy[1].move(enemy[2])
		enemy[1] = enemyRect
		mainDisplay.blit(enemy[0], enemyRect)
		if playerRect.colliderect(enemyRect):
			playing = False

	for bonus in bonuses:
		bonusRect = bonus[1].move(bonus[2])
		bonus[1] = bonusRect
		mainDisplay.blit(bonus[0], bonusRect)
		if playerRect.colliderect(bonusRect):
			score += 1
			bonuses.pop(bonuses.index(bonus))
		
	pygame.display.flip()
	
	for enemy in enemies:
		if enemy[1].left < 0:
			enemies.pop(enemies.index(enemy))
	for bonus in bonuses:
		if bonus[1].bottom > HEIGHT:
			bonuses.pop(bonuses.index(bonus))
	
	
	