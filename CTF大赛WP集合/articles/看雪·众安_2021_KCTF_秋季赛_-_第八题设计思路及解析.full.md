---
title: 看雪·众安 2021 KCTF 秋季赛 | 第八题设计思路及解析
contest: 看雪·众安 2021 KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: reverse
tags:
- Android CrackMe
- ArmVMP
- DES加密
- Frida hook
- 轮密钥swap
- libart.so hook
- NewStringUTF
- 双输入name/serial
- 双重DES
attack_chain: IDA发现DES→Frida hook 0x789打印参数→输入转hex再加密+相同内容再加密→swap 48个轮密钥倒序→hook libart NewStringUTF("恭喜成功")→同一name不同serial+不同name同serial 爆破得正确密文→DES解密
key_payload: Frida hook sub_788 DES;swapkey(48轮密钥倒序);encdata1=[0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4];encdata2=[0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5];hex=638f6773593bd91d788e891e6cf42efa
one_liner: 看雪众安KCTF2021秋Q8《群狼环伺》Android CrackMe：双重DES+Frida hook 48轮密钥倒序+双输入爆破
lesson: DES轮密钥swap函数可解密；hook NewStringUTF+debugger断点爆破
quality: high
full_path: 看雪·众安_2021_KCTF_秋季赛_-_第八题设计思路及解析.full.md
meta_path: 看雪·众安_2021_KCTF_秋季赛_-_第八题设计思路及解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 看雪·众安 2021 KCTF 秋季赛 | 第八题设计思路及解析。看雪众安KCTF2021秋Q8《群狼环伺》Android CrackMe：双重DES+Frida hook 48轮密钥倒序+双输入爆破。经验：DES轮密钥swap函数可解密；hook NewStringUTF+debugger断点爆破
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/15720.html
reasoning_chain:
- Android CrackMe ArmVMP保护 → 触发点：很多函数被VM化
- 假设：IDA搜密码学常量找DES → 动作：发现DES后查找引用
- 观察：sub_788是DES过程 → 下一步：手动Create Function识别未识别函数
- Frida hook baseAddr.add(0x789) → 触发点：打印Enc Data/Key/Output三参数
- 假设：双重DES结构（输入转hex+加密+相同再加密）→ 动作：观察hexdump
- 观察：可倒序48个轮密钥swap解密 → 动作：写swapkey函数addr.add(i*8).readU64
- hook libart baseAddr.add(0xae765) NewStringUTF("恭喜成功") → 触发点：断点命中
- 假设：固定name变serial + 固定serial变name → 动作：双方向爆破
- 观察：encdata1+encdata2两密文 → 再次swap回原序 → DES解密得hex
failed_attempts:
- 试图不解双重DES直接逆向 → 失败：双重嵌套+swap密钥顺序复杂
- 试图用unidbg而不是Frida → 失败：unidbg在ArmVMP下不友好
- 忽略swap 48轮密钥 → 失败：DES默认密钥顺序得到错误结果
key_observations:
- ArmVMP保护下手动Create Function识别DES是关键
- Frida hook 0x789入口+0xae765 NewStringUTF双断点
- 48轮DES密钥swap（u64读+倒序写）可解密
- 双输入爆破=固定一个变另一个找密文
- NewStringUTF("恭喜成功") + debugger命中是动态爆破标志
prerequisites:
- ArmVMP保护机制理解
- Frida hook Java/Native API
- DES算法结构与轮密钥生成
- Android JNI/libart.so基础
---
# 看雪·众安 2021 KCTF 秋季赛 | 第八题设计思路及解析

> 原文: https://www.ctfiot.com/15720.html
> ID: 15720

看雪·众安 2021 KCTF秋季赛的第八题《群狼环伺》已于今天中午12点截止答题！

本题共有3支战队成功破解，分别是辣鸡战队、金左手、mininep。

