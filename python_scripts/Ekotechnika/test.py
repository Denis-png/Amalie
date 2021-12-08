from datetime import datetime, timedelta


date = datetime.today().date()
print(date.strftime("%Y%m%d"))
date_from = date - timedelta(days=1)
print(date_from)

