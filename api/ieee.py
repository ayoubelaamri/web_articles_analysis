import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def scrap_ieee(date,searchTerm):

    ids=[]
    titles=[]
    authors=[]
    abstracts=[]

    driver = webdriver.Chrome("./chromedriver.exe")

    print("-----> Fetching: https://www.ieee.org/")
    driver.get('https://www.ieee.org/')

    print("-----> Looking for search Input...")
    searchInput = driver.find_element_by_name('q') #ieee
        
    print("-----> Typing search keyword ...")
    searchInput.clear()
    searchInput.send_keys(searchTerm)
    searchInput.send_keys(Keys.RETURN)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'gs-title')) # ieee
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("-----> Timed out waiting for page to load !")
    finally:
        print("-----> Page loaded !")
        print("-----> Scraping data ...")

        title = driver.find_elements_by_xpath('//div[@class="gs-title"]/a[@class="gs-title"]') #ieee
        author = driver.find_elements_by_xpath('//div[@class="gsc-url-top"]/div[@class="gs-bidi-start-align gs-visibleUrl gs-visibleUrl-short"]') #ieee
        abstract = driver.find_elements_by_xpath('//div[@class="gsc-table-cell-snippet-close"]/div[@class="gs-bidi-start-align gs-snippet"]') #ieee
            
        print("-----> Data Scraped Successfully !")
        
        for i in range(len(title)):
            titles.append(title[i].text)
            authors.append(author[i].text)
            abstracts.append(abstract[i].text)
    
    for i in range(len(titles)):
        ids.append(i+1)

    print("-----> Saving the csv file ...")
    df = pd.DataFrame({'ID':ids, 'TITLE':titles, 'AUTHOR':authors, 'ABSTRACT':abstracts}) 
    df.to_csv('../../dataset/ieee.csv', index=False, encoding='utf-8')
    print("-----> CSV saved Successfully !")

    driver.quit()