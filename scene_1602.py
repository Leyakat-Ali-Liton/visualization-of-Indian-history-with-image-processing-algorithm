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

def draw_royal_ship(t, x, y):
    # Basic shapes drawing using OpenGL/Turtle
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.fillcolor("#5C3A21")
    t.begin_fill()
    t.goto(x + 50, y)
    t.goto(x + 40, y - 20)
    t.goto(x - 30, y - 20)
    t.goto(x - 40, y)
    t.goto(x - 40, y + 15)
    t.goto(x - 20, y + 15)
    t.goto(x - 15, y)
    t.goto(x, y)
    t.end_fill()

    t.color("black")
    t.pensize(3)
    t.penup()
    t.goto(x - 10, y + 15)
    t.pendown()
    t.goto(x - 10, y + 45)

    t.pensize(1)
    t.fillcolor("#F5F5DC")
    t.begin_fill()
    t.penup()
    t.goto(x - 10, y + 20)
    t.pendown()
    t.goto(x + 15, y + 20)
    t.goto(x + 10, y + 40)
    t.goto(x - 10, y + 40)
    t.end_fill()

    t.color("black")
    t.pensize(3)
    t.penup()
    t.goto(x + 20, y)
    t.pendown()
    t.goto(x + 20, y + 55)

    t.pensize(1)
    t.fillcolor("#F5F5DC")
    t.begin_fill()
    t.penup()
    t.goto(x + 20, y + 25)
    t.pendown()
    t.goto(x + 45, y + 25)
    t.goto(x + 35, y + 50)
    t.goto(x + 20, y + 50)
    t.end_fill()

    t.penup()
    t.goto(x + 20, y + 55)
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    t.goto(x + 35, y + 55)
    t.goto(x + 35, y + 47)
    t.goto(x + 20, y + 47)
    t.goto(x + 20, y + 55)
    t.end_fill()

    t.color("red")
    t.pensize(2)
    t.penup()
    t.goto(x + 27.5, y + 55)
    t.pendown()
    t.goto(x + 27.5, y + 47)
    t.penup()
    t.goto(x + 20, y + 51)
    t.pendown()
    t.goto(x + 35, y + 51)
    t.color("black")

def draw_businessman(t, x, y):
    draw_rectangle(t, x, y, 10, 25, "#2F4F4F")
    draw_circle(t, x + 5, y + 30, 5, "#FFDAB9")
    draw_rectangle(t, x, y + 35, 10, 8, "black")
    draw_line(t, x - 3, y + 35, x + 13, y + 35, "black", 2)
    draw_line(t, x + 12, y + 15, x + 12, y, "silver", 2)

def animate_title_text(screen, text_pen):
    start_y = 400
    target_y = 200
    text_x = 180
    outline_offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, -3), (0, 3), (-3, 0), (3, 0)]

    for y in range(start_y, target_y, -10):
        text_pen.clear()

        text_pen.color("white")
        for ox, oy in outline_offsets:
            text_pen.penup()
            text_pen.goto(text_x + ox, y + oy)
            text_pen.write("ARRIVAL OF THE BRITISH\nEAST INDIA COMPANY", align="center", font=("Georgia", 22, "bold"))
            text_pen.goto(text_x + ox, (y - 42) + oy)
            text_pen.write("CIRCA 1600 - 1602", align="center", font=("Georgia", 18, "italic bold"))

        text_pen.penup()
        text_pen.goto(text_x, y)
        text_pen.color("black")
        text_pen.write("ARRIVAL OF THE BRITISH\nEAST INDIA COMPANY", align="center", font=("Georgia", 22, "bold"))

        text_pen.goto(text_x, y - 42)
        text_pen.color("#8B0000")
        text_pen.write("CIRCA 1600 - 1602", align="center", font=("Georgia", 18, "italic bold"))

        screen.update()
        time.sleep(0.02)

def play_animation(screen, anim_pen):
    if os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")
    elif os.path.exists("map.gif"):
        screen.bgpic("map.gif")
    else:
        screen.bgpic("nopic")
        screen.bgcolor("#F4EBD0")

    anim_pen.clear()

    text_pen = turtle.Turtle()
    text_pen.hideturtle()
    text_pen.speed(0)
    animate_title_text(screen, text_pen)

    start_x, start_y = 380, -280
    end_x, end_y = 190, -45

    steps = 150
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    curr_x, curr_y = start_x, start_y

    for _ in range(steps):
        anim_pen.clear()
        draw_royal_ship(anim_pen, curr_x, curr_y)
        draw_royal_ship(anim_pen, curr_x + 100, curr_y)

        screen.update()
        curr_x, curr_y = translate_2d(curr_x, curr_y, dx, dy)
        time.sleep(0.04)

    people_pen = turtle.Turtle()
    people_pen.hideturtle()
    people_pen.speed(0)

    ship_positions = [
        (curr_x + 10, curr_y + 15),
        (curr_x + 110, curr_y + 15)
    ]

    walk_steps = 35
    for w in range(walk_steps):
        people_pen.clear()
        for i, (sx, sy) in enumerate(ship_positions):
            px, py = translate_2d(sx, sy, -(w * 0.5), w * 1.5)
            draw_businessman(people_pen, px, py)
            draw_businessman(people_pen, px + 25, py - 10)

        screen.update()
        time.sleep(0.06)

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(width=900, height=600)
    screen.tracer(0)
    screen.title("British East India Company Arrival")

    anim_pen = turtle.Turtle()
    anim_pen.hideturtle()
    anim_pen.speed(0)

    play_animation(screen, anim_pen)

    screen.mainloop()