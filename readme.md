# **Dynamic Web Scraper**

This project is a Python-based web scraper designed to dynamically navigate an e-commerce website, extract product listings from various category pages, and then scrape detailed information from each individual product page. It uses Selenium to handle JavaScript-heavy pages and BeautifulSoup for HTML parsing.

## **Table of Contents**

1. [Setup Instructions]()  
2. [Project Structure]()  
3. [How to Run]()  
4. [Configuration]()  
5. [Libraries Used]()  
6. [Disclaimer]()

### **Setup Instructions**

It is highly recommended to run this project within a Python virtual environment to manage dependencies cleanly.

**1\. Create a Virtual Environment:**

Open your terminal or command prompt in the project directory and run:

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

\# For Windows  
python \-m venv venv  
.\\venv\\Scripts\\activate

**2\. Install Dependencies:**

Create/Use file named requirements.txt in the project directory and add the following lines:

selenium  
beautifulsoup4  
webdriver-manager

Now, install these libraries using pip:

pip install \-r requirements.txt

This command will install all the necessary packages for the scraper to function.

### **Project Structure**

The project is divided into four main scripts, each with a specific responsibility:

* **scrape\_url\_script.py**: Contains the Selenium WebDriver setup and the function to scrape a URL. It handles scrolling down the page to load all dynamically generated content.  
* **extract\_product\_information.py**: Takes a saved HTML file of a product listing page and extracts summary data for each product (title, price, URL, etc.).  
* **detailed\_product\_information.py**: Navigates to an individual product URL to scrape more detailed information like material, description, color/size variants, and additional images.  
* **navigator.py**: This is the main entry point for the project. It orchestrates the entire process by first finding category links on the homepage, then navigating to each, and finally calling the appropriate functions to scrape and extract data.

### **How to Run**

1. Get the Homepage (First Run Only):  
   The scraper relies on a local copy of the website's homepage (home.html) to find category links. To generate this file for the first time, open navigator.py and uncomment the following line:  
   \# scrape\_specific\_url(base\_url, "home.html")

   Run the script once to create home.html, then you can comment the line out again for subsequent runs.  
2. Execute the Scraper:  
   Make sure your virtual environment is activated, then run the main navigator script from your terminal:  
   python navigator.py

   The script will start navigating the category pages, scraping product data, and saving it to data.json.

**Important Note on Testing Limitations:**

By default, the scripts are configured to run in a limited "testing mode" to prevent long run times and excessive requests during initial setup.

* In **scrape\_url\_script.py**, the page scroll is limited to a maximum height of 100,000 pixels.  
* In **navigator.py**, the main loop is limited to scraping only the **first category page**.  
* In **extract\_product\_information.py**, the product extraction loop is limited to the **first 5 products** on that page.

**To perform a full scrape, you must locate and remove or comment out the if...break blocks in all three of those files.**

### **Configuration**

The scraper's ability to find data depends on specific HTML tags, classes, and attributes. These are defined as configuration variables at the top of the Maps\_to\_page function in navigator.py.

If the target website's structure changes, you will need to inspect the new HTML and update these variables accordingly.

### **Libraries Used**

* **Selenium**: An automation tool used to control a web browser, essential for rendering JavaScript and handling dynamic content.  
  * [Selenium Documentation](https://www.selenium.dev/documentation/)  
* **BeautifulSoup**: A powerful library for parsing HTML and XML documents, making it easy to navigate and search the HTML tree.  
  * [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
* **WebDriver Manager**: A library that automatically handles the downloading and management of the correct browser driver (e.g., ChromeDriver) required by Selenium.  
  * [WebDriver Manager on PyPI](https://pypi.org/project/webdriver-manager/)

### **Disclaimer**

This tool is for educational purposes. Please be responsible and respectful when scraping websites. Always check a website's robots.txt file and its terms of service to understand its scraping policies. Avoid sending too many requests in a short period to prevent overloading the website's servers.