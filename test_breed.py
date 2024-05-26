import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model('dog_breed_model_1.h5')

# Define the class labels (dog breeds)
class_labels = ['Dalmatian', 'Greyhound', 'Poodle', 'Samoyed', 'Dachshund']

# Function to preprocess the input image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict the dog breed
def predict_breed(img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]
    return predicted_class

# Get the input image path from the user
image_path = input("Enter the path to the dog image: ")

# Check if the image file exists
if os.path.isfile(image_path):
    # Predict the dog breed
    predicted_breed = predict_breed(image_path)
    print("Predicted dog breed:", predicted_breed)
else:
    print("Image file not found.")
