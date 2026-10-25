import turtle
import time
delay = 0.1

#Screen
wn = turtle.Screen()
wn.title("Pookie Snake")
wn.bgcolor('light pink')
wn.setup(width=600, height=600)
wn.tracer(0)


# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape('square')
head.color('black')
head.penup()
head.goto(0,0)
head.direction = 'right'

# function
def go_up():
	head.direction == 'up'
def go_down():
	head.direction == 'down'
def go_left():
	head.direction == 'left'
def go_right():
	head.direction == 'right'

def move():
	if head.direction == 'up':
		y = head.ycor()
		head.sety(y+20)
	if head.direction == 'down':
		y = head.ycor()
		head.sety(y-20)
	if head.direction == 'Left':
		x = head.xcor()
		head.setx(x-20)
	if head.direction == 'Right':
		x = head.xcor()
		head.setx(x+20)


# keyboard bindings
wn.listen()
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')

# main game loop
while True:
	wn.update()	
	move()

	time.sleep(delay)

wn.mainloop()
