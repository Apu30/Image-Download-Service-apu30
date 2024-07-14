from flask import Flask, jsonify, request, send_from_directory
import os
import requests
from urllib.parse import urlparse

app = Flask(__name__)
IMAGE_STORAGE_DIR = "stored_images"

#Endpoint Logic for downloading the images
@app.route('/upload_image_urls', methods=['POST'])
def upload_image_urls():
    image_urls = request.json.get('image_urls', [])
    saved_images = []
    if not os.path.exists(IMAGE_STORAGE_DIR):
        os.makedirs(IMAGE_STORAGE_DIR)
    for url in image_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_filename = os.path.basename(urlparse(url).path)
                image_filepath = os.path.join(IMAGE_STORAGE_DIR, image_filename)
                with open(image_filepath, 'wb') as image_file:
                    image_file.write(response.content)
                saved_images.append(url)
        except Exception as error:
            print(f"Error downloading {url}: {error}")
    return jsonify({'saved_images': saved_images})

#Endpoint logic for showing the available images
@app.route('/list_images', methods=['GET'])
def list_images():
    if os.path.exists(IMAGE_STORAGE_DIR):
        saved_images = os.listdir(IMAGE_STORAGE_DIR)
    else:
        saved_images = []
    return jsonify({'saved_images': saved_images})

#Endpoint logic for showing the retrieving the image provided in image url
@app.route('/retrieve_image', methods=['GET'])
def retrieve_image():
    image_url = request.args.get('image_url')
    image_filename = os.path.basename(urlparse(image_url).path)
    image_filepath = os.path.join(IMAGE_STORAGE_DIR, image_filename)
    if os.path.exists(image_filepath):
        return send_from_directory(IMAGE_STORAGE_DIR, image_filename)
    else:
        return jsonify({'message': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)