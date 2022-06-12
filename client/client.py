import json
import logging
from typing import Callable
import core.game as game
from websockets import client
import asyncio


class Client:
    def __init__(
        self,
        replay: Callable[[], None],
        error: Callable[[str], None],
    ) -> None:
        """
        Constructs a Client

        Args:
            replay: replay function
            error: error function
        """

        self.symbol = game.O
        self.cell_pos = None
        self.replay = replay
        self.error = error

        self.ttt = None

    def get_symbol(self) -> game.SymbolType:
        """
        Returns the current symbol of the client

        Returns:
            The current symbol of the client
        """

        return self.symbol

    async def get_tictactoe(self) -> game.TicTacToe:
        """
        Returns a Tic-Tac-Toe Game representing the current state of the game

        Returns:
            a Tic-Tac-Toe Game
        """

        while self.ttt is None:
            await asyncio.sleep(0.1)

        return self.ttt

    def set_cell_pos(self, pos: tuple[int, int]):
        """
        Tell the server your next move.

        Args:
            pos: a tuple representing the position x, y
        """

        self.cell_pos = pos

    def start(self, uri: str, *, join=True, watch=False, key=""):
        """
        Start the Client's connection with the server
        Both join and watch cannot be True at the same time.

        Args:
            uri: URI of the websocket server
            join: the client wants to join an existing game. Defaults to True.
            watch: the client wants to watch an existing game. Defaults to False.
            key: the key for joining or watching a game.
        
        Returns:
            A Task to establish websocket connection and then play the game.
        """

        async def websocket_task():
            """
            The actual asynchronous task for establishing connection and playing Tic-Tac-Toe.

            Raises:
                Exception: received an unknown type of response from the server
            """

            async with client.connect(uri) as websocket:
                event = {"type": "init"}
                if join:
                    event["join"] = key
                elif watch:
                    event["watch"] = key

                await websocket.send(json.dumps(event))

                while True:
                    try:
                        message = await asyncio.wait_for(
                            websocket.recv(), timeout=0.001
                        )
                        message = json.loads(message)
                        # print(str(message))

                        if message["type"] == "init":
                            print(f"python -m [client module] join {message['join']}")
                            print(f"python -m [client module] watch {message['watch']}")

                            self.ttt = game.TicTacToe.from_dict(message["data"])
                            self.symbol = game.X
                            await self.replay()
                        elif message["type"] == "replay":
                            self.ttt = game.TicTacToe.from_dict(message["data"])
                            await self.replay()
                        elif message["type"] == "error":
                            await self.error(message["message"])
                        else:
                            raise Exception("unknown type")
                    except asyncio.TimeoutError:
                        pass

                    if self.cell_pos:
                        x, y = self.cell_pos
                        event = {
                            "type": "play",
                            "x": x,
                            "y": y,
                        }
                        logging.info(f"{game.TicTacToe.symbol_to_str(self.symbol)} at ({x}, {y})")

                        self.cell_pos = None
                        await websocket.send(json.dumps(event))


        return websocket_task
