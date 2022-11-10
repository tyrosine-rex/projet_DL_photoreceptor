# forme des PR : contours moins circulaires
# VGG : supprimer les dernières couches et les remplacer par des couches correspondant aux classes des nombres de photorécepteurs

import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import math as m
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops
import random as r
import os

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

n_img = 10
# n_img = 1000

experiments = ('training', 'testing')
global_img_i = 0
used_img_i = []
# dim = 32
dim = 200
x = dim/6
dx = x/10
width = dim/12
w = width
n_vertices = 16
mu = 4
sigma = 2
n_circles_det = [round(x) for x in np.random.normal(mu, sigma, n_img)]
# n_circles_det = [4 for _ in range(n_img)]
# print(n_circles_det)
img_extension = '.tif'
o = -x
min_angle = -180
max_angle = 180
min_intensity = 127
max_intensity = 255
homogeneous = False
if homogeneous:
    min_intensity = max_intensity
change_blur = True
blur_radius = dim//40
change_brightness = True
min_brightness_factor = 0.4
max_brightness_factor = 1.0
change_offset = True
min_offset = 0
max_offset = dim//20

centers = ((0+o, 0+o), (0+o, x+o), (x+o-dx, 1.5*x+o), (2*x+o-2*dx, 0+o), (2*x+o-2*dx, x+o), (2*x+o-2*dx, 2*x+o))

for i in range(len(n_circles_det)):
    if n_circles_det[i] < 1:
        n_circles_det[i] = 1
    elif n_circles_det[i] > 6:
        n_circles_det[i] = 6
# print(n_circles_det)

for experiment in experiments:
    # Create testing / training directories if they don't exist
    try:
        os.mkdir(experiment)
    except:
        pass

    # Create a directory for each class if it doesn't exist
    for i in range(10):
        try:
            os.mkdir('./'+experiment+'/'+str(i))
        except:
            pass
    
    for k in range(1, 7):
        # Generate <n_img> vignettes
        for img_i in range(n_img):
            center_sizes = np.random.normal(width, width/8, 6)
            center_offsets = np.random.normal(0, dim//55, 6)

            offset = r.uniform(min_offset, max_offset)
            brightness_factor = r.uniform(min_brightness_factor, max_brightness_factor)

            image = Image.new('L', (dim, dim))
            draw = ImageDraw.Draw(image)

            centers_translated = [(center[0] + dim/2 + offset, center[1] + dim/2 + offset) for center in centers]
            # polygons = [[] for i in range(len(centers_translated))]
            polygons = []

            # Build a polygon around each center
            for i in range(len(centers_translated)):
                # for j in range(1, n_vertices+1):
                #     poly_point = []
                #     for item in zip(pol2cart(center_sizes[i], j*2*m.pi/n_vertices), (centers_translated[i][0] + center_offsets[i], centers_translated[i][1])):
                #         poly_point.append(sum(item))
                #     poly_point = tuple(poly_point)
                #     polygons[i].append(poly_point)
                # polygons[i].append(polygons[i][0])
                w, h = dim/2.5, dim/2.5
                # shape = [(35, 20), (w - 10, h - 10)]
                shape = [(20*i,10*i), (w - 10, h - 10)]
                # polygons[i].append(shape)
                polygons.append(shape)

            maliste = [True if i < k else False for i in range(len(centers))]
            p = r.sample(maliste, len(maliste))
            # print(sum(p), p)
            for i in range(len(polygons)):
                if p[i]:
                    # draw.polygon((polygons[i]), fill=r.randint(min_intensity, max_intensity))
                    draw.ellipse(polygons[i], fill=r.randint(min_intensity, max_intensity))
            n_circles = str(sum(p))
            # print(n_circles)

            im = image.rotate(r.randint(min_angle, max_angle))
            if change_blur:
                im = im.filter(ImageFilter.GaussianBlur(blur_radius))
            if change_offset:
                im = ImageChops.offset(im, r.randint(min_offset, max_offset), r.randint(min_offset, max_offset))
            if experiment == 'testing':
                im = ImageOps.mirror(im)
            if change_brightness:
                obj = ImageEnhance.Brightness(im)
                im = obj.enhance(brightness_factor)

            try:
                im.save('./'+experiment+'/'+n_circles+'/'+str(global_img_i)+img_extension)
            except:
                os.mkdir('./'+n_circles)
                im.save('./'+experiment+'/'+n_circles+'/'+str(global_img_i)+img_extension)

            global_img_i += 1
