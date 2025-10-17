# Import the necessary functions from other project scripts.
from extract_product_information import extract_product_data
from scrape_url_script import scrape_specific_url
from bs4 import BeautifulSoup

def navigate_to_page():
    """
    Finds category links on a homepage, navigates to each,
    and initiates the data extraction process.
    """
    # The base URL of the target website.
    base_url = "https://www.nnnow.com"


    # To get fresh category links, uncomment the line below occasionally.
    # This will re-scrape the homepage and save it.
    scrape_specific_url(base_url, "home.html")
    
    # Read the locally saved homepage HTML to find navigation links.
    with open("home.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
    # Parse the homepage content.
    soup = BeautifulSoup(html_content, 'html.parser')
    with open("home_pretty.html", 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
    # Find all the anchor tags that correspond to second-level category pages.
    navigation_pages = soup.find_all('a', class_='nw-navtreev2-link nw-navtreev2-link-level2')

    # The filename for storing the HTML of category pages.
    HTML_FILE = 'file.html'

    print(f"Found {len(navigation_pages)} category links.")
    print("Category Links:")
    # Print the discovered links for verification.
    for link in navigation_pages:
        print(f" - {link.get_text(strip=True)}: {link.get('href')}")

    # --- SCRAPER CONFIGURATION ---
    # This section defines the specific HTML tags, classes, and attributes
    # needed to find product data on the target website. If the website's
    # design changes, these values will need to be updated.
    CLASS_LIST = ["nwc-grid-col", "nwc-grid-col-xs-6", "nwc-grid-col-sm-4", "nw-productlist-eachproduct"]
    PRODUCT_URL_TAG = 'div'
    PRODUCT_URL_CLASS = 'nwc-hide' 
    PRODUCT_URL_DICT = {"itemprop" : "url"}
    ATTR_DICT = {"itemprop": "itemListElement"}
    PRODUCT_TITLE_TAG = 'div'
    PRODUCT_TITLE_CLASS = 'nw-productview-producttitle'
    PRODUCT_BRAND_CLASS = 'nw-productview-brandtxt'
    PRODUCT_BRAND_TAG = 'h3'
    PRODUCT_SALE_PRICE_TAG = 'span'
    PRODUCT_SALE_PRICE_CLASS = ["nw-priceblock-amt", "nw-priceblock-sellingprice", "is-having-discount"]
    PRODUCT_PRICE_TAG = 'del'
    PRODUCT_PRICE_CLASS = ["nw-priceblock-amt", "nw-priceblock-mrp", "is-having-discount"]
    PRODUCT_IMAGE_TAG = 'div'
    PRODUCT_IMAGE_CLASS = 'nwc-hide'
    PRODUCT_IMAGE_DICT = {"itemprop": "image"}
    pretty_filepath = "file_pretty.html"
    
    count = 0

    # Loop through each category page found.
    for page in navigation_pages:
        if count >= 1:
            break  # Limit to the first category page for testing.
        
        # Get the relative URL from the anchor tag.
        page_url = page.get('href','')
        # Construct the full, absolute URL.
        complete_page_url = page_url if page_url.startswith('https') else f"https://{page_url}"
        print(f"Navigating to category page: {complete_page_url}")

        # Scrape the full HTML of the category page.
        scrape_specific_url(complete_page_url, HTML_FILE)
        
        # Call the extraction function with the scraped HTML and the configuration.
        extracted_data = extract_product_data(
            html_filepath=HTML_FILE,
            class_list=CLASS_LIST,
            url_tag=PRODUCT_URL_TAG,
            url_class=PRODUCT_URL_CLASS,
            attr_url_dictionary=PRODUCT_URL_DICT,
            attributes_dictionary= ATTR_DICT,
            title_tag=PRODUCT_TITLE_TAG,
            title_class=PRODUCT_TITLE_CLASS,
            product_sale_price_tag=PRODUCT_SALE_PRICE_TAG,
            product_sale_price_class=PRODUCT_SALE_PRICE_CLASS,
            product_price_tag=PRODUCT_PRICE_TAG,
            product_price_class=PRODUCT_PRICE_CLASS,
            product_brand_tag=PRODUCT_BRAND_TAG,
            product_brand_class=PRODUCT_BRAND_CLASS,
            product_image_tag=PRODUCT_IMAGE_TAG,
            product_image_class=PRODUCT_IMAGE_CLASS,
            product_image_dict=PRODUCT_IMAGE_DICT,
            pretty_filepath=pretty_filepath
        )
        # Check if any data was returned.
        if extracted_data:
            print(f"\nSuccessfully extracted data for {len(extracted_data)} items from {complete_page_url}.")
            # Print a few items as a sample to verify the results.
            for item in extracted_data[:5]:
                print(f"Name: {item['title']} \n URL: {item['link']} \n Price: {item['price']} \n Sale Price: {item['sale_price']} \n Image: {item['image']} \n Material: {item['material']} \n Description: {item['description']} \n Additional Images: {item['additional_image_link']} \n Variant Options: {item['variant_options']} \n Product Category: {item['product_category']} \n Gender: {item['gender']} \n")
        else:
            print(f"No data extracted from {complete_page_url}.")
        count += 1
    
# This ensures the script runs automatically when executed from the command line.
if __name__ == "__main__":
    navigate_to_page()
