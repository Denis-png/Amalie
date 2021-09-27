import pandas as pd
from os import listdir, replace

# Database connection parameters
import psycopg2

params = {
    'host': 'localhost',
    'database': 'data',
    'user': 'eds',
    'password': 'eds2021',
    'port': '5432'
}


class Tomst:
    def __init__(self, dir):
        self.conn = psycopg2.connect(**params)
        self.dir = dir
        self.files = listdir(dir)
        self.path = ''
        self.data = []
        self.temp = pd.DataFrame(columns=['date', 'time', 'value', 'signal', 'sensor_id', 'variable_id'])
        self.result = {'TEMPERATURE': pd.DataFrame(columns=['date', 'time', 'value', 'signal', 'sensor_id', 'variable_id']), 'SWP': pd.DataFrame(columns=['date', 'time', 'value', 'signal', 'sensor_id', 'variable_id'])}
        self.serial = ''

    def get_data(self):
        for filename in self.files:
            counter = 0
            if '.csv' in filename:
                self.path = self.dir + '/' + filename
                self.data = pd.read_csv(self.path, sep=';')
                if counter == 20:
                    break
                counter = counter + 1

                return self.data

    def process_data(self, external_data):
        for filename in self.files:
            # GET SERIAL NUMBER
            self.serial = filename.split('_')[1]

            # GET DATE AND TIME
            date_time_list = self.data[self.data.columns[1]].tolist()
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
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT id FROM global.dashboard_sensors WHERE serial_number = '%s' " % self.serial)
                sensor_id = cursor.fetchone()
                cursor.close()
            self.temp['sensor_id'] = sensor_id[0]


            # LOOP FOR TEMPERATURE VARIABLES
            count = 3
            var_list = ['T1', 'T2', 'T3']
            for var in var_list:

                # GET VALUES
                values = self.data[self.data.columns[count]]


                # GET VARIABLE ID
                if self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(
                        "SELECT id FROM global.dashboard_variables WHERE variable_id = '%s' " % var)
                    variable_id = cursor.fetchone()
                    cursor.close()

                def convert_to_double(value):
                    return float(value.replace(',', '.'))

                self.temp['value'] = list(map(convert_to_double, values))
                self.temp['variable_id'] = variable_id[0]

                external_data['TEMPERATURE'] = pd.concat([external_data['TEMPERATURE'], self.temp])

                count += 1

            # GET SWP VARIABLE

            # GET VALUES
            values = self.data[self.data.columns[6]]


            # GET SWP VARIABLE ID
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT id FROM global.dashboard_variables WHERE variable_id = 'vol_moisture' ")
                variable_id = cursor.fetchone()
                cursor.close()

            self.temp['value'] = values
            self.temp['variable_id'] = variable_id[0]

            replace('/home/eds/Amalie_03/python_api/tomst_files_new/{}'.format(filename), '/home/eds/Amalie_03/python_api/tomst_files_collected/{}'.format(filename))

            external_data['SWP'] = pd.concat([external_data['SWP'], self.temp])

        return external_data


'''tomst = Tomst('files')
tomst.get_data()
data = {'TEMPERATURE': pd.DataFrame(columns=['date', 'time', 'value', 'signal', 'sensor_id', 'variable_id']), 'SWP': pd.DataFrame(columns=['date', 'time', 'value', 'signal', 'sensor_id', 'variable_id'])}
print(tomst.process_data(data))'''





