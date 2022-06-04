import json
import core.game as game
from websockets import client
import asyncio

import pickle
import base64


class Client:
    def __init__(
        self,
        replay,
        error,
    ) -> None:
        self.symbol = game.O
        self.cell_pos = None
        self.replay = replay
        self.error = error

        self.ttt = None

    def get_symbol(self):
        return self.symbol

    async def get_tictactoe(self) -> game.TicTacToe:
        while self.ttt is None:
            await asyncio.sleep(0.1)

        return self.ttt

    def set_cell_pos(self, pos: tuple[int, int]):
        self.cell_pos = pos

    def start(self, uri, *, join=True, watch=False, key=""):
        async def websocket_task():
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
                        print(str(message))

                        if message["type"] == "init":
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
                        self.cell_pos = None
                        await websocket.send(json.dumps(event))

                        print(event)

        return websocket_task
