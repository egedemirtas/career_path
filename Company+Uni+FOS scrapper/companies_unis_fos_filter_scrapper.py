from socket import if_nameindex
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
# from selenium import WebDriverWait
from requests.utils import quote
from bs4 import BeautifulSoup
import json
import ScrapperClass
import traceback
import sys
import time


CURRENT_USERNAME=""
CURRENT_PASS=""
BANNED=False
END_SCRIPT=False
LOGGED_IN=False

#incase linkedin automatically logs out
def login_checker(driver1, last_url):
    sleep(2)
    if "authwall" in driver1.current_url or "login" in driver1.current_url or "https://www.linkedin.com" == driver1.current_url:
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
    wait = randint(7, 10)
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

    wait = randint(14, 25)
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


with open("unbanned_accounts.json", "r", encoding="utf8") as write_file1:
    free_accounts = json.load(write_file1)
    CURRENT_USERNAME = free_accounts[0]["username"]
    CURRENT_PASS = free_accounts[0]["password"]

# Creation of a new instance of Google Chrome
driver = webdriver.Chrome(executable_path= r'C:\Users\EGE\Desktop\ENS491\career path\chromedriver_win32\chromedriver.exe')



scrapper = ScrapperClass.Scrapper()


while not END_SCRIPT:
    if not LOGGED_IN: login(driver)

    # f_universities = open('top50_uni_facet.json', 'r')
    f_universities = open('top50_uni_facet.json', 'r')
    data_university_read = json.load(f_universities)

    f_fieldofstudy = open('fieldofstudy.json', 'r')
    data_fieldofstudy_read = json.load(f_fieldofstudy)

    f = open('companies_large.json', 'r')
    data_read = json.load(f)

    double_buffer = True

    data = {}
    fos_dict = {}
    univ = ""
    foS = ""
    company_link = ""
    company_name = ""
    removeitems = []
    num_filters=0
    latest_save_file=""
    last_url=""

    companies=[]
    if scrapper.getCurrUniv() != '':
        for i,item in enumerate(data_read):
            if scrapper.getCurrUniv() == item:
                break
            removeitems.append(item)

        for i in removeitems:
            data_read.pop(i)
    try:
        start_time = time.time()
        for company_link in data_read:
            print("time passed: ", time.time() - start_time, "===================================================================")
            print("Company Link:", company_link)
            scrapper.setCurrUniv(company_link)
            company = {}
            univ_dict = {}

            #go to company link
            last_url=company_link+"/people/"
            driver.get(last_url)
            wait = randint(8, 13)
            sleep(wait)
            BANNED = ban_checker(driver)##########################################################################################################
            if BANNED: break
            login_checker(driver,last_url)##############################################################################################
            num_filters = num_filters+1
            
            #get company name
            company_name = driver.find_element_by_class_name("org-top-card-summary__title.t-24.t-black.t-bold.truncate").text
            print(company_name)

            #get company employee number
            company_emp_num = -1
            try:
                company_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
            except:
                sleep(wait)
                BANNED = ban_checker(driver)##########################################################################################################
                if BANNED: break
                login_checker(driver,last_url)##############################################################################################
                company_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
                print("company num:", company_emp_num, "==================================================================")

            #assign company name
            company["company_name"] = company_name
            #assign company emp number
            company["company_emp_count"] = company_emp_num
            #assign uni array
            company["universities"] = []
            
            #data_university_read = uni name: facet
            for univ in data_university_read:
                #initialize uni object
                university={}
                #assign uni name
                university["uni_name"] = univ
                #initialize field array
                university["fields"] = []

                #go to: Amazon && 
                last_url=company_link + "/people/?facetSchool=" +data_university_read[univ]
                driver.get(last_url)
                wait = randint(8, 13)
                sleep(wait)
                BANNED = ban_checker(driver)##########################################################################################################
                if BANNED: break
                login_checker(driver,last_url)##############################################################################################
                num_filters = num_filters+1

                #assign uni specific emp number
                uni_emp_num = -1
                try:
                    uni_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
                except:
                    sleep(wait)
                    BANNED = ban_checker(driver)##########################################################################################################
                    if BANNED: break
                    login_checker(driver,last_url)##############################################################################################
                    uni_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
                    print("uni num:", uni_emp_num, "==================================================================")
                university["uni_emp_count"] = uni_emp_num

                if uni_emp_num == -1 or uni_emp_num > 0:
                    for foS in data_fieldofstudy_read:
                        print(
                            "Go to:", company_link + "/people/?facetFieldOfStudy=" +data_fieldofstudy_read[foS] + "&facetSchool=" +data_university_read[univ])
                        #go to Amazon && Sabanci && CS
                        #apply filters
                        last_url=company_link + "/people/?facetFieldOfStudy=" +data_fieldofstudy_read[foS] + "&facetSchool=" +data_university_read[univ]
                        driver.get(last_url)
                        wait = randint(8, 13)
                        sleep(wait)
                        BANNED = ban_checker(driver)##########################################################################################################
                        if BANNED: break
                        login_checker(driver,last_url)##############################################################################################
                        num_filters = num_filters+1

                        #create a field obj: "computerscience"
                        field = {}
                        field["field_name"] = foS

                        #add uni specific && fos specific emp number
                        fos_emp_num = -1
                        try:
                            fos_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
                        except:
                            sleep(wait)
                            BANNED = ban_checker(driver)##########################################################################################################
                            if BANNED: break
                            login_checker(driver,last_url)##############################################################################################
                            fos_emp_num = int(((driver.find_element_by_class_name("t-20.t-black.t-bold").text).split(" ")[0]).replace(',', ''))
                            print("uni num:", fos_emp_num, "==================================================================")
                        field["fos_emp_count"] = fos_emp_num

                        #add details to the field
                        details = {
                            "What they do": [],
                            "What they are skilled at": []
                        }

                        soup = BeautifulSoup(
                            driver.find_element_by_tag_name("body").get_attribute(
                                "innerHTML"), 'html.parser')

                        #what they do
                        soup3 = BeautifulSoup(
                            str(
                                soup.findAll(
                                    "div",
                                    class_=
                                    "artdeco-card p4 m2 org-people-bar-graph-module__current-function"
                                )), 'html.parser')
                        whereTheyDo_arr = soup3.get_text("|",
                                                        strip=True).split("|")[2:-1]
                        print("this is where they do array :", whereTheyDo_arr)

                        for i in range(0, len(whereTheyDo_arr), 2):
                            details["What they do"].append({"skill":whereTheyDo_arr[i + 1],"count":whereTheyDo_arr[i]})


                        #what they skilled
                        soup4 = BeautifulSoup(
                            str(
                                soup.findAll(
                                    "div",
                                    class_=
                                    "artdeco-card p4 m2 org-people-bar-graph-module__skill-explicit"
                                )), 'html.parser')
                        whereTheySkilled_arr = soup4.get_text(
                            "|", strip=True).split("|")[3:-1]
                        print("this is where they skilled array :",
                            whereTheySkilled_arr)

                        for i in range(0, len(whereTheySkilled_arr), 2):
                            details["What they are skilled at"].append({"skill":whereTheySkilled_arr[i + 1],"count":whereTheySkilled_arr[i]})
                        field["details"] = details
                        university["fields"].append(field)
                else:
                    for foS in data_fieldofstudy_read:
                        #create a field obj: "computerscience"
                        field = {}
                        field["field_name"] = foS

                        field["fos_emp_count"] = 0

                        #add details to the field
                        details = {
                            "What they do": [],
                            "What they are skilled at": []
                        }
                        field["details"] = details
                        university["fields"].append(field)
                
                BANNED = ban_checker(driver)##########################################################################################################
                if BANNED: break
                company["universities"].append(university)
            companies.append(company)
            BANNED = ban_checker(driver)##########################################################################################################
            if BANNED: break

            #https://www.linkedin.com/company/amazon/
            # last_char=len(company_link)-1
            # with open(company_link[company_link[:last_char].rfind("/")+1:last_char] +".json", "w", encoding="utf8") as write_file:
            #     json.dump(data, write_file,ensure_ascii=False)
            if (double_buffer):
                data=""
                with open("data_dummy1.json", "r", encoding="utf8") as write_file:
                    try:
                        data = json.load(write_file)
                        for c in companies:
                            data.append(c)
                    except:
                        data=companies
                with open("data_dummy1.json", "w", encoding="utf8") as write_file:
                    json.dump(data, write_file, ensure_ascii=False)
                    # json.dump(companies, write_file, ensure_ascii=False)
                double_buffer = False
                latest_save_file = "data_dummy1.json"
            else:
                data=""
                with open("data_dummy2.json", "r", encoding="utf8") as write_file:
                    try:
                        data = json.load(write_file)
                        for c in companies:
                            data.append(c)
                    except:
                        data=companies
                with open("data_dummy2.json", "w", encoding="utf8") as write_file:
                    json.dump(data, write_file, ensure_ascii=False)
                    # json.dump(companies, write_file, ensure_ascii=False)
                double_buffer = True
                latest_save_file = "data_dummy2.json"
            if company_link=="https://www.linkedin.com/company/speletchat/": 
                END_SCRIPT=True
                break

    except Exception as e:
        print(traceback.format_exc())
        print(sys.exc_info()[2])

        with open("data_dummy_e.json", "w", encoding="utf8") as write_file:
            json.dump(companies, write_file, ensure_ascii=False)

        with open("error_logs.txt", "w", encoding="utf8") as write_file:
            write_file.write("Last visted company: " + company_link + 
                            "\nUniv: " +univ + 
                            "\nFOS:" + foS + 
                            "\nfos_dict: " + str(fos_dict) + 
                            "\nNumber of filters applied: " + str(num_filters) +
                            "\nLatest save location:" + latest_save_file)

