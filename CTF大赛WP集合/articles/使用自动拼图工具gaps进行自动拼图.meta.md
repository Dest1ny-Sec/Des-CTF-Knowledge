---
title: 使用自动拼图工具 gaps 进行自动拼图
contest: CTF练习
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [gaps, puzzle-solver, genetic-algorithm, montage, ImageMagick, 600-pieces, automatic-puzzle, MISC]
attack_chain:
  - 600 张 40×40 PNG 图片，无规律命名
  - Step 1: 安装 ImageMagick + GraphicsMagick + montage 拼接
  - montage ./files/*.png -tile 20X30 -geometry +0+0 flag.png
  - 或尝试 30X20 排列
  - Step 2: 安装 poetry + tk + gaps (https://github.com/nemanja-m/gaps)
  - Step 3: gaps run ./flag.png resolve.png --size=40 --generations=20 --population=200
  - Step 4: 调整 tile 维度再跑一次
  - Step 5: 增加迭代: --generations=400 --population=400 --size=40
  - 输出 resolved puzzle image
key_payload: 'gaps run puzzle.png solution.png --size=40 --generations=400 --population=400'
one_liner: MISC 拼图题 600 张 40×40：montage 拼接 + gaps 遗传算法自动拼图，--generations=400 --population=400 增加迭代。
lesson: gaps 是 CTF MISC 拼图题必备工具，遗传算法自动求解；montage 用于快速拼接预览。
quality: medium
---

# 使用自动拼图工具 gaps 进行自动拼图

**来源**: ctfiot.com ID 162924

## 题目
- 600 张 40×40 PNG 图片
- 图片名称无规律
- 手动拼图尝试次数太大

## 工具链

### 1. 安装依赖
```bash
apt-get install -y graphicsmagick-imagemagick-compat
curl -sSL https://install.python-poetry.org | python3 -
sudo apt-get install python-tk
git clone https://github.com/nemanja-m/gaps
cd gaps
pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. montage 拼接
```bash
montage ./files/*.png -tile 20X30 -geometry +0+0 flag.png
# 或调整
montage ./files/*.png -tile 30X20 -geometry +0+0 flag.png
```

### 3. gaps 自动拼图
```bash
# 基础
gaps run ./flag.png resolve.png --generations=20 --population=200 --size=40

# 增加迭代
gaps run ./flag.png resolve.png --generations=400 --population=400 --size=40
```

## gaps 命令选项
- `-s, --size INTEGER`：单块拼图尺寸（像素），自动检测
- `-g, --generations INTEGER`：遗传算法迭代次数（默认 20）
- `-p, --population INTEGER`：初始种群大小（默认 200）
- `-d, --debug`：每代显示最佳个体

## 评价
MISC 拼图题入门到进阶：montage 工具拼接 + gaps 遗传算法自动求解。是 CTF MISC 必备工具。
