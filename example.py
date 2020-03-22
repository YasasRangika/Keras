import pandas as pd
import datetime

# # read csv without indexing to get min and max timstamps
# tmp = pd.read_csv('5.162.125.116.csv')
# min_index = min(tmp['timestamp'])
# max_index = datetime.datetime.strptime(min_index, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)

df = pd.read_csv('5.162.125.116.csv', index_col=0, parse_dates=True)

# times_sample = pd.to_datetime(min_index, max_index)
# Select the specified dates and just the Consumption column
consum_sample = df.loc[df, ['http_method']].copy()
print(consum_sample)

# Convert the data to one second frequency, without filling any missings
consum_freq = consum_sample.asfreq('S', method=None, fill_value=None)
print(consum_freq)
# Create a column with missings forward filled
# consum_freq['http_method-new'] = consum_sample.asfreq('S', method='ffill')
# print(consum_freq)

# -----------------------------------------------------------------------------------------
# opsd_daily = pd.read_csv('opsd_germany_daily.csv', index_col=0, parse_dates=True)
#
# times_sample = pd.to_datetime(['2013-02-03', '2013-02-06', '2013-02-08'])
# # Select the specified dates and just the Consumption column
# consum_sample = opsd_daily.loc[times_sample, ['Consumption']].copy()
# # print(consum_sample)
#
# # Convert the data to daily frequency, without filling any missings
# consum_freq = consum_sample.asfreq('D')
# # Create a column with missings forward filled
# consum_freq['Consumption - Forward Fill'] = consum_sample.asfreq('D', method='ffill')
# print(consum_freq)