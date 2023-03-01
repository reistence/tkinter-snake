"""Small Tkinter beginner project - Snake Game"""
from tkinter import *
from tkinter import ttk
import random
import sys
import os

root = Tk()
root.title("Tkinter - Snake")
# root.geometry('300x500+1200+40')
root.resizable(0, 0)
root.iconbitmap("./pyt.ico")
root.attributes("-alpha", 0.95)


score = 0
direction = "down"

GAME_WIDTH = 700
GAME_HEIGTH = 700
SPEED = 180
SPACE_SIZE = 50
BODY_PARTS = 2
SNAKE_COLOR = "red"
FOOD_COLOR = "green"
BG_COLOR = "black"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGTH/SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y +
                           SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        root.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGTH:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=("Rubik", 50), text="GAME OVER", fill="red", tag="gameover")
    return True


def restart():
    global canvas, snake, food, direction, score

    # reset score and direction
    score = 0
    direction = "down"
    label.config(text="Score: {}".format(score))

    # delete gameover text if it exists
    canvas.delete("gameover")

    # delete all snake squares and food
    for square in snake.squares:
        canvas.delete(square)
    canvas.delete("food")

    # create a new snake and food
    snake = Snake()
    food = Food()

    # start the game again
    next_turn(snake, food)


label = Label(root, text="Score: {}".format(score), font=("Rubik", 30))
label.pack()
angainBtn = Button(root, text="Restart",
                   command=restart)
angainBtn.pack()

canvas = Canvas(root, bg=BG_COLOR, height=GAME_HEIGTH, width=GAME_WIDTH)
canvas.pack()


root.update()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_heigth = root.winfo_screenheight()

x = int((screen_width/2) - (root_width/2))
y = int((screen_heigth/2) - (root_height/2))

root.geometry(f"{root_width}x{root_height}+{x}+{y}")

root.bind("<Left>", lambda event: change_direction("left"))
root.bind("<Right>", lambda event: change_direction("right"))
root.bind("<Up>", lambda event: change_direction("up"))
root.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

root.mainloop()
