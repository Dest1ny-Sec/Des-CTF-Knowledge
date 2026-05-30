# Y老师的密码学 · 第一篇

> 原文: https://www.ctfiot.com/267088.html
> ID: 267088

我们新点击蓝字

关注我们

声明

本文作者：Generate

本文字数：3745字

阅读时长：约20分钟

附件/链接：无

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

整理了几个以前存的题目附件，依次对这些题目做了一个复现工作

记录一下这几个题目的做题思路

Y老师的密码学 · 第一篇

fizzbuzz100

题目

#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

whileTrue:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    ifnot out:
        out = pt
    print(out)

从脚本可以看出来这道题属于典型的”选择密文攻击”。想要实现”选择密文攻击”肯定是需要和远程环境实现交互的，然后我们可以构造任意的密文并且获得对应的明文，这也是选择密文攻击的主要思想:

通过选择密文攻击获得特定的明文

下面使用了lazzzaro博客中写到的构造思路：

通过这样的方式我们就可以通过我们构造的密文以及返回回来的数据来求解出我们想要的明文。

由于对解密过后的pt有限制不能被3整除也不能被5整除，我们可以直接写脚本一直传输各种我们所构造的ct，直到回显数字过来，然后手动解密一下即可

from Crypto.Util.number import *
from pwn import *
# a=remote("be.ax",31100)
# l=a.recv().split(b'=')
# print(l)
# while True:
#     X = getPrime(10)
#     c = int(l[3][:-2])
#     n = int(l[1][:-2])
#     Y = (c * (X ** 65537)) % n
#     a.sendline(str(Y).encode())
#     print(X)
#     print(Y)
#     print(a.recvline())
n=10923590886634228827134658466234332962160546970259806875947299955117094723
2996590557964241534101853321789427925631360625471407190264507981047481840604
5770295033165358752485494005614706506946041594393587695948197211669743677637
1201851439874292252155611926493174569162636187926889061627634316983399923186
1189833
c=54154300348903111005066683187322110240325256042602814495907789220256344603
9329651492217054936857491785316431371347695833366523065193277532980043371316
2219549684070989291489469384068884401333991713653240631955340521542862833755
5863105880457193242611315359206147315741465280238895273742546724024586290588
394695
w=907
y=26641182241400186140764833732531788410188640530460941989584702007887972922
0893088977366572306324954901383970069683822351533581707241548687145888017505
0739702872878490121501943582580854230668238851423909090028374384975663116055
0184102438364341973285800800919002105937122573558829974207210810107339187277
577768
ct=1617872921486161438959529626097492037660629295223293116750255222467849722125817349217082369174984216697864465452996697846569528891027592080706141175012700498085383500035413467709314885420625836615662777908956038879208002465859460678671983566645413919704836898065353721740490145081034
flag=ct*inverse(w,n)%n
print(long_to_bytes(flag))
#corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}

eyes

题目：

from Crypto.Util.number import bytes_to_long, getPrime

# my NEW and IMPROVED secret sharing scheme!! (now with multivariate quadratics)

with open('flag.txt', 'rb') as f:
    flag = f.read()

s = bytes_to_long(flag)
p = getPrime(len(bin(s)))
print(p)
F = GF(p)
N = 1024

conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])

A = random_matrix(F, N, N)

for i in range(0, N):
    for j in range(0, i):
        A[i, j] = 0
B = random_matrix(F, N, 1)
C = matrix(F, [F(s)])

fn = lambda x: (x.T * A * x + B.T * x + C)[0][0]

L = []
for i in range(7):
    L.append(fn(conv(i + 1)))

print(L)

这个题目看起来很复杂，其实实质很简单，通过观察conv矩阵可以发现可以将每一次计算出的L用A,B,C里面的元素表达出来，具体表达如下：

通过等式变形可以得到：c=(L[6]-(L[2]+L[4]+L[5]-2*(L[0]+L[1]+L[3]))-(L[0]+L[1]+L[3]))%p

