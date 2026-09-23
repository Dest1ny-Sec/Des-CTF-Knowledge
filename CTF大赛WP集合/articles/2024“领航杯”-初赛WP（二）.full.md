---
title: 2024"领航杯"-初赛WP（二）
contest: 领航杯
year: 2024
difficulty: medium
vuln_type:
- lattice
- crypto_rsa
- web_unknown
- auth_bypass
- misc_unknown
tags:
- RSA p^4+tp
- Amm开方
- 身份证号校验和
- web sum字符密码
- ACXI 注册绕过
- AES加密
attack_chain: '1. CRYPTO_Evaluate: p=p^4+tp (512-bit随机p+20-bit小扰动tp) → AMM 开方 (p^4 mod n) 拿 p / 2. MISC-veee: 1W 个身份证号 → 提取校验位不对的 → 转 ASCII → base64 隐写 / 3. WEB_ACXI_: 注册 test/123456 → 服务器加和 ord(c) 当 hash → 爆破 0x202f5 = 131829 → 多个 7 字符密码 sum 匹配 0x0202f5 → 绕过 admin 校验'
key_payload: 'p, tp = genPrime()  # p^4 + tp 素数 ; AMM(p^4 mod n) 拿 p ; this_is_pwd_j71nas2 ; 0x202f5 = 131829 ; sum(ord(c) for c in ''test123456'') = 0x2f5'
one_liner: RSA p^4+tp AMM 开方 + 身份证校验和提取 + web sum 哈希碰撞。
lesson: p^4+tp 模数可对 p^4 用 AMM 开方求 p 候选；web 弱哈希常是 sum(ord) 单值校验。
quality: medium
full_path: 2024“领航杯”-初赛WP（二）.full.md
meta_path: 2024“领航杯”-初赛WP（二）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024"领航杯"-初赛WP（二）。RSA p^4+tp AMM 开方 + 身份证校验和提取 + web sum 哈希碰撞。。经验：p^4+tp 模数可对 p^4 用 AMM 开方求 p 候选；web 弱哈希常是 sum(ord) 单值校验。
category: crypto
subcategory: lattice
subcategories:
- lattice
- rsa
- web_other
- logic
- misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/219953.html
reasoning_chain:
- 触发点：CRYPTO_Evaluate 给 n = p*q, p=p^4+tp q=q^4+tq, tp/tq 各 20bit 小扰动 → 假设：AMM 开方能恢复 p
- 动作：算 p^4 mod n + AMM(p^4 mod n) 候选 → 观察：得到真实 p（含 20bit 扰动）
- 下一步：算 d=inverse(e,phi) 解密出 flag
- 触发点：MISC-veee 1W 个身份证号清单 → 假设：部分身份证校验位异常 → 动作：verify_id 检查每条
- 观察：异常身份证最后一位有误 → 动作：提取最后一位组合 → 746869735f69735f7077645f6a37316e617332
- 动作：hex2bytes → 'this_is_pwd_j71nas2' →观察：拿到密码
- 触发点：WEB_ACXI 注册 test/123456 提示 admin 才能拿 flag → 假设：登录逻辑弱校验
- 动作：读 cookie 校验逻辑 → 观察：服务器算 sum(ord(c) for c in pwd) 当 hash 比对
- 假设：只要 ord 和匹配 0x202f5 = 131829 即可 → 动作：爆破多组 7 字符密码组合满足 sum
- 观察：绕过 admin 校验，拿到 flag
failed_attempts:
- 试图直接登录 admin/admin → 失败：账号不存在
- 试图对密码做 MD5 爆破 → 失败：服务端只对 ord 求和不做哈希
- 试图遍历 ASCII 128字符直接硬碰撞 → 失败：要求恰好 7 字符特定 sum 值
key_observations:
- RSA p^4+tp 形式：对 p^4 用 AMM 算法即可解 p候选（小扰动不影响开方主分支）
- 身份证 GB11643 加权 [7,9,10,5,8,4,2] % 11 + check_codes 是固定校验
- Web 弱哈希常是 sum(ord) 单值校验，可通过约束求解找到等值密码组合
- python re.search 加 lambda 比 sed/awk 灵活提取异常字符
prerequisites:
- SageMath AMM 开方算法
- Python re 正则匹配与 lambda 应用
- Web session/cookie 伪造基础
- ASCII 字符 ord 求和爆破（约束满足）
---
# 2024“领航杯”-初赛WP（二）

