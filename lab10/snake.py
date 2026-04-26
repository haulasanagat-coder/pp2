import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
BLOCK = 20
FPS = 5

# Color definitions
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)    # Snake body
RED = (255, 0, 0)      # 1-point food
YELLOW = (255, 255, 0) # 3-point food
BLUE = (0, 0, 255)     # 5-point food
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake with Timed Food")

# Game clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Custom event for food expiration (despawn)
FOOD_DESPAWN = pygame.USEREVENT + 1
FOOD_LIFETIME = 4000  # Food disappears after 3 seconds


class Snake:
    def __init__(self):
        # Initialize snake with starting body position
        self.body = [[100, 100]]
        self.dx = BLOCK  # X movement direction
        self.dy = 0      # Y movement direction
        self.grow = False  # Growth flag

    def move(self):
        # Calculate new head position
        head = self.body[-1][:]
        head[0] += self.dx
        head[1] += self.dy
        self.body.append(head)
        
        # Remove tail if not growing (normal movement)
        if not self.grow:
            self.body.pop(0)
        else:
            self.grow = False  # Reset growth after eating

    def draw(self):
        # Draw each segment of the snake
        for block in self.body:
            pygame.draw.rect(screen, GREEN, (*block, BLOCK, BLOCK))

    def change_direction(self, dx, dy):
        # Prevent snake from reversing into itself
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx = dx
            self.dy = dy

    def collide_self(self):
        # Check if head collides with body
        return self.body[-1] in self.body[:-1]


class Food:
    def __init__(self):
        # Spawn food with random position, value, and color
        self.reset()

    def random_position(self):
        # Generate position aligned with grid
        return [
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK),
        ]

    def reset(self):
        # Create new food with random weight and start timer
        self.position = self.random_position()
        
        # Assign random food value (weight)
        rand = random.randint(1, 10)
        if rand <= 6:
            self.value = 1    # Common: 1 point (red)
            self.color = RED
        elif rand <= 9:
            self.value = 3    # Rare: 3 points (yellow)
            self.color = YELLOW
        else:
            self.value = 5    # Epic: 5 points (blue)
            self.color = BLUE
        
        # Start despawn timer
        pygame.time.set_timer(FOOD_DESPAWN, FOOD_LIFETIME)

    def draw(self):
        # Draw food with its assigned color
        pygame.draw.rect(screen, self.color, (*self.position, BLOCK, BLOCK))


def draw_score(score):
    # Display current score on screen
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def main():
    snake = Snake()
    food = Food()
    speed = FPS
    score = 0

    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Control snake direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction(-BLOCK, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(BLOCK, 0)
                elif event.key == pygame.K_UP:
                    snake.change_direction(0, -BLOCK)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, BLOCK)

            # Despawn food when timer ends
            if event.type == FOOD_DESPAWN:
                food.reset()

        # Move snake
        snake.move()
        head = snake.body[-1]

        # Wall collision check (game over)
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT):
            break

        # Self collision check (game over)
        if snake.collide_self():
            break

        # Food collision (eat food)
        if head == food.position:
            snake.grow = True
            score += food.value       # Add food weight to score
            food.reset()              # Spawn new food
            speed += 0.3              # Increase game speed

        # Draw all elements
        snake.draw()
        food.draw()
        draw_score(score)

        # Update display and control speed
        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()