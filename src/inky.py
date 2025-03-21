import pygame

from phantom import Phantom, BFS, check_position
from pinky import get_future_position
from blinky import Blinky


# gives the closest valid position for inky (since its algorithm can point towards an unreachable cell)
def get_first_available_position(matrix, initial_position):
    # bring position to a possible position (regarding the boundaries of the matrix)
    if initial_position[0] < 0:
        initial_position[0] = 0
    elif initial_position[0] >= len(matrix[0]):
        initial_position[0] = len(matrix[0]) - 1

    if initial_position[1] < 0:
        initial_position[1] = 0
    elif initial_position[1] >= len(matrix):
        initial_position[1] = len(matrix) - 1

    queue = [initial_position]
    while len(queue) > 0:
        position = queue.pop(0)
        if check_position(matrix, position):
            return position

        if position[0] > 0:
            queue.append([position[0] - 1, position[1]])
        if position[0] < len(matrix[0]) - 1:
            queue.append([position[0] + 1, position[1]])
        if position[1] > 0:
            queue.append([position[0], position[1] - 1])
        if position[1] < len(matrix) - 1:
            queue.append([position[0], position[1] + 1])

    return None


class Inky(Phantom):
    def __init__(self, x, y, speed, blinky: Blinky):
        Phantom.__init__(self, "assets/characters/inky.png", x, y, speed)
        self.blinky = blinky
        self.name = "Inky"

    # the aiming position of Inky is the symmetric of Blinky's position
    # about the prediction of Pacman's position after 2 rounds
    # this way Inky helps Blinky surround Pacman
    def construct_path(self, game_map, pacman):
        first_half = get_future_position(game_map.matrix, pacman, 2)
        rough_position = [2 * first_half[0] - self.blinky.get_position_in_labyrinth()[0],
                          2 * first_half[1] - self.blinky.get_position_in_labyrinth()[1]]

        parents_matrix = BFS(game_map.matrix,
                             get_first_available_position(game_map.matrix, rough_position),
                             self.get_position_in_labyrinth())
        self.path = parents_matrix[self.get_position_in_labyrinth()[0]][self.get_position_in_labyrinth()[1]]

        # don't move if the phantom is already in the right place
        if self.path == (-1, -1):
            self.path = self.get_position_in_labyrinth()

    def reset_image(self):
        self.image = pygame.image.load("assets/characters/inky.png").convert_alpha()
