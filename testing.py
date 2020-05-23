# This file is just for intermediate testing

from datetime import datetime

# Check to see if you can increment a datetime object to compare the values of the table in the db.
datetime_str = "05/22/2020"

datetime_obj = datetime.strptime(datetime_str, '%m/%d/%y')

print(type(datetime_obj))
print(datetime_obj)
