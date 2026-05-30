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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760488616-wxsync-2025-10-6a60ef787c962c7076a0bda6e9e7aa6f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760488617-wxsync-2025-10-5dd7e40ff508db08bfe6f99328cd990e.png)