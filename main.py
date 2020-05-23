# These may be useless imports that you can get rid of later
# from selenium.webdriver.common.action_chains import ActionChains
# from webdrivermanager import ChromeDriverManager
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as expect
import time
import re
from selenium import webdriver
import selenium
selenium.__file__

# At first, we will simply take the total cases so far for each province constantly update it these values in a SQL db.
# The initial act of running a script to obtain data from a site is Web Scraping
# To open the Selenium webdriver and go to the correct page.
# Note: You'll need chromeversion 83, otherwise another chrome webdriver or update chrome to that specific one.
# Open using incognito, to not overwrite user's default chrome settings.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ici.radio-canada.ca/info/2020/coronavirus-covid-19-pandemie-cas-carte-maladie-symptomes-propagation/index-en.html")

time.sleep(5)  # Give time for the webpage to load before the code moves forward

totalCasesDict = {}

provinceList = ["Quebec", "Ontario", "Alberta", "British Columbia", "Nova Scotia", "Saskatchewan", "Manitoba",
                "Newfoundland and Labr.", "New Brunswick", "Prince Edward Island", "Yukon", "Northwest Territories"
                ,"Nunavut"]

# Search for and collect the data for each province.
for x in range(0, len(provinceList)):
    totalCases = driver.find_element_by_name(provinceList[x]).text
    totalCases = re.sub('[^0-9]', '', totalCases)
    print(totalCases)
    totalCasesDict[provinceList[x]] = int(totalCases)

print(totalCasesDict)

driver.quit() # Quit and ends the program



# It seems the date of data origin is Feb 15, 2020 -> 02.15.2020 (The date we will start collecting data)
# Create an SQL database that holds the data for each date for different locations, city by city (So we can compare
# temperature data).













