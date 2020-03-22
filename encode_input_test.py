import pandas as pd
import pytz
from datetime import datetime
import hashlib
import numpy as np

f_name = 'inputs/5.162.125.116.csv'
df = pd.read_csv(f_name)

# assign values by headers to variables
DIMENSION = len(df)
TIME_STAMP = df['timestamp']

bool_http = pd.notnull(df['http_method'])
HTTP_METHOD = df[['http_method']][bool_http]

bool_path = pd.notnull(df['invoke_path'])
INVOKE_PATH = df[['invoke_path']][bool_path]

bool_agent = pd.notnull(df['user_agent'])
USER_AGENT = df[['user_agent']][bool_agent]

# going through single csv file
for i in range(DIMENSION):
    # encode date and time to timestamp value
    input_ = TIME_STAMP[i]
    # slice_object = slice(26)
    # time = input_[slice_object]
    dt = datetime.strptime(input_, '%Y-%m-%d %H:%M:%S')
    ts = pytz.utc.localize(dt).timestamp()
    interval_ = int(ts)
    df.at[i, "timestamp"] = interval_
    df.to_csv(f_name, index=False)

# mapping function for http_method
def method(argument):
    switcher = {
        "GET": 1,
        "POST": 2,
        "DELETE": 3
    }
    return switcher.get(argument, 0)

# label encoding for http_method
for row in HTTP_METHOD.iterrows():
    df.at[row[0], "http_method"] = method(row[1][0])
    df.to_csv(f_name, index=False)

# binary encode resource access path
for row in INVOKE_PATH.iterrows():
    md5 = hashlib.md5(row[1][0].encode('utf-8')).hexdigest()
    res = ''.join(format(ord(i), 'b') for i in md5[:10])
    df.at[row[0], "invoke_path"] = res
    df.to_csv(f_name, index=False)

# label encoding user agent
for row in USER_AGENT.iterrows():
    s = row[1][0]
    splt = s.split("/", 1)

    if "Mozilla" in splt[0]:
        browser = "m"
    elif "Opera" in splt[0]:
        browser = "o"
    elif "Firefox" in splt[0]:
        browser = "f"
    else:
        print("Error with browser categorization!")

    if "Windows" in splt[1]:
        plat_form = "w"
    elif "Linux" in splt[1]:
        plat_form = "l"
    else:
        print("Error with platform categorization!")

    status = browser + plat_form

    if "mw" in status:
        out = 1
    elif "ml" in status:
        out = 2
    elif "ow" in status:
        out = 3
    elif "ol" in status:
        out = 4
    elif "fw" in status:
        out = 5
    elif "fl" in status:
        out = 6
    else:
        print("Error with final label encoding!")

    df.at[row[0], "user_agent"] = out
    df.to_csv(f_name, index=False)
df = df.replace(np.nan, 0)
df.to_csv(f_name)
