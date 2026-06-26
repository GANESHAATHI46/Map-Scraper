# scraper.py
"""
scraper.py
--------------------------------
Generic Selenium browser helper
"""

import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from parser import BusinessParser
import config

class BusinessScraper:

    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless

    def start(self):
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def open(self, url):
        self.driver.get(url)

    def wait_for(self, by, value, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def find_all(self, by, value):
        return self.driver.find_elements(by, value)

    def get_text(self, by, value):
        try:
            return self.find(by, value).text
        except Exception:
            return ""

    def get_attribute(self, by, value, attribute):
        try:
            return self.find(by, value).get_attribute(attribute)
        except Exception:
            return ""

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def click(self, by, value):
        self.find(by, value).click()

    def close(self):
        if self.driver:
            self.driver.quit()

    def search(self, keyword):
        """
        Search for the keyword on Google Maps and extract business information.
        """
        print(f"Navigating to Google Maps for: {keyword}")
        url = f"https://www.google.com/maps/search/{urllib.parse.quote(keyword)}"
        self.open(url)
        
        businesses = []
        try:
            # Wait for the feed to load
            feed = self.wait_for(By.CSS_SELECTOR, "div[role='feed']", timeout=20)
        except TimeoutException:
            print("Could not find the results feed. Check keyword or connection.")
            return businesses

        print("Scrolling through results...")
        for _ in range(config.MAX_SCROLL):
            try:
                self.driver.execute_script("var feed = document.querySelector(\"div[role='feed']\"); if (feed) feed.scrollTo(0, feed.scrollHeight);")
                time.sleep(2)
            except Exception:
                pass
            
        print("Finding business links...")
        items = self.find_all(By.CSS_SELECTOR, "a.hfpxzc")
        urls = [item.get_attribute("href") for item in items if item.get_attribute("href")]
        
        # Remove duplicates while preserving order
        urls = list(dict.fromkeys(urls))
        print(f"Found {len(urls)} unique businesses. Extracting details...")
        
        for url in urls:
            try:
                self.open(url)
                time.sleep(config.WAIT_TIME)
                
                name = self.get_text(By.CSS_SELECTOR, "h1")
                
                # Extract rating & reviews
                rating_text = self.get_text(By.CSS_SELECTOR, "div.F7nice")
                rating = BusinessParser.parse_rating(rating_text)
                reviews = BusinessParser.parse_reviews(rating_text)
                
                # Category typically found in this button class
                category = self.get_text(By.CSS_SELECTOR, "button.DkEaL")
                
                # Extract Address, Phone, Website from information buttons
                address = ""
                phone = ""
                website = ""
                
                info_buttons = self.find_all(By.CSS_SELECTOR, "button.CsEnBe")
                for btn in info_buttons:
                    aria_label = btn.get_attribute("aria-label") or ""
                    if aria_label.startswith("Address:"):
                        address = aria_label.replace("Address:", "").strip()
                    elif aria_label.startswith("Phone:"):
                        phone = BusinessParser.parse_phone(aria_label)
                    elif aria_label.startswith("Website:"):
                        website = aria_label.replace("Website:", "").strip()
                        
                lat, lng = BusinessParser.parse_lat_long(url)
                
                record = BusinessParser.build_record(
                    name=name,
                    category=category,
                    rating=rating,
                    reviews=reviews,
                    address=address,
                    phone=phone,
                    website=website,
                    latitude=lat,
                    longitude=lng,
                    maps_url=url
                )
                
                businesses.append(record)
                print(f"Scraped: {name}")
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                
        return businesses