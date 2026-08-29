---
title: 可信度量赛题官方WP - TCM PCR寄存器+SM3摘要+可信报告防重放
contest: 全国大学生信息安全竞赛(信安国赛) + 伽玛实验场
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags: [可信计算, TCM, PCR寄存器, 可信度量, SM3, 防重放, nonce, quote_report, 主动可信免疫, key_manage, 4种策略组合, 16种枚举, NEX, F1sh, 北工大]
attack_chain: 检查quote_report->nonce == external_data_store(防重放) → 检查pcrValue == empty_digest(全0则无策略) → 遍历memdb获取4种策略(科研/生产/测试/公开)摘要值 → 16种组合(0-15,每位bit对应一策略) → SM3(oldPcrValue||digestValue)扩展 → 与quote_report->pcrValue对比 → 拼接成"策略1|策略2"
key_payload: SM3(PCR旧值||digestValue) + 2^4=16种组合 + calculate_context_sm3(buf,len,out)
one_liner: 北工大胡俊老师设计信安国赛可信度量题,3队解出:东北大学NEX一血/F1sh二血/北工大三血。
lesson: 可信计算TCM PCR寄存器写入原理:newPcrValue = SM3(oldPcrValue||digestValue);4种策略(科研/生产/测试/公开)2^4=16种组合;防重放:比对external_data_store中的预期nonce与quote_report->nonce;NEX一血用VSCode Remote-SSH插件直接连环境;memdb哈希表存储与查询次序无关需按策略名排序存数组。
quality: high
---
