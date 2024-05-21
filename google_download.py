import os
import time
from bing_image_downloader import downloader

# Specify the dog breeds and number of images to download
dog_breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']
num_images = 1000

# Get the path to the Downloads directory on your Mac
downloads_dir = os.path.expanduser("~/Downloads")

# Create a directory for the dog breeds inside the Downloads directory
output_dir = os.path.join(downloads_dir, "dog_breeds")
os.makedirs(output_dir, exist_ok=True)

# Set a timeout threshold (in seconds) for no new image downloads
timeout_threshold = 180  # 5 minutes

# Download images for each dog breed
for breed in dog_breeds:
    print(f"Downloading images for breed: {breed}")
    start_time = time.time()
    last_download_time = start_time
    downloaded_images = 0

    while downloaded_images < num_images:
        try:
            downloader.download(breed, limit=num_images - downloaded_images, output_dir=output_dir,
                                adult_filter_off=True, force_replace=False, timeout=60)
            downloaded_images = len(os.listdir(os.path.join(output_dir, breed)))
            last_download_time = time.time()
        except Exception as e:
            print(f"Error downloading images for breed {breed}: {str(e)}")

        # Check if no new images have been downloaded for the specified timeout threshold
        if time.time() - last_download_time > timeout_threshold:
            print(f"No new images downloaded for breed {breed} in the last {timeout_threshold} seconds. Moving to the next breed.")
            break

    print(f"Downloaded {downloaded_images} images for breed: {breed}")
    print("------------------------")

print("Image downloading completed.")