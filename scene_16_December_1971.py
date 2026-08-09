import turtle
import time
import os


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


def draw_rectangle(t, x, y, width, height, color):
    # Basic shapes drawing using OpenGL/Turtle
    draw_polygon(t, [(x, y), (x + width, y), (x + width, y - height), (x, y - height)], color)


def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty


def draw_star(pen, x, y, size, color):
    # Basic shapes drawing using OpenGL/Turtle
    pen.penup()
    pen.goto(x, y)
    pen.setheading(0)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(5):
        pen.forward(size)
        pen.right(144)
    pen.end_fill()
    pen.setheading(0)


def draw_bd_flag(pen, x, y, scale=0.5):
    width = 300 * scale
    height = 180 * scale

    draw_line_dda(pen, x, -250, x, 250, "silver", 6)

    draw_rectangle(pen, x, y, width, height, "#006a4e")

    center_x = x + (width * 9 / 20)
    center_y = y - (height / 2)
    radius = 60 * scale

    draw_midpoint_circle(pen, center_x, center_y, radius, "#f42a41", fill=True)

    map_points = [
        (-25, -30), (-35, -10), (-40, 0), (-30, 15), (-20, 35), (-10, 40),
        (0, 25), (10, 30), (20, 30), (35, 20), (20, 5), (15, -5),
        (30, -15), (40, -30), (30, -45), (20, -30), (5, -25),
        (-5, -35), (-15, -25), (-25, -30)
    ]

    translated_map = [translate_2d(center_x, center_y, p[0] * scale, p[1] * scale) for p in map_points]
    draw_polygon(pen, translated_map, "#FFD700")


def draw_pk_flag(pen, x, y, scale=0.5):
    width = 300 * scale
    height = 180 * scale

    draw_line_dda(pen, x, -250, x, 250, "silver", 6)

    stripe_width = width * 0.25
    draw_rectangle(pen, x, y, stripe_width, height, "white")
    draw_rectangle(pen, x + stripe_width, y, width - stripe_width, height, "#00401A")

    crescent_x = x + stripe_width + ((width - stripe_width) / 2)
    crescent_y = y - height / 2
    radius = 45 * scale

    draw_midpoint_circle(pen, crescent_x, crescent_y, radius, "white", fill=True)

    inner_yc = (crescent_y - radius) + (15 * scale) + (radius * 0.85)
    draw_midpoint_circle(pen, crescent_x + (12 * scale), inner_yc, radius * 0.85, "#00401A", fill=True)

    draw_star(pen, crescent_x + (15 * scale), crescent_y + (10 * scale), 20 * scale, "white")


def play_animation(screen, anim_pen):
    if os.path.exists("16_December.gif"):
        screen.bgpic("16_December.gif")
    else:
        screen.bgcolor("#1a1a1a")
        anim_pen.color("white")
        anim_pen.write("Missing 16_December.gif", align="center", font=("Arial", 16, "bold"))

    anim_pen.clear()
    anim_pen.hideturtle()
    anim_pen.speed(0)
    screen.update()
    time.sleep(1)

    text_pen = turtle.Turtle()
    text_pen.hideturtle()
    text_pen.penup()

    flag_pen = turtle.Turtle()
    flag_pen.hideturtle()
    flag_pen.speed(0)

    total_steps = 40
    start_y_up = -120
    end_y_up = 200

    start_y_down = 200
    end_y_down = -120

    for step in range(total_steps + 1):
        flag_pen.clear()

        _, current_bd_y = translate_2d(0, start_y_up, 0, step * ((end_y_up - start_y_up) / total_steps))
        _, current_pk_y = translate_2d(0, start_y_down, 0, -step * ((start_y_down - end_y_down) / total_steps))

        draw_bd_flag(flag_pen, -350, current_bd_y, scale=0.45)
        draw_pk_flag(flag_pen, 200, current_pk_y, scale=0.45)

        screen.update()
        time.sleep(0.06)

    time.sleep(0.5)

    text_pen.goto(2, 232)
    text_pen.color("black")
    text_pen.write("১৬ ডিসেম্বর ১৯৭১: ঐতিহাসিক আত্মসমর্পণ", align="center", font=("Times New Roman", 22, "bold"))
    text_pen.goto(0, 230)
    text_pen.color("#FFC300")
    text_pen.write("১৬ ডিসেম্বর ১৯৭১: ঐতিহাসিক আত্মসমর্পণ", align="center", font=("Times New Roman", 22, "bold"))

    screen.update()
    time.sleep(1.2)

    text_pen.goto(2, 172)
    text_pen.color("black")
    text_pen.write("জয় বাংলা!", align="center", font=("Georgia", 30, "bold"))
    text_pen.goto(0, 170)
    text_pen.color("#00FF88")
    text_pen.write("জয় বাংলা!", align="center", font=("Georgia", 30, "bold"))

    screen.update()
    time.sleep(1.0)

    text_pen.goto(2, 112)
    text_pen.color("black")
    text_pen.write("স্বাধীন বাংলাদেশ", align="center", font=("Georgia", 26, "bold"))
    text_pen.goto(0, 110)
    text_pen.color("#FF5733")
    text_pen.write("স্বাধীন বাংলাদেশ", align="center", font=("Georgia", 26, "bold"))

    screen.update()


if __name__ == "__main__":
    sc = turtle.Screen()
    sc.setup(width=800, height=600)
    sc.title("16 December 1971 - Victory Day")
    sc.tracer(0)
    p = turtle.Turtle()
    p.hideturtle()
    play_animation(sc, p)
    turtle.done()