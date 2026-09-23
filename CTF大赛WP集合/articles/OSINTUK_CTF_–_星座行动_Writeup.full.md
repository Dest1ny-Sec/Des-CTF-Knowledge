---
title: OSINTUK CTF – 星座行动 Writeup (UK 都市传说 OSINT)
contest: OSINTUK
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags:
- UK OSINT
- 都市传说
- 星座杀手
- Google Maps
- 维吉尼亚密码
- 虚无密码
- 报纸隐写
attack_chain: '|'
key_payload: '|'
one_liner: 'OSINTUK 星座行动: 5 道 UK 都市传说主题 OSINT (Albert Square + Big John''s + toyota island + 报纸 + 虚无密码)。'
lesson: '|'
quality: high
full_path: OSINTUK_CTF_–_星座行动_Writeup.full.md
meta_path: OSINTUK_CTF_–_星座行动_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'OSINTUK CTF – 星座行动 Writeup (UK 都市传说 OSINT)。OSINTUK 星座行动: 5 道 UK 都市传说主题 OSINT (Albert Square + Big John''s + toyota island + 报纸 + 虚无密码)。。经验：|'
category: misc
subcategory: misc_other
tools_used:
- John
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/295078.html
reasoning_chain:
- Developed in Darkness 题 → 触发点：宝丽来照片定位
- 假设：反向图片搜索 → 动作：Google 图片搜索 → 观察：曼彻斯特阿尔伯特广场
- Everton Park 题 → 触发点：图片含皇家利物浦大厦
- 动作：以皇家利物浦大厦为参照 → Google Maps 比对方位角
- 观察：后撤到所有建筑出现 → 假设：定位 everton park
- Big John's 题 → 触发点：A41 路牌 + Big John's 外卖
- 动作：Google 搜 Big John's + West Brom → 观察：找到地址 + 邮编
- Remote Access + TV Newspapers + 虚无密码 → 假设：报纸隐写 + 维吉尼亚密码
- 动作：维吉尼亚解报纸首字母 → 观察：得 flag
failed_attempts:
- 只靠 Google 反向搜 → 失败：需方位角 + 参照物定位
- 不解维吉尼亚 → 失败：报纸首字母是密文
- 只搜 Big John's → 失败：必须加 West Brom
key_observations:
- 阿尔伯特广场 / 利物浦大厦是 UK 著名地标
- Google Maps 方位角 + 参照物定位是 OSINT 进阶
- Big John's 是英国西布罗姆维奇外卖店
- 报纸隐写 + 维吉尼亚是 CTF 古典密码组合
- Royal Liver Building 是利物浦标志性建筑
prerequisites:
- Google Maps 高级使用
- UK 地理常识
- 维吉尼亚密码破解
- OSINT 报纸隐写思路
---
# OSINTUK CTF – 星座行动 Writeup

> 原文: https://www.ctfiot.com/295078.html
> ID: 295078

Developed in Darkness

“星座杀手”的出现，令全球执法部门陷入恐慌。数月来，当局一直处于高度戒备状态，试图破解这起横跨各大洲的残忍杀戮案。他的作案手法是什么？一系列发送给警方的线索，每一条都指向他作案的地点。

在他最近一次的连环杀人案中，凶手夺去了七条生命，但作案模式却令人费解。每个犯罪现场似乎都随机出现，散落在不同的城市。调查人员推测他是按照一份名单作案，但无人能破解他选择的逻辑。有人认为这些地点与星象有关，也有人认为线索中隐藏着更深层的含义，但尽管人们竭尽全力，仍然无人能解开其中的谜团。

现在，凶手似乎再次出现，并重新开始了作案仪式。 一张宝丽来照片被寄到了伦敦警察总部。作为此案的首席侦探，你必须追踪到这名凶手，并彻底阻止他的罪行。

宝丽来照片中那个正方形叫什么名字？

反向图片搜索找到具体位置：

