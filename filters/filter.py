__author__ = 'Otniel'

import Image
import sys
import numpy as np

from abc import ABCMeta, abstractmethod
from utils.neighborhoods import BasePixelNeighborhood, CrossPixelNeighborhood, PlusPixelNeighborhood

class BaseFilter:
    __metaclass__ = ABCMeta
    def __init__(self, image, type):
        self.image = image
        self.image_width = image.size[0]
        self.image_height = image.size[1]
        self.pixels = image.load()

        if type == '1':
            self.neighborhood = CrossPixelNeighborhood(self.pixels, self.image.size)
        elif type == '2':
            self.neighborhood = PlusPixelNeighborhood(self.pixels, self.image.size)
        else:
            self.neighborhood = BasePixelNeighborhood(self.pixels, self.image.size)

    def apply_filter(self):
        filtered_image = Image.new(self.image.mode, self.image.size)
        filtered_pixels = filtered_image.load()
        for x in xrange(self.image_width):
            for y in xrange(self.image_height):
                filtered_pixels[x, y] = self.calculate_filtered_pixel(x, y)
        return filtered_image

    @abstractmethod
    def calculate_filtered_pixel(self, x, y):
        pass

class MinFilter(BaseFilter):
    def calculate_filtered_pixel(self, x, y):
        neighbor_coordinates = self.neighborhood.get_neighbor_coordinates(x, y)
        pixels = [self.pixels[coordinate] for coordinate in neighbor_coordinates]
        return np.min(pixels)

class MaxFilter(BaseFilter):
    def calculate_filtered_pixel(self, x, y):
        neighbor_coordinates = self.neighborhood.get_neighbor_coordinates(x, y)
        pixels = [self.pixels[coordinate] for coordinate in neighbor_coordinates]
        return np.max(pixels)

class MedianFilter(BaseFilter):
    def calculate_filtered_pixel(self, x, y):
        neighbor_coordinates = self.neighborhood.get_neighbor_coordinates(x, y)
        pixels = [self.pixels[coordinate] for coordinate in neighbor_coordinates]
        return np.median(pixels)

image = Image.open('/home/otniel/Documents/repos/computer-vision/filters/grayscale_mason.png')
filter = MaxFilter(image, 0)
image = filter.apply_filter()
image.save('max_mason.png')