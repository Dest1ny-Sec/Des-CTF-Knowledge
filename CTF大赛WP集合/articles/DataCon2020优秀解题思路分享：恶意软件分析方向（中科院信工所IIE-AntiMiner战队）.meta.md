---
title: DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）
contest: DataCon 2020
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags: [malware, lief, section-entropy, regex, bitcoin-wallet, function-pattern, cfg]
attack_chain:
  - 用LIEF库解析PE section属性
  - 统计R/W/X section size和熵均值
  - rsrc section个数
  - 正则提取: 路径[C-Zc-z]:/、reg/、url、IP、btc/ltc/xmr钱包
  - MZ/PE/coin/cpu/gpu/pool等模式
  - m32_pattern: \x55\x8b\xec[^\xc3]*\xc3 函数识别
  - capstone反汇编得操作码序列
  - graphviz生成CFG可视化
key_payload: m32_pat = re.compile(b'\x55\x8b\xec[^\xc3]*\xc3')  # 函数头
one_liner: DataCon2020恶意软件分析：LIEF+正则+CFG图可视化
lesson: PE section熵+操作码序列+CFG是恶意软件家族分类特征
quality: high
---

# DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）

## 题目信息
- 比赛：DataCon 2020
- 方向：恶意软件分析
- 战队：中科院信工所 IIE-AntiMiner

## 关键攻击链
### 1. PE 静态特征提取
```python
import lief
binary = lief.parse(path)
entry_section = binary.entrypoint.section
section_info["entry"] = len(entry_section)
section_info["section_num"] = len(binary.sections)
sR, sW, sX = [], [], []
entrR, entrW, entrX = [], [], []
rsrc_num = 0
for s in binary.sections:
    props = [str(c).split('.')[-1] for c in s.characteristics_lists]
    if "MEM_READ" in props:
        sR.append(s.size); entrR.append(s.entropy)
    if "MEM_WRITE" in props:
        sW.append(s.size); entrW.append(s.entropy)
    if "MEM_EXECUTE" in props:
        sX.append(s.size); entrX.append(s.entropy)
    if 'rsrc' in s.name:
        rsrc_num += 1
```

### 2. 关键模式正则
- 路径：`[C-Zc-z]:(?:(?:\\\\|/)[^\\\\/:*?"<>|"\x00-\x19\x7f-\xff]+)+(?:\\\\|/)?`
- URL：`https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+`
- IP：标准 0-255 段
- BTC 钱包：`(?:1|3|bc1|bitcoincash:q)(?:(?![0OIi])[0-9A-Za-z]){25,34}`
- LTC：`ltc1|M|L[A-Za-z0-9]{25,36}`
- XMR：`[0-9A-Za-z]{90,100}` 门罗币
- 矿池相关：`pool|cpu|gpu|coin` 大小写不敏感

### 3. 函数级特征
- `m32_pat = re.compile(b'\x55\x8b\xec[^\xc3]*\xc3')` # 32 位函数头尾
- capstone 反汇编得操作码序列
- `function_op.append(self.opcode_dict[mnemonic])`

### 4. CFG 图可视化
- graphviz IDA palette 配色
- node: title="165" label="__aulldiv" color=75
- edge: sourcename → targetname

## 评分
- quality: high（PE 静态分析 + 函数操作码 + CFG 可视化完整特征工程）
