import typing

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
    def __init__(
        self,
        board: dict[tuple[int, int], str],
        state: typing.Union["TicTacToe.InProgress", "TicTacToe.Draw", "TicTacToe.Win"],
        turn: int,
    ):
        self.board = board
        self.state = state
        self.turn = turn

    @staticmethod
    def new():
        return TicTacToe(
            {(x, y): EMPTY for y in range(3) for x in range(3)},
            TicTacToe.InProgress(),
            0,
        )

    def __dict(self):
        return {
            "board": dict(self.board),
            "state": self.state.copy(),
            "turn": self.turn,
        }

    def curr_board(self):
        return self.board

    def curr_player(self):
        return PLAYERS[self.turn]

    def curr_state(self):
        return self.state

    def play(self, x: int, y: int):
        if self.board[(x, y)] in PLAYERS:
            return self
        elif not isinstance(self.state, TicTacToe.InProgress):
            return self
        else:
            newttt = TicTacToe(**self.__dict())
            newttt.board[(x, y)] = newttt.curr_player()
            for points in STRATS[(x, y)]:
                states = [newttt.board[p] for p in points]
                if states[0] in PLAYERS:
                    count = states.count(states[0])
                    if count == 3:
                        if isinstance(newttt.state, TicTacToe.Win):
                            newttt.state.strats.append(points)
                        else:
                            newttt.state = TicTacToe.Win(states[0], [points])

            if isinstance(newttt.state, TicTacToe.InProgress):
                if all(s for s in newttt.board.values()):
                    newttt.state = TicTacToe.Draw()
                else:
                    newttt.turn = (newttt.turn + 1) % len(PLAYERS)

            return newttt

    class InProgress:
        def __init__(self) -> None:
            pass

        def copy(self):
            return self

    class Win:
        def __init__(self, player: str, strats: list[list[tuple[int, int]]]) -> None:
            self.player = player
            self.strats = strats

        def copy(self):
            return self

    class Draw:
        def __init__(self) -> None:
            pass

        def copy(self):
            return self
