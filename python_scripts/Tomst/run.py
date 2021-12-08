from python_scripts.Tomst.Tomst import Tomst
import time
import pandas as pd
from os import listdir

from python_scripts.Database.Database import DataDB

# Script run
while len(listdir('files_new')) > 0:
    # Start timer
    start = time.time()

    new_set = Tomst('files_new')
    raw_data = new_set.get_data()
    data = new_set.process_data(raw_data)
    date_range = new_set.get_date_range()
    print(date_range)

    # Init database object for specified schema
    db = DataDB()
    db_table = 'data_Tomst'

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
            if (row[0], row[1], row[2]) not in actual:
                db.insert_rows(db_table, row)
            elif ((row[0], row[1], row[2]) in nan) \
                    & (not pd.isna(row[3])):
                db.update_nan(db_table, row[::-1])
                print('Updated record in {}/{} with {}'.format(table, row[4], row[3]))
    # Stop timer. Output time of run
    print(time.time() - start)
