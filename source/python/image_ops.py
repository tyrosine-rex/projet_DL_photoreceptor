import sys
from PIL import Image
from PIL import ImageOps

# python image_dir

if len(sys.argv) > 1:
	image_dir = sys.argv[1]

for image in image_dir:
	image = Image.open('your_image.png')
	inverted_image = PIL.ImageOps.invert(image)
	inverted_image.save('new_name.png')
