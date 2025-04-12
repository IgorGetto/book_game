import random
import pygame

from animation import Player


pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

all_sprite = pygame.sprite.Group()
meteors = pygame.sprite.Group()

# персонаж 1
"""
player = pygame.sprite.Sprite(all_sprite)
player.image = pygame.transform.scale(pygame.image.load('mozg/mozg.png'), (200, 200))
player.rect = player.image.get_rect()
player.rect.x = 100
player.rect.y = 100
"""
# нужно это создание персонажа ВМЕСТО того что было ранее
player = Player(rect_x=200, rect_y=200)
all_sprite.add(player)

# обьект для ловли
book = pygame.sprite.Sprite(all_sprite)
book.image = pygame.transform.scale(pygame.image.load('mozg/book.png'), (100, 100))
book.rect = book.image.get_rect()
book.rect.x = 140
book.rect.y = 60

# основные переменные

books = 0
speed = 10
lives = 3
gameover = False
pause = False

# делаем рандомную позицию спрайту
def set_random_pos(sprite):
    w = sprite.rect.width
    h = sprite.rect.height
    sprite.rect.x = random.randint(w // 2, SCREEN_WIDTH - w // 2)
    sprite.rect.y = random.randint(h // 2, SCREEN_HEIGHT - h // 2)

# спавним рандомный метеор в рандомном месте
def spawn_meteor():
    meteor = pygame.sprite.Sprite(all_sprite, meteors)
    image_index = random.randint(1, 4)
    meteor.image = pygame.image.load(f'./meteors/meteor{image_index}.png')
    meteor.rect = meteor.image.get_rect()
    meteor.rect.x = random.randint(
        meteor.rect.width // 2, SCREEN_WIDTH - meteor.rect.width // 2
    )
    meteor.rect.y = -150

# экран отрисовки конца игры
def game_over(screen, text_for_screen):
    screen.fill('black')
    font_object = pygame.font.Font(None, 62)
    text = font_object.render(text_for_screen, False, 'white')
    screen.blit(text, (100, 100))

# движение игрока
def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.centerx -= speed
    if keys[pygame.K_d] and player.rect.right < SCREEN_WIDTH:
        player.rect.centerx += speed
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.centery -= speed
    if keys[pygame.K_s] and player.rect.bottom < SCREEN_WIDTH:
        player.rect.centery += speed

# полет метеоров
def move_metiors():
    for m in meteors:
        m.rect.centery += speed
        if m.rect.top > SCREEN_HEIGHT:
            m.rect.x = random.randint(0, SCREEN_HEIGHT - m.rect.width)
            m.rect.centery = random.randint(-1200, -100)

# проверка что поймали нашу 'монетку'
def check_collide():
    global books
    #  проверка на столкновение (у меня это BOOK)
    if pygame.sprite.collide_mask(player, book):
        book.rect.centerx = random.randint(50, 950)
        book.rect.centery = random.randint(50, 950)
        books += 1

# проверка что метеор в нас попал
def check_collide_metiors():
    for m in meteors:
        if pygame.sprite.collide_mask(player, m):
            m.rect.x = random.randint(0, SCREEN_WIDTH - m.rect.width)
            m.rect.centery = random.randint(-1000,-100)
            return True
    return False


def start():
    global books, lives, gameover, pause
    books = 0
    lives = 3
    gameover = False
    pause = False
    spawn_meteor()
    move_metiors()

start()

run = True
while run:
    screen.fill((0, 0, 64))
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    pause = not pause
                else:
                    start()
            if event.key == pygame.K_h:
                if not gameover:
                    if not pause:
                        if books - 15 >= 0:
                            books -= 15
                            lives += 1
    all_sprite.draw(screen)
    if not gameover:
        if not pause:
            move_player()
            move_metiors()
            check_collide()

            if check_collide_metiors():
                if lives - 1 >= 0:
                    lives -= 1
                else:
                    gameover = True
        else:
            game_over(screen, 'PAUSE')
    else:
        game_over(screen, 'GAME OVER')

    # отрисовка очков и спрайтов, обновление экрана (это все постоянное)
    
    font_object = pygame.font.SysFont('Arial', 28)
    text = font_object.render(f'Очки: {books}', False, 'black', 'red')
    text2 = font_object.render(f'Жизни: {lives}', False, 'black', 'red')
    screen.blit(text, (0,  50))
    screen.blit(text2, (0,  100))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
