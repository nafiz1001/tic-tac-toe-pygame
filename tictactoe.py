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
        prev_ttt: Union["TicTacToe", None],
        prev_point: tuple[int, int] | None,
        prev_player: SymbolType,
    ):
        super().__init__()

        self.__prev_ttt = prev_ttt
        self.__prev_point = prev_point
        self.__prev_player = prev_player
        self.__curr_player = [X, O, X][self.__prev_player]
        self.__curr_state = TicTacToe.InProgress()
        self.__hash = hash(
            (
                *sorted(ttt.point_added() for ttt in self.__rev_path()),
                self.curr_player(),
            )
        )

        if self.__prev_ttt and self.__prev_point and self.__prev_player != EMPTY_CELL:
            board = self.curr_board()
            for strat in STRATS[self.__prev_point]:
                states = [board[p] for p in strat]
                if states[0] in PLAYERS:
                    count = states.count(states[0])
                    if count == 3:
                        if isinstance(self.__curr_state, TicTacToe.Win):
                            self.__curr_state.strats.append(strat)
                        else:
                            self.__curr_state = TicTacToe.Win(states[0], [strat])
            if isinstance(self.__curr_state, TicTacToe.InProgress) and all(
                board[p] != EMPTY_CELL for p in board
            ):
                self.__curr_state = TicTacToe.Draw()

    @staticmethod
    def new():
        return TicTacToe(
            None,
            None,
            EMPTY_CELL,
        )

    def __rev_path(self):
        ttt = self
        while ttt and ttt.__prev_point and ttt.__prev_player != EMPTY_CELL:
            yield ttt
            ttt = ttt.__prev_ttt

    def curr_board(self):
        board = dict(EMPTY_BOARD)
        board.update({ttt.__prev_point: ttt.__prev_player for ttt in self.__rev_path()})

        return board

    def curr_player(self):
        return self.__curr_player

    def curr_state(self):
        return self.__curr_state

    def point_added(self):
        return self.__prev_point

    def __repr__(self) -> str:
        games = reversed(list(self.__rev_path()))
        to_symbol = {X: "X", O: "O"}
        return "TicTacToe: " + " -> ".join(
            f"{to_symbol[g.__prev_player]}{g.__prev_point}" for g in games
        )

    def __hash__(self) -> int:
        return self.__hash

    def play(self, target: tuple[int, int]):
        board = self.curr_board()
        if board[target] in PLAYERS:
            return self
        elif not isinstance(self.__curr_state, TicTacToe.InProgress):
            return self
        else:
            return TicTacToe(self, target, self.curr_player())

    def procedures(self) -> Iterable[Callable[[], "TicTacToe"]]:
        def procedure(p):
            def execute():
                return self.play(p)

            return execute

        if isinstance(self.curr_state(), TicTacToe.InProgress):
            for p, s in self.curr_board().items():
                if s == EMPTY_CELL:
                    yield procedure(p)

    def evaluation_index(self) -> int:
        return self.curr_player() - 1

    def evaluation(self) -> Sequence[int]:
        state = self.curr_state()
        if isinstance(state, TicTacToe.Win):
            if state.player == X:
                return (len(state.strats), -len(state.strats))
            else:
                return (-len(state.strats), len(state.strats))
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
