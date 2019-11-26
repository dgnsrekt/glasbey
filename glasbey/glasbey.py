# encoding: utf-8

import csv
import numpy as np
from colorspacious import cspace_converter, cspace_convert
from webcolors import rgb_to_hex, hex_to_rgb, IntegerRGB
from static import MAX_COLOR_RANGE, MAX_RGB255_COLORS
from path import CAM02_UCS_LUT_PATH
from path import Path

from progressbar import ProgressBar, Percentage, Bar, ETA

MAX_RANGE = 256


def timeit(f):
    def timed(*args, **kw):
        import time

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print("function time {} : {} sec".format(f.__name__, te - ts))
        return result

    return timed


class ColorTable:
    def __init__(self):
        if CAM02_UCS_LUT_PATH.exists():
            self.colors = self.load_color_table()
        else:
            self.colors = self.generate_color_table()
            self.save_color_table(self.colors)

        # add some self.color validation maybe len of table/ size of file

    def load_color_table(self):
        return np.load(CAM02_UCS_LUT_PATH)["lut"]

    def save_color_table(self, color_table):
        np.savez_compressed(CAM02_UCS_LUT_PATH, lut=color_table)

    def generate_color_table(self):
        """ Generates a lookup table with all possible RGB colors, encoded in a perceptually
        uniform CAM02-UCS color space.  Table rows correspond to individual RGB colors.
        Table columns correspond to J', a', and b' components.
        :return: LUT as Numpy array
        """

        i = 0

        widgets = ["Generating color table: ", Percentage(), " ", Bar(), " ", ETA()]
        bar = ProgressBar(widgets=widgets, maxval=(MAX_RANGE ** 2)).start()

        colors = np.empty(shape=(MAX_RGB255_COLORS, 3), dtype=float)
        converter = cspace_converter("sRGB255", "CAM02-UCS")

        for red in range(MAX_RANGE):
            for green in range(MAX_RANGE):
                distance = i * MAX_RANGE
                for blue in range(MAX_RANGE):
                    colors[distance + blue, :] = (red, green, blue)
                colors[distance : distance + MAX_RANGE] = converter(
                    colors[distance : distance + MAX_RANGE]
                )
                i += 1
                bar.update(i)

        return colors

    @property
    def shape(self):
        return self.colors.shape

    def __getitem__(self, lut_index):
        return self.colors[lut_index]


def sRGB255_to_lut_index(sRGB_value):
    red, green, blue = sRGB_value
    return (red * MAX_RANGE + green) * MAX_RANGE + blue


class Palette:
    def __init__(self):
        self.palette = []

    @staticmethod
    def update_distances(colors, color, distances):
        distance = np.linalg.norm((colors - color), axis=1)
        return np.minimum(distances, distance.reshape(distances.shape))

    def generate_palette(self, palette_size):  # colortable needed here

        color_table = ColorTable()
        converter = cspace_converter("CAM02-UCS", "sRGB1")

        if len(self.palette) < 1:
            self.palette = [color_table[-1, :]]

        if palette_size <= len(self.palette):
            return converter(self.palette[0:palette_size])

        number_of_colors = color_table.shape[0]
        distances = np.ones(shape=(number_of_colors, 1)) * 1000

        for i in range(len(self.palette) - 1):
            print("d", end="", flush=True)
            distances = self.update_distances(color_table.colors, self.palette[i], distances)

        while len(self.palette) < palette_size:
            print("p", end="", flush=True)
            distances = self.update_distances(color_table.colors, self.palette[-1], distances)
            self.palette.append(color_table[np.argmax(distances), :])

        return converter(self.palette[0:palette_size])

    def load_base_palette(self, base_palette):
        color_table = ColorTable()
        self.palette = [color_table[sRGB255_to_lut_index(rgb), :] for rgb in base_palette]

    def load_hex_palette_file(self, path):
        path = Path(path)
        assert path.exists()

        base_palette = []
        with open(path, "r") as palette_read_file:
            for color in palette_read_file.readline():
                rgb_color = hex_to_rgb(color)
                base_palette.append(rgb_color)

        if len(base_palette) > 0:
            self.load_base_palette(base_palette)

    def save_hex_palette_file(self, path, overwrite=False):
        hex_palette = self.get_hex_palette()

        if overwrite is False:
            assert path.exists() is False #TODO: correct execption

        with open(path, "w") as palette_write_file:
            for color in hex_palette:
                palette_write_file.write(color)

    def load_rgb_palette_file(self, path):
        path = Path(path)
        assert path.exists()

        base_palette = []
        with open(path, "r") as palette_read_file:
            for color in palette_read_file.readline():
                rgb_color = hex_to_rgb(color)
                base_palette.append(rgb_color)

        if len(base_palette) > 0:
            self.load_base_palette(base_palette)

    def get_hex_palette(self):
        hex_palette = []

        assert len(self) > 1 #TODO: Correct execption.
        for color in self.palette:
            hex_color = rgb_to_hex(color)
            hex_palette.append(hex_color)
        return hex_palette

    def __len__(self):
        return len(self.palette)


def main():
    lut = ColorTable()
    base_palette = [(0, 22, 244), (22, 33, 223), (200, 255, 66)]
    for p in base_palette:
        h = rgb_to_hex(p)
        print("hex:", h)
        r = hex_to_rgb(h)
        print("rgb:", r)

    exit()
    p = Palette(lut)
    # p.generate_palette(5)
    # print(p.palette)
    # p.load_base_palette(base_palette)
    # print(p.palette)
    p.load_palette_file("palette.txt")
    print(p.palette)
    x = p.generate_palette(256)
    print()
    print(x)

    # x = [(rgb[0] * 256 + rgb[1]) * 256 + rgb[2] for rgb in base_palette]
    # x = [lut.convert_sRGB255_to_lut_index(rgb) for rgb in base_palette]
    # print(x)
    # print(lut[base_palette[0], :])
