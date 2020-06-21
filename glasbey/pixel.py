from PIL import Image, ImageDraw
import logging
from math import ceil, sqrt
from random import choices
from color_mind import ColorMind
import requests
from glasbey import Palette

SIZE = 10  # Suggest range 2 -> MAX 12

# COLORS = ColorMind.random_palette()
# COLORS = choices(COLORS, k=2 ** SIZE)

base = ColorMind.random_palette()
p = Palette()
p.load_base_palette(base)
COLORS = p.generate_palette(2 ** SIZE)
COLORS = p.convert_palette_to_rgb(COLORS)
print("LEN OF COLORS:", len(COLORS))

# COLORS = choices(COLORS, k=(2 ** SIZE) * 256)

BLOCK_SIZE = 100

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
im.save(f"PALETTE_{len(COLORS)}", "JPEG")
