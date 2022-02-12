import sys, pygame
import tictactoe

ttt = tictactoe.TicTacToe()

pygame.init()

size = width, height = 500, 500
cellsize = cellwidth, cellheight = width / 3, height / 3

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

font = pygame.font.Font(None, int(min(cellwidth, cellheight)))
SYMBOLS = {
    tictactoe.TicTacToe.X: font.render("X", True, (0, 0, 0xFF)),
    tictactoe.TicTacToe.O: font.render("O", True, (0xFF, 0, 0)),
}


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
            pos = pygame.mouse.get_pos()
            pos = (pos[0] // cellwidth, pos[1] // cellheight)
            curr_player = ttt.curr_player()
            if ttt.play(*pos):
                textpos = SYMBOLS[curr_player].get_rect(
                    x=pos[0] * cellwidth, y=pos[1] * cellheight
                )
                screen.blit(SYMBOLS[curr_player], textpos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ttt.reset()
            draw_grid(screen)

    pygame.display.flip()
    pygame.time.wait(10)
