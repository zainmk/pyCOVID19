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
totalCasesDataList = []
numberOfDaysList = []


def data_collect(cityName):
    mycursor.execute("SELECT `Total Cases` FROM " + cityName)
    myResult = mycursor.fetchall()
    counter = 0
    for item in myResult:
        counter = counter + 1
        numberOfDaysList.append(counter)
        totalCasesDataList.append(int(item[0]))



def basic_stats(cityName):
    data_collect(cityName)
    print("Mean Value:", numpy.mean(totalCasesDataList))
    print("Median Value:", numpy.median(totalCasesDataList))
    print("Standard Deviation:", numpy.std(totalCasesDataList))
    print("The 90th percentile is: ", numpy.percentile(totalCasesDataList, 90))
    print()


def linear_analysis(cityName):
    data_collect(cityName)
    slope, intercept, r, p, std_err = stats.linregress(numberOfDaysList, totalCasesDataList)
    yValue = lambda x: slope*x + intercept
    nextDayPred = yValue(len(numberOfDaysList))
    print("Linear Reg. Analysis Results: R Value = ", str(r), "Next Day Prediction of Total Cases: ", nextDayPred)
    myModel = list(map(yValue, numberOfDaysList))
    plt.scatter(numberOfDaysList, totalCasesDataList)
    plt.plot(numberOfDaysList, myModel)
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of COVID Cases")


def polynomial_analysis(cityName, degree):
    data_collect(cityName)
    myModel = numpy.poly1d(numpy.polyfit(numberOfDaysList, totalCasesDataList, degree))
    myLine = numpy.linspace(1, len(totalCasesDataList), 100)
    nextDayPred = myModel(len(numberOfDaysList))
    R = r2_score(totalCasesDataList, myModel(numberOfDaysList))
    print("Polynomial Reg. Analysis with Degree ", degree, ": R Value = ", str(R), "Next Day Predic. = ", nextDayPred)
    plt.scatter(numberOfDaysList, totalCasesDataList)
    plt.plot(myLine, myModel(myLine))
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of COVID Cases")
    plt.show()




























