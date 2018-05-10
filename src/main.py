from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *

WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500

SHOT_SIZE_X = 4
SHOT_SIZE_Y = 14

SPACESHIP_SIZE_X = 42
SPACESHIP_SIZE_Y = 42

BASE_SPEED = 100

ENEMY_SIZE_X = 25
ENEMY_SIZE_Y = 25

ENEMY_START_X = 25
ENEMY_START_Y = 25

ENEMY_SPACING_X = 40
ENEMY_SPACING_Y = 40


def main():
    window = Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
    window.set_title("Space Invaders")

    background = GameImage("img/background.png")

    spaceship = Sprite("img/spaceship.png")
    spaceship.set_position(50, WINDOW_SIZE_Y - 50)

    spaceship_speed = 2 * BASE_SPEED

    shots = []
    shot_speed = 4 * BASE_SPEED

    # create enemies
    enemies = []
    for i in range(2):
        line = []
        for j in range(5):
            enemy = Sprite("img/enemy.png")
            enemy.set_position(ENEMY_START_X + j * (ENEMY_SIZE_X + ENEMY_SPACING_X),ENEMY_START_Y + i * (ENEMY_SIZE_Y + ENEMY_SPACING_Y))
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
    last_shot_time = window.delta_time()
    last_enemy_move = window.delta_time()

    while True:
        time = window.delta_time()
        total_time += time

        # spaceship move
        if kb.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_SIZE_X <= WINDOW_SIZE_X:
                spaceship.set_position(spaceship.x + spaceship_speed * time, spaceship.y)
        elif kb.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * time, spaceship.y)
        if kb.key_pressed("SPACE"):
            if total_time - last_shot_time >= 0.1:
                new_shot = Sprite("img/shot.png")
                new_shot.set_position(spaceship.x + SPACESHIP_SIZE_X / 2, spaceship.y - SHOT_SIZE_Y)
                shots.append(new_shot)
                last_shot_time = total_time
        elif kb.key_pressed("ESC"):
            return

        # update shots positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * time)
            if shot.y <= 0 - SHOT_SIZE_Y:
                shots.remove(shot)

        # update enemies positions
        if total_time - last_enemy_move > 1:
            if enemy_n_of_moves_x > 4:
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
        window.update()

main()