__author__ = 'otniel'

from PIL import Image, ImageDraw
from collections import Counter
from math import sqrt
from homeworks.border_detection import BorderDetector
from utils.tools import is_border_pixel
import math
import numpy as np


class EllipseDetection:
    def __init__(self, image):
        self.border_detector = BorderDetector(image)
        self.border_detector.detect_borders()
        self.pixels = self.image.load()
        self.image = self.border_detector.draw_image_borders()