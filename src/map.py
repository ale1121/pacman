import pygame

from wall import Wall, Tunnel
from pellets import SmallPellet, PowerPellet

CELL_SIZE = 24
BORDER = 2 * CELL_SIZE


# reads the map matrix from the given file
def read_map(map_file):
    with open(map_file, 'r') as file:
        map_lines = file.readlines()

    map_matrix = [list(line.strip()) for line in map_lines]
    return map_matrix


class Map:
    def __init__(self, map_file, image):
        self.image = image
        self.matrix = []
        self.left_tunnel = pygame.sprite.Sprite()
        self.right_tunnel = pygame.sprite.Sprite()
        self.pellets = pygame.sprite.Group()
        self.pellet_matrix = []
        self.create_map(map_file)
        self.add_pellets(map_file)

    # creates the map by reading the map matrix and adding all the walls
    def create_map(self, map_file):
        map_matrix = read_map(map_file)
        for i in range(len(map_matrix)):
            row = []
            for j in range(len(map_matrix[i])):
                row.append(self.create_object(map_matrix[i][j], i, j))
            self.matrix.append(row)

    def create_object(self, symbol, i, j):
        if symbol == '#':
            new_object = Wall(j, i)
        elif symbol == 'X':
            if j == 0:
                new_object = Tunnel(j, i)
                self.left_tunnel = new_object
            else:
                new_object = Tunnel(j, i)
                self.right_tunnel = new_object
        else:
            new_object = None
        return new_object

    def add_pellets(self, map_file):
        map_matrix = read_map(map_file)
        for i in range(len(map_matrix)):
            row = []
            for j in range(len(map_matrix[i])):
                if map_matrix[i][j] == '.':
                    pellet = SmallPellet(j, i)
                    self.pellets.add(pellet)
                elif map_matrix[i][j] == 'o':
                    pellet = PowerPellet(j, i)
                    self.pellets.add(pellet)
                else:
                    pellet = None
                row.append(pellet)
            self.pellet_matrix.append(row)
