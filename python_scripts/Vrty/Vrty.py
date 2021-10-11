import json

import requests
import pandas as pd
from dotenv import dotenv_values
from datetime import datetime
from python_scripts.Database.Database import DataDB

# Get environment variables
env = dotenv_values()


class Vrty:
    def __init__(self):
        self.api = json.loads(env['API'])
        self.headers = {'Authorization': env['AUTH']}
        self.db = DataDB()

    def get_data(self, date_from, date_to):
        for url in self.api:
            data = requests.request("GET", url.format(date_from, date_to), headers=self.headers, data={})
            print(data.text)
            df = pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'signal', 'variable_id'])

            result = {'TEMPERATURE': df, 'HUMIDITY': df, 'WATER_LEVEL': df, 'WATER_TEMPERATURE': df}

            for record in data.json():

                serial_number = record['srcImsi']
                # sensor_id = self.db.get_sensor_id_by_serial(serial_number)

                date = datetime.strptime(record['timestampUtc'][:10], '%Y-%m-%d').date()
                time = datetime.strptime(record['timestampUtc'][11:19], '%H:%M:%S').time()

                humidity = record['humidity']

                result['HUMIDITY'] = result['HUMIDITY'].append({
                    'sensor_id': serial_number,
                    'date': date,
                    'time': time,
                    'value': humidity,
                }, ignore_index=True)

                temperature = record['temperature']

                result['TEMPERATURE'] = result['TEMPERATURE'].append({
                    'sensor_id': serial_number,
                    'date': date,
                    'time': time,
                    'value': temperature,
                }, ignore_index=True)

                water_level = record['waterLevelMillimeters']

                result['WATER_LEVEL'] = result['WATER_LEVEL'].append({
                    'sensor_id': serial_number,
                    'date': date,
                    'time': time,
                    'value': water_level,
                }, ignore_index=True)

                water_temperature = record['waterTemperature']

                result['WATER_TEMPERATURE'] = result['WATER_TEMPERATURE'].append({
                    'sensor_id': serial_number,
                    'date': date,
                    'time': time,
                    'value': water_temperature,
                }, ignore_index=True)

            print(result)
