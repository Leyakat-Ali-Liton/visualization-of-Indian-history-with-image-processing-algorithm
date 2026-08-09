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

def bresenham_line(pen, x1, y1, x2, y2, color="white", size=2):
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

def midpoint_circle(pen, xc, yc, r, color="red", size=2, fill=False):
    # Mid-Point circle drawing algorithm
    try:
        x = 0
        y = r
        p = 1 - r
        pen.color(color)
        pen.pensize(size)
        while x <= y:
            if fill:
                pen.penup(); safe_goto(pen, xc - x, yc + y); pen.pendown(); safe_goto(pen, xc + x, yc + y)
                pen.penup(); safe_goto(pen, xc - x, yc - y); pen.pendown(); safe_goto(pen, xc + x, yc - y)
                pen.penup(); safe_goto(pen, xc - y, yc + x); pen.pendown(); safe_goto(pen, xc + y, yc + x)
                pen.penup(); safe_goto(pen, xc - y, yc - x); pen.pendown(); safe_goto(pen, xc + y, yc - x)
            else:
                for px, py in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
                    pen.penup()
                    safe_goto(pen, xc + px, yc + py)
                    pen.pendown()
                    pen.dot(size, color)
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1
        pen.penup()
    except:
        pass

def draw_filled_pillar(pen, cx, cy, width, height, color="#FFFFFF"):
    # Basic shapes drawing using OpenGL/Turtle
    try:
        pen.penup()
        safe_goto(pen, cx - width / 2, cy)
        pen.pendown()
        pen.color(color)
        pen.fillcolor(color)
        pen.begin_fill()
        safe_goto(pen, cx - width / 2, cy + height)
        safe_goto(pen, cx + width / 2, cy + height)
        safe_goto(pen, cx + width / 2, cy)
        safe_goto(pen, cx - width / 2, cy)
        pen.end_fill()
        pen.penup()
    except:
        pass

def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty

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

def get_safe_bangla_pos(used_positions):
    for _ in range(50):
        bx = random.randint(30, 360)
        by = random.randint(-40, 110)

        if -100 < bx < 100 and 100 < by < 150:
            continue
        if 60 < bx < 200 and 60 < by < 110:
            continue

        overlap = False
        for (ux, uy) in used_positions:
            if abs(bx - ux) < 35 and abs(by - uy) < 35:
                overlap = True
                break

        if not overlap:
            used_positions.append((bx, by))
            return bx, by

    return random.randint(220, 350), random.randint(-30, 50)

def play_animation_1952(screen, pen):
    screen.tracer(0)
    pen.clear()

    image_name = "map.gif"
    if os.path.exists(image_name):
        screen.bgpic(image_name)

    dhaka_x_map, dhaka_y_map = 190, 15
    for r in range(10, 65, 10):
        midpoint_circle(pen, dhaka_x_map, dhaka_y_map, r, color="#E03C31", size=2)
        safe_update(screen)
        time.sleep(0.05)

    pen.clear()

    try:
        screen.bgpic("nopic")
        screen.bgcolor("#2a1b1b")
    except:
        pass

    static_pen = turtle.Turtle()
    static_pen.hideturtle()
    static_pen.speed(0)

    student_pen = turtle.Turtle()
    student_pen.hideturtle()
    student_pen.speed(0)

    bullet_pen = turtle.Turtle()
    bullet_pen.hideturtle()
    bullet_pen.speed(0)

    urdu_pen = turtle.Turtle()
    urdu_pen.hideturtle()
    urdu_pen.speed(0)

    blood_text_pen = turtle.Turtle()
    blood_text_pen.hideturtle()
    blood_text_pen.speed(0)

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

    try:
        static_pen.penup()
        safe_goto(static_pen, 0, 120)
        static_pen.color("#00ffcc")
        static_pen.write("রাষ্ট্রভাষা বাংলা চাই!", align="center", font=("Arial", 22, "bold"))
    except:
        pass

    for s in soldiers:
        draw_soldier(static_pen, s["x"], s["y"])
    for st in students:
        draw_student(student_pen, st["x"], st["y"], state=st["state"])

    urdu_chars = ["ا", "ب", "پ", "ت", "ج", "چ", "خ", "د"]
    urdu_active = [{"char": c, "x": random.randint(-380, -150), "y": random.randint(0, 140)} for c in urdu_chars]

    def draw_urdu():
        urdu_pen.clear()
        for u in urdu_active:
            urdu_pen.penup()
            safe_goto(urdu_pen, u["x"], u["y"])
            urdu_pen.color("#90EE90")
            urdu_pen.write(u["char"], align="center", font=("Arial", 36, "bold"))

    draw_urdu()
    safe_update(screen)
    time.sleep(0.5)

    bangla_chars = ["অ", "আ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", "ঝ", "ঞ", "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ",
                    "ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ", "ঈ", "ঋ"]
    active_bangla_letters = []
    blood_stages = ["বাং", "বাংলা ভা", "বাংলা ভাষা"]
    used_letter_positions = []

    for volley in range(3):
        if len(urdu_active) > 2:
            urdu_active = random.sample(urdu_active, len(urdu_active) - 3)
        else:
            urdu_active = []
        draw_urdu()

        for _ in range(6):
            bx, by = get_safe_bangla_pos(used_letter_positions)
            char = random.choice(bangla_chars)
            active_bangla_letters.append({"char": char, "x": bx, "y": by, "color": "#F8F9FA"})

        bullet_length = 25
        frames = 8
        for frame in range(frames):
            bullet_pen.clear()
            for s in soldiers:
                start_x = s["x"] + 45
                end_x = start_x + 220
                tx = (end_x - start_x) * (frame / float(frames - 1))
                curr_x, curr_y = translate_2d(start_x, s["y"] + 8, tx, 0)
                bullet_pen.penup()
                safe_goto(bullet_pen, curr_x, curr_y)
                bullet_pen.pendown()
                bullet_pen.color("orange")
                bullet_pen.pensize(3)
                safe_goto(bullet_pen, curr_x + bullet_length, curr_y)
            safe_update(screen)
            time.sleep(0.04)

        bullet_pen.clear()
        if volley == 0:
            students[0]["state"] = "fallen"
        elif volley == 1:
            students[1]["state"] = "fallen"
            students[2]["state"] = "fallen"
        elif volley == 2:
            students[3]["state"] = "fallen"

        if active_bangla_letters:
            for _ in range(5):
                random.choice(active_bangla_letters)["color"] = "#FF0000"

        student_pen.clear()
        for st in students:
            draw_student(student_pen, st["x"], st["y"], state=st["state"])

        for letter in active_bangla_letters:
            student_pen.penup()
            safe_goto(student_pen, letter["x"], letter["y"])
            student_pen.color(letter["color"])
            student_pen.write(letter["char"], align="center", font=("Arial", 28, "bold"))

        blood_text_pen.clear()
        blood_text_pen.penup()
        safe_goto(blood_text_pen, 130, 80)
        blood_text_pen.color("#B22222")
        blood_text_pen.write(blood_stages[volley], align="center", font=("Arial", 38, "bold"))

        if volley == 2:
            for _ in range(25):
                blood_text_pen.penup()
                sx = 130 + random.randint(-110, 110)
                sy = 100 + random.randint(-30, 40)
                safe_goto(blood_text_pen, sx, sy)
                blood_text_pen.color("#8B0000")
                blood_text_pen.dot(random.randint(4, 10))

        safe_update(screen)
        time.sleep(1.2)

    time.sleep(1.5)

    bullet_pen.clear()
    student_pen.clear()
    static_pen.clear()
    urdu_pen.clear()
    blood_text_pen.clear()
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