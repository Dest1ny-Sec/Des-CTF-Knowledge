# Writeup｜1024羊群之谜

> 原文: https://www.ctfiot.com/66460.html
> ID: 66460

周一（10.24）发布的羊群之谜，大家都顺利通关了吗

1024｜秘密行动！你能破解羊群之谜，拿下财富密码吗？

小编在后台看到大家踊跃参与身影，甚是欣慰

这次，小编特地邀请到率先攻破所有题目并飞速肝出Writeup的不愿意透露姓名大佬，来为大家做一期分享~

✦

第一关

✦

直接查A地址是没有解析的，于是遍历一下A、CNAME、TXT等

而查询TXT会发现

;; ANSWER SECTION:
berichyang.group.       600     IN      TXT     "spf1 a mx ?all nice try, but this is not your flag, try another~"

这里重点关注一下spf这个关键词，提示让人想到是邮件相关的解析协议，这一类解析通常用TXT来做。

大概有以下几种协议

SPF（Sender Policy Framework）

DKIM（DomainKeys Identified Mail）

DMARC（Domain-based Message Authentication, Reporting and Conformance）

✦

第二关

✦

这个关卡，感觉就有点烂大街的意思了，当时游戏火的时候，各种修改，网上的文章教程多如牛毛，后来协议增加了加密验证，才得到了一定的遏制

这里我们使用burp抓包就可以看到map_id这个参数，早期版本就存在这个漏洞，直接修改关卡地图，让难度都如第一关一样简单

所以，直接修改map关卡

修改两关的map_id=80001,这样第二关改成第一关的难度

✦

第三关

✦

说实话，第三关我一开始没有看懂题，我以为是pwn呢，但是一看没有输入当时就懵了好一会

看提示说让用trace和异常。说实话异常暂时没想到如何让他触发异常形成内存转储，转而使用trace方案

trace的话，首先想到ptrace，也就注入hook方面的东西了

#include <stdio.h>
#include 

const char *flag = "M01N{**************************}"; 

int main(){

    printf("flag addr : %pn",flag);
    flag = "I hope you are very happy every day.nBut you should think of ptrace or unexpected";
    puts(flag);
    return 0;
}

代码十分简单，先赋值了flag，当时想到了强网杯还是啥的题，以为是有个先于main函数的异常处理，解密flag来着，但是仔细看了一下想复杂了，就是全局变量存储flag，然后main函数执行的时候会对它进行二次覆盖，而我们要做的就是在覆盖之前把他的内存读一下就好了

nc连上服务器

ctf@9033f7730e96:~$ ls -al
ls -al
total 40
drwxr-xr-x 1 root ctf  4096 Oct 24 08:50 .
drwxr-xr-x 1 root root 4096 Oct 20 12:54 ..
-rw-r--r-- 1 root ctf   220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 root ctf  3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 root ctf   807 Apr  4  2018 .profile
-rw-r--r-- 1 root ctf    44 Oct 24 08:48 hint.txt
---s--x--x 1 root ctf  8688 Oct 19 07:56 play
-rw-r--r-- 1 root ctf   293 Oct 21 02:13 play.c

看了一下权限，具有s属性，这里让我摔了一跤

最初的写法是直接用ptrace找一个切入点，在main函数附近，覆盖之前。因为是全局变量，所以进入main函数的时候全局变量已经装载完成了，且地址固定。write的系统调用很多，也是比较频繁的，通过hook这个的一瞬间去直接print

printf("flag:%s", 0x400638);

但是这里有一个非常大的问题，我就没注意，进程是我没有权限的，我的权限是非root用户，此时的内存是不可读不可写，就令人非常尴尬，也尝试过使用LD_PRELOAD去hook mai函数，或者说是去hook__libc_start_main这个，但是同样问题，本机ok，因为本机都是root权限，到了服务器上就疯狂报错

对了这里要提一点很灵性的东西，出题人专门给安装了wget，就是让你写程序去搞他的，但是我最初甚至妄想直接wget上传拖回来看看

通过多次尝试，发现这里内存不可读写，但是寄存器是可以操作的

