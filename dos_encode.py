from typing import Any, Union
import pandas as pd
import hashlib
import numpy as np
import uuid

# HTTP_METHOD = 'http_method'
# INVOKE_PATH = 'invoke_path'
# USER_AGENT = 'user_agent'
# RESPONSE_CODE = 'response_code'
# IP_ADDRESS = 'ip_address'
# ACCESS_TOKEN = 'access_token'

HTTP_METHOD = 'Method'
INVOKE_PATH = 'URL'
USER_AGENT = 'User-agent'
RESPONSE_CODE = 'Response Code'
IP_ADDRESS = 'client-ip'
ACCESS_TOKEN = 'Authorization'


def ip_encode(ip):
    val = "".join([bin(int(x) + 256)[3:] for x in ip.split('.')])
    bin_val = int(val, 2)
    return (bin_val - 0) / 4294967295


def encode(f_name):
    df = pd.read_csv(f_name)

    bool_http = pd.notnull(df[HTTP_METHOD])
    http_method = df[[HTTP_METHOD]][bool_http]
    # selecting all not null values for invoke_path
    bool_path = pd.notnull(df[INVOKE_PATH])
    invoke_path = df[[INVOKE_PATH]][bool_path]
    # selecting all not null values for user_agent
    bool_agent = pd.notnull(df[USER_AGENT])
    user_agent = df[[USER_AGENT]][bool_agent]
    # selecting all not null values for response_code
    bool_res_code = pd.notnull(df[RESPONSE_CODE])
    response_code = df[[RESPONSE_CODE]][bool_res_code]
    # selecting all not null values for access_token
    bool_token = pd.notnull(df[ACCESS_TOKEN])
    access_token = df[[ACCESS_TOKEN]][bool_token]

    ip = ip_encode(df[IP_ADDRESS][0])

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
        df.at[row[0], HTTP_METHOD] = norm_value
        df.to_csv(f_name, index=False)

    # response code normalization
    for row in response_code.iterrows():
        # response codes -> 200,201,400,401,403,404,405,409,500,503
        norm_code = (row[1][0] - 0) / 303
        df.at[row[0], RESPONSE_CODE] = norm_code
        df.to_csv(f_name, index=False)

    # binary encode resource access path
    for row in invoke_path.iterrows():
        val = row[1][0].replace("https://172.17.0.1:8243/", "")
        md5 = hashlib.md5(val.encode('utf-8')).hexdigest()
        res = ''.join(format(ord(i), 'b') for i in md5[:10])
        res = res[0:60]
        bin_val = int(res, 2)
        # MinMax normalization applied -> min value = 0 & max value = 1152921504606846975( =
        # '111111111111111111111111111111111111111111111111111111111111')
        norm_val = (bin_val - 0) / 1152921504606846975
        df.at[row[0], INVOKE_PATH] = norm_val
        df.to_csv(f_name, index=False)

    # binary encode access token uuid
    for row in access_token.iterrows():
        int_val = uuid.UUID(row[1][0].replace('Bearer', '').replace(' ', '')).int
        # MinMax normalization applied -> min value = 0 & max value = 340282366920938463463374607431768211455( =
        # 'ffffffff-ffff-ffff-ffff-ffffffffffff')
        norm_val = int_val / 340282366920938463463374607431768211455
        df.at[row[0], ACCESS_TOKEN] = norm_val
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
        df.at[row[0], USER_AGENT] = norm_out
        df.to_csv(f_name, index=False)

    # df.iloc[:, 0] = df.iloc[:, 0].replace(to_replace=np.nan, value=ip)
    df.iloc[:, 1] = df.iloc[:, 1].replace(to_replace=[np.nan, df[IP_ADDRESS][0]], value=ip)
    # replace all NaN values with zero
    df = df.replace(np.nan, 0)
    # remove other columns
    keep_cols = [IP_ADDRESS, ACCESS_TOKEN, HTTP_METHOD, INVOKE_PATH, USER_AGENT, RESPONSE_CODE]
    df.to_csv(f_name, columns=keep_cols, index=False)
    df1 = pd.read_csv(f_name)
    df1.columns = ['ip_address', 'access_token', 'http_method', 'invoke_path', 'user_agent', 'response_code']
    df1.to_csv(f_name, index=False)
