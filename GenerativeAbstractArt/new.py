import math

from PIL import Image, ImageDraw
import random as rand
import torch

canvas_height = 2000
canvas_width = 5000

bg = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(bg)

lines = []
rectangles = []


def draw_base_lines():
    num_lines = 40

    for i in range(num_lines):
        # Center point
        y_center_point_dist = torch.distributions.Normal(canvas_height // 2, 250)
        y_center_point_line = y_center_point_dist.sample()

        # Line length
        line_len_dist = rand.uniform(5, 800)

        # Start point (bottom)
        y_start_point_line = y_center_point_line + line_len_dist // 2

        # End point (top)
        y_end_point_line = y_start_point_line - line_len_dist

        # X position
        x_start_point = rand.uniform(20, canvas_width - 20)

        # Print info
        # print(f"Line starts at {int(y_start_point_line)}")
        # print(f"Line ends at {int(y_end_point_line)}")
        # print(f"Line length: {int(line_len_dist)}")

        # Append line coordinates to list
        lines.append((x_start_point, y_start_point_line, y_end_point_line))

        # Add a rectangle or circle to line
        shape = 'rectangle' if rand.choice([0, 1]) == 1 else 'circle'
        if shape == 'rectangle':
            draw_rect(x_start_point, y_start_point_line, y_end_point_line)
        elif shape == 'circle':
            draw_circle(x_start_point, y_start_point_line, y_end_point_line)

        draw.line([(x_start_point, y_start_point_line), (x_start_point, y_end_point_line)], fill='black')

    bg.show()


def draw_rect(line_x, line_start, line_end):
    line_length = line_start - line_end

    # Rectangle width
    rect_width_dist = torch.distributions.Normal(50, 25)
    rect_width = math.fabs(int(rect_width_dist.sample()))

    # Rectangle height
    rect_height_dist = torch.distributions.Normal(line_length // 4, 10)
    rect_height = math.fabs(int(rect_height_dist.sample()))

    flip = True if rand.choice([0, 1]) == 1 else False
    bottom = True if rand.choice([0, 1]) == 1 else False

    # Flip rectangle if necessary
    if flip:
        tl_x = line_x - rect_width
        br_x = line_x
    else:
        tl_x = line_x
        br_x = line_x + rect_width

    # Place rectangle at bottom if necessary
    if bottom:
        tl_y = line_start
        br_y = line_start + rect_height
    else:
        tl_y = line_end
        br_y = line_end + rect_height

    # Print info:
    print(f"Top left: x = {int(tl_x)} | y = {int(tl_y)}")
    print(f"Bottom right: x = {int(br_x)} | y = {int(br_y)}")

    rectangles.append((tl_x, tl_y, br_x, br_y))

    draw.rectangle([(tl_x, tl_y), (br_x, br_y)], fill='black')


def draw_circle(line_x, line_start, line_end):
    radius_dist = torch.distributions.Normal(50, 25)
    radius = math.fabs(int(radius_dist.sample()))

    flip = True if rand.choice([0, 1]) == 1 else False
    bottom = True if rand.choice([0, 1]) == 1 else False

    # Flip circle if necessary
    if flip:
        tl_x = line_x - radius
        br_x = line_x
    else:
        tl_x = line_x
        br_x = line_x + radius

    # Place circle at bottom if necessary
    if bottom:
        tl_y = line_start - radius // 2
        br_y = line_start + radius // 2
    else:
        tl_y = line_end - radius // 2
        br_y = line_end + radius // 2

    # Bounding box
    bbox = [tl_x, tl_y, br_x, br_y]

    # Fill color
    fill_color = 'black' if rand.choice([0, 1]) == 1 else 'white'

    draw.ellipse(bbox, outline='black', fill=fill_color)


draw_base_lines()
