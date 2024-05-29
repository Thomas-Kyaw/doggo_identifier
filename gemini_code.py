import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# 1. Load and Preprocess the Dataset (from TFDS)
(train_ds, val_ds, test_ds), ds_info = tfds.load(
    'stanford_dogs', 
    split=['train', 'test[:50%]', 'test[50%:]'],
    shuffle_files=True,
    as_supervised=True,  
    with_info=True
)

def preprocess_image(image, label):
    image = tf.image.resize(image, (224, 224))  
    image = image / 255.0  
    return image, label

train_ds = train_ds.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE).batch(32).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE).batch(32).prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE).batch(32).prefetch(tf.data.AUTOTUNE)


# 2. Build the Model (Transfer Learning with VGG16)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(120, activation='softmax')(x) 

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 3. Train the Model (Initial Training)
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)  # Early stopping to prevent overfitting

history = model.fit(
    train_ds,
    epochs=10,                
    validation_data=val_ds,
    callbacks=[early_stop]
)

# 4. Fine-tuning (Unfreeze some layers)
for layer in base_model.layers[-5:]:  # Unfreeze the last 5 layers
    layer.trainable = True

# Recompile with a lower learning rate for fine-tuning
model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(1e-5), metrics=['accuracy'])

# Train the model again (fine-tuning)
history_fine = model.fit(
    train_ds,
    epochs=5,                 
    validation_data=val_ds,
    callbacks=[early_stop]
)

# 5. Evaluate the Model
test_loss, test_acc = model.evaluate(test_ds)
print('Test accuracy:', test_acc)

# 6. Save and Load the Model
model.save('dog_breed_model.h5')  # Save the model
# later...
# loaded_model = load_model('dog_breed_model.h5')  # Load the model
