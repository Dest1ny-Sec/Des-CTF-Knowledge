from collections import Counter
f = open('./out.txt','r')
f_read = f.read()
print(Counter(f_read))