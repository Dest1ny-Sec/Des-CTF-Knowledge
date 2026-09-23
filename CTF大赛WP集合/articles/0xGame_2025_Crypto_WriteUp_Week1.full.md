---
title: 0xGame 2025/Crypto WriteUp Week1
contest: 0xGame
year: 2025
difficulty: easy
vuln_type:
- crypto_rsa
- diffie_hellman
- block_cipher
- vigenere
- web_qrcode
tags:
- 新人向
- factordb
- Vigenère 标准
- Vigenère 魔改乘法
- GB2312
- 三进制 base
- iroot(7) 整数根
- POW 爆破
- DH s=1 退化
attack_chain:
- 子题 1 流量登录：扫 QR 码填 6 位验证码
- 子题 2 DH 退化：设 Bob 公钥 B=1 → s=pow(1,a,p)=1 → 直接用 s=1 派生 AES key
- 子题 3 RSA factordb：n 256-bit 太小，直接 factordb 分解 p,q
- 子题 4 Vigenère 标准：已知 key "Welcome-2025-0xGame"，解密
- 子题 5 Vigenère 魔改乘法：((char_index + bias) * char_index) mod len → 逐位解二次同余
- 子题 6 flag 切 4 段：b64 + hex + 三进制 a/w/q + iroot(7) → 拼回 flag (gb2312)
- 子题 7 POW + 2025 位 RSA：4 字符前缀爆破 + d=inverse(e, n-1)
key_payload: ''
one_liner: 7 个新人向 crypto 子题合集（DH s=1 / factordb / Vigenère 两种 / GB2312 三进制 iroot / POW + 2025 位 RSA）
lesson: DH 协议 s 值退化时（公钥=1）直接 s=1；factordb 是小指数 RSA 标准武器；Vigenère 乘法变种需逐位解二次同余；多段编码拼接时按段确认长度和编码
quality: high
full_path: 0xGame_2025_Crypto_WriteUp_Week1.full.md
meta_path: 0xGame_2025_Crypto_WriteUp_Week1.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 0xGame 2025/Crypto WriteUp Week1。7 个新人向 crypto 子题合集（DH s=1 / factordb / Vigenère 两种 / GB2312 三进制 iroot / POW + 2025 位 RSA）。关键路径：子题 1 流量登录：扫 QR 码填 6 位验证码 → 子题 2 DH 退化：设 Bob 公钥 B=1 → s=pow(1,a,p)=1 →...
category: crypto
subcategory: rsa
subcategories:
- rsa
- symmetric
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/273923.html
reasoning_chain:
- 触发点：7 个新人向 crypto 子题合集，难度 1-3 星 → 假设：每题都是经典弱点的演示
- Q1 trigger：pwntools 流量登录 + QR 码 + 6 位验证码 → 动作：题面已经把 QR 数据 print 出来 → 观察：手动输入验证码登录成功
- Q2 DH trigger：Alice 给 p, g, A，等 Bob 公钥 → 假设：B=1 退化 → s=pow(1,a,p)=1
- 动作：sendline(b'1') → 观察：enc = AES-ECB(sha256(long_to_bytes(1))) → 解密得 flag
- Q3 RSA trigger：n 512-bit（其实只是 256-bit 素数之积）→ 假设：太小 → 动作：factordb.com 或 yafu → 观察：秒出 p, q
- Q4 Vigenere trigger：key='Welcome-2025-0xGame' 明文出现在源码 → 动作：直接 vigenere_decrypt → 观察：flag
- Q5 Vigenere 魔改 trigger：((char_idx+bias)*char_idx) % len = new_index → 假设：每个密文字符解二次同余
- 动作：对每个密文字符遍历 94 个 char_idx → 观察：唯一解集合 → itertools.product 拼回 → flag='excellent'
- Q6 trigger：4 段编码 b64 + hex + 三进制 a/w/q + iroot(7) → 假设：分段分别解码，gb2312 编码
- 动作：b64decode + bytes.fromhex + awaqaq 倒推 + gmpy2.iroot(c4,7) → 观察：gb2312 拼出中文 flag
- Q7 trigger：30s POW + 2025-bit n（n 是 getPrime 单素数）→ 动作：multiprocess sha256 爆 4 字符前缀 → inverse(e, n-1)
failed_attempts:
- Q2 用正常 DH 计算 s → 失败：未发现 B=1 退化是合法输入
- Q3 试 Pollard rho 本地分解 → 失败：太慢，factordb 一秒出
- Q5 暴力破解 94^14 全部字符 → 失败：单个字符解二次同余更高效
- Q6 直接拼接不解 gb2312 → 失败：raw bytes 是乱码，gb2312 编码才能读出中文
- Q7 误以为 n 是 p*q → 失败：inverse(e, (p-1)(q-1)) 解不出，n 是单素数 n-1 就是 phi
key_observations:
- DH协议 B=1 是经典退化攻击：pow(1,a,p)=1，与 a 无关
- RSA n< 600 bit 几乎都能被 factordb 秒分解
- Vigenere 二次变种 new_index = (c+b)*c mod len → 解二次同余 + 字符集约束（'0xGame{' 前缀已知）
- 多段编码题按段确认长度和编码类型，gb2312 这种罕见编码要最后再 decode
- n = getPrime(2025) 单素数时 phi(n)=n-1，inverse(e, n-1) 直接解，无需因式分解
prerequisites:
- pwntools remote/sendlineafter 交互
- Crypto.Util.number（long_to_bytes/inverse）
- factordb.com / yafu 大数分解
- gmpy2.iroot 整数 k 次根
- base64 / hex / 三进制编码互转 + gb2312 解码
---
# 0xGame 2025 Crypto WriteUp Week1

