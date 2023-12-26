import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def download_images(url, save_folder):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')

        for img_tag in img_tags:
            img_url = img_tag.get('src')
            img_url = urljoin(url, img_url)

            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                # Extracting the image file name from the URL
                img_filename = os.path.join(save_folder, os.path.basename(img_url))
                
                with open(img_filename, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded: {img_filename}")
            else:
                print(f"Failed to download image from {img_url}")
    else:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")

# URL of the page with images
url = 'https://books.toscrape.com/catalogue/category/books/science_22/index.html'
# Folder to save the images
save_folder = 'book_images'

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Call the function to download images
download_images(url, save_folder)
