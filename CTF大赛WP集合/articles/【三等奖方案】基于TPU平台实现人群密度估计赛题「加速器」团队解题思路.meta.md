---
title: CCF BDCI 2022 三等奖 - TPU 人群密度估计 加速器团队
contest: CCF BDCI 2022 (第十届CCF大数据与计算智能大赛)
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [TPU, VGG16, 模型加速, 输入尺度, batch_size, BMODEL, 算能芯片, 图像预处理]
attack_chain: 选定VGG → 试不同batch size → 调整预处理图片最大/最小尺寸 → 调整模型输入尺寸 → 找到最佳组合
key_payload: VGG + 预处理最大780×780 + 最小144×144 + 模型输入144×144
one_liner: 高级工程师单挑用VGG+精确尺寸组合在算能TPU上拿下三等奖。
lesson: 模型加速首先选对基础模型 — 直接转FP32bmodel对比4个模型(CANNet/CSRNet/MCNN/VGG)选VGG;batch_size从1换8反而速度加倍,故放弃;预处理图片最大/最小尺寸+模型输入尺寸的组合对最终成绩影响最大。
quality: medium
---
