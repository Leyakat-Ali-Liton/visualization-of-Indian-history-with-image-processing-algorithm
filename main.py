import time
import turtle
import scene_1602
import scene_1757
import scene_1855
import scene_1930
import scene_1947
import scene_1952
import scene_7_March_1971
import scene_16_December_1971
import scene_2024


class SceneInterrupt(Exception):
    pass


original_sleep = time.sleep


def stoppable_sleep(secs):
    if getattr(turtle, "_interrupt_scene", False):
        raise SceneInterrupt("Scene Interrupted")
    original_sleep(secs)


time.sleep = stoppable_sleep


# =========================================================

class ChroniclesOfBengal:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Chronicles of Bengal - Interactive History Map")
        self.screen.setup(width=900, height=600)
        self.screen.bgcolor("#1a1a1a")
        self.screen.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

        self.anim_pen = turtle.Turtle()
        self.anim_pen.hideturtle()
        self.anim_pen.speed(0)

        self.is_transitioning = False
        self.pending_render = False
        turtle._interrupt_scene = False

        # --- একদম সঠিক self.events লিস্ট (মিসিং ডাটাগুলো ফিক্স করা হয়েছে) ---
        self.events = [
            {"year": "", "title": "",
             "desc": "Trade ships arrive at the shores of Bengal."},
            {"year": "1757", "title": "Battle of Plassey",
             "desc": "Fall of Nawab Siraj-ud-Daulah, start of British rule."},
            {"year": "1855-1857", "title": "Santhal Rebellion & Sepoy Mutiny",
             "desc": "Early sparks of resistance and tribal uprisings."},
            {"year": "1930s", "title": "Anti-British Resistance",
             "desc": "Surya Sen, Pritilata, Khudiram fight for freedom."},
            {"year": "1947", "title": "Partition of India",
             "desc": "Bengal is divided. End of British colonial rule."},
            {"year": "1952", "title": "Language Movement",
             "desc": "Ekushey February. Martyrs sacrifice lives for Bengali."},
            {"year": "1971 (March 7)", "title": "Bangabandhu's Historic Speech",
             "desc": "The call for independence at Race Course Maidan."},
            {"year": "", "title": "",
             "desc": "Liberation War victory. A new nation is born."},
            {"year": "", "title": "",
             "desc": "Student-led mass movement shaping the future."}
        ]

        # Scene handlers
        self.scene_modules = {
            0: scene_1602.play_animation,
            1: scene_1757.play_animation,
            2: scene_1855.play_animation,
            3: scene_1930.play_animation,
            4: scene_1947.play_animation_1947,
            5: scene_1952.play_animation_1952,
            6: scene_7_March_1971.play_animation,
            7: scene_16_December_1971.play_animation,
            8: scene_2024.play_animation,
        }

        self.current_idx = 0
        self.bind_controls()

        # Initial Render without a transition wipe
        self.render(first_load=True)

    def draw_midpoint_circle(self, x_center, y_center, radius, color):
        self.pen.penup()
        self.pen.goto(x_center, y_center - radius)
        self.pen.pendown()
        self.pen.color(color)
        self.pen.begin_fill()
        self.pen.circle(radius)
        self.pen.end_fill()

    def draw_timeline_line(self):
        self.pen.penup()
        self.pen.goto(-400, -250)
        self.pen.pendown()
        self.pen.pensize(3)
        self.pen.color("#555555")
        self.pen.goto(400, -250)

        step = 800 / (len(self.events) - 1)
        for i in range(len(self.events)):
            x = -400 + (i * step)
            color = "#00ffcc" if i == self.current_idx else "#ffffff"
            radius = 10 if i == self.current_idx else 5
            self.draw_midpoint_circle(x, -250, radius, color)

    def play_cinematic_wipe(self):
        """Draws a smooth curtain-wipe across the screen to transition scenes."""
        wipe_pen = turtle.Turtle()
        wipe_pen.hideturtle()
        wipe_pen.speed(0)
        wipe_pen.color("#111111")

        for x in range(-450, 451, 60):
            wipe_pen.clear()
            wipe_pen.penup()
            wipe_pen.goto(-450, -300)
            wipe_pen.pendown()
            wipe_pen.begin_fill()
            wipe_pen.goto(x, -300)
            wipe_pen.goto(x, 300)
            wipe_pen.goto(-450, 300)
            wipe_pen.goto(-450, -300)
            wipe_pen.end_fill()
            self.screen.update()
            time.sleep(0.01)

        wipe_pen.clear()

    def request_transition(self, direction):
        """Prepares the system to abort the current scene and transition."""
        if self.is_transitioning or self.pending_render:
            return

        new_idx = self.current_idx + direction
        if 0 <= new_idx < len(self.events):
            self.current_idx = new_idx
            self.pending_render = True

            # 1. Neutralize old turtles INSTANTLY to freeze the screen
            for t in self.screen.turtles():
                if t not in (self.pen, self.anim_pen):
                    t.goto = lambda *args, **kwargs: None
                    t.dot = lambda *args, **kwargs: None
                    t.write = lambda *args, **kwargs: None
                    t.circle = lambda *args, **kwargs: None
                    t.pendown = lambda *args, **kwargs: None
                    t.begin_fill = lambda *args, **kwargs: None
                    t.end_fill = lambda *args, **kwargs: None

            # 2. Trigger the kill switch for the active scene loop
            turtle._interrupt_scene = True

            # 3. Schedule the new scene to start slightly after the old one is killed
            self.screen.ontimer(self.render_deferred, 100)

    def render_deferred(self):
        """Executes the render once the old scene has been successfully interrupted."""
        turtle._interrupt_scene = False
        self.pending_render = False
        self.render(first_load=False)

    def render(self, first_load=False):
        self.is_transitioning = True

        if not first_load:
            self.play_cinematic_wipe()

        # Clean the board entirely behind the "curtain"
        for t in self.screen.turtles():
            if t != self.pen:
                t.clear()
                t.hideturtle()

        # Hard reset the background
        try:
            self.screen.bgpic("nopic")
        except:
            pass
        self.screen.bgcolor("#1a1a1a")
        self.pen.clear()

        # Spawn a brand new pen for the new scene
        self.anim_pen = turtle.Turtle()
        self.anim_pen.hideturtle()
        self.anim_pen.speed(0)

        # --- Draw the Base UI (নতুন আই-ক্যাচিং ড্রপ-শ্যাডো ডিজাইন) ---
        evt = self.events[self.current_idx]

        # Year Text (With Black Drop Shadow)
        self.pen.penup()
        self.pen.goto(2, 218)  # Shadow offset
        self.pen.color("black")
        self.pen.write(evt.get("year", ""), align="center", font=("Georgia", 38, "bold"))

        self.pen.goto(0, 220)
        self.pen.color("#FFD700")  # Golden color for year
        self.pen.write(evt.get("year", ""), align="center", font=("Georgia", 38, "bold"))

        # Title Text (With Black Drop Shadow)
        self.pen.goto(2, 178)  # Shadow offset
        self.pen.color("black")
        self.pen.write(evt.get("title", ""), align="center", font=("Georgia", 22, "bold"))

        self.pen.goto(0, 180)
        self.pen.color("#FFFFFF")  # White color for Title
        self.pen.write(evt.get("title", ""), align="center", font=("Georgia", 22, "bold"))

        # Footer instructions
        self.pen.goto(0, -280)
        self.pen.color("#777777")
        self.pen.write("Press ENTER/RIGHT to advance | Press BACKSPACE/LEFT to go back", align="center",
                       font=("Arial", 11, "italic"))

        self.draw_timeline_line()
        self.screen.update()

        self.is_transitioning = False

        # Run the scene safely
        if self.current_idx in self.scene_modules:
            try:
                self.scene_modules[self.current_idx](self.screen, self.anim_pen)
            except SceneInterrupt:
                pass

    def next_event(self):
        self.request_transition(1)

    def prev_event(self):
        self.request_transition(-1)

    def bind_controls(self):
        self.screen.listen()
        self.screen.onkey(self.next_event, "Return")
        self.screen.onkey(self.next_event, "Right")
        self.screen.onkey(self.prev_event, "BackSpace")
        self.screen.onkey(self.prev_event, "Left")


if __name__ == "__main__":
    app = ChroniclesOfBengal()
    turtle.done()