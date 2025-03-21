import pygame
from phantom import BFS, Phantom


class Blinky(Phantom):
    def __init__(self, x, y, speed):
        Phantom.__init__(self, "assets/characters/blinky.png", x, y, speed)
        self.name = "Blinky"

    def construct_path(self, game_map, pacman):
        # construct the fastest route towards the current position of pacman using BFS

        parents_matrix = BFS(game_map.matrix, pacman.get_position_in_labyrinth(), self.get_position_in_labyrinth())
        self.path = parents_matrix[self.get_position_in_labyrinth()[0]][self.get_position_in_labyrinth()[1]]

    def reset_image(self):
        self.image = pygame.image.load("assets/characters/blinky.png").convert_alpha()
