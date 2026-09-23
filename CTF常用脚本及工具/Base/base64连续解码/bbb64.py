import base64

with open('./flag.txt','r') as f:
    data = f.readlines()[0]
    # print(data)
while True:
    data = base64.b64decode(data)
    if '{' in data.decode('utf-8'):
        print(data)
        exit(0)