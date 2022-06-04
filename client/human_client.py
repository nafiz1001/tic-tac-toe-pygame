import sys, pygame
import gui.board as board
from client.client import Client
import core.game as tictactoe
import asyncio


class HumanClient(Client):
    def __init__(self, screen: pygame.surface.Surface) -> None:
        super().__init__(self.replay, self.error)
        self.board = board.Board(screen)
        self.board.draw_grid()
        pygame.display.flip()

    def update_cell_pos(self):
        cell_pos = self.board.pos_to_cell(*pygame.mouse.get_pos())
        super().set_cell_pos(cell_pos)

    def win(self, winner, strats):
        for points in strats:
            self.board.draw_line(points[0], points[-1])
        pygame.display.flip()
        return asyncio.sleep(0)

    def replay(self):
        parent = super()

        async def __replay():
            ttt = await parent.get_tictactoe()

            curr_board = ttt.get_board()
            self.board.draw_grid()
            for (x, y), p in curr_board.items():
                if p != tictactoe.EMPTY_CELL:
                    self.board.draw_symbol(x, y, p)
            pygame.display.flip()

            state = ttt.get_state()
            if isinstance(state, tictactoe.Win):
                await self.win(state.player, state.strats)

        return __replay()

    def error(self, message):
        print(message)
        return asyncio.sleep(0)

    def start(self, uri, *, join=True, watch=False, key=""):
        websocket_task = super().start(uri, join=join, watch=watch, key=key)

        async def human_task():
            mouseup = False
            # main loop
            while True:
                event = pygame.event.wait(10)
                if event.type == pygame.QUIT:
                    # player wants to exit
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    # player clicked completely
                    mouseup = True
                elif event.type == pygame.NOEVENT:
                    await asyncio.sleep(0)

                if mouseup:
                    mouseup = False
                    self.update_cell_pos()

        async def gather():
            await asyncio.gather(websocket_task(), human_task())

        return gather


if __name__ == "__main__":
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tic-Tac-Toe")

    client = HumanClient(screen)

    args = {"join": False, "watch": False, "key": ""}
    if sys.argv[1:3]:
        args[sys.argv[1]] = True
        args["key"] = sys.argv[2]

    asyncio.run(client.start("ws://localhost:8001", **args)())
