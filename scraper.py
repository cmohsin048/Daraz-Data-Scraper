
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from pymongo import MongoClient
import re

# Function to convert 'Sold' values to numeric
def convert_to_numeric(value):
    value_str = str(value).replace('Sold', '').strip()
    if 'K' in value_str:
        return int(float(value_str.replace('K', '')) * 1000)
    else:
        return int(value_str)

username = 'Mohsin_Raza'
password = 'cmohsin02'

connection_string = 'your connection string'

client = MongoClient(connection_string)

db = client['your data base name']
collection = db['your directory name']

print('Connected to the database')

# Initialize ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-extensions')
options.add_argument('--disable-setuid-sandbox')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# Increase v8 heap size
options.add_argument('--js-flags=--max_old_space_size=9096')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)

driver.get('paste the url any category like the given below')
# e.g('https://www.daraz.pk/smartphones/?spm=a2a0e.searchlistcategory.cate_7.1.102f5712PLHNQj')
driver.maximize_window()

# Example loop to navigate through page
current_page_number = 1
pages_url = []
max_attempts = 3

while current_page_number <=5:
    for attempt in range(max_attempts):
        try:
            class_selector = f'.ant-pagination-item.ant-pagination-item-{current_page_number}'
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, class_selector)))
            next_page_element = driver.find_element(By.CSS_SELECTOR, class_selector)
            anchor_tag = next_page_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            pages_url.append(anchor_tag)
            # print(f"Scraped URL for page {current_page_number}: {anchor_tag}")
            driver.get(anchor_tag)
            driver.maximize_window()
            current_page_number += 1
            break
        except TimeoutException:
            print("Page took too long to load. Retrying...")
            driver.refresh()
            continue
    else:
        print("Failed to load page after several attempts.")
        break

for i, page_url in enumerate(pages_url, 1):
    driver.get(page_url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    print(f'\n\n\nPage #{i} - URL: {page_url}')

    def scrape_remaining_information(product_info, a):
        product_url = product_info['url']
        score = product_info['score']
        reviews = product_info['reviews']
        sold = product_info['sold']
        product_id = product_info['product_id']
        category = product_info['category']
        sub_category = product_info['sub_category']
        Thirty_day_sales = product_info.get('Thirty_day_sales', 0)

        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                driver.get(product_url)
                driver.maximize_window()
                wait = WebDriverWait(driver, 20)  # Set the timeout to 20 seconds
                brand_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pdp-product-brand__brand-link")))

                # Continue with the rest of the scraping
                sku = re.search(r'-s(\d+)\.html', product_url).group(1)
                Brand = brand_element.text
                delivery_fee = driver.find_element(By.CSS_SELECTOR, ".delivery-option-item.delivery-option-item_type_standard .delivery-option-item__shipping-fee").text
                product_title = driver.find_element(By.CLASS_NAME, "pdp-mod-product-badge-title").text
                price_element = driver.find_element(By.CLASS_NAME, "pdp-price_size_xl")

                price_text = price_element.text
                numeric_price = int(''.join(c for c in price_text if c.isdigit()))

                whole_data = {
                    'url': product_url, 'category': category, 'sub_category': sub_category,
                    'product_id': product_id, 'sku': sku, 'Title': product_title, 'price':  numeric_price, 'Brand': Brand,
                    'delivery_fee': delivery_fee, 'Total_sales': sold, 'Rating': score, 'reviews': reviews, 'Thirty_day_sales': Thirty_day_sales
                }
                return whole_data
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error: Unable to scrape information for Product #{a} at URL: {product_url}. Retrying... ({attempt + 1}/{max_attempts})")
                if attempt < max_attempts - 1:
                    continue  # Retry the loop
                else:
                    print(f"Max attempts reached. Unable to scrape information for Product #{a} at URL: {product_url}.")
                    return None

    def scrape_product_data(product, i):
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                product_url = product.find_element(By.ID, "id-a-link").get_attribute("href")
                product_id_match = re.search(r'[si](\d+)-[si](\d+)\.html', product_url)
                if product_id_match:
                    product_id = product_id_match.group(1)
                else:
                    raise ValueError("Unable to extract product_id from URL")
                
                #based on what category you are trying to scrap data from
                category = "" 
                #e.g "Electronic Devices"
                sub_category = "Landline Phones"
                #e.g "Landline Phones"

                try:
                    score_text = product.find_element(By.CLASS_NAME, "ratig-num--KNake").text
                    score = float(score_text.split('/')[0])
                except NoSuchElementException:
                    score = '0'
                try:
                    reviews_element = product.find_element(By.CLASS_NAME, "rating__review--ygkUy")
                    reviews_text = reviews_element.text
                    match = re.search(r'\((\d+)\)', reviews_text)
                    if match is not None:
                      reviews = int(match.group(1))
                    else:
                      reviews=0
                except NoSuchElementException:
                    reviews = '0'

                try:
                    sold = product.find_element(By.XPATH, ".//div[contains(text(), 'Sold')]").text
                except NoSuchElementException:
                    sold = '0'

                sold_numeric = convert_to_numeric(sold)
                product_data = {
                    'url': product_url,
                    'score': score,
                    'reviews': reviews,
                    'sold': sold_numeric,
                    'category': category,
                    'sub_category': sub_category,
                    "product_id": product_id,
                    'Thirty_day_sales': 0
                }
                return product_data

            except (NoSuchElementException, TimeoutException, ValueError) as e:
                print(f"Error: Unable to scrape initial data for Product #{i}. Retrying... ({attempt + 1}/{max_attempts})")
                if attempt < max_attempts - 1:
                    continue  # Retry the loop
                else:
                    print(f"Max attempts reached. Unable to scrape initial data for Product #{i}.")
                    return None

    # Initial scrape on the first page
    products_data = []
    products = driver.find_elements(By.CLASS_NAME, "gridItem--Yd0sa")

    for j, product in enumerate(products, 1):
        product_info = scrape_product_data(product, j)
        if product_info:
            products_data.append(product_info)

    for a, product_info in enumerate(products_data, 1):
        scraped_data = scrape_remaining_information(product_info, a)

        if scraped_data:
            # Check if product with the same product_id and md5_hash exists
            existing_product = collection.find_one({
                'product_id': scraped_data['product_id']
            })

            if existing_product:
                # Update existing product
                total_sales_previous = existing_product.get('Total_sales', 0)
                total_sales_current = scraped_data.get('Total_sales', 0)
                thirty_day_sales = total_sales_current - total_sales_previous

                collection.update_one(
                    {'_id': existing_product['_id']},
                    {'$set': {
                        'url': scraped_data['url'],
                        'category': scraped_data['category'],
                        'sub_category': scraped_data['sub_category'],
                        'product_id': scraped_data['product_id'],
                        'sku': scraped_data['sku'],
                        'Title': scraped_data['Title'],
                        'price': scraped_data['price'],
                        'Brand': scraped_data['Brand'],
                        'delivery_fee': scraped_data['delivery_fee'],
                        'Total_sales': total_sales_current,
                        'Rating': scraped_data['Rating'],
                        'reviews':scraped_data['reviews'],
                        'Thirty_day_sales': thirty_day_sales
                    }}
                )
            else:
                # Insert new product only if no duplicate found
                existing_duplicate_check = collection.find_one({
                    'product_id': scraped_data['product_id'],
                })

                if not existing_duplicate_check:
                    collection.insert_one(scraped_data)

# Close the driver and MongoDB connection
driver.quit()
client.close()
