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

BACKGROUNDS = ["PaperBackground1.png", "PaperBackground1.png", "PaperBackground1.png"]
CURRENT_LEVEL = 2 # текущий уровень



#ЗАГРУЖАЕМ ПЛАТФОРМЫ

def load_from_file(filename):
    platforms = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                x, y= map(int, line.split(','))
                platforms.append([x, HEIGHT - y])
    return platforms

def kill_load_from_file(filename):
    platforms = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                x, y, p= map(int, line.split(','))
                platforms.append([[x, HEIGHT - y], p])
    return platforms

def horisontal_moving_load_from_file(filename):
    platforms = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                x, start_y, end_y = map(int, line.split(','))
                platforms.append([x, HEIGHT - start_y, HEIGHT - end_y])
    return platforms

def vertical_moving_load_from_file(filename):
    platforms = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                y, start_x, end_x = map(int, line.split(','))
                platforms.append([y, start_x, end_x])
    return platforms



PLATFORMS = []
KILL_PARTS = []
M_KILL_PLATFORMS = []
FRAGMENTS = []
M_PLARFORMS = []
CREATURES = []
for level in range(3): # добавляем платформы Для каждого уровня
    platforms_data_file = f'level_parts/platforms_level_{level}.txt'
    kill_parts_data_file = f'level_parts/kill_parts_level_{level}.txt'
    m_kill_parts_data_file = f'level_parts/moving_kill_parts_level_{level}.txt'
    fragments_data_file = f'level_parts/fragments_level_{level}.txt'
    platform_moving_file = f'level_parts/moving_platforms_level_{level}.txt'
    creature_file = f'level_parts/creature_level_{level}.txt'
    M_KILL_PLATFORMS.append((horisontal_moving_load_from_file(m_kill_parts_data_file)))
    PLATFORMS.append(load_from_file(platforms_data_file))
    KILL_PARTS.append(kill_load_from_file(kill_parts_data_file))
    FRAGMENTS.append(kill_load_from_file(fragments_data_file))
    M_PLARFORMS.append(vertical_moving_load_from_file(platform_moving_file))
    CREATURES.append(load_from_file(creature_file))

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

def next_level(background_pic):
    background_path = background_pic  # Путь к файлу фона
    background = pygame.image.load(background_pic).convert()
    background_image = pygame.transform.scale(background, (WIDTH, image_height))
    return background_image


# ЗАГРУЖАЕМ ПЕРСОНАЖА

image2 = pygame.image.load("inky.png")
image2 = pygame.transform.scale(image2, (HERO_HEIGHT + 20, HERO_HEIGHT + 30))

image = pygame.image.load("inky2.png")
image = pygame.transform.scale(image, (HERO_HEIGHT + 20, HERO_HEIGHT + 30))


dead_hero = pygame.image.load("DeadMushroom.png")
dead_hero = pygame.transform.scale(dead_hero, (HERO_HEIGHT + 30, HERO_HEIGHT + 30))
creature_1 = pygame.image.load("PaperHole.png")
creature_1 = pygame.transform.scale(creature_1, (CREATURE_HIGHT + 50, CREATURE_HIGHT + 50))
#ФОНОВАЯ МУЗЫКА
#pygame.mixer.init()
#pygame.mixer.music.load("ForestMusic2.mp3")
#pygame.mixer.music.play(-1)


class Button: # КЛАСС КНОПКИ
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action # действие, которое нужно выполнить при нажатии
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) # Создаем прямоугольник
        self.rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
        self.font = pygame.font.Font(None, 32) # Инициализируем шрифт
        self.text_surface = self.font.render(self.text, True, 'white') # Создаем поверхность с текстом
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) # Выравниваем текст по центру кнопки
        self.draw(screen)

    def draw(self, surface):
        pygame.draw.rect(surface, 'orange', self.rect) # Рисуем прямоугольник кнопки
        surface.blit(self.text_surface, self.text_rect) # Рисуем текст на кнопке

    def is_clicked(self, pos): # pos - координаты клика мыши
         return self.rect.collidepoint(pos)

    def on_click(self): # Вызываем действие при клике на кнопку
        if self.action == 'restart':
            self.restart()
    def restart(self): # перезапустить игру
        print('ПЕРЕЗАПУСКАЕМ ИГРУ')
        # СБРАСЫВАЕМ ПРОГРЕСС НА УРОВНЕ
        game.__init__()
        game.hero.__init__(game.hero.hero_coords_y, game.hero.hero_coords_x, game.hero.HERO_HEIGHT)


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x , self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)


