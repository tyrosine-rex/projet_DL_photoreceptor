# forme des PR : contours moins circulaires
# VGG : supprimer les dernières couches et les remplacer par des couches correspondant aux classes des nombres de photorécepteurs

import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import math as m
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops
import random as r
import os
import sys

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

if len(sys.argv) > 1:
    print(sys.argv[1])
    target_dir = './'+sys.argv[1]+'/'
else:
    target_dir = './'

print('target_dir', target_dir)

try:
    os.mkdir(target_dir)
except FileExistsError:
    print('Directory already exists, nothing was done')

homogeneous = True
n_img = 30

# experiments = ('training', 'testing')
global_img_i = 0
# used_img_i = []
# dim = 32
dim = 60
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


img_extension = '.png'
o = -x
min_angle = -180
max_angle = 180
min_intensity = 100
max_intensity = 255
if homogeneous:
    min_intensity = max_intensity
change_blur = True
blur_radius = 1.5
change_brightness = True
min_brightness_factor = 0.4
max_brightness_factor = 1.0
change_offset = True
min_offset = -dim//10
max_offset = dim//10

centers = ((0+o, 0+o), (0+o, x+o), (x+o-dx, 1.5*x+o), (2*x+o-2*dx, 0+o), (2*x+o-2*dx, x+o), (2*x+o-2*dx, 2*x+o))

for i in range(len(n_circles_det)):
    if n_circles_det[i] < 1:
        n_circles_det[i] = 1
    elif n_circles_det[i] > 6:
        n_circles_det[i] = 6
# print(n_circles_det)

# for experiment in experiments:
    # # Create testing / training directories if they don't exist
    # try:
    #     os.mkdir(experiment)
    # except:
    #     pass

# Create a directory for each class if it doesn't exist
for i in range(10):
    dir_to_create = target_dir+str(i)
    try:
        os.mkdir(dir_to_create)
    except FileExistsError:
        print(dir_to_create, 'already exists')

# For each biologically realistic class (i.e. 1 to 6 included)
for k in range(1, 7):
    # Randomly generate <n_img> vignettes from the existing ones
    for img_i in range(n_img):
        center_sizes = np.random.normal(width*0.8, width*0.05, 6)
        # center_offsets = np.random.normal(0, dim//55, 6)
        center_offsets = np.random.normal(0, 0, 6)

        # offset = r.uniform(min_offset, max_offset)
        offset = 0
        # brightness_factor = r.uniform(min_brightness_factor, max_brightness_factor)
        brightness_factor = 1

        image = Image.new('L', (dim, dim))
        draw = ImageDraw.Draw(image)

        centers_translated = [(center[0] + dim/2 + offset, center[1] + dim/2 + offset) for center in centers]
        # polygons = [[] for i in range(len(centers_translated))]
        polygons = []

        # Build a polygon around each center
        for i in range(len(centers_translated)):
            polygons.append([])
            for j in range(1, n_vertices+1):
                poly_point = []
                for item in zip(pol2cart(center_sizes[i], j*2*m.pi/n_vertices), (centers_translated[i][0] + center_offsets[i], centers_translated[i][1])):
                    poly_point.append(sum(item))
                poly_point = tuple(poly_point)
                polygons[i].append(poly_point)
            polygons[i].append(polygons[i][0])
            
            # Ellipse
            # w, h = dim/2.5, dim/2.5
            # # shape = [(35, 20), (w - 10, h - 10)]
            # shape = [(20*i,10*i), (w - 10, h - 10)]
            # # polygons[i].append(shape)
            # polygons.append(shape)

        maliste = [True if i < k else False for i in range(len(centers))]
        p = r.sample(maliste, len(maliste))
        # print(sum(p), p)
        for i in range(len(polygons)):
            if p[i]:
                draw.polygon((polygons[i]), fill=r.randint(min_intensity, max_intensity))
                # draw.ellipse(polygons[i], fill=r.randint(min_intensity, max_intensity))
        n_circles = str(sum(p))
        # print(n_circles)

        im = image.rotate(r.randint(min_angle, max_angle))
        if change_blur:
            im = im.filter(ImageFilter.GaussianBlur(blur_radius))
        if change_offset:
            im = ImageChops.offset(im, r.randint(min_offset, max_offset), r.randint(min_offset, max_offset))
        if change_brightness:
            obj = ImageEnhance.Brightness(im)
            im = obj.enhance(brightness_factor)
        
        imm = ImageOps.mirror(im)

        try:
            if r.randint(0,1) == 1:
                im.save(target_dir+n_circles+'/'+str(global_img_i)+''+img_extension)
            else:
                imm.save(target_dir+n_circles+'/'+str(global_img_i)+''+img_extension)
        except:
            os.mkdir('./'+n_circles)
            if r.randint(0,1) == 1:
                im.save(target_dir+n_circles+'/'+str(global_img_i)+''+img_extension)
            else:
                imm.save(target_dir+n_circles+'/'+str(global_img_i)+''+img_extension)

        global_img_i += 1
