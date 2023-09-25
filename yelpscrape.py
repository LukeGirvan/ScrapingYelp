import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
BASE_URL = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Belfast'
COOKIE_NOTIFICATION_XPATH = '//*[@id="onetrust-reject-all-handler"]'
NEXT_BUTTON_XPATH = '//*[@id="main-content"]/div/ul/li[13]/div/div[1]/div/div[11]/span/a'
MAX_PAGES = 10

def close_cookie_notification(driver):
    try:
        cookie_notification = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, COOKIE_NOTIFICATION_XPATH))
        )
        accept_button = cookie_notification.find_element(By.XPATH, COOKIE_NOTIFICATION_XPATH)
        accept_button.click()
    except Exception as e:
        print(f"Error handling cookie notification: {str(e)}")

def scrape_restaurants(driver):
    top_10_restaurants = []

    for page in range(1, MAX_PAGES + 1):
        for i in range(3, 13):
            restaurant = {}
            restaurant['name'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a').text
            restaurant['review'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div').text
            restaurant['img'] = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div/ul/li[{i}]/div[1]/div/div/div[1]/div/div/div/div/div/div/div[1]/div/a/img').get_attribute('src')
            top_10_restaurants.append(restaurant)

        # Click the "Next" button to go to the next page
        next_button = driver.find_element(By.XPATH, NEXT_BUTTON_XPATH)
        next_button.click()

        # Wait for a random time (to mimic human behavior)
        time.sleep(random.uniform(2, 5))

    return top_10_restaurants

def main():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    # Close or dismiss the cookie notification
    close_cookie_notification(driver)

    top_10_restaurants = scrape_restaurants(driver)

    # Print or process the scraped restaurant information
    for restaurant in top_10_restaurants:
        print(f"Name: {restaurant['name']}")
        print(f"Review: {restaurant['review']}")
        print(f"Image URL: {restaurant['img']}")

    driver.quit()

if __name__ == "__main__":
    main()








