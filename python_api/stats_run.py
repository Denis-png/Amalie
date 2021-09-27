from datetime import date,timedelta
import time
from Stats import Stats
from Cleverfarm import CleverfarmAPI


# Script run
# Start timer
start = time.time()

# Init stats object on cleverfarm schema
stats_month = Stats('global')
# Init empty object with api list
api = CleverfarmAPI()
# Get all features names and update them as dictionary key
features = api.get_features()

for table in features.keys():
    if date.today().day == 1:
        month_end = (date.today() - timedelta(days=1))
        month_start = month_end.replace(day=1)
        feature_stats = stats_month.collect_stats(table, month_start, month_end)
        stats_month.insert_stats(table, feature_stats)
        print('Collected statistics for %s table' % table)
# Stop timer. Output time of run
print(time.time()-start)
