from Database import Database


class SumStats:
    def __init__(self):
        self.db = Database()
        self.companies = self.db.fetchall('SELECT id, name FROM global."companies"')

    def stats(self):
        for company in self.companies:
            
            company_id = company[0]
            company_name = company[1]

            variables = self.db.fetchall(f'SELECT id,name FROM global."variables" WHERE company_id={company_id}')

            for variable in variables:
                
                variable_id = variable[0]
                variable_name = variable[1]

                mean = self.db.fetchall(f'SELECT AVG(value) FROM global."data_{company_name}" WHERE variable_id={variable_id} AND value != double precision \'NaN\' ')[0][0]
                median = self.db.fetchall(f'SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) FROM global."data_{company_name}" WHERE variable_id={variable_id} AND value != double precision \'NaN\'')[0][0]
                std = self.db.fetchall(f'SELECT STDDEV(value) FROM global."data_{company_name}" WHERE variable_id={variable_id} AND value != double precision \'NaN\'')[0][0]
                maximum = self.db.fetchall(f'SELECT MAX(value) FROM global."data_{company_name}" WHERE variable_id={variable_id} AND value != double precision \'NaN\'')[0][0]
                minimum = self.db.fetchall(f'SELECT MIN(value) FROM global."data_{company_name}" WHERE variable_id={variable_id} AND value != double precision \'NaN\'')[0][0]

                exist_check = self.db.fetchall(f'SELECT id FROM global."summary_stats" WHERE company_id={company_id} AND variable_id={variable_id}')

                if len(exist_check) > 0:
                    self.db.execute(f'UPDATE global."summary_stats" SET mean={mean},median={median},std={std},max={maximum},min={minimum} WHERE company_id={company_id} AND variable_id={variable_id}')
                else:
                    self.db.execute(f'INSERT INTO global."summary_stats" (company_id,variable_id,mean,median,std,max,min) VALUES ({company_id},{variable_id},{mean},{median},{std},{maximum},{minimum})')

            