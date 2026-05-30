# AI-SEARCH-INDEX — CTF知识库全局检索索引

> **用途**: AI Agent 在收到CTF问题时，先读本文件定位资源，再按需加载具体文章/脚本。
> **更新**: 文章/工具/脚本增删时同步更新本索引。
> **Skill**: 使用 `/ctf-solver` 调用CTF解题助手（5种模式：Payload速查/WP搜索/工具推荐/技术速查/完整方案）
>
> **2026-05 新增**:
> - [PAYLOAD-CHEATSHEET.md](PAYLOAD-CHEATSHEET.md) — 10大类高频Payload速查表（做题时直接查，不用翻文章）

---

## 零、快速入口（新）

| 我想要的 | 最快路径 |
|---------|---------|
| Payload/命令 | → [PAYLOAD-CHEATSHEET.md](PAYLOAD-CHEATSHEET.md) (直接翻对应章节) |
| 找相似WP | → 直接 grep 关键词搜索 [CTF大赛WP集合/articles/](CTF大赛WP集合/articles/) |
| 了解漏洞原理 | → 读 `.idx.md` 定位 → `Read offset=X limit=Y` 读知识文章 |
| 找现成脚本 | → [SCRIPTS-INDEX.md](CTF常用脚本及工具/SCRIPTS-INDEX.md) (50+脚本速查) |
| 完整解题 | → `/ctf-solver` Skill 模式5 |

---

## 一、按技术标签检索

### SQL注入
- **知识**: [SQL.md](SQL.md) → [SQL.idx.md](SQL.idx.md) (2611行)
- **工具**: [sqlmap速查](工具使用/sqlmap-Cheat-Sheet.md)
- **WP**: [SQLI-LABS](WP汇总/各大靶场WP汇总.md), [ctfshow-php特性](WP汇总/ctfshow-php特性.md)
- **代码审计**: [php代码审计.md](php代码审计.md) L990-L1112 (SQL注入 WITH ROLLUP), L1278-L1322 (sql闭合绕过)
- **关键词**: `联合注入` `报错注入` `堆叠注入` `盲注` `WAF绕过` `宽字节` `二次注入` `DNS注入` `sqlmap`

### 命令执行/RCE
- **知识**: [命令执行.md](命令执行.md) → [命令执行.idx.md](命令执行.idx.md) (3463行)
- **WP**: [ctfshow-命令执行wp](WP汇总/ctfshow-命令执行wp.md)
- **代码审计**: [php代码审计.md](php代码审计.md) (preg_match绕过/变量覆盖可导致RCE)
- **关键词**: `system` `passthru` `exec` `shell_exec` `反弹shell` `无回显` `DNSlog` `disable_functions` `无字母` `通配符`

### 文件上传
- **知识**: [文件上传漏洞.md](文件上传漏洞.md) → [文件上传漏洞.idx.md](文件上传漏洞.idx.md) (2115行)
- **WP**: [ctfshow-文件上传wp](WP汇总/ctfshow-文件上传wp.md), [upload-labs WP](WP汇总/文件上传/README.md)
- **代码审计**: [php代码审计.md](php代码审计.md) L1414 (move_uploaded_file截断)
- **关键词**: `WebShell` `蚁剑` `MIME绕过` `图片马` `.htaccess` `解析漏洞` `截断` `前端绕过`

### 文件包含/LFI
- **知识**: [文件包含.md](文件包含.md) → [文件包含.idx.md](文件包含.idx.md) (2617行)
- **WP**: [文件包含WP](WP汇总/文件包含/README.md)
- **代码审计**: [php代码审计.md](php代码审计.md) L1421 (include截断)
- **关键词**: `php伪协议` `filter` `input` `日志包含` `session包含` `临时文件` `phar` `截断`

