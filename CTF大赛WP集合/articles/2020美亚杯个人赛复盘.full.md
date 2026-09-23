---
title: 2020 美亚杯个人赛复盘
contest: 2020 美亚杯 (Meiya Cup) 个人赛
year: 2020
difficulty: medium
vuln_type:
- forensic_disk
- forensic_memory
- misc_unknown
tags:
- 美亚杯
- 笔记本取证
- 手机取证
- USB取证
- 邮件取证
- WhatsApp
- 信用卡诈骗
- 中文取证
- NTFS
- exif
- Registry
- IndexerVolumeGuid
attack_chain:
- 笔记本 SHA-1 哈希验证
- 查 OS / SID / 最后登录 / 时区
- 找最常用浏览器 + 历史 + 版本
- 受害人在 shyl1211@mtzh.gow.tw 邮箱 / 信用卡号 / CSC
- USB IndexerVolumeGuid 时间戳找最后插入时间
- ZIP SHA-256 + 修改时间 + 解压内容
- WhatsApp 聊天 + 群组 Big Big Club 创建时间
- Bob/Cole/AP 邮件关联诈骗主脑
- USB 隐藏程序（VeraCrypt/KeePass 类）找密码
- WiFi MAC + 钱包地址 + media_wa_type 调查
key_payload: shy1211@mtzh.gow.tw + 信用卡号 + ZIP SHA-256
one_liner: 美亚杯经典诈骗案：笔记本+手机+USB 三件套 61 问取证
lesson: 中文 CTF 取证赛最大特色是 60+ 问答题，每问 1-3 分，工具链要全（FTK/X-Ways/Autopsy/火眼）
quality: high
full_path: 2020美亚杯个人赛复盘.full.md
meta_path: 2020美亚杯个人赛复盘.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2020 美亚杯个人赛复盘。美亚杯经典诈骗案：笔记本+手机+USB 三件套 61 问取证。关键路径：笔记本 SHA-1 哈希验证 → 查 OS / SID / 最后登录 / 时区 → 找最常用浏览器 + 历史 + 版本。经验：中文 CTF 取证赛最大特色是 60+ 问答题，每问 1-3 分，工具链要全（FTK/X-Ways/Autopsy/火眼...
category: forensic
subcategory: disk_forensics
subcategories:
- disk_forensics
- memory_forensics
- misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/63974.html
reasoning_chain:
- '[触发点] 61 道问答题涉及 SHA-1/OS/SID/USB 时间/邮箱账号/WhatsApp →假设：单题分1-3 分的取证海，需要三件套全做 / [假设] 用 FTK/X-Ways/Autopsy + 火眼取证套装分头扫不同证据类型 → [动作] mount E01镜像 → hash SHA-1 验证 / [观察] 拿到镜像指纹，对应题 1 / [下一步] Registry 解 OS/SID，浏览器历史取 OS、版本'
- '[触发点] 题目提 ''Ho PCKYI 邮箱 shy1211@mtzh.gow.tw'' → 假设：受害人是邮件骗子 → [动作] 搜邮件数据库 → [观察] 找到信用卡号 + CSC / [下一步] 转去 USB IndexerVolumeGuid 时间戳'
- '[触发点] IndexerVolumeGuid 在 USB 插入时写 → 假设：此时间即最后插入 → [动作] 读 Registry SYSTEM\MountedDevices / [观察] 拿到本地时间 / [下一步] 解压 ZIP 算 SHA-256 + 发票 SHA-256'
- '[触发点] 看到 ''WhatsApp Big Big Club 群组'' → 假设：群组创建时间是主脑 → [动作] 解 WhatsApp msgstore.db / [观察] 拿到创建时间 + 主脑命名 / [下一步] 关联 Bob/Cole/AP 三方邮件'
failed_attempts:
- 试图只装 One 看 UTXO → 失败：61 问覆盖3 件套不能脱节
- 试图直接用 R-Studio 扫邮件 → 失败：邮件软件版本有自定义 DB 格式
key_observations:
- 中文取证赛 60+ 问答题，单题 1-3 分，要工具链全（FTK/X-Ways/Autopsy/火眼）
- IndexerVolumeGuid 是 Windows USB 插入证据的关键文件
- WhatsApp msgstore.db + Crypt12 是手机取证切入点
- 邮件主脑追踪要拉三方关系（Alice ↔ AP ↔ Bob/Cole）
prerequisites:
- FTK/X-Ways Imager 基础使用
- Windows Registry / NTFS 底层结构认知
- Android 取证（ADB / img解析 / WhatsApp Crypt12）
- 邮件取证基本流程（PST/OST/MBOX）
---
# 2020美亚杯个人赛复盘

> 原文: https://www.ctfiot.com/63974.html
> ID: 63974

1、Alice的笔记本计算机已成功被取证并制作成镜像(Forensic Image), 下列哪个是镜像的SHA-1哈希值?

2、Alice的笔记本计算机安装了哪个操作系统(Operating System)?

