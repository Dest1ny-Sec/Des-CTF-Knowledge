# 天山固网-2025网络安全技能竞赛-WriteUp

> 原文: https://www.ctfiot.com/267054.html
> ID: 267054

天山固网-2025网络安全技能竞赛-WriteUp

MISC

Children of the stream

疑似比赛偷偷塞入脑洞题

下载附件以后是一个流量包然后可以看到有一个rar压缩包把rar压缩包保存下来之后发现需要解压密码

当我们导出全部文件可以看到一个图片，并且在他的详情页中找到描述然后看下图片的属性可以看到有描述I’ve heard of Dvorak

根据提示我们联想到Dvorak键盘，接下来我们就需要去找压缩包密码看到这个流量我们追踪一下，然后可以看到有一大串的英文字符，这个就是脑洞的地方，就是要按照大小写转换成0和1然后再转换成二维码先用这个脚本转换成0和1然后统计一下字符长度开个根号就是图片的大小

然后大概就是42我们再使用0和1转换成二维码的脚本就可以得到二维码了

扫描二维码

text =""""""
# 转换大小写为 0/1
result = []
for ch in text:
    if ch.isupper():
        result.append("1")
    elif ch.islower():
        result.append("0")
    # else:
    #     result.append(ch)  # 空格或其他符号保持不变

binary_str = "".join(result)
print(binary_str)

# 转换为二维码图片
from PIL import Image
MAX = 42
pic = Image.new("RGB",(MAX, MAX))
str = ""
i=0
for y in range (0,MAX):
    for x in range (0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0, 0, 0))
        else:
            pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("flag.png")

得到这个字符串以后我们可以试一下：ssdsahjkhsdfhhkjjhksdfjhds

发现并不是压缩包的解压密码

然后我们之前不是看到 Dvorak键盘么然后我们在网上找一下这个键盘的在线解密

得到的这个就是解压密码：ooeoadhtdoeuddthhdtoeuhdeo

flag：DASCTF{jhughudshhjg_qiwjains_jsmka}

Crypto

shuffle secret

看这个题目描述得知可能会考察随机数

然后我们可以看到题目给出的代码

这个random.seed(0) 固定了随机数种子

这样 random.shuffle(secret) 的结果是确定性的（固定输入 → 固定输出）。

然后我们就使用它这个代码生成2000组数字，可以得到原来的素因子得到p然后我们就可以做rsa了

生成2000组数字的代码就在原来的代码上进行修改一下就可以

import random
from Crypto.Util.number import *
import secrets

def shuffle_secret(secret):
    random.seed(0)
    secret = list(secret)
    random.shuffle(secret)
    return''.join(secret)

def myPrime():
    whileTrue:
        if isPrime(p := random.getrandbits(64)):
            return p

def get_factors():
    factors = [myPrime() for _ in range(2000)]
    return factors

if __name__ == '__main__':
    secret = 'rCr3h0s1ry_t__s4pB_teg_yipF__dnMyFF'
    shuffle_secret_val = shuffle_secret(secret)
    print(f"{shuffle_secret_val=}")

    factors = get_factors()
    print(f"{len(factors)=}")
    print(f"{factors=}")

生成以后我们就用下面的脚本可以跑出p(Pollard’s p-1 分解法)

import gmpy2
import random
from Crypto.Util.number import *
n =
e =65537
c =
t = pow(2,1024)
k = 2
x = 
for i in range(len(x)):
    k = pow(k,x[i],n)
    if k>t:
        if i%15 ==0:
            g = gmpy2.gcd(k-1,n)
            if g!=1:
                print("因子:",g)
                break

然后就做rsa就可以了

flag：DASCTF{Dont_be_LazY_try_hard_to_le4rn_Crypt0gr4phy}

X0r_Mast3r

看一下题目给的附件，然后我们可以看到gift生成是异或了一下然后我们就想到了剪枝

附件里面有一个publickey文件然后我们使用tools.qsnctf.com解析一下

