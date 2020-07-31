import datetime
import json
import mysql.connector
import selenium
from selenium import webdriver
import calendar
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


selenium.__file__

# ---------------------------------------------------------------------------------------------------------------------#
#                          Initializing variables for global scope and checking for table existence
# ---------------------------------------------------------------------------------------------------------------------#



def collect_data():
    updateDate = "01-03-2020"
    isItToday = False
    alreadyExists = False
    todayStr = datetime.datetime.now().strftime("%d-%m-%Y")
    monthDict = {"January": "01", "February": "02", "March": "03", "April": "04",
                 "May": "05", "June": "06", "July": "07", "August": "08", "September": "09",
                 "October": "10", "November": "11", "December": "12"}
    shortMonthDict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                      "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    tempData = {}
    casesData = {}
    totalCasesByDate = {}
    datesForCOVID = []

    updateDateDay = str(int(updateDate[:2]))
    updateDateMonth = str(int(updateDate[3:5]))  # This will eliminate leading 0's but return a string
    updateDateYear = updateDate[6:]

    # ---------------------------------------------------------------------------------------------------------------------#
    #                      Begin by acquiring data for the total number of COVID cases by day from the update
    #                                  date and fill in the database with the required values.
    # ---------------------------------------------------------------------------------------------------------------------#
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(
        "https://www.publichealthontario.ca/en/data-and-analysis/infectious-disease/covid-19-data-surveillance/covid-19-data-tool")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Trends"]'))).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id=\"trendsField\"]/div[2]/div/div'))).click()

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id=\"trendsField\"]/div[2]/div/div/div[2]/div[32]'))).click()
            break
        except:
            pass

    divElementOverSVG = driver.find_element_by_xpath("//*[@id=\"covidChart1\"]/div/div[1]")
    innerHTML = divElementOverSVG.get_attribute("innerHTML")

    counter = 0
    stringList = []

    # Find number of days between March 01, 2020 and Today
    numberOfElapsedDays = (datetime.datetime.now() - datetime.datetime.strptime("15-01-2020", "%d-%m-%Y")).days

    for x in range(0, numberOfElapsedDays):
        counter = innerHTML.find("aria-label", counter)
        startingIndex = counter + 12
        endCounter = innerHTML.find("\"", startingIndex)
        subString = innerHTML[startingIndex: endCounter]
        stringList.append(subString)
        counter = counter + 12

    check = False
    newCasesByDate = {}
    for x in stringList:
        for y in shortMonthDict:
            if y in x:
                monthIndex = x.find(y)
                dayIndex = monthIndex + 4
                dayStr = x[dayIndex: dayIndex + 2]
                monthStr = shortMonthDict[y]
                yearIndex = dayIndex + 4
                yearStr = x[yearIndex: yearIndex + 4]
                currentDateStr = dayStr + "-" + monthStr + "-" + yearStr
                casesStr = x[x.find(" ", yearIndex) + 1:]
                newCasesByDate[currentDateStr] = casesStr

    totalCasesByDate = {}
    runningTotal = 0
    for x in newCasesByDate:
        runningTotal = runningTotal + int(newCasesByDate[x])
        totalCasesByDate[x] = str(runningTotal)

    keyList = list(totalCasesByDate.keys())

    for k in keyList:
        if k == updateDate:
            break
        del totalCasesByDate[k]

    # ---------------------------------------------------------------------------------------------------------------------#
    #                               Acquire data for temperature readings and update accordingly.
    # ---------------------------------------------------------------------------------------------------------------------#
    # Adjust for these with data collection with cases
    currentDay = int(updateDateDay)
    currentMonth = updateDateMonth
    currentYear = updateDateYear
    isItToday = False

    while not isItToday:
        driver.get(
            "https://www.wunderground.com/history/monthly/ca/toronto/CYTZ/date/" + currentYear + "-" + currentMonth)
        time.sleep(5)

        for currentDay in range(currentDay, calendar.monthrange(int(currentYear), int(currentMonth))[1] + 1):
            dateTimeStr = str(currentDay).zfill(2) + "-" + currentMonth.zfill(2) + "-" + currentYear

            if dateTimeStr == todayStr:
                isItToday = True
                break
            else:
                fTemp = driver.find_element_by_xpath(
                    "//*[@id=\"inner-content\"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div["
                    "2]/table/tbody/tr/td[2]/table/tr[" + str(currentDay + 1) + "]/td[2]").text
                cTemp = round((float(fTemp) - 32) * (5 / 9), 1)
                tempData[dateTimeStr] = cTemp
        if not isItToday:
            currentDay = 1
            currentMonth = str(int(currentMonth) + 1)
            if currentMonth == 13:
                currentMonth = str(1)
                currentYear = str(int(currentYear) + 1)

    driver.close()

    return totalCasesByDate, tempData























