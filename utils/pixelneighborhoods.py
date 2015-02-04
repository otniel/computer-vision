__author__ = 'otniel'

from utils.neighborhoods import BaseNeighborhood, CrossNeighborhood, PlusNeighborhood

class BasePixelNeighborhood():
    def __init__(self, pixels, image_size):
        self.pixels = pixels
        self.neighborhood = BaseNeighborhood(image_size)

    def get_binary_pixel_neighborhood(self, x, y):
        neighbors = [self.pixels[coordinate] for coordinate in (self.neighborhood.get_neighbor_coordinates(x, y))]
        binary_neighbors = [1 if neighbor == 255 else 0 for neighbor in neighbors]
        return binary_neighbors

class CrossPixelNeighborhood(BasePixelNeighborhood):
    def __init__(self, pixels, image_size):
        self.pixels = pixels
        self.neighborhood = CrossNeighborhood(image_size)

class PlusPixelNeighborhood(BasePixelNeighborhood):
    def __init__(self, pixels, image_size):
        self.pixels = pixels
        self.neighborhood = PlusNeighborhood(image_size)