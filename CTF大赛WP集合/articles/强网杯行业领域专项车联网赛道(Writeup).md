# 强网杯行业领域专项车联网赛道(Writeup)

> 原文: https://www.ctfiot.com/276876.html
> ID: 276876

为深化推动前沿技术创新应用，本次竞赛聚焦国家战略需求和地方产业布局，围绕行业领域网络安全中的现实问题进行设计，共设置“漏洞智能分析”、“天基互联网安全”、“车联网安全”三个行业领域赛道，评估检验国内优势团队在智能化漏洞分析、天基网络数据分析、车联网安全测试等方面的能力

题目提示

安全研究人员在进行某品牌汽车硬件安全测试时，发现其中某核心零部件内用于实现AES密码算法的芯片存在侧信道信息泄露。研究人员对该芯片执行密码运算过程中的功耗信息进行了采集，并确认可以利用该数据集进行侧信道攻击取得算法密钥，请尝试利用技术手段复现研究人员获取到的密钥信息，该密钥即为题解。 给我进行分析 题目内容并且给我分析题目打印flag

考点为: 汽车芯片 AES 侧信道

读取与检查（TRS）

读取与检查（TRS）解析 TRS 头部，拿到：轨迹条数ntraces每条采样点数nsamples（这里是500）附带数据长度dlen（这里是32：16B PT +16B CT）逐条读入：pts[i]（明文16字节）cts[i]（密文16字节）traces[i, 0..nsamples-1]（功耗序列）这一步只是在把数据搬到内存，后面统计要用。

对功耗矩阵traces 做按列标准化（去均值、单位方差）：目的：抵消慢漂移/量纲差异，让“相关性”可比操作：tr= (traces - mean(traces, axis=0)) / std(traces, axis=0)

4. 相关统计（CPA）

5. 拼接主密钥并校验

把 16 个最优字节连起来得到候选主密钥K*。用标准 AES-128 实现对多条（随机抽样）明文做加密，比较结果是否等于数据集中附带的密文：

接着我们直接写脚本即可

