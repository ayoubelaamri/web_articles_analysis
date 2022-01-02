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

def scrap_pubmed(date,searchTerm):

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "D:\workspace\Business_Intelligence\BI_Project\dataset"}
    options.add_experimental_option("prefs",prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("start-maximized")

    # driver = webdriver.Chrome("./chromedriver.exe", chrome_options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print("-----> Fetching: https://pubmed.ncbi.nlm.nih.gov/")
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')

    print("-----> Looking for search Input...")
    searchInput = driver.find_element(By.NAME, 'term') #pubmed
        
    print("-----> Typing search keyword ...")
    searchInput.clear()
    searchInput.send_keys(searchTerm)
    searchInput.send_keys(Keys.RETURN)

    print("-----> Looking for filter ...")
    try:
        filter_present = EC.presence_of_element_located((By.CLASS_NAME, 'datepicker-dropdown dropdown dropdown-container')) # pubmed
        # filter_present = EC.presence_of_element_located((By.XPATH, '//*[@id="datepicker-trigger"]/parent::li')) # pubmed
        WebDriverWait(driver, 10).until(filter_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        print("-----> Typing Year filter ..")
        filter = driver.find_element(By.XPATH, '//*[@id="datepicker-trigger"]/parent::li')
        filter.click()
        yearInput = driver.find_element(By.CLASS_NAME, 'start-year')
        yearInput.send_keys(date)
        yearInput.send_keys(Keys.RETURN)

    print("-----> Looking for Save Button ...")
    try:
        saveButton_present = EC.presence_of_element_located((By.CLASS_NAME, 'save-results save-results-panel-trigger')) # pubmed
        # saveButton_present = EC.presence_of_element_located((By.ID, 'save-results-panel-trigger')) # pubmed
        WebDriverWait(driver, 10).until(saveButton_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        print("-----> Page loaded !")
        print("-----> Scraping data ...")

        saveButton = driver.find_element(By.ID,'save-results-panel-trigger')
        saveButton.click()

        select_input1 = driver.find_element(By.ID, "save-action-selection")
        select_object1 = Select(select_input1)
        select_object1.select_by_visible_text('All results')

        select_input2 = driver.find_element(By.ID,"save-action-format")
        select_object2 = Select(select_input2)
        select_object2.select_by_visible_text('CSV')

        # submitButton = driver.find_elements_by_xpath('//button[@class="gs-title"]/a[@class="gs-title"]')
        submitButton = driver.find_element(By.CLASS_NAME,'action-panel-submit')
        submitButton.click()

    time.sleep(2)

    while any([filename.endswith(".crdownload") or filename.endswith(".tmp") for filename in os.listdir("D:\workspace\Business_Intelligence\BI_Project\dataset")]):
        time.sleep(0.5)

    print("-----> Data Scraped Successfully !")
    driver.quit()

    #Rename downloaded file
    old_name = r"D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\csv-"+searchTerm.replace(" ", "")+"-set.csv"
    new_name = r"D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\pubmed.csv"
    os.rename(old_name, new_name)

# scrap_pubmed("2017", "test")