file_loc = ''  # deploy
# file_loc = '../.' # production

import pandas as pd
import time
from datetime import datetime
grouped_testing_data = pd.read_csv(file_loc + './data/testing_data.csv')
# print(grouped_testing_data)

d1 = "2020-02-04"
newdate1 = time.strptime(d1, "%Y-%m-%d")
# remove the date
grouped_testing_data = grouped_testing_data[grouped_testing_data['updatedon'] != d1 ]

dates_list = pd.Series(grouped_testing_data['updatedon']).to_list()
dates = [datetime.strptime( x, "%Y-%m-%d %H:%M:%S" ) for x in dates_list]
#print(date)
total_test = pd.Series(grouped_testing_data['totaltested']).to_list()
# print(total_test)
