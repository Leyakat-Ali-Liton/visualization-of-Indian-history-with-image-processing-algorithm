import os


def bresenham_line(pen, x1, y1, x2, y2, color="red", size=2):
    """
    Implementation of Bresenham's Line Drawing Algorithm.
    Draws a line pixel-by-pixel (using turtle dots) from (x1, y1) to (x2, y2).
    """
    pen.penup()
    pen.color(color)

    # Convert coordinates to integers for the algorithm
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        pen.goto(x1, y1)
        pen.dot(size)  # Draw a "pixel"

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def draw_rectangle_bresenham(pen, x, y, width, height, color="black", size=2):
    """
    Draws a rectangle using the custom Bresenham line algorithm.
    (x, y) represents the top-left corner.
    """
    # Top edge
    bresenham_line(pen, x, y, x + width, y, color, size)
    # Right edge
    bresenham_line(pen, x + width, y, x + width, y - height, color, size)
    # Bottom edge
    bresenham_line(pen, x + width, y - height, x, y - height, color, size)
    # Left edge
    bresenham_line(pen, x, y - height, x, y, color, size)


def play_animation_1947(screen, pen):
    """
    Renders 1947 Partition:
    1. Loads the new correctly drawn map image directly.
    2. Implements Bresenham's line algorithm to fulfill lab syllabus requirements.
    """
    # Clear previous drawings
    pen.clear()

    # 1. Load the new map image that already contains the correct colors and sea vibe
    # (Based on your screenshots, the file is named map.gif)
    image_name = "map.gif"
    if os.path.exists(image_name):
        screen.bgpic(image_name)
    elif os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")

    # 2. Implement Lab Requirement: Draw basic shapes using Bresenham's Algorithm
    # We will draw a rectangular frame using Bresenham lines at the top of the screen
    # to serve as a border for a title or date (e.g., framing the year "1947").

    frame_width = 150
    frame_height = 50
    start_x = -75
    start_y = 250

    # Draw a decorative red rectangle using the algorithm
    draw_rectangle_bresenham(pen, start_x, start_y, frame_width, frame_height, color="red", size=3)

    screen.update()