### SSRF
- **知识**: [SSRF漏洞.md](SSRF漏洞.md) → [SSRF漏洞.idx.md](SSRF漏洞.idx.md) (1882行)
- **关键词**: `gopher` `redis` `fastcgi` `DNS-rebinding` `dict` `file_get_contents` `curl` `内网`

### PHP反序列化
- **知识**: [PHP反序列化漏洞总结.md](PHP反序列化漏洞总结.md) → [PHP反序列化漏洞总结.idx.md](PHP反序列化漏洞总结.idx.md) (6959行)
- **WP**: [ctfshow-反序列化wp](WP汇总/CTfshow-反序序列化wp.md)
- **脚本**: [python-Picke序列化](CTF常用脚本及工具/python-Picke序列化/)
- **关键词**: `POP链` `phar` `字符逃逸` `wakeup` `SoapClient` `session` `原生类` `魔术方法`

### SSTI
- **知识**: [SSTI.md](SSTI.md) (270+行)
- **WP**: [ctfshow-SSTI](WP汇总/ctfshow-SSTI.md), [ssti入门](WP汇总/ssti入门知识点.md)
- **关键词**: `Jinja2` `Flask` `__mro__` `__subclasses__` `__globals__` `popen`

### JWT
- **知识**: [JWT.md](JWT.md) → [JWT.idx.md](JWT.idx.md) (424行)
- **关键词**: `None算法` `KID注入` `JKU` `HS256` `RS256` `密钥爆破` `jwt-cracker`

### PHP代码审计
- **知识**: [php代码审计.md](php代码审计.md) → [php代码审计.idx.md](php代码审计.idx.md) (1641行)
- **关键词**: `弱类型` `preg_match` `变量覆盖` `extract` `strcmp` `md5碰撞` `intval` `%00截断` `register_globals`

### 图片隐写
- **知识**: [图片隐写.md](图片隐写.md) → [图片隐写.idx.md](图片隐写.idx.md) (892行)
- **脚本**: [图片爆破宽高](CTF常用脚本及工具/图片爆破宽高/), [频域盲水印](CTF常用脚本及工具/频域盲水印/), [RGB转图片](CTF常用脚本及工具/RGB转图片/)
- **工具**: [steghide爆破](CTF常用脚本及工具/steghide爆破密码/)
- **关键词**: `IHDR` `CRC` `LSB` `Stegsolve` `pngcheck` `文件头` `GIF` `JPG` `盲水印`

### 音频隐写
- **知识**: [音频隐写.md](音频隐写.md) (280+行)
- **关键词**: `MP3Stego` `频谱` `波形` `DTMF` `SilentEye` `LSB音频`

### 压缩包
- **知识**: [压缩包总结.md](压缩包总结.md) → [压缩包总结.idx.md](压缩包总结.idx.md) (643行)
- **脚本**: [CRC32爆破](CTF常用脚本及工具/CRC32校验爆破/) (1-5字节), [批量解压](CTF常用脚本及工具/批量解压压缩包+带密码/), [遍历压缩包](CTF常用脚本及工具/遍历读取压缩包文件判断1和0/)
- **关键词**: `ZIP` `RAR` `7z` `CRC` `明文攻击` `伪加密` `掩码` `字典`

### 编码/密码
- **脚本**:
  - Base全家桶: [Base/](CTF常用脚本及工具/Base/) (B16/B32/B64/B85/隐写/异或/字符替换)
  - 古典密码: [rot](CTF常用脚本及工具/rot/), [维吉尼亚](CTF常用脚本及工具/维吉尼亚加密/), [凯撒变体](CTF常用脚本及工具/变异凯撒/), [四方密码](CTF常用脚本及工具/四方密码/), [Nihilist](CTF常用脚本及工具/Nihilist密码/), [toy密码](CTF常用脚本及工具/toy密码/)
  - 现代密码: [RSA综合脚本利用](CTF常用脚本及工具/RSA综合脚本利用/), [DES](CTF常用脚本及工具/DES_Python-master/), [md5爆破](CTF常用脚本及工具/md5爆破/)
  - 编码工具: [进制转换](CTF常用脚本及工具/进制互相转换/), [hex倒叙](CTF常用脚本及工具/hex倒叙/), [hex减位](CTF常用脚本及工具/hex减位/), [字符替换](CTF常用脚本及工具/字符替换表/), [文本转GBK](CTF常用脚本及工具/文本转gbk编码/)
  - Python笔记: [python-note.md](CTF常用脚本及工具/python-note.md)

