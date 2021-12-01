from python_scripts.Database.DB_Tools import DatabaseTools

db = DatabaseTools()

na_per = db.na_percentage('TEMPERATURE')

print(na_per)