class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x , self.y, CREATURE_WIDTH - 15, CREATURE_HIGHT + 20)

    def draw(self, screen):
        if game.fragments_taken == 3:
            screen.blit(creature_1, self.rect)



class KillPart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x , self.y, KP_WIDTH, KP_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, 'red', self.rect)

class MovingPlatform:
    def __init__(self, y, start_x, end_x):
        self.y = y
        self.x = start_x
        self.end_x = end_x
        self.rect = pygame.Rect(self.x, self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.move_part_level1_velocity = 3
        self.move_right = True
    def draw(self, screen):
        pygame.draw.rect(screen, 'brown', self.rect)

    def update_pos_right(self):
        self.rect.x += self.move_part_level1_velocity

    def update_pos_left(self):
        self.rect.x -= self.move_part_level1_velocity


class MovingPart:
    def __init__(self, x, start_y, width, height, end_y):
        self.x = x
        self.y = start_y
        self.width = width
        self.height = height
        self.end_y = end_y
        self.rect = pygame.Rect(self.x , self.y, width, height)
        self.move_part_level1_velocity = 3
        self.move_up = True

    def draw(self, screen):
        pygame.draw.rect(screen, 'orange', self.rect)

    def update_pos_down(self):
        self.rect.y += self.move_part_level1_velocity

    def update_pos_up(self):
        self.rect.y -= self.move_part_level1_velocity

class MovingKillPart:
    pass

class Fragment: # Класс фрагмента
    def __init__(self, coords):
        self.coords = coords
        x, y = coords
        self.rect = pygame.Rect(x, y, FRAGMENT_WIDTH, FRAGMENT_HEIGHT)
        self.is_taken = False # взят ли фрагмент

    def draw(self, screen):
        if not self.is_taken: # рисуем фрагмент если он не взят
            pygame.draw.rect(screen, 'yellow', self.rect)




class Hero:
    def __init__(self, x, y):
        self.hero_x = x
        self.hero_y = y
        self.velocity_y = 0
        self.hero = pygame.Rect(self.hero_x, self.hero_y, HERO_HEIGHT, HERO_HEIGHT)
        self.on_ground = True
        self.can_jump = True
        self.moving_right = False
        self.moving_left = False
        self.defeat = False # Игрок не проиграл
        self.hero_can_move = True
        self.creature_contact = False
        self.current_image = image


    def draw(self, screen): # отрисовываем персонажа
        hero_rect = pygame.Rect(self.hero_x, self.hero_y, 50, 50)
        if game.restart_game: # если игрок проиграл
            screen.blit(dead_hero, (self.hero_x - HERO_CONSTANT / 1.7, self.hero_y - HERO_CONSTANT))
        else:
            if self.moving_left:
                self.current_image = image2
            elif self.moving_right:
                self.current_image = image
            screen.blit(self.current_image, (self.hero_x - HERO_CONSTANT / 1.7, self.hero_y - HERO_CONSTANT))

    def jump(self):
        if self.can_jump and self.velocity_y <= 0:
            print('JUMP')
            self.velocity_y = -HERO_JUMP_STRENGTH
            self.on_ground = False
            self.can_jump = False

    def move(self): # ДВИГАЕМ ИГРОКА
        if self.moving_right and self.hero.right < WIDTH:
            self.hero_x += HERO_MOVE_SPEED
            self.hero.x = self.hero_x
        if self.moving_left and self.hero.left > 0:
            self.hero_x -= HERO_MOVE_SPEED
            self.hero.x = self.hero_x


    def update(self, platforms, fragment):

        if not self.hero_can_move and not self.can_jump:
            return

        if self.hero.colliderect(game.creature): # СОПРИКОСНОВЕНИЕ С СУЩЕСТВОМ
            game.contact_with_creature()
            self.creature_contact = True
        else:
            self.creature_contact = False
            game.f_pressed = False

        for part in game.moving_kill_parts: # ДВИЖЕНИЕ KПЛАТФОРМ
            if self.hero.colliderect(part): # если игрок пересек kплатформу
                game.defeat()
                self.defeat = True
            if part.rect.y >= part.end_y and part.move_up: # если kплатформа достигла конечной позиции
                part.update_pos_up()
            else:
                part.move_up = False
                part.update_pos_down()
                if part.rect.y >= part.y:
                    part.move_up = True

        for part in game.moving_platforms: # ДВИЖЕНИЕ ПЛАТФОРМ
            if part.rect.x <= part.end_x and part.move_right: # если платформа достигла конечной позиции
                part.update_pos_right()
            else:
                part.move_right = False
                part.update_pos_left()
                if part.rect.x <= part.x:
                    part.move_right = True

        on_platform = False
        for part in game.moving_platforms:
            if self.hero.colliderect(part.rect):  # w
                print('ПЕРЕСЕКЛИСЬ')
                print(self.hero.x, part.rect.x)
                if self.hero.bottom == part.rect.top + 1: # если игрок на платформе
                    if part.move_right:
                        self.hero_x += part.move_part_level1_velocity
                    else:
                        self.hero_x -= part.move_part_level1_velocity
                    self.hero.x = self.hero_x


                if self.hero.bottom >= part.rect.top + 20 and self.velocity_y < 0 and self.velocity_y == -1:  # если игрок не допрыгивает до платформы
                    self.velocity_y = 10
                    self.hero_y = part.rect.bottom
                    break

                elif self.velocity_y >= 0 and self.hero.bottom >= part.rect.top and self.hero.bottom <= part.rect.bottom:
                    print('ON PLATFORM')# касаемся сверху (падаем на платформу)
                    on_platform = True  # устанавливаем флаг, что мы на платформе
                    self.velocity_y = 0
                    self.hero.bottom = part.rect.top + 1
                    self.hero_y = self.hero.bottom - HERO_HEIGHT
                    self.on_ground = True
                    self.can_jump = True

                    break  # выходим из цикла, так как игрок приземлился на платформу
            elif not on_platform and not (self.hero_x + HERO_HEIGHT < part.x or self.hero_x + HERO_HEIGHT > part.x + PLATFORM_WIDTH):  # если игрок не на платформе, то устанавливаем on_ground в False
                print(self.hero.x + HERO_HEIGHT, part.rect.x)
                self.on_ground = False

        #if self.on_ground:
            #on_platform = True

        for part in game.kill_parts:  # ДВИЖЕНИЕ ПЛАТФОРМ
            if self.hero.colliderect(part[0]):# если игрок пересек платформу
                game.defeat()


        self.move()
        if not self.can_jump or not self.on_ground and self.velocity_y > 0:
            game.move_parts()

        # Проверка касания земли
        if self.hero_y >= HERO_START_Y - game.GROUND_HEIGHT:
            if -game.background_pos < image_height - HEIGHT and game.GROUND_HEIGHT <= 0 and self.hero.bottom >= HEIGHT:
                self.hero_y = HERO_START_Y
                self.hero.y = self.hero_y
                self.defeat = True
                game.defeat()
            else:
                self.hero_y = HERO_START_Y - game.GROUND_HEIGHT
                self.velocity_y = 0
                self.on_ground = True
                self.can_jump = True
                self.hero.y = self.hero_y


        # Применяем гравитацию, если игрок не на земле (ПАДЕНИЕ)
        if not self.on_ground:
            self.velocity_y += GRAVITY
            self.hero_y += self.velocity_y
            self.hero.y = self.hero_y

        for fragment in game.fragments:
            if self.hero.colliderect(fragment[0]): # ЕСЛИ ИГРОК ВЗЯЛ ФРАГМЕНТ
               game.fragments_taken += 1
               game.fragments.pop(game.fragments.index(fragment)) # удаляем фрагмент из списка
               fragment[0].is_taken = True

        # Проверка касания платформы

        for platform in platforms:

            # ПРОВЕРКА НА ПЕРЕСЕЧЕНИЕ ПЛАТФОРМ
            if self.hero.colliderect(platform.rect):  # w

                if self.hero.bottom >= platform.rect.top + 20 and self.velocity_y < 0 and self.velocity_y == -1:  # если игрок не допрыгивает до платформы
                    self.velocity_y = 10
                    self.hero_y = platform.rect.bottom
                    break

                elif self.velocity_y > 0 and self.hero.bottom >= platform.rect.top and self.hero.bottom <= platform.rect.bottom:  # касаемся сверху (падаем на платформу)
                    self.velocity_y = 0
                    self.hero.bottom = platform.rect.top
                    self.hero_y = self.hero.bottom - HERO_HEIGHT
                    self.on_ground = True
                    self.can_jump = True
                    on_platform = True  # устанавливаем флаг, что мы на платформе
                    print(platforms.index(platform))
                    break  # выходим из цикла, так как игрок приземлился на платформу

        if not on_platform and self.hero_y < HEIGHT - HERO_HEIGHT:  # если игрок не на платформе, то устанавливаем on_ground в False
            self.on_ground = False


class Game:
    def __init__(self):
        self.already_draw = False
        self.restart_game = False
        self.level_change = False
        self.background_image = next_level(BACKGROUNDS[CURRENT_LEVEL])

        self.platforms = []
        self.fragments = []
        self.kill_parts = []
        self.moving_kill_parts = []
        self.moving_platforms = []

        self.create_moving_kill_parts()
        self.create_moving_platforms()
        self.create_kill_parts()
        self.create_platforms()
        self.create_fragment()
        self.create_creature()
        self.f_pressed = False

        self.moving_background = False
        self.background_pos = -(image_height - HEIGHT)
        self.hero = Hero(HERO_START_X, HERO_START_Y)

        self.jump_stop_power = 100
        self.jumpstop_init = False   # флаг, проверяющий определяли ли мы высоту прыжка анимации ранее
        self.def_animation = False  # анимация поражения не проигрывается
        self.not_draw_hero = False

        self.fragments_taken = 0

        print(self.background_pos)

        self.GROUND_HEIGHT = 35


    def create_platforms(self):
        # Создаем платформы

        for x, y in PLATFORMS[CURRENT_LEVEL]:
            self.platforms.append(Platform(x, y))

    def create_creature(self):
        for coords in CREATURES[CURRENT_LEVEL]:
            x, y = coords
            self.creature = Creature(x, y)
            print('creature')
            print(x,y)
        #self.creature.rect.bottomleft = 500, HEIGHT - 1865

    def create_kill_parts(self):
        for coords, p in KILL_PARTS[CURRENT_LEVEL]:
            x,y = coords
            self.kill_parts.append([KillPart(x, y), p])



    def contact_with_creature(self): # разговариваем с существом
        if self.fragments_taken == 3:
            self.change_level()
            print('TALK')



    def create_moving_kill_parts(self):
        for x, y_start, y_end in M_KILL_PLATFORMS[CURRENT_LEVEL]:
            self.moving_kill_parts.append((MovingPart(x, y_start, 40, 100, y_end)))

    def create_moving_platforms(self):
        for y, x_start, x_end in M_PLARFORMS[CURRENT_LEVEL]:
            print('mp')
            print(y, x_start, x_end)
            self.moving_platforms.append((MovingPlatform(HEIGHT - y, x_start, x_end)))


    def create_fragment(self):
        for coords, p in FRAGMENTS[CURRENT_LEVEL]:
            x,y = coords
            self.fragments.append([Fragment(coords), p])
        #self.fragments.append([Fragment([555, HEIGHT - 840]), 7])
        #self.fragments.append([Fragment([40, HEIGHT - 1560]), 19])
        #self.fragments.append([Fragment([540, HEIGHT - 2160]), 25]) #параметры, номер платформы


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.restart_game:
                        game.__init__()
                        game.hero.__init__(HERO_START_X, HERO_START_Y)
                    else:
                        self.hero.jump()
                if event.key == pygame.K_d:
                    self.hero.moving_right = True
                if event.key == pygame.K_a:
                    self.hero.moving_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.hero.moving_right = False
                if event.key == pygame.K_a:
                    self.hero.moving_left = False
        return True

    def update(self):
        self.hero.update(self.platforms, self.fragments)

    def move_parts(self): # ДВИГАЕМ ФОН И ПЛАТФОРМЫ
        # ПРОВЕРЯЕМ НА СКОЛЬКО НУЖНО ДВИГАТЬ ОБЪЕКТЫ

        if self.hero.hero_y <= HEIGHT // 2:
            move = MOVE_BACKGROUND_CONSTANT + 2.5
        elif self.hero.hero_y <= HEIGHT // 1.75:
            move = MOVE_BACKGROUND_CONSTANT + 2
        elif self.hero.hero_y <= HEIGHT // 1.5:
            move = MOVE_BACKGROUND_CONSTANT + 1
        else:
            move = MOVE_BACKGROUND_CONSTANT

        # ДВИГАЕМ

        if game.background_pos <= 0:

            for platform in self.platforms:
                platform.rect.y += move
            self.creature.rect.y += move

            for part in self.moving_kill_parts:
                part.rect.y += move
                part.y += move
                part.end_y += move
            for platform in self.moving_platforms:
                platform.rect.y += move

            for fragment in self.fragments:
                fragment[0].rect.y = self.platforms[fragment[-1]].rect.top - FRAGMENT_HEIGHT

            for part in self.kill_parts:
                part[0].rect.y = self.platforms[part[-1]].rect.top - KP_HEIGHT

            self.background_pos += move
            if self.GROUND_HEIGHT > 0:
                self.GROUND_HEIGHT -= move


    def render(self): # ОТРИСОВКА ФОНА, ПЛАТФОРМ И ФРАГМЕНТА

        screen.fill((255, 255, 255))
        screen.blit(self.background_image, (0, self.background_pos))


        for platform in self.platforms:
            platform.draw(screen)
        for fragment in self.fragments:
            fragment[0].rect.y = self.platforms[fragment[-1]].rect.top - FRAGMENT_HEIGHT
            fragment[0].draw(screen)
        for part in self.kill_parts:
            if not self.already_draw:
                part[0].rect.y = self.platforms[part[-1]].rect.top - KP_HEIGHT
                part[0].draw(screen)
            else:
                part[0].draw(screen)
                self.already_draw = True
        for move_kill_part in self.moving_kill_parts:
            move_kill_part.draw(screen)

        for platform in self.moving_platforms:
            platform.draw(screen)

        if not self.def_animation:
            self.hero.draw(screen)
        else:
            print('Игрок проиграл, анимация прыжка')
            self.defeat_animation_jump()
            self.hero.draw(screen)
        if game.hero.defeat: #  если игрок проиграл выводим соответствующую надпись
            print('text!')
            self.defeat_text()

        self.fragments_count_text_show()
        if game.hero.creature_contact:
            self.contact_with_creature()

        if game.fragments_taken >= 0:
            self.creature.draw(screen)

        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.handle_input()
            self.update()
            self.render()
            clock.tick(FPS)
        pygame.quit()

    def fragments_count_text_show(self):
        font = pygame.font.SysFont(None, 40)
        if self.fragments_taken != 3:
            text = font.render(f"Фрагментов собрано: {self.fragments_taken}/3", True, 'dark blue')  # Текст, сглаживание, цвет
        else:
            text = font.render(f"Все фрагменты собраны!", True, 'dark blue')
        text_rect = text.get_rect(topleft=(10, 10))  # форматирование текста
        screen.blit(text, text_rect)  # выводим текст

    def defeat(self): # проигрыш

        self.restart_game = True
        self.def_animation = True
        self.defeat_jump = 0
        game.hero.can_jump = False
        game.hero.hero_can_move = False

        print('проигрываем анимацию поражения')

    def defeat_animation_jump(self):
        if self.defeat_jump < self.jump_stop_power:
            game.hero.hero_y -= HERO_JUMP_STRENGTH
            game.hero.hero.y -= HERO_JUMP_STRENGTH
            self.defeat_jump += HERO_JUMP_STRENGTH
        else:
            self.defeat_animation_fall()
    def defeat_animation_fall(self):
        if game.hero.hero_y - HERO_HEIGHT < HEIGHT:
            game.hero.hero_y += HERO_JUMP_STRENGTH
            game.hero.hero.y += HERO_JUMP_STRENGTH
        else:
            self.def_animation = False
            game.hero.defeat = True
            self.defeat_text()

    def defeat_text(self):

        font = pygame.font.SysFont("Splash", 70)
        text = font.render("GAME OVER", True, 'orange')  # Текст, сглаживание, цвет
        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)) # форматирование текста посередине
        screen.blit(text, text_rect) # выводим текст

        font = pygame.font.Font(None, 35)
        text = font.render('Чтобы продолжить игру нажмите "пробел"', True, 'black')  # Текст, сглаживание, цвет
        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 40))  # форматирование текста посередине
        screen.blit(text, text_rect)  # выводим текст


        game.hero.can_jump = False
        game.hero.hero_can_move = False
        pygame.display.flip()

    def change_level(self): # следующий уровень
        global CURRENT_LEVEL
        CURRENT_LEVEL += 1
        self.__init__()
        print('Меняем фон')
        self.level_change = True


# Создание и запуск игры
game = Game()
game.run()