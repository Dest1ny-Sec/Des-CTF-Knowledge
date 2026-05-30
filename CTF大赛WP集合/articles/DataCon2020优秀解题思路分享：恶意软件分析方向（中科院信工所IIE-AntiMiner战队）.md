# DataCon2020优秀解题思路分享：恶意软件分析方向（中科院信工所IIE-AntiMiner战队）

> 原文: https://www.ctfiot.com/75697.html
> ID: 75697


```
# OEP处section名长度
section_info["entry"] = len(entry_section)
section_info["section_num"] = len(lief_binary.sections)
# 可读、可写、可执行sections大小均值
sR, sW, sX = [], [], []
# 可读、可写、可执行sections熵值均值
entrR, entrW, entrX = [], [], []
# 资源section个数
rsrc_num = 0
for s in lief_binary.sections:
 props = [str(c).split('.')[-1] for c in s.characteristics_lists]
 if "MEM_READ" in props:
 sR.append(s.size)
 entrR.append(s.entropy)
 if "MEM_WRITE" in props:
 sW.append(s.size)
 entrW.append(s.entropy)
 if "MEM_EXECUTE" in props:
 sX.append(s.size)
 entrX.append(s.entropy)
 if 'rsrc' in s.name:
 rsrc_num += 1
section_info['size_R'], section_info['size_W'], section_info['size_X'] = np.mean(sR), np.mean(sW), np.mean(sX)
section_info['entr_R'], section_info['entr_W'], section_info['entr_X'] = np.mean(entrR), np.mean(entrW), np.mean(entrX)
section_info['rsrc_num'] = rsrc_num
self.path_pattern = re.compile(b'[C-Zc-z]:(?:(?:\\\\|/)[^\\\\/:*?"<>|"\x00-\x19\x7f-\xff]+)+(?:\\\\|/)?')
self.regs_pattern = re.compile(b'reg', re.IGNORECASE)
# re.compile(b'[A-Z_ ]{5,}(?:\\\\[a-zA-Z ]+)+')
self.urls_pattern = re.compile(b'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
# self.strings_pattern = re.compile(b'[\x20-\x7f]{5,}')
self.ip_pattern = re.compile(b'(?:(?:25[0-5]|2[0-4]\d|[01]?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d{1,2})')
​
# #比特币钱包地址
self.wallet_pattern_btc = re.compile(b'(?:1|3|bc1|bitcoincash:q)(?:(?![0OIi])[0-9A-Za-z]){25,34}')
self.wallet_pattern_ltc = re.compile(b'(?:
ltc1|M|L)[A-Za-z0-9]{25,36}')
self.wallet_pattern_xmr = re.compile(b'[0-9A-Za-z]{90,100}') #门罗币
​
self.mz_pattern = re.compile(b'MZ')
self.pe_pattern = re.compile(b'PE')
self.pool_pattern = re.compile(b'pool', re.IGNORECASE)
self.cpu_pattern = re.compile(b'cpu', re.IGNORECASE)
self.gpu_pattern = re.compile(b'gpu', re.IGNORECASE)
self.coin_pattern = re.compile(b'coin', re.IGNORECASE)
self.m32_pat = re.compile(b'\x55\x8b\xec[^\xc3]*\xc3')
# …………
all_functions = self.m32_pat.findall(binary)
for function in all_functions:
 function_op = []
 for _, _, mnemonic, _ in self.md32.disasm_lite(function, 0x0):
 try:
 function_op.append(self.opcode_dict[mnemonic])
 
except Exception:
 break
 else:
 op_pattern.append(function_op)
graph: {
title: "Building graph"
// IDA palette
// ....
colorentry 71: 255 255 0
colorentry 72: 0 0 0
colorentry 73: 0 0 0
colorentry 74: 0 0 0
colorentry 75: 0 255 255
colorentry 76: 192 192 192
// ....
node: { title: "165" label: "__aulldiv" color: 75 textcolor: 73 bordercolor: black }
node: { title: "166" label: "__aulldvrm" color: 75 textcolor: 73 bordercolor: black }
node: { title: "167" label: "__aullshr" color: 75 textcolor: 73 bordercolor: black }
// ....
// node 169
edge: { sourcename: "169" targetname: "135" }
edge: { sourcename: "169" targetname: "136" }
edge: { sourcename: "169" targetname: "170" }
edge: { sourcename: "169" targetname: "171" }
// ....
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6375d4b622a7c.png)