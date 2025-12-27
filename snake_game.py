import turtle
import random
import time

# Game Variables
score = 0
delay = 0.1
game_over = False

# Screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.setup(width=600, height=600)
screen.bgcolor("#fdf0d5")

# Snake
class Snake(object):
    def __init__(self):
        self.segments = []
        self.direction = "right"
        self.movements = {
            "up": (0, 20),
            "down": (0, -20),
            "left": (-20, 0),
            "right": (20, 0)
        }
        
        screen.tracer(0)
        for i in range(4):
            body = self.new(i*20, 0)
            self.segments.insert(0, body)
        screen.update()

    def new(self, x, y):
        body = turtle.Turtle()
        body.shape("square")
        body.color("#4f772d")
        body.speed(0)
        body.penup()
        body.setpos(x, y)
        
        return body
    
    def head_pos(self):
        head = self.segments[0]
        return head.xcor(), head.ycor()
    
    def move(self, dont_grow):
        # Get current head position
        head_x, head_y = self.head_pos()

        # Calculate next head position
        dx, dy = self.movements[self.direction]
        next_x, next_y = head_x + dx, head_y + dy
        if next_x < -300 or next_x > 300 or next_y < -300 or next_y > 300:
            return True # Game over if out of bounds
        
        # Create new head 
        head = self.new(next_x, next_y)
        self.segments.insert(0, head)
        
        # Remove tail if not eating
        if dont_grow:
            tail = self.segments.pop()
            tail.hideturtle()

        return False

    def eat(self, food):
        food.move()

        self.move(False)

# Food
class Food(object):
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("#a4161a")
        self.food.speed(0)
        self.food.penup()

        self.move()

    def move(self):
        x, y = 20*random.randint(-14, 14), 20*random.randint(-14, 14)
        self.food.setpos(x, y)
    
    def food_pos(self):
        return self.food.xcor(), self.food.ycor()



# Keybinds & controls
def up():
    if snake.direction != "down":
        snake.direction = "up"

def down():
    if snake.direction != "up":
        snake.direction = "down"

def left():
    if snake.direction != "right":
        snake.direction = "left"

def right():
    if snake.direction != "left":
        snake.direction = "right"

screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.listen()

# Get snake and food positions
def get_pos(snake, food):
    sx, sy = snake.head_pos()
    fx, fy = food.food_pos()
    return sx, sy, fx, fy


snake = Snake()
food = Food()
while True: # Game loop
    screen.tracer(0)

    # Get snake head and food positions 
    head_x, head_y, food_x, food_y = get_pos(snake, food)

    # Check for food collision
    if head_x == food_x and head_y == food_y:
        snake.eat(food) # Eat and calls move()
        score += 1
    else:
        game_over = snake.move(True) # Move only, also checks for wall collsions

    # Update positions after moving
    head_x, head_y, food_x, food_y = get_pos(snake, food)
    
    # Check for self collision
    for i in range(1, len(snake.segments)):
        seg_x, seg_y = snake.segments[i].pos()
        if head_x == seg_x and head_y == seg_y:
            game_over = True

    if game_over:
        break

    screen.update()
    time.sleep(delay)

screen.mainloop()