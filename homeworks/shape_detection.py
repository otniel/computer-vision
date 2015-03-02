__author__ = 'otniel'

from PIL import Image, ImageDraw

from utils.tools import binarize_rgb_image, generate_random_color
from utils.neighborhoods import BaseNeighborhood
from homeworks.border_detection import BorderDetector
from time import sleep
VISITED_NEIGHBOR_COLOR = 127

class ShapeDetector:
    def __init__(self, image):
        border_detector = BorderDetector(image)
        border_detector.detect_borders()
        self.image = border_detector.draw_image_borders()
        self.border_pixels = border_detector.border_pixels
        self.new_image = Image.new("RGB", self.image.size)
        self.new_pixels = self.new_image.load()
        for border in self.border_pixels:
            self.new_pixels[border] = (255, 255, 255)
        self.pixels = self.image.load()
        self.neighborhood = BaseNeighborhood(image.size)
        self.shapes = []
        self.num_shapes = 0

    def detect_shapes(self):
        for y in xrange(self.image.size[1]):
            for x in xrange(self.image.size[0]):
                pixel_coordinate = (x, y)
                if self.pixel_is_not_visited(pixel_coordinate) and not self._is_border(pixel_coordinate):
                    shape = self.find_shape(pixel_coordinate)
                    self.shapes.append(shape)
        self.draw_shape_locators()
        self.print_shape_percentajes()
        self.new_image.show()

    def _is_border(self, pixel_coordinate):
        return pixel_coordinate in self.border_pixels

    def pixel_is_not_visited(self, neighbor):
        return self.pixels[neighbor] != VISITED_NEIGHBOR_COLOR

    # DFS
    def find_shape(self, pixel_coordinate):
        pixel_stack = []
        pixel_stack.append(pixel_coordinate)
        mass = []
        color = generate_random_color()
        while pixel_stack:
            x, y = pixel_stack.pop()
            neighbors = self.neighborhood.get_neighbor_coordinates(x, y)
            for neighbor in neighbors:
                if self.pixel_is_not_visited(neighbor) and not self._is_border(neighbor):
                    self.visit_pixel(neighbor, color)
                    pixel_stack.append(neighbor)
                    mass.append(neighbor)
        shape = Shape(mass)
        return shape

    def visit_pixel(self, pixel, color):
        self.pixels[pixel] = VISITED_NEIGHBOR_COLOR
        self.new_pixels[pixel] = color

    def draw_shape_locators(self):
        draw = ImageDraw.Draw(self.new_image)
        for index, shape in enumerate(self.shapes):
            draw.text(shape.center_of_mass, "*" + str(index + 1))
            x_min, y_min, x_max, y_max = shape.get_bounding_box_coordinates()
            draw.rectangle([x_min, y_min, x_max, y_max])

    def print_shape_percentajes(self):
        max_shape = [len(shape.mass) for shape in self.shapes]
        total_pixels = self.image.size[0] * self.image.size[1]
        for index, shape in enumerate(self.shapes):
            percentage = len(shape.mass) / float(total_pixels) * 100
            print "Shape %d is the %.6f %s of the entire image" % (index, percentage, '%')

    def draw_image_shapes(self):
        return self.new_image

class Shape:
    def __init__(self, mass=[]):
        self.mass = mass
        self.x_components = [point[0] for point in mass]
        self.y_components = [point[1] for point in mass]
        self.center_of_mass = self.calculate_center_of_mass()

    def calculate_center_of_mass(self):
        x = sum(self.x_components) / len(self.mass)
        y = sum(self.y_components) / len(self.mass)
        return (x, y)

    def get_bounding_box_coordinates(self):
        x_min = min(self.x_components)
        x_max = max(self.x_components)
        y_min = min(self.y_components)
        y_max = max(self.y_components)
        return (x_min, y_min, x_max, y_max)

image = Image.open('../test-images/shapes.png')
image = image.convert('RGB')
sd = ShapeDetector(image)
sd.detect_shapes()
image_shapes = sd.draw_image_shapes()
image_shapes.save("../test-images/detected_shapes.png")
