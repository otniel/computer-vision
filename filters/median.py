__author__ = 'Otniel'

import Image
import sys

from utils.neighborhoods import BasePixelNeighborhood, CrossPixelNeighborhood, PlusPixelNeighborhood
from filter import BaseFilter

class MedianFilter(BaseFilter):
    def apply_filter(self):
        for x in xrange(self.image_width):
            for y in xrange(self.image_height):
                self.pixels[x, y] = self.calculate_median_pixel(x, y)
        self.image.save(self.image_output_name)

    def calculate_median_pixel(self, x, y):
        pixels = self.get_sorted_pixels(x, y)
        l = len(pixels)

        if l % 2 == 0:
            pixel_1, pixel_2 = pixels[l / 2 - 1], pixels[l / 2]
            return self.average_pixel(pixel_1, pixel_2)
        return pixels[l / 2]

    def get_sorted_pixels(self, x, y):
        neighbor_coordinates = self.neighborhood.get_neighbor_coordinates(x, y)
        pixels = [self.pixels[coordinate] for coordinate in neighbor_coordinates]
        return self.sort_pixels(pixels)

    def sort_pixels(self, pixels):
        return sorted(pixels, key=lambda pixel: pixel[0])

    def average_pixel(self, pixel_1, pixel_2):
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