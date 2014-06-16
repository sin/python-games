import simpleguitk as simplegui
import random

BORDER = 1
BLOCK = 30
WIDTH = 25
HEIGHT = 15
BLOCKS = WIDTH * HEIGHT
HALF_BLOCK = BLOCK / 2
BORDER_SIZE = BORDER * BLOCK
FRAME_WIDTH = WIDTH * BLOCK + BORDER * BLOCK * 2
FRAME_HEIGHT = HEIGHT * BLOCK + BORDER * BLOCK * 2
count = 0
score = 0
lenght = 1
last_score = 0
high_score = 0
blink = False

# initialize game
def init():
    global snake, score, direction
    global velocity, velocity_change
    snake = [[WIDTH // 2, HEIGHT // 2]]
    score = 0
    lenght = 1
    velocity = (1, 0)
    velocity_change = []
    direction = "right"
    move_timer.start()
    food_timer.start()
    new_food()

# game over function
def game_over():
    global last_score, high_score
    move_timer.stop()
    food_timer.stop()
    blink_timer.start()
    last_score = score
    if score > high_score:
        high_score = last_score


def new_food():
    food_timer.stop()
    food_timer.start()
    new_food_pos()

# new food position function
def new_food_pos():
    global food
    if len(snake) == BLOCKS - 1:
        game_over()
        pass
    food = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if food in snake:
        new_food_pos()

# move handler
def move_handler():
    global snake, velocity, velocity_change, score, lenght
    if len(velocity_change) > 0:
        velocity = velocity_change.pop(0)
    head = list(snake[0])
    head[0] = (head[0] + velocity[0]) % WIDTH
    head[1] = (head[1] + velocity[1]) % HEIGHT
    if head in snake:
        game_over()
        pass
    else:
        snake.insert(0, head)
    if head == food:
        score += 100
        lenght += 1
        new_food()
    else:
        snake.pop()

# food handler
def food_handler():
    global score
    score -= 25
    new_food_pos()

# blink handler
def blink_handler():
    global count, blink
    count += 1
    blink = True if blink == False else False
    if count > 10:
        count = 0
        blink = False
        blink_timer.stop()
        init()

# draw handler
def draw_handler(canvas):

    # draw board
    x = BORDER * BLOCK
    x2 = FRAME_WIDTH - BORDER * BLOCK
    y = FRAME_HEIGHT // 2
    canvas.draw_line((x, y), (x2, y), HEIGHT * BLOCK, "#FFF")

    # draw food
    x = BORDER_SIZE + food[0] * BLOCK
    y = BORDER_SIZE + food[1] * BLOCK + HALF_BLOCK
    canvas.draw_line((x, y), (x + BLOCK, y), BLOCK, "#F00")

    # draw snake
    color = "#F00" if blink == True else "#000"
    for point in snake:
        x = BORDER_SIZE + point[0] * BLOCK
        y = BORDER_SIZE + point[1] * BLOCK + HALF_BLOCK
        canvas.draw_line((x, y), (x + BLOCK, y), BLOCK, color)

    # draw grid
    for i in range(0, FRAME_WIDTH, BLOCK):
        canvas.draw_line((i, 0), (i, FRAME_HEIGHT), 0.3, "#999")
    for i in range(0, FRAME_HEIGHT, BLOCK):
        canvas.draw_line((0, i), (FRAME_WIDTH, i), 0.3, "#999")

    # update labels
    lenght_label.set_text("Lenght: " + str(lenght))
    score_label.set_text("Score: " + str(score))
    last_score_label.set_text("Last score: " + str(last_score))
    high_score_label.set_text("Highest score: " + str(high_score))

# keydown handler
def keydown_handler(key):
    global new_velocity, direction
    if key == simplegui.KEY_MAP["left"] and direction != "right":
        direction = "left"
        velocity_change.append([-1,0])
    if key == simplegui.KEY_MAP["right"] and direction != "left":
        direction = "right"
        velocity_change.append([1,0])
    if key == simplegui.KEY_MAP["up"] and direction != "down":
        direction = "up"
        velocity_change.append([0,-1])
    if key == simplegui.KEY_MAP["down"] and direction != "up":
        direction = "down"
        velocity_change.append([0,1])

# create frame
frame = simplegui.create_frame("Snake", FRAME_WIDTH, FRAME_HEIGHT, 150)
frame.set_canvas_background("#000")

# event handlers
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown_handler)
lenght_label = frame.add_label("Lenght: " + str(lenght))
score_label = frame.add_label("Score: " + str(score))
last_score_label = frame.add_label("Last score: " + str(last_score))
high_score_label = frame.add_label("Hightest score: " + str(high_score))
move_timer = simplegui.create_timer(150, move_handler)
food_timer = simplegui.create_timer(6000, food_handler)
blink_timer = simplegui.create_timer(100, blink_handler)

# start frame
frame.start()
init()