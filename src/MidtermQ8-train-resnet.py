#!/usr/bin/env python
import os, sys
import matplotlib.pyplot as plt

base_dir = 'Q8-crop-weed-dataset'
train_dir = os.path.join(base_dir, 'training_data')
validation_dir = os.path.join(base_dir, 'testing_data')

# Directory with our training crop pictures
train_crops_dir = os.path.join(train_dir, 'crops')

# Directory with our training weed pictures
train_weeds_dir = os.path.join(train_dir, 'weeds')

# Directory with our validation crop pictures
validation_crops_dir = os.path.join(validation_dir, 'crops')

# Directory with our validation weed pictures
validation_weeds_dir = os.path.join(validation_dir, 'weeds')

# Set up matplotlib fig, and size it to fit 4x4 pics
# import matplotlib.image as mpimg
# nrows = 4
# ncols = 4

# fig = plt.gcf()
# fig.set_size_inches(ncols*4, nrows*4)
# pic_index = 100
# train_crop_fnames = os.listdir( train_crops_dir )
# train_weed_fnames = os.listdir( train_weeds_dir )

# next_crop_pix = [os.path.join(train_crops_dir, fname) 
#                 for fname in train_crop_fnames[ pic_index-8:pic_index] 
#                ]
#
# next_weed_pix = [os.path.join(train_weeds_dir, fname) 
#                 for fname in train_weed_fnames[ pic_index-8:pic_index]
#                ]

# for i, img_path in enumerate(next_crop_pix+next_weed_pix):
#   # Set up subplot; subplot indices start at 1
#   sp = plt.subplot(nrows, ncols, i + 1)
#   sp.axis('Off') # Don't show axes (or gridlines)
#
#   img = mpimg.imread(img_path)
#   plt.imshow(img)

# plt.show()

# Add our data-augmentation parameters to ImageDataGenerator


import tensorflow
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255., rotation_range = 40, width_shift_range = 0.2, height_shift_range = 0.2, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1.0/255.)

train_generator = train_datagen.flow_from_directory(train_dir, batch_size = 40, class_mode = 'binary', target_size = (224, 224))

validation_generator = test_datagen.flow_from_directory( validation_dir, batch_size = 20, class_mode = 'binary', target_size = (224, 224))

from tensorflow.keras.applications import ResNet50

base_model = ResNet50(input_shape=(224, 224,3), include_top=False, weights="imagenet")

for layer in base_model.layers:
    layer.trainable = False

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D

base_model = Sequential()
base_model.add(ResNet50(include_top=False, weights='imagenet', pooling='max'))
base_model.add(Dense(1, activation='sigmoid'))

base_model.compile(optimizer = tensorflow.keras.optimizers.SGD(learning_rate=0.0001), loss = 'binary_crossentropy', metrics = ['acc'])

resnet_history = base_model.fit(train_generator, validation_data = validation_generator, steps_per_epoch = 32, epochs = 10)

base_model.save("model")

