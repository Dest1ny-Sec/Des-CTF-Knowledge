# 【相关分享】星芒杯2025 WriteUP

> 原文: https://www.ctfiot.com/285553.html
> ID: 285553

❝

由于传播、利用本公众号”隼目安全”所提供的信息而造成的任何直接或者间接的后果及损失,均由使用者本人负责,公众号”隼目安全”及作者不为此承担任何责任,一旦造成后果请自行承担!如有侵权烦请告知,我们会立即删除并致歉谢谢！

【web】

代码审计

<?php$source= file_get_contents(__FILE__);$hidden_source= preg_replace('/define('FLAG', '.*?');/','define('FLAG', '[FLAG HIDDEN]');',$source);echo"". htmlspecialchars($hidden_source) ."";error_reporting(0);define('FLAG','[FLAG HIDDEN]');functionshow_flag($key) { if($key==='secret_key') { echo"

Flag: ". FLAG; }}$func=$_GET['func'] ??'';$param=$_GET['param'] ??'';if(function_exists($func)) { call_user_func($func,$param);}?>

题目描述：访问目标网站，你将看到PHP源码。审计该源码，分析存在的漏洞，将直接导致 flag 输出的核心函数名作为 flag 提交，flag格式：flag{xxxxx}。

额文字游戏，直接把rce函数call_user_func套上flag提交

布莱切利庄园

username是乱码，将该字符串按ISO-8859-1编码还原为原始字节流，将得到的字节流按 UTF-8 重新解码

password是盲文，直接解码就行

密码：darkguard98

print("éu0081u0097èu00bfxb9èu0099u009açu00a9u00baæu009fu0092".encode('latin1').decode('utf-8'))、#遗迹虚空柒

有点奇怪，再开一次容器后

用户名变成了:
遗迹秘密伍

密码变成了:
secretgate45

登录后发现/archives?file=存在文件读取

/flag发现是一个音频文件

然后在读取 web.xml 发现Servlet 3.0+看不到类名 所以要根据包名去猜

?file=/usr/local/tomcat/webapps/ROOT/WEB-INF/classes/com/scp/temple/servlet/ArchivesServlet.class

读取ArchivesServlet.class

发现引入了java.util.Base64并且调用了encodeToString

我没有反编译，直接猜了一个参数

?file=/flag&filter=base64

base64解码导出音频，一听咔咔咔 马上知道是sstv

布莱切利庄园

分析题目 我们需要伪造一个 Payload 为{"name":"COMMANDER"}的 Token 来通过api/mails接口拦截指挥官的邮件

Header 中的 alg 改为 None，并去掉签名部分

伪造了COMMANDER的身份后，并拦截到了两封密电

HTTP/1.1 200 OKContent-Length: 207Content-Type: application/json;charset=UTF-8Date: Sat, 06 Dec 2025 02:44:22 GMTConnection: close{"user":"COMMANDER","mails":["发件人: 气象部|主题: 天气预报nn密文：nKFJCURZLZQJABAWNJUQYQYSRLNPPPNAAYLIFWH","发件人: 最高指令|主题: FLAGnn密文：nIHNIHNUELFBMTGNQJUPSMWYEH"]}

已知明文:

明文:
WEATHERFORECASTWINDNORTHVISIBILITYGOOD(来自上一封邮件)

密文:
KFJCURZLZQJABAWNJUQYQYSRLNPPPNAAYLIFWH(来自气象部邮件)

用途:
用于反推 Enigma 的密钥

使用反推的密钥解密这段密文:

密文:
IHNIHNUELFBMTGNQJUPSMWYEH(来自最高指令)

先爆破Enigma的Rotor Start Position,锁定Rotor Start Position以后再爆破Plugboard，然后使用密钥解密密文

import itertools
class Enigma: def __init__(self, start_pos, pairs=[]): self.rotors = [ {'w':'EKMFLGDQVZNTOWYHXUSPAIBRCJ','n':'Q'}, {'w':'AJDKSIRUXBLHWTMCQGZNPYFVOE','n':'E'}, {'w':'BDFHJLCPRTXVZNYEIWGAKMUSQO','n':'V'} ] self.reflector ='YRUHQSLDPXNGOKMIEBFZCWVJAT' self.pos = [ord(p) - 65forpinstart_pos] self.pb = list(range(26)) fora, binpairs: u, v = ord(a) - 65, ord(b) - 65 self.pb[u], self.pb[v] = v, u def crypt(self, char): ifchr(self.pos[1] + 65) == self.rotors[1]['n']: self.pos[0] = (self.pos[0] + 1) % 26 self.pos[1] = (self.pos[1] + 1) % 26 elifchr(self.pos[2] + 65) == self.rotors[2]['n']: self.pos[1] = (self.pos[1] + 1) % 26 self.pos[2] = (self.pos[2] + 1) % 26 c = self.pb[ord(char) - 65] foriinrange(2, -1, -1): offset = self.pos[i] c = (c + offset) % 26 c = (ord(self.rotors[i]['w'][c]) - 65 - offset) % 26 c = ord(self.reflector[c]) - 65 foriinrange(3): offset = self.pos[i] c = (c + offset) % 26 c = (self.rotors[i]['w'].find(chr(c + 65)) - offset) % 26 returnchr(self.pb[c] + 65)plain ="WEATHERFORECASTWINDNORTHVISIBILITYGOOD"cipher ="KFJCURZLZQJABAWNJUQYQYSRLNPPPNAAYLIFWH"target ="IHNIHNUELFBMTGNQJUPSMWYEH"alphabet ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"best_pos =""fori, j, kinitertools.product(alphabet, repeat=3): pos = i + j + k e = Enigma(pos) matches = sum(1forp, cinzip(plain, cipher)ife.crypt(p) == c) ifmatches > 25: best_pos = pos breakfinal_pairs = []forp1initertools.combinations(alphabet, 2): rem = [xforxinalphabetifx notinp1] forp2initertools.combinations(rem, 2): pairs = [p1, p2] e = Enigma(best_pos, pairs) ifall(e.crypt(p) == cforp, cinzip(plain, cipher)): final_pairs = pairs break iffinal_pairs:
breakres =""e = Enigma(best_pos, final_pairs)forcintarget: res += e.crypt(c)print(f"Key: {best_pos}, Plugboard: {final_pairs}")print(f"Flag: flag{{{res.lower()}}}")

【misc】

禾信智安

神秘的编码纸条

base64两层

【crypto】

Signature

ECDSA 签名恢复

from pwn import *import hashlib
from ecdsa import SECP256k1from ecdsa.util import sigdecode_stringimport json
# ================= 终极配置 =================# 增加样本池到 50 对 (共100个签名)，方便优中选优NCOUNT = 50 # 保持适当的测量次数，防止超时TRAIN_TIMES = 80
# 保持 8 bit，这是最佳平衡点KBITS = 8 # ===========================================context.log_level ='info'print(f"[*] Connecting... (Collecting {NCOUNT*2} sigs to pick TOP 3)")io = remote('nc1.ctfplus.cn',26373)io.sendlineafter(b"Enter kbits", str(KBITS).encode())io.sendlineafter(b"Enter ncount and train_times:", f"{NCOUNT} {TRAIN_TIMES}".encode())print("[*] Receiving data...")try: # 增加超时时间，防止数据量大时断开 raw_data = io.recvline(timeout=30).decode().strip().replace("'",'"') data = json.loads(raw_data)
except Exception as e: print(f"[-] Error receiving data: {e}") print("[-] Server might have timed out. Reduce TRAIN_TIMES slightly.") exit()costs = data['costs']sigs = data['sigs']# 数据清洗samples = []forc, s_hexinzip(costs, sigs): sig_bytes = bytes.fromhex(s_hex) r, s = sigdecode_string(sig_bytes, SECP256k1.order) samples.append({'cost': c,'r': r,'s': s})
# 排序samples.sort(key=lambda x: x['cost'])
# === 关键诊断：打印耗时数据 ===print("n[+] Timing Analysis (nanoseconds):")print(f"Top 1 (Fastest): {samples[0]['cost']}")print(f"Top 3: {samples[2]['cost']}")print(f"Top 10: {samples[9]['cost']}")print(f"Top 50 (Median): {samples[50]['cost']}")
# 如果 Top3 和 Median 差别很小，说明侧信道失败ifsamples[50]['cost'] - samples[2]['cost'] < 100000: print("n[!] WARNING: Timing gap is too small! Data might be useless.") print("[!] Recommendation: Run the script again.")else: print("n[+] Good gap detected! High probability of success.")
# === 只取前 3 个最稳的样本 ===# 只要这3个是干净的，就必出 Flagfiltered_samples = samples[:3]rs = [x['r']forxinfiltered_samples]ss = [x['s']forxinfiltered_samples]msg = b"try hack me!"z = int.from_bytes(hashlib.sha256(msg).digest(),'big')print("n"+"="*20 +" COPY SAGE CODE "+"="*20)print(f"rs = {rs}")print(f"ss = {ss}")print(f"z = {z}")print(f"kbits = {KBITS}")print(f"order = {int(SECP256k1.order)}")print("Running correct HNP solver (Eliminating d)...")#获取密文后运行Sage代码如下：# rs = [42781960159024299958163639356878453190501432691827926213851649420102986506453, 39048226050737083614040617721217157354131877742605504762042212999754192445011, 39048226050737083614040617721217157354131877742605504762042212999754192445011]# ss = [65714030334550582835969301395866405087191574479259550020255991947690098006834, 91178713750437107105945632930291498245533930619184888878476278979837930006418, 91178713750437107105945632930291498245533930619184888878476278979837930006418]# z = 69670596422853282396471780477436535764323143921602727122946730040594665238047
# kbits = 8
# order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# print("Running correct HNP solver (Eliminating d)...")
# # 1. 准备参数
# m = len(rs)
# # 计算 t_i 和 u_i
# # k_i - t_i * d = u_i (mod n)
# ts = []# us = []# for i in range(m):# s_inv = inverse_mod(ss[i], order)
# t = (rs[i] * s_inv) % order
# u = (z * s_inv) % order
# ts.append(t)
# us.append(u)
# # 2. 构建矩阵 (SVP approach eliminating d)
# # 我们将方程转化为: k_i - A_i * k_0 - B_i = 0 (mod n)
# # 这样就消去了 d，只剩下短向量 k
# matrix_rows = []# # t0_inv 用于消元
# t0_inv = inverse_mod(ts[0], order)
# # 构造矩阵
# # 第一行: k0 的系数
# row0 = [1] + [(ts[i] * t0_inv) % order for i in range(1, m)] + [0]# matrix_rows.append(row0)
# # 中间行: 模数 n
# for i in range(1, m):# row = [0] * (m + 1)
# row[i] = order
# matrix_rows.append(row)
# # 最后一行: 常数项 B_i
# # B_i = u_i - A_i * u_0
# bi_list = [(us[i] - (ts[i] * t0_inv % order) * us[0]) % order for i in range(1, m)]# # 这里的常数项在 SVP 中通常作为最后一维，带上一个 scaling factor (比如 2^8)
# # 我们构建向量 v = (k0, k1, k2, ..., 2^kbits)
# row_last = [0] + bi_list + [2**(kbits)]# matrix_rows.append(row_last)
# # 3. 运行 LLL
# L = Matrix(ZZ, matrix_rows)
# print(f"Lattice dimension: {L.nrows()}x{L.ncols()}")
# L_reduced = L.LLL()
# # 4. 寻找答案
# found = False
# for row in L_reduced:# # 我们的目标向量第一列应该是 k0
# # k0 必须是 8-bit 的短整数
# k0_candidate = abs(row[0]) # if k0_candidate > 0 and k0_candidate < 2**(kbits + 5):# # 找到了可能的 k0！# # 利用 k0 恢复 d
# # d = (k0 - u0) * t0^-1
# d_candidate = ((k0_candidate - us[0]) * t0_inv) % order # # 验证一下
# # 算一下对应的公钥或者检查其他 k 是否也小
# valid = True
# for i in range(1, m):# ki = (us[i] + ts[i] * d_candidate) % order
# if ki > 2**(kbits + 5):# valid = False
# break # if valid:# print("n" + "!"*50)
# print("SUCCESS! KEY RECOVERED")
# print(f"Private Key: {d_candidate}")
# print("!"*50)
# found = True
# break
# if not found:# print("Solver failed. NOW you can blame the data.")guess = input("Paste the Private Key found in Sage here: ")io.sendlineafter(b"Guess the privatekey", str(guess).encode())io.interactive()

往期推荐

【重要通知】警惕！有人在仿冒Xshell散播病毒？！

2025年广西网络与信息安全职业技能竞赛决赛 awd web部分 赛后WriteUP以及自我检讨

坏了坏了

2025年广西网络与信息安全职业技能竞赛WriteUP

Z0Scan设计与实现：通用插件与分布式扫描新思路


```
<?php$source= file_get_contents(__FILE__);$hidden_source= preg_replace('/define('FLAG', '.*?');/','define('FLAG', '[FLAG HIDDEN]');',$source);echo"". htmlspecialchars($hidden_source) ."";error_reporting(0);define('FLAG','[FLAG HIDDEN]');functionshow_flag($key) { if($key==='secret_key') { echo"

Flag: ". FLAG; }}$func=$_GET['func'] ??'';$param=$_GET['param'] ??'';if(function_exists($func)) { call_user_func($func,$param);}?>
print("éu0081u0097èu00bfxb9èu0099u009açu00a9u00baæu009fu0092".encode('latin1').decode('utf-8'))、#遗迹虚空柒
?file=/usr/local/tomcat/webapps/ROOT/WEB-INF/classes/com/scp/temple/servlet/ArchivesServlet.class
?file=/flag&filter=base64
HTTP/1.1 200 OKContent-Length: 207Content-Type: application/json;charset=UTF-8Date: Sat, 06 Dec 2025 02:44:22 GMTConnection: close{"user":"COMMANDER","mails":["发件人: 气象部|主题: 天气预报nn密文：nKFJCURZLZQJABAWNJUQYQYSRLNPPPNAAYLIFWH","发件人: 最高指令|主题: FLAGnn密文：nIHNIHNUELFBMTGNQJUPSMWYEH"]}
import itertools
class Enigma: def __init__(self, start_pos, pairs=[]): self.rotors = [ {'w':'EKMFLGDQVZNTOWYHXUSPAIBRCJ','n':'Q'}, {'w':'AJDKSIRUXBLHWTMCQGZNPYFVOE','n':'E'}, {'w':'BDFHJLCPRTXVZNYEIWGAKMUSQO','n':'V'} ] self.reflector ='YRUHQSLDPXNGOKMIEBFZCWVJAT' self.pos = [ord(p) - 65forpinstart_pos] self.pb = list(range(26)) fora, binpairs: u, v = ord(a) - 65, ord(b) - 65 self.pb[u], self.pb[v] = v, u def crypt(self, char): ifchr(self.pos[1] + 65) == self.rotors[1]['n']: self.pos[0] = (self.pos[0] + 1) % 26 self.pos[1] = (self.pos[1] + 1) % 26 elifchr(self.pos[2] + 65) == self.rotors[2]['n']: self.pos[1] = (self.pos[1] + 1) % 26 self.pos[2] = (self.pos[2] + 1) % 26 c = self.pb[ord(char) - 65] foriinrange(2, -1, -1): offset = self.pos[i] c = (c + offset) % 26 c = (ord(self.rotors[i]['w'][c]) - 65 - offset) % 26 c = ord(self.reflector[c]) - 65 foriinrange(3): offset = self.pos[i] c = (c + offset) % 26 c = (self.rotors[i]['w'].find(chr(c + 65)) - offset) % 26 returnchr(self.pb[c] + 65)plain ="WEATHERFORECASTWINDNORTHVISIBILITYGOOD"cipher ="KFJCURZLZQJABAWNJUQYQYSRLNPPPNAAYLIFWH"target ="IHNIHNUELFBMTGNQJUPSMWYEH"alphabet ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"best_pos =""fori, j, kinitertools.product(alphabet, repeat=3): pos = i + j + k e = Enigma(pos) matches = sum(1forp, cinzip(plain, cipher)ife.crypt(p) == c) ifmatches > 25: best_pos = pos breakfinal_pairs = []forp1initertools.combinations(alphabet, 2): rem = [xforxinalphabetifx notinp1] forp2initertools.combinations(rem, 2): pairs = [p1, p2] e = Enigma(best_pos, pairs) ifall(e.crypt(p) == cforp, cinzip(plain, cipher)): final_pairs = pairs break iffinal_pairs:
breakres =""e = Enigma(best_pos, final_pairs)forcintarget: res += e.crypt(c)print(f"Key: {best_pos}, Plugboard: {final_pairs}")print(f"Flag: flag{{{res.lower()}}}")
from pwn import *import hashlib
from ecdsa import SECP256k1from ecdsa.util import sigdecode_stringimport json
# ================= 终极配置 =================# 增加样本池到 50 对 (共100个签名)，方便优中选优NCOUNT = 50 # 保持适当的测量次数，防止超时TRAIN_TIMES = 80
# 保持 8 bit，这是最佳平衡点KBITS = 8 # ===========================================context.log_level ='info'print(f"[*] Connecting... (Collecting {NCOUNT*2} sigs to pick TOP 3)")io = remote('nc1.ctfplus.cn',26373)io.sendlineafter(b"Enter kbits", str(KBITS).encode())io.sendlineafter(b"Enter ncount and train_times:", f"{NCOUNT} {TRAIN_TIMES}".encode())print("[*] Receiving data...")try: # 增加超时时间，防止数据量大时断开 raw_data = io.recvline(timeout=30).decode().strip().replace("'",'"') data = json.loads(raw_data)
except Exception as e: print(f"[-] Error receiving data: {e}") print("[-] Server might have timed out. Reduce TRAIN_TIMES slightly.") exit()costs = data['costs']sigs = data['sigs']# 数据清洗samples = []forc, s_hexinzip(costs, sigs): sig_bytes = bytes.fromhex(s_hex) r, s = sigdecode_string(sig_bytes, SECP256k1.order) samples.append({'cost': c,'r': r,'s': s})
# 排序samples.sort(key=lambda x: x['cost'])
# === 关键诊断：打印耗时数据 ===print("n[+] Timing Analysis (nanoseconds):")print(f"Top 1 (Fastest): {samples[0]['cost']}")print(f"Top 3: {samples[2]['cost']}")print(f"Top 10: {samples[9]['cost']}")print(f"Top 50 (Median): {samples[50]['cost']}")
# 如果 Top3 和 Median 差别很小，说明侧信道失败ifsamples[50]['cost'] - samples[2]['cost'] < 100000: print("n[!] WARNING: Timing gap is too small! Data might be useless.") print("[!] Recommendation: Run the script again.")else: print("n[+] Good gap detected! High probability of success.")
# === 只取前 3 个最稳的样本 ===# 只要这3个是干净的，就必出 Flagfiltered_samples = samples[:3]rs = [x['r']forxinfiltered_samples]ss = [x['s']forxinfiltered_samples]msg = b"try hack me!"z = int.from_bytes(hashlib.sha256(msg).digest(),'big')print("n"+"="*20 +" COPY SAGE CODE "+"="*20)print(f"rs = {rs}")print(f"ss = {ss}")print(f"z = {z}")print(f"kbits = {KBITS}")print(f"order = {int(SECP256k1.order)}")print("Running correct HNP solver (Eliminating d)...")#获取密文后运行Sage代码如下：# rs = [42781960159024299958163639356878453190501432691827926213851649420102986506453, 39048226050737083614040617721217157354131877742605504762042212999754192445011, 39048226050737083614040617721217157354131877742605504762042212999754192445011]# ss = [65714030334550582835969301395866405087191574479259550020255991947690098006834, 91178713750437107105945632930291498245533930619184888878476278979837930006418, 91178713750437107105945632930291498245533930619184888878476278979837930006418]# z = 69670596422853282396471780477436535764323143921602727122946730040594665238047
# kbits = 8
# order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# print("Running correct HNP solver (Eliminating d)...")
# # 1. 准备参数
# m = len(rs)
# # 计算 t_i 和 u_i
# # k_i - t_i * d = u_i (mod n)
# ts = []# us = []# for i in range(m):# s_inv = inverse_mod(ss[i], order)
# t = (rs[i] * s_inv) % order
# u = (z * s_inv) % order
# ts.append(t)
# us.append(u)
# # 2. 构建矩阵 (SVP approach eliminating d)
# # 我们将方程转化为: k_i - A_i * k_0 - B_i = 0 (mod n)
# # 这样就消去了 d，只剩下短向量 k
# matrix_rows = []# # t0_inv 用于消元
# t0_inv = inverse_mod(ts[0], order)
# # 构造矩阵
# # 第一行: k0 的系数
# row0 = [1] + [(ts[i] * t0_inv) % order for i in range(1, m)] + [0]# matrix_rows.append(row0)
# # 中间行: 模数 n
# for i in range(1, m):# row = [0] * (m + 1)
# row[i] = order
# matrix_rows.append(row)
# # 最后一行: 常数项 B_i
# # B_i = u_i - A_i * u_0
# bi_list = [(us[i] - (ts[i] * t0_inv % order) * us[0]) % order for i in range(1, m)]# # 这里的常数项在 SVP 中通常作为最后一维，带上一个 scaling factor (比如 2^8)
# # 我们构建向量 v = (k0, k1, k2, ..., 2^kbits)
# row_last = [0] + bi_list + [2**(kbits)]# matrix_rows.append(row_last)
# # 3. 运行 LLL
# L = Matrix(ZZ, matrix_rows)
# print(f"Lattice dimension: {L.nrows()}x{L.ncols()}")
# L_reduced = L.LLL()
# # 4. 寻找答案
# found = False
# for row in L_reduced:# # 我们的目标向量第一列应该是 k0
# # k0 必须是 8-bit 的短整数
# k0_candidate = abs(row[0]) # if k0_candidate > 0 and k0_candidate < 2**(kbits + 5):# # 找到了可能的 k0！# # 利用 k0 恢复 d
# # d = (k0 - u0) * t0^-1
# d_candidate = ((k0_candidate - us[0]) * t0_inv) % order # # 验证一下
# # 算一下对应的公钥或者检查其他 k 是否也小
# valid = True
# for i in range(1, m):# ki = (us[i] + ts[i] * d_candidate) % order
# if ki > 2**(kbits + 5):# valid = False
# break # if valid:# print("n" + "!"*50)
# print("SUCCESS! KEY RECOVERED")
# print(f"Private Key: {d_candidate}")
# print("!"*50)
# found = True
# break
# if not found:# print("Solver failed. NOW you can blame the data.")guess = input("Paste the Private Key found in Sage here: ")io.sendlineafter(b"Guess the privatekey", str(guess).encode())io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099238-wxsync-2025-12-fae44099e0d15e2b162e8aa5004b59cc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099240-wxsync-2025-12-e1fe3285847ddf32cb98a702e410a8cb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099242-wxsync-2025-12-58214c0410c2cc9eee91435ede593c4f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099245-wxsync-2025-12-966de32174729e825deb6e93b19f0826.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099248-wxsync-2025-12-f0d695c508ea6784eb17df0d6cc04412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099250-wxsync-2025-12-3c42490c982c4338463c5eb66a055076.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099253-wxsync-2025-12-abfe253f75569ac5dc296989df0a45cd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099255-wxsync-2025-12-554da7430e2e3930b732202ac1ea38f8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099257-wxsync-2025-12-c6fb8f7af70d80d51434de7cde7fe9bc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765099260-wxsync-2025-12-e50e94ea0cb2fff6fd91796048f5f7d5.png)