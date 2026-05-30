# 解析2025LitCTF leak

> 原文: https://www.ctfiot.com/279542.html
> ID: 279542

RSA私钥泄露攻击深度解析：180位泄露如何导致2048位RSA彻底崩溃

警示：在密码学的世界里，”小漏洞”往往意味着”大灾难”

触目惊心的现实

想象一下：你的银行使用了2048位的RSA加密，这在当前标准下被认为是”坚不可摧”的。但如果攻击者只获得了你私钥中极小一部分——仅仅180位信息——会发生什么？

一道来自LitCTF 2025的密码学题目揭示了一个令人不安的真相：攻击者完全可以恢复你的完整私钥！

这不是理论威胁，而是现实存在的攻击方法。今天，让我们深入这个看似不可思议但数学上完美成立的攻击世界。

漏洞的发现

题目核心代码分析

# 看似正常的RSA实现，却隐藏着致命漏洞fromCrypto.Util.numberimport*fromencimportflagm = bytes_to_long(flag)p,q,e = getPrime(1024),getPrime(1024),getPrime(101)n = p*qtemp = gmpy2.invert(e,p-1) # 计算dp = e^(-1) mod (p-1)c = pow(m,e,n)hint = temp>>180# 致命的一行：泄露dp的高位！print(f"e ={e}")print(f"n ={n}")print(f"c ={c}")print(f"hint ={hint}")

关键参数解析

RSA模数: 2048位（看似安全）

公钥指数e: 101位素数

泄露信息: dp的高841位（dp = e⁻¹ mod (p-1)）

未知部分: 仅180位

0 ≤ x < 2^180(约1.5×10^54种可能)

1 ≤ k < e(约10^30种可能)

F(x,k) = A + e * x + k能被p整除

x < 2^180 ≪ 2^1024 ≈ p

k < e ≪ p

构造格基：

LLL算法：寻找格中的短向量

提取解：从短向量中恢复x和k

边信道攻击：

时序攻击：通过测量计算时间获取部分信息

功耗分析：通过分析功耗模式推断密钥位

电磁辐射：捕获设备发出的电磁信号

实现漏洞：

缓冲区溢出：意外泄露内存内容

Heartbleed类漏洞：读取服务器内存

错误的随机数生成：产生可预测的模式

物理攻击：

故障注入：故意制造计算错误

电压分析：通过改变电压获取信息

探针攻击：直接访问芯片内部

2008年：研究人员展示了如何通过部分密钥恢复攻击RSA

2012年：Heartbleed漏洞导致大量私钥泄露

2017年：ROCA漏洞影响RSA密钥生成

避免计算和存储dp、dq等CRT参数

实施严格的内存保护机制

及时清理敏感数据

硬件安全模块(HSM)保护密钥

定期密钥轮换

实施访问控制和审计

监控异常行为

代码安全审计

渗透测试

密码学实现审查

侧信道攻击防护评估

数学特性：dp比d更小，更容易构造多项式

CRT实现：实际RSA优化中确实会使用dp

攻击难度：提供了更精确的数学关系

Shor算法：可以完全破解RSA

后量子密码学：正在开发新的加密方案

格基密码学：既是攻击工具也是防御手段

经典论文：Coppersmith, D. (1996) “Finding small roots”

推荐书籍：《 Handbook of Applied Cryptography》

在线课程：Coursera密码学课程

实践平台：CTFtime、Hack The Box


```
# 看似正常的RSA实现，却隐藏着致命漏洞fromCrypto.Util.numberimport*fromencimportflagm = bytes_to_long(flag)p,q,e = getPrime(1024),getPrime(1024),getPrime(101)n = p*qtemp = gmpy2.invert(e,p-1) # 计算dp = e^(-1) mod (p-1)c = pow(m,e,n)hint = temp>>180# 致命的一行：泄露dp的高位！print(f"e ={e}")print(f"n ={n}")print(f"c ={c}")print(f"hint ={hint}")
```



```
e * d ≡ 1 (mod φ(n))其中 φ(n) = (p-1)(q-1)
```



```
dp = d mod (p-1) = e^(-1) mod (p-1)
```



```
e * dp ≡ 1 (mod p-1)
```



```
e * dp - 1 = k * (p-1) -- 关键公式！
```



```
e * dp + k ≡ 1 (mod p)e * dp + k - 1 ≡ 0 (mod p)
```



```
dp = hint * 2^180 + x其中 0 ≤ x < 2^180
```



```
e * (hint * 2^180 + x) - 1 = k * (p-1)
```



