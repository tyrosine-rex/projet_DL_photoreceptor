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

n_img_train = 111
n_img_test = 111
classes = [str(i) for i in range(10)]
experiments = ['training', 'testing']
img_extension = '.png'
augmented_prefix = 'aug_'
dim = 60
global_img_i = 0
min_translation = 0
max_translation = 5

print('len(sys.argv):', len(sys.argv))

if len(sys.argv) > 1:
    dir_to_augment = sys.argv[1]
else:
    print('Please specify a directory containing experiments and classes')

print('dir_to_augment:', dir_to_augment)

if len(sys.argv) > 2:
    dir_to_augment = sys.argv[2]
else:
    target_dir = './data_aug_target'

expdirs = experiments
print(expdirs)

# Create target directory if it does not exist
try:
    print('Creating directory:', target_dir)
    os.mkdir(target_dir)
except:
    pass
# # Create a directory for each class at the root of the target directory
# for i in range(len(classes)):
#     try:
#         print('Creating directory:', target_dir+'/'+str(classes[i]))
#         os.mkdir(target_dir+'/'+str(classes[i]))
#     except:
#         pass

for expdir in experiments:
    # Create testing / training directories
    tgt_dir = augmented_prefix+expdir
    # full_tgt_dir = dir_to_augment+'/'+tgt_dir
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

for expdir in experiments:
    # Generate augmented image sets from a batch of training images
    if expdir == 'training':
        print('expdir:', expdir)

        # For each class folder in training set, copy images and generate some if necessary
        # for classdir in os.listdir(dir_to_augment+'/'+expdir):
        for classdir in os.listdir(dir_to_augment):
            # full_source_dir = dir_to_augment+'/'+expdir+'/'+classdir
            full_source_dir = dir_to_augment+'/'+classdir
            # full_dest_dir = dir_to_augment+'/'+augmented_prefix+expdir+'/'+classdir
            full_dest_dir = target_dir+'/'+augmented_prefix+expdir+'/'+classdir
            print('source, dest:', full_source_dir, full_dest_dir)

            # Generate images
            class_vignettes = os.listdir(full_source_dir)
            print(len(class_vignettes), 'class_vignettes')
            if len(class_vignettes) > 0:
                # Copy all exsiting images into the augmented directory
                for img_file in class_vignettes:
                    vignette = Image.open(full_source_dir+'/'+img_file)
                    final = vignette
                    final.save(target_dir+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'o'+'d'+img_extension)
                    ImageOps.mirror(final).save(target_dir+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'o'+'m'+img_extension)
                    # shutil.copyfile(full_source_dir+'/'+img_file, full_dest_dir+'/'+str(global_img_i)+img_extension)
                    global_img_i += 1

                # As long as there are not enough images, create new ones randomly
                for i in range(len(class_vignettes), n_img_train):
                    # class_vignettes = os.listdir(full_source_dir)

                    # Randomly choose an image
                    idx_choice = r.randint(0, len(class_vignettes)-1)
                    print(i, 'idx_choice', idx_choice)

                    vignette = Image.open(full_source_dir+'/'+class_vignettes[idx_choice])
                    
                    print(len(class_vignettes))
                    print(class_vignettes[idx_choice])
            
                    rotated = vignette.rotate(r.randint(-180, 180))
                    final = rotated

                    # enhancer = ImageEnhance.Sharpness(final)
                    # for i in range(4):
                    #     factor = i
                    #     enhancer.enhance(factor).show(f"Sharpness {factor:f}")
                    # break

                    # Save final image in the training directory and its mirror in the testing directory
                    # final.save(dir_to_augment+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'d'+img_extension)
                    # ImageOps.mirror(final).save(dir_to_augment+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'m'+img_extension)
                    final.save(target_dir+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'ad'+img_extension)
                    ImageOps.mirror(final).save(target_dir+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+'am'+img_extension)

                    global_img_i += 1

                for i in range(len(class_vignettes), n_img_test):
                    # class_vignettes = os.listdir(full_source_dir)

                    # Randomly choose an image
                    idx_choice = r.randint(0, len(class_vignettes)-1)
                    print(i, 'idx_choice', idx_choice)

                    vignette = Image.open(full_source_dir+'/'+class_vignettes[idx_choice])
                    
                    print(len(class_vignettes))
                    print(class_vignettes[idx_choice])
            
                    rotated = vignette.rotate(r.randint(-180, 180))
                    final = rotated

                    # enhancer = ImageEnhance.Sharpness(final)
                    # for i in range(4):
                    #     factor = i
                    #     enhancer.enhance(factor).show(f"Sharpness {factor:f}")
                    # break

                    final2 = Image.asarray(final)

                    # Save final image in the training directory and its mirror in the testing directory
                    if r.randint(0, 1) == 1:
                        final2.save(target_dir+'/'+augmented_prefix+experiments[1]+'/'+classdir+'/'+str(global_img_i)+'_conv'+img_extension)
                    else:
                        ImageOps.mirror(final2).save(target_dir+'/'+augmented_prefix+experiments[1]+'/'+classdir+'/'+str(global_img_i)+'_conv'+img_extension)

                    global_img_i += 1

print('global_img_i:', global_img_i)

# for experiment in experiments:
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
