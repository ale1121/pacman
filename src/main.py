import pygame

from blinky import Blinky
from clyde import Clyde
from pinky import Pinky
from inky import Inky
from pacman import Pacman
from map import Map
from animation import SpriteSheet
import button

pygame.init()

CELL_SIZE = 24
BORDER = 2 * CELL_SIZE
PACMAN_SPEED = 4

clock = pygame.time.Clock()

# set up the game window
screen_width = 32 * CELL_SIZE + 2 * BORDER
screen_height = 31 * CELL_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pacman")

# initialise the game map
map_file = "assets/map/map.txt"
map_image = pygame.image.load("assets/map/map.png")
game_map = Map(map_file, map_image)

# create buttons and ui elements
resume_img = pygame.image.load("assets/ui/resume_button.png")
resume_button = button.Button(screen_width / 2, screen_height / 2 - 60, resume_img)

quit_img = pygame.image.load("assets/ui/quit_button.png")
quit_button = button.Button(screen_width / 2, screen_height / 2 + 60, quit_img)
quit_button_end = button.Button(screen_width / 2 - 2, screen_height / 2 - 25, quit_img)

start_img = pygame.image.load("assets/ui/start_button.png")
start_button = button.Button(screen_width / 2, screen_height / 2 + 70, start_img)

pause_screen_img = pygame.image.load("assets/ui/pause_screen.png")

font_file = "assets/ui/font.ttf"
font25 = pygame.font.Font(font_file, 25)

# create characters
pacman = Pacman(screen_width / 2 - BORDER, 23 * CELL_SIZE + 12, PACMAN_SPEED)

blinky = Blinky(screen_width / 2 - 36 - BORDER, 11 * CELL_SIZE + 12, 0)
inky = Inky(screen_width / 2 - 36 - 2 * CELL_SIZE - BORDER, 11 * CELL_SIZE + 12, 0, blinky)
pinky = Pinky(screen_width / 2 - 36 + 3 * CELL_SIZE - BORDER, 11 * CELL_SIZE + 12, 0)
clyde = Clyde(screen_width / 2 - 36 + 5 * CELL_SIZE - BORDER, 11 * CELL_SIZE + 12, 0)

ghosts = pygame.sprite.Group()
ghosts.add(blinky)
ghosts.add(pinky)
ghosts.add(clyde)
ghosts.add(inky)

lives = 3
levels = 3
level = 1  # starting level

paused = False
run = True  # the program stays active while this variable is True

turns_frightened = -1


def draw_text(text, size, color, position, font=None):
    if font is None:
        font = pygame.font.Font(font_file, size)
    img = font.render(text, True, color)
    screen.blit(img, position)


# checks whether the game should continue running
def check_end():
    global paused
    key = pygame.key.get_pressed()

    # if space was pressed, pause
    if key[pygame.K_SPACE]:
        paused = True

    # check for quit
    if key[pygame.K_ESCAPE]:
        return False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


# reset all characters to their initial state and position
def restart_round():
    pacman.go_to_start()
    for ghost in ghosts:
        ghost.turns_sleep = 0
        ghost.unset_frightened()
        ghost.reset_image()
        ghost.go_to_start()


# this function is called after a level is completed or the player has lost all lives
def end_level(win):
    global run, level

    if win:
        # the player has successfully finished the current level
        screen.fill("black")
        img = SpriteSheet("assets/animations/map_win.png", 768, 744)
        img.animate(screen, (BORDER, 0), 200)
        screen.fill("black")
        print_game()
        level += 1  # advance to the next level
        if level <= levels:
            # initialise and start the next level
            init_level()
            print_game()
            draw_text("Level " + str(level), 30, "white", (screen_width / 2 - 65, 16 * CELL_SIZE + 18))
            pygame.display.update()
            pygame.time.delay(2000)
            play()
            return
        # the player has completed all the levels and won the game
        draw_text("CONGRATULATIONS!", 30, "green", (screen_width / 2 - 170, 16 * CELL_SIZE + 18))
    else:
        # the player has no more lives left and lost the game
        screen.fill("black")
        print_game()
        draw_text("GAME OVER", 30, "red", (screen_width / 2 - 99, 16 * CELL_SIZE + 18))
    pygame.display.update()
    pygame.time.delay(1500)

    # display quit button
    while run:
        run = check_end()
        if quit_button_end.draw(screen):
            run = False
        pygame.display.update()


