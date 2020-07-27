import data_analysis


print("Updating data...")
import calgary
import toronto


# Running the different kinds of statistical analysis coded in 'data_analysis.py'
choiceDict = {"1": "calgarytb", "2": "torontotb"}

print("Choose a city to perform data analysis on...")
print("1. Calgary, AB")
print("2. Toronto, ON")

choice = input()

data_analysis.regular_trend(choiceDict[choice])

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














