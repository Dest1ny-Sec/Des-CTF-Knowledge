# [ffuf的使用](https://www.cnblogs.com/-Lucky-/p/17268230.html)

ffuf:模糊测试

使用 ffuf 进行枚举、模糊测试和目录暴力破解

安装
https://github.com/ffuf/ffuf

建议：https://github.com/danielmiessler/SecLists

ffuf -h

**HTTP选项:**

```diff
-H          请求头'Name:Value'用冒号分隔。可接受多个标志
-X          要使用的HTTP方法。如get,post
-b          Cookie数据`"NAME1=VALUE1; NAME2=VALUE2"`
-d          POST 数据
-http2      使用HTTP2协议（默认值：false）
-ignore-body    不要获取响应内容。（默认值：false）
-r          遵循重定向（默认值：false）
-recursion  递归扫描，只支持FUZZ关键字，并且-u结尾（默认值：false）
-recursion-depth    最大递归深度。（默认值：0）
-replay-proxy   使用此代理重播匹配的请求
-timeout        HTTP请求超时（秒）。（默认值：10）
-u          目标url
-x          代理URL（SOCKS5或HTTP）。例如：http://127.0.0.1:8080或socks5://127.0.0.1:8080
```

**常规选项**

```diff
-V          显示版本信息（默认值：false）
-ac         自动校准过滤选项（默认值：false）
-acc        自定义自动校准字符串。可以多次使用。含义-ac
-ach        每主机自动校准（默认值：false）
-ack        自动校准关键字（默认值：FUZZ）
-acs        自动校准策略：“基本”或“高级”（默认值：基本）
-c          将输出着色。（默认值：false）
-config     从文件加载配置
-json       json输出，打印换行分隔的json记录（默认值：false）
-maxtime    整个进程的最大运行时间（以秒为单位）。（默认值：0）
-maxtime-job    作业每个作业的最大运行时间（以秒为单位）。（默认值：0）
-noninteractive -非交互式禁用交互式控制台功能（默认值：false）
-p          请求之间的“延迟”秒数，或一系列随机延迟。例如“0.1”或“0.1-2.0”
-rate       每秒请求的速率（默认值：0）
-s          不打印附加信息（静默模式）（默认值：false）
-sa         在所有错误情况下停止。暗示-sf和-se。（默认值：false）
-se         在出现虚假错误时停止（默认值：false）
-sf         当>95%的响应返回403 Forbidden时停止（默认值：false）
-t          并发线程数。（默认值：40）
-v          详细输出，打印完整的URL和重定向位置（如果有）以及结果。（默认值：false）
```

**匹配器选项**

```diff
-mc         匹配HTTP状态代码，或“全部”表示所有内容。（默认值：200,204,301,302,307,403,404,500）
-ml         匹配响应行数
-mmode      匹配器集运算符。以下任一项：和或（默认值：或）
-mr         匹配正则表达式
-ms         匹配HTTP响应大小
-mt         匹配第一个响应字节的毫秒数，大于或小于。例如：>100或<100
-mw         匹配响应的单词数量
```

**过滤器选项：**

```diff
-fc         从响应中筛选HTTP状态代码。代码和范围的逗号分隔列表
-fl         根据响应的行数进行过滤。行计数和范围的逗号分隔列表
-fmode      筛选器集运算符。以下任一项：和或（默认值：或）
-fr         筛选器正则表达式
-fs         筛选器HTTP响应大小。大小和范围的逗号分隔列表
-ft         根据到第一个响应字节的毫秒数进行筛选，大于或小于。例如：>100或<100
-fw         按响应的字数进行筛选。以逗号分隔的单词计数和响铃列表
```

**输入选项**

```diff
-D          DirSearch单词列表兼容模式。与-e标志一起使用。（默认值：false）
-e          扩展名的逗号分隔列表。扩展FUZZ关键字
-ic         忽略单词列表注释（默认值：false）
-input-cmd      要测试的输入数。与--input cmd一起使用。（默认值：100）
-input-shell    用于运行命令的外壳
-mode       多单词列表操作模式。可用模式：clusterbomb, pitchfork, sniper (default: clusterbomb)
-request    包含原始http请求的文件
-request-proto      与原始请求一起使用的协议（默认值：https）
-w          用冒号分隔的单词列表文件路径和（可选）关键字
```

**输出选项**

```diff
-debug-log      将所有内部日志记录写入指定的文件。
-o              将输出写入文件
-od             将匹配结果存储到的目录路径
-of             输出文件格式。可用格式：json、ejson、html、md、csv、ecsv（或所有格式的“all”）（默认值：json）
-or             如果没有结果，就不要创建输出文件（默认值：false）
```

**示例用法**

至少需要提供两个选项：-u指定 URL 和-w指定词表。default 关键字FUZZ用于告诉 ffuf 将在何处注入词表条目

```bash
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

开始枚举通用文件列表，例如 raft-medium-files-lowercase.txt
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files-lowercase.txt

可以在 index 之后附加扩展名
ffuf -u http://10.10.172.97/indexFUZZ -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt

筛选
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt -e .php,.txt

对目录的fuzz
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt

过滤状态码为403 -fc 403
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files-lowercase.txt -fc 403

匹配状态码为200
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files-lowercase.txt -mc 200

过滤匹配正则表达式的文件
ffuf -u http://10.10.172.97/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files-lowercase.txt -fr '/\..*'

子域枚举和虚拟主机枚举
ffuf -u http://FUZZ.mydomain.com -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fs 0
ffuf -u http://mydomain.com -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H 'Host: FUZZ.mydomain.com' -fs 0
```