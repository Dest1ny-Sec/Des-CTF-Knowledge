# -*- coding: cp936 -*-
import base64

flag = 'Tr0y{Base64isF4n}' #flag
bin_str = ''.join([bin(ord(c)).replace('0b', '').zfill(8) for c in flag]) # 转为二进制并将0b去除 前面填充0符合8位
# print(bin_str)
base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

with open('0.txt', 'rb') as f0, open('1.txt', 'wb') as f1: #'0.txt'是明文, '1.txt'用于存放隐写后的 base64
    for line in f0.readlines():
        rowstr = base64.b64encode(line.replace('\n', '')) #编码后的字符串
        # print(rowstr)
        equalnum = rowstr.count('=') # 计算每行有多少个等号
        # print(equalnum)

        if equalnum and len(bin_str):
            offset = int('0b'+bin_str[:equalnum * 2], 2) # 将bin_str开头equalnum*2 个二进制转化为十进制整型  0b0101 => 5
            char = rowstr[len(rowstr) - equalnum - 1] # 输出等号前的字符
            # print(char)
            rowstr = rowstr.replace(char, base64chars[base64chars.index(char) + offset])
            print(base64chars[base64chars.index(char) + offset])
            bin_str = bin_str[equalnum*2:]

        f1.write(rowstr + '\n')