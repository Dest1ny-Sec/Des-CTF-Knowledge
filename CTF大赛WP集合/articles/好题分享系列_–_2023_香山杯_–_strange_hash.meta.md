---
title: 2023 香山杯 strange_hash - Rescue Prime逆运算求CICO
contest: 2023 香山杯 + 2023全国高校密码数学挑战赛赛道一
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags: [Rescue_Prime, CICO, 有限域密码, SageMath, Zmod, 对角矩阵, 逆运算, 矩阵求逆, 求幂, 全国高校密码数学挑战赛, p-1, 模逆]
attack_chain: 解sha256(XXXX+proof[4:]) POW → 提交4元素向量(input[0],input[1],input[2]=0,input[3]=0) → 目标output=vector([1,1,0]) → 倒推:output-Con[3] → ×M^-1 → ×diag(tmp)^2 → -Con[2] → ×M^-1 → ×diag(tmp)^(Inv-1) ... → input = tmp - ConInv
key_payload: Rescue_Prime + diag_matrix(tmp)^2 (平方) + diag_matrix(tmp)^(Inv-1) (1/3次方逆)
one_liner: 香山杯strange_hash倒推Rescue_Prime的2轮运算(input+0让check通过),核心技巧:加→减、乘→逆、幂→对角矩阵^(-1)。
lesson: Rescue_Prime 2轮运算每轮都包含"加Con→乘M→x^3→加Con→乘M→x^(1/3)",逆向时:加→减,乘→×M^-1,三次方→×diag(tmp)^2(因为(x^3)逆=(x^-3),对角化后用^2得x^2),1/3次方→×diag(tmp)^(Inv-1)(因为(x^(1/3))逆=x^(p-1-1/3));末元素是0会在第一次向量加法时被抛掉不影响后续,故可加0凑4元素骗过check。
quality: high
---
