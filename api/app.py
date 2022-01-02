from flask import Flask, redirect
import pandas as pd
import os.path
 
# import scrapping functions
from scopus import scrap_scopus
from pubmed import scrap_pubmed
from ieee import scrap_ieee
from explore_dataset import prepare_dataset
from mongoImport import mongoimport

app = Flask(__name__)

@app.route('/run/<site>/<date>/<searchTerm>')
def run_scraping(site,date,searchTerm):

    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\pubmed.csv"):
        os.remove("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\pubmed.csv")
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv"):
        os.remove("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv")
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\ieee.csv"):
        os.remove("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\ieee.csv")

    if(site == "all"):
        urls = ['https://pubmed.ncbi.nlm.nih.gov/', 'https://www.ieee.org/', 'https://www.scopus.com']
        print("-----> Selection : ALL WEBSITES")
    else:
        if(site == "pubmed"):
            urls = ['https://pubmed.ncbi.nlm.nih.gov/']
            print("-----> Selection : PUBMED")
        if(site == "ieee"):
            urls = ['https://www.ieee.org/']
            print("-----> Selection : IEEE")
        if(site == "scopus"):
            urls = ['https://www.scopus.com']
            print("-----> Selection : SCOPUS")

    try:

        for url in urls:
            if(url == "https://pubmed.ncbi.nlm.nih.gov/"):
                scrap_pubmed(date,searchTerm)
            if(url == "https://www.ieee.org/"):
                scrap_ieee(date,searchTerm)
            if(url == "https://www.scopus.com"):
                scrap_scopus(date,searchTerm)

        prepare_dataset()

        mongoimport("../dataset/final_dataset/metadata.csv", "bi_project_db", "metadata", 'localhost', 27017)
        mongoimport("../dataset/final_dataset/articles.csv", "bi_project_db", "articles", 'localhost', 27017)
        mongoimport("../dataset/final_dataset/authors.csv", "bi_project_db", "authors", 'localhost', 27017)
        mongoimport("../dataset/final_dataset/journals.csv", "bi_project_db", "journals", 'localhost', 27017)
        mongoimport("../dataset/final_dataset/keywords.csv", "bi_project_db", "keywords", 'localhost', 27017)
        mongoimport("../dataset/final_dataset/countries.csv", "bi_project_db", "countries", 'localhost', 27017)
    
    except Exception:
        return {"redirect": False}

    return {"redirect": True}
