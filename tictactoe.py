import random

X = "x"
O = "o"
PLAYERS = [X, O]


class TicTacToe:
    def __init__(self, ttt: "TicTacToe" = None):
        self.reset()
        if ttt:
            self.state.update(ttt.state)
            self.turn = ttt.turn

    def reset(self):
        self.state = {(x, y): "" for y in range(3) for x in range(3)}
        self.turn = 0

    def curr_player(self):
        return PLAYERS[self.turn]

    def play(self, x: int, y: int):
        if self.state[(x, y)] in PLAYERS:
            return False
        else:
            self.state[(x, y)] = self.curr_player()
            self.turn = (self.turn + 1) % len(PLAYERS)
            return True

    def winner(self):
        def helper(points: list[tuple[int, int]]):
            states = [self.state[p] for p in points]
            if states[0] in PLAYERS:
                count = states.count(states[0])
                if count == 3:
                    return states[0]

            return None

        # horizontal
        for y in range(3):
            points = [(x, y) for x in range(3)]
            player = helper(points)
            if player:
                return player, points

        # vertical
        for x in range(3):
            points = [(x, y) for y in range(3)]
            player = helper(points)
            if player:
                return player, points

        # top left - bottom right
        points = [(i, i) for i in range(3)]
        player = helper(points)
        if player:
            return player, points

        # top right - bottom left
        points = [(2 - i, i) for i in range(3)]
        player = helper(points)
        if player:
            return player, points
