with open("./cipher.txt","r") as f:
    data = f.read()
    for i in range(0,len(data),8):
        # print(data[i:i+8])
        print(chr(int(data[i:i+8],2)),end="")