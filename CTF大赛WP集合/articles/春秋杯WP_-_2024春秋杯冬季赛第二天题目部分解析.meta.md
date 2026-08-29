---
title: 春秋杯WP | 2024春秋杯冬季赛第二天题目部分解析
contest: 春秋杯2024冬季赛
year: 2024
difficulty: medium
vuln_type: misc_math
tags: [Python沙箱逃逸, 生成器栈帧, 字符高尔夫, Unpacking assignment, Pyhumor, Python虚拟机逆向, RSA]
attack_chain: python_jail:生成器gi_frame.f_back.f_back.f_back.f_back.f_globals['BOX']→golf revenge:46字符生成1000以内质数→right_data:模数257线性方程组逆推→Pyhumor:Python VM逆向取30bit值→cpy/easy_http/b0okshelf/mygo/factor/skip/Nu1tka
key_payload: "def b(): def a(): yield g.gi_frame.f_back.f_back.f_back.f_back; g=a();g=[x for x in g][0]; return g.f_globals['BOX'];k,P,*s=1,1,;while k<1e3:s+=P%k*[k];P*=k*k;k+=1"
one_liner: 春秋杯2024冬季赛D2十题混合：Python jail+字符高尔夫+线性方程组+PyVM逆向
lesson: Python沙箱逃逸核心：生成器gi_frame+f_back回溯+f_globals取全局；字符高尔夫用Unpacking+s+=P%k*[k]
quality: high
---

# 春秋杯WP | 2024春秋杯冬季赛第二天题目部分解析

**赛事**：春秋杯2024冬季赛 Day 2

**包含题目**：python_jail / golf_revenge / right_data / Pyhumor / cpy / easy_http / b0okshelf / mygo / factor / skip / Nu1tka

**关键题目解析**：

**1. python_jail（生成器栈帧逃逸）**
```python
def b():
  def a():
    yield g.gi_frame.f_back.f_back.f_back.f_back
  g = a(); g = [x for x in g][0]
  return g.f_globals['BOX']
s = b()
```
- 利用生成器 `gi_frame` 栈帧对象
- 连续 `f_back` 回溯到外层frame
- 最终通过 `f_globals` 访问全局符号表 `BOX`

**2. golf revenge（46字符生成1000以内质数）**
```python
k,P,*s=1,1,
while k<1e3:s+=P%k*[k];P*=k*k;k+=1
```
- Unpacking assignment压缩 `k=1;P=1;s=[]`
- `s+=P%k*[k]` 巧用空list追加不改变
- 布尔短路代替if判断
- `1e3` 代替 1000

**3. right_data（线性方程组逆推）**
- 模数 257
- 65792个方程 (i*coefs1[j] + j*coefs2[j]) % 257 == values[j]
- findflag遍历i,j，找满足所有方程的解
- flag字符: `chr((j - i) % 257)`
- flag: `flag{087834ea-dcbf-488a-a713-e496b3130d40}`

**4. Pyhumor（Python VM逆向）**
- IDA定位check函数 → attach动调
- flag长度 = 40
- 两个数组（长度5+4）从内存取值
- 注意PyVM每32bit只存30bit → 自行转换
- 数组：
  ```
  [0xfbbc7f84591ff393, 0x360c751ee6bd9abd, 0x60854fc80d82350a, 
   0x139692ebf3ee3c4f, 0x8571b17650a42bd4]
  [0xf656460d, 0xda144260, 0xeef1c943, 0xe4390f66]
  ```

**5-10. cpy / easy_http / b0okshelf / mygo / factor / skip / Nu1tka**：
- 在本WP中部分涉及，详情略

**技术总结**：
- Python沙箱逃逸：生成器栈帧 + f_back回溯
- 字符高尔夫：Unpacking + 短路逻辑 + 1e3数值简写
- PyVM逆向注意30bit存储特性

**质量评估**：高（多题payload + 完整exp）
