import random

from game import Game


class AI:
    def __init__(self) -> None:
        pass

    def mcts(self, game: Game, max_sample: int) -> Game:
        procedures = list(game.procedures())

        if procedures:
            index = game.evaluation_index()
            evaluations = [0] * len(procedures)

            for i, procedure in enumerate(procedures):
                newgame = procedure()

                for _ in range(max_sample):
                    newnewgame = newgame
                    newnewprocedures = list(newnewgame.procedures())

                    while newnewprocedures:
                        newnewgame = random.choice(newnewprocedures)()
                        newnewprocedures = list(newnewgame.procedures())

                    evaluations[i] += newnewgame.evaluation()[index]

            best_index, _ = max(enumerate(evaluations), key=lambda x: x[1])
            return procedures[best_index]()
