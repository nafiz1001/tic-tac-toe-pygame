import sys, pygame
import board as board
import client as tictactoe_client
import game as tictactoe
import asyncio

# initialize pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

# initialize board
board = board.Board(screen)

board.draw_grid()
# update display
pygame.display.flip()

# initialize client interface


def play(point, symbol):
    board.draw_symbol(*point, symbol)
    pygame.display.flip()


def replay(curr_board: dict, curr_player):
    board.draw_grid()
    for (x, y), p in curr_board.items():
        if p != tictactoe.EMPTY_CELL:
            board.draw_symbol(x, y, p)
    pygame.display.flip()


def win(player, strats):
    print(player)
    for points in strats:
        board.draw_line(points[0], points[-1])
    pygame.display.flip()


def draw():
    print("draw")


client = tictactoe_client.Client(play, replay, win, draw)


def gui_task():
    mouseup = False
    # main loop
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            # player wants to exit
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            # player clicked completely
            mouseup = True

        if mouseup:
            # it is the player's turn
            cell_pos = board.pos_to_cell(*pygame.mouse.get_pos())
            client.set_next_move(*cell_pos)
            mouseup = False


def websocket_task():
    asyncio.run(client.start("ws://localhost:8001", sys.argv))


from threading import Thread

p = Thread(target=websocket_task, daemon=True)
p.start()

gui_task()
