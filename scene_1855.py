import turtle
import time
import os

def draw_rectangle(t, x, y, width, height, color):
    # Basic shapes drawing using OpenGL/Turtle
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()

def draw_circle(t, xc, yc, r, color):
    # Mid-Point circle drawing algorithm
    x = 0
    y = r
    p = 1 - r
    t.color(color)
    t.pensize(1)
    while x <= y:
        t.penup(); t.goto(xc - x, yc + y); t.pendown(); t.goto(xc + x, yc + y)
        t.penup(); t.goto(xc - x, yc - y); t.pendown(); t.goto(xc + x, yc - y)
        t.penup(); t.goto(xc - y, yc + x); t.pendown(); t.goto(xc + y, yc + x)
        t.penup(); t.goto(xc - y, yc - x); t.pendown(); t.goto(xc + y, yc - x)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

def draw_polygon(t, points, color):
    # Basic shapes drawing using OpenGL/Turtle
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    t.end_fill()

def draw_line(t, x1, y1, x2, y2, color, size=2):
    # DDA line drawing algorithm
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.pensize(size)
    for _ in range(steps):
        x += x_inc
        y += y_inc
        t.goto(x, y)
    t.pensize(1)
    t.color("black")

def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty

def draw_labels(t):
    draw_rectangle(t, -340, 110, 240, 35, "#111111")
    t.penup()
    t.goto(-219, 117)
    t.pendown()
    t.color("black")
    t.write("Leaders & Rebel Forces", align="center", font=("Georgia", 13, "bold"))
    t.penup()
    t.goto(-220, 119)
    t.pendown()
    t.color("#00FFCC")
    t.write("Leaders & Rebel Forces", align="center", font=("Georgia", 13, "bold"))

    draw_rectangle(t, 100, 110, 240, 35, "#111111")
    t.penup()
    t.goto(219, 117)
    t.pendown()
    t.color("black")
    t.write("British Soldiers", align="center", font=("Georgia", 13, "bold"))
    t.penup()
    t.goto(220, 119)
    t.pendown()
    t.color("#FF5252")
    t.write("British Soldiers", align="center", font=("Georgia", 13, "bold"))
    t.color("black")

def draw_rebel(t, x, y, is_dead, r_type):
    if not is_dead:
        if r_type == "santhal":
            draw_rectangle(t, x, y, 15, 35, "#8B4513")
            draw_circle(t, x + 7, y + 45, 10, "#8B4513")
            draw_rectangle(t, x - 2, y + 5, 20, 10, "white")
            draw_line(t, x + 15, y + 35, x + 25, y + 20, "brown", 2)
            draw_line(t, x + 25, y + 20, x + 15, y + 5, "brown", 2)
            draw_line(t, x + 15, y + 35, x + 15, y + 5, "white", 1)
        else:
            draw_rectangle(t, x, y, 15, 35, "#B22222")
            draw_circle(t, x + 7, y + 45, 10, "#A0522D")
            draw_polygon(t, [(x - 5, y + 55), (x + 20, y + 55), (x + 7, y + 65)], "white")
            draw_line(t, x + 15, y + 25, x + 30, y + 35, "silver", 3)
    else:
        color = "#8B4513" if r_type == "santhal" else "#B22222"
        draw_rectangle(t, x - 15, y - 10, 35, 15, color)
        draw_circle(t, x - 20, y - 5, 10, "#8B4513" if r_type == "santhal" else "#A0522D")
        draw_circle(t, x - 10, y - 5, 8, "red")

def draw_british_soldier(t, x, y, is_dead):
    if not is_dead:
        draw_rectangle(t, x, y, 15, 35, "red")
        draw_circle(t, x + 7, y + 45, 10, "#FFDAB9")
        draw_polygon(t, [(x - 5, y + 55), (x + 20, y + 55), (x + 7, y + 65)], "black")
        draw_line(t, x, y + 25, x - 30, y + 25, "#4A2311", 3)
    else:
        draw_rectangle(t, x - 10, y - 10, 35, 15, "red")
        draw_circle(t, x + 30, y - 5, 10, "#FFDAB9")
        draw_circle(t, x + 15, y - 5, 8, "darkred")

def render_all_armies(t, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead):
    t.clear()
    for i in range(10):
        draw_rebel(t, rebel_coords[i][0], rebel_coords[i][1], rebel_dead[i], rebel_types[i])
    for i in range(10):
        draw_british_soldier(t, british_coords[i][0], british_coords[i][1], british_dead[i])

