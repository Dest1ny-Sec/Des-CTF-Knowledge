---
title: DASCTF 2022 5 月出题人挑战赛官方 Write
contest: DASCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [golang-upload, cve-2021-42013, golang-ssti, ua-spoof, sys-auth-rc4, docker-layer, suid, mt19937-symbolic]
attack_chain:
  - hackme: 上传 users.go 白名单绕过
  - getme: CVE-2021-42013 目录穿越读 access_log
  - fxxkgo: golang jwt {{.}} 模板注入
  - 魔法浏览器: UA 修改 + JS 反混淆
  - Power Cookie: cookie=admin 1
  - ezcms: Mc_Encryption_Key 解密 update.php
  - delflag: docker save + layer extract
  - Yusa MT19937 线性攻击
  - 山重水复: off-by-one 改 size 0x481
  - house of kiwi 劫持
key_payload: Apache 2.4.50 目录穿越 + MT19937 符号执行
one_liner: DASCTF 2022 5 月出题人挑战赛官方 WP，6 Web + 6 Misc + 3 Crypto + 2 Pwn。
lesson: golang web 框架的 SSTI 比 Python 难利用，但模板渲染时同样注入 . 用 {{.}} 即拿到 key。
quality: high
---

DASCTF 2022 5 月出题人挑战赛官方 WP（来源 ctfiot，656 队伍报名）。

**WEB 1: hackme** — golang 上传。`users.go` 在白名单；上传恶意 `users.go`：
```go
package main
import ("fmt"; "os/exec")
func exp() {
    out, _ := exec.Command("cat","/flag").Output()
    fmt.Println(string(out[:]))
}
func main() { exp() }
```

**WEB 2: getme** — Apache 2.4.50 CVE-2021-42013。`http://127.0.0.1:11777/icons/.%%32%65/.%%32%65/.../flag` 路径穿越。`/icons/.%%32%65/logs/access_log` 读 access_log；超长路径找真 flag。

**WEB 3: fxxkgo** — golang SSTI。注册时 `nickname` 传 `{{.}}` 模板注入拿到 key；is_admin=true 拿 flag。

**WEB 4: 魔法浏览器** — F12 看 JS 提示用魔法浏览器 UA；插件伪装访问拿 flag。

**WEB 5: Power Cookie** — cookie 改 admin 1 拿 flag。

**WEB 6: ezcms** — admin:123456 认证码 123456 登后台。`update.php` 用 `Mc_Encryption_Key='GKwHuLj9AOhaxJ2'` RC4 加密。`sys_auth(url)` 构造加密的远程 zip URL；远程 zip 含一句话木马。

**MISC 1: delflag** — `docker save snowywar/blue -o blue.tar` + docker-layer-extract 工具 + zsteg/stegsolve 提 blue 像素 LSB → 还原 flag2.png → 进一步 LSB → gzip 解压。

**MISC 2: 噪音** — wav 频谱，rounded_data 排序后 15 个不同值；unique.index() 转 hex。

**MISC 3: 神必流量** — 7z 头提取；URL 下载 out.txt；Golang main.exe 逆向 key="6603"；XOR 还原。

**MISC 4: 不懂 PCB 的厨师** — PCB 软件导入转 3D 视图看 flag。

**MISC 5: 卡比** — 卡比文字表替换 `ptrh{gwdvswvqbfiszsz}` + 维吉尼亚 kirby 解密 = `flag{imverylikekirby}`。

**MISC 6: rootme** — SUID 提权。`find / -perm -4000` + `date -f /root/flag.txt`。

**CRYPTO: Yusa 的密码学课堂 3 题**
1. 一见如故 — 魔改 MT19937 线性攻击恢复
2. 二眼深情 — 状态转移矩阵 untamper
3. 三行情书 — 2000 个输出与 2037740385 AND，z3 符号执行恢复原始 MT 状态

**PWN 1: 山重水复** — off-by-one 改 size 为 0x481；堆块重叠；main_arena+96 写 tcache fd；改末 2 字节为 _IO_2_1_stdout_ 1/16 爆破；泄 libc/ld；劫持 _dl_rtld_lock_recursive = one_gadget。

**PWN 2: twists and turns** — house of kiwi 在无 free_hook/malloc_hook/exit_hook 情况下劫持程序流。idx 负数溢出；mmap 0x21918 前面开合法空间；ORW 绕沙箱。

**PWN 3: BadUdisk** — `printf oct` 八进制写入 label；`sh` 反弹到 /tmp/log 写脚本；cd ../mybin 绕过。
