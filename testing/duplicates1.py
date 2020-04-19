import pandas as pd

df = pd.read_csv('../5.162.125.116.csv')

# print(df.loc[df['timestamp'] == '2020-03-18 13:55:18', 'http_method'].iloc[0])

duplicate_in_time = df.duplicated(subset=['timestamp'])
# print(duplicate_in_time)

for inst in duplicate_in_time:
    print(inst)
    break

'''
for i in range(len(df)):
    # print(df['timestamp'].iloc[i])
    if duplicate_in_time.any() and df.loc[df['timestamp'] == df['timestamp'].iloc[i], 'http_method'].iloc[0] == "GET":
        print(df.loc[~duplicate_in_time], end='\n\n')
'''

# if duplicate_in_time.any():
#     print(df.loc[duplicate_in_time])
#     exit(0)
