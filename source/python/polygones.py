##
# 50 images / classe (300 total), couleur homogène, png, 60px : 0.3367
# 50 images / classe (300 total), couleur hétérogène, png, 60px : 0.2500
##

import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import math as m
import numpy as np
from PIL import Image, ImageFilter, ImageOps
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

# n_img = 1000
n_img = 500 # int(310/6) = 51
homogeneous = False

experiments = ('training', 'testing')
global_img_i = 0
used_img_i = []
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
blur_radius = 1
o = -x
min_intensity = 40
max_intensity = 220
if homogeneous:
    min_intensity = max_intensity = 200 # augmente nettement la précision ! (> 95% vs 65% avec des fluctiations)

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
        for img_i in range(n_img):
            image = Image.new('L', (dim, dim))
            draw = ImageDraw.Draw(image)

            centers_translated = [(center[0] + dim/2, center[1] + dim/2) for center in centers]
            polygons = [[] for i in range(len(centers_translated))]

            # Build a polygon around each center
            for i in range(len(centers_translated)):
                for j in range(1, n_vertices+1):
                    poly_point = []
                    for item in zip(pol2cart(width, j*2*m.pi/n_vertices), (centers_translated[i][0], centers_translated[i][1])):
                        poly_point.append(sum(item))
                    poly_point = tuple(poly_point)
                    polygons[i].append(poly_point)
                polygons[i].append(polygons[i][0])

            # maliste = [True if i < n_circles_det[img_i] else False for i in range(len(centers))]
            maliste = [True if i < k else False for i in range(len(centers))]
            p = r.sample(maliste, len(maliste))
            # print(sum(p), p)
            for i in range(len(polygons)):
                if p[i]:
                    draw.polygon((polygons[i]), fill=r.randint(min_intensity, max_intensity))
            n_circles = str(sum(p))
            # print(n_circles)

            rotated = image.rotate(r.randint(-180, 180))
            blurred = rotated.filter(ImageFilter.BoxBlur(blur_radius))
            final = blurred
            if experiment == 'testing':
                final = ImageOps.mirror(final)

            try:
                final.save('./'+experiment+'/'+n_circles+'/'+str(global_img_i)+img_extension)
            except:
                os.mkdir('./'+n_circles)
                final.save('./'+experiment+'/'+n_circles+'/'+str(global_img_i)+img_extension)

            global_img_i += 1
