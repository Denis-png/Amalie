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
            return duplicates

    def na_percentage(self, table):
        pass

    def stats(self, table):
        pass