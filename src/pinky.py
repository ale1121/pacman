import pygame
from phantom import Phantom, BFS


def walk_a_cell(matrix, position, direction):
    if position[1] + direction[1] < 0 or position[0] + direction[0] < 0:
        return -1, -1

    if position[1] + direction[1] >= len(matrix) or position[0] + direction[0] >= len(matrix[0]):
        return -1, -1

    if matrix[position[1] + direction[1]][position[0] + direction[0]] is None:
        return position[0] + direction[0], position[1] + direction[1]
    elif matrix[position[1] + direction[1]][position[0] + direction[0]].type == "tunnel":
        return len(matrix[0]) - 1 - position[0] - direction[0], position[1] + direction[1]
    return -1, -1


# predict Pacman's future position after a certain number of steps
# the prediction is based on the fact that Pacman will move straight forward
# as long as it is possible
def get_future_position(matrix, pacman, steps):
    (i, j) = pacman.get_position_in_labyrinth()
    direction = pacman.direction
    direction = (direction[0] // pacman.speed, direction[1] // pacman.speed)
    for _ in range(0, steps):
        (next_i, next_j) = walk_a_cell(matrix, (i, j), direction)
        if next_i != -1:
            (i, j) = (next_i, next_j)
            continue

        # try moving in other directions, start with the perpendicular ones
        direction = (direction[1], direction[0])
        (next_i, next_j) = walk_a_cell(matrix, (i, j), direction)
        if next_i != -1:
            (i, j) = (next_i, next_j)
            continue

        direction = (-direction[0], -direction[1])
        (next_i, next_j) = walk_a_cell(matrix, (i, j), direction)
        if next_i != -1:
            (i, j) = (next_i, next_j)
            continue

        # the ghost should now go in the opposite direction (it would actually run away from pacman)
        # do not include this case, so that this phantom could actually catch pacman

    return i, j


class Pinky(Phantom):
    def __init__(self, x, y, speed):
        Phantom.__init__(self, "assets/characters/pinky.png", x, y, speed)
        self.name = "Pinky"

    def construct_path(self, game_map, pacman):
        # if this phantom is very close to pacman, it will act like blinky
        diff = pacman.get_position_in_labyrinth()
        diff = (diff[0] - self.get_position_in_labyrinth()[0], diff[1] - self.get_position_in_labyrinth()[1])
        diff = (diff[0] ** 2, diff[1] ** 2)
        if sum(diff) <= 16:
            pacman_position = pacman.get_position_in_labyrinth()
        else:
            pacman_position = get_future_position(game_map.matrix, pacman, 4)

        parents_matrix = BFS(game_map.matrix, pacman_position, self.get_position_in_labyrinth())
        self.path = parents_matrix[self.get_position_in_labyrinth()[0]][self.get_position_in_labyrinth()[1]]

    def reset_image(self):
        self.image = pygame.image.load("assets/characters/pinky.png").convert_alpha()
