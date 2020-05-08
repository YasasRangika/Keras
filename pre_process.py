import datetime
import glob
import os
import shutil
import pandas as pd
from encode_input import encode

to_dir = 'inputs/'
path = '/home/yasas/Documents/research/datasets/1K'
all_files = glob.glob(path + "/*.csv")


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
    VAL = opsd_daily['timestamp']

    for i in range(len(opsd_daily)):
        # encode date and time to timestamp value
        input_ = VAL[i]
        slice_object = slice(19)
        time = input_[slice_object]
        dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        opsd_daily.at[i, "timestamp"] = dt
        opsd_daily.to_csv(f_path, index=False)


def rm_duplicates(f_path):
    df = pd.read_csv(f_path)
    df.drop_duplicates(subset="timestamp", keep="first", inplace=True)
    df.to_csv(f_path, index=False)


def setIndex(f_path):
    df = pd.read_csv(f_path)
    min_index = min(df['timestamp'])
    max_index = datetime.datetime.strptime(min_index, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # fill missing with NaN values by incrementing seconds one by one
    df = df.set_index('timestamp').reindex(pd.date_range(min_index, max_index, freq='S').fillna())
    # name the new index column(time stamp column)
    df.index.names = ['timestamp']
    df.to_csv(f_path)


count = 0
for filename in all_files:
    df = pd.read_csv(filename)
    # group by ip address
    by_state = df.groupby("ip_address")

    # taking all ip address to name list
    name = df['ip_address']

    # take one by one grouped ips
    for state, frame in by_state:
        df = pd.DataFrame(frame)
        # IP, token and other non changing columns removed[Selected timestamp - 1hr](After
        # 1hr token may be a different one if not time extended)
        header = ["timestamp", "ip_address", "access_token", "http_method", "invoke_path", "user_agent", "response_code"]
        df.to_csv(to_dir+'%s.csv' % frame.iloc[0]['ip_address'], columns=header, index=False)
        count = count + 1
print("Unique ip count :", count)

for j in os.listdir(to_dir):
    # open all csv files in the given directory
    if j.endswith('.csv'):
        f_path = to_dir + j
        rm_millisec(f_path)
        rm_duplicates(f_path)
        setIndex(f_path)
        encode(f_path)

# use thin clean method later
# clean_dir(to_dir)
