from socket import if_nameindex
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
# from selenium import WebDriverWait
from requests.utils import quote
from bs4 import BeautifulSoup
import json
import traceback
import sys
import time

import re

CURRENT_USERNAME=""
CURRENT_PASS=""
BANNED=False
END_SCRIPT=False
LOGGED_IN=False

#incase linkedin automatically logs out
def login_checker(driver1, last_url):
    sleep(2)
    if "authwall" in driver1.current_url or "login" in driver1.current_url:
        login(driver1)
        driver1.get(last_url)
    try:
        if (driver1.find_element_by_class_name("secondary-action")) or ("check" in driver1.current_url):
            driver1.get(last_url)
    except:
        print("Everything is good, still logged in")

def logout(driver1):
    driver1.get("https://www.linkedin.com/m/logout/")
    global LOGGED_IN
    LOGGED_IN=False

def login(driver1):
    # Load the page on the browser
    driver1.get('https://www.linkedin.com')
    wait = randint(6, 10)
    sleep(wait)
    username = driver1.find_element_by_id('session_key')
    username.send_keys(CURRENT_USERNAME)
    wait = randint(4, 5)
    sleep(wait)

    # locate password form by_class_name
    password = driver1.find_element_by_id('session_password')
    # send_keys() to simulate key strokes
    password.send_keys(CURRENT_PASS)
    sleep(5)
    # locate submit button by_class_name
    log_in_button = driver1.find_element_by_class_name('sign-in-form__submit-button')
    # .click() to mimic button click
    log_in_button.click()

    global LOGGED_IN
    LOGGED_IN=True

    wait = randint(8, 12)
    sleep(wait)

def ban_checker(driver1):
    try:
        banned_account=""
        accounts=""
        ban_string = driver1.find_element_by_class_name('t-sans.t-18.t-black.t-normal.text-align-center.mt4').text
        if "upgrade to get unlimited people browsing" in ban_string:
            with open("unbanned_accounts.json", "r", encoding="utf8") as write_file2:
                accounts = json.load(write_file2)
                banned_account = accounts.pop(0)
                print(accounts[0]["username"])
                global CURRENT_USERNAME
                CURRENT_USERNAME = accounts[0]["username"]
                global CURRENT_PASS 
                CURRENT_PASS= accounts[0]["password"]
            with open("unbanned_accounts.json", "w", encoding="utf8") as write_file2:
                json.dump(accounts, write_file2, ensure_ascii=False)
            with open("banned_accounts.json", "r", encoding="utf8") as write_file3:
                accounts = json.load(write_file3)
                accounts.append(banned_account)
            with open("banned_accounts.json", "w", encoding="utf8") as write_file3:
                json.dump(accounts, write_file3, ensure_ascii=False)
            logout(driver1)
            # login(driver1)
            return True
        else:
            return False
    except Exception as e:
        print("ban_checker function threw exception")
        return False

def searcher(text):
    for foS in data_skill_read:
        for skill in data_skill_read[foS]:
            try:
                '''
                if re.search(r"\b"+skill["skill_name"]+"\b", text) is not None: 
                    print(skill["skill_name"], "has been found")
                    skill["count"] += 1
                '''
                if skill["skill_name"] in text:
                    skill["count"] += 1
            except:
                if skill["skill_name"] in text: 
                    skill["count"] += 1

with open("unbanned_accounts.json", "r", encoding="utf8") as read_file1:
    free_accounts = json.load(read_file1)
    CURRENT_USERNAME = free_accounts[0]["username"]
    CURRENT_PASS = free_accounts[0]["password"]

data_skill_read={}
with open("search_skill.json", "r", encoding="utf8") as read_file:
    data_skill_read = json.load(read_file)

# Creation of a new instance of Google Chrome
driver = webdriver.Chrome(executable_path= r'C:\Users\EGE\Desktop\ENS491\career path\chromedriver_win32\chromedriver.exe')

if not LOGGED_IN: login(driver)

search_skills = open('search_skill.json', 'r')
search_skills_data = json.load(search_skills)

driver.get("https://www.linkedin.com/jobs/search/?geoId=102105699&keywords=computer%20science&location=Turkey")
sleep(7)

page_number = 1

for page_index in range(0, 10): #this is how many pages of job list we want to iterate for now
    job_count = len(driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view"))
    print("========================================================================================================\nNumber of jobs found:", job_count)
    for job_index in range(0,job_count):
        driver.execute_script("document.getElementsByClassName( 'jobs-search-results__list-item occludable-update p0 relative ember-view' )[" + str(job_index) + "].scrollIntoView();")
        driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")[job_index].click()
        job_title = driver.find_element_by_class_name("jobs-details-top-card__job-title.t-20.t-black.t-normal").text
        try:
            curr_company = driver.find_element_by_class_name("jobs-details-top-card__company-url.t-black--light.t-normal.ember-view").text
        except:
            continue
        print("Company:", curr_company, "---------", job_index)
        text = driver.find_element_by_class_name("jobs-box__html-content.jobs-description-content__text.t-14.t-normal").text
        searcher(str(text))
        sleep(2)
    #driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")[page_number].click()
    driver.get("https://www.linkedin.com/jobs/search/?geoId=102105699&keywords=computer%20science&location=Turkey&start=" + str(page_number*25))
    page_number+=1
    with open("search_skill.json", "w", encoding="utf8") as write_file:
        json.dump(data_skill_read, write_file, ensure_ascii=False)
    sleep(3)


