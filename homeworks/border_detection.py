import matplotlib.pyplot as plt
import Image
import numpy as np

from masks.mask import Mask
from utils.neighborhoods import BaseNeighborhood
from utils.gradients import Gradients
from utils.tools import MAX_PIXEL_INTENSITY, MIN_PIXEL_INTENSITY
from utils.tools import grayscale_rgb_image, calculate_threshold, calculate_global_gradient
from filters.filter import MedianFilter
from math import sqrt, atan2, pi, cos, sin, ceil

class BorderDetector:
    def __init__(self, image):
        self.image = self.preprocess_image(image)
        self.neighborhood = BaseNeighborhood(image.size)
        self.border_pixels = []
        self.angles = []
        self.coordinates_rhos_and_theta = []
        self.rho_and_angle = []
    def preprocess_image(self, image):
        image = grayscale_rgb_image(image)
        filter = MedianFilter(image)
        preprocessed_image = filter.apply_filter()
        return preprocessed_image

    def detect_borders(self):
        gradient_magnitudes = self.calculate_gradient_magnitudes()
        threshold = calculate_threshold(gradient_magnitudes)
        magnitude_index = 0
        for y in xrange(self.image.size[1]):
            for x in xrange(self.image.size[0]):
                if gradient_magnitudes[magnitude_index] > threshold:
                    self.border_pixels.append((x, y))
                    angle = atan2(y, x)
                    self.angles.append(np.rad2deg(angle))
                    rho = x * cos(angle) + y * sin(angle)
                    self.rho_and_angle.append((ceil(rho), ceil(angle)))
                    self.coordinates_rhos_and_theta.append([(x, y), (ceil(rho), ceil(angle))])
                magnitude_index += 1

    def calculate_gradient_magnitudes(self):
        gradient = self.calculate_gradient()
        return np.array([pixel for pixel in gradient])

    def calculate_gradient(self):
        horizontal_gradient = self.calculate_horizontal_gradient()
        vertical_gradient = self.calculate_vertical_gradient()
        return calculate_global_gradient(horizontal_gradient, vertical_gradient)

    def calculate_horizontal_gradient(self):
        horizoontal_mask = Mask(self.image, '../masks/sobel_horizontal.txt')
        horizoontal_mask.apply_mask()
        return horizoontal_mask.get_gradient_list()

    def calculate_vertical_gradient(self):
        vertical_mask = Mask(self.image, '../masks/sobel_vertical.txt')
        vertical_mask.apply_mask()
        return vertical_mask.get_gradient_list()

    def draw_image_borders(self):
        bordered_detected_image = Image.new("L", self.image.size)
        bordered_pixels = bordered_detected_image.load()
        for pixel in self.border_pixels:
            bordered_pixels[pixel] = MAX_PIXEL_INTENSITY
        return bordered_detected_image

if __name__ == '__main__':
    image = Image.open('../test-images/squares.png')
    image = image.convert('RGB')
    bt = BorderDetector(image)
    bt.detect_borders()
    bordered_image = bt.draw_image_borders()
    bordered_image.show()
    # bordered_image.save('../test-images/circulo-bordered.png')