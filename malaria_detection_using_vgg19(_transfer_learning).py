# -*- coding: utf-8 -*-
"""Malaria Detection using VGG19( Transfer Learning)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hzPnkNeoI3dMZIK46A2dj7tuOQODo3B3
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os

train_path="/content/gdrive/My Drive/Dataset/Train"
test_path="/content/gdrive/My Drive/Dataset/Test"
class_names=os.listdir(train_path)
class_names_test=os.listdir(test_path)

class_names

# import the libraries as shown below

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten,Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

# re-size all the images to this
IMAGE_SIZE = [224, 224]

vgg19 = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg19.layers:
    layer.trainable = False

folders = glob('/content/gdrive/My Drive/Dataset/Train/*')

folders

x = Flatten()(vgg19.output)

prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg19.input, outputs=prediction)

model.summary()

from tensorflow.keras.layers import MaxPooling2D

### Create Model from scratch using CNN
model=Sequential()
model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(224,224,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation ="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dense(2,activation="softmax"))
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/gdrive/My Drive/Dataset/Train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/gdrive/My Drive/Dataset/Test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# fit the model
# Run the cell. It will take some time to execute
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=20,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

from tensorflow.keras.models import load_model

model.save('model_vgg19.h5')

y_pred = model.predict(test_set)

import numpy as np
y_pred = np.argmax(y_pred, axis=1)

y_pred

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model=load_model('model_vgg19.h5')

"""**Testing model on a test image**"""

img=image.load_img('C3thin_original_IMG_20150608_162922_cell_145.png',target_size=(224,224))

x=image.img_to_array(img)
x

x.shape

x=x/255

x=np.expand_dims(x,axis=0)
img_data=preprocess_input(x)
img_data.shape

model.predict(img_data)

a=np.argmax(model.predict(img_data), axis=1)

if(a==1):
    print("Uninfected")
else:
    print("Infected")

