import random
import tictactoe


class TicTacToeAI:
    def __init__(self, ttt: tictactoe.TicTacToe, symbol: str) -> None:
        self.ttt = ttt
        self.symbol = symbol

    def play(self):
        if self.ttt.curr_player() == self.symbol:
            state = self.ttt.curr_board()
            open_points = [k for k in state if not state[k]]

            if open_points:
                evaluations = [0] * len(open_points)
                for i, op in enumerate(open_points):
                    remaining_points = [p for p in open_points if p != op]

                    for _ in range(50):
                        newttt = tictactoe.TicTacToe(self.ttt)
                        newttt.play(*op)

                        random.shuffle(remaining_points)
                        for rp in remaining_points:
                            res = newttt.curr_state()
                            if isinstance(res, tictactoe.TicTacToe.Win):
                                if res.player == self.symbol:
                                    evaluations[i] += len(res.strats)
                                else:
                                    evaluations[i] -= len(res.strats)
                                break
                            elif isinstance(res, tictactoe.TicTacToe.Draw):
                                break

                            newttt.play(*rp)

                best, _ = max(zip(open_points, evaluations), key=lambda x: x[1])
                return best
