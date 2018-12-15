import unittest
import Game

b_for_ex = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
]


class TestStringMethods(unittest.TestCase):
    def test_one(self):
        g = Game.Computer()
        self.assertEqual(g.player_counter, 0)

    def test_receive_shot(self):
        success1, c11, c12 = Game.receive_shot('a1')
        success2, _, _ = Game.receive_shot('t5')
        self.assertEqual(success1, True)
        self.assertEqual(c11, 0)
        self.assertEqual(c12, 0)
        self.assertEqual(success2, False)

    def test_set_player_ships(self):
        player_board = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        g = Game.Computer()
        d = {i: 0 for i in range(1, 5, 1)}
        length, success = Game.set_player_ships(g, 'a1:b1', d)
        self.assertEqual(g.player_board, player_board)
        self.assertEqual(length, 2)
        self.assertEqual(success, True)
        length, success = Game.set_player_ships(g, 'a10:f10', d)
        self.assertEqual(success, False)
        length, success = Game.set_player_ships(g, 'c3:d4', d)
        self.assertEqual(success, False)
        length, success = Game.set_player_ships(g, 'c11:c10', d)
        self.assertEqual(success, False)
        length, success = Game.set_player_ships(g, 's4', d)
        self.assertEqual(success, False)

    def test_free_space(self):
        g = Game.Computer()
        l = Game.free_space(g, 'a', 'b', 1, 1)
        l_check = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(l, l_check)
        l = Game.free_space(g, 'c', 'c', 3, 6)
        l_check = [0 for _ in range(3 * 6)]
        self.assertEqual(l, l_check)
        d = {i: 0 for i in range(1, 5, 1)}
        _, _ = Game.set_player_ships(g, 'a1:b1', d)
        l = Game.free_space(g, 'a', 'a', 2, 3)
        l_check = [0 for _ in range(4 * 3)]
        self.assertNotEqual(l, l_check)

    def test_handle_dialog(self):
        pass

    def test_end_of_game(self):
        g = Game.Computer()
        who = g.end_of_game()
        who_check = 'Nobody'
        self.assertEqual(who, who_check)
        g.player_ships = {i: 0 for i in range(1, 5, 1)}
        who = g.end_of_game()
        who_check = "alice"
        self.assertEqual(who, who_check)
        g1 = Game.Computer()
        g1.alice_ships = {i: 0 for i in range(1, 5, 1)}
        who = g1.end_of_game()
        who_check = 'player'
        self.assertEqual(who, who_check)

    def test_clear_board(self):
        g = Game.Computer()
        b = g.alice_board
        self.assertFalse(2 in b)

    def test_create_and_placed_ships(self):
        g = Game.Computer()
        b = g.alice_board
        count = 0
        for row in b:
            for el in row:
                if el == 1:
                    count += 1
        self.assertEqual(count, (1 * 4 + 2 * 3 + 3 * 2 + 4 * 1))

    def test_player_shot(self):
        g = Game.Computer()
        g.alice_board = b_for_ex
        success, c1, c2 = Game.receive_shot('j9')
        self.assertTrue(success)
        self.assertTrue(g.player_shot(c1, c2))
        self.assertEqual(g.alice_board[8][9], -1)
        success, c1, c2 = Game.receive_shot('j1')
        self.assertTrue(success)
        self.assertFalse(g.player_shot(c1, c2))
        self.assertEqual(g.alice_board[0][9], 2)

    def test_req_one(self):
        sessionStorage = {}
        request = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "command": "Что ты умеешь",
                "nlu": {
                    "entities": [],
                    "tokens": [
                        "что",
                        "ты",
                        "умеешь"
                    ]
                },
                "original_utterance": "Что ты умеешь",
                "type": "SimpleUtterance"
            },
            "session": {
                "message_id": 5,
                "new": False,
                "session_id": "766c8360-d2183428-7dc80021-6166061d",
                "skill_id": "7e59ae3a-373f-4657-8987-1bd342e3b348",
                "user_id": "3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A"
            },
            "version": "1.0"
        }
        response = {
            "version": request['version'],
            "session": request['session'],
            "response": {
                'text': 'ha',
                "end_session": False
            }
        }
        Game.handle_dialog(request, response)
        check = {'version': '1.0',
                 'session': {'message_id': 5, 'new': False, 'session_id': '766c8360-d2183428-7dc80021-6166061d',
                             'skill_id': '7e59ae3a-373f-4657-8987-1bd342e3b348',
                             'user_id': '3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A'},
                 'response': {
                     'text': 'Если вы еще не расставили корабли то укажите их координаты.'
                             ' Однопалубные можно ставить, указав лишь одну координату(Например: a1)\n'
                             'Корабли большей длины необходимо ставить, указывая их начальные и конечные координаты\n'
                             'Примеры : a1:a3 или a1:c1\n'
                             'Между любыми кораблями должно быть расстояние минимуум в одну клетку. '
                             'Нельзя ставить корабли полностью или частично за пределы поля.\n'
                             'Если же вы уже рассавили корабли, то вам лишь нужно написать команду- выстрел в формате буква-число. '
                             'Используються первые 10 букв латинсокго алфавита(abcd...). А числа от 1 до 10.\n'
                             'Стрелять за пределы поля и в уже подбитые корабли нельзя',
                     'end_session': False, 'buttons': [{'title': 'Помощь', 'hide': True}]}}
        self.assertEqual(response, check)

    def test_req_two(self):
        sessionStorage = {}
        request = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "command": "",
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "original_utterance": "",
                "type": "SimpleUtterance"
            },
            "session": {
                "message_id": 0,
                "new": True,
                "session_id": "fbfdee58-c6137313-1406eb2c-24fda153",
                "skill_id": "7e59ae3a-373f-4657-8987-1bd342e3b348",
                "user_id": "3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A"
            },
            "version": "1.0"
        }
        response = {
            "version": request['version'],
            "session": request['session'],
            "response": {
                'text': 'ha',
                "end_session": False
            }
        }
        Game.handle_dialog(request, response)
        check1 = {'version': '1.0',
                  'session': {'message_id': 0, 'new': True, 'session_id': 'fbfdee58-c6137313-1406eb2c-24fda153',
                              'skill_id': '7e59ae3a-373f-4657-8987-1bd342e3b348',
                              'user_id': '3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A'},
                  'response': {
                      'text': 'Приветствую! Этот навык явялеться закрытым(он не отобрадаеться в каталоге). '
                              'Расставь свои корабли.\nОднопалубные можно ставить лишь указав одну координату.\n'
                              'Например так : a1 или h10.\n'
                              'Корабли большей длины можно поставить, указав их начальные и конечный координаты через ":"\n'
                              'Например так: a1:a3 или a1:b1\n'
                              'Координаты указываються в виде пары буква - число\n'
                              'Используються первые 10 букв латинсокго алфавита(abcd...). А числа от 1 до 10.\n'
                              'В игре 4 корабля длины 1. 3 длины 2. 2 длины 3. 1 длины 4.\n'
                              'Между любыми кораблями должно быть расстояние минимуум в одну клетку.'
                              ' Нельзя ставить корабли полностью или частично за пределы поля.'
                              'При использовании кнопки random корабли автоматичекси выставятся произвольным образом\nУдачи!',
                      'end_session': False, 'buttons': [{'title': 'random', 'hide': True}]}}

        self.assertEqual(response, check1)
        request = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "command": "a1:b1",
                "nlu": {
                    "entities": [],
                    "tokens": [
                        "a",
                        "1",
                        "b",
                        "1"
                    ]
                },
                "original_utterance": "a1:b1",
                "type": "SimpleUtterance"
            },
            "session": {
                "message_id": 1,
                "new": False,
                "session_id": "fbfdee58-c6137313-1406eb2c-24fda153",
                "skill_id": "7e59ae3a-373f-4657-8987-1bd342e3b348",
                "user_id": "3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A"
            },
            "version": "1.0"
        }
        response = {
            "version": request['version'],
            "session": request['session'],
            "response": {
                'text': 'ha',
                "end_session": False
            }
        }
        Game.handle_dialog(request, response)
        check2 = {'version': '1.0',
                  'session': {'message_id': 1, 'new': False, 'session_id': 'fbfdee58-c6137313-1406eb2c-24fda153',
                              'skill_id': '7e59ae3a-373f-4657-8987-1bd342e3b348',
                              'user_id': '3D95D8CAAAAEEB9E8DA84C9144C0102DDA6BEEE714EB9A6A6E747FB16C27DD5A'},
                  'response': {
                      'text': 'Отлично. Давай следующий.\n'
                              'Вот твое текущее поле\n'
                              '⊗ 🄰 🄱 🄲 🄳 🄴 🄵 🄶 🄷 🄸 🄹\n'
                              '①⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '②⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '③⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '④⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑤⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑥⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑧⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑨⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n'
                              '⑩⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n',
                      'end_session': False, 'buttons': [{'title': 'Помощь', 'hide': True}]}}
        self.assertEqual(response, check2)


if __name__ == '__main__':
    unittest.main()
