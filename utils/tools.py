__author__ = 'otniel'

import Image
import numpy as np
import random
import matplotlib.pyplot as plt

from math import sqrt, floor

MAX_PIXEL_INTENSITY = 255
HALF_PIXEL_INTENSITY = 127
MIN_PIXEL_INTENSITY = 0


def invert_rgb_image(image):
    pixels = image.load()
    inverted_image = Image.new(image.mode, image.size)
    inverted_pixels = inverted_image.load()
    for y in xrange(image.size[1]):  # kight
        for x in xrange(image.size[0]):  # width
            inverted_pixels[x, y] = _invert_rgb_pixel(pixels[x, y])
    return inverted_image


def _invert_rgb_pixel(pixel):
    r, g, b = pixel
    return (MAX_PIXEL_INTENSITY - r), (MAX_PIXEL_INTENSITY - g), (MAX_PIXEL_INTENSITY - b)


def grayscale_rgb_image(image):
    print "Grayscaling image..."
    pixels = image.load()
    grayscale_image = Image.new("RGB", image.size)
    grayscale_pixels = grayscale_image.load()
    for y in xrange(image.size[1]):  # height
        for x in xrange(image.size[0]):  # width
            gpx = _get_grayscale_pixel(pixels[x, y])
            grayscale_pixels[x, y] = (gpx, gpx, gpx)
    return grayscale_image


def _get_grayscale_pixel(rgb_pixel):
    red, green, blue = rgb_pixel
    # Weighted sum
    return int(sum([x * y for (x, y) in zip([red, green, blue],
                                            [0.2126, 0.7152, 0.0722])]))  # Intensity coefficients [http://u.to/qEtWCg]


def binarize_rgb_image(image):
    grayscale_image = grayscale_rgb_image(image)
    return binarize_image(grayscale_image)


def binarize_image(image):
    binary_image = image
    binary_pixels = binary_image.load()
    threshold = calculate_image_threshold(image)
    for y in xrange(image.size[1]):  # height
        for x in xrange(image.size[0]):  # width
            bp = _binarize_pixel(binary_pixels[x, y][0], threshold)
            binary_pixels[x, y] = (bp, bp, bp)
    return binary_image


def _binarize_pixel(pixel, threshold=HALF_PIXEL_INTENSITY):
    if pixel >= threshold:
        return MAX_PIXEL_INTENSITY
    return MIN_PIXEL_INTENSITY


def calculate_threshold(data):  # Reference: http://goo.gl/7nP48T page 12
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
    data = np.array([pixels[0] for pixels in data])
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
    :return 2-dimensional list with pixels - gradient:
    """
    return [sqrt(x ** 2 + y ** 2) for (x, y) in
            zip(horizontal_gradient, vertical_gradient)]


def get_pixels_list(image):
    pixels = image.load()
    return np.array([pixels[x, y][0] for y in xrange(image.size[1]) for x in xrange(image.size[0])])


def generate_random_color():
    black_limit, white_limit = MIN_PIXEL_INTENSITY + 50, MAX_PIXEL_INTENSITY - 50
    r = _get_random_intensity(black_limit, white_limit)
    g = _get_random_intensity(black_limit, white_limit)
    b = _get_random_intensity(black_limit, white_limit)
    return r, g, b


def _get_random_intensity(black_limit=MIN_PIXEL_INTENSITY, white_limit=MAX_PIXEL_INTENSITY):
    return random.randint(black_limit, white_limit)


def generate_color_palette(number_of_colors=5):
    return [generate_random_color() for number in xrange(number_of_colors)]


def get_image_diagonal_distance(image):
    return int(sqrt(image.size[0] ** 2 + image.size[1] ** 2))


def is_border_pixel(pixel):
    return pixel == MAX_PIXEL_INTENSITY


def image_to_cartesian_coordinates(x, y, width, height):
    cartesian_x_axis = int(x - (width / 2.0))
    cartesian_y_axis = int((height / 2.0) - y)
    return cartesian_x_axis, cartesian_y_axis


def cartesian_to_image_coordinates(x, y, width, height):
    cartesian_x_axis = x + (width / 2.0)
    cartesian_y_axis = (height / 2.0) - y
    return cartesian_x_axis, cartesian_y_axis


def convert_rgb_to_hex(rgb):
    if any(channel > 255 or channel < 0 for channel in rgb):
        return "All color channels must be in [0 - 255]"

    r, g, b = rgb
    r = hex(r).split('x')[1].zfill(2)
    g = hex(g).split('x')[1].zfill(2)
    b = hex(b).split('x')[1].zfill(2)
    return '#' + r + g + b


def normalize_grayscale_image(image):
    frecuencies = dict()
    pixels = image.load()
    width, height = image.size

    for y in xrange(height):
        for x in xrange(width):
            color = pixels[x, y][0]
            if color in frecuencies:
                frecuencies[color] += 1
            else:
                frecuencies[color] = 1

    threshold = 10
    max, min = -1, 999999
    for color in frecuencies:
        if frecuencies[color] > threshold:
            if color < min:
                min = color
            if color > max:
                max = color
    range = float(max - min)
    new_image = Image.new('RGB', image.size)
    new_pixels = new_image.load()
    for y in xrange(height):
        for x in xrange(width):
            color = pixels[x, y][0]
            if color <= min:
                new_pixels[x, y] = (0, 0, 0)
            elif color >= max:
                new_pixels[x, y] = (255, 255, 255)
            else:
                i = int(255 * (color - min) / range)
                new_pixels[x, y] = (i, i, i)
    return new_image


def normalize_rgb_image(image):
    gray_image = grayscale_rgb_image(image)
    return normalize_grayscale_image(gray_image)


if __name__ == '__main__':
    rgb_image = Image.open('../test-images/mason.jpg')
    # print "Inverting image..."
    # inverted_image = invert_rgb_image(rgb_image)
    # inverted_image.save('../test-images/inverted_mason.png')

    # print "Grayscaling image..."
    gray_image = grayscale_rgb_image(rgb_image)
    gray_image.save('../test-images/grayscale_mason.png')

    # print "Binarizing image..."
    # binary_image = binarize_rgb_image(rgb_image)
    # binary_image.save('../test-images/automatic_binary_mason.png')

    # print convert_rgb_to_hex((12, 2, 1112))
    norm_im = normalize_grayscale_image(gray_image)
    norm_im.save('../test-images/new_normalized.png')