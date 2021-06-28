from query.models import *
from dashboard.models import *

GLOBAL = [Sensors, MaintenanceActions]
CLEVERFARM = [Swp, Tmp, Hum, Rnf, Lfw, Prs, Wnd, Wng, Wns]
DVORAK = []



class CFRouter(object):
    def db_read(self, model, **hints):
        if model in CLEVERFARM:
            return 'cleverfarm'
        elif model in DVORAK:
            return 'dvorak'
        elif model in GLOBAL:
            return 'global'
        return 'main'

    def db_write(self, model, **hints):
        if model in CLEVERFARM:
            return 'cleverfarm'
        elif model in DVORAK:
            return 'dvorak'
        elif model in GLOBAL:
            return 'global'
        return 'main'
