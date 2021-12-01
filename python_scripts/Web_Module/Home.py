from python_scripts.Database.DB_Tools import DatabaseTools
from datetime import datetime


class Home:
    def __init__(self, table):
        self.db = DatabaseTools()
        self.table = table

    def daterange_data(self):
        res = self.db.get_daterange(self.table)
        data = {}
        for row in res:
            date_time = datetime.combine(row[0], row[1]).strftime("%Y-%m-%d %H:%M:%S")
            sens_name = self.db.sensor_name_by_id(row[2])
            if sens_name in data.keys():
                data[sens_name].append([date_time, row[2]])
            else:
                data[sens_name] = []
                data[sens_name].append([date_time, row[2]])
            # for row_min in res_min:
            #     if row_min[2] == row_max[2]:
            #         date_time_min = datetime.combine(row_min[0], row_min[1]).strftime("%Y-%m-%d %H:%M:%S")
            #         data.append({'x': sens_name, 'low': date_time_min, 'high': date_time_max})
        return data

    def rows_by_sensor(self):
        pass

    def na_count(self):
        pass