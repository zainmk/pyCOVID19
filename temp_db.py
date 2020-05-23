# This file is for opening a SQL db and then webscraping using Selenium to load temperature data per city into the db.

import datetime


# _______________________________________________________________
# All the load-ins required for Selenium Webdriver

from selenium.webdriver.common.action_chains import ActionChains
from webdrivermanager import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
import time
import re
from selenium import webdriver
import selenium
selenium.__file__
# ________________________________________________________________

# All the load-ins required for mySQL
import mysql.connector
# _______________________________________________________________

# We start by loading up our db and creating it if it doesnt already exist. We will start with just a temp db for
# Calgary, AB.

mydb = mysql.connector.connect(
  host="localhost",
  user="guestuser",
  passwd="guestpassword",
  database="tempdb"
)

mycursor = mydb.cursor()

x = datetime.datetime.now()
x = x.strftime("%X")
print(x)




# Use Selenium to webscrape the temperature data.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2012-07-09%7C2020-05-20&dlyRange="
           "2012-07-12%7C2020-05-20&mlyRange=%7C&StationID=50430&Prov=AB&urlExtension=_e.html&searchType=stnProv&opt"
           "Limit=yearRange&StartYear=2020&EndYear=2020&selRowPerPage=100&Line=158&lstProvince=&timeframe=2&Day=1&Year="
           "2020&Month=2")


foundElement = driver.find_element_by_xpath("//*[@id='dynamicDataTable']/table/tbody/tr[15]/td[3]")
print(foundElement.text)

tempPerDay = {}





