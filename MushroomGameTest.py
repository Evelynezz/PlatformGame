from tkinter.constants import CURRENT

import pygame
from PIL import Image
from pygame.examples.midi import BACKGROUNDCOLOR

# Инициализация PyGame
pygame.init()

# Размеры экрана
WIDTH = 600
HEIGHT = 800


# СПИСКИ С УНИКАЛЬНЫМИ ЭЛЕМЕНТАМИ КАЖДОГО УРОВНЯ

BACKGROUNDS = ["ForestBackground.png", "PurpleForestBackground.png"]
CURRENT_LEVEL = 0 # текущий уровень




# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Настройки игрока
HERO_HEIGHT = 50
HERO_START_X = 0
HERO_JUMP_STRENGTH = 16.4
HERO_MOVE_SPEED = 5
GRAVITY = 1
GROUND_HEIGHT = 35
HERO_START_Y = HEIGHT - HERO_HEIGHT

# Настройки платформы
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
MOVE_BACKGROUND_CONSTANT = 1
HERO_CONSTANT = 25
MOVE_BACKGROUND_CONSTANT_TWO = MOVE_BACKGROUND_CONSTANT * 2 # ускоренное движение фона

FRAGMENT_WIDTH = 40
FRAGMENT_HEIGHT = 40

CREATURE_WIDTH = 100
CREATURE_HIGHT = 100

FPS = 30

background_pic = BACKGROUNDS[0] # текущая фоновая картинка
# размеры фоновой картинки
image = Image.open(background_pic)
image_width, image_height = image.size
proportions = image_height / image_width
image_height = 2400
print(image_width)

KP_HEIGHT = 20
KP_WIDTH = 35

# Размеры экрана

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mushroom game")

# ЗАГРУЖАЕМ ПЕРСОНАЖА
image = pygame.image.load("Mushroom1.png")
image = pygame.transform.scale(image, (HERO_HEIGHT + 30, HERO_HEIGHT + 30))

def next_level(background_pic):
    background_path = background_pic  # Путь к файлу фона
    background = pygame.image.load(background_pic).convert()
    background_image = pygame.transform.scale(background, (WIDTH, image_height))
    return background_image