我们便可以轻松求出flag了，当然这道题目也还有别的求解方法，大家可以自行去选择突破口。

from Crypto.Util.number import *
p=1873089703968291141600166892623234932796169766648225659075834963115683566265697596115468506218441065194050127470898727249982614285036691594726454694776985338487833409983284911305295748861807972501521427415609
L=[676465814304447223312460173335785175339355609820794166139539526721603814168727462048669021831468838980965201045011875121145342768742089543742283566458551844396184709048082643767027680757582782665648386615861, 1472349801957960100239689272370938102886275962984822725248081998254467608384820156734807260120564701715826694945455282899948399224421878450502219353392390325275413701941852603483746312758400819570786735148132, 202899433056324646894243296394578497549806047448163960638380135868871336000334692955799247243847240605199996942959637958157086977051654225700427599193002536157848015527462060033852150223217790081847181896018, 1065982806799890615990995824412253076607488063240855100580513221962298598002468338823225586171107539104635808108356492123167315175110515086192932230998426512947581115358738651206273178867911944034690138825583, 1676559204037482856674710667663849447914859348633288513196735253002541076530170853584406282605482862202276451646974549657672382936948091649764874334064431407644457518190694888175499630744741620199798070517691, 13296702617103868305327606065418801283865859601297413732594674163308176836719888973529318346255955107009306239107173490429718438658382402463122134690438425351000654335078321056270428073071958155536800755626, 1049859675181292817835885218912868452922769382959555558223657616187915018968273717037070599055754118224873924325840103339766227919051395742409319557746066672267640510787473574362058147262440814677327567134194]
F = GF(p)
N = 1024
conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])
c=(L[6]-(L[2]+L[4]+L[5]-2*(L[0]+L[1]+L[3]))-(L[0]+L[1]+L[3]))%p
print(long_to_bytes(c))
#corctf{mind your ones and zeroes because zero squared is zero and one squared is one}

cbc

题目：

import random

def random_alphastring(size):
    return"".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i+klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext
    
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

message = open("message.txt").read().upper()
message = "".join([char for char in message if char in alphabet])
flag = open("flag.txt").read()
flag = flag.lstrip("corctf{").rstrip("}")
message += flag
assert all([char in alphabet for char in message])

key = random_alphastring(bs)
iv, ct = cbc(key, pad(bs, message))
print(f"{iv = }")
print(f"{ct = }")

很有趣的一个题目，我们可以先用ct-iv这样可以获得pt+key，这一部分我主要是通过编写python代码进行求解的：

iv = 'RLNZXWHLULXRLTNP'
ct = 'ZQTJIHLVWMPBYIFRQBUBUESOOVCJHXXLXDKPBQCUXWGJDHJPQTHXFQIQMBXNVOIPJBRHJQOMBMNJSYCRAHQBPBSMMJWJKTPRAUYZVZTHKTPUAPGAIJPMZZZDZYGDTKFLWAQTSKASXNDRRQQDJVBREUXFULWGNSIINOYULFXLDNMGWWVSCEIORQESVPFNMWZKPIYMYVFHTSRDJWQBTWHCURSBPUKKPWIGXERMPXCHSZKYMFLPIAHKTXOROOJHUCSGINWYEILFIZUSNRVRBHVCJPVPSEGUSYOAMXKSUKSWSOJTYYCMEHEUNPJAYXXJWESEWNSCXBPCCIZNGOVFRTGKYHVSZYFNRDOVPNWEDDJYITHJUBVMWDNNNZCLIPOSFLNDDWYXMYVCEOHZSNDUXPIBKUJIJEYOETXWOJNFQAHQOVTRRXDCGHSYNDYMYWVGKCCYOBDTZZEQQEFGSPJJIAAWVDXFGPJKQJCZMTPMFZDVRMEGMPUEMOUVGJXXBRFCCCRVTUXYTTORMSQBLZUEHLYRNJAAIVCRFSHLLPOANFKGRWBYVSOBLCTDAUDVMMHYSYCDZTBXTDARWRTAFTCVSDRVEENLHOHWBOPYLMSDVOZRLENWEKGAWWCNLOKMKFWWAZJJPFDSVUJFCODFYIMZNZTMAFJHNLNMRMLQRTJJXJCLMQZMOFOGFPXBUTOBXUCWMORVUIIXELTVIYBLPEKKOXYUBNQONZLPMGWMGRZXNNJBUWBEFNVXUIAEGYKQSLYSDTGWODRMDBHKCJVWBNJFTNHEWGOZFEZMTRBLHCMHIFLDLORMVMOOHGXJQIIYHZFMROGUUOMXBTFMKERCTYXFIHVNFWWIUFTGLCKPJRFDRWDXIKLJJLNTWNQIOFWSIUQXMFFVIIUCDEDFEJNLKLQBALRKEYWSHESUJJXSHYWNRNPXCFUEFRJKSIGXHFTKNJXSYVITDOGYIKGJIOOHUFILWYRBTCQPRPNOKFKROTFZNOCZXZEYUNWJZDPJDGIZLWBBDGZJNRQRPFFGOTGFBACCRKLAPFLOGVYFXVIIJMBBMXWJGLPOQQHMNBCINRGZRBVSMLKOAFGYRUDOPCCULRBE'

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

