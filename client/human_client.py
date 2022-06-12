import logging
import sys, pygame
import gui.board as board
from client.client import Client
import core.game as tictactoe
import asyncio


class HumanClient(Client):
    def __init__(self, screen: pygame.surface.Surface) -> None:
        """
        Constructrs a HumanClient

        Args:
            screen: an instance of a pygame.surface.Surface
        """

        super().__init__(self.update, self.error)
        self.board = board.Board(screen)
        self.board.draw_grid()
        pygame.display.flip()

    def update_cell_pos(self):
        """
        Sets the next cell to the position of the mouse in the surface
        specified in the constructor.
        """

        cell_pos = self.board.pos_to_cell(*pygame.mouse.get_pos())
        super().set_cell_pos(cell_pos)

    def win(self, winner: tictactoe.SymbolType, strats: list[list[tuple[int, int]]]):
        """
        Called when someone won a game of Tic-Tac-Toe.
        Draws green lines across winning moves.

        Args:
            winner: the winning player
            strats: the winning moves as a list of list of points set by the winning player

        Returns:
            A no-op asynchronous task
        """

        for points in strats:
            self.board.draw_line(points[0], points[-1])
        pygame.display.flip()
        return asyncio.sleep(0)

    def update(self):
        """
        Redraws the entire board keep the board to be up to date with the server.
        Draws green lines if someone won the game.

        Returns:
            An asynchrous task that actually peforms update.
        """

        parent = super()

        async def __update():
            """
            Redraws the entire board keep the board to be up to date with the server.
            Draws green lines if someone won the game.
            """

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

        return __update()

    def error(self, message):
        """
        Indicate to the user the error between the client and server.

        Args:
            message: error message

        Returns:
            A no-op asynchronous task.
        """

        print(message)
        return asyncio.sleep(0)

    def start(self, uri, *, join=True, watch=False, key=""):
        """
        Establish connection with the server and allow the user to play a game of Tic-Tac-Toe with GUI.

        Args:
            uri: URI of the websocket server
            join: the client wants to join an existing game. Defaults to True.
            watch: the client wants to watch an existing game. Defaults to False.
            key: the key for joining or watching a game.

        Returns:
            A Task to establish websocket connection and then allow the user to play the game.
        """

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
    logging.basicConfig(level=logging.INFO)

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
