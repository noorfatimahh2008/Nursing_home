#  Nursing Home Scraper - Medicare.gov

This Python-based scraper uses `undetected-chromedriver` and `Selenium` to collect data about nursing homes from [Medicare.gov](https://www.medicare.gov/care-compare/). It automates search, navigates results, and scrapes key details like name, address, and phone number.

---

##  Features

- Headless browser automation
- Automatically searches for **"New York, NY"**
- Navigates to the 12th page of results
- Extracts **300 nursing home profile links**
- Scrapes:
  -  Name
  -  Location
  -  Phone number
- Saves data to `scraped_data.csv`

---

##  Technologies Used

- **Python 3**
- **Selenium**
- **Undetected ChromeDriver**
- **Chrome Headless Mode**
- **CSV** module

---

##  Installation

Install dependencies:

```bash
pip install selenium undetected-chromedriver
