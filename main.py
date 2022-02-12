import sys, pygame

pygame.init()

size = width, height = 500, 500

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")


def draw_grid(surface):
    cellrect = pygame.rect.Rect(0, 0, width / 3, height / 3)

    for y in range(3):
        for x in range(3):
            cellrect.size = (width / 3, height / 3)
            cellrect.topleft = (x * cellrect.width, y * cellrect.height)
            pygame.draw.rect(surface, 0x000000, cellrect)
            cellrect.inflate_ip(-2, -2)
            pygame.draw.rect(surface, 0x777777, cellrect)


draw_grid(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
    pygame.time.wait(10)
