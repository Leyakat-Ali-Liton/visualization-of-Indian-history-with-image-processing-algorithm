import turtle
import time
import os
import math


def draw_rectangle(t, x, y, width, height, color):
    # Basic shapes drawing using OpenGL/Turtle
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.goto(x + width, y)
    t.goto(x + width, y + height)
    t.goto(x, y + height)
    t.goto(x, y)
    t.end_fill()


def draw_circle(t, xc, yc, r, color):
    # Mid-Point circle drawing algorithm
    x = 0
    y = r
    p = 1 - r
    t.color(color)
    t.pensize(1)
    while x <= y:
        t.penup();
        t.goto(xc - x, yc + y);
        t.pendown();
        t.goto(xc + x, yc + y)
        t.penup();
        t.goto(xc - x, yc - y);
        t.pendown();
        t.goto(xc + x, yc - y)
        t.penup();
        t.goto(xc - y, yc + x);
        t.pendown();
        t.goto(xc + y, yc + x)
        t.penup();
        t.goto(xc - y, yc - x);
        t.pendown();
        t.goto(xc + y, yc - x)
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
    font_style = ("Georgia", 18, "bold")

    t.penup()
    t.goto(-218, 148)
    t.pendown()
    t.color("black")
    t.write("Nawab Siraj-ud-Daulah's Forces", align="center", font=font_style)

    t.penup()
    t.goto(-220, 150)
    t.pendown()
    t.color("#FFD700")
    t.write("Nawab Siraj-ud-Daulah's Forces", align="center", font=font_style)

    t.penup()
    t.goto(222, 148)
    t.pendown()
    t.color("black")
    t.write("British East India Company", align="center", font=font_style)

    t.penup()
    t.goto(220, 150)
    t.pendown()
    t.color("#FFFFFF")
    t.write("British East India Company", align="center", font=font_style)
    t.color("black")


def draw_bengali_forces(t):
    draw_rectangle(t, -350, -90, 90, 60, "#696969")
    draw_circle(t, -260, -60, 35, "#696969")
    draw_polygon(t, [(-225, -60), (-210, -60), (-220, -120), (-235, -120), (-240, -80)], "#696969")
    draw_polygon(t, [(-230, -70), (-190, -85), (-225, -90)], "white")
    draw_circle(t, -280, -50, 25, "#555555")
    draw_rectangle(t, -340, -130, 20, 40, "#696969")
    draw_rectangle(t, -280, -130, 20, 40, "#696969")

    t.penup()
    t.goto(-170, -80)
    t.pendown()
    t.fillcolor("#4A2311")
    t.begin_fill()
    t.goto(-100, -60)
    t.goto(-100, -40)
    t.goto(-170, -60)
    t.end_fill()
    draw_circle(t, -150, -80, 20, "#5C3A21")


def draw_british_forces(t):
    t.penup()
    t.goto(250, -90)
    t.pendown()
    t.fillcolor("#333333")
    t.begin_fill()
    t.goto(160, -70)
    t.goto(160, -50)
    t.goto(250, -70)
    t.end_fill()
    draw_circle(t, 230, -90, 25, "#5C3A21")
    draw_circle(t, 230, -90, 10, "black")

    draw_rectangle(t, 270, -90, 22, 50, "red")
    draw_line(t, 270, -40, 292, -90, "white", 2)
    draw_line(t, 292, -40, 270, -90, "white", 2)
    draw_circle(t, 281, -30, 12, "#FFDAB9")
    draw_polygon(t, [(260, -18), (302, -18), (281, 0)], "black")
    draw_polygon(t, [(270, -55), (170, -55), (170, -60), (270, -60)], "#4A2311")


