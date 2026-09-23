---
title: 【WP】NewStar CTF 2025 Week1&Week2 之 WEB 方向题解
contest: NewStarCTF
year: 2025
difficulty: easy
vuln_type: web_unknown
tags:
- token-calc
- expression-regex
- requests-Session
- cookie-maintain
- /start_challenge
- /verify_token
- multiply-xor
attack_chain: POST /start_challenge 拿 expression token 表达式 + hint + multiplier + xor_value + 新 session/正则提取 num1*num2^0x... 计算 token/POST /verify_token 提交 token/保持 session cookie 跨请求
key_payload: expression = "token = (1234 * 5678) ^ 0xDEADBEEF"  token = (1234*5678) ^ 0xDEADBEEF
one_liner: NewStar CTF 2025 Week1&Week2 Web 入门题，token 计算 + Session 维持 + 正则表达式。
lesson: requests.Session() 自动维持 cookie；正则 re.search 提取表达式数字和异或值；token = (num1*num2) ^ xor_val 是基础算术 XOR；Web 入门题通常用 icook 维持 session。
quality: medium
full_path: 【WP】NewStar_CTF_2025_Week1&Week2_之WEB方向题解.full.md
meta_path: 【WP】NewStar_CTF_2025_Week1&Week2_之WEB方向题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WP】NewStar CTF 2025 Week1&Week2 之 WEB 方向题解。NewStar CTF 2025 Week1&Week2 Web 入门题，token 计算 + Session 维持 + 正则表达式。。经验：requests.Session() 自动维持 cookie；正则 re.search 提取表达式数字和异或值；toke...
category: web
subcategory: web_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/274196.html
reasoning_chain:
- POST /start_challenge → 服务器返回 JSON：expression + hint + multiplier + xor_value → 触发点：需要计算 token
- expression = "token = (num1 * num2) ^ 0xDEADBEEF" → 假设：正则提取 num1/num2/xor_val
- 计算 token = (num1 * num2) ^ xor_val → 动作：int(xor_val, 16) 解析十六进制
- POST /verify_token 提交 token → 假设：保持 session cookie
- requests.Session() 自动维持 cookie + update 新 session cookie → 观察：完成
failed_attempts:
- 试图无 session 直接 verify → 401
- 试图 eval(expression) 直接算 → 表达式被服务器加限制
- 试图手动解析 JSON → 实际是嵌套结构
key_observations:
- requests.Session() 自动维持 cookie 是 Web 入门题基础
- 正则 re.search 提取表达式数字和异或值
- token = (num1*num2) ^ xor_val 是基础算术 XOR
- 服务端每次返回新 session cookie 必须在客户端更新
prerequisites:
- requests.Session() 用法
- 正则表达式 re.search/r'(...)*...^0x...'
- HTTP Cookie 维持原理
- 算术 XOR 与十六进制
---
# 【WP】NewStar CTF 2025 Week1&Week2 之WEB方向题解

> 原文: https://www.ctfiot.com/274196.html
> ID: 274196

importrequestsimportreimportjsondefcalculate_token(expression): """从表达式中计算token值""" # 使用正则表达式提取数字和异或值 match= re.search(r'token = ((d+) * (d+)) ^ (0x[0-9a-f]+)', expression) ifmatch: num1 =int(match.group(1)) num2 =int(match.group(2)) xor_val =int(match.group(3),16) # 计算token: (num1 * num2) ^ xor_val product = num1 * num2 token = product ^ xor_val returntoken else: raiseValueError("无法解析表达式")defmain(): # 基础URL base_url ="https://eci-2ze5w79g3ev2py8ceky2.cloudeci1.ichunqiu.com:
5000" # 初始cookie initial_cookies = { "Hm_lvt_2d0601bd28de7d49818249cf35d95943":"1756542647", "session":".eJxNy00KwyAQQOG7zNqFCok_695DJB2MMGqZjFAovXubnev3vg8cZybCXjC1SVJfVJEh2l1brZZ4SWZJUhtCNG4LzmoX_Hq8x98Z7_3mggIapeAz1Q5ReKKCeSH3fHN4DB7w_QEpuikw.aOM1Xg.UkjBnjZdrYMWyH6SDHw2G3b54ws" } # 创建session对象来保持cookie session = requests.Session() session.cookies.update(initial_cookies) # 设置请求头 headers = { "Sec-Ch-Ua-Platform":""Windows"", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36", "Sec-Ch-Ua":""Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"", "Dnt":"1", "Content-Type":"application/json", "Sec-Ch-Ua-Mobile":"?0", "Accept":"*/*", "Origin": base_url, "Sec-Fetch-Site":"same-origin", "Sec-Fetch-Mode":"cors", "Sec-Fetch-Dest":"empty", "Referer":f"{base_url}/home", "Accept-Encoding":"gzip, deflate, br", "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8", "Priority":"u=1, i" } # 第一步：发送start_challenge请求 print("发送start_challenge请求...") start_response = session.post( f"{base_url}/start_challenge", headers=headers, data="" ) ifstart_response.status_code !=200: print(f"start_challenge请求失败:{start_response.status_code}") return # 更新cookie（使用服务器返回的新session） if'session'instart_response.cookies: session.cookies.set('session', start_response.cookies['session']) print(f"更新session cookie:{start_response.cookies['session']}") # 解析响应数据 try: response_data = start_response.json() expression = response_data.get("expression","") hint = response_data.get("hint","") multiplier = response_data.get("multiplier","") xor_value = response_data.get("xor_value","") print(f"表达式:{expression}") print(f"提示:{hint}") print(f"乘数:{multiplier}") print(f"异或值:{xor_value}") # 计算token token = calculate_token(expression) print(f"计算得到的token:{token}") exceptExceptionase: print(f"解析响应数据失败:{e}") return # 第二步：发送verify_token请求 print("n发送verify_token请求...") verify_data = {"token": token} verify_response = session.post( f"{base_url}/verify_token", headers=headers, json=verify_data ) # 再次更新cookie（如果有新的） if'session'inverify_response.cookies: session.cookies.set('session', verify_response.cookies['session']) print(f"再次更新session cookie:{verify_response.cookies['session']}") print(f"验证响应状态码:{verify_response.status_code}") print(f"验证响应内容:{verify_response.text}")if__name__ =="__main__": main()


