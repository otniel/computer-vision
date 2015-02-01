__author__ = 'Otniel'

import Image
import sys

from abc import ABCMeta, abstractmethod
from utils.neighborhoods import BasePixelNeighborhood, CrossPixelNeighborhood, PlusPixelNeighborhood

class BaseFilter:
    def __init__(self, image_name, type='0'):
        self.image = Image.open(image_name)
        self.image_width = self.image.size[0]
        self.image_height = self.image.size[1]
        self.pixels = self.image.load()

        if type == '1':
            self.neighborhood = CrossPixelNeighborhood(self.image_width, self.image_height)
            self.image_output_name = "cross_neighborhood_out.jpg"
        elif type == '2':
            self.neighborhood = PlusPixelNeighborhood(self.image_width, self.image_height)
            self.image_output_name = "plus_neighborhood_out.jpg"
        else:
            self.neighborhood = BasePixelNeighborhood(self.image_width, self.image_height)
            self.image_output_name = "_out.jpg"

    @abstractmethod
    def apply_filter(self):
        pass

    def average_from_two_pixels(self, pixel_1, pixel_2):
        return tuple([(x+y)/2 for(x,y) in zip(pixel_1, pixel_2)])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage -> ./median.py FILENAME"
        print "Optional argument TYPE: 0 = normal neighborhood, 1 = cross neighborhood, 2 = plus neighborhood (default 0)"
        print "Example: ./median.py mason.jpg 1"
        print
        exit()

    image_name = sys.argv[1]

    mf = MedianFilter(image_name)
    mf.apply_filter()