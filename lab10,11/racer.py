import pygame
import random

# Initialize 
pygame.init()

WIDTH = 500
HEIGHT = 600

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# frame rate
clock = pygame.time.Clock()

# Game Initial Settings 
# Player car rectangle: x, y, width, height
car = pygame.Rect(180, 500, 40, 60)

# List to store all coin objects
coins = []

# Custom event for coin spawn timer
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer, 1500)  # Spawn coin every 1500ms

# Game score and speed increase settings
score = 0
SPEED_UP_THRESHOLD = 5  # Increase speed every N coins collected
coin_speed = 5          # Initial coin falling speed

# Font for displaying text
font = pygame.font.SysFont("Arial", 24)

# Main game loop flag
running = True

#  Main Game Loop 
while running:
    screen.fill((50, 50, 50))

    # Event Handling 
    for event in pygame.event.get():
        # Quit game if window is closed
        if event.type == pygame.QUIT:
            running = False

        # Spawn random coins with different weights/values
        if event.type == coin_timer:
            # Random X position within screen bounds
            x = random.randint(0, WIDTH - 20)
            
            # Random weighted coin values
            rand = random.randint(1, 10)
            if rand <= 7:
                coin_value = 1   # Common coin
            elif rand <= 9:
                coin_value = 3   # Rare coin
            else:
                coin_value = 5   # Epic coin
            
            # Store coin rectangle and its value in list
            coins.append([pygame.Rect(x, -20, 20, 20), coin_value])

    # Player Car Control 
    keys = pygame.key.get_pressed()
    # Move left with screen boundary limit
    if keys[pygame.K_LEFT] and car.left > 0:
        car.x -= 7
    # Move right with screen boundary limit
    if keys[pygame.K_RIGHT] and car.right < WIDTH:
        car.x += 7

    # Draw player car (green)
    pygame.draw.rect(screen, (0, 255, 0), car)

    # Coin Movement & Collision 
    # Iterate over copy of list to avoid removal errors
    for coin_data in coins[:]:
        coin_rect, value = coin_data
        
        # Make coin fall down
        coin_rect.y += coin_speed

        # Different color for different coin weights
        if value == 1:
            coin_color = (255, 255, 0)    # 1 point
        elif value == 3:
            coin_color = (0, 255, 255)    # 3 points
        else:
            coin_color = (255, 0, 255)    # 5 points
        
        pygame.draw.rect(screen, coin_color, coin_rect)

        # Check collision between car and coin
        if car.colliderect(coin_rect):
            coins.remove(coin_data)
            score += value

        # Remove coin when it goes out of screen bottom
        if coin_rect.y > HEIGHT:
            coins.remove(coin_data)

    # Increase Speed by Score
    # Increase falling speed every N collected coins
    if score != 0 and score % SPEED_UP_THRESHOLD == 0:
        coin_speed = 5 + (score // SPEED_UP_THRESHOLD)

    # Draw UI Text 
    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    speed_text = font.render(f"Speed: {coin_speed}", True, (255, 255, 255))
    
    screen.blit(score_text, (WIDTH - 120, 10))
    screen.blit(speed_text, (20, 10))

    # Update game display
    pygame.display.update()
    clock.tick(60)

# Close pygame
pygame.quit()