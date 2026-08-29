---
title: 【相关分享】星芒杯 2025 WriteUP
contest: 星芒杯
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [代码审计, call_user_func-RCE, ISO-8859-1-to-UTF8, 盲文解码, file读取-LFI, 隼目安全]
attack_chain: 1. PHP 代码审计 call_user_func($func, $param) 函数名 RCE /2. 提交 flag{call_user_func} /3. 布莱切利庄园 ISO-8859-1 → UTF-8 username 还原 /4. 盲文 password 解码 /5. /archives?file= 文件读取
key_payload: flag{call_user_func}  darkguard98 / secretgate45  ISO-8859-1 latin1
one_liner: 星芒杯 2025 Web WP，代码审计 call_user_func RCE + ISO-8859-1/UTF-8 编码还原 + 盲文解码 + LFI 文件读取。
lesson: call_user_func($func, $param) 是 PHP 经典 RCE；ISO-8859-1 → UTF-8 双重编码还原是乱码恢复经典；盲文密码可直接解码；?file= LFI 是常见文件读取。
quality: medium
---

# 【相关分享】星芒杯 2025 WriteUP

## 概览
星芒杯 2025 WriteUP，Web 方向代码审计 + 字符编码 + LFI。

## Web

### 代码审计
```php
<?php
$source = file_get_contents(__FILE__);
$hidden_source = preg_replace('/define\('FLAG', '.*?'\);/', 'define(\'FLAG\', \'[FLAG HIDDEN]\');', $source);
echo "" . htmlspecialchars($hidden_source) . "";
error_reporting(0);
define('FLAG', '[FLAG HIDDEN]');
function show_flag($key) {
    if ($key === 'secret_key') {
        echo "\nFlag: " . FLAG;
    }
}
$func = $_GET['func'] ?? '';
$param = $_GET['param'] ?? '';
if (function_exists($func)) {
    call_user_func($func, $param);
}
```

- 漏洞：`call_user_func($func, $param)` 任意函数名调用
- 答案：`flag{call_user_func}`

### 布莱切利庄园
```python
print("éu0081u0097èu00bfxb9èu0099u009açu00a9u00baæu009fu0092".encode('latin1').decode('utf-8'))
# 输出: 遗迹秘密伍
```

- 盲文 password: `secretgate45` 或 `darkguard98`
- 登录后 `/archives?file=` 存在 LFI

## 经验提炼
- `call_user_func($func, $param)` 是 PHP 经典 RCE
- ISO-8859-1 → UTF-8 双重编码还原是乱码恢复经典
- 盲文密码可直接解码
- `?file=` LFI 是常见文件读取
- preg_replace 单引号转义
- function_exists 检查函数名
- 星芒杯 2025 主办方是"隼目安全"
- `?encode('latin1').decode('utf-8')` 是双编码还原
- LFI + 读源代码二次审计
- flag 直接是函数名是出题人 trick
