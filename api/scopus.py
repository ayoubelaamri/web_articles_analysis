import pandas as pd
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pymongo import MongoClient
 

def scrap_scopus(date,searchTerm):

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "D:\workspace\Business_Intelligence\BI_Project\dataset"}
    options.add_experimental_option("prefs",prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("start-maximized")

    # driver = webdriver.Chrome("./chromedriver.exe", chrome_options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print("-----> Fetching: https://www.scopus.com")
    print("-----> Login required ! Fetching login page ..")
    driver.get('https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D48f3e4805b880caf26d809cc11e5e07e&state=userLogin%7CtxId%3DCDFC20C34D2472E00424ABB73DEEB50F.i-0662f0017888dc2d0%3A4&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS')
    print("-----> Looking for email input ..")
    emailInput = driver.find_element(By.NAME, 'pf.username')
    print("-----> Typing email ..")
    emailInput.send_keys("senoralpha39@gmail.com")
    emailInput.send_keys(Keys.RETURN)
    try:
        print("-----> Looking for pass input ..")
        passInput_present = EC.presence_of_element_located((By.NAME, 'password'))
        WebDriverWait(driver, 20).until(passInput_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        print("-----> Typing password ..")
        passInput = driver.find_element(By.NAME, 'password')
        passInput.send_keys("147147147")
        passInput.send_keys(Keys.RETURN)

    try:
        searchInput_present = EC.presence_of_element_located((By.CLASS_NAME, 'flex-grow-1'))
        WebDriverWait(driver, 10).until(passInput_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        fieldInput = driver.find_element(By.XPATH, '//els-select[@label="Search within"]//select')
        fieldObject = Select(fieldInput)
        fieldObject.select_by_visible_text('All fields')

        # addYearButton = driver.find_element_by_class_name('button--link-black add-year-range-button margin-size-16-r')
        addYearButton = driver.find_element(By.XPATH, '//div[@class="button-slot-left"]//button')
        addYearButton.click()
        yearInput = driver.find_element(By.XPATH, '//els-select[@label="Published from"]//select')
        yearObject = Select(yearInput)
        yearObject.select_by_visible_text(date)

        print("-----> Looking for search Input...")
        searchInput = driver.find_element(By.CLASS_NAME, 'flex-grow-1')
        searchInput.send_keys(searchTerm)
        searchInput.send_keys(Keys.RETURN)

    try:
        element_present = EC.presence_of_element_located((By.ID, 'mainResults-allPageCheckBox'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        print("-----> Page loaded !")
        print("-----> Scraping data ...")

        checkAllButton = driver.find_element(By.XPATH, '//li[@id="selectAllCheck"]')
        checkAllButton.click()

        saveButton = driver.find_element(By.ID, 'directExport')
        saveButton.click()

    try:
        exportType_present = EC.presence_of_element_located((By.XPATH, '//div[@class="col-md-12 chunkExportForm"]/ul/li[1]'))
        # exportType_present = EC.presence_of_element_located((By.ID, 'exportTypeAndFormat'))
        WebDriverWait(driver, 20).until(exportType_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        exportType = driver.find_element(By.XPATH, '//div[@class="col-md-12 chunkExportForm"]/ul/li[1]')
        # exportType = driver.find_element(By.ID, 'exportTypeAndFormat')
        exportType.click()
        submitButton = driver.find_element(By.ID, 'chunkExportTrigger')
        submitButton.click()

    while any([filename.endswith(".crdownload") or filename.endswith(".tmp") for filename in os.listdir("D:\workspace\Business_Intelligence\BI_Project\dataset")]):
        time.sleep(0.5)

    print("-----> Data Scraped Successfully !")
    driver.quit()

    #Rename downloaded file
    old_name = r"D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\csv-"+searchTerm.replace(" ", "")+"-set.csv"
    new_name = r"D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv"
    os.rename(old_name, new_name)

# scrap_scopus("2017", "test")