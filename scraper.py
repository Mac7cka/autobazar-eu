import re
import time
import random
from datetime import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent


# Constants
LOADING_TIME = random.uniform(2, 4)


# ====== Setup Driver ======
def setup_driver():
    options = uc.ChromeOptions()

    # options.add_argument('--headless=new') to run invisibly
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Random user agent
    ua = UserAgent()
    options.add_argument(f'--user-agent={ua.random}')

    # Load uBlock Origin extension (.crx file)
    options.add_extension("C:/Users/hutan/Downloads/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_64_0_0.crx")

    # Start undetected Chrome
    return uc.Chrome(options=options)


# ====== Utility Functions ======
def is_today(date_str):
    try:
        deal_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        return deal_date == datetime.today().date()
    except ValueError:
        return False


def click_on_next_btn_pagination(driver):
    """ Click the 'Next listings' (Ďalšie inzeráty) button to go to the next page. """
    try:
        # Wait for the button to be visible and clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Ďalšie inzeráty") and contains(@class, "inline-block")]'))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(random.uniform(0.3, 0.6))  # slight pause after scroll
        next_button.click()
        time.sleep(LOADING_TIME)

        # Wait for listings to reload
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Listingsstyled__List-sc-1iabgue-0"))
        )

    except TimeoutException:
        print("⏳ No 'Ďalšie inzeráty' button found or clickable.")
    except Exception as e:
        print(f"❌ Failed to click next page: {e}")


def last_card_is_from_today(driver):
    """ Checks if the last visible car card on the page is from today. """
    try:
        cars_container = driver.find_element(By.CSS_SELECTOR,
                                             'body > div:nth-child(1) > div:nth-child(2) > main:nth-child(3) > '
                                             'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                             'div:nth-child(2) > div:nth-child(7)'
                                             )
        car_cards = cars_container.find_elements(By.CLASS_NAME, "flex-row")
        if not car_cards:
            return False

        last_card = car_cards[-1]
        spans = last_card.find_elements(By.TAG_NAME, 'span')
        for span in spans:
            date_text = span.text.strip()
            if re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', date_text):
                return is_today(date_text)
    except Exception as e:
        print(f"⚠️ Error checking last card date: {e}")
    return False


# ====== Validate of correct order in spec fields ======
def validate_car_data(data):
    """ Validates and cleans scraped car data """
    try:
        year_pattern = r'^\d{4}$'
        mileage_pattern = r'^\d{1,3}(\s?\d{3})*\s?(km|mi)?$'
        power_pattern = r'^\d{1,4}\s?(kW|hp)?$'

        valid_year = re.match(year_pattern, data.get("year", ""))
        valid_mileage = re.match(mileage_pattern, data.get("mileage", ""))
        valid_power = re.match(power_pattern, data.get("power", ""))

        return all([valid_year, valid_mileage, valid_power])

    except Exception as e:
        print(f"⚠️ Validation Error: {e}")
        return False


def sort_results(results):
    """ Sorts results by year (desc), mileage (asc), and price (desc) """
    try:
        return sorted(results, key=lambda x: (
            int(x["year"]) if x["year"].isdigit() else 0,
            int(re.sub(r'\D', '', x["mileage"])) if x["mileage"] else 0,
            int(re.sub(r'\D', '', x["price"])) if x["price"] else 0
        ), reverse=True)
    except Exception as e:
        print(f"⚠️ Sorting Error: {e}")
        return results


# ====== Scraping Core ======
def scrape_data(driver):
    """ Scrapes car listings from a single page. """
    results = []

    try:
        cars_container = driver.find_element(By.CSS_SELECTOR,
                                             'body > div:nth-child(1) > div:nth-child(2) > main:nth-child(3) > '
                                             'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                             'div:nth-child(2) > div:nth-child(7)'
                                             )
        car_cards = cars_container.find_elements(By.CLASS_NAME, "flex-row")
        print(f"🚗 Found {len(car_cards)} car listings.")

        for card in car_cards:
            try:
                # Get date
                data = card.find_elements(By.TAG_NAME, 'span')
                date_added = None
                for d in data:
                    text = d.text.strip()
                    if re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', text):
                        date_added = text
                        break
                if not date_added or not is_today(date_added):
                    continue  # skip if not from today

                ActionChains(driver).move_to_element(card).perform()
                time.sleep(random.uniform(0.3, 0.6))

                title = card.find_element(By.CSS_SELECTOR, 'h2').text

                # Link
                link_el = card.find_element(By.TAG_NAME, 'a')
                link = link_el.get_attribute("href")
                if link and link.startswith('/'):
                    link = "https://www.autobazar.eu" + link

                # Image
                img_el = card.find_element(By.CSS_SELECTOR, 'img')
                img = next(
                    (img_el.get_attribute(attr) for attr in ['src', 'data-src', 'data-lazy', 'data-original']
                     if img_el.get_attribute(attr)), None
                )

                # Price
                try:
                    price_el = WebDriverWait(card, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, './/*[self::span or self::div][contains(text(), "€") or contains(text(), "Kč")]')
                        )
                    )
                    price = price_el.text.strip()
                except:
                    price = data[0].text if data else "N/A"

                # Specs
                specs = card.find_elements(By.CSS_SELECTOR, '.text-white\\/60')
                fields = [spec.text for spec in specs]
                while len(fields) < 5:
                    fields.append("N/A")
                year, transmission, fuel, mileage, power = fields[:5]

                car_data = {
                    'title': title,
                    'img': img,
                    'price': price,
                    'date_added': date_added,
                    'year': year,
                    'transmission': transmission,
                    'fuel': fuel,
                    'mileage': mileage,
                    'power': power,
                    'link': link
                }

                if validate_car_data(car_data):
                    results.append(car_data)






            except Exception as e:
                print(f"❌ Error scraping a card: {e}")

    except Exception as e:
        print(f"❌ Error locating container or cards: {e}")

    return results


# ====== Paginated Scraping Loop ======
def scrape_all_data(driver):
    all_results = []
    page = 1

    while True:
        print(f"\n📄 Scraping page {page}...")

        page_results = scrape_data(driver)
        all_results.extend(page_results)

        if not last_card_is_from_today(driver):
            print("🛑 Last card is not from today. Stopping.")
            break

        click_on_next_btn_pagination(driver)
        page += 1

    sorted_results = sort_results(all_results)

    print(f"\n✅ Total listings scraped: {len(all_results)}")
    return sorted_results
