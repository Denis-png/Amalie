from datetime import date, timedelta
import psycopg2

# Database connection parameters
params = {
    'host': 'localhost',
    'database': 'data',
    'user': 'postgres',
    'password': 'vfrcfqvth',
    'port': '5432'
}


# Object for data stored in DB
class DataDB:
    # Init object with connection to DB and corresponding schema
    def __init__(self, schema):
        self.params = params
        self.conn = psycopg2.connect(**params)
        self.schema = schema

    # Method for collecting NaN values from datatable
    def get_nan(self, tables):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_name,date,time FROM %s.\"%s\" WHERE value = double precision 'NaN'" % (self.schema, tables))
            temp = cursor.fetchall()
            cursor.close()
            return temp

    # Method for collecting current day data
    def get_actual(self, tables):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_name,date,time FROM %s.\"%s\" WHERE date >= '%s'" % (self.schema, tables, (date.today() - timedelta(days=1))))
            temp = cursor.fetchall()
            cursor.close()
            return temp

    # Method for inserting rows into datatable(should be used with get_actual() to avoid duplications)
    def insert_rows(self,tables, rows):
        if self.conn:
            query = "INSERT INTO %s.\"%s\"(sensor_name,date,time,value,signal) VALUES(%%s,%%s,%%s,%%s,%%s)" % (self.schema, tables)
            cursor = self.conn.cursor()
            cursor.execute(query,rows)
            self.conn.commit()
            cursor.close()

    # Method for updating NaN values if new received are not NaN
    def update_nan(self, tables, row):
        if self.conn:
            query = "UPDATE %s.\"%s\" SET signal = %%s, value = %%s " \
                    "WHERE time = %%s AND date = %%s AND sensor_name = %%s " \
                    "AND value = double precision 'NaN'" % (self.schema, tables)
            cursor = self.conn.cursor()
            cursor.execute(query,row)
            self.conn.commit()
            cursor.close()
            print('Updated data in {} successfully'.format(tables))