def pq_high_xor(p="", q=""):
    lp, lq = len(p), len(q)
    tp0 = int(p + (512-lp) * "0", 2)
    tq0 = int(q + (512-lq) * "0", 2)
    tp1 = int(p + (512-lp) * "1", 2)
    tq1 = int(q + (512-lq) * "1", 2)

    if tp0 * tq0 > n or tp1 * tq1 < n:
        return
    if lp == leak_bits:
        pq.append(tp0)
        return

    if xor[lp] == "1":
        pq_high_xor(p + "0", q + "1")
        pq_high_xor(p + "1", q + "0")
    else:
        pq_high_xor(p + "0", q + "0")
        pq_high_xor(p + "1", q + "1")

def pq_low_xor(p="", q=""):
    lp, lq = len(p), len(q)
    tp = int(p, 2) if p else0
    tq = int(q, 2) if q else0

    if tp * tq % 2**lp != n % 2**lp:
        return
    if lp == leak_bits:
        pq.append(tp)
        return

    if xor[-lp-1] == "1":
        pq_low_xor("0" + p, "1" + q)
        pq_low_xor("1" + p, "0" + q)
    else:
        pq_low_xor("0" + p, "0" + q)
        pq_low_xor("1" + p, "1" + q)
#for i in range(200,300):
leak = leak << 215
leak_bits = 512-215
xor = bin(leak)[2:].zfill(512)
pq = []

pq_high_xor()
# print(pq)

for p_high in pq:
    x = PolynomialRing(Zmod(n), 'x').gen()
    f = p_high + x
    res = f.monic().small_roots(X=2**215, beta=0.44,epsilon=1/16)
    if res:
        p = int(p_high+res[0])
        print(p)

得到p和q以后就是rsa了

from Crypto.Util.number import *
p=12849041580187712114287340210939396034424272221812148338878681353480052959626982507824137597050709378850940287288828758690514971324264679315212899800699649
q=12873211897459556383148381598553582828419349814854356501114717109080249055667413399225499444590500163395293435005743026518120878091777335879008061804074573
n=16540843494102499415836904244978840191029498840763686795549650936067514623
3043101006492521091959823423540542967459193522177826921732843078657511418718
2770689749905170745519843062613652139329837516178725502388350154295296315239
7382307164081785688671310884502037288325565062878881953233601744472220994437
0924877
e=65537
c = 32514400111560285767114059428272978369671794111207540192987911899965917441745193707727404259848540711110916899114259203696404123229134392494554874352785281551973075869313034289563994886386821257391009141162559968535288461313309953574507706583653092150741608080020850440840533409996254003612114636139855553078
m=pow(c,inverse(e,(p-1)*(q-1)),n)
print(long_to_bytes(m))

REVERSE

AndroidDemo

拿到题目先反编译一下，在Java_com_example_androiddemo_MainActivity_check这个函数里面有关键比较得到key然后分析一下发现是aes加密的ecb模式解密一下就可以了

You say i do

拖入ida后直接开启动调发现需要输入50长度的字符串

输入DASCTF{123456789ABCDEFHIGKLMN987654321qwertyuiopl}

这里去看eax，发现是从25的位置上的字符K开始cmp的，如果对比一致就接着往下对比

看[rsp+0C8h+var_24]，0x5F也就是_，所以我们直接从内存拿剩下部分就行，可以拿到后半段flag：_@nd_s33k_15_interesting}

然后接着看

观察他取代码的方式，通过获取我前面flag的输入字符，加上edx(i<<8)，整体再左移3+全局变量ptr，赋给rdx，进行call，通过前几个字符串DASCTF观察，rdx通常被赋0xB0 0x?? 0x30, 0xE0, 0xC3(xor)，所以我们直接去遍历ptr，按上面的算法反推就可拿到前半段flag

import idaapi
import idc

