from datetime import datetime
import os

try:
    os.replace(os.path.abspath('Tomst/files_new')+'/'+'test.docx', os.path.abspath('Tomst/files_collected')+'/'+'Collected_on_{}/'.format(datetime.now().date())+'test.docx')
except FileNotFoundError:
    os.mkdir(os.path.abspath('Tomst/files_collected')+'/'+'Collected_on_{}'.format(datetime.now().date()))


print('Collected_on_{}/'.format(datetime.now().date()))