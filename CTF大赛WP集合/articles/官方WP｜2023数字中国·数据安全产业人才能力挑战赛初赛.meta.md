---
title: 2023数字中国·数据安全产业人才能力挑战赛初赛官方WP
contest: 2023数字中国·数据安全产业人才能力挑战赛初赛
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [盲注, AES解密, XXE, jar协议, 临时文件RCE, scxml状态机RCE, Go逆向, net_Listen, tcp_pseudo_header, checksum, TcpSyn包构造, ip2int, 数字中国]
attack_chain: 端口管理:SQL盲注substr(hex(password))取出admin密码+AES解密 → key:帮助文档泄露用户名dcic+弱口令000000登录+id遍历找flag用户 → XxMe:XXE+jar协议上传临时文件+xxe列目录拿临时文件名+object路由加载poc.xml SCXML状态机RCE(.getClass().forName Runtime.exec) → LetsGO:Go逆向找main_handle_input,构造TCP SYN包(lport=99/rport=233/seqnum=0xdeadbeef/flag=2),计算pseudo_header checksum,与server判断一致后"win"
key_payload: 盲注substr(hex(password)) + jar://1.zip!/a.php上传 + SCXML Runtime.exec反弹shell + TCP SYN构造seq=0xdeadbeef
one_liner: 2023数字中国数据安全赛3题官方WP:SQL盲注+AES/XXE jar+SCXML RCE/Go TCP SYN包构造。
lesson: 盲注用substr+hex提取完整密码;XXE+jar协议上传临时文件+object SCXML执行;XXE p1.xml列/tmp目录拿临时文件名;Go逆向看main_handle_input逻辑;TCP构造需算pseudo_header+checksum;SYN包lport=99/rport=233/seq=0xdeadbeef/flag=0x8002。
quality: high
---
