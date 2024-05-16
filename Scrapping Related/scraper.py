from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
import pandas as pd
from os.path import exists

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(options=options)
    return driver


def hide_onesignal_prompt(driver):
    try:
        # Wait until the OneSignal dialog is likely to have loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onesignal-slidedown-container')))
        # Execute JavaScript to hide the OneSignal dialog container
        driver.execute_script("document.getElementById('onesignal-slidedown-container').style.display = 'none';")
        print("OneSignal prompt hidden.")
    except Exception as e:
        print(f"Error hiding OneSignal prompt: {str(e)}")


def scrape_with_selenium():
    driver = setup_driver()
    driver.get("https://airdrops.io/latest/")
    hide_onesignal_prompt(driver)
    all_data = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))

        for _ in range(1):  # Ensure you're clicking 'Show More' as many times as you need
            try:
                show_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showmore > span"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                show_more_button.click()
                print("Clicked 'Show More'")
                time.sleep(2)
            except TimeoutException:
                print("No more 'Show More' button available or page took too long to respond.")
                break

        articles = driver.find_elements(By.TAG_NAME, 'article')
        article_links = []

        for article in articles:
            try:
                div = article.find_element(By.CSS_SELECTOR, 'div.inside-article')
                onclick_text = div.get_attribute('onclick')
                if onclick_text:
                    url = onclick_text.split("'")[1]
                    article_links.append(url)
            except NoSuchElementException:
                continue

        for link in article_links:
            driver.get(link)
            time.sleep(1)

            try:
                # Check if the airdrop listing is expired
                article_div = driver.find_element(By.CSS_SELECTOR, 'div.inside-article')
                is_expired = "expired" in article_div.get_attribute("class")
            except NoSuchElementException:
                print(f"Article div not found for URL {link}, may be expired or not available.")
                continue

            try:
                title = driver.find_element(By.TAG_NAME, 'h1').text 
            except NoSuchElementException:
                title = "n/a"

            try:   
                features = driver.find_element(By.CSS_SELECTOR, 'span.drop-features p').text 
            except NoSuchElementException:
                features = "n/a"

            try:
                guide_elements = driver.find_elements(By.CSS_SELECTOR, 'div.airdrop-guide li')
                guide = [f"{idx + 1}. {li.text}" for idx, li in enumerate(guide_elements)] 
            except NoSuchElementException:
                guide = ["n/a"]

            airdrop_info = driver.find_element(By.CLASS_NAME, 'airdrop-info')
            
            try:
                total_value_element = airdrop_info.find_element(By.XPATH, './/li[contains(text(), "Total value:")]')
                total_value = total_value_element.text.split(': ')[1] if ':' in total_value_element.text else total_value_element.text
            except NoSuchElementException:
                total_value = "n/a"

            try:
                platform_element = airdrop_info.find_element(By.XPATH, './/li[contains(text(), "Platform:")]')
                platform = platform_element.text.split(': ')[1] if ':' in platform_element.text else platform_element.text
            except NoSuchElementException:
                platform = "n/a"

            # Extracting the Requirements
            requirements = []
            try:
                requirement_sections = driver.find_elements(By.CSS_SELECTOR, ".aidrop-req-wrapper.grid-33.grid-parent")
                if requirement_sections:
                    for section in requirement_sections:
                        req_title = section.find_element(By.CSS_SELECTOR, ".aidrop-req-title").text
                        # Removing the trailing 'required'
                        req_title = req_title.replace(" required", "")
                        req_items = section.find_elements(By.TAG_NAME, "li")
                        req_details = []
                        for idx, item in enumerate(req_items):
                            item_text = item.text.strip()
                            if item_text:  # Only add if there's text
                                req_details.append(f"{idx + 1}) {item_text}")
                        if req_details:
                            formatted_details = ", ".join(req_details)
                            requirements.append(f"{req_title}: {formatted_details}")
                        else:
                            requirements.append(req_title)  # Add without colon if no details
                else:
                    print("No requirement sections found.")
            except Exception as e:
                print(f"Error processing requirements: {str(e)}")

            formatted_requirements = "; ".join(requirements) if requirements else "n/a"
            print(f"Requirements for {url}: {formatted_requirements}")



            # Handling various status scenarios
            status = "n/a"  # Default status
            status_elements = airdrop_info.find_elements(By.TAG_NAME, 'li')
            for status_element in status_elements:
                if "unconfirmed" in status_element.text.lower():
                    status = "Airdrop Unconfirmed"
                    break
                elif "confirmed" in status_element.text.lower():
                    status = "Airdrop Confirmed"
                    break
            if is_expired:
                status = "Expired"

            all_data.append({
                "title": title,
                "features": features,
                "guide": guide,
                "total_value": total_value,
                "status": status,
                "platform": platform,
                "requirements": formatted_requirements
            })

    finally:
        driver.quit()

    return all_data

def merge_and_update_data(new_data, filename='airdrops_data.csv'):
    new_df = pd.DataFrame(new_data)
    if exists(filename):
        existing_df = pd.read_csv(filename)
        updated_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['title'], keep='last')
    else:
        updated_df = new_df
    updated_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Data saved/updated in '{filename}'.")

scraped_data = scrape_with_selenium()
merge_and_update_data(scraped_data)


