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

ENEMY_SIZE_X = 25
ENEMY_SIZE_Y = 25

ENEMY_START_X = 50
ENEMY_START_Y = 25

ENEMY_SPACING_X = 40
ENEMY_SPACING_Y = 40

BUTTON_BORDER = 30
BUTTON_SPACING = 20


def main():
    game_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    mouse_input = Mouse()

    background = GameImage("../img/background_menu.jpg")

    bt_play = Sprite("../img/jogar.png", 2)
    bt_difficulty = Sprite("../img/dificuldade.png", 1)
    bt_ranking = Sprite("../img/ranking.png", 1)
    bt_exit = Sprite("../img/sair.png", 1)
    bt_play.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER)
    bt_difficulty.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING))
    bt_ranking.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING) * 2)
    bt_exit.set_position(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, BUTTON_BORDER + (BUTTON_HEIGHT + BUTTON_SPACING) * 3)

    while True:
        if mouse_input.is_over_object(bt_play):
            bt_play.set_curr_frame(1)
            if mouse_input.is_button_pressed(1):
                game()
        else:
            bt_play.set_curr_frame(0)
        if mouse_input.is_over_object(bt_difficulty) and mouse_input.is_button_pressed(1):
            menu_difficulty()
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


def game():
    p_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    p_window.set_title("Space Invaders")

    background = GameImage("../img/background_game.png")

    spaceship = Sprite("../img/spaceship.png")
    spaceship.set_position(50, WINDOW_HEIGHT - 50)

    spaceship_speed = 2 * BASE_SPEED

    shots = []
    shot_speed = 4 * BASE_SPEED

    # create enemies
    enemies = []
    for i in range(2):
        line = []
        for j in range(5):
            enemy = Sprite("../img/enemy.png")
            enemy.set_position(ENEMY_START_X + j * (ENEMY_SIZE_X + ENEMY_SPACING_X),
                               ENEMY_START_Y + i * (ENEMY_SIZE_Y + ENEMY_SPACING_Y))
            line.append(enemy)
        enemies.append(line)
    enemy_speed_x = 0.3 * BASE_SPEED
    enemy_speed_y = 0.3 * BASE_SPEED
    enemy_move_x = 1
    enemy_move_y = 0
    enemy_n_of_moves_x = 0
    enemy_n_of_moves_y = 0

    kb = Keyboard()

    total_time = 0
    last_shot_time = p_window.delta_time()
    last_enemy_move = p_window.delta_time()

    while True:
        delta_time = p_window.delta_time()
        total_time += delta_time

        # spaceship move
        if kb.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_SIZE_X <= WINDOW_WIDTH:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)
        elif kb.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)
        if kb.key_pressed("SPACE"):
            if total_time - last_shot_time >= 0.1:
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
        if total_time - last_enemy_move > 1:
            if enemy_n_of_moves_x > 5:
                enemy_n_of_moves_x = 0
                enemy_move_x = 0
                enemy_move_y = 1
            if enemy_n_of_moves_y > 0:
                enemy_speed_x = 0 - enemy_speed_x
                enemy_n_of_moves_y = 0
                enemy_move_x = 1
                enemy_move_y = 0

            if enemy_move_x == 1:
                enemy_n_of_moves_x += 1
            if enemy_move_y == 1:
                enemy_n_of_moves_y += 1
            for line in enemies:
                for enemy in line:
                    enemy.set_position(enemy.x + (enemy_speed_x * enemy_move_x), enemy.y + (enemy_speed_y * enemy_move_y))
            last_enemy_move = total_time

        background.draw()
        spaceship.draw()
        for shot in shots:
            shot.draw()
        for line in enemies:
            for enemy in line:
                if enemy is not None:
                    enemy.draw()
        p_window.update()


def menu_difficulty():
    game_window = Window(600, 400)

    mouse_input = Mouse()

    background = GameImage("../img/background_menu.jpg")

    bt_easy = Sprite("../img/facil.png", 1)
    bt_medium = Sprite("../img/medio.png", 1)
    bt_hard = Sprite("../img/dificil.png", 1)
    bt_easy.set_position(175, 63)
    bt_medium.set_position(175, 156)
    bt_hard.set_position(175, 250)

    while True:
        if mouse_input.is_over_object(bt_easy) and mouse_input.is_button_pressed(1):
            print("Easy")
        if mouse_input.is_over_object(bt_medium) and mouse_input.is_button_pressed(1):
            print("Medium")
        if mouse_input.is_over_object(bt_hard) and mouse_input.is_button_pressed(1):
            print("Hard")

        background.draw()
        bt_easy.draw()
        bt_medium.draw()
        bt_hard.draw()

        game_window.update()


main()
