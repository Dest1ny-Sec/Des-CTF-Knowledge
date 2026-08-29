---
title: 破阵阁・网安淬锋巅峰赛 应急响应WP
contest: 破阵阁网安淬锋巅峰赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [应急响应, Tomcat后门, /var/crash可疑tomcat, /etc/profile后门, crontab持久化, 内存马/类加载器后门, 后门用户dev, manager未授权]
attack_chain: netstat -anptu查java进程→发现/var/crash/tomcat后门ELF→rm -rf删除→检查/etc/profile后门命令→crontab -r清持久化→找webapps/a可疑目录→work/Catalina/localhost/a/类加载器字节码马→rm -rf清除→删除examples/login.jsp后门→修复manager context.xml限制IP→删除dev后门用户
key_payload: "netstat -anptu;/var/crash/tomcat ELF后门;/etc/profile;crontab -r;work/Catalina/localhost/a/ 类加载器字节码马;webapps/a;examples/login.jsp;manager/META-INF/context.xml ^.*$全IP;dev后门用户"
one_liner: 破阵阁应急响应：Tomcat后门排查全流程（进程/ELF/profile/crontab/内存马/后门用户）
lesson: Tomcat应急响应必查项：crash目录ELF、profile、crontab、work/Catalina类加载器字节码、manager权限
quality: high
---

# 破阵阁・网安淬锋巅峰赛 应急响应WP

**赛事**：破阵阁・网安淬锋巅峰赛 - 应急拯救计划：隐匿潜袭（2025）

**性质**：应急响应实战（Tomcat服务器后门排查）

**环境**：
- 账号 root
- 密码 idgfxuxvr2tqekhz

**应急响应完整流程**：

**Step 1：进程排查**
```bash
netstat -anptu  # 查java进程
```

**Step 2：删除后门程序**
- 发现 `/var/crash/tomcat`（crash是崩溃转储目录，可疑）
- file命令查看 → ELF可执行文件 → **后门**
- `rm -rf tomcat`

**Step 3：profile文件清理**
- /etc/profile 是登录shell自动运行
- 包含后门静默运行命令
- `vim /etc/profile` 编辑清除

**Step 4：持久化清理**
```bash
crontab -r  # 清除crontab持久化
```

**Step 5：内存马/类加载器字节码马**
```bash
find /opt/apache-tomcat-8.5.100/webapps
# 发现 a命名的可疑目录
```
- login.jsp没内容但work目录有编译残留
- 落脚点：`/opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/org/apache/jsp/login_jsp.java`
- 典型的 **JSP/Servlet "类加载器后门（字节码马）**
- 攻击者发参数 → 服务端当Java类加载进JVM → request/response传进去执行
- 清除：
  ```bash
  rm -rf /opt/apache-tomcat-8.5.100/work/Catalina/localhost/a/
  rm -rf /opt/apache-tomcat-8.5.100/webapps/a
  rm -rf /opt/apache-tomcat-8.5.100/webapps/examples/login.jsp  # 同样后门
  ```

**Step 6：Tomcat Manager后门**
```bash
vim /opt/apache-tomcat-8.5.100/webapps/manager/META-INF/context.xml
```
- `^.*$` 允许任意IP访问manager
- **后门化配置**，正常应只允许本地
- 限制IP访问

**Step 7：删除后门用户**
- dev用户所属组与root一致 → 权限等同root
- 后门用户，删除：
  ```bash
  sed -i '/^dev:/d' /etc/passwd
  sed -i '/^dev:/d' /etc/shadow
  sed -i '/^dev:/d' /etc/group
  sed -i '/^dev:/d' /etc/gshadow
  ```

**质量评估**：高（完整Tomcat应急响应6步流程 + 命令具体）
