import sys, pygame

pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bouncing ball")

ballrect = pygame.rect.Rect(0, 0, screen.get_height() / 10, screen.get_height() / 10)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    pygame.draw.circle(screen, (0xFF, 0, 0), ballrect.center, ballrect.height)
    pygame.display.flip()
    pygame.time.wait(10)
