import pygame

CELL_SIZE = 24


class MapElement(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, size, size)
        self.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
        self.type = ""


class Wall(MapElement):
    def __init__(self, x, y):
        MapElement.__init__(self, x, y, CELL_SIZE)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.type = "wall"


class Tunnel(MapElement):
    def __init__(self, x, y):
        MapElement.__init__(self, x, y, CELL_SIZE)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.type = "tunnel"

