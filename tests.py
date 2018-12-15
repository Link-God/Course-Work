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
    def test_init(self):
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

if __name__ == '__main__':
    unittest.main()
