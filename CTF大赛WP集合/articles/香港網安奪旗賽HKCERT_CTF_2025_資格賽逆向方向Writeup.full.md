---
title: 香港網安奪旗賽HKCERT CTF 2025 資格賽逆向方向Writeup
contest: HKCERT CTF 2025 資格賽
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- SM4
- custom-SBOX
- XXTEA
- modified-TEA
- AES-custom
- custom-Base64
- rsa
- key-schedule
- cipher-reversal
attack_chain:
- '题目1SM4魔改: 重新派生SBOX_P=SBOX[(i^167)&255]再rotl8(val, i&3),tau函数4字节替换+T=tau^rotl^rotl^rotl^rotl,expand_key 32轮派生rk'
- '题目2魔改AES+自定义Base64: 32字节KEY_SEED+256字节SBOX+32字节CIPHERTEXT打包,密钥扩展10轮(每轮f=17+1~10)'
- '题目3魔改XXTEA: sum从DELTA*32开始倒推,key=[0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3],解密逆向v3/v4'
- '题目4 srand随机+alloca栈帧: time(0)^getpid()%20作为srand seed,生成36字节cipherXOR,爆破seed'
- '题目5混淆比较: 主函数将s[j]^rand()与cipher比较,绕混淆爆破随机种子'
key_payload: hkcert25{...}
one_liner: HKCERT 2025资格赛逆向方向5题,涵盖魔改SM4+自定义SBOX+魔改AES+魔改XXTEA+随机种子爆破,密码学逆向全方向深度。
lesson: 魔改对称加密的破题关键是先识别原算法(SM4/AES/XXTEA),再识别SBOX/常量/DELTA/key的修改,逐项还原。随机数种子爆破:time^pid取低20位是常见弱种子。
quality: high
full_path: 香港網安奪旗賽HKCERT_CTF_2025_資格賽逆向方向Writeup.full.md
meta_path: 香港網安奪旗賽HKCERT_CTF_2025_資格賽逆向方向Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '香港網安奪旗賽HKCERT CTF 2025 資格賽逆向方向Writeup。HKCERT 2025资格赛逆向方向5题,涵盖魔改SM4+自定义SBOX+魔改AES+魔改XXTEA+随机种子爆破,密码学逆向全方向深度。。关键路径：题目1SM4魔改: 重新派生SBOX_P=SBOX[(i^167)&255]再rotl8(val, i&3),tau函数4字节替换+T=tau^rotl^rotl^ro...'
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/288018.html
reasoning_chain:
- '5 道逆向题覆盖魔改 SM4/AES/XXTEA + 随机种子爆破 → 触发点: 密码学逆向全方向'
- '题1 SM4 魔改: 看到 SBOX[(i^167)&255] → 假设派生 SBOX_P 后再 rotl8 → 动作: 写 Python 重现 tau/T 函数'
- '观察: 标准 SM4 的线性变换 + 自定义 S 盒 → 下一步: expand_key 多 XOR MASK'
- '题2 魔改 AES: 32 字节 KEY_SEED + 256 字节 SBOX + 32 字节密文 → 假设 KEY_SEED 是字符串''8080...'''
- '动作: parse raw_data 提三段 → f_c 生成 initial_key → key_expansion 10 轮 (e = f*17) → InvMixColumns 解密'
- '题3 魔改 XXTEA: sum 从 DELTA*32 开始倒推 → 假设 idx = (sum>>2)&3 → 动作: 逐轮逆 v3/v4 还原'
- '观察: key=[0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3] 来自 .rodata → 32 轮解完得 flag'
- '题4 srand 随机: time(0)^getpid()%20 → 触发点: 弱种子只能取 0~19 → 动作: 循环 20 枚种子'
- '观察: rand()%256 XOR cipher[i] 在 seed=某值时输出明文 flag'
- '题5 混淆比较: s[j]^rand() 与 cipher 比 → 假设绕混淆爆破同 seed → 动作: 复用题 4 种子结果'
failed_attempts:
- '试图直接调 SM4 标准库解 → 失败: SBOX 与线性变换都被改'
- '试图用 AES 标准 SBOX 解 → 失败: 题目给了 256 字节新 SBOX'
- '试图猜 DELTA 常量 → 失败: DELTA=0x9E3779B9 是标准但 sum 起点必须倒算'
- '试图遍历更大 seed 范围 → 失败: time(0)^pid%20 限制 0~19 必爆'
key_observations:
- '魔改对称密码破题: 先识别原算法 (SM4/AES/XXTEA) → 再定位改动的 SBOX/DELTA/MASK/key'
- srand(time(0)^getpid())%20 是经典弱随机种子, 必爆 0~19
- XXTEA 加密 sum 起点 = DELTA*N, 解密必须从 DELTA*N 倒推
- IDA .rodata 提取的密钥永远是最干净的, 优先于伪代码推导
prerequisites:
- SM4/AES/XXTEA 算法原理 (SBOX / 线性变换 / 轮密钥)
- Python struct/位运算 + IDA 静态分析
- rand/srand 弱种子爆破思路
- 差分密码学 / 魔改密码还原通用方法
---
# 香港網安奪旗賽HKCERT CTF 2025 資格賽逆向方向Writeup

> 原文: https://www.ctfiot.com/288018.html
> ID: 288018

