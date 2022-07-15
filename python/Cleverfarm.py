import json
import pandas as pd
import requests
from dotenv import dotenv_values, load_dotenv
from datetime import datetime, timedelta
from Database import Database
from termcolor import colored

# Getting environment variables
env = dotenv_values()

# Object with data from Cleverfarm APIs
class CleverfarmAPI:
    # Initial variables
    def __init__(self):

        # API urls
        self.api = json.loads(env['CLEVERFARM'])

        # Database object init
        self.db = Database()

        # Logs messages array
        self.logs = {}


    def get_latest_row(self, sensor, variable):

        date_time = self.db.fetchall(f'SELECT date, time FROM global."data_Cleverfarm" WHERE sensor_id={sensor} AND variable_id={variable} \
                                        ORDER BY date DESC, time DESC LIMIT 1')

        return date_time[0]


    # Method to get features - table names
    def get_data(self):
        for req in self.api:
            res = requests.get(req)
            if res.status_code == 200:
                for sensor in res.json()['sensors']:

                    sensor_name = res.json()['name'] 
                    variable_name = sensor['feature']

                    self.logs[f'{sensor_name}/{variable_name}'] = []

                    try:
                        sensor_id = self.db.fetchall(f'SELECT id FROM global.sensors WHERE sensor_name = \'{sensor_name}\'')[0][0] 
                    except IndexError:
                        self.logs[f'{sensor_name}/{variable_name}'].append({'type': ('ERROR', 'red'), 'msg': f'Sensor "{sensor_name}" was not found in database.'})

                    try:
                        variable_id = self.db.fetchall(f'SELECT id FROM global.variables WHERE name = \'{variable_name}\' ')[0][0]
                    except IndexError:
                        self.logs[f'{sensor_name}/{variable_name}'].append({'type': ('ERROR', 'red'), 'msg': f'Variable "{variable_name}" was not found in database.'})

                    datetime_last = self.get_latest_row(sensor_id, variable_id)

                    for row in sensor['data']:

                        # Datetime from string with timezone
                        date_time = datetime.strptime(row['time'], "%Y-%m-%dT%H:%M:%S%z")

                        date = date_time.date()
                        time = date_time.time()

                        value = row['value']

                        if ((date == datetime_last[0] and time > datetime_last[1]) or (date > datetime_last[0])) and not pd.isna(value):

                            self.db.execute(f'INSERT INTO global."data_Cleverfarm" (sensor_id, date, time, value, variable_id) \
                                                        VALUES({sensor_id}, \'{date}\', \'{time}\', {value}, {variable_id})')

                            self.logs[f'{sensor_name}/{variable_name}'].append({'type': ('SUCCESS', 'green'), 'msg': f'Record inserted: {date} {time} - {value}'})
                        elif pd.isna(value):
                            if time < datetime.now().time():
                                self.logs[f'{sensor_name}/{variable_name}'].append({'type': ('WARNING', 'yellow'), 'msg': f'Record has NaN value ({date} {time}).'})
            else:
                self.logs[f'Cleverfarm/{req}'] = []
                self.logs[f'Cleverfarm/{req}'].append({'type': ('ERROR', 'red'), 'msg': f'No response from API.'})

        return self.logs
                


                        
                                                       

                


