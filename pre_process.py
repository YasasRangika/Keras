import pandas as pd
import datetime
import numpy as np

'''
df = pd.read_csv("t1.csv")

# group by ip address
by_state = df.groupby("ip_address")

count = 0
# taking all ip address to name list
name = df['ip_address']

# take one by one grouped ips
for state, frame in by_state:
    df = pd.DataFrame(frame)
    # IP, token and other non changing columns removed[Selected timestamp - 1hr](After
    # 1hr token may be different)
    header = ["timestamp", "http_method", "invoke_path", "user_agent", "response_code"]
    df.to_csv('inputs/%s.csv' % frame.iloc[0]['ip_address'], columns=header, index=False)
    count = count + 1
print("Unique ip count :", count)
'''
'''
# removing milliseconds from time stamp*******************
opsd_daily = pd.read_csv('inputs/5.162.125.116.csv')
VAL = opsd_daily['timestamp']

for i in range(len(opsd_daily)):
    # encode date and time to timestamp value
    input_ = VAL[i]
    slice_object = slice(19)
    time = input_[slice_object]
    dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    # print(dt)
    opsd_daily.at[i, "timestamp"] = dt
    opsd_daily.to_csv('inputs/5.162.125.116.csv', index=False)
'''

'''
df = pd.read_csv('inputs/5.162.125.116.csv')
df.drop_duplicates(subset="timestamp", keep="first", inplace=True)
df.to_csv('inputs/5.162.125.116.csv', index=False)
'''

'''
df = pd.read_csv('inputs/5.162.125.116.csv')
min_index = min(df['timestamp'])
max_index = datetime.datetime.strptime(min_index, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)
df['timestamp'] = pd.to_datetime(df['timestamp'])
# fill missing with NaN values by incrementing seconds one by one
df = df.set_index('timestamp').reindex(pd.date_range(min_index, max_index, freq='S').fillna())
# df = df.replace(np.nan, 0)
# name the new index column(time stamp column)
df.index.names = ['timestamp']
df.to_csv('inputs/5.162.125.116.csv')
'''

