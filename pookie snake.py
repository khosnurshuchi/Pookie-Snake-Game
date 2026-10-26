
import turtle
import time
import random

# Pookie colors
pink = "#ff69b4"
light_pink = "#ffe4f1"
purple = "#c8a2e8"
dark_purple = "#8e4585"
white = "#ffffff"
mint = "#b8f2e6"

delay = 100

# Score
score = 0
high_score = 0
segments = []

# Screen
wn = turtle.Screen()
wn.title("🎀 Pookie Snake - The Ookiest Game Ever 🎀")
wn.bgcolor(light_pink)
wn.setup(width=700, height=700)
wn.tracer(0)

# Create a heart shape
heart_shape = (
    (0, -10), (-10, 0), (-15, 8), (-14, 15),
    (-8, 20), (0, 13), (8, 20), (14, 15),
    (15, 8), (10, 0)
)
wn.register_shape("pookie_heart", heart_shape)

# Decorations
decor = turtle.Turtle()
decor.hideturtle()
decor.speed(0)
decor.penup()

decor.goto(-300, 290)
decor.color(pink)
decor.write("♥  ♡  ✧  P O O K I E  S N A K E  ✧  ♡  ♥",
            align="center", font=("Arial", 19, "bold"))

decor.goto(-300, -310)
decor.write("♡ stay cute • eat strawberries • be iconic ♡",
            align="center", font=("Arial", 13, "bold"))

# Game border
border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.color(pink)
border.pensize(5)
border.penup()
border.goto(-280, -280)
border.pendown()

for i in range(4):
    border.forward(560)
    border.left(90)

border.penup()

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color(pink)
head.shapesize(1.15, 1.15)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake eyes
eye1 = turtle.Turtle()
eye1.speed(0)
eye1.shape("circle")
eye1.color("black")
eye1.shapesize(0.18)
eye1.penup()
eye1.hideturtle()

eye2 = turtle.Turtle()
eye2.speed(0)
eye2.shape("circle")
eye2.color("black")
eye2.shapesize(0.18)
eye2.penup()
eye2.hideturtle()

# Strawberry food
food = turtle.Turtle()
food.speed(0)
food.shape("pookie_heart")
food.color("#ff2f75")
food.penup()
food.goto(0, 100)

# Food sparkle
sparkle = turtle.Turtle()
sparkle.hideturtle()
sparkle.speed(0)
sparkle.penup()
sparkle.color("#e75480")

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()
pen.goto(0, 245)
pen.color(dark_purple)

def update_score():
    pen.clear()
    pen.write(
        "♡ Score: {}   |   Bestie Score: {} ♡".format(
            score, high_score
        ),
        align="center",
        font=("Arial", 15, "bold")
    )

update_score()

# Cute message
message = turtle.Turtle()
message.hideturtle()
message.speed(0)
message.penup()
message.color(dark_purple)
message.goto(0, -295)
message.write("YOU GOT THIS, POOKIE! ♡",
              align="center", font=("Arial", 11, "bold"))

# Direction functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)

    elif head.direction == "down":
        head.sety(head.ycor() - 20)

    elif head.direction == "left":
        head.setx(head.xcor() - 20)

    elif head.direction == "right":
        head.setx(head.xcor() + 20)

def update_eyes():
    x = head.xcor()
    y = head.ycor()

    if head.direction == "left":
        eye1.goto(x - 5, y + 4)
        eye2.goto(x - 5, y - 4)

    elif head.direction == "right":
        eye1.goto(x + 5, y + 4)
        eye2.goto(x + 5, y - 4)

    elif head.direction == "up":
        eye1.goto(x - 4, y + 5)
        eye2.goto(x + 4, y + 5)

    else:
        eye1.goto(x - 4, y + 5)
        eye2.goto(x + 4, y + 5)

    eye1.showturtle()
    eye2.showturtle()

def reset_game():
    global score, delay

    head.goto(0, 0)
    head.direction = "stop"

    eye1.hideturtle()
    eye2.hideturtle()

    for segment in segments:
        segment.hideturtle()

    segments.clear()

    score = 0
    delay = 100

    food.goto(
        random.randint(-13, 13) * 20,
        random.randint(-13, 13) * 20
    )

    update_score()

# Keyboard controls
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Optional WASD controls
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
def game_loop():
    global score, high_score, delay

    try:
        wn.update()

        # Border collision
        if (head.xcor() > 270 or head.xcor() < -270
                or head.ycor() > 270 or head.ycor() < -270):
            reset_game()

        # Move body segments
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        # Move snake
        move()
        update_eyes()

        # Eat the heart strawberry
        if head.distance(food) < 20:
            food.goto(
                random.randint(-13, 13) * 20,
                random.randint(-13, 13) * 20
            )

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color(
                random.choice([pink, purple, mint, "#ffb6c1"])
            )
            new_segment.shapesize(0.85, 0.85)
            new_segment.penup()
            segments.append(new_segment)

            score += 10
            high_score = max(score, high_score)
            delay = max(45, delay - 2)

            update_score()

        # Hit own body
        for segment in segments:
            if segment.distance(head) < 15:
                reset_game()
                break

        wn.update()
        wn.ontimer(game_loop, delay)

    except turtle.Terminator:
        pass

game_loop()
wn.mainloop()
