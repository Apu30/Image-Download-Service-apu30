import requests
from urllib.parse import urlparse
import os

def extract_image_filename(image_url):
    parsed_url = urlparse(image_url)
    image_path = parsed_url.path
    image_filename = os.path.basename(image_path)
    return image_filename

# Server URL
BASE_URL = 'http://127.0.0.1:5000'

# Endpoint URLs
UPLOAD_IMAGE_URLS = f'{BASE_URL}/upload_image_urls'
LIST_IMAGES_URL = f'{BASE_URL}/list_images'
RETRIEVE_IMAGE_URL = f'{BASE_URL}/retrieve_image'

# Upload the list of image URLs
image_urls = ["https://pngimg.com/uploads/bouquet/bouquet_PNG63.png","https://pngimg.com/uploads/winter/winter_PNG70.png","https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg","https://get.pxhere.com/photo/light-structure-night-monument-evening-landmark-lighting-berlin-brandenburg-gate-906353.jpg"]

# 1. Operation 1: Upload image URLs and download corresponding images
payload = {'image_urls': image_urls}
response = requests.post(UPLOAD_IMAGE_URLS, json=payload)

if response.status_code == 200:
    saved_images = response.json().get('saved_images')
    print("Uploaded images successfully.....")
    print("Downloaded Images are:\n", saved_images)
else:
    print("Failed to upload images")
    print(response.json()) 

# 2. Operation 2: List available images
response = requests.get(LIST_IMAGES_URL)

if response.status_code == 200:
    available_images = response.json().get('saved_images')
    print("\n Available images:")
    print(available_images)
    print("Link to view the list of available images:", LIST_IMAGES_URL)
else:
    print("Failed to list images")

# 3. Operation 3: Retrieve an image
# (change 'image_url' to the desired image URL)
image_url = "https://pngimg.com/uploads/bouquet/bouquet_PNG63.png"
image_filename = extract_image_filename(image_url)

if image_filename in available_images:
    retrieve_params = {'image_url': image_url}
    response = requests.get(RETRIEVE_IMAGE_URL, params=retrieve_params) 

    # Check if retrieving the image was successful
    if response.status_code == 200:
        print("\nRetrieved image successfully......")
        print("Link to retrieve the image:", RETRIEVE_IMAGE_URL + f"?image_url={image_url}")
    else:
        print("Failed to retrieve image")
else:
    print("The specified image URL is not available or hasn't been uploaded previously.")