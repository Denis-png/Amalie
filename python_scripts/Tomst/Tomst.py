import pandas as pd
from datetime import datetime
from os import listdir, replace, path, mkdir

from python_scripts.Database.Database import DataDB

class Tomst:
    def __init__(self, dir: str):
        self.db = DataDB()
        self.dir = dir
        self.path = ''
        self.current_file = ''
        self.temp = pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'variable_id'])
        self.result = {'TEMPERATURE': pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'variable_id']), 'SWP': pd.DataFrame(columns=['sensor_id', 'date', 'time', 'value', 'variable_id'])}

    def get_data(self):
        for filename in listdir(self.dir):
            if '.csv' in filename:
                self.path = self.dir + '/' + filename
                raw_data = pd.read_csv(self.path, sep=';')
                self.current_file = filename
                print('Loaded {}'.format(filename))
                return raw_data

    def process_data(self, data: list):
        # GET SERIAL NUMBER
        serial = self.current_file.split('_')[1]

        # GET DATE AND TIME
        date_time_list = data[data.columns[1]].tolist()
        date = []
        time = []

        for row in date_time_list:
            date.append(pd.to_datetime(row.split(' ')[0]))
            time.append(pd.to_datetime(row.split(' ')[1]))

        date = pd.Series(date)
        time = pd.Series(time)

        self.temp['date'] = date.dt.date
        self.temp['time'] = time.dt.time

        # GET SENSOR ID
        sensor_id = self.db.get_sensor_id_by_serial(serial)
        self.temp['sensor_id'] = sensor_id

        '''
        LOOP FOR TEMPERATURE VARIABLES
        '''
        count = 3
        var_list = ['T1', 'T2', 'T3']
        for var in var_list:

            # GET VALUES
            values = data[data.columns[count]]

            # GET VARIABLE ID
            variable_id = self.db.get_variable_id(var)

            def convert_to_double(value):
                return float(value.replace(',', '.'))

            self.temp['value'] = list(map(convert_to_double, values))
            self.temp['variable_id'] = variable_id

            self.result['TEMPERATURE'] = pd.concat([self.result['TEMPERATURE'], self.temp])

            count += 1
        '''
        GET SWP VARIABLE
        '''

        # GET VALUES
        values = data[data.columns[6]]

        # GET SWP VARIABLE ID
        variable_id = self.db.get_variable_id('vol_moisture')

        self.temp['value'] = values
        self.temp['variable_id'] = variable_id

        try:
            replace(path.abspath(self.path), path.abspath('files_collected')+'/Processed_on_{}'.format(datetime.now().date())+'/'+self.current_file)
        except FileNotFoundError:
            print('Creating a new directory at files_collected/...')
            mkdir(path.abspath('files_collected')+'/Processed_on_{}'.format(datetime.now().date()))
            replace(path.abspath(self.path), path.abspath('files_collected')+'/Processed_on_{}'.format(datetime.now().date())+'/'+self.current_file)

        print('Moved {} to the /files_collected/Processed_on_{}'.format(self.current_file, datetime.now().date()))

        self.result['SWP'] = pd.concat([self.result['SWP'], self.temp])
        return self.result

    def get_date_range(self):
        start_date = 0
        end_date = 0
        for data in self.result.values():
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