恭喜辣鸡战队用时100442秒拿下“一血”，接下来和我一起来看看该赛题的设计思路和相关解析吧~

出题团队简介

第八题《群狼环伺》出题方： 【ArmVMP】战队

赛题设计思路

赛题解析

本赛题解析由看雪论坛ThTsOd给出：

IDA上来一看，没啥函数：

找一下密码学常量，发现有个DES：

查找引用：

发现有部分函数没有识别，手动Create Function。

sub_788就是DES过程了，hook下打印三个参数：

Interceptor.attach(baseAddr.add(0x789),{ onEnter: function (args){ console.log((this.context as any).lr.sub(baseAddr)); console.log(JSON.stringify(this.context)); console.log(hexdump((this.context as any).r0,{ offset:0, length:
128*3, header:
true, ansi:
true })); //Enc Data console.log(hexdump((this.context as any).r1,{ offset:0, length:8, header:
true, ansi:
true })); }, onLeave: function (ret){ //After Enc console.log(hexdump((this.context as any).r2,{ offset:0, length:8, header:
true, ansi:
true })); }});

可以看到将输入转成hex再转hex后，加密了一次，随后是加密相同的内容：

这里可以将DES轮秘钥倒过来，解密。

function swapkey(addr:
NativePointer){ var key = [] for(var i = 0;i<48;i+=1){ key.push(addr.add(i*8).readU64()); } for(var i = 0;i<48;i+=1){ addr.add(i*8).writeU64(key[47-i]); }}

当提交成功时，会出现”恭喜成功”，但是在java层代码和native层代码没有找到这个字符串，这里无意尝试把以下内容修改了。

程序崩溃，查看logcat：

UTF-8转换相关，hook下libart.so的CheckJNI::
NewStringUTF(dump自己的so文件，ida找一下这个函数)

Interceptor.attach(baseAddr.add(0xae765), { onEnter: function (args){ //console.log(args[1].readCString(),args[1]); if(args[1].readCString() == "恭喜成功" || args[1].readCString() == "输入错误"){ var mainAddr = Module.findBaseAddress("libcrackme.so"); console.log((this.context as any).lr.sub(mainAddr)); for(var i=0;i<64;i++){ //console.log((this.context as any).sp.add(i*4).readPointer(),(this.context as any).sp.add(i*4).readPointer().sub(mainAddr)); } console.log(hexdump(args[1])); console.log(JSON.stringify(this.context)); console.log(hexdump(this.context.sp.add(0xB0),{ offset:0, length:
192, header:
true, ansi:
true })); debugger; } }, onLeave: function (ret){ } });

这样可以在判断完结果后将程序断下（frida的debugger命中会暂停当前线程）。

搜一下正确输入的加密结果，运行程序时保持name相同，serial不同。

bd 3a b0 69 39 40 f8 cd 42 0d e3 8a 79 db 52 bd

找到一个：

运行程序时保持name不同（这里输入KCTF），serial相同。

同样也找到一个：

这时就能猜出DES加密结果应该为：

45 68 97 A3 29 2A 7F D4 F5 90 73 57 46 02 AE D5

就可以得到正确答案了。

