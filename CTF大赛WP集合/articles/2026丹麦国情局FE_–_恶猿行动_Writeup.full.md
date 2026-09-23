---
title: 2026 丹麦国情局 FE – 恶猿行动 Writeup（OPERATION BAD PRIMATE 渗透）
contest: 2026 丹麦国情局 FE
year: 2026
difficulty: hard
vuln_type:
- sqli
- lfi
- pwn_unknown
- ssh
- web_unknown
tags:
- 丹麦国情局 FE 恶猿行动 2026
- MonkEZ/EDO 公司服务器
- OPERATION BAD PRIMATE
- vmdk 虚拟机
- 仅主机模式
- nmap 三个 ssh + 一个 http
- sqlite 登录 SQLMap
- robots.txt 目录扫描
- 路径穿越 + AES 加密 SSH 私钥
- docker 逃逸 bash_history
- TLS 客户端证书密钥被删
- root@printserver
- root access
attack_chain:
- '部署: 下载 vmdk → VM 仅主机模式（避免 NAT 暴露）'
- '外部侦察: nmap 三个 ssh + 一个 http'
- '初始访问: 登录框随便输 → sqlmap dump users → 拿 ssh 凭据'
- docker 登录 → html 注释提示至少 2 个漏洞
- robots.txt 目录扫描 → 路径穿越
- 路径穿越拿 AES 加密的 SSH 私钥
- 'docker 逃逸: bash_history 查 docker 命令 → 需 TLS 客户端证书'
- 证书密钥已被删 → 需从备份/历史恢复
- '最终: root@printserver'
key_payload: robots.txt → 路径穿越 → AES SSH 私钥
one_liner: 2026 丹麦国情局 FE 恶猿行动：MonkEZ/EDO 服务器渗透 - sqlmap + robots 路径穿越 + AES SSH 私钥 + docker 逃逸 + TLS 客户端证书恢复。
lesson: 丹麦国情局 FE 是面向计算机网络利用部 (CNE) 培训的高仿真 APT 渗透靶场，核心是 docker 逃逸 + TLS 客户端证书恢复；用 vmdk 部署 + 仅主机模式 防 VM 反弹。
quality: high
full_path: 2026丹麦国情局FE_–_恶猿行动_Writeup.full.md
meta_path: 2026丹麦国情局FE_–_恶猿行动_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2026 丹麦国情局 FE – 恶猿行动 Writeup（OPERATION BAD PRIMATE 渗透）。2026 丹麦国情局 FE 恶猿行动：MonkEZ/EDO 服务器渗透 - sqlmap + robots 路径穿越 + AES SSH 私钥 + docker 逃逸 + TLS 客户端证书恢复。。关键路径：部署: 下载 vmdk → VM 仅主机模式（避免 NAT 暴露） → 外部...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- lfi
- pwn_other
- web_other
tools_used:
- nmap
- sqlmap
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/298748.html
reasoning_chain:
- vmdk 虚拟机 + 仅主机模式 → 触发点：避免 NAT 暴露，模拟 APT 内网
- 外部侦察 nmap → 观察：3 个 ssh + 1 个 http 端口
- 登录框随便输 + sqlmap dump users → 动作：拿 ssh 凭据
- docker 登录 + html 注释提示至少 2 个漏洞 → 假设：路径穿越 + 加密文件泄漏
- robots.txt 目录扫描 → 动作：猜目录 → 观察：发现内部路径
- 假设：路径穿越读 AES 私钥 → 动作：构造 ../ → 观察：拿到 AES 加密 SSH 私钥
- 假设：AES 密钥在容器内某文件 → 动作：探索文件系统 → 观察：找到密钥
- 'docker 逃逸: bash_history 查 docker 命令 → 假设：需要 TLS 客户端证书连管理 daemon'
- 证书密钥已被删 → 假设：从 .swp / git 历史 / 备份恢复
- 最终 root@printserver → 完成
failed_attempts:
- 直接从外网 nmap 扫 → 失败：仅主机模式需先登入跳板
- sqlmap 用 random user-agent → 失败：WAF 拦截
- 尝试 john 爆破 SSH 私钥 passphrase → 失败：AES 私钥需要先解对称加密
key_observations:
- vmdk 仅主机模式 = 防 VM 反弹的标准隔离方案
- robots.txt 路径扫描 + 路径穿越 + AES SSH 私钥是 docker 入门链
- bash_history 暴露 docker 命令是凭据恢复入口
- TLS 客户端证书密钥删除后需查备份/.swp/git history
- OPERATION BAD PRIMATE 是丹麦 CNE 培训靶场，docker 逃逸 + TLS 恢复是核心
prerequisites:
- vmdk/VMware 部署（仅主机模式网络）
- nmap/sqlmap/dirb/dirsearch 扫描器链
- 路径穿越 + AES 加密文件恢复
- docker daemon TLS 客户端证书认证
---
# 2026丹麦国情局FE – 恶猿行动 Writeup

> 原文: https://www.ctfiot.com/298748.html
> ID: 298748

OPERATION BAD PRIMATE

前言

主要关键的攻击向量与密码学、二进制有很大关系

vpn network还差最后两个二进制接管vpn network，这也直接告诉我我应该回去学习一下二进制了

后面过完春节再把它协调进我的大师计划中吧，看来二进制始终是要面对的，既然他们给我开了一个头，那我一定会做到

机密：相对机密

日期：2026-01-29

来源：战略关注与考量部

致：计算机网络利用部（CNE）培训

部 截止日期：2026-02-30

