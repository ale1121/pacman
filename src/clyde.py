import pygame
from phantom import Phantom, BFS

# a dictionary containing the circular moves that clyde should do when he comes too close to Pacman
standard_clyde_moves = {(3, 29): (4, 29),
                        (4, 29): (5, 29),
                        (5, 29): (6, 29),
                        (6, 29): (7, 29),
                        (7, 29): (8, 29),
                        (8, 29): (9, 29),
                        (9, 29): (10, 29),
                        (10, 29): (11, 29),
                        (11, 29): (12, 29),
                        (12, 29): (13, 29),
                        (13, 29): (14, 29),
                        (14, 29): (14, 28),
                        (14, 28): (14, 27),
                        (14, 27): (14, 26),
                        (14, 26): (13, 26),
                        (13, 26): (12, 26),
                        (12, 26): (11, 26),
                        (11, 26): (11, 25),
                        (11, 25): (11, 24),
                        (11, 24): (11, 23),
                        (11, 23): (10, 23),
                        (10, 23): (9, 23),
                        (9, 23): (8, 23),
                        (8, 23): (8, 24),
                        (8, 24): (8, 25),
                        (8, 25): (8, 26),
                        (8, 26): (7, 26),
                        (7, 26): (6, 26),
                        (6, 26): (5, 26),
                        (5, 26): (4, 26),
                        (4, 26): (3, 26),
                        (3, 26): (3, 27),
                        (3, 27): (3, 28),
                        (3, 28): (3, 29)
                        }


class Clyde(Phantom):
    def __init__(self, x, y, speed):
        Phantom.__init__(self, "assets/characters/clyde.png", x, y, speed)
        self.is_going_to_top_left = False
        self.name = "Clyde"

    def construct_path(self, game_map, pacman):
        diff = pacman.get_position_in_labyrinth()
        diff = (diff[0] - self.get_position_in_labyrinth()[0], diff[1] - self.get_position_in_labyrinth()[1])
        diff = (diff[0] ** 2, diff[1] ** 2)

        # when clyde comes too close to Pacman, he goes straight
        # to the top left and after that the route should be recalculated
        # this prevents clyde from oscillating 8 cells apart from Pacman
        if sum(diff) >= 64 and self.is_going_to_top_left is False:
            parents_matrix = BFS(game_map.matrix, pacman.get_position_in_labyrinth(), self.get_position_in_labyrinth())
            self.path = parents_matrix[self.get_position_in_labyrinth()[0]][self.get_position_in_labyrinth()[1]]
            return

        next_move = standard_clyde_moves.get(self.get_position_in_labyrinth())
        if next_move is None:
            self.is_going_to_top_left = True
            parents_matrix = BFS(game_map.matrix, (2, 29), self.get_position_in_labyrinth())
            self.path = parents_matrix[self.get_position_in_labyrinth()[0]][self.get_position_in_labyrinth()[1]]
        else:
            self.is_going_to_top_left = False
            self.path = next_move

    def reset_image(self):
        self.image = pygame.image.load("assets/characters/clyde.png").convert_alpha()