#Re-create theCPArecovery script after kernel resetscript_path="/mnt/data/recover_aes_flag_cpa.py"code=r'''#!/usr/bin/env python3#-*-coding: utf-8-*-"""Recover AES-128 master key (flag) from a Riscure TRS dataset via CPA.- Pure Python + NumPy.- Leakage model: First-round SubBytes + Hamming Weight.- Output: hex key + flag{UPPERCASE_HEX}.Usage: python recover_aes_flag_cpa.py AES128.trs python recover_aes_flag_cpa.py AES128.trs --window 50:300 --verify 200 python recover_aes_flag_cpa.py AES128.trs --no-verify"""importargparse, os, sys, randomimportnumpy as np#--------------------TRSparsing--------------------def parse_trs_header(f): f.seek(0) header={} whileTrue: t=f.read(1) ifnot t:break l=f.read(1) ifnot l:break t=t[0]; l=l[0] v=f.read(l) header[t]=v ift==0x5F: # end-of-header break returnheader, f.tell()def read_trs(path): withopen(path,"rb")asf: header, offset=parse_trs_header(f) ntraces =int.from_bytes(header.get(0x41, b"x00x00x00x00"),"little") nsamples=int.from_bytes(header.get(0x42, b"x00x00x00x00"),"little") coding =int.from_bytes(header.get(0x43, b"x00"),"little") dlen =int.from_bytes(header.get(0x44, b"x00x00"),"little") ifdlen<32: raiseValueError("TRS record data length < 32 (need 16B PT + 16B CT).") pts=np.empty((ntraces,16), dtype=np.uint8) cts=np.empty((ntraces,16), dtype=np.uint8) traces=np.empty((ntraces, nsamples), dtype=np.uint8) withopen(path,"rb")asf: f.seek(offset) foriinrange(ntraces): meta=f.read(dlen) iflen(meta)!=dlen: raiseEOFError("Unexpected EOF while reading metadata") pts[i]=np.frombuffer(meta[:16], dtype=np.uint8) cts[i]=np.frombuffer(meta[16:32], dtype=np.uint8) pw=f.read(nsamples) iflen(pw)!=nsamples: raiseEOFError("Unexpected EOF while reading power trace") traces[i]=np.frombuffer(pw, dtype=np.uint8) returnpts, cts, traces, (ntraces, nsamples, coding, dlen)#--------------------AES(encryptforverification)--------------------SBOX=[ 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76, 0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0, 0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15, 0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75, 0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84, 0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf, 0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8, 0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2, 0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73, 0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb, 0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79, 0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08, 0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a, 0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e, 0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf, 0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]RCON=[0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]def sub_word(w):return[SBOX[b]forbinw]def key_expansion_bytes(key16): w=[list(key16[i:i+4])foriinrange(0,16,4)] foriinrange(4,44): temp=w[i-1].copy() ifi%4==0: temp=sub_word(temp[1:]+temp[:1]) temp[0]^=RCON[i//4] w.append([ (w[i-4][j]^temp[j])&0xffforjinrange(4) ]) rks=[] forrinrange(11): rks.append(sum(w[4*r:4*r+4], [])) returnrksdef bytes_to_state(b16): s=[[0]*4for_inrange(4)] forcinrange(4): forrinrange(4): s[r][c]=b16[r+4*c] returnsdef state_to_bytes(s): out=[0]*16 forcinrange(4): forrinrange(4): out[r+4*c]=s[r][c] returnoutdef xtime(a): a<<=1 ifa&0x100: a^=0x11b returna&0xffdef mul2(a):returnxtime(a)def mul3(a):returnmul2(a)^adef sub_bytes_state(s):return[[SBOX[v]forvinrow]forrowins]def shift_rows_state(s): return[ [s[0][0], s[0][1], s[0][2], s[0][3]], [s[1][1], s[1][2], s[1][3], s[1][0]], [s[2][2], s[2][3], s[2][0], s[2][1]], [s[3][3], s[3][0], s[3][1], s[3][2]], ]def mix_columns_state(s): out=[[0]*4for_inrange(4)] forcinrange(4): a0,a1,a2,a3=s[0][c], s[1][c], s[2][c], s[3][c] out[0][c]=(mul2(a0)^mul3(a1)^a2^a3)&0xff out[1][c]=(a0^mul2(a1)^mul3(a2)^a3)&0xff out[2][c]=(a0^a1^mul2(a2)^mul3(a3))&0xff out[3][c]=(mul3(a0)^a1^a2^mul2(a3))&0xff returnoutdef add_round_key_state(s, rkey): rk=bytes_to_state(rkey) return[[ (s[r][c]^rk[r][c])&0xffforcinrange(4)]forrinrange(4)]def aes128_encrypt_block(pt16, key16): rks=key_expansion_bytes(key16) s=bytes_to_state(pt16) s=add_round_key_state(s, rks[0]) forrinrange(1,10): s=sub_bytes_state(s); s=shift_rows_state(s); s=mix_columns_state(s); s=add_round_key_state(s, rks[r]) s=sub_bytes_state(s); s=shift_rows_state(s); s=add_round_key_state(s, rks[10]) returnstate_to_bytes(s)#--------------------CPAcore--------------------HW=np.array([bin(x).count("1")forxinrange(256)], dtype=np.uint8)SBOX_np=np.array(SBOX, dtype=np.uint8)def recover_key_cpa(pts, traces, window=None, verbose=True): N,T=traces.shape ifwindowisnotNone: s, e=window ifnot (0<=s<e<=T): raiseValueError("Bad window range") traces=traces[:, s:e] tr=traces.astype(np.float32) tr-=tr.mean(axis=0, keepdims=True) std=tr.std(axis=0, ddof=1, keepdims=True) std[std==0]=1.0 tr/=std key=[] bestcorr=[] poi=[] forbinrange(16): p=pts[:, b] xors=np.bitwise_xor(p[:,None], np.arange(256, dtype=np.uint8)) # (N,256) vals=SBOX_np[xors] # (N,256) preds=HW[vals].astype(np.float32) # (N,256) preds-=preds.mean(axis=0, keepdims=True) ps=preds.std(axis=0, ddof=1, keepdims=True); ps[ps==0]=1.0 preds/=ps corr=(preds.T@ tr)/(len(p)-1) # (256,T') abs_corr=np.abs(corr) g=int(abs_corr.max(axis=1).argmax()) key.append(g) bestcorr.append(float(abs_corr[g].max())) poi.append(int(abs_corr[g].argmax())) ifverbose: print(f"[byte {b:2d}] guess=0x{g:02x}, |corr|max={bestcorr[-1]:.4f}, POI={poi[-1]}") returnkey, bestcorr, poidef main(): ap=argparse.ArgumentParser(description="Recover AES-128 key (flag) from TRS via CPA") ap.add_argument("trs", help="path to TRS file (e.g., AES128.trs)") ap.add_argument("--window", help="time window 'start:end' over samples (e.g., 50:300)") ap.add_argument("--verify", type=int,default=50, help="random verification size (0 to skip)") ap.add_argument("--no-verify", action="store_true", help="disable verification") args=ap.parse_args() pts, cts, traces, meta=read_trs(args.trs) ntr, nsamp, coding, dlen=meta print(f"[+] Loaded TRS: traces={ntr}, samples={nsamp}, coding={coding}, dlen={dlen}") window=None ifargs.window: s, e=args.window.split(":") window=(int(s), int(e)) print(f"[+] Using window: {window[0]}:{window[1]} (len={window[1]-window[0]})") key_bytes, bestcorr, poi=recover_key_cpa(pts, traces, window=window, verbose=True) key_hex=''.join(f'{x:02x}'forxinkey_bytes) key_hex_upper=key_hex.upper() print("n[+] Recovered AES-128 key (hex):", key_hex) print("[+] FLAG (uppercase with braces):", f"flag{{{key_hex_upper}}}") ifnot args.no_verify and args.verify>0: rng=random.Random(2025) idxs=rng.sample(range(ntr),min(args.verify, ntr)) ok=0 foriinidxs: ifaes128_encrypt_block(list(pts[i]), key_bytes)==list(cts[i]): ok+=1 print(f"[+] Verify: matched {ok}/{len(idxs)} = {ok/len(idxs)*100:.1f}%")if__name__=="__main__": main()'''withopen(script_path,"w", encoding="utf-8")asf: f.write(code)script_path

