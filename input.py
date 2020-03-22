import pandas as pd

df = pd.read_csv("t1.csv")

# group by ip address
by_state = df.groupby("ip_address")

count = 0
# taking all ip address to name list
name = df['ip_address']

# take one by one grouped ips
for state, frame in by_state:
    df = pd.DataFrame(frame)
    # IP, token and other non changing columns removed[Selected timestamp - 1hr](After
    # 1hr token may be different)
    header = ["timestamp", "http_method", "invoke_path", "user_agent", "response_code"]
    df.to_csv('inputs/%s.csv' % frame.iloc[0]['ip_address'], columns=header, index=False)
    count = count + 1
print("Unique ip count :", count)
