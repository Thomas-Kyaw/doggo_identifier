import os
from PIL import Image

# Directory setup
base_dir = os.path.expanduser("~/Downloads/dog_images")
breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']
target_size = (224, 224)  # Specify the target resolution for resizing
output_base_dir = os.path.expanduser("~/Downloads/prep_images")

# Function to resize and save the image
def resize_and_save(img_path, output_path, size):
    try:
        img = Image.open(img_path)
        img = img.convert('RGB')  # Convert to RGB mode
        img = img.resize(size)
        img.save(output_path, "JPEG", quality=90)
    except Exception as e:
        print(f"Error processing image {img_path}: {e}")

# Function to prepare the data
def prepare_data():
    for breed in breeds:
        print(f"Processing {breed} images...")
        breed_dir = os.path.join(base_dir, breed)
        output_dir = os.path.join(output_base_dir, breed)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        image_files = os.listdir(breed_dir)
        num_images = len(image_files)
        
        for i, img_file in enumerate(image_files):
            img_path = os.path.join(breed_dir, img_file)
            output_filename = f"{breed}_{i+1:04d}.jpg"  # Format: breed_0001.jpg
            output_path = os.path.join(output_dir, output_filename)
            
            resize_and_save(img_path, output_path, target_size)
            
        print(f"Processed {num_images} images for {breed}")

# Main function
def main():
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)
    
    prepare_data()
    print("Data preparation completed.")

if __name__ == "__main__":
    main()
    