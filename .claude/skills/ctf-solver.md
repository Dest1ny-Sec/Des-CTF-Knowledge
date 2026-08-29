---
name: ctf-solver
description: CTF解题助手。支持5种模式：快速查Payload、找相似WP、推荐工具脚本、技术概念速查、完整攻击方案生成。
---

# CTF 解题助手 v2

你有以下资源可用，**根据用户意图选择最合适的模式**，不要每次都跑完整流程。

## 可用资源速查

| 资源 | 路径 | 何时用 |
|------|------|--------|
| Payload速查表 | `PAYLOAD-CHEATSHEET.md` | 用户要payload/命令时 |
| WP技术标签索引 | `CTF大赛WP集合/wp_technique_index.json` | 搜索相似WP时（630KB, 1156篇） |
| 知识文章(12篇) | `*.md` (非.idx.md) | 需要漏洞原理/bypass技巧时 |
| 文章.idx索引(9篇) | `*.idx.md` | 大文件分段定位，避免全文读取 |
| 大赛WP(1156篇 meta) | `CTF大赛WP集合/articles/*.meta.md` | 需要看具体WP结构化元数据时 |
| 靶场WP | `WP汇总/` | ctfshow/SQLI-LABS等基础靶场 |
| 脚本工具(50+) | `CTF常用脚本及工具/` | 有现成脚本可用时 |
| 工具手册 | `工具使用/` | sqlmap/ffuf/Wireshark用法 |

---

## 五个模式（先判断用户意图，选一个执行）

### 模式1：快速查Payload → 用 PAYLOAD-CHEATSHEET.md

**触发条件**: 用户说"给我XX的payload"、"XX怎么绕"、"XX的命令是什么"

**执行**:
```
1. Read PAYLOAD-CHEATSHEET.md (全文，约200行)
2. 找到对应章节，输出payload
3. 如果用户需要更多上下文，用"来源"字段找到对应知识文章，Read offset=行号 limit=范围 读取更多细节
```

**PAYLOAD-CHEATSHEET.md 章节索引**:
- 一、SQL注入 → 1.1联合/1.2报错/1.3堆叠/1.4盲注/1.5WAF绕过
- 二、命令执行/RCE → 2.1拼接符/2.2空格绕过/2.3关键字/2.4cat替换/2.5无回显/2.6反弹shell/2.7无字母数字
- 三、文件包含 → 3.1伪协议/3.2死亡exit/3.3后缀绕过/3.4日志session/3.5pearcmd
- 四、SSTI → Flask/Jinja2 payloads
- 五、JWT → 算法攻击/KID注入/工具
- 六、SSRF → gopher redis/fastcgi/IP绕过
- 七、文件上传 → 后缀绕过/图片马
- 八、反序列化 → PHP格式/魔术方法/phar
- 九、编码解码 → Base/古典密码/特征识别
- 十、压缩包/图片隐写 → 常用命令

### 模式2：找相似WP → 用 wp_technique_index.json

**触发条件**: 用户说"找几个XX类型的WP"、"有没有做过类似的题"

**执行**:
```python
# 步骤1: 先看wp_technique_index.json的_meta.technique_stats了解标签分布
# 步骤2: 按技术标签精准搜索
python3 -c "
import json
with open('CTF大赛WP集合/wp_technique_index.json') as f:
    data = json.load(f)

# 按标签筛选（从stats选目标标签）
target = 'XXE'  # 替换为实际标签
matches = [(k, v) for k, v in data['articles'].items() 
           if target in v['techniques']]

# 按质量分排序，取Top 5
matches.sort(key=lambda x: -x[1]['quality_score'])
for k, v in matches[:5]:
    print(f'[{v[\"quality_score\"]}] [{v[\"year\"]}] {v[\"title\"][:80]}')
    print(f'  标签: {v[\"techniques\"]}')
    print(f'  比赛: {v[\"competition\"]}')
    print()
"
```

