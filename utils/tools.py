__author__ = 'otniel'

import Image
import numpy as np
import random
import matplotlib.pyplot as plt

from utils.pixelneighborhoods import BasePixelNeighborhood
from math import sqrt
MAX_PIXEL_INTENSITY = 255
HALF_PIXEL_INTENSITY = 127
MIN_PIXEL_INTENSITY = 0

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
    print "Grayscaling image..."
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
    threshold = calculate_image_threshold(image)
    for y in xrange(image.size[1]): # height
        for x in xrange(image.size[0]): # width
            binary_pixels[x, y] = _binarize_pixel(binary_pixels[x, y], threshold)
    return binary_image

def calculate_threshold(data): # Reference: http://goo.gl/7nP48T page 12
    threshold = data.mean()
    previous_mean_one, previous_mean_two = 0, 0
    group_one, group_two = _get_lower_group(data, threshold), _get_upper_group(data, threshold)
    mean_one, mean_two = group_one.mean(), group_two.mean()
    threshold = 0.5 * (mean_one + mean_two)
    while previous_mean_one != mean_one or previous_mean_two != mean_two:
        previous_mean_one, previous_mean_two = mean_one, mean_two
        group_one, group_two = _get_lower_group(data, threshold), _get_upper_group(data, threshold)
        mean_one, mean_two = int(group_one.mean()), int(group_two.mean())
        threshold = 0.5 * (mean_one + mean_two)
    return threshold

def calculate_image_threshold(image):
    data = get_pixels_list(image)
    return calculate_threshold(data)

def _get_lower_group(data, threshold):
    return np.array([value for value in data if value < threshold])

def _get_upper_group(data, threshold):
    return np.array([value for value in data if value > threshold])

def plot_data(data):
    hist, bins = np.histogram(data)
    center = (bins[:-1] + bins[1:]) / 2
    width = 0.7 * (bins[1] - bins[0])
    plt.bar(center, hist, align='center', width=width)
    plt.show()

def calculate_global_gradient(horizontal_gradient, vertical_gradient):
    """
    :param horizontal_gradient:
    :param vertical_gradient:
    :return 2-dimensoinal list with pixels - gradient:
    """

    # Pixels from arbitrary gradient, they are the same
    pixels = [pixel for pixel in horizontal_gradient]
    return [sqrt(x ** 2 + y ** 2) for (x, y) in
            zip(horizontal_gradient, vertical_gradient)]

def _binarize_pixel(pixel, threshold=HALF_PIXEL_INTENSITY):
    if pixel >= threshold:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY

def get_pixels_list(image):
    pixels = image.load()
    return np.array([pixels[x, y] for y in xrange(image.size[1]) for x in xrange(image.size[0])])

def generate_random_color():
    black_limit, white_limit = MIN_PIXEL_INTENSITY + 50, MAX_PIXEL_INTENSITY - 50
    r = _get_random_intensity(black_limit, white_limit)
    g = _get_random_intensity(black_limit, white_limit)
    b = _get_random_intensity(black_limit, white_limit)
    return (r, g, b)

def _get_random_intensity(black_limit=MIN_PIXEL_INTENSITY, white_limit=MAX_PIXEL_INTENSITY):
    return random.randint(black_limit, white_limit)

def generate_color_palette(number_of_colors = 5):
    return [generate_random_color() for number in xrange(number_of_colors)]


if __name__ == '__main__':
    rgb_image = Image.open('../mason.jpg')
    print "Inverting image..."
    inverted_image = invert_rgb_image(rgb_image)
    inverted_image.save('images/inverted_mason.png')

    print "Grayscaling image..."
    gray_image = grayscale_rgb_image(rgb_image)
    gray_image.save('images/grayscale_mason.png')

    print "Binarizing image..."
    binary_image = binarize_rgb_image(rgb_image)
    binary_image.save('images/automatic_binary_mason.png')