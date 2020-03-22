import pandas as pd
from datetime import datetime

# removing milliseconds from time stamp*******************
opsd_daily = pd.read_csv('5.162.125.116.csv')
VAL = opsd_daily['timestamp']

for i in range(len(opsd_daily)):
    # encode date and time to timestamp value
    input_ = VAL[i]
    slice_object = slice(19)
    time = input_[slice_object]
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    # print(dt)
    opsd_daily.at[i, "timestamp"] = dt
    opsd_daily.to_csv('5.162.125.116.csv', index=False)

df = pd.read_csv("5.162.125.116.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
# fill missing with NaN values by incrementing seconds one by one
df = df.set_index('timestamp').reindex(pd.date_range(min(df['timestamp']), max(df['timestamp']), freq='S').fillna())
# name the new index column(time stamp column)
df.index.names = ['timestamp']
df.to_csv("5.162.125.116.csv")