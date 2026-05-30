content1 = ''
with open('1.txt','r') as f:
    content = f.read().split(' ')
    # print(content)
    for i in content:
        content1 += i.zfill(8) + '\n'
    # print(content1)

with open('2.txt','w+') as f:
    f.write(content1)