from datetime import datetime
from os import listdir, path

class Logger:
    def __init__(self):
        pass

    def get_log(self, company):
        err_count = 0
        modules = [x for x in listdir('/home/denis-png/Projects/Amalie/python_scripts')]
        try:
            with open(f'/home/denis-png/Projects/Amalie/python_scripts/Logger/logs/Log_{datetime.today().date()}.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if company in line:
                        err_count += 1
                f.close()
            return err_count
        except FileNotFoundError:
            with open(f'/home/denis-png/Projects/Amalie/python_scripts/Logger/logs/Log_{datetime.today().date()}.txt', 'w') as f:
                f.write('===Log file for common errors handling===\n')
                f.close()

            return err_count

    def update_log(self, err):
        try:
            with open(f'../Logger/logs/Log_{datetime.today().date()}.txt', 'a') as f:
                for msg in err:
                    f.write(msg['date'] + ' - ' + msg['company'] + ': ' + msg['message'] + '\n')
                f.close()
            print('Updated logs')
        except FileNotFoundError:
            with open(f'../Logger/logs/Log_{datetime.today().date()}.txt', 'w') as f:
                f.write('===Log file for common errors handling===\n')
                for msg in err:
                    f.write(msg['date'] + ' - ' + msg['company'] + ': ' + msg['message'] + '\n')
                f.close()
            print('Created logs')