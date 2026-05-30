#coding:utf-8
import os

path = "G:\\Github\\CTF-Note\\tools\\批量修改文件名后缀\\test"

for i in os.listdir(path):
    # print(i)
    if i == 'flag.zip':
        continue
    else:
        old_name = os.path.join(path,i)
        new_name = os.path.join(path,i + '.jpg')
        os.rename(old_name,new_name)