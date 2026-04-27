# tools.py
import pygame
import math
from datetime import datetime

# tools name
BRUSH = "brush"
RECT = "rect"
CIRCLE = "circle"
ERASER = "eraser"
SQUARE = "square"
RIGHT_TRI = "right_triangle"
EQ_TRI = "equilateral_tri"
RHOMBUS = "rhombus"
LINE = "line"
FILL = "fill"
TEXT = "text"

# pencil size
SMALL = 2
MEDIUM = 5
LARGE = 10

# dawing
def draw_brush(surface, color, size, p1, p2):
    pygame.draw.line(surface, color, p1, p2, size)

def draw_eraser(surface, size, p1, p2):
    pygame.draw.line(surface, (255,255,255), p1, p2, size * 2)

def draw_straight_line(surface, color, size, start, end):
    pygame.draw.line(surface, color, start, end, size)

def draw_rect_outline(surface, color, size, start, end):
    x1, y1 = start
    x2, y2 = end
    rect = (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
    pygame.draw.rect(surface, color, rect, size)

def draw_circle_outline(surface, color, size, start, end):
    r = int(math.dist(start, end))
    pygame.draw.circle(surface, color, start, r, size)

def draw_square_outline(surface, color, size, start, end):
    x1, y1 = start
    x2, y2 = end
    side = max(abs(x2-x1), abs(y2-y1))
    sx = x1 if x2 >= x1 else x1 - side
    sy = y1 if y2 >= y1 else y1 - side
    pygame.draw.rect(surface, color, (sx, sy, side, side), size)

def draw_right_triangle(surface, color, size, start, end):
    x1, y1 = start
    x2, y2 = end
    pts = [(x1,y1), (x2,y1), (x1,y2)]
    pygame.draw.polygon(surface, color, pts, size)

def draw_equilateral_tri(surface, color, size, start, end):
    x1, y1 = start
    side = int(math.dist(start, end))
    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side//2, int(y1 - math.sqrt(3) * side / 2))
    pygame.draw.polygon(surface, color, [p1,p2,p3], size)

def draw_rhombus(surface, color, size, start, end):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    pts = [(x1, cy), (cx, y1), (x2, cy), (cx, y2)]
    pygame.draw.polygon(surface, color, pts, size)

# filling
def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    w, h = surface.get_size()
    queue = [(x, y)]
    surface.set_at((x, y), new_color)
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    while queue:
        cx, cy = queue.pop(0)
        for dx, dy in dirs:
            nx = cx + dx
            ny = cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny)) == target_color:
                    surface.set_at((nx, ny), new_color)
                    queue.append((nx, ny))

# save
def save_canvas(surface):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"paint_{stamp}.png"
    pygame.image.save(surface, name)
    print(f"Saved: {name}")

# text font
def get_text_font():
    return pygame.font.SysFont(None, 24)