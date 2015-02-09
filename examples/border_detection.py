import matplotlib.pyplot as plt
import Image
import numpy as np

from masks.mask import Mask
from utils.tools import grayscale_rgb_image, calculate_threshold
from filters.filter import MedianFilter
from math import sqrt

print "WARNING: Border detection may take several minutes depending on the image resolution"
image = Image.open('../mason.jpg')
print "Grayscaling image..."
image = grayscale_rgb_image(image)
filter = MedianFilter(image)
image = filter.apply_filter()

bt = BinaryImageTools(image)
print "Removing salt and pepper..."
bt.remove_salt_and_pepper_noise()

ver_mask = Mask(image, '../masks/sobel_vertical.txt')
ver_mask.apply_mask()
vertical_gradient = ver_mask.get_gradient_list()

hor_mask = Mask(image, '../masks/sobel_horizontal.txt')
hor_mask.apply_mask()
horizontal_gradient = hor_mask.get_gradient_list()

def calculate_global_gradient(horizontal_gradient, vertical_gradient):
    pixels = [pixel[0] for pixel in horizontal_gradient]
    return [[pixel, sqrt(x[1] ** 2 + y[1] ** 2)] for (pixel, x, y) in
            zip(pixels, horizontal_gradient, vertical_gradient)]

print "Calculating gradient..."
gradient = calculate_global_gradient(horizontal_gradient, vertical_gradient)
magnitudes = np.array([pixel[1] for pixel in gradient])
print "Calculating threshold..."
threshold = calculate_threshold(magnitudes)

img = Image.new("L", image.size)
new_pixels = img.load()

magnitude_index = 0
for y in xrange(image.size[1]):
    for x in xrange(image.size[0]):
        if magnitudes[magnitude_index] < threshold:
            new_pixels[x, y] = 0
        else:
            new_pixels[x, y] = 255
        magnitude_index += 1

img.save('borders.png')