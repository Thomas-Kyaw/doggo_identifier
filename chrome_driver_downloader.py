import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Directory setup
base_dir = os.path.expanduser("~/Downloads/dog_images")
breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']
images_needed = 1500

# Selenium setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def create_directories():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    for breed in breeds:
        breed_dir = os.path.join(base_dir, breed)
        if not os.path.exists(breed_dir):
            os.mkdir(breed_dir)

def download_image(img_url, breed, count):
    breed_dir = os.path.join(base_dir, breed)
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(os.path.join(breed_dir, f"{breed}_{count}.jpg"), 'wb') as handler:
                handler.write(response.content)
            print(f"Downloaded image {count} for {breed}")
        else:
            print(f"Failed to download image {count} for {breed}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image {count} for {breed}: {e}")

def fetch_images_from_google(breed, start_count, count=images_needed):
    driver.get(f"https://www.google.com/search?q={breed}&tbm=isch")
    time.sleep(2)  # Give time for images to load

    # Scroll to load more images
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Get image URLs
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all('img', {'class': 'rg_i'})
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

    # Filter out invalid URLs
    img_urls = [url for url in img_urls if url.startswith('http')]

    # Download images
    for i, url in enumerate(img_urls):
        if i >= count:
            break
        download_image(url, breed, start_count + i)

def get_existing_image_count(breed):
    breed_dir = os.path.join(base_dir, breed)
    if os.path.exists(breed_dir):
        return len([f for f in os.listdir(breed_dir) if f.endswith('.jpg')])
    return 0

def main():
    create_directories()
    for breed in breeds:
        existing_images = get_existing_image_count(breed)
        if existing_images < images_needed:
            print(f"Fetching images for {breed}")
            fetch_images_from_google(breed, existing_images, images_needed - existing_images)
            print(f"Downloaded additional images for {breed}")
        else:
            print(f"Skipping {breed} as it already has {existing_images} images")

if __name__ == "__main__":
    main()
    driver.quit()
