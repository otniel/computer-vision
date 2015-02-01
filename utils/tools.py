__author__ = 'otniel'

import Image
from filters.median import MedianFilter
from utils.neighborhoods import BasePixelNeighborhood

MAX_PIXEL_INTENSITY = 255
MIN_PIXEL_INTENSITY = 0
FIXED_THRESHOLD = 127

def invert_rgb_image(image):
    pixels = image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            pixels[x, y] = invert_pixel(pixels[x, y])

def invert_rgb_pixel(pixel):
    r, g, b = pixel
    return ((MAX_PIXEL_INTENSITY - r), (MAX_PIXEL_INTENSITY - g), (MAX_PIXEL_INTENSITY - b))

def rgb_to_grayscale(image):
    pixels = image.load()
    grayscale_image = Image.new("L", image.size)
    grayscale_pixels = grayscale_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            grayscale_pixels[x, y] = get_grayscale_pixel(pixels[x, y])
    return grayscale_image

def get_grayscale_pixel(rgb_pixel):
    red, green, blue = rgb_pixel
    # Weighted sum
    return sum([x*y for (x,y) in zip([red, green, blue],
                                     [0.2126, 0.7152, 0.0722])]) # Intensity coefficients [http://u.to/qEtWCg]

def binarize_rgb_image(image):
    grayscale_image = rgb_to_grayscale(image)
    pixels = grayscale_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            pixels[x, y] = _binarize_pixel
    return grayscale_image

def _binarize_pixel(pixel):
    if pixel >= 127:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY

def erode_binary_image(image):
    neighborhood = BasePixelNeighborhood(image.load(), image.size)

    eroded_image = Image.new("L", image.size)
    eroded_pixels = eroded_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            eroded_pixels[x, y] = _erode_pixel(neighborhood, x, y)
    return eroded_image

def _erode_pixel(neighborhood, x, y):
    binary_neighbors = neighborhood.get_binary_pixel_neighborhood(x, y)
    if sum(binary_neighbors) < 8:
        return MIN_PIXEL_INTENSITY
    return MAX_PIXEL_INTENSITY

def dilate_binary_image(image):
    neighborhood = BasePixelNeighborhood(image.load(), image.size)

    dilated_image = Image.new("L", image.size)
    dilated_pixels = dilated_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            dilated_pixels[x, y] = _dilate_pixel(neighborhood, x, y)
    return dilated_image

def _dilate_pixel(neighborhood, x, y):
    binary_neighbors = neighborhood.get_binary_pixel_neighborhood(x, y)
    if sum(binary_neighbors) > 0:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY

def detect_edges_in_binary_images(image):
    neighborhood = BasePixelNeighborhood(image.load(), image.size)

    edged_image = Image.new("L", image.size)
    edged_pixels = edged_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            pixels_neigh = neighborhood.get_binary_pixel_neighborhood(x, y)
            sigma = sum(pixels_neigh)
            if sigma == 8:
                edged_pixels[x, y] = MIN_PIXEL_INTENSITY
            else:
                edged_pixels[x, y] = MAX_PIXEL_INTENSITY
    return edged_image

def remove_salt_noise(image):
    neighborhood = BasePixelNeighborhood(image.load(), image.size)

    unsalted_image = Image.new("L", image.size)
    unsalted_pixels = unsalted_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            unsalted_pixels[x, y] = remove_salt_pixel(neighborhood, x, y)
    return unsalted_image

def remove_salt_pixel(neighborhood, x, y):
    binary_neighbors = neighborhood.get_binary_pixel_neighborhood(x, y)
    if sum(binary_neighbors) == 8:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY

def remove_pepper_noise(image):
    neighborhood = BasePixelNeighborhood(image.load(), image.size)
    unpeppered_image = Image.new("L", image.size)
    unpeppered_pixels = unpeppered_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            unpeppered_pixels[x, y] = remove_pepper_pixel(neighborhood, x, y)
    return unpeppered_image

def remove_pepper_pixel(neighborhood, x, y):
    binary_neighbors = neighborhood.get_binary_pixel_neighborhood(x, y)
    if sum(binary_neighbors) == 0:
        return MIN_PIXEL_INTENSITY
    return MAX_PIXEL_INTENSITY