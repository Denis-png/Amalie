from Cleverfarm import CleverfarmAPI
from Tomst import Tomst
from Bluebeatle import BlueBeatle
from Ekotechnika import Ekotechnika
from SummaryStats import SumStats

from termcolor import colored
from datetime import datetime

import schedule
import time
import json

# Summary stats 
def sum_stats():
    sum_stats = SumStats()
    sum_stats.stats()


# Get and insert Cleverfarm data
def cleverfarm_run():
    global cleverfarm_logs
    cleverfarm = CleverfarmAPI()
    logs = cleverfarm.get_data()
    
    cleverfarm_logs = []


    for name,log in logs.items():

        for row in log:

            date_time = datetime.today()


            print(f'{date_time.date()} {datetime.strftime(date_time, "%H:%M")} |', end='')

            print(colored(row["type"][0], row["type"][1]), end='')
            
            print(f'|{row["msg"]}| \033[1m[{name}]\033[0m')

            cleverfarm_logs.append(
                        {"date": f"{date_time.date()} {datetime.strftime(date_time, '%H:%M:%S')}", 
                        "type":row["type"], 
                        "msg":row["msg"], 
                        "sensor": name
                        })



# Get and insert Tomst data
def tomst_run():
    global tomst_logs
    tomst = Tomst()
    logs = tomst.get_data()
    
    tomst_logs = []

    for name,log in logs.items():
        
        for row in log:
            date_time = datetime.today()


            print(f'{date_time.date()} {datetime.strftime(date_time, "%H:%M")} |', end='')

            print(colored(row["type"][0], row["type"][1]), end='')
            
            print(f'|{row["msg"]}| \033[1m[{name}]\033[0m')

            tomst_logs.append(
                        {"date": f"{date_time.date()} {datetime.strftime(date_time, '%H:%M:%S')}", 
                        "type":row["type"], 
                        "msg":row["msg"], 
                        "sensor": name
                        })



# Get and insert Vrty data
def bluebeatle_run():
    global vrty_logs
    bb = BlueBeatle()
    logs = bb.get_data()
    
    bb_logs = []

    for name,log in logs.items():
        print(f'\033[1m---------------[{name}]---------------\033[0m')
        
        for row in log:
            date_time = datetime.today()


            print(f'{date_time.date()} {datetime.strftime(date_time, "%H:%M")} |', end='')

            print(colored(row["type"][0], row["type"][1]), end='')
            
            print(f'|{row["msg"]}| \033[1m[{name}]\033[0m')

            bb_logs.append(
                        {"date": f"{date_time.date()} {datetime.strftime(date_time, '%H:%M:%S')}", 
                        "type":row["type"], 
                        "msg":row["msg"], 
                        "sensor": name
                        })




# Get and insert Ekotechnika data
def ekotechnika_run():
    global ekotechnika_logs
    ekotechnika = Ekotechnika()
    logs = ekotechnika.get_data()

    ekotechnika_logs = []

    for name,log in logs.items():
        print(f'\033[1m---------------[{name}]---------------\033[0m')
        
        for row in log:
            date_time = datetime.today()


            print(f'{date_time.date()} {datetime.strftime(date_time, "%H:%M")} |', end='')

            print(colored(row["type"][0], row["type"][1]), end='')
            
            print(f'|{row["msg"]}| \033[1m[{name}]\033[0m')

            ekotechnika_logs.append(
                        {"date": f"{date_time.date()} {datetime.strftime(date_time, '%H:%M:%S')}", 
                        "type":row["type"], 
                        "msg":row["msg"], 
                        "sensor": name
                        })

# Get and insert EmsBrno data
def emsbrno_run():
    pass

# Get and insert EddyCovariance data
def eddycov_run():
    pass



if __name__ == '__main__':
 

    schedule.every().hour.do(cleverfarm_run)

    schedule.every().hour.do(bluebeatle_run)

    schedule.every().hour.do(ekotechnika_run)

    schedule.every().hour.do(tomst_run)

    schedule.every().hour.do(sum_stats)


    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)

        schedule.run_pending()

        log_file = open('logs/daily.txt', 'w')

        log_names = ['cleverfarm', 'bluebeatle', 'ekotechnika', 'tomst']

        logs = {}
    

        for name in log_names:
            try:
                logs[name] = globals()[f'{name}_logs']
            
            except (NameError,KeyError) as e:
                continue
        

        log_file.write(json.dumps(logs))

        log_file.close()

