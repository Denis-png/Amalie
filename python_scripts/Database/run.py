from DB_Tools import DatabaseTools

db_tools = DatabaseTools()

# db_tools.backup('data')

dup = db_tools.find_duplicates('SWP')
