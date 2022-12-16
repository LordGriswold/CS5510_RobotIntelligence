#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import pathlib
import sys, os, glob

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# may need to set target_size = (224, 224)

model = tf.keras.models.load_model("model_karas")

for layer in model.layers:
	if "BatchNormalization" in layer.__class__.__name__:
		layer.trainable=False
		print(f"{layer.weights = }")

class_names = ['crop', 'weed']

for file in glob.glob("Q8-crop-weed-dataset/testing_data/*/*.jpeg"):
	print(f"{file = }")
	img = tf.keras.utils.load_img(
			file, target_size = (224, 224)
	)
	img_array = tf.keras.utils.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0) # Create a batch

	predictions = model.predict(img_array)
	score = tf.nn.softmax(predictions[0])
	rounded = [round(x[0]) for x in predictions]

	print(f"{rounded = }")

	print(f"{np.argmax(score) = }")
	print(f"{np.max(score) = }")

	print(
			f"{file} most likely belongs to {class_names[np.argmax(score)]} with a {(100 * np.max(score)):.2f} percent confidence."
			#.format(class_names[np.argmax(score)], 100 * np.max(score))
	)



	