```
F(x,k) = A + e * x + k ≡ 0 (mod p)其中 A = e * hint * 2^180
```



```
[2^180, 0, A][ 0, e, e][ 0, 0, n]
```



```
# 完整的SageMath攻击实现fromsage.allimport*# 题目参数e =1915595112993511209389477484497n =12058282950596489853905564906853910576358068658769384729579819801721022283769030646360180235232443948894906791062870193314816321865741998147649422414431603039299616924238070704766273248012723702232534461910351418959616424998310622248291946154911467931964165973880496792299684212854214808779137819098357856373383337861864983040851365040402759759347175336660743115085194245075677724908400670513472707204162448675189436121439485901172477676082718531655089758822272217352755724670977397896215535981617949681898003148122723643223872440304852939317937912373577272644460885574430666002498233608150431820264832747326321450951c =5408361909232088411927098437148101161537011991636129516591281515719880372902772811801912955227544956928232819204513431590526561344301881618680646725398384396780493500649993257687034790300731922993696656726802653808160527651979428360536351980573727547243033796256983447267916371027899350378727589926205722216229710593828255704443872984334145124355391164297338618851078271620401852146006797653957299047860900048265940437555113706268887718422744645438627302494160620008862694047022773311552492738928266138774813855752781598514642890074854185464896060598268009621985230517465300289580941739719020511078726263797913582399hint =10818795142327948869191775315599184514916408553660572070587057895748317442312635789407391509205135808872509326739583930473478654752295542349813847128992385262182771143444612586369461112374487380427668276692719788567075889405245844775441364204657098142930# 攻击开始s =180X_bound = Integer(1) << s # 2^180Y_bound = eA = e * hint * (Integer(1) << s)# 构造多项式R.<X,Y> = PolynomialRing(ZZ)F = A + e*X + Y # F(x,k) ≡ 0 (mod p)# 变量缩放（让搜索空间变成单位量级）F_scaled = F(X = X_bound*X, Y = Y_bound*Y)# 构造多项式簇polys = []m =3# 经验值：3~5通常足够foriinrange(m+1): polys.append(F_scaled * (X**i)) polys.append(n * (X**i)) polys.append(F_scaled * (Y**i)) polys.append(n * (Y**i))# LLL算法找短向量mons = sorted({monforginpolysformoning.monomials()}, key=lambdamon: (mon.degree(), mon.degree(X)))M = Matrix(ZZ, [[g.monomial_coefficient(mon)formoninmons]forginpolys])Mred = M.LLL()# 从短向量中提取小根cands = []forrinMred.rows()[:10]: poly = sum(ZZ(r[i]) * mons[i]foriinrange(len(mons))) poly = poly(X = X / X_bound, Y = Y / Y_bound) cands.append(poly)# 使用resultant消元求解root_x =Noneforiinrange(len(cands)): forjinrange(i+1, len(cands)): res = cands[i].resultant(cands[j], Y).primitive_part() forxr, multinres.roots(ZZ): if0<= xr < X_bound: root_x = int(xr) break ifroot_xisnotNone: break ifroot_xisnotNone: break# 恢复kk =Noneforgincands: g1 = g(X = root_x) ifnotg1.is_constant(): foryr, multing1.roots(ZZ): k_candidate = int(yr) * int(Y_bound) if0< k_candidate < Y_bound: k = k_candidate break ifkisnotNone: break# 恢复私钥并解密p = gcd(A + e*root_x + k, n)q = n // pphi = (p-1)*(q-1)d = inverse_mod(e, phi)m = pow(c, d, n)flag = Integer(m).to_bytes((m.nbits()+7)//8,'big')print("攻击成功！")print(f"p ={p}")print(f"flag ={flag}")
```



```
攻击成功！p = 165459963496095383138895428904171454952248628537893256724281704284flag = b'LitCTF{03ecda15d1a89b06454c6050c1bd489f}'
```



```
原始dp：约1024位泄露hint：约841位未知部分：180位泄露比例：82.4%
```



```
2^180 ≈ 1.5×10^542^1024 ≈ 1.8×10^308比例约为2^-844
```



```
暴力搜索：O(2^281) ≈ 10^84 - 不可行格攻击：O(log^3 n) - 可行
```



```
# 推荐做法：使用标准库而不是自定义实现fromcryptography.hazmat.primitives.asymmetricimportrsa, paddingfromcryptography.hazmat.primitivesimporthashes# 生成密钥private_key = rsa.generate_private_key( public_exponent=65537, key_size=2048,)# 加密ciphertext = public_key.encrypt( message, padding.OAEP( mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None ))
```
