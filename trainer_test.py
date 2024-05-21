import os
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models, optimizers

# Directory setup
external_drive = '/Volumes/Extra HardD'
base_dir = os.path.join(external_drive, 'dog_images')
breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']
images_needed = 1000

# Function to create directories for training, validation, and test sets
def create_split_directories():
    for split in ['train', 'validation', 'test']:
        split_dir = os.path.join(base_dir, split)
        if not os.path.exists(split_dir):
            os.mkdir(split_dir)
        for breed in breeds:
            breed_dir = os.path.join(split_dir, breed)
            if not os.path.exists(breed_dir):
                os.mkdir(breed_dir)

def split_data():
    create_split_directories()
    for breed in breeds:
        breed_dir = os.path.join(base_dir, breed)
        images = [img for img in os.listdir(breed_dir) if not img.startswith("._")]  # Skip hidden files
        np.random.shuffle(images)
        train_split = int(0.7 * len(images))
        val_split = int(0.15 * len(images))
        for i, image in enumerate(images):
            if i < train_split:
                dest_dir = os.path.join(base_dir, 'train', breed)
            elif i < train_split + val_split:
                dest_dir = os.path.join(base_dir, 'validation', breed)
            else:
                dest_dir = os.path.join(base_dir, 'test', breed)
            shutil.copy(os.path.join(breed_dir, image), os.path.join(dest_dir, image))

# Split the data
split_data()

# Custom data generator with error handling
def create_safe_data_generator(data_generator):
    for batch in data_generator:
        try:
            yield batch
        except Exception as e:
            print(f"Error in data generator: {e}")
            continue

# Image data generator with data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Flow from directory
train_generator = train_datagen.flow_from_directory(
    os.path.join(base_dir, 'train'),
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    os.path.join(base_dir, 'validation'),
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    os.path.join(base_dir, 'test'),
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Load the pre-trained model
conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

# Freeze the convolutional base
conv_base.trainable = False

# Build the model
model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(len(breeds), activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(learning_rate=2e-5),
              metrics=['accuracy'])

# Train the model with custom data generator
history = model.fit(
    create_safe_data_generator(train_generator),
    steps_per_epoch=100,  # Adjust based on your dataset size
    epochs=30,
    validation_data=create_safe_data_generator(validation_generator),
    validation_steps=50  # Adjust based on your dataset size
)

# Evaluate the model
test_loss, test_acc = model.evaluate(create_safe_data_generator(test_generator), steps=50)
print(f"Test accuracy: {test_acc}")

# Save the model
model.save('dog_breed_classifier.h5')
