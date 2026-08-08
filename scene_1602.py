import turtle
import time
import os


# --- Basic Helper Functions for Shapes ---
def draw_rectangle(t, x, y, width, height, color):
    t.penup();
    t.goto(x, y);
    t.pendown()
    t.fillcolor(color);
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()


def draw_circle(t, x, y, radius, color):
    t.penup();
    t.goto(x, y - radius);
    t.pendown()
    t.fillcolor(color);
    t.begin_fill()
    t.circle(radius)
    t.end_fill()


def draw_line(t, x1, y1, x2, y2, color, size=2):
    t.penup();
    t.goto(x1, y1);
    t.pendown()
    t.color(color);
    t.pensize(size)
    t.goto(x2, y2)
    t.pensize(1);
    t.color("black")


# --- Object Drawing Functions ---
def draw_royal_ship(t, x, y):
    """DDA/Bresenham concept-এর মাধ্যমে রয়েল শিপ ও পতাকার পলিগন ড্রয়িং"""
    t.penup()
    t.goto(x, y)
    t.pendown()

    # জাহাজের মূল কাঠামো (Hull)
    t.fillcolor("#5C3A21")
    t.begin_fill()
    t.goto(x + 50, y)
    t.goto(x + 40, y - 20)
    t.goto(x - 30, y - 20)
    t.goto(x - 40, y)
    # পেছনের কেবিন (Poop Deck)
    t.goto(x - 40, y + 15)
    t.goto(x - 20, y + 15)
    t.goto(x - 15, y)
    t.goto(x, y)
    t.end_fill()

    # পেছনের পাল (Back Mast & Sail)
    t.color("black")
    t.pensize(3)
    t.penup();
    t.goto(x - 10, y + 15);
    t.pendown()
    t.goto(x - 10, y + 45)

    t.pensize(1)
    t.fillcolor("#F5F5DC")
    t.begin_fill()
    t.penup();
    t.goto(x - 10, y + 20);
    t.pendown()
    t.goto(x + 15, y + 20)
    t.goto(x + 10, y + 40)
    t.goto(x - 10, y + 40)
    t.end_fill()

    # সামনের পাল (Front Mast & Sail)
    t.color("black")
    t.pensize(3)
    t.penup();
    t.goto(x + 20, y);
    t.pendown()
    t.goto(x + 20, y + 55)

    t.pensize(1)
    t.fillcolor("#F5F5DC")
    t.begin_fill()
    t.penup();
    t.goto(x + 20, y + 25);
    t.pendown()
    t.goto(x + 45, y + 25)
    t.goto(x + 35, y + 50)
    t.goto(x + 20, y + 50)
    t.end_fill()

    # ব্রিটিশ ইস্ট ইন্ডিয়া কোম্পানির প্রাথমিক পতাকা
    t.penup();
    t.goto(x + 20, y + 55);
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    t.goto(x + 35, y + 55)
    t.goto(x + 35, y + 47)
    t.goto(x + 20, y + 47)
    t.goto(x + 20, y + 55)
    t.end_fill()

    # পতাকার লাল ক্রস
    t.color("red")
    t.pensize(2)
    t.penup();
    t.goto(x + 27.5, y + 55);
    t.pendown()
    t.goto(x + 27.5, y + 47)
    t.penup();
    t.goto(x + 20, y + 51);
    t.pendown()
    t.goto(x + 35, y + 51)
    t.color("black")


def draw_businessman(t, x, y):
    """ব্রিটিশ ব্যবসায়ী (Top Hat এবং কোট পরিহিত)"""
    draw_rectangle(t, x, y, 10, 25, "#2F4F4F")  # Body
    draw_circle(t, x + 5, y + 30, 5, "#FFDAB9")  # Head

    # Top Hat
    draw_rectangle(t, x, y + 35, 10, 8, "black")
    draw_line(t, x - 3, y + 35, x + 13, y + 35, "black", 2)

    # Walking stick
    draw_line(t, x + 12, y + 15, x + 12, y, "silver", 2)


# --- Main Animation Logic ---
def play_animation(screen, anim_pen):
    if os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")
    elif os.path.exists("map.gif"):
        screen.bgpic("map.gif")
    else:
        screen.bgpic("nopic")
        screen.bgcolor("#1a1a1a")

    anim_pen.clear()

    # ফেজ ১: ২টি জাহাজের আগমন
    start_x, start_y = 380, -280

    # গন্তব্যস্থল পরিবর্তন করে বাংলার উপকূলের সমান্তরালে আনা হয়েছে
    end_x, end_y = 190, -45

    steps = 150
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    curr_x, curr_y = start_x, start_y

    for _ in range(steps):
        anim_pen.clear()

        # প্রথম জাহাজ (বামেরটি)
        draw_royal_ship(anim_pen, curr_x, curr_y)

        # দ্বিতীয় জাহাজ (ডানেরটি) - এবার কোনো Y offset নেই, একদম সমান্তরাল (Horizontal)
        draw_royal_ship(anim_pen, curr_x + 100, curr_y)

        screen.update()
        curr_x += dx
        curr_y += dy
        time.sleep(0.04)

    # ফেজ ২: আনবোর্ডিং (ব্যবসায়ীদের জাহাজ থেকে নামা)
    people_pen = turtle.Turtle()
    people_pen.hideturtle()
    people_pen.speed(0)

    # দুটি জাহাজের ডেক অনুযায়ী ব্যবসায়ীদের স্টার্টিং পয়েন্ট
    ship_positions = [
        (curr_x + 10, curr_y + 15),  # প্রথম জাহাজের ডেক
        (curr_x + 110, curr_y + 15)  # দ্বিতীয় জাহাজের ডেক
    ]

    walk_steps = 35
    for w in range(walk_steps):
        people_pen.clear()
        for i, (sx, sy) in enumerate(ship_positions):
            # ব্যবসায়ীরা জাহাজ থেকে সোজা উপরের দিকে (ভূমির ভেতরে) হেঁটে যাবে
            px = sx - (w * 0.5)
            py = sy + (w * 1.5)

            draw_businessman(people_pen, px, py)
            draw_businessman(people_pen, px + 25, py - 10)

        screen.update()
        time.sleep(0.06)