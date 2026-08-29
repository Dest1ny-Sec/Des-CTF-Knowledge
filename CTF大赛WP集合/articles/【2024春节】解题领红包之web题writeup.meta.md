---
title: 2024 春节 解题领红包之 web 题 writeup
contest: 2024 春节活动 (52pojie)
year: 2024
difficulty: easy
vuln_type: [misc_math, web_unknown]
tags: [52pojie, 春节活动, ASCII-art, banner, banner-grab, slider, CSS-variable, LCG, mod-inverse, egcd, JavaScript-decode]
attack_chain: ["Q1: netcat 124.232.185.97 2024challenge.52pojie.cn → 抓 ASCII 艺术", "从 ASCII 字符形状读出 flag: flag{5P3rF1ag3}", "Q2: 网页有 slider1/slider2 → 改 --var1=71 --var2=20", "读 num = 1213159497, while 循环 num & 0xff 转字符 → flag12{...}", "Q3: LCG 模逆 1103515245 模 2^32 → modinv = pow(1103515245, -1, 2**32)", "Q4: 18464037713 × 999063388 验证 2^65 范围爆破"]
key_payload: "flag{5P3rF1ag3} / flag12{...}"
one_liner: 2024 春节 web：ASCII art 读字 + CSS slider + LCG 模逆 + 大数因子
lesson: netcat 抓 banner 读字；CSS 变量 + slider 是 web 入门；LCG 模逆是密码学入门
quality: medium
---

# 2024 春节 解题领红包之 web 题 writeup

原文 https://www.ctfiot.com/165808.html （52pojie 春节活动）

## Q1: ASCII Banner
```bash
nc 124.232.185.97 2024challenge.52pojie.cn
```
- 拿到 ASCII 艺术字符
- 从字符形状读出：
  ```
  flag{5P3rF1ag3}
  ```

## Q2: CSS Slider 解码
```html
<label for="slider1">Variable 1:</label>
<input id="slider1" type="range" />
<label for="slider2">Variable 2:</label>
<input id="slider2" type="range" />

<script>
document.getElementById('slider1').addEventListener('input', function () {
    document.documentElement.style.setProperty('--var1', this.value);
});
document.getElementById('slider2').addEventListener('input', function () {
    document.documentElement.style.setProperty('--var2', this.value);
});
</script>

:root {
    --var1: 71;
    --var2: 20;
}
```
```js
let num = 1213159497;
let str = '';
while (num > 0) {
    str = String.fromCodePoint(num & 0xff) + str;
    num >>= 8;
}
console.log(`flag12{${str}}`);
```

## Q3: LCG 模逆
```python
def egcd(a, b):
    if a == 0: return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('无解')
    return x % m

# 计算 1103515245 模 2^32 的逆元
modulus = 2**32
a = 1103515245
inverse_a = modinv(a, modulus)
print("结果:", inverse_a)
```

## Q4: 大数因子
```python
>>> (pow(2,31)-1) / 999063388
2.149496891582619
>>> (pow(2,63)-1) / 999063388
9232018856.5
>>> bin(18464037713*999063388)
'0b10000000000000000000000000000000000000000000000000000000000011100'
>>> bin(28)
'0b11100'
```

## 教学价值
- **netcat 抓 banner** 入门 MISC
- **CSS 变量 + slider** 入门 web interactive
- **JS num 转字符** while + bit shift
- **LCG** (Linear Congruential Generator) 经典 PRNG
- **模逆** (Modular Inverse) egcd / pow(a,-1,m)
- **大数因子** 算术 + bin 观察

## 工具
- netcat
- 浏览器 DevTools
- Python math
- bin/hex/dec 转换
