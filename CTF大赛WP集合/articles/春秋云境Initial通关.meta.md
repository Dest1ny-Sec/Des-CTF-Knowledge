---
title: 春秋云境Initial通关
contest: 春秋云境靶场
year: 2023
difficulty: easy
vuln_type: rce
tags: [ThinkPHP, 内网渗透, frp代理, MS17-010, DCSync, 域控]
attack_chain: ThinkPHP指纹识别→漏洞扫描→RCE getshell→sudo mysql提权读flag1→frp代理→MS17-010打域内机→DCSync域管→域管权限读flag2/3
key_payload: "sudo mysql -e '! cat /root/flag/flag01.txt';MS17-010;DCSync"
one_liner: 春秋云境Initial靶场：ThinkPHP RCE入口→MS17-010横向→DCSync拿域管
lesson: 入门级内网渗透：边界ThinkPHP漏洞→frp代理→MS17-010→DCSync拿域控
quality: medium
---

# 春秋云境Initial通关

**靶场**：春秋云境Initial（简单难度，单flag分段）

**攻击链**：
1. **入口机**：电源管理系统 → 指纹识别ThinkPHP → 扫描ThinkPHP漏洞
2. **RCE getshell**：www-data权限 → `sudo mysql -e '! cat /root/flag/flag01.txt'` 提权读flag1
3. **内网扫描**：frp代理 → 扫描发现 172.22.1.2(域控) / 172.22.1.15(边界机) / 172.22.1.18(信呼OA) / 172.22.1.21(永恒之蓝)
4. **横向**：MS17-010打域内机 → DCSync拿下域管 → 域管权限读flag2/3

**关键技术**：
- ThinkPHP漏洞识别与利用
- sudo mysql -e 提权技巧
- frp内网代理
- MS17-010 (EternalBlue)
- DCSync域控权限提升

**质量评估**：中（流程清晰但细节偏简，命令级payload充分）
