import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the saved model
model = load_model('dog_breed_classifier.h5')

# Directory setup
external_drive = '/Volumes/Extra HardD'
base_dir = os.path.join(external_drive, 'dog_images')

# Create a function to predict the breed of a new image
def predict_breed(model, img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    breed = list(train_generator.class_indices.keys())[predicted_class]
    return breed

# Example usage
img_path = 'path_to_your_image.jpg'
breed = predict_breed(model, img_path)
print(f"The predicted breed is: {breed}")
 