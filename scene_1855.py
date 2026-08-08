import turtle
import time
import os


# --- Basic Geometric Shapes ---
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


def draw_polygon(t, points, color):
    t.penup();
    t.goto(points[0]);
    t.pendown()
    t.fillcolor(color);
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
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


# --- Scene Elements ---
def draw_labels(t):
    # টেক্সট ওভারল্যাপ ঠিক করার জন্য Y-অক্ষ 200 থেকে 120 করা হয়েছে
    t.penup();
    t.goto(-220, 120);
    t.pendown()
    t.color("#00ffcc")
    t.write("Leaders & Rebel Forces", align="center", font=("Arial", 16, "bold"))

    t.penup();
    t.goto(220, 120);
    t.pendown()
    t.color("#ff4444")
    t.write("British Soldiers", align="center", font=("Arial", 16, "bold"))
    t.color("black")


# --- Character Drawings (Alive & Dead States) ---
def draw_rebel(t, x, y, is_dead, r_type):
    if not is_dead:
        if r_type == "santhal":
            draw_rectangle(t, x, y, 15, 35, "#8B4513")  # Body
            draw_circle(t, x + 7, y + 45, 10, "#8B4513")  # Head
            draw_rectangle(t, x - 2, y + 5, 20, 10, "white")  # Cloth
            # Bow
            draw_line(t, x + 15, y + 35, x + 25, y + 20, "brown", 2)
            draw_line(t, x + 25, y + 20, x + 15, y + 5, "brown", 2)
            draw_line(t, x + 15, y + 35, x + 15, y + 5, "white", 1)
        else:
            # Sepoy
            draw_rectangle(t, x, y, 15, 35, "#B22222")  # Coat
            draw_circle(t, x + 7, y + 45, 10, "#A0522D")  # Head
            draw_polygon(t, [(x - 5, y + 55), (x + 20, y + 55), (x + 7, y + 65)], "white")  # Turban
            # Sword
            draw_line(t, x + 15, y + 25, x + 30, y + 35, "silver", 3)
    else:
        # Dead Rebel
        color = "#8B4513" if r_type == "santhal" else "#B22222"
        draw_rectangle(t, x - 15, y - 10, 35, 15, color)
        draw_circle(t, x - 20, y - 5, 10, "#8B4513" if r_type == "santhal" else "#A0522D")
        draw_circle(t, x - 10, y - 5, 8, "red")  # Blood


def draw_british_soldier(t, x, y, is_dead):
    if not is_dead:
        draw_rectangle(t, x, y, 15, 35, "red")
        draw_circle(t, x + 7, y + 45, 10, "#FFDAB9")
        draw_polygon(t, [(x - 5, y + 55), (x + 20, y + 55), (x + 7, y + 65)], "black")
        # Gun Aiming
        draw_line(t, x, y + 25, x - 30, y + 25, "#4A2311", 3)
    else:
        # Dead British
        draw_rectangle(t, x - 10, y - 10, 35, 15, "red")
        draw_circle(t, x + 30, y - 5, 10, "#FFDAB9")
        draw_circle(t, x + 15, y - 5, 8, "darkred")


def render_all_armies(t, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead):
    t.clear()
    for i in range(10):
        draw_rebel(t, rebel_coords[i][0], rebel_coords[i][1], rebel_dead[i], rebel_types[i])
    for i in range(10):
        draw_british_soldier(t, british_coords[i][0], british_coords[i][1], british_dead[i])