### 流量分析
- **工具**: [Wireshark](工具使用/Wireshark使用.md), [tshark](工具使用/tshark使用.md)
- **脚本**: [USB流量](CTF常用脚本及工具/usb流量/), [流量数据提取](CTF常用脚本及工具/流量数据提取脚本/), [TTL隐写](CTF常用脚本及工具/TTL隐写/), [曼彻斯特编码](CTF常用脚本及工具/曼彻斯特编码/)
- **关键词**: `pcap` `pcapng` `USB` `TTL` `曼彻斯特`

### 隐写术（综合）
- **知识**: [图片隐写](图片隐写.md), [音频隐写](音频隐写.md), [压缩包总结](压缩包总结.md)
- **脚本**:
  - 图片类: [频域盲水印](CTF常用脚本及工具/频域盲水印/), [图片爆破宽高](CTF常用脚本及工具/图片爆破宽高/), [RGB转图片](CTF常用脚本及工具/RGB转图片/), [字节转二维码](CTF常用脚本及工具/字节转二维码/)
  - 压缩包类: [CRC32爆破](CTF常用脚本及工具/CRC32校验爆破/), [批量解压](CTF常用脚本及工具/批量解压压缩包+带密码/)
  - 其他: [steghide爆破](CTF常用脚本及工具/steghide爆破密码/), [TTL隐写](CTF常用脚本及工具/TTL隐写/)
- **关键词**: `LSB` `盲水印` `CRC` `文件头` `metadata`

