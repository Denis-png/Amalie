import time
from os import listdir

from .. import Database
from Cleverfarm import CleverfarmAPI
import pandas as pd

# Script run
# Start timer
start = time.time()

# Init empty object with api list
new_set = CleverfarmAPI()
# Get all features names and update them as dictionary key
new_set.get_features()
# Get data from all api and store it in a dict variable {'feature_name':[data]}
data = new_set.create_df_from_api()
# Get date range for new collected dataframe
date_range = new_set.get_date_range()
# Init database object for specified schema
db = Database.DataDB()

# Preprocessing and inserting data to database
for table in data.keys():
    # For each feature create list of tuples (rows) from dataset
    rows = [tuple(x) for x in data.get(table).to_numpy()]
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
