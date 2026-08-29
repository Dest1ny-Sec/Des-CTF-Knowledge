---
title: NepnepxCATCTF 部分 WriteUp (MISC 6 题速查)
contest: NepnepxCATCTF
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [vmdk flag 搜索, QQ 空间 OSINT, DeepSound 隐写, rabbit+Ook 编码, png 隐藏密文]
attack_chain: |
  1. Cat_Jump (MISC):
     - 16 进制编辑器打开 vmdk 文件
     - 搜索 "CatCTF{" 字符串
     - flag: CatCTF{EFI_1sv3ry_funn9}
  2. Peekaboo (OSINT):
     - jpg 文件尾部找到 QQ 号
     - 访问 QQ 空间 → 王者荣耀登录
     - 看打野英雄数据 (百里玄策 = 唯一用过的)
     - flag: CatCTF{bailixuance}
  3. miao~ (隐写):
     - jpg 尾手动分离 wav
     - audacity 看频谱图 → DeepSound 工具解密
     - 密码 "CatCTF" → flag.txt → 兽语密码 (http://hi.pcmoe.net/roar.html)
     - flag: CatCTF{d0_y0u_Hate_c4t_ba3k1ng_?_M1ao~}
  4. CatCat (编码):
     - 文件名 rabbit → sojson rabbit 解密 (需密码)
     - jpg 010Editor 搜 password → 密码 "catflag"
     - rabbit 解出 → base91 解码 → Ook 密码 (cat→Ook)
     - https://www.splitbrain.org/services/ook
     - flag: CatCTF{Th1s_V3ry_cute_catcat!!!}
  5. MeowMeow (png 隐写):
     - png 文件 010Editor 看尾部
     - 3 段密文 → 拼成 CatCTF{CAT_GOES_MEOW}
     - flag: CatCTF{CAT_GOES_MEOW}
  6. CatchCat (待补)
key_payload: |
  # Cat_Jump:
  # 16 进制编辑器打开 vmdk, 搜 "CatCTF{" → CatCTF{EFI_1sv3ry_funn9}
  
  # miao~:
  # jpg 尾 wav (audacity 频谱) + DeepSound (密码 CatCTF) → flag.txt
  # 兽语密码: http://hi.pcmoe.net/roar.html
  # CatCTF{d0_y0u_Hate_c4t_ba3k1ng_?_M1ao~}
  
  # CatCat:
  # sojson rabbit 解密 (密码 catflag) → base91 → Ook 密码
  # https://www.splitbrain.org/services/ook
  # CatCTF{Th1s_V3ry_cute_catcat!!!}
  
  # MeowMeow:
  # png 010Editor 看尾 → 3 段密文 → CatCTF{CAT_GOES_MEOW}
one_liner: NepnepxCATCTF 部分 WriteUp: 6 道 MISC 速查 (vmdk flag 搜索 / QQ 空间 OSINT / DeepSound 兽语 / rabbit+Ook 编码 / png 隐藏)。
lesson: |
  - vmdk 文件可以 16 进制搜 flag 字符串
  - QQ 空间 OSINT + 王者荣耀打野英雄数据
  - DeepSound 是常用音频隐写工具 (密码 "CatCTF")
  - rabbit 加密 (sojson) + base91 + Ook 密码是编码题三件套
  - png 文件尾部 010Editor 看 hex
quality: medium
---

# NepnepxCATCTF 部分 WriteUp

> 来源: ctfiot.com 89555 - 天权信安网络安全团队

## 6 道 MISC 速查

### 01. Cat_Jump
16 进制编辑器打开 vmdk 文件 → 搜 `CatCTF{` 字符串 → `CatCTF{EFI_1sv3ry_funn9}`

### 02. Peekaboo
- jpg 文件尾部找到 QQ 号
- 访问 QQ 空间 → 王者荣耀登录
- 看打野英雄数据 (百里玄策 = 唯一用过的)
- `CatCTF{bailixuance}`

### 03. miao~
- jpg 尾手动分离 wav
- audacity 频谱图分析
- **DeepSound** 工具解密 (密码 "CatCTF")
- flag.txt 兽语密码 (http://hi.pcmoe.net/roar.html)
- `CatCTF{d0_y0u_Hate_c4t_ba3k1ng_?_M1ao~}`

### 04. CatCat
- 文件名 rabbit → sojson rabbit 解密 (需密码)
- jpg 010Editor 搜 password → 密码 "catflag"
- rabbit 解出 → base91 解码 → Ook 密码 (cat→Ook)
- https://www.splitbrain.org/services/ook
- `CatCTF{Th1s_V3ry_cute_catcat!!!}`

### 05. MeowMeow
- png 文件 010Editor 看尾部
- 3 段密文 → 拼成 `CatCTF{CAT_GOES_MEOW}`

### 06. CatchCat (待补)

## 评价

NepnepxCATCTF MISC 6 题速查，亮点是：
- **vmdk 16 进制搜字符串** 是取证入门技巧
- **QQ 空间 OSINT + 王者荣耀** 是国内 OSINT 特色
- **DeepSound 音频隐写** + 兽语密码组合
- **rabbit + base91 + Ook 密码** 编码三件套

适用读者：MISC 入门 / OSINT 入门 / 国产 CTF
