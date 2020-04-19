import numpy as np
import pandas as pd
import glob

path = 'inputs'
all_files = glob.glob(path + "/*.csv")

li = []

df = pd.concat((pd.read_csv(f) for f in all_files))
df.to_csv("input.csv", index=False)

a3d = np.array(list(df.groupby('ip_address').apply(pd.DataFrame.as_matrix)))
print(a3d)
print(a3d.shape)