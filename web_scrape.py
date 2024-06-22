from unittest import skip
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import numpy as np
from urllib.error import HTTPError

blank_df=pd.DataFrame()
df=pd.read_csv("book_sum.csv")
df=df.iloc[:,1:]

url="https://angryloki.github.io/mreid-resolver/#"

options = Options()
options.add_argument("--headless")

blank_u=[]
blank_code=[]

def getImage(url):    
    try:
        html = BeautifulSoup(url,"html.parser")
        img = html.find('img')
        ur=img.get('src')
    except AttributeError as e:
        return None
    return ur

try:    
    for base_id in df['freebase_id'].iloc[8500:9000]:
        driver = webdriver.Firefox(options=options)
        # driver = webdriver.Firefox()      
        driver.get(url+base_id) 
        time.sleep(1.5)             
        checkurl = getImage(driver.page_source)            
        if checkurl ==None:
            blank_u.append(np.nan)
            blank_code.append(base_id)
            print(len(blank_u))
            driver.close()
            driver.quit()
            print("Image URL not found")             
        else:                      
            blank_u.append(checkurl)
            blank_code.append(base_id)    
            print(len(blank_u))     
            driver.close()
            driver.quit()
            print("Image URL found")                                
    blank_df['base_id']=blank_code
    blank_df['url']=blank_u    
    blank_df.to_csv("data/base_url_20.csv",index=False)
except(ElementNotVisibleException, WebDriverException, NoSuchElementException):
    print("Fail")
    


