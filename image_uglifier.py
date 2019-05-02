import os
import numpy as np
import pandas as pd
import scipy
from imageio import imread, imsave
from scipy import ndarray
from collections import OrderedDict
import skimage as sk
from skimage import transform
from skimage import util
import random

class uglifier():

    def __init__(self):
        self.available_tranforms = OrderedDict({
            'gaussian_blur':self.gaussian_blur,
            'down_sample':self.down_sample,
            'random_noise':self.random_noise,
            'up_sample':self.up_sample,
            })

    def random_noise(self, image_array: ndarray) -> ndarray:
        sigma=0.1
        noisy = sk.util.random_noise(image_array, mode='speckle', var=sigma**2, clip=False)
        sigma=0.12
        return sk.util.random_noise(noisy, var=sigma**2, clip=False)

    def gaussian_blur(self, image_array: ndarray) -> ndarray:
        return sk.filters.gaussian(image_array,sigma=1, preserve_range=True)

    def up_sample(image):
        return transform.rescale(image, 5.0/1.0, anti_aliasing=False)

    def down_sample(self, image):
        return transform.rescale(image, 1.0/4.0, anti_aliasing=False)
        
    def apply_transforms(self, image):
        transformed_image = image
        for key, func in self.available_tranforms.items():
            #deformed[key]=func(image)
            transformed_image = func(transformed_image) 
        return transformed_image

class find_modify_save():

    def __init__(self, dir_path, originals_folder, save_folder, id_depth):
        self.dir_path = dir_path
        self.orginals_folder = originals_folder
        self.save_folder = save_folder
        self.id_depth = id_depth
    
    def get_image(self):
        path = os.path.join(self.dir_path, self.orginals_folder)
        for root, dirs, files in os.walk(path):
            for file in files:
                yield root, file

    def run(self):
        make_ugly = uglifier()

        for root, file in self.get_image():
            file_path = os.path.join(root, file)
            id_path = file_path.split(os.sep)[self.id_depth:]
            id_path = os.path.join(*id_path)
            self.current_id_path = id_path
            #print(id_path)
            save_to = os.path.join(self.dir_path, self.save_folder, id_path)
            #print(os.path.basename(save_to))
            #print(os.path.dirname(save_to))

            image = imread(file_path)
            ugly_image = make_ugly.apply_transforms(image)
            
            # checks if directory exists and if not makes the directory
            if not os.path.exists(os.path.dirname(save_to)):
                os.makedirs(os.path.dirname(save_to))
            
            imsave(save_to, ugly_image)

if __name__ == '__main__':
    dir_path =r'/Volumes/GoogleDrive/My Drive/!NIH MRSP/Research with MIP/Projects/Super_Resolution/Automate_Super_Res_DB'
    originals_folder = 'jpg'
    save_folder = 'ugly_jpg'
    id_depth = -3
    
    ugly_images = find_modify_save(dir_path, originals_folder, save_folder, id_depth)
    ugly_images.run()
