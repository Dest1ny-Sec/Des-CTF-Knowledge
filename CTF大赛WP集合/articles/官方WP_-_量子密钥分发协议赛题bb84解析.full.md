---
title: 量子密钥分发协议赛题bb84官方WP - 第十六届信安国赛
contest: 第十六届全国大学生信息安全竞赛(信安国赛)初赛 + 伽玛实验场
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags:
- 量子密钥分发
- BB84协议
- 偏振编码
- 一次一密
- 流密码
- 异或
- UTF-8
- 线性同余
- 安徽问天量子
- 香农熵
- 误码率
- 100%纠错
- EPC1-APD
attack_chain: 读csv获Alice随机序列EPC1+Bob探测器APD1-APD4 → 有效探测(APD仅1个为1) → 对基成功(EPC1=1/2→APD1/2为1;EPC1=3/4→APD3/4为1) → 误码筛(EPC1=1∧APD2=1等) → 误码率计算 → 100%纠错假设 → 线性同余(A=1709,B=2003,M=keyPool.length,indexBegin=17)索引取安全密钥 → 异或解密hex密文 → UTF-8编码得明文
key_payload: BB84偏振协议 + 100%纠错 + 一次一密 + 流密码异或 + 线性同余(A=1709,B=2003)
one_liner: 安徽问天量子设计信安国赛BB84量子密钥分发赛题:偏振对基+误码筛+线性同余取密钥+流密码异或。
lesson: BB84协议:4种偏振态(0°/45°/90°/135°=H/V/±/+),Alice随机选基+随机比特,选错基时误码;有效探测=仅1个APD响应;对基成功条件:EPC1=1/2用APD1/2,EPC1=3/4用APD3/4;100%纠错假设简化算法;一次一密=密钥长度=明文长度;流密码=异或;线性同余公式res=(A*index+B) % M;UTF-8编码最终明文。
quality: high
full_path: 官方WP_-_量子密钥分发协议赛题bb84解析.full.md
meta_path: 官方WP_-_量子密钥分发协议赛题bb84解析.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: 量子密钥分发协议赛题bb84官方WP - 第十六届信安国赛。安徽问天量子设计信安国赛BB84量子密钥分发赛题:偏振对基+误码筛+线性同余取密钥+流密码异或。。经验：BB84协议:4种偏振态(0°/45°/90°/135°=H/V/±/+),Alice随机选基+随机比特,选错基时误码;...
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/119468.html
reasoning_chain:
- 信安国赛 BB84 量子密钥分发：Alice 随机选基 + Bob 探测器 APD1-4 随机响应 → 触发点：标准 BB84 协议题型
- 读 csv 拿 Alice 偏振 EPC1（1/2/3/4 对应四种偏振态）+ Bob APD1-4 探测器响应 → 假设：API 仅 1 个 APD =1 才是有效探测 → 动作：过滤
- 对基成功条件：EPC1=1/2 → APD1/2 为 1；EPC1=3/4 → APD3/4 为 1 → 假设：错基 = 误码 → 动作：筛对基成功比特
- 对基后又筛除错配 → 误码率计算 → 假设：100% 纠错 → 动作：取全部对基比特为安全密钥池
- 线性同余公式 (A=1709, B=2003, M=keyPool.length, indexBegin=17)：key[(A*i+B) % M] → 假设：按公式逐索引取 → 动作：循环取密钥
- 异或解密 hex 密文 → UTF-8 编码 → flag
failed_attempts:
- 试图用所有 EPC1 + 所有 APD1 数据 → 失败：必须过滤 API 仅 1 个 =1 才有效
- 用错基比特参与密钥 → 失败：错基 = 误码需丢弃
- 线性同余指数从 0 开始 → 失败：indexBegin=17 必须按题面给的值
key_observations:
- BB84 协议核心：4 种偏振态（H/V/+/-）、选错基必然引入误码、对基成功的比特才安全
- 有效探测 = 仅 1 个 APD 响应（避免探测器同时触发歧义）
- 一次一密 = 密钥长度 = 明文长度 = XOR 解密
- 100% 纠错假设是入门级 BB84 题型常用简化
prerequisites:
- BB84 量子密钥分发协议流程
- Python csv 读写与 numpy 数据处理
- 线性同余 PRNG 公式理解
- 流密码 / 一次一密 / XOR 加密原理
---
# 官方WP | 量子密钥分发协议赛题bb84解析

> 原文: https://www.ctfiot.com/119468.html
> ID: 119468

编者荐语：

量子通信是一种运用量子力学原理来传输和加密信息的先进技术，其中的关键技术包含量子密钥分发。BB84协议是1984年首次提出来的量子密钥分发安全协议，它能够在不可靠的信道上为通信双方建立一个随机的密钥，从而保障信息的机密性和完整性。

本文分享了第十六届全国大学生信息安全竞赛初赛基于量子密钥分发协议而设计的bb84赛题的解析。

“bb84”赛题已部署在伽玛实验场，欢迎前去挑战。

BB84偏振协议解析

