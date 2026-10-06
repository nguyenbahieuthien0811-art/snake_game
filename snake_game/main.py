# main.py--

### Imports ###
import sys 
from random import choice, randint
from time import sleep

import pygame as pg 
pg.init()



### Data ###

game_over = False

SCR_WIDTH = 900
SCR_HEIGHT = 700

FPS = 60

TILE_SIZE = 20

GRID_WIDTH = SCR_WIDTH // TILE_SIZE
GRID_HEIGHT = SCR_HEIGHT // TILE_SIZE
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (100, 220, 100)
DARK_GREEN = (70, 170, 70)
RED = (220, 60, 60)
GRAY = (100, 100, 100)

SNAKE_SPEED = 8  # Number of frames between snake moves

MOVE_DELAY = 1000 // SNAKE_SPEED  # Delay in seconds between snake moves

last_move = 0

score = 0

game_state = "menu"  # Possible states: "menu", "playing", "game_over"

font = pg.font.Font(None, 32)
big_font = pg.font.Font(None, 64)

### Window set up

# This is where we create our main window object and setup its params
mw = pg.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pg.display.set_caption("Block Control Demo")
clock = pg.time.Clock()

### Classes
class snake(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.body = [
            [10, 10],
            [9, 10],
            [8, 10],
        ]

        self.direction = (1, 0)  # Start moving to the right
        self.next_direction = (1, 0)  # Next direction to move

        self.grow = False  # Flag to indicate if the snake should grow

    def change_direction(self, direction):
        if direction == (1, 0) and self.direction == (-1, 0):
            return

        if direction == (-1, 0) and self.direction == (1, 0):
            return

        if direction == (0, 1) and self.direction == (0, -1):
            return

        if direction == (0, -1) and self.direction == (0, 1):
            return

        self.next_direction = direction

    def move(self):

        self.direction = self.next_direction

        head_x = self.body[0][0]
        head_y = self.body[0][1]

        direction_x = self.direction[0]
        direction_y = self.direction[1]

        new_head = [
            head_x + direction_x,
            head_y + direction_y
        ]  

        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False  # Reset the grow flag after growing
        else:
            self.body.pop()  # Remove the last segment if not growing

    def grow_snake(self):

        self.grow = True

    def wrap_around(self):

        if self.body[0][0] < 0:

            self.body[0][0] = GRID_WIDTH - 1

        elif self.body[0][0] >= GRID_WIDTH:

            self.body[0][0] = 0

        if self.body[0][1] < 0:

            self.body[0][1] = GRID_HEIGHT - 1

        elif self.body[0][1] >= GRID_HEIGHT:

            self.body[0][1] = 0

    def check_self_collision(self):

        head = self.body[0]

        if head in self.body[1:]:

            return True

        return False

    def update_rect(self):

        self.rect.topleft = (
            self.body[0][0] * TILE_SIZE,
            self.body[0][1] * TILE_SIZE
        )

    def draw(self, screen):

        for part in self.body:

            x = part[0] * TILE_SIZE
            y = part[1] * TILE_SIZE

            rect = pg.Rect(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE
            )

            pg.draw.rect(
                screen,
                GREEN,
                rect,
                border_radius=5
            )

        head = self.body[0]

        head_rect = pg.Rect(
            head[0] * TILE_SIZE,
            head[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        pg.draw.rect(
            screen,
            DARK_GREEN,
            head_rect,
            border_radius=6
        )

        self.update_rect()

class food(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pg.Surface(
            (TILE_SIZE, TILE_SIZE),
            pg.SRCALPHA
        )

        pg.draw.circle(
            self.image,
            RED,
            (TILE_SIZE // 2, TILE_SIZE // 2),
            7
        )

        self.rect = self.image.get_rect()

        self.position = (0, 0)

    def spawn(self, snake_body):

        while True:

            x = randint(
                0,
                GRID_WIDTH - 1
            )

            y = randint(
                0,
                GRID_HEIGHT - 1
            )

            if [x, y] not in snake_body:

                self.position = (x, y)

                break

        self.rect.topleft = (
            self.position[0] * TILE_SIZE,
            self.position[1] * TILE_SIZE
        )

class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text
    ):

        self.rect = pg.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

    def draw(self, screen):

        pg.draw.rect(
            screen,
            GREEN,
            self.rect,
            border_radius=10
        )

        text_surface = font.render(
            self.text,
            True,
            BLACK
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    def clicked(self, position):

        return self.rect.collidepoint(position)


### Functions ###

def check_quit(event):
    if event.type == pg.QUIT:
        return True
def draw_text(
    text,
    font_used,
    color,
    x,
    y,
    center=True
):

    text_surface = font_used.render(
        text,
        True,
        color
    )

    if center:

        text_rect = text_surface.get_rect(
            center=(x, y)
        )

    else:

        text_rect = text_surface.get_rect(
            topleft=(x, y)
        )

    mw.blit(
        text_surface,
        text_rect
    )


def reset_game():

    global player
    global apple
    global score
    global SNAKE_SPEED
    global MOVE_DELAY
    global last_move

    player = snake()

    apple = food()

    apple.spawn(
        player.body
    )

    score = 0

    SNAKE_SPEED = 8

    MOVE_DELAY = 1000 // SNAKE_SPEED

    last_move = pg.time.get_ticks()


def increase_speed():

    global SNAKE_SPEED
    global MOVE_DELAY

    if SNAKE_SPEED < 20:

        SNAKE_SPEED += 0.25

        MOVE_DELAY = 1000 // SNAKE_SPEED


def start_game():

    global game_state

    reset_game()

    game_state = "playing"


def draw_menu():

    mw.fill(BLACK)

    draw_text(
        "CLASSIC SNAKE",
        big_font,
        GREEN,
        SCR_WIDTH // 2,
        220
    )


    start_button.draw(mw)

    draw_text(
        "WASD / Arrow Keys to move",
        font,
        WHITE,
        SCR_WIDTH // 2,
        470
    )

    draw_text(
        "SPACE to pause",
        font,
        WHITE,
        SCR_WIDTH // 2,
        510
    )


def draw_pause():

    draw_text(
        "PAUSED",
        big_font,
        WHITE,
        SCR_WIDTH // 2,
        SCR_HEIGHT // 2 - 30
    )

    draw_text(
        "Press SPACE to continue",
        font,
        WHITE,
        SCR_WIDTH // 2,
        SCR_HEIGHT // 2 + 30
    )


def draw_game_over():

    mw.fill(BLACK)

    draw_text(
        "GAME OVER",
        big_font,
        RED,
        SCR_WIDTH // 2,
        240
    )

    draw_text(
        "Score: " + str(score),
        font,
        WHITE,
        SCR_WIDTH // 2,
        320
    )

    draw_text(
        "Press R to restart",
        font,
        GREEN,
        SCR_WIDTH // 2,
        390
    )

    draw_text(
        "Press ESC to quit",
        font,
        WHITE,
        SCR_WIDTH // 2,
        440
    )


def draw_game():

    mw.fill(BLACK)

    player.draw(mw)

    mw.blit(
        apple.image,
        apple.rect
    )

    draw_text(
        "Score: " + str(score),
        font,
        WHITE,
        15,
        15,
        False
    )


def check_food():

    global score

    if player.body[0] == list(apple.position):

        player.grow_snake()

        apple.spawn(
            player.body
        )

        score += 1

        increase_speed()

### Sprite and Groups ###

snake_group = pg.sprite.Group()

food_group = pg.sprite.Group()

player = snake()

apple = food()

apple.spawn(
    player.body
)

snake_group.add(
    player
)

food_group.add(
    apple
)

start_button = Button(
    SCR_WIDTH // 2 - 100,
    340,
    200,
    60,
    "START GAME"
)

### Game Loop ###

while not game_over:

    #- Events

    for event in pg.event.get():

        if check_quit(event):

            game_over = True

        if game_state == "menu":

            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if start_button.clicked(
                        event.pos
                    ):

                        start_game()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_RETURN:

                    start_game()

                elif event.key == pg.K_ESCAPE:

                    game_over = True


        elif game_state == "playing":

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_UP or event.key == pg.K_w:

                    player.change_direction(
                        (0, -1)
                    )

                elif event.key == pg.K_DOWN or event.key == pg.K_s:

                    player.change_direction(
                        (0, 1)
                    )

                elif event.key == pg.K_LEFT or event.key == pg.K_a:

                    player.change_direction(
                        (-1, 0)
                    )

                elif event.key == pg.K_RIGHT or event.key == pg.K_d:

                    player.change_direction(
                        (1, 0)
                    )

                elif event.key == pg.K_SPACE:

                    game_state = "paused"

                elif event.key == pg.K_ESCAPE:

                    game_state = "menu"


        elif game_state == "paused":

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:

                    game_state = "playing"

                elif event.key == pg.K_ESCAPE:

                    game_state = "menu"


        elif game_state == "game_over":

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_r:

                    start_game()

                elif event.key == pg.K_ESCAPE:

                    game_over = True


    #- Update

    if game_state == "playing":

        current_time = pg.time.get_ticks()

        if current_time - last_move >= MOVE_DELAY:

            player.move()

            player.wrap_around()

            check_food()

            if player.check_self_collision():

                game_state = "game_over"

            last_move = current_time


    ### Draw ###

    if game_state == "menu":

        draw_menu()

    elif game_state == "playing":

        draw_game()

    elif game_state == "paused":

        draw_game()

        draw_pause()

    elif game_state == "game_over":

        draw_game_over()


    pg.display.flip()

    clock.tick(FPS)


sleep(1)

pg.quit()

sys.exit()




