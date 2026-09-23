---
title: 破阵阁・网安淬锋巅峰赛 应急响应WP
contest: 破阵阁网安淬锋巅峰赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- 应急响应
- Tomcat后门
- /var/crash可疑tomcat
- /etc/profile后门
- crontab持久化
- 内存马/类加载器后门
- 后门用户dev
- manager未授权
attack_chain: netstat -anptu查java进程→发现/var/crash/tomcat后门ELF→rm -rf删除→检查/etc/profile后门命令→crontab -r清持久化→找webapps/a可疑目录→work/Catalina/localhost/a/类加载器字节码马→rm -rf清除→删除examples/login.jsp后门→修复manager context.xml限制IP→删除dev后门用户
key_payload: netstat -anptu;/var/crash/tomcat ELF后门;/etc/profile;crontab -r;work/Catalina/localhost/a/ 类加载器字节码马;webapps/a;examples/login.jsp;manager/META-INF/context.xml ^.*$全IP;dev后门用户
one_liner: 破阵阁应急响应：Tomcat后门排查全流程（进程/ELF/profile/crontab/内存马/后门用户）
lesson: Tomcat应急响应必查项：crash目录ELF、profile、crontab、work/Catalina类加载器字节码、manager权限
quality: high
full_path: 破阵阁・网安淬锋巅峰赛_应急响应WP.full.md
meta_path: 破阵阁・网安淬锋巅峰赛_应急响应WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 破阵阁・网安淬锋巅峰赛 应急响应WP。破阵阁应急响应：Tomcat后门排查全流程（进程/ELF/profile/crontab/内存马/后门用户）。经验：Tomcat应急响应必查项：crash目录ELF、profile、crontab、work/Catalina类加载器字节...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/297281.html
reasoning_chain:
- netstat -anptu查java进程 → 触发点：看到异常Exit 1的tomcat进程
- 假设：tomcat在/var/crash目录可疑 → 动作：file命令查看ELF可执行
- 观察：crash是崩溃转储目录不该有tomcat → 确认后门 → rm -rf tomcat
- /etc/profile是登录shell自动运行 → 触发点：profile后门静默命令
- 动作：vim /etc/profile清除后门命令 → 下一步：crontab持久化清理
- crontab -r清除持久化 → 假设：还有内存马/类加载器字节码马
- 动作：find /opt/apache-tomcat-8.5.100/webapps 发现a可疑目录
- login.jsp无内容但work/Catalina/localhost/a/有编译残留 → 触发点：典型JSP类加载器后门
- rm -rf work/Catalina/localhost/a/ + rm -rf webapps/a + rm -rf examples/login.jsp
- vim manager/META-INF/context.xml ^.*$限制IP → sed删除dev后门用户 → 应急完成
failed_attempts:
- 试图只杀进程不删文件 → 失败：进程重启后门复活
- 试图只删crontab → 失败：profile+类加载器马仍是持久化
- 忽略后门用户dev → 失败：UID=0等价root持续入侵
key_observations:
- Tomcat应急响应必查项：crash目录ELF + profile + crontab + work/Catalina类加载器字节码
- JSP/Servlet 类加载器后门 = 源码清空但work目录有编译类
- manager/META-INF/context.xml ^.*$ = 允许任意IP访问manager（后门化）
- dev后门用户与root同组=UID=0等价root
- sed -i '/^dev:/d' /etc/{passwd,shadow,group,gshadow} 四文件清理
prerequisites:
- Linux应急响应基础（netstat/find/file/crontab）
- Tomcat目录结构（webapps/work/META-INF）
- JSP类加载器/字节码马原理
- Linux用户管理与/etc/{passwd,shadow,group,gshadow}
---
# 破阵阁・网安淬锋巅峰赛 应急响应WP

> 原文: https://www.ctfiot.com/297281.html
> ID: 297281

应急拯救计划：隐匿潜袭

攻击者手法全面升级，在Tomcat服务器中留下了更深层的后门。请彻底排查所有入侵痕迹，只有完美清除所有后门，才能获取最终的flag！

账号 root  
密码 idgfxuxvr2tqekhz

Tomcat后门程序

先通过netstat命令来查看一下java进程

netstat -anptu

tomcat放到了/var/crash目录下。这个程序刚刚异常退出了（Exit 1），crash是崩溃转储目录，很奇怪。

看到tomcat的文件头是elf可执行文件，确定这就是后门程序

rm -rf tomcat

profile文件是当我们登陆shell时自动运行的文件。

profile文件中也有后门静默运行的命令痕迹，清除掉

vim /etc/profile

后门持久化文件检查

清除持久化

crontab -r

内存马清除

a命名的可疑目录

find /opt/apache-tomcat-8.5.100/webapps

login.jsp没有内容？怀疑是内存马落脚点，源码被清空但编译类仍在。

找到编译后的落脚点：

/opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/org/apache/jsp/login_jsp.java  
# 编译残留在work目录

定位后门位置

典型的 JSP/Servlet “类加载器后门（字节码马）”：攻击者发一个参数，服务端把它当成 Java 类加载进 JVM，然后把 request/response 传进去执行。

rm -rf /opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/  
rm -rf /opt/apache-tomcat-8.5.100/webapps/a  
rm -rf /opt/apache-tomcat-8.5.100/webapps/examples/login.jsp  
# examples/login.jsp 同样也是后门落脚点

vim /opt/apache-tomcat-8.5.100/webapps/manager/META-INF/context.xml

^.*$ 等于允许任意来源IP访问manager，这是后门化配置，正常应只允许本地访问，manager 文件被篡改

后门用户清除

发现dev的所属组和root所属组一致，相当于dev的权限等同于root，怀疑是后门用户，删除掉

sed -i '/^dev:/d' /etc/passwd  
sed -i '/^dev:/d' /etc/shadow  
sed -i '/^dev:/d' /etc/group  
sed -i '/^dev:/d' /etc/gshadow


```
账号 root  
密码 idgfxuxvr2tqekhz
netstat -anptu
rm -rf tomcat
vim /etc/profile
crontab -r
find /opt/apache-tomcat-8.5.100/webapps
/opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/org/apache/jsp/login_jsp.java  
# 编译残留在work目录
rm -rf /opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/  
rm -rf /opt/apache-tomcat-8.5.100/webapps/a  
rm -rf /opt/apache-tomcat-8.5.100/webapps/examples/login.jsp  
# examples/login.jsp 同样也是后门落脚点
vim /opt/apache-tomcat-8.5.100/webapps/manager/META-INF/context.xml
sed -i '/^dev:/d' /etc/passwd  
sed -i '/^dev:/d' /etc/shadow  
sed -i '/^dev:/d' /etc/group  
sed -i '/^dev:/d' /etc/gshadow
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]