import pygame
from config import *
from game import run_game
from db import get_top_leaderboard
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")
clock = pygame.time.Clock()

# Font initialization
font_sm = pygame.font.SysFont(None, 30)
font_md = pygame.font.SysFont(None, 40)
font_lg = pygame.font.SysFont(None, 60)

# UI Helper Functions
def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def draw_button(text, x, y, w, h, color, hover):
    mx, my = pygame.mouse.get_pos()
    c = hover if x<mx<x+w and y<my<y+h else color
    pygame.draw.rect(screen, c, (x,y,w,h))
    draw_text(text, font_sm, BLACK, x+10, y+10)
    return x<mx<x+w and y<my<y+h

# Screens
def username_input():
    name = ""
    while True:
        screen.fill(BLACK)
        draw_text("Enter Username:", font_lg, WHITE, 200, 200)
        draw_text(name, font_md, GREEN, 200, 280)
        draw_text("Press ENTER to start", font_sm, WHITE, 200, 330)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10 and e.unicode.isalnum():
                    name += e.unicode
        pygame.display.update()

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("SNAKE", font_lg, GREEN, 300, 100)
        draw_text("Name:", font_md, WHITE, 330, 200)
        b1 = draw_button("PLAY", 300,250,200,50, GREEN, (0,200,0))
        b2 = draw_button("LEADERBOARD", 300,320,200,50, BLUE, (0,0,200))
        b3 = draw_button("SETTINGS", 300,390,200,50, (255,0,255), (200,0,200))
        b4 = draw_button("QUIT", 300,460,200,50, RED, (200,0,0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b1: return "play"
                if b2: return "leaderboard"
                if b3: return "settings"
                if b4:
                    pygame.quit()
                    exit()
        pygame.display.update()

def leaderboard_screen():
    while True:
        screen.fill(BLACK)
        draw_text("TOP 10", font_lg, WHITE, 350,50)
        data = get_top_leaderboard()
        if not data:
            draw_text("No records yet!", font_md, WHITE, 300, 200)
        else:
            y = 120
            draw_text(f"{'RANK':<6}{'NAME':<12}{'SCORE':<8}{'LEVEL'}", font_md, GREEN, 50, y)
            for i, (name, s, l, t) in enumerate(data,1):
                y+=40
                draw_text(f"{i:<6}{name:<12}{s:<8}{l}", font_sm, WHITE, 50, y)
        back = draw_button("BACK", 330,500,140,50, WHITE, GRAY)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit();exit()
            if e.type == pygame.MOUSEBUTTONDOWN and back:
                return
        pygame.display.update()

def settings_screen():
    global settings
    temp = settings.copy()
    colors = [(0,255,0),(255,0,255),(0,255,255),(255,255,0)]
    c_idx = colors.index(tuple(temp["snake_color"])) if tuple(temp["snake_color"]) in colors else 0
    while True:
        screen.fill(BLACK)
        draw_text("SETTINGS", font_lg, WHITE, 300,50)
        draw_text(f"Grid: {'ON' if temp['grid'] else 'OFF'}", font_md, WHITE, 200,150)
        draw_text(f"Sound: {'ON' if temp['sound'] else 'OFF'}", font_md, WHITE, 200,200)
        draw_text("Snake Color:", font_md, WHITE, 200,250)
        pygame.draw.rect(screen, colors[c_idx], (400,250,40,40))
        
        b_grid = draw_button("TOGGLE", 500,150,100,40, WHITE, GRAY)
        b_sound = draw_button("TOGGLE", 500,200,100,40, WHITE, GRAY)
        b_color = draw_button("CHANGE", 500,300,100,40, WHITE, GRAY)
        save = draw_button("SAVE & BACK", 300,400,200,50, GREEN, GRAY)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit();exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_grid:
                    temp["grid"] = not temp["grid"]
                if b_sound:
                    temp["sound"] = not temp["sound"]
                if b_color:
                    c_idx = (c_idx + 1) % 4
                if save:
                    temp["snake_color"] = list(colors[c_idx])
                    settings = temp
                    save_settings(settings)
                    return
        pygame.display.update()

# Main loop
def main():
    username = username_input()
    while True:
        choice = main_menu()
        if choice == "play":
            while True:
                res = run_game(username, screen, font_sm, font_md, font_lg)
                if res == "menu":
                    break
        elif choice == "leaderboard":
            leaderboard_screen()
        elif choice == "settings":
            settings_screen()

if __name__ == "__main__":
    main()