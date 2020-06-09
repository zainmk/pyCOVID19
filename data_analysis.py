import datetime
import json
import mysql.connector
import calendar

import numpy
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

mydb = mysql.connector.connect(
    host="localhost",
    user="guestuser",
    passwd="guestpassword",
    database="tempdb"
)
mycursor = mydb.cursor()

"""
choiceDict = {"1": "calgary"}
print("Choose one of the following cities to analyze COVID data:")
print("1. Calgary, AB")
choice = input()
print(choiceDict[choice])
"""
choice = "calgarytb"

mycursor.execute("SELECT `Total Cases` FROM " + choice)
myResult = mycursor.fetchall()
totalCasesDataList = []

for x in myResult:
    totalCasesDataList.append(int(x[0]))

mycursor.execute("SELECT `Date(d-m-y)` FROM " + choice)
myResult = mycursor.fetchall()
numberOfDaysList = []
for x in range(1, (len(myResult) + 1)):
    numberOfDaysList.append(x)

print("Mean Value:", numpy.mean(totalCasesDataList))
print("Median Value:", numpy.median(totalCasesDataList))
print("Standard Deviation:", numpy.std(totalCasesDataList))
print("The 90th percentile is: ", numpy.percentile(totalCasesDataList, 90))
print()


# Linear Regression between Total Cases and Days after March 01, 2020
slope, intercept, r, p, std_err = stats.linregress(numberOfDaysList, totalCasesDataList)


def yValue(x):
    return slope * x + intercept


predictionForNextDay = yValue(len(numberOfDaysList))
print("Linear Regression Analysis has a r value of " + str(r) + " and a next day prediction of ", predictionForNextDay)
myModel = list(map(yValue, numberOfDaysList))
plt.scatter(numberOfDaysList, totalCasesDataList)
plt.plot(numberOfDaysList, myModel)
plt.xlabel("Days Post March 01, 2020")
plt.ylabel("Total Number of COVID Cases")
plt.show(block=True)

# Polynomial Regression between Total Cases and Days after March 01, 2020
myModel = numpy.poly1d(numpy.polyfit(numberOfDaysList, totalCasesDataList, 10))
myLine = numpy.linspace(1, len(totalCasesDataList), 100)
predictionForNextDay = myModel(len(numberOfDaysList))
polynomialR = r2_score(totalCasesDataList, myModel(numberOfDaysList))
print("The R value for Polynomial Regression is: ", polynomialR, " and a prediction of: ", predictionForNextDay)

plt.scatter(numberOfDaysList, totalCasesDataList)
plt.plot(myLine, myModel(myLine))
plt.xlabel("Days Post March 01, 2020")
plt.ylabel("Total Number of COVID Cases")
plt.show()






