def find_pattern_and_decode(start_addr):
    pattern = [0x30, 0xE0, 0xC3]
    seg = idaapi.getseg(start_addr)
    ifnot seg:
        print("无法获取段信息")
        return
    end_addr = seg.end_ea
    print(f"搜索范围: 0x{start_addr:X} - 0x{end_addr:X}")
    current_addr = start_addr
    found_count = 0
    result_chars = []
    while current_addr < end_addr - 2:
        if (idc.get_wide_byte(current_addr) == 0x30and
            idc.get_wide_byte(current_addr + 1) == 0xE0and
            idc.get_wide_byte(current_addr + 2) == 0xC3):
            print(f"找到模式 30 E0 C3 在地址: 0x{current_addr:X}")
            found_count += 1
            # 向上搜索 0xB0
            search_addr = current_addr
            found_b0 = False

            for i in range(12):
                search_addr -= 1
                if search_addr < start_addr:
                    break
                if idc.get_wide_byte(search_addr) == 0xB0:
                    # 计算偏移
                    offset = search_addr - start_addr
                    print(f" 偏移: 0x{offset:X} ({offset})")
                    # 右移3位并 & 0xFF
                    result = (offset >> 3) & 0xFF
                    print(f" 右移3位后: 0x{result:X} ({result})")
                    if32 <= result <= 126:
                        char = chr(result)
                        print(f" 字符: '{char}'")
                        result_chars.append(char)
                    found_b0 = True
                    break
            ifnot found_b0:
                print(f" 未找到对应的 0xB0")
        current_addr += 1
    if result_chars:
        print(f"flag: {''.join(result_chars)}")
    else:
        print("未解码出任何字符")

def main():

    start_address = 0x000055555558DAC0
    print(f"起始地址: 0x{start_address:X}")
    find_pattern_and_decode(start_address)

if __name__ == "__main__":
    main()