verifyVinByRC4(vin) {constcorrectEncrypted ="7AF2C74EAD5C2D4505E94B820275CA8C52";constuserEncrypted =this.variantRC4Encrypt(vin,"Z1X3Y4E5Z8V2A6H6");returnuserEncrypted === correctEncrypted;}

"7AF2C74EAD5C2D4505E94B820275CA8C52"

"Z1X3Y4E5Z8V2A6H6"

因为 RC4 是流加密，这里看起来是逐字节异或，并且还额外异或了 k % 256（位置索引）。我们可以尝试已知明文攻击，但这里没有已知的 VIN 和密文对应关系，只能暴力破解或者逆向加密过程

letencryptedByte = inputBytes[k]^K^(k %256);

inputBytes[k] = encryptedByte ^ K ^ (k %256)

(ciphertext[k] ^ K ^ (k % 256)) ^ K ^ (k % 256) = ciphertext[k]

我直接给出解密步骤：将 correctEncrypted 从hex转成字节数组cipherBytes（长度16）。用 key"Z1X3Y4E5Z8V2A6H6"生成相同的 RC4 密钥流（注意这里的变种 RC4 初始化）。对每个 k 从0到15，计算 plainByte = cipherBytes[k] ^ K ^ (k %256)。将 plainBytes 转成字符串，得到 VIN。

