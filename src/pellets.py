import pygame

CELL_SIZE = 24
BORDER = 2 * CELL_SIZE
color = (250, 185, 176)


class Pellet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "pellet"
        self.gives_powers = False
        self.points = 10


class SmallPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self)
        self.image = pygame.Surface((6, 6))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (9 + x * CELL_SIZE, 9 + y * CELL_SIZE)

    def draw(self, screen):
        screen.blit(self.image, (BORDER + self.rect.x, self.rect.y))


class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self)
        self.image = pygame.image.load("assets/map/power_pellet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
        self.gives_powers = True
        self.points = 50

    def draw(self, screen):
        screen.blit(self.image, (BORDER + self.rect.x, self.rect.y))
