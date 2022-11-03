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

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

n_img = 100
classes = [str(i) for i in range(10)]
experiments = ['training', 'testing']
img_extension = '.tif'
augmented_prefix = 'eaug_'
dim = 60
global_img_i = 0

print('len(sys.argv):', len(sys.argv))

if len(sys.argv) > 1:
    dir_to_augment = sys.argv[1]
else:
    print('Please specify a directory containing experiments and classes')

print('dir_to_augment:', dir_to_augment)

# expdirs = os.listdir(dir_to_augment)
expdirs = experiments
print(expdirs)

for expdir in experiments:
    # Create testing / training directories
    tgt_dir = augmented_prefix+expdir
    full_tgt_dir = dir_to_augment+'/'+tgt_dir
    if not tgt_dir in expdirs:
        print('Creating directory:', full_tgt_dir)
        os.mkdir(full_tgt_dir)
        for i in range(10):
            print('Creating directory:', full_tgt_dir+'/'+str(i))
            os.mkdir(full_tgt_dir+'/'+str(i))
    else:
        print('Target directory already exists:', full_tgt_dir)

for expdir in experiments:
    # Generate augmented image sets from a batch of training images
    if expdir == 'training':
        print('expdir:', expdir)

        for classdir in os.listdir(dir_to_augment+'/'+expdir):
            full_classdir = dir_to_augment+'/'+expdir+'/'+classdir
            print(full_classdir)

            class_vignettes = os.listdir(full_classdir)
            # print(len(class_vignettes), 'class_vignettes', class_vignettes)
            if len(class_vignettes) > 0:
                # Copy all exsiting images into the augmented directory
                # for img_file in class_vignettes:
                #     shutil.copyfile(full_classdir)

                # As long as images need to be generated, create new ones randomly
                for i in range(len(class_vignettes), n_img+1):
                    class_vignettes = os.listdir(full_classdir)

                    idx_choice = r.randint(0, len(class_vignettes)-1)
                    print(i, 'idx_choice', idx_choice)

                    vignette = Image.open(full_classdir+'/'+class_vignettes[idx_choice])
                    
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
                    final.save(dir_to_augment+'/'+augmented_prefix+experiments[0]+'/'+classdir+'/'+str(global_img_i)+img_extension)
                    ImageOps.mirror(final).save(dir_to_augment+'/'+augmented_prefix+experiments[1]+'/'+classdir+'/'+str(global_img_i)+img_extension)

                    global_img_i += 1

print('global_img_i:', global_img_i)
        
        # for vignette in os.listdir(full_classdir):
        #     print(vignette)

#     print('expdir', expdir)
#     for img in os.listdir(expdir):
#         print('Current image:', img)



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
