import random
import game


class GameAI:
    def __init__(self) -> None:
        pass

    def play(self, game: game.Game) -> game.Game:
        procedures = list(game.procedures())

        if procedures:
            index = game.evaluation_index()
            evaluations = [0] * len(procedures)

            for i, procedure in enumerate(procedures):
                newgame = procedure()

                for _ in range(100):
                    newnewgame = newgame
                    newnewprocedures = list(newnewgame.procedures())

                    while newnewprocedures:
                        newnewgame = random.choice(newnewprocedures)()
                        newnewprocedures = list(newnewgame.procedures())

                    evaluations[i] += newnewgame.evaluation()[index]

            best_index, _ = max(enumerate(evaluations), key=lambda x: x[1])
            return procedures[best_index]()
