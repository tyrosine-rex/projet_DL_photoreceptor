# +/- niveaux de gris mais ne pas borner en 0 ou en 255, car arrive souvent en pratique (mouches plus vieilles par exemple)
# translations légères

import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import math as m
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import random as r
import os
import sys
import shutil
from PIL import ImageEnhance

n_img_train = 1000
n_img_test = 500
classes = [str(i) for i in range(10)]
expdirs = ['training', 'testing']
img_extension = '.png'
augmented_prefix = 'aug_'
dim = 60
global_img_i_train = 0
global_img_i_test = 0
min_translation = 0
max_translation = 5
names = ['']
name = ''

# print('sys.argv:', sys.argv)

# Define directory to augment, which contains class folders
if len(sys.argv) > 1:
    dir_to_augment = sys.argv[1]
else:
    print('Please specify a directory containing experiments and classes')
print('dir_to_augment:', dir_to_augment)

# Define target directory
if len(sys.argv) > 2:
    target_dir = sys.argv[2]
else:
    target_dir = './data_aug_target'
print('target_dir:', target_dir)

# Create target directory if it does not exist
try:
    print('Creating directory:', target_dir)
    os.mkdir(target_dir)
except:
    pass

for expdir in expdirs:
    # Create testing / training directories
    tgt_dir = augmented_prefix+expdir
    full_tgt_dir = target_dir+'/'+tgt_dir
    if not tgt_dir in expdirs:
        print('Creating directory:', full_tgt_dir)
        try:
            os.mkdir(full_tgt_dir)
        except:
            print('Experiment directory already exists')
        for i in range(10):
            print('Creating directory:', full_tgt_dir+'/'+str(i))
            try:
                os.mkdir(full_tgt_dir+'/'+str(i))
            except:
                print('Class directory already exists')
    else:
        print('Target directory already exists:', full_tgt_dir)

# Generate augmented image sets from existing images
for expdir in expdirs:
    if expdir == 'training':
        print('expdir:', expdir)

        # For each class folder, copy images and generate some if necessary
        for classdir in os.listdir(dir_to_augment):
            full_source_dir = dir_to_augment+'/'+classdir
            full_dest_dir = target_dir+'/'+augmented_prefix+expdir+'/'+classdir
            print('source, dest:', full_source_dir, full_dest_dir)

            # Get the paths of the existing images
            class_vignettes = os.listdir(full_source_dir)
            print(len(class_vignettes), 'class_vignettes')

            # Copy all exsiting images into the augmented directory without any change
            if len(class_vignettes) > 0:
                for img_file in class_vignettes:
                    vignette = Image.open(full_source_dir+'/'+img_file)
                    final = vignette
                    while name in names:
                        name = str(r.randint(1000000,9999999))
                    final.save(target_dir+'/'+augmented_prefix+expdirs[0]+'/'+classdir+'/'+str(name)+img_extension)
                    names.append(name)

                    # global_img_i_train += 1

                # As long as there are not enough images, create new ones randomly
                if n_img_train > len(class_vignettes):
                    for i in range(len(class_vignettes), n_img_train):
                        # class_vignettes = os.listdir(full_source_dir)

                        # Randomly choose an image
                        idx_choice = r.randint(0, len(class_vignettes)-1)
                        print(i, '(train) idx_choice', idx_choice)

                        vignette = Image.open(full_source_dir+'/'+class_vignettes[idx_choice])
                        
                        # print(len(class_vignettes))
                        # print(class_vignettes[idx_choice])
                
                        rotated = vignette.rotate(r.randint(-180, 180))
                        final = rotated

                        # Save final image in the training directory and its mirror in the testing directory
                        while name in names:
                            name = str(r.randint(1000000,9999999))

                        if r.randint(0, 1) == 1:
                            final.save(target_dir+'/'+augmented_prefix+expdirs[0]+'/'+classdir+'/'+str(name)+img_extension)
                        else:
                            ImageOps.mirror(final).save(target_dir+'/'+augmented_prefix+expdirs[0]+'/'+classdir+'/'+str(name)+img_extension)
                        names.append(name)

                        # global_img_i_train += 1

                # Generate test images
                for i in range(n_img_test):
                    # class_vignettes = os.listdir(full_source_dir)

                    # Randomly choose an image
                    idx_choice = r.randint(0, len(class_vignettes)-1)
                    print(i, '(test) idx_choice', idx_choice)

                    vignette = Image.open(full_source_dir+'/'+class_vignettes[idx_choice])
                    
                    # print(len(class_vignettes))
                    # print(class_vignettes[idx_choice])
            
                    rotated = vignette.rotate(r.randint(-180, 180))
                    final = rotated

                    # Save final image in the training directory and its mirror in the testing directory
                    while name in names:
                        name = str(r.randint(1000000,9999999))

                    if r.randint(0, 1) == 1:
                        final.save(target_dir+'/'+augmented_prefix+expdirs[1]+'/'+classdir+'/'+str(name)+img_extension)
                    else:
                        ImageOps.mirror(final).save(target_dir+'/'+augmented_prefix+expdirs[1]+'/'+classdir+'/'+str(name)+img_extension)
                    names.append(name)

                    # global_img_i_train += 1

# print('global_img_i:', global_img_i)

# for experiment in expdirs:
#     # Create testing / training directories if they do not exist
#     try:
#         os.mkdir(experiment)
#     except:
#         pass

#     # Create a directory for each class in the experiment directory
#     for i in range(len(classes)):
#         try:
#             os.mkdir('./'+experiment+'/'+str(classes[i]))
#         except:
#             pass
