import turtle
import time
import os
import math


# --- Basic Shape Functions ---
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


# --- Force Drawings ---
def draw_labels(t):
    """স্ক্রিনের দুই পাশে পক্ষের নাম লেখা"""
    t.penup();
    t.goto(-220, 150);
    t.pendown()
    t.color("#00ffcc")
    t.write("Nawab Siraj-ud-Daulah's Forces", align="center", font=("Arial", 16, "bold"))

    t.penup();
    t.goto(220, 150);
    t.pendown()
    t.color("#ff4444")
    t.write("British East India Company", align="center", font=("Arial", 16, "bold"))
    t.color("black")


def draw_bengali_forces(t):
    """বাঙালি সৈন্য, হাতি এবং একটি কামান"""
    # হাতির শরীর
    draw_rectangle(t, -350, -90, 90, 60, "#696969")
    draw_circle(t, -260, -60, 35, "#696969")  # মাথা
    draw_polygon(t, [(-225, -60), (-210, -60), (-220, -120), (-235, -120), (-240, -80)], "#696969")  # শুঁড়
    draw_polygon(t, [(-230, -70), (-190, -85), (-225, -90)], "white")  # দাঁত
    draw_circle(t, -280, -50, 25, "#555555")  # কান
    draw_rectangle(t, -340, -130, 20, 40, "#696969")  # পা
    draw_rectangle(t, -280, -130, 20, 40, "#696969")

    # নবাবের একটি কামান
    t.penup();
    t.goto(-170, -80);
    t.pendown()
    t.fillcolor("#4A2311");
    t.begin_fill()
    t.goto(-100, -60);
    t.goto(-100, -40);
    t.goto(-170, -60)
    t.end_fill()
    draw_circle(t, -150, -80, 20, "#5C3A21")


def draw_british_forces(t):
    """ব্রিটিশ কামান এবং রিয়েলিস্টিক ইংরেজ সৈন্য (Redcoat)"""
    # কামান (Cannon)
    t.penup();
    t.goto(250, -90);
    t.pendown()
    t.fillcolor("#333333");
    t.begin_fill()
    t.goto(160, -70);
    t.goto(160, -50);
    t.goto(250, -70)
    t.end_fill()
    draw_circle(t, 230, -90, 25, "#5C3A21")  # চাকা
    draw_circle(t, 230, -90, 10, "black")

    # ইংরেজ সৈন্য (Redcoat)
    draw_rectangle(t, 270, -90, 22, 50, "red")  # লাল কোট
    # বুকের সাদা ক্রস বেল্ট
    t.pensize(2);
    t.color("white")
    t.penup();
    t.goto(270, -40);
    t.pendown();
    t.goto(292, -90)
    t.penup();
    t.goto(292, -40);
    t.pendown();
    t.goto(270, -90)
    t.pensize(1);
    t.color("black")

    # মাথা এবং ব্রিটিশ ত্রিকোণ টুপি (Tricorn Hat)
    draw_circle(t, 281, -30, 12, "#FFDAB9")
    draw_polygon(t, [(260, -18), (302, -18), (281, 0)], "black")

    # বন্দুক (Musket) তাক করা
    draw_polygon(t, [(270, -55), (170, -55), (170, -60), (270, -60)], "#4A2311")


def draw_nawab(t, is_dead=False):
    """নবাবের স্ট্যান্ডিং এবং ফলিং (পতন) মোশন - উন্নত পোশাক সহ"""
    t.clear()
    if not is_dead:
        # নবাব দাঁড়িয়ে আছেন
        draw_rectangle(t, -60, -90, 26, 55, "#FFD700")  # গোল্ডেন রাজকীয় পোশাক
        draw_rectangle(t, -65, -90, 8, 55, "purple")  # কাঁধের রাজকীয় শাল
        draw_circle(t, -47, -25, 14, "#FFDAB9")  # মাথা

        # নবাবের বড় পাগড়ি ও মণি
        draw_polygon(t, [(-65, -15), (-29, -15), (-47, 5)], "darkgreen")
        draw_circle(t, -47, -5, 4, "red")  # পাগড়ির মণি

        # তলোয়ার হাতে
        t.pensize(3);
        t.color("silver")
        t.penup();
        t.goto(-40, -60);
        t.pendown();
        t.goto(-10, -20)
        t.pensize(1);
        t.color("black")
    else:
        # নবাব মাটিতে পড়ে গেছেন (Rotation and Translation effect)
        draw_rectangle(t, -100, -120, 55, 26, "#FFD700")  # বডি
        draw_rectangle(t, -100, -125, 55, 8, "purple")  # শাল
        draw_circle(t, -35, -107, 14, "#FFDAB9")  # মাথা
        draw_polygon(t, [(-25, -120), (-25, -84), (-5, -107)], "darkgreen")  # পড়ে যাওয়া পাগড়ি

        # রক্তের পতন (Blood effect)
        draw_circle(t, -55, -120, 15, "red")
        draw_circle(t, -70, -115, 10, "darkred")
        draw_circle(t, -40, -125, 8, "red")


