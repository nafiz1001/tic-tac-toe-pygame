import sys, pygame
import tictactoe

ttt = tictactoe.TicTacToe()

pygame.init()

size = width, height = 500, 500
cellsize = cellwidth, cellheight = width / 3, height / 3
cellmin = min(cellwidth, cellheight)

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
    textpos = SYMBOLS[symbol].get_rect(center=cell_to_pos(x, y))
    screen.blit(SYMBOLS[symbol], textpos)


def draw_grid(surface):
    cellrect = pygame.rect.Rect(0, 0, cellwidth, cellheight)

    for y in range(3):
        for x in range(3):
            cellrect.size = (cellwidth, cellheight)
            cellrect.topleft = (x * cellrect.width, y * cellrect.height)
            pygame.draw.rect(surface, 0x000000, cellrect)
            cellrect.inflate_ip(-2, -2)
            pygame.draw.rect(surface, 0x777777, cellrect)


draw_grid(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            cellpos = pos_to_cell(*pygame.mouse.get_pos())
            symbol = ttt.curr_player()
            if ttt.play(*cellpos):
                draw_symbol(*cellpos, symbol)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ttt.reset()
            draw_grid(screen)

    pygame.display.flip()
    pygame.time.wait(10)
