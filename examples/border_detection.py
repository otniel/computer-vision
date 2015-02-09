import matplotlib.pyplot as plt
import Image
import numpy as np

from masks.mask import Mask
from utils.tools.tools import grayscale_rgb_image
from math import sqrt

image = Image.open('/home/otniel/Documents/repos/computer-vision/doge.jpg')
image = grayscale_rgb_image(image)

ver_mask = Mask(image, '/home/otniel/Documents/repos/computer-vision/masks/sobel_vertical.txt')
ver_mask.apply_mask()
vertical_gradient_list = ver_mask.get_gradient_list()
vertical_gradient = np.array(vertical_gradient_list)
vertical_gradient.reshape(vertical_gradient.size)
vertical_gradient = [vertical.pop() for vertical in vertical_gradient.tolist()]

hor_mask = Mask(image, '/home/otniel/Documents/repos/computer-vision/masks/sobel_horizontal.txt')
hor_mask.apply_mask()
horizontal_gradient_list = hor_mask.get_gradient_list()
horizontal_gradient = np.array(horizontal_gradient_list)
horizontal_gradient.reshape(horizontal_gradient.size)
horizontal_gradient = [horizontal.pop() for horizontal in horizontal_gradient.tolist()]
print horizontal_gradient

def calculate_global_gradient(horizontal_gradient, vertical_gradient):
    pixels = [pixel[0] for pixel in horizontal_gradient]
    return [[pixel, sqrt(x[1] ** 2 + y[1] ** 2)] for (pixel, x, y) in
            zip(pixels, horizontal_gradient, vertical_gradient)]

gradient = calculate_global_gradient(horizontal_gradient, vertical_gradient)
magnitudes = np.array([pixel[1] for pixel in gradient])

def get_lower_group(histogram, threshold):
    return np.array([value for value in histogram if value < threshold])

def get_upper_group(histogram, threshold):
    return np.array([value for value in histogram if value > threshold])

def calculate_threshold(histogram):
    print "Calculating threshold..."
    threshold = histogram.mean()
    previous_mean_one, previous_mean_two = 0, 0
    group_one, group_two = get_lower_group(histogram, threshold), get_upper_group(histogram, threshold)
    mean_one, mean_two = group_one.mean(), group_two.mean()
    threshold = 0.5 * (mean_one + mean_two)
    while previous_mean_one != mean_one or previous_mean_two != mean_two:
        previous_mean_one, previous_mean_two = mean_one, mean_two
        group_one, group_two = get_lower_group(histogram, threshold), get_upper_group(histogram, threshold)
        mean_one, mean_two = int(group_one.mean()), int(group_two.mean())
        threshold = 0.5 * (mean_one + mean_two)
    return threshold

threshold = calculate_threshold(magnitudes)
print threshold
gradient = np.array(gradient)
print gradient.shape
#gradient = gradient.reshape(30, 30)
print gradient.reshape(900, 1, 2)
img = Image.new("L", image.size)

#hist, bins = np.histogram(magnitudes)
#width = 0.7 * (bins[1] - bins[0])
#center = (bins[:-1] + bins[1:]) / 2
#plt.bar(center, hist, align='center', width=width)
#plt.show()