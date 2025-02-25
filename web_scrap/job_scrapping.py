from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv

# Configure Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument("--headless") 
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# Start WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open job search page
url = "https://www.theladders.com/search"
driver.get(url)

# Wait for manual login
print("Browser is open. Please log in manually.")
time.sleep(35)  # Increase if needed

# Function to scroll down and load all jobs
def load_all_jobs():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new jobs to load
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # No more jobs loaded
            break
        last_height = new_height

# Scroll to load all job listings
load_all_jobs()

# Extract job listings
jobs_data = []

try:
    # Wait for job list container to appear
    job_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-content-container"))
    )

    

    for job in job_cards:
        try:
            title = job.find_element(By.CSS_SELECTOR, "a.job-card-title").text.strip()
            company = job.find_element(By.CSS_SELECTOR, "span.job-card-company-name").text.strip()
            
            # Salary (optional, not all jobs have salary listed)
            try:
                salary = job.find_element(By.CSS_SELECTOR, "p.salary").text.strip()
            except:
                salary = "Not specified"

            # Job description
            description = job.find_element(By.CSS_SELECTOR, "p.job-card-description").text.strip()

            # Location
            location = job.find_element(By.CSS_SELECTOR, "em.remote-location-text").text.strip()

            # Posted date
            posted_date = job.find_element(By.CSS_SELECTOR, "p.posted-date").text.strip()

            # Job link
            job_link = job.find_element(By.CSS_SELECTOR, "a.job-card-title").get_attribute("href")

            # Store job data
            jobs_data.append({
                "Title": title,
                "Company": company,
                "Salary": salary,
                "Description": description,
                "Location": location,
                "Posted Date": posted_date,
                "Link": "https://www.theladders.com" + job_link
            })

            print(f"Scraped: {title} | {company} | {location}")

        except Exception as e:
            print(f"Error extracting job: {e}")

    print(f"\nTotal Jobs Found: {len(job_cards)}")

except Exception as e:
    print(f"Failed to scrape jobs: {e}")

finally:
    driver.quit()

# Save data to JSON
json_file = "theladders_jobs.json"
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(jobs_data, file, indent=4, ensure_ascii=False)

print(f"\nJob data saved to {json_file} (JSON) ")

# Save data to CSV
csv_file = "theladders_jobs.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Title", "Company", "Salary", "Description", "Location", "Posted Date", "Link"])
    writer.writeheader()
    writer.writerows(jobs_data)

print(f"\nJob data saved to {csv_file}")
