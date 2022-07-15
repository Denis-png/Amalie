import json
import requests
import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta
from Database import Database
from termcolor import colored

# Get environment variables
env = dotenv_values()


class Vrty:
    def __init__(self):
        self.api = json.loads(env['VRTY'])
        self.headers = {'Authorization': env['AUTH_VRTY']}
        self.db = Database()

        self.logs = {}


    def get_latest_row(self, sensor, variable):

        date_time = self.db.fetchall(f'SELECT date, time FROM global."data_Vrty" WHERE sensor_id={sensor} AND variable_id={variable} \
                                        ORDER BY date DESC, time DESC LIMIT 1')

        return date_time[0]


    def get_data(self):
        for req in self.api:

            today = datetime.now().date()
            start_time = datetime.strptime('00:00:00', '%H:%M:%S').time()

            start_date = datetime.combine(today - timedelta(days=1), start_time)
            until_date = datetime.combine(today, start_time)
            while start_date < until_date:
                for i in range(30):
                    end_date = start_date + timedelta(minutes=1)
                    data = requests.request("GET", req.format(start_date, end_date), headers=self.headers, data={})
                    if data.status_code == 200:
                        if len(data.json()) > 0:
                            for row in data.json():

                                serial = row['srcImsi']
                                try:
                                    sensor_id = self.db.fetchall(f'SELECT id FROM global.sensors WHERE serial_number=\'{serial}\'')[0][0]

                                    variables = self.db.fetchall('SELECT id, variable_id FROM global.variables WHERE note=\'Vrty\'')
                                    
                                    date_time = datetime.strptime(row['timestampUtc'], '%Y-%m-%dT%H:%M:%S%z')
                                    date = date_time.date()
                                    time = date_time.time()

                                    for var in variables:
                                        self.logs[f'{serial}/{var[1]}'] = []

                                        variable_id = var[0]

                                        value = row[var[1]]

                                        insert_row = (sensor_id, date, time, value, variable_id)

                                        datetime_last = self.get_latest_row(sensor_id, variable_id)


                                        if (datetime_last[0] is None) or ((date == datetime_last[0] and time > datetime_last[1]) or (date > datetime_last[0])):

                                            self.db.execute('INSERT INTO global."data_Vrty" (sensor_id, date, time, value, variable_id) \
                                                VALUES (%s, \'%s\', \'%s\', %s, %s)' % insert_row)
                                            self.logs[f'{serial}/{var[1]}'].append({'type': ('SUCCESS', 'green'), 'msg': f'Record inserted: {date} {time} - {value}'})


                                except IndexError:
                                    self.logs[f'Vrty/{serial}'] = []
                                    self.logs[f'Vrty/{serial}'].append({'type': ('ERROR', 'red'), 'msg': f'Sensor with serial number {serial} is not in database.'})
                                    continue         

                            break
                        else:
                            continue
                    else:
                        self.logs[f'Vrty/{req}'] = []
                        self.logs[f'Vrty/{req}'].append({'type': ('ERROR', 'red'), 'msg': f'No response from {req} ({start_date}/{end_date})'})

                start_date = start_date + timedelta(minutes=30)
        return self.logs

