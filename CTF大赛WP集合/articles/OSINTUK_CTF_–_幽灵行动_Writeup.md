# OSINTUK CTF – 幽灵行动 Writeup

> 原文: https://www.ctfiot.com/290898.html
> ID: 290898

发了封邮件过来，简单通个宵打了一下，其实整体还是挺简单的，几乎就是入门级，大多数都很轻松完成了，几乎没有难点。但因为知识盲区第一题卡了好我几个小时，最终只能排13了

The Artifact

首先从反向图片搜索的思路看：根据图片中的MAG218可识别信息，以及整体风格，这很明显就是迪拜。但很遗憾我们的答案是伦敦的一家酒店，这根本不符

于是我开始先对图片进行反向搜索，找到图片作者，对作者一顿操作，依旧错误

接着我通过以下方法进行反向搜索可能的伦敦酒店：

寻找MAG218附近的酒店品牌，同时出现的伦敦的同品牌酒店

寻找位于伦敦的迪拜风格酒店

联合上述思路寻找2017年以前建成的伦敦酒店

寻找伦敦中与MAG218金融城属性相似的酒店

……

通过exiftool查看图片元数据：

这是一个what am i的谜语，解出来的意思就是`red herring`，提醒我们需要转移视线了

其实到这里不难看出来，图片是迪拜，我们却要给一个伦敦的答案，这显然很难扯上联系，加上提示所以迪拜可能是障眼法

后来一看是隐写：

到这，折磨才刚刚开始，因为缺乏这方面的知识和经验，这三个单词也硬控了我几个小时，

一开始我尝试搜索名字为数字的酒店，如：Number Sixteen、100号、ten等等等等，依旧错误，门牌号等等等等，依旧错误

最后丢给ai跑几下跑出来了，叫做what3words

then.number.known

The Getaway

这里其实提醒的挺明显的，直指2017.9，直接谷歌地图对着酒店一顿翻，翻仔细一点，

就能看到其中一张全景图从酒店大厅内部能看到酒店门口外面，并且有一辆符合特征的TX，放大最大车牌也是清晰可见

The Odometer

The Key Source

这也相当简单了，谷歌带双引号直接搜Hackney Today，

进去往下翻找到对应日期的

第八页简单扫一眼下去，最明显就是的what goes around comes around

osintuk{WHAT_GOES_AROUND_COMES_AROUND}

The Final Transmission

这最后一道题更是不用脑子，根据经验，首先背景信息里给的这密文一看就像凯撒，然后说了需要4的密钥，一眼丁真 维吉尼亚密码直接判死了

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756485-wxsync-2026-01-39fcbca17188a2fd569f48a511550284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756487-wxsync-2026-01-8885a162d20af4106761f2bb5bf0ffa6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756489-wxsync-2026-01-8f6f7a95d485d4e7a0378afe689ea0c6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756492-wxsync-2026-01-5028c9ce9ed25b42100617a1226e8272.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756495-wxsync-2026-01-7049f2f1b920424be23a9bda50160d7a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756497-wxsync-2026-01-6733ae7b0ca26b3894a259159ff53ed2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756499-wxsync-2026-01-ef7ce83e5eed0cf6ccaabb07c6eb44d3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756502-wxsync-2026-01-11221a7b7e45a014e0d1e7ef60a1573a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756505-wxsync-2026-01-71d09e0111bdcaeaf7f4fd920c12486d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767756506-wxsync-2026-01-f9f7bd2351d89a9cd3631d41f5286757.png)