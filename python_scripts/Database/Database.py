import psycopg2
from dotenv import dotenv_values

# Getting environment variables
env = dotenv_values()


# Object for data stored in DB
class DataDB:
    # Init object with connection to DB and corresponding schema
    def __init__(self):
        self.params = {
            'host': env['HOST'],
            'database': env['DATABASE'],
            'user': env['USER'],
            'password': env['PASSWORD'],
            'port': env['PORT']
        }
        self.conn = psycopg2.connect(**self.params)

    # Method for collecting NaN values from datatable
    def get_nan(self, table: str):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_id,date,time,variable_id FROM global.\"%s\" WHERE value = double precision 'NaN'" % table)
            temp = cursor.fetchall()
            cursor.close()
            return temp

    # Method for collecting data for specified date range
    def get_actual(self, table: str, date_range: list):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT sensor_id,date,time,variable_id FROM global.\"%s\" WHERE date >= '%s' AND date <= '%s'" % (
            table, date_range[0], date_range[1]))
            temp = cursor.fetchall()
            cursor.close()
            return temp

    # Method for inserting rows into datatable(should be used with get_actual() to avoid duplications)
    def insert_rows(self, table, row: tuple):
        if self.conn:
            query = "INSERT INTO global.\"%s\"(sensor_id,date,time,value,variable_id) " \
                    "VALUES(%%s,%%s,%%s,%%s,%%s)" % table
            cursor = self.conn.cursor()
            cursor.execute(query,row)
            self.conn.commit()
            cursor.close()

    # Method for updating NaN values if new received are not NaN
    def update_nan(self, tables: dict, row: tuple):
        if self.conn:
            query = "UPDATE global.\"%s\" SET variable_id = %%s, value = %%s " \
                    "WHERE time = %%s AND date = %%s AND sensor_id = %%s" \
                    "AND value = double precision 'NaN'" % tables
            cursor = self.conn.cursor()
            cursor.execute(query,row)
            self.conn.commit()
            cursor.close()

    # Method for getting a sensor_id by sensor_name
    def get_sensor_id_by_name(self, sensor_name: str):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM global.sensors WHERE sensor_name = '%s' " % sensor_name)
            sensor_id = cursor.fetchone()
            cursor.close()
            return int(sensor_id[0])

    # Method for getting a sensor_id by serial number
    def get_sensor_id_by_serial(self, serial: str):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM global.sensors WHERE serial_number = '%s' " % serial)
            sensor_id = cursor.fetchone()
            cursor.close()
            return int(sensor_id[0])

    # Method for getting a variable id by variable_id column
    def get_variable_id(self, variable_id: str):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM global.variables WHERE variable_id = '%s' " % variable_id)
            variable_id = cursor.fetchone()
            cursor.close()
            return int(variable_id[0])

    def get_variable_by_company(self, company):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                f'SELECT variable_id FROM global."variables" WHERE note=\'{company}\';')
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def get_recent_by_variable(self, table, variable):
        if self.conn:
            cursor = self.conn.cursor()
            variable_id = self.get_variable_id(variable)
            cursor.execute(
                f'SELECT DISTINCT ON (variable_id) date, time FROM global."{table}" WHERE variable_id={variable_id} ORDER BY variable_id, date DESC, time DESC;')

            rows = cursor.fetchone()
            cursor.close()
            return rows



