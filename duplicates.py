import pandas as pd

df = pd.read_csv('5.162.125.116.csv')
# df.sort('http_method').drop_duplicates(subset=['timestamp'], take_last=True)

# grp = df.groupby(['timestamp'])
# c_maxes = grp['http_method'].transform(max)
# df = df.loc[df['http_method'] == c_maxes]

# df.drop_duplicates(['http_method'], keep='last')

df.drop_duplicates(subset="timestamp", keep="first", inplace=True)
print(df)
# ids = df["timestamp"]
# duplicates = df[ids.isin(ids[ids.duplicated()])].sort_values("http_method")
# print(duplicates.head(30))

# Better peformance-remove comparing two columns, but when it has two columns to compare with GET and POST for example
# it will not compare.. Find a way to compare and keep only POSTs and DELETEs
# duplicates = df.reset_index().drop_duplicates(subset=['timestamp', 'http_method'], keep="first").set_index('timestamp')
# print(duplicates[['http_method']])

# duplicate_in_time = duplicates.duplicated(subset=['timestamp'])
# if duplicate_in_time.any():
#     print(duplicates.loc[duplicate_in_time])
# duplicates = df[df.duplicated(keep=False)]

# duplicates = df[df['timestamp'].duplicated() == True]

# if df['timestamp'].duplicated():
#     print("hi")
# else:
#     print("Bye")

# print(df['timestamp'].duplicated())
# print(duplicates.head(20))
