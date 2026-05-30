c = "joch{NBR/HN`)EJJkA6X!<BPc:.B_d"

for move in range(0,50):
    flag = ""
    for i in c:
        flag += chr(ord(i)- move)
        move = move -1

    print(flag)