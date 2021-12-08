import json
import pandas as pd
import requests
from dotenv import dotenv_values, load_dotenv
from datetime import datetime

import sys
sys.path.append('/home/eds/Current/Amalie/')

from python_scripts.Database.Database import DataDB

# Getting environment variables
env = dotenv_values()

# Object with data from Cleverfarm APIs
class CleverfarmAPI:
    # Initial variables
    def __init__(self):
        # API urls
        self.api = json.loads(env['API'])
        # Empty data dictionary
        self.data = {}
        # Database object init
        self.db = DataDB()
        self.err = []

    # Method to get features - table names
    def get_features(self):
        for req in self.api:
            res = requests.get(req)
            if res.status_code == 200:
                for sensor in res.json()['sensors']:
                    if sensor['feature'] not in self.data.keys():
                        # Updating data dictionary with features as keys and empty dataframe as values
                        self.data.update({sensor['feature']: pd.DataFrame()})
            else:
                self.err.append({'date':str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")), 'company': 'Cleverfarm', 'message': f'Api connection error for {req}'})
        return self.data

    # Method for data frame creation from received data
    def create_df_from_api(self):
        for req in self.api:
            res = requests.get(req)
            if res.status_code == 200:
                for sensor in res.json()['sensors']:
                    df = pd.DataFrame(sensor['data'])  # Init dataframe from received data

                    sensor_name = res.json()['name']   # Sensor name for querying sensor_id
                    sensor_id = self.db.get_sensor_id_by_name(sensor_name)  # Sensor_id
                    df.insert(0, 'sensor_id', sensor_id)

                    df.insert(1, 'date', pd.to_datetime(df['time'].str.slice(start=0, stop=10)))  # Separating date to date column
                    df['date'] = df['date'].dt.date

                    df['time'] = pd.to_datetime(df['time'].str.slice(start=11, stop=19))  # Assigning time column to store only time
                    df['time'] = df['time'].dt.time

                    # df.insert(4, 'signal', res.json()['signal']) Column with signal property

                    variable_id = self.db.get_variable_id(sensor['feature'])  # Variable_id
                    df.loc[:, 'variable_id'] = variable_id

                    temp = [self.data[sensor['feature']], df]  # Temporary list containing collected data and new
                    self.data[sensor['feature']] = pd.concat(temp)  # Concat on list to merge data together
            else:
                self.err.append({'date':str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")), 'company': 'Cleverfarm', 'message': f'Api connection error for {req}'})
        return self.data, self.err

    def get_date_range(self):
        start_date = 0
        end_date = 0
        for data in self.data.values():
            temp_df = data.sort_values(by='date')
            min_date = min(temp_df['date'])
            max_date = max(temp_df['date'])
            if start_date == 0 and end_date == 0:
                start_date = min_date
                end_date = max_date
            elif start_date > min_date:
                start_date = min_date
            elif end_date < max_date:
                end_date = max_date
        return [start_date, end_date]



