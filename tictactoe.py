X = "x"
O = "o"
EMPTY = ""
PLAYERS = [X, O]

WINNING_STRATS = (
    # horizontal
    [[(x, y) for x in range(3)] for y in range(3)]
    # vertical
    + [[(x, y) for y in range(3)] for x in range(3)]
    # top left - bottom right
    + [[(i, i) for i in range(3)]]
    # top right - bottom left
    + [[(2 - i, i) for i in range(3)]]
)

STRATS = {
    (x, y): [strat for strat in WINNING_STRATS if (x, y) in strat]
    for y in range(3)
    for x in range(3)
}


class TicTacToe:
    def __init__(self, ttt: "TicTacToe" = None):
        self.reset()
        if ttt:
            self.board.update(ttt.board)
            self.state = ttt.state
            self.turn = ttt.turn

    def reset(self):
        self.board = {(x, y): EMPTY for y in range(3) for x in range(3)}
        self.state: TicTacToe.InProgress | TicTacToe.Draw | TicTacToe.Win = (
            TicTacToe.InProgress()
        )
        self.turn = 0

    def curr_board(self):
        return self.board

    def curr_player(self):
        return PLAYERS[self.turn]

    def curr_state(self):
        return self.state

    def play(self, x: int, y: int):
        if self.board[(x, y)] in PLAYERS:
            return False
        elif not isinstance(self.state, TicTacToe.InProgress):
            return False
        else:
            self.board[(x, y)] = self.curr_player()
            for points in STRATS[(x, y)]:
                states = [self.board[p] for p in points]
                if states[0] in PLAYERS:
                    count = states.count(states[0])
                    if count == 3:
                        if isinstance(self.state, TicTacToe.Win):
                            self.state.strats.append(list(points))
                        else:
                            self.state = TicTacToe.Win(states[0], [list(points)])

            if isinstance(self.state, TicTacToe.InProgress):
                if all(s for s in self.board.values()):
                    self.state = TicTacToe.Draw()
                else:
                    self.turn = (self.turn + 1) % len(PLAYERS)

            return True

    class InProgress:
        def __init__(self) -> None:
            pass

    class Win:
        def __init__(self, player: str, strats: list[list[tuple[int, int]]]) -> None:
            self.player = player
            self.strats = strats

    class Draw:
        def __init__(self) -> None:
            pass
