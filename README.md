# Autobazar.eu scraper

## 📜 Description


A robust Python-based web scraper for collecting daily updated car listings from [autobazar.eu](https://www.autobazar.eu). 
Built using `Selenium` with stealth techniques to bypass bot detection, and exports structured results to Excel or JSON 
for easy processing or sharing.

---

## 📌 Features

- **Fully Automated Daily Scraper**  
  Fetches only *today's* new listings across multiple pages, stopping intelligently once older ads appear.

- **Undetected Selenium with Anti-Bot Measures**  
  Uses `undetected-chromedriver`, randomized user agents, and optional uBlock Origin to avoid detection and remove clutter.

- **Custom Filters via Config**  
  Easily configurable: brand, model IDs, year, price, mileage limits are all centralized in a config file.

- **Clean Data with Validation & Sorting**  
  Only valid car listings (based on date, year, mileage, power, etc.) are included, then sorted by year, mileage, and price.

- **Consent Handling**  
  Automatically accepts GDPR consent forms in iframe popups.

- **Export to Excel**  
  Saves results in a neatly formatted `.xlsx` file with auto-adjusted column widths.

- **Email Support (Optional)**  
  Ready to email you the listings file – just plug in your SMTP credentials.

---

## 🧠 Project Highlights 



- ✅ **Detection Avoidance:** Implements anti-bot scraping with `undetected-chromedriver` and rotating user agents.  
- ✅ **Smart Pagination:** Automatically navigates pages and halts scraping when listings are no longer from today.  
- ✅ **Real-Time Date Filtering:** Ensures only fresh listings are collected, avoiding stale or cached data.  
- ✅ **Modular & Reusable Design:** Clearly separated logic (`main`, `scraper`, `utils`, `config`) for easy maintenance and extension.  
- ✅ **Error Handling & Logging:** Gracefully manages missing elements, timeouts, and logs progress during scraping.  
- ✅ **Excel Reporting:** Ready for non-technical stakeholders to review listings in spreadsheet format.  
- ✅ **GDPR Compliance Handling:** Automates the dismissal of cookie and consent banners.

---

## 📁 Project Structure

├── main.py # Entry point for the scraper
├── scraper.py # Scraping logic with anti-bot setup
├── email_handler.py # (Optional) For sending email alerts
├── utils.py # Helpers for file saving, dotenv loading, and consent handling
├── config.py # All configurable constants (price, model, brand, etc.)
├── .env # (Optional) Email credentials for alerts
└── requirements.txt # All dependencies

---

## ⚙️ Requirements

Install dependencies via:
pip install -r requirements.txt

### Python Packages:

selenium

undetected-chromedriver

fake-useragent

pandas

openpyxl

python-dotenv

## 📝 Setup Instructions


## ⚙️ Configuration

In `config.py`, adjust the following parameters as needed:

BRAND = "volkswagen"
MODELS = [34932, 34930, 349240]
MIN_YEAR = 2015
MAX_PRICE = 10000
MAX_MILEAGE = 300000


## Dependencies

- Configure .env File: 
  Create a .env file in the project directory and add your email credentials as shown above.

## Environment Variables

The following environment variables should be set in a `.env` file:

- `FROM_EMAIL`: Your email address (sender)
- `MY_PASSWORD`: Your email password (or app-specific password)
- `TO_EMAIL`: The recipient's email address

## Run the Scraper:

python main.py



This project is intended for educational and personal use only. Always respect the site's robots.txt and terms of service.