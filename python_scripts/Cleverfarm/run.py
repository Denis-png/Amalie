import time
from os import listdir
import sys

from Cleverfarm import CleverfarmAPI
import pandas as pd


sys.path.append('/home/denis-png/Projects/Amalie/python_scripts/Database')

from python_scripts.Database.Database import DataDB
from python_scripts.Logger.Logger import Logger

# Script run
# Start timer
start = time.time()
db_table = 'data_Cleverfarm'
log = Logger()
# Init empty object with api list
new_set = CleverfarmAPI()
# Get all features names and update them as dictionary key
new_set.get_features()
# Get data from all api and store it in a dict variable {'feature_name':[data]}
data, err = new_set.create_df_from_api()
# Get date range for new collected dataframe
date_range = new_set.get_date_range()
# Init database object for specified schema
db = DataDB()

if err:
    log.update_log(err)

# Preprocessing and inserting data to database
for table in data.keys():
    # For each feature create list of tuples (rows) from dataset
    rows = [tuple(x) for x in data.get(table).to_numpy()]
    # Collect data for date_range from database
    actual = db.get_actual(db_table, date_range)
    # Collect all the rows with NaN values
    nan = db.get_nan(db_table)

    # Check for duplicates and insert/update new values
    for row in rows:
        if (row[0], row[1], row[2], row[4]) not in actual:
            db.insert_rows(db_table, row)
        elif ((row[0], row[1], row[2], row[4]) in nan) \
                & (not pd.isna(row[3])):
            db.update_nan(db_table, row[::-1])
            print('Updated record in {}/{} with {}'.format(db_table, row[4], row[3]))

# Stop timer. Output time of run
print(time.time() - start)
