# At first, we will simply take the total cases so far for each province constantly update it these values in a SQL db.
# The initial act of running a script to obtain data from a site is Web Scraping
# To open the Selenium webdriver and go to the correct page.
# Note: You'll need chromeversion 83, otherwise another chrome webdriver or update chrome to that specific one.
# Open using incognito, to not overwrite user's default chrome settings.
# It seems the date of data origin is March 01, 2020 -> 01.03.2020 (The date we will start collecting data)
# Create an SQL database that holds the data for each date for different locations, city by city (So we can compare
# temperature data).

import calgary
import data_analysis

# Running the different kinds of statistical analysis coded in 'data_analysis.py'

data_analysis.data_collect("calgarytb")
data_analysis.basic_stats_total_cases("calgarytb")
data_analysis.linear_analysis_days_vs_total_cases("calgarytb")
data_analysis.polynomial_analysis_days_vs_total_cases("calgarytb")
data_analysis.linear_analysis_days_vs_new_cases("calgarytb") # ----- Linear Reg. does not fit the pattern at all
data_analysis.polynomial_analysis_days_vs_new_cases("calgarytb")
data_analysis.linear_analysis_temp_vs_total_cases("calgarytb")
data_analysis.linear_analysis_temp_vs_new_cases("calgarytb") # ------- Linear Reg. does not fit the pattern at all
data_analysis.multiple_regression_days_and_temp_vs_total_cases("calgarytb")
data_analysis.multiple_regression_days_and_temp_vs_new_cases("calgarytb")


















