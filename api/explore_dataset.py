
from typing import Text
import pandas as pd
import numpy as np
import os.path
from functools import reduce

def prepare_dataset():

    # import datasets
    print("Importing datasets ..")
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\pubmed.csv"):
        pubmed = pd.read_csv('../dataset/pubmed.csv')
        pubmed = pubmed.rename(columns={'Title':'article_title', 'Publication Year': 'article_date', 'Journal/Book': 'journal_name'})
        pubmed["Keywords"] = np.nan
        pubmed["article_abstract"] = np.nan
        pubmed["country_name"] = np.nan
        pubmed["source"] = "pubmed"
        pubmed = pubmed[["article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name","source"]]
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv"):
        scopus = pd.read_csv('../dataset/scopus.csv')
        scopus = scopus.rename(columns={'Title':'article_title', 'Year': 'article_date', 'Source title': 'journal_name', 'Index Keywords': 'Keywords', 'Abstract': 'article_abstract', 'Correspondence Address': 'country_name'})
        scopus["source"] = "scopus"
        scopus = scopus[["article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name","source"]]
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv"):
        ieee = pd.read_csv('../dataset/ieee.csv')
        ieee = ieee.rename(columns={'Document Title':'article_title', 'Publication Year': 'article_date', 'Publication Title': 'journal_name', 'IEEE Terms': 'Keywords', 'Abstract': 'article_abstract'})
        ieee["country_name"] = np.nan
        ieee = ieee[["article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name"]]

    # springer = springer.rename(columns={'Item Title':'article_title', 'Publication Year': 'article_date', 'Publication Title': 'journal_name'})
    # Authors = springer["Authors"]
    # unified_list = []
    # for i in range(len(Authors)):
    #     unified = str(Authors[i])
    #     unified = unified.replace(" ", ";")
    #     unified_list.append(unified)
    # Authors = unified_list
    # springer["Authors"] = Authors
    # springer["Keywords"] = np.nan
    # springer["article_abstract"] = np.nan
    # springer["country_name"] = np.nan
    # springer = springer[["article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name"]]

    # Combine all datasets
    print("Combine all datasets ..")
    metadata = pd.DataFrame(columns = ["article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name","source"])
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\scopus.csv"):
        metadata = metadata.append(scopus, ignore_index=True)
    if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\pubmed.csv"):  
        metadata = metadata.append(pubmed, ignore_index=True)
    # if os.path.exists("D:\\workspace\\Business_Intelligence\\BI_Project\\dataset\\ieee.csv"):  
        # metadata = metadata.append(ieee, ignore_index=True)

    #create index column
    print("Creating global index column ..")
    metadata = metadata.reset_index()

    # Unify Delimiters 

    Authors = metadata["Authors"]
    unified_list = []
    for i in range(len(Authors)):
        unified = str(Authors[i])
        unified = unified.replace(", ", ";")
        unified = unified.replace("; ", ";")
        unified_list.append(unified)
    Authors = unified_list
    metadata["Authors"] = Authors
    
    Keywords = metadata["Keywords"]
    unified_list = []
    for i in range(len(Keywords)):
        unified = unified = str(Keywords[i])
        unified = unified.replace("; ", ";")
        unified_list.append(unified)
    Keywords = unified_list
    metadata["Keywords"] = Keywords

    # Extract Country Name :
    print("Extract countries names ..")
    Countries = metadata['country_name']
    splited_list = []
    for i in range(len(Countries)):
        string = str(Countries[i])
        if (string != 'nan'):
            x1 = string.split("; ")
            if (len(x1) > 2):
                x2 = x1[1].split(", ")
                if (len(x2) > 1):
                    x3 = x2[-1]
                    splited_list.append(x3)
                else:
                    splited_list.append('unvailable')
            else:
                splited_list.append('unvailable')
        else:
            splited_list.append('unvailable')
    Countries = splited_list
    metadata['country_name'] = Countries

    #delete end of lines' points of Authors column
    print("Cleaning authors string ..")
    Authors = metadata['Authors']
    sliced_list = []
    for i in range(len(Authors)):
        string = str(Authors[i])
        if (string != 'nan'):
            sliced = string[:-1]
            sliced_list.append(sliced)
        else :
            sliced_list.append('nan')
    Authors = sliced_list
    metadata['Authors'] = Authors

    # # split authors string:
    # # step 1 : split authors column
    # print("Spliting authors string ..")
    # temp1 = metadata['Authors'].str.split(';', expand=True)
    # metadata = metadata.join(temp1)
    # # step 2 : unpivot author's columns
    # print("Unpivoting author's columns ..")
    # metadata = pd.melt(metadata, id_vars=["index","article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name","source"], var_name=[])
    # metadata = metadata.rename(columns={'value':'author_name'})

    # # split keywords string:
    # # step 1 : split keywords column
    # print("Spliting keywords string ..")
    # temp2 = metadata['Keywords'].str.split(';', expand=True)
    # metadata = metadata.join(temp2)
    # # step 2 : unpivot keyword's columns
    # print("Unpivoting keywords's columns ..")
    # metadata = pd.melt(metadata, id_vars=["index","article_title","Authors","journal_name","article_date","Keywords","article_abstract","country_name","source","author_name"], var_name=[])
    # metadata = metadata.rename(columns={'value':'keyword'})

    #fill blank or Nan
    print("Fill blanks & NaNs ..")
    metadata = metadata.replace(np.nan, 'unvailable', regex=True)
    # metadata = metadata.replace('', np.nan, regex=True)
    # metadata = metadata.replace(r'^\s*$', np.nan, regex=True)
    # metadata = metadata.fillna("unvailable")

    # Verifying Columns DataType :
    # metadata["article_date"] = metadata["article_date"].astype('object')
    # metadata["index"] = metadata["index"].astype('object')
    # print(metadata.dtypes)

    # export to csv
    print("-----> Saving Metadata Table ...")
    metadata.to_csv( "../dataset/final_dataset/metadata.csv", index=False, encoding='utf-8-sig')

    # Articles Table =======================================================================
    print("-----> Saving Articles Table ...")
    articles = pd.DataFrame()
    articles["index"] = metadata["index"]
    articles["article_title"] = metadata["article_title"]
    articles["article_date"] = metadata["article_date"]
    articles["article_abstract"] = metadata["article_abstract"]
    articles.to_csv( "../dataset/final_dataset/articles.csv", index=False, encoding='utf-8-sig')

    # Authors Table =======================================================================
    print("-----> Saving Authors Table ...")
    authors = pd.DataFrame()
    authors["index"] = metadata["index"]
    authors["Authors"] = metadata["Authors"]
    authors.to_csv( "../dataset/final_dataset/authors.csv", index=False, encoding='utf-8-sig')

    # Journals Table =======================================================================
    print("-----> Saving Journals Table ...")
    journals = pd.DataFrame()
    journals["index"] = metadata["index"]
    journals["journal_name"] = metadata["journal_name"]
    journals.to_csv( "../dataset/final_dataset/journals.csv", index=False, encoding='utf-8-sig')

    # Keywords Table =======================================================================
    print("-----> Saving Keywords Table ...")
    keywords = pd.DataFrame()
    keywords["index"] = metadata["index"]
    keywords["Keywords"] = metadata["Keywords"]
    keywords.to_csv( "../dataset/final_dataset/keywords.csv", index=False, encoding='utf-8-sig')

    # Countries Table =======================================================================
    print("-----> Saving Countries Table ...")
    countries = pd.DataFrame()
    countries["index"] = metadata["index"]
    countries["country_name"] = metadata["country_name"]
    countries.to_csv( "../dataset/final_dataset/countries.csv", index=False, encoding='utf-8-sig')

    print("Final Dataset saved Successfully !")

# prepare_dataset()