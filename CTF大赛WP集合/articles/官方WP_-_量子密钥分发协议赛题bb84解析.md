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
/// <param name="keyPool"></param>
/// <returns></returns>
List<int> GetRandomKey(int[] keyPool)
{
  int A = 1709;
  int B = 2003;
  int M = keyPool.Length;
  int indexBegin = 17;
  // newKey： 经线性同余计算得到的索引所对应的的数据
  List<int> newKey = new List<int>();
  newKey.Add(keyPool[indexBegin]);
  for (int i = 1; i < OriInfoByteLen; i++)
  {
    int res = (A * indexBegin + B) % M;
    newKey.Add(keyPool[res]);
    indexBegin = res;
  }
  return newKey;
}
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1686218675.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1686218675.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1686218676.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1686218677.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686218678.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686218678.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1686218680.gif)