“星座杀手”的恐怖统治仍在继续，他的信息也变得越来越阴森恐怖。在成功从宝丽来照片中锁定曼彻斯特的阿尔伯特广场后，杀手的嘲弄游戏愈演愈烈。执法部门感受到越来越大的压力，每一条线索都让他们离绝望的边缘更近一步。但杀手依然行踪诡秘，他精心设计的谜题几乎无法破解。

警局刚刚收到一条新线索，这次是一个 U 盘。U 盘里只有一张图片，其他所有内容都被清空了。

找到拍摄这张照片的公园。

图片中是能非常清晰地看到皇家利物浦大厦，所以我这里用它作为参照物，

根据皇家利物浦大厦的位置，谷歌地图中与图片的方位角度进行比对，

然后根据参照物一直往后退，直到图片所有参照物建筑出现，并且地势满足条件

答案就是everton park

The Last Meal

随着“星座杀手”的每一步行动，他的游戏都变得更加复杂。在从神秘线索中发现利物浦的地点后，杀手的挑衅仍在继续。每张照片都让线索变得更加阴暗、更加隐晦，仿佛杀手在挑战你，看你能否跟上他那扭曲的计划。现在，车站又收到了一张拍立得照片，这次显示的是一家普通餐厅的招牌。我们无从得知这张照片是否被篡改过，它很可能被修改过。但愿这里没有其他受害者。

找出宝丽来照片中快餐店的邮政编码。

右边的绿色牌子显示A41公路，左边最显眼的Big John’s外卖，直接将两个关键词在google搜索：

谷歌地球直接搜Big Johnsin West Brom

Remote Access

调查人员收到一个装有单张照片的 U 盘，没有任何附带信息。照片显示的是一个乡村公路交叉口，路标很少，很难立即确定其位置。

照片背景中，一座大型工业建筑占据了天际线。虽然道路本身提供的线索不多，但这种建筑特征并不常见，或许是解开照片拍摄地点之谜的关键。

凶手正是利用了旁观者能够识别出其他人会忽略的东西。

这张照片是在哪个岛屿上拍摄的？

把这几个方位标出来
Birmingham – A38 (S)

Willington – B5008

Nottingham – A50 (E)

Uttoxeter – A50 (W)

地面上的A50虽然模糊，但上面这些信息很容易知道在A50

现在在A50，A38在前面，目的地在Nottingham – A50的东边，顺着这条路可以定位到发电站位置

查看发电站确认最终位置，toyota island

Ghost Writer

调查人员截获了一篇报纸文章，据信是“星座杀手”故意篡改的。关键信息，很可能是地点名称，已被仔细删除。

尽管如此，文章本身却是真实的。它的语言、布局和上下文都完好无损，这表明仍然可以通过间接细节确定失窃地点。而且，奇怪的是，凶手在漫画背面写着“1931年万圣节”，这几乎是在嘲讽我们。

凶手以前也这样做过：去除显而易见的线索，只留下足够多的信息供仔细调查。

你的任务是确定文章最初指的是哪个城镇或地点。

文章中隐去了哪个地点？

懒得看了，费眼，直接跑ai

Character Witness

调查人员在最后一个犯罪现场找到了一张手写纸条。乍一看，这张纸条似乎毫无意义，只是一串串重复的字符，没有任何明显的结构。

分析人士认为，这张纸条是故意加密的，加密方法虽然简单，但并不显眼。根据以往的趋势，一旦解码，信息应该会指向一个特定的地点。

凶手可能已经在之前的线索中暗示了关键所在，只是我们不够细心。

这条信息透露了什么地点？

直接ai跑出来了，虚无密码:

The Big Picture

这是最终决战。

最后一张图像已经出现，这张图像没有任何明显的线索，似乎无法单独辨认。调查人员认为这是精心设计的。凶手希望他的作案手法现在能被识破。或许之前的作案地点并非随机出现，它们可能构成一个精心设计的序列。只有识别出这个结构，才能确定最终的作案地点。

这不再是寻找线索的问题，而是预测凶手的下一步行动的问题。

“星座杀手”下一个作案地点会是哪条街？

这就有点rz了，我还以为我们熟悉的十二星座，对半天没对上

吗的阴间题，不做了，睡觉回家过年

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