from math import isnan
from datetime import datetime,date,timedelta
import time
from Cleverfarm import CleverfarmAPI
from Database import DataDB

# Script run
# Start timer
start = time.time()
# Init empty object with api list
new_set = CleverfarmAPI()
# Get all features names and update them as dictionary key
new_set.get_features()
# Get data from all api and store it in a dict variable {'feature_name':[data]}
data = new_set.create_df_from_api()
# Init database object for specified schema
server = DataDB('cleverfarm')

for table in data.keys():
    # For each feature create list of tuples (rows) from dataset
    rows = [tuple(x) for x in data.get(table).to_numpy()]
    # Collect data for today from database
    actual = server.get_actual(table)
    nan = server.get_nan(table)
    for row in rows:
        if (row[0],datetime.strptime(row[1], "%Y-%m-%d").date(),datetime.strptime(row[2],"%H:%M:%S").time()) not in actual:
            server.insert_rows(table,row)
            print('Added data to {} successfully'.format(table))
        if ((row[0],datetime.strptime(row[1], "%Y-%m-%d").date(),datetime.strptime(row[2],"%H:%M:%S").time()) in nan) \
                    & (not isnan(row[3])):
            server.update_nan(table, row[::-1])


# Stop timer. Output time of run
print(time.time()-start)