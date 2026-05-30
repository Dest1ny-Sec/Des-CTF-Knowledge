# WIZ Cloud Hunting Games 挑战赛WP

> 原文: https://www.ctfiot.com/247131.html
> ID: 247131

点击蓝字

关注我们

声明

本文作者：shadowabi
本文字数：3029字

阅读时长：约8分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

Cloud Hunting Games 是 WIZ 最新推出的一个新的 CTF 挑战赛，这一次是从云安全应急响应的维度来进行挑战。
挑战赛入口：https://www.cloudhuntinggames.com

背景

❝

ExfilCola 是一家很有前途的初创公司，拥有可以打破可乐巨头双头垄断的革命性苏打水配方，它收到了一封来自名为“FizzShadows”的威胁组织的数据勒索电子邮件，声称已经破坏了他们的系统。

如果秘方被盗，公司的未来将面临直接风险。作为选定的专家，您必须防止公式被泄露在为时已晚之前。

Challenge 1

这一关其实就是去调查取证，找到秘密配方被窃取的证据，并提供当时被调用的身份凭证 arn 号。

查询语句官方已经默认给好了，直接点 RUN Query 即可

然后点 Columns，筛选我们需要的关键信息。

很显然，根据线索的提示，这是 S3 存储桶内的文件窃取，那么我们需要筛选出，GetObject 事件，访问的 object 需要和 secret 相关，以及 arn 号

那么就是这三列

可以选择 Download as CSV，在 excel 表格里筛选

也可以用 search 功能来搜

拉到最下面，可以发现，这个 txt 是比较可疑的，提交对应的 arn 号即可

Challenge 2

在挑战 1 中，我们找到了 arn 号，接下来就需要去溯源这个身份凭证是什么时候被失陷的。

和上面一样的方法，这里给出最佳解法：

这个  Moe.Jito 并不是常见的调用用户，而且仅有一次扮演记录，很可疑。也可以综合 IP 和上下文调用记录、凭证失陷时间来判断。

Challenge 3

这个挑战就是继续深挖，攻击者是否有横向移动的痕迹。

直接下载整个 CSV，我的办法是筛选 EventName，看日志中是否有和服务器相关的，然后再结合上下文判断

EventName 中有一个 ListFunctions20150331 事件，查看发现是和云函数相关的，并且根据后续的行动，可推断该函数和获取凭证相关，且后续有攻击者使用痕迹

此时可证明，该云函数工作负载已遭到攻击者入侵

Challenge 4

第四关应该是最难的一关，非常容易想太多。

第四关是找，攻击者是怎么入侵该云函数的工作负载的。

已经提示了机器不出网，所以可以排除和网络连接相关的入侵手法。

很显然，找攻击者什么时候入侵机器，第一想法是找 ssh 登录日志

last 提示文件不存在。去 /var/log 里找，发现有攻击者的留言。

有可能日志被删了，或者被隐藏了

回到最开始的地方，我们并不是在 /root 目录中，而是在 /home/user 中，这也是一个提示

当前目录下没文件，但是返回 home 目录，会发现有一个 postgresql-user 目录

两个python文件很显然是用来获取凭证的，而 .bash_history 则揭示了攻击者所使用的手法。

由于 history 文件内容多，这里用 head 即可

先去跟 /tmp/…/ 目录，因为这很显然是一个隐藏目录，正常程序不会这样写

可以发现，这里的内容和 /var/log 一致，再结合 .bash_history 中的 findmnt，大概率，攻击者是用这里的文件夹 mount 了 /var/log

在 findmnt 中也是这样的

直接 umount /var/log 即可

然后进入 /var/log，发现有个 auth.log，head auth.log 能得到攻击者 ip

Challenge 5

这一关相对简单，提示攻击者做了持久化，要反打攻击者。

做持久化，最明显就是 crontab 定时任务。直接用 crontab -l 或者 找 /etc/crontab/ 是没东西的。

这里我差点就错过关键线索，在群友的提醒下，/var/spool/cron/crontabs 也是可以放的，我之前一直以为这是 centos 才会放这。

第二个坑点来了，这里看起来是某个 pgsql 的二进制文件，但仔细看参数，他是用 bash 执行的，也就是说，他必然是一个 sh 脚本。

这里把 sh 脚本解开会得到攻击者的完整攻击脚本。

这里我们只需要关注攻击者怎么将结果回传到他的 VPS 上即可

这里就很明显了，结果是通过 curl 回传到他的服务器上的，直接把攻击脚本前面的变量拼接进来就可以了

根据任务提示，我们需要去删除掉泄漏的秘密。恰好他的文件管理系统是有删除功能的，直接删就过关了。

通关凭证

shadowabi 和 他的小伙伴们组团上分，是国内第一批打完这个挑战赛的。

作者

shadowabi

自强不息

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647233-wxsync-2025-05-c1791da0e1cf4ba822cbb9abb096f2ce.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647235-wxsync-2025-05-2f51c95e7f9c72a1aa448b3e956af10b.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647238-wxsync-2025-05-34d12981d854a6eae37beeed5dfd0980.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647241-wxsync-2025-05-f5bed97bcc6b83197cbe3b38985d94c6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647245-wxsync-2025-05-2b72378dd510f079f6c746748580cd4d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647247-wxsync-2025-05-ef09381a1369053beac6bf640f1dc4f6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647250-wxsync-2025-05-855527c257b4280e99627219da81b576.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647253-wxsync-2025-05-c56aa4ecf7d77aa5400dc5caae627874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647255-wxsync-2025-05-2b28af60149aecf070bb0ea75581a6e3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1747647257-wxsync-2025-05-378d480ad7e8f2f3cb672ecec59eae13.png)