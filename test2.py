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
book_url = book.find('a')['href'].replace('../../../','http://books.toscrape.com/catalogue/')
book_urls.append(book_url)
# Check if there is a next page
next_button = soup.find('li', class_='next')
if next_button:
next_page_url = next_button.find('a')['href']
category_url = '/'.join(category_url.split('/')[:-1]) +
'/' + next_page_url
else:
break
return book_urls
# Function to scrape book details from Phase 1
def scrape_book_details(url):
# The rest of the scraping code from Phase 1 goes here
# ...
pass # Replace with the actual scraping code
# The chosen category URL (example: science category)
category_url =
'http://books.toscrape.com/catalogue/category/books/science_22/index.
html'
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

fields = ['product_page_url', 'universal_product_code', 'title',
'price_including_tax',
'price_excluding_tax', 'quantity_available',
'product_description', 'category',
'review_rating', 'image_url']
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as
file:
writer = csv.DictWriter(file, fieldnames=fields)
writer.writeheader()
for book_data in books_data:
writer.writerow(book_data)
print(f"All book details from the category have been saved to
{csv_file_path}")