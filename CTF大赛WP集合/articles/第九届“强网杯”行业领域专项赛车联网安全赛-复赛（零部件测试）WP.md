# 第九届“强网杯”行业领域专项赛车联网安全赛-复赛（零部件测试）WP

> 原文: https://www.ctfiot.com/283162.html
> ID: 283162

前言

虽然复赛是远程车机零部件测试，但是感觉跟车机关系不大，基本是把CTF题目放到了车机的临时目录里😂，虽然是团队赛，但一个队伍只有一个人可以登陆远程环境，团队赛变个人赛了，打到一半远程环境还崩了一段时间，全体504 Gateway Time-out

修好了之后上传工具文件也报错，联系工作人员，也没有后续，直到比赛结束也没有解决

由于车机数量有限，16支队伍分成了两组，第一组是9:30-11:00,第二组是11:00-12:30，疑似是比赛环境没有重置，有第二组的选手反馈自己的题目被删了😂

以上仅是个人吐槽，与他人无关，还是希望主办方能够完善线上测试的赛制，优化测试环境，给参赛选手好一点的参赛感受，现在转回正题，下面是本次比赛的题解。

强网复赛-签到

题目：

在目录data/local/tmp下有password.txt，读取即可

强网复赛-APP

题目：

在data/local/tmp下面有个app,jadx打开，找到主函数就是flag

强网复赛-固件

题目：

在data/local/tmp下面有个固件包，adb pull下来之后直接放010 Editor里，搜索flag即可

强网复赛-OTA

这道题最后没时间做了，留了张最后的截屏，看了眼大概思路应该是通过分析data/local/tmp下的流量包，提取出下载的固件来分析得到flag，如果有做出来的师傅可以交流指导一下

本篇文章来源于微信公众号: erkangkang的网安生活

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639489-wxsync-2025-11-ea1e9f5c7b5fd7445bdac64ff2769e6e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639490-wxsync-2025-11-61b95dd6ec15070ad6bfaa32e97a3f9e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639492-wxsync-2025-11-7a75450f831d70342cf28ace5899c7bd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639494-wxsync-2025-11-901198fc4949dfaa19bcfa8b0033ae95.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639496-wxsync-2025-11-b02ee861f32a3ac24df8f5b73c3828d1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639498-wxsync-2025-11-86a27fd4457af9408f123a7a99d8f441.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639499-wxsync-2025-11-02876ef48d7361c43a066c7ece934985.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639501-wxsync-2025-11-26db04ba69298f6aa564c4cfe90782af.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639503-wxsync-2025-11-64334ad3004c1450e05563185a0b0061.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763639505-wxsync-2025-11-3ee83ff9502106b4b737e6bd8ada268b.png)