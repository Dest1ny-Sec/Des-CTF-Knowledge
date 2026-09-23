
s = "d4e8e1f4a0f7e1f3a0e6e1f3f4a1a0d4e8e5a0e6ece1e7a0e9f3baa0c4c4c3d4c6fbb9b2b2e1e2b9b9b7b4e1b4b7e3e4b3b2b2e3e6b4b3e2b5b0b6b1b0e6e1e5e1b5fd"

str_s = ''
str_get = []

for j in range(129): # 循环测试所有数减掉1-128得到的ASCII码
    str_16 = ''
    for i in range(len(s)):
        if i % 2 ==0:
            str_s = s[i] + s[i+1]
            str_16 += chr(int(str_s,16)-j) # 十六进制转十进制
    print(str_16)