def animate_projectile(screen, pen, p_type, start_x, start_y, end_x, end_y, color, duration):
    """ল্যাব রিকয়ারমেন্ট: Translation & Parabolic Motion Simulation"""
    pen.clear()
    pen.color(color)
    steps = 20
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps

    for i in range(steps):
        pen.clear()
        x = start_x + dx * i
        y = start_y + dy * i

        if p_type == "cannon":
            # Parabolic Arc for Cannonball
            arc = math.sin(math.pi * (i / steps)) * 40
            draw_circle(pen, x, y + arc, 6, color)
        elif p_type == "arrow":
            # Linear Line for Arrow
            pen.penup();
            pen.goto(x, y);
            pen.pendown()
            pen.pensize(2)
            pen.goto(x + (20 if dx > 0 else -20), y + (dy / dx) * 20 if dx != 0 else y)
            pen.pensize(1)
        else:  # musket bullet
            pen.penup();
            pen.goto(x, y);
            pen.pendown()
            pen.pensize(4)
            pen.goto(x + (15 if dx > 0 else -15), y)
            pen.pensize(1)

        screen.update()
        time.sleep(duration / steps)
    pen.clear()


def play_animation(screen, anim_pen):
    # ফেজ ১: ম্যাপ জুম ইফেক্ট
    if os.path.exists("colored_map.gif"):
        screen.bgpic("colored_map.gif")
    elif os.path.exists("map.gif"):
        screen.bgpic("map.gif")

    anim_pen.clear()
    target_x, target_y = 150, -20
    anim_pen.pensize(3);
    anim_pen.color("red")
    for scale in range(1, 6):
        anim_pen.clear()
        draw_rectangle(anim_pen, target_x - scale * 10, target_y - scale * 10, scale * 20, scale * 20, "")
        screen.update()
        time.sleep(0.1)

    time.sleep(0.5)
    anim_pen.clear()

    # ফেজ ২: পলাশীর মাঠের ব্যাকগ্রাউন্ড ও সৈন্য স্থাপন
    if os.path.exists("plassey_bg.gif"):
        screen.bgpic("plassey_bg.gif")
    else:
        screen.bgpic("nopic");
        screen.bgcolor("#8B0000")

    draw_labels(anim_pen)
    draw_bengali_forces(anim_pen)
    draw_british_forces(anim_pen)

    nawab_pen = turtle.Turtle();
    nawab_pen.hideturtle();
    nawab_pen.speed(0)
    draw_nawab(nawab_pen, is_dead=False)
    screen.update()
    time.sleep(1)

    # ফেজ ৩: ১০ সেকেন্ডের দীর্ঘ যুদ্ধ (Looping Projectiles)
    projectile_pen = turtle.Turtle();
    projectile_pen.hideturtle();
    projectile_pen.speed(0)

    # ৩ বার গোলাগুলি বিনিময় হবে (প্রায় ৯-১০ সেকেন্ড)
    for _ in range(3):
        # ১. নবাবের পক্ষ থেকে কামান ফায়ার
        animate_projectile(screen, projectile_pen, "cannon", -100, -50, 200, -80, "black", 0.7)
        # ২. ব্রিটিশদের কামান ফায়ার
        animate_projectile(screen, projectile_pen, "cannon", 160, -60, -150, -80, "#333333", 0.7)
        # ৩. নবাবের পক্ষ থেকে তীরের বৃষ্টি
        animate_projectile(screen, projectile_pen, "arrow", -100, -30, 250, -40, "silver", 0.5)
        animate_projectile(screen, projectile_pen, "arrow", -80, -10, 270, -20, "silver", 0.5)
        # ৪. ব্রিটিশ বন্দুকের ফায়ার
        animate_projectile(screen, projectile_pen, "bullet", 170, -55, -20, -55, "yellow", 0.5)

        time.sleep(0.2)

    # ফেজ ৪: চূড়ান্ত আঘাত এবং নবাবের পতন
    # ব্রিটিশ বন্দুক থেকে ফাইনাল ফায়ার
    draw_circle(projectile_pen, 170, -55, 15, "orange")  # Muzzle Flash
    screen.update();
    time.sleep(0.1);
    projectile_pen.clear()

    # গুলি নবাবের বুকে লাগছে
    animate_projectile(screen, projectile_pen, "bullet", 170, -55, -45, -55, "yellow", 0.5)

    # নবাবের পতন
    draw_nawab(nawab_pen, is_dead=True)
    screen.update()