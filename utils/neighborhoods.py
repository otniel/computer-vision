__author__ = 'otniel'

class BasePixelNeighborhood:
    def __init__(self, pixels, image_size):
        self.pixels = pixels
        self.width = image_size[0]
        self.height = image_size[1]

    def get_neighbor_coordinates(self, x, y):
        if self._is_corner(x, y):
            return self.corner_neighbors(x, y)

        if self._is_border(x, y):
            return self.border_neighbors(x, y)

        return self._all_neighbors(x, y)

    def get_binary_pixel_neighborhood(self, x, y):
        neighbors = [self.pixels[coordinate] for coordinate in (self.get_neighbor_coordinates(x, y))]
        binary_neighbors = [1 if neighbor == 255 else 0 for neighbor in neighbors]
        return binary_neighbors

    def _is_corner(self, x, y):
        return self._is_top_left(x, y) or self._is_top_right(x, y) \
               or self._is_bottom_left(x, y) or self._is_bottom_right(x, y)

    def _is_border(self, x, y):
        return self._is_top_border(x, y) or self._is_bottom_border(x, y) \
               or self._is_right_border(x, y) or self._is_left_border(x, y)

    def _is_top_left(self, x, y):
        return x == 0 and y == 0

    def _is_top_right(self, x, y):
        return x == self.width - 1 and y == 0

    def _is_bottom_left(self, x, y):
        return x == 0 and y == self.height - 1

    def _is_bottom_right(self, x, y):
        return x == self.width - 1 and y == self.height - 1

    def _is_top_border(self, x, y):
        return y == 0 and self._is_corner(x, y) is False

    def _is_bottom_border(self, x, y):
        return y == self.height - 1 and self._is_corner(x, y) is False

    def _is_right_border(self, x, y):
        return x == 0 and self._is_corner(x, y) is False

    def _is_left_border(self, x, y):
        return x == self.width - 1 and self._is_corner(x, y) is False

    def corner_neighbors(self, x, y):
        if self._is_top_left(x, y):
            return self._top_left_neighbors(x, y)

        if self._is_top_right(x, y):
            return self._top_right_neighbors(x, y)

        if self._is_bottom_left(x, y):
            return self._bottom_left_neighbors(x, y)

        if self._is_bottom_right(x, y):
            return self._bottom_right_neighbors(x, y)

    def _top_left_neighbors(self, x, y):
        return ((x, y+1), (x+1, y+1), (x+1, y))

    def _top_right_neighbors(self, x, y):
        return ((x-1, y), (x-1, y+1), (x, y+1))

    def _bottom_left_neighbors(self, x, y):
        return ((x, y-1), (x+1, y-1), (x+1, y))

    def _bottom_right_neighbors(self, x, y):
        return ((x-1, y), (x-1, y-1), (x, y-1))

    def border_neighbors(self, x, y):
        if self._is_top_border(x, y):
            return self._top_neighbors(x, y)

        if self._is_bottom_border(x, y):
            return self._bottom_neighbors(x, y)

        if self._is_left_border(x, y):
            return self._left_neighbors(x, y)

        if self._is_right_border(x, y):
            return self._right_neighbors(x, y)

    def _top_neighbors(self, x, y):
        return ((x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y))

    def _bottom_neighbors(self, x, y):
        return ((x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y))

    def _left_neighbors(self, x, y):
        return ((x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1))

    def _right_neighbors(self, x, y):
        return ((x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1))

    def _all_neighbors(self, x, y):
        return ((x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1))

class CrossPixelNeighborhood(BasePixelNeighborhood):
    def _top_left_neighbors(self, x, y):
        return ((x+1, y+1),)

    def _top_right_neighbors(self, x, y):
        return ((x-1, y+1),)

    def _bottom_left_neighbors(self, x, y):
        return ((x+1, y-1),)

    def _bottom_right_neighbors(self, x, y):
        return ((x-1, y-1),)

    def _top_neighbors(self, x, y):
        return ((x-1, y+1), (x+1, y+1))

    def _bottom_neighbors(self, x, y):
        return ((x-1, y-1), (x+1, y-1))

    def _left_neighbors(self, x, y):
        return ((x+1, y-1), (x+1, y+1))

    def _right_neighbors(self, x, y):
        return ((x-1, y-1), (x-1, y+1))

    def _all_neighbors(self, x, y):
        return ((x-1, y-1), (x-1, y+1), (x+1, y+1), (x+1, y-1))

class PlusPixelNeighborhood(BasePixelNeighborhood):
    def _top_left_neighbors(self, x, y):
        return ((x, y+1), (x+1, y))

    def _top_right_neighbors(self, x, y):
        return ((x-1, y), (x, y+1))

    def _bottom_left_neighbors(self, x, y):
        return ((x, y-1), (x+1, y))

    def _bottom_right_neighbors(self, x, y):
        return ((x-1, y), (x, y-1))

    def _top_neighbors(self, x, y):
        return ((x, y+1),)

    def _bottom_neighbors(self, x, y):
        return ((x, y-1),)

    def _left_neighbors(self, x, y):
        return ((x+1, y),)

    def _right_neighbors(self, x, y):
        return ((x-1, y),)

    def _all_neighbors(self, x, y):
        return ((x, y-1), (x-1, y), (x, y+1), (x+1, y))