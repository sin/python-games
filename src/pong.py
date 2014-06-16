import simpleguitk as simplegui
import random

WIDTH = 640
HEIGHT = 440
BORDER = 20
LINE_WIDTH = 8
BALL_RADIUS = LINE_WIDTH / 2
PAD_WIDTH = LINE_WIDTH
PAD_HEIGHT = 80
PAD_SPEED = 5
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
MIN_PAD_POS = HALF_PAD_HEIGHT + LINE_WIDTH + BORDER
MAX_PAD_POS = HEIGHT - HALF_PAD_HEIGHT - LINE_WIDTH - BORDER
MIN_BALL_V_POS = BORDER + LINE_WIDTH
MAX_BALL_V_POS = HEIGHT - BORDER - LINE_WIDTH
MIN_BALL_H_POS = BORDER + PAD_WIDTH + BALL_RADIUS
MAX_BALL_H_POS = WIDTH - BORDER - PAD_WIDTH - BALL_RADIUS

# spaws ball
def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(2, 5), -random.randrange(1, 4)]
    if right == False:
        ball_vel[0] = -ball_vel[0]

# starts new game
def new_game():
    global pad1_pos, pad2_pos, pad1_vel, pad2_vel
    global score1, score2
    pad1_pos = pad2_pos = HEIGHT / 2
    pad1_vel, pad2_vel = 0, 0
    score1, score2 = 0, 0
    ball_init(random.choice([True, False]))

# draw handler
def draw(c):
    global score1, score2, pad1_pos, pad2_pos, ball_pos, ball_vel

    # left pad position
    if (pad1_pos + pad1_vel < MIN_PAD_POS):
        pad1_pos = MIN_PAD_POS
    elif (pad1_pos + pad1_vel > MAX_PAD_POS):
        pad1_pos = MAX_PAD_POS
    else:
        pad1_pos += pad1_vel

    # right pad position
    if (pad2_pos + pad2_vel < MIN_PAD_POS):
        pad2_pos = MIN_PAD_POS
    elif (pad2_pos + pad2_vel > MAX_PAD_POS):
        pad2_pos = MAX_PAD_POS
    else:
        pad2_pos += pad2_vel

    # ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # top and bottom walls ball collisions
    if (ball_pos[1] <= MIN_BALL_V_POS or ball_pos[1] >= MAX_BALL_V_POS):
        ball_vel[1] = -ball_vel[1]

    # left wall ball collisions
    if (ball_pos[0] <= MIN_BALL_H_POS):
        min_collision_pos = pad1_pos - HALF_PAD_HEIGHT - BALL_RADIUS
        max_collision_pos = pad1_pos + HALF_PAD_HEIGHT + BALL_RADIUS
        if (ball_pos[1] > min_collision_pos and ball_pos[1] < max_collision_pos):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.08
        else:
            score2 += 1
            ball_init(True)

    # right wall ball collisions
    if (ball_pos[0] >= MAX_BALL_H_POS):
        min_collision_pos = pad2_pos - HALF_PAD_HEIGHT - BALL_RADIUS
        max_collision_pos = pad2_pos + HALF_PAD_HEIGHT + BALL_RADIUS
        if (ball_pos[1] > min_collision_pos and ball_pos[1] < max_collision_pos):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.08
        else:
            score1 += 1
            ball_init(False)

    # vertical line
    c.draw_line([WIDTH / 2, BORDER], [WIDTH / 2, HEIGHT - BORDER], LINE_WIDTH, "White")
    c.draw_line([WIDTH / 2, BORDER + 30], [WIDTH / 2, BORDER + 50], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 70], [WIDTH / 2, BORDER + 90], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 110], [WIDTH / 2, BORDER + 130], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 150], [WIDTH / 2, BORDER + 170], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 190], [WIDTH / 2, BORDER + 210], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 230], [WIDTH / 2, BORDER + 250], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 270], [WIDTH / 2, BORDER + 290], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 310], [WIDTH / 2, BORDER + 330], LINE_WIDTH, "Black")
    c.draw_line([WIDTH / 2, BORDER + 350], [WIDTH / 2, BORDER + 370], LINE_WIDTH, "Black")

    # top line
    top_line_left = [BORDER, BORDER + LINE_WIDTH / 2]
    top_line_right = [WIDTH - BORDER , BORDER + LINE_WIDTH / 2]
    c.draw_line(top_line_left, top_line_right, LINE_WIDTH, "White")

    # bottom line
    bottom_line_left = [BORDER, HEIGHT - BORDER - LINE_WIDTH / 2]
    bottom_line_right = [WIDTH - BORDER , HEIGHT - BORDER - LINE_WIDTH / 2]
    c.draw_line(bottom_line_left, bottom_line_right, LINE_WIDTH, "White")

    # left pad
    pad1_top = [BORDER + PAD_WIDTH / 2, pad1_pos - HALF_PAD_HEIGHT]
    pad1_bottom = [BORDER + PAD_WIDTH / 2, pad1_pos + HALF_PAD_HEIGHT]
    c.draw_line(pad1_top, pad1_bottom, 8, "White")

    # right pad
    pad2_top = [WIDTH - BORDER - PAD_WIDTH / 2, pad2_pos - HALF_PAD_HEIGHT]
    pad2_bottom = (WIDTH - BORDER - PAD_WIDTH / 2, pad2_pos + HALF_PAD_HEIGHT)
    c.draw_line(pad2_top, pad2_bottom, 8, "White")

    # ball
    c.draw_line((ball_pos[0] - 4, ball_pos[1]), (ball_pos[0] + 4, ball_pos[1]), 8, "White")

    # scores
    c.draw_text(str(score1), [(WIDTH / 8 * 3 - 20), 120], 70, "White", "sans-serif")
    c.draw_text(str(score2), [(WIDTH / 8 * 5 - 20), 120], 70, "White", "sans-serif")

# event handlers
def keydown(key):
    global pad1_vel, pad2_vel
    if key == simplegui.KEY_MAP["w"]:
        pad1_vel = -PAD_SPEED
    if key == simplegui.KEY_MAP["s"]:
        pad1_vel = PAD_SPEED
    if key == simplegui.KEY_MAP["up"]:
        pad2_vel = -PAD_SPEED
    if key == simplegui.KEY_MAP["down"]:
        pad2_vel = PAD_SPEED

def keyup(key):
    global pad1_vel, pad2_vel
    if key == simplegui.KEY_MAP["w"] and pad1_vel == -PAD_SPEED:
        pad1_vel = 0
    if key == simplegui.KEY_MAP["s"] and pad1_vel == PAD_SPEED:
        pad1_vel = 0
    if key == simplegui.KEY_MAP["up"] and pad2_vel == -PAD_SPEED:
        pad2_vel = 0
    if key == simplegui.KEY_MAP["down"] and pad2_vel == PAD_SPEED:
        pad2_vel = 0

# creates frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT, 130)
frame.add_button("Reset", new_game, 130)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# starts frame
frame.start()
new_game()