importstruct
# 1. 嚴格從 Java 代碼中提取的 CK 數組（註意：與標準 SM4 不衕）CK = [ 462357,472066609,943670861,1415275113,1886879365, -1936483679, -1464879427, -993275175, -521670923, -66909679,404694573,876298825,1347903077,1819507329, -2003855715, -1532251463, -1060647211, -589042959, -117504499,337322537,808926789,1280531041,1752135293, -2071227751, -1599623499, -1128019247, -656414995, -184876535,269950501,741554753,1213159005,1684763257]# 將 Java 的有符號 int 轉換爲 Python 的無符號 32位 intCK = [x &0xFFFFFFFFforxinCK]# 2. 從 Java 代碼提取的 FK 數組FK = [-1548633402,1453994832,1736282519, -1301273892]FK = [x &0xFFFFFFFFforxinFK]# 3. 從 Java 代碼提取的 SBOX（有符號 byte 轉無符號）SBOX_SIGNED = [ -42, -112, -23, -2, -52, -31,61, -73,22, -74,20, -62,40, -5,44,5,43,103, -102,118,42, -66,4, -61, -86,68,19,38,73, -122,6, -103, -100,66,80, -12, -111, -17, -104,122,51,84,11,67, -19, -49, -84,98, -28, -77,28, -87, -55,8, -24, -107, -128, -33, -108, -6,117, -113,63, -90,71,7, -89, -4, -13,115,23, -70, -125,89,60,25, -26, -123,79, -88,104,107, -127, -78,113,100, -38, -117, -8, -21,15,75,112,86, -99,53,30,36,14,94,99,88, -47, -94,37,34,124,59,1,33,120, -121, -44,0,70,87, -97, -45,39,82,76,54,2, -25, -96, -60, -56, -98, -22, -65, -118, -46,64, -57,56, -75, -93, -9, -14, -50, -7,97,21, -95, -32, -82,93, -92, -101,52,26,85, -83, -109,50,48, -11, -116, -79, -29,29, -10, -30,46, -126,102, -54,96, -64,41,35, -85,13,83,78,111, -43, -37,55,69, -34, -3, -114,47,3, -1,106,114,109,108,91,81, -115,27, -81, -110, -69, -35, -68,127,17, -39,92,65,31,16,90, -40,10, -63,49, -120, -91, -51,123, -67,45,116, -48,18, -72, -27, -76, -80, -119,105, -105,74,12, -106,119,126,101, -71, -15,9, -59,110, -58, -124,24, -16,125, -20,58, -36,77,32,121, -18,95,62, -41, -53,57,72]SBOX = [x &0xFFforxinSBOX_SIGNED]# ================= 覈心邏輯 =================defrotl(i, n):“”“32位循環左移”“”return((i << n) | (i >> (32- n))) &0xFFFFFFFFdefrotl8(i, n):“”“8位循環左移”“”return((i << n) | (i >> (8- n))) &0xFF
# 生成 SBOX_P（複現 Java static 塊）SBOX_P = [0] *256foriinrange(256):
val = SBOX[(i ^167) &255]SBOX_P[i] = rotl8(val, i &3)defsbox_transform(i):
returnSBOX_P[(i ^60) &0xFF]deftau(i):b0 = sbox_transform((i >>24) &0xFF)b1 = sbox_transform((i >>16) &0xFF)b2 = sbox_transform((i >>8) &0xFF)b3 = sbox_transform(i &0xFF)return(b0 <<24) | (b1 <<16) | (b2 <<8) | b3defT(i):t = tau(i)returnt ^ rotl(t,2) ^ rotl(t,10) ^ rotl(t,18) ^ rotl(t,24)defT_prime(i):t = tau(i)returnt ^ rotl(t,13) ^ rotl(t,23)defderive_key(seed_str):
seed_bytes = seed_str.encode('utf-8')key =bytearray(16)foriinrange(16): val = (seed_bytes[i %len(seed_bytes)] + (i *17) +35) &0xFF key[i] = valreturnbytes(key)defexpand_key(key_bytes):mk =list(struct.unpack('>4I', key_bytes))k = [0] *36k[0:4] = [mk[i] ^ FK[i]foriinrange(4)]rk = []foriinrange(32): temp = k[i+1] ^ k[i+2] ^ k[i+3] ^ CK[i] rk_val = k[i] ^ T_prime(temp) rk.append(rk_val) k[i+4] = rk_valreturnrkdefsm4_decrypt_block(block_bytes, rk_list):# SM4解密：輸入密文，使用逆序的輪密鑰X =list(struct.unpack('>4I', block_bytes))
# 輪密鑰必鬚是逆序的（rk31...rk0）rk_inv = rk_list[::-1]foriinrange(32): temp = X[1] ^ X[2] ^ X[3] ^ rk_inv[i] result = X[0] ^ T(temp) X = [X[1], X[2], X[3], result]# 解密後需要反序輸齣（X35，X34，X33，X32）-> Bytesreturnstruct.pack('>4I', X[3], X[2], X[1], X[0])
# ================= 執行解密 =================TARGET_CIPHER_HEX ="21c2692a4775c413356a31fc55c38f6218bed9d46c45bd0eb777be9334c999d7"KEY_SEED ="happ"# 1. 準備數據target_bytes =bytes.fromhex(TARGET_CIPHER_HEX)key = derive_key(KEY_SEED)
# 2. 生成輪密鑰rk = expand_key(key)
# 3. 解密plaintext =b""foriinrange(0,len(target_bytes),16):
block = target_bytes[i:i+16]plaintext += sm4_decrypt_block(block, rk)
# 4. 去除填充（PKCS7）try:
pad_len = plaintext[-1]# 簡單的填充檢查if0< pad_len <=16: plaintext = plaintext[:-pad_len]print(f"Flag:{plaintext.decode('utf-8')}")exceptExceptionase:
print(f"Decryption raw bytes:{plaintext}")print(f"Error:{e}")

