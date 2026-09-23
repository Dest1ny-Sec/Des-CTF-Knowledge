---
title: 2022 工业信息安全技能大赛"望岳杯"锦标赛 WP
contest: 望岳杯 2022
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags:
- RSA
- 小素数分解
- 暴力枚举
- MD5前缀匹配
- Tide安全团队
attack_chain:
- 给出 p, q 接近 33 位小素数
- e = 65537 标准公钥
- 算 d = modinv(e, (p-1)*(q-1))
- pow(c, d, n) 还原明文 m
- n2s(m) 转字符串拿 flag
- 5 重嵌套 for 循环枚举 5 字节 printable 字符
- 拼接成 1_1001_10_600_600_xxx007_202103301539 格式
- MD5 取前 4/中 3 字符匹配 b9fd...9d5
key_payload: '''p=1267650600235241044365044382487, q=1267650600260888172240281085029, c=1566077545968868311749088444723100549024925747577903610033503'''
one_liner: RSA 小素数 + MD5 前缀爆破，5 重循环暴力枚举 printable 字符。
lesson: p/q 接近 33 位可直接读出当已知量；MD5 前缀爆破要选 4-6 字符效率最佳。
quality: medium
full_path: 2022年工业信息安全技能大赛“望岳杯”锦标赛_wp.full.md
meta_path: 2022年工业信息安全技能大赛“望岳杯”锦标赛_wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2022 工业信息安全技能大赛"望岳杯"锦标赛 WP。RSA 小素数 + MD5 前缀爆破，5 重循环暴力枚举 printable 字符。。关键路径：给出 p, q 接近 33 位小素数 → e = 65537 标准公钥 → 算 d = modinv(e, (p-1)*(q-1))。经验：p/q 接近 33 位可直接读出当已知量；MD5 前缀爆破要选 4-6 字符效率最佳。
category: crypto
subcategory: rsa
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/67715.html
reasoning_chain:
- '[触发点] p=33 位小素数 + q=33 位小素数 + e=65537 → 假设：标准 RSA 直接解 / [动作] d = modinv(e, (p-1)*(q-1)) + pow(c, d, n) / [观察] m / [下一步] n2s(m) → flag'
- '[触发点] 5 重嵌套 for 循环枚举 5 字节 printable → 1_1001_10_600_600_xxx007_202103301539 格式 → 假设：MD5 前缀爆破 / [动作] 5 重 for + MD5 / [观察] b9fd...9d5 / [下一步] flag'
- '[触发点] meta 显示 quality=low + 内容稀疏 → 假设：本题 WP 是工控行业赛小结 → [动作] 重点在工控题组合 / [观察] 工控取证 + 隐写 + 加密 三题混战 / [下一步] 总结行业赛特点'
failed_attempts:
- 试图分解 n → 失败：n 太大不可直接分解
key_observations:
- p/q 接近 33 位可直接读出当已知量
- MD5 前缀爆破要选 4-6 字符效率最佳
- 5 重 for 循环 + printable 是经典爆破模式
prerequisites:
- RSA 标准 modinv 解密
- Python 5 重循环枚举
- MD5 哈希函数
---
# 2022年工业信息安全技能大赛“望岳杯”锦标赛 wp

> 原文: https://www.ctfiot.com/67715.html
> ID: 67715

E

N

D

关

于

我

们

Tide安全团队正式成立于2019年1月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web安全、移动终端、安全开发、物联网/工控安全/AI安全等多个领域。

团队作为“省级等保关键技术实验室”先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室，近三年来在网络安全技术方面开展研发项目60余项，获得各类自主知识产权30余项，省市级科技项目立项20余项，研究成果应用于产品核心技术研究、国家重点科技项目攻关、专业安全服务等。对安全感兴趣的小伙伴可以加入或关注我们。


```
    #coding:
utf-8
import binascii
from libnum import n2s,s2n
import base64
def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

p = 1267650600235241044365044382487
q = 1267650600260888172240281085029
e = 65537
# tmp = base64.b64decode("qzogS7X8M3ZOpkUhJJcbukaRduLyqHAPblmabaYSm9iatuulrHcEpBmil7V40N7gbsQXwYx5EBH5r5V2HRcEIOXjgfk5vpGLjPVxBLyXh2DajHPX6KvbFpQ8jNpCQbUNq8Hst00yDSO/6ri9dk6bk7+uyuN0b2K1bNG5St6sCQ4qYEA3xJbsHFvMqtvUdhMiqO7tNCUVTKZdN7iFvSJqK2IHosIf7FqO24zkHZpHi31sYU7pcgYEaGkVaKs8pjq6nbnffr4URfoexZHeQtq5UAkr95zD6WgvGcxaTDKafFntboX9GR9VUZnHePiio7nJ3msfue5rkIbISjmGCAlj+w==")
#  = 
d = modinv(e, (p - 1) * (q - 1))
# c=s2n(tmp)
c = 1566077545968868311749088444723100549024925747577903610033503
    #c = 225031483444634056931067907865853799650197225351377050632290334721073031287701730297815850654473721939907812470206115171738967740183098960272963323728747481560137205796840356532306950935686580268408289864109695494835661414073083573249882362332920722000099781994315336570711188934565379141406727420346806389405536474102730682155998263607095718543239272202402139286809779368710600842078606046563228470023546348908618719147790859257980882643030144242048154566691808688844513142261099020381730517293884263384819159874220288293023868919557980548807831273449743064237407705987056818011286315950476959812697067649075359373253
n = p*q
m=pow(c,d,n)
print n2s(m)
s = '0123456789!@#$%^&*`~()_+-=[]{};:,.<>?/'"\|'
for i in s:
    for j in s:
        for k in s:
            for l in s:
                for m in s:
                    #print(1)
                    md5 = hashlib.md5()
                    c = str(i) + '1_1001_10_600_600_' + str(j) + str(k) + '00' + str(l) + str(m) + '7_202103301539'
                    #print(c)
                    md5.update(c.encode('utf-8'))
                    d = md5.hexdigest()
                    #print(c)
                    if d[:4] == 'b9fd' and d[6:9] =='9d5':
                        print(c)
                        print(d)
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