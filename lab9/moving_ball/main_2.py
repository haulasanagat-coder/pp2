import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Red Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

ball = Ball(WIDTH, HEIGHT)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()

    pygame.draw.circle(screen, RED, (ball.x, ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()