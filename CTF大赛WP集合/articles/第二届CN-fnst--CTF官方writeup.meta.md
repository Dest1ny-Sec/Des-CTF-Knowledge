---
title: 第二届CN-fnst--CTF官方writeup
contest: CN-fnst--CTF
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [公益CTF,Misc,Misc-crypto,Web-SSTI,Web-RCE,Pwn-stack,Heap,Sandbox-shellcode,RE-XOR,Crypto-RSA]
attack_chain: 钓鱼执法反作弊→key.html歌词数字提hex→silenteye音频隐写→二十八星宿四象限→玄武00青龙01白虎10朱雀11二进制解flag→Flask SSTI unicode十六进制属性名绕黑名单→canary+ret2libc栈溢出ROP→fmtstr_payload覆盖got→seccomp openat+read+write shellcode→fastbin attack free_hook→凯撒密码1位移→UPX脱壳+XOR key爆破→RSA yafu分解n→dp泄露构造φ→2331位01序列合法状态DP
key_payload: flag{BaguA_M4ster_0v0}|{%print g['pop'][('_'*2)|attr("x5fx5faddx5fx5f")('globals')...%}|b'a'*(0x8*3-1)+b'Z'+p(canary)+prdi+...+p(0x400737)|fmtstr_payload(8, {elf.got["exit"]: p(elf.sym["main"])})+fmtstr_payload(8, {elf.got["printf"]: p(system)})+b'/bin/sh\x00'
one_liner: 公益赛事998人注册584队参赛,反作弊在某鱼钓鱼执法+14题覆盖Misc隐写音频四象限二进制/Flask SSTI黑名单绕/canary栈溢出ROP/格式化字符串盖got/seccomp openat shellcode/fastbin free_hook/凯撒+图片隐写/UPX脱壳+XOR爆破/RSA yafu/DP泄露/2331位状态DP
lesson: 1) Flask SSTI WAF可读源文件后用十六进制属性名x5fx5faddx5fx5f绕黑名单('__add__'→'x5fx5faddx5fx5f'); 2) 栈溢出canary末字节必为\x00爆破1字节绕过; 3) fmtstr_payload(offset, {got: value})两步覆盖exit→main循环+printf→system; 4) seccomp禁execve时用openat+read+write纯汇编ORW; 5) tcache下fake_fast布置后backdoor地址前置; 6) RSA已知dp可直接计算p: e*dp ≡ 1 (mod p-1) → p = e*dp - 1 + k*((e*dp-1)//(k+1))... 7) 二十八星宿四象限编码本质是2bit/字符的二进制编码
quality: high
---

## 备注

公益CTF,2题送分(夜观天象+真·签到)+12题高/中等难度。作者擅用pwnfunc封装(setup_arch+ru+sl+sa+leak_got+success+ia)。

### 题目清单(14题)

1. **夜观天象** — key.html歌词数字676966742069732070407373776464→hex转ascii得gift=**p@sswdd**→silenteye用p@sswdd作密码解密音频得flag.txt
2. **二十八星宿** — 二十八宿4组对应00/01/10/11四象限(玄武/青龙/白虎/朱雀),转8位二进制→ASCII得**flag{BaguA_M4ster_0v0}**
3. **ez_python** — Flask+flask_limiter,get参数file任意文件读(过proc),/shell?name触发SSTI但WAF过滤os/set/__builtins__/=/./{{/}}/popen/+/__,用十六进制属性名x5fx5faddx5fx5f绕
4. **signin** — pwnfunc栈溢出,输入name=1,Introduce=24字节(0x8*3-1)最后一字节'Z',覆盖canary低1字节为00(逐字节爆破),Say something构造prdi+puts(puts@got)泄libc→binsh+system
5. **真·签到** — sh;cat flag
6. **ez_fmt** — fmtstr_payload(offset=8, {exit_got: main_addr})回main循环,再fmtstr_payload(8, {printf_got: system})→sl('/bin/sh\x00')
7. **ez_sandbox** — seccomp禁execve,openat(-100, 'flag', 0)→read(3, buf, 1024)→write(1, buf, 1)汇编shellcode
8. **babyheap** — show chunk0泄leak,fake_fast = leak - 0x7B,backdoor前置编辑chunk5写入backdoor地址,再alloc触发调用
9. **babyheap_revenge** — 9次alloc(0x20)+free(4)+free(3)→edit(0) 0x90字节填满触发0x91溢出→heap_base=heap0-0x490,libc leak减0x3C3B78,og=0xef9f4,free(1)+alloc fake 0x71→alloc 0x13+p(heap0+0x10)+asm(shellcraft.sh())+edit+free触发
10. **Sign in** — 假base64字符串(凯撒位移1)→toolscat.com/img/image-mask图种隐写
11. **AmaZing_BruteForce** — UPX壳脱壳→16字节密文XOR,itertools.product(ascii_lowercase, repeat=4)爆破key
12. **ezphp** — md5强弱类型比较(0e...科学计数法)
13. **ezCrypto** — yafu分解n=1455925529734358105461406532259911790807347616464991065301847=1201147059438530786835365194567×1212112637077862917192191913841,mod_inverse+pow(c,d,n)解
14. **神秘dp** — 给定e=65537,dp,p,q,n,c直接算d解RSA
15. **math** — 2331位01序列(禁止1111/0000连续)状态DP统计合法数,next_prime得p,解RSA

## 评级

- **quality: high** — 14题覆盖6大类漏洞,核心题目技术细节完整(SSTI属性名绕WAF/seccomp ORW/fastbin/canary爆破/fmtstr_payload),缺失部分主要为第11题正则特征未截图
- **vuln_type: misc_unknown** — 主分类杂项(覆盖M/A/W/P/Crypto),以misc_unknown为兜底
- 实际漏洞类型涉及:ssti(web+黑名单绕)、rce(SSRF+反序列化)、pwn_unknown(栈溢出+canary)、pwn_unknown(格式化字符串)、pwn_unknown(seccomp+ORW)、heap_exploit(fastbin)、reverse(凯撒+UPX+XOR)、crypto_rsa(yafu分解)、crypto_rsa(dp泄露)、misc_math(状态DP)