functiondecryptVin(){ constcorrectEncrypted="7AF2C74EAD5C2D4505E94B820275CA8C52"; constkey="Z1X3Y4E5Z8V2A6H6"; // 将16进制字符串转换为字节数组 functionhexToBytes(hex){ constbytes=[]; for(leti=0; i < hex.length; i +=2) { bytes.push(parseInt(hex.substr(i,2),16)); } returnbytes; } // 字符串转字节数组 functionstringToBytes(str){ letbytes=[]; for(leti=0; i < str.length; i++) { bytes.push(str.charCodeAt(i)); } returnbytes; } // 字节数组转字符串 functionbytesToString(bytes){ letstr=''; for(leti=0; i < bytes.length; i++) { str += String.fromCharCode(bytes[i]); } returnstr; } // 变种RC4解密（与加密过程相同，因为XOR是对称的） functionvariantRC4Decrypt(cipherBytes, key){ letS=Array.from({length:256}, (_, i) => i); letj=0; letkeyBytes=stringToBytes(key); // RC4 KSA (Key Scheduling Algorithm) - 正向 for(leti=0; i <256; i++) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } // 额外的反向KSA（与加密相同） j =0; for(leti=255; i >=0; i--) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } leti=0; j =0; letoutput=[]; // 生成密钥流并解密 for(letk=0; k < cipherBytes.length; k++) { i = (i +1) %256; j = (j + S[i]) %256; [S[i], S[j]] = [S[j], S[i]]; lett=(S[i] + S[j]) %256; letK=S[(S[i] + S[j] + S[t]) %256]; // 解密：cipher ^ K ^ position = plain letdecryptedByte=cipherBytes[k] ^ K ^ (k %256); output.push(decryptedByte); } returnoutput; } // 执行解密 constcipherBytes=hexToBytes(correctEncrypted); constdecryptedBytes=variantRC4Decrypt(cipherBytes, key); constvin=bytesToString(decryptedBytes); console.log("解密得到的 VIN:", vin); console.log("Flag格式: FLAG{"+ vin +"}"); // 验证解密是否正确 functionvariantRC4Encrypt(input, key){ letS=Array.from({length:256}, (_, i) => i); letj=0; letkeyBytes=stringToBytes(key); for(leti=0; i <256; i++) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } j =0; for(leti=255; i >=0; i--) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } leti_val=0; j =0; letoutput=[]; letinputBytes=stringToBytes(input); for(letk=0; k < inputBytes.length; k++) { i_val = (i_val +1) %256; j = (j + S[i_val]) %256; [S[i_val], S[j]] = [S[j], S[i_val]]; lett=(S[i_val] + S[j]) %256; letK=S[(S[i_val] + S[j] + S[t]) %256]; letencryptedByte=inputBytes[k] ^ K ^ (k %256); output.push(encryptedByte); } // 字节数组转16进制字符串 functionbytesToHex(bytes){ lethex=''; for(leti=0; i < bytes.length; i++) { letbyte=bytes[i]; letchar1=Math.floor(byte/16); letchar2=byte%16; hex +="0123456789ABCDEF"[char1] +"0123456789ABCDEF"[char2]; } returnhex; } returnbytesToHex(output); } constreEncrypted=variantRC4Encrypt(vin, key); console.log("重新加密验证:", reEncrypted); console.log("验证结果:", reEncrypted === correctEncrypted ?"成功":"失败"); returnvin;}// 运行解密decryptVin();

运行即可得到flag

#!/usr/bin/env python3"""CAN数据提取脚本 - 统计每个信号出现次数最多的值"""importre, csv, sysfromcollectionsimportdefaultdict, CounterCAN_LINE_RE = re.compile(r'(([d.]+))s+can0s+([0-9a-fA-F]+)#([0-9a-fA-F]+)')defparse_signal_map(path='signal_map.csv'): """解析信号映射表""" signals = {} withopen(path,'r', encoding='utf-8')asf: r = csv.DictReader(f) forrowinr: signals[row['signal']] = { 'can_id':int(row['can_id'],16), 'byte':int(row['byte']), 'len':int(row['len']), 'type': row['type'] } returnsignalsdefload_frames(path): """加载CAN数据帧""" frames = [] withopen(path,'r', encoding='utf-8')asf: forlineinf: m = CAN_LINE_RE.match(line.strip()) ifnotm: continue ts =float(m.group(1)) cid =int(m.group(2),16) data =bytes.fromhex(m.group(3)) frames.append((ts, cid, data)) returnframesdefextract_all_signals_data(frames, signals): """提取所有信号的所有数据""" signal_data = defaultdict(list) forts, cid, datainframes: forsig_name, infoinsignals.items(): ifcid == info['can_id']andlen(data) > info['byte']: byte_pos = info['byte'] length = info['len'] # 提取值（根据长度） iflength ==1: value = data[byte_pos] eliflength ==2: value = data[byte_pos] | (data[byte_pos+1] <<8) else: value = data[byte_pos] signal_data[sig_name].append(value) returnsignal_datadefmain(): iflen(sys.argv) <2: print("用法: python 1.py canlog.txt") sys.exit(1) canlog = sys.argv[1] signals = parse_signal_map() frames = load_frames(canlog) signal_data = extract_all_signals_data(frames, signals) # 输出到文件 withopen('signal_most_frequent.txt','w', encoding='utf-8')asf: # 按信号数字大小排序 sorted_signals =sorted(signal_data.keys(), key=lambdax:int(x.split('_')[1])ifx.startswith('sig_')else0) forsig_nameinsorted_signals: # 统计每个值出现的次数 value_counts = Counter(signal_data[sig_name]) # 找到出现次数最多的值 ifvalue_counts: most_common_value, count = value_counts.most_common(1)[0] # 转换为ASCII字符表示 if0<= most_common_value <=255: ascii_char =chr(most_common_value) char_repr =f"'{ascii_char}'"ifascii_char.isprintable()elsef"(非打印字符:{most_common_value})" else: char_repr =f"(数值:{most_common_value})" f.write(f"{sig_name}: 最常出现值={char_repr}, 出现次数={count}n") else: f.write(f"{sig_name}: 无数据n")if__name__ =="__main__": main()

KSA：j = (j + S[i] + key[i % L] + 3) mod 256（多了常数 +3），并对 S[i] 与 S[j] 交换；初始 S[i]=i（虽然你那堆 SSE 常量很绕，本质就是 0..255）。PRGA：每轮i = (i + 1) mod 256j = (j + S[i]) mod 256交换 S[i] 与 S[j]t = (S[i] + S[j]) mod 256取 S[t] 的低 8 位当作密钥字节，与明文字节异或（这点也按你的实现用“32 位数组 + 取低字节”对齐了）

# hardcoded inputsC ="3017284f2ed903814311c68d5149bf5c12"RK =b"SecretKey" PK =b"PMZPFVDM" defksa_plus3(k): S=list(range(256)); j=0; L=len(k) foriinrange(256): j=(j+S[i]+k[i%L]+3)&255 S[i],S[j]=S[j],S[i] returnSdefrc4_stream(S, data): i=j=0; out=bytearray() forbindata: i=(i+1)&255; j=(j+S[i])&255 S[i],S[j]=S[j],S[i] out.append(b ^ S[(S[i]+S[j])&255]) returnbytes(out)definvert_pre(y, key): L=len(key) returnbytes((((y[i]^key[i%L]) - key[i%L]) &0xFF)foriinrange(len(y)))pre = rc4_stream(ksa_plus3(RK),bytes.fromhex(C)) orig = invert_pre(pre, PK) print(f"flag{{{orig.decode('ascii')}}}")


```
为深化推动前沿技术创新应用，本次竞赛聚焦国家战略需求和地方产业布局，围绕行业领域网络安全中的现实问题进行设计，共设置“漏洞智能分析”、“天基互联网安全”、“车联网安全”三个行业领域赛道，评估检验国内优势团队在智能化漏洞分析、天基网络数据分析、车联网安全测试等方面的能力
```



```
安全研究人员在进行某品牌汽车硬件安全测试时，发现其中某核心零部件内用于实现AES密码算法的芯片存在侧信道信息泄露。研究人员对该芯片执行密码运算过程中的功耗信息进行了采集，并确认可以利用该数据集进行侧信道攻击取得算法密钥，请尝试利用技术手段复现研究人员获取到的密钥信息，该密钥即为题解。 给我进行分析 题目内容并且给我分析题目打印flag
```



```
读取与检查（TRS）解析 TRS 头部，拿到：轨迹条数ntraces每条采样点数nsamples（这里是500）附带数据长度dlen（这里是32：16B PT +16B CT）逐条读入：pts[i]（明文16字节）cts[i]（密文16字节）traces[i, 0..nsamples-1]（功耗序列）这一步只是在把数据搬到内存，后面统计要用。
```



```
对功耗矩阵traces 做按列标准化（去均值、单位方差）：目的：抵消慢漂移/量纲差异，让“相关性”可比操作：tr= (traces - mean(traces, axis=0)) / std(traces, axis=0)
```



```
把 16 个最优字节连起来得到候选主密钥K*。用标准 AES-128 实现对多条（随机抽样）明文做加密，比较结果是否等于数据集中附带的密文：
```



```
#Re-create theCPArecovery script after kernel resetscript_path="/mnt/data/recover_aes_flag_cpa.py"code=r'''#!/usr/bin/env python3#-*-coding: utf-8-*-"""Recover AES-128 master key (flag) from a Riscure TRS dataset via CPA.- Pure Python + NumPy.- Leakage model: First-round SubBytes + Hamming Weight.- Output: hex key + flag{UPPERCASE_HEX}.Usage: python recover_aes_flag_cpa.py AES128.trs python recover_aes_flag_cpa.py AES128.trs --window 50:300 --verify 200 python recover_aes_flag_cpa.py AES128.trs --no-verify"""importargparse, os, sys, randomimportnumpy as np#--------------------TRSparsing--------------------def parse_trs_header(f): f.seek(0) header={} whileTrue: t=f.read(1) ifnot t:break l=f.read(1) ifnot l:break t=t[0]; l=l[0] v=f.read(l) header[t]=v ift==0x5F: # end-of-header break returnheader, f.tell()def read_trs(path): withopen(path,"rb")asf: header, offset=parse_trs_header(f) ntraces =int.from_bytes(header.get(0x41, b"x00x00x00x00"),"little") nsamples=int.from_bytes(header.get(0x42, b"x00x00x00x00"),"little") coding =int.from_bytes(header.get(0x43, b"x00"),"little") dlen =int.from_bytes(header.get(0x44, b"x00x00"),"little") ifdlen<32: raiseValueError("TRS record data length < 32 (need 16B PT + 16B CT).") pts=np.empty((ntraces,16), dtype=np.uint8) cts=np.empty((ntraces,16), dtype=np.uint8) traces=np.empty((ntraces, nsamples), dtype=np.uint8) withopen(path,"rb")asf: f.seek(offset) foriinrange(ntraces): meta=f.read(dlen) iflen(meta)!=dlen: raiseEOFError("Unexpected EOF while reading metadata") pts[i]=np.frombuffer(meta[:16], dtype=np.uint8) cts[i]=np.frombuffer(meta[16:32], dtype=np.uint8) pw=f.read(nsamples) iflen(pw)!=nsamples: raiseEOFError("Unexpected EOF while reading power trace") traces[i]=np.frombuffer(pw, dtype=np.uint8) returnpts, cts, traces, (ntraces, nsamples, coding, dlen)#--------------------AES(encryptforverification)--------------------SBOX=[ 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76, 0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0, 0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15, 0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75, 0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84, 0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf, 0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8, 0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2, 0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73, 0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb, 0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79, 0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08, 0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a, 0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e, 0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf, 0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]RCON=[0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]def sub_word(w):return[SBOX[b]forbinw]def key_expansion_bytes(key16): w=[list(key16[i:i+4])foriinrange(0,16,4)] foriinrange(4,44): temp=w[i-1].copy() ifi%4==0: temp=sub_word(temp[1:]+temp[:1]) temp[0]^=RCON[i//4] w.append([ (w[i-4][j]^temp[j])&0xffforjinrange(4) ]) rks=[] forrinrange(11): rks.append(sum(w[4*r:4*r+4], [])) returnrksdef bytes_to_state(b16): s=[[0]*4for_inrange(4)] forcinrange(4): forrinrange(4): s[r][c]=b16[r+4*c] returnsdef state_to_bytes(s): out=[0]*16 forcinrange(4): forrinrange(4): out[r+4*c]=s[r][c] returnoutdef xtime(a): a<<=1 ifa&0x100: a^=0x11b returna&0xffdef mul2(a):returnxtime(a)def mul3(a):returnmul2(a)^adef sub_bytes_state(s):return[[SBOX[v]forvinrow]forrowins]def shift_rows_state(s): return[ [s[0][0], s[0][1], s[0][2], s[0][3]], [s[1][1], s[1][2], s[1][3], s[1][0]], [s[2][2], s[2][3], s[2][0], s[2][1]], [s[3][3], s[3][0], s[3][1], s[3][2]], ]def mix_columns_state(s): out=[[0]*4for_inrange(4)] forcinrange(4): a0,a1,a2,a3=s[0][c], s[1][c], s[2][c], s[3][c] out[0][c]=(mul2(a0)^mul3(a1)^a2^a3)&0xff out[1][c]=(a0^mul2(a1)^mul3(a2)^a3)&0xff out[2][c]=(a0^a1^mul2(a2)^mul3(a3))&0xff out[3][c]=(mul3(a0)^a1^a2^mul2(a3))&0xff returnoutdef add_round_key_state(s, rkey): rk=bytes_to_state(rkey) return[[ (s[r][c]^rk[r][c])&0xffforcinrange(4)]forrinrange(4)]def aes128_encrypt_block(pt16, key16): rks=key_expansion_bytes(key16) s=bytes_to_state(pt16) s=add_round_key_state(s, rks[0]) forrinrange(1,10): s=sub_bytes_state(s); s=shift_rows_state(s); s=mix_columns_state(s); s=add_round_key_state(s, rks[r]) s=sub_bytes_state(s); s=shift_rows_state(s); s=add_round_key_state(s, rks[10]) returnstate_to_bytes(s)#--------------------CPAcore--------------------HW=np.array([bin(x).count("1")forxinrange(256)], dtype=np.uint8)SBOX_np=np.array(SBOX, dtype=np.uint8)def recover_key_cpa(pts, traces, window=None, verbose=True): N,T=traces.shape ifwindowisnotNone: s, e=window ifnot (0<=s<e<=T): raiseValueError("Bad window range") traces=traces[:, s:e] tr=traces.astype(np.float32) tr-=tr.mean(axis=0, keepdims=True) std=tr.std(axis=0, ddof=1, keepdims=True) std[std==0]=1.0 tr/=std key=[] bestcorr=[] poi=[] forbinrange(16): p=pts[:, b] xors=np.bitwise_xor(p[:,None], np.arange(256, dtype=np.uint8)) # (N,256) vals=SBOX_np[xors] # (N,256) preds=HW[vals].astype(np.float32) # (N,256) preds-=preds.mean(axis=0, keepdims=True) ps=preds.std(axis=0, ddof=1, keepdims=True); ps[ps==0]=1.0 preds/=ps corr=(preds.T@ tr)/(len(p)-1) # (256,T') abs_corr=np.abs(corr) g=int(abs_corr.max(axis=1).argmax()) key.append(g) bestcorr.append(float(abs_corr[g].max())) poi.append(int(abs_corr[g].argmax())) ifverbose: print(f"[byte {b:2d}] guess=0x{g:02x}, |corr|max={bestcorr[-1]:.4f}, POI={poi[-1]}") returnkey, bestcorr, poidef main(): ap=argparse.ArgumentParser(description="Recover AES-128 key (flag) from TRS via CPA") ap.add_argument("trs", help="path to TRS file (e.g., AES128.trs)") ap.add_argument("--window", help="time window 'start:end' over samples (e.g., 50:300)") ap.add_argument("--verify", type=int,default=50, help="random verification size (0 to skip)") ap.add_argument("--no-verify", action="store_true", help="disable verification") args=ap.parse_args() pts, cts, traces, meta=read_trs(args.trs) ntr, nsamp, coding, dlen=meta print(f"[+] Loaded TRS: traces={ntr}, samples={nsamp}, coding={coding}, dlen={dlen}") window=None ifargs.window: s, e=args.window.split(":") window=(int(s), int(e)) print(f"[+] Using window: {window[0]}:{window[1]} (len={window[1]-window[0]})") key_bytes, bestcorr, poi=recover_key_cpa(pts, traces, window=window, verbose=True) key_hex=''.join(f'{x:02x}'forxinkey_bytes) key_hex_upper=key_hex.upper() print("n[+] Recovered AES-128 key (hex):", key_hex) print("[+] FLAG (uppercase with braces):", f"flag{{{key_hex_upper}}}") ifnot args.no_verify and args.verify>0: rng=random.Random(2025) idxs=rng.sample(range(ntr),min(args.verify, ntr)) ok=0 foriinidxs: ifaes128_encrypt_block(list(pts[i]), key_bytes)==list(cts[i]): ok+=1 print(f"[+] Verify: matched {ok}/{len(idxs)} = {ok/len(idxs)*100:.1f}%")if__name__=="__main__": main()'''withopen(script_path,"w", encoding="utf-8")asf: f.write(code)script_path
```



```
verifyVinByRC4(vin) {constcorrectEncrypted ="7AF2C74EAD5C2D4505E94B820275CA8C52";constuserEncrypted =this.variantRC4Encrypt(vin,"Z1X3Y4E5Z8V2A6H6");returnuserEncrypted === correctEncrypted;}
```



```
"7AF2C74EAD5C2D4505E94B820275CA8C52"
```



```
"Z1X3Y4E5Z8V2A6H6"
```



```
因为 RC4 是流加密，这里看起来是逐字节异或，并且还额外异或了 k % 256（位置索引）。我们可以尝试已知明文攻击，但这里没有已知的 VIN 和密文对应关系，只能暴力破解或者逆向加密过程
```



```
letencryptedByte = inputBytes[k]^K^(k %256);
```



```
inputBytes[k] = encryptedByte ^ K ^ (k %256)
```



```
(ciphertext[k] ^ K ^ (k % 256)) ^ K ^ (k % 256) = ciphertext[k]
```



```
我直接给出解密步骤：将 correctEncrypted 从hex转成字节数组cipherBytes（长度16）。用 key"Z1X3Y4E5Z8V2A6H6"生成相同的 RC4 密钥流（注意这里的变种 RC4 初始化）。对每个 k 从0到15，计算 plainByte = cipherBytes[k] ^ K ^ (k %256)。将 plainBytes 转成字符串，得到 VIN。
```



```
functiondecryptVin(){ constcorrectEncrypted="7AF2C74EAD5C2D4505E94B820275CA8C52"; constkey="Z1X3Y4E5Z8V2A6H6"; // 将16进制字符串转换为字节数组 functionhexToBytes(hex){ constbytes=[]; for(leti=0; i < hex.length; i +=2) { bytes.push(parseInt(hex.substr(i,2),16)); } returnbytes; } // 字符串转字节数组 functionstringToBytes(str){ letbytes=[]; for(leti=0; i < str.length; i++) { bytes.push(str.charCodeAt(i)); } returnbytes; } // 字节数组转字符串 functionbytesToString(bytes){ letstr=''; for(leti=0; i < bytes.length; i++) { str += String.fromCharCode(bytes[i]); } returnstr; } // 变种RC4解密（与加密过程相同，因为XOR是对称的） functionvariantRC4Decrypt(cipherBytes, key){ letS=Array.from({length:256}, (_, i) => i); letj=0; letkeyBytes=stringToBytes(key); // RC4 KSA (Key Scheduling Algorithm) - 正向 for(leti=0; i <256; i++) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } // 额外的反向KSA（与加密相同） j =0; for(leti=255; i >=0; i--) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } leti=0; j =0; letoutput=[]; // 生成密钥流并解密 for(letk=0; k < cipherBytes.length; k++) { i = (i +1) %256; j = (j + S[i]) %256; [S[i], S[j]] = [S[j], S[i]]; lett=(S[i] + S[j]) %256; letK=S[(S[i] + S[j] + S[t]) %256]; // 解密：cipher ^ K ^ position = plain letdecryptedByte=cipherBytes[k] ^ K ^ (k %256); output.push(decryptedByte); } returnoutput; } // 执行解密 constcipherBytes=hexToBytes(correctEncrypted); constdecryptedBytes=variantRC4Decrypt(cipherBytes, key); constvin=bytesToString(decryptedBytes); console.log("解密得到的 VIN:", vin); console.log("Flag格式: FLAG{"+ vin +"}"); // 验证解密是否正确 functionvariantRC4Encrypt(input, key){ letS=Array.from({length:256}, (_, i) => i); letj=0; letkeyBytes=stringToBytes(key); for(leti=0; i <256; i++) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } j =0; for(leti=255; i >=0; i--) { j = (j + S[i] + keyBytes[i % keyBytes.length]) %256; [S[i], S[j]] = [S[j], S[i]]; } leti_val=0; j =0; letoutput=[]; letinputBytes=stringToBytes(input); for(letk=0; k < inputBytes.length; k++) { i_val = (i_val +1) %256; j = (j + S[i_val]) %256; [S[i_val], S[j]] = [S[j], S[i_val]]; lett=(S[i_val] + S[j]) %256; letK=S[(S[i_val] + S[j] + S[t]) %256]; letencryptedByte=inputBytes[k] ^ K ^ (k %256); output.push(encryptedByte); } // 字节数组转16进制字符串 functionbytesToHex(bytes){ lethex=''; for(leti=0; i < bytes.length; i++) { letbyte=bytes[i]; letchar1=Math.floor(byte/16); letchar2=byte%16; hex +="0123456789ABCDEF"[char1] +"0123456789ABCDEF"[char2]; } returnhex; } returnbytesToHex(output); } constreEncrypted=variantRC4Encrypt(vin, key); console.log("重新加密验证:", reEncrypted); console.log("验证结果:", reEncrypted === correctEncrypted ?"成功":"失败"); returnvin;}// 运行解密decryptVin();
```



```
#!/usr/bin/env python3"""CAN数据提取脚本 - 统计每个信号出现次数最多的值"""importre, csv, sysfromcollectionsimportdefaultdict, CounterCAN_LINE_RE = re.compile(r'(([d.]+))s+can0s+([0-9a-fA-F]+)#([0-9a-fA-F]+)')defparse_signal_map(path='signal_map.csv'): """解析信号映射表""" signals = {} withopen(path,'r', encoding='utf-8')asf: r = csv.DictReader(f) forrowinr: signals[row['signal']] = { 'can_id':int(row['can_id'],16), 'byte':int(row['byte']), 'len':int(row['len']), 'type': row['type'] } returnsignalsdefload_frames(path): """加载CAN数据帧""" frames = [] withopen(path,'r', encoding='utf-8')asf: forlineinf: m = CAN_LINE_RE.match(line.strip()) ifnotm: continue ts =float(m.group(1)) cid =int(m.group(2),16) data =bytes.fromhex(m.group(3)) frames.append((ts, cid, data)) returnframesdefextract_all_signals_data(frames, signals): """提取所有信号的所有数据""" signal_data = defaultdict(list) forts, cid, datainframes: forsig_name, infoinsignals.items(): ifcid == info['can_id']andlen(data) > info['byte']: byte_pos = info['byte'] length = info['len'] # 提取值（根据长度） iflength ==1: value = data[byte_pos] eliflength ==2: value = data[byte_pos] | (data[byte_pos+1] <<8) else: value = data[byte_pos] signal_data[sig_name].append(value) returnsignal_datadefmain(): iflen(sys.argv) <2: print("用法: python 1.py canlog.txt") sys.exit(1) canlog = sys.argv[1] signals = parse_signal_map() frames = load_frames(canlog) signal_data = extract_all_signals_data(frames, signals) # 输出到文件 withopen('signal_most_frequent.txt','w', encoding='utf-8')asf: # 按信号数字大小排序 sorted_signals =sorted(signal_data.keys(), key=lambdax:int(x.split('_')[1])ifx.startswith('sig_')else0) forsig_nameinsorted_signals: # 统计每个值出现的次数 value_counts = Counter(signal_data[sig_name]) # 找到出现次数最多的值 ifvalue_counts: most_common_value, count = value_counts.most_common(1)[0] # 转换为ASCII字符表示 if0<= most_common_value <=255: ascii_char =chr(most_common_value) char_repr =f"'{ascii_char}'"ifascii_char.isprintable()elsef"(非打印字符:{most_common_value})" else: char_repr =f"(数值:{most_common_value})" f.write(f"{sig_name}: 最常出现值={char_repr}, 出现次数={count}n") else: f.write(f"{sig_name}: 无数据n")if__name__ =="__main__": main()
```



```
KSA：j = (j + S[i] + key[i % L] + 3) mod 256（多了常数 +3），并对 S[i] 与 S[j] 交换；初始 S[i]=i（虽然你那堆 SSE 常量很绕，本质就是 0..255）。PRGA：每轮i = (i + 1) mod 256j = (j + S[i]) mod 256交换 S[i] 与 S[j]t = (S[i] + S[j]) mod 256取 S[t] 的低 8 位当作密钥字节，与明文字节异或（这点也按你的实现用“32 位数组 + 取低字节”对齐了）
```



```
# hardcoded inputsC ="3017284f2ed903814311c68d5149bf5c12"RK =b"SecretKey" PK =b"PMZPFVDM" defksa_plus3(k): S=list(range(256)); j=0; L=len(k) foriinrange(256): j=(j+S[i]+k[i%L]+3)&255 S[i],S[j]=S[j],S[i] returnSdefrc4_stream(S, data): i=j=0; out=bytearray() forbindata: i=(i+1)&255; j=(j+S[i])&255 S[i],S[j]=S[j],S[i] out.append(b ^ S[(S[i]+S[j])&255]) returnbytes(out)definvert_pre(y, key): L=len(key) returnbytes((((y[i]^key[i%L]) - key[i%L]) &0xFF)foriinrange(len(y)))pre = rc4_stream(ksa_plus3(RK),bytes.fromhex(C)) orig = invert_pre(pre, PK) print(f"flag{{{orig.decode('ascii')}}}")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176925-wxsync-2025-11-a123f82123c440e771bffe3704b58098.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176927-wxsync-2025-11-ade3e0d098a9782bef211ce31a96050a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176928-wxsync-2025-11-6e364a197951dd7636f4d0afd40d5e5b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176930-wxsync-2025-11-569458ea4b9c3bb51252023b00adc92e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176931-wxsync-2025-11-269cc6eb26c5c1efb0dd78d4d0ec3518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176934-wxsync-2025-11-944ff0f120c5a47ba5668a78c53d6fe0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176936-wxsync-2025-11-9f4b3c28bc7111601d9770651a6d2a9b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176937-wxsync-2025-11-06097471ec9d07fd0f6909e15c3e94bf.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176939-wxsync-2025-11-3e4d0ca5e784744eebd4cdc5fd9b4251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762176941-wxsync-2025-11-dc6d4ac7a911673b6fa6289592f76f94.png)