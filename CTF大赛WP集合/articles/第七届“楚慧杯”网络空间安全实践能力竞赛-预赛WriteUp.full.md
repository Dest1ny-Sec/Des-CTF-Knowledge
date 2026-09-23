---
title: 第七届"楚慧杯"网络空间安全实践能力竞赛-预赛WriteUp
contest: 第七届楚慧杯预赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags:
- 楚慧杯预赛
- mobile/misc/crypt
- AES解密
- VeraCrypt容器
- BitLocker加密卷
- stegsolve LSB
- passware
- CRC改高度
attack_chain: mobile:level_one(直接看)→level_up AES解密→crypt:VeraCrypt容器从jpg FFD9后提取→secret:BitLocker+改图片高度+stegsolve→pocky:hex写新文件
key_payload: flag{380605c6-7123-4f71-b573-601e8c4457b4};flag{6b1df900-1284-11ed-9fa7-5405dbe5e745};flag{4ba7689c6dee7749403380b11c416de6};flag{b6aa5b40559fc9762918cd32f5f6bd0f};password1=OXi password2=ChaiYan;620224-121649-497585-220572-660704-152383-484957-174713
one_liner: 第七届楚慧杯预赛：mobile AES+misc VeraCrypt+BitLocker+stegsolve+改CRC
lesson: 综合取证常用：FFD9后藏文件+改图片高度+BitLocker密码恢复+stegsolve提取
quality: medium
full_path: 第七届“楚慧杯”网络空间安全实践能力竞赛-预赛WriteUp.full.md
meta_path: 第七届“楚慧杯”网络空间安全实践能力竞赛-预赛WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第七届"楚慧杯"网络空间安全实践能力竞赛-预赛WriteUp。第七届楚慧杯预赛：mobile AES+misc VeraCrypt+BitLocker+stegsolve+改CRC。经验：综合取证常用：FFD9后藏文件+改图片高度+BitLocker密码恢复+stegsolve提取
category: misc
subcategory: misc_other
tools_used:
- Stegsolve
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/106699.html
reasoning_chain:
- 触发点：mobile level_one 直接读、level_up AES 解密→假设：常规编码
- 动作：读取 APK 字符串 + AES decrypt(已知 key/iv)→观察：拿到 flag2
- 假设：misc crypt 是 VeraCrypt 容器→动作：jpg 文件 FFD9 后另存为 .vc →观察：VeraCrypt 挂载
- 假设：资源管理器看不到→用 X-Ways 打开容器→观察：找到 flag3
- 假设：secret 是 BitLocker 加密卷→动作：改图片 CRC 错误的高度还原→观察：拿到 password1=OXi
- 假设：stegsolve 找 LSB 隐藏数据→动作：提取 password2=ChaiYan →观察：组合密钥
- 动作：passware 跑 OXiChaiYan 出 recovery key→观察：解密 BitLocker→拿到 flag4
failed_attempts:
- 试图 mount VeraCrypt 直接看 → 失败：资源管理器不显示文件
- 试图单一密码解 BitLocker → 失败：需要 password1+password2 组合
- 试图 stegsolve 一键还原 → 失败：要先改图片高度修复 CRC
key_observations:
- jpg 文件尾 FFD9 后常藏 VeraCrypt/zip/其他容器
- 改图片高度可绕过 CRC 错误显示完整画面，但隐藏数据暴露
- BitLocker 密码恢复可用 Passware Kit Forensic 跑字典
- 取证综合题常用组合：改图片高度 → stegsolve → 组合密码 → 挂载解密
prerequisites:
- VeraCrypt 容器挂载
- BitLocker 加密原理与恢复密钥
- stegsolve LSB 隐写提取
- PNG/JPG 高度修改 + CRC 校验
---
# 第七届“楚慧杯”网络空间安全实践能力竞赛-预赛WriteUp

> 原文: https://www.ctfiot.com/106699.html
> ID: 106699

mobile

level_one

[B@15db9742flag{380605c6-7123-4f71-b573- 601 e8c4457b4}

level_up

aes解密

结果为

flag{6b1df900-1284-11ed-9fa7-5405dbe5e745}

misc

crypt

图⽚备注提示了 VeraCrypt 容器

找到jpg⽂件尾 FFD9 ，将后⾯的内容另存为vc容器⽂件使⽤ VeraCrypt 挂载容器

资源管理器打开看不到⽂件，因此使⽤ X-Ways 打开

结果为

flag{4ba7689c6dee7749403380b11c416de6}

secret

镜像内⼀个bitlocker加密卷，⼀个有图⽚

图⽚crc不正确

修改图⽚⾼度后拿到password1 OXi

stegsolve找到password2 ChaiYan

passware跑出密钥

620224-121649-497585-220572-660704-152383-484957-174713 并⽣成解密后的镜像⽂件

或者取证⼤师使⽤密码 OXiChaiYan 直接解密

明⽂攻击

结果为

flag{b6aa5b40559fc9762918cd32f5f6bd0f}

pocky

将⽣成的hex⽤winhex写到新⽂件中

发现jpg尾部有压缩包数据

导出压缩包，⾥⾯有⼀张图和⼀个加密的压缩包

反转后补上⽂件头

拿到内容

签到

压缩包伪加密，直接⽤winzip⼀键修复即可

然后打开之后缩⼩，即可得到flag

结果为

 flag{b3b2cc1ffcaa12f61c6e61c519d1db2f}

web

python_easy

注册界⾯SSTI读config得到key

字节型直接⽤⽹上的项⽬改写⼀下，把key写死

伪造admin

修改cookie，访问flag

结果为

flag{3d12b41b-2c23-11ed-afc5-98fa9b8aee74}

sign

golang的ssti漏洞直接读flag name={{.FileRead “/tmp/flag”}}

结果为

flag{79d07778-2c32-11ed-b8ad-98fa9b8aee74}

⼩f的⽹站

Dir扫⼀下得到console

同时file存在绝对路径泄露

计算pin码

同时存在任意⽂件读取

读取⽤户名

读取机器id

读取mac地址

输⼊进⼊console得到flag

结果为

flag{8229a22e014cb1fb9d349ec485cf2895}

ez_pop

第⼀层：php反序列化

绕md5强⽐较

参考⽂章：

https://blog.csdn.net/LYJ20010728/article/details/114492485

shell.txt⽂件内容

shell.txt拖进fastcoll

⽣成两个⽂件内容不⼀样但md5值相同的⽂件，绕过if，进⼊include

构造pop链，本地跑

读到hint.php内容为⽂件上传的路径uploadkfc.php，访问/uploadkfc.php第⼆层：⽂件上传的绕过

利⽤之前反序列化⽂件包含的点读到有如下上传的限制：image/png类型检查和⽂件内容检查

Content-Type：image/pngfile_put_contents(shell.php,’xxx’)转base64绕过

结果为

flag{e0w91c4a-6e34-59fb-b8af-b1f9440b92b4}

crypto

RollingBase

爆破⼀下对于字典的旋转

结果为

flag{416d3b4a10a9925363a44275d8655c5d}

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！

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