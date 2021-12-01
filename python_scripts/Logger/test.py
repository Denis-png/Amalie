from datetime import datetime
from os import listdir, path

modules = [x for x in listdir(path.abspath('../'))]

print(modules)