import psycopg2
import pandas
from dotenv import dotenv_values
from os import system, path
from datetime import datetime


# Getting environment variables
env = dotenv_values()


class DatabaseTools:
    def __init__(self):
        self.params = {
            'host': env['HOST'],
            'database': env['DATABASE'],
            'user': env['USER'],
            'password': env['PASSWORD'],
            'port': env['PORT']
        }
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

    def backup(self, database):
        system('pg_dump --dbname=postgresql://{}:{}@{}:{}/{database} --file="{}/{database}-{}-backup.sql" --create'
               .format(env['USER'], env['PASSWORD'], env['HOST'], env['PORT'], path.abspath('Backups'), datetime.now().date(), database=database))
        print('Database {} was saved successfully'.format(database))

    def restore(self, database, schema):
        pass

    def find_duplicates(self, table):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_id,date,time,value,variable_id,COUNT(*) "
                           "FROM global.\"%s\" "
                           "GROUP BY sensor_id, date, time, value, variable_id "
                           "HAVING COUNT(*) > 1" % table)
            duplicates = cursor.fetchall()
            cursor.close()
            if duplicates:
                return len(duplicates)
            else:
                return 'No duplicates found!'

    def sensor_name_by_id(self, sensor_id):
        self.cur.execute(f'SELECT sensor_name FROM global."sensors" WHERE id={sensor_id}')
        data = self.cur.fetchone()
        return data[0]

    def get_daterange(self, table):
        self.cur.execute(f'SELECT date, time, sensor_id FROM global."{table}";')
        data = self.cur.fetchall()

        return data

    def na_percentage(self, table):
        self.cur.execute(f"SELECT COUNT(*) FROM global.\"{table}\" WHERE value = double precision 'NaN'")
        na_count = self.cur.fetchone()
        self.cur.execute(f'SELECT COUNT(*) FROM global."{table}"')
        total_count = self.cur.fetchone()
        return (na_count[0] / total_count[0]) * 100

    def rows_by_sensor(self, table):
        self.cur.execute(f'SELECT sensor_id, COUNT(*) FROM global."{table}" GROUP BY ')

    def stats(self, table):
        pass

    def add_company(self, dt_name):
        self.cur.execute(f'CREATE TABLE global."data_{dt_name}"('
                         f'id serial primary key ,'
                         f'date date,'
                         f'time time,'
                         f'value float,'
                         f'sensor_id int,'
                         f'variable_id int,'
                         f'FOREIGN KEY (sensor_id) REFERENCES global.sensors(id),'
                         f'FOREIGN KEY (variable_id) REFERENCES global.variables(id));')
        print(f'Created new table data_{dt_name}.')
        self.conn.commit()
        self.cur.close()
