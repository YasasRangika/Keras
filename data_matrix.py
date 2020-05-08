import numpy as np
import pandas as pd
import os
import random
from pathlib import Path

IP_ADDRESS = 'ip_address'
# IP_ADDRESS = 'client-ip'
DIR = 'out'
SIZE = 1000


def get_random_files():
    file_list = list(Path(DIR).glob('**/*.csv'))
    if not len(file_list):
        return "No files matched that extension"
    rand = random.randint(0, len(file_list) - 1)
    return file_list[rand]


arr = np.empty([SIZE, 3])
df = pd.DataFrame()
for j in range(SIZE):
    file = get_random_files()
    if os.path.dirname(file) == "out/normal":
        arr[j][0] = 1
        arr[j][1] = 0
        arr[j][2] = 0
    elif os.path.dirname(file) == "out/DOS":
        arr[j][0] = 0
        arr[j][1] = 1
        arr[j][2] = 0
    elif os.path.dirname(file) == "out/abnormal_token":
        arr[j][0] = 0
        arr[j][1] = 0
        arr[j][2] = 1
    f = pd.read_csv(file)
    f = f.iloc[:-1]
    df = df.append(f)
    os.remove(file)

df.to_csv("x_dataset.csv", index=False)
a3d = np.array(list(df.groupby(IP_ADDRESS, sort=False).apply(pd.DataFrame.as_matrix)))

# np.savetxt('y_dataset.txt', arr)
with open('n_folded/x_train_1.csv', 'w') as outfile:
    for data_slice in a3d:
        np.savetxt(outfile, data_slice, fmt='%-20.18f')

# new_data = np.loadtxt('n_folded/x_train_1.csv')
# x_train = new_data.reshape((SIZE, 3600, 6))
# print(x_train)
# print(x_train.shape)

# y_train = np.loadtxt('y_dataset.txt')
# print(y_train)
# print(y_train.shape)



