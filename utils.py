from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import logging
import pandas as pd
from openpyxl import load_workbook
import datetime


def load_dotenv():
    """ Load environment variables from a .env file. """
    from dotenv import load_dotenv
    if not os.path.exists(".env"):
        logging.error("No .env file found.")
        return
    load_dotenv()


def save_to_excel(deals):
    """ Save the scraped car deals data to an Excel file with adjusted column widths and return file path. """
    if not deals:
        print("No deals found, skipping file save.")
        return None  # Return None if there are no deals

    # Get today's date for filename
    today = datetime.datetime.now().strftime("%d_%m_%Y")
    file_path = f"car_deals_{today}.xlsx"

    # Convert deals to DataFrame
    df = pd.DataFrame(deals)
    df.to_excel(file_path, index=False)

    # Adjust column widths using openpyxl
    wb = load_workbook(file_path)
    ws = wb.active
    for col in ws.columns:
        max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2  # Add padding

    # Save adjusted file
    wb.save(file_path)

    print(f"✅ Saved {len(deals)} deals to {file_path}")

    return file_path  # Return the file path for email attachment


def handle_consent(driver):
    try:
        # Wait for the iframe to appear and switch
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='privacy.autobazar.eu']"))
        )

        # Wait for the 'Accept All' button and click
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(text())="Prijať všetko"]'))
        ).click()

        # Switch back to main content
        driver.switch_to.default_content()

    except Exception as e:
        print(f"❌ Error handling consent: {e}")




