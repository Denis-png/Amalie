import pandas as pd
import requests

# List of API links for Cleverfarm company
api = ['https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/e06990a6-2c04-4bb3-a5be-48ffea49f603',
       'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/22626fb7-dbbb-45ef-8787-f3bccbb2526b',
       'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/f07231f8-39bc-4133-b799-591665b166a9',
       'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/230ac88f-4186-482c-ac02-f3b93e618b03',
       'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/0919e6f9-d6cf-4b2c-9321-01b6f54054e3',
       # 'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/efba0291-d89f-4966-908a-97fb1afe7f26',
       'https://p0c1rtf2ce.execute-api.eu-central-1.amazonaws.com/prod/88ff105f-2dde-4541-a3d7-0d6143b5452c']

# Object with data from Cleverfarm APIs
class CleverfarmAPI:
    # Initial variables
    def __init__(self):
        # API urls
        self.api = api
        # Empty data dictionary
        self.data = {}

    # Method to get features - table names
    def get_features(self):
        for req in self.api:
            res = requests.get(req)
            if res.status_code == 200:
                for sensor in res.json()['sensors']:
                    if sensor['feature'] not in self.data.keys():
                        # Updating data dictionary with features as keys and empty dataframe as values
                        self.data.update({sensor['feature']: pd.DataFrame()})
            else:
                print('CONNECTION ERROR: ', req.status_code)
        return self.data

    # Method for data frame creation from received data
    def create_df_from_api(self):
        for req in self.api:
            res = requests.get(req)
            if res.status_code == 200:
                for sensor in res.json()['sensors']:
                        df = pd.DataFrame(sensor['data'])  # Init dataframe from received data
                        df.insert(0, 'sensor_name', res.json()['name'])  # Adding a column with sensor's name
                        df.insert(1, 'date', df['time'].str.slice(start=0, stop=10))  # Separating date to date column
                        df['time'] = df['time'].str.slice(start=11, stop=19)  # Assigning time column to store only time
                        df.insert(4, 'signal', res.json()['signal'])  # Last column with signal property
                        temp = [self.data[sensor['feature']], df]  # Temporary list containing collected data and new
                        self.data[sensor['feature']] = pd.concat(temp)  # Concat on list to merge data together
            else:
                print('CONNECTION ERROR: ', req.status_code)
        return self.data
