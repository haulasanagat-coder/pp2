import pygame
import random
from config import *
from db import get_personal_best, save_game_session, get_or_create_player

class Snake:
    def __init__(self, color):
        self.body = [[WIDTH//2, HEIGHT//2]]
        self.dx = BLOCK
        self.dy = 0
        self.grow = False
        self.color = color
        self.shield = False

    def move(self):
        head = self.body[-1].copy()
        head[0] += self.dx
        head[1] += self.dy
        self.body.append(head)
        if not self.grow:
            self.body.pop(0)
        self.grow = False

    def draw(self, screen):
        for seg in self.body:
            pygame.draw.rect(screen, self.color, (*seg, BLOCK, BLOCK))

    def change_dir(self, dx, dy):
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx = dx
            self.dy = dy

    def collide_self(self):
        return self.body[-1] in self.body[:-1]

    def shorten(self, n):
        if len(self.body) > n:
            self.body = self.body[:-n]
        else:
            self.body = self.body[:1]

class Food:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.reset()

    def random_pos(self):
        while True:
            pos = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]
            if pos not in self.obstacles:
                return pos

    def reset(self):
        self.pos = self.random_pos()
        rand = random.randint(1,12)
        if rand <= 6:
            self.val = 1
            self.color = RED
            self.type = "normal"
        elif rand <=9:
            self.val =3
            self.color=YELLOW
            self.type="normal"
        elif rand <=11:
            self.val=5
            self.color=BLUE
            self.type="normal"
        else:
            self.val=-2
            self.color=DARK_RED
            self.type="poison"
        pygame.time.set_timer(FOOD_DESPAWN, 4000)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, BLOCK, BLOCK))

class PowerUp:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.active = False
        self.type = None
        self.pos = None
        self.color = None

    def spawn(self):
        self.pos = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]
        while self.pos in self.obstacles:
            self.pos = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]
        t = random.choice(["speed", "slow", "shield"])
        self.type = t
        self.color = PURPLE if t=="speed" else CYAN if t=="slow" else GRAY
        self.active = True
        pygame.time.set_timer(POWERUP_DESPAWN, 8000)

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (*self.pos, BLOCK, BLOCK))

def draw_grid(screen):
    if settings["grid"]:
        for x in range(0, WIDTH, BLOCK):
            pygame.draw.line(screen, (50,50,50), (x,0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK):
            pygame.draw.line(screen, (50,50,50), (0,y), (WIDTH, y))

def game_over_screen(username, score, level, best, screen, font_sm, font_md, font_lg):
    """Game over screen interface"""
    save_game_session(get_or_create_player(username), score, level)
    while True:
        screen.fill(BLACK)
        screen.blit(font_lg.render("GAME OVER", True, RED), (280,100))
        screen.blit(font_md.render(f"Score: {score}", True, WHITE), (320,200))
        screen.blit(font_md.render(f"Level: {level}", True, WHITE), (320,250))
        screen.blit(font_md.render(f"Personal Best: {best}", True, YELLOW), (320,300))
        
        # Buttons
        mx, my = pygame.mouse.get_pos()
        b_retry = (230,400,140,50)
        b_menu = (430,400,140,50)
        
        # Retry button
        c = GRAY if (b_retry[0] < mx < b_retry[0]+b_retry[2] and b_retry[1] < my < b_retry[1]+b_retry[3]) else WHITE
        pygame.draw.rect(screen, c, b_retry)
        screen.blit(font_sm.render("RETRY", True, BLACK), (b_retry[0]+10, b_retry[1]+10))
        
        # Menu button
        c = GRAY if (b_menu[0] < mx < b_menu[0]+b_menu[2] and b_menu[1] < my < b_menu[1]+b_menu[3]) else WHITE
        pygame.draw.rect(screen, c, b_menu)
        screen.blit(font_sm.render("MENU", True, BLACK), (b_menu[0]+10, b_menu[1]+10))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if (b_retry[0] < mx < b_retry[0]+b_retry[2] and b_retry[1] < my < b_retry[1]+b_retry[3]):
                    return "retry"
                if (b_menu[0] < mx < b_menu[0]+b_menu[2] and b_menu[1] < my < b_menu[1]+b_menu[3]):
                    return "menu"
        pygame.display.update()

def run_game(username, screen, font_sm, font_md, font_lg):
    """Run a single game round, return action result: retry/menu"""
    best = get_personal_best(username)
    snake = Snake(settings["snake_color"])
    obstacles = []
    level = 1
    score = 0
    speed = BASE_FPS
    powerup = PowerUp(obstacles)
    food = Food(obstacles)
    powerup_active = None
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        current_time = pygame.time.get_ticks()

        # Spawn obstacles starting from level 3
        if level >=3 and not obstacles:
            for _ in range(level*2):
                pos = [random.randrange(0,WIDTH,BLOCK), random.randrange(0,HEIGHT,BLOCK)]
                if pos != snake.body[-1] and pos not in snake.body:
                    obstacles.append(pos)
            food.obstacles = obstacles
            powerup.obstacles = obstacles

        # Randomly spawn power-ups
        if not powerup.active and random.randint(0,300) == 0:
            powerup.spawn()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == FOOD_DESPAWN:
                food.reset()
            if e.type == POWERUP_DESPAWN:
                powerup.active = False
            if e.type == POWERUP_END:
                powerup_active = None
                speed = BASE_FPS + (level-1)*0.5
                snake.shield = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT: snake.change_dir(-BLOCK,0)
                elif e.key == pygame.K_RIGHT: snake.change_dir(BLOCK,0)
                elif e.key == pygame.K_UP: snake.change_dir(0,-BLOCK)
                elif e.key == pygame.K_DOWN: snake.change_dir(0,BLOCK)

        snake.move()
        head = snake.body[-1]

        # Collision detection
        game_over_flag = False
        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT:
            if not snake.shield: game_over_flag = True
            else: snake.shield = False
        if head in snake.body[:-1]:
            if not snake.shield: game_over_flag = True
            else: snake.shield = False
        if head in obstacles:
            if not snake.shield: game_over_flag = True
            else: snake.shield = False
        if game_over_flag:
            break

        # Eat food
        if head == food.pos:
            if food.type == "poison":
                snake.shorten(2)
                if len(snake.body) <=1:
                    break
            else:
                snake.grow = True
                score += food.val
                if score % 10 == 0:
                    level +=1
                    speed +=0.5
            food.reset()

        # Collect power-up
        if powerup.active and head == powerup.pos:
            powerup.active = False
            powerup_active = powerup.type
            pygame.time.set_timer(POWERUP_END, 5000)
            if powerup.type == "speed": speed +=3
            elif powerup.type == "slow": speed = max(3, speed-3)
            elif powerup.type == "shield": snake.shield = True

        # Draw game elements
        for obs in obstacles:
            pygame.draw.rect(screen, BROWN, (*obs, BLOCK, BLOCK))
        snake.draw(screen)
        food.draw(screen)
        powerup.draw(screen)

        # UI information
        screen.blit(font_sm.render(f"Score: {score}", True, WHITE), (10,10))
        screen.blit(font_sm.render(f"Level: {level}", True, WHITE), (150,10))
        screen.blit(font_sm.render(f"Best: {best}", True, YELLOW), (280,10))
        screen.blit(font_sm.render(f"User: {username}", True, GREEN), (400,10))
        if snake.shield:
            screen.blit(font_sm.render("SHIELD ACTIVE", True, CYAN), (600,10))

        pygame.display.update()
        clock.tick(speed)

    # Game over, save record and show game over screen
    return game_over_screen(username, score, level, best, screen, font_sm, font_md, font_lg)