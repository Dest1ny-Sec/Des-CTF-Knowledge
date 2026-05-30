# DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测

> 原文: https://www.ctfiot.com/233929.html
> ID: 233929

高效的静态规则匹配在大样本数据集中初步过滤出可疑恶意包及混淆软件包；

较为耗时的基于字符串的污点分析在规则匹配的可疑恶意包结果中进一步收缩范围；

将两步过滤结果的可疑样本通过构造的prompt提交给ChatGPT验证其恶意性，同时学习新的恶意特征更新已有的静态规则；

针对静态规则匹配检测出的混淆软件包，采用动态分析的方式确认其恶意性。本项目能够高效检测出npm软件包中的恶意包，误报率低、准确率高、能够检测新的攻击。

https://gitee.com/jenniedn/mal-npmdetector.git

此类恶意包通常结构简单，具有统一模板。安装后会自动执行恶意脚本，收集并回传系统和用户信息等敏感数据，如用户目录、用户名、DNS服务器，网卡信息和 passwd 文件内容等;

此类恶意包危害极大，成功攻击后，攻击者可获取目标机器当前用户权限，并进步尝试提权，以最高权限执行任意命令，全面控制受害设备;

此类恶意包在用户机器上下载或释放并执行已经精心制作好的后门木马;

此类恶意包以窃取计算资源为目的，将受害者的机器变为攻击者矿池的算力节点,为其持续提供算力。

此类恶意包会读取用户电脑上的重要目录文件内容，加密后再写回原文件，并留下勒索提示。

此类恶意包没有太多实际作用，但是大量充斥于NPM开源仓库，某些情形下容易造成NPM整个仓库不可用。

⭐ 给个 Star，支持我们的项目！

👀 Watch 关注项目，随时获取最新动态

🍴 Fork 仓库，进行二次开发或学习研究！

📝 提交 Issue 或 PR，共同优化软件供应链生态！

👉 访问 Gitee 仓库：https://gitee.com/jenniedn/mal-npmdetector.git

https://gitee.com/jenniedn/mal-npmdetector.git

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-20e718c284b1ad978c3d5733485253c8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-9bc3829240348813e03834b9c409cb73.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-5c2121d868762f8af5391b201a924210.png)