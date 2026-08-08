import os
import time
import random
import turtle


# =========================================================
# HELPER: Safe Update to Prevent TclError when Skipping
# =========================================================
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


# =========================================================
# LAB ALGORITHMS & SHAPES
# =========================================================

def bresenham_line(pen, x1, y1, x2, y2, color="white", size=2):
    try:
        pen.penup()
        pen.color(color)
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            safe_goto(pen, x1, y1)
            pen.dot(size)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    except:
        pass


def midpoint_circle(pen, xc, yc, r, color="red", size=2, fill=False):
    try:
        pen.penup()
        pen.color(color)
        x = 0;
        y = int(r);
        p = 1 - r

        def draw_points_and_fill(xc, yc, x, y):
            points = [(xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                      (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)]
            for px, py in points:
                safe_goto(pen, px, py)
                pen.dot(size)
                if fill:
                    bresenham_line(pen, xc - x, yc + y, xc + x, yc + y, color=color, size=size)
                    bresenham_line(pen, xc - x, yc - y, xc + x, yc - y, color=color, size=size)

        draw_points_and_fill(xc, yc, x, y)
        while x < y:
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1
            draw_points_and_fill(xc, yc, x, y)
    except:
        pass


def draw_filled_pillar(pen, cx, cy, width, height, color="#FFFFFF"):
    try:
        pen.penup();
        safe_goto(pen, cx - width / 2, cy);
        pen.pendown()
        pen.color(color);
        pen.fillcolor(color);
        pen.begin_fill()
        safe_goto(pen, cx - width / 2, cy + height);
        safe_goto(pen, cx + width / 2, cy + height)
        safe_goto(pen, cx + width / 2, cy);
        safe_goto(pen, cx - width / 2, cy)
        pen.end_fill();
        pen.penup()
    except:
        pass


# =========================================================
# CHARACTER DRAWINGS
# =========================================================

def draw_soldier(pen, cx, cy):
    midpoint_circle(pen, cx, cy + 30, 10, color="#1A2421", size=2, fill=True)
    midpoint_circle(pen, cx, cy + 25, 7, color="#C68E17", size=2, fill=True)
    bresenham_line(pen, cx, cy + 18, cx, cy - 15, color="#4A5D23", size=15)
    bresenham_line(pen, cx - 5, cy + 5, cx + 30, cy + 5, color="#4A5D23", size=6)
    bresenham_line(pen, cx + 15, cy + 8, cx + 45, cy + 8, color="#222222", size=4)
    bresenham_line(pen, cx - 4, cy - 15, cx - 12, cy - 40, color="#4A5D23", size=7)
    bresenham_line(pen, cx + 4, cy - 15, cx + 12, cy - 40, color="#4A5D23", size=7)
    bresenham_line(pen, cx - 12, cy - 40, cx - 18, cy - 45, color="#111111", size=9)
    bresenham_line(pen, cx + 12, cy - 40, cx + 18, cy - 45, color="#111111", size=9)


def draw_student(pen, cx, cy, state="standing"):
    if state == "standing":
        midpoint_circle(pen, cx, cy + 30, 9, color="#FFDAB9", size=2, fill=True)
        midpoint_circle(pen, cx, cy + 36, 7, color="#111111", size=2, fill=True)
        bresenham_line(pen, cx, cy + 20, cx, cy - 20, color="#F8F9FA", size=14)
        bresenham_line(pen, cx - 10, cy + 10, cx - 12, cy - 10, color="#F8F9FA", size=5)
        bresenham_line(pen, cx + 10, cy + 10, cx + 12, cy - 10, color="#F8F9FA", size=5)
        bresenham_line(pen, cx - 4, cy - 20, cx - 8, cy - 45, color="#2C3E50", size=6)
        bresenham_line(pen, cx + 4, cy - 20, cx + 8, cy - 45, color="#2C3E50", size=6)
    elif state == "fallen":
        midpoint_circle(pen, cx + 20, cy - 40, 18, color="#8B0000", size=2, fill=True)
        midpoint_circle(pen, cx + 10, cy - 35, 12, color="#AA0000", size=2, fill=True)
        midpoint_circle(pen, cx + 35, cy - 38, 9, color="#FFDAB9", size=2, fill=True)
        midpoint_circle(pen, cx + 40, cy - 38, 7, color="#111111", size=2, fill=True)
        bresenham_line(pen, cx + 25, cy - 40, cx - 15, cy - 40, color="#F8F9FA", size=14)
        bresenham_line(pen, cx + 5, cy - 40, cx + 15, cy - 40, color="#8B0000", size=14)
        bresenham_line(pen, cx - 15, cy - 38, cx - 40, cy - 32, color="#2C3E50", size=6)
        bresenham_line(pen, cx - 15, cy - 42, cx - 40, cy - 48, color="#2C3E50", size=6)


def draw_shaheed_minar(pen, cx, cy, scale=1.0):
    midpoint_circle(pen, cx, cy + int(25 * scale), int(18 * scale), color="#E03C31", size=3, fill=True)
    draw_filled_pillar(pen, cx, cy, width=8 * scale, height=50 * scale, color="#FFFFFF")
    draw_filled_pillar(pen, cx - 18 * scale, cy, width=6 * scale, height=35 * scale, color="#FFFFFF")
    draw_filled_pillar(pen, cx + 18 * scale, cy, width=6 * scale, height=35 * scale, color="#FFFFFF")
    draw_filled_pillar(pen, cx - 34 * scale, cy, width=5 * scale, height=20 * scale, color="#FFFFFF")
    draw_filled_pillar(pen, cx + 34 * scale, cy, width=5 * scale, height=20 * scale, color="#FFFFFF")
    bresenham_line(pen, cx - 42 * scale, cy - 2 * scale, cx + 42 * scale, cy - 2 * scale, color="#DDDDDD", size=8)
    bresenham_line(pen, cx - 46 * scale, cy - 8 * scale, cx + 46 * scale, cy - 8 * scale, color="#AAAAAA", size=8)


# =========================================================
# MAIN SCENE ENTRY POINT
# =========================================================

def play_animation_1952(screen, pen):
    screen.tracer(0)
    pen.clear()

    # --- PHASE 1: MAP VIEW ---
    image_name = "map.gif"
    if os.path.exists(image_name):
        screen.bgpic(image_name)

    dhaka_x_map, dhaka_y_map = 190, 15

    # Pulse animation
    for r in range(10, 65, 10):
        midpoint_circle(pen, dhaka_x_map, dhaka_y_map, r, color="#E03C31", size=2)
        safe_update(screen)
        time.sleep(0.00)

    # No Wait. Instant clear and transition.
    pen.clear()

    # --- PHASE 2: INSTANT BATTLE ---
    try:
        screen.bgpic("nopic")
        screen.bgcolor("#2a1b1b")
    except:
        pass

    # Setup Dedicated Pens for Layering (REMOVES LAG)
    static_pen = turtle.Turtle()
    static_pen.hideturtle()
    static_pen.speed(0)

    student_pen = turtle.Turtle()
    student_pen.hideturtle()
    student_pen.speed(0.1)

    bullet_pen = turtle.Turtle()
    bullet_pen.hideturtle()
    bullet_pen.speed(0.1)

    # Characters Data
    army_x = -220
    fight_y = -80
    soldiers = [
        {"x": army_x, "y": fight_y},
        {"x": army_x - 40, "y": fight_y + 25},
        {"x": army_x - 40, "y": fight_y - 25},
        {"x": army_x - 80, "y": fight_y + 10}
    ]

    st_start_x = 20
    students = [
        {"x": st_start_x, "y": fight_y, "state": "standing"},
        {"x": st_start_x + 50, "y": fight_y + 15, "state": "standing"},
        {"x": st_start_x + 100, "y": fight_y - 10, "state": "standing"},
        {"x": st_start_x + 150, "y": fight_y + 20, "state": "standing"},
        {"x": st_start_x + 200, "y": fight_y, "state": "standing"},
        {"x": st_start_x + 250, "y": fight_y - 15, "state": "standing"}
    ]

    # DRAW STATIC ELEMENTS ONCE (Reduces CPU calculation overhead)
    try:
        static_pen.penup()
        safe_goto(static_pen, 0, 140)
        static_pen.color("#00ffcc")
        static_pen.write("রাষ্ট্রভাষা বাংলা চাই!", align="center", font=("Arial", 22, "bold"))
    except:
        pass

    urdu_letters = ["ا", "ب", "پ", "ت", "ج", "چ", "خ", "د"]
    for i in range(8):
        static_pen.penup()
        safe_goto(static_pen, random.randint(-380, -100), random.randint(-20, 120))
        static_pen.color("#5a6b5d")
        static_pen.write(urdu_letters[i], align="center", font=("Arial", 28, "bold"))

    for s in soldiers:
        draw_soldier(static_pen, s["x"], s["y"])

    # Draw initial students
    for st in students:
        draw_student(student_pen, st["x"], st["y"], state=st["state"])

    safe_update(screen)

    # --- 3 FAST VOLLEYS OF FIRE ---
    bangla_chars = ["অ", "আ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", "ঝ", "ঞ", "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ",
                    "ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ"]
    active_letters = []

    for volley in range(3):
        # 1. Spawn letters
        for _ in range(2):
            bx = random.randint(30, 350);
            by = random.randint(-40, 100)
            char = random.choice(bangla_chars)
            active_letters.append({"char": char, "x": bx, "y": by, "color": "#F8F9FA"})
            student_pen.penup();
            safe_goto(student_pen, bx, by)
            student_pen.color("#F8F9FA");
            student_pen.write(char, align="center", font=("Arial", 28, "bold"))

        # 2. Fast Bullet Dash (Only 1 frame of movement to make it lightning fast)
        bullet_pen.clear()
        bullet_pen.pensize(4)
        bullet_pen.color("orange")
        for s in soldiers:
            bullet_pen.penup()
            safe_goto(bullet_pen, s["x"] + 45, s["y"] + 8)
            bullet_pen.pendown()
            safe_goto(bullet_pen, s["x"] + 250, s["y"] + 8)  # Long fast bullet line stretching towards students

        safe_update(screen)
        time.sleep(0.01)  # Tiny wait just so the bullet flash is visible

        # 3. Bullet Hits & Instant Death
        bullet_pen.clear()

        if volley == 0:
            students[0]["state"] = "fallen"
        elif volley == 1:
            students[1]["state"] = "fallen"
            students[2]["state"] = "fallen"
        elif volley == 2:
            students[3]["state"] = "fallen"

            # Turn some letters red
        if active_letters:
            random.choice(active_letters)["color"] = "#FF0000"

        # Only clear and redraw the students and letters, NOT the whole scene (Zero lag)
        student_pen.clear()
        for st in students:
            draw_student(student_pen, st["x"], st["y"], state=st["state"])
        for letter in active_letters:
            student_pen.penup();
            safe_goto(student_pen, letter["x"], letter["y"])
            student_pen.color(letter["color"]);
            student_pen.write(letter["char"], align="center", font=("Arial", 28, "bold"))

        safe_update(screen)
        time.sleep(0.00)  # Instant transition to next volley

    # --- PHASE 3: THE MONUMENT RISES IMMEDIATELY ---
    # NO time.sleep here at all. Immediately clear and draw monument.
    bullet_pen.clear()
    student_pen.clear()
    static_pen.clear()
    pen.clear()

    try:
        screen.bgcolor("#1E272E")
    except:
        pass

    try:
        pen.penup()
        safe_goto(pen, 0, 140)
        pen.color("#E03C31")
        pen.write('"Rashtrabhasha Bangla Chai"', align="center", font=("Arial", 16, "italic"))
    except:
        pass

    draw_shaheed_minar(pen, cx=0, cy=-120, scale=3.5)
    safe_update(screen)