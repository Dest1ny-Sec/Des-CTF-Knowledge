# 四川省信息安全技术大赛 AWD部分WriteUp

> 原文: https://www.ctfiot.com/76769.html
> ID: 76769

写在前面

有一年多没打过awd了，这次awd的题目正好遇到了会的，一道PHP一道python还有一个java，队伍里面正好有个java佬，直接起飞。

初始分七万，15分钟一轮，一个flag一百分，最后打了22w多分，我们14w分的时候第二名才11w，具体最后差我们多少不太清楚。

题外话：敢欺负我师弟？无所谓，我会出手。（

我主要做的php和python题，所以就说下这两道题怎么做的

PHP

由于前30分钟是加固时间，所以可以不慌不忙的把php修好。

php这道题拿到手SSH上去之后首先做的就是对网站进行整站备份，为了加快scp/sftp传输速度，直接tar压缩整站。

源代码搞下来之后用D盾、河马进行webshell查杀，使用seay进行自动代码审计，一共找到了两三个读flag点，一个文件上传点。

在复原的时候还是尽量按照AWD赛时的思路去还原，争取还原选手赛时最真实的思路。

备份下源代码之后我们尝试开启waf的流量记录功能或者weblogger，但是我们自己魔改后的waf开不起来，并且担心主办方check原版waf的路径，所以最后没有开waf。

weblogger部署之后站点无法正常访问，遂放弃，本次AWD PHP题所有的漏洞点均为人工审计得出。

接下来先随意看一下目录有没有隐藏文件或者敏感文件，在根目录发现db.sql，直接删掉

接下来根据经验去查看uploads目录是否有可疑文件

在检查完之后还需要做的就是连接数据库进行备份，这里我疏忽了忘记了备份，不过问题不大，应该是没有人能成功打进来我们的靶机进行提权或者破坏，不过无法确定，因为这次的平台没有给每道题的状态，如靶机是否down，每轮是否被check等，呵呵。

进入数据库之后要做的就是修改网站后台密码，这也是常识了，一般来说网站后台密码是弱口令，试了下123456还是admin来着就进去了。

这里改密码出了点问题，我以为密码是MD5之后的值 但是我md5之后的结果和网站存储的结果不太一样，所以后面我改掉之后自己的网站也没有再上去了，只要保证别人登不进去后台就可以，我自己需要的话可以在改回去默认的密码。

网站后台改完基本上数据库也OK了，接下来进行代码审计

命令执行与任意SQL执行

manage_comment_del.php

这个点有命令执行，但是我无法执行命令，因为当时加固阶段网站被waf搞down了，所以我直接修了

这里的修复方式同理，不再赘述。

Manage_rce.php

修复方式也很简单 直接把对应的代码删掉

manage_sql.php

这题给??整乐了，看到SQL注入都不load_file是吧，说句题外话，在打网站后台漏洞的时候我根本没打过rce，直接打SQL语句这个点，过了很久了大部分人还没修，乐。

把TRUE改成FALSE就可以修复了。

任意文件上传

user_upload.php

没啥过滤，修复方法如下

PHP题基本就到这里了，后面或许出了新洞，没有再审计了，一直在干flask内存马。

Python

python这题给了一个blog系统，是flask写的，那么我首先想到的就是模板注入。

代码看了半天也没啥收获，其实这里我的思路有点问题，我忘记直接去搜render_template_string了。直接搜的话可以在加固阶段直接定位到漏洞点。在加固阶段这题也没看出来啥，代码太多了，上去网站功能也很多，前两个小时就没怎么管这道题。

后面我们java和php题都搞完了之后发现有扣分，估计就是python题出问题了，好巧不巧根目录给了web日志

那么就可以充分发挥流量人的特长，看日志。

日志中有大量扫描器等垃圾流量，试了试不太行，最后发现扣分的时候一直有向/auth/reset路由发送请求，遂进入代码查看

看最后的渲染方法是什么，flask人狂喜，已经可以定位漏洞点就在这里了，我首先做的是修复，其次是批量攻击

这题修也非常简单，我直接把花括号过滤了,传了花括号直接返回

下面需要做的就是对这题进行利用，知道这个漏洞点之后我自己试了一下，但是并没有回显SSTI打过去的payload，比较奇怪，我以为是自己payload的问题，遂写了几句话看一下别人payload

最后看到payload就是最简单的ssti payload，由于备份没有存所以展示不了了。可以去看hackbar最简单的那个。

既然确定了是在这里利用漏洞，那么回显的flag在哪里？

我从burp直接看了render后的结果，然后翻了一下源代码发现回显结果是以注释的形式体现，所以这题也就解出来了，最后写脚本批量交，每一轮能打四千多分。

原文始发于Polo：四川省信息安全技术大赛 AWD部分WriteUp

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c4466e4751.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c446f997eb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44792b31e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c449a87276.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44a62e829.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44b7afa07.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44c3386b3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44cf0f910.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44de924a8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_637c44ea9f5f3.png)