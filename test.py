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
'universal_product_code': soup.find('th',
text='UPC').find_next_sibling('td').text,
'title': soup.find('div', class_='product_main').h1.text,
'price_including_tax': soup.find('th', text='Price (incl.
tax)').find_next_sibling('td').text,
'price_excluding_tax': soup.find('th', text='Price (excl.
tax)').find_next_sibling('td').text,
'quantity_available': soup.find('th',
text='Availability').find_next_sibling('td').text.split('(')[1].split
(' ')[0], # Extracting number from the string
'product_description': soup.find('meta', attrs={'name':
'description'})['content'].strip(),
'category': soup.find('ul',
class_='breadcrumb').find_all('li')[2].text.strip(),
'review_rating': soup.find('p',
class_='star-rating')['class'][1],
'image_url': soup.find('img')['src'].replace('../../',
'http://books.toscrape.com/')
}
return product_details
# Define the CSV file name
csv_file = 'book_details.csv'     

# Function to save details to CSV
def save_to_csv(data, file_name):
# Field names for CSV
fields = ['product_page_url', 'universal_product_code', 'title',
'price_including_tax',
'price_excluding_tax', 'quantity_available',
'product_description', 'category',
'review_rating', 'image_url']
with open(file_name, mode='w', newline='', encoding='utf-8') as
file:
writer = csv.DictWriter(file, fieldnames=fields)
writer.writeheader()
writer.writerow(data)
# URL of the book to scrape
book_url =
"https://books.toscrape.com/catalogue/the-most-perfect-thing-inside-a
nd-outside-a-birds-egg_938/index.html"
# Scrape the book details
book_details = scrape_book_details(book_url)
# Save the book details to CSV
save_to_csv(book_details, csv_file)
print(f"Book details saved to {csv_file}"