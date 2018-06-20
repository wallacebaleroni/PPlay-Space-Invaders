from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.collision import *

import random


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

DIF_EASY = 3
DIF_MEDI = 4
DIF_HARD = 5

LEFT = -1
RIGHT = 1

UP = -1
DOWN = 1


def main():
    game_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    game_window.set_title("Minimalist Space Invaders")

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

    click_cooldown_time = 0.75
    total_time = 0
    last_click = 0

    # Main menu loop
    while True:
        if mouse_input.is_over_object(bt_play):
            bt_play.set_curr_frame(1)
            if mouse_input.is_button_pressed(1) and total_time - last_click > click_cooldown_time:
                game(difficulty, 0)
                last_click = total_time
        else:
            bt_play.set_curr_frame(0)
        if mouse_input.is_over_object(bt_difficulty) and mouse_input.is_button_pressed(1) and total_time - last_click > click_cooldown_time:
            difficulty = menu_difficulty()
            last_click = total_time
        if mouse_input.is_over_object(bt_ranking) and mouse_input.is_button_pressed(1) and total_time - last_click > click_cooldown_time:
            print("Ranking")
            last_click = total_time
        if mouse_input.is_over_object(bt_exit) and mouse_input.is_button_pressed(1) and total_time - last_click > click_cooldown_time:
            return

        background.draw()
        bt_play.draw()
        bt_difficulty.draw()
        bt_ranking.draw()
        bt_exit.draw()

        game_window.update()

        delta_time = game_window.delta_time()
        total_time += delta_time


def game(difficulty, score):
    p_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    p_window.set_title("Minimalist Space Invaders")
    p_window.update()

    background = GameImage("../img/background_game.png")

    spaceship = Sprite("../img/spaceship.png")
    spaceship.set_position(50, WINDOW_HEIGHT - 50)

    spaceship_speed = 2 * BASE_SPEED

    shots = []
    shot_speed = 4 * BASE_SPEED

    enemies_shots = []

    lives = 3

    # create enemies
    enemies, alive_enemies = create_monsters(6, 2)
    if enemies is None:
        return

    enemy_speed = 1.5
    enemy_dir_x = RIGHT
    enemy_dir_y = DOWN

    kb = Keyboard()

    shot_time = 0.1 * difficulty
    super_shot_time = 1
    total_time = 0
    last_shot_time = 0
    last_enemy_move = 0
    last_enemy_shot = 0
    shot_charging = False
    current_charging_time = 0
    charging_time = 1.5

    enemy_shot_cooldown = 1
    jafoi = False

    while True:
        # spaceship move
        if kb.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_SIZE_X <= WINDOW_WIDTH:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)
        elif kb.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)

        if total_time - last_shot_time >= super_shot_time and not jafoi and current_charging_time > charging_time:
            print("Pode soltar")
            jafoi = True

        if kb.key_pressed("SPACE"):
            shot_charging = True
            current_charging_time += delta_time
        elif shot_charging:
            jafoi = False
            if total_time - last_shot_time >= super_shot_time and current_charging_time > charging_time:
                new_shot = Shot(spaceship.x, spaceship.y, True)
                shots.append(new_shot)
                last_shot_time = total_time
            elif total_time - last_shot_time >= shot_time:
                new_shot = Shot(spaceship.x, spaceship.y, False)
                shots.append(new_shot)
                last_shot_time = total_time
            shot_charging = False
            current_charging_time = 0

        if kb.key_pressed("ESC"):
            return

        # update enemies positions
        if total_time - last_enemy_move > enemy_speed:
            enemy_dir_x, enemy_dir_y = move_monsters(enemies, enemy_dir_x, enemy_dir_y)
            last_enemy_move = total_time

        # update shots positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * delta_time)
            if shot.y <= 0 - SHOT_SIZE_Y:
                shots.remove(shot)

        # creates monsters shots
        if total_time - last_enemy_shot > enemy_shot_cooldown:
            # count how many alive
            total = 0
            for i in range(len(enemies)):
                total += alive_enemies[i].count(1)
            chosen = random.randint(0, total)

            # makes the chosen shoot
            it = 0
            for i in range(len(enemies)):
                for j in range(len(enemies[0])):
                    if alive_enemies[i][j] == 1:
                        if it == chosen:
                            new_shot = Sprite("../img/shot.png")
                            new_shot.set_position(enemies[i][j].x + ENEMY_WIDTH / 2, enemies[i][j].y)
                            enemies_shots.append(new_shot)
                        it += 1

            last_enemy_shot = total_time

        # updates monsters shots positions
        for shot in enemies_shots:
            shot.set_position(shot.x, shot.y + shot_speed * delta_time)
            if shot.y <= 0 - SHOT_SIZE_Y:
                shots.remove(shot)

        # check spaceship shot collisions
        for shot in shots:
            for i in range(len(enemies)):
                for j in range(len(enemies[0])):
                    if alive_enemies[i][j] == 1:
                        if Collision.collided(shot.sprite, enemies[i][j]):
                            alive_enemies[i][j] = 0
                            score += difficulty * 10
                            if not shot.loaded:
                                shots.remove(shot)

        # check enemies shot collisions
        for shot in enemies_shots:
            if Collision.collided(shot, spaceship):
                lives -= 1
                enemies_shots.remove(shot)

        # check end of the game
        if everyone_dead(alive_enemies):
            print("YOU WIN")
            print("Now the difficulty is: ", end="")
            if difficulty == 1:
                print("easy")
            if difficulty == 2:
                print("medium")
            for i in range(3, difficulty):
                print("very", end=" ")
            if difficulty >= 3:
                print("hard")
            game(difficulty + 1, score)
            return
        if lives == 0:
            print("YOU LOST")
            return

        background.draw()
        spaceship.draw()
        p_window.draw_text(str(score), 0, 0, color=(255, 255, 255))
        p_window.draw_text(str(lives), WINDOW_WIDTH - 10, 0, color=(255,255,255))
        for shot in shots:
            shot.draw()
        for shot in enemies_shots:
            shot.draw()
        draw_monsters(enemies, alive_enemies)
        p_window.update()

        delta_time = p_window.delta_time()
        total_time += delta_time


