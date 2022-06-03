from ai_controller import AIController

SymbolType = int
EMPTY_CELL = SymbolType(0)
X = SymbolType(1)
O = SymbolType(2)
PLAYERS = [X, O]

WINNING_STRATS = (
    # horizontal
    [[(x, y) for x in range(3)] for y in range(3)]
    # vertical
    + [[(x, y) for y in range(3)] for x in range(3)]
    # top left to bottom right
    + [[(i, i) for i in range(3)]]
    # top right to bottom left
    + [[(2 - i, i) for i in range(3)]]
)

STRATS = {
    (x, y): [strat for strat in WINNING_STRATS if (x, y) in strat]
    for y in range(3)
    for x in range(3)
}

EMPTY_BOARD = 0


class IllegalMove(Exception):
    """The exception thrown if the player makes an illegal move"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args[0]

    def __str__(self) -> str:
        return self.message


class InProgress:
    """Represents the in-progress state of the game"""

    def __init__(self) -> None:
        pass


class Win:
    """
    Represents the winning state of the
    game including the winning player and
    the winning moves to win the game
    """

    def __init__(self, player: SymbolType, strats: list[list[tuple[int, int]]]) -> None:
        self.player = player
        self.strats = strats


class Draw:
    """Represents the draw state of the game"""

    def __init__(self) -> None:
        pass


class TicTacToe(AIController[tuple[int, int]]):
    """
    A class to represent a tic-tac-toe game.
    """

    def __init__(
        self,
        player: SymbolType = X,
        board: dict[tuple[int, int], SymbolType] = EMPTY_BOARD,
        state: Draw | InProgress | Win = InProgress(),
        last_move: tuple[int, int] | None = None,
    ):
        """Constructs a TicTacToe instance"""

        self.player = player
        self.board = (
            {(x, y): EMPTY_CELL for y in range(3) for x in range(3)}
            if board is EMPTY_BOARD
            else board
        )
        self.state = state
        self.last_move = last_move

    def get_board(self):
        """Returns the current board"""

        return self.board

    def get_player(self):
        """Returns current player"""

        return self.player

    @staticmethod
    def symbol_to_str(symbol: SymbolType):
        """Returns string representation of symbol"""

        return ["?", "X", "O"][symbol]

    def get_state(self):
        """Returns current state of the game"""

        return self.state

    def __str__(self):
        """Returns the current state of the game in string format"""

        board = "\n".join(
            [
                "".join([TicTacToe.symbol_to_str(self.board[(x, y)]) for x in range(3)])
                for y in range(3)
            ]
        )
        return f"{self.player}\n{board}\n{self.state}\n{self.last_move}"

    def play(self, target: tuple[int, int]):
        """
        Plays a single round by marking a cell at (target[0], target[1]).
        Throws IllegalMove exception if the cell is already occupied
        or the game is not in progress (i.e. someone won or tied).
        """

        if self.board[target] in PLAYERS:
            raise IllegalMove(f"Cell at ({target[0]}, {target[1]}) already occupied")
        elif not isinstance(self.state, InProgress):
            raise IllegalMove(f"The  game is not in progress")
        else:
            self.board[target] = self.player
            self.last_move = target

            # determine new game state
            for strat in STRATS[target]:
                count = sum(self.player == self.board[p] for p in strat)
                if count == 3:
                    if isinstance(self.state, Win):
                        self.state.strats.append(strat)
                    else:
                        self.state = Win(self.player, [strat])
            if isinstance(self.state, InProgress) and all(
                self.board[p] != EMPTY_CELL for p in self.board
            ):
                self.state = Draw()

            # switch to next player
            self.player = [EMPTY_CELL, O, X][self.player]

    def copy(self):
        """Returns a copy of self."""

        return TicTacToe(
            player=self.player,
            board={(x, y): self.board[(x, y)] for y in range(3) for x in range(3)},
            state=self.state,
            last_move=self.last_move,
        )

    def branches(self):
        """
        Returns a sequence of available moves and copies of the next
        game state. It comes in handy when implementing an AI.
        """

        if isinstance(self.state, InProgress):
            for p, s in self.board.items():
                if s == EMPTY_CELL:
                    ttt = self.copy()
                    ttt.play(p)
                    yield p, ttt

    def evaluation(self):
        """
        Returns the approximate/precise evaluation/score of the
        current game state relative to the first player which is "X".
        It comes in handy when implementing an AI.
        """

        if isinstance(self.state, Win):
            if self.state.player == X:
                return len(self.state.strats)
            else:
                return -len(self.state.strats)
        else:
            return 0
