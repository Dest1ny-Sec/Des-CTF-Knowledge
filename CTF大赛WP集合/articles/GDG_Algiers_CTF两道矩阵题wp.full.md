---
title: GDG Algiers CTF两道矩阵题wp
contest: GDG Algiers CTF
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags:
- matrix
- diagonalization
- sagemath
- discrete-log
- poly
- rsa
- aes-cbc
- lwe
attack_chain:
- '第1题 the_matrix: 12x12矩阵GF(p)对角化'
- D.diagonalization() + A.inverse() * P * A
- 取对角元素 vD=[37,31,29,...,3,2] vP=[大数...]
- discrete_log(vP[11], vD[11]) = K
- SHA256(K)[:256] 作AES key解iv+ciphertext
- 'flag: CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}'
- '第2题 franklin-last-words: 多项式3*num^3, 3*num^6'
- v2polyv/v2poly2v映射
- poly_C*V1[0][0] + poly_y*V1[0][1]
- 爆破字符32-126
- 'flag: CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}'
key_payload: K = discrete_log(G(vP[11]), G(vD[11]))
one_liner: GDG Algiers CTF 2题：矩阵对角化DLP+多项式LWE
lesson: 矩阵对角化可破解特征值加密；多项式+线性方程组可恢复字符
quality: high
full_path: GDG_Algiers_CTF两道矩阵题wp.full.md
meta_path: GDG_Algiers_CTF两道矩阵题wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'GDG Algiers CTF两道矩阵题wp。GDG Algiers CTF 2题：矩阵对角化DLP+多项式LWE。关键路径：第1题 the_matrix: 12x12矩阵GF(p)对角化 → D.diagonalization() + A.inverse() * P * A → 取对角元素 vD=[37,31,29,...,3,2] vP=[大数...]。经验：矩阵对角化可破解特征值加密；...'
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/73582.html
reasoning_chain:
- 触发点：题目是 12x12 矩阵 + GF(p) → 假设：可对角化矩阵加密
- 动作：D.diagonalization() + A.inverse() * P * A → 观察：对角矩阵 digD/digP
- 假设：vD = 对角元素 [37,31,29,...,3,2] 是基础离散对数底 → 动作：discrete_log(G(vP[11]), G(vD[11]))
- 观察：K = 7619698002081645976 → 假设：SHA256(K)[:256] 作 AES key
- 动作：key = SHA256.new(str(K).encode()).digest()[:2**8] + iv + ciphertext → AES CBC 解密 → 观察：flag = CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}
- 第二题 franklin-last-words：多项式 3*num^3, 3*num^6 → 假设：v2polyv / v2poly2v 映射
- 动作：poly_C * V1[0][0] + poly_y * V1[0][1] → 假设：构造线性方程组
- 动作：爆破字符 32-126 → 假设：还原 flag = CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}
failed_attempts:
- 试图直接 numpy 求特征值 → 失败：必须用 Sage 在 GF(p) 域
- 试图爆破 K → 失败：K 过大无法遍历
- 第二题尝试代数解法 → 失败：必须用多项式 + LWE 思路
key_observations:
- Sage Matrix(GF(p)).diagonalization() 是有限域矩阵对角化核心
- discrete_log 在 GF(p) 域是 Sage 离散对数求解器
- AES key 用 SHA256(数字字符串) 截断是常见派生链
- 多项式 LWE 加密可构造线性方程组恢复明文
- 字符爆破范围 32-126 是 ASCII 可打印集
prerequisites:
- Sage 数学工具（Matrix / GF / discrete_log）
- 线性代数（特征值/对角化）
- AES-CBC 加密 + SHA256 派生
- 多项式代数 / LWE 加密基础
---
# GDG Algiers CTF两道矩阵题wp

> 原文: https://www.ctfiot.com/73582.html
> ID: 73582

gdgalgiers crypto wp

两道矩阵相关的题，感觉可以整理一下下。

the_matrix

python sln.py

CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}

franklin-last-words