合作服务宣布，MonkEZ/EDO公司可能参与官方武器生产，此外还有 其官方贸易的农业和兽用饲料产品; 花园。

调查显示该公司很可能正在使用 以饲料产品为掩护，掩护非法活动。

我们需要了解公司内部的情况，包括 可访问财务报表、供应商列表及内部沟通 确认或否认怀疑。

借助人力情报线人，我们已撤离出一份旧备份 公司的服务器之一。你的任务是分析这些备份 寻找并识别可能让我们访问 公司的服务器和系统。服务器无法再有互联网，但我们可以通过人力情报（HUMINT）进行网络访问。

我们的消息来源进一步报告，自从备份文件被获取后， MonkEZ/EDO 已经更改了所有密码和 ssh 密钥。 看起来其他方面都没变。

因此，重点是找到即使更改后也能正常运行的服务器路径。

行动目标：

尽可能多地识别旧服务器备份中的漏洞， 这些数据可以用来获得对正确服务器的全部或部分访问权限。

记录如何利用已识别的漏洞 并且合并。最终目标是获得根访问权限 服务器（root@printserver）。

虚拟机部署

下载vmdk后，在vm新建虚拟机并使用这个vmdk，

请注意：在不确定该虚拟机是否200%安全之前，不要按照FE官方指示那样设置为NAT，因为设置NAT可以导致该虚拟机访问你的本地网络、互联网，除非你知道你自己在干什么，否则请设置为“仅主机”模式

外部侦察

nmap一扫，三个ssh和一个http，

初始访问 – 立足点

进来一个登录框，随便输入并登录后，发现提示sqlite，

直接上sqlmap就能出来

dump users表后去登录，

拿到了ssh初始访问凭据

直接登ssh，在docker

同时发现html注释提示至少2个漏洞

目录扫描发现robots.txt，

顺势发现路径穿越漏洞，获得一个aes加密的ssh私钥：

docker逃逸

有bash_history

很显然，经过尝试之后，想要访问docker，必须启用tls，

即携带客户端证书、密钥，但是它已经被删除了。

线索:

我们检查一下我们手上的东西，在hostconf/目录中：

makeCert.sh用于生成ca证书/私钥、服务器证书、客户端证书，最主要的内容:

也就是ca key基于key_in-text.txt的配置生成

makeKey.py主要是一个生成rsa key的脚本，但这个脚本存在漏洞，

密码学不是我的强项，所以我把它交给了AI：

在 RSA 算法中，模数 $n$ 是两个素数 $p$ 和 $q$ 的乘积（$n = p times q$）。根据算术基本定理，任何合数分解为素数乘积的形式在不计顺序的情况下是唯一的。

由于您提供的 Python 脚本逻辑中，$p$ 和 $q$ 的差值被限制在一个极小的范围内（约 1026 左右），这使得我们能够通过数学手段（费马分解法的变体）精确地锁定这对唯一的 $p$ 和 $q$。

所以根据这个漏洞，只要拿到服务器的n就能确定服务端使用的rsa私钥，恰好家目录/hostconf/目录中有ca.pem，我们从ca.pem拿到n然后结合py脚本的漏洞得到服务器使用的rsa私钥：（注意ca.pem的备份，否则运行makeCert.sh后会被覆盖

带着这个文件运行makeCert.sh就能生成合法的客户端证书和私钥，用于访问docker

接着就是祖传挂载宿主机根目录，

root目录中有ssh私钥、ssh服务配置，

内部侦察 – 核心网络

10.0.42.0/24有一台新主机

横向移动 -> 核心网络

查看hostcontainer的bash_history

线索：

根据10.0.42.1的端口扫描结果看，它就是router

检查git目录:

总感觉这个存在至少两个攻击路径，但我率先发现了pwgen的密码爆破，

有一个shadow备份文件，经过对比，这个备份文件不是当前主机的，猜测应该就是router的

passwdGen.py使用的lcg算法存在漏洞，生成的密码范围在1677万个，

让ai写一个脚本，把这1677万个密码全部做成一个密码本，

再通过工具进行yescrypt爆破，不到一分钟，说明这条攻击路径是正确的：

github[.]com/cyclone-github/yescrypt_crack

登录router ssh

VPN网络侦察

有三台主机，从端口上看，主要有两台主机值得关注

由于67做了网络隔离，无法访问外部网络，加上我的parrot虚拟机已经有非常久没有使用了，存在许多无法表达的系统问题和网络问题，这里我仅借助我的老parrot虚拟机上的小工具以及反向ssh做端口转发，

在router把67的两台主机的3000、7000端口通过socat做一个端口转发

接着在hostcontainer反向ssh做一个远程端口转发，这样我们的parrot虚拟机就能直接在本地访问对应的服务

10.0.67.102

3000端口，wasm sandbox

在我的学习生涯中也是第一次接触到这种东西，我找到了奇安信的一篇文章：

10.0.67.199

7000端口，一个交互程序

当写入note并超出256个字节后，后面的数字会被当成序号并识别成对应的动作指令

所以我认为它应该是远程缓冲区溢出，但是搞笑的是距离上一次在TryHackMe做远程缓冲区溢出的题已经是在三年前，加上没有攻击环境，我已经失去快速进攻的机会

结束

打到这已经花了两天时间，重新启用parrot渗透虚拟机遇到非常多的问题以及靶机踩了许多坑。

最重要的是马上就是春节，我不得不离开这个CTF，

我要继续享受假期了，否则没机会了（

总的来说这是一个挺不错的体验，包括wasm sandbox，至少他直接警告了我，

我的二进制能力非常有限，

保持学习

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