# called when pacman collides with a ghost while in power mode
def eat_ghost(ghost):
    # display the points earned by eating the ghost
    ghosts.remove(ghost)
    print_game()
    draw_text(str(pacman.powerup_score), 20, "cyan", ghost.rect)
    pygame.display.update()
    pygame.time.delay(600)
    ghosts.add(ghost)

    # increase the current score
    pacman.score += pacman.powerup_score
    # the next ghost eaten will provide double the points
    pacman.powerup_score *= 2

    # reset ghost
    ghost.unset_frightened()
    ghost.go_to_start()
    ghost.reset_image()
    ghost.path = ghost.get_position_in_labyrinth()
    ghost.turns_sleep = 300  # 5 seconds


# called when pacman collides with a ghost in regular mode
def lose_life():
    global lives

    # animation
    screen.fill((0, 0, 0))
    screen.blit(game_map.image, (BORDER, 0))
    img = SpriteSheet("assets/animations/pacman_die.png", 45, 45)
    img.animate(screen, (BORDER + pacman.rect.x - 8, pacman.rect.y - 9), 100)

    lives -= 1
    if lives == 0:
        # there are no more lives left and the game was lost
        end_level(False)
        return

    restart_round()
    print_game()
    pygame.display.update()
    pygame.time.delay(1000)


def print_lives():
    pacman_img = pygame.image.load("assets/characters/pacman.png")
    for i in range(lives):
        screen.blit(pacman_img, (33 * CELL_SIZE, 29 * CELL_SIZE - 2 * i * CELL_SIZE))


def print_game():
    screen.fill((0, 0, 0))
    screen.blit(game_map.image, (BORDER, 0))
    for pellet in game_map.pellets:
        pellet.draw(screen)
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)
    print_lives()
    draw_text(str(pacman.score), 0, "white", (32 * CELL_SIZE + 10, 2), font25)


# contains the main game loop
def play():
    global run, paused, turns_frightened
    while run:
        clock.tick(60)
        run = check_end()  # check for pause or end

        # check ghosts frightened status
        if turns_frightened == 60:
            for ghost in ghosts:
                if ghost.is_frightened:
                    ghost.image = pygame.image.load("assets/characters/frightened_ghost_timeout.png").convert_alpha()
        if turns_frightened == 0:
            for ghost in ghosts:
                if ghost.is_frightened:
                    ghost.reset_image()
                    ghost.unset_frightened()
            turns_frightened = -1
        elif turns_frightened > 0:
            turns_frightened -= 1

        if paused:
            # display pause screen
            screen.blit(pause_screen_img, (screen_width / 2 - 180, screen_height / 2 - 225))
            if resume_button.draw(screen):
                paused = False
            if quit_button.draw(screen):
                run = False
        else:
            # check for collisions between pacman and ghosts
            for ghost in ghosts:
                if pygame.sprite.spritecollide(pacman, [ghost], False):
                    if ghost.is_frightened:
                        eat_ghost(ghost)
                    else:
                        lose_life()
                        break

            # update all characters
            ghosts.update(game_map, pacman)
            if pacman.update(game_map):
                pacman.powerup_score = 200
                for ghost in ghosts:
                    ghost.get_frightened()
                turns_frightened = 300
            print_game()

            if len(game_map.pellets) == 0:
                # the level was cleared
                end_level(True)

        pygame.display.update()


# reset the game map and increase ghost speed
def init_level():
    global game_map, level, lives
    for ghost in ghosts:
        ghost.speed = level + 1
        ghost.unset_frightened()
        ghost.go_to_start()
        ghost.reset_image()
        ghost.path = ghost.get_position_in_labyrinth()
    pacman.go_to_start()
    game_map = Map(map_file, map_image)


# displays the game map and waits for the user to start the game
def wait_to_start():
    global run
    while run:
        run = check_end()
        print_game()
        draw_text("Press any key to start", 17, "yellow", (screen_width / 2 - 130, 16 * CELL_SIZE + 24))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                init_level()
                play()
        pygame.display.update()


def start_screen():
    global run

    # title screen animations
    pacman_animation = SpriteSheet("assets/animations/pacman.png", 264, 78)
    pacman_animation.animate(screen, (screen_width / 2 - 132, screen_height / 2 - 39), 20)
    title_animation = SpriteSheet("assets/animations/title.png", 512, 256)
    title_animation.animate(screen, (screen_width / 2 - 256, screen_height / 2 - 158), 150)

    title = pygame.image.load("assets/ui/title.png")

    # display instructions
    with open("assets/ui/help.txt", 'r') as file:
        help_txt = file.read()
    draw_text(help_txt, 15, "white", (20, screen_height - 30))

    while run:
        # wait for the user to start or quit the game

        run = check_end()

        screen.blit(title, (screen_width / 2 - 256, screen_height / 2 - 158))
        if start_button.draw(screen):
            wait_to_start()

        pygame.display.update()


def main():
    start_screen()


if __name__ == "__main__":
    main()
