import pygame
from abc import abstractmethod

CELL_SIZE = 24
BORDER = 2 * CELL_SIZE
DEFAULT_CHARACTER_RECT_SIZE = CELL_SIZE


# the super class representing a sprite that moves in the labyrinth
class Character(pygame.sprite.Sprite):
    def __init__(self, image_png_file, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        self.start_position = (x, y)
        self.speed = speed
        self.direction = (0, 0)

        self.rect = pygame.rect.Rect(x, y, 24, 24)
        self.rect.center = (x, y)

        self.image = pygame.image.load(image_png_file)

    @abstractmethod
    def update(self, *argv):
        pass

    def draw(self, surface):
        surface.blit(self.image, (BORDER + self.rect.x - 8, self.rect.y - 8))

    def get_position_in_labyrinth(self):
        return self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE

    @abstractmethod
    def go_to_start(self):
        pass
