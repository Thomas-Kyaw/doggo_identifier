import os
import requests
import flickrapi
import time

# Directory setup
base_dir = os.path.expanduser("~/Downloads/dog_images")
breeds = ['Samoyed', 'Dalmatian', 'Dachshund', 'Greyhound', 'Poodle']
images_needed = 1000

# Unsplash API key
unsplash_access_key = 'lTgblcVeKFaXylPJC4ezvAw9PhoFebvL2g7tXJsGlDg'

# Flickr API setup
flickr_api_key = '5f606aee1df7dca3dd9b9478a5b115fe'
flickr_api_secret = '73ef5339d2955cb5'
flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret, format='parsed-json')

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
        img_data = requests.get(img_url).content
        with open(os.path.join(breed_dir, f"{breed}_{count}.jpg"), 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded image {count} for {breed}")
    except Exception as e:
        print(f"Error downloading image {count} for {breed}: {e}")

def fetch_images_from_unsplash(breed, count=images_needed):
    page = 1
    downloaded = 0
    img_urls = []
    while downloaded < count:
        search_url = f"https://api.unsplash.com/search/photos?query={breed}&client_id={unsplash_access_key}&per_page=30&page={page}"
        try:
            response = requests.get(search_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if 'results' not in data:
                print(f"Unexpected response structure: {data}")
                break
            results = data['results']
            if not results:
                print(f"No more results for {breed}")
                break
            for result in results:
                if downloaded >= count:
                    break
                img_url = result['urls']['small']
                img_urls.append(img_url)
                downloaded += 1
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Request error fetching images for {breed}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error fetching images for {breed}: {e}")
            break
    return img_urls

def fetch_images_from_flickr(breed, count=images_needed):
    img_urls = []
    try:
        photos = flickr.photos.search(text=breed, per_page=count, page=1, media='photos', sort='relevance')
        for photo in photos['photos']['photo']:
            photo_id = photo['id']
            photo_info = flickr.photos.getSizes(photo_id=photo_id)
            for size in photo_info['sizes']['size']:
                if size['label'] == 'Small':
                    img_urls.append(size['source'])
            if len(img_urls) >= count:
                break
    except Exception as e:
        print(f"Error fetching images from Flickr for {breed}: {e}")
    return img_urls

def main():
    create_directories()
    for breed in breeds:
        existing_images = len(os.listdir(os.path.join(base_dir, breed)))
        if existing_images < images_needed:
            print(f"Fetching images for {breed}")
            unsplash_urls = fetch_images_from_unsplash(breed, images_needed - existing_images)
            flickr_urls = fetch_images_from_flickr(breed, images_needed - existing_images - len(unsplash_urls))
            all_urls = unsplash_urls + flickr_urls
            for i, url in enumerate(all_urls):
                download_image(url, breed, existing_images + i)
            print(f"Downloaded additional images for {breed}")

if __name__ == "__main__":
    main()
