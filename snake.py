import turtle
import time
from random import *

DELAY = 0.15
WIDTH = 800
HEIGHT = 600
SPEED = 20

window = turtle.Screen()
window.title("snake")
window.bgcolor("black")
window.setup(WIDTH, HEIGHT)
window.tracer(0) #stop window from updating

def setupKeyListener(window):
    window.listen()
    window.onkeypress(headS.move_up, "Up")
    window.onkeypress(headS.move_down, "Down")
    window.onkeypress(headS.move_left, "Left")
    window.onkeypress(headS.move_right, "Right")

# Snake
class Snake():
    def __init__(self, head = None, direction = None):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("white")
        self.head.setposition(0,0)
        self.head.penup()
        self.direction = "down"
    
    def xcor(self):
        return self.head.xcor()
    def ycor(self):
        return self.head.ycor()
    def setposition(self, x, y):
        self.head.setposition(x, y)
    def move_up(self):
        self.direction = "up"
    def move_down(self):
        self.direction = "down"
    def move_left(self):
        self.direction = "left"
    def move_right(self):
        self.direction = "right"

    def move(self):
        if self.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + SPEED)
        if self.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - SPEED)
        if self.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - SPEED)
        if self.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + SPEED)

headS = Snake()
tailS = headS
snake = []
snake.append(headS)
setupKeyListener(window)

def resetGame():
    global snake, headS, tailS
    for s in snake:
        s.head.reset()
    snake.clear()
    headS = Snake()
    headS.setposition(0,0)
    tailS = headS
    snake.append(headS)
    setupKeyListener(window)

# End of Snake

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.speed(0)
food.setposition(randrange(-WIDTH/2+20, WIDTH/2-20, 20), randrange(-HEIGHT/2+20, HEIGHT/2-20, 20))

def randomFood():
    x = randrange(-WIDTH/2+20, WIDTH/2-20, 20)
    y = randrange(-HEIGHT/2+20, HEIGHT/2-20, 20)
    flag = spaceAvailable(x,y)
    while flag == False:
        x = randrange(-WIDTH/2+20, WIDTH/2-20, 20)
        y = randrange(-HEIGHT/2+20, HEIGHT/2-20, 20)
        flag = spaceAvailable(x, y)
    return (x, y)
        
def spaceAvailable(x, y):
    for s in snake:
        if (x == s.head.xcor() and y == s.head.ycor()):
            return False
    return True

def eaten():
    global tailS, snake
    food.setposition(randomFood())
    
    #increase snake length
    newSnake = Snake()

    # if tail of snake is going:
    # 'up', new tail is added to the bottom, 'down' -> added on top
    # 'left' -> added right side, 'right' -> added left side
    if(tailS.direction == "up"):
        newSnake.head.setposition(tailS.head.xcor(), tailS.head.ycor()-20)
    elif (tailS.direction == "down"):
        newSnake.head.setposition(tailS.head.xcor(), tailS.head.ycor()+20)
    elif (tailS.direction == "right"):
        newSnake.head.setposition(tailS.head.xcor()-20, tailS.head.ycor())
    elif (tailS.direction == "left"):
        newSnake.head.setposition(tailS.head.xcor()+20, tailS.head.ycor())

    newSnake.direction = tailS.direction
    tailS = newSnake
    snake.append(newSnake)
# End of Food

def moveSnake():
    global snake, headS
    for s in snake:
        s.move()
        if(headS.xcor() == WIDTH/2 or headS.xcor() == -WIDTH/2 or headS.ycor() == HEIGHT/2 or headS.ycor() == -HEIGHT/2):
            resetGame()
            break
        if(s is not headS and (headS.xcor() == s.head.xcor() and headS.ycor() == s.head.ycor())):
            resetGame()
            break

def updateSnakeDirection():
    global snake, headS
    hDir = headS.direction
    i = 1
    while i < len(snake):
        tmp = snake[i].direction
        snake[i].direction = hDir
        hDir = tmp
        i+=1
    
while True:
    window.update()
    time.sleep(DELAY)

    moveSnake()
    updateSnakeDirection()

    # snake eats food
    if(snake[0].head.xcor() == food.xcor() and snake[0].head.ycor() == food.ycor()):
        eaten()
        print(len(snake))