> 原文: https://www.ctfiot.com/219953.html
> ID: 219953

点击上方蓝字关注我们

郑重说明

数字人才创研院秉承探究学习与交流知识‍‍的原则，所有发布的技术文章仅供参考，目的在于助力你获得更多知识；与此同时，让我们共同遵守《网络安全法》，未经授权请勿利用文章中的技术内容对任何计算机系统进行非授权操作，否则对他人或单位而造成的直接或间接后果或损失，均由使用者本人负责。

   公众号发表的文章如有涉及您的侵权，烦请私信联系告知，我们会立即删除并对您表达最诚挚的歉意！感谢您的理解！‍

Purpose of recommendation

推荐观点

赛事的开展不仅给广大参赛学生提供了网络安全实战平台，同时也搭建了发现人才和人才交流的平台。   竞技赛场，你追我赶，各参赛选手以竞赛活动为契机，以赛促学、以赛促训，畅享不一样“饕餮盛宴”的竞赛。   知己知彼，百战百胜，小编分享官方WriteUp，旨在让大家了解赛事赛题的难度变化与知识范畴，发现团队薄弱之处，提升团队技术能力。   推荐指数：★★★★★

01

CRYPTO_Evaluate

试题代码如下：

# -*- coding: utf-8 -*-from Crypto.Util.number import bytes_to_long
from secret import flagimport randomimport gmpy2 def genPrime():    while True:        p = random.getrandbits(512)        tp = random.getrandbits(20)        if gmpy2.is_prime(p**4 + tp):            return p**4 + tp, tp p, tp = genPrime()q, tq = genPrime()m = bytes_to_long(flag)e = 0x10001n = p*qc = pow(m, e, n)print("n = %s" % n)print("e = %s" % e)print("c = %s" % c)print("tp = %s" % tp)print("tq = %s" % tq)

02

MISC-veee

1、打开附件文件，看到2个文件，一个没有后缀，一个为文本文件

2、先看文本文件，发现为一组1W个的身份证号码清单，粗略检查后发现部分身份号码不正确，存在异常字符a

3、先使用python脚本提取错误的身份证号码，进行二次分析，分析发现最后一位似乎有问题，改下代码提取最后一位并组合

import randomimport refrom datetime import datetime, timedelta#需引入constant.py文件import constant as const
class IdNumber(str):    def __init__(self, id_number):        super(IdNumber, self).__init__()        self.id = id_number        self.area_id = int(self.id[0:6])        self.birth_year = int(self.id[6:10])        self.birth_month = int(self.id[10:12])        self.birth_day = int(self.id[12:14])    def get_area_name(self):        """根据区域编号取出区域名称"""        return const.AREA_INFO[self.area_id]    def get_birthday(self):        """通过身份证号获取出生日期"""        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)    def get_age(self):        """通过身份证号获取年龄"""        now = (datetime.now() + timedelta(days=1))        year, month, day = now.year, now.month, now.day        if year == self.birth_year:            return 0        else:            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):                return year - self.birth_year - 1            else:                return year - self.birth_year    def get_sex(self):        """通过身份证号获取性别， 女生：0，男生：1"""        return int(self.id[16:17]) % 2    def get_check_digit(self):        """通过身份证号获取校验码"""        check_sum = 0        for i in range(0, 17):            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])        check_digit = (12 - (check_sum % 11)) % 11        return check_digit if check_digit < 10 else 'X'    @classmethod    def verify_id(cls, id_number):        """校验身份证是否正确"""        if re.match(const.ID_NUMBER_18_REGEX, id_number):            check_digit = cls(id_number).get_check_digit()            return str(check_digit) == id_number[-1]        else:            return bool(re.match(const.ID_NUMBER_15_REGEX, id_number))
def check():    with open('sfz.txt', 'r', encoding='utf-8') as file:        for line in file:            value = line.strip()            if  IdNumber.verify_

