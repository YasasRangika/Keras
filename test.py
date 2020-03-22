import pandas as pd

# df = pd.read_csv("inputs/5.162.125.116.csv")
# idx = pd.date_range(min(df['timestamp']), max(df['timestamp']), freq='S')
# series = pd.Series(range(113), index=df['timestamp'])
# print(series)
idx = pd.date_range('2020-03-18 13:55:16.895347', '2020-03-18 13:55:26.895347', freq='S')

s = pd.Series({'2020-03-18 13:55:16.895347': 'GET',
              '2020-03-18 13:55:17.895347': 'GET',
              '2020-03-18 13:55:19.895347': "POST",
              '2020-03-18 13:55:21.895347': "DELETE"})
s.index = pd.DatetimeIndex(s.index)
#df.index = pd.to_datetime(df['timestamp'])
s = s.reindex(idx, fill_value=None)
#df = df.reindex(idx, fill_value=None)
print(s.head(10))

# series.resample('1s').asfreq()[0:5]
# print(series)