def draw_nawab(t, is_dead=False):
    t.clear()
    if not is_dead:
        draw_rectangle(t, -60, -90, 26, 55, "#FFD700")
        draw_rectangle(t, -65, -90, 8, 55, "purple")
        draw_circle(t, -47, -25, 14, "#FFDAB9")
        draw_polygon(t, [(-65, -15), (-29, -15), (-47, 5)], "darkgreen")
        draw_circle(t, -47, -5, 4, "red")
        draw_line(t, -40, -60, -10, -20, "silver", 3)
    else:
        draw_rectangle(t, -100, -120, 55, 26, "#FFD700")
        draw_rectangle(t, -100, -125, 55, 8, "purple")
        draw_circle(t, -35, -107, 14, "#FFDAB9")
        draw_polygon(t, [(-25, -120), (-25, -84), (-5, -107)], "darkgreen")
        draw_circle(t, -55, -120, 15, "red")
        draw_circle(t, -70, -115, 10, "darkred")
        draw_circle(t, -40, -125, 8, "red")


def animate_projectile(screen, pen, p_type, start_x, start_y, end_x, end_y, color, duration):
    pen.clear()
    pen.color(color)
    steps = 20
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps

    for i in range(steps):
        pen.clear()
        x, y = translate_2d(start_x, start_y, dx * i, dy * i)

        if p_type == "cannon":
            arc = math.sin(math.pi * (i / steps)) * 40
            draw_circle(pen, x, y + arc, 6, color)
        elif p_type == "arrow":
            arr_ex = x + (20 if dx > 0 else -20)
            arr_ey = y + (dy / dx) * 20 if dx != 0 else y
            draw_line(pen, x, y, arr_ex, arr_ey, color, 2)
        else:
            bul_ex = x + (15 if dx > 0 else -15)
            draw_line(pen, x, y, bul_ex, y, color, 4)

        screen.update()
        time.sleep(duration / steps)
    pen.clear()


def play_animation(screen, anim_pen):
    if os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")
    elif os.path.exists("map.gif"):
        screen.bgpic("map.gif")

    anim_pen.clear()
    target_x, target_y = 150, -20
    anim_pen.pensize(3)
    anim_pen.color("red")

    for scale in range(1, 6):
        anim_pen.clear()
        draw_rectangle(anim_pen, target_x - scale * 10, target_y - scale * 10, scale * 20, scale * 20, "")
        screen.update()
        time.sleep(0.1)

    time.sleep(0.5)
    anim_pen.clear()

    if os.path.exists("plassey_bg.gif"):
        screen.bgpic("plassey_bg.gif")
    else:
        screen.bgpic("nopic")
        screen.bgcolor("#8B0000")

    draw_labels(anim_pen)
    draw_bengali_forces(anim_pen)
    draw_british_forces(anim_pen)

    nawab_pen = turtle.Turtle()
    nawab_pen.hideturtle()
    nawab_pen.speed(0)
    draw_nawab(nawab_pen, is_dead=False)
    screen.update()
    time.sleep(1)

    projectile_pen = turtle.Turtle()
    projectile_pen.hideturtle()
    projectile_pen.speed(0)

    for _ in range(3):
        animate_projectile(screen, projectile_pen, "cannon", -100, -50, 200, -80, "black", 0.7)
        animate_projectile(screen, projectile_pen, "cannon", 160, -60, -150, -80, "#333333", 0.7)
        animate_projectile(screen, projectile_pen, "arrow", -100, -30, 250, -40, "silver", 0.5)
        animate_projectile(screen, projectile_pen, "arrow", -80, -10, 270, -20, "silver", 0.5)
        animate_projectile(screen, projectile_pen, "bullet", 170, -55, -20, -55, "yellow", 0.5)
        time.sleep(0.2)

    draw_circle(projectile_pen, 170, -55, 15, "orange")
    screen.update()
    time.sleep(0.1)
    projectile_pen.clear()

    animate_projectile(screen, projectile_pen, "bullet", 170, -55, -45, -55, "yellow", 0.5)

    draw_nawab(nawab_pen, is_dead=True)
    screen.update()