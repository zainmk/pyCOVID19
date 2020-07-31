import datetime
import json
import mysql.connector
import calendar

import calgary_SQL_less
import toronto_SQL_less

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn import linear_model
import pandas as pd
import statsmodels.api as sm


mydb = mysql.connector.connect(
    host="localhost",
    user="guestuser",
    passwd="guestpassword",
    database="tempdb"
)
mycursor = mydb.cursor()

cityDict = {"calgarytb": "Calgary, AB", "torontotb": "Toronto, ON"}
totalCasesDataList = []
newCasesDataList = []
numberOfDaysList = []
tempList = []


def data_collect(cityName):
    if not (totalCasesDataList or newCasesDataList or numberOfDaysList or tempList):
        mycursor.execute("SELECT `Total # Of Cases` FROM " + cityName)
        myResult = mycursor.fetchall()
        counter = 0
        for item in myResult:
            counter = counter + 1
            numberOfDaysList.append(counter)
            totalCasesDataList.append(int(item[0]))
        newCasesDataList.append(totalCasesDataList[0])
        print(newCasesDataList)
        for x in range(1, len(totalCasesDataList)):
            newCasesDataList.append(totalCasesDataList[x] - totalCasesDataList[x - 1])
        mycursor.execute("SELECT `temp(C)` FROM " + cityName)
        myResult = mycursor.fetchall()
        for x in myResult:
            tempList.append(float(x[0]))


def data_collect_SQL_less(cityName):
    if not (totalCasesDataList or newCasesDataList or numberOfDaysList or tempList):
        totalCOVIDCases = []
        TemperatureData = []

        if cityName == 'calgarytb':
            totalCOVIDCases, TemperatureData = calgary_SQL_less.collect_data()
        if cityName == 'torontotb':
            totalCOVIDCases, TemperatureData = toronto_SQL_less.collect_data()

        # Format data for analysis
        counter = 0
        for item in totalCOVIDCases:
            counter = counter + 1
            numberOfDaysList.append(counter)
            totalCasesDataList.append(int(totalCOVIDCases[item]))
        newCasesDataList.append(totalCasesDataList[0])
        for x in range(1, len(totalCasesDataList)):
            newCasesDataList.append(totalCasesDataList[x] - totalCasesDataList[x-1])
        for item in TemperatureData:
            tempList.append(float(TemperatureData[item]))

        print(numberOfDaysList)
        print(totalCasesDataList)
        print(newCasesDataList)
        print(tempList)


def basic_stats_total_cases(cityName, sql):
    if sql:
        data_collect(cityName)
    else:
        data_collect_SQL_less(cityName)

    print("Mean Value:", np.mean(totalCasesDataList))
    print("Median Value:", np.median(totalCasesDataList))
    print("Standard Deviation:", np.std(totalCasesDataList))
    print("The 90th percentile is: ", np.percentile(totalCasesDataList, 90))
    print()

# Function that compares the trends for all cities
def city_comparison():
    data_collect("calgarytb")
    calgary_total_cases = totalCasesDataList
    data_collect("torontotb")
    toronto_total_cases = totalCasesDataList



def regular_trend(cityName):
    data_collect(cityName)
    plt.plot(numberOfDaysList, totalCasesDataList)
    plt.title("Total Number of Cases for " + cityDict[cityName] + " , Days Post March 01, 2020")
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of Cases")
    plt.xticks(np.arange(0, 180, step=30), )
    plt.show()





def linear_analysis_days_vs_total_cases(cityName):
    data_collect(cityName)
    slope, intercept, r, p, std_err = stats.linregress(numberOfDaysList, totalCasesDataList)
    yValue = lambda x: slope*x + intercept
    nextDayPred = yValue(len(numberOfDaysList))
    r = round(r, 5)
    nextDayPred = int(nextDayPred)

    myModel = list(map(yValue, numberOfDaysList))
    plt.scatter(numberOfDaysList, totalCasesDataList)
    plt.plot(numberOfDaysList, myModel)
    plt.title("Linear Regression Analysis Results of " + cityDict[cityName] + " \n R-Value: " + str(r) + "  Next Day Pred:" + str(nextDayPred))
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of COVID Cases")
    plt.show()


def polynomial_analysis_days_vs_total_cases(cityName, degree=15):
    data_collect(cityName)
    myModel = np.poly1d(np.polyfit(numberOfDaysList, totalCasesDataList, degree))
    myLine = np.linspace(1, len(totalCasesDataList), 100)
    nextDayPred = myModel(len(numberOfDaysList))
    R = r2_score(totalCasesDataList, myModel(numberOfDaysList))
    R = round(R, 4)
    nextDayPred = int(nextDayPred)

    plt.scatter(numberOfDaysList, totalCasesDataList)
    plt.plot(myLine, myModel(myLine))
    plt.title("Polynomial Regression Analysis Results of " + cityDict[cityName] + " \n Degree:" + str(degree) + "   R-Value:" + str(R) + "  Next Day Pred:" + str(nextDayPred))
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of COVID Cases")
    plt.show()


