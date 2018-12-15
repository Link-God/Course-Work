# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем методы для генерации рандомного числа и выбора элемента из списка.
from random import randint, choice

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


class Computer:
    """Класс отвечающий за работу "Алисы" и состояние игры в целом"""

    def __init__(self):
        """
        Инициализирем основные поля класса.Вызывает функцию для растоновки кораблей на поле "Алисы"
        """
        self.player_ships = {i: 5 - i for i in range(1, 5, 1)}  # Список кораблей пользователя(длина - количество)
        self.alice_ships = {i: 5 - i for i in range(1, 5, 1)}  # Список кораблей "Алисы"(длина - количество)
        self.alice_board = list([0] * 10 for _ in range(10))  # Игровое поле "Алисы". Изначально пустое
        self.player_board = list([0] * 10 for _ in range(10))  # Игровое поле пользователя. Изначально пустое
        self.was_first_hit = False  # Хранит результат первого выстрела после потопления корабля(первого за сессию)
        self.was_second_hit = [False, '']  # Хранит результата выстрела после певого успешного выстерла
        # и направление относительно него.
        self.shooting_cords = [0, 0]  # Предыдущий вестрел
        self.strategy = 0  # Текущая стратегия. 0 - есть все 1 и 2 палубгные. 1 - нет 1 палубных. 2 - нет 1 и 2 палубных
        self.counter = 0  # Счетчик успешных выстрелов. Для удаления потопленных кораблей пользователя.
        self.player_counter = 0  # Хранит длину последнего корабля потопленного пользователем.
        # Используеться для удаления из списка кораблей "Алисы" и "потопления" последнего потбитого корабля.
        self.create_ships()

    def clear_boar(self):
        """
        Так как для того что бы корабли не стояли вплотную.
        При расстановке пространтво вокруг кораблей было заполнено цифрой "2".
        Эта функция оставляет на поле только корабли.
        :return: Работает на прямую с полями класса поэтому ничего не возвращает.
        """
        for i in range(len(self.alice_board)):
            for j in range(len(self.alice_board[0])):
                if self.alice_board[i][j] == 2:
                    self.alice_board[i][j] = 0
                if self.player_board[i][j] == 2:
                    self.player_board[i][j] = 0

    def create_ships(self, who='alice'):
        """
        Произвольно расставляет корабли на поле "Алисы" или пользователя в зависимости от параметра who.
        :param who: Отвечает за выбор поля для рассттовки. 'alice' - используеться поле "Aлисы".
        'player' - используеться поле пользователя.
        Этот парамент передаеться если в запросе от сервера при расстановке кораблей была передана команда random.
        :return:Работает на прямую с полями класса поэтому ничего не возвращает.
        """
        ships = (1, 4, 3, 3, 2, 2, 2, 1, 1, 1)  # Список длин кораблей которые необходимо расставить.
        direction = ('up', 'down', 'right', 'left')  # Список возможных направлений.
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
        """
        Проверяет возможно ли от заданных координат в заданном направлении поставить корабль заданной длины.
        :param who: Отвечает за выбор поля для рассттовки. 'alice' - используеться поле "Aлисы".
        'player' - используеться поле пользователя.
        :param direction: Выбранное направление.
        :param length: Длина корабля.
        :param cord1: Начальна координата по горизонтали.
        :param cord2: Нчальная координата по вертикали.
        :return: False - если нельзя. True - если можно.
        """
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
        """
        Размещает корабль заданной длины от заданных начальных координат в заданном направлении.
        :param who: Отвечает за выбор поля для рассттовки. 'alice' - используеться поле "Aлисы".
        'player' - используеться поле пользователя.
        :param direction: Выбранное направление.
        :param length: Длина корабля.
        :param cord1: Начальна координата по горизонтали.
        :param cord2: Нчальная координата по вертикали.
        :return: Работает на прямую с полями класса поэтому ничего не возвращает.
        """
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
        """
        Анализ и обработка выстрела пользователя. Изменяет поле в зависимоти от результата(рисуем промах или попадание).
        :param cord1: Координата выстрела пользователья по горизонтали.
        :param cord2: Координата выстрела пользователья  по вертикали.
        :return: True - при попадании. False - при промахе или при попадании в уже подбитый корабль.
        """
        if self.alice_board[cord1][cord2] != 1:
            if self.alice_board[cord1][cord2] == -1:
                return False
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
        """
        Выбираем стратегию и инициализирем выстрел "Алисы" .
        :return: True - при попадании. False - при промахе или при попадании в уже подбитый корабль.
        """
        if self.player_ships[1] == 0:
            if self.player_ships[2] == 0:
                self.strategy = 2
            else:
                self.strategy = 1
        return self.base_shot()

    def base_shot(self):
        """
        Выбираем произвольную непутсую координату и инициализируем необходимый алгоритм выстрела.
        Алгоритм выстрела зависит от стратегии, от результата прошлого выстерла.
        Если ничиго не знаем о новом корабле то просто выбираем координату.
        Если в прошлый выстрел попал в корабль то стреляем только в соседнии(не по диагонали) кооринаты.
        Если выстрел в соседнюю координату был успешен, то стерляем  только по вертикали или горизонтали.
        :return: True - при попадании. False - при промахе.
        """
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
        """
        Проверка целесообразности выстрела в данную клетку при стратегии 1.
        :param cord1: Координата клетки по горизонтали.
        :param cord2: Координата клетки по вертикали.
        :return: True - если целесообразно. False - если нет.
        """
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
        """
        Проверка целесообразности выстрела в данную клетку при стратегии 2.
        :param cord1: Координата клетки по горизонтали.
        :param cord2: Координата клетки по вертикали.
        :return: True - если целесообразно. False - если нет.
        """
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
        """
        Проверка "убит" ли корабль(подбит целиком).
        :param player: False - если потопила "Алиса". True - если пользователь.
        :param player_cord1: Координата выстрела пользователя по горизонатли.(не используеться при выстреле "Алисы")
        :param player_cord2: Координата выстрела пользователя по вертикали.(не используеться при выстреле "Алисы")
        :return: True - Если "убит". False - если нет.
        """
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
        """
        Закрашивает область вокруг потопленного корабля
        :param player_or_alice: Если 'player', значит подбил пользователь. Иначе подбила "Алиса".
        :param player_cord1: Координата выстрела пользователья по горизонтали.(не используеться при выстреле "Алисы")
        :param player_cord2: Координата выстрела пользователья  по вертикали.(не используеться при выстреле "Алисы")
        :return: Работает на прямую с полями класса поэтому ничего не возвращает.
        """
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
        """
        Учтанавливает длину последнего "убитого" пользователем корабля.
        Так как пользователь может при попадании в один корабль , может решить "убить" иной.
        :param player_cord1: Координата выстрела пользователья по горизонтали.
        :param player_cord2: Координата выстрела пользователья по вертикали.
        :param direction: Направление расположения корабля относительно выстрела.
        :return:  Работает на прямую с полями класса поэтому ничего не возвращает.
        """
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
        """
        Определяет крайнюю точку "убитого" корабля. И направления относительно этой точки.
        :param player_cord1: Координата последнего вытсрела пользователя по горизонтали.
        :param player_cord2: Координата последнего вытсрела пользователя по вертикали.
        :return: Координаты крайней точки и направление относительно нее.
        """
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
        """
        Стреляет в соседние не по диагонали точки относительно последнего успешного выстрела "Алисы".
        :return: True - при попадании. False - при промахе.
        """
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
        """
        Вспомогательная функция.
        Если алгоритм финальной стадии выстрелов по кораблю дошел до одного из краев корабля.
        Например :  .. 0 0 |1 -1 -1 -1| 2 0 ... (первый успешный выстрел в данном примере первая слева -1).
        Меняет координаты и направление выстрелов так, что бы следующтй выстрел был успешным.
        :return: Работает на прямую с полями класса поэтому ничего не возвращает.
        """
        i, j = 0, 0
        if self.was_second_hit[1] == 'up':
            i = 1
            self.was_second_hit[1] = 'up'
            self.was_second_hit[1] = 'down'
        elif self.was_second_hit[1] == 'down':
            i = -1
        elif self.was_second_hit[1] == 'right':
            j = -1
            self.was_second_hit[1] = 'left'
        elif self.was_second_hit[1] == 'left':
            j = 1
            self.was_second_hit[1] = 'right'
        while True:
            if self.player_board[self.shooting_cords[0] + i][self.shooting_cords[1] + j] == 1:
                break
            self.shooting_cords[0] += i
            self.shooting_cords[1] += j

    def final_shot(self):
        """
        Стреляет по горизонатли или вертикали в зависимости от направления второго успешного выстрела.
        Так же окончалетельно "убивает" корабль.(не обязательно при первом же вызове)
        :return: True - при попадании. False - при промахе.
        """
        cord1, cord2 = self.shooting_cords[0], self.shooting_cords[1]
        if self.was_second_hit[1] == 'right':
            if cord2 + 1 > 9 or self.player_board[cord1][cord2 + 1] == 2:
                self.change_shooting_cords_for_final_shot()
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
        """
        Определяет победителя
        :return: "player"  - если выйграл пользователь. "alice" -если выйграла "Алиса". "Nobody" - если еще никто.
        """
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
    """
    Функция получает тело запроса и возвращает ответ.
    :return: Ответ в виде Json.
    """
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
    """
    Анализирует запрос и составляет ответ.
    :param req: Запрос в формате Json.
    :param res: Ответ в формате Json.
    :return: Работает непосредственно с res.
    """
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
            'text'] = 'Приветствую! Этот навык явялеться закрытым(он не отобрадаеться в каталоге).' \
                      ' Расставь свои корабли.\n' \
                      'Однопалубные можно ставить лишь указав одну координату.\n' \
                      'Например так : a1 или h10.\n' \
                      'Корабли большей длины можно поставить, указав их начальные и конечный координаты через ":"\n' \
                      'Например так: a1:a3 или a1:b1\n' \
                      'Координаты указываються в виде пары буква - число\n' \
                      'Используються первые 10 букв латинсокго алфавита(abcd...). А числа от 1 до 10.\n' \
                      'В игре 4 корабля длины 1. 3 длины 2. 2 длины 3. 1 длины 4.\n' \
                      'Между любыми кораблями должно быть расстояние минимуум в ' \
                      'одну клетку. Нельзя ставить корабли полностью или частично за пределы поля.' \
                      'При использовании кнопки random корабли автоматичекси выставятся произвольным образом\n' \
                      'Удачи!'

        res['response']['buttons'] = [
            {
                'title': 'random',
                'hide': True
            }
        ]
        return

    helping_string = 'Если вы еще не расставили корабли то укажите их координаты. Однопалубные можно ставить,' \
                     ' указав лишь одну координату(Например: a1)\n' \
                     'Корабли большей длины необходимо ставить, указывая их начальные и конечные координаты\n' \
                     'Примеры : a1:a3 или a1:c1\n' \
                     'Между любыми кораблями должно быть расстояние минимуум в ' \
                     'одну клетку. Нельзя ставить корабли полностью или частично за пределы поля.\n' \
                     'Если же вы уже рассавили корабли, то вам лишь нужно написать команду- выстрел в формате' \
                     ' буква-число. Используються первые 10 букв латинсокго алфавита(abcd...). А числа от 1 до 10.\n' \
                     'Стрелять за пределы поля и в уже подбитые корабли нельзя'

    text = req['request']['original_utterance']

    res['response']['buttons'] = [
        {
            'title': 'Помощь',
            'hide': True
        }
    ]

    # Помощь
    if text.lower() == 'помощь' or 'что ты умеешь' in text.lower():
        res['response']['text'] = helping_string
        return

    # Расстановка кораблей
    if sessionStorage[user_id]['first_response']:
        computer = sessionStorage[user_id]['alice']
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
            res['response']['text'] = 'Это не по правилам. Между любыми кораблями должно быть расстояние минимуум в ' \
                                      'одну клетку. Нельзя ставить корабли полностью или частично за пределы поля.\n' \
                                      'Необходимо использовать первые 10 букв латинского алфаваита.\n' \
                                      'a b c d e f g h i j\n' \
                                      'И числа от 1 до 10'
            return

    # Игра
    computer = sessionStorage[user_id]['alice']
    success, cord1, cord2 = receive_shot(text)
    if success:
        if computer.alice_board[cord1][cord2] == -1:
            res['response']['text'] = 'Корабль уже потоплен.\n' \
                                      'Стреляйте в клетки, в которых нет горящих кораблей.'
            return
        sessionStorage[user_id]['player_shot'] = computer.player_shot(cord1, cord2)
        if not sessionStorage[user_id]['player_shot']:
            while computer.alice_shot():
                pass
        enemy_board, player_board = boards_like_a_text(computer)
        who_win = computer.end_of_game()
        if who_win == 'player':
            res['response']['text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board + \
                                      '\nВы выйграли!!!\nПоздравляю!!!'
            res['response']['end_session'] = True
            return
        elif who_win == 'alice':
            res['response'][
                'text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board + '\nВы к сожаланию проиграли.'
            res['response']['end_session'] = True
            return
        res['response']['text'] = 'Поле Алисы\n' + enemy_board + 'Твое поле\n' + player_board
        # sessionStorage[user_id]['alice_shot'] = not sessionStorage[user_id]['player_shot']
        return
    else:
        res['response']['text'] = 'Ну кто так стреляет , давай еще разок.\n' \
                                  'Напоминаю, стреляйте только в пределах поля.\n' \
                                  'Необходимо использовать первые 10 букв латинского алфаваита.\n' \
                                  'a b c d e f g h i j\n' \
                                  'И числа от 1 до 10'
        return


def set_player_ships(computer, string, dict_of_ships):
    """
    Раставялет корабли пользователя.
    :param computer: Объект класса отвечающий за текущую игру.
    :param string: Текст пользователя.
    :param dict_of_ships: Словарь который хранит длину и количество кораблей которые осталось расставить.
    :return: Длину поставленного корабля(0 при неудаче) и True если это удалось сделать по правилам, иначе False.
    """
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
    """
    Проверяет свободно ли место вокруг пространства куда планируется поставить корабль.
    :param computer: Объект класса отвечающий за текущую игру.
    :param letter1: Первая буква в запросе пользователя.
    :param letter2: Вторая буква в запросе пользователя.
    :param number1: Первое число в запросе пользователя.
    :param number2: Второе число в запросе пользователя.
    :return: Список состояния ближайших клеток. (0 или 2 - свободно, 1 - занято)
    """
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
    """
    Преобразует текущее состояние игровых полей в текстовый формат.
    :param computer: Объект класса отвечающий за текущую игру.
    :return: Поля в текстовом формате.
    """
    enemy_board = computer.alice_board
    player_board = computer.player_board
    numbers = ('①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩')
    enemy_board_text, player_board_text = "⊗ 🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹\n", '⊗ 🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹\n'
    i = -1
    for row in enemy_board:
        i += 1
        enemy_board_text += numbers[i]
        for element in row:
            if element == 0 or element == 1:
                enemy_board_text += '⬜'
            # elif element == 1:
            #     enemy_board_text += '⬛'
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
    """
    Обработка координат выстрела
    :param string: Строка запроса пользователя.
    :return: True если выстрел в пределах поля. False если вне пределов. Так же координаты выстрела(при False [-1, -1])
    """
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
