import pygame

from character import Character

CELL_SIZE = 24
BORDER = 2 * CELL_SIZE


def add_cell(matrix, i, j, surrounding_cells, _type):
    if matrix[i][j] is not None and matrix[i][j].type == _type:
        surrounding_cells.add(matrix[i][j])


# creates a sprite group containing all the elements of a given type surrounding the given rect
def get_surrounding_cells(matrix, rect, _type, check_corners):
    (i, j) = (rect.y // 24, rect.x // 24)
    surrounding_cells = pygame.sprite.Group()
    add_cell(matrix, i, j, surrounding_cells, _type)
    add_cell(matrix, i - 1, j, surrounding_cells, _type)
    add_cell(matrix, i + 1, j, surrounding_cells, _type)
    add_cell(matrix, i, j - 1, surrounding_cells, _type)
    add_cell(matrix, i, j + 1, surrounding_cells, _type)
    if check_corners:
        add_cell(matrix, i - 1, j - 1, surrounding_cells, _type)
        add_cell(matrix, i - 1, j + 1, surrounding_cells, _type)
        add_cell(matrix, i + 1, j - 1, surrounding_cells, _type)
        add_cell(matrix, i + 1, j + 1, surrounding_cells, _type)
    return surrounding_cells


# returns true if the given rect collides with any of the walls around it
def check_wall_collision(rect, map_matrix):
    surrounding_walls = get_surrounding_cells(map_matrix, rect, "wall", True)
    return [wall for wall in surrounding_walls if rect.colliderect(wall.rect)]


# if the rect collides with one of the surrounding pellets, return that pellet
def check_pellet_collision(rect, pellet_matrix):
    surrounding_cells = get_surrounding_cells(pellet_matrix, rect, "pellet", False)
    for pellet in surrounding_cells:
        if rect.colliderect(pellet.rect):
            return pellet
    return None


class Pacman(Character):
    def __init__(self, x, y, speed):
        Character.__init__(self, "assets/characters/pacman.png", x, y, speed)

        self.next_direction = (0, 0)
        self.score = 0
        self.powerup_score = 200

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image_up = pygame.transform.rotate(self.image_left, -90)
        self.image_down = pygame.transform.flip(self.image_up, False, True)
        self.next_image = self.image_left

    def update(self, game_map):
        # set the direction based on user input
        key = pygame.key.get_pressed()

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.next_direction = (-self.speed, 0)
            self.next_image = self.image_left
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.next_direction = (self.speed, 0)
            self.next_image = self.image_right
        elif key[pygame.K_w] or key[pygame.K_UP]:
            self.next_direction = (0, -self.speed)
            self.next_image = self.image_up
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.next_direction = (0, self.speed)
            self.next_image = self.image_down

        return self.advance(game_map)

    # advance to the next position. returns True if pacman eats a power pellet
    def advance(self, game_map):
        power_up = False

        # check if pacman can move in the new direction given by the user
        new_rect = self.rect.move(self.next_direction)
        if not check_wall_collision(new_rect, game_map.matrix):
            # update pacman's position and set the new direction as the current direction
            self.rect.center = new_rect.center
            self.direction = self.next_direction
            self.image = self.next_image
        else:
            # if the new direction is not available, try to continue moving in the current direction.
            new_rect = self.rect.move(self.direction)
            if not check_wall_collision(new_rect, game_map.matrix):
                self.rect.center = new_rect.center

        pellet = check_pellet_collision(self.rect, game_map.pellet_matrix)
        if pellet is not None:
            # if a pellet was hit, add the points and remove the pellet from the map
            self.score += pellet.points
            pellet.kill()
            game_map.pellet_matrix[pellet.rect.y // 24][pellet.rect.x // 24] = None
            if pellet.gives_powers:
                power_up = True

        # if pacman reaches a tunnel, teleport to the opposite tunnel
        if self.rect.colliderect(game_map.left_tunnel):
            self.rect.midright = game_map.right_tunnel.rect.midleft

        if self.rect.colliderect(game_map.right_tunnel):
            self.rect.midleft = game_map.left_tunnel.rect.midright

        return power_up

    def draw(self, surface):
        surface.blit(self.image, (BORDER + self.rect.x - 8, self.rect.y - 8))

    def go_to_start(self):
        self.rect.center = self.start_position
        self.direction = (0, 0)
        self.next_direction = (0, 0)
