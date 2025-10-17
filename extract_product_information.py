# Import necessary libraries for data parsing and file handling.
from time import time
from bs4 import BeautifulSoup # Used for parsing HTML and extracting data.
from hashlib import sha256 # Used for creating a unique hash ID for products.
import json # Used for saving the extracted data to a JSON file.
import os # Used for interacting with the operating system, like writing new lines.
import random

# This script assumes a separate file named 'detailed_product_information.py' exists,
# containing the 'extract_detailed_product_info' function.
from detailed_product_information import extract_detailed_product_info

def append_record(record):
    """Appends a single JSON record to the data file, followed by a new line."""
    with open('data.json', 'a') as f:
        json.dump(record, f)
        f.write(os.linesep)

def extract_product_data(html_filepath,pretty_filepath, class_list, url_tag, url_class,attr_url_dictionary,attributes_dictionary,product_brand_tag,product_brand_class,product_price_tag,product_price_class,product_sale_price_tag,product_sale_price_class,title_tag,title_class,product_image_tag,product_image_class,product_image_dict):
    """
    Extracts product information from a given html file with product listings in the form a list of dictionaries
    """
    # This list will store the dictionaries of product data.
    products_data = []

    try:
        # Read the content from the saved HTML file.
        with open(html_filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        # Handle the case where the HTML file doesn't exist.
        print(f"Error: '{html_filepath}' not found. Cannot Extract data.")
        return products_data # Return an empty list.

    # Parse the HTML content with BeautifulSoup for easy data extraction.
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup:
        with open(pretty_filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

    # Find all parent elements that contain individual product listings.
    product_listings = soup.find_all(class_=class_list, attrs = attributes_dictionary)

    if not product_listings:
        # Inform the user if no products were found with the given criteria.
        print("No product listings found with the specified selectors. Check the tags and class names.")
        return products_data # Return an empty list.

    print(f"Found {len(product_listings)} products. Extracting data...")
    count = 0
    # Iterate through each product listing found.
    for product_tag in product_listings:
        if count >= 5:
            break  # Limit to 5 products for testing purposes.

        #there are too many requests in a short time, so we add a delay
        if count%10 == 0 and count != 0:
            random_delay = random.uniform(5,12)  # Random delay between 5 to 12 seconds for more realistic behavior
            print(f"Pausing for {random_delay:.2f} seconds to avoid overwhelming the server.")
            time.sleep(random_delay)

        # Find individual data points (title, price, etc.) within each product tag.
        title_tag_element = product_tag.find(title_tag, class_=title_class)
        url_tag_element = product_tag.find(url_tag, class_=url_class, attrs = attr_url_dictionary)
        brand_tag_element = product_tag.find(product_brand_tag,class_=product_brand_class)
        price_tag_element = product_tag.find(product_price_tag,class_=product_price_class)
        sale_price_tag_element = product_tag.find(product_sale_price_tag,class_=product_sale_price_class)
        image_tag_element = product_tag.find(product_image_tag,class_=product_image_class,attrs=product_image_dict)

        # Safely extract text, providing a default value if an element is not found.
        title = title_tag_element.get_text(strip=True) if title_tag_element else "Name not found"
        url = url_tag_element.get_text(strip=True) if url_tag_element else "URL not found"
        # Ensure the URL has the correct protocol prefix.
        complete_url = url if url.startswith('https') else f"https://{url}"

        # Check for and skip duplicate products based on their URL.
        if any(prod['link'] == complete_url for prod in products_data):
            print(f"Product with URL {complete_url} already exists. Skipping duplicate.")
            continue  # Skip to the next iteration.

        # This block calls an external function to scrape the detailed product page.
        # It can be commented out to speed up testing or if not needed.
        detailed_info = extract_detailed_product_info(complete_url)
        material = detailed_info.get('material', 'Material not found')
        description = detailed_info.get('description', 'Description not found')
        product_category = detailed_info.get('product_category', 'Category not found')
        additional_image_link = detailed_info.get('additional_image_link', [])
        variant_options = detailed_info.get('variant_options', [{'color':"Not found",'size':"Not found","price" : "Not found","sale_price" : "Not found"}])
        gender = detailed_info.get('gender', '')
        
        # Generate a unique and consistent ID from the product URL.
        id = sha256(url.encode('utf-8')).hexdigest()
        brand = brand_tag_element.get_text(strip=True) if brand_tag_element else "Brand Not Found"
        price = price_tag_element.get_text(strip=True) if price_tag_element else "Price Not Found"
        sale_price = sale_price_tag_element.get_text(strip=True) if sale_price_tag_element else "Sale Price Not Found"
        image = image_tag_element.get_text(strip=True) if image_tag_element else "Image Not Found"

        # Assemble the extracted data into a dictionary.
        product = {
            'id':id,'title': title, 
            'link': url, 
            'product_category':product_category,
            'brand':brand,
            'price': price,
            'gender': gender,
            'sale_price': sale_price,
            'image': image,
            'material' : material,
            'description': description,
            'additional_image_link': additional_image_link,
            'variant_options': variant_options
        }

        # Add the product dictionary to our list for this run.
        products_data.append(product)
        # Append the new product record directly to the JSON file for persistence.
        append_record(product)
        count += 1
        print(f"Extracted {count}/{len(product_listings)}: {title}")

    return products_data