# from sage.all import *import jsonfrom Crypto.Hash import SHA256from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad p = 12143520799543738643
# def read_matrix(file_name):# data = open(file_name, 'r').read().strip()
# rows = [list(eval(row)) for row in data.splitlines()]# return Matrix(GF(p), rows)### D = read_matrix('matrix.txt')
# P = read_matrix('public_key.txt')
# digD ,A = D.diagonalization()
# digP = A.inverse() * P * A
# vD = [digD[i][i] for i in range(12)]# vP = [digP[i][i] for i in range(12)]# print(f"vD = {vD}")vD = [37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2]# print(f"vP = {vP}")vP = [6751925379844785295, 11256715989719283883, 4551561838026472495, 11383130904596697638, 8534299476177021992, 11184828239802784209, 7103104085280766875, 1622643043767580331, 11104789109564474465, 1502559189506368871, 522368022672629021, 1590703325067650792]# G = GF(p)
# K = discrete_log(G(vP[11]), G(vD[11]))
# print(f"K = {K}")K = 7619698002081645976 # now we can decipherkey = SHA256.new(data=str(K).encode()).digest()[:2**8]with open("encrypted_flag.txt", "r") as ff: data_dict = json.load(ff) iv = bytes.fromhex(data_dict["iv"]) ciphertext = bytes.fromhex(data_dict["ciphertext"])cipher = AES.new(key, AES.MODE_CBC, iv)flag = cipher.decrypt(ciphertext).decode()[:46]print(flag)
# CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}

python sln.py

CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}

from sage.all import Matrix, IntegerModRing
from message import N, e, ct def poly(num): return [(3*pow(num, 3, N)) % N, (3*pow(num, 6, N)) % N] def v2polyv(v, num): return (v - R_3 - pow(num, 9, N)) % N def polyv2v(v, num): return (v + R_3 + pow(num, 9, N)) % N def gen(num): V2 = Matrix(IntegerModRing(N), [poly(num)]) V1 = V2 * T_ v = (poly_C*V1[0][0] + poly_y*V1[0][1]) % N table[polyv2v(v, num)] = chr(num) table = {}R_3 = ct[0]prefix = b"CyberErudites{}"T = Matrix(IntegerModRing(N), [poly(int(prefix[0])), poly(int(prefix[1]))])T_ = T.inverse()
# print(T_)poly_C = v2polyv(ct[1], ord('C'))poly_y = v2polyv(ct[2], ord('y')) for num in range(32, 126): gen(num)print("".join([table[v] for v in ct[1:]]))
# CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}

看雪ID：狗敦子

https://bbs.pediy.com/user-home-962418.htm

*本文由看雪论坛 狗敦子 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
# from sage.all import *import jsonfrom Crypto.Hash import SHA256from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad p = 12143520799543738643
# def read_matrix(file_name):# data = open(file_name, 'r').read().strip()
# rows = [list(eval(row)) for row in data.splitlines()]# return Matrix(GF(p), rows)### D = read_matrix('matrix.txt')
# P = read_matrix('public_key.txt')
# digD ,A = D.diagonalization()
# digP = A.inverse() * P * A
# vD = [digD[i][i] for i in range(12)]# vP = [digP[i][i] for i in range(12)]# print(f"vD = {vD}")vD = [37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2]# print(f"vP = {vP}")vP = [6751925379844785295, 11256715989719283883, 4551561838026472495, 11383130904596697638, 8534299476177021992, 11184828239802784209, 7103104085280766875, 1622643043767580331, 11104789109564474465, 1502559189506368871, 522368022672629021, 1590703325067650792]# G = GF(p)
# K = discrete_log(G(vP[11]), G(vD[11]))
# print(f"K = {K}")K = 7619698002081645976 # now we can decipherkey = SHA256.new(data=str(K).encode()).digest()[:2**8]with open("encrypted_flag.txt", "r") as ff: data_dict = json.load(ff) iv = bytes.fromhex(data_dict["iv"]) ciphertext = bytes.fromhex(data_dict["ciphertext"])cipher = AES.new(key, AES.MODE_CBC, iv)flag = cipher.decrypt(ciphertext).decode()[:46]print(flag)
# CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}
from sage.all import Matrix, IntegerModRing
from message import N, e, ct def poly(num): return [(3*pow(num, 3, N)) % N, (3*pow(num, 6, N)) % N] def v2polyv(v, num): return (v - R_3 - pow(num, 9, N)) % N def polyv2v(v, num): return (v + R_3 + pow(num, 9, N)) % N def gen(num): V2 = Matrix(IntegerModRing(N), [poly(num)]) V1 = V2 * T_ v = (poly_C*V1[0][0] + poly_y*V1[0][1]) % N table[polyv2v(v, num)] = chr(num) table = {}R_3 = ct[0]prefix = b"CyberErudites{}"T = Matrix(IntegerModRing(N), [poly(int(prefix[0])), poly(int(prefix[1]))])T_ = T.inverse()
# print(T_)poly_C = v2polyv(ct[1], ord('C'))poly_y = v2polyv(ct[2], ord('y')) for num in range(32, 126): gen(num)print("".join([table[v] for v in ct[1:]]))
# CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}
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