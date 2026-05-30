# 2023年春秋杯网络安全冬季联赛RDG部分Writeup

> 原文: https://www.ctfiot.com/170482.html
> ID: 170482

代码位置在这里

application/controllers/Patient.php

这里是一个文件上传的功能，漏洞点在于allowed_types=’*’，未限制文件类型。

漏洞修复就是添加文件名过滤规则

2、头像设置位置有命令注入

修复去掉自定义binary ：$bin_file = “file”;

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711698656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1711698656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1711698657.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1711698658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1711698658.jpeg)