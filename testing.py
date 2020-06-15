import datetime
import mysql.connector
import selenium
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import datetime
import data_analysis

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in"
           "-toronto/")

element = driver.find_element_by_xpath("")


