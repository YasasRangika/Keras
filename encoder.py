import pytz
from datetime import datetime
from crc64iso.crc64iso import crc64
import re
import hashlib
import pandas as pd

df = pd.read_csv("trafficSet.csv")

DIMENSION = 15
TIME_STAMP = df['timestamp']
IP_ADDRESS = df['ip_address']
ACCESS_TOKEN = df['access_token']
HTTP_METHOD = df['http_method']
INVOKE_PATH = df['invoke_path']
COOKIE = df['cookie']
ACCEPT = df['accept']
CONTENT_TYPE = df['content_type']
X_FORWARD_FOR = df['x_forwarded_for']
USER_AGENT = df['user_agent']

def method(argument):
    switcher = {
        "GET": 1,
        "POST": 2,
        "DELETE": 3
    }
    return switcher.get(argument, 404)

def content(argument):
    switcher = {
        "application/json": 1,
        "application/xml": 2
    }
    return switcher.get(argument, 404)

for i in range(DIMENSION-1):
    inpt = TIME_STAMP[i]
    slice_object = slice(26)
    time = inpt[slice_object]
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    ts = pytz.utc.localize(dt).timestamp()
    intval = int(ts)
    df.set_value(i, "timestamp", intval)
    df.to_csv("trafficSet.csv", index=False)

    ip = IP_ADDRESS[i]
    val = "".join([bin(int(x)+256)[3:] for x in ip.split('.')])
    df.set_value(i, "ip_address", val)
    df.to_csv("trafficSet.csv", index=False)

    line = ACCESS_TOKEN[i]
    line = re.sub('-', '', line)

    checksum = crc64(line)

    res = ''.join(format(ord(j), 'b') for j in checksum)
    df.set_value(i, "access_token", res)
    df.to_csv("trafficSet.csv", index=False)

    df.set_value(i, "http_method", method(HTTP_METHOD[i]))
    df.to_csv("trafficSet.csv", index=False)

    md5 = hashlib.md5(INVOKE_PATH[i].encode('utf-8')).hexdigest()
    res = ''.join(format(ord(i), 'b') for i in md5[:10])
    df.set_value(i, "invoke_path", res)
    df.to_csv("trafficSet.csv", index=False)

    line = COOKIE[i]
    line = re.sub('JSESSIONID=', '', line)
    checksum = crc64(line)
    res = ''.join(format(ord(i), 'b') for i in checksum)
    df.set_value(i, "cookie", res)
    df.to_csv("trafficSet.csv", index=False)

    df.set_value(i, "accept", content(ACCEPT[i]))
    df.to_csv("trafficSet.csv", index=False)

    df.set_value(i, "content_type", content(CONTENT_TYPE[i]))
    df.to_csv("trafficSet.csv", index=False)

    ip = X_FORWARD_FOR[i]
    val = "".join([bin(int(x)+256)[3:] for x in ip.split('.')])
    df.set_value(i, "x_forwarded_for", val)
    df.to_csv("trafficSet.csv", index=False)

    s = USER_AGENT[i]
    splt = s.split("/", 1)
    # kept defaults to zero to exit from the code if there is a fault
    browser = 0
    plat_form = 0

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

    res = ''.join(format(ord(i), 'b') for i in browser + plat_form)
    df.set_value(i, "user_agent", res)
    df.to_csv("trafficSet.csv", index=False)

#For label encoding user agent
'''    for i in range(len(frame) - 1):
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

        # print(out)
        # df.set_value(i, 'user_agent', out)
        # df.at[i, 'user_agent'] = out
        #USER_AGENT[i].update(i, out)
        df.loc[i, 'user_agent'] = out'''