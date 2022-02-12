import random
import tictactoe


class TicTacToeAI:
    def __init__(self, ttt: tictactoe.TicTacToe, symbol: str) -> None:
        self.ttt = ttt
        self.symbol = symbol

    def play(self):
        state = self.ttt.state
        open_points = [k for k in state if not state[k]]
        if open_points:
            choice = random.choice(open_points)
            return choice