import random

def random_alphastring(size):
    return"".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in
               zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def sub_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in
               zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i + klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext

def decode(key, ciphertext):
    klen = len(key)
    blocks = [ciphertext[i:i + klen] for i in range(0, len(ciphertext), klen)]
    plaintext = ""
    for block in blocks:
        block = sub_key(key, block)
        plaintext += block
    return plaintext

def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

blocks = [ct[i:i + bs] for i in range(0, len(ct), bs)]
ct_noiv = ""
prev_block = iv
for block in blocks:
    sblock = sub_key(prev_block, block)
    ct_noiv += sblock
    prev_block = block

print(ct_noiv)
#IDJUSTLIKETOINTERJECTFORAMOMENTWHATYOUREREFERINGTOASLINUXISINFACTGNULINUXORASIVERECENTLYTAKENTOCALLINGITGNUPLUSLINUXLINUXISNOTANOPERATINGSYSTEMUNTOITSELFBUTRATHERANOTHERFREECOMPONENTOFAFULLYFUNCTIONINGGNUSYSTEMMADEUSEFULBYTHEGNUCORELIBSSHELLUTILITIESANDVITALSYSTEMCOMPONENTSCOMPRISINGAFULLOSASDEFINEDBYPOSIXMANYCOMPUTERUSERSRUNAMODIFIEDVERSIONOFTHEGNUSYSTEMEVERYDAYWITHOUTREALIZINGITTHROUGHAPECULIARTURNOFEVENTSTHEVERSIONOFGNUWHICHISWIDELYUSEDTODAYISOFTENCALLEDLINUXANDMANYOFITSUSERSARENOTAWARETHATITISBASICALLYTHEGNUSYSTEMDEVELOPEDBYTHEGNUPROJECTTHEREREALLYISALINUXANDTHESEPEOPLEAREUSINGITBUTITISJUSTAPARTOFTHESYSTEMTHEYUSELINUXISTHEKERNELTHEPROGRAMINTHESYSTEMTHATALLOCATESTHEMACHINESRESOURCESTOTHEOTHERPROGRAMSTHATYOURUNTHEKERNELISANESSENTIALPARTOFANOPERATINGSYSTEMBUTUSELESSBYITSELFITCANONLYFUNCTIONINTHECONTEXTOFACOMPLETEOPERATINGSYSTEMLINUXISNORMALLYUSEDINCOMBINATIONWITHTHEGNUOPERATINGSYSTEMTHEWHOLESYSTEMISBASICALLYGNUWITHLINUXADDEDORGNULINUXALLTHESOCALLEDLINUXDISTRIBUTIONSAREREALLYDISTRIBUTIONSOFGNULINUXANYWAYHERECOMESTHEFLAGITSEVERYTHINGAFTERTHISATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS

