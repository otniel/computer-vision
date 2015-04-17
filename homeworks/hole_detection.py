import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from utils.tools import normalize_rgb_image, normalize_grayscale_image
from utils.detect_peaks import detect_peaks


class HoleDetection:
    def __init__(self, image):
        self.image = normalize_rgb_image(image)
        self.pixels = self.image.load()
        self.width, self.height = self.image.size

    def smooth_list(self, the_list, width):
        smoothed_list = []
        for index, value in enumerate(the_list):
            window = the_list[max(0, index-1):min(index+width, len(the_list))]
            new_value = int(sum(window) / len(window))
            smoothed_list.append(new_value)
        return smoothed_list

    def detect_holes(self):
        horizontal_histogram = self.get_horizontal_histogram()
        vertical_histogram = self.get_vertical_histogram()

        smoothed_horizontal = self.smooth_list(horizontal_histogram, 5)
        smoothed_horizontal = self.smooth_list(smoothed_horizontal, 5)
        smoothed_horizontal = self.smooth_list(smoothed_horizontal, 5)

        smoothed_vertical = self.smooth_list(vertical_histogram, 5)
        smoothed_vertical = self.smooth_list(smoothed_vertical, 5)
        smoothed_vertical = self.smooth_list(smoothed_vertical, 5)

        horizontal_candidates = (np.gradient(np.sign(np.gradient(np.array(smoothed_horizontal)))) > 0).nonzero()[0]
        vertical_candidates = (np.gradient(np.sign(np.gradient(np.array(smoothed_vertical)))) > 0).nonzero()[0]

        # Drawing candidates
        for y in xrange(self.height):
            for x in horizontal_candidates:
                self.pixels[x, y] = (255, 0, 0)
        for x in xrange(self.width):
            for y in vertical_candidates:
                self.pixels[x, y] = (0, 0, 255)

        self.image.save('../test-images/holes_intersection.png')

    def get_horizontal_histogram(self):
        horizontal_histogram = []
        for x in range(self.width):
            total_row = 0
            for y in range(self.height):
                total_row += self.pixels[x, y][0]
            horizontal_histogram.append(total_row / self.height)
        return horizontal_histogram

    def get_vertical_histogram(self):
        vertical_histogram = []
        for y in range(self.height):
            total_column = 0
            for x in range(self.width):
                total_column += self.pixels[x, y][0]
            vertical_histogram.append(total_column / self.width)
        return vertical_histogram

image = Image.open('../test-images/holes.png')
hd = HoleDetection(image)
hd.detect_holes()