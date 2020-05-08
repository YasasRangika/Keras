import numpy as np
import pandas as pd

IP_ADDRESS = 'ip_address'
PATH = 'n_folded/n_folds/fold_6/'

df = pd.DataFrame()
f = pd.read_csv('x_chunks/chunk_1.csv')
df = df.append(f)
f = pd.read_csv('x_chunks/chunk_2.csv')
df = df.append(f)
f = pd.read_csv('x_chunks/chunk_3.csv')
df = df.append(f)
f = pd.read_csv('x_chunks/chunk_4.csv')
df = df.append(f)
f = pd.read_csv('x_chunks/chunk_5.csv')
df = df.append(f)

# df.to_csv("n_folded/x_train_1.csv", index=False)
a3d = np.array(list(df.groupby(IP_ADDRESS, sort=False).apply(pd.DataFrame.as_matrix)))
with open(PATH + 'x_train.txt', 'w') as outfile:
    for data_slice in a3d:
        np.savetxt(outfile, data_slice, fmt='%-20.18f')

new_data = np.loadtxt(PATH + 'x_train.txt')
x_train = new_data.reshape((800, 3600, 6))
print(x_train)
print(x_train.shape)


arr_1 = np.loadtxt('y_chunks/chunk_1.txt')
arr_2 = np.loadtxt('y_chunks/chunk_2.txt')
arr_3 = np.loadtxt('y_chunks/chunk_3.txt')
arr_4 = np.loadtxt('y_chunks/chunk_4.txt')
arr_5 = np.loadtxt('y_chunks/chunk_5.txt')
arr = np.concatenate((arr_1, arr_2))
arr = np.concatenate((arr, arr_3))
arr = np.concatenate((arr, arr_4))
arr = np.concatenate((arr, arr_5))
np.savetxt(PATH + 'y_train.txt', arr)

y_train = np.loadtxt(PATH + 'y_train.txt')
print(y_train)
print(y_train.shape)