由于key不知道，但是我们可以把pt+key当作维吉尼亚加密过后的密文，由于文本长度很长，直接使用在线工具对其分析就可以还原出flag：https://www.guballa.de/vigenere-solver。

从这道题目也可以看出来我们在做题的时候要灵活一点，一道题的求解不一定只用到一种思路，可能会用到很多东西，不要被限制住了思想。

#corctf{ATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS}

fizzbuzz101

题目：

#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

whileTrue:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    ifnot out:
        out = "101"
    print(out)

相对于100做了改进，不再返回解密后的数字过来，但是我们可以通过回显判断明文的低位，这时候我们可以想到LSB Oracle Attack。这道题我们只能确定明文是否是3，5或者是15的倍数，因为padding是随机的，我们先找到一个2*flag是5的倍数的padding，接下来我们需要找到一个k满足(k-1)*pt<n,k*pt>n。当<n时一定会返回Buzz或者是FizzBuzz，一旦大于n我们可以得到下面这个式子：

由于k*pt是5的倍数，而n不是5的倍数，所以返回的结果一定不是5的倍数，所以不会返回Buzz。由此我们可以获得这样一个信息：

得到了这样一个大概范围后我们使用二分法去不断逼近，可以获得一个相差等于1的范围。此时其实还是在一个很大的范围内，我们还需要想办法去缩小范围，于是可以选择将等式两边全都乘5

将5*k0作为新的k我们又可以获得以下信息：

其中k*pt是5的倍数，5n也是5的倍数，所以解密得到的明文也会是5的倍数，所以我们根据是否出现Buzz来判断二分法的缩减方式，这里注意此时和前一种情况的二分判断条件刚好相反。此时pt在下面这一范围内：

我们可以发现pt的范围在缩小，所以我们循环这一过程，不断在前一个基础上乘5，我们就能逐渐的逼近pt的值，因为pt经过了padding，而flag处于中间部分，所以我们不需要找到完全正确的pt就能获得flag

from Crypto.Util.number import *
from pwn import *
def oracle(x):
    io.sendlineafter(b'> ', str(pow(x, e, n) * ct % n).encode())
    returnb'Buzz'notin io.recvline()

def binary_search(left, right, reverse=False):
    while left < right - 1:
        mid = (left + right) // 2
        if oracle(mid) ^ reverse:
            right = mid
        else:
            left = mid
    return left, right

