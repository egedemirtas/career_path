from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
# from selenium import WebDriverWait
from requests.utils import quote
from bs4 import BeautifulSoup
import json
from fuzzywuzzy import fuzz
from selenium.webdriver.chrome.options import Options


# # Creation of a new instance of Google Chrome
#driver = webdriver.Chrome(executable_path=r'C:\Users\EGE\Desktop\ENS491\career path\chromedriver_win32\chromedriver.exe')           

opts = Options()
opts.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'")

driver = webdriver.Chrome(options=opts, executable_path=r'C:\Users\EGE\Desktop\ENS491\career path\chromedriver_win32\chromedriver.exe')

# Load the page on the browser
driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys('egealperdemirkaya@gmail.com')
sleep(4.3)

# locate password form by_class_name
password = driver.find_element_by_id('session_password')
# send_keys() to simulate key strokes
password.send_keys('ege97alper99')
sleep(6.2)

sleep(0.5)
# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

log_in_button.click()
wait = randint(7,10)
sleep(wait)

data = {}


f = open('top50_uni_facet.json','r')
uni_names = json.load(f)

uni_list=[]

for uni_name in uni_names:
    #search = driver.find_element_by_class_name('search-global-typeahead__input always-show-placeholder')

    
    univ = quote(uni_name)
    #driver.get('https://www.linkedin.com/search/results/schools/?keywords=%C4%B0zmir%20K%C3%A2tip%20%C3%87elebi%20%C3%9Cniversitesi&origin=SWITCH_SEARCH_VERTICAL')
    driver.get('https://www.linkedin.com/search/results/schools/?keywords='+univ+'&origin=SWITCH_SEARCH_VERTICAL')
    #search_query = driver.find_element_by_name('q')
    wait = randint(3,5)
    sleep(wait)

    # selected_uni = driver.find_elements_by_class_name("entity-result__title-line.flex-shrink-1.entity-result__title-text--black")
    selected_uni = driver.find_elements_by_class_name("entity-result__title-text.t-16")
    
    try:
        if uni_name.strip() == 'Bahcesehir Universitesi':
            raise Exception("")

        selected_uni[0].click()

        sleep(3)
        
        driver.get(str(driver.current_url)+"people/")

        #print(selected_uni)
        wait =randint(3,5)
        sleep(wait)

        select_uni_name = driver.find_element_by_class_name("org-top-card-summary__title.t-24.t-black.t-bold.truncate").text
        print("uni name in file:", uni_name)
        print("uni name in linkedin:", select_uni_name)
        print("---------------------------------")
        
        alumni_number = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
        
        uni_list.append({"uni_name": uni_name, "alumni_count": alumni_number})

        wait = randint(3,5)
        sleep(wait)
    except Exception as e:
        print(e)
        wait = randint(1,3)
        sleep(wait)
        print(uni_name, " could not found")
    #break

with open("universities_alumni_number.json", "w", encoding="utf8") as write_file:
    json.dump(uni_list, write_file,ensure_ascii=False)