importstruct
# ================= 1. 數據提取與解析 =================# 從僞代碼中提取的原始字符串（格式化處理）# xx 代錶十六進製，普通字符代錶 ASCIIraw_data_str = (r"8080XKc616^9095b56aa^Tfe9aabcd179^82f1Jcb7,90d5 87f"r"e69&-!a8159fj[=qa48df1,90d893'a0 31daaf78ef8f5c6fe("r"9aeda7c9|lead96nffbfab+82kO^9dy99Bcc_c0]Hdab8b1}e8/S"r"d9v@A4 0fa 8a8ce9sb9ude 98bZb7za6eb 1091e4c1016 295"r"8ab5f0a11917idf1fa3X% afc5f2 bf91ad5c8c7bafe6ec80"r"{Ja5a98897VIb6 5cd1eM9efd$g> 7C):
db1586xpcad21cb4e2"r"N84 4Q81bah`P135c~ 69889f68cbcfbe#bd92m7d78f14f36 c"r"aeb0? f4Re0227ftFfcee9cb287.E11e7d1d0*def<12YacT;o d"r"e3dc9bGc4bba2c2K383d4cec1Dddb394 fr85d6fbd3We5bc18"r"21bc3wUea ee1L96<d1s/acfec2 0Ve1&49ae1/b5Oa386fb87f8"r"91 a9b 0fb f8d$w")
# 解析器：將 xx 解析爲字節，其他字符保持不變data_bytes =bytearray()i =0whilei <len(raw_data_str):
ifraw_data_str[i] =='\': # 讀取後兩位作爲 hex hex_val = raw_data_str[i+1:i+3] data_bytes.append(int(hex_val,16)) i +=3else: data_bytes.append(ord(raw_data_str[i])) i +=1
# 提取關鍵區段
# Offset 0-31: 密鑰種子KEY_SEED = data_bytes[0:32]# Offset 32-288: S-Box (256 bytes)SBOX =list(data_bytes[32:
288])
# Offset 288-320: 密文（32 bytes）CIPHERTEXT = data_bytes[288:
320]# 生成逆 S-BoxINV_SBOX = [0] *256fori, vinenumerate(SBOX):
INV_SBOX[v] = i
# ================= 2. 覈心算法複現 =================# 輔助函數: f_cdeff_c(a, b, c):# return c * -23 + (a ^ b) & 255res = (c * -23+ (a ^ b)) &0xFFreturnres
# 1. 生成初始 16 字節密鑰defgenerate_initial_key(seed):
key = [0] *16fordinrange(16): # 對應僞代碼中的 Loop L_b 和 L_d # (d + i)[0] = f_c((d + 1024)[0], (d + 1040)[0], d & 255) # 1024是數據開頭，1040是數據+16 val_a = seed[d] val_b = seed[d +16] key[d] = f_c(val_a, val_b, d)returnkey
# 2. 密鑰擴展（Key Schedule）defkey_expansion(initial_key):# 存儲所有輪密鑰（11組，每組16字節）round_keys = []round_keys.append(list(initial_key))
# Round 0 Keycurrent_key =list(initial_key)
# 對應 Loop L_n -> L_q
# f 從 1 到 10forfinrange(1,11): prev_key =list(current_key) new_key = [0] *16 e = f *17 # 對應 Loop L_r # (d + g + a)[0]:
byte = (e ^ (a + c)[0]:
ubyte) ^ a; # c 是上一輪密鑰的地址，g 是當前輪密鑰地址 forainrange(16): new_key[a] = (e ^ prev_key[a]) ^ a round_keys.append(new_key) current_key = new_keyreturnround_keys
# 3. AES 逆列混淆（Inverse MixColumns）# 使用標準的 AES 逆矩陣乘法defgmul(a, b):p =0for_inrange(8): ifb &1: p ^= a hi_bit_set = a &0x80 a <<=1 ifhi_bit_set: a ^=0x1B b >>=1returnp &0xFFdefinv_mix_columns(state):# state: list of 16 bytesnew_state = [0] *16forcinrange(4): col = state[c*4: c*4+4] # InvMixColumns Matrix: # 14 11 13 9 # 9 14 11 13 # 13 9 14 11 # 11 13 9 14 new_state[c*4+0] = gmul(col[0],14) ^ gmul(col[1],11) ^ gmul(col[2],13) ^ gmul(col[3],9) new_state[c*4+1] = gmul(col[0],9) ^ gmul(col[1],14) ^ gmul(col[2],11) ^ gmul(col[3],13) new_state[c*4+2] = gmul(col[0],13) ^ gmul(col[1],9) ^ gmul(col[2],14) ^ gmul(col[3],11) new_state[c*4+3] = gmul(col[0],11) ^ gmul(col[1],13) ^ gmul(col[2],9) ^ gmul(col[3],14)returnnew_state
# 4. 解密單個 Blockdefdecrypt_block(ciphertext_block, round_keys):
state =list(ciphertext_block)
# Initial AddRoundKey (Round 10)rk = round_keys[10]state = [b ^ kforb, kinzip(state, rk)]# Rounds 9 down to 1forrinrange(9,0, -1): # InvShiftRows # Row 1: shift right 1 (inv of left 1) state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9] # Row 2: shift right 2 state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6] # Row 3: shift right 3 state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3] # InvSubBytes state = [INV_SBOX[b]forbinstate] # AddRoundKey rk = round_keys[r] state = [b ^ kforb, kinzip(state, rk)] # InvMixColumns state = inv_mix_columns(state)
# Round 0 (Final)
# InvShiftRowsstate[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]# InvSubBytesstate = [INV_SBOX[b]forbinstate]# AddRoundKey (Round 0)rk = round_keys[0]state = [b ^ kforb, kinzip(state, rk)]returnbytes(state)
# ================= 3. 執行 =================# 計算密鑰initial_key = generate_initial_key(KEY_SEED)print(f"Initial Key:{bytes(initial_key).hex()}")
# 擴展密鑰round_keys = key_expansion(initial_key)
# 解密（處理兩個 block）flag_bytes =b""foriinrange(0,32,16):
block = CIPHERTEXT[i : i+16]decrypted = decrypt_block(block, round_keys)flag_bytes += decryptedprint(f"Decrypted:{flag_bytes}")
# 去除 padding（假設最後是 null 或者 pkcs7，直接轉 string 試試）try:
print(f"Flag:{flag_bytes.decode('utf-8').strip()}")
except:
print("Flag contains non-printable chars, check hex.")

importstructdefto_uint32(x):
returnx &0xFFFFFFFFdefdecrypt():# 1. 目標密文
# 來自:（v3 ^ 0x6421ACBE |（unsigned int）v4 ^ 0xFA7CB432）== 0v3 =0x6421ACBEv4 =0xFA7CB432 # 2. 真正的密鑰（從 IDA .rodata 穫取）# Hex: 0F 1E 2D 3C 4B 5A 69 78 87 96 A5 B4 C3 D2 E1 F0
# Little Endian 解析k = [0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3]# 3. Delta 和 Sum 配置DELTA =0x9E3779B9 # 關於 Sum 的初始值：# 加密循環是：# v6 = DELTA;# do { ...使用 v6...； v6 += DELTA； } while（...）運行 32 次
# 第 1 輪使用 DELTA * 1 # ...# 第 32 輪使用 DELTA * 32
# 所以解密時，我們要從第 32 輪的狀態開始，即 sum = DELTA * 32sum_val = to_uint32(DELTA *32)for_inrange(32): # 4. 逆曏 v4 # 索引計算:（sum >> 2）& 3 idx = (sum_val >>2) &3 # 加密邏輯迴顧: # term1 = ((v3 >> 5) ^ (v3 << 2)) + ((v3 >> 3) ^ (v3 << 4)) # term2 = (sum ^ v3) + (v3 ^ k[idx ^ 1]) # v4 += term1 ^ term2 # 解密邏輯: v4 -= term1 ^ term2 term1 = ((v3 >>5) ^ (v3 <<2)) + ((v3 >>3) ^ (v3 <<4)) term2 = (sum_val ^ v3) + (v3 ^ k[idx ^1]) v4 = to_uint32(v4 - (term1 ^ term2)) # 5. 逆曏 v3 # 加密邏輯迴顧: # term3 = ((v4 >> 5) ^ (v4 << 2)) + ((v4 >> 3) ^ (v4 << 4)) # term4 = (sum ^ v4) + (v4 ^ k[idx]) # v3 += term3 ^ term4 # 解密邏輯: v3 -= term3 ^ term4 term3 = ((v4 >>5) ^ (v4 <<2)) + ((v4 >>3) ^ (v4 <<4)) term4 = (sum_val ^ v4) + (v4 ^ k[idx]) v3 = to_uint32(v3 - (term3 ^ term4)) # 6. Sum 遞減 sum_val = to_uint32(sum_val - DELTA)returnstruct.pack("> (j*8)) &255; // little-endian

int__cdeclmain(intargc,constchar**argv,constchar**envp){unsignedintv3;// ebx__pid_tv4;// eaxvoid*v5;// rspvoid*v7;// rsp__int64 v8[7];// [rsp+8h] [rbp-4A0h] BYREFunsigned__int64 j;// [rsp+40h] [rbp-468h]size_tv10;// [rsp+48h] [rbp-460h]unsigned__int64 i;// [rsp+50h] [rbp-458h]__int64 v12;// [rsp+58h] [rbp-450h]__int64 *v13;// [rsp+60h] [rbp-448h]__int64 v14;// [rsp+68h] [rbp-440h]void*s1;// [rsp+70h] [rbp-438h]chars[1032];// [rsp+78h] [rbp-430h] BYREFunsigned__int64 v17;// [rsp+480h] [rbp-28h]v17 = __readfsqword(0x28u);v3 =time(0LL);v4 =getpid();srand((v4 ^ v3) %0x14);v12 =35LL;v8[4] =36LL;v8[5] =0LL;v8[2] =36LL;v8[3] =0LL;v5 =alloca(48LL);v13 = v8;for( i =0LL; i <0x24; ++i )*((_BYTE *)v13 + i) =rand();printf("Enter your guess (exactly %zu bytes): ",0x24uLL);if(fgets(s,1024, stdin) ){v10 =strlen(s);if( v10 && s[v10 -1] ==10) s[--v10] =0;if( v10 ==36) { v14 =35LL; v8[0] =36LL; v8[1] =0LL; v7 =alloca(48LL); s1 = v8; for( j =0LL; j <0x24; ++j ) *((_BYTE *)s1 + j) = *((_BYTE *)v13 + j) ^ s[j]; if( !memcmp(s1, &cipher,0x24uLL) ) puts("Correct! Your input is the plaintext."); else puts("Incorrect."); return0; }else { printf("Wrong length: expected %zu, got %zun",0x24uLL, v10); return1; }}else{fwrite("No inputn",1uLL,9uLL, stderr);return1;}}

db 1Fh ; DATA XREF: main+386↑o cipher db 1Fh ; DATA XREF: main+386↑o cipher db 1Fh ; DATA XREF: main+386↑o.rodata:
0000000000002021 db 0C9h .rodata:
0000000000002021 db 0C9h.rodata:
0000000000002022 db 0EDh .rodata:
0000000000002022 db 0EDh.rodata:
0000000000002023 db 29h ; ) .rodata:
0000000000002023 db 29h ; ).rodata:
0000000000002024 db 0A6h .rodata:
0000000000002024 db 0A6h.rodata:
0000000000002025 db 0FEh .rodata:
0000000000002025 db 0FEh.rodata:
0000000000002026 db 44h ; D .rodata:
0000000000002026 db 44h ; D.rodata:
0000000000002027 db 0EEh .rodata:
0000000000002027 db 0EEh.rodata:
0000000000002028 db 82h .rodata:
0000000000002028 db 82h.rodata:
0000000000002029 db 45h ; E .rodata:
0000000000002029 db 45h ; E.rodata:
000000000000202A db 0E9h .rodata:
000000000000202A db 0E9h.rodata:
000000000000202B db 0D8h .rodata:
000000000000202B db 0D8h.rodata:
000000000000202C db 7Fh ; .rodata:
000000000000202C db 7Fh ;.rodata:
000000000000202D db 42h ; B .rodata:
000000000000202D db 42h ; B.rodata:
000000000000202E db 10h .rodata:
000000000000202E db 10h.rodata:
000000000000202F db 0E0h .rodata:
000000000000202F db 0E0h.rodata:
0000000000002030 db 0BBh .rodata:
0000000000002030 db 0BBh.rodata:
0000000000002031 db 4Bh ; K .rodata:
0000000000002031 db 4Bh ; K.rodata:
0000000000002032 db 0D0h .rodata:
0000000000002032 db 0D0h.rodata:
0000000000002033 db 5 .rodata:
0000000000002033 db 5.rodata:
0000000000002034 db 4Ch ; L .rodata:
0000000000002034 db 4Ch ; L.rodata:
0000000000002035 db 76h ; v .rodata:
0000000000002035 db 76h ; v.rodata:
0000000000002036 db 90h .rodata:
0000000000002036 db 90h.rodata:
0000000000002037 db 0CBh .rodata:
0000000000002037 db 0CBh.rodata:
0000000000002038 db 48h ; H .rodata:
0000000000002038 db 48h ; H.rodata:
0000000000002039 db 9Ch .rodata:
0000000000002039 db 9Ch.rodata:
000000000000203A db 7Ah ; z .rodata:
000000000000203A db 7Ah ; z.rodata:
000000000000203B db 0A9h .rodata:
000000000000203B db 0A9h.rodata:
000000000000203C db 0F0h .rodata:
000000000000203C db 0F0h.rodata:
000000000000203D db 33h ; 3 .rodata:
000000000000203D db 33h ; 3.rodata:
000000000000203E db 55h ; U .rodata:
000000000000203E db 55h ; U.rodata:
000000000000203F db 25h ; % .rodata:
000000000000203F db 25h ; %.rodata:
0000000000002040 db 64h ; d .rodata:
0000000000002040 db 64h ; d.rodata:
0000000000002041 db 88h .rodata:
0000000000002041 db 88h.rodata:
0000000000002042 db 3Dh ; = .rodata:
0000000000002042 db 3Dh ; =.rodata:
0000000000002043 db 0F7h .rodata:
0000000000002043 db 0F7h.rodata:
0000000000002044 db 0 .rodata:
0000000000002044 db 0.rodata:
0000000000002045 db 0 .rodata:
0000000000002045 db 0.rodata:
0000000000002046 db 0 .rodata:
0000000000002046 db 0.rodata:
0000000000002047 db 0 .rodata:
0000000000002047 db 0.rodata:
0000000000002048 cipher_len db 24h ; $.rodata:
0000000000002049 db 0 .rodata:
0000000000002049 db 0.rodata:
000000000000204A db 0 .rodata:
000000000000204A db 0.rodata:
000000000000204B db 0 .rodata:
000000000000204B db 0.rodata:
000000000000204C db 0 .rodata:
000000000000204C db 0.rodata:
000000000000204D db 0 .rodata:
000000000000204D db 0.rodata:
000000000000204E db 0 .rodata:
000000000000204E db 0.rodata:
000000000000204F db 0 .rodata:
000000000000204F db 0.rodata:
0000000000002050 ; const char format[].rodata:
0000000000002050 format db 'Enter your guess (exactly %zu bytes): ',0 .rodata:
0000000000002050 format db 'Enter your guess (exactly %zu bytes): ',0.rodata:
0000000000002050

#include<stdio.h>#include<stdlib.h>#include<string.h>#include<ctype.h>// 密文數據unsignedcharcipher[] = {0x1F,0xC9,0xED,0x29,0xA6,0xFE,0x44,0xEE,0x82,0x45,0xE9,0xD8,0x7F,0x42,0x10,0xE0,0xBB,0x4B,0xD0,0x05,0x4C,0x76,0x90,0xCB,0x48,0x9C,0x7A,0xA9,0xF0,0x33,0x55,0x25,0x64,0x88,0x3D,0xF7};intmain(){printf("[*] Environment Check (Ubuntu 22.04):n");srand(0);printf(" Seed 0, First rand() = %d (Expected: 1804289383)n",rand());printf("--------------------------------------------------n");for(intseed =0; seed <20; seed++) { srand（seed）；// 重置種子 chardecrypted[37]; memset(decrypted,0,37); // 生成密鑰併解密 for(inti =0; i <36; i++) { intr =rand(); // 題目邏輯: key是rand（）的低8位 decrypted[i] = cipher[i] ^ (r &0xFF); } // 打印結果 printf("Seed %02d: ", seed); // 打印字符串部分（過濾不可見字符以便觀察） for(inti=0; i<36; i++) { if(isprint(decrypted[i])) { printf("%c", decrypted[i]); }else{ printf（“.”）；// 不可見字符顯示爲點 } } printf("n"); // 打印 HEX（如果字符串看不清，看 HEX 頭） // printf(" HEX: %02X %02X %02X ...n", (unsigned char)decrypted[0], (unsigned char)decrypted[1], (unsigned char)decrypted[2]); }return0;}


```
importstruct
# 1. 嚴格從 Java 代碼中提取的 CK 數組（註意：與標準 SM4 不衕）CK = [ 462357,472066609,943670861,1415275113,1886879365, -1936483679, -1464879427, -993275175, -521670923, -66909679,404694573,876298825,1347903077,1819507329, -2003855715, -1532251463, -1060647211, -589042959, -117504499,337322537,808926789,1280531041,1752135293, -2071227751, -1599623499, -1128019247, -656414995, -184876535,269950501,741554753,1213159005,1684763257]# 將 Java 的有符號 int 轉換爲 Python 的無符號 32位 intCK = [x &0xFFFFFFFFforxinCK]# 2. 從 Java 代碼提取的 FK 數組FK = [-1548633402,1453994832,1736282519, -1301273892]FK = [x &0xFFFFFFFFforxinFK]# 3. 從 Java 代碼提取的 SBOX（有符號 byte 轉無符號）SBOX_SIGNED = [ -42, -112, -23, -2, -52, -31,61, -73,22, -74,20, -62,40, -5,44,5,43,103, -102,118,42, -66,4, -61, -86,68,19,38,73, -122,6, -103, -100,66,80, -12, -111, -17, -104,122,51,84,11,67, -19, -49, -84,98, -28, -77,28, -87, -55,8, -24, -107, -128, -33, -108, -6,117, -113,63, -90,71,7, -89, -4, -13,115,23, -70, -125,89,60,25, -26, -123,79, -88,104,107, -127, -78,113,100, -38, -117, -8, -21,15,75,112,86, -99,53,30,36,14,94,99,88, -47, -94,37,34,124,59,1,33,120, -121, -44,0,70,87, -97, -45,39,82,76,54,2, -25, -96, -60, -56, -98, -22, -65, -118, -46,64, -57,56, -75, -93, -9, -14, -50, -7,97,21, -95, -32, -82,93, -92, -101,52,26,85, -83, -109,50,48, -11, -116, -79, -29,29, -10, -30,46, -126,102, -54,96, -64,41,35, -85,13,83,78,111, -43, -37,55,69, -34, -3, -114,47,3, -1,106,114,109,108,91,81, -115,27, -81, -110, -69, -35, -68,127,17, -39,92,65,31,16,90, -40,10, -63,49, -120, -91, -51,123, -67,45,116, -48,18, -72, -27, -76, -80, -119,105, -105,74,12, -106,119,126,101, -71, -15,9, -59,110, -58, -124,24, -16,125, -20,58, -36,77,32,121, -18,95,62, -41, -53,57,72]SBOX = [x &0xFFforxinSBOX_SIGNED]# ================= 覈心邏輯 =================defrotl(i, n):“”“32位循環左移”“”return((i << n) | (i >> (32- n))) &0xFFFFFFFFdefrotl8(i, n):“”“8位循環左移”“”return((i << n) | (i >> (8- n))) &0xFF
# 生成 SBOX_P（複現 Java static 塊）SBOX_P = [0] *256foriinrange(256):
val = SBOX[(i ^167) &255]SBOX_P[i] = rotl8(val, i &3)defsbox_transform(i):
returnSBOX_P[(i ^60) &0xFF]deftau(i):b0 = sbox_transform((i >>24) &0xFF)b1 = sbox_transform((i >>16) &0xFF)b2 = sbox_transform((i >>8) &0xFF)b3 = sbox_transform(i &0xFF)return(b0 <<24) | (b1 <<16) | (b2 <<8) | b3defT(i):t = tau(i)returnt ^ rotl(t,2) ^ rotl(t,10) ^ rotl(t,18) ^ rotl(t,24)defT_prime(i):t = tau(i)returnt ^ rotl(t,13) ^ rotl(t,23)defderive_key(seed_str):
seed_bytes = seed_str.encode('utf-8')key =bytearray(16)foriinrange(16): val = (seed_bytes[i %len(seed_bytes)] + (i *17) +35) &0xFF key[i] = valreturnbytes(key)defexpand_key(key_bytes):mk =list(struct.unpack('>4I', key_bytes))k = [0] *36k[0:4] = [mk[i] ^ FK[i]foriinrange(4)]rk = []foriinrange(32): temp = k[i+1] ^ k[i+2] ^ k[i+3] ^ CK[i] rk_val = k[i] ^ T_prime(temp) rk.append(rk_val) k[i+4] = rk_valreturnrkdefsm4_decrypt_block(block_bytes, rk_list):# SM4解密：輸入密文，使用逆序的輪密鑰X =list(struct.unpack('>4I', block_bytes))
# 輪密鑰必鬚是逆序的（rk31...rk0）rk_inv = rk_list[::-1]foriinrange(32): temp = X[1] ^ X[2] ^ X[3] ^ rk_inv[i] result = X[0] ^ T(temp) X = [X[1], X[2], X[3], result]# 解密後需要反序輸齣（X35，X34，X33，X32）-> Bytesreturnstruct.pack('>4I', X[3], X[2], X[1], X[0])
# ================= 執行解密 =================TARGET_CIPHER_HEX ="21c2692a4775c413356a31fc55c38f6218bed9d46c45bd0eb777be9334c999d7"KEY_SEED ="happ"# 1. 準備數據target_bytes =bytes.fromhex(TARGET_CIPHER_HEX)key = derive_key(KEY_SEED)
# 2. 生成輪密鑰rk = expand_key(key)
# 3. 解密plaintext =b""foriinrange(0,len(target_bytes),16):
block = target_bytes[i:i+16]plaintext += sm4_decrypt_block(block, rk)
# 4. 去除填充（PKCS7）try:
pad_len = plaintext[-1]# 簡單的填充檢查if0< pad_len <=16: plaintext = plaintext[:-pad_len]print(f"Flag:{plaintext.decode('utf-8')}")exceptExceptionase:
print(f"Decryption raw bytes:{plaintext}")print(f"Error:{e}")
importstruct
# ================= 1. 數據提取與解析 =================# 從僞代碼中提取的原始字符串（格式化處理）# xx 代錶十六進製，普通字符代錶 ASCIIraw_data_str = (r"8080XKc616^9095b56aa^Tfe9aabcd179^82f1Jcb7,90d5 87f"r"e69&-!a8159fj[=qa48df1,90d893'a0 31daaf78ef8f5c6fe("r"9aeda7c9|lead96nffbfab+82kO^9dy99Bcc_c0]Hdab8b1}e8/S"r"d9v@A4 0fa 8a8ce9sb9ude 98bZb7za6eb 1091e4c1016 295"r"8ab5f0a11917idf1fa3X% afc5f2 bf91ad5c8c7bafe6ec80"r"{Ja5a98897VIb6 5cd1eM9efd$g> 7C):
db1586xpcad21cb4e2"r"N84 4Q81bah`P135c~ 69889f68cbcfbe#bd92m7d78f14f36 c"r"aeb0? f4Re0227ftFfcee9cb287.E11e7d1d0*def<12YacT;o d"r"e3dc9bGc4bba2c2K383d4cec1Dddb394 fr85d6fbd3We5bc18"r"21bc3wUea ee1L96<d1s/acfec2 0Ve1&49ae1/b5Oa386fb87f8"r"91 a9b 0fb f8d$w")
# 解析器：將 xx 解析爲字節，其他字符保持不變data_bytes =bytearray()i =0whilei <len(raw_data_str):
ifraw_data_str[i] =='\': # 讀取後兩位作爲 hex hex_val = raw_data_str[i+1:i+3] data_bytes.append(int(hex_val,16)) i +=3else: data_bytes.append(ord(raw_data_str[i])) i +=1
# 提取關鍵區段
# Offset 0-31: 密鑰種子KEY_SEED = data_bytes[0:32]# Offset 32-288: S-Box (256 bytes)SBOX =list(data_bytes[32:
288])
# Offset 288-320: 密文（32 bytes）CIPHERTEXT = data_bytes[288:
320]# 生成逆 S-BoxINV_SBOX = [0] *256fori, vinenumerate(SBOX):
INV_SBOX[v] = i
# ================= 2. 覈心算法複現 =================# 輔助函數: f_cdeff_c(a, b, c):# return c * -23 + (a ^ b) & 255res = (c * -23+ (a ^ b)) &0xFFreturnres
# 1. 生成初始 16 字節密鑰defgenerate_initial_key(seed):
key = [0] *16fordinrange(16): # 對應僞代碼中的 Loop L_b 和 L_d # (d + i)[0] = f_c((d + 1024)[0], (d + 1040)[0], d & 255) # 1024是數據開頭，1040是數據+16 val_a = seed[d] val_b = seed[d +16] key[d] = f_c(val_a, val_b, d)returnkey
# 2. 密鑰擴展（Key Schedule）defkey_expansion(initial_key):# 存儲所有輪密鑰（11組，每組16字節）round_keys = []round_keys.append(list(initial_key))
# Round 0 Keycurrent_key =list(initial_key)
# 對應 Loop L_n -> L_q
# f 從 1 到 10forfinrange(1,11): prev_key =list(current_key) new_key = [0] *16 e = f *17 # 對應 Loop L_r # (d + g + a)[0]:
byte = (e ^ (a + c)[0]:
ubyte) ^ a; # c 是上一輪密鑰的地址，g 是當前輪密鑰地址 forainrange(16): new_key[a] = (e ^ prev_key[a]) ^ a round_keys.append(new_key) current_key = new_keyreturnround_keys
# 3. AES 逆列混淆（Inverse MixColumns）# 使用標準的 AES 逆矩陣乘法defgmul(a, b):p =0for_inrange(8): ifb &1: p ^= a hi_bit_set = a &0x80 a <<=1 ifhi_bit_set: a ^=0x1B b >>=1returnp &0xFFdefinv_mix_columns(state):# state: list of 16 bytesnew_state = [0] *16forcinrange(4): col = state[c*4: c*4+4] # InvMixColumns Matrix: # 14 11 13 9 # 9 14 11 13 # 13 9 14 11 # 11 13 9 14 new_state[c*4+0] = gmul(col[0],14) ^ gmul(col[1],11) ^ gmul(col[2],13) ^ gmul(col[3],9) new_state[c*4+1] = gmul(col[0],9) ^ gmul(col[1],14) ^ gmul(col[2],11) ^ gmul(col[3],13) new_state[c*4+2] = gmul(col[0],13) ^ gmul(col[1],9) ^ gmul(col[2],14) ^ gmul(col[3],11) new_state[c*4+3] = gmul(col[0],11) ^ gmul(col[1],13) ^ gmul(col[2],9) ^ gmul(col[3],14)returnnew_state
# 4. 解密單個 Blockdefdecrypt_block(ciphertext_block, round_keys):
state =list(ciphertext_block)
# Initial AddRoundKey (Round 10)rk = round_keys[10]state = [b ^ kforb, kinzip(state, rk)]# Rounds 9 down to 1forrinrange(9,0, -1): # InvShiftRows # Row 1: shift right 1 (inv of left 1) state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9] # Row 2: shift right 2 state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6] # Row 3: shift right 3 state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3] # InvSubBytes state = [INV_SBOX[b]forbinstate] # AddRoundKey rk = round_keys[r] state = [b ^ kforb, kinzip(state, rk)] # InvMixColumns state = inv_mix_columns(state)
# Round 0 (Final)
# InvShiftRowsstate[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]# InvSubBytesstate = [INV_SBOX[b]forbinstate]# AddRoundKey (Round 0)rk = round_keys[0]state = [b ^ kforb, kinzip(state, rk)]returnbytes(state)
# ================= 3. 執行 =================# 計算密鑰initial_key = generate_initial_key(KEY_SEED)print(f"Initial Key:{bytes(initial_key).hex()}")
# 擴展密鑰round_keys = key_expansion(initial_key)
# 解密（處理兩個 block）flag_bytes =b""foriinrange(0,32,16):
block = CIPHERTEXT[i : i+16]decrypted = decrypt_block(block, round_keys)flag_bytes += decryptedprint(f"Decrypted:{flag_bytes}")
# 去除 padding（假設最後是 null 或者 pkcs7，直接轉 string 試試）try:
print(f"Flag:{flag_bytes.decode('utf-8').strip()}")
except:
print("Flag contains non-printable chars, check hex.")
importstructdefto_uint32(x):
returnx &0xFFFFFFFFdefdecrypt():# 1. 目標密文
# 來自:（v3 ^ 0x6421ACBE |（unsigned int）v4 ^ 0xFA7CB432）== 0v3 =0x6421ACBEv4 =0xFA7CB432 # 2. 真正的密鑰（從 IDA .rodata 穫取）# Hex: 0F 1E 2D 3C 4B 5A 69 78 87 96 A5 B4 C3 D2 E1 F0
# Little Endian 解析k = [0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3]# 3. Delta 和 Sum 配置DELTA =0x9E3779B9 # 關於 Sum 的初始值：# 加密循環是：# v6 = DELTA;# do { ...使用 v6...； v6 += DELTA； } while（...）運行 32 次
# 第 1 輪使用 DELTA * 1 # ...# 第 32 輪使用 DELTA * 32
# 所以解密時，我們要從第 32 輪的狀態開始，即 sum = DELTA * 32sum_val = to_uint32(DELTA *32)for_inrange(32): # 4. 逆曏 v4 # 索引計算:（sum >> 2）& 3 idx = (sum_val >>2) &3 # 加密邏輯迴顧: # term1 = ((v3 >> 5) ^ (v3 << 2)) + ((v3 >> 3) ^ (v3 << 4)) # term2 = (sum ^ v3) + (v3 ^ k[idx ^ 1]) # v4 += term1 ^ term2 # 解密邏輯: v4 -= term1 ^ term2 term1 = ((v3 >>5) ^ (v3 <<2)) + ((v3 >>3) ^ (v3 <<4)) term2 = (sum_val ^ v3) + (v3 ^ k[idx ^1]) v4 = to_uint32(v4 - (term1 ^ term2)) # 5. 逆曏 v3 # 加密邏輯迴顧: # term3 = ((v4 >> 5) ^ (v4 << 2)) + ((v4 >> 3) ^ (v4 << 4)) # term4 = (sum ^ v4) + (v4 ^ k[idx]) # v3 += term3 ^ term4 # 解密邏輯: v3 -= term3 ^ term4 term3 = ((v4 >>5) ^ (v4 <<2)) + ((v4 >>3) ^ (v4 <<4)) term4 = (sum_val ^ v4) + (v4 ^ k[idx]) v3 = to_uint32(v3 - (term3 ^ term4)) # 6. Sum 遞減 sum_val = to_uint32(sum_val - DELTA)returnstruct.pack("> (j*8)) &255; // little-endian
int__cdeclmain(intargc,constchar**argv,constchar**envp){unsignedintv3;// ebx__pid_tv4;// eaxvoid*v5;// rspvoid*v7;// rsp__int64 v8[7];// [rsp+8h] [rbp-4A0h] BYREFunsigned__int64 j;// [rsp+40h] [rbp-468h]size_tv10;// [rsp+48h] [rbp-460h]unsigned__int64 i;// [rsp+50h] [rbp-458h]__int64 v12;// [rsp+58h] [rbp-450h]__int64 *v13;// [rsp+60h] [rbp-448h]__int64 v14;// [rsp+68h] [rbp-440h]void*s1;// [rsp+70h] [rbp-438h]chars[1032];// [rsp+78h] [rbp-430h] BYREFunsigned__int64 v17;// [rsp+480h] [rbp-28h]v17 = __readfsqword(0x28u);v3 =time(0LL);v4 =getpid();srand((v4 ^ v3) %0x14);v12 =35LL;v8[4] =36LL;v8[5] =0LL;v8[2] =36LL;v8[3] =0LL;v5 =alloca(48LL);v13 = v8;for( i =0LL; i <0x24; ++i )*((_BYTE *)v13 + i) =rand();printf("Enter your guess (exactly %zu bytes): ",0x24uLL);if(fgets(s,1024, stdin) ){v10 =strlen(s);if( v10 && s[v10 -1] ==10) s[--v10] =0;if( v10 ==36) { v14 =35LL; v8[0] =36LL; v8[1] =0LL; v7 =alloca(48LL); s1 = v8; for( j =0LL; j <0x24; ++j ) *((_BYTE *)s1 + j) = *((_BYTE *)v13 + j) ^ s[j]; if( !memcmp(s1, &cipher,0x24uLL) ) puts("Correct! Your input is the plaintext."); else puts("Incorrect."); return0; }else { printf("Wrong length: expected %zu, got %zun",0x24uLL, v10); return1; }}else{fwrite("No inputn",1uLL,9uLL, stderr);return1;}}
db 1Fh ; DATA XREF: main+386↑o cipher db 1Fh ; DATA XREF: main+386↑o cipher db 1Fh ; DATA XREF: main+386↑o.rodata:
0000000000002021 db 0C9h .rodata:
0000000000002021 db 0C9h.rodata:
0000000000002022 db 0EDh .rodata:
0000000000002022 db 0EDh.rodata:
0000000000002023 db 29h ; ) .rodata:
0000000000002023 db 29h ; ).rodata:
0000000000002024 db 0A6h .rodata:
0000000000002024 db 0A6h.rodata:
0000000000002025 db 0FEh .rodata:
0000000000002025 db 0FEh.rodata:
0000000000002026 db 44h ; D .rodata:
0000000000002026 db 44h ; D.rodata:
0000000000002027 db 0EEh .rodata:
0000000000002027 db 0EEh.rodata:
0000000000002028 db 82h .rodata:
0000000000002028 db 82h.rodata:
0000000000002029 db 45h ; E .rodata:
0000000000002029 db 45h ; E.rodata:
000000000000202A db 0E9h .rodata:
000000000000202A db 0E9h.rodata:
000000000000202B db 0D8h .rodata:
000000000000202B db 0D8h.rodata:
000000000000202C db 7Fh ; .rodata:
000000000000202C db 7Fh ;.rodata:
000000000000202D db 42h ; B .rodata:
000000000000202D db 42h ; B.rodata:
000000000000202E db 10h .rodata:
000000000000202E db 10h.rodata:
000000000000202F db 0E0h .rodata:
000000000000202F db 0E0h.rodata:
0000000000002030 db 0BBh .rodata:
0000000000002030 db 0BBh.rodata:
0000000000002031 db 4Bh ; K .rodata:
0000000000002031 db 4Bh ; K.rodata:
0000000000002032 db 0D0h .rodata:
0000000000002032 db 0D0h.rodata:
0000000000002033 db 5 .rodata:
0000000000002033 db 5.rodata:
0000000000002034 db 4Ch ; L .rodata:
0000000000002034 db 4Ch ; L.rodata:
0000000000002035 db 76h ; v .rodata:
0000000000002035 db 76h ; v.rodata:
0000000000002036 db 90h .rodata:
0000000000002036 db 90h.rodata:
0000000000002037 db 0CBh .rodata:
0000000000002037 db 0CBh.rodata:
0000000000002038 db 48h ; H .rodata:
0000000000002038 db 48h ; H.rodata:
0000000000002039 db 9Ch .rodata:
0000000000002039 db 9Ch.rodata:
000000000000203A db 7Ah ; z .rodata:
000000000000203A db 7Ah ; z.rodata:
000000000000203B db 0A9h .rodata:
000000000000203B db 0A9h.rodata:
000000000000203C db 0F0h .rodata:
000000000000203C db 0F0h.rodata:
000000000000203D db 33h ; 3 .rodata:
000000000000203D db 33h ; 3.rodata:
000000000000203E db 55h ; U .rodata:
000000000000203E db 55h ; U.rodata:
000000000000203F db 25h ; % .rodata:
000000000000203F db 25h ; %.rodata:
0000000000002040 db 64h ; d .rodata:
0000000000002040 db 64h ; d.rodata:
0000000000002041 db 88h .rodata:
0000000000002041 db 88h.rodata:
0000000000002042 db 3Dh ; = .rodata:
0000000000002042 db 3Dh ; =.rodata:
0000000000002043 db 0F7h .rodata:
0000000000002043 db 0F7h.rodata:
0000000000002044 db 0 .rodata:
0000000000002044 db 0.rodata:
0000000000002045 db 0 .rodata:
0000000000002045 db 0.rodata:
0000000000002046 db 0 .rodata:
0000000000002046 db 0.rodata:
0000000000002047 db 0 .rodata:
0000000000002047 db 0.rodata:
0000000000002048 cipher_len db 24h ; $.rodata:
0000000000002049 db 0 .rodata:
0000000000002049 db 0.rodata:
000000000000204A db 0 .rodata:
000000000000204A db 0.rodata:
000000000000204B db 0 .rodata:
000000000000204B db 0.rodata:
000000000000204C db 0 .rodata:
000000000000204C db 0.rodata:
000000000000204D db 0 .rodata:
000000000000204D db 0.rodata:
000000000000204E db 0 .rodata:
000000000000204E db 0.rodata:
000000000000204F db 0 .rodata:
000000000000204F db 0.rodata:
0000000000002050 ; const char format[].rodata:
0000000000002050 format db 'Enter your guess (exactly %zu bytes): ',0 .rodata:
0000000000002050 format db 'Enter your guess (exactly %zu bytes): ',0.rodata:
0000000000002050
    #include<stdio.h>#include<stdlib.h>#include<string.h>#include<ctype.h>// 密文數據unsignedcharcipher[] = {0x1F,0xC9,0xED,0x29,0xA6,0xFE,0x44,0xEE,0x82,0x45,0xE9,0xD8,0x7F,0x42,0x10,0xE0,0xBB,0x4B,0xD0,0x05,0x4C,0x76,0x90,0xCB,0x48,0x9C,0x7A,0xA9,0xF0,0x33,0x55,0x25,0x64,0x88,0x3D,0xF7};intmain(){printf("[*] Environment Check (Ubuntu 22.04):n");srand(0);printf(" Seed 0, First rand() = %d (Expected: 1804289383)n",rand());printf("--------------------------------------------------n");for(intseed =0; seed <20; seed++) { srand（seed）；// 重置種子 chardecrypted[37]; memset(decrypted,0,37); // 生成密鑰併解密 for(inti =0; i <36; i++) { intr =rand(); // 題目邏輯: key是rand（）的低8位 decrypted[i] = cipher[i] ^ (r &0xFF); } // 打印結果 printf("Seed %02d: ", seed); // 打印字符串部分（過濾不可見字符以便觀察） for(inti=0; i<36; i++) { if(isprint(decrypted[i])) { printf("%c", decrypted[i]); }else{ printf（“.”）；// 不可見字符顯示爲點 } } printf("n"); // 打印 HEX（如果字符串看不清，看 HEX 頭） // printf(" HEX: %02X %02X %02X ...n", (unsigned char)decrypted[0], (unsigned char)decrypted[1], (unsigned char)decrypted[2]); }return0;}
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