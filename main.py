import random
import pygame

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

all_sprite = pygame.sprite.Group()

# персонаж 1
player = pygame.sprite.Sprite(all_sprite)
player.image = pygame.transform.scale(pygame.image.load('mozg.png'), (200, 200))
player.rect = player.image.get_rect()
player.rect.x = 100
player.rect.y = 100

# обьект для ловли
book = pygame.sprite.Sprite(all_sprite)
book.image = pygame.transform.scale(pygame.image.load('book.png'), (100, 100))
book.rect = book.image.get_rect()
book.rect.x = 140
book.rect.y = 60

books = 0
run = True
while run:
    screen.fill((0, 0, 64))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprite.draw(screen)
    # движение
    speed = 10
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.centerx -= speed
    if keys[pygame.K_d] and player.rect.right < 1200:
        player.rect.centerx += speed
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.centery -= speed 
    if keys[pygame.K_s] and player.rect.bottom < 1200:
        player.rect.centery += speed

    #  проверка на столкновение (у меня это BOOK)
    if pygame.sprite.collide_mask(player, book):
        book.rect.centerx = random.randint(50, 950)
        book.rect.centery = random.randint(50, 950)
        books += 1

    # отрисовка очков
    font_object = pygame.font.SysFont('Arial', 28)
    text = font_object.render(f'Очки: {books}', False, 'black', 'red')
    screen.blit(text, (0,  50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
