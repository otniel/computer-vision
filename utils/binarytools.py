__author__ = 'otniel'

import Image

from utils.pixelneighborhoods import BasePixelNeighborhood, CrossPixelNeighborhood, PlusPixelNeighborhood

MAX_PIXEL_INTENSITY = 255
MIN_PIXEL_INTENSITY = 0
FIXED_THRESHOLD = 127

class BinaryImageTools:
    def __init__(self, image, neighborhood=0):
        self.image = image
        self.pixels = image.load()
        if neighborhood == '1':
            self.neighborhood = CrossPixelNeighborhood(self.pixels, self.image.size)
        elif neighborhood == '2':
            self.neighborhood = PlusPixelNeighborhood(self.pixels, self.image.size)
        else:
            self.neighborhood = BasePixelNeighborhood(self.pixels, self.image.size)

    def erode_image(self):
        eroded_image = Image.new(self.image.mode, self.image.size)
        eroded_pixels = eroded_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                eroded_pixels[x, y] = self._erode_pixel(x, y)
        return eroded_image

    def _erode_pixel(self, x, y):
        binary_neighbors = self.neighborhood.get_binary_pixel_neighborhood(x, y)
        if sum(binary_neighbors) > 0:
            return MAX_PIXEL_INTENSITY
        return MIN_PIXEL_INTENSITY

    def dilate_image(self):
        dilated_image = Image.new(self.image.mode, self.image.size)
        dilated_pixels = dilated_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                dilated_pixels[x, y] = self._dilate_pixel(x, y)
        return dilated_image

    def _dilate_pixel(self, x, y):
        binary_neighbors = self.neighborhood.get_binary_pixel_neighborhood(x, y)
        if sum(binary_neighbors) < 8:
            return MIN_PIXEL_INTENSITY
        return MAX_PIXEL_INTENSITY

    # Basic "Edge detection" with the local neighborhood
    def detect_edges_in_images(self):
        edged_image = Image.new(self.image.mode, self.image.size)
        edged_pixels = edged_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                edged_pixels[x, y] = self._edged_pixel(x, y)
        return edged_image

    def _edged_pixel(self, x, y):
        binary_neighbors = self.neighborhood.get_binary_pixel_neighborhood(x, y)
        if sum(binary_neighbors) == 8:
            return MIN_PIXEL_INTENSITY
        return MAX_PIXEL_INTENSITY

    def remove_salt_noise(self):
        unsalted_image = Image.new(self.image.mode, self.image.size)
        unsalted_pixels = unsalted_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                unsalted_pixels[x, y] = self._remove_salt_pixel(x, y)
        return unsalted_image

    def _remove_salt_pixel(self, x, y):
        binary_neighbors = self.neighborhood.get_binary_pixel_neighborhood(x, y)
        if sum(binary_neighbors) > 6:
            return MAX_PIXEL_INTENSITY
        return MIN_PIXEL_INTENSITY

    def remove_pepper_noise(self):
        unpeppered_image = Image.new(self.image.mode, self.image.size)
        unpeppered_pixels = unpeppered_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                unpeppered_pixels[x, y] = self._remove_pepper_pixel(x, y)
        return unpeppered_image

    def _remove_pepper_pixel(self, x, y):
        binary_neighbors = self.neighborhood.get_binary_pixel_neighborhood(x, y)
        if sum(binary_neighbors) < 2:
            return MIN_PIXEL_INTENSITY
        return MAX_PIXEL_INTENSITY

    def remove_salt_and_pepper_noise(self):
        clean_image = Image.new(self.image.mode, self.image.size)
        clean_pixels = clean_image.load()
        for y in xrange(self.image.size[1]): # height
            for x in xrange(self.image.size[0]): # width
                clean_pixels[x, y] = self._remove_salt_and_pepper(x, y)
        return clean_image

    def _remove_salt_and_pepper(self, x, y):
        clean_pixel = self._remove_pepper_pixel(x, y)
        clean_pixel = self._remove_salt_pixel(x, y)
        return clean_pixel

if __name__ == '__main__':
    from utils.tools import binarize_rgb_image

    rgb_image = Image.open('../mason.jpg')
    binary_image = binarize_rgb_image(rgb_image)
    bt = BinaryImageTools(binary_image)

    print "Eroding image..."
    eroded_image = bt.erode_image()
    eroded_image.save('images/eroded_mason.png')

    print "Dilating image..."
    dilated_image = bt.dilate_image()
    dilated_image.save('images/dilated_mason.png')

    print "Removing salt..."
    unsalted_image = bt.remove_salt_noise()
    unsalted_image.save('images/unsalted_mason.png')

    print "Removing pepper..."
    unpeppered_image = bt.remove_pepper_noise()
    unpeppered_image.save('images/unpeppered_mason.png')

    print "Cleaning image..."
    cleaned_image = bt.remove_salt_and_pepper_noise()
    cleaned_image.save('images/clean_mason.png')