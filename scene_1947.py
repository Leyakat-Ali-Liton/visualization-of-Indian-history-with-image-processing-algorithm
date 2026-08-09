import os
import time
import random
import turtle


def safe_update(screen):
    try:
        screen.update()
    except:
        pass


def safe_goto(pen, x, y):
    try:
        pen.goto(x, y)
    except:
        pass


def draw_line(pen, x1, y1, x2, y2, color="red", size=2):
    # DDA line drawing algorithm
    try:
        dx = x2 - x1
        dy = y2 - y1
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            return
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        pen.penup()
        safe_goto(pen, x, y)
        pen.pendown()
        pen.color(color)
        pen.pensize(size)
        for _ in range(steps):
            x += x_inc
            y += y_inc
            safe_goto(pen, x, y)
        pen.pensize(1)
        pen.penup()
    except:
        pass


def draw_rectangle_dda(pen, x, y, width, height, color="black", size=2):
    # Basic shapes drawing using OpenGL/Turtle
    draw_line(pen, x, y, x + width, y, color, size)
    draw_line(pen, x + width, y, x + width, y - height, color, size)
    draw_line(pen, x + width, y - height, x, y - height, color, size)
    draw_line(pen, x, y - height, x, y, color, size)


def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty


def draw_crack(screen, pen, x1, y1, x2, y2, color="#111111", size=4):
    steps = 20
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps

    curr_x, curr_y = x1, y1
    for _ in range(steps):
        tx = dx + random.uniform(-10, 10)
        ty = dy + random.uniform(-10, 10)
        next_x, next_y = translate_2d(curr_x, curr_y, tx, ty)

        draw_line(pen, curr_x, curr_y, next_x, next_y, color, size)
        curr_x, curr_y = next_x, next_y

        safe_update(screen)
        time.sleep(0.03)

    draw_line(pen, curr_x, curr_y, x2, y2, color, size)


def cinematic_transition(screen):
    wipe = turtle.Turtle()
    wipe.hideturtle()
    wipe.speed(0)
    wipe.color("#111111")

    for x in range(-450, 451, 60):
        wipe.clear()
        wipe.penup()
        safe_goto(wipe, -450, -300)
        wipe.pendown()
        wipe.begin_fill()
        safe_goto(wipe, x, -300)
        safe_goto(wipe, x, 300)
        safe_goto(wipe, -450, 300)
        safe_goto(wipe, -450, -300)
        wipe.end_fill()
        safe_update(screen)
        time.sleep(0.01)

    return wipe


def reveal_transition(screen, wipe):
    for x in range(-450, 451, 60):
        wipe.clear()
        wipe.penup()
        safe_goto(wipe, x, -300)
        wipe.pendown()
        wipe.begin_fill()
        safe_goto(wipe, 450, -300)
        safe_goto(wipe, 450, 300)
        safe_goto(wipe, x, 300)
        safe_goto(wipe, x, -300)
        wipe.end_fill()
        safe_update(screen)
        time.sleep(0.01)

    wipe.clear()


def play_animation_1947(screen, pen):
    screen.tracer(0)
    pen.clear()

    meeting_img = "partison_meeting.gif"

    if os.path.exists(meeting_img):
        screen.bgpic(meeting_img)
    else:
        try:
            screen.bgpic("nopic")
        except:
            pass
        screen.bgcolor("#1a1a1a")

    text_pen = turtle.Turtle()
    text_pen.hideturtle()
    text_pen.speed(0)

    text_pen.penup()
    safe_goto(text_pen, 0, 60)
    text_pen.color("#00FFFF")
    text_pen.write("Lahore Resolution", align="center", font=("Arial", 28, "bold"))

    safe_goto(text_pen, 0, 15)
    text_pen.color("#FFFFFF")
    text_pen.write("লাহোর প্রস্তাব", align="center", font=("Arial", 24, "bold"))

    safe_update(screen)
    time.sleep(3.0)

    text_pen.clear()

    wipe_pen = cinematic_transition(screen)

    map_image = "map.gif"
    if os.path.exists(map_image):
        screen.bgpic(map_image)
    elif os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")

    reveal_transition(screen, wipe_pen)
    safe_update(screen)
    time.sleep(0.5)

    anim_pen = turtle.Turtle()
    anim_pen.hideturtle()
    anim_pen.speed(0)

    draw_crack(screen, anim_pen, -100, 190, -145, 60, color="#111111", size=6)
    draw_crack(screen, anim_pen, 215, 30, 195, -70, color="#111111", size=6)

    time.sleep(0.5)

    text_pen.penup()
    safe_goto(text_pen, -280, 100)
    text_pen.color("white")
    text_pen.write("West Pakistan", align="center", font=("Arial", 16, "bold"))

    safe_goto(text_pen, 0, -50)
    text_pen.color("#111111")
    text_pen.write("India", align="center", font=("Arial", 22, "bold"))

    safe_goto(text_pen, 230, -10)
    text_pen.color("white")
    text_pen.write("East Pakistan", align="center", font=("Arial", 14, "bold"))

    safe_update(screen)
    time.sleep(0.5)

    frame_width = 180
    frame_height = 65
    start_x = -90
    start_y = 275

    draw_rectangle_dda(pen, start_x, start_y, frame_width, frame_height, color="red", size=3)
    safe_update(screen)