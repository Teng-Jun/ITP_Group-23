from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-notifications")  # Disable notifications

# Set up the ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the page
url = "https://de.fi/rekt-database"
driver.get(url)

# Maximize the browser window
driver.maximize_window()
print("Browser window maximized.")

# Wait for the page to load
time.sleep(10)

# Handle the "Got It" pop-up if it appears
try:
    got_it_button = driver.find_element(By.XPATH, "//button[contains(text(),'Got It')]")
    got_it_button.click()
    print("Clicked 'Got It' pop-up.")
except Exception as e:
    print("No 'Got It' pop-up appeared or could not click:", e)

# Wait for the overlay to disappear
time.sleep(5)  # Additional wait for safety

# Define lists to store the scraped data
project_names = []
chain_names = []
funds_lost = []
dates = []
issue_types = []

# Function to scrape data from the page
def scrape_data():
    try:
        # Use page source to get the full HTML
        inner_html = driver.page_source
        soup = BeautifulSoup(inner_html, 'html.parser')

        # Find all scam entry rows with the correct class
        scam_entries = soup.find_all('div', class_='scam-database-row')  # Generalized to avoid class-specific issues
        print(f"Found {len(scam_entries)} scam entries.")

        # Scrape data for the entries
        for entry in scam_entries:
            try:
                # Get the project name
                project_name_elem = entry.find('div', class_='name-wrapper').find('span')
                project_name = project_name_elem.text.strip() if project_name_elem else "N/A"
                project_names.append(project_name)
                print(f"Project Name: {project_name}")  # Print project name

                # Get the chain name
                chain_name_elem = entry.find('div', class_='name-wrapper').find('p')
                chain_name = chain_name_elem.text.strip() if chain_name_elem else "N/A"
                chain_names.append(chain_name)
                print(f"Chain Name: {chain_name}")  # Print chain name

                # Get the type of issue
                issue_type_elem = entry.find_all('div', class_='column-rekt-function')
                issue_type = issue_type_elem[0].text.strip() if issue_type_elem else "N/A"
                issue_types.append(issue_type)
                print(f"Issue Type: {issue_type}")  # Print issue type

                # Get the funds lost
                funds_lost_elem = entry.find('div', class_='column funds-lost')
                funds_lost_value = funds_lost_elem.text.strip() if funds_lost_elem else "N/A"
                funds_lost.append(funds_lost_value)
                print(f"Funds Lost: {funds_lost_value}")  # Print funds lost

                # Get the date
                date_elem = entry.find('div', class_='date')
                date_value = date_elem.text.strip() if date_elem else "N/A"
                dates.append(date_value)
                print(f"Date: {date_value}")  # Print date

                print("-" * 40)  # Separator for clarity

            except Exception as e:
                print(f"Error processing entry: {e}")
                continue
    except Exception as e:
        print(f"Error locating scam entries: {e}")

# Scrape the initial data
scrape_data()

# Loop through pages
while True:
    try:
        # Click the "Next" button
        next_button = driver.find_element(By.XPATH, "//div[contains(@class, 'arrow right')]")
        next_button.click()  # Click the "Next" button
        print("Clicked 'Next' button.")
        
        time.sleep(5)  # Wait for new entries to load

        # Check if the "Next" button is disabled after a short delay
        time.sleep(5)  # Buffer time for button state to update
        if 'disabled' in next_button.get_attribute('class'):
            print("Next button is disabled. Exiting loop.")
            break  # Exit loop if the "Next" button is disabled

        # Scrape data from the new page
        scrape_data()

    except Exception as e:
        print("No more pages to navigate or error clicking 'Next':", e)
        break  # Exit loop if no more pages or an error occurs

# Store the data in a pandas DataFrame
scam_data = pd.DataFrame({
    "Project Name": project_names,
    "Chain Name": chain_names,
    "Funds Lost": funds_lost,
    "Issue Type": issue_types,
    "Date": dates,
})

# Close the browser
driver.quit()

# Show the DataFrame or save to CSV
print(scam_data)
# Save to CSV if needed
scam_data.to_csv("scam_airdrop_data.csv", index=False)
