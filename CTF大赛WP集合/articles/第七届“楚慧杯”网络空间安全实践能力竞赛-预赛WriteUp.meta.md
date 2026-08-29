---
title: 第七届"楚慧杯"网络空间安全实践能力竞赛-预赛WriteUp
contest: 第七届楚慧杯预赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [楚慧杯预赛, mobile/misc/crypt, AES解密, VeraCrypt容器, BitLocker加密卷, stegsolve LSB, passware, CRC改高度]
attack_chain: mobile:level_one(直接看)→level_up AES解密→crypt:VeraCrypt容器从jpg FFD9后提取→secret:BitLocker+改图片高度+stegsolve→pocky:hex写新文件
key_payload: "flag{380605c6-7123-4f71-b573-601e8c4457b4};flag{6b1df900-1284-11ed-9fa7-5405dbe5e745};flag{4ba7689c6dee7749403380b11c416de6};flag{b6aa5b40559fc9762918cd32f5f6bd0f};password1=OXi password2=ChaiYan;620224-121649-497585-220572-660704-152383-484957-174713"
one_liner: 第七届楚慧杯预赛：mobile AES+misc VeraCrypt+BitLocker+stegsolve+改CRC
lesson: 综合取证常用：FFD9后藏文件+改图片高度+BitLocker密码恢复+stegsolve提取
quality: medium
---

# 第七届"楚慧杯"网络空间安全实践能力竞赛-预赛WriteUp

**赛事**：第七届楚慧杯预赛（2022）

**Mobile方向**：

**level_one**：直接读
- flag: `flag{380605c6-7123-4f71-b573-601e8c4457b4}`

**level_up**：AES解密
- 结果：`flag{6b1df900-1284-11ed-9fa7-5405dbe5e745}`

**Misc方向**：

**crypt**（VeraCrypt容器）：
- jpg文件尾 FFD9 后另存为vc容器
- VeraCrypt挂载容器
- 资源管理器看不到文件，用X-Ways打开
- flag: `flag{4ba7689c6dee7749403380b11c416de6}`

**secret**（BitLocker加密卷）：
- 镜像内一个BitLocker加密卷
- 图片crc不正确 → 改图片高度拿 password1 = `OXi`
- stegsolve找 password2 = `ChaiYan`
- passware跑出密钥：
  ```
  620224-121649-497585-220572-660704-152383-484957-174713
  ```
- 生成解密后的镜像文件
- 或者取证大师用 `OXiChaiYan` 直接解密
- 明文攻击
- flag: `flag{b6aa5b40559fc9762918cd32f5f6bd0f}`

**pocky**：
- hex用winhex写到新文件
- 发现jpg尾部有压缩包数据

**质量评估**：中（综合取证+密码学，4个flag完整）