if(true){ //DES Decrypt swapkey((this.context as any).r0); //Data 1 if((this.context as any).lr.sub(baseAddr) == 0xe8b5){ var encdata = [0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4]; (this.context as any).r1.writeByteArray(encdata); } //Data 2 if((this.context as any).lr.sub(baseAddr) == 0xe8e5){ var encdata = [0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5]; swapkey((this.context as any).r0);//Swap Again (this.context as any).r1.writeByteArray(encdata); }}

应该输入的hex 为 63 8f 67 73 59 3b d9 1d 78 8e 89 1e 6c f4 2e fa

再转换一次： 3633386636373733353933626439316437383865383931653663663432656661，即为正确答案。

部分代码如下：

function swapkey(addr:
NativePointer){ var key = [] for(var i = 0;i<48;i+=1){ key.push(addr.add(i*8).readU64()); } for(var i = 0;i<48;i+=1){ addr.add(i*8).writeU64(key[47-i]); }} function hook(){ var baseAddr = Module.findBaseAddress("libcrackme.so"); Interceptor.attach(baseAddr.add(0x789), { onEnter: function (args){ console.log((this.context as any).lr.sub(baseAddr)); //console.log(JSON.stringify(this.context)); // console.log(hexdump((this.context as any).r0,{ // offset:0, // length:
128*3, // header:
true, // ansi:
true // })); if(true){ //DES Decrypt swapkey((this.context as any).r0); //Data 1 if((this.context as any).lr.sub(baseAddr) == 0xe8b5){ var encdata = [0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4]; (this.context as any).r1.writeByteArray(encdata); } //Data 2 if((this.context as any).lr.sub(baseAddr) == 0xe8e5){ var encdata = [0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5]; swapkey((this.context as any).r0);//Swap Again (this.context as any).r1.writeByteArray(encdata); } } //Enc Data console.log(hexdump((this.context as any).r1,{ offset:0, length:8, header:
true, ansi:
true })); }, onLeave: function (ret){ //After Enc console.log(hexdump((this.context as any).r2,{ offset:0, length:8, header:
true, ansi:
true })); } } );} function hookart(){ var baseAddr = Module.findBaseAddress("/system/lib/libart.so"); //var baseAddr = Module.findExportByName(null,"_ZN3art12_GLOBAL__N_18CheckJNI12NewStringUTFEP7_JNIEnvPKc"); console.log("Art",baseAddr) Interceptor.attach(baseAddr.add(0xae765), { onEnter: function (args){ //console.log(args[1].readCString(),args[1]); if(args[1].readCString() == "恭喜成功" || args[1].readCString() == "输入错误"){ var mainAddr = Module.findBaseAddress("libcrackme.so"); console.log((this.context as any).lr.sub(mainAddr)); for(var i=0;i<64;i++){ //console.log((this.context as any).sp.add(i*4).readPointer(),(this.context as any).sp.add(i*4).readPointer().sub(mainAddr)); } console.log(hexdump(args[1])); console.log(JSON.stringify(this.context)); console.log(hexdump(this.context.sp.add(0xB0),{ offset:0, length:
192, header:
true, ansi:
true })); debugger; } }, onLeave: function (ret){ } } );}

往期解析

1、看雪·众安 2021 KCTF 秋季赛 | 第二题设计思路及解析

2、看雪·众安 2021 KCTF 秋季赛 | 第三题设计思路及解析

3、看雪·众安 2021 KCTF 秋季赛 | 第四题设计思路及解析

4、看雪·众安 2021 KCTF 秋季赛 | ‍第五题设计思路及解析

5、看雪·众安 2021 KCTF 秋季赛 | 第六题设计思路及解析

6、看雪·众安 2021 KCTF 秋季赛 | 第七题设计思路及解析

?还在等什么，快来参赛吧！

– End –

公众号ID：ikanxue

官方微博：看雪安全

商务合作：wsc@kanxue.com

球分享

球点赞

球在看

戳“阅读原文”展开第9题的角逐！


