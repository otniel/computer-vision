__author__ = 'otniel'

from utils.neighborhoods import BaseNeighborhood, CrossNeighborhood, PlusNeighborhood

class BasePixelNeighborhood():
    def __init__(self, image):
        self.pixels = image.load()
        self.neighborhood = BaseNeighborhood(image.size)

    def get_pixel_neighbors(self, x, y):
        return [self.pixels[coordinate] for coordinate in (self.neighborhood.get_neighbor_coordinates(x, y))]

    def get_binary_pixel_neighborhood(self, x, y):
        neighbors = self.get_pixel_neighbors(x, y)
        binary_neighbors = [1 if neighbor == 255 else 0 for neighbor in neighbors]
        return binary_neighbors

class CrossPixelNeighborhood(BasePixelNeighborhood):
    def __init__(self, image):
        self.pixels = image.load()
        self.neighborhood = BaseNeighborhood(image.size)

class PlusPixelNeighborhood(BasePixelNeighborhood):
    def __init__(self, image):
        self.pixels = image.load()
        self.neighborhood = BaseNeighborhood(image.size)