```
importrequestsimportreimportjsondefcalculate_token(expression): """从表达式中计算token值""" # 使用正则表达式提取数字和异或值 match= re.search(r'token = ((d+) * (d+)) ^ (0x[0-9a-f]+)', expression) ifmatch: num1 =int(match.group(1)) num2 =int(match.group(2)) xor_val =int(match.group(3),16) # 计算token: (num1 * num2) ^ xor_val product = num1 * num2 token = product ^ xor_val returntoken else: raiseValueError("无法解析表达式")defmain(): # 基础URL base_url ="https://eci-2ze5w79g3ev2py8ceky2.cloudeci1.ichunqiu.com:
5000" # 初始cookie initial_cookies = { "Hm_lvt_2d0601bd28de7d49818249cf35d95943":"1756542647", "session":".eJxNy00KwyAQQOG7zNqFCok_695DJB2MMGqZjFAovXubnev3vg8cZybCXjC1SVJfVJEh2l1brZZ4SWZJUhtCNG4LzmoX_Hq8x98Z7_3mggIapeAz1Q5ReKKCeSH3fHN4DB7w_QEpuikw.aOM1Xg.UkjBnjZdrYMWyH6SDHw2G3b54ws" } # 创建session对象来保持cookie session = requests.Session() session.cookies.update(initial_cookies) # 设置请求头 headers = { "Sec-Ch-Ua-Platform":""Windows"", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36", "Sec-Ch-Ua":""Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"", "Dnt":"1", "Content-Type":"application/json", "Sec-Ch-Ua-Mobile":"?0", "Accept":"*/*", "Origin": base_url, "Sec-Fetch-Site":"same-origin", "Sec-Fetch-Mode":"cors", "Sec-Fetch-Dest":"empty", "Referer":f"{base_url}/home", "Accept-Encoding":"gzip, deflate, br", "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8", "Priority":"u=1, i" } # 第一步：发送start_challenge请求 print("发送start_challenge请求...") start_response = session.post( f"{base_url}/start_challenge", headers=headers, data="" ) ifstart_response.status_code !=200: print(f"start_challenge请求失败:{start_response.status_code}") return # 更新cookie（使用服务器返回的新session） if'session'instart_response.cookies: session.cookies.set('session', start_response.cookies['session']) print(f"更新session cookie:{start_response.cookies['session']}") # 解析响应数据 try: response_data = start_response.json() expression = response_data.get("expression","") hint = response_data.get("hint","") multiplier = response_data.get("multiplier","") xor_value = response_data.get("xor_value","") print(f"表达式:{expression}") print(f"提示:{hint}") print(f"乘数:{multiplier}") print(f"异或值:{xor_value}") # 计算token token = calculate_token(expression) print(f"计算得到的token:{token}") exceptExceptionase: print(f"解析响应数据失败:{e}") return # 第二步：发送verify_token请求 print("n发送verify_token请求...") verify_data = {"token": token} verify_response = session.post( f"{base_url}/verify_token", headers=headers, json=verify_data ) # 再次更新cookie（如果有新的） if'session'inverify_response.cookies: session.cookies.set('session', verify_response.cookies['session']) print(f"再次更新session cookie:{verify_response.cookies['session']}") print(f"验证响应状态码:{verify_response.status_code}") print(f"验证响应内容:{verify_response.text}")if__name__ =="__main__": main()
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