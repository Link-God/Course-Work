# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

from random import randint, choice
import json
import logging
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}


class Computer:
    def __init__(self):
        self.player_ships = {i: 5 - i for i in range(1, 5, 1)}
        self.alice_ships = {i: 5 - i for i in range(1, 5, 1)}
        self.alice_board = list([0] * 10 for _ in range(10))
        self.was_first_hit = False
        self.was_second_hit = [False, '']
        self.shooting_cords = [0, 0]
        self.strategy = 0
        self.counter = 0
        self.player_counter = 0
        self.player_board = list([0] * 10 for _ in range(10))
        self.create_ships()

    def clear_boar(self):
        for i in range(len(self.alice_board)):
            for j in range(len(self.alice_board[0])):
                if self.alice_board[i][j] == 2:
                    self.alice_board[i][j] = 0
                if self.player_board[i][j] == 2:
                    self.player_board[i][j] = 0

    def create_ships(self, who='alice'):
        ships = [1, 4, 3, 3, 2, 2, 2, 1, 1, 1]
        direction = ('up', 'down', 'right', 'left')
        for ship in ships:
            while True:
                this_direction = choice(direction)
                cords_one = randint(0, 9)
                cords_two = randint(0, 9)
                if self.get_normal_direct(who, this_direction, ship, cords_one, cords_two):
                    break
            self.placed_ship(who, ship, this_direction, cords_one, cords_two)
        self.clear_boar()

    def get_normal_direct(self, who, direction, length, cord1, cord2):
        if who == 'alice':
            board = self.alice_board
        else:
            board = self.player_board
        i = 0
        if direction == 'up' and cord1 - length >= 0:
            while i < length:
                if cord1 - i < 0 or board[cord1 - i][cord2] == 1 or board[cord1 - i][cord2] == 2:
                    return False
                i += 1
            return True
        elif direction == 'down' and cord1 + length <= 9:
            while i < length:
                if cord1 + i > 9 or board[cord1 + i][cord2] == 1 or board[cord1 + i][cord2] == 2:
                    return False
                i += 1
            return True
        elif direction == 'right' and cord2 + length <= 9:
            while i < length:
                if cord2 + i > 9 or board[cord1][cord2 + i] == 1 or board[cord1][cord2 + i] == 2:
                    return False
                i += 1
            return True
        elif direction == 'left' and cord2 - length >= 0:
            while i < length:
                if cord2 - i < 0 or board[cord1][cord2 - i] == 1 or board[cord1][cord2 - i] == 2:
                    return False
                i += 1
            return True
        else:
            return False

    def placed_ship(self, who, length, direction, cord1, cord2):
        if who == 'alice':
            board = self.alice_board
        else:
            board = self.player_board
        if direction == 'up':
            i = j = 0
            while j < length + 2:
                if cord1 - j + 1 > 9 or cord1 - j + 1 < 0:
                    j += 1
                else:
                    if cord2 - 1 >= 0:
                        board[cord1 - j + 1][cord2 - 1] = 2

                    board[cord1 - j + 1][cord2] = 2

                    if cord2 + 1 <= 9:
                        board[cord1 - j + 1][cord2 + 1] = 2
                    j += 1
            while i < length:
                board[cord1 - i][cord2] = 1
                i += 1
        if direction == 'down':
            i = j = 0
            while j < length + 2:
                if cord1 + j - 1 > 9 or cord1 + j - 1 < 0:
                    j += 1
                else:
                    if cord2 - 1 >= 0:
                        board[cord1 + j - 1][cord2 - 1] = 2

                    board[cord1 + j - 1][cord2] = 2

                    if cord2 + 1 <= 9:
                        board[cord1 + j - 1][cord2 + 1] = 2
                    j += 1
            while i < length:
                board[cord1 + i][cord2] = 1
                i += 1
        if direction == 'right':
            i = j = 0
            while j < length + 2:
                if cord2 + j - 1 > 9 or cord2 + j - 1 < 0:
                    j += 1
                else:
                    if cord1 - 1 >= 0:
                        board[cord1 - 1][cord2 + j - 1] = 2

                    board[cord1][cord2 + j - 1] = 2

                    if cord1 + 1 <= 9:
                        board[cord1 + 1][cord2 + j - 1] = 2
                    j += 1
            while i < length:
                board[cord1][cord2 + i] = 1
                i += 1
        if direction == 'left':
            i = j = 0
            while j < length + 2:
                if cord2 - j + 1 < 0 or cord2 - j + 1 > 9:
                    j += 1
                else:
                    if cord1 - 1 >= 0:
                        board[cord1 - 1][cord2 - j + 1] = 2

                    board[cord1][cord2 - j + 1] = 2

                    if cord1 + 1 <= 9:
                        board[cord1 + 1][cord2 - j + 1] = 2
                    j += 1
            while i < length:
                board[cord1][cord2 - i] = 1
                i += 1

    def player_shot(self, cord1, cord2):
        if self.alice_board[cord1][cord2] != 1:
            self.alice_board[cord1][cord2] = 2
            return False
        elif self.alice_board[cord1][cord2] == 1:
            self.alice_board[cord1][cord2] = -1
            if self.it_death(True, cord1, cord2):
                self.space_near_ship('player', cord1, cord2)
                self.alice_ships[self.player_counter] -= 1
                self.player_counter = 0
            return True

    def alice_shot(self):
        if self.player_ships[1] == 0:
            if self.player_ships[2] == 0:
                self.strategy = 2
            else:
                self.strategy = 1
        return self.base_shot()

    def base_shot(self):
        if not self.was_first_hit:
            if self.strategy == 0:
                self.shooting_cords[0] = cord1 = randint(0, 9)
                self.shooting_cords[1] = cord2 = randint(0, 9)
            else:
                while True:
                    self.shooting_cords[0] = cord1 = randint(0, 9)
                    self.shooting_cords[1] = cord2 = randint(0, 9)
                    if self.player_board[cord1][cord2] == 0 or self.player_board[cord1][cord2] == 1:
                        if self.strategy == 1 and self.good_shot_when_none_one_len(cord1, cord2):
                            break
                        elif self.strategy == 2 and self.good_shot_when_none_one_and_two_len(cord1, cord2):
                            break
            if self.player_board[cord1][cord2] == 1:
                self.counter = 1
                self.was_first_hit = True
                self.player_board[cord1][cord2] = -1
                if self.it_death():
                    self.was_first_hit = False
                    self.counter = 0
                    self.player_ships[1] -= 1
                return True
            elif self.player_board[cord1][cord2] == -1 or self.player_board[cord1][cord2] == 2:
                self.alice_shot()
            else:
                self.player_board[cord1][cord2] = 2
                return False
        if self.was_first_hit and not self.was_second_hit[0]:
            if self.cross_shot():
                return True
            else:
                return False
        if self.was_first_hit and self.was_second_hit[0]:
            if self.final_shot():
                return True
            else:
                return False

    def good_shot_when_none_one_len(self, cord1, cord2):
        try:
            up = self.alice_board[cord1 - 1][cord2]
        except IndexError:
            up = -1
        try:
            down = self.alice_board[cord1 + 1][cord2]
        except IndexError:
            down = -1
        try:
            left = self.alice_board[cord1][cord2 - 1]
        except IndexError:
            left = -1
        try:
            right = self.alice_board[cord1][cord2 + 1]
        except IndexError:
            right = -1
        if (up == 0 or up == 1) or (down == 0 or down == 1) or (right == 0 or right == 1) or (
                left == 0 or left == 1):
            return True
        else:
            return False

    def good_shot_when_none_one_and_two_len(self, cord1, cord2):
        count_up_down = 1
        try:
            i = 0
            while count_up_down < 3:
                if self.alice_board[cord1 - i][cord2] == 0:
                    count_up_down += 1
                else:
                    break
                i += 1
        except IndexError:
            pass
        try:
            i = 0
            while count_up_down < 3:
                if self.alice_board[cord1 + i][cord2] == 0:
                    count_up_down += 1
                else:
                    break
                i += 1
        except IndexError:
            pass
        count_left_right = 1
        try:
            i = 0
            while count_up_down < 3:
                if self.alice_board[cord1][cord2 - i] == 0:
                    count_left_right += 1
                else:
                    break
                i += 1
        except IndexError:
            pass
        try:
            i = 0
            while count_up_down < 3:
                if self.alice_board[cord1][cord2 + i] == 0:
                    count_left_right += 1
                else:
                    break
                i += 1
        except IndexError:
            pass
        if count_up_down == 3 or count_left_right == 3:
            return True
        else:
            return False

    def it_death(self, player=False, player_cord1=-1, player_cord2=-1):
        cord1, cord2 = self.shooting_cords[0], self.shooting_cords[1]
        seb = self.player_board
        if player:
            cord1, cord2 = player_cord1, player_cord2
            seb = self.alice_board
        up, down, right, left = True, True, True, True
        if cord1 == 0:
            up = True
        else:
            try:
                i_up = 0
                while up:
                    if cord1 - i_up < 0:
                        raise IndexError
                    if seb[cord1 - i_up][cord2] == 1:
                        up = False
                    else:
                        if seb[cord1 - i_up][cord2] == 2 or seb[cord1 - i_up][cord2] == 0:
                            break
                        elif seb[cord1 - i_up][cord2] == -1:
                            i_up += 1
            except IndexError:
                up = True
        if cord1 == 9:
            down = True
        else:
            try:
                i_down = 0
                while down:
                    if cord1 + i_down > 9:
                        raise IndexError
                    if seb[cord1 + i_down][cord2] == 1:
                        down = False
                    else:
                        if seb[cord1 + i_down][cord2] == 2 or seb[cord1 + i_down][cord2] == 0:
                            break
                        elif seb[cord1 + i_down][cord2] == -1:
                            i_down += 1
            except IndexError:
                down = True

        if cord2 == 9:
            right = True
        else:
            try:
                i_right = 0
                while right:
                    if cord2 + i_right > 9:
                        raise IndexError
                    if seb[cord1][cord2 + i_right] == 1:
                        right = False
                    else:
                        if seb[cord1][cord2 + i_right] == 2 or seb[cord1][cord2 + i_right] == 0:
                            break
                        elif seb[cord1][cord2 + i_right] == -1:
                            i_right += 1
            except IndexError:
                right = True
        if cord2 == 0:
            left = True
        else:
            try:
                i_left = 0
                while left:
                    if cord2 - i_left < 0:
                        raise IndexError
                    if seb[cord1][cord2 - i_left] == 1:
                        left = False
                    else:
                        if seb[cord1][cord2 - i_left] == 2 or seb[cord1][cord2 - i_left] == 0:
                            break
                        elif seb[cord1][cord2 - i_left] == -1:
                            i_left += 1
            except IndexError:
                left = True
        if up and down and left and right and not player:
            self.space_near_ship('alice')
        return up and down and left and right

    def space_near_ship(self, player_or_alice, player_cord1=0, player_cord2=0):
        cord1, cord2, counter, direction = 0, 0, 0, ''
        board = [[]]
        if player_or_alice == 'player':
            cord1, cord2 = player_cord1, player_cord2
            board = self.alice_board
            cord1, cord2, direction = self.get_player_direction_and_final_cords(cord1, cord2)
            self.set_player_counter(cord1, cord2, direction)
            counter = self.player_counter

        elif player_or_alice == 'alice':
            cord1, cord2 = self.shooting_cords[0], self.shooting_cords[1]
            board = self.player_board
            direction = self.was_second_hit[1]
            counter = self.counter
        if counter == 1:
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if cord1 + i < 0 or cord1 + i > 9 or cord2 + j < 0 or cord2 + j > 9:
                        continue
                    if i == 0 and j == 0:
                        continue
                    try:
                        board[cord1 + i][cord2 + j] = 2
                    except IndexError:
                        pass
        if counter != 0:
            ii, jj, len_i, len_j = 0, 0, 0, 0
            if direction == 'up':
                ii = 1
                len_i = counter + abs(ii)
                len_j = 2
            elif direction == 'down':
                ii = -1
                len_i = counter + abs(ii)
                len_j = 2
            elif direction == 'right':
                jj = -1
                len_i = 2
                len_j = counter + abs(jj)
            elif direction == 'left':
                jj = 1
                len_i = 2
                len_j = counter + abs(jj)
            for i in range(-1, len_i, 1):
                for j in range(-1, len_j, 1):
                    try:
                        if ii != 0:
                            that_i = ii * i
                        else:
                            that_i = i
                        if jj != 0:
                            that_j = jj * j
                        else:
                            that_j = j
                        if cord1 + that_i < 0 or cord1 + that_i > 9 or cord2 + that_j < 0 or cord2 + that_j > 9:
                            continue
                        if board[cord1 + that_i][cord2 + that_j] == -1:
                            continue
                        board[cord1 + that_i][cord2 + that_j] = 2
                    except IndexError:
                        pass

    def set_player_counter(self, player_cord1, player_cord2, direction):
        cord1, cord2 = player_cord1, player_cord2
        if not direction:
            self.player_counter = 1
            return
        i, j = 0, 0
        if direction == 'up':
            i = 1
        elif direction == 'down':
            i = -1
        elif direction == 'right':
            j = -1
        elif direction == 'left':
            j = 1
        try:
            while self.alice_board[cord1][cord2] == -1:
                self.player_counter += 1
                cord1 += i
                cord2 += j
        except IndexError:
            return

    def get_player_direction_and_final_cords(self, player_cord1, player_cord2):
        cord1, cord2 = player_cord1, player_cord2
        board = self.alice_board
        if player_cord1 == 0:
            if board[cord1 + 1][cord2] == -1:
                return cord1, cord2, 'up'
            else:
                while True:
                    if board[cord1][cord2] != -1:
                        cord2 -= 1
                        break
                    cord2 += 1
                return cord1, cord2, 'right'
        elif player_cord1 == 9:
            if board[cord1 - 1][cord2] == -1:
                return cord1, cord2, 'down'
            else:
                while True:
                    if board[cord1][cord2] != -1:
                        cord2 -= 1
                        break
                    cord2 += 1
                return cord1, cord2, 'right'
        if player_cord2 == 9:
            if board[cord1][cord2 - 1] == -1:
                return cord1, cord2, 'right'
            else:
                while True:
                    if board[cord1][cord2] != -1:
                        cord1 -= 1
                        break
                    cord1 += 1
                return cord1, cord2, 'down'
        elif player_cord2 == 0:
            if board[cord1][cord2 + 1] == -1:
                return cord1, cord2, 'left'
            else:
                while True:
                    if board[cord1][cord2] != -1:
                        cord1 -= 1
                        break
                    cord1 += 1
                return cord1, cord2, 'down'
        if board[cord1 + 1][cord2] == -1 or board[cord1 - 1][cord2] == -1:
            try:
                while True:
                    if board[cord1][cord2] != -1:
                        cord1 -= 1
                        break
                    cord1 += 1
            except IndexError:
                cord1 -= 1
            return cord1, cord2, 'down'
        elif board[cord1][cord2 + 1] == -1 or board[cord1][cord2 - 1] == -1:
            try:
                while True:
                    if board[cord1][cord2] != -1:
                        cord2 -= 1
                        break
                    cord2 += 1
            except IndexError:
                cord2 -= 1
            return cord1, cord2, 'right'
        else:
            return cord1, cord2, ''

    def cross_shot(self):
        possible_shots = list()
        cord1, cord2 = self.shooting_cords[0], self.shooting_cords[1]
        if cord1 - 1 >= 0 and self.player_board[cord1 - 1][cord2] != 2:
            possible_shots.append([cord1 - 1, cord2, 'up'])
        if cord1 + 1 <= 9 and self.player_board[cord1 + 1][cord2] != 2:
            possible_shots.append([cord1 + 1, cord2, 'down'])
        if cord2 - 1 >= 0 and self.player_board[cord1][cord2 - 1] != 2:
            possible_shots.append([cord1, cord2 - 1, 'left'])
        if cord2 + 1 <= 9 and self.player_board[cord1][cord2 + 1] != 2:
            possible_shots.append([cord1, cord2 + 1, 'right'])
        ps = choice(possible_shots)
        cord1, cord2 = ps[0], ps[1]
        if self.player_board[cord1][cord2] == 1:
            self.shooting_cords[0] = cord1
            self.shooting_cords[1] = cord2
            self.player_board[cord1][cord2] = -1
            self.counter = 2
            self.was_second_hit[1] = ps[2]
            if self.it_death():
                self.was_first_hit = False
                self.counter = 0
                self.player_ships[2] -= 1
            else:
                self.was_second_hit[0] = True
                self.was_second_hit[1] = ps[2]
            return True
        else:
            self.player_board[cord1][cord2] = 2
            return False

    def change_shooting_cords_for_final_shot(self):
        i, j = 0, 0
        if self.was_second_hit[1] == 'up':
            i = 1
        elif self.was_second_hit[1] == 'down':
            i = -1
        elif self.was_second_hit[1] == 'right':
            j = -1
        elif self.was_second_hit[1] == 'left':
            j = 1
        while True:
            if self.player_board[self.shooting_cords[0] + i][self.shooting_cords[1] + j] == 1:
                break
            self.shooting_cords[0] += i
            self.shooting_cords[1] += j

    def final_shot(self):
        cord1, cord2 = self.shooting_cords[0], self.shooting_cords[1]
        if self.was_second_hit[1] == 'right':
            if cord2 + 1 > 9 or self.player_board[cord1][cord2 + 1] == 2:
                self.change_shooting_cords_for_final_shot()
                self.was_second_hit[1] = 'left'
                return self.final_shot()
            if self.player_board[cord1][cord2 + 1] == 1:
                self.shooting_cords[1] += 1
                self.counter += 1
                self.player_board[cord1][cord2 + 1] = -1
                if self.it_death():
                    self.player_ships[self.counter] -= 1
                    self.counter = 0
                    self.was_first_hit = False
                    self.was_second_hit[0] = False
                return True
            elif self.player_board[cord1][cord2 + 1] == -1:
                self.shooting_cords[1] += 1
                return self.final_shot()
            else:
                self.player_board[cord1][cord2 + 1] = 2
                self.was_second_hit[1] = 'left'
                return False

        if self.was_second_hit[1] == 'left':
            if cord2 - 1 < 0 or self.player_board[cord1][cord2 - 1] == 2:
                self.change_shooting_cords_for_final_shot()
                self.was_second_hit[1] = 'right'
                return self.final_shot()
            if self.player_board[cord1][cord2 - 1] == 1:
                self.shooting_cords[1] -= 1
                self.counter += 1
                self.player_board[cord1][cord2 - 1] = -1
                if self.it_death():
                    self.player_ships[self.counter] -= 1
                    self.counter = 0
                    self.was_first_hit = False
                    self.was_second_hit[0] = False
                return True
            elif self.player_board[cord1][cord2 - 1] == -1:
                self.shooting_cords[1] -= 1
                return self.final_shot()
            else:
                self.player_board[cord1][cord2 - 1] = 2
                self.was_second_hit[1] = 'right'
                return False

        if self.was_second_hit[1] == 'up':
            if cord1 - 1 < 0 or self.player_board[cord1 - 1][cord2] == 2:
                self.change_shooting_cords_for_final_shot()
                self.was_second_hit[1] = 'down'
                return self.final_shot()
            if self.player_board[cord1 - 1][cord2] == 1:
                self.shooting_cords[0] -= 1
                self.counter += 1
                self.player_board[cord1 - 1][cord2] = -1
                if self.it_death():
                    self.player_ships[self.counter] -= 1
                    self.counter = 0
                    self.was_first_hit = False
                    self.was_second_hit[0] = False
                return True
            elif self.player_board[cord1 - 1][cord2] == -1:
                self.shooting_cords[0] -= 1
                return self.final_shot()
            else:
                self.player_board[cord1 - 1][cord2] = 2
                self.was_second_hit[1] = 'down'
                return False

        if self.was_second_hit[1] == 'down':
            if cord1 + 1 > 9 or self.player_board[cord1 + 1][cord2] == 2:
                self.change_shooting_cords_for_final_shot()
                self.was_second_hit[1] = 'up'
                return self.final_shot()
            if self.player_board[cord1 + 1][cord2] == 1:
                self.shooting_cords[0] += 1
                self.counter += 1
                self.player_board[cord1 + 1][cord2] = -1
                if self.it_death():
                    self.player_ships[self.counter] -= 1
                    self.counter = 0
                    self.was_first_hit = False
                    self.was_second_hit[0] = False
                return True
            elif self.player_board[cord1 + 1][cord2] == -1:
                self.shooting_cords[0] += 1
                return self.final_shot()
            else:
                self.player_board[cord1 + 1][cord2] = 2
            self.was_second_hit[1] = 'up'
            return False

    def end_of_game(self):
        player, alice = True, True
        for how_many_ship in self.alice_ships.values():
            if how_many_ship != 0:
                player = False
        for how_many_ship in self.player_ships.values():
            if how_many_ship != 0:
                alice = False
        if player:
            return 'player'
        elif alice:
            return 'alice'
        else:
            return 'Nobody'


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    logging.info('SS: %r', sessionStorage)
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            'text': 'ha',
            "end_session": False
        }
    }
    try:
        handle_dialog(request.json, response)
    except KeyError:
        response["response"]['text'] = 'Что-то пошло не так. Алиса признает техническое поражение. Вы выйграли'
        response['response']['end_session'] = True

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'alice': Computer(),
            'player_shot': True,
            'alice_shot': False,
            'first_response': True,
            'ships_for_set': {i: 0 for i in range(1, 5, 1)}
        }

        res['response'][
            'text'] = 'Привет! Расставь свои корабли.\n' \
                      'Однопалубные можно ставить лишь указав одну координату.\n' \
                      'Например так : a1 или h10.\n' \
                      'Корабли большей длины можно поставить, указав их начальные и конечный координаты через ":"\n' \
                      'Например так: a1:a3 или a1:b1\n' \
                      'Удачи!'

        res['response']['buttons'] = [
            {
                'title': 'random',
                'hide': True
            }
        ]
        # res['response']['buttons'] = get_suggests(user_id)
        return

    # Расстановка кораблей
    if sessionStorage[user_id]['first_response']:
        computer = sessionStorage[user_id]['alice']
        text = req['request']['original_utterance']
        if text == 'random':
            computer.create_ships('player')
            enemy_board, player_board = boards_like_a_text(computer)
            res['response'][
                'text'] = 'Отлично. ' \
                          'Давай начнем играть.\n' + 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board
            sessionStorage[user_id]['first_response'] = False
            return
        ships = sessionStorage[user_id]['ships_for_set']
        length, success = set_player_ships(computer, text, ships)
        if success:
            ships[length] += 1
            if list(ships.values()) == [4, 3, 2, 1]:
                enemy_board, player_board = boards_like_a_text(computer)
                res['response'][
                    'text'] = 'Отлично. ' \
                              'Давай начнем играть.\n' + 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board
                sessionStorage[user_id]['first_response'] = False
                return
            else:
                _, board = boards_like_a_text(computer)
                res['response']['text'] = 'Отлично. Давай следующий.\n' \
                                          'Вот твое текущее поле\n' + board
                return
        else:
            res['response']['text'] = 'Это не по правилам.'
            return

    # Игра
    # if sessionStorage[user_id]['player_shot']:
    computer = sessionStorage[user_id]['alice']
    text = req['request']['original_utterance']
    success, cord1, cord2 = receive_shot(text)
    if success:
        sessionStorage[user_id]['player_shot'] = computer.player_shot(cord1, cord2)
        if not sessionStorage[user_id]['player_shot']:
            while computer.alice_shot():
                pass
        enemy_board, player_board = boards_like_a_text(computer)
        who_win = computer.end_of_game()
        if who_win == 'player':
            res['response']['text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board + '\nВы выйграли'
            res['response']['end_session'] = True
            return
        elif who_win == 'alice':
            res['response'][
                'text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board + '\nВы к сожаланию проиграли'
            res['response']['end_session'] = True
            return
        res['response']['text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board
        # sessionStorage[user_id]['alice_shot'] = not sessionStorage[user_id]['player_shot']
        return
    else:
        res['response']['text'] = 'Ну кто так стреляет , давай еще разок'
        return


# if sessionStorage[user_id]['alice_shot']:
#     computer = sessionStorage[user_id]['alice']
#     sessionStorage[user_id]['alice_shot'] = computer.alice_shot()
#     sessionStorage[user_id]['player_shot'] = not sessionStorage[user_id]['alice_shot']
#     enemy_board, player_board = boards_like_a_text(computer)
#     res['response']['text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board
#     return


def set_player_ships(computer, string, dict_of_ships):
    letters = [chr(i + ord('a')) for i in range(10)]
    numbers = [i + 1 for i in range(10)]
    length, success = 0, True
    try:
        string = string.replace(' ', '')
        string = string.lower()
        if len(string) <= 3:
            letter, number = string[0], int(string[1:])
            check_list = free_space(computer, letter, letter, number, number)
            if 1 in check_list:
                raise ValueError
            if letter not in letters or number not in numbers:
                raise NameError
            length = 1
            if dict_of_ships[length] == (5 - length):
                raise NameError
            cord1, cord2 = number - 1, ord(letter) - ord('a')
            computer.player_board[cord1][cord2] = 1
        else:
            seed = string.find(':')
            s1, s2 = string[0:seed], string[seed + 1:]
            letter1, letter2 = s1[0], s2[0]
            print(letter1 == letter2)
            number1, number2 = int(s1[1:]), int(s2[1:])
            if letter1 != letter2 and number1 != number2:
                raise NameError
            if letter1 not in letters or letter2 not in letters or number1 not in numbers or number2 not in numbers:
                raise NameError
            check_list = free_space(computer, letter1, letter2, number1, number2)
            if 1 in check_list:
                raise ValueError
            if letter1 == letter2:
                if abs(number2 - number1) + 1 > 4:
                    raise NameError
                else:
                    length = abs(number2 - number1) + 1
                if dict_of_ships[length] == (5 - length):
                    raise NameError
                start = min(number1, number2) - 1
                end = max(number1, number2)
                cord2 = ord(letter1) - ord('a')
                for i in range(start, end, 1):
                    computer.player_board[i][cord2] = 1
            elif number1 == number2:
                if abs(ord(letter1) - ord(letter2)) + 1 > 4:
                    raise NameError
                else:
                    length = abs(ord(letter1) - ord(letter2)) + 1
                if dict_of_ships[length] == (5 - length):
                    raise NameError
                start = min(ord(letter1), ord(letter2)) - ord('a')
                end = max(ord(letter1), ord(letter2)) - ord('a') + 1
                cord1 = number1 - 1
                for i in range(start, end, 1):
                    computer.player_board[cord1][i] = 1
    except (NameError, IndexError, ValueError):
        success = False
    return length, success


def free_space(computer, letter1, letter2, number1, number2):
    board = computer.player_board
    nearest = []
    min_cord1 = min(number1, number2) - 1
    max_cord1 = max(number1, number2) - 1
    min_cord2 = min(ord(letter1), ord(letter2)) - ord('a')
    max_cord2 = max(ord(letter1), ord(letter2)) - ord('a')
    for i in range(min_cord1 - 1, max_cord1 + 2, 1):
        for j in range(min_cord2 - 1, max_cord2 + 2, 1):
            try:
                if i < 0 or i > 9 or j < 0 or j > 9:
                    raise IndexError
                nearest.append(board[i][j])
            except IndexError:
                nearest.append(0)
    return nearest


def boards_like_a_text(computer):
    enemy_board = computer.alice_board
    player_board = computer.player_board
    numbers = ('①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩')
    enemy_board_text, player_board_text = '⊗ 🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹\n', '⊗ 🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹\n'
    i = -1
    for row in enemy_board:
        i += 1
        enemy_board_text += numbers[i]
        for element in row:
            if element == 0:
                enemy_board_text += '⬜'
            elif element == 1:
                enemy_board_text += '⬛'
            elif element == 2:
                enemy_board_text += '⊠'
            elif element == -1:
                enemy_board_text += '🔥'
        enemy_board_text += '\n'
    i = -1
    for row in player_board:
        i += 1
        player_board_text += numbers[i]
        for element in row:
            if element == 0:
                player_board_text += '⬜'
            elif element == 1:
                player_board_text += '⬛'
            elif element == 2:
                player_board_text += '⊠'
            elif element == -1:
                player_board_text += '🔥'
        player_board_text += '\n'
    return enemy_board_text, player_board_text


def receive_shot(string):
    success = True
    cord1, cord2 = -1, -1
    string = string.replace(' ', '').lower()
    numbers = [i for i in range(10)]
    try:
        cord1 = int(string[1:]) - 1
        cord2 = ord(string[0]) - ord('a')
        if cord1 not in numbers or cord2 not in numbers:
            raise NameError
    except (TypeError, IndexError, NameError, ValueError):
        success = False
    return success, cord1, cord2
