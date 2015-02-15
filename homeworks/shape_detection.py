__author__ = 'otniel'

import Image

from utils.tools import binarize_rgb_image
from utils.neighborhoods import BaseNeighborhood
from homeworks.border_detection import BorderDetector

def bfs(graph, root):
    pass

image = Image.open('../test-images/doge.jpg')
bt = BorderDetector(image)
bordered_image = bt.detect_borders()
pixels = bordered_image.load()

for y in xrange(image.size[1]):
    for x in xrange(image.size[0]):
        print pixels[x, y]