虽然有源码，不太喜欢看源码，这样情况下，看源码很难看出来利用思路

这里正好有一个调用，我们把他提前不就成了吗

所以考虑修改寄存器，将地址劫持到puts

相当于跳过了给flag替换赋值的步骤，当第一次调用write的时候肯定还没有对flag进行覆盖，所以直接劫持，在进入write的时候强制跳转到0x40058E

程序就直接变成了

#include <stdio.h>
#include 

const char *flag = "M01N{**************************}"; 
    ……
    puts(flag);
    ……
int main(){
    ……
    puts(flag);
    ……
    printf("flag addr : %pn",flag);
    flag = "I hope you are very happy every day.nBut you should think of ptrace or unexpected";
    puts(flag);
    return 0;
    return 0;
}

(由于会有多处调用write，上述伪代码只是简要的作为描述理解。)

直接puts(flag)

直接输出了没有被替换的flag

flag M01N{w1sh_y0u_happiness_forever}

当时做题的时候，还没有出hint，目前官方已经给的非常详细了

ctf@64ec566022a6:~$ cat hint.txt
cat hint.txt

https://clubby789.me/zer0pts2022/#readflag

✦

后记

✦

不愿意透露姓名的大佬：

Ok，终于婆婆妈妈，啰里啰唆的说完了。希望别嫌弃吧，为了鼠标垫折腰。而且文笔就这样，当年要是文科好，也去不了计算机专业，就这样吧

熄灯~

小编：

看了本期Writeup，大家是不是茅塞顿开，想亲自来复现一遍

好消息来了！小编特地将题目环境保留至本周五，欢迎感兴趣的同学来学习复现交流

感谢粉丝对本次活动的热情参与

也非常感谢这位不愿意透露姓名的大佬提供如此优秀的Writeup

欢迎大家在评论区留下你对“羊群之谜”的想法、疑惑、解题过程中的奇思妙想和有趣的故事~

绿盟科技M01N战队专注于Red Team、APT等高级攻击技术、战术及威胁研究，涉及Web安全、终端安全、AD安全、云安全等相关领域。通过研判现网攻击技术发展方向，以攻促防，为风险识别及威胁对抗提供决策支撑，全面提升安全防护能力。

M01N Team公众号

聚焦高级攻防对抗热点技术

绿盟科技蓝军技术研究战队

官方攻防交流群

网络安全一手资讯

攻防技术答疑解惑

扫码加好友即可拉群


```
;; ANSWER SECTION:
berichyang.group.       600     IN      TXT     "spf1 a mx ?all nice try, but this is not your flag, try another~"
    #include <stdio.h>
    #include 

const char *flag = "M01N{**************************}"; 

int main(){

    printf("flag addr : %pn",flag);
    flag = "I hope you are very happy every day.nBut you should think of ptrace or unexpected";
    puts(flag);
    return 0;
}
ctf@9033f7730e96:~$ ls -al
ls -al
total 40
drwxr-xr-x 1 root ctf  4096 Oct 24 08:50 .
drwxr-xr-x 1 root root 4096 Oct 20 12:54 ..
-rw-r--r-- 1 root ctf   220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 root ctf  3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 root ctf   807 Apr  4  2018 .profile
-rw-r--r-- 1 root ctf    44 Oct 24 08:48 hint.txt
---s--x--x 1 root ctf  8688 Oct 19 07:56 play
-rw-r--r-- 1 root ctf   293 Oct 21 02:13 play.c
printf("flag:%s", 0x400638);
    #include <stdio.h>
    #include 

const char *flag = "M01N{**************************}"; 
    ……
    puts(flag);
    ……
int main(){
    ……
    puts(flag);
    ……
    printf("flag addr : %pn",flag);
    flag = "I hope you are very happy every day.nBut you should think of ptrace or unexpected";
    puts(flag);
    return 0;
    return 0;
}
ctf@64ec566022a6:~$ cat hint.txt
cat hint.txt

https://clubby789.me/zer0pts2022/#readflag
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666794176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1666794176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1666794178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666794179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666794180.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666794181.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666794182.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666794182.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666794183.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666794183.jpeg)