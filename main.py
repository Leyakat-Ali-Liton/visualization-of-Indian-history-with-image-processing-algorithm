import turtle
import scene_1602
import scene_1757
import scene_1855
import scene_1930
import scene_1947
import scene_1952


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

        self.events = [
            {"year": "1600-1602", "title": "Arrival of British East India Company",
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
            {"year": "1971 (Dec 16)", "title": "Birth of Bangladesh",
             "desc": "Liberation War victory. A new nation is born."},
            {"year": "1990", "title": "Anti-Autocracy Uprising",
             "desc": "Fall of autocratic regime, restoration of democracy."},
            {"year": "2024", "title": "July Mass Uprising",
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
        }
        self.current_idx = 0

        self.bind_controls()
        self.render()

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

    def render(self):
        # 1. Stop all previous animations by neutralizing old turtles
        for t in self.screen.turtles():
            if t != self.pen:
                t.clear()
                t.hideturtle()
                # Override drawing methods so background loops do nothing
                t.goto = lambda *args, **kwargs: None
                t.dot = lambda *args, **kwargs: None
                t.write = lambda *args, **kwargs: None
                t.circle = lambda *args, **kwargs: None
                t.pendown = lambda *args, **kwargs: None
                t.begin_fill = lambda *args, **kwargs: None
                t.end_fill = lambda *args, **kwargs: None

        self.pen.clear()

        # 2. Spawn a brand new pen for the new scene
        self.anim_pen = turtle.Turtle()
        self.anim_pen.hideturtle()
        self.anim_pen.speed(0)

        evt = self.events[self.current_idx]

        self.pen.penup()
        self.pen.goto(0, 220)
        self.pen.color("#ff4444")
        self.pen.write(evt["year"], align="center", font=("Courier", 36, "bold"))

        self.pen.goto(0, 180)
        self.pen.color("#00ffcc")
        self.pen.write(evt["title"], align="center", font=("Arial", 20, "bold"))

        self.pen.goto(0, -280)
        self.pen.color("#777777")
        self.pen.write("Press ENTER/RIGHT to advance | Press BACKSPACE/LEFT to go back", align="center",
                       font=("Arial", 11, "italic"))

        self.draw_timeline_line()
        self.screen.update()

        if self.current_idx in self.scene_modules:
            self.scene_modules[self.current_idx](self.screen, self.anim_pen)

    def next_event(self):
        if self.current_idx < len(self.events) - 1:
            self.current_idx += 1
            self.render()

    def prev_event(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.render()

    def bind_controls(self):
        self.screen.listen()
        self.screen.onkey(self.next_event, "Return")
        self.screen.onkey(self.next_event, "Right")

        self.screen.onkey(self.prev_event, "BackSpace")
        self.screen.onkey(self.prev_event, "Left")


if __name__ == "__main__":
    app = ChroniclesOfBengal()
    turtle.done()