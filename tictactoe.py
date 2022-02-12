import random

X = "x"
O = "o"
PLAYERS = [X, O]


class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {(x, y): "" for y in range(3) for x in range(3)}
        self.turn = random.randint(0, len(PLAYERS) - 1)

    def curr_player(self):
        return PLAYERS[self.turn]

    def play(self, x: int, y: int):
        if self.state[(x, y)] in PLAYERS:
            return False
        else:
            self.state[(x, y)] = self.curr_player()
            self.turn = (self.turn + 1) % len(PLAYERS)
            return True

    def __winner(self, points: list[tuple[int, int]]):
        h = [self.state[p] for p in points]
        if h[0] in PLAYERS:
            count = h.count(h[0])
            if count == 3:
                return h[0]

        return None

    def game_over(self):
        # horizontal
        for y in range(3):
            points = [(x, y) for x in range(3)]
            player = self.__winner(points)
            if player:
                return player, points

        # vertical
        for x in range(3):
            points = [(x, y) for y in range(3)]
            player = self.__winner(points)
            if player:
                return player, points

        # top left - bottom right
        points = [(i, i) for i in range(3)]
        player = self.__winner(points)
        if player:
            return player, points

        del points
        del player

        # top right - bottom left
        points = [(2 - i, i) for i in range(3)]
        player = self.__winner(points)
        if player:
            return player, points

        del points
        del player
