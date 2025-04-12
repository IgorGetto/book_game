import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y):
        pygame.sprite.Sprite.__init__(self)
        # загрузка твоих картинок для анимации
        self.anim = [pygame.transform.scale(pygame.image.load('images/run1.png'), (250, 250)),
                     pygame.transform.scale(pygame.image.load('images/run2.png'), (250, 250))]
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = rect_x
        self.rect.centery = rect_y

        self.frame = 0  # текущий кадр
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # как быстро кадры меняются

    def update(self):
        # смена кадров по времени
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]

player = Player(rect_x=200, rect_y=200)
all_sprites.add(player)