### Reverse
- **脚本**: [xor](CTF常用脚本及工具/reverse/xor/), [Brainfuck](CTF常用脚本及工具/Python-Brainfuck-master/)
- **二进制工具**: [文件异或](CTF常用脚本及工具/文件异或/), [二进制8位倒序](CTF常用脚本及工具/二进制每8位倒序/), [十进制转字符](CTF常用脚本及工具/十进制转字符/)
- **APP逆向**: [jadx-gui](https://github.com/skylot/jadx)（需从官网下载）

### 取证/Misc工具
- **知识**: [内存取证命令速查](工具使用/内存取证秒杀所有命令.md)
- **工具**: [ScreenToGif](https://github.com/NickeManarin/ScreenToGif)（需从官网下载）
- **脚本**: [日志匹配](CTF常用脚本及工具/日志匹配/), [去重](CTF常用脚本及工具/去重/), [批量修改文件名](CTF常用脚本及工具/批量修改文件名后缀/)

---

## 二、按CTF题型快速匹配

| 题型 | 优先级阅读 | 可用脚本 | 相关WP | 大赛WP参考 |
|------|-----------|---------|--------|-----------|
| **Web-SQL注入** | SQL.md | sqlmap, md5爆破 | SQLI-LABS WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep SQL |
| **Web-命令执行** | 命令执行.md | — | ctfshow命令执行 WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep RCE |
| **Web-文件上传** | 文件上传漏洞.md | — | upload-labs, ctfshow WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep upload |
| **Web-文件包含** | 文件包含.md | — | 文件包含WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep LFI |
| **Web-SSRF** | SSRF漏洞.md | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep SSRF |
| **Web-SSTI** | SSTI.md | — | ctfshow SSTI WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep SSTI |
| **Web-JWT** | JWT.md | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep JWT |
| **Web-PHP反序列化** | PHP反序列化漏洞总结.md | Pickle脚本 | ctfshow反序列化 WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 反序列化 |
| **Web-PHP代码审计** | php代码审计.md | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 代码审计 |
| **Web-Nodejs** | WP汇总/Nodejs/ | — | Nodejs原型链污染 WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep Node |
| **Web-XSS** | WP汇总/XSS/ | — | XSS WP | [大赛WP集合](CTF大赛WP集合/articles/) ← grep XSS |
| **Misc-图片隐写** | 图片隐写.md | 宽高爆破/盲水印/CRC/steghide | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 隐写/图片 |
| **Misc-音频隐写** | 音频隐写.md | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 音频/MP3 |
| **Misc-压缩包** | 压缩包总结.md | CRC爆破/批量解压/明文攻击 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep ZIP/压缩 |
| **Misc-流量分析** | 工具使用/ | USB/TTL/曼彻斯特/流量提取 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 流量/pcap |
| **Misc-编码解码** | python-note.md | Base全家桶/进制转换/密码脚本 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 编码 |
| **Crypto-RSA** | RSA综合脚本利用/ | 全套 RSA 攻击脚本 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep RSA/Crypto |
| **Crypto-古典密码** | 维吉尼亚/凯撒/四方等 | 多种古典密码脚本 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 古典/密码 |
| **Crypto-MD5** | — | md5爆破 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep MD5/Hash |
| **Reverse** | reverse/ | xor/Brainfuck/文件异或 | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep Reverse/逆向 |
| **取证(Memory)** | 内存取证命令速查.pdf | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep 取证/内存 |
| **PWN** | — | — | — | [大赛WP集合](CTF大赛WP集合/articles/) ← grep PWN/ROP |

---

## 三、工具→知识链路

| 工具/脚本 | 关联知识文章 | 关联WP |
|-----------|------------|--------|
| sqlmap | SQL.md (L288-L670) | SQLI-LABS |
| ffuf/Dirsearch | — | — |
| Wireshark/tshark | — | — |
| steghide爆破 | 图片隐写.md | — |
| 图片爆破宽高脚本 | 图片隐写.md (IHDR章节) | — |
| 频域盲水印脚本 | 图片隐写.md | — |
| CRC32爆破脚本 | 压缩包总结.md (CRC章节), 图片隐写.md (PNG CRC) | — |
| USB流量脚本 | — | — |
| TTL隐写脚本 | — | — |
| RSA综合脚本 | — | — |
| md5爆破脚本 | php代码审计.md (L228-L277 md5碰撞) | — |
| 日志匹配脚本 | 文件包含.md (日志包含) | — |
| DES加解密脚本 | — | — |

---

## 四、CTF大赛WP集合（1156篇真实比赛WriteUp）

> **来源**: ctfiot.com | **数量**: 1156篇正文 | **路径**: [CTF大赛WP集合/articles/](CTF大赛WP集合/articles/)
> **使用**: 按大赛名搜索文件名即可定位，文件名=文章标题。

### 热门大赛WP速查

| 大赛 | 篇数 | 搜索关键词 |
|------|------|-----------|
| KCTF | 55篇 | `ls CTF大赛WP集合/articles/ | grep -i KCTF` |
| 强网杯 | 38篇 | `ls CTF大赛WP集合/articles/ | grep 强网杯` |
| SCTF | 37篇 | `ls CTF大赛WP集合/articles/ | grep -i SCTF` |
| 春秋杯 | 30篇 | `ls CTF大赛WP集合/articles/ | grep 春秋杯` |
| 西湖论剑 | 24篇 | `ls CTF大赛WP集合/articles/ | grep 西湖论剑` |
| Datacon | 21篇 | `ls CTF大赛WP集合/articles/ | grep -i Datacon` |
| RCTF | 21篇 | `ls CTF大赛WP集合/articles/ | grep -i RCTF` |
| 长城杯 | 16篇 | `ls CTF大赛WP集合/articles/ | grep 长城杯` |
| 网鼎杯 | 15篇 | `ls CTF大赛WP集合/articles/ | grep 网鼎杯` |
| N1CTF | 14篇 | `ls CTF大赛WP集合/articles/ | grep -i N1CTF` |
| NCTF | 14篇 | `ls CTF大赛WP集合/articles/ | grep -i NCTF` |
| 羊城杯 | 11篇 | `ls CTF大赛WP集合/articles/ | grep 羊城杯` |
| WCTF | 11篇 | `ls CTF大赛WP集合/articles/ | grep -i WCTF` |
| HITCON | 10篇 | `ls CTF大赛WP集合/articles/ | grep -i HITCON` |
| 腾讯游戏安全 | 10篇 | `ls CTF大赛WP集合/articles/ | grep 腾讯` |
| 数字中国 | 9篇 | `ls CTF大赛WP集合/articles/ | grep 数字中国` |
| CISCN | 9篇 | `ls CTF大赛WP集合/articles/ | grep -i CISCN` |
| ACTF | 9篇 | `ls CTF大赛WP集合/articles/ | grep -i ACTF` |
| RealWorld CTF | 9篇 | `ls CTF大赛WP集合/articles/ | grep -i RealWorld` |
| HCTF | 9篇 | `ls CTF大赛WP集合/articles/ | grep -i HCTF` |
| HKCERT | 9篇 | `ls CTF大赛WP集合/articles/ | grep -i HKCERT` |
| SECCON | 8篇 | `ls CTF大赛WP集合/articles/ | grep -i SECCON` |
| SUCTF | 7篇 | `ls CTF大赛WP集合/articles/ | grep -i SUCTF` |
| 蓝帽杯 | 7篇 | `ls CTF大赛WP集合/articles/ | grep 蓝帽杯` |
| ByteCTF | 6篇 | `ls CTF大赛WP集合/articles/ | grep -i ByteCTF` |
| WMCTF | 6篇 | `ls CTF大赛WP集合/articles/ | grep -i WMCTF` |

> 更多大赛（386个）可通过搜索articles目录查找

### 按方向搜索WP

```bash
# Web方向
ls CTF大赛WP集合/articles/ | grep -iE "Web|XSS|SQL|SSRF|SSTI|JWT|upload|文件上传|命令执行|反序列化|java|php"

# Reverse方向  
ls CTF大赛WP集合/articles/ | grep -iE "Reverse|逆向|re$|CrackMe|VM|混淆|脱壳|unpack"

# Crypto方向
ls CTF大赛WP集合/articles/ | grep -iE "Crypto|RSA|AES|ECC|密码|加密|Lattice|离散"

# PWN方向
ls CTF大赛WP集合/articles/ | grep -iE "PWN|堆|栈|ROP|Heap|Kernel|内核|shellcode"

# Misc方向
ls CTF大赛WP集合/articles/ | grep -iE "Misc|隐写|取证|流量|内存|USB|蓝牙|压缩包|图片|音频"

# 搜索文章正文内容
grep -rl "关键词" CTF大赛WP集合/articles/
```

---

## 五、全局搜索关键词速查

```bash
# 按漏洞类型
grep -rn "SQL注入\|RCE\|SSRF\|SSTI\|XSS\|CSRF\|文件上传\|文件包含\|反序列化" --include="*.md"

# 按技术关键字
grep -rn "bypass\|绕过\|WAF\|payload\|反弹\|webshell\|注入\|隐写\|爆破" --include="*.md"

# 按工具名
grep -rn "sqlmap\|ffuf\|dirsearch\|nmap\|burp\|wireshark\|tshark\|jadx\|stegsolve" --include="*.md"

# 按CTF题型
grep -rn "Misc\|Crypto\|Web\|Reverse\|PWN\|取证\|流量" --include="*.md"
```
