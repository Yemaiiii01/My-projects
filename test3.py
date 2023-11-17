import requests
from bs4 import BeautifulSoup
import csv
import os
# Function to extract all categories
def extract_categories(main_url):
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')
category_links = soup.find('ul',
class_='nav-list').find('ul').find_all('a')
categories = {cat.text.strip(): main_url + cat['href'] for cat in
category_links}
return categories
# Include the scraping functions from Phases 1 and 2 here
# def scrape_book_details(url):
# # Phase 1 code...
# pass
#
# def fetch_book_urls(category_url):
# # Phase 2 code...
# pass
# The main URL of 'Books to Scrape'
main_url = 'http://books.toscrape.com/'
# Extract all categorie

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
with open(csv_file_path, mode='w', newline='', encoding='utf-8')
as file:
writer = csv.DictWriter(file, fieldnames=fields)
writer.writeheader()
for book_data in books_data:
writer.writerow(book_data)
print(f"Completed category: {category_name}")
print("All categories have been processed.")