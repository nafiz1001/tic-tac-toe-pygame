import tictactoe
import pygame


class TicTacToeBoard:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.size = self.width, self.height = self.surface.get_size()
        self.cellsize = self.cellwidth, self.cellheight = (
            self.width // 3,
            self.height // 3,
        )
        self.cellmin = min(self.cellsize)

        font = pygame.font.Font(None, int(self.cellmin))
        self.symbols = {
            tictactoe.X: font.render("X", True, (0, 0, 0xFF)),
            tictactoe.O: font.render("O", True, (0xFF, 0, 0)),
        }

    def pos_to_cell(self, x: int, y: int):
        return x // self.cellwidth, y // self.cellheight

    def cell_to_pos(self, x: int, y: int):
        return (self.cellwidth * (x + 0.5), self.cellheight * (y + 0.5))

    def draw_symbol(self, x: int, y: int, symbol: str):
        src = self.symbols[symbol]
        rect = src.get_rect(center=self.cell_to_pos(x, y))
        self.surface.blit(src, rect)

    def draw_line(self, a: tuple[int, int], b: tuple[int, int]):
        pygame.draw.line(
            self.surface, 0x00FF00, self.cell_to_pos(*a), self.cell_to_pos(*b), 5
        )

    def draw_grid(self):
        cellrect = pygame.rect.Rect(0, 0, self.cellwidth, self.cellheight)

        for y in range(3):
            for x in range(3):
                cellrect.size = self.cellsize
                cellrect.topleft = (x * cellrect.width, y * cellrect.height)
                pygame.draw.rect(self.surface, 0x000000, cellrect)
                cellrect.inflate_ip(-2, -2)
                pygame.draw.rect(self.surface, 0x777777, cellrect)
