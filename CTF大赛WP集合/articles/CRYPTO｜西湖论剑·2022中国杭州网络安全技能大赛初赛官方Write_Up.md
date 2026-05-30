# CRYPTO｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/97733.html
> ID: 97733

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛CRYPTO题目的Write Up

CRYPTO

2022西湖论剑大赛官方WP

（一）

MyCurveErrorLearn

题目定义的问题可以被描述为ECHNP(DH)

ECHNP(DH)：指定素数p、正整数m，以及

上的椭圆曲线
。点$Q in E, Rin 。定义E上的函数f，未知数Pin E，存在预言机mathcal{O}_{P,R}(t)=f(P+[t]R)。通过预言机mathcal{O}_{P,R}恢复P$。

参考文献HNP第7.1节 Elliptic Curve Hidden Number Problem中的构造，考虑输入0，则可以得到

，此时分别输入

，则可以得到多项式

（二）

LockByLock

由附件可知在secureProcedure中得到了A加密flag的密文c1，B加密c1的密文c2，A解密c2的密文c3.

我们可以做两次输入让A，B来重复上述步骤并且得到中间值。

有

显然可以构造

然后已知e的范围，所以我们使用Pollard’s kangaroo求即可。求完之后带入secureProcedure中得到的结果取一次共模即可。

（三）

MyErrorLearn

题目定义的问题可以被描述为MIHNP

MIHNP：指定素数p以及正整数k，d，未知数

，令

为独立随机乘数。从d对

中恢复
。

其中

参考文献HNP第7章The Modular Inversion Hidden Number Problem中的构造，有

有

。

使用二元coppersmith求解此多项式方程，即可得到e。从而恢复s。

（四）

MyErrorLearnTwice

题目定义的问题可以被描述为MIHNP

MIHNP：指定素数p以及正整数k，d，未知数

，令

为独立随机乘数。从d对

中恢复
。

其中

参考文献HNP第7章The Modular Inversion Hidden Number Problem中的构造，有

有

。设

，所以我们可以利用d组输出得到
项方程

则
为
的
维对角线方阵。
为

维矩阵，由上述多项式方程构造得到每一列。

考虑向量

为最短格向量。使用LLL算法即可求解e，从而得到s。

（五）

MyOracle

题目的关键点是找到Oracle泄露的有用信息，构造模型，很显然，mod是随机的，则当mod为偶数时，会泄露r的LSB，由此我们可以构造矩阵来恢复MT的全部state，从而预测随机数。

具体矩阵构造方式参考cryptography-wiki MT19937.

— 往期回顾 —

MISC｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1676352513.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676352513.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1676352514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676352514.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1676352515.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/9-1676352515.jpeg)