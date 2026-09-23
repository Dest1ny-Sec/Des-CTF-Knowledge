import zipfile
lis = []
result = ""
data = ""
size = 1
with zipfile.ZipFile('love.zip', 'r') as zipobj: #读取压缩包
    for file_name in zipobj.namelist(): #遍历名称
        info = zipobj.getinfo(file_name)
        file_name = file_name.encode('cp437').decode('gbk')
        lis.append([file_name,info.file_size])
# print(lis)
del lis[0]
for i in range(len(lis)): #处理文件名和数据
    lis[i][0] = lis[i][0].replace("out/","")
    lis[i][0] = lis[i][0].replace(".png", "")
    lis[i][0] = int(lis[i][0])
    if lis[i][1]==262: # 判断文件大小
        lis[i][1]='0'
    else:
        lis[i][1]='1'
# print(lis)
lis = sorted(lis)
# print(lis)
for i in range(len(lis)):
    data += lis[i][1] #数据大小
    if len(data)%8==0: #集齐八位二进制时
        result+=chr(int(data,2))
        data=""
with open("2.txt","w") as fp:
    fp.write(result)
