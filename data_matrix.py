import numpy as np
import pandas as pd
import os
import random
from pathlib import Path

IP_ADDRESS = 'ip_address'
# IP_ADDRESS = 'client-ip'
DIR = 'out'
SIZE = 200


def get_random_files():
    file_list = list(Path(DIR).glob('**/*.csv'))
    if not len(file_list):
        return "No files matched that extension"
    rand = random.randint(0, len(file_list) - 1)
    return file_list[rand]


arr = np.empty([SIZE, 2])
df = pd.DataFrame()
for j in range(SIZE):
    file = get_random_files()
    if os.path.dirname(file) == "out/Norm":
        arr[j][0] = 1
        arr[j][1] = 0
    elif os.path.dirname(file) == "out/DOS":
        arr[j][0] = 0
        arr[j][1] = 1
    f = pd.read_csv(file)
    f = f.iloc[:-1]
    df = df.append(f)
    os.remove(file)
df.to_csv("test.csv", index=False)
a3d = np.array(list(df.groupby(IP_ADDRESS, sort=False).apply(pd.DataFrame.as_matrix)))

np.savetxt('y_test.txt', arr)
with open('x_test.txt', 'w') as outfile:
    for data_slice in a3d:
        np.savetxt(outfile, data_slice, fmt='%-20.18f')

new_data = np.loadtxt('x_test.txt')
x_test = new_data.reshape((SIZE, 3600, 5))
print(x_test)
print(x_test.shape)

y_test = np.loadtxt('y_test.txt')
print(y_test)
print(y_test.shape)



