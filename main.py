import sys, pygame
import tictactoe
import ai

ttt = tictactoe.TicTacToe()
tttai = ai.TicTacToeAI(ttt, tictactoe.X)

pygame.init()

size = width, height = 500, 500
cellsize = cellwidth, cellheight = width / 3, height / 3
cellmin = min(cellsize)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

font = pygame.font.Font(None, int(cellmin))
SYMBOLS = {
    tictactoe.X: font.render("X", True, (0, 0, 0xFF)),
    tictactoe.O: font.render("O", True, (0xFF, 0, 0)),
}


def pos_to_cell(x: int, y: int):
    return x // cellwidth, y // cellheight


def cell_to_pos(x: int, y: int):
    return (cellwidth * (x + 0.5), cellheight * (y + 0.5))


def draw_symbol(x: int, y: int, symbol: str):
    src = SYMBOLS[symbol]
    rect = src.get_rect(center=cell_to_pos(x, y))
    screen.blit(src, rect)


def draw_line(a: tuple[int, int], b: tuple[int, int]):
    pygame.draw.line(screen, 0x00FF00, cell_to_pos(*a), cell_to_pos(*b), 5)


def draw_grid(surface):
    cellrect = pygame.rect.Rect(0, 0, cellwidth, cellheight)

    for y in range(3):
        for x in range(3):
            cellrect.size = cellsize
            cellrect.topleft = (x * cellrect.width, y * cellrect.height)
            pygame.draw.rect(surface, 0x000000, cellrect)
            cellrect.inflate_ip(-2, -2)
            pygame.draw.rect(surface, 0x777777, cellrect)


draw_grid(screen)

while True:
    mouseup = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseup = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ttt.reset()
            draw_grid(screen)

        if not ttt.winner():
            symbol = ttt.curr_player()
            cellpos = None

            if symbol == tictactoe.O and mouseup:
                cellpos = pos_to_cell(*pygame.mouse.get_pos())
            elif symbol == tictactoe.X:
                cellpos = tttai.play()

            if cellpos and ttt.play(*cellpos):
                draw_symbol(*cellpos, symbol)
                res = ttt.winner()
                if res:
                    winner, pos = res
                    draw_line(pos[0], pos[-1])

    pygame.display.flip()
    pygame.time.wait(10)
