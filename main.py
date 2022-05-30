import sys, pygame
import tictactoe
import tictactoe_board as board
import ai
import random

# create tic-tac-toe instance
ttt = tictactoe.TicTacToe()

# create tic-tac-toe AI
tttai = ai.AI()

# initialize symbol for ai
tttai_symbol = random.choice(tictactoe.PLAYERS)

# initialize pygame
pygame.init()

size = width, height = 500, 500

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

# initialize board
board = board.TicTacToeBoard(screen)

board.draw_grid()
# update display
pygame.display.flip()

print(str(ttt))

mouseup = False

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # player wants to exit
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            # player clicked completely
            mouseup = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # player wants to restart the game
            ttt = tictactoe.TicTacToe()
            tttai_symbol = random.choice(tictactoe.PLAYERS)

            board.draw_grid()
            # updates display
            pygame.display.flip()

            print(str(ttt))

        if isinstance(ttt.get_state(), tictactoe.InProgress):
            symbol = ttt.get_player()
            cell_pos = None

            if symbol != tttai_symbol and mouseup:
                # it is the player's turn
                cell_pos = board.pos_to_cell(*pygame.mouse.get_pos())
                mouseup = False
            elif symbol == tttai_symbol:
                # it is the AI's turn
                max_player = tttai_symbol == tictactoe.X
                cell_pos = tttai.monte_carlo_method(ttt, max_player, 50)

            if cell_pos:
                try:
                    # attempt to draw at cell_pos
                    ttt.play(cell_pos)
                    board.draw_symbol(*cell_pos, symbol)
                    res = ttt.get_state()
                    if isinstance(res, tictactoe.Win):
                        # someone won the game, so draw
                        # lines on matching cells
                        for points in res.strats:
                            board.draw_line(points[0], points[-1])

                except tictactoe.IllegalMove as e:
                    print(str(e))

                # update display
                pygame.display.flip()

                print(str(ttt))