**WP搜索常用标签** (从index的technique_stats中选):
| 要搜的内容 | 使用标签 |
|-----------|---------|
| SQL注入相关 | SQL注入 |
| RCE相关 | 命令执行/RCE |
| 文件上传 | 文件上传 |
| 文件包含 | 文件包含/LFI |
| SSRF | SSRF |
| SSTI | SSTI |
| JWT | JWT |
| 反序列化 | 反序列化 |
| PHP审计 | PHP代码审计 |
| XXE | XXE |
| 原型链污染 | 原型链污染 |
| 条件竞争 | 条件竞争 |
| XSS | XSS |
| CSRF | CSRF |
| Java安全 | Java安全 |
| Nodejs | Nodejs |
| Python安全 | Python安全 |
| 图片隐写 | 图片隐写 |
| 压缩包 | 压缩包 |
| 流量分析 | 流量分析 |
| 编码解码 | 编码解码 |
| RSA | RSA |
| 逆向 | 逆向工程 / APP逆向 |
| PWN | PWN |

**搜到高质量WP后**: 读取1-2篇Top结果的完整内容（Read file_path），提取关键解题思路。

**注意**: 搜索WP内容时仍然可以用grep做补充：
```bash
grep -rl "具体关键词" "CTF大赛WP集合/articles/" --include="*.meta.md" | head -5
```

### 模式3：工具/脚本推荐

**触发条件**: 用户说"这题需要什么工具"、"有没有现成的脚本"

**执行**:
1. 根据题目类型，从下面速查表匹配脚本
2. 列出脚本路径并说明用途
3. 如果脚本目录有多个文件，用 `ls` 查看具体内容

**脚本速查表**:
| 场景 | 脚本路径 | 用途 |
|------|---------|------|
| SQL注入 | 工具使用/sqlmap-Cheat-Sheet.pdf | sqlmap速查 |
| Base编码 | CTF常用脚本及工具/Base/ (8个子目录) | B16/B32/B64/B85/隐写/异或 |
| CRC爆破 | CTF常用脚本及工具/CRC32校验爆破/ | 1-5字节CRC32爆破 |
| PNG宽高 | CTF常用脚本及工具/图片爆破宽高/ | IHDR宽高CRC爆破 |
| 盲水印 | CTF常用脚本及工具/频域盲水印/ | 频域盲水印提取 |
| RSA全套 | CTF常用脚本及工具/RSA综合脚本利用/ (20+子目录) | 各类型RSA攻击 |
| USB流量 | CTF常用脚本及工具/usb流量/ | USB HID键盘数据解析 |
| TTL隐写 | CTF常用脚本及工具/TTL隐写/ | TTL值编解码 |
| 压缩包 | CTF常用脚本及工具/批量解压压缩包+带密码/ | 批量解压+密码爆破 |
| md5爆破 | CTF常用脚本及工具/md5爆破/ | MD5字典/彩虹表 |
| XOR | CTF常用脚本及工具/reverse/xor/ | 异或加解密 |
| 维吉尼亚 | CTF常用脚本及工具/维吉尼亚加密/ | 维吉尼亚解密 |
| 古典密码 | CTF常用脚本及工具/rot/ + 变异凯撒/ + 四方密码/ + Nihilist密码/ | 各类古典密码 |
| steghide | CTF常用脚本及工具/steghide爆破密码/ | steghide密码爆破 |
| 日志匹配 | CTF常用脚本及工具/日志匹配/ | LFI日志包含辅助 |
| DES | CTF常用脚本及工具/DES_Python-master/ | DES加解密 |
| 反序列化 | CTF常用脚本及工具/python-Picke序列化/ | Pickle反序列化 |
| 流量提取 | CTF常用脚本及工具/流量数据提取脚本/ | pcap数据提取 |
| 曼彻斯特 | CTF常用脚本及工具/曼彻斯特编码/ | 曼彻斯特编解码 |
| Brainfuck | CTF常用脚本及工具/Python-Brainfuck-master/ | Brainfuck解释器 |
| 进制转换 | CTF常用脚本及工具/进制互相转换/ + hex倒叙/ + hex减位/ | 各种进制转换 |
| 文件异或 | CTF常用脚本及工具/文件异或/ | 文件级XOR |
| 二维码 | CTF常用脚本及工具/字节转二维码/ + RGB转图片/ | 数据转图像 |
| 字符统计 | CTF常用脚本及工具/字符频率统计分析/ + 去重/ + 字符替换表/ | 文本分析 |
| emoji | CTF常用脚本及工具/emoji/ | emoji-aes加解密 |
| 双参数爆破 | CTF常用脚本及工具/双参数爆破脚本/ | Web参数爆破 |

