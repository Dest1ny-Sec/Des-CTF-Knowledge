tmp = ''
with open('attachment.txt','r') as f:
    for i in f.readlines():
        if len(i.strip('\n')) == 6:
            tmp += '0'
        else:
            tmp += '1'
print(tmp)