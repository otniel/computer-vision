import matplotlib.pyplot as plt
import Image
import numpy as np

from masks.mask import Mask
from utils.tools import MAX_PIXEL_INTENSITY, MIN_PIXEL_INTENSITY
from utils.tools import grayscale_rgb_image, calculate_threshold, calculate_global_gradient
from filters.filter import MedianFilter
from math import sqrt

class BorderDetector:
    def __init__(self, image):
        self.image = self.preprocess_image(image)

    def preprocess_image(self, image):
        print "WARNING: Border detection may take SEVERAL minutes depending on the image resolution"
        image = grayscale_rgb_image(image)
        filter = MedianFilter(image)
        preprocessed_image = filter.apply_filter()
        return preprocessed_image

    def detect_borders(self):
        gradient_magnitudes = self.calculate_gradient_magnitudes()
        threshold = calculate_threshold(gradient_magnitudes)
        return self.draw_image_borders(gradient_magnitudes, threshold)

    def calculate_gradient_magnitudes(self):
        gradient = self.calculate_gradient()
        return np.array([pixel[1] for pixel in gradient])

    def calculate_gradient(self):
        print "Calculating gradient..."
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

    def draw_image_borders(self, magnitudes, threshold):
        bordered_detected_image = Image.new("L", self.image.size)
        bordered_pixels = bordered_detected_image.load()
        magnitude_index = 0
        for y in xrange(self.image.size[1]):
            for x in xrange(self.image.size[0]):
                if magnitudes[magnitude_index] < threshold:
                    bordered_pixels[x, y] = MIN_PIXEL_INTENSITY
                else:
                    bordered_pixels[x, y] = MAX_PIXEL_INTENSITY
                magnitude_index += 1
        return bordered_detected_image

if __name__ == '__main__':
    image = Image.open('../test-images/circulo.png')
    bt = BorderDetector(image)
    bordered_image = bt.detect_borders()
    bordered_image.save('../test-images/circulo-bordered.png')