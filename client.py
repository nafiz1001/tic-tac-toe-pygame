import json
from typing import Callable
import game
from websockets import client
import asyncio


class Client:
    def __init__(
        self,
        play: Callable[[tuple[int, int], game.SymbolType], None],
        replay: Callable[
            [dict[tuple[int, int], game.SymbolType], game.SymbolType], None
        ],
        win: Callable[[game.SymbolType, list[list[tuple[int, int]]]], None],
        draw: Callable[[], None],
    ) -> None:
        self.symbol = game.O
        self.play = play
        self.replay = replay
        self.win = win
        self.draw = draw
        self.cell_pos = None

    def set_next_move(self, x, y):
        self.cell_pos = (x, y)

    def start(self, uri, *args):
        args = list(*args)

        async def main():
            async with client.connect(uri) as websocket:
                event = {"type": "init"}
                if len(args) == 3:
                    event[args[1]] = args[2]
                elif len(args) > 3:
                    raise Exception()

                print(args)
                await websocket.send(json.dumps(event))

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                        message = json.loads(message)
                        if message["type"] == "init":
                            print(str(message))
                            self.symbol = game.X
                        elif message["type"] == "replay":
                            board_data = message["board"]
                            board = {}
                            for i, p in enumerate(board_data):
                                x = i % 3
                                y = i / 3
                                board[(x, y)] = p
                            s = message["player"]
                            self.replay(board, s)
                        elif message["type"] == "play":
                            x = message["x"]
                            y = message["y"]
                            s = message["player"]
                            self.play((x, y), s)
                        elif message["type"] == "win":
                            self.win(message["player"], message["strats"])
                            return
                        elif message["type"] == "draw":
                            self.draw()
                            return
                        else:
                            print(message)
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

                        print(event)
                        await websocket.send(json.dumps(event))

        return main()
