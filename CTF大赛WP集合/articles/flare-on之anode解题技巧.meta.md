---
title: flare-on 之 anode 解题技巧
contest: FLARE-ON
year: 2018
difficulty: medium
vuln_type: reverse
tags: [nodejs, nexe, js-extract, switch-fsm, bigint-truthy, state-machine]
attack_chain:
  - 识别 NEXE 打包的 NodeJS 可执行
  - 十六进制编辑搜 "Enter flag" 特征字符串
  - 提取 JS 源码
  - 解读 44 字节输入 → 16 个 long state 状态机
  - state = 1337; state ^= random(2^30)
  - switch(state) 跳转
  - 大数 1n / 93909087n 永真 → 走 if 分支
  - 逆推 b[i] 异或/加减
  - 对比 target 数组
key_payload: NEXE 提 JS 源码 + 长 switch 状态机逆推
one_liner: FLARE-ON anode NodeJS NEXE 打包逆向，从十六进制编辑提取 JS 源码 + 状态机逆推。
lesson: NEXE 把 JS 源码直接打包进 EXE（无加密无压缩），十六进制编辑就能还原。
quality: high
---

FLARE-ON 之 anode 题解题技巧（来源 ctfiot）。

**类型判断**
Anode 是 FLARE-ON 经典题，请求用户输入 44 字节 flag，判断是否正确。从 IDA 信息可知：NodeJS 编写 + NEXE 打包成 EXE。

**源码提取（关键步骤）**
NEXE 把 JS 源码直接打包到 EXE 中，**不经过加密或压缩**。用十六进制编辑工具搜特征字符串 `Enter flag` 就能定位源码位置。

**JS 逻辑**
```javascript
readline.question(`Enter flag: `, flag => {
    if (flag.length !== 44) { console.log("Try again."); process.exit(0); }
    var b = [];
    for (var i = 0; i < flag.length; i++) b.push(flag.charCodeAt(i));
    if (1n) { console.log("uh-oh, math is too correct..."); process.exit(0); }
    
    var state = 1337;
    while (true) {
        state ^= Math.floor(Math.random() * (2**30));
        switch (state) {
            case 306211:
                if (Math.random() < 0.5) {
                    b[30] -= b[34] + b[23] + b[5] + b[37] + b[33] + b[12] + Math.floor(Math.random() * 256);
                    b[30] &= 0xFF;
                } else {
                    b[26] -= b[24] + b[41] + b[13] + b[43] + b[6] + b[30] + 225;
                    b[26] &= 0xFF;
                }
                state = 868071080;
                continue;
            // ... 省略 100+ case
            case 1071767211:
                if (Math.random() < 0.5) { ... } else { ... }
                state = 109621765;
                continue;
            default:
                console.log("uh-oh, math.random() is too random...");
                process.exit(0);
        }
        break;
    }
    
    var target = [106, 196, 106, 178, 174, 102, 31, 91, 66, 255, 86, 196, 74, 139, 219, 166, 106, 4, 211, 68, 227, 72, 156, 38, 239, 153, 223, 225, 73, 171, 51, 4, 234, 50, 207, 82, 18, 111, 180, 212, 81, 189, 73, 76];
    if (b.every((x,i) => x === target[i])) console.log('Congrats!');
});
```

**解法要点**
1. `1n` / `93909087n` 是 BigInt，永真 → `if (1n)` 永远走 if 分支
2. 每个 case 都是 `b[i] = b[i] ± b[j] + ...`
3. 状态机长度固定，最后 b[] 与 target[] 比较
4. 从 target 反推：先还原 case 顺序，然后从后往前逆运算

**坑点**
- 状态跳转是 `state = X; continue;` 形成确定性 FSM（不走 default）
- Math.random() 在 case 分支选择中影响 if/else（但 `1n` 永真只走 if）
- 写逆推脚本前要先把所有 case 整理出来按 case state 排序

**flag 长度 44 字符**，可解。
