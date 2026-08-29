---
title: 强网杯 WriteUp - ChaMd5 Venom (2022全方向12题)
contest: 强网杯
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [admin/123绕, Phar反序列化, SSRF_AdminShow, file://协议, spl_autoload, .inc上传, 仿冒sakai类, mprotect触发, House_of_Apple, House_of_Kiwi_FSOP, RSA_多模数_AMM, 模方程求解, 沙箱逃逸, JS_DataView, libQJS_jerryscript, ecrecover_4模, setcontext+61, ChaMd5_Venom, 招新]
attack_chain: Web1 admin/123登录 → Web2 upload.phpshowfile.phpPhar反序列化+SSRF AdminShow+10.10.10.10/10.10.10.101内网 → Web3 balancer路由Pickle反序列化+userdata伪造(cossystemS'bash -c...') → Web4 .inc文件上传+同名class触发spl_autoload+__wakeup执行eval($_REQUEST['sakai']) → Pwn devnull:栈溢出+rdx=7 mprotect触发+shellcraft.execve → Pwn house_of_cat:tcache+libc setcontext+61+io_wfile_jumps vtable → Pwn JS libQJS jerryscript:f64_to_hex+ArrayBuffer+DataView任意读+JIT magic 0x62触发 → Cr RSA:e=3多模数AMM求根+CRT还原flag → Pwn bisy/pwnhouse:JS ArrayBuffer JIT漏洞 → Re:方程组z3+d810去混淆+TEA+rot13+VM逆向
key_payload: Phar反序列化+SSRF AdminShow+Pickle RCE + .inc spl_autoload + mprotect+rdx=7 + RSA e=3 AMM
one_liner: 强网杯2022 ChaMd5 Venom全方向12题:admin绕/Phar+SSRF/Pickle+userdata/.inc spl_autoload/栈溢出mprotect/House of cat FSOP/JS libQJS ecrecover+AMM。
lesson: Phar反序列化生成新文件+SHA1修复签名+phar://协议触发__destruct;Pickle反序列化userdata cookie伪造;多模数RSA e=3时用AMM算法在每个a_i下求e次根再CRT;JS ArrayBuffer+DataView+Float64Array+Uint8Array拼接64位值;libQJS jerryscript JIT magic=0x62触发;House of cat setcontext+61劫持RDX做movaps对齐;伪造类触发spl_autoload+__wakeup。
quality: high
---
