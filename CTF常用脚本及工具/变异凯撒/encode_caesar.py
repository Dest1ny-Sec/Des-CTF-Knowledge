flag = "joch{NBR/HN`)EJJkA6X!<BPc:.B_d"
move = 4

c = ""
for i in flag:
    c += chr(ord(i)+ move)
    move = move-1

print(c)