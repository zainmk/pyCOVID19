import datetime
import mysql.connector
import selenium
from selenium import webdriver
import calendar

selenium.__file__

# Note: May have to start the MySQL service on 'Services' to access localhost
# Note: Temperatures are listed in Celsius

mydb = mysql.connector.connect(
    host="localhost",
    user="guestuser",
    passwd="guestpassword",
    database="tempdb"
)

tableName = "calgarytb"

mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
alreadyExists = False

for x in mycursor:
    for y in x:
        if tableName == y:
            alreadyExists = True

if not alreadyExists:
    mycursor.execute("CREATE TABLE " + tableName + "(id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), "
                                                   "temp VARCHAR(255))")

# ________________________________________________________________________________ #

monthDict = {"January": "01", "February": "02", "March": "03", "April": "04",
             "May": "05", "June": "06", "July": "07", "August": "08", "September": "09",
             "October": "10", "November": "11", "December": "12"}
isItToday = False
tempData = {}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2012-07-09%7C2020-05-20&dlyRange"
           "=2012-07-12%7C2020-05-20&mlyRange=%7C&StationID=50430&Prov=AB&urlExtension=_e.html&searchType=stnProv"
           "&optLimit=yearRange&StartYear=2020&EndYear=2020&selRowPerPage=100&Line=158&lstProvince=&timeframe=2"
           "&Day=1&Year=2020&Month=3") # We begin data collection with March 01, 2020

# __________________________________________________________________________________________ #
# Iterate through web pages of different months until today's date is reached.

while not isItToday:
    # Extract the web page month and year
    headerTitle = driver.find_element_by_xpath("//*[@id=\"wb-cont\"]")
    print(headerTitle.text)
    for key in monthDict:
        if key in headerTitle.text:
            currentMonth = monthDict[key]
    print(currentMonth)
    currentYear = headerTitle.text[-4:]
    print(currentYear)

    # Populate the tempData Dictionary with values obtained from HTML web page for mean temperature and date associated
    for x in range(1, calendar.monthrange(int(currentYear), int(currentMonth))[1] + 1):
        dateTimeStr = str(x) + "-" + currentMonth + "-" + currentYear
        print(dateTimeStr)
        todayDateTimeObj = datetime.datetime.now()
        todayStr = todayDateTimeObj.strftime("%d-%m-%Y")
        if dateTimeStr == todayStr:
            isItToday = True
        if isItToday:
            break

        foundElement = driver.find_element_by_xpath("//*[@id=\"dynamicDataTable\"]/table/tbody/tr["+ str(x) + "]/td[3]")
        inputTemp = foundElement.text

        try:
            inputTemp = int(inputTemp)
        except ValueError:
            inputTemp = "Missing Info"

        tempData[dateTimeStr] = str(inputTemp)

    if isItToday:
        break

    # If it still isnt today's date and the while loop hasnt been broken, click 'Next Month' for next month's data
    nextMonthButton = driver.find_element_by_xpath("//*[@id=\"nav-next2\"]/a/span[1]")
    nextMonthButton.click()

print(tempData)


# -------------------------------------------------------------------------------------------------------------- #
#            At this point we have all our temperature data in a dictionary, ready to put into a database.
#            The problem is I have to extract the most recent date and populate from that day on
# -------------------------------------------------------------------------------------------------------------- #

# Check the most recent value of the tb value for date or if there is any at all...

mycursor.execute("SELECT date FROM calgarytb")
myresult = mycursor.fetchall()

if not myresult:
    inputList = [(k, v) for k, v in tempData.items()]
    sql = "INSERT INTO calgarytb (date, temp) VALUES (%s, %s)"
    val = inputList
    mycursor.executemany(sql, val)
    mydb.commit()
else:
    mycursor.execute("SELECT date, temp FROM calgarytb")
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    lastDate = myresult[-1][0]
    print(lastDate)








