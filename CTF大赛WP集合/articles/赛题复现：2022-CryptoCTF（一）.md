# 赛题复现：2022-CryptoCTF（一）

> 原文: https://www.ctfiot.com/58892.html
> ID: 58892

这一届似乎出的比上一届简单一点？有好几只大佬队伍ak的。

第一部分是easy和medium-easy难度的。

warm-up

Mic-Check

分值：19

考点：签到

Can you hear me?2022-Jul-Thu 12:20:26

If you can, enter your first flag:

CCTF{Th3_B3sT_1S_Yet_t0_C0m3!!}

easy

Klamkin

分值：61

考点：Congruence

challenge

We need to have a correct solution!

nc 04.cr.yp.toc.tf 13777

[root@VM-0-7-centos ~]# nc 04.cr.yp.toc.tf 13777
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hello, now we are finding the integer solution of two divisibility  |
|  relation. In each stage send the requested solution. Have fun :)    |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| We know (ax + by) % q = 0 for any (a, b) such that (ar + bs) % q = 0
| and (q, r, s) are given!
| Options: 
| [G]et the parameters 
| [S]end solution 
| [Q]uit
G
| q = 289932383341902531151841340632555887679
| r = 197196838427345567639010598439485580615
| s = 59132640739541526585077026866726580617
| Options: 
| [G]et the parameters 
| [S]end solution 
| [Q]uit
S
| please send requested solution like x, y such that y is 12-bit: 

thought

虽然是一道简单题，但这道题目的题面看起来还是挺绕的。

题目给出了 

，然后我们需要解出 

 满足 

然后由于“已知对于任意的 

 满足 

”，所以让我们输入特定比特长度的 
 或者 

首先我们就是需要解出一对 

 了，显然我们可以直接设 

 ，

然后我们根据要求，定下一个 
 或者 
，然后再根据同余式算出另外一个值即可。

以下是交互脚本。

exp

from Crypto.Util.number import *
from pwn import *

def x(n):
    x = getPrime(n)
    y = -a*x*inverse(b,q) % q
    assert (a*x + b*y) % q == 0
    sh.sendline(str(x)+","+str(y))

def y(n):
    y = getPrime(n)
    x = -b*y*inverse(a,q) % q
    assert (a*x + b*y) % q == 0
    sh.sendline(str(x)+","+str(y))

sh = remote("04.cr.yp.toc.tf",13777)
context.log_level = 'debug'

sh.recvuntil("[Q]uit")
sh.sendline("G")

sh.recvuntil("| q = ")
q = int(sh.recvuntil("n")[:-1])
sh.recvuntil("| r = ")
r = int(sh.recvuntil("n")[:-1])
sh.recvuntil("| s = ")
s = int(sh.recvuntil("n")[:-1])

sh.recvuntil("[Q]uit")
sh.sendline("S")

while True:
    a = inverse(r,q)
    b = inverse(-s,q)
    assert (a*r + b*s) % q == 0

    ch = sh.recvuntil("bit: n").split(b" ")
    print(ch)
    if ch[-4]== b"x":
        x(int(ch[-2][:2]))
    else:
        y(int(ch[-2][:2]))

sh.interactive()

result

[+] Opening connection to 04.cr.yp.toc.tf on port 13777: Done
[DEBUG] Received 0xdb bytes:
    b'||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||n'
    b'|  Hello, now we are finding the integer solution of two divisibility  |n'
    b'|  relation. In each stage send the requested solution. Have fun :)    |n'
[DEBUG] Received 0xeb bytes:
    b'||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||n'
    b'| We know (ax + by) % q = 0 for any (a, b) such that (ar + bs) % q = 0n'
    b'| and (q, r, s) are given!n'
    b'| Options: n'
    b'|t[G]et the parameters n'
    b'|t[S]end solution n'
    b'|t[Q]uitn'
[DEBUG] Sent 0x2 bytes:
    b'Gn'
[DEBUG] Received 0xc7 bytes:
    b'| q = 248930089074638341399935646008896010497n'
    b'| r = 65697821096685931683761068135861058583n'
    b'| s = 8664059547396611157411147813907067755n'
    b'| Options: n'
    b'|t[G]et the parameters n'
    b'|t[S]end solution n'
    b'|t[Q]uitn'
[DEBUG] Sent 0x2 bytes:
    b'Sn'
[DEBUG] Received 0x43 bytes:
    b'| please send requested solution like x, y such that y is 12-bit: n'
