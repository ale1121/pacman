import pygame


# converts an image into a sprite sheet which can be animated.
# the sprite sheet must contain only one row, but can have any number of columns
class SpriteSheet:
    # width, height - the dimensions of one frame
    def __init__(self, image_path, width, height):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.width = width
        self.height = height
        self.nr_frames = self.sheet.get_size()[0] / width
        self.mask = pygame.surface.Surface((width, height))
        self.mask.fill((0, 0, 0))

    def get_frame(self, frame):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * self.width), 0, self.width, self.height))
        image.set_colorkey((0, 0, 0))

        return image

    def animate(self, screen, position, cooldown):
        i = 0
        last_update = pygame.time.get_ticks()
        while i < self.nr_frames:
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= cooldown:
                screen.blit(self.mask, position)
                screen.blit(self.get_frame(i), position)
                last_update = current_time
                i += 1
            pygame.display.update()
        screen.blit(self.mask, position)