---
title: idekCTF 2022: NMPZ (OSINT)
contest: idekCTF
year: 2022
difficulty: easy
vuln_type: misc_math
tags: [osint, country-recognition, nmpz, capital-letter, underscore, population]
attack_chain:
  - 1-17.png 17 张图片
  - 判断拍摄国家
  - > 1000 万人国家取首字母大写
  - < 100 万人国家取下划线
  - 100万-1000万国家正常取首字母
  - 拼接成 flag
key_payload: 17 国首字母 + 人口阈值编码
one_liner: idekCTF 2022 NMPZ OSINT 题：17 张图识别国家，按人口阈值决定首字母/下划线。
lesson: 当 OSINT 题目有"阈值规则"时（如人口 > 1000 万），可以用作答案的快速筛选。
quality: medium
---

idekCTF 2022 OSINT 入门题 NMPZ (No Memory, Pure Zeal?)。17 张图，识别每张的拍摄国家，按人口阈值决定编码。

**规则**：
- 国家人口 > 10,000,000 → 首都字母（大写）
- 国家人口 < 1,000,000 → 下划线 `_`
- 其他 → 普通首字母

17 张图 = 17 个国家首字母 / 下划线 → 拼成 flag。

**质量评估**：题目本身入门级，meta 仅作索引。
