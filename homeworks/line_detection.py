from homeworks.border_detection import BorderDetector
from PIL import Image
from collections import Counter

import numpy as np

class LineDetector:
    def __init__(self, image):
        self.border_detector = BorderDetector(image)
        self.border_detector.detect_borders()
        self.image = self.border_detector.draw_image_borders()
        self.border_pixels = self.border_detector.border_pixels
        self.angles = sorted(self.border_detector.angles)
        self.line_pixels = []

    def detect_lines(self):
        best_votes = self.get_best_votes()
        for candidate in self.border_detector.coordinates_rhos_and_theta:
            if candidate[1] in best_votes:
                self.line_pixels.append(candidate[0])

    def get_best_votes(self):
        counter = Counter(self.border_detector.rho_and_angle)
        commons = counter.most_common(100)
        best_votes = np.array([common[0] for common in commons])
        return best_votes

    def draw_lined_image(self):
        lined_image = Image.new("RGB", self.image.size, "white")
        lined_pixels = lined_image.load()
        for pixel in self.border_pixels:
            lined_pixels[pixel] = (255, 255, 255)
        for pixel in self.line_pixels:
            lined_pixels[pixel] = (255, 0, 0)
        return lined_image


image = Image.open('../test-images/multiple_lines.png')
image = image.convert('RGB')
ld = LineDetector(image)
ld.detect_lines()
lined_image = ld.draw_lined_image()
lined_image.save('../test-images/multiple_lined.png')
# angles_ranking = Counter(ld.angles)
#print angles_ranking.most_common()
#ld.plot()