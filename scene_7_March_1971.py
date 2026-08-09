import turtle
import time
import random
import math


def draw_line_dda(t, x1, y1, x2, y2, color, thickness=1):
    # DDA line drawing algorithm (Optimized for smoother animation)
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

    # Turtle-এ দ্রুত রেন্ডারিংয়ের জন্য একটু বড় স্টেপে পিক্সেল প্লট করা হলো
    step_jump = 2 if steps > 40 else 1
    for _ in range(0, steps, step_jump):
        x += x_inc * step_jump
        y += y_inc * step_jump
        t.goto(x, y)
    t.pensize(1)
    t.penup()


def draw_midpoint_circle(t, xc, yc, r, color):
    # Mid-Point circle drawing algorithm (Used for microphones to satisfy algorithm requirement)
    x = 0
    y = r
    p = 1 - r
    t.color(color)
    t.penup()
    while x <= y:
        for px, py in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
            t.goto(xc + px, yc + py)
            t.dot(2, color)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1


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


def translate_rotate_2d(x, y, length, angle_deg):
    # 2D Geometric transformation (Translation & Rotation)
    rad = math.radians(angle_deg)
    return x + length * math.cos(rad), y + length * math.sin(rad)


def draw_crowd(pen):
    # Massive performance fix: Using simple dots for background to prevent lag during transition
    pen.speed(0)
    for y in range(-300, -80, 15):
        for _ in range(40):
            x = random.randint(-450, 450)
            body_color = random.choice(["#2b2b2b", "#363636", "#424242", "#1a1a1a"])
            pen.penup()
            pen.goto(x, y - 8)
            pen.pendown()
            pen.dot(18, body_color)
            pen.penup()
            pen.goto(x, y)
            pen.pendown()
            pen.dot(10, "#111111")


def draw_stage(pen):
    stage_points = [(-450, -150), (450, -150), (450, -300), (-450, -300)]
    draw_polygon(pen, stage_points, "#3b2f2f")

    podium_points = [(-100, -150), (40, -150), (40, 50), (-100, 50)]
    draw_polygon(pen, podium_points, "#5c5c5c")

    mics = [(-80, 50), (-50, 60), (-20, 50), (10, 40)]
    for mx, my in mics:
        draw_line_dda(pen, mx, 50, mx, my, "#111", 4)
        draw_midpoint_circle(pen, mx, my, 7, "silver")


def draw_bangabandhu_static(pen):
    pen.speed(0)

    legs_points = [(-230, -150), (-190, -150), (-180, -80), (-240, -80)]
    draw_polygon(pen, legs_points, "#eeeeee")

    punjabi_lower = [(-260, -80), (-160, -80), (-150, -10), (-270, -10)]
    draw_polygon(pen, punjabi_lower, "white")

    coat_points = [(-250, -10), (-150, -10), (-130, 60), (-170, 75), (-230, 60)]
    draw_polygon(pen, coat_points, "black")

    collar_points = [(-170, 75), (-155, 70), (-150, 85), (-170, 85)]
    draw_polygon(pen, collar_points, "white")

    pen.penup()
    pen.goto(-160, 105)
    pen.pendown()
    pen.dot(70, "#1a1a1a")

    g1_x, g1_y = translate_rotate_2d(-135, 115, 25, 10)
    draw_line_dda(pen, -135, 115, g1_x, g1_y, "black", 4)

    g2_x, g2_y = translate_rotate_2d(-130, 112, 15, 10)
    draw_line_dda(pen, -130, 112, g2_x, g2_y, "white", 2)


def play_animation(screen, anim_pen):
    screen.bgcolor("#e0d2b4")
    anim_pen.clear()

    draw_crowd(anim_pen)
    draw_stage(anim_pen)
    draw_bangabandhu_static(anim_pen)
    screen.update()

    arm_pen = turtle.Turtle()
    arm_pen.hideturtle()
    arm_pen.speed(0)

    text_pen = turtle.Turtle()
    text_pen.hideturtle()

    font_style = ("Helvetica", 28, "bold")

    text_pen.penup()
    text_pen.goto(142, 118)
    text_pen.color("#888888")
    text_pen.write('"এবারের সংগ্রাম...', font=font_style)

    text_pen.goto(140, 120)
    text_pen.color("#8B0000")
    text_pen.write('"এবারের সংগ্রাম...', font=font_style)

    shoulder_x, shoulder_y = -140, 50
    # স্মুথ মুভমেন্টের জন্য ছোট ছোট অ্যাঙ্গেল স্টেপ
    smooth_angles_1 = [35, 40, 45, 50, 55, 60, 65, 70, 65, 60, 55, 50, 45, 40]

    for _ in range(3):
        for angle in smooth_angles_1:
            arm_pen.clear()

            p1_x, p1_y = shoulder_x, shoulder_y
            p2_x, p2_y = translate_rotate_2d(p1_x, p1_y, 85, angle)
            p3_x, p3_y = translate_rotate_2d(p2_x, p2_y, 15, angle)
            p4_x, p4_y = translate_rotate_2d(p3_x, p3_y, 25, angle)

            draw_line_dda(arm_pen, p1_x, p1_y, p2_x, p2_y, "white", 22)
            draw_line_dda(arm_pen, p2_x, p2_y, p3_x, p3_y, "#1a1a1a", 24)
            draw_line_dda(arm_pen, p3_x, p3_y, p4_x, p4_y, "#1a1a1a", 6)

            screen.update()
            time.sleep(0.015)  # ডিলে কমিয়ে অ্যানিমেশন ফাস্ট করা হয়েছে

    time.sleep(0.3)

    text_pen.penup()
    text_pen.goto(142, 58)
    text_pen.color("#888888")
    text_pen.write('আমাদের মুক্তির সংগ্রাম!"', font=font_style)

    text_pen.goto(140, 60)
    text_pen.color("#8B0000")
    text_pen.write('আমাদের মুক্তির সংগ্রাম!"', font=font_style)

    smooth_angles_2 = [45, 50, 55, 60, 65, 70, 65, 60, 55, 50]

    for _ in range(4):
        for angle in smooth_angles_2:
            arm_pen.clear()

            p1_x, p1_y = shoulder_x, shoulder_y
            p2_x, p2_y = translate_rotate_2d(p1_x, p1_y, 85, angle)
            p3_x, p3_y = translate_rotate_2d(p2_x, p2_y, 15, angle)
            p4_x, p4_y = translate_rotate_2d(p3_x, p3_y, 25, angle)

            draw_line_dda(arm_pen, p1_x, p1_y, p2_x, p2_y, "white", 22)
            draw_line_dda(arm_pen, p2_x, p2_y, p3_x, p3_y, "#1a1a1a", 24)
            draw_line_dda(arm_pen, p3_x, p3_y, p4_x, p4_y, "#1a1a1a", 6)

            screen.update()
            time.sleep(0.012)

    time.sleep(1.0)


if __name__ == "__main__":
    sc = turtle.Screen()
    sc.setup(width=900, height=600)
    sc.tracer(0)
    p = turtle.Turtle()
    p.hideturtle()
    play_animation(sc, p)
    turtle.done()
