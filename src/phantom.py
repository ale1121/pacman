from abc import ABC, abstractmethod
import pygame
import character

CELL_SIZE = 24


# add a position to the queue, if it can be walked by a character
def add_to_queue(queue, matrix, old_position, new_position, parents_matrix):
    if matrix[new_position[1]][new_position[0]] is None:
        parents_matrix[new_position[0]][new_position[1]] = old_position
        queue.append(new_position)
        return

    if matrix[new_position[1]][new_position[0]].type == "tunnel":
        parents_matrix[new_position[0]][new_position[1]] = old_position
        parents_matrix[len(matrix[0]) - 1 - new_position[0]][new_position[1]] = new_position
        queue.append((len(matrix[0]) - 1 - new_position[0], new_position[1]))


def BFS(matrix, start, goal):
    (start_x, start_y) = start
    (goal_x, goal_y) = goal

    x_size = len(matrix[0])
    y_size = len(matrix)

    parents_matrix = [[None for _ in range(y_size)] for _ in range(x_size)]
    parents_matrix[start_x][start_y] = (-1, -1)
    queue = [(start_x, start_y)]

    while len(queue) != 0:
        (current_x, current_y) = queue.pop(0)
        if current_x == goal_x and current_y == goal_y:
            return parents_matrix

        # visit all its neighbors
        if current_x > 0 and parents_matrix[current_x - 1][current_y] is None:
            add_to_queue(queue,
                         matrix,
                         (current_x, current_y),
                         (current_x - 1, current_y),
                         parents_matrix)

        if current_x < x_size - 1 and parents_matrix[current_x + 1][current_y] is None:
            add_to_queue(queue,
                         matrix,
                         (current_x, current_y),
                         (current_x + 1, current_y),
                         parents_matrix)

        if current_y > 0 and parents_matrix[current_x][current_y - 1] is None:
            add_to_queue(queue,
                         matrix,
                         (current_x, current_y),
                         (current_x, current_y - 1),
                         parents_matrix)

        if current_y < y_size - 1 and parents_matrix[current_x][current_y + 1] is None:
            add_to_queue(queue,
                         matrix,
                         (current_x, current_y),
                         (current_x, current_y + 1),
                         parents_matrix)

    return parents_matrix


def check_position(matrix, position):
    return matrix[position[1]][position[0]] is None or matrix[position[1]][position[0]].type != "wall"


class Phantom(character.Character, ABC):

    def __init__(self, image_png_file, x, y, speed):
        character.Character.__init__(self, image_png_file, x, y, speed)
        # indicate turns until next check (a check is required each time the
        # phantom reaches the center of a cell
        self.turns_until_check = 0
        self.path = None
        self.is_frightened = False
        self.turns_sleep = 0

    def update(self, game_map, pacman):
        if self.turns_sleep > 0:
            self.turns_sleep -= 1
            return

        if self.turns_until_check == 0:
            if self.is_frightened:
                self.path = self.get_furthest_neighbor(pacman, game_map.matrix)
            else:
                self.construct_path(game_map, pacman)

            # set the current direction
            (i, j) = self.path

            if (i, j) == (31, 14):  # left tunnel
                self.rect.midleft = game_map.left_tunnel.rect.midright
                return
            if (i, j) == (0, 14):  # right tunnel
                self.rect.midright = game_map.right_tunnel.rect.midleft
                return

            self.direction = ((i - self.get_position_in_labyrinth()[0]) * self.speed,
                             (j - self.get_position_in_labyrinth()[1]) * self.speed)

            self.turns_until_check = CELL_SIZE // self.speed

        self.turns_until_check -= 1
        self.rect.center = self.rect.move(self.direction).center

    @abstractmethod
    def construct_path(self, game_map, pacman):
        pass

    def go_to_start(self):
        self.rect.center = self.start_position
        self.path = None
        self.turns_until_check = 0

    # calculate the furthest neighbor to the Pacman's current position
    def get_furthest_neighbor(self, pacman, matrix):
        position = self.get_position_in_labyrinth()
        parents_matrix = BFS(matrix, pacman.get_position_in_labyrinth(), position)

        # if a position from parents_matrix is None and the cell was not a wall, then that
        # position is further from pacman that current position

        if position[0] > 0 and \
                check_position(matrix, (position[0] - 1, position[1])) and \
                parents_matrix[position[0] - 1][position[1]] is None:
            return position[0] - 1, position[1]

        if position[0] < len(matrix[0]) - 1 and \
                check_position(matrix, (position[0] + 1, position[1])) and \
                parents_matrix[position[0] + 1][position[1]] is None:
            return position[0] + 1, position[1]

        if position[1] > 0 and \
                check_position(matrix, (position[0], position[1] - 1)) and \
                parents_matrix[position[0]][position[1] - 1] is None:
            return position[0], position[1] - 1

        if position[1] < len(matrix) - 1 and \
                check_position(matrix, (position[0], position[1] + 1)) and \
                parents_matrix[position[0]][position[1] + 1] is None:
            return position[0], position[1] + 1

        # no neighbour is further from pacman, remain in the same position
        return position

    def get_frightened(self):
        self.image = pygame.image.load("assets/characters/frightened_ghost.png")
        self.is_frightened = True

    def unset_frightened(self):
        self.is_frightened = False

    @abstractmethod
    def reset_image(self):
        pass
