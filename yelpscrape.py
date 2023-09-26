import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
BASE_URL = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Madrid%2C+Spain'
COOKIE_NOTIFICATION_XPATH = '//*[@id="onetrust-reject-all-handler"]'
MAX_PAGES = 10

# Function to handle the cookie notification
def close_cookie_notification(driver, COOKIE_NOTIFICATION_XPATH):
    try:
        # Wait for the cookie notification to appear and find the accept button
        cookie_notification = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, COOKIE_NOTIFICATION_XPATH))
        )
        accept_button = cookie_notification.find_element(By.XPATH, COOKIE_NOTIFICATION_XPATH)
        accept_button.click()  # Click on the accept button
    except Exception as e:
        print(f"Error handling cookie notification: {str(e)}")

# Function to scrape restaurants
def scrape_restaurants(driver, is_sponsored):
    top_10_restaurants = []

    # Determine the XPATH for the "Next" button based on whether the page has sponsors
    if is_sponsored:
        NEXT_BUTTON_XPATH = '//*[@id="main-content"]/div/ul/li[21]/div/div[1]/div/div[11]/span/a'
    else:
        NEXT_BUTTON_XPATH = '//*[@id="main-content"]/div/ul/li[13]/div/div[1]/div/div[11]/span/a'

    for page in range(1, MAX_PAGES + 1):
        # Determine the range of restaurant elements based on whether the page has sponsors
        for i in range(8 if is_sponsored else 3, 18 if is_sponsored else 13):
            restaurant = {}
            # Extract restaurant information using XPATHs
            restaurant['name'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a').text
            restaurant['review'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div').text
            restaurant['img'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div[1]/div/div/div[1]/div/div/div/div/div/div/div[1]/div/a/img').get_attribute('src')
            top_10_restaurants.append(restaurant)

        # Click the "Next" button to go to the next page
        try:
            next_button = driver.find_element(By.XPATH, NEXT_BUTTON_XPATH)
            next_button.click()
            print("Clicked on the 'Next' button successfully.")
        except Exception as e:
            print(f"Error clicking on the 'Next' button: {str(e)}")

        # Wait for a random time (to mimic human behavior)
        time.sleep(random.uniform(2, 5))

    return top_10_restaurants

# Function to check if there are sponsored results on the page
def is_sponsor(driver):
    try:
        sponsored_results = driver.find_element(By.XPATH, "//*[contains(@class, 'css-agyoef') and contains(text(), 'Sponsored Results')]")
        return True  # Sponsored results are present
    except Exception as e:
        return False  # Sponsored results are not present

# Main function
def main():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    close_cookie_notification(driver, COOKIE_NOTIFICATION_XPATH)
    is_sponsored = is_sponsor(driver)

    top_10_restaurants = scrape_restaurants(driver, is_sponsored)

    for restaurant in top_10_restaurants:
        print(f"Name: {restaurant['name']}")
        print(f"Review: {restaurant['review']}")
        print(f"Image URL: {restaurant['img']}")

    driver.quit()

if __name__ == "__main__":
    main()









