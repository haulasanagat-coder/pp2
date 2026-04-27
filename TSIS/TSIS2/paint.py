# paint.py
import pygame
import tools

# Initialize
pygame.init()

# Window settings
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
canvas = screen.copy()

# Drawing state
drawing = False
current_tool = tools.BRUSH
color = (0, 0, 0)
brush_size = tools.MEDIUM
start_pos = (0, 0)
last_mouse_pos = (0, 0)

# Text tool
text_active = False
text_input = ""
text_pos = (0, 0)
font = tools.get_text_font()
hint_font = pygame.font.SysFont(None, 20)

# English control hints
def draw_hints():
    hints = [
        "[Tools] 1-Brush 2-Rect 3-Circle 4-Eraser 5-Square",
        "6-RightTri 7-EqTri 8-Rhombus 9-Line 0-Fill T-Text",
        "[Size] s-Small m-Medium l-Large | [Color] R-Red G-Green B-Blue",
        "[Save] Ctrl+S | Text: Enter=Confirm / ESC=Cancel"
    ]
    y_offset = 10
    for line in hints:
        text_surf = hint_font.render(line, True, (50, 50, 50))
        screen.blit(text_surf, (10, y_offset))
        y_offset += 22

running = True

while running:
    screen.blit(canvas, (0, 0))
    draw_hints()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            # Tool selection
            if event.key == pygame.K_1:
                current_tool = tools.BRUSH
                text_active = False
            elif event.key == pygame.K_2:
                current_tool = tools.RECT
                text_active = False
            elif event.key == pygame.K_3:
                current_tool = tools.CIRCLE
                text_active = False
            elif event.key == pygame.K_4:
                current_tool = tools.ERASER
                text_active = False
            elif event.key == pygame.K_5:
                current_tool = tools.SQUARE
                text_active = False
            elif event.key == pygame.K_6:
                current_tool = tools.RIGHT_TRI
                text_active = False
            elif event.key == pygame.K_7:
                current_tool = tools.EQ_TRI
                text_active = False
            elif event.key == pygame.K_8:
                current_tool = tools.RHOMBUS
                text_active = False
            elif event.key == pygame.K_9:
                current_tool = tools.LINE
                text_active = False
            elif event.key == pygame.K_0:
                current_tool = tools.FILL
                text_active = False
            elif event.key == pygame.K_t:
                current_tool = tools.TEXT
                text_active = False

            # Color shortcuts
            if event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)

            # Brush size
            if not text_active:
                if event.key == pygame.K_s:
                    brush_size = tools.SMALL
                elif event.key == pygame.K_m:
                    brush_size = tools.MEDIUM
                elif event.key == pygame.K_l:
                    brush_size = tools.LARGE

            # Save canvas
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                tools.save_canvas(canvas)

            # Text input handle
            if text_active and current_tool == tools.TEXT:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_input, True, color)
                    canvas.blit(txt_surf, text_pos)
                    text_active = False
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        # Mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_mouse_pos = event.pos

            if current_tool == tools.FILL:
                tools.flood_fill(canvas, *event.pos, color)

            if current_tool == tools.TEXT:
                text_active = True
                text_pos = event.pos
                text_input = ""

        # Mouse up: final shape draw
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            s = start_pos
            e = event.pos

            if current_tool == tools.RECT:
                tools.draw_rect_outline(canvas, color, brush_size, s, e)
            elif current_tool == tools.CIRCLE:
                tools.draw_circle_outline(canvas, color, brush_size, s, e)
            elif current_tool == tools.SQUARE:
                tools.draw_square_outline(canvas, color, brush_size, s, e)
            elif current_tool == tools.RIGHT_TRI:
                tools.draw_right_triangle(canvas, color, brush_size, s, e)
            elif current_tool == tools.EQ_TRI:
                tools.draw_equilateral_tri(canvas, color, brush_size, s, e)
            elif current_tool == tools.RHOMBUS:
                tools.draw_rhombus(canvas, color, brush_size, s, e)
            elif current_tool == tools.LINE:
                tools.draw_straight_line(canvas, color, brush_size, s, e)

    # Mouse drag drawing & preview
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and drawing:
        if current_tool == tools.BRUSH:
            tools.draw_brush(canvas, color, brush_size, last_mouse_pos, (mx, my))
            last_mouse_pos = (mx, my)
        elif current_tool == tools.ERASER:
            tools.draw_eraser(canvas, brush_size, last_mouse_pos, (mx, my))
            last_mouse_pos = (mx, my)
        else:
            preview = canvas.copy()
            if current_tool == tools.LINE:
                tools.draw_straight_line(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.RECT:
                tools.draw_rect_outline(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.CIRCLE:
                tools.draw_circle_outline(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.SQUARE:
                tools.draw_square_outline(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.RIGHT_TRI:
                tools.draw_right_triangle(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.EQ_TRI:
                tools.draw_equilateral_tri(preview, color, brush_size, start_pos, (mx, my))
            elif current_tool == tools.RHOMBUS:
                tools.draw_rhombus(preview, color, brush_size, start_pos, (mx, my))
            screen.blit(preview, (0,0))

    # Live text preview
    if text_active:
        txt_surf = font.render(text_input, True, color)
        screen.blit(txt_surf, text_pos)

    pygame.display.update()

pygame.quit()