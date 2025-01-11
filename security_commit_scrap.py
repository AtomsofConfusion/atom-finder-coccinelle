import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup Selenium WebDriver
def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Lock for thread-safe CSV writing
from threading import Lock
write_lock = Lock()

# Create a CSV file to save results
csv_filename = "CVE_Git_Commits.csv"

# Write header row to CSV file
with open(csv_filename, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["CVE ID", "Git Commit URL"])  # Add header row

# Process a single page of a month-year combination
def process_page(year, month, page):
    driver = setup_driver()
    try:
        url = f"https://www.cvedetails.com/vulnerability-list/year-{year}/month-{month}/{month_name(month)}.html?page={page}&order=1"
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Handle cookie consent
        close_cookie_consent(driver)

        # Print current URL for debugging
        print(f"Processing URL: {url}")

        # Extract CVE links from the page
        cve_links = extract_cve_links(driver)
        if not cve_links:
            print(f"No CVE entries found for {month_name(month)} {year} on page {page}.")
            return

        # Visit each CVE page and extract references
        for link in cve_links:
            visit_cve_page_and_extract_references(driver, link)
    except Exception as e:
        print(f"Error processing page {page} for {month_name(month)} {year}: {e}")
    finally:
        driver.quit()

# Function to extract CVE links from the page
def extract_cve_links(driver):
    cve_links = []
    try:
        cve_link_xpath = "/html/body/div[1]/div/div[2]/div/main/div[3]/div[3]//a"
        cve_elements = driver.find_elements(By.XPATH, cve_link_xpath)
        for cve_button in cve_elements:
            href = cve_button.get_attribute("href")
            if href:
                cve_links.append(href)
    except Exception as e:
        print(f"Error while extracting CVE links: {e}")
    return cve_links

# Function to visit a CVE page and extract references
def visit_cve_page_and_extract_references(driver, cve_url):
    try:
        driver.get(cve_url)
        time.sleep(3)
        print(f"Visiting CVE page: {driver.title}")

        close_cookie_consent(driver)
        cve_id = extract_cve_id_from_title(driver.title)
        extract_references(driver, cve_id)
    except Exception as e:
        print(f"Error visiting CVE page {cve_url}: {e}")

# Function to extract and save reference links
def extract_references(driver, cve_id):
    try:
        section_idx = 1
        while True:
            if(section_idx == 10):
                break;
            header_xpath = f"/html/body/div[1]/div/div[2]/div/main/div[{section_idx}]/h2"
            try:
                header = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, header_xpath))
                )
                if "References for CVE-" in header.text:
                    print("Found references section!")
                    references_section_xpath = f"/html/body/div[1]/div/div[2]/div/main/div[{section_idx}]/div/ul"
                    reference_links = driver.find_elements(By.XPATH, references_section_xpath + "/li/a")
                    for link in reference_links:
                        href = link.get_attribute("href")
                        if href and is_git_commit_url(href):
                            print(f"Saving: {cve_id} -> {href}")
                            with write_lock:
                                # Save to CSV instead of Excel
                                with open(csv_filename, mode="a", newline='', encoding="utf-8") as file:
                                    writer = csv.writer(file)
                                    writer.writerow([cve_id, href])  # Save to CSV
                    break
            except Exception:
                pass
            section_idx += 1
    except Exception as e:
        print(f"Error extracting references for CVE {cve_id}: {e}")

# Function to close cookie consent banner
def close_cookie_consent(driver):
    try:
        cookie_consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/a[2]"))
        )
        cookie_consent_button.click()
    except Exception:
        pass

# Function to check if URL is a Git commit URL
def is_git_commit_url(url):
    import re
    match = re.fullmatch(r"https://github\.com/[^/]+/[^/]+/commit/[a-f0-9]{40}", url)
    return match is not None

# Function to extract CVE ID from page title
def extract_cve_id_from_title(title):
    if "CVE-" in title:
        return title.split("CVE-")[1].split()[0]
    return "Unknown-CVE"

# Get month name from number
def month_name(month):
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return months[month]

# Parallelize processing of pages
def process_month_year(year, month):
    with ThreadPoolExecutor() as executor:
        futures = []
        for page in range(1, 30):  # Assume 50 pages max
            futures.append(executor.submit(process_page, year, month, page))

        # Wait for all futures to complete
        for future in as_completed(futures):
            future.result()

# Iterate through years and months
def iterate_all_years_and_months():
    for year in range(2015, 2016):
        for month in range(1, 2):
            process_month_year(year, month)

if __name__ == "__main__":
    iterate_all_years_and_months()
    print(f"Data saved to {csv_filename}")
