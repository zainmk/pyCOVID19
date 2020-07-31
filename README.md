# pyCOVID19
Combination of Selenium(Webscraping), MySQL, and ML to analyze data related to COVID-19

pyCOVID is a personal project of mine to test and apply what I've learned about python and its various tools. It begins with Webscraping
data from several websites that host data related to COVID-19. Initially this is just data based of the city for the number of cases.
Then after webscraping the approriate data, we upload and use MySQL, locally, to store the data and maintain it in a database that updates
accordingly when it needs to. After the data has been collected, we finally use models of machine learning and statistical analysis to
analyze the data and see if we can make any future predictions and/or updates.

Initially, for me the project was meant to exemplify my knowledge of python on a currently global topic of interest and for myself, see
what it really means to 'flatten the curve'. As I progress through the project, several changes will be made in terms of the...
  - type of data that is being compared (ex. temp of a city vs. new cases of COVID)
  - Geographical Location of Cities (Starting with Canada).
  - Experimenting with different kinds of elemtary data analysis
 
 Downloading the program requires ChromeDriver v83 (https://chromedriver.chromium.org/) and MySQL80 Community Server (https://dev.mysql.com/downloads/mysql/)
 
 Schedule:
 
May 18, 2020 - Start Date for Project

May 23, 2020 - Pushed existing intial code to Github

June 06, 2020 - Updated code posted. 'Calgary, AB' data collection is now complete and some elementary data analysis has been conducted.

June 28, 2020 - Added and updated data collection for 'Toronto, ON', now fully complete. Runs well wtih data analysis methods

July 30, 2020 - Fixed some bugs with the webscraping portion of the code. Added funcitonality for use without an SQL database. Added some data analysis methods.

...