3、在Alice的笔记本, 创建用户帐户的SID是甚么？

4、在Alice的笔记本,用户的最后登录时间是甚么时候？(本地时间)

5、在Alice的笔记本,最后登录的用户名称是甚么？

6、Alice笔记本计算机的名称是甚么？

7、在Alice的笔记本, 最后登录的用户何时更改了Windows登录密码？（当地时间）

8、Alice笔记本计算机的时区是甚么？

9、在Alice的笔记本, OS分区的文件系统是甚么？

10、计算机上预设安装了甚么浏览器？

11、在Alice的笔记本,哪个是最常用的浏览器？

12、在Alice的笔记本, 最常用的浏览器是甚么版本？

13、在Alice的笔记本, Alice浏览了哪个在线商店的网站

14、在Alice的笔记本, 受害人的信用卡号是甚么?（Ho PCKYI-电子邮件：shy1211@mtzh.gow.tw）

15、在Alice的笔记本, 受害人的信用卡CSC号码是甚么（何PCKYI-电子邮件：shy1211@mtzh.gow.tw）

16、除了上述在USB 找出ZIP文件,请找出相同ZIP文件的路径？

17、ZIP文件的哈希值（SHA-256）是甚么？

18、ZIP文件的修改时间是多少?(当地时间)

19、USB驱动器在Alice笔记本计算机上的最后插入时间是何时？(当地时间)

IndexerVolumeGuid这个文件是在U盘插入时生成。

20、解压的ZIP文件内有哪些文件？

21、“ ZIP文件中发票的哈希值（SHA 256）是多少=发票（1）

名称：WhatsApp Image 2020-09-29 at 18.35.25.jpeg”

跳转到源文件

22、“ ZIP文件中发票的哈希值（SHA 256）是多少=发票（2）

名称：WhatsApp Image 2020-09-29 at 18.37.47.jpeg”

23、Alice笔记本计算机上安装了哪种电子邮件软件？

24、Alice笔记本计算机上的电子邮件软件的版本是甚么？

25、Alice笔记本计算机登录电子邮件软件的电子邮件帐户是甚么？

26、Alice在上述电子邮件对话中获得了哪些数据/文件？

27、该电子邮件的发信者的电子邮件地址是甚么？

28、上述已收的电子邮件, 发件人的IP地址是甚么？

29、在笔记本, Alice的电子邮件地址是甚么？

30、除了Alice，还有其他电子邮件地址与该骗局有关吗？

31、哪些人有AP和主脑之间的电子邮件记录？有文件传输吗？

32、在ZIP 文件中, 有多少受害人的信用卡数据被盗?

33、已被黑客盗用其信用卡资料购买的受害者是谁?

34、被盗用的内容是甚么？

35、Alice的手机型号是甚么？

36、Alice手机的操作系统版本是甚么？

37、Alice手机的总储存空间是多少?

38、在Alice 手机, IMG-20200929-WA0002的创建时间是甚么？(本地时间)

39、在Alice 手机,IMG-20200929-WA0004的创建时间是甚么？(本地时间)

40、IMG-20200929-WA0002和IMG-20200929-WA0004的元数据和相机型号是甚么？

41、在Alice 手机, 预设浏览器浏览历史记录的文件在哪里？

42、储存Chrome浏览历史记录的文件是甚么？

43、Alice手机的Whatsapp ID和账户名称是甚么？

44、与Bob和Cole的最后WhatsApp的时间是甚么？(本地时间)

45、主脑的名字是甚么？

46、Alice，Bob和Cole之间的WhatsApp群组的ID和名称是甚么?

47、哪一个表，显示了聊天群组“ Big Big Club”的创建时间？(本地时间)

48、聊天群组“ Big Big Club”是甚么时候创建的？(本地时间)

49、Alice是否曾经登陆whatsapp网站？如果有的话，她是在何时登入? 所用的是甚么浏览器？（提示：在移动取证图像上找到结果）(UTC +0)

50、Alice如何收到这笔钱？钱包地址是甚么？

51、“Deleted by the sender”的media_wa_type是甚么?

52、Alice手机的Wifi MAC地址是甚么？

用原数据搜索

53、Alice USB驱动器内的ZIP档案的密码是甚么? (某些字符被刻意用*遮盖)

54、Alice USB驱动器内的哪一个程序是用作储存秘密数据?

55、打开秘密讯息的密码是甚么? (某些字符被刻意用*遮盖)

56、USB驱动器内，其中一个档案的秘密讯息是甚么? (某些字符被刻意用*遮盖)

57、贴在笔记本计算器机上的密码有甚么用途?

从文件恢复安全信息

58、Alice USB驱动器内的档案有甚么种类?

59、Alice USB驱动器的哈希值（SHA-256）是甚么？

60、在USB驱动器中找到的ZIP文件（Downloads.7z），它的哈希值（SHA-256）是甚么？

61、在Alice的USB内, ZIP文件的最后修改时间是？

原文始发于微信公众号（Th0r安全）：2020美亚杯个人赛复盘

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