whileTrue:
    io = remote("be.ax",31101)
    io.recvuntil(b'n = ')
    n = int(io.recvline().decode())
    io.recvuntil(b'e = ')
    e = int(io.recvline().decode())
    io.recvuntil(b'ct = ')
    ct = int(io.recvline().decode())
    ifnot oracle(2):
        k = 1
        whileTrue:
            k *= 2
            if oracle(k):
                break
        left, right = binary_search(k // 2, k)
        prog = io.progress('Flag')

        for i in range(1, 1000):
            left, right = binary_search(5 * left, 5 * right, reverse=True)
            print(left,right)
            prog.status(str(long_to_bytes(5 ** i * n // right)[16:-16]))
        break

    io.close()
#corctf{''.join(fizz_buzz(x) for x in range(99, 102)) == "FizzBuzz101" == cool_username}

以后会经常对一些有趣的题目做讲解复现工作，感兴趣的师傅可以多关注我们团队公众号的更新，相关问题也可以留言，期待和大家共同探讨更多的密码学题目。

作者

Generate

follow your heart

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

whileTrue:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    ifnot out:
        out = pt
    print(out)
from Crypto.Util.number import *
from pwn import *
# a=remote("be.ax",31100)
# l=a.recv().split(b'=')
# print(l)
# while True:
#     X = getPrime(10)
#     c = int(l[3][:-2])
#     n = int(l[1][:-2])
#     Y = (c * (X ** 65537)) % n
#     a.sendline(str(Y).encode())
#     print(X)
#     print(Y)
#     print(a.recvline())
n=10923590886634228827134658466234332962160546970259806875947299955117094723
2996590557964241534101853321789427925631360625471407190264507981047481840604
5770295033165358752485494005614706506946041594393587695948197211669743677637
1201851439874292252155611926493174569162636187926889061627634316983399923186
1189833
c=54154300348903111005066683187322110240325256042602814495907789220256344603
9329651492217054936857491785316431371347695833366523065193277532980043371316
2219549684070989291489469384068884401333991713653240631955340521542862833755
5863105880457193242611315359206147315741465280238895273742546724024586290588
394695
w=907
y=26641182241400186140764833732531788410188640530460941989584702007887972922
0893088977366572306324954901383970069683822351533581707241548687145888017505
0739702872878490121501943582580854230668238851423909090028374384975663116055
0184102438364341973285800800919002105937122573558829974207210810107339187277
577768
ct=1617872921486161438959529626097492037660629295223293116750255222467849722125817349217082369174984216697864465452996697846569528891027592080706141175012700498085383500035413467709314885420625836615662777908956038879208002465859460678671983566645413919704836898065353721740490145081034
flag=ct*inverse(w,n)%n
print(long_to_bytes(flag))
    #corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}
from Crypto.Util.number import bytes_to_long, getPrime

# my NEW and IMPROVED secret sharing scheme!! (now with multivariate quadratics)

with open('flag.txt', 'rb') as f:
    flag = f.read()

s = bytes_to_long(flag)
p = getPrime(len(bin(s)))
print(p)
F = GF(p)
N = 1024

conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])

A = random_matrix(F, N, N)

for i in range(0, N):
    for j in range(0, i):
        A[i, j] = 0
B = random_matrix(F, N, 1)
C = matrix(F, [F(s)])

fn = lambda x: (x.T * A * x + B.T * x + C)[0][0]

L = []
for i in range(7):
    L.append(fn(conv(i + 1)))

print(L)
from Crypto.Util.number import *
p=1873089703968291141600166892623234932796169766648225659075834963115683566265697596115468506218441065194050127470898727249982614285036691594726454694776985338487833409983284911305295748861807972501521427415609
L=[676465814304447223312460173335785175339355609820794166139539526721603814168727462048669021831468838980965201045011875121145342768742089543742283566458551844396184709048082643767027680757582782665648386615861, 1472349801957960100239689272370938102886275962984822725248081998254467608384820156734807260120564701715826694945455282899948399224421878450502219353392390325275413701941852603483746312758400819570786735148132, 202899433056324646894243296394578497549806047448163960638380135868871336000334692955799247243847240605199996942959637958157086977051654225700427599193002536157848015527462060033852150223217790081847181896018, 1065982806799890615990995824412253076607488063240855100580513221962298598002468338823225586171107539104635808108356492123167315175110515086192932230998426512947581115358738651206273178867911944034690138825583, 1676559204037482856674710667663849447914859348633288513196735253002541076530170853584406282605482862202276451646974549657672382936948091649764874334064431407644457518190694888175499630744741620199798070517691, 13296702617103868305327606065418801283865859601297413732594674163308176836719888973529318346255955107009306239107173490429718438658382402463122134690438425351000654335078321056270428073071958155536800755626, 1049859675181292817835885218912868452922769382959555558223657616187915018968273717037070599055754118224873924325840103339766227919051395742409319557746066672267640510787473574362058147262440814677327567134194]
F = GF(p)
N = 1024
conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])
c=(L[6]-(L[2]+L[4]+L[5]-2*(L[0]+L[1]+L[3]))-(L[0]+L[1]+L[3]))%p
print(long_to_bytes(c))
    #corctf{mind your ones and zeroes because zero squared is zero and one squared is one}
import random

def random_alphastring(size):
    return"".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i+klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext
    
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

message = open("message.txt").read().upper()
message = "".join([char for char in message if char in alphabet])
flag = open("flag.txt").read()
flag = flag.lstrip("corctf{").rstrip("}")
message += flag
assert all([char in alphabet for char in message])

