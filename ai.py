import random
import tictactoe


class TicTacToeAI:
    def __init__(self, ttt: tictactoe.TicTacToe, symbol: str) -> None:
        self.ttt = ttt
        self.symbol = symbol

    def play(self):
        if self.ttt.curr_player() == self.symbol:
            state = self.ttt.state
            open_points = [k for k in state if not state[k]]

            if open_points:
                evaluations = list[int]()
                for op in open_points:
                    remaining_points = [p for p in open_points if p != op]
                    evaluation = 0

                    for _ in range(50):
                        newttt = tictactoe.TicTacToe(self.ttt)
                        newttt.play(*op)

                        random.shuffle(remaining_points)
                        for rp in remaining_points:
                            res = newttt.winner()
                            if res:
                                winner, _ = res
                                if winner == self.symbol:
                                    evaluation += 1
                                else:
                                    evaluation -= 2
                                break
                            elif newttt.draw():
                                break

                            newttt.play(*rp)

                    evaluations.append(evaluation)

                best, _ = max(zip(open_points, evaluations), key=lambda x: x[1])
                return best
