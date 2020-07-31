# Add code to the data analysis for selecting the SQL-less code

import data_analysis

# Ask for SQL or no
SQLchoice = 0

print("Would you like to use the SQL database?")
print("1. No")
print("2. Yes")
SQLchoice = input()
SQLchoice = int(SQLchoice) - 1


# Running the different kinds of statistical analysis coded in 'data_analysis.py'
choiceDict = {"1": "calgarytb", "2": "torontotb"}

print("Choose a city to perform data analysis on...")
print("1. Calgary, AB")
print("2. Toronto, ON")
choice = input()


if SQLchoice == 1:
    print("Updating data...")
    if choice == 1:
        import calgary
    if choice == 2:
        import toronto


data_analysis.basic_stats_total_cases(choiceDict[choice], SQLchoice)

# data_analysis.regular_trend(choiceDict[choice])

"""
data_analysis.data_collect(choiceDict[choice])
data_analysis.basic_stats_total_cases(choiceDict[choice])
data_analysis.linear_analysis_days_vs_total_cases(choiceDict[choice])
data_analysis.polynomial_analysis_days_vs_total_cases(choiceDict[choice])
data_analysis.linear_analysis_days_vs_new_cases(choiceDict[choice])
data_analysis.polynomial_analysis_days_vs_new_cases(choiceDict[choice])
data_analysis.linear_analysis_temp_vs_total_cases(choiceDict[choice])
data_analysis.linear_analysis_temp_vs_new_cases(choiceDict[choice])
data_analysis.multiple_regression_days_and_temp_vs_total_cases(choiceDict[choice])
data_analysis.multiple_regression_days_and_temp_vs_new_cases(choiceDict[choice])
"""














