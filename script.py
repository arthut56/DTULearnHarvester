from dotenv import load_dotenv
import os
load_dotenv()
user_email = os.getenv("CREDENTIALS_EMAIL")
user_password = os.getenv("CREDENTIALS_PASSWORD")

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup

from utils import wait_for_shadow_element

driver = webdriver.Chrome()
driver.get("https://learn.inside.dtu.dk")

#login logic
username_input = driver.find_element(By.ID, "userNameInput")
username_input.send_keys(user_email)
password_input = driver.find_element(By.ID, "passwordInput")
password_input.send_keys(user_password)
driver.find_element(By.ID, "submitButton").click()

# at this point, you're in the main page
wait = WebDriverWait(driver, timeout=10)  # wait up to 10 seconds
host = wait.until(EC.presence_of_element_located((By.TAG_NAME, "d2l-my-courses-v2")))

shadow_root1 = driver.execute_script("return arguments[0].shadowRoot", host)
host2 = shadow_root1.find_element(By.CSS_SELECTOR, "d2l-my-courses-container-v2")
shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", host2)
time.sleep(1)

shadow_root2.find_elements(By.CSS_SELECTOR, "d2l-tab")[0].click()
time.sleep(1)
driver.quit()