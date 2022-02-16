import random
import tictactoe


class TicTacToeAI:
    def __init__(self) -> None:
        pass

    def play(self, ttt: tictactoe.TicTacToe):
        symbol = ttt.curr_player()
        open_points = [p for p, s in ttt.curr_board().items() if not s]

        if open_points:
            evaluations = [0] * len(open_points)
            indices = list(range(1, len(evaluations)))

            for i, op in enumerate(open_points):
                path = [op] + [p for p in open_points if p != op]
                for _ in range(100):
                    random.shuffle(indices)
                    for a, b in zip(indices[:-1], indices[1:]):
                        path[a], path[b] = path[b], path[a]

                    newttt = ttt
                    for p in path:
                        newttt = newttt.play(p)

                    res = newttt.curr_state()
                    if isinstance(res, tictactoe.TicTacToe.Win):
                        if res.player == symbol:
                            evaluations[i] += len(res.strats)
                        else:
                            evaluations[i] -= len(res.strats)

            best, _ = max(zip(open_points, evaluations), key=lambda x: x[1])
            return best
