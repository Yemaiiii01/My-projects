# Main Python script for scraping 
import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape book details
def scrape_book_details(url):
    # Send a GET request to the product page
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the required details
    product_details = {
        'product_page_url': url,
        'universal_product_code': soup.find('th', text='UPC').find_next_sibling('td').text,
        'title': soup.find('div', class_='product_main').h1.text,
        'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
        'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
        'quantity_available': soup.find('th', text='Availability').find_next_sibling('td').text.split('(')[1].split(' ')[0],  # Extracting number from the string
        'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'review_rating': soup.find('p', class_='star-rating')['class'][1],
        'image_url': soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
    }
    
    return product_details

# Define the CSV file name
csv_file = 'book_details.csv'

# Function to save details to CSV
def save_to_csv(data, file_name):
  # Field names for CSV
    fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
              'price_excluding_tax', 'quantity_available', 'product_description', 'category', 
              'review_rating', 'image_url']
    
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerow(data)

# URL of the book to scrape
book_url = "https://books.toscrape.com/catalogue/the-most-perfect-thing-inside-and-outside-a-birds-egg_938/index.html"

# Scrape the book details
book_details = scrape_book_details(book_url)

# Save the book details to CSV
save_to_csv(book_details, csv_file)

print(f"Book details saved to {csv_file}")
import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch book URLs from a single category
def fetch_book_urls(category_url):
    book_urls = []
    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            book_url = book.find('a')['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            book_urls.append(book_url)

        # Check if there is a next page
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_url
        else:
            break
    return book_urls

# Function to scrape book details from Phase 1
def scrape_book_details(url):
    # The rest of the scraping code from Phase 1 goes here
    # ...
    pass  # Replace with the actual scraping code

# The chosen category URL (example: science category)
category_url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'

# Fetch all book URLs in the chosen category
book_urls = fetch_book_urls(category_url)

# List to store all books' details
books_data = []

# Iterate over each book URL and scrape details
for book_url in book_urls:
    book_details = scrape_book_details(book_url)
    books_data.append(book_details)

# CSV file path to save the details
csv_file_path = 'category_books_details.csv'

# Save all book details into a single CSV file
fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available', 'product_description', 'category', 
          'review_rating', 'image_url']

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for book_data in books_data:
        writer.writerow(book_data)

print(f"All book details from the category have been saved to {csv_file_path}")
import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to extract all categories
def extract_categories(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_links = soup.find('ul', class_='nav-list').find('ul').find_all('a')
    categories = {cat.text.strip(): main_url + cat['href'] for cat in category_links}
    return categories

# Include the scraping functions from Phases 1 and 2 here
# def scrape_book_details(url):
#     # Phase 1 code...
#     pass
#
# def fetch_book_urls(category_url):
#     # Phase 2 code...
#     pass

# The main URL of 'Books to Scrape'
main_url = 'http://books.toscrape.com/'

# Extract all categories
categories = extract_categories(main_url)

# Directory to store CSV files
csv_dir = 'book_categories'
os.makedirs(csv_dir, exist_ok=True)

# Process each category
for category_name, category_url in categories.items():
    # Fetch book URLs for the category
    book_urls = fetch_book_urls(category_url)
    
    # List to store all books' details
    books_data = []
    
    # Scrape details for each book
    for book_url in book_urls:
        book_details = scrape_book_details(book_url)
        books_data.append(book_details)
    
    # Define the CSV file path for the category
    csv_file_path = os.path.join(csv_dir, f'{category_name}.csv')
    
    # Save the book details in a CSV file named after the category
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for book_data in books_data:
            writer.writerow(book_data)
    
    print(f"Completed category: {category_name}")

print("All categories have been processed.")

import os
import requests
from bs4 import BeautifulSoup

# Function to download an image from a URL
def download_image(image_url, folder_path, book_title):
    # Make a GET request to fetch the raw image data
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Clean/replace characters that are invalid for file names
        safe_title = "".join([c for c in book_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        # Create the image file path
        image_file_path = os.path.join(folder_path, f'{safe_title}.jpg')
        with open(image_file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return image_file_path
    else:
        print(f"Failed to retrieve image from {image_url}")

# Modify the scrape_book_details function from Phase 1 to include image download
def scrape_book_details(url, image_folder_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the image URL and book title
    image_url = soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
    book_title = soup.find('div', class_='product_main').h1.text

    # Download the image
    image_file_path = download_image(image_url, image_folder_path, book_title)
    
    # Rest of the book details extraction code...
    # ...

    # Return book details including the local image file path
    book_details['image_file_path'] = image_file_path
    return book_details
import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to download an image from a URL
def download_image(image_url, folder_path, book_title):
    # Make a GET request to fetch the raw image data
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Clean/replace characters that are invalid for file names
        safe_title = "".join([c for c in book_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        # Create the image file path
        image_file_path = os.path.join(folder_path, f'{safe_title}.jpg')
        with open(image_file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return image_file_path
    else:
        print(f"Failed to retrieve image from {image_url}")

# Function to scrape book details
def scrape_book_details(url, image_folder_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the required details
    product_details = {
        'product_page_url': url,
        'universal_product_code': soup.find('th', text='UPC').find_next_sibling('td').text,
        'title': soup.find('div', class_='product_main').h1.text,
        'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
        'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
        'quantity_available': soup.find('th', text='Availability').find_next_sibling('td').text,
        'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'review_rating': soup.find('p', class_='star-rating')['class'][1],
        'image_url': soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
    }

    # Download the image
    product_details['image_file_path'] = download_image(product_details['image_url'], image_folder_path, product_details['title'])
    
    return product_details

# Function to fetch book URLs from a single category, including pagination
def fetch_book_urls(category_url):
    book_urls = []
    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('h3 > a')
        for book in books:
            book_url = book['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            book_urls.append(book_url)

        # Check for a 'next' button for pagination
        next_button = soup.select_one('li.next > a')
        if next_button:
            next_page_url = next_button['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_url
        else:
            break
    return book_urls

# Function to extract all categories
def extract_categories(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_links = soup.select('ul.nav-list > li > ul > li > a')
    categories = {cat.text.strip(): main_url + cat['href'] for cat in category_links}
    return categories

# The main URL of 'Books to Scrape'
main_url = 'http://books.toscrape.com/'

# Extract all categories
categories = extract_categories(main_url)

# Directory to store CSV files
csv_dir = '/mnt/data/book_categories'
os.makedirs(csv_dir, exist_ok=True)

# Directory to store book images
image_dir = '/mnt/data/book_images'
os.makedirs(image_dir, exist_ok=True)

# Process each category
for category_name, category_url in categories.items():
    # Fetch book URLs for the category
    book_urls = fetch_book_urls(category_url)
    
    # List to store all books' details
    books_data = []
    
    # Scrape details for each book
    for book_url in book_urls:
        book_details = scrape_book_details(book_url, image_dir)
        books_data.append(book_details)
    
    # Define the CSV file path for the category
    csv_file_path = os.path.join(csv_dir, f'{category_name.replace("/", "-")}.csv')

# Save the book details in a CSV file named after the category
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = list(books_data[0].keys())  # Assumes all dictionaries have the same keys
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book_data in books_data:
            writer.writerow(book_data)
    
    print(f"Completed category: {category_name}")

print("All categories have been processed.")
