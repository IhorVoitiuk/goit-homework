from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless=chrome')


with webdriver.Chrome(service=service, options=options) as driver:

    driver.get("http://quotes.toscrape.com/login")
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "username")))
    username = driver.find_element(by=By.ID, value="username")
    password = driver.find_element(by=By.ID, value="password")

    username.send_keys("admin")
    password.send_keys("admin")
    sumbit = driver.find_element(by=By.XPATH, value="//input[@class='btn btn-primary']")
    sumbit.click()

    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, "quote")))
    html = driver.page_source
    links = driver.find_elements(by=By.TAG_NAME, value='a')
    for link in links:
        print(link.get_attribute('href'))

    sleep(3)
    driver.quit()