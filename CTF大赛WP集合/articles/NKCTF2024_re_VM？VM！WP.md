# NKCTF2024 re VM？VM！WP

> 原文: https://www.ctfiot.com/197341.html
> ID: 197341

NKCTF2024 re VM？VM！WP

这个函数是把输入的字符转化为二进制并倒序存储

sub_1570太大而加载不出来，这里是加密的主逻辑，目的是需要输出1

通过删除栈的方法强行转化伪代码

实际上是一个2324*2324的像素图

在上面进行染色

cable management | /den/face0xff/writeups

(https://ctf.0xff.re/2022/dicectf_2022/cable_management)【游戏框架系列】Wireworld元胞自动机

(https://zhuanlan.zhihu.com/p/25593938)

根据资料知道，是在模拟Wireworld元胞自动机

组成：

空

导体

电子头

电子尾

每代变化：

空→空

电子头→电子尾

电子尾→导体

当仅有一个或仅有两个电子头的邻居是导体时，导体→电子头

1就是终点，到达就返回1

由此根据数据绘图分析，这实际上是利用wireworld高度抽象的虚拟机

数据量太大，这里用脚本提取

#data_extractimport idaapi  import idautils    # 设置你要读取数据的起始和结束地址  START_ADDR = 0x4018  # 替换为你的起始地址  END_ADDR = 0x535D93  # 替换为你的结束地址  BYTES_PER_LINE = 16  # 每行显示的字节数    # 打开一个文件用于写入，如果文件不存在则创建它  with open('output.txt', 'w') as f:      # 用于记录当前行已经写入了多少字节      bytes_written = 0      # 遍历指定地址范围内的每个地址      for ea in range(START_ADDR, END_ADDR + 1):          # 读取当前地址的一个字节          byte_value = idaapi.get_byte(ea)          # 将字节转换为十六进制字符串          hex_string = '0x{:
02X}'.format(byte_value)          # 写入文件，并在需要时添加逗号          if bytes_written > 0 and bytes_written % BYTES_PER_LINE != 0:              f.write(',')          f.write(hex_string)          bytes_written += 1          # 如果当前行已经写入了足够的字节数，则换行          if bytes_written % BYTES_PER_LINE == 0:              f.write(',n')    # 文件会在脚本执行完毕后自动关闭  print("Data has been written to output.txt")

from PIL import Images = [...]img = Image.new('RGB', (0x914, 0x914), (255, 255, 255))pixels = img.load()for i in range(len(s)):    if s[i] == 0x1:        i_row = i // 0x914        i_col = i % 0x914        #print("0x01_row:"+f"{i_row:X}" + "  0x01_col:"+f"{i_col:X}")        pixels[i_row, i_col] = (255, 0, 0)
    elif s[i] == 0xEC:        i_row = i // 0x914        i_col = i % 0x914        #print("0xEC_row:"+f"{i_row:X}" + "  0xEC_col:"+f"{i_col:X}")        pixels[i_row, i_col] = (0, 0, 255)
    elif s[i] == 0x11:        i_row = i // 0x914        i_col = i % 0x914        #print("0x11_row:"+f"{i_row:X}" + "  0x11_col:"+f"{i_col:X}"        pixels[i_row, i_col] = (0, 255, 0)
    elif s[i] == 0xCD:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (0, 0, 0)
    elif s[i] == 0x80:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (255, 255, 0)        elif s[i] == 0xEA:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (0, 255, 255)
img.save('D:\下载\CTF附件\nk\image.png')

Wireworld Simulator

(https://danprince.github.io/wireworld/)

信号就会消失

所以这其实是在模拟异或（逻辑门），原理是在这里

箭头所指的导线周围有三个电子头，但我们的规则是当仅有一个或仅有两个电子头的邻居是导体时，导体→电子头

因此就达到了异或的效果

图中除了大量的异或，还有别的图形

这个则是一个二极管，像神经突触一样，只会从“突触前模”向“突触后膜”单向传导

我们可以根据这些特征把整个图分割开，由于每个输入的字符都转化为8位二进制注入（绿色就是注入点），所以我每八个循环分割一次，最后得到29块，对应29个输入的字符

可以看到，蓝色电子头总是在循环结构相同的位置上，代表着这个位置上电信号的1和0，将他们连接在一起就相当于组成了一个由0、1组成的key（可以脚本取key，我嫌麻烦就直接手敲吧）

我们要求的flag是上面一排注入点的0/1状态，加密过程就是我之前说的一系列异或，我们期望得到的结果就是全0

由此我们可以写出解密的函数，将key与全0序列异或逆序转化成字符串

def decode(key):    key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))    #print(key_string)    res = [0]    for i in range(len(key)-1):        tmp = res[i]^key[i]        res.append(tmp)    #print(res)    flag = long_to_bytes(int("".join([str(i) for i in res]), 2))    print(flag)