key = random_alphastring(bs)
iv, ct = cbc(key, pad(bs, message))
print(f"{iv = }")
print(f"{ct = }")
iv = 'RLNZXWHLULXRLTNP'
ct = 'ZQTJIHLVWMPBYIFRQBUBUESOOVCJHXXLXDKPBQCUXWGJDHJPQTHXFQIQMBXNVOIPJBRHJQOMBMNJSYCRAHQBPBSMMJWJKTPRAUYZVZTHKTPUAPGAIJPMZZZDZYGDTKFLWAQTSKASXNDRRQQDJVBREUXFULWGNSIINOYULFXLDNMGWWVSCEIORQESVPFNMWZKPIYMYVFHTSRDJWQBTWHCURSBPUKKPWIGXERMPXCHSZKYMFLPIAHKTXOROOJHUCSGINWYEILFIZUSNRVRBHVCJPVPSEGUSYOAMXKSUKSWSOJTYYCMEHEUNPJAYXXJWESEWNSCXBPCCIZNGOVFRTGKYHVSZYFNRDOVPNWEDDJYITHJUBVMWDNNNZCLIPOSFLNDDWYXMYVCEOHZSNDUXPIBKUJIJEYOETXWOJNFQAHQOVTRRXDCGHSYNDYMYWVGKCCYOBDTZZEQQEFGSPJJIAAWVDXFGPJKQJCZMTPMFZDVRMEGMPUEMOUVGJXXBRFCCCRVTUXYTTORMSQBLZUEHLYRNJAAIVCRFSHLLPOANFKGRWBYVSOBLCTDAUDVMMHYSYCDZTBXTDARWRTAFTCVSDRVEENLHOHWBOPYLMSDVOZRLENWEKGAWWCNLOKMKFWWAZJJPFDSVUJFCODFYIMZNZTMAFJHNLNMRMLQRTJJXJCLMQZMOFOGFPXBUTOBXUCWMORVUIIXELTVIYBLPEKKOXYUBNQONZLPMGWMGRZXNNJBUWBEFNVXUIAEGYKQSLYSDTGWODRMDBHKCJVWBNJFTNHEWGOZFEZMTRBLHCMHIFLDLORMVMOOHGXJQIIYHZFMROGUUOMXBTFMKERCTYXFIHVNFWWIUFTGLCKPJRFDRWDXIKLJJLNTWNQIOFWSIUQXMFFVIIUCDEDFEJNLKLQBALRKEYWSHESUJJXSHYWNRNPXCFUEFRJKSIGXHFTKNJXSYVITDOGYIKGJIOOHUFILWYRBTCQPRPNOKFKROTFZNOCZXZEYUNWJZDPJDGIZLWBBDGZJNRQRPFFGOTGFBACCRKLAPFLOGVYFXVIIJMBBMXWJGLPOQQHMNBCINRGZRBVSMLKOAFGYRUDOPCCULRBE'

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

import random

def random_alphastring(size):
    return"".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in
               zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def sub_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in
               zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return"".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i + klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext

def decode(key, ciphertext):
    klen = len(key)
    blocks = [ciphertext[i:i + klen] for i in range(0, len(ciphertext), klen)]
    plaintext = ""
    for block in blocks:
        block = sub_key(key, block)
        plaintext += block
    return plaintext

def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

blocks = [ct[i:i + bs] for i in range(0, len(ct), bs)]
ct_noiv = ""
prev_block = iv
for block in blocks:
    sblock = sub_key(prev_block, block)
    ct_noiv += sblock
    prev_block = block

