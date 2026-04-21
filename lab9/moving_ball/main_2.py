import pygame
from ball import Ball

pygame.init()

#Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Red Ball")
#color
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Create ball object
ball = Ball(WIDTH, HEIGHT)
#FPS control
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

#Event handling (keyboard + quit)
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

#Draw the ball
    pygame.draw.circle(screen, RED, (ball.x, ball.y), ball.radius)
#Update screen
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()