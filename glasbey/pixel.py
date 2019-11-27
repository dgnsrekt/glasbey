from PIL import Image, ImageDraw
import logging
from math import ceil, sqrt
from random import choices
from color_mind import ColorMind
import requests

SIZE = 8  # Suggest range 2 -> MAX 12

COLORS = ColorMind.random_palette()
COLORS = choices(COLORS, k=2 ** SIZE)

BLOCK_SIZE = 25

HEIGHT, WIDTH = BLOCK_SIZE * ceil(sqrt(len(COLORS))), BLOCK_SIZE * ceil(sqrt(len(COLORS)))


def to_coordinate(coordinate):
    return coordinate * BLOCK_SIZE


def draw_block(context, x, y, color):
    x = to_coordinate(x)
    y = to_coordinate(y)

    location = (x, y, x + BLOCK_SIZE, y + BLOCK_SIZE)

    context.rectangle(location, fill=f"rgb{str(color)}")


im = Image.new("RGB", (HEIGHT, WIDTH), "grey")

draw_context = ImageDraw.Draw(im, "RGB")

matrix = ceil(sqrt(len(COLORS)))

idx = 0
for y in range(matrix):
    for x in range(matrix):
        if idx < len(COLORS):
            draw_block(draw_context, x, y, COLORS[idx])
        idx += 1


im.show()