print(ct_noiv)
#IDJUSTLIKETOINTERJECTFORAMOMENTWHATYOUREREFERINGTOASLINUXISINFACTGNULINUXORASIVERECENTLYTAKENTOCALLINGITGNUPLUSLINUXLINUXISNOTANOPERATINGSYSTEMUNTOITSELFBUTRATHERANOTHERFREECOMPONENTOFAFULLYFUNCTIONINGGNUSYSTEMMADEUSEFULBYTHEGNUCORELIBSSHELLUTILITIESANDVITALSYSTEMCOMPONENTSCOMPRISINGAFULLOSASDEFINEDBYPOSIXMANYCOMPUTERUSERSRUNAMODIFIEDVERSIONOFTHEGNUSYSTEMEVERYDAYWITHOUTREALIZINGITTHROUGHAPECULIARTURNOFEVENTSTHEVERSIONOFGNUWHICHISWIDELYUSEDTODAYISOFTENCALLEDLINUXANDMANYOFITSUSERSARENOTAWARETHATITISBASICALLYTHEGNUSYSTEMDEVELOPEDBYTHEGNUPROJECTTHEREREALLYISALINUXANDTHESEPEOPLEAREUSINGITBUTITISJUSTAPARTOFTHESYSTEMTHEYUSELINUXISTHEKERNELTHEPROGRAMINTHESYSTEMTHATALLOCATESTHEMACHINESRESOURCESTOTHEOTHERPROGRAMSTHATYOURUNTHEKERNELISANESSENTIALPARTOFANOPERATINGSYSTEMBUTUSELESSBYITSELFITCANONLYFUNCTIONINTHECONTEXTOFACOMPLETEOPERATINGSYSTEMLINUXISNORMALLYUSEDINCOMBINATIONWITHTHEGNUOPERATINGSYSTEMTHEWHOLESYSTEMISBASICALLYGNUWITHLINUXADDEDORGNULINUXALLTHESOCALLEDLINUXDISTRIBUTIONSAREREALLYDISTRIBUTIONSOFGNULINUXANYWAYHERECOMESTHEFLAGITSEVERYTHINGAFTERTHISATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

whileTrue:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    ifnot out:
        out = "101"
    print(out)
from Crypto.Util.number import *
from pwn import *
def oracle(x):
    io.sendlineafter(b'> ', str(pow(x, e, n) * ct % n).encode())
    returnb'Buzz'notin io.recvline()

def binary_search(left, right, reverse=False):
    while left < right - 1:
        mid = (left + right) // 2
        if oracle(mid) ^ reverse:
            right = mid
        else:
            left = mid
    return left, right

whileTrue:
    io = remote("be.ax",31101)
    io.recvuntil(b'n = ')
    n = int(io.recvline().decode())
    io.recvuntil(b'e = ')
    e = int(io.recvline().decode())
    io.recvuntil(b'ct = ')
    ct = int(io.recvline().decode())
    ifnot oracle(2):
        k = 1
        whileTrue:
            k *= 2
            if oracle(k):
                break
        left, right = binary_search(k // 2, k)
        prog = io.progress('Flag')

        for i in range(1, 1000):
            left, right = binary_search(5 * left, 5 * right, reverse=True)
            print(left,right)
            prog.status(str(long_to_bytes(5 ** i * n // right)[16:-16]))
        break

    io.close()
    #corctf{''.join(fizz_buzz(x) for x in range(99, 102)) == "FizzBuzz101" == cool_username}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342308-wxsync-2025-08-c1791da0e1cf4ba822cbb9abb096f2ce.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342310-wxsync-2025-08-2f51c95e7f9c72a1aa448b3e956af10b.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342311-wxsync-2025-08-cab46db2439b6b016446f2b77c8762ba.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342313-wxsync-2025-08-ed169fbb36681af548d8bc382be6647b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342314-wxsync-2025-08-9fcf74f9b360863664e9823e93813cae.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342315-wxsync-2025-08-861158ca217343f13326a0c3b210094d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342317-wxsync-2025-08-285c61a00c01199e7e61817334604c6c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342318-wxsync-2025-08-3f775e92d7165b915b01dd4035260202.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342320-wxsync-2025-08-cc7fda43da4639499587d4db66a500b7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756342321-wxsync-2025-08-2f3cffdf7a80aeece13df6fe8b9c526a.png)