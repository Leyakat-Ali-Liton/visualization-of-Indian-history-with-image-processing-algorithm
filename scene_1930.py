import turtle
import time
import os


def draw_bresenham_line(t, x1, y1, x2, y2, color):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    t.pensize(4)
    t.goto(x2, y2)


def draw_midpoint_circle(t, x_center, y_center, radius, color):
    t.penup()
    t.goto(x_center, y_center - radius)
    t.pendown()
    t.color(color)
    t.pensize(3)
    t.circle(radius)


def play_animation(screen, anim_pen):
    if os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")
    elif os.path.exists("map.gif"):
        screen.bgpic("map.gif")

    anim_pen.clear()

    # চট্টগ্রামের একদম পারফেক্ট কোঅর্ডিনেট (আগের চেয়ে আরেকটু ডানে ও ওপরে)
    chattogram_x, chattogram_y = 310, -40

    anim_pen.pensize(3)
    anim_pen.color("red")

    for scale in range(1, 6):
        anim_pen.clear()
        anim_pen.penup()
        anim_pen.goto(chattogram_x - scale * 12, chattogram_y - scale * 12)
        anim_pen.pendown()
        for _ in range(4):
            anim_pen.forward(scale * 24)
            anim_pen.left(90)

        anim_pen.penup()
        anim_pen.goto(chattogram_x, chattogram_y + scale * 12 + 5)
        anim_pen.pendown()
        anim_pen.write("Chattogram", align="center", font=("Arial", 12 + scale, "bold"))
        screen.update()
        time.sleep(0.15)

    time.sleep(1)
    anim_pen.clear()

    if os.path.exists("club_interior.gif"):
        screen.bgpic("club_interior.gif")
    else:
        screen.bgcolor("#1a2b3c")
        anim_pen.write("Missing club_interior.gif", align="center", font=("Arial", 14, "bold"))

    action_pen = turtle.Turtle()
    action_pen.hideturtle()
    action_pen.speed(0)

    for i in range(8):
        action_pen.clear()
        draw_bresenham_line(action_pen, -250, -50 + (i * 15), 100, -10 - (i * 5), "yellow")
        draw_bresenham_line(action_pen, 200, -30, -150, -70 + (i * 8), "orange")
        screen.update()
        time.sleep(0.06)

    action_pen.clear()

    for _ in range(2):
        radius = 10
        for _ in range(7):
            draw_midpoint_circle(action_pen, 80, -40, radius, "gray")
            radius += 18
            screen.update()
            time.sleep(0.05)
            action_pen.clear()

    anim_pen.penup()
    anim_pen.goto(0, -250)
    anim_pen.color("white")
    anim_pen.write("Press 'SPACEBAR' to view the historical conclusion.", align="center", font=("Courier", 16, "bold"))
    screen.update()

    def trigger_martyrdom_scene():
        screen.onkey(None, "space")
        anim_pen.clear()
        action_pen.clear()
        if os.path.exists("cyanide_normal.gif"):
            screen.bgpic("cyanide_normal.gif")
        anim_pen.goto(0, -260)
        anim_pen.color("white")
        anim_pen.write("Pritilata chose martyrdom over capture (1932).", align="center", font=("Arial", 18, "bold"))
        screen.update()
        time.sleep(3.5)
        anim_pen.clear()
        anim_pen.color("red")
        anim_pen.write("Her sacrifice ignited the revolution.", align="center", font=("Arial", 20, "bold"))
        screen.update()

    screen.listen()
    screen.onkey(trigger_martyrdom_scene, "space")