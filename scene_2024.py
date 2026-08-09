import turtle
import time
import random
import math


def draw_line_dda(t, x1, y1, x2, y2, color, thickness=1):
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
    t.pensize(thickness)
    for _ in range(steps):
        x += x_inc
        y += y_inc
        t.goto(x, y)
    t.pensize(1)
    t.penup()


def draw_midpoint_circle(t, xc, yc, r, color, fill=False):
    # Mid-Point circle drawing algorithm
    x = 0
    y = r
    p = 1 - r
    t.color(color)
    while x <= y:
        if fill:
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
        else:
            for px, py in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
                t.penup();
                t.goto(xc + px, yc + py);
                t.pendown();
                t.dot(2, color)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
    t.penup()


def draw_polygon(t, points, color):
    # Basic shapes drawing using OpenGL/Turtle
    if not points:
        return
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    t.end_fill()
    t.penup()


def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty


def draw_protester(pen, x, y):
    draw_line_dda(pen, x, y - 10, x, y - 35, "#1a1a1a", 3)
    draw_line_dda(pen, x, y - 35, x - 8, y - 50, "#1a1a1a", 3)
    draw_line_dda(pen, x, y - 35, x + 8, y - 50, "#1a1a1a", 3)
    draw_line_dda(pen, x, y - 20, x - 12, y - 5, "#1a1a1a", 3)
    draw_line_dda(pen, x, y - 20, x + 12, y - 5, "#1a1a1a", 3)
    draw_midpoint_circle(pen, x, y - 10, 6, "#111111", fill=True)
    draw_line_dda(pen, x - 6, y - 8, x + 6, y - 8, "#ff3333", 2)


def draw_helicopter(pen, x, y, angle=0):
    draw_midpoint_circle(pen, x, y + 25, 25, "#444444", fill=True)
    draw_midpoint_circle(pen, x + 10, y + 20, 10, "#88ccff", fill=True)

    # 2D Geometric transformation (Translation & Rotation)
    blade_length = 45
    bx1 = x + math.cos(angle) * blade_length
    by1 = (y + 45) + math.sin(angle) * 6
    bx2 = x - math.cos(angle) * blade_length
    by2 = (y + 45) - math.sin(angle) * 6

    draw_line_dda(pen, bx1, by1, bx2, by2, "black", 5)
    draw_line_dda(pen, x + 20, y + 15, x + 60, y + 15, "black", 3)
    draw_midpoint_circle(pen, x + 60, y + 15, 4, "black", fill=True)


def draw_detailed_person(pen, px, py, step_index):
    draw_midpoint_circle(pen, px, py + 25, 7, "#111111", fill=True)
    draw_line_dda(pen, px, py + 18, px, py - 10, "#222222", 3)

    leg_offset = 6 if (step_index % 2 == 0) else -6

    draw_line_dda(pen, px, py - 10, px - 8 + leg_offset, py - 35, "#222222", 3)
    draw_line_dda(pen, px, py - 10, px + 8 - leg_offset, py - 35, "#222222", 3)
    draw_line_dda(pen, px, py + 5, px - 10, py - 5, "#222222", 3)
    draw_line_dda(pen, px, py + 5, px + 10, py - 5, "#222222", 3)


def play_animation(screen, anim_pen):
    screen.bgcolor("#d9d9d9")
    anim_pen.clear()

    text_pen = turtle.Turtle()
    text_pen.hideturtle()
    text_pen.speed(0)

    heli_pen = turtle.Turtle()
    heli_pen.hideturtle()
    heli_pen.speed(0)

    person_pen = turtle.Turtle()
    person_pen.hideturtle()
    person_pen.speed(0)

    crowd_pen = turtle.Turtle()
    crowd_pen.hideturtle()
    crowd_pen.speed(0)

    text_pen.penup()
    text_pen.goto(2, 102)
    text_pen.color("#aaaaaa")
    text_pen.write("5 August 2024", align="center", font=("Georgia", 24, "bold"))
    text_pen.goto(0, 104)
    text_pen.color("#cc0000")
    text_pen.write("5 August 2024", align="center", font=("Georgia", 24, "bold"))

    screen.update()

    hx, hy = 0, -30
    heli_pen.clear()
    draw_helicopter(heli_pen, hx, hy, angle=0)
    screen.update()

    start_px, start_py = -120, -30
    total_boarding_steps = 40

    for step in range(total_boarding_steps):
        person_pen.clear()
        tx = (hx - start_px) * (step / (total_boarding_steps - 1))
        curr_px, _ = translate_2d(start_px, start_py, tx, 0)

        draw_detailed_person(person_pen, curr_px, start_py, step)
        screen.update()
        time.sleep(0.1)

    person_pen.clear()
    screen.update()

    text_pen.clear()
    text_pen.goto(2, 102)
    text_pen.color("#aaaaaa")
    text_pen.write("", align="center", font=("Georgia", 20, "bold"))
    text_pen.goto(0, 104)
    text_pen.color("#8B0000")
    text_pen.write("", align="center", font=("Georgia", 20, "bold"))
    screen.update()
    time.sleep(1.0)

    total_slow_steps = 50
    blade_angle = 0
    for _ in range(total_slow_steps):
        heli_pen.clear()
        draw_helicopter(heli_pen, hx, hy, angle=blade_angle)
        screen.update()
        blade_angle += 0.8
        time.sleep(0.1)
        _, hy = translate_2d(hx, hy, 0, 6)

    heli_pen.clear()
    text_pen.clear()
    screen.update()

    text_pen.goto(2, 212)
    text_pen.color("#aaaaaa")
    text_pen.write("পালাইছে রে পালাইছে, খুনি হাসিনা পালাইছে", align="center", font=("Georgia", 26, "bold"))
    text_pen.goto(0, 214)
    text_pen.color("#990000")
    text_pen.write("পালাইছে রে পালাইছে, খুনি হাসিনা পালাইছে", align="center", font=("Georgia", 26, "bold"))

    text_pen.goto(2, 152)
    text_pen.color("#aaaaaa")
    text_pen.write("Dawn of Freedom - Mass Uprising Success", align="center", font=("Georgia", 20, "bold"))
    text_pen.goto(0, 154)
    text_pen.color("#006a4e")
    text_pen.write("Dawn of Freedom - Mass Uprising Success", align="center", font=("Georgia", 20, "bold"))

    screen.update()

    for _ in range(70):
        x = random.randint(-430, 430)
        y = random.randint(-240, -40)
        draw_protester(crowd_pen, x, y)
        screen.update()
        time.sleep(0.015)

    time.sleep(0.5)

    banner_pen = turtle.Turtle()
    banner_pen.hideturtle()
    banner_pen.speed(0)

    draw_polygon(banner_pen, [(-240, -45), (240, -45), (240, 10), (-240, 10)], "#006a4e")

    banner_pen.penup()
    banner_pen.goto(0, -32)
    banner_pen.color("white")
    banner_pen.write("5 AUGUST JULY REVOLUTION - 2024", align="center", font=("Arial", 16, "bold"))
    screen.update()
    time.sleep(2)


if __name__ == "__main__":
    sc = turtle.Screen()
    sc.setup(width=900, height=600)
    sc.title("5 August 2024 - Historic Turn")
    sc.tracer(0)

    p = turtle.Turtle()
    p.hideturtle()

    play_animation(sc, p)
    turtle.done()