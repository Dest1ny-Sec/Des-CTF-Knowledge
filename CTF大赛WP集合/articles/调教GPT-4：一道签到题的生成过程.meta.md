---
title: 调教GPT-4:一道签到题的生成过程
contest: 数据安全产业人才能力挑战赛 初赛
year: 2023
difficulty: low
vuln_type: web_unknown
tags: [AI-CTF-design, GPT-4, prompt-engineering, signin, xff-spoof, XSS, SQLAlchemy, sqli, base64, signin-system]
attack_chain:
- 调教GPT-4生成新颖签到题,经过多轮prompt调整
- 第一次尝试:SQLAlchemy unique email绕过(失败,UNIQUE constraint不能绕过)
- 第二次尝试:XFF头伪造不同IP(过于基础,不新颖)
- 第三次尝试:HTML不转义名字导致XSS(逻辑问题,看源码可见flag)
- 第四次尝试:请求头挑战(被按下Stop generating)
- 最终:放弃XFF/XSS路线,改用SQLAlchemy+base64编码flag机制
- GPT-4生成代码反复出现"Stop generating"和误导性解释
- 经验:AI生成CTF题需要多轮验证,漏洞不能利用时AI会编造逻辑
key_payload: AI CTF design lessons
one_liner: 数据安全产业人才能力挑战赛调教GPT-4生成签到题的过程记录,涵盖多轮prompt工程经验+SQLAlchemy ORM unique+SQL注入+base64编码+AI生成代码的局限。
lesson: AI生成CTF题需要多轮验证+人工测试;SQLAlchemy ORM默认防SQL注入,要找不常见漏洞点(XFF/XSS等);AI会编造漏洞逻辑,要保持怀疑态度。
quality: low
---

## 题目列表

1篇调教GPT-4设计签到题的过程记录(非WP,作为出题经验)

## 关键考点

### 第一次Prompt
- 目标:基础简单web签到题,新颖不常见,完整输出
- GPT-4响应:SQLAlchemy+Flask,user表name+email,unique email
- 问题:UNIQUE constraint failed,无法绕过,漏洞不存在

### 第二次Prompt
- 目标:有趣漏洞,不用SQLAlchemy
- GPT-4响应:XFF头伪造不同IP
- 问题:过于基础,常见考点

### 第三次Prompt
- 目标:增加timestamp字段,显示最近签到用户
- GPT-4响应:HTML不转义名字导致XSS
- 问题:看源码可直接看到getFlag()函数,无意义

### 第四次Prompt
- 目标:SQL注入漏洞
- GPT-4响应:app.py加搜索路由+base64编码flag
- 问题:与签名系统无关,逻辑混乱

### 第五次Prompt
- 目标:SQLAlchemy漏洞
- GPT-4响应:无
- 失败:Stop generating

### 第六次Prompt
- 目标:凯撒密码(被嫌弃)
- GPT-4响应:自定义编码函数
- 问题:考察点偏重编码解密,不适合web题

### 第七次Prompt
- 目标:HTTP请求头挑战
- GPT-4响应:不完整
- 失败:Stop generating

### 经验教训
1. AI生成CTF题需要多轮验证
2. AI会编造不存在的漏洞逻辑
3. 漏洞不能利用时AI会坚持"理论存在"
4. SQLAlchemy ORM默认防SQL注入
5. XFF/HTML转义等"基础"考点是CTF常见
6. AI的代码经常需要人工修正

## 实战价值
- 这是出题者视角的AI辅助CTF设计经验
- 调教AI生成高质量题目需要明确"新颖+可利用"双标准
- SQLAlchemy+Flask是签到系统的常见栈
- base64编码+SQL过滤是常见WAF
