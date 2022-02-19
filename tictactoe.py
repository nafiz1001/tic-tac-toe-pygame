from collections.abc import Callable, Sequence
from typing import Iterable, Union
from game import Game

SymbolType = int
EMPTY_CELL = SymbolType(0)
X = SymbolType(1)
O = SymbolType(2)
PLAYERS = [X, O]

EMPTY_BOARD = {(x, y): EMPTY_CELL for y in range(3) for x in range(3)}

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


class TicTacToe(Game):
    def __init__(
        self,
        ttt: Union["TicTacToe", None],
        point: Union[tuple[int, int], None],
    ):
        super().__init__()

        self.player = PLAYERS[ttt.player % len(PLAYERS) if ttt else 0]
        self.board = dict(ttt.board) if ttt else dict(EMPTY_BOARD)
        self.point = point
        self.state = TicTacToe.InProgress()

        if point and ttt:
            self.board[point] = ttt.player
            for strat in STRATS[point]:
                count = sum(ttt.player == self.board[p] for p in strat)
                if count == 3:
                    if isinstance(self.state, TicTacToe.Win):
                        self.state.strats.append(strat)
                    else:
                        self.state = TicTacToe.Win(ttt.player, [strat])
            if isinstance(self.state, TicTacToe.InProgress) and all(
                self.board[p] != EMPTY_CELL for p in self.board
            ):
                self.state = TicTacToe.Draw()

    @staticmethod
    def new():
        return TicTacToe(
            None,
            None,
        )

    def curr_board(self):
        return self.board.items()

    def curr_player(self):
        return self.player

    def curr_state(self):
        return self.state

    def point_added(self):
        return self.point

    def play(self, target: tuple[int, int]):
        if self.board[target] in PLAYERS:
            return self
        elif not isinstance(self.state, TicTacToe.InProgress):
            return self
        else:
            return TicTacToe(self, target)

    def procedures(self) -> Iterable[Callable[[], "TicTacToe"]]:
        def procedure(p):
            def execute():
                return self.play(p)

            return execute

        if isinstance(self.state, TicTacToe.InProgress):
            for p, s in self.board.items():
                if s == EMPTY_CELL:
                    yield procedure(p)

    def evaluation_index(self) -> int:
        return self.player - 1

    def evaluation(self) -> Sequence[int]:
        if isinstance(self.state, TicTacToe.Win):
            if self.state.player == X:
                return (len(self.state.strats), -len(self.state.strats))
            else:
                return (-len(self.state.strats), len(self.state.strats))
        else:
            return (0, 0)

    class InProgress:
        def __init__(self) -> None:
            pass

    class Win:
        def __init__(
            self, player: SymbolType, strats: list[list[tuple[int, int]]]
        ) -> None:
            self.player = player
            self.strats = strats

    class Draw:
        def __init__(self) -> None:
            pass