#VM?VM!from Crypto.Util.number import long_to_byteskey0 = [1, 0, 1, 1, 0, 0, 1, 0]
key1 = [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1,1, 0, 0, 1, 1, 1, 0, 0,1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1]
key2 = [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0]
key3 = [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0]def decode(key):    key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))    #print(key_string)    res = [0]    for i in range(len(key)-1):        tmp = res[i]^key[i]        res.append(tmp)    #print(res)    flag = long_to_bytes(int("".join([str(i) for i in res]), 2))    print(flag)decode(key0)decode(key1)decode(key2)decode(key3)


```
    #data_extractimport idaapi  import idautils    # 设置你要读取数据的起始和结束地址  START_ADDR = 0x4018  # 替换为你的起始地址  END_ADDR = 0x535D93  # 替换为你的结束地址  BYTES_PER_LINE = 16  # 每行显示的字节数    # 打开一个文件用于写入，如果文件不存在则创建它  with open('output.txt', 'w') as f:      # 用于记录当前行已经写入了多少字节      bytes_written = 0      # 遍历指定地址范围内的每个地址      for ea in range(START_ADDR, END_ADDR + 1):          # 读取当前地址的一个字节          byte_value = idaapi.get_byte(ea)          # 将字节转换为十六进制字符串          hex_string = '0x{:
02X}'.format(byte_value)          # 写入文件，并在需要时添加逗号          if bytes_written > 0 and bytes_written % BYTES_PER_LINE != 0:              f.write(',')          f.write(hex_string)          bytes_written += 1          # 如果当前行已经写入了足够的字节数，则换行          if bytes_written % BYTES_PER_LINE == 0:              f.write(',n')    # 文件会在脚本执行完毕后自动关闭  print("Data has been written to output.txt")
from PIL import Images = [...]img = Image.new('RGB', (0x914, 0x914), (255, 255, 255))pixels = img.load()for i in range(len(s)):    if s[i] == 0x1:        i_row = i // 0x914        i_col = i % 0x914        #print("0x01_row:"+f"{i_row:X}" + "  0x01_col:"+f"{i_col:X}")        pixels[i_row, i_col] = (255, 0, 0)
    elif s[i] == 0xEC:        i_row = i // 0x914        i_col = i % 0x914        #print("0xEC_row:"+f"{i_row:X}" + "  0xEC_col:"+f"{i_col:X}")        pixels[i_row, i_col] = (0, 0, 255)
    elif s[i] == 0x11:        i_row = i // 0x914        i_col = i % 0x914        #print("0x11_row:"+f"{i_row:X}" + "  0x11_col:"+f"{i_col:X}"        pixels[i_row, i_col] = (0, 255, 0)
    elif s[i] == 0xCD:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (0, 0, 0)
    elif s[i] == 0x80:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (255, 255, 0)        elif s[i] == 0xEA:        i_row = i // 0x914        i_col = i % 0x914        #print("0xCD:"+f"{i:X}")        pixels[i_row, i_col] = (0, 255, 255)
img.save('D:\下载\CTF附件\nk\image.png')
def decode(key):    key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))    #print(key_string)    res = [0]    for i in range(len(key)-1):        tmp = res[i]^key[i]        res.append(tmp)    #print(res)    flag = long_to_bytes(int("".join([str(i) for i in res]), 2))    print(flag)
#VM?VM!from Crypto.Util.number import long_to_byteskey0 = [1, 0, 1, 1, 0, 0, 1, 0]
key1 = [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1,1, 0, 0, 1, 1, 1, 0, 0,1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1]
key2 = [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0]
key3 = [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0]def decode(key):    key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))    #print(key_string)    res = [0]    for i in range(len(key)-1):        tmp = res[i]^key[i]        res.append(tmp)    #print(res)    flag = long_to_bytes(int("".join([str(i) for i in res]), 2))    print(flag)decode(key0)decode(key1)decode(key2)decode(key3)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1722752501.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722752501.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722752502.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1722752503.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722752504.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1722752504.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1722752505.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1722752506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722752506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1722752507.png)