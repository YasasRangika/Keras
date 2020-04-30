import datetime
import glob
import os
import shutil
import pandas as pd
from dos_encode import encode

# TIME_STAMP = 'timestamp'
# HTTP_METHOD = 'http_method'
# INVOKE_PATH = 'invoke_path'
# USER_AGENT = 'user_agent'
# RESPONSE_CODE = 'response_code'
# IP_ADDRESS = 'ip_address'
TIME_STAMP = 'TimeStamp'
HTTP_METHOD = 'Method'
INVOKE_PATH = 'URL'
USER_AGENT = 'User-agent'
RESPONSE_CODE = 'Response Code'
IP_ADDRESS = 'client-ip'

to_dir = 'inputs/'
all_files = 'DDOS.csv'


def clean_dir(path_to_dir):
    for filenames in os.listdir(path_to_dir):
        file_path = os.path.join(path_to_dir, filenames)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def rm_millisec(f_path):
    """removing milliseconds from time stamp"""
    opsd_daily = pd.read_csv(f_path)
    VAL = opsd_daily[TIME_STAMP]

    for i in range(len(opsd_daily)):
        # encode date and time to timestamp value
        input_ = VAL[i]
        # print(datetime.datetime.strptime(VAL[i], '%Y-%m-%d %H:%M:%S.%f').replace(microsecond=0))
        # slice_object = slice(19)
        # time = input_[slice_object]
        # dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        opsd_daily.at[i, TIME_STAMP] = datetime.datetime.strptime(VAL[i], '%Y-%m-%d %H:%M:%S.%f').replace(microsecond=0)
        opsd_daily.to_csv(f_path, index=False)
# datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').replace(microsecond=0)

def rm_duplicates(f_path):
    df = pd.read_csv(f_path)
    df.drop_duplicates(subset=TIME_STAMP, keep="first", inplace=True)
    df.to_csv(f_path, index=False)


def setIndex(f_path):
    df = pd.read_csv(f_path)
    min_index = min(df[TIME_STAMP])
    max_index = datetime.datetime.strptime(min_index, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)
    df[TIME_STAMP] = pd.to_datetime(df[TIME_STAMP])
    # fill missing with NaN values by incrementing seconds one by one
    df = df.set_index(TIME_STAMP).reindex(pd.date_range(min_index, max_index, freq='S').fillna())
    # name the new index column(time stamp column)
    df.index.names = [TIME_STAMP]
    df.to_csv(f_path)


count = 0

df = pd.read_csv(all_files)
# group by ip address
by_state = df.groupby(IP_ADDRESS)

# taking all ip address to name list
name = df[IP_ADDRESS]

# # take one by one grouped ips
# for state, frame in by_state:
#     df = pd.DataFrame(frame)
#     # IP, token and other non changing columns removed[Selected timestamp - 1hr](After
#     # 1hr token may be a different one if not time extended)
#     header = [TIME_STAMP, IP_ADDRESS, HTTP_METHOD, INVOKE_PATH, USER_AGENT, RESPONSE_CODE]
#     df.to_csv('inputs/%s.csv' % frame.iloc[0][IP_ADDRESS], columns=header, index=False)
#     count = count + 1
# print("Unique ip count :", count)
#
# for j in os.listdir(to_dir):
#     # open all csv files in the given directory
#     if j.endswith('.csv'):
#         f_path = to_dir + j
#         rm_millisec(f_path)
#         rm_duplicates(f_path)
#         setIndex(f_path)
#         encode(f_path)

# use thin clean method later
# clean_dir(to_dir)
