import psycopg2
from dotenv import dotenv_values

# Getting environment variables
env = dotenv_values()


# Object for data stored in DB
class Database:
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
        
    def execute(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        

        if 'INSERT' in query or 'UPDATE' in query:
            self.conn.commit()

        cursor.close()
        return

    def fetchall(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        temp = cursor.fetchall()
        cursor.close()

        return temp
