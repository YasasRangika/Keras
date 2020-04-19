from typing import Any, Union
import pandas as pd
import hashlib
import numpy as np


def ip_encode(ip):
    val = "".join([bin(int(x) + 256)[3:] for x in ip.split('.')])
    bin_val = int(val, 2)
    return (bin_val - 0) / 4294967295


def encode(f_name):
    df = pd.read_csv(f_name)

    bool_http = pd.notnull(df['http_method'])
    http_method = df[['http_method']][bool_http]
    # selecting all not null values for invoke_path
    bool_path = pd.notnull(df['invoke_path'])
    invoke_path = df[['invoke_path']][bool_path]
    # selecting all not null values for user_agent
    bool_agent = pd.notnull(df['user_agent'])
    user_agent = df[['user_agent']][bool_agent]
    # selecting all not null values for response_code
    bool_res_code = pd.notnull(df['response_code'])
    response_code = df[['response_code']][bool_res_code]

    ip = ip_encode(df['ip_address'][0])

    # mapping function for http_method
    def method(argument):
        switcher = {
            "GET": 1,
            "POST": 2,
            "DELETE": 3,
            "PUT": 4
        }
        return switcher.get(argument, 0)

    # label encoding for http_method
    for row in http_method.iterrows():
        val = method(row[1][0])
        norm_value: Union[int, float] = (val - 0) / 4
        df.at[row[0], "http_method"] = norm_value
        df.to_csv(f_name, index=False)

    # response code normalization
    for row in response_code.iterrows():
        # response codes -> 200,201,400,401,403,404,405,409,500,503
        norm_code = (row[1][0] - 0) / 303
        df.at[row[0], "response_code"] = norm_code
        df.to_csv(f_name, index=False)

    # binary encode resource access path
    for row in invoke_path.iterrows():
        md5 = hashlib.md5(row[1][0].encode('utf-8')).hexdigest()
        res = ''.join(format(ord(i), 'b') for i in md5[:10])
        res = res[0:60]
        bin_val = int(res, 2)
        # MinMax normalization applied -> min value = 0 & max value = 1152921504606846975( =
        # '111111111111111111111111111111111111111111111111111111111111')
        norm_val = (bin_val - 0) / 1152921504606846975
        df.at[row[0], "invoke_path"] = norm_val
        df.to_csv(f_name, index=False)

    # label encoding user agent
    for row in user_agent.iterrows():
        s = row[1][0]
        splt = s.split("/", 1)

        if "Mozilla" in splt[0]:
            browser = "m"
        elif "Opera" in splt[0]:
            browser = "o"
        elif "Firefox" in splt[0]:
            browser = "f"
        else:
            browser = None
            print("Error with browser categorization!")

        if "Windows" in splt[1]:
            plat_form = "w"
        elif "Linux" in splt[1]:
            plat_form = "l"
        else:
            plat_form = None
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
            out = 0
            print("Error with final label encoding!")

        norm_out = (out - 0) / 6
        df.at[row[0], "user_agent"] = norm_out
        df.to_csv(f_name, index=False)

    # df.iloc[:, 0] = df.iloc[:, 0].replace(to_replace=np.nan, value=ip)
    df.iloc[:, 1] = df.iloc[:, 1].replace(to_replace=[np.nan, df['ip_address'][0]], value=ip)
    # replace all NaN values with zero
    df = df.replace(np.nan, 0)
    # remove other columns
    keep_cols = ["ip_address", "http_method", "invoke_path", "user_agent", "response_code"]
    df.to_csv(f_name, columns=keep_cols, index=False)
