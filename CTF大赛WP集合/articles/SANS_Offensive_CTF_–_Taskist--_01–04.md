# SANS Offensive CTF – Taskist:: 01–04

> 原文: https://www.ctfiot.com/166045.html
> ID: 166045

Summary: 概括：

This Write Up outlines several vulnerabilities discovered within the application, including IDOR (Insecure Direct Object Reference), privilege escalation, SSRF (Server-Side Request Forgery), and unauthorized file access issues.

本文概述了应用程序中发现的多个漏洞，包括 IDOR（不安全的直接对象引用）、权限升级、SSRF（服务器端请求伪造）和未经授权的文件访问问题。

Taskist::01- IDOR Vulnerability in “/api/tasks/<ID>”

Taskist::01-“/api/tasks/<ID>”中的 IDOR 漏洞

Description: The application has an Insecure Direct Object Reference vulnerability in the /api/tasks/64 endpoint, allowing unauthorized access to admin’s tasks information.

描述：该应用程序在 /api/tasks/64 端点中存在不安全的直接对象引用漏洞，允许未经授权访问管理员的任务信息。

Impact: Admin notes containing confidential information, including the flag, are exposed to unauthorized users.

影响：包含机密信息（包括标志）的管理员注释会暴露给未经授权的用户。

Recommendation: Implement proper access controls and authorization mechanisms to restrict access to sensitive data based on user roles and permissions.

建议：实施适当的访问控制和授权机制，根据用户角色和权限限制对敏感数据的访问。

POC: 概念验证：

1. Now after logging into the application you can see the source code (ctrl + u), observe the endpoints/paths.

1.现在登录应用程序后，您可以看到源代码（ctrl + u），观察端点/路径。

2. After observing you can find the only endpoint which is potential to IDOR. Sending the request to Intruder along with the first 100 numbers as payloads and start the attack.

2.观察后可以找到唯一可能发生IDOR的终点。将请求连同前 100 个数字作为有效负载发送给 Intruder 并开始攻击。

Intruder 入侵者

flag-1 标志-1

Taskist::02: Privilege Escalation via Update Password Feature

Taskist::02：通过更新密码功能提升权限

Description: The application allows changing the user_id parameter to an admin user’s user_id during the update password feature, leading to unauthorized privilege escalation.

描述：该应用程序允许在更新密码功能期间将 user_id 参数更改为管理员用户的 user_id，从而导致未经授权的权限提升。

Impact: Unauthorized users can change the admin’s password, compromising the admin account’s security.

影响：未经授权的用户可以更改管理员密码，从而危及管理员帐户的安全。

Recommendation: Implement strict validation checks to ensure that only authorized users can update passwords, and enforce proper authentication mechanisms to prevent privilege escalation attacks.

建议：实施严格的验证检查以确保只有授权用户才能更新密码，并强制执行适当的身份验证机制以防止权限升级攻击。

POC: 概念验证：

Navigate to Password Reset Functionality, Intercept the request and observe that “user_id” is being passed. Change the “user_id” value to admin’s user_id

导航到密码重置功能，拦截请求并观察正在传递“user_id”。将“user_id”值更改为管理员的user_id

admin-password 管理员密码

Flag-2 旗帜-2

Taskist::03: SSRF Vulnerability leads to Unauthorized File Read Access

Taskist::03：SSRF 漏洞导致未经授权的文件读取访问

Description: By exploiting a vulnerability in the application’s handling of the proc/self/environ path. The main code ususally lies within app.js.

描述：利用应用程序处理 proc/self/environ 路径时的漏洞。主要代码通常位于 app.js 中。

You can see an attacker can gain unauthorized access to sensitive files, such as /app/index.js.

您可以看到攻击者可以获得对敏感文件的未经授权的访问，例如/app/index.js。

flag-3 标志-3

Impact: Attackers can read sensitive application files containing configuration details or other critical information.

影响：攻击者可以读取包含配置详细信息或其他关键信息的敏感应用程序文件。

Recommendation: Implement proper input validation and sanitization to prevent directory traversal attacks, and restrict access to sensitive files to authorized users only.

建议：实施适当的输入验证和清理以防止目录遍历攻击，并将敏感文件的访问限制为仅授权用户。

POC: 概念验证：

1. After logging in as an admin, we can observe that there are `site configuration` settings along with import and export features. 重试  错误原因

2. Now by analyzing the source code of `site_config.js`, we can observe that the import feature is validating to variables not to be as ‘undefined’. 重试  错误原因

3. Now after exploring the export functionality we are able to download `site-config.json`. When we look at the variables of the json file, the validating variables of import feature and export json file are the same for the first 2 variables. Here we can conclude that the vulnerability should be exploited over here. 重试  错误原因

4. By Uploading the dummy file and intercepting the request, replace the url with burp collaborator. We got a hit!, SSRF Confirmed. 重试  错误原因

5. We should look for sensitive information files which disclose the endpoints of the server function. By analyzing the tasks list in the admin dashboard we can say that 2 out 3 are pending. A Hint to the “/app” directory, which is not accomplished by admin. 重试  错误原因

6. Brute forcing with common LFI Payloads!??no, we should look for sensitive endpoints, some of sensitive endpoints are “/proc/*/*”. 重试  错误原因

flag — 3 标志 — 3

Taskist::04: SSRF Vulnerability leads to chaining access to the root directory.

Taskist::04：SSRF 漏洞导致对根目录的链接访问。

Description: The application’s file upload functionality is vulnerable to Server-Side Request Forgery (SSRF), allowing attackers to initiate requests to arbitrary URLs, including local files such as ‘file:///’.

描述：该应用程序的文件上传功能容易受到服务器端请求伪造（SSRF）的攻击，允许攻击者向任意 URL 发起请求，包括“file:///”等本地文件。

Impact: Attackers can exploit this vulnerability to read sensitive files on the server, such as /root/flag.txt, leading to unauthorized disclosure of sensitive information.

影响：攻击者可利用该漏洞读取服务器上的敏感文件，如/root/flag.txt，导致敏感信息未经授权泄露。

Recommendation: Implement strict input validation and filtering mechanisms to prevent SSRF attacks, and restrict file upload functionality to trusted sources only.

建议：实施严格的输入验证和过滤机制以防止 SSRF 攻击，并将文件上传功能仅限于可信来源。

Note: The Taskist-4 should have been deployed at the user level to gain chain further to get flag{} at root level. Maybe it’s not a bug but a Feature Who Knows what kind of rabbit hole it might be misleading us with other things.

注意：Taskist-4 应部署在用户级别，以进一步获得链以在根级别获取 flag{}。也许这不是一个错误，而是一个功能，谁知道它可能会用其他东西误导我们什么样的兔子洞。

POC: (unintentional solution, by directly reading the root flag)

POC：（无意的解决方案，通过直接读取根标志）

1. Send a Request to “file:///etc/*” to know whether we are able to access the root files, after conclusion we are able to access the root directory files. Send request for “file:///root/flag.txt”

1. 向“file:///etc/*”发送请求，了解是否能够访问根目录文件，结束后就可以访问根目录文件了。发送“file:///root/flag.txt”的请求

flag-4 标志-4

Unintentional soltuion — Admin

无意的解决方案 — 管理员

Authors: 0xPb, daniel1895

作者：0xPb、daniel1895

Thanks for reading!!! 谢谢阅读！！！

原文始发于Prasanth Bodepu：SANS Offensive CTF – Taskist:: 01–04