746869735f69735f7077645f6a37316e617332this_is_pwd_j71nas2

03

RE_easystd

04

WEB_ACXI_

访问网站就是简单的登录注册界面。可以注册个账号登录（test/123456），提示需要admin才能拿到flag。

hex(773094245109)0xb4000202f5hex(244813267701)0x39000202f5

0x202f5 = 131829

hex(721554637612)0xa80002032c

hix = 0                                for c in 'test123456': hix += ord(c)       hex(hix)
# 0x2f5 hix = 0                                for c in 'test1234567': hix += ord(c)       hex(hix)                               # 0x32c

0x0202f5   ^

0x01????

如果喜欢，敬请关注，后期内容更精彩！

END


```
# -*- coding: utf-8 -*-from Crypto.Util.number import bytes_to_long
from secret import flagimport randomimport gmpy2 def genPrime():    while True:        p = random.getrandbits(512)        tp = random.getrandbits(20)        if gmpy2.is_prime(p**4 + tp):            return p**4 + tp, tp p, tp = genPrime()q, tq = genPrime()m = bytes_to_long(flag)e = 0x10001n = p*qc = pow(m, e, n)print("n = %s" % n)print("e = %s" % e)print("c = %s" % c)print("tp = %s" % tp)print("tq = %s" % tq)
import randomimport refrom datetime import datetime, timedelta#需引入constant.py文件import constant as const
class IdNumber(str):    def __init__(self, id_number):        super(IdNumber, self).__init__()        self.id = id_number        self.area_id = int(self.id[0:6])        self.birth_year = int(self.id[6:10])        self.birth_month = int(self.id[10:12])        self.birth_day = int(self.id[12:14])    def get_area_name(self):        """根据区域编号取出区域名称"""        return const.AREA_INFO[self.area_id]    def get_birthday(self):        """通过身份证号获取出生日期"""        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)    def get_age(self):        """通过身份证号获取年龄"""        now = (datetime.now() + timedelta(days=1))        year, month, day = now.year, now.month, now.day        if year == self.birth_year:            return 0        else:            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):                return year - self.birth_year - 1            else:                return year - self.birth_year    def get_sex(self):        """通过身份证号获取性别， 女生：0，男生：1"""        return int(self.id[16:17]) % 2    def get_check_digit(self):        """通过身份证号获取校验码"""        check_sum = 0        for i in range(0, 17):            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])        check_digit = (12 - (check_sum % 11)) % 11        return check_digit if check_digit < 10 else 'X'    @classmethod    def verify_id(cls, id_number):        """校验身份证是否正确"""        if re.match(const.ID_NUMBER_18_REGEX, id_number):            check_digit = cls(id_number).get_check_digit()            return str(check_digit) == id_number[-1]        else:            return bool(re.match(const.ID_NUMBER_15_REGEX, id_number))
def check():    with open('sfz.txt', 'r', encoding='utf-8') as file:        for line in file:            value = line.strip()            if  IdNumber.verify_
746869735f69735f7077645f6a37316e617332this_is_pwd_j71nas2
hex(773094245109)0xb4000202f5hex(244813267701)0x39000202f5
0x202f5 = 131829
hex(721554637612)0xa80002032c
hix = 0                                for c in 'test123456': hix += ord(c)       hex(hix)
# 0x2f5 hix = 0                                for c in 'test1234567': hix += ord(c)       hex(hix)                               # 0x32c
0x0202f5   ^
0x01????
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