from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 70

SHOT_SIZE_X = 4
SHOT_SIZE_Y = 14

SPACESHIP_SIZE_X = 42
SPACESHIP_SIZE_Y = 42

BASE_SPEED = 100

ENEMY_WIDTH = 25
ENEMY_HEIGHT = 25

ENEMY_START_POS_X = 25
ENEMY_START_POS_Y = 25

ENEMY_SPACING_X = ENEMY_WIDTH
ENEMY_SPACING_Y = ENEMY_HEIGHT

BUTTON_BORDER = 30
BUTTON_SPACING = 20

DIF_EASY = 1
DIF_MEDI = 2
DIF_HARD = 3

LEFT = -1
RIGHT = 1

UP = -1
DOWN = 1


def main():
    game_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    mouse_input = Mouse()

    background = GameImage("../img/background_menu.jpg")

    bt_play = Sprite("../img/play.png", 2)
    bt_difficulty = Sprite("../img/difficulty.png", 1)
    bt_ranking = Sprite("../img/ranking.png", 1)
    bt_exit = Sprite("../img/quit.png", 1)
    bt_play.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER)
    bt_difficulty.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING))
    bt_ranking.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING) * 2)
    bt_exit.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING) * 3)

    difficulty = DIF_EASY

    while True:
        if mouse_input.is_over_object(bt_play):
            bt_play.set_curr_frame(1)
            if mouse_input.is_button_pressed(1):
                game(difficulty)
        else:
            bt_play.set_curr_frame(0)
        if mouse_input.is_over_object(bt_difficulty) and mouse_input.is_button_pressed(1):
            difficulty = menu_difficulty()
        if mouse_input.is_over_object(bt_ranking) and mouse_input.is_button_pressed(1):
            print("Ranking")
        if mouse_input.is_over_object(bt_exit) and mouse_input.is_button_pressed(1):
            return

        background.draw()
        bt_play.draw()
        bt_difficulty.draw()
        bt_ranking.draw()
        bt_exit.draw()

        game_window.update()


def game(difficulty):
    p_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    p_window.set_title("Space Invaders")
    p_window.update()

    background = GameImage("../img/background_game.png")

    spaceship = Sprite("../img/spaceship.png")
    spaceship.set_position(50, WINDOW_HEIGHT - 50)

    spaceship_speed = 2 * BASE_SPEED

    shots = []
    shot_speed = 4 * BASE_SPEED

    # create enemies
    enemies = create_monsters(6, 2)
    if enemies is None:
        return

    enemy_speed = 1.5
    enemy_dir_x = RIGHT
    enemy_dir_y = DOWN

    kb = Keyboard()

    shot_time = 0.1 * difficulty
    total_time = 0
    last_shot_time = 0
    last_enemy_move = 0

    while True:
        # spaceship move
        if kb.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_SIZE_X <= WINDOW_WIDTH:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)
        elif kb.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)
        if kb.key_pressed("SPACE"):
            if total_time - last_shot_time >= shot_time:
                new_shot = Sprite("../img/shot.png")
                new_shot.set_position(spaceship.x + SPACESHIP_SIZE_X / 2, spaceship.y - SHOT_SIZE_Y)
                shots.append(new_shot)
                last_shot_time = total_time
        elif kb.key_pressed("ESC"):
            return

        # update shots positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * delta_time)
            if shot.y <= 0 - SHOT_SIZE_Y:
                shots.remove(shot)

        # update enemies positions
        if total_time - last_enemy_move > enemy_speed:
            enemy_dir_x, enemy_dir_y = move_monsters(enemies, enemy_dir_x, enemy_dir_y)
            last_enemy_move = total_time

        background.draw()
        spaceship.draw()
        for shot in shots:
            shot.draw()
        draw_monsters(enemies)
        p_window.update()

        delta_time = p_window.delta_time()
        total_time += delta_time


def menu_difficulty():
    game_window = Window(600, 400)

    mouse_input = Mouse()

    background = GameImage("../img/background_menu.jpg")

    bt_easy = Sprite("../img/easy.png", 1)
    bt_medium = Sprite("../img/medium.png", 1)
    bt_hard = Sprite("../img/hard.png", 1)
    bt_easy.set_position(175, 63)
    bt_medium.set_position(175, 156)
    bt_hard.set_position(175, 250)

    while True:
        if mouse_input.is_over_object(bt_easy) and mouse_input.is_button_pressed(1):
            return DIF_EASY
        if mouse_input.is_over_object(bt_medium) and mouse_input.is_button_pressed(1):
            return DIF_MEDI
        if mouse_input.is_over_object(bt_hard) and mouse_input.is_button_pressed(1):
            return DIF_HARD

        background.draw()
        bt_easy.draw()
        bt_medium.draw()
        bt_hard.draw()

        game_window.update()


def create_monsters(w, h):
    if w * ENEMY_WIDTH + (w - 1) * ENEMY_SPACING_X > WINDOW_WIDTH * 2 / 3 + ENEMY_START_POS_X:
        print("Too much enemies")
        return None
    enemies = []
    for i in range(h):
        line = []
        for j in range(w):
            enemy = Sprite("../img/enemy.png")
            enemy.set_position(ENEMY_START_POS_X + j * (ENEMY_WIDTH + ENEMY_SPACING_X),
                               ENEMY_START_POS_Y + i * (ENEMY_HEIGHT + ENEMY_SPACING_Y))
            line.append(enemy)
        enemies.append(line)
    return enemies


def draw_monsters(enemies):
    for line in enemies:
        for enemy in line:
            if enemy is not None:
                enemy.draw()


def move_monsters(enemies, enemy_dir_x, enemy_dir_y):
    enemy_step_x = ENEMY_WIDTH + ENEMY_SPACING_X
    enemy_step_y = ENEMY_HEIGHT + ENEMY_SPACING_Y

    if (((enemies[0][len(enemies[0]) - 1].x + ENEMY_WIDTH) + (enemy_step_x * enemy_dir_x) >= WINDOW_WIDTH - ENEMY_START_POS_X)
        or (enemies[0][0].x + (enemy_step_x * enemy_dir_x) < ENEMY_START_POS_X)):
        for line in enemies:
            for enemy in line:
                enemy.set_position(enemy.x, enemy.y + enemy_step_y * enemy_dir_y)
        enemy_dir_x = 0 - enemy_dir_x
    else:
        for line in enemies:
            for enemy in line:
                enemy.set_position(enemy.x + enemy_step_x * enemy_dir_x, enemy.y)

    return enemy_dir_x, enemy_dir_y



main()
