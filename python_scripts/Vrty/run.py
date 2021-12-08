from datetime import datetime
from Vrty import Vrty
import sys
import requests
import time
import pandas as pd
from python_scripts.Database.Database import DataDB
from python_scripts.Logger.Logger import Logger

# Script run
# Start timer

start = time.time()
log = Logger()
# Init empty object with api list
new_set = Vrty()
# Get data for specified date range
data, err = new_set.get_data()
table = 'data_Vrty'
# Init database object for specified schema
db = DataDB()

if err:
    log.update_log(err)
# For each feature create list of tuples (rows) from dataset
if data.size > 0:
    date_range = [datetime.combine(min(data.date), min(data.time)), datetime.combine(max(data.date), max(data.time))]
    rows = [tuple(x) for x in data.to_numpy()]
    # Collect data for date_range from database
    actual = db.get_actual(table, date_range)
    # Collect all the rows with NaN values
    nan = db.get_nan(table)

    # Check for duplicates and insert/update new values
    for row in rows:
        if (row[0], row[1], row[2]) not in actual:
            db.insert_rows(table, row)
        elif ((row[0], row[1], row[2]) in nan) \
                & (not pd.isna(row[3])):
            db.update_nan(table, row[::-1])
            print('Updated record in {} with {}'.format(table, row[3]))
    # Stop timer. Output time of run
    print(time.time() - start)