```
Interceptor.attach(baseAddr.add(0x789),{ onEnter: function (args){ console.log((this.context as any).lr.sub(baseAddr)); console.log(JSON.stringify(this.context)); console.log(hexdump((this.context as any).r0,{ offset:0, length:
128*3, header:
true, ansi:
true })); //Enc Data console.log(hexdump((this.context as any).r1,{ offset:0, length:8, header:
true, ansi:
true })); }, onLeave: function (ret){ //After Enc console.log(hexdump((this.context as any).r2,{ offset:0, length:8, header:
true, ansi:
true })); }});
function swapkey(addr:
NativePointer){ var key = [] for(var i = 0;i<48;i+=1){ key.push(addr.add(i*8).readU64()); } for(var i = 0;i<48;i+=1){ addr.add(i*8).writeU64(key[47-i]); }}
Interceptor.attach(baseAddr.add(0xae765), { onEnter: function (args){ //console.log(args[1].readCString(),args[1]); if(args[1].readCString() == "恭喜成功" || args[1].readCString() == "输入错误"){ var mainAddr = Module.findBaseAddress("libcrackme.so"); console.log((this.context as any).lr.sub(mainAddr)); for(var i=0;i<64;i++){ //console.log((this.context as any).sp.add(i*4).readPointer(),(this.context as any).sp.add(i*4).readPointer().sub(mainAddr)); } console.log(hexdump(args[1])); console.log(JSON.stringify(this.context)); console.log(hexdump(this.context.sp.add(0xB0),{ offset:0, length:
192, header:
true, ansi:
true })); debugger; } }, onLeave: function (ret){ } });
if(true){ //DES Decrypt swapkey((this.context as any).r0); //Data 1 if((this.context as any).lr.sub(baseAddr) == 0xe8b5){ var encdata = [0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4]; (this.context as any).r1.writeByteArray(encdata); } //Data 2 if((this.context as any).lr.sub(baseAddr) == 0xe8e5){ var encdata = [0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5]; swapkey((this.context as any).r0);//Swap Again (this.context as any).r1.writeByteArray(encdata); }}
function swapkey(addr:
NativePointer){ var key = [] for(var i = 0;i<48;i+=1){ key.push(addr.add(i*8).readU64()); } for(var i = 0;i<48;i+=1){ addr.add(i*8).writeU64(key[47-i]); }} function hook(){ var baseAddr = Module.findBaseAddress("libcrackme.so"); Interceptor.attach(baseAddr.add(0x789), { onEnter: function (args){ console.log((this.context as any).lr.sub(baseAddr)); //console.log(JSON.stringify(this.context)); // console.log(hexdump((this.context as any).r0,{ // offset:0, // length:
128*3, // header:
true, // ansi:
true // })); if(true){ //DES Decrypt swapkey((this.context as any).r0); //Data 1 if((this.context as any).lr.sub(baseAddr) == 0xe8b5){ var encdata = [0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4]; (this.context as any).r1.writeByteArray(encdata); } //Data 2 if((this.context as any).lr.sub(baseAddr) == 0xe8e5){ var encdata = [0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5]; swapkey((this.context as any).r0);//Swap Again (this.context as any).r1.writeByteArray(encdata); } } //Enc Data console.log(hexdump((this.context as any).r1,{ offset:0, length:8, header:
true, ansi:
true })); }, onLeave: function (ret){ //After Enc console.log(hexdump((this.context as any).r2,{ offset:0, length:8, header:
true, ansi:
true })); } } );} function hookart(){ var baseAddr = Module.findBaseAddress("/system/lib/libart.so"); //var baseAddr = Module.findExportByName(null,"_ZN3art12_GLOBAL__N_18CheckJNI12NewStringUTFEP7_JNIEnvPKc"); console.log("Art",baseAddr) Interceptor.attach(baseAddr.add(0xae765), { onEnter: function (args){ //console.log(args[1].readCString(),args[1]); if(args[1].readCString() == "恭喜成功" || args[1].readCString() == "输入错误"){ var mainAddr = Module.findBaseAddress("libcrackme.so"); console.log((this.context as any).lr.sub(mainAddr)); for(var i=0;i<64;i++){ //console.log((this.context as any).sp.add(i*4).readPointer(),(this.context as any).sp.add(i*4).readPointer().sub(mainAddr)); } console.log(hexdump(args[1])); console.log(JSON.stringify(this.context)); console.log(hexdump(this.context.sp.add(0xB0),{ offset:0, length:
192, header:
true, ansi:
true })); debugger; } }, onLeave: function (ret){ } } );}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]