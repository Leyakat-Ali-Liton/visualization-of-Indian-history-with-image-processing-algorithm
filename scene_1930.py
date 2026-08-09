import turtle
import time
import os
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
FRAME_DELAY = 1 / FPS

COLORS = {
    "bg": "#0a0a0a",
    "text_main": "#ffffff",
    "text_highlight": "#ff4444",
    "gold": "#ffd700",
    "fire": ["#ffff00", "#ffaa00", "#ff0000", "#555555"],
    "tracer": ["#ffffff", "#ffffaa", "#ffdd88"]
}

IMG_CLUB = "pritilata_club_interior.gif"
IMG_STAND = "pritilata.gif"
IMG_CYANIDE = "pritilata_cyanide.gif"


def draw_line(t, x1, y1, x2, y2, color, thickness=2):
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


def draw_midpoint_circle(t, xc, yc, r, color, thickness=2):
    # Mid-Point circle drawing algorithm
    x = 0
    y = r
    p = 1 - r
    while x <= y:
        for px, py in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
            t.penup()
            t.goto(xc + px, yc + py)
            t.dot(thickness, color)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1


def draw_rectangle(t, x, y, width, height, color):
    # Basic shapes drawing using OpenGL/Turtle
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    if color:
        t.begin_fill()
    t.goto(x + width, y)
    t.goto(x + width, y + height)
    t.goto(x, y + height)
    t.goto(x, y)
    if color:
        t.end_fill()
    t.penup()


def translate_2d(x, y, tx, ty):
    # 2D Geometric transformation (Translation)
    return x + tx, y + ty


class TypewriterEngine:
    def __init__(self, t):
        self.t = t
        self.t.hideturtle()
        self.t.penup()

    def write_text(self, text, x, y, size=16, color="white", align="center", speed=0.03):
        self.t.goto(x, y)
        self.t.color(color)
        current_text = ""
        for char in text:
            current_text += char
            self.t.clear()
            self.t.write(current_text, align=align, font=("Courier", size, "bold"))
            turtle.update()
            time.sleep(speed)
        time.sleep(0.5)

    def clear(self):
        self.t.clear()


