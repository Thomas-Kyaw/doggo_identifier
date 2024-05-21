from PIL import Image
import os

# Function to convert images to JPEGP
def convert_images_to_jpeg():
    for breed in breeds:
        breed_dir = os.path.join(base_dir, breed)
        for file_name in os.listdir(breed_dir):
            if file_name.startswith("._"):  # Skip hidden files
                continue
            file_path = os.path.join(breed_dir, file_name)
            try:
                img = Image.open(file_path)
                rgb_img = img.convert('RGB')
                rgb_img.save(file_path, format='JPEG')
                print(f"Converted {file_name} to JPEG")
            except Exception as e:
                print(f"Error converting {file_name}: {e}")

# Directory setup
base_dir = '/Volumes/Extra HardD/dog_images'
breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']

# Convert all images to JPEG
convert_images_to_jpeg()