### 模式4：技术概念速查

**触发条件**: 用户说"XX漏洞是什么"、"XX怎么防御"、"XX的原理"

**执行**:
```
1. 先判断属于哪个知识文章（用下面的映射表）
2. 读对应的 .idx.md 索引文件找到相关行号
3. Read offset=行号 limit=行数 只读目标章节（避免浪费上下文）
```

**知识文章映射表**:
| 题目特征 | 知识文章 | 索引文件 | 行数 |
|---------|---------|---------|------|
| SQL注入/WAF绕过 | SQL.md | SQL.idx.md | 2611 |
| 命令执行/反弹shell/无回显 | 命令执行.md | 命令执行.idx.md | 3463 |
| 文件上传/Webshell | 文件上传漏洞.md | 文件上传漏洞.idx.md | 2115 |
| 文件包含/php伪协议 | 文件包含.md | 文件包含.idx.md | 2617 |
| SSRF/内网/gopher | SSRF漏洞.md | SSRF.idx.md | 1882 |
| PHP反序列化/POP链 | PHP反序列化漏洞总结.md | PHP反序列化漏洞总结.idx.md | 6959 |
| PHP代码审计/弱类型 | php代码审计.md | php代码审计.idx.md | 1641 |
| 图片隐写/LSB/宽高 | 图片隐写.md | 图片隐写.idx.md | 892 |
| 压缩包/CRC/明文攻击 | 压缩包总结.md | 压缩包总结.idx.md | 643 |
| JWT/None算法/KID | JWT.md | JWT.idx.md | 424 |
| SSTI/模板注入 | SSTI.md | — | 270+ |
| 音频隐写/频谱/MP3 | 音频隐写.md | — | 152 |

### 模式5：完整攻击方案

**触发条件**: 用户说"帮我做这道题"、"分析这道CTF"、给了题目代码/描述但没有具体指向

**执行**: 这是唯一需要走完整流程的模式。按以下顺序：

```
步骤1: 题目分析
  - 识别: 题型(Web/Misc/Crypto/Reverse/PWN) + 具体漏洞 + 技术栈
  - 如果题目信息不足，主动问用户要更多信息（题目描述/源码/URL等）

步骤2: 知识检索（用模式4的方法）
  - 读 .idx.md 定位 → Read offset/limit 精确读取相关章节

步骤3: 相似WP搜索（用模式2的方法）
  - 用 wp_technique_index.json 按技术标签搜索
  - 读1-2篇Top质量的WP

步骤4: Payload提取（用模式1的方法）
  - 读 PAYLOAD-CHEATSHEET.md 对应章节
  - 提取适用于当前题目的具体payload

步骤5: 工具推荐（用模式3的方法）
  - 匹配现成脚本

步骤6: 输出结构化方案
```

**方案输出格式**:
```
## 题目分析
- 题型 + 考点 + 技术栈

## 知识要点
[引用文章的具体章节和行号范围]

## 相似WP参考
[引用1-2篇高质量WP的核心思路]

## 攻击步骤
1. ...
2. ...

## 关键Payload
[来自PAYLOAD-CHEATSHEET.md或知识文章的具体payload]

## 可用工具/脚本
[路径 + 用途说明]

## 常见坑点
[从WP和经验中总结]
```

---

## 核心规则

1. **大文件必须用 .idx.md 定位**：SQL.md(2611)、命令执行.md(3463)、PHP反序列化漏洞总结.md(6959)、文件包含.md(2617)、文件上传漏洞.md(2115)、SSRF漏洞.md(1882)。先读 .idx.md 找到行号，再用 offset/limit 精确读取。

2. **WP搜索优先用索引**：`wp_technique_index.json` 精准按技术标签搜索，质量分排序。原始grep只作补充。

3. **Payload优先查速查表**：`PAYLOAD-CHEATSHEET.md` 覆盖10大类常见payload，做题为快不翻文章。

4. **优先推荐现成脚本**：50+脚本直接可用，告诉用户确切路径。

5. **没有知识文章的漏洞类型**：XXE、原型链污染、条件竞争等 → 直接用模式2搜WP，WP中的实战思路就是"知识文章"。

6. **不要每次跑完整流程**：根据用户意图选模式。用户要payload就给payload，别绕圈。
