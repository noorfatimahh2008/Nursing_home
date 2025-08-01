from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import csv
import time

options = uc.ChromeOptions()
options.add_argument("--remote-debugging-port=2007")
options.add_argument("--user-data-dir=D:/nursing_home/chrome_session")
options.add_argument("--headless=new")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# ✅ Chrome Driver Create karo
driver = uc.Chrome(options=options)


# **STEP 2: Go to Search Page & Perform Search**
driver.get("https://www.medicare.gov/care-compare/?providerType=NursingHome")

wait = WebDriverWait(driver, 10)
time.sleep(2)

# Scroll down for visibility
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

# Locate the search input field
input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-labelledby='locationFieldLabel']")))
input_field.send_keys(Keys.CONTROL + "a")
input_field.send_keys(Keys.BACKSPACE)
input_field.send_keys("New York,NY")
time.sleep(2)
input_field.send_keys(Keys.ENTER)
time.sleep(5)

# Click Search Button
search_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ProviderSearchSearchButton__submit')]")
search_button.click()
time.sleep(5)
# Scroll to load results
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
# # Element locate karo
element = driver.find_element(By.XPATH, '//*[@id="app"]/main/ccxp-provider-search-results/div/div[2]/div/ccxp-provider-search-results-list/div/div[18]/ccxp-pager/nav/ul/li[12]/a')

# Click karo
element.click()
# **STEP 3: Collect All Nursing Home Links**
links = []
for i in range(1, 301):  
    try:
        link_element = driver.find_element(By.XPATH, f'//*[@id="result-card-{i}"]/div[2]/div[1]/div[1]/div[1]/a')
        link = link_element.get_attribute("href")
        links.append(link)
        print(f"Collected link {i}: {link}")
    except Exception as e:
        print(f"Error collecting link {i}: {e}")

print("✅ All 300 links collected!")

# **STEP 4: Scrape Data From Each Link**
with open("scraped_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Location", "Phone Number"])  # Header row

    for index, link in enumerate(links):
        try:
            driver.get(link)
            time.sleep(5)  # Wait for page to load

            try:
                name = driver.find_element(By.XPATH, '//*[@id="app"]/main/ccxp-provider-details/div/div[2]/ng-component/ccxp-provider-details-hero-container/div/div[2]/div[1]/h1').text.strip()
            except:
                name = "N/A"

            try:
                location = driver.find_element(By.XPATH, '//*[@id="app"]/main/ccxp-provider-details/div/div[2]/ng-component/ccxp-provider-details-hero-container/div/div[2]/div[2]/div[2]/div[2]/ccxp-address/div/div').text.strip()
            except:
                location = "N/A"

            try:
                phone = driver.find_element(By.XPATH, '//*[@id="app"]/main/ccxp-provider-details/div/div[2]/ng-component/ccxp-provider-details-hero-container/div/div[2]/div[2]/div[2]/div[4]/a').text.strip()
            except:
                phone = "N/A"

            writer.writerow([name, location, phone])
            print(f"Scraped {index+1}: {name} - {location} - {phone}")

        except Exception as e:
            print(f"Error scraping {index+1}: {e}")

print("✅ Scraping complete! Data saved in 'scraped_data.csv'.")
csv_filename = "nursing_home.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Sold", "Location"])  # Write headers
    writer = csv.writer(file)

print(f"\n✅ Data from both pages saved in {csv_filename}")

# Close the WebDriver
driver.quit()

