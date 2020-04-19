import pandas as pd
import datetime

# making data frame from csv file
df = pd.read_csv("../5.162.125.116.csv", index_col=0, parse_dates=True)

# read csv without indexing to get min and max timstamps
tmp = pd.read_csv('../5.162.125.116.csv')
min_index = min(tmp['timestamp'])
max_index = datetime.datetime.strptime(min_index, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)

pidx = df.period_range(start ='2004-11-11 02:45:21', end ='2004-11-11 02:45:30', freq ='S')
print(pidx)

# consum_freq = df.asfreq('S', method=None, fill_value=None)
# print(consum_freq)

# idx = pd.date_range(min_index, max_index, freq='S')
# # print(idx)
#
# df.index = pd.to_datetime(df['timestamp'])
#
# df = df.reindex(idx, method='bfill')
# print(df.head())



