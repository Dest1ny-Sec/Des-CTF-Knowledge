# GDG Algiers CTF两道矩阵题wp

> 原文: https://www.ctfiot.com/73582.html
> ID: 73582

gdgalgiers crypto wp

两道矩阵相关的题，感觉可以整理一下下。

the_matrix

python sln.py

CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}

franklin-last-words

# from sage.all import *import jsonfrom Crypto.Hash import SHA256from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad p = 12143520799543738643# def read_matrix(file_name):# data = open(file_name, 'r').read().strip()# rows = [list(eval(row)) for row in data.splitlines()]# return Matrix(GF(p), rows)### D = read_matrix('matrix.txt')# P = read_matrix('public_key.txt')# digD ,A = D.diagonalization()# digP = A.inverse() * P * A# vD = [digD[i][i] for i in range(12)]# vP = [digP[i][i] for i in range(12)]# print(f"vD = {vD}")vD = [37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2]# print(f"vP = {vP}")vP = [6751925379844785295, 11256715989719283883, 4551561838026472495, 11383130904596697638, 8534299476177021992, 11184828239802784209, 7103104085280766875, 1622643043767580331, 11104789109564474465, 1502559189506368871, 522368022672629021, 1590703325067650792]# G = GF(p)# K = discrete_log(G(vP[11]), G(vD[11]))# print(f"K = {K}")K = 7619698002081645976 # now we can decipherkey = SHA256.new(data=str(K).encode()).digest()[:2**8]with open("encrypted_flag.txt", "r") as ff: data_dict = json.load(ff) iv = bytes.fromhex(data_dict["iv"]) ciphertext = bytes.fromhex(data_dict["ciphertext"])cipher = AES.new(key, AES.MODE_CBC, iv)flag = cipher.decrypt(ciphertext).decode()[:46]print(flag)# CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}

python sln.py

CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}

from sage.all import Matrix, IntegerModRingfrom message import N, e, ct def poly(num): return [(3*pow(num, 3, N)) % N, (3*pow(num, 6, N)) % N] def v2polyv(v, num): return (v - R_3 - pow(num, 9, N)) % N def polyv2v(v, num): return (v + R_3 + pow(num, 9, N)) % N def gen(num): V2 = Matrix(IntegerModRing(N), [poly(num)]) V1 = V2 * T_ v = (poly_C*V1[0][0] + poly_y*V1[0][1]) % N table[polyv2v(v, num)] = chr(num) table = {}R_3 = ct[0]prefix = b"CyberErudites{}"T = Matrix(IntegerModRing(N), [poly(int(prefix[0])), poly(int(prefix[1]))])T_ = T.inverse()# print(T_)poly_C = v2polyv(ct[1], ord('C'))poly_y = v2polyv(ct[2], ord('y')) for num in range(32, 126): gen(num)print("".join([table[v] for v in ct[1:]]))# CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}

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
# from sage.all import *import jsonfrom Crypto.Hash import SHA256from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad p = 12143520799543738643# def read_matrix(file_name):# data = open(file_name, 'r').read().strip()# rows = [list(eval(row)) for row in data.splitlines()]# return Matrix(GF(p), rows)### D = read_matrix('matrix.txt')# P = read_matrix('public_key.txt')# digD ,A = D.diagonalization()# digP = A.inverse() * P * A# vD = [digD[i][i] for i in range(12)]# vP = [digP[i][i] for i in range(12)]# print(f"vD = {vD}")vD = [37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2]# print(f"vP = {vP}")vP = [6751925379844785295, 11256715989719283883, 4551561838026472495, 11383130904596697638, 8534299476177021992, 11184828239802784209, 7103104085280766875, 1622643043767580331, 11104789109564474465, 1502559189506368871, 522368022672629021, 1590703325067650792]# G = GF(p)# K = discrete_log(G(vP[11]), G(vD[11]))# print(f"K = {K}")K = 7619698002081645976 # now we can decipherkey = SHA256.new(data=str(K).encode()).digest()[:2**8]with open("encrypted_flag.txt", "r") as ff: data_dict = json.load(ff) iv = bytes.fromhex(data_dict["iv"]) ciphertext = bytes.fromhex(data_dict["ciphertext"])cipher = AES.new(key, AES.MODE_CBC, iv)flag = cipher.decrypt(ciphertext).decode()[:46]print(flag)# CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}
```



```
from sage.all import Matrix, IntegerModRingfrom message import N, e, ct def poly(num): return [(3*pow(num, 3, N)) % N, (3*pow(num, 6, N)) % N] def v2polyv(v, num): return (v - R_3 - pow(num, 9, N)) % N def polyv2v(v, num): return (v + R_3 + pow(num, 9, N)) % N def gen(num): V2 = Matrix(IntegerModRing(N), [poly(num)]) V1 = V2 * T_ v = (poly_C*V1[0][0] + poly_y*V1[0][1]) % N table[polyv2v(v, num)] = chr(num) table = {}R_3 = ct[0]prefix = b"CyberErudites{}"T = Matrix(IntegerModRing(N), [poly(int(prefix[0])), poly(int(prefix[1]))])T_ = T.inverse()# print(T_)poly_C = v2polyv(ct[1], ord('C'))poly_y = v2polyv(ct[2], ord('y')) for num in range(32, 126): gen(num)print("".join([table[v] for v in ct[1:]]))# CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668336811.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668336812.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668336812.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668336812.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668336813.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668336813.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1668336813.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668336814.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668336814.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668336814.gif)