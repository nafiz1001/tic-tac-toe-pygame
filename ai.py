import functools
import random
import tictactoe


class TicTacToeAI:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def play(self, ttt: tictactoe.TicTacToe):
        if ttt.curr_player() == self.symbol:
            state = ttt.curr_board()
            open_points = [k for k in state if not state[k]]

            if open_points:
                evaluations = [0] * len(open_points)
                indices = list(range(1, len(evaluations)))

                for i, op in enumerate(open_points):
                    path = [op] + [p for p in open_points if p != op]
                    for _ in range(100):
                        random.shuffle(indices)
                        for a, b in zip(indices[:-1], indices[1:]):
                            path[a], path[b] = path[b], path[a]

                        newttt = functools.reduce(tictactoe.TicTacToe.play, path, ttt)

                        res = newttt.curr_state()
                        if isinstance(res, tictactoe.TicTacToe.Win):
                            if res.player == self.symbol:
                                evaluations[i] += len(res.strats)
                            else:
                                evaluations[i] -= len(res.strats)

                best, _ = max(zip(open_points, evaluations), key=lambda x: x[1])
                return best
