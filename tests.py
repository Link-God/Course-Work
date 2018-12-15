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


if __name__ == '__main__':
    unittest.main()
