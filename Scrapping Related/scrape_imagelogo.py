import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import time
import requests

def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
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

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

def scrape_images():
    folder_name = "potentialairdrops_images_crawled"
    create_folder(folder_name)

    driver = setup_driver()
    driver.get("https://airdrops.io/speculative/")
    hide_onesignal_prompt(driver)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))

        for _ in range(16):  # Ensure you're clicking 'Show More' as many times as you need
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
                title = driver.find_element(By.TAG_NAME, 'h1').text 
            except NoSuchElementException:
                title = "n/a"
                continue
            
            try:
                image_element = driver.find_element(By.CSS_SELECTOR, 'img.airdrop-logo')
                image_url = image_element.get_attribute('src')
                print(f"Image URL found: {image_url}")

                response = requests.get(image_url)
                if response.status_code == 200:
                    # Save the image to a file in the specified folder
                    with open(os.path.join(folder_name, f"{title}.jpg"), 'wb') as f:
                        f.write(response.content)
                    print(f"Image saved: {os.path.join(folder_name, f'{title}.jpg')}")
                else:
                    print(f"Failed to download image: {image_url}")
            except NoSuchElementException:
                print("Image not found.")
            except Exception as e:
                print(f"An error occurred while downloading the image: {str(e)}")

    finally:
        driver.quit()

scrape_images()
