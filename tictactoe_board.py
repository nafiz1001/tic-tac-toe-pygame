import tictactoe
import pygame


class TicTacToeBoard:
    def __init__(self, surface: pygame.Surface) -> None:
        """Constructs a TicTacToeBoard instance"""

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
        """
        Converts position in pixel inside surface to
        2-D cell position that ranges from [0, 3).
        """

        return min(x // self.cellwidth, 2), min(y // self.cellheight, 2)

    def cell_to_pos(self, x: int, y: int):
        """
        Converts cell position ([0, 2]) to the
        position of the cell's middle in pixel unit.
        """

        return (self.cellwidth * (x + 0.5), self.cellheight * (y + 0.5))

    def draw_symbol(self, x: int, y: int, symbol: str):
        """
        Draws symbol at cell x, y.
        It draws an 'X' if the symbol is 'X'.
        It draws an 'O' if the symbol is 'O'.
        """

        src = self.symbols[symbol]
        rect = src.get_rect(center=self.cell_to_pos(x, y))
        self.surface.blit(src, rect)

    def draw_line(self, a: tuple[int, int], b: tuple[int, int]):
        """Draws a diagonal line from point a to point b."""

        pygame.draw.line(
            self.surface, 0x00FF00, self.cell_to_pos(*a), self.cell_to_pos(*b), 5
        )

    def draw_grid(self):
        """
        Draws the entire tic-tac-toe board from
        scratch, erasing all changes made.
        """

        cellrect = pygame.rect.Rect(0, 0, self.cellwidth, self.cellheight)

        for y in range(3):
            for x in range(3):
                cellrect.size = self.cellsize
                cellrect.topleft = (x * cellrect.width, y * cellrect.height)
                pygame.draw.rect(self.surface, 0x000000, cellrect)
                cellrect.inflate_ip(-2, -2)
                pygame.draw.rect(self.surface, 0x777777, cellrect)
