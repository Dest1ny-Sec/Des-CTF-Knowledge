---
title: CrewCTF 2023 Writeups
contest: CrewCTF 2023
year: 2023
difficulty: medium
vuln_type: rce
tags: [web, subprocess.dc, filename-injection, deno, ssrf, import-dynamic]
attack_chain:
  - sequence参数传入后+'.dc'作为dc脚本执行
  - 过滤空格+flag关键字但可用其他文件名
  - subprocess.run(['dc', script_file]) 命令注入
  - Deno: import(`http://${PROVIDER_HOST}/?token=...`) SSRF
  - 提供自己的HTTP server返回恶意模块
key_payload: script_file=os.path.basename(sequence+'.dc')
one_liner: CrewCTF 2023两题：dc子进程RCE+Deno动态import SSRF
lesson: os.path.basename+subprocess.run仍有命令注入风险；Deno动态import可被SSRF
quality: low
---

# CrewCTF 2023 Writeups

## 题目信息
- 比赛：CrewCTF 2023
- 类别：Web

## 关键攻击链
### 题目 1：dc 子进程
```python
sequence = request.args.get('sequence', None)
script_file = os.path.basename(sequence + '.dc')
if ' ' in script_file or 'flag' in script_file:
    return ':('
proc = subprocess.run(['dc', script_file], capture_output=True, text=True, timeout=1)
output = proc.stdout
```
- 利用：`os.path.basename` 截断但仍可注入
- 绕过 flag 过滤：换文件名或路径

### 题目 2：Deno 动态 import
```js
const { FLAG } = await import(`http://${PROVIDER_HOST}/?token=${PROVIDER_TOKEN}`);
```
- SSRF：PROVIDER_HOST 可被控制
- 提供恶意 HTTP server，返回构造模块读取 flag
- Deno 模块缓存路径：`/home/app/.cache/deno/{deps,npm,gen,registries}`

## 评分
- quality: low（仅 31 行，纯代码片段 + 简单分析）
