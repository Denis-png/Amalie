from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
import sys
import time
sys.path.append('/home/eds/Current/Amalie/')

from python_scripts.Vrty.Vrty import Vrty
from python_scripts.Database.Database import DataDB
from python_scripts.Logger.Logger import Logger

log = Logger()


start_date = datetime(2021, 5, 24, 00, 00)

print(log.get_log())
