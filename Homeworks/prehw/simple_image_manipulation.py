import Image
import sys

if len(sys.argv) != 3:
    print "Usage -> simple_image_manipulation.py FILENAME_INPUT FILENAME_OUTPUT"
    exit()

filename_input = sys.argv[1] 
filename_output = sys.argv[2]

image = Image.open(filename_input);

if image.mode != 'RGBA':
    image = image.convert('RGBA')

width = image.size[0]
height = image.size[1]

pixels = image.load()

for x_axis in range(width-1):
    for y_axis in range(height-1):
        red,green,blue,alpha = pixels[x_axis, y_axis]
        new_pixel =  blue,green,red,alpha
        pixels[x_axis, y_axis] = new_pixel

image.save(filename_output)