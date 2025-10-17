# Import necessary libraries.
from bs4 import BeautifulSoup # Used for parsing HTML.
# Assumes 'scrape_url_script.py' exists and contains the scrape_specific_url function.
from scrape_url_script import scrape_specific_url


def get_size_price_availability(color_soup, color):
    """
    Extracts size, price, and availability for a specific product color variant.
    """

    # Pre-defined list of sizes. Note: This might need adjustment if sizes vary.
    sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    size = []
    # Find all buttons that represent product sizes.
    size_tag = color_soup.find_all('button', class_='nwc-btn nw-size-chip')

    # Populate the size list based on the number of size tags found.
    for i in range(len(size_tag)):
        size.append(sizes[i])

    # Find all tags containing the price.
    price_tags = color_soup.find_all('span', class_='nwc-hide', attrs={"itemprop": "price"})
    # Find all tags indicating stock availability.
    availability_tag = color_soup.find_all('span', class_='nwc-hide', attrs={"itemprop": "availability"})
    availability = []
    # Extract the text from each availability tag.
    for tag in availability_tag:
        availability.append(tag.get_text(strip=True))
    price = []
    # Extract the text from each price tag.
    for tag in price_tags:
        price.append(tag.get_text(strip=True))
    
    # Structure the collected data into a dictionary.
    variant = {
        'color': color,
        'size': size,
        'price': price,
        'availability': availability
    }

    print(f"Extracted variant: {variant}")

    return variant

def get_variant_options(url_soup):
    """
    Finds all color options on a product page and scrapes each one for details.
    """
    variant_options = []
    # Find all links corresponding to different color options.
    color_tags = url_soup.find_all('a', class_='nw-color-item nwc-anchortag')
    # Get the URL of the currently selected color.
    color_url = url_soup.find('a', class_='nw-color-item selected nwc-anchortag').get('href','')
    # Construct the full URL for the color page.
    complete_color_url = color_url if color_url.startswith('https') else f"https://www.nnnow.com{color_url}"
    # Scrape the color page and save its HTML.
    scrape_specific_url(complete_color_url, "temp.html")
    # Read the saved HTML file.
    with open("temp.html", 'r', encoding='utf-8') as f:
            color_html_content = f.read()
    # Parse the color page's HTML.
    color_soup = BeautifulSoup(color_html_content, 'html.parser')
    # Extract the name of the color.
    color_name = color_soup.find('span', class_='nw-color-name').get_text(strip=True) if color_soup.find('span', class_='nw-color-name') else 'Not found'
    # Get the size, price, and availability for this color.
    variant_info = get_size_price_availability(color_soup, color=color_name)
    variant_options.append(variant_info)

    print(color_tags)

    # Loop through the other available color options.
    for i in range(int(len(color_tags)/2)):
        color_url = color_tags[i].get('href','')
        complete_color_url = color_url if color_url.startswith('https') else f"https://www.nnnow.com{color_url}"
        # Scrape each color's page to get its specific details.
        scrape_specific_url(complete_color_url, "temp.html")
        with open("temp.html", 'r', encoding='utf-8') as f:
            color_html_content = f.read()
        color_soup = BeautifulSoup(color_html_content, 'html.parser')
        color_name = color_soup.find('span', class_='nw-color-name').get_text(strip=True) if color_soup.find('span', class_='nw-color-name') else 'Not found'
        variant_info = get_size_price_availability(color_soup, color=color_name)
        variant_options.append(variant_info)

    return variant_options

def extract_detailed_product_info(complete_url):
    """
    Orchestrates the scraping of a single product page for all detailed information.
    """
    try:
        # Scrape the main product URL and save its HTML to a temporary file.
        scrape_specific_url(complete_url, "temp.html")
        # Read the content of the temporary HTML file.
        with open("temp.html", 'r', encoding='utf-8') as f:
            url_html_content = f.read()
        # Parse the page's HTML content.
        url_soup = BeautifulSoup(url_html_content, 'html.parser')
        # Save a prettified version for debugging purposes.
        with open("temp2.html","w",encoding='utf-8') as f:
            f.write(url_soup.prettify())
    except Exception as e:
        # Handle errors during the scraping process gracefully.
        print(f"Error fetching or reading the product page: {e}")
        # Return a dictionary with default "not found" values.
        return {
            'material' : "Material not found",
            'description': "Description not found",
            'additional_image_link': [],
            'variant_options':[{
                                'color':"Not found",
                                'size':"Not found",
                                "price" : "Not found",
                                "sale_price" : "Not found"
                            }]
        }

    # Find all tags related to the product description.
    description_tags = url_soup.find_all('div', class_='nw-pdp-desktopaccordiondetailssection')
    description = ""
    # Extract material from the first description section.
    material = description_tags[0].find_all('li', class_='nw-pdp-desktopaccordiondetailsli')[0].get_text(strip=True)
    # Extract title and list items from the second description section.
    desc1 = description_tags[1].find('h3', class_='nw-pdp-desktopaccordiondetailstitle').get_text(strip=True)
    desc2 = description_tags[1].find_all('li', class_='nw-pdp-desktopaccordiondetailsli')
    # Combine the parts into a single description string.
    if desc1:
        description += desc1
    if desc2:
        description += " ".join([li.get_text(strip=True) for li in desc2])
    description += "\n"

    # Extract the product category from the breadcrumb navigation.
    breadcrumb_tags = url_soup.find_all('span', class_='nw-breadcrumb-listitem')
    product_category = ""
    for tag in breadcrumb_tags:
        category = tag.get_text(strip=True)
        if category:
            product_category += category + " > "
    
    # Infer gender from the breadcrumb trail.
    gender = breadcrumb_tags[2].get_text(strip=True) if len(breadcrumb_tags) > 2 else ''

    # Extract URLs for additional product images.
    image_tags = url_soup.find_all('div', class_='nwc-lazyimg-container nw-thumbnail-imagelazy is-loaded')
    additional_images = []
    for img_tag in image_tags:
        img = img_tag.find('img')
        # Check if the image tag has a 'src' attribute before appending.
        if img and img.has_attr('src'):
            additional_images.append(img['src'])

    print(f"Extracted additional images: {additional_images}")

    # Get all variant options (colors, sizes, etc.).
    variant_options = get_variant_options(url_soup)

    # Return the final dictionary of all extracted details.
    return {
        'material' : material,
        'description': description,
        'additional_image_link': additional_images,
        'variant_options': variant_options,
        'product_category': product_category,
        'gender': gender
    }
