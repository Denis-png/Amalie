import requests
import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta

import sys
sys.path.append('/home/eds/Current/Amalie/')

from python_scripts.Database.Database import DataDB
# Getting environment variables
env = dotenv_values()


class Ekotechnika:
    def __init__(self):
        self.stations_url = env['STATIONS']
        self.sensors_url = env['SENSORS']
        self.data_url = env['API']
        self.auth = {
            'logName': env['USERNAME'],
            'logPass': env['PASSWORD'],
        }
        self.variables = {}
        self.db = DataDB()


    def sensors_vars(self):
        stations = requests.request("GET", self.stations_url, params=self.auth)
        sensors = requests.request("GET", self.sensors_url, params=self.auth)
        for station in stations.json()['stationsList']:
            for sensor in sensors.json()['getStationsSensors']:
                if station['id'] == sensor['id']:
                    self.variables[sensor['id']] = []
                    for variable in sensor['sensors']:
                        self.variables[sensor['id']].append({variable['id']: variable['name']})

        return self.variables

    def get_data(self, date_to):
        date_from = date_to - timedelta(days=1)
        date_to, date_from = date_to.strftime("%Y%m%d"), date_from.strftime("%Y%m%d")
        df = pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'variable_id'])
        for station_id in self.variables:
            url = self.data_url.format(self.auth['logName'], self.auth['logPass'], station_id, date_from, date_to)
            data = requests.request("GET", url)

            sensor_id = self.db.get_sensor_id_by_serial(station_id)
            for record in data.json()['mdataData']:

                # Processing date and time
                date_str = record[0][0:8]
                time_str = record[0][9:17]

                date = datetime.strptime(date_str, '%Y%m%d').date()
                time = datetime.strptime(time_str, '%H:%M:%S').time()

                for var in record[1]:
                    key = list(var)[0]
                    value = var[key]
                    var_id_long = f'{station_id}_{key}'
                    variable_id = self.db.get_variable_id(var_id_long)
                    df = df.append({
                        'sensor_id': sensor_id,
                        'date': date,
                        'time': time,
                        'value': value,
                        'variable_id': variable_id
                    }, ignore_index=True)

        return df










# variables = {
#   '1': 'Coulombetr',
#   '2': 'Precipitation',
#   '3': 'MatricPotential1',
#   '4': 'Temperature1',
#   '5': 'MatricPotential2',
#   '6': 'Temperature2',
#   '7': 'MatricPotential3',
#   '8': 'Temperature3',
#   '9': 'MatricPotential4',
#   '10': 'Temperature4',
#   '11': 'VapourPressure',
#   '12': 'AirTemperature',
#   '13': 'RelativeHumidity',
#   '14': 'AtmosphericPressure'
# }
#
# for station in stations.json()['stationsList']:
#     new_url = 'https://envirodata.cz/restapi/GetMData/mdataData?logName=Hradilek&logPass=7aIVCxxhfE&stationId={}&dateFrom=20210810&dateTo=20210811'.format(station['id'])
#     data_api = requests.request('GET', url=new_url, headers=headers, data=payload)
#     print(data_api.json())