def linear_analysis_days_vs_new_cases(cityName):
    data_collect(cityName)
    slope, intercept, r, p, std_err = stats.linregress(numberOfDaysList, newCasesDataList)
    yValue = lambda x: slope*x + intercept
    nextDayPred = yValue(len(numberOfDaysList))
    r = round(r, 4)
    nextDayPred = int(nextDayPred)
    myModel = list(map(yValue, numberOfDaysList))
    plt.scatter(numberOfDaysList, newCasesDataList)
    plt.plot(numberOfDaysList, myModel)
    plt.title("Linear Regression Analysis Results of " + cityDict[cityName] + "\n R-Value:" + str(r) + "   Next Day Pred:" + str(nextDayPred))
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Number of New COVID Cases")
    plt.show()


def polynomial_analysis_days_vs_new_cases(cityName, degree=15):
    data_collect(cityName)
    myModel = np.poly1d(np.polyfit(numberOfDaysList, newCasesDataList, degree))
    myLine = np.linspace(1, len(newCasesDataList), 100)
    nextDayPred = myModel(len(numberOfDaysList))
    R = r2_score(newCasesDataList, myModel(numberOfDaysList))
    R = round(R, 4)
    nextDayPred = int(nextDayPred)

    plt.scatter(numberOfDaysList, newCasesDataList)
    plt.plot(myLine, myModel(myLine))
    plt.title("Polynomial Regression Analysis Results of " + cityDict[cityName] + "\n Degree:" + str(degree) + "   R-Value: " + str(R) + "   Next Day Pred: " + str(nextDayPred))
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("New Number of COVID Cases")
    plt.show()


def linear_analysis_temp_vs_total_cases(cityName):
    data_collect(cityName)
    slope, intercept, r, p, std_err = stats.linregress(tempList, totalCasesDataList)
    yValue = lambda x: slope * x + intercept
    nextDayPred = yValue(tempList[-1])
    r = str(round(r, 4))
    nextDayPred = str(int(nextDayPred))

    myModel = list(map(yValue, tempList))
    plt.scatter(tempList, totalCasesDataList)
    plt.plot(tempList, myModel)
    plt.title("Linear Regression Analysis Results of " + cityDict[cityName] + "\n R-Value:" + r + "   Next Day Pred:" + nextDayPred)
    plt.xlabel("Temperature (C)")
    plt.ylabel("Total Number of COVID Cases")
    plt.show()


def linear_analysis_temp_vs_new_cases(cityName):
    data_collect(cityName)
    slope, intercept, r, p, std_err = stats.linregress(tempList, newCasesDataList)
    yValue = lambda x: slope * x + intercept
    nextDayPred = yValue(len(tempList))
    r = str(round(r, 4))
    nextDayPred = str(int(nextDayPred))

    myModel = list(map(yValue, tempList))
    plt.scatter(tempList, newCasesDataList)
    plt.plot(tempList, myModel)
    plt.title("Linear Regression Analysis Results of " + cityDict[cityName] + "\n R-Value:" + r + "   Next Day Pred:" + nextDayPred)
    plt.xlabel("Temperature (C)")
    plt.ylabel("Number of New COVID Cases")
    plt.show()


def multiple_regression_days_and_temp_vs_total_cases(cityName):
    data_collect(cityName)
    Data_Input = {'Days': numberOfDaysList, 'Temp': tempList, 'Cases': totalCasesDataList}
    df = pd.DataFrame(Data_Input, columns=['Days', 'Temp', 'Cases'])
    X = df[['Days', 'Temp']]
    Y = df['Cases']

    # With Statsmodel
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()

    print_model = model.summary()
    print()
    print("Multiple Regression Analysis for " + cityDict[cityName] + " with Temperature and Days vs. Total Cases")
    print(print_model)
    print()
    print()


def multiple_regression_days_and_temp_vs_new_cases(cityName):
    data_collect(cityName)
    Data_Input = {'Days': numberOfDaysList, 'Temp': tempList, 'Cases': newCasesDataList}
    df = pd.DataFrame(Data_Input, columns=['Days', 'Temp', 'Cases'])
    X = df[['Days', 'Temp']]
    Y = df['Cases']

    # With Statsmodel
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()

    print_model = model.summary()
    print()
    print("Multiple Regression Analysis for " + cityDict[cityName] + " with Temperature and Days vs. New COVID Cases")
    print(print_model)
    print()
    print()


def basic_plot(cityName):
    data_collect(cityName)

    plt.scatter(numberOfDaysList, totalCasesDataList)
    plt.title("Basic Plot")
    plt.axvline(x=30)
    plt.xlabel("Days Post March 01, 2020")
    plt.ylabel("Total Number of COVID Cases")
    plt.show()





