def animate_volley(screen, pen, active_rebels, active_british, duration):
    steps = 25
    for i in range(steps):
        pen.clear()

        tx = ((350 - (-240)) / steps) * i
        sk_arrow_x, _ = translate_2d(-240, -50, tx, 0)
        draw_line(pen, sk_arrow_x, -50, sk_arrow_x + 20, -50, "silver", 3)
        draw_line(pen, sk_arrow_x, -100, sk_arrow_x + 20, -100, "silver", 3)

        for rx, ry, rtype in active_rebels:
            tx_r = ((350 - rx) / steps) * i
            cx, cy = translate_2d(rx + 20, ry + 25, tx_r, 0)
            if rtype == "santhal":
                draw_line(pen, cx, cy, cx + 15, cy, "silver", 2)
            else:
                draw_line(pen, cx, cy, cx + 10, cy, "orange", 3)

        for bx, by in active_british:
            tx_b = -((bx - (-350)) / steps) * i
            cx, cy = translate_2d(bx - 20, by + 25, tx_b, 0)
            draw_line(pen, cx, cy, cx - 15, cy, "yellow", 3)

        screen.update()
        time.sleep(duration / steps)
    pen.clear()

def play_animation(screen, anim_pen):
    if os.path.exists("rebellion_bg.gif"):
        screen.bgpic("rebellion_bg.gif")
    else:
        screen.bgpic("nopic")
        screen.bgcolor("#3d1c04")

    anim_pen.clear()

    if os.path.exists("sidhu_kanhu.gif"):
        screen.addshape("sidhu_kanhu.gif")
        sk_turtle = turtle.Turtle()
        sk_turtle.hideturtle()
        sk_turtle.speed(0)
        sk_turtle.penup()
        sk_turtle.goto(-330, -75)
        sk_turtle.shape("sidhu_kanhu.gif")
        sk_turtle.showturtle()

    rebel_coords = [(-250, -130), (-200, -130), (-150, -130), (-100, -130), (-50, -130),
                    (-230, -60), (-180, -60), (-130, -60), (-80, -60), (-30, -60)]
    rebel_types = ["santhal", "sepoy", "santhal", "sepoy", "santhal",
                   "sepoy", "santhal", "sepoy", "santhal", "sepoy"]

    british_coords = [(120, -130), (180, -130), (240, -130), (300, -130), (360, -130),
                      (150, -60), (210, -60), (270, -60), (330, -60), (390, -60)]

    rebel_dead = [False] * 10
    british_dead = [False] * 10

    draw_labels(anim_pen)

    army_pen = turtle.Turtle()
    army_pen.hideturtle()
    army_pen.speed(0)
    render_all_armies(army_pen, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead)
    screen.update()
    time.sleep(1)

    projectile_pen = turtle.Turtle()
    projectile_pen.hideturtle()
    projectile_pen.speed(0)

    volleys = [
        ([0], []),
        ([5], [0, 1]),
        ([], [2, 3, 5]),
        ([], [4, 6, 7]),
        ([], [8, 9])
    ]

    for b_deaths, r_deaths in volleys:
        active_rebels = [(rebel_coords[i][0], rebel_coords[i][1], rebel_types[i]) for i in range(10) if not rebel_dead[i]]
        active_british = [(british_coords[i][0], british_coords[i][1]) for i in range(10) if not british_dead[i]]

        animate_volley(screen, projectile_pen, active_rebels, active_british, duration=2.0)

        for b_idx in b_deaths: british_dead[b_idx] = True
        for r_idx in r_deaths: rebel_dead[r_idx] = True

        render_all_armies(army_pen, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead)
        screen.update()
        time.sleep(0.3)

    time.sleep(1)

    anim_pen.penup()
    anim_pen.goto(2, -2)
    anim_pen.pendown()
    anim_pen.color("black")
    anim_pen.write("Rebellion Crushed - British Won", align="center", font=("Georgia", 26, "bold"))

    anim_pen.penup()
    anim_pen.goto(0, 0)
    anim_pen.pendown()
    anim_pen.color("#FFD700")
    anim_pen.write("Rebellion Crushed - British Won", align="center", font=("Georgia", 26, "bold"))
    screen.update()