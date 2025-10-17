# Import necessary libraries for web scraping.
import time  # Used for adding delays.
from selenium import webdriver  # The core library for browser automation.
from selenium.webdriver.chrome.service import Service as ChromeService # Manages the ChromeDriver service.
from selenium.webdriver.chrome.options import Options # Allows setting custom Chrome options.
from webdriver_manager.chrome import ChromeDriverManager # Automatically manages the Chrome driver.

def setup_driver():
    """
    This function gets our automated Chrome browser ready to go.
    We'll set it up with special options to make it look less like a bot.
    """
    print("Setting up the automated browser (WebDriver)...")
    
    # Initialize Chrome options for customization.
    options = Options() 
    
    # Set a realistic User-Agent to avoid being identified as a bot.
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    
    # Run in headless mode (no visible browser window) for efficiency.
    options.add_argument("--headless")
    
    # Arguments to ensure stable headless operation.
    options.add_argument("--window-size=1920,1080") # Set a standard screen size.
    options.add_argument("--no-sandbox") # Required for running in many server/container environments.
    options.add_argument("--disable-gpu") # Disable GPU acceleration, not needed for headless.
    options.add_argument("--disable-dev-shm-usage") # Prevents issues with shared memory in Docker/Linux.
    
    # Options to hide automation flags from websites.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Automatically download and install the correct ChromeDriver.
    service = ChromeService(ChromeDriverManager().install())
    
    # Initialize the Chrome driver with the service and options.
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute script to remove the 'navigator.webdriver' property to avoid detection.
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("Browser setup is complete!")
    return driver

def scrape_specific_url(scraping_url, output_filename, scroll_pause_time=2.5, max_no_change_scrolls=3):
    """
    This function takes a URL, scrolls all the way to the bottom to load everything,
    and then saves the final HTML of the page to a file.
    """
    # Initialize the configured WebDriver.
    driver = setup_driver()
    
    # Use a try...finally block to ensure the driver quits properly.
    try:
        print(f"Let's go to: {scraping_url}...")
        
        # Navigate to the target URL.
        driver.get(scraping_url) 
        
        # Wait for the initial page content to load.
        print("Giving the page a moment to load...")
        time.sleep(5)

        print("Starting to scroll down the page to find all the content.")
        
        # Get the initial scroll height of the page.
        last_height = driver.execute_script("return document.body.scrollHeight")
        # Counter for consecutive scrolls with no height change.
        consecutive_scrolls_without_change = 0

        # Loop until the page stops loading new content.
        while consecutive_scrolls_without_change < max_no_change_scrolls:
            # Scroll to the bottom of the page.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load after scrolling.
            time.sleep(scroll_pause_time)
            
            # Calculate the new scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # A failsafe to stop scrolling on extremely long pages. Can be removed.
            if new_height >= 100000:
                last_height = new_height
                print(f"Page is getting very long! Stopping scroll at {new_height}px.")
                break

            # Check if the scroll height has changed.
            if new_height == last_height:
                # If height is unchanged, increment the no-change counter.
                consecutive_scrolls_without_change += 1
                print(f"Page height hasn't changed. Checking again... ({consecutive_scrolls_without_change}/{max_no_change_scrolls})")
            else:
                # If height changed, new content loaded; reset the counter.
                consecutive_scrolls_without_change = 0
                print(f"Scrolled down. New page height is now: {new_height}px")
            
            # Update the last known height.
            last_height = new_height

        print(f"\nLooks like we've reached the bottom! The final page height is {last_height}px.")
        
        # Get the final page source after all content has loaded.
        final_html = driver.page_source
        
        # Save the complete HTML to the specified output file.
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"Success! The full webpage content has been saved to '{output_filename}'")

    except Exception as e:
        # Handle and report any exceptions during the process.
        print(f"Oh no, something went wrong: {e}")
    finally:
        # This block ensures the browser is closed, even if errors occurred.
        print("Closing the browser session now. Bye!")
        driver.quit()