[b'n|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'12-bit:', b'n']
[DEBUG] Sent 0x2c bytes:
    b'36385751892032159627624237030492875755,3539n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 13-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'13-bit:', b'n']
[DEBUG] Sent 0x2d bytes:
    b'134300229126114739440789160858242865128,7993n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 16-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'16-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'196535357683169499069413298376157574596,49991n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that x is 16-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'x', b'is', b'16-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'36847,229436344314746801153667328942317085633n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 19-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'19-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'90733961161770834421760416122416141408,462541n'
[DEBUG] Received 0x4e bytes:
    b'| Congrats, you got the flag: CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}n'

Baphomet

分值：56

考点：已知明文攻击

challenge

#!/usr/bin/env python3

from base64 import b64encode
from flag import flag

def encrypt(msg):
 ba = b64encode(msg.encode('utf-8'))
 baph, key = '', ''

 for b in ba.decode('utf-8'):
  if b.islower():
   baph += b.upper()
   key += '0'
  else:
   baph += b.lower()
   key += '1'

 baph = baph.encode('utf-8')
 key = int(key, 2).to_bytes(len(key) // 8, 'big')

 enc = b''
 for i in range(len(baph)):
  enc += (baph[i] ^ key[i % len(key)]).to_bytes(1, 'big')

 return enc

enc = encrypt(flag)
f = open('flag.enc', 'wb')
f.write(enc)
f.close()

thought

题目将明文base64之后，根据大小写来构造密钥比特，随后将密钥比特转成字节作为key，循环自身异或大小写翻转的明文base64.

那么这里的思路就是，我们已知flag会是以“CCTF{”开头，另外密文总长度为48个字符，这意味着key的长度只有 48 / 8 = 6 个字节。

于是我们将“CCTF{“进行base64编码，随后取前六个字符和密文异或即可计算出密钥，随后就能恢复整个明文，

最后明文大小写翻转然后base64解码即可获得flag。

exp

#!/usr/bin/env python3
#
with open("flag.enc","rb") as f:
 enc = f.read()
print(len(enc))

from base64 import b64encode,b64decode
msg=b"CCTF{"
ba = b64encode(msg)
baph, key = '', ''
for b in ba.decode('utf-8'):
 if b.islower():
  baph += b.upper()
  key += '0'
 else:
  baph += b.lower()
  key += '1'

baph = baph.encode('utf-8')[:6]
print(baph)

key = b""
for i in range(len(baph)):
 key += (baph[i] ^ enc[i]).to_bytes(1, 'big')
print(key)

dec = b""
for i in range(len(enc)):
 dec += (enc[i] ^ key[i % len(key)]).to_bytes(1, 'big')
print(dec)

flag=""
for b in dec.decode('utf-8'):
 if b.islower():
  flag += b.upper()
 else:
  flag += b.lower()
print(b64decode(flag.encode('utf-8')))
#key = int(key, 2).to_bytes(len(key) // 8, 'big')

result

48
b'q0nurN'
b'xf9bxadxacNxff'
b'q0nurNTvCfaZCL8WuL9St3DfuL8Xn1PFDeGZx1bYmgjmm019'
b'CCTF{UpP3r_0R_lOwER_17Z_tH3_Pr0bL3M}'
[Finished in 0.2s]

medium-easy

SOTS

分值：49

考点：two_square

challenge

He who abides far away from his home, is ever longing for the day he shall return.

nc 05.cr.yp.toc.tf 37331

[root@VM-0-7-centos ~]# nc 05.cr.yp.toc.tf 37331
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hey math experts, in this challenge we will deal with the numbers   |
|  those are the sum of two perfect square, now try hard to find them! |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| Generating the `n', please wait...
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
G
| n = 1243565868390316746681363697659435925395524656187056587629633961874200469
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
S
| Send your pair x, y here: 

Thought

题目给出 
，要求给出两个数 

 满足 

，这里我们直接去网站上计算，或者sagemath自带有two_square函数

exp

https://www.alpertron.com.ar/QUAD.HTM

# sagemath

sage: two_squares(5545629715339564937545617256977338230363684107665849984098838446686735017)
(1166738044093249132248421369078945211, 2045568882195127737861825295828693636)

result

root@VM-0-7-centos ~]# nc 05.cr.yp.toc.tf 37331
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hey math experts, in this challenge we will deal with the numbers   |
|  those are the sum of two perfect square, now try hard to find them! |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| Generating the `n', please wait...
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
g
| n = 5545629715339564937545617256977338230363684107665849984098838446686735017
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
s
| Send your pair x, y here: 
2010025793396973084655790372917576051,1226958037268770577663190958375036304
| Congratz! the flag is CCTF{3Xpr3sS_4z_Th3_sUm_oF_7w0_Squ4rE5!}

polyRSA

分值：42

考点：RSA

challenge

Hello RSA, my old friend!

#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def keygen(nbit = 64):
 while True:
  k = getRandomNBitInteger(nbit)
  p = k**6 + 7*k**4 - 40*k**3 + 12*k**2 - 114*k + 31377
  q = k**5 - 8*k**4 + 19*k**3 - 313*k**2 - 14*k + 14011
  if isPrime(p) and isPrime(q):
   return p, q

def encrypt(msg, n, e = 31337):
 m = bytes_to_long(msg)
 return pow(m, e, n)

p, q = keygen()
n = p * q
enc = encrypt(flag, n)
print(f'n = {n}')
print(f'enc = {enc}')

Thought

 都是由 
 表示的，那么我们可以构造方程 

，用sagemath自带的求根函数即可求得 
，然后就能计算出 

 了。

exp

n = 44538727182858207226040251762322467288176239968967952269350336889655421753182750730773886813281253762528207970314694060562016861614492626112150259048393048617529867598499261392152098087985858905944606287003243
enc = 37578889436345667053409195986387874079577521081198523844555524501835825138236698001996990844798291201187483119265306641889824719989940722147655181198458261772053545832559971159703922610578530282146835945192532
R.<k> = ZZ[]

p = k**6 + 7*k**4 - 40*k**3 + 12*k**2 - 114*k + 31377
q = k**5 - 8*k**4 + 19*k**3 - 313*k**2 - 14*k + 14011

f = p*q-n
x = f.roots()[0][0]

pp=p(x)
qq=q(x)
phi = (pp-1)*(qq-1)
d = inverse_mod(31337,phi)
from Crypto.Util.number import *
print(long_to_bytes(pow(enc,d,n)))

result

b'CCTF{F4C70r!N9_tRIcK5_aR3_fUN_iN_RSA?!!!}'

Infinity castle

分值：131

考点：二次方、三次方、立方和、平方差、积分、泰勒展开

challenge

Can you break our new schema and decrypt the mixed encrypted message without having the public key and shared secret?!

#!/usr/bin/env python3

from Crypto.Util.number import *
from os import urandom

class TaylorSeries():

 def __init__(self, order):
  self.order = order
  
 def coefficient(self, n):
  i = 0
  coef = 1
  while i < n:
   i += 1
   coef *= (coef * (1/2-i+1)) / i
  return coef

 def find(self, center):
  sum = 0
  center -= 1
  i = 0
  while i < self.order:
   sum += (center**(1/2-i) * self.coefficient(i))
   i += 1
  return sum

def xor(cip, key):
 repeation = 1 + (len(cip) // len(key))
 key = key * repeation
 key = key[:len(cip)]
 
 msg = bytes([c ^ k for c, k in zip(cip, key)])
 return msg

# If you run these 3 functions (diamond, triage, summarize) with big numbers, they will never end
# You need to optimize them first

def diamond(num):
 output = 0
 for i in range(num):
  output += i*2 + 1
 return output

def triage(num):
 output = 0
 index = 0
 for i in range(num):
  output += (i+index)*6 + 1
  index += i
 return output

def summarize(b):
 order = getRandomRange(1000, 2000)
 t = TaylorSeries(order)
 output = 0
 
 i = 2
 while i < b:
  b1 = t.find(i)
  b2 = t.find(i+1)
  output += (b1+b2) / 2
  i += 1
 return output

KEY_SIZE = 2048
p, q = [getPrime(KEY_SIZE) for _ in '01']

e, n = 0x10001, p*q

f = open ('./message.txt', 'rb')
message = f.read()
f.close()
msg_length = len(message)
padded_msg = message + urandom(len(long_to_bytes(n)) - msg_length)
padded_msg_length = len(padded_msg)

xor_key = long_to_bytes(int(summarize(n)))[:padded_msg_length]
assert(len(xor_key) == 512)

enc0 = xor(padded_msg, xor_key)
assert(bytes_to_long(enc0) < n)

c0 =  abs(diamond(p) - diamond(q))
c1 =  triage(p)
c1 += 3*n*(p+q)
c1 += triage(q)

m = bytes_to_long(enc0)
enc1 = pow(m, e, n)

print(f"c0 = {c0}")
print(f"c1 = {c1}")
print(f"enc = {enc1}")

Thought

这里三个函数经过测试发现分别表示如下三个函数：

diamond：

triage：

summarize：

 【这里求积分用了泰勒展开，所以不是很好认】

那么利用 

 我们构造方程可以解出 

，然后根据summarize的表达式计算 

，即可恢复flag。

exp

def xor(cip, key):
 repeation = 1 + (len(cip) // len(key))
 key = key * repeation
 key = key[:len(cip)]
 msg = bytes([c ^^ k for c, k in zip(cip, key)])
 return msg

c0 = 194487778980461745865921475300460852453586088781074246328543689440168930873549359227127363759885970436167330043371627413542337857082400024590112412164095470165662281502211335756288082198009158469871465280749846525326701136380764079685636158337203211609233704905784093776008350120607841177268965738426317288541638374141671346404729428158104872411498098187946543666987926130124245185069569476433120128275581891425551325847219504501925282012199947834686225770246801353666030075146469275695499044424390475398423700504158154044180028733800154044746648133536737830623670383925046006108348861714435567006327619892239876863209887013290251890513192375749866675256952802329688897844132157098061758362137357387787072005860610663777569670198971946904157425377235056152628515775755249828721767845990597859165193162537676147173896835503209596955703313430433124688537275895468076469102220355973904702901083642275544954262724054693167603475188412046722656788470695566949847884250306735314144182029335732280420629131990311054229665691517003924788583771265625694414774865289407885678238795596912006567817508035434074250123869676396153982762032750080222602796273083162627489526255501643913672882350236497429678928099868244687228703074267962827621792960
c1 = 102325064080381160170299055162846304227217463467232681115953623386548494169967745781550171804781503102663445039561476870208178139548389771866145006535051362059443515034504958703659546162037904784821960707630188600064568878674788077706711506213779443920430038560373854184526850365974450688458342413544179732143225845085164110594063440979455274250021370090572731855665413325275414458572412561502408983107820534723804225765540316307539962199024757378469001612921489902325166003841336027940632451584642359132723894801946906069322200784708303615779699081247051006259449466759863245508473429631466831174013498995506423210088549372249221415401309493511477847517923201080509933268996867995533386571564898914042844521373220497356837599443280354679778455765441375957556266205953496871475611269965949025704864246188576674107448587696941054123618319505271195780178776338475090463487960063464172195337956577785477587755181298859587398321270677790915227557908728226236404532915215698698185501562405374498053670694387354757252731874312411228777004316623425843477845333936913444143768519959591070492639650368662529749434618783626718975406802741753688956961837855306815380844030665696781685152837849982159679122660714556706669865596780528277684800454866433826417980212164051043504955615794706595412705883261111953152250227679858538249797999044336210905975316421254442221408945203647754303635775048438188044803368249944201671941949138202928389951227347433255867504906597772044398973241425387514239164853656233776024571606159378910745571588836981735827902305330330946219857271646498602227088657739442867033212012876837654750348578740516798444734534291467314881324902354425889448102902750077077381896216130734894767553834949561471219923459897244690006643798812989271282475503126962274052192342840870308710338336817452628324667507548265612892611100350882163205858101959976
enc = 122235247669762131006183252122503937958296387791525458429403709404875223067116491817728568224832483391622109986550732469556761300197133827976956875865159629512476600711420561872409721582387803219651736262581445978042694384374119142613277808898398213602093802571586386354257378956087240174787723503606671543195193114158641301908622673736098768829071270132073818245595918660134745516367731595853832524328488074054536278197115937409643221809577554866060292157239061557708159310445977052686561229611117673473208278176118561352693319461471419694590218295911647368543698198762827636021268989705079848502749837879584394379300566277359149621932579222865430374652678738198451655509408564586496375811666876030847654260305392984710580761255795785508407844683687773983669843744274915862335181251050775093896006210092665809300090715190088851654138383362259256212093670748527819287681468901379286722214112321906917311154811516336259463356911326393701445497605365038857575515541024824906818473933597129846235905072394148879079996812146836910199111439031562946495046766063326815863624262541346543552652673629442370320109404700346028639853707278295255350982238521659924641921142615894039995513480511108116053798143154593343124822462519555715118822045

var('p,q')

f1 = p^2-q^2 - c0
f2 = (p+q)^3 - c1

#solve([f1,f2],p,q)
p=25465500595039564722385454268618341460440964303654692306893194812608651011894765148023201769023925823267446913594798724374078776058926548056279105656348138942211069695157129067986030357247987537066065195208337853580939616954961742954173270603234042184081995050125067398704045490448077961447418406856674045777724275017678698252609741079175784928310951915104807404003531834525200421059550762294584722178356010146438598799668537922242765662363844939035164178525445220653839693135494967926642943210917823981779895464411806829004306900926935124663285407830585204630912848783431051369106939431567473170247979142455819150893
q=21307368246113800130311098641506744510559988209047095448061577734947715969121645982743962584143752085867914325394457857827478912559095766977509129246922499990951138184298921892924074303356650532229644986118338361761354192554363128824141104808606558539422865199413633150757655174985683830034245659632460363700309887626934298289805670092066041542014924213128271705967504359900458092855272034197878632989626323553684162988741101770565319360726673172671459797955787997515498457867020749156835947018833861229200382521269341946614058721285386773372009177934062994798868703374266787876752211055631019633581263575312198649933
phi=(p-1)*(q-1)
e=0x10001
from Crypto.Util.number import *
d=inverse(e,phi)
n = p*q
padded_msg = long_to_bytes(pow(enc,d,n))

xor_key = long_to_bytes(int(2/3*n^(3/2)))[:512]
enc0 = xor(padded_msg, xor_key)
print(enc0)

result

b'Never heard of using taylor series and integral beside RSA?!nBut there are always ways to make things complicatednnCCTF{Mix1ng_c4lcUluS_w17h_Numb3r_The0Rry_S33ms_s7r0ng_cRyp70_Sch3m4!!}nnWe compute integrals with just measuring the area with a little fraction, forget about tough works!nGood luck with the rest of CryptoCTF2022x9ax92Wxcfxa2dlx1ax91x96'x88xecxfezxcdxc2xe7x0bCx90xa3xc7xe7Uxb4Fxa535Vx19x9bx9exd4xf7xe7Xx02x19Yx86xfax9fx0b!x9axc1xd2xcayGx8af/x14xefxf9x1dxc2x9axcbx9da}g8xb8\ 2~xf3xe3xb6$xb6ix12xd6x82xfacx15xeeVa[sxa0Sx00yx0cx18xc34xbdx96fdxecxcfxb9x02<Qx8bxb8x9dxd5xefDuxdaxd2xf0xc6gx97xf8x952x0crs=x19.x11"x08x81xe7*x87xb8xbd>x82n~xf7l,tux96}*xab`x17xe7xf4xd7N^xe3xfexf3@x1ex1cx15xffCxecVVrxcax8dx03xc5xdaxd6xbf=xc6x14+xf2x14N'

Keydream

分值：105

考点：RSA

challenge

Everything is better homemade, we developed a homemade RSA, test it to see if it’s really better?

#!/usr/bin/env python3

from Crypto.Util.number import *
import string
from flag import flag

def randstr(l):
 rstr = [(string.printable[:62] + '_')[getRandomRange(0, 62)] for _ in range(l)]
 return ''.join(rstr)

def encrypt(msg, l):
 while True:
  rstr = 'CCTF{it_is_fake_flag_' + randstr(l) + '_90OD_luCk___!!}'
  p = bytes_to_long(rstr.encode('utf-8'))
  q = bytes_to_long(rstr[::-1].encode('utf-8'))
  if isPrime(p) and isPrime(q):
   n = p * q
   e, m = 65537, bytes_to_long(msg.encode('utf-8'))
   c = pow(m, e, n)
   return n, c

n, c = encrypt(flag, 27)

print(f'n = {n}')
print(f'c = {c}')

Thought

这里我们的构造出如下方程

未知的比特不多，直接调coppersmith‘s method即可。

exp

n = 23087202318856030774680571525957068827041569782431397956837104908189620961469336659300387982516148407611623358654041246574100274275974799587138270853364165853708786079644741407579091918180874935364024818882648063256767259283714592098555858095373381673229188828791636142379379969143042636324982275996627729079
c = 3621516728616736303019716820373078604485184090642291670706733720518953475684497936351864366709813094154736213978864841551795776449242009307288704109630747654430068522939150168228783644831299534766861590666590062361030323441362406214182358585821009335369275098938212859113101297279381840308568293108965668609

from Crypto.Util.number import *

phigh = bytes_to_long(b"CCTF{it_is_fake_flag_")
plow = bytes_to_long(b'_90OD_luCk___!!}')
P.<x> = PolynomialRing(Zmod(n))
f = (phigh << 344) + (x * 2^128) + plow
x0 = f.monic().small_roots(X=2^216, beta=0.4,epsilon=0.02)[0]
p = int(f(x0))
q = n//p
e = 65537
phi = (p-1)*(q-1)
d = inverse(e,phi)
print(long_to_bytes(pow(c,d,n)))

result

'Congratz, the flag is: CCTF{h0M3_m4dE_k3Y_Dr1vEn_CrYp7O_5ySTeM!}'

Jeksign

分值：100

考点：丢番图方程

challenge

Solve the equation, we like to have the solution!

nc 02.cr.yp.toc.tf 17113

#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import gensol, nbit_gensol
from flag import flag

m = bytes_to_long(flag.encode('utf-8'))
print(m)

a = 1337
b = 31337

def die(*args):
 pr(*args)
 quit()

def pr(*args):
 s = " ".join(map(str, args))
 sys.stdout.write(s + "n")
 sys.stdout.flush()

def sc():
 return sys.stdin.readline().strip()

def main():
 border = "|"
 pr(border*72)
 pr(border, "Welcome crypto guys! Here we are looking for the solution of special", border)
 pr(border, "Diophantine equation: 1337(z^4 - x^2) = 31337(y^2 - z^4) in natural ", border)
 pr(border, "numbers, in each stage solve the equation in mentioned interval :)  ", border)
 pr(border*72)

 STEP, level = 0, 19

 while True:
  p, q = nbit_gensol(1337, 31337, STEP + 30)
  x, y, z = gensol(a, b, p, q)
  pr(border, f"Send a solution like `x, y, z' such that the `z' is {STEP + 30}-bit: ")
  ans = sc()
  try:
   X, Y, Z = [int(_) for _ in ans.split(',')]
   NBIT = Z.bit_length()
  except:
   die(border, 'Your input is not valid, Bye!')
  if 1337*(Z**4 - X**2) == 31337*(Y**2 - Z**4) and NBIT == STEP + 30:
   if STEP == level - 1:
    die(border, f'Congrats, you got the flag: {flag}')
   else:
    pr('| good job, try to solve the next challenge :P')
    STEP += 1
  else:
   die(border, 'your answer is not correct, Bye!!')

if __name__ == '__main__':
 main()

Thought

题目要求我们给出20个满足 的 

，且对 
 的比特长度有要求

合并同类项

所以有

exp

from Crypto.Util.number import *
from sympy import *

from pwn import *
context.log_level = 'debug'
sh = remote("02.cr.yp.toc.tf",17113)
for i in range(30,49):
 ch = sh.recvuntil("-bit: n")
 z = getPrime(i)
 x = z**2
 y = x
 sh.sendline(str(x)+","+str(y)+","+str(z))
sh.interactive()

result

| Congrats, you got the flag: CCTF{4_diOpH4nT1nE_3Qua7i0n__8Y__Jekuthiel_Ginsbur!!}

Volgo

challenge

There is no land behind the Volga!! The Soviets surround us,and we have only a single key table to communicate to the outside!! Hopefully, the Soviets wouldn’t be able read our messages.

http://03.cr.yp.toc.tf:11117/

GET ENCRYPTDE FLAG 🙂

{"flag": "ZZNVH EOOAA JSGPB DAKCP MQRGM MBXDT NAULS MYJRI USVAY WQGUK KEWRJ BAPPW YDWQU KFDHC OOOWF QVANE XLEEK MVFBX HYQOR SFKGU AKWEB LEPXV LHRCG MKMSO DVOZS JFESS LTUEY QUGAA IODSI IZEQJ ROTBS TKSEH JBORC ZZNVH EOOAA"}

{"flag": "GGMCT NJOAA QAEYB FJZLP VKZTA DHIIG RVYGC RPQQN LHWRR YSDXM YDSJL ZUROG KHXNX DGPSM PPEBK INKSS WEVSH ZNEKW OTZNR NFLYQ KLIRC JVWLI PSNBF OEFHC NDUVO CABZC LCTEN NMDSI XVDEL DRADR YIPBQ IKOLM DJAQA GGMCT NJOAA"}

{"flag": "IISNJ IFFAA TYPMO WDJHA ZMNBD LKUAY TYPVD UGAYU OQMOO YRVUS SLFZI IXKVW LYUGT JWTYV XNEYU HLQVV IXUMJ BKNUQ WMLQT QKIWV UXOCA CVSPG UKJQG XCSFI RJEKU BWLBM AVRFW DMOPT VFXTD VROND XSEHF ZLWEJ VOVSX IISNJ IFFAA"}

{"flag": "BBHAC QDFAA KGBMH RVZSK RNVZH NGRAM WYHHE HKHJU UCQBL HPVAP TXDCZ ZMKWX ETCKC CMBSC VKUUF BMAIV RTAJE EWOUS SMOTQ KNQBF IRDVZ YJWQK WEAIA TONBI MMBUI RCULP BKEIO LNOAM XLUDR XJYAM DMWJN DUXXV FDVOC BBHAC QDFAA"}

Thought

看题目名字 

  好像是一个密码机还是啥的，先不管，经过交互我们发现，同样的flag加密好像会得到不同的值，然后所有明文加密后都会有十个字符的前缀和后缀包裹，并且前缀等于后缀。

A
{"cipher": "BBHAC QDFAA IXXXX BBHAC QDFAA"}
AA
{"cipher": "BBHAC QDFAA IUXXX BBHAC QDFAA"}
AAA
{"cipher": "BBHAC QDFAA IUVXX BBHAC QDFAA"}
B
{"cipher": "BBHAC QDFAA HXXXX BBHAC QDFAA"}
BB
{"cipher": "BBHAC QDFAA HTXXX BBHAC QDFAA"}
C
{"cipher": "BBHAC QDFAA GXXXX BBHAC QDFAA"}

可以看到，加密是分组的，长度为5，不够的时候密文会由X继续填充。

当前缀为”BBHAC QDFAA“ 时，

第一个字符的位置，

第二个字符的位置，

可以发现规律，

，

换言之，，

那么，我们只需要一次交互，获取每个位置的求和值，类似于 

 ，看FLAG的长度我们需要发155个”A“过去

'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
{"cipher": "BBHAC QDFAA IUVLR EJVRR FJUSV MLFRY WRGMP HQGSO MVPQF AOPPR HJLPF YXOPQ IKUJY KFIAP UMOLQ ZLBZV TXSIJ SHZIO WPNUO JPSUK HFREL NVZTS TGLVN PTGFR GYGRS STPGB PZWTG DYITJ SOPQU JHWPT SIBSE QDYSW TPPMT BBHAC QDFAA"}

计算出 

 后对flag的密文做模减运算就可以获取flag了。

exp

TABLE="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

CIPHER = "BBHAC QDFAA IUVLR EJVRR FJUSV MLFRY WRGMP HQGSO MVPQF AOPPR HJLPF YXOPQ IKUJY KFIAP UMOLQ ZLBZV TXSIJ SHZIO WPNUO JPSUK HFREL NVZTS TGLVN PTGFR GYGRS STPGB PZWTG DYITJ SOPQU JHWPT SIBSE QDYSW TPPMT BBHAC QDFAA".replace(" ","")

FLAGENC= "BBHAC QDFAA KGBMH RVZSK RNVZH NGRAM WYHHE HKHJU UCQBL HPVAP TXDCZ ZMKWX ETCKC CMBSC VKUUF BMAIV RTAJE EWOUS SMOTQ KNQBF IRDVZ YJWQK WEAIA TONBI MMBUI RCULP BKEIO LNOAM XLUDR XJYAM DMWJN DUXXV FDVOC BBHAC QDFAA".replace(" ","")

PLAINTEXT = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

KEY = ""
FLAG = ""
for i in range(155):
 KEY += TABLE[(TABLE.index(CIPHER[i])+TABLE.index(PLAINTEXT[i]))%26]

for i in range(155):
    FLAG += TABLE[(TABLE.index(KEY[i]) - TABLE.index(FLAGENC[i]))%26]
print(FLAG)
print(FLAG.replace("Z"," "))

result

# YOUZKNOWZHOWZTOZFORMATZFLAGZJUSTZPUTZUPCOMINGZLETTERSZWITHINZCURLYZBRACESZFOLLOWEDZBYZCCTFZOOJMPMDDIXCLNNWFTEJUMFXKBRVVMOPSLSSLUTXVDVNDMYYPHPWFJRNJBVBOMUYR

# YOU KNOW HOW TO FORMAT FLAG JUST PUT UPCOMING LETTERS WITHIN CURLY BRACES FOLLOWED BY CCTF OOJMPMDDIXCLNNWFTEJUMFXKBRVVMOPSLSSLUTXVDVNDMYYPHPWFJRNJBVBOMUYR

flag: CCTF{OOJMPMDDIXCLNNWFTEJUMFXKBRVVMOPSLSSLUTXVDVNDMYYPHPWFJRNJBVBOMUYR}


```
CCTF{Th3_B3sT_1S_Yet_t0_C0m3!!}
```



```
nc 04.cr.yp.toc.tf 13777
```



```
[root@VM-0-7-centos ~]# nc 04.cr.yp.toc.tf 13777
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hello, now we are finding the integer solution of two divisibility  |
|  relation. In each stage send the requested solution. Have fun :)    |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| We know (ax + by) % q = 0 for any (a, b) such that (ar + bs) % q = 0
| and (q, r, s) are given!
| Options: 
| [G]et the parameters 
| [S]end solution 
| [Q]uit
G
| q = 289932383341902531151841340632555887679
| r = 197196838427345567639010598439485580615
| s = 59132640739541526585077026866726580617
| Options: 
| [G]et the parameters 
| [S]end solution 
| [Q]uit
S
| please send requested solution like x, y such that y is 12-bit:
```



```
from Crypto.Util.number import *
from pwn import *

def x(n):
    x = getPrime(n)
    y = -a*x*inverse(b,q) % q
    assert (a*x + b*y) % q == 0
    sh.sendline(str(x)+","+str(y))

def y(n):
    y = getPrime(n)
    x = -b*y*inverse(a,q) % q
    assert (a*x + b*y) % q == 0
    sh.sendline(str(x)+","+str(y))

sh = remote("04.cr.yp.toc.tf",13777)
context.log_level = 'debug'

sh.recvuntil("[Q]uit")
sh.sendline("G")

sh.recvuntil("| q = ")
q = int(sh.recvuntil("n")[:-1])
sh.recvuntil("| r = ")
r = int(sh.recvuntil("n")[:-1])
sh.recvuntil("| s = ")
s = int(sh.recvuntil("n")[:-1])

sh.recvuntil("[Q]uit")
sh.sendline("S")

while True:
    a = inverse(r,q)
    b = inverse(-s,q)
    assert (a*r + b*s) % q == 0

    ch = sh.recvuntil("bit: n").split(b" ")
    print(ch)
    if ch[-4]== b"x":
        x(int(ch[-2][:2]))
    else:
        y(int(ch[-2][:2]))

sh.interactive()
```



```
[+] Opening connection to 04.cr.yp.toc.tf on port 13777: Done
[DEBUG] Received 0xdb bytes:
    b'||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||n'
    b'|  Hello, now we are finding the integer solution of two divisibility  |n'
    b'|  relation. In each stage send the requested solution. Have fun :)    |n'
[DEBUG] Received 0xeb bytes:
    b'||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||n'
    b'| We know (ax + by) % q = 0 for any (a, b) such that (ar + bs) % q = 0n'
    b'| and (q, r, s) are given!n'
    b'| Options: n'
    b'|t[G]et the parameters n'
    b'|t[S]end solution n'
    b'|t[Q]uitn'
[DEBUG] Sent 0x2 bytes:
    b'Gn'
[DEBUG] Received 0xc7 bytes:
    b'| q = 248930089074638341399935646008896010497n'
    b'| r = 65697821096685931683761068135861058583n'
    b'| s = 8664059547396611157411147813907067755n'
    b'| Options: n'
    b'|t[G]et the parameters n'
    b'|t[S]end solution n'
    b'|t[Q]uitn'
[DEBUG] Sent 0x2 bytes:
    b'Sn'
[DEBUG] Received 0x43 bytes:
    b'| please send requested solution like x, y such that y is 12-bit: n'
[b'n|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'12-bit:', b'n']
[DEBUG] Sent 0x2c bytes:
    b'36385751892032159627624237030492875755,3539n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 13-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'13-bit:', b'n']
[DEBUG] Sent 0x2d bytes:
    b'134300229126114739440789160858242865128,7993n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 16-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'16-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'196535357683169499069413298376157574596,49991n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that x is 16-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'x', b'is', b'16-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'36847,229436344314746801153667328942317085633n'
[DEBUG] Received 0x72 bytes:
    b'| good job, try to solve the next challenge :Pn'
    b'| please send requested solution like x, y such that y is 19-bit: n'
[b'|', b'good', b'job,', b'try', b'to', b'solve', b'the', b'next', b'challenge', b':Pn|', b'please', b'send', b'requested', b'solution', b'like', b'x,', b'y', b'such', b'that', b'y', b'is', b'19-bit:', b'n']
[DEBUG] Sent 0x2e bytes:
    b'90733961161770834421760416122416141408,462541n'
[DEBUG] Received 0x4e bytes:
    b'| Congrats, you got the flag: CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}n'
```



```
#!/usr/bin/env python3

from base64 import b64encode
from flag import flag

def encrypt(msg):
 ba = b64encode(msg.encode('utf-8'))
 baph, key = '', ''

 for b in ba.decode('utf-8'):
  if b.islower():
   baph += b.upper()
   key += '0'
  else:
   baph += b.lower()
   key += '1'

 baph = baph.encode('utf-8')
 key = int(key, 2).to_bytes(len(key) // 8, 'big')

 enc = b''
 for i in range(len(baph)):
  enc += (baph[i] ^ key[i % len(key)]).to_bytes(1, 'big')

 return enc

enc = encrypt(flag)
f = open('flag.enc', 'wb')
f.write(enc)
f.close()
```



```
#!/usr/bin/env python3
#
with open("flag.enc","rb") as f:
 enc = f.read()
print(len(enc))

from base64 import b64encode,b64decode
msg=b"CCTF{"
ba = b64encode(msg)
baph, key = '', ''
for b in ba.decode('utf-8'):
 if b.islower():
  baph += b.upper()
  key += '0'
 else:
  baph += b.lower()
  key += '1'

baph = baph.encode('utf-8')[:6]
print(baph)

key = b""
for i in range(len(baph)):
 key += (baph[i] ^ enc[i]).to_bytes(1, 'big')
print(key)

dec = b""
for i in range(len(enc)):
 dec += (enc[i] ^ key[i % len(key)]).to_bytes(1, 'big')
print(dec)

flag=""
for b in dec.decode('utf-8'):
 if b.islower():
  flag += b.upper()
 else:
  flag += b.lower()
print(b64decode(flag.encode('utf-8')))
#key = int(key, 2).to_bytes(len(key) // 8, 'big')
```



```
48
b'q0nurN'
b'xf9bxadxacNxff'
b'q0nurNTvCfaZCL8WuL9St3DfuL8Xn1PFDeGZx1bYmgjmm019'
b'CCTF{UpP3r_0R_lOwER_17Z_tH3_Pr0bL3M}'
[Finished in 0.2s]
```



```
nc 05.cr.yp.toc.tf 37331
```



```
[root@VM-0-7-centos ~]# nc 05.cr.yp.toc.tf 37331
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hey math experts, in this challenge we will deal with the numbers   |
|  those are the sum of two perfect square, now try hard to find them! |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| Generating the `n', please wait...
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
G
| n = 1243565868390316746681363697659435925395524656187056587629633961874200469
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
S
| Send your pair x, y here:
```



```
# sagemath

sage: two_squares(5545629715339564937545617256977338230363684107665849984098838446686735017)
(1166738044093249132248421369078945211, 2045568882195127737861825295828693636)
```



```
root@VM-0-7-centos ~]# nc 05.cr.yp.toc.tf 37331
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hey math experts, in this challenge we will deal with the numbers   |
|  those are the sum of two perfect square, now try hard to find them! |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| Generating the `n', please wait...
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
g
| n = 5545629715339564937545617256977338230363684107665849984098838446686735017
| Options: 
| [G]et the n 
| [S]olve the challenge! 
| [Q]uit
s
| Send your pair x, y here: 
2010025793396973084655790372917576051,1226958037268770577663190958375036304
| Congratz! the flag is CCTF{3Xpr3sS_4z_Th3_sUm_oF_7w0_Squ4rE5!}
```



```
#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def keygen(nbit = 64):
 while True:
  k = getRandomNBitInteger(nbit)
  p = k**6 + 7*k**4 - 40*k**3 + 12*k**2 - 114*k + 31377
  q = k**5 - 8*k**4 + 19*k**3 - 313*k**2 - 14*k + 14011
  if isPrime(p) and isPrime(q):
   return p, q

def encrypt(msg, n, e = 31337):
 m = bytes_to_long(msg)
 return pow(m, e, n)

p, q = keygen()
n = p * q
enc = encrypt(flag, n)
print(f'n = {n}')
print(f'enc = {enc}')
```



```
n = 44538727182858207226040251762322467288176239968967952269350336889655421753182750730773886813281253762528207970314694060562016861614492626112150259048393048617529867598499261392152098087985858905944606287003243
enc = 37578889436345667053409195986387874079577521081198523844555524501835825138236698001996990844798291201187483119265306641889824719989940722147655181198458261772053545832559971159703922610578530282146835945192532
R.<k> = ZZ[]

p = k**6 + 7*k**4 - 40*k**3 + 12*k**2 - 114*k + 31377
q = k**5 - 8*k**4 + 19*k**3 - 313*k**2 - 14*k + 14011

f = p*q-n
x = f.roots()[0][0]

pp=p(x)
qq=q(x)
phi = (pp-1)*(qq-1)
d = inverse_mod(31337,phi)
from Crypto.Util.number import *
print(long_to_bytes(pow(enc,d,n)))
```



```
b'CCTF{F4C70r!N9_tRIcK5_aR3_fUN_iN_RSA?!!!}'
```



```
#!/usr/bin/env python3

from Crypto.Util.number import *
from os import urandom

class TaylorSeries():

 def __init__(self, order):
  self.order = order
  
 def coefficient(self, n):
  i = 0
  coef = 1
  while i < n:
   i += 1
   coef *= (coef * (1/2-i+1)) / i
  return coef

 def find(self, center):
  sum = 0
  center -= 1
  i = 0
  while i < self.order:
   sum += (center**(1/2-i) * self.coefficient(i))
   i += 1
  return sum

def xor(cip, key):
 repeation = 1 + (len(cip) // len(key))
 key = key * repeation
 key = key[:len(cip)]
 
 msg = bytes([c ^ k for c, k in zip(cip, key)])
 return msg

# If you run these 3 functions (diamond, triage, summarize) with big numbers, they will never end
# You need to optimize them first

def diamond(num):
 output = 0
 for i in range(num):
  output += i*2 + 1
 return output

def triage(num):
 output = 0
 index = 0
 for i in range(num):
  output += (i+index)*6 + 1
  index += i
 return output

def summarize(b):
 order = getRandomRange(1000, 2000)
 t = TaylorSeries(order)
 output = 0
 
 i = 2
 while i < b:
  b1 = t.find(i)
  b2 = t.find(i+1)
  output += (b1+b2) / 2
  i += 1
 return output

KEY_SIZE = 2048
p, q = [getPrime(KEY_SIZE) for _ in '01']

e, n = 0x10001, p*q

f = open ('./message.txt', 'rb')
message = f.read()
f.close()
msg_length = len(message)
padded_msg = message + urandom(len(long_to_bytes(n)) - msg_length)
padded_msg_length = len(padded_msg)

xor_key = long_to_bytes(int(summarize(n)))[:padded_msg_length]
assert(len(xor_key) == 512)

enc0 = xor(padded_msg, xor_key)
assert(bytes_to_long(enc0) < n)

c0 =  abs(diamond(p) - diamond(q))
c1 =  triage(p)
c1 += 3*n*(p+q)
c1 += triage(q)

m = bytes_to_long(enc0)
enc1 = pow(m, e, n)

print(f"c0 = {c0}")
print(f"c1 = {c1}")
print(f"enc = {enc1}")
```



```
def xor(cip, key):
 repeation = 1 + (len(cip) // len(key))
 key = key * repeation
 key = key[:len(cip)]
 msg = bytes([c ^^ k for c, k in zip(cip, key)])
 return msg

c0 = 194487778980461745865921475300460852453586088781074246328543689440168930873549359227127363759885970436167330043371627413542337857082400024590112412164095470165662281502211335756288082198009158469871465280749846525326701136380764079685636158337203211609233704905784093776008350120607841177268965738426317288541638374141671346404729428158104872411498098187946543666987926130124245185069569476433120128275581891425551325847219504501925282012199947834686225770246801353666030075146469275695499044424390475398423700504158154044180028733800154044746648133536737830623670383925046006108348861714435567006327619892239876863209887013290251890513192375749866675256952802329688897844132157098061758362137357387787072005860610663777569670198971946904157425377235056152628515775755249828721767845990597859165193162537676147173896835503209596955703313430433124688537275895468076469102220355973904702901083642275544954262724054693167603475188412046722656788470695566949847884250306735314144182029335732280420629131990311054229665691517003924788583771265625694414774865289407885678238795596912006567817508035434074250123869676396153982762032750080222602796273083162627489526255501643913672882350236497429678928099868244687228703074267962827621792960
c1 = 102325064080381160170299055162846304227217463467232681115953623386548494169967745781550171804781503102663445039561476870208178139548389771866145006535051362059443515034504958703659546162037904784821960707630188600064568878674788077706711506213779443920430038560373854184526850365974450688458342413544179732143225845085164110594063440979455274250021370090572731855665413325275414458572412561502408983107820534723804225765540316307539962199024757378469001612921489902325166003841336027940632451584642359132723894801946906069322200784708303615779699081247051006259449466759863245508473429631466831174013498995506423210088549372249221415401309493511477847517923201080509933268996867995533386571564898914042844521373220497356837599443280354679778455765441375957556266205953496871475611269965949025704864246188576674107448587696941054123618319505271195780178776338475090463487960063464172195337956577785477587755181298859587398321270677790915227557908728226236404532915215698698185501562405374498053670694387354757252731874312411228777004316623425843477845333936913444143768519959591070492639650368662529749434618783626718975406802741753688956961837855306815380844030665696781685152837849982159679122660714556706669865596780528277684800454866433826417980212164051043504955615794706595412705883261111953152250227679858538249797999044336210905975316421254442221408945203647754303635775048438188044803368249944201671941949138202928389951227347433255867504906597772044398973241425387514239164853656233776024571606159378910745571588836981735827902305330330946219857271646498602227088657739442867033212012876837654750348578740516798444734534291467314881324902354425889448102902750077077381896216130734894767553834949561471219923459897244690006643798812989271282475503126962274052192342840870308710338336817452628324667507548265612892611100350882163205858101959976
enc = 122235247669762131006183252122503937958296387791525458429403709404875223067116491817728568224832483391622109986550732469556761300197133827976956875865159629512476600711420561872409721582387803219651736262581445978042694384374119142613277808898398213602093802571586386354257378956087240174787723503606671543195193114158641301908622673736098768829071270132073818245595918660134745516367731595853832524328488074054536278197115937409643221809577554866060292157239061557708159310445977052686561229611117673473208278176118561352693319461471419694590218295911647368543698198762827636021268989705079848502749837879584394379300566277359149621932579222865430374652678738198451655509408564586496375811666876030847654260305392984710580761255795785508407844683687773983669843744274915862335181251050775093896006210092665809300090715190088851654138383362259256212093670748527819287681468901379286722214112321906917311154811516336259463356911326393701445497605365038857575515541024824906818473933597129846235905072394148879079996812146836910199111439031562946495046766063326815863624262541346543552652673629442370320109404700346028639853707278295255350982238521659924641921142615894039995513480511108116053798143154593343124822462519555715118822045

var('p,q')

f1 = p^2-q^2 - c0
f2 = (p+q)^3 - c1

#solve([f1,f2],p,q)
p=25465500595039564722385454268618341460440964303654692306893194812608651011894765148023201769023925823267446913594798724374078776058926548056279105656348138942211069695157129067986030357247987537066065195208337853580939616954961742954173270603234042184081995050125067398704045490448077961447418406856674045777724275017678698252609741079175784928310951915104807404003531834525200421059550762294584722178356010146438598799668537922242765662363844939035164178525445220653839693135494967926642943210917823981779895464411806829004306900926935124663285407830585204630912848783431051369106939431567473170247979142455819150893
q=21307368246113800130311098641506744510559988209047095448061577734947715969121645982743962584143752085867914325394457857827478912559095766977509129246922499990951138184298921892924074303356650532229644986118338361761354192554363128824141104808606558539422865199413633150757655174985683830034245659632460363700309887626934298289805670092066041542014924213128271705967504359900458092855272034197878632989626323553684162988741101770565319360726673172671459797955787997515498457867020749156835947018833861229200382521269341946614058721285386773372009177934062994798868703374266787876752211055631019633581263575312198649933
phi=(p-1)*(q-1)
e=0x10001
from Crypto.Util.number import *
d=inverse(e,phi)
n = p*q
padded_msg = long_to_bytes(pow(enc,d,n))

xor_key = long_to_bytes(int(2/3*n^(3/2)))[:512]
enc0 = xor(padded_msg, xor_key)
print(enc0)
```



```
b'Never heard of using taylor series and integral beside RSA?!nBut there are always ways to make things complicatednnCCTF{Mix1ng_c4lcUluS_w17h_Numb3r_The0Rry_S33ms_s7r0ng_cRyp70_Sch3m4!!}nnWe compute integrals with just measuring the area with a little fraction, forget about tough works!nGood luck with the rest of CryptoCTF2022x9ax92Wxcfxa2dlx1ax91x96'x88xecxfezxcdxc2xe7x0bCx90xa3xc7xe7Uxb4Fxa535Vx19x9bx9exd4xf7xe7Xx02x19Yx86xfax9fx0b!x9axc1xd2xcayGx8af/x14xefxf9x1dxc2x9axcbx9da}g8xb8\ 2~xf3xe3xb6$xb6ix12xd6x82xfacx15xeeVa[sxa0Sx00yx0cx18xc34xbdx96fdxecxcfxb9x02<Qx8bxb8x9dxd5xefDuxdaxd2xf0xc6gx97xf8x952x0crs=x19.x11"x08x81xe7*x87xb8xbd>x82n~xf7l,tux96}*xab`x17xe7xf4xd7N^xe3xfexf3@x1ex1cx15xffCxecVVrxcax8dx03xc5xdaxd6xbf=xc6x14+xf2x14N'
```



```
#!/usr/bin/env python3

from Crypto.Util.number import *
import string
from flag import flag

def randstr(l):
 rstr = [(string.printable[:62] + '_')[getRandomRange(0, 62)] for _ in range(l)]
 return ''.join(rstr)

def encrypt(msg, l):
 while True:
  rstr = 'CCTF{it_is_fake_flag_' + randstr(l) + '_90OD_luCk___!!}'
  p = bytes_to_long(rstr.encode('utf-8'))
  q = bytes_to_long(rstr[::-1].encode('utf-8'))
  if isPrime(p) and isPrime(q):
   n = p * q
   e, m = 65537, bytes_to_long(msg.encode('utf-8'))
   c = pow(m, e, n)
   return n, c

n, c = encrypt(flag, 27)

print(f'n = {n}')
print(f'c = {c}')
```



```
n = 23087202318856030774680571525957068827041569782431397956837104908189620961469336659300387982516148407611623358654041246574100274275974799587138270853364165853708786079644741407579091918180874935364024818882648063256767259283714592098555858095373381673229188828791636142379379969143042636324982275996627729079
c = 3621516728616736303019716820373078604485184090642291670706733720518953475684497936351864366709813094154736213978864841551795776449242009307288704109630747654430068522939150168228783644831299534766861590666590062361030323441362406214182358585821009335369275098938212859113101297279381840308568293108965668609

from Crypto.Util.number import *

phigh = bytes_to_long(b"CCTF{it_is_fake_flag_")
plow = bytes_to_long(b'_90OD_luCk___!!}')
P.<x> = PolynomialRing(Zmod(n))
f = (phigh << 344) + (x * 2^128) + plow
x0 = f.monic().small_roots(X=2^216, beta=0.4,epsilon=0.02)[0]
p = int(f(x0))
q = n//p
e = 65537
phi = (p-1)*(q-1)
d = inverse(e,phi)
print(long_to_bytes(pow(c,d,n)))
```



```
'Congratz, the flag is: CCTF{h0M3_m4dE_k3Y_Dr1vEn_CrYp7O_5ySTeM!}'
```



```
nc 02.cr.yp.toc.tf 17113
```



```
#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import gensol, nbit_gensol
from flag import flag

m = bytes_to_long(flag.encode('utf-8'))
print(m)

a = 1337
b = 31337

def die(*args):
 pr(*args)
 quit()

def pr(*args):
 s = " ".join(map(str, args))
 sys.stdout.write(s + "n")
 sys.stdout.flush()

def sc():
 return sys.stdin.readline().strip()

def main():
 border = "|"
 pr(border*72)
 pr(border, "Welcome crypto guys! Here we are looking for the solution of special", border)
 pr(border, "Diophantine equation: 1337(z^4 - x^2) = 31337(y^2 - z^4) in natural ", border)
 pr(border, "numbers, in each stage solve the equation in mentioned interval :)  ", border)
 pr(border*72)

 STEP, level = 0, 19

 while True:
  p, q = nbit_gensol(1337, 31337, STEP + 30)
  x, y, z = gensol(a, b, p, q)
  pr(border, f"Send a solution like `x, y, z' such that the `z' is {STEP + 30}-bit: ")
  ans = sc()
  try:
   X, Y, Z = [int(_) for _ in ans.split(',')]
   NBIT = Z.bit_length()
  except:
   die(border, 'Your input is not valid, Bye!')
  if 1337*(Z**4 - X**2) == 31337*(Y**2 - Z**4) and NBIT == STEP + 30:
   if STEP == level - 1:
    die(border, f'Congrats, you got the flag: {flag}')
   else:
    pr('| good job, try to solve the next challenge :P')
    STEP += 1
  else:
   die(border, 'your answer is not correct, Bye!!')

if __name__ == '__main__':
 main()
```



```
from Crypto.Util.number import *
from sympy import *

from pwn import *
context.log_level = 'debug'
sh = remote("02.cr.yp.toc.tf",17113)
for i in range(30,49):
 ch = sh.recvuntil("-bit: n")
 z = getPrime(i)
 x = z**2
 y = x
 sh.sendline(str(x)+","+str(y)+","+str(z))
sh.interactive()
```



```
| Congrats, you got the flag: CCTF{4_diOpH4nT1nE_3Qua7i0n__8Y__Jekuthiel_Ginsbur!!}
```



```
http://03.cr.yp.toc.tf:11117/
```



```
{"flag": "ZZNVH EOOAA JSGPB DAKCP MQRGM MBXDT NAULS MYJRI USVAY WQGUK KEWRJ BAPPW YDWQU KFDHC OOOWF QVANE XLEEK MVFBX HYQOR SFKGU AKWEB LEPXV LHRCG MKMSO DVOZS JFESS LTUEY QUGAA IODSI IZEQJ ROTBS TKSEH JBORC ZZNVH EOOAA"}

{"flag": "GGMCT NJOAA QAEYB FJZLP VKZTA DHIIG RVYGC RPQQN LHWRR YSDXM YDSJL ZUROG KHXNX DGPSM PPEBK INKSS WEVSH ZNEKW OTZNR NFLYQ KLIRC JVWLI PSNBF OEFHC NDUVO CABZC LCTEN NMDSI XVDEL DRADR YIPBQ IKOLM DJAQA GGMCT NJOAA"}

{"flag": "IISNJ IFFAA TYPMO WDJHA ZMNBD LKUAY TYPVD UGAYU OQMOO YRVUS SLFZI IXKVW LYUGT JWTYV XNEYU HLQVV IXUMJ BKNUQ WMLQT QKIWV UXOCA CVSPG UKJQG XCSFI RJEKU BWLBM AVRFW DMOPT VFXTD VROND XSEHF ZLWEJ VOVSX IISNJ IFFAA"}

{"flag": "BBHAC QDFAA KGBMH RVZSK RNVZH NGRAM WYHHE HKHJU UCQBL HPVAP TXDCZ ZMKWX ETCKC CMBSC VKUUF BMAIV RTAJE EWOUS SMOTQ KNQBF IRDVZ YJWQK WEAIA TONBI MMBUI RCULP BKEIO LNOAM XLUDR XJYAM DMWJN DUXXV FDVOC BBHAC QDFAA"}
```



```
A
{"cipher": "BBHAC QDFAA IXXXX BBHAC QDFAA"}
AA
{"cipher": "BBHAC QDFAA IUXXX BBHAC QDFAA"}
AAA
{"cipher": "BBHAC QDFAA IUVXX BBHAC QDFAA"}
B
{"cipher": "BBHAC QDFAA HXXXX BBHAC QDFAA"}
BB
{"cipher": "BBHAC QDFAA HTXXX BBHAC QDFAA"}
C
{"cipher": "BBHAC QDFAA GXXXX BBHAC QDFAA"}
```



```
'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
{"cipher": "BBHAC QDFAA IUVLR EJVRR FJUSV MLFRY WRGMP HQGSO MVPQF AOPPR HJLPF YXOPQ IKUJY KFIAP UMOLQ ZLBZV TXSIJ SHZIO WPNUO JPSUK HFREL NVZTS TGLVN PTGFR GYGRS STPGB PZWTG DYITJ SOPQU JHWPT SIBSE QDYSW TPPMT BBHAC QDFAA"}
```



```
TABLE="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

CIPHER = "BBHAC QDFAA IUVLR EJVRR FJUSV MLFRY WRGMP HQGSO MVPQF AOPPR HJLPF YXOPQ IKUJY KFIAP UMOLQ ZLBZV TXSIJ SHZIO WPNUO JPSUK HFREL NVZTS TGLVN PTGFR GYGRS STPGB PZWTG DYITJ SOPQU JHWPT SIBSE QDYSW TPPMT BBHAC QDFAA".replace(" ","")

FLAGENC= "BBHAC QDFAA KGBMH RVZSK RNVZH NGRAM WYHHE HKHJU UCQBL HPVAP TXDCZ ZMKWX ETCKC CMBSC VKUUF BMAIV RTAJE EWOUS SMOTQ KNQBF IRDVZ YJWQK WEAIA TONBI MMBUI RCULP BKEIO LNOAM XLUDR XJYAM DMWJN DUXXV FDVOC BBHAC QDFAA".replace(" ","")

PLAINTEXT = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

KEY = ""
FLAG = ""
for i in range(155):
 KEY += TABLE[(TABLE.index(CIPHER[i])+TABLE.index(PLAINTEXT[i]))%26]

for i in range(155):
    FLAG += TABLE[(TABLE.index(KEY[i]) - TABLE.index(FLAGENC[i]))%26]
print(FLAG)
print(FLAG.replace("Z"," "))
```



```
# YOUZKNOWZHOWZTOZFORMATZFLAGZJUSTZPUTZUPCOMINGZLETTERSZWITHINZCURLYZBRACESZFOLLOWEDZBYZCCTFZOOJMPMDDIXCLNNWFTEJUMFXKBRVVMOPSLSSLUTXVDVNDMYYPHPWFJRNJBVBOMUYR

# YOU KNOW HOW TO FORMAT FLAG JUST PUT UPCOMING LETTERS WITHIN CURLY BRACES FOLLOWED BY CCTF OOJMPMDDIXCLNNWFTEJUMFXKBRVVMOPSLSSLUTXVDVNDMYYPHPWFJRNJBVBOMUYR
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1664160186.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/1-1664160187.png)