作者：安徽问天量子科技股份有限公司-量子信息教育创新平台产品团队
量子信息已经被《“十四五”国家信息化规划》视为重要的前沿领域之一，属于国家重点发展的具备引领新兴产业发展潜力的前沿技术。其中，量子密码和量子计算与网络空间安全有较紧密的关联，也为网络空间安全的发展提供新的机遇和挑战。量子密钥分发是量子密码研究中的重点。BB84协议于1984年提出，该协议是量子密钥技术发展的开端，是最经典也是当前广泛应用的协议，具有非常重要的意义。在本届大学生“国赛”初赛出一道量子信息相关的题目，也是为了让选手以比赛的这种方式，能了解到一些量子相关的知识和最新的进展。

BB84赛题要求选手快速熟悉BB84偏振协议流程，了解其有效探测、对基过程、安全密钥、误码率等相关知识。此外，选手还需掌握根据线性同余理论从已得到的安全密钥序列中，选取生成最终用于加密的安全密钥。

题目考察的是选手对基于BB84偏振编码协议的量子密钥分发技术原理的快速学习和理解，为了节省选手网上搜索相关知识的时间，便于选手更高效地学习BB84协议流程，我们提供了参考资料（参考资料.docx）以及配套的BB84偏振编码协议的web参考软件（Qsim-CTF.exe）。

根据参考资料，解析csv文件，获取安全密钥序列；

根据线性同余理论从已得到的安全密钥序列中，获取最终用于加密的安全密钥。

解题步骤如下：

EPC1：为Alice端根据四个偏振量子态调制编码的随机数序列（1,2,3,4），序列长度为n；

APD1-APD4：为Bob端四个探测器响应序列（0,1），每组序列长度为n，共四组，序列编号分别为1,2,3,4；

如图所示，对于每列数据，只保留APD1-APD4有且只有一个1 的情况，不符合的舍弃，有效探测序列长度为

；

对基成功判定条件如下：

EPC1为1，APD1或APD2为1；

EPC1为2，APD1或APD2为1；

EPC1为3，APD3或APD4为1；

EPC1为4，APD3或APD4为1；

符合的数据保留，不符合的数据丢弃，对基成功序列的长度为

；

首先，在对基成功前提下，筛选误码，误码判定条件如下：

EPC1为1，APD2为1；

EPC1为2，APD1为1；

EPC1为3，APD4为1；

EPC1为4，APD3为1；

得到此时错误的比特数为，计算出误码率为：

根据公式，计算出安全密钥量。

成码率/安全密钥量计算公式：

；

表示二进制香农熵；

出于对题目难度均衡化的考量，我们在题干参数信息中潜藏关键信息“我们默认实现最理想的100%纠错”，选手提取到此条关键信息后，即可简化算法过程。

根据“一次一密”关键词，可知悉：密钥长度=明文长度；

根据“流密码”关键词，可知悉：加密采用对称加密方式，加密和解密时使用同一密钥，且进行异或运算；

根据“UTF8编码方式”关键词，可知悉：最终需通过UTF8进行编码得到明文。

然后根据密文（16进制）长度乘以4为二进制密文的长度，也就是从安全密钥序列中最终获取的密钥长度，根据线性同余的方式去取索引，示例代码（C#语言）如下：

异或运算得到01比特数组，再进行UTF8进行编码得到明文，示例代码（C#语言）如下：


```
// ciphertext密文，srcLen明文长度
string ciphertext = "自定义的密文信息";
char[] charArr = ciphertext.ToArray();
int srcLen = ciphertext.Length / 2;
byte[] byteData = new byte[srcLen];

OriInfoLen = srcLen * 8;
// hexArr：将十六进制数据两两一组，便于后面的异或运算
List<string> hexArr = new List<string>();
for (int i = 0; i < srcLen; i++)
{
  string tempStr = $"{charArr[i * 2]}{charArr[i * 2 + 1]}";
  hexArr.Add(tempStr);
}

// orderKeys线性同余得到二进制数组
int[] orderKeys = GetRandomKey(tmp).ToArray();
// OriInfoLen为密文长度的4倍
for (int i = 0; i < OriInfoLen; i++)
{
  int value = orderKeys[i * 8 + 7] + orderKeys[i * 8 + 6] * 2 + orderKeys[i * 8 + 5] * 4 + orderKeys[i * 8 + 4] * 8 + orderKeys[i * 8 + 3] * 16 + orderKeys[i * 8 + 2] * 32 + orderKeys[i * 8 + 1] * 64 + orderKeys[i * 8] * 128;
  nums.Add(value);
}

/// <summary>
/// 线性同余得到密钥
/// </summary>
/// 
/// <returns></returns>
List GetRandomKey(int[] keyPool)
{
  int A = 1709;
  int B = 2003;
  int M = keyPool.Length;
  int indexBegin = 17;
  // newKey： 经线性同余计算得到的索引所对应的的数据
  List newKey = new List();
  newKey.Add(keyPool[indexBegin]);
  for (int i = 1; i < OriInfoByteLen; i++)
  {
    int res = (A * indexBegin + B) % M;
    newKey.Add(keyPool[res]);
    indexBegin = res;
  }
  return newKey;
}
for (int i = 0; i < OriInfoLen; i++)
{
  int value = Convert.ToInt32(hexArr[i], 16);
  int res = value ^ nums[i];
  byteData[i] = Convert.ToByte(res);
}
var plaintext = Encoding.UTF8.GetString(byteData);
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