flag: DASCTF{l1s7en_7o_Me__Hide

然后拼起来

DASCTF{l1s7en_7o_Me__Hide_@nd_s33k_15_interesting}


```
text =""""""
# 转换大小写为 0/1
result = []
for ch in text:
    if ch.isupper():
        result.append("1")
    elif ch.islower():
        result.append("0")
    # else:
    #     result.append(ch)  # 空格或其他符号保持不变

binary_str = "".join(result)
print(binary_str)
# 转换为二维码图片
from PIL import Image
MAX = 42
pic = Image.new("RGB",(MAX, MAX))
str = ""
i=0
for y in range (0,MAX):
    for x in range (0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0, 0, 0))
        else:
            pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("flag.png")
import random
from Crypto.Util.number import *
import secrets

def shuffle_secret(secret):
    random.seed(0)
    secret = list(secret)
    random.shuffle(secret)
    return''.join(secret)

def myPrime():
    whileTrue:
        if isPrime(p := random.getrandbits(64)):
            return p

def get_factors():
    factors = [myPrime() for _ in range(2000)]
    return factors

if __name__ == '__main__':
    secret = 'rCr3h0s1ry_t__s4pB_teg_yipF__dnMyFF'
    shuffle_secret_val = shuffle_secret(secret)
    print(f"{shuffle_secret_val=}")

    factors = get_factors()
    print(f"{len(factors)=}")
    print(f"{factors=}")
import gmpy2
import random
from Crypto.Util.number import *
n =
e =65537
c =
t = pow(2,1024)
k = 2
x = 
for i in range(len(x)):
    k = pow(k,x[i],n)
    if k>t:
        if i%15 ==0:
            g = gmpy2.gcd(k-1,n)
            if g!=1:
                print("因子:",g)
                break
def pq_high_xor(p="", q=""):
    lp, lq = len(p), len(q)
    tp0 = int(p + (512-lp) * "0", 2)
    tq0 = int(q + (512-lq) * "0", 2)
    tp1 = int(p + (512-lp) * "1", 2)
    tq1 = int(q + (512-lq) * "1", 2)

    if tp0 * tq0 > n or tp1 * tq1 < n:
        return
    if lp == leak_bits:
        pq.append(tp0)
        return

    if xor[lp] == "1":
        pq_high_xor(p + "0", q + "1")
        pq_high_xor(p + "1", q + "0")
    else:
        pq_high_xor(p + "0", q + "0")
        pq_high_xor(p + "1", q + "1")

def pq_low_xor(p="", q=""):
    lp, lq = len(p), len(q)
    tp = int(p, 2) if p else0
    tq = int(q, 2) if q else0

    if tp * tq % 2**lp != n % 2**lp:
        return
    if lp == leak_bits:
        pq.append(tp)
        return

    if xor[-lp-1] == "1":
        pq_low_xor("0" + p, "1" + q)
        pq_low_xor("1" + p, "0" + q)
    else:
        pq_low_xor("0" + p, "0" + q)
        pq_low_xor("1" + p, "1" + q)
    #for i in range(200,300):
leak = leak << 215
leak_bits = 512-215
xor = bin(leak)[2:].zfill(512)
pq = []

pq_high_xor()
# print(pq)

for p_high in pq:
    x = PolynomialRing(Zmod(n), 'x').gen()
    f = p_high + x
    res = f.monic().small_roots(X=2**215, beta=0.44,epsilon=1/16)
    if res:
        p = int(p_high+res[0])
        print(p)
from Crypto.Util.number import *
p=12849041580187712114287340210939396034424272221812148338878681353480052959626982507824137597050709378850940287288828758690514971324264679315212899800699649
q=12873211897459556383148381598553582828419349814854356501114717109080249055667413399225499444590500163395293435005743026518120878091777335879008061804074573
n=16540843494102499415836904244978840191029498840763686795549650936067514623
3043101006492521091959823423540542967459193522177826921732843078657511418718
2770689749905170745519843062613652139329837516178725502388350154295296315239
7382307164081785688671310884502037288325565062878881953233601744472220994437
0924877
e=65537
c = 32514400111560285767114059428272978369671794111207540192987911899965917441745193707727404259848540711110916899114259203696404123229134392494554874352785281551973075869313034289563994886386821257391009141162559968535288461313309953574507706583653092150741608080020850440840533409996254003612114636139855553078
m=pow(c,inverse(e,(p-1)*(q-1)),n)
print(long_to_bytes(m))
import idaapi
import idc

def find_pattern_and_decode(start_addr):
    pattern = [0x30, 0xE0, 0xC3]
    seg = idaapi.getseg(start_addr)
    ifnot seg:
        print("无法获取段信息")
        return
    end_addr = seg.end_ea
    print(f"搜索范围: 0x{start_addr:X} - 0x{end_addr:X}")
    current_addr = start_addr
    found_count = 0
    result_chars = []
    while current_addr < end_addr - 2:
        if (idc.get_wide_byte(current_addr) == 0x30and
            idc.get_wide_byte(current_addr + 1) == 0xE0and
            idc.get_wide_byte(current_addr + 2) == 0xC3):
            print(f"找到模式 30 E0 C3 在地址: 0x{current_addr:X}")
            found_count += 1
            # 向上搜索 0xB0
            search_addr = current_addr
            found_b0 = False

            for i in range(12):
                search_addr -= 1
                if search_addr < start_addr:
                    break
                if idc.get_wide_byte(search_addr) == 0xB0:
                    # 计算偏移
                    offset = search_addr - start_addr
                    print(f" 偏移: 0x{offset:X} ({offset})")
                    # 右移3位并 & 0xFF
                    result = (offset >> 3) & 0xFF
                    print(f" 右移3位后: 0x{result:X} ({result})")
                    if32 <= result <= 126:
                        char = chr(result)
                        print(f" 字符: '{char}'")
                        result_chars.append(char)
                    found_b0 = True
                    break
            ifnot found_b0:
                print(f" 未找到对应的 0xB0")
        current_addr += 1
    if result_chars:
        print(f"flag: {''.join(result_chars)}")
    else:
        print("未解码出任何字符")

def main():

    start_address = 0x000055555558DAC0
    print(f"起始地址: 0x{start_address:X}")
    find_pattern_and_decode(start_address)

if __name__ == "__main__":
    main()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342177-wxsync-2025-08-2023e1a41d2fa3e43a94125a4bc27db8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342179-wxsync-2025-08-8f37624ea3cb74b8186999d479bd26db.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342180-wxsync-2025-08-e0b55014b2e78b82b87bd96e04a8eda9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342183-wxsync-2025-08-554620bce15c0adf0721fb08d2d577d4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342184-wxsync-2025-08-8fdc9484c92876f079c540ec89701105.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342186-wxsync-2025-08-31fab57727ed44efbcc3b5738f65d0a5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342188-wxsync-2025-08-c6a29cab98cdcd66ca518349899f5b19.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342189-wxsync-2025-08-c1dc3f4736c3c77ae37d3c466c06fc95.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342191-wxsync-2025-08-f995c8c6461c4af90ab665f6fa2921b0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342193-wxsync-2025-08-d6f3dd541fbfcc3529aedeb9e67d8f1e.png)