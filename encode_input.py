import os
import pandas as pd
import pytz
from datetime import datetime
from crc64iso.crc64iso import crc64
import re
import hashlib

for j in os.listdir('inputs/'):
    # open all csv files in the given directory
    if j.endswith('.csv'):
        f_name = 'inputs/' + j
        df = pd.read_csv(f_name)

        # assign values by headers to variables
        DIMENSION = len(df)
        TIME_STAMP = df['timestamp']
        HTTP_METHOD = df['http_method']
        INVOKE_PATH = df['invoke_path']
        USER_AGENT = df['user_agent']

        # mapping function for http_method
        def method(argument):
            switcher = {
                "GET": 1,
                "POST": 2,
                "DELETE": 3
            }
            return switcher.get(argument, 404)

        # going through single csv file
        for i in range(DIMENSION):
            # encode date and time to timestamp value
            input_ = TIME_STAMP[i]
            slice_object = slice(26)
            time = input_[slice_object]
            dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            ts = pytz.utc.localize(dt).timestamp()
            interval_ = int(ts)
            df.at[i, "timestamp"] = interval_
            df.to_csv(f_name, index=False)

            # label encoding for http_method
            df.at[i, "http_method"] = method(HTTP_METHOD[i])
            df.to_csv(f_name, index=False)

            # binary encode resource access path
            md5 = hashlib.md5(INVOKE_PATH[i].encode('utf-8')).hexdigest()
            res = ''.join(format(ord(i), 'b') for i in md5[:10])
            df.at[i, "invoke_path"] = res
            df.to_csv(f_name, index=False)

            # label encoding user agent
            s = USER_AGENT[i]
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

            df.at[i, "user_agent"] = out
            df.to_csv(f_name, index=False)
