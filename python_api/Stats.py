import pandas as pd
import psycopg2

# Database connection parameters
params = {
    'host': 'localhost',
    'database': 'data',
    'user': 'postgres',
    'password': 'vfrcfqvth',
    'port': '5432'
}


# Object for collecting and inserting data statistics
class Stats:
    # Initializing connection to DB on schema
    def __init__(self, schema):
        self.params = params
        self.conn = psycopg2.connect(**params)
        self.schema = schema

    # Method for collecting statistics from existing data
    def collect_stats(self, tables, month_start, month_end):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_name,value FROM %s.\"%s\" WHERE date >= '%s' AND date <= '%s' " % (
             self.schema, tables, month_start, month_end))
            data_for_stats = cursor.fetchall()
            cursor.close()
        # Create df from data for whole month
        temp = pd.DataFrame(data_for_stats, columns=['sensor_name','value'])
        df = pd.DataFrame()
        # Creating new columns with corresponding statistics(can be expanded)
        df.insert(0,'sensor_name', temp['sensor_name'].unique())
        df.insert(1,'year',month_start.year)
        df.insert(2, 'month', month_start.month)
        df.insert(3, 'feature', tables)
        df.insert(4, 'mean', temp.groupby(['sensor_name']).mean().values)
        df.insert(5, 'min', temp.groupby(['sensor_name']).min().values)
        df.insert(6, 'max', temp.groupby(['sensor_name']).max().values)
        return df

    # Method for inserting stats to the stats datatable
    def insert_stats(self, tables, feat_stats):
        # Create list of tuples, each tuple is a row in table
        stat_rows = [tuple(x) for x in feat_stats.to_numpy()]
        # Inserting to the DB
        if self.conn:
            query = "INSERT INTO %s.cleverfarm_stats(sensor_name,year,month,feature,mean,min,max) " \
                    "VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % self.schema
            cursor = self.conn.cursor()
            cursor.executemany(query, stat_rows)
            self.conn.commit()
            cursor.close()
            print('Inserted stats for {} successfully'.format(tables))
