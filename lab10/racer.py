import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# машина
car = pygame.Rect(180, 500, 40, 60)

# монеты
coins = []
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer, 1500)

score = 0

font = pygame.font.SysFont("Arial", 24)

running = True
while running:
    screen.fill((50, 50, 50))

    # события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # создаем монету
        if event.type == coin_timer:
            x = random.randint(0, WIDTH - 20)
            coins.append(pygame.Rect(x, -20, 20, 20))

    # управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.x -= 5
    if keys[pygame.K_RIGHT]:
        car.x += 5

    # рисуем машину
    pygame.draw.rect(screen, (0, 255, 0), car)

    # движение монет
    for coin in coins[:]:
        coin.y += 5
        pygame.draw.rect(screen, (255, 255, 0), coin)

        # проверка столкновения
        if car.colliderect(coin):
            coins.remove(coin)
            score += 1

        # удаляем если ушла вниз
        elif coin.y > HEIGHT:
            coins.remove(coin)

    # вывод счета
    text = font.render(f"Coins: {score}", True, (255,255,255))
    screen.blit(text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(60)