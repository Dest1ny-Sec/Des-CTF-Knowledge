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
```



```
netstat -anptu
```



```
rm -rf tomcat
```



```
vim /etc/profile
```



```
crontab -r
```



```
find /opt/apache-tomcat-8.5.100/webapps
```



```
/opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/org/apache/jsp/login_jsp.java  
# 编译残留在work目录
```



```
rm -rf /opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/  
rm -rf /opt/apache-tomcat-8.5.100/webapps/a  
rm -rf /opt/apache-tomcat-8.5.100/webapps/examples/login.jsp  
# examples/login.jsp 同样也是后门落脚点
```



```
vim /opt/apache-tomcat-8.5.100/webapps/manager/META-INF/context.xml
```



```
sed -i '/^dev:/d' /etc/passwd  
sed -i '/^dev:/d' /etc/shadow  
sed -i '/^dev:/d' /etc/group  
sed -i '/^dev:/d' /etc/gshadow
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511568-wxsync-2026-02-2533d9a78b628a164298b6513ef81d41.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511569-wxsync-2026-02-e8f391d030a929abc13a025ee6b87a43.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511571-wxsync-2026-02-70194d28d49be2457d115456daaed580.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511573-wxsync-2026-02-845bdb848e6130cd9e9d0200520123b3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511574-wxsync-2026-02-c38cfceed2aa54bb579883f419579e05.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511576-wxsync-2026-02-2b195118101b96dd512c558a70a8f72c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511578-wxsync-2026-02-3b03a7d515a5f6d8442d8e5b8ca8591d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511580-wxsync-2026-02-835f536fcbe9c370df316753c0affe42.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511582-wxsync-2026-02-c4146a9cb48811e50158b331e14cea7a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1770511584-wxsync-2026-02-23db27c306dd35e5f26d4bf254517de6.png)