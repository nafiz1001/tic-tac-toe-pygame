import random
from typing import TypeVar

from ai_controller import AIController

T = TypeVar("T")


class AI:
    """A general purpose AI that only expects an AIController object to play the game"""

    @staticmethod
    def monte_carlo_method(game: AIController[T], max_player: bool, max_sample: int):
        """Picks the next move using Monte Carlo Method"""

        branches = list(game.branches())

        if branches:
            evaluations = [0 for _ in branches]

            for i, (_, next_turn) in enumerate(branches):
                for _ in range(max_sample):
                    last_turn = next_turn

                    while True:
                        sub_branches = list(last_turn.branches())
                        if sub_branches:
                            last_turn = random.choice(sub_branches)[1]
                        else:
                            evaluations[i] += last_turn.evaluation() * (
                                1 if max_player else -1
                            )
                            break

            best_index, _ = max(enumerate(evaluations), key=lambda x: x[1])
            return branches[best_index][0]
