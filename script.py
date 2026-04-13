from dotenv import load_dotenv
import os
load_dotenv()
user_email = os.getenv("CREDENTIALS_EMAIL")
user_password = os.getenv("CREDENTIALS_PASSWORD")

import requests
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://learn.inside.dtu.dk")

#login logic
username_input = driver.find_element(By.ID, "userNameInput")
username_input.send_keys(user_email)
password_input = driver.find_element(By.ID, "passwordInput")
password_input.send_keys(user_password)
driver.find_element(By.ID, "submitButton").click()
wait = WebDriverWait(driver, timeout=5)
element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

#reuse selenium's cookies after logging in
selenium_cookies = driver.get_cookies()
session = requests.Session()
for cookie in selenium_cookies:
    session.cookies.set(cookie['name'], cookie['value'])

driver.close()

enrollments = session.get("https://learn.inside.dtu.dk/d2l/api/lp/1.47/enrollments/myenrollments/").json()
mycourses = session.get("https://learn.inside.dtu.dk/d2l/le/manageCourses/api/mycourses").json()


def get_course_id_from_course_no(course_no, users_courses):
    for course_metadata_ in users_courses.get("Courses"):
        if course_metadata_.get("Name").split(" ")[0] == course_no:
            return course_metadata_.get("OrgUnitId")

def sanitize_filename(name):
    # replace any character that's invalid in filenames
    return re.sub(r'[<>:"/\\|?*]', '-', name)

course_id = get_course_id_from_course_no("02160", mycourses)
course_data = session.get(f"https://learn.inside.dtu.dk/d2l/api/le/1.47/{course_id}/content/root/").json()

print("Downloading...")
no_files = 0
for tab in course_data:
    for document in tab.get("Structure"):
        document_id = document.get("Id")
        document_title = sanitize_filename(document.get("Title"))
        url = f"https://learn.inside.dtu.dk/d2l/le/content/{course_id}/topics/files/download/{document_id}/DirectFileTopicDownload"

        response = session.get(url)
        if response.status_code != 200:
            continue

        with open(document_title, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {document_title}")

        no_files += 1

print(f"Downloaded {no_files} files")

#TODO: add logic for considering modules and take action based on this
#TODO: find a way of knowing file type prior to saving (to add suffix)
#TODO: add alt way of specifying credentials

#Interesting note: courses you TA'd do not count/work

#File type 1 is file i.e. works with DirectFileTopicDownload
#File type 0 is a module/folder, requires recursion

#test ID = 02160 -> 187639 (agile, old PREFERRED) or 296238 (agile, new)
# course ID != course no.
# direct download
#https://learn.inside.dtu.dk/d2l/le/content/{course ID}/topics/files/download/{file ID}/DirectFileTopicDownload
# access a module (appears to be deprecated)
# https://learn.inside.dtu.dk/d2l/api/le/1.47/{course ID}/content/modules/{module ID}/structure/

#https://learn.inside.dtu.dk/d2l/api/le/1.47/296238/content/root/

