from scraper import *
from utils import load_dotenv, save_to_excel, handle_consent
from config import *
import os
import time
import logging
import json


# Setup logging
logging.basicConfig(level=logging.INFO)
load_dotenv()

# Email credentials
FROM_EMAIL = os.getenv("FROM_EMAIL")   # Replace with your email
MY_PASSWORD = os.getenv("MY_PASSWORD")    # Replace with your email password or app-specific password
TO_EMAIL = os.getenv("TO_EMAIL")       # Replace with your email


def main():
    driver = setup_driver()
    try:
        # Scraping logic
        url = (
            f"{URL}vysledky/osobne-vozidla/{BRAND}/?model={MODELS}&priceTo={MAX_PRICE}&yearFrom={MIN_YEAR}"
            f"&mileageTo={MAX_MILEAGE}&sortBy=dateDesc")
        driver.get(url)
        time.sleep(random.uniform(2, 3))
        handle_consent(driver)

        deals = scrape_all_data(driver)
        print(deals)

        with open("deals.json", "w") as file:
            json.dump(deals, file, indent=4)

        # Optionally send email
        # file_path = save_to_excel(deals)
        # if file_path:
        #     send_email_with_attachment(deals, file_path)
    finally:
        driver.quit()
        logging.info("Driver closed properly.")


if __name__ == "__main__":
    main()
