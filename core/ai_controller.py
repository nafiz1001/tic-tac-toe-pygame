from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class AIController(Generic[T]):
    """
    An abstract game interface primarily designed for artificial intelligence
    """

    def branches(self) -> Iterable[tuple[T, "AIController[T]"]]:
        """
        Returns a sequence of available moves and copies of the next state.
        """

        pass

    def evaluation(self) -> int:
        """
        Returns the approximate/precise evaluation/score of
        the current game state relative to the first player.
        """

        return 0
