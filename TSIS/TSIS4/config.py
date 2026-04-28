import json
import os
import pygame

# Window and basic game settings
WIDTH, HEIGHT = 800, 600
BLOCK = 20
BASE_FPS = 8

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (139, 0, 0)    # Poison food
PURPLE = (128, 0, 128)   # Speed boost power-up
CYAN = (0, 255, 255)     # Slow down power-up
GRAY = (128, 128, 128)   # Shield power-up
BROWN = (139, 69, 19)    # Obstacle

# Custom Pygame events
FOOD_DESPAWN = pygame.USEREVENT + 1
POWERUP_DESPAWN = pygame.USEREVENT + 2
POWERUP_END = pygame.USEREVENT + 3

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "snake_game",
    "user": "postgres",
    "password": "1234"  # Change to your own password
}

# User settings file path
SETTINGS_FILE = "settings.json"

# Load and save game settings
def load_settings():
    default = {
        "snake_color": [0, 255, 0],
        "grid": False,
        "sound": False
    }
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return default

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

# Global settings variable (Parentheses are required here!)
settings = load_settings()