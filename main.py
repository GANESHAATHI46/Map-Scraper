# main.py
"""
main.py
-------------------------
Application entry point
"""

from config import SEARCH_KEYWORD, OUTPUT_FILE, HEADLESS
from scraper import BusinessScraper
from excel import ExcelManager


def main():
    print("=" * 50)
    print("Business Scraper")
    print("=" * 50)

    print(f"Search: {SEARCH_KEYWORD}")

    # Start scraper
    scraper = BusinessScraper(headless=HEADLESS)

    try:
        scraper.start()

        # Generic method that your scraper implementation provides
        businesses = scraper.search(SEARCH_KEYWORD)

    finally:
        scraper.close()

    # Save results
    excel = ExcelManager(OUTPUT_FILE)
    excel.save(businesses)

    print("\nFinished!")
    print(f"Collected {len(businesses)} businesses")


if __name__ == "__main__":
    main()