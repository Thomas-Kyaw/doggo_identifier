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
timeout_threshold = 180  # 3 minutes

# Download images for each dog breed
for breed in dog_breeds:
    print(f"Downloading images for breed: {breed}")
    start_time = time.time()
    last_download_time = start_time
    downloaded_images = 0
    prev_downloaded_images = 0

    while downloaded_images < num_images:
        try:
            downloader.download(breed, limit=num_images - downloaded_images, output_dir=output_dir,
                                adult_filter_off=True, force_replace=False, timeout=60)
            downloaded_images = len(os.listdir(os.path.join(output_dir, breed)))

            # Check if new images have been downloaded
            if downloaded_images > prev_downloaded_images:
                prev_downloaded_images = downloaded_images
                last_download_time = time.time()
            else:
                # No new images have been downloaded
                if time.time() - last_download_time > timeout_threshold:
                    print(f"No new images downloaded for breed {breed} in the last {timeout_threshold} seconds. Moving to the next breed.")
                    break

        except Exception as e:
            print(f"Error downloading images for breed {breed}: {str(e)}")

    print(f"Downloaded {downloaded_images} images for breed: {breed}")
    print("------------------------")

print("Image downloading completed.")
