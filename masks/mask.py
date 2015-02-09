__author__ = 'otniel'

import Image
import numpy as np

from utils.neighborhoods import BaseNeighborhood

CURRENT_PIXEL_POSITION = 4

class Mask:
    def __init__(self, image, mask_filename='default.txt'):
        self.image = image
        self.pixels = self.image.load()
        self.mask = self._read_mask_from_file_name(mask_filename)
        self.mask_width, self.mask_height = self.mask.shape
        self.image_width, self.image_height = self.image.size
        self.neighborhood = BaseNeighborhood(image.size)

    def _read_mask_from_file_name(self, mask_filename):
        with open(mask_filename, 'r') as mask_file:
            return self.get_matrix_from_file(mask_file)

    def get_matrix_from_file(self, matrix_file):
        return np.array([map(int, line.split(',')) for line in matrix_file])

    def _mask_not_normalized(self):
        return np.sum(self.mask) != 1.0

    def _normalize_mask(self):
        for y in xrange(self.mask_height):
            for x in xrange(self.mask_width):
                self.mask[x, y] /= np.sum(self.mask)

    def _reshape_mask(self):
        self.mask = self.mask.reshape(self.total_mask_elements)
        mask_list = self.mask.tolist()
        self.mask = np.array(mask_list)

    def _is_not_one_dimension_mask(self):
        return self.mask.ndim != 1

    def apply_mask(self):
        self.gradient_list = []
        for y in xrange(self.image_height):
            for x in xrange(self.image_width):
                row = []
                if self.neighborhood._is_neither_corner_or_border(x, y): # Ignore borders and corners
                    row.append([self.pixels[x, y], self.convolve_pixel(x, y)])
                else:
                    row.append([0, 0])
                self.gradient_list.append(row)
    def convolve_pixel(self, x, y):
        neighbors = self.get_image_pixels(x, y)
        one_dimemsion_mask = self.mask.reshape(self.mask.size)
        return sum([neighbor * mask_item for (neighbor, mask_item) in zip(neighbors, one_dimemsion_mask)])

    def get_image_pixels(self, x, y):
        neighbors = np.array([self.pixels[coordinate]
                              for coordinate in self.neighborhood.get_neighbor_coordinates(x, y)])
        # Insert current pixel
        return np.insert(neighbors, CURRENT_PIXEL_POSITION, self.pixels[x, y])

    def get_gradient_list(self):
        return self.gradient_list