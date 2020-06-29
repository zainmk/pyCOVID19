import datetime
import json
import mysql.connector
import selenium
from selenium import webdriver
import calendar

selenium.__file__

mydb = mysql.connector.connect(
    host="localhost",
    user="guestuser",
    passwd="guestpassword",
    database="tempdb"
)
mycursor = mydb.cursor()

# ---------------------------------------------------------------------------------------------------------------------#
#                          Initializing variables for global scope and checking for table existence
# ---------------------------------------------------------------------------------------------------------------------#
tableName = "calgarytb"
updateDate = "01-03-2020"
isItToday = False
alreadyExists = False
todayStr = datetime.datetime.now().strftime("%d-%m-%Y")
monthDict = {"January": "01", "February": "02", "March": "03", "April": "04",
             "May": "05", "June": "06", "July": "07", "August": "08", "September": "09",
             "October": "10", "November": "11", "December": "12"}
tempData = {}
casesData = {}
totalCasesByDate = {}
datesForCOVID = []


# Creating table if it doesnt exist and updating the 'updateDate' if it already does
mycursor.execute("SHOW TABLES")
for x in mycursor:
    for y in x:
        if tableName == y:
            alreadyExists = True

if alreadyExists:
    mycursor.execute("SELECT `Date(d-m-y)` FROM calgarytb")
    myresult = mycursor.fetchall()
    if myresult:
        lastDate = myresult[-1][0]
        updateDate_datetime_obj = datetime.datetime.strptime(lastDate, '%d-%m-%Y')
        updateDate_datetime_obj += datetime.timedelta(days=1)
        updateDate = updateDate_datetime_obj.strftime("%d-%m-%Y")
        if updateDate == todayStr:
            isItToday = True
else:
    mycursor.execute("CREATE TABLE " + tableName + "(id INT AUTO_INCREMENT PRIMARY KEY, `Date(d-m-y)` VARCHAR(255), "
                                                   "`Total # Of Cases` VARCHAR(255),`temp(C)` VARCHAR(255))")

updateDateMonth = str(int(updateDate[3:5]))  # This will eliminate leading 0's but return a string
updaetDateYear = str(int(updateDate[6:]))

# ---------------------------------------------------------------------------------------------------------------------#
#                      Begin by acquiring data for the total number of COVID cases by day from the update
#                                  date and fill in the database with the required values.
# ---------------------------------------------------------------------------------------------------------------------#
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.alberta.ca/stats/covid-19-alberta-statistics.htm")
geospatialButton = driver.find_element_by_xpath("//*[@id=\"covid-19-in-alberta\"]/ul/li[5]/a")
geospatialButton.click()
test = driver.find_element_by_xpath("//*[@id=\"geospatial\"]/div[1]/script")
innerHTML = test.get_attribute('innerHTML')
innerHTMLjson = json.loads(innerHTML)

datesExtracted = innerHTMLjson["x"]["data"][0]["x"]
totalCases = innerHTMLjson["x"]["data"][0]["y"]

for x in range(0, len(datesExtracted)):  # Rearranges the dates so they are in d-m-y format
    datesForCOVID.append(datesExtracted[x][8:] + "-" + datesExtracted[x][5:7] + "-" + datesExtracted[x][0:4])

for x in range(0, len(datesForCOVID)): # Properly Total Cases per date dictionary
    totalCasesByDate[datesForCOVID[x]] = totalCases[x]

tempTotalCasesByDate = {}
startNumberOfCases = 0
tempCurrentDate = updateDate
while tempCurrentDate != todayStr:
    tempTotalCasesByDate[tempCurrentDate] = startNumberOfCases
    if tempCurrentDate in totalCasesByDate:
        startNumberOfCases = totalCasesByDate[tempCurrentDate]
        tempTotalCasesByDate[tempCurrentDate] = startNumberOfCases
    tempCurrentDateObj = datetime.datetime.strptime(tempCurrentDate, '%d-%m-%Y')
    tempCurrentDateObj += datetime.timedelta(days=1)
    tempCurrentDate = tempCurrentDateObj.strftime("%d-%m-%Y")
    if tempCurrentDate in totalCasesByDate:
        startNumberOfCases = totalCasesByDate[tempCurrentDate]
totalCasesByDate = tempTotalCasesByDate

# Fill in the db 'calgarytb' with the values acquired, if any.
mycursor.execute("SELECT `Date(d-m-y)` FROM calgarytb")
myresult = mycursor.fetchall()
if totalCasesByDate:
    inputList = [(k, v) for k, v in totalCasesByDate.items()]
    sql = "INSERT INTO calgarytb (`date(d-m-y)`, `Total # Of Cases`) VALUES (%s, %s)"
    val = inputList
    mycursor.executemany(sql, val)
    mydb.commit()

# ---------------------------------------------------------------------------------------------------------------------#
#                               Acquire data for temperature readings and update accordingly.
# ---------------------------------------------------------------------------------------------------------------------#

driver.get("https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2012-07-09%7C2020-05-20&dlyRange"
           "=2012-07-12%7C2020-05-20&mlyRange=%7C&StationID=50430&Prov=AB&urlExtension=_e.html&searchType=stnProv"
           "&optLimit=yearRange&StartYear=2020&EndYear=2020&selRowPerPage=100&Line=158&lstProvince=&timeframe=2"
           "&Day=1&Year=2020&Month=" + updateDateMonth)  # We begin data collection with whatever month is in updateDate

while not isItToday:
    # Extract the web page month and year
    headerTitle = driver.find_element_by_xpath("//*[@id=\"wb-cont\"]")
    for key in monthDict:
        if key in headerTitle.text:
            currentMonth = monthDict[key]
    currentYear = headerTitle.text[-4:]

    updateDateDayInt = int(updateDate[:2])

    if int(currentMonth) != int(updateDateMonth):
        updateDateDayInt = 1

    # Populate the tempData Dictionary with values obtained from HTML web page for mean temperature and date associated
    for updateDateDayInt in range(updateDateDayInt, calendar.monthrange(int(currentYear), int(currentMonth))[1] + 1):
        dateTimeStr = str(updateDateDayInt).zfill(2) + "-" + currentMonth + "-" + currentYear

        if dateTimeStr == todayStr:
            isItToday = True
            break
        else:
            foundElement = driver.find_element_by_xpath(
                "//*[@id=\"dynamicDataTable\"]/table/tbody/tr[" + str(updateDateDayInt) + "]/td[3]")
            inputTemp = foundElement.text
            try:
                float(inputTemp)
            except ValueError:
                prevDateObj = datetime.datetime.strptime(dateTimeStr, "%d-%m-%Y")
                prevDay = prevDateObj - datetime.timedelta(days=1)
                prevDateStr = prevDay.strftime("%d-%m-%Y")
                inputTemp = tempData[prevDateStr]
            tempData[dateTimeStr] = inputTemp

    # If it still isn't today's date and the while loop hasn't been broken, click 'Next Month' for next month's data
    if not isItToday:
        nextMonthButton = driver.find_element_by_xpath("//*[@id=\"nav-next2\"]/a/span[1]")
        nextMonthButton.click()

for key, value in tempData.items():
    sql = "UPDATE calgarytb SET `temp(C)` ='" + value + "' WHERE `Date(d-m-y)` ='" + key + "'"
    mycursor.execute(sql)
    mydb.commit()

driver.close()


