class ScreenTransition:
    def __init__(self, t):
        self.t = t
        self.t.hideturtle()
        self.t.speed(0)

    def wipe_right(self, color="black"):
        for x in range(-WIDTH // 2, WIDTH // 2 + 20, 20):
            draw_rectangle(self.t, x, -HEIGHT // 2, 20, HEIGHT, color)
            turtle.update()
            time.sleep(0.01)
        self.t.clear()


class Particle:
    def __init__(self, x, y, dx, dy, life, color, size):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self):
        self.x, self.y = translate_2d(self.x, self.y, self.dx, self.dy)
        self.dy -= 0.2
        self.life -= 1

    def draw(self, t):
        if self.life > 0:
            t.penup()
            t.goto(self.x, self.y)
            t.dot(self.size * (self.life / self.max_life), self.color)


class ParticleSystem:
    def __init__(self, t):
        self.t = t
        self.t.hideturtle()
        self.particles = []

    def add_explosion(self, x, y, count=20):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.randint(15, 30)
            color = random.choice(COLORS["fire"])
            size = random.randint(3, 8)
            self.particles.append(Particle(x, y, dx, dy, life, color, size))

    def update_and_draw(self):
        self.t.clear()
        active_particles = []
        for p in self.particles:
            p.update()
            p.draw(self.t)
            if p.life > 0:
                active_particles.append(p)
        self.particles = active_particles


class BulletTracer:
    def __init__(self, t):
        self.t = t
        self.t.hideturtle()
        self.tracers = []

    def add_tracer(self):
        start_x = random.randint(-WIDTH // 2, -WIDTH // 4)
        start_y = random.randint(-HEIGHT // 4, HEIGHT // 4)
        end_x = random.randint(WIDTH // 4, WIDTH // 2)
        end_y = random.randint(-HEIGHT // 4, HEIGHT // 4)
        color = random.choice(COLORS["tracer"])

        steps = 5
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        self.tracers.append({"x": start_x, "y": start_y, "dx": dx, "dy": dy, "steps": steps, "color": color})

    def update_and_draw(self):
        self.t.clear()
        active_tracers = []
        for tr in self.tracers:
            if tr["steps"] > 0:
                old_x, old_y = tr["x"], tr["y"]
                tr["x"], tr["y"] = translate_2d(tr["x"], tr["y"], tr["dx"], tr["dy"])
                draw_line(self.t, old_x, old_y, tr["x"], tr["y"], tr["color"], thickness=3)
                tr["steps"] -= 1
                active_tracers.append(tr)
        self.tracers = active_tracers


def scene_intro(screen, text_engine):
    screen.bgcolor(COLORS["bg"])
    screen.bgpic("nopic")
    turtle.update()

    text_engine.write_text("CHITTAGONG, BENGAL", 0, 50, size=24, speed=0.05)
    time.sleep(1)
    text_engine.write_text("September 23, 1932", 0, 0, size=18, color="gray", speed=0.05)
    time.sleep(1)
    text_engine.clear()

    text_engine.write_text("The Pahartali European Club bore a sign:", 0, 20, size=16)
    text_engine.write_text('"Dogs and Indians not allowed"', 0, -20, size=20, color=COLORS["text_highlight"],
                           speed=0.08)
    time.sleep(2)
    text_engine.clear()


def scene_attack(screen, text_engine, p_sys, b_sys, transition):
    transition.wipe_right()

    if os.path.exists(IMG_CLUB):
        screen.bgpic(IMG_CLUB)
    else:
        screen.bgcolor("#2c1b18")
        text_engine.write_text("[ Missing: pritilata_club_interior.gif ]", 0, 0)

    text_engine.write_text("Pritilata Waddedar leads a daring night raid...", 0, -250, size=16, color="white",
                           speed=0.02)

    for frame in range(120):
        if frame % 10 == 0:
            b_sys.add_tracer()
        if frame % 25 == 0:
            x = random.randint(-200, 200)
            y = random.randint(-100, 150)
            p_sys.add_explosion(x, y, count=30)
            draw_midpoint_circle(p_sys.t, x, y, random.randint(30, 60), "white", thickness=5)

        p_sys.update_and_draw()
        b_sys.update_and_draw()
        turtle.update()
        time.sleep(FRAME_DELAY)

    p_sys.t.clear()
    b_sys.t.clear()
    text_engine.clear()


def scene_the_stand(screen, text_engine, transition):
    transition.wipe_right()

    if os.path.exists(IMG_STAND):
        screen.bgpic(IMG_STAND)
    else:
        screen.bgcolor("#1a1a1a")
        text_engine.write_text("[ Missing: pritilata.gif ]", 0, 0)

    border = turtle.Turtle()
    border.hideturtle()
    border.speed(0)

    draw_line(border, -WIDTH // 2, -HEIGHT // 2, WIDTH // 2, -HEIGHT // 2, "black", 20)
    draw_line(border, WIDTH // 2, -HEIGHT // 2, WIDTH // 2, HEIGHT // 2, "black", 20)
    draw_line(border, WIDTH // 2, HEIGHT // 2, -WIDTH // 2, HEIGHT // 2, "black", 20)
    draw_line(border, -WIDTH // 2, HEIGHT // 2, -WIDTH // 2, -HEIGHT // 2, "black", 20)

    turtle.update()

    text_engine.write_text("The mission was successful.", 0, -220, size=18)
    time.sleep(1)
    text_engine.write_text("But Pritilata was critically wounded by a bullet.", 0, -260, size=16, color="#ffaaaa")
    time.sleep(3)
    text_engine.clear()


def scene_martyrdom(screen, text_engine, transition):
    transition.wipe_right("white")

    if os.path.exists(IMG_CYANIDE):
        screen.bgpic(IMG_CYANIDE)
    else:
        screen.bgcolor("black")
        text_engine.write_text("[ Missing: pritilata_cyanide.gif ]", 0, 0)

    ash = turtle.Turtle()
    ash.hideturtle()
    ash.speed(0)

    text_engine.write_text("To avoid capture and protect her comrades...", 0, 200, size=16, color="white")

    for _ in range(60):
        ash.clear()
        for _ in range(20):
            x = random.randint(-WIDTH // 2, WIDTH // 2)
            y = random.randint(-HEIGHT // 2, HEIGHT // 2)
            ash.penup()
            ash.goto(x, y)
            ash.color(random.choice(["#555555", "#888888", "#aaaaaa"]))
            ash.dot(random.randint(1, 3))
        turtle.update()
        time.sleep(0.05)

    text_engine.write_text("She chose the path of martyrdom.", 0, -220, size=22, color=COLORS["text_highlight"])
    text_engine.write_text("Swallowing cyanide, she became Bengal's first woman martyr.", 0, -260, size=14,
                           color="gray")

    time.sleep(4)


def scene_finale(screen, text_engine, transition):
    transition.wipe_right("black")
    screen.bgpic("nopic")
    screen.bgcolor("black")

    text_engine.write_text("Her sacrifice ignited a revolution.", 0, 0, size=20, color="white")
    time.sleep(2)
    text_engine.write_text("Pritilata Waddedar (1911 - 1932)", 0, -40, size=16, color=COLORS["gold"])

    time.sleep(2)


def play_animation(screen, anim_pen):
    text_engine = TypewriterEngine(anim_pen)
    transition = ScreenTransition(anim_pen)

    pt = turtle.Turtle()
    pt.hideturtle()

    bt = turtle.Turtle()
    bt.hideturtle()

    p_sys = ParticleSystem(pt)
    b_sys = BulletTracer(bt)

    scene_intro(screen, text_engine)
    scene_attack(screen, text_engine, p_sys, b_sys, transition)
    scene_the_stand(screen, text_engine, transition)
    scene_martyrdom(screen, text_engine, transition)
    scene_finale(screen, text_engine, transition)

    pt.clear()
    bt.clear()


if __name__ == "__main__":
    sc = turtle.Screen()
    sc.title("Pritilata Waddedar - The Pahartali Raid (1932)")
    sc.setup(width=WIDTH, height=HEIGHT)
    sc.tracer(0)

    p = turtle.Turtle()
    p.hideturtle()

    play_animation(sc, p)
    turtle.done()