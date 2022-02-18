import sys, pygame
import tictactoe
import tictactoe_board as board
import ai
import random

ttt = tictactoe.TicTacToe.new()
tttai = ai.AI()
tttai_symbol = random.choice(tictactoe.PLAYERS)

pygame.init()

size = width, height = 500, 500

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

board = board.TicTacToeBoard(screen)

board.draw_grid()
while True:
    mouseup = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseup = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ttt = tictactoe.TicTacToe.new()
            tttai_symbol = random.choice(tictactoe.PLAYERS)
            board.draw_grid()

        if isinstance(ttt.curr_state(), tictactoe.TicTacToe.InProgress):
            symbol = ttt.curr_player()
            cellpos = None

            if symbol != tttai_symbol and mouseup:
                cellpos = board.pos_to_cell(*pygame.mouse.get_pos())
            elif symbol == tttai_symbol:

                def cast(g) -> tictactoe.TicTacToe:
                    return g

                newgame = cast(tttai.mcts(ttt, 100))
                cellpos = newgame.point_added()

            if cellpos:
                newttt = ttt.play(cellpos)
                if newttt is not ttt:
                    ttt = newttt
                    board.draw_symbol(*cellpos, symbol)
                    res = ttt.curr_state()
                    if isinstance(res, tictactoe.TicTacToe.Win):
                        for points in res.strats:
                            board.draw_line(points[0], points[-1])

    pygame.display.flip()
    pygame.time.wait(10)
