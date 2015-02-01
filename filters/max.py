__author__ = 'Otniel'

import Image
import sys

from utils.neighborhoods import BasePixelNeighborhood, CrossPixelNeighborhood, PlusPixelNeighborhood
from filter import BaseFilter

class MaxFilter(BaseFilter):
    def apply_filter(self):
        for x in xrange(self.image_width):
            for y in xrange(self.image_height):
                self.pixels[x, y] = self.calculate_max_pixel(x, y)
        # self.image.save(self.image_output_name)

    def calculate_max_pixel(self, x, y):
        pixels = self.get_sorted_neighbors(x, y)
        l = len(pixels)
        print '--------------------'
        print pixels
        print
        print pixels[l - 1]
        print '-------------------'
        return pixels[l - 1]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage -> ./max.py FILENAME"
        print "Optional argument TYPE: 0 = normal neighborhood, 1 = cross neighborhood, 2 = plus neighborhood (default 0)"
        print "Example: ./max.py mason.jpg 1"
        print
        exit()

    image_name = sys.argv[1]

    mf = MaxFilter(image_name)
    mf.apply_filter()