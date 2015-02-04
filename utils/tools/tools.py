__author__ = 'otniel'

import Image
from utils.pixelneighborhoods import BasePixelNeighborhood

MAX_PIXEL_INTENSITY = 255
MIN_PIXEL_INTENSITY = 0
FIXED_THRESHOLD = 127

def invert_rgb_image(image):
    pixels = image.load()
    inverted_image = Image.new(image.mode, image.size)
    inverted_pixels = inverted_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            inverted_pixels[x, y] = _invert_rgb_pixel(pixels[x, y])
    return inverted_image

def _invert_rgb_pixel(pixel):
    r, g, b = pixel
    return ((MAX_PIXEL_INTENSITY - r), (MAX_PIXEL_INTENSITY - g), (MAX_PIXEL_INTENSITY - b))

def grayscale_rgb_image(image):
    pixels = image.load()
    grayscale_image = Image.new("L", image.size)
    grayscale_pixels = grayscale_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            grayscale_pixels[x, y] = _get_grayscale_pixel(pixels[x, y])
    return grayscale_image

def _get_grayscale_pixel(rgb_pixel):
    red, green, blue = rgb_pixel
    # Weighted sum
    return sum([x*y for (x,y) in zip([red, green, blue],
                                     [0.2126, 0.7152, 0.0722])]) # Intensity coefficients [http://u.to/qEtWCg]

def binarize_rgb_image(image):
    grayscale_image = grayscale_rgb_image(image)
    return binarize_image(grayscale_image)

def binarize_image(image):
    binary_image = image
    binary_pixels = binary_image.load()
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            binary_pixels[x, y] = _binarize_pixel(binary_pixels[x, y])
    return binary_image

def _binarize_pixel(pixel):
    if pixel >= FIXED_THRESHOLD:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY

if __name__ == '__main__':

    rgb_image = Image.open('mason.jpg')

    inverted_image = invert_rgb_image(rgb_image)
    inverted_image.save('inverted_mason.png')

    gray_image = grayscale_rgb_image(rgb_image)
    gray_image.save('grayscale_mason.png')

    binary_image = binarize_rgb_image(rgb_image)
    binary_image.save('binary_mason.png')


