import keras
from keras import layers, models
from keras.datasets import mnist

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# load data
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# explore the data
print(train_images.shape)
print(test_images.shape)
print(train_labels.shape)

# Image
IMAGE_INDEX = 1500
plt.imshow(train_images[IMAGE_INDEX], cmap=plt.cm.binary)
plt.show()

train_labels[IMAGE_INDEX]
train_images[1]


# 1) Prepare Data
train_images = train_images.reshape((60000, 28 * 28))
test_images = test_images.reshape((10000, 28 * 28))
train_images.shape

'''train_images = train_images.astype("float32") / 255.0
test_images = test_images.astype("float32") / 255.0'''


# 2) Scale the inputs-data from 0-225 -> 0-1
train_images = train_images / 255.0
test_images = test_images / 255.0


# 3) prepare labels -> one-hot-encoding
"""
Input [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Output
 - [1, 0, 0, 0, 0, 0, 0, 0, 0, 0] => 0
 - [0, 1, 0, 0, 0, 0, 0, 0, 0, 0] => 1
 - [0, 0, 1, 0, 0, 0, 0, 0, 0, 0] => 2
 - [0, 0, 0, 1, 0, 0, 0, 0, 0, 0] => 3
 - [0, 0, 0, 0, 1, 0, 0, 0, 0, 0] => 4
 - [0, 0, 0, 0, 0, 1, 0, 0, 0, 0] => 5
 - [0, 0, 0, 0, 0, 0, 1, 0, 0, 0] => 6
 - [0, 0, 0, 0, 0, 0, 0, 1, 0, 0] => 7
 - [0, 0, 0, 0, 0, 0, 0, 0, 1, 0] => 8
 - [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] => 9

"""

train_labels = to_categorical(train_labels)

# test_labels = to_categorical(test_labels)

# 4) Build the model

ACTIVATION_FUNCTION = 'sigmoid'

model = models.Sequential([
    # INPUT LAYER (primera capa -izq-)
    keras.Input(shape=(28 * 28,)),

    # 1 hidden layer (capa oculta)
    #                   q tantas neuronas, que tipo de activacion, nombre de la capa
    keras.layers.Dense(512, activation=ACTIVATION_FUNCTION, name= "First_hidden_layer"),

    # 2 hidden layer (capa oculta)
    keras.layers.Dense(128, activation=ACTIVATION_FUNCTION),

    # 3 output layer (capa de salida)
    keras.layers.Dense(10, activation=ACTIVATION_FUNCTION),


])
"""layers.Dropout(0.2),
 layers.Dense(10, activation='softmax')"""

# sumario del modelo
model.summary()

# compilacion del modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

## training Fase

# entrenamiento del modelo                      -para q sea mas random

"""model.fit(train_images, train_labels, epochs=5, shuffle=True)
print("\nFinished training the model...\n")
model.fit(train_images, train_labels, epochs=5, shuffle=True, validation_split=0.2)
"""

version = model.fit(train_images, train_labels, epochs=5, shuffle=True, validation_split=0.2)

# plotten
plt.plot(version.history['accuracy'])
plt.plot(version.history['val_accuracy'])
plt.legend(['Training_acc', 'Validation_accuracy'])
plt.title('\nModel Accuracy\n')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()


# Predictions
predict = model.predict(test_images)

rounded_pred = np.argmax(predict, axis=1)
for i in rounded_pred:
    print(i)


# Confusion MAtrix
cm = confusion_matrix(test_labels, rounded_pred)
display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.arange(10))
display.plot(cmap="Blues", values_format="d")
plt.title("Confusion Matrix")
plt.show()