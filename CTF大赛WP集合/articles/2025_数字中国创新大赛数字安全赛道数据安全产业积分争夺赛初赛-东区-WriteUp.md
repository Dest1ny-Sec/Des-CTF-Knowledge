# 2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区-WriteUp

> 原文: https://www.ctfiot.com/235930.html
> ID: 235930

点击上方蓝字·关注我们

前言：

随便参加着玩玩，记录一下，仅供参考！

文章同步CSDN，感谢大家观看，麻烦点个赞！

数据安全-ez_upload

数据分析-溯源与取证

2.服务器网站遭到了黑客攻击，但服务器的web日志文件被存放在了加密驱动器中，请解密获得该日志并将黑客ip作为答案提交。

awk -F " " '{print $1}' 1.log | sort | uniq -c | sort -nr

数据分析-数据社工

数据分析-数据跨境

3.请分析审计导出的流量文件，确认是否存在内部人员与外部人员之间的语音通话记录。鉴于信息泄露的风险，请提取并还原所有相关通话内容，并根据对话内容提交答案。本题的答案由小写的26个英文字母组成。

关注我们

欢迎关注鱼影安全社区,专注CTF,职业技能大赛中高职技能培训,金砖企业赛,世界技能大赛省选拔赛,企业赛,行业赛,电子取证和CTF系列培训。

鱼影安全团队招人啦,有感兴趣的师傅可以私信我

需要数据包流量分析 专项培训的 比如比赛等 可以联系小编  价格优惠！


```
awk -F " " '{print $1}' 1.log | sort | uniq -c | sort -nr
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-53687720fcbb8e9dc3244c980d38c03a.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-eeadea661050cb72420d50702ccef121.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-7c258514c0cbca4a2afd7f568674f945-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-b63893fb101ec48ac37008d12854f80c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-0c0e5f702e477e1ec743b4cc7eda4f7c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-e2d9f8a0fc8ad2cec39a374326537b4b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-5d0179cc2975cc01f1777264fa092a11.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-f83563b84f37ae4592e73fe4dab75ae9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a88e3da61851a2780fd2268f09e9c633.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-8a86dcc23c79cc2b5f0ce379dc6bd0fa.png)