import Image

image = Image.open('/home/otniel/Pictures/mas-mezcla-maistro.jpg');
print image.mode

if image.mode != 'RGBA':
    image = image.convert('RGBA')

image.save('/home/otniel/Pictures/maistro.jpg')