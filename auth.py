from dotenv import load_dotenv
import os
load_dotenv()
user_email = os.getenv("CREDENTIALS_EMAIL")
user_password = os.getenv("CREDENTIALS_PASSWORD")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests


def get_authenticated_session():
    driver = webdriver.Chrome()
    driver.get("https://learn.inside.dtu.dk")

    #login logic
    username_input = driver.find_element(By.ID, "userNameInput")
    username_input.send_keys(user_email)
    password_input = driver.find_element(By.ID, "passwordInput")
    password_input.send_keys(user_password)
    driver.find_element(By.ID, "submitButton").click()
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

    #reuse selenium's cookies after logging in
    selenium_cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    driver.close()
    return session