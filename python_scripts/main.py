
from datetime import datetime,date,timedelta
import time
from os import listdir
from Cleverfarm import CleverfarmAPI
from Tomst import Tomst
from Database import DataDB
import pandas as pd

# Script run
# Start timer
start = time.time()
# Init empty object with api list
new_set = CleverfarmAPI()
# Get all features names and update them as dictionary key
new_set.get_features()
# Get data from all api and store it in a dict variable {'feature_name':[data]}
cleverfarm = new_set.create_df_from_api()

if listdir('/home/eds/Amalie_03/python_api/tomst_files_new'):
	tomst_init = Tomst('/home/eds/Amalie_03/python_api/tomst_files_new')
	tomst_init.get_data()
	tomst = tomst_init.process_data(cleverfarm)
else:
	tomst = {}
	
data = {**cleverfarm, **tomst}

# Init database object for specified schema
server = DataDB('global')

for table in data.keys():
    # For each feature create list of tuples (rows) from dataset
    rows = [tuple(x) for x in data.get(table).to_numpy()]
    # Collect data for today from database
    actual = server.get_actual(table)
    nan = server.get_nan(table)
    for row in rows:
        if (row[0], row[1], row[2]) not in actual:
            server.insert_rows(table,row)
            print('Added data to {} successfully'.format(table))
        if ((row[0], row[1], row[2]) in nan) \
                    & (not pd.isna(row[3])):
            print(row[3])
            server.update_nan(table, row[::-1])


# Stop timer. Output time of run
print(time.time()-start)
