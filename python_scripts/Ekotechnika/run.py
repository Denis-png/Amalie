from Ekotechnika import Ekotechnika
import time
import pandas as pd
from datetime import datetime, timedelta

import sys
sys.path.append('/home/eds/Current/Amalie/')

from python_scripts.Database.Database import DataDB
from python_scripts.Logger.Logger import Logger


# Script run
# Start timer
start = time.time()
db_table = 'data_Ekotechnika'
date = datetime(2021, 9, 23).date()
stop_date = datetime(2021, 4, 30).date()

log = Logger()
db = DataDB()

new_set = Ekotechnika()
new_set.sensors_vars()

while date > stop_date:
    try:
        print(date)
        date_range = [date - timedelta(days=1), date]
        data = new_set.get_data(date)
        rows = [tuple(x) for x in data.to_numpy()]

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
        date = date - timedelta(days=1)
        print(time.time() - start)
    except KeyError:
        log.update_log([
            {'date': str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),
              'company': 'Ekotechnika',
              'message': f'Empty data for {date - timedelta(days=1)} / {date}!'}
             ])
        date = date - timedelta(days=1)

print(time.time() - start)
