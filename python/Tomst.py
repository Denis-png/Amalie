import pandas as pd
import csv
from datetime import datetime
from os import listdir, replace, path, mkdir
from Database import Database
from termcolor import colored

class Tomst:
    def __init__(self):
        self.db = Database()
        self.init_dir = '../data/Tomst/new/'
        self.end_dir = '../data/Tomst/old/'
        # Get variable ids
        self.t1 = self.db.fetchall(f'SELECT id FROM global.variables WHERE variable_id = \'T1\'')[0][0]
        self.t2 = self.db.fetchall(f'SELECT id FROM global.variables WHERE variable_id = \'T2\'')[0][0]
        self.t3 = self.db.fetchall(f'SELECT id FROM global.variables WHERE variable_id = \'T3\'')[0][0]
        self.vm = self.db.fetchall(f'SELECT id FROM global.variables WHERE variable_id = \'vol_moisture\'')[0][0]

        self.logs = {}

    def get_existing(self, sensor, start_date, end_date):

        temp = self.db.fetchall(f'SELECT sensor_id, date, time, value, variable_id FROM global."data_Tomst" WHERE sensor_id={sensor} \
                                                                             AND date>=\'{start_date}\' AND date<=\'{end_date}\';')
        return temp

    def get_date_range(self, path):
        with open(path, newline='') as csvfile:
            raw_data = csv.reader(csvfile, delimiter=';')

            date_range = [
                datetime.strptime(next(raw_data)[1], "%Y.%m.%d %H:%M").date(),
                datetime.strptime(csvfile.readlines()[-1].split(';')[1], "%Y.%m.%d %H:%M").date()
            ]

        csvfile.close()
        
        return date_range


    def get_data(self):
        if len(listdir(self.init_dir)) > 0:
            for filename in listdir(self.init_dir):
                if '.csv' in filename:
                    path = self.init_dir + '/' + filename
                    
                    with open(path, newline='') as csvfile:
                        raw_data = csv.reader(csvfile, delimiter=';')

                        print('Loaded {}'.format(filename))

                        date_range = self.get_date_range(path)


                        # Get sensor id by serial nubmer
                        serial = filename.split('_')[1]
                        sensor_id = self.db.fetchall(f'SELECT id from global.sensors WHERE serial_number=\'{serial}\'')[0][0]

                        exists = self.get_existing(sensor_id, date_range[0], date_range[1])

                        self.logs[f'{serial}'] = []

                        for row in raw_data:
                            
                            # Get date and time
                            date_time = datetime.strptime(row[1], "%Y.%m.%d %H:%M")
                            date = date_time.date()
                            time = date_time.time()



                            # Create list of tuples (variable_id, value)
                            values = [
                                (self.t1, float(row[3].replace(',', '.'))), 
                                (self.t2, float(row[4].replace(',', '.'))), 
                                (self.t3, float(row[5].replace(',', '.'))), 
                                (self.vm, float(row[6].replace(',', '.')))
                            ]

                            row_count = 0

                            for value in values:

                                insert_row = (sensor_id, date, time, value[1], value[0])
                                
                                if insert_row not in exists:
                                    self.db.execute('INSERT INTO global."data_Tomst" (sensor_id, date, time, value, variable_id) \
                                                                        VALUES (%s,\'%s\',\'%s\',%s,%s);' % insert_row)
                                    row_count += 1

                            self.logs[f'{serial}'].append({'type': ('SUCCESS', 'green'), 'msg': f'{row_count} records inserted'})                                                
                                
                    csvfile.close()


                    try:
                        replace(path, self.end_dir + f'Processed_on_{datetime.now().date()}' + '/' + filename)
                        self.logs[f'{serial}'].append({'type': ('INFO', 'blue'), 'msg': f'File {filename} has been moved to Processed_on_{datetime.now().date()}'})

                    except FileNotFoundError:
                        self.logs[f'{serial}'].append({'type': ('INFO', 'blue'), 'msg': f'Created new directory Processed_on_{datetime.now().date()}'})

                        mkdir(self.end_dir + f'Processed_on_{datetime.now().date()}')

                        replace(path, self.end_dir + f'Processed_on_{datetime.now().date()}' + '/' + filename)
                        self.logs[f'{serial}'].append({'type': ('INFO', 'blue'), 'msg': f'File {filename} has been moved to Processed_on_{datetime.now().date()}'})

            return self.logs
        else:
            processed = [datetime.strptime(x.split('_')[2], '%Y-%m-%d') for x in listdir(self.end_dir)]

            latest = max(processed)

            self.logs['Tomst'] = [{'type': ('WARNING', 'yellow'), 'msg': f'No new files found in data/Tomst/new, latest proccessing was on {latest.date()}'}]

            return self.logs


                                


            

