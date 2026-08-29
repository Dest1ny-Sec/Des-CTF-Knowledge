---
title: CCF BDCI 2022 三等奖 - TPU 人群密度估计 innovation 团队
contest: CCF BDCI 2022 (第十届CCF大数据与计算智能大赛)
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [TPU, 人群密度估计, VGG, CSRNet, MCNN, INT8量化, BMODEL, 图像增强, 算能芯片, 模型部署]
attack_chain: 选VGG模型 → 转为int8bmodel格式 → 量化校准230次迭代 → 测试图像旋转/缩放至576×768 → 锐度+亮度1.5倍增强 → 推理精度+速度联合优化
key_payload: VGG-INT8 + 576×768 + 锐度×1.5 + 亮度×1.5
one_liner: 台州学院innovation团队用VGG-INT8+图像增强在算能TPU上B榜第五。
lesson: 模型选择需兼顾精度和泛化 — A榜10张图选VGG，到A榜1201张MCNN精度严重下滑；量化迭代次数对精度影响不大(趋于平稳)；图像预处理(尺寸+锐度+亮度组合)对最终FINAL_SCORE贡献最大。
quality: high
---
