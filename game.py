from typing import Iterable
from collections.abc import Callable, Sequence


class Game:
    def __init__(self) -> None:
        pass

    def procedures(self) -> Iterable[Callable[[], "Game"]]:
        pass

    def evaluation_index(self) -> int:
        return 0

    def evaluation(self) -> Sequence[int]:
        return [0]