def menu_difficulty():
    game_window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game_window.set_title("Minimalist Space Invaders")

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
    alive = []
    for i in range(h):
        e_line = []
        a_line = []
        for j in range(w):
            enemy = Sprite("../img/enemy.png")
            enemy.set_position(ENEMY_START_POS_X + j * (ENEMY_WIDTH + ENEMY_SPACING_X),
                               ENEMY_START_POS_Y + i * (ENEMY_HEIGHT + ENEMY_SPACING_Y))
            e_line.append(enemy)
            a_line.append(1)
        enemies.append(e_line)
        alive.append(a_line)

    return enemies, alive


def draw_monsters(enemies, alive):
    for i in range(len(enemies)):
        for j in range(len(enemies[0])):
            if alive[i][j] == 1:
                enemies[i][j].draw()


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


def everyone_dead(alive):
    for linha in alive:
        for a in linha:
            if a == 1:
                return False
    return True


class Shot:
    def __init__(self, s_pos_x, s_pos_y, loaded):
        self.x = s_pos_x + SPACESHIP_SIZE_X / 2
        self.y = s_pos_y - SHOT_SIZE_Y

        self.loaded = loaded
        if loaded:
            self.sprite = Sprite("../img/sshot.png")
            self.x = s_pos_x + SPACESHIP_SIZE_X / 2 - 5
            self.y = s_pos_y - SHOT_SIZE_Y
        else:
            self.sprite = Sprite("../img/shot.png")
            self.x = s_pos_x + SPACESHIP_SIZE_X / 2
            self.y = s_pos_y - SHOT_SIZE_Y
        self.sprite.set_position(self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.sprite.set_position(x, y)

    def draw(self):
        self.sprite.draw()


main()
