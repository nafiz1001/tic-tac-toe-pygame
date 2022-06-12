import asyncio
import sys
import core.game as tictactoe
import core.ai as tictactoe_ai
from client.client import Client


class AIClient(Client):
    def __init__(self) -> None:
        """
        Constructs an AIClient
        """

        super().__init__(self.replay, self.error)
        self.ai = tictactoe_ai.AI()

    def play(self):
        """
        Perform a single move

        Returns:
            An asynchronous task that performs the single move
        """

        parent = super()

        async def __play():
            ttt = await parent.get_tictactoe()
            max_player = parent.get_symbol() == tictactoe.X
            point = self.ai.monte_carlo_method(ttt, max_player, 50)
            if point:
                parent.set_cell_pos(point)
            else:
                print("game is over?")

        return __play()

    def replay(self):
        """
        Equivalent to AIClient.play

        Returns:
            An asynchronous task that performs the single move
        """

        return self.play()

    def error(self, message):
        """Returns a no-op asynchronous task

        Args:
            message: ignored

        Returns:
            A no-op asynchronous task
        """

        return asyncio.sleep(0)

    def start(self, uri, *, join=True, watch=False, key=""):
        """
        Establishes the AIClient's connection with the server
        Both join and watch cannot be True at the same time.

        Args:
            uri: URI of the websocket server
            join: the client wants to join an existing game. Defaults to True.
            watch: the client wants to watch an existing game. Defaults to False.
            key: the key for joining or watching a game.
        
        Returns:
            A Task to establish websocket connection and then use the AI to play the game.
        """

        return super().start(uri, join=join, watch=watch, key=key)


if __name__ == "__main__":
    client = AIClient()

    args = {"join": False, "watch": False, "key": ""}
    if sys.argv[1:3]:
        args[sys.argv[1]] = True
        args["key"] = sys.argv[2]

    asyncio.run(client.start("ws://localhost:8001", **args)())
