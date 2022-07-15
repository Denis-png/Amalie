import requests
import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta
from Database import Database
from termcolor import colored

# Getting environment variables
env = dotenv_values()

class Ekotechnika:
    def __init__(self):
        self.stations_url = env['STATIONS_EKOTECHNIKA']
        self.sensors_url = env['SENSORS_EKOTECHNIKA']
        self.api = env['EKOTECHNIKA']
        self.auth = {
            'logName': env['USERNAME_EKOTECHNIKA'],
            'logPass': env['PASSWORD_EKOTECHNIKA'],
        }

        self.db = Database()

        self.logs = {}

    def get_latest_row(self, sensor, variable):

        date_time = self.db.fetchall(f'SELECT date, time FROM global."data_Ekotechnika" WHERE sensor_id={sensor} AND variable_id={variable} \
                                        ORDER BY date DESC, time DESC LIMIT 1')

        return date_time[0]


    def get_data(self):

        end_date = datetime.strftime(datetime.now().date(), '%Y%m%d')
        start_date = datetime.strftime(datetime.now() - timedelta(days=1), '%Y%m%d')


        serials = requests.request("GET", self.stations_url, params=self.auth)
        if serials.status_code == 200:
            for serial in serials.json()['stationsList']:
                
                data = requests.request("GET", self.api.format(self.auth['logName'], self.auth['logPass'], serial["id"], start_date, end_date))

                if data.status_code == 200:

                    sensor_id = self.db.fetchall(f'SELECT id FROM global.sensors WHERE serial_number=\'{serial["id"]}\'')[0][0]
                    
                    if len(data.json()['mdataData']) > 0:
                        
                        for row in sorted(data.json()['mdataData']):

                            
                            date = datetime.strptime(row[0][0:8], '%Y%m%d').date()
                            time = datetime.strptime(row[0][9:17], '%H:%M:%S').time()

                            for var in row[1]:
                                var_key = f'{serial["id"]}_{list(var)[0]}'

                                self.logs[f'{serial["id"]}/{var_key}'] = []

                                try:
                                    variable_id = self.db.fetchall(f'SELECT id FROM global.variables WHERE variable_id=\'{var_key}\'')[0][0]

                                    value = var[list(var)[0]]

                                    datetime_last = self.get_latest_row(sensor_id, variable_id)

                                    
                                    if (datetime_last[0] is None) or (date == datetime_last[0] and time > datetime_last[1]) or (date > datetime_last[0]):

                                        insert_row = (sensor_id, date, time, value, variable_id)

                                        self.db.execute('INSERT INTO global."data_Ekotechnika" (sensor_id,date,time,value,variable_id) \
                                                        VALUES (%s, \'%s\', \'%s\', %s, %s)' % insert_row)

                                        self.logs[f'{serial["id"]}/{var_key}'].append({'type': ('SUCCESS', 'green'), 'msg': f'Record inserted: {date} {time} - {value}'})


                                except IndexError:
                                    self.logs[f'{serial["id"]}/{var_key}'].append({'type': ('ERROR', 'red'), 'msg': f'Variable {var_key} is not in database'})

                    else:
                        self.logs[f'Ekotechnika/{serial["id"]}'] = []
                        if data.json()["lastReceived"] != 'null':
                            latest = datetime.strptime(data.json()["lastReceived"], '%Y%m%d %H:%M:%S')
                            self.logs[f'Ekotechnika/{serial["id"]}'].append({'type': ('ERROR', 'red'), 'msg': f'Empty response, latest recieved {latest}'})
                        else:
                            self.logs[f'Ekotechnika/{serial["id"]}'].append({'type': ('ERROR', 'red'), 'msg': f'Empty response, no info on latest recieved...'})
                else:
                    self.logs[f'Ekotechnika/{serial["id"]}-{serial["title"]}'] = []
                    self.logs[f'Ekotechnika/{serial["id"]}-{serial["title"]}'].append({'type': ('ERROR', 'red'), 'msg': f'No response from {self.api}'})
        else:
            self.logs[f'Ekotechnika/{self.stations_url}'] = []
            self.logs[f'Ekotechnika/{self.stations_url}'].append({'type': ('ERROR', 'red'), 'msg': f'No response from {self.stations_url}'})

        return self.logs
            













