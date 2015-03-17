from PIL import Image, ImageDraw
from collections import Counter
from math import sqrt
from homeworks.border_detection import BorderDetector
from utils.tools import get_image_diagonal_distance, is_border_pixel, plot_data, calculate_threshold

import math
import numpy as np


def get_bordered_image(image):
    border_detector = BorderDetector(image)
    border_detector.detect_borders()
    return border_detector.draw_image_borders()


class CircleDetector:
    def __init__(self, image):
        self.MAX_RADIUS = get_image_diagonal_distance(image)
        self.image = get_bordered_image(image)
        self.accumulator = []

    def detect_circles(self):
        pixels = self.image.load()
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                if is_border_pixel(pixels[x, y]):
                    self.make_vote(x, y)

        votes = self.get_best_votes()
        frequents = np.array([vote[1] for vote in votes])
        threshold = calculate_threshold(frequents)
        centers = []
        drawer = ImageDraw.Draw(self.image)
        for vote in votes:
            if vote[1] > threshold:
                x_center, y_center, radius = vote[0]
                drawer.ellipse((x_center - 1, y_center - 1, x_center + 1, y_center + 1), fill = 'blue', outline ='blue')
                centers.append(vote[0])
        print "EJEMPLO VOTO", votes[2][0]
        self.image.show()
        print "Cantidad de centros: %d" % len(centers)
        return self.accumulator, votes

    def make_vote(self, x, y):
        for x_center in range(20, 200, 10):
            for y_center in range(20, 200, 10):
                candidate_radius = math.floor(sqrt((x - x_center) ** 2 + (y - y_center) ** 2))
                print "Making vote for (%d, %d)..." % (x, y)
                vote = x_center, y_center, candidate_radius
                self.accumulator.append(vote)

    def get_best_votes(self):
        counter = Counter(self.accumulator)
        commons = counter.most_common(270)
        best_votes = np.array([common[0] for common in commons])
        return commons

    def draw_lined_image(self):
        lined_image = Image.new("RGB", self.image.size, "white")
        lined_pixels = lined_image.load()
        for pixel in self.border_pixels:
            lined_pixels[pixel] = (255, 255, 255)
        for pixel in self.line_pixels:
            lined_pixels[pixel] = (255, 0, 0)
        return lined_image


image = Image.open('../test-images/circulo.png')
image = image.convert("RGB")
cd = CircleDetector(image)
accumulator, votes = cd.detect_circles()
print "Imprimiendo votos"
print "Listo"
plot_data(accumulator)
