import json
import requests
import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta

from python_scripts.Database.Database import DataDB


# Get environment variables
env = dotenv_values()


class Vrty:
    def __init__(self):
        self.api = json.loads(env['API'])
        self.headers = {'Authorization': env['AUTH']}
        self.db = DataDB()
        self.step = 30
        self.table = 'data_Vrty'
        self.err = []
        self.count = 0

    def get_data(self, start_date=datetime(2021, 5, 24, 00, 00)):
        self.count += 1
        if self.count > 10:
            return pd.DataFrame(), self.err
        for url in self.api:
            df = pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'variable_id'])

            vars = [x[0] for x in self.db.get_variable_by_company('Vrty')]

            step = '30min'

            for var in vars:
                date_time = self.db.get_recent_by_variable(self.table, var)
                if not date_time:
                    end_date = datetime(2021, 5, 25, 00, 00)
                    break
                elif datetime.combine(date_time[0], date_time[1]) > start_date:
                    start_date = datetime.combine(date_time[0], date_time[1])

                end_date = start_date + timedelta(days=1)

            datetime_range = pd.date_range(start_date, end_date, freq=step)
            for i in range(len(datetime_range)):
                if i == len(datetime_range)-1:
                    if df.size <= 0:
                        start_date += timedelta(days=1)
                        start_date = start_date.replace(second=0)
                        print('Looking for data...')
                        print(start_date)
                        df, errs = self.get_data(start_date)
                        self.err += errs
                        return df, self.err
                    return df, self.err
                date_from = datetime_range[i]
                date_to = datetime_range[i + 1]

                data = requests.request("GET", url.format(date_from, date_to), headers=self.headers, data={})
                if len(data.text) <= 2:
                    self.err.append({'date': str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),
                                     'company': 'Vrty',
                                     'message': f'Empty data for {date_from} / {date_to}!'})
                    continue
                for record in data.json():
                    try:
                        serial_number = record['srcImsi']
                    except TypeError:
                        self.err.append({'date': str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),
                                         'company': 'Vrty',
                                         'message': f'Request for {date_from} / {date_to} had crashed!'})
                        continue

                    try:
                        sensor_id = self.db.get_sensor_id_by_serial(serial_number)
                    except TypeError:
                        self.err.append({'date': str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),
                                         'company': 'Vrty',
                                         'message': f'{serial_number} is not in Sensor table!'})
                        continue

                    date = datetime.strptime(record['timestampUtc'][:10], '%Y-%m-%d').date()
                    time = datetime.strptime(record['timestampUtc'][11:19], '%H:%M:%S').time()

                    for var in vars:
                        values = record[var]

                        variable_id = self.db.get_variable_id(var)

                        df = df.append({
                            'sensor_id': sensor_id,
                            'date': date,
                            'time': time,
                            'value': values,
                            'variable_id': variable_id,
                        }, ignore_index=True)
            return df, self.err


