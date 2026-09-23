s2 = ''
with open("key.txt",'r') as f:
    data = f.read()
    data = data[::-1]
    # print(data)
    for i in range(0,len(data),2):
        s1 = data[i:i+2]
        s2 += s1[::-1]
        # print(s2)
    with open("key1.txt",'w+') as f1:
        f1.write(s2)