# --- Combat Animation (Translation) ---
def animate_volley(screen, pen, active_rebels, active_british, duration):
    steps = 25
    for i in range(steps):
        pen.clear()

        # ১. সিধু-কানহুর বিশেষ তীর ছোঁড়া (Real Image এর পজিশন থেকে)
        sk_arrow_x = -240 + ((350 - (-240)) / steps) * i
        draw_line(pen, sk_arrow_x, -50, sk_arrow_x + 20, -50, "silver", 3)  # সিধুর তীর
        draw_line(pen, sk_arrow_x, -100, sk_arrow_x + 20, -100, "silver", 3)  # কানহুর তীর

        # ২. সাধারণ সৈন্যদের ফায়ার
        for rx, ry, rtype in active_rebels:
            cx = rx + 20 + ((350 - rx) / steps) * i
            cy = ry + 25
            if rtype == "santhal":
                draw_line(pen, cx, cy, cx + 15, cy, "silver", 2)
            else:
                draw_line(pen, cx, cy, cx + 10, cy, "orange", 3)

        # ৩. ব্রিটিশদের গুলি
        for bx, by in active_british:
            cx = bx - 20 - ((bx - (-350)) / steps) * i
            cy = by + 25
            draw_line(pen, cx, cy, cx - 15, cy, "yellow", 3)

        screen.update()
        time.sleep(duration / steps)
    pen.clear()


def play_animation(screen, anim_pen):
    # Phase 1: Background
    if os.path.exists("rebellion_bg.gif"):
        screen.bgpic("rebellion_bg.gif")
    else:
        screen.bgpic("nopic")
        screen.bgcolor("#3d1c04")

    anim_pen.clear()

    # Phase 1.5: সিধু-কানহুর ছবি যুক্ত করা
    if os.path.exists("sidhu_kanhu.gif"):
        screen.addshape("sidhu_kanhu.gif")
        sk_turtle = turtle.Turtle()
        sk_turtle.hideturtle()
        sk_turtle.speed(0)
        sk_turtle.penup()
        sk_turtle.goto(-330, -75)  # বাম পাশে লিডার হিসেবে পজিশন
        sk_turtle.shape("sidhu_kanhu.gif")
        sk_turtle.showturtle()

    # Coordinates for armies (shifted right slightly to make room for the image)
    rebel_coords = [(-250, -130), (-200, -130), (-150, -130), (-100, -130), (-50, -130),
                    (-230, -60), (-180, -60), (-130, -60), (-80, -60), (-30, -60)]
    rebel_types = ["santhal", "sepoy", "santhal", "sepoy", "santhal",
                   "sepoy", "santhal", "sepoy", "santhal", "sepoy"]

    british_coords = [(120, -130), (180, -130), (240, -130), (300, -130), (360, -130),
                      (150, -60), (210, -60), (270, -60), (330, -60), (390, -60)]

    rebel_dead = [False] * 10
    british_dead = [False] * 10

    # Draw initial static graphics
    draw_labels(anim_pen)

    army_pen = turtle.Turtle();
    army_pen.hideturtle();
    army_pen.speed(0)
    render_all_armies(army_pen, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead)
    screen.update()
    time.sleep(1)

    # Phase 2: 10+ Seconds Epic Battle Loop
    projectile_pen = turtle.Turtle();
    projectile_pen.hideturtle();
    projectile_pen.speed(0)

    volleys = [
        ([0], []),
        ([5], [0, 1]),
        ([], [2, 3, 5]),
        ([], [4, 6, 7]),
        ([], [8, 9])
    ]

    for b_deaths, r_deaths in volleys:
        active_rebels = [(rebel_coords[i][0], rebel_coords[i][1], rebel_types[i]) for i in range(10) if
                         not rebel_dead[i]]
        active_british = [(british_coords[i][0], british_coords[i][1]) for i in range(10) if not british_dead[i]]

        # Animate shooting
        animate_volley(screen, projectile_pen, active_rebels, active_british, duration=2.0)

        # Apply deaths
        for b_idx in b_deaths: british_dead[b_idx] = True
        for r_idx in r_deaths: rebel_dead[r_idx] = True

        render_all_armies(army_pen, rebel_coords, rebel_types, rebel_dead, british_coords, british_dead)
        screen.update()
        time.sleep(0.3)

    time.sleep(1)

    # Phase 3: Final Victory Screen
    anim_pen.penup();
    anim_pen.goto(0, 0);
    anim_pen.pendown()
    anim_pen.color("yellow")
    anim_pen.write("Rebellion Crushed - British Won", align="center", font=("Courier", 30, "bold"))
    screen.update()