> 原文: https://www.ctfiot.com/273923.html
> ID: 273923

忽然想起好久没有更新了，趁各大学校网安社团招新之际，写点新人向的writeup。需要pdf版可以在后台私信我。

使用yafu工具分解：https://wiki.mrskye.cn/Crypto/yafu%E5%AE%89%E8%A3%85%E5%8F%8A%E4%BD%BF%E7%94%A8/

使用factordb在线网站分解：https://factordb.com/

给定一个字典mapper，0,1,2分别对应a,w,q

将num模3后，寻找mapper里面数字对应的字母，并且给密文加上这个字母

对num进行整除3处理，并且将值赋值给新的num

循环到时停止


```
frompwnimport*# 连接服务器io = remote("nc1.ctfplus.cn",39427)
# 注册用户io.sendlineafter(b"Choice: ",b"R")io.sendlineafter(b"Username: ",b"admin")
# 获取QR码数据print("=== QR Code Data ===")qr_data = io.recvuntil(b"Choice: ").decode()print(qr_data)print("====================")
# 开始登录io.sendline(b"L")
# 等待验证码输入提示io.recvuntil(b"Verification Code: ")print("请扫描QR码并输入6位验证码:")
# 手动输入验证码verification_code = input().strip()io.sendline(verification_code.encode())
# 检查登录结果result = io.recvline().decode()print(f"登录结果:{result}")
# 获取flagio.sendlineafter(b"Choice: ",b"G")flag = io.recvline().decode().strip()print(f"Flag:{flag}")io.close()
0xGame{5368d6e9-8512-4afe-819f-e22093588509}
fromCrypto.Util.numberimport*fromsecretimportflagfromhashlibimportsha256fromCrypto.CipherimportAESfromCrypto.Util.Paddingimportpadp = getPrime(512)print(f"The Prime is{p}")g = getRandomRange(2, p)print(f"The Generator is{g}")a = getRandomRange(2, p)A = pow(g, a, p)print(f"Alice's Public Key is{A}")B = int(input("Bob's Public Key: "))assertB != As = pow(B, a, p)key = sha256(long_to_bytes(s)).digest()cipher = AES.new(key, AES.MODE_ECB)enc = cipher.encrypt(pad(flag,16))print(f"Encrypted Flag:{enc.hex()}")
frompwnimport*fromCrypto.Util.numberimport*fromhashlibimportsha256fromCrypto.CipherimportAESfromCrypto.Util.Paddingimportunpaddefmy_recvline(split_str): back = io.recvline().decode().strip("n").split(split_str)[-1] returnbackio = remote("nc1.ctfplus.cn",15831)p = int(my_recvline("is "))g = int(my_recvline("is "))A = int(my_recvline("is "))B =1io.sendlineafter(b"Key: ",str(B).encode())ciphertext = bytes.fromhex(my_recvline("Flag: "))io.close()s =1key = sha256(long_to_bytes(s)).digest()cipher = AES.new(key, AES.MODE_ECB)flag = unpad(cipher.decrypt(ciphertext),16)print(flag)
b'0xGame{690e5ecb-faec-424c-8871-0ea9d02ebe46}'
fromCrypto.Util.numberimport*fromsecretimportflagp, q = [getPrime(256)for_inrange(2)]n = p * qe =65537m = bytes_to_long(flag)c = pow(m, e, n)print(f"n ={n}")print(f"c ={c}")
# n = 5288062996177288067805240670327919739339874127477405321607402348589147491552053048231920112750216696782518281218048178087877077018108705271341382858124037
# c = 2454797328903978848197140611862882439826920912955785083080835692389929572917351093371626343669582289242212514789420568997224614087740388703381025018563979
fromCrypto.Util.numberimport*n =5288062996177288067805240670327919739339874127477405321607402348589147491552053048231920112750216696782518281218048178087877077018108705271341382858124037c =2454797328903978848197140611862882439826920912955785083080835692389929572917351093371626343669582289242212514789420568997224614087740388703381025018563979p =60979507724530093051797511853954365018147917052474373616663462193464369184711q =86718689499194998339746379891242621495538434539975542252458947218776577824467e =65537d = inverse(e,(p -1)*(q -1))m = pow(c,d,n)flag = long_to_bytes(m)print(flag)
b'0xGame{F4ct0rDB_1s_usefu1_r19ht?}'
fromstringimportdigits, ascii_letters, punctuationfromsecretimportflagkey ="Welcome-2025-0xGame"alphabet = digits + ascii_letters + punctuationdefvigenere_encrypt(plaintext, key): ciphertext ="" key_index =0 forcharinplaintext: bias = alphabet.index(key[key_index]) char_index = alphabet.index(char) new_index = (char_index + bias) % len(alphabet) ciphertext += alphabet[new_index] key_index = (key_index +1) % len(key) returnciphertextprint(vigenere_encrypt(flag, key))
# WL"mKAaequ{q_aY$oz8`wBqLAF_{cku|eYAczt!pmoqAh+
new_index = (char_index + bias) % len(alphabet)
char_index = (new_index - bias) % len(alphabet)
fromstringimportdigits, ascii_letters, punctuationkey ="Welcome-2025-0xGame"alphabet = digits + ascii_letters + punctuationdefvigenere_decrypt(ciphertext, key): plaintext ="" key_index =0 forcharinciphertext: bias = alphabet.index(key[key_index]) new_index = alphabet.index(char) char_index = (new_index - bias) % len(alphabet) plaintext += alphabet[char_index] key_index = (key_index +1) % len(key) returnplaintextciphetext ='WL"mKAaequ{q_aY$oz8`wBqLAF_{cku|eYAczt!pmoqAh+'flag = vigenere_decrypt(ciphetext,key)print(flag)
0xGame{you_learned_vigenere_cipher_2df4b1c2e3}
fromstringimportdigits, ascii_letters, punctuation, ascii_lowercasefromsecretimportflagassertflag.startswith("0xGame{")andflag.endswith("}")assertset(flag[7:-1]) < set(ascii_lowercase)key ="QAQ(@.@)"alphabet = digits + ascii_letters + punctuationdefvigenere_encrypt(plaintext, key): ciphertext ="" key_index =0 foriinplaintext: bias = alphabet.index(key[key_index]) char_index = alphabet.index(i) new_index = ((char_index + bias) * char_index) % len(alphabet) ciphertext += alphabet[new_index] key_index = (key_index +1) % len(key) returnciphertextprint(vigenere_encrypt(flag, key))
# 0l0CSoYM<c;amo_P_
new_index = ((char_index + bias) * char_index) % len(alphabet)
assertflag.startswith("0xGame{")andflag.endswith("}")assertset(flag[7:-1]) < set(ascii_lowercase)
fromstringimportdigits, ascii_letters, punctuationimportitertoolskey ="QAQ(@.@)"alphabet = digits + ascii_letters + punctuationdefvigenere_decrypt_all_possibilities(ciphertext, key, flag_head): possibilities = [] # 每个位置可能的字符列表 key_index =0 cnt =0 forcharinciphertext: bias = alphabet.index(key[key_index]) new_index = alphabet.index(char) possible_chars = [] forchar_indexinrange(len(alphabet)): ifcnt <=6: # 对于 cnt <= 7 的情况，直接取原字符 possible_chars.append(flag_head[cnt]) break if((char_index + bias) * char_index) % len(alphabet) == new_index: ifalphabet[char_index]inascii_lettersandalphabet[char_index].islower(): possible_chars.append(alphabet[char_index]) ifnotpossible_chars: possible_chars.append('}') # 用}标记未找到，其实也就是收尾工作 possibilities.append(possible_chars) cnt +=1 key_index = (key_index +1) % len(key) returnpossibilitiesciphetext ="0l0CSoYM<c;amo_P_"flag_head ="0xGame{"possibilities = vigenere_decrypt_all_possibilities(ciphetext, key, flag_head)
# 生成所有可能的组合forcandidateinitertools.product(*possibilities): plain =''.join(candidate) flag = plain print(flag)'''0xGame{axcellent}0xGame{axcellezt}0xGame{axcsllent}0xGame{axcsllezt}0xGame{excellent}0xGame{excellezt}0xGame{excsllent}0xGame{excsllezt}'''
0xGame{excellent}
fromCrypto.Util.numberimport*frombase64importb64encodefromosimporturandomflag = open('flag.txt').read().strip().encode('gb2312')flag += urandom(100- len(flag))defawaqaq(bt:
bytes): mapper = {0:'a',1:'w',2:'q'} out ='' num = int.from_bytes(bt) whilenum >0: out += mapper[num %3] num //=3 returnoutif__name__=='__main__': flags = [flag[i*len(flag)//4:(i+1)*len(flag)//4]foriinrange(4)] ciphertexts = [] c0 = b64encode(flags[0]) c1 = flags[1].hex() c2 = awaqaq(flags[2]) c3 = int.from_bytes(flags[3],'little') **7 print(c0) print(c1) print(c2) print(c3)'''b'MHhHYW1le7u2063AtLW9MHhHYW1lMjAyNQ=='a3accfd6d4dac4e3d2d1beadd1a7bbe143727970746fb5c4bbwqwwwqqaawwwaaqawqwawwwwaaawwwawaqqwwwqaqwwqwaaqwaqqaaawqqqaqaqwaaawwwqaqaaaaqawaqqqwwqqwaqwqwwwawawqqwwqqawqwaqwwawwqwaqqaqwaw5787980659359196741038715872684190805073807486263453249083702093905274294594502252203577660251756609738877887210677202141957646934092054500618364441642896304387589669635034683021946777034215355675802286923927161922717560413551789421376288823912349463080999424773600185557948875343480056576969695671340947861706467351885610345887785319870159654836532664189086047061137903149197973327299859185905186913896041309284477616128'''
frombase64importb64decodeimportgmpy2defawaqaq(out:
str): mapper = {'a':0,'w':1,'q':2} num =0 forchinout[::-1]: num = num *3+ mapper[ch] returnnum.to_bytes(25,'big')c0 =b'MHhHYW1le7u2063AtLW9MHhHYW1lMjAyNQ=='c1 ='a3accfd6d4dac4e3d2d1beadd1a7bbe143727970746fb5c4bb'c2 ='wqwwwqqaawwwaaqawqwawwwwaaawwwawaqqwwwqaqwwqwaaqwaqqaaawqqqaqaqwaaawwwqaqaaaaqawaqqqwwqqwaqwqwwwawawqqwwqqawqwaqwwawwqwaqqaqwaw'c4 =5787980659359196741038715872684190805073807486263453249083702093905274294594502252203577660251756609738877887210677202141957646934092054500618364441642896304387589669635034683021946777034215355675802286923927161922717560413551789421376288823912349463080999424773600185557948875343480056576969695671340947861706467351885610345887785319870159654836532664189086047061137903149197973327299859185905186913896041309284477616128flag0 = b64decode(c0).decode("gb2312", errors='ignore')#使用ignore能忽略解密时的错误flag1 = bytes.fromhex(c1).decode('gb2312', errors='ignore')flag2 = awaqaq(c2).decode('gb2312', errors='ignore')flag3 = int(gmpy2.iroot(c4,7)[0]).to_bytes(25,'little').decode('gb2312', errors='ignore')flag = flag0 + flag1 + flag2 + flag3print(flag)
0xGame{欢迎来到0xGame2025，现在你已经学会Crypto的本知识了，快来试试更难的挑战吧！}
fromCrypto.Util.numberimport*fromhashlibimportsha256fromosimporturandom,environimportrandomimportstringimportsignalflag = environ['FLAG']defproof_of_work()-> bool: s =''.join(random.choice(string.ascii_letters+string.digits)for_inrange(32)) print(f'[+] sha256(XXXX+{s[4:]}) =={sha256(s.encode()).hexdigest()}') ifinput(f'[-] Give me XXXX:') == s[:4]: returnTrue else: returnFalseif__name__=='__main__': signal.alarm(30) ifnotproof_of_work(): print(f'[!] Wrong!') exit() n = getPrime(2025) e =65537 m = int.from_bytes(flag.encode() + urandom(253- len(flag))) c = pow(m,e,n).to_bytes(254,'little').hex() print(f'[+] Here's today's encrypted flag:') print(f'[+] n ={n}') print(f'[+] e ={e}') print(f'[+] c ={c}')
s =''.join(random.choice(string.ascii_letters+string.digits)for_inrange(32))
importstringimportitertoolsfrompwnimport*fromhashlibimportsha256frommultiprocessingimportPoolfromCrypto.Util.numberimport*defpow_worker(args): prefix, target, combinations = args forcombincombinations: x =''.join(comb) ifsha256((x + prefix).encode()).hexdigest() == target: returnx returnNonedefsolve_pow_local(prefix, target, processes): ''' :
param prefix: 已知的token字符串 :
param target: token的哈希值 :
param processes: 你想要的进程数量，尽量只占用你电脑cpu数量的一半 :
return: ''' table = string.ascii_letters + string.digits print(f"Starting POW solving with{processes}processes...") # 生成所有组合并分块 all_combinations = itertools.product(table, repeat=4) chunk_size =1000 chunks = [] current_chunk = [] forcombinall_combinations: current_chunk.append(comb) iflen(current_chunk) >= chunk_size: chunks.append((prefix, target, current_chunk)) current_chunk = [] ifcurrent_chunk: chunks.append((prefix, target, current_chunk)) print(f"Created{len(chunks)}chunks for processing") # 多进程计算 withPool(processes=processes)aspool: forresultinpool.imap_unordered(pow_worker, chunks): ifresult: pool.terminate() returnresult returnNoneif__name__ =='__main__': io = remote("nc1.ctfplus.cn",45273) # 处理数据 challenge_line = io.recvline().decode().strip() print(f"Challenge:{challenge_line}") prefix = challenge_line.split("XXXX+")[1].split(")")[0] target = challenge_line.split("== ")[1] print(f"POW: XXXX+{prefix}->{target}") # 使用多进程爆破 solution = solve_pow_local(prefix, target,8) io.sendlineafter(b":", solution.encode()) print("Solution sent successfully!") # 解密 io.recvline() n = int(io.recvline().decode().strip("n").split(" = ")[-1]) e = int(io.recvline().decode().strip("n").split(" = ")[-1]) c = int.from_bytes(bytes.fromhex(io.recvline().decode().strip("n").split(" = ")[-1]),'little') io.close() d = inverse(e, n -1) m = pow(c, d, n) flag = long_to_bytes(m) print(flag)
0xGame{3aca3562-efe5-4056-a01d-e6b0f0f1bf80}
```


---
## 附图

[图片已移除]
[图片已移除]