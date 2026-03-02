#Smart Sugarcane Disease Detection using & Solution System AI Project
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import cv2
import numpy as np


# Image Preprocessing 
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
    "C:\\Users\\LENOVO\\Desktop\\sugarncne_dataset\\train",
    target_size=(128,128),
    batch_size=32,
    class_mode='categorical')

test_set = test_datagen.flow_from_directory(
    "C:\\Users\\LENOVO\\Desktop\\sugarncne_dataset\\test",
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical')

#CNN Model
model = Sequential()

model.add(Conv2D(32,(3,3),input_shape=(128,128,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64,(3,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128,(3,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4,activation='softmax'))

#Compile
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

#Train CNN Model
history = model.fit(
    training_set,
    steps_per_epoch=200 // 32,
    epochs=10,
    validation_steps=200 // 32,
    validation_data=test_set)

#Accuracy & Loss Graph
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(['Train Accuracy','Validation Accuracy'])
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(['Train Loss','Validation Loss'])
plt.show()

#Save & Load Model
model.save("sugarcane_model.h5")

# Predict Using Opencv
model = tf.keras.models.load_model("sugarcane_model.h5")


img_path = "c:\\Users\\LENOVO\\Desktop\\Image\\IMG_20260227_114612_1.jpg"   # image upload

# Load & preprocess image
img = cv2.imread(img_path)
img = cv2.resize(img,(128,128))
img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
img = img / 255.0
img = np.expand_dims(img,axis=0)

# Clear Image
img_show = cv2.imread(img_path)
img_show = cv2.cvtColor(img_show, cv2.COLOR_BGR2RGB)

# Image Prediction
prediction = model.predict(img)
class_index = np.argmax(prediction)
confidence = np.max(prediction) * 100

#Solution  System
class_names = ['Healthy', 'Mosaic', 'RedRot', 'Rust']
solutions = {
    "Healthy": "Plant healthy. Use proper irrigation and organic manure.",
    "Mosaic": "Use virus-free seed material. Control aphids using Imidacloprid (0.3 ml/L water).",
    "RedRot": "Remove infected plants. Spray Carbendazim (1g/L water).",
    "Rust": "Spray Mancozeb (2g/L water) every 10 days.",
}
disease = class_names[class_index]
solution = solutions[disease]

#Displaying Result
print("Disease:", disease)
print("Confidence:", round(confidence,2),"%")
print("Solutions:", solution)

# Show Image
plt.imshow(img_show)
plt.title(f"{disease} ({round(confidence,2)}%)")
plt.axis("off")
plt.show()

