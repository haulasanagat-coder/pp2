import pygame
import math

# Initialize 
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))  # White background

# Drawing state variables
drawing = False  # Flag to check if mouse is pressed
tool = "brush"   # Current selected drawing tool
color = (0, 0, 0)
start_pos = (0, 0)

# Main loop
running = True
while running:
    # Handle all events
    for event in pygame.event.get():
        # Quit the program when window is closed
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls for selecting tools and colors
        if event.type == pygame.KEYDOWN:
            # Shape tools
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rect"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"
            elif event.key == pygame.K_5:
                tool = "square"          
            elif event.key == pygame.K_6:
                tool = "right_triangle"   
            elif event.key == pygame.K_7:
                tool = "equilateral_tri"  
            elif event.key == pygame.K_8:
                tool = "rhombus"         

            # Color selection
            if event.key == pygame.K_r:
                color = (255, 0, 0)    # Red
            elif event.key == pygame.K_g:
                color = (0, 255, 0)    # Green
            elif event.key == pygame.K_b:
                color = (0, 0, 255)    # Blue

        # Start drawing when mouse is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  # Save the starting point

        # Finish drawing when mouse is released
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            x1, y1 = start_pos
            x2, y2 = event.pos
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            # Draw rectangle
            if tool == "rect":
                rect = (min(x1, x2), min(y1, y2), width, height)
                pygame.draw.rect(screen, color, rect, 2)

            # Draw circle
            elif tool == "circle":
                radius = int(math.dist(start_pos, event.pos))
                pygame.draw.circle(screen, color, start_pos, radius, 2)

            # Draw perfect square
            elif tool == "square":
                side = max(width, height)
                # Adjust position to keep square anchored at start point
                if x2 < x1:
                    x1 -= side
                if y2 < y1:
                    y1 -= side
                pygame.draw.rect(screen, color, (x1, y1, side, side), 2)

            #  Draw right triangle
            elif tool == "right_triangle":
                p1 = (x1, y1)
                p2 = (x2, y1)
                p3 = (x1, y2)
                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            #  Draw equilateral triangle
            elif tool == "equilateral_tri":
                side = int(math.dist(start_pos, event.pos))
                # Calculate 3 points of equilateral triangle
                p1 = (x1, y1)
                p2 = (x1 + side, y1)
                p3 = (x1 + side//2, int(y1 - math.sqrt(3)*side//2))
                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            # raw rhombus (diamond shape)
            elif tool == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                points = [
                    (x1, cy),   # Left
                    (cx, y1),   # Top
                    (x2, cy),   # Right
                    (cx, y2)    # Bottom
                ]
                pygame.draw.polygon(screen, color, points, 2)

    # Real-time drawing while mouse is moving
    if event.type == pygame.MOUSEMOTION and drawing:
        # Freehand brush
        if tool == "brush":
            pygame.draw.circle(screen, color, event.pos, 5)
        # Eraser (white circle)
        elif tool == "eraser":
            pygame.draw.circle(screen, (255, 255, 255), event.pos, 10)

    # Update the display
    pygame.display.update()

# Quit Pygame properly
pygame.quit()