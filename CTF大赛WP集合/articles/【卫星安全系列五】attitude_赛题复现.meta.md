---
title: 【卫星安全系列五】attitude 赛题复现
contest: Hack-A-Sat 2020 attitude
year: 2023
difficulty: hard
vuln_type: misc_math
tags: [卫星姿态, 四元数, 旋转矩阵, Kabsch算法, rmsd库, scipy.spatial.transform.Rotation, 恒星追踪, 卡尔曼]
attack_chain:
  - 题目: 给 2500 行恒星 (X,Y,Z,星等) 参考向量 dataA_list
  - nc 拿到 4 浮点观测向量 (id, x, y, z)
  - 卫星姿态: 星体坐标系 → 惯性坐标系 旋转关系
  - 描述方式: 旋转矩阵 / 四元数 (q=[w,x,y,z]) / 欧拉角 / DCM / 轴角
  - Kabsch 算法: 中心化 + 协方差矩阵 + SVD 分解 + 旋转矩阵
  - pip install rmsd 库
  - R = rmsd.kabsch(A, B) 计算最优旋转
  - sol = Rotation.from_matrix(R).as_quat() 矩阵转四元数
  - 发送 ','.join(str(x) for x in sol) 四元数
  - 重复 20 次验证通过
key_payload: 'rmsd.kabsch + scipy Rotation.as_quat() 四元数'
one_liner: 卫星姿态 attitude: 2500 恒星向量 + Kabsch 算法 SVD 旋转矩阵 + 四元数提交 20 次。
lesson: 卫星姿态用四元数 (w,x,y,z) 表示避免万向锁；Kabsch 算法通过 SVD 找两组点集最佳旋转；rmsd 库 + scipy.spatial.transform.Rotation 是 Python 卫星题双神器。
quality: high
---

# 【卫星安全系列五】attitude 赛题复现

## 概览
- **来源**: ctfiot 153356 (Hack-A-Sat 2020 Qualifier)
- **类型**: 卫星姿态 + 旋转矩阵 + 四元数
- **难度**: ⭐⭐⭐⭐

## 题目
- `test.txt`: 2500 行恒星天球坐标 (X, Y, Z, 星等)
- nc 后端返回追踪器观测向量 (id, x, y, z)
- 提交四元数 (w, x, y, z) 描述卫星姿态
- 20 次验证通过

## 卫星姿态表示
| 方式 | 说明 |
|------|------|
| 旋转矩阵 | 3×3 正交矩阵, 行列式 = 1 |
| 四元数 | q = [w, x, y, z], 避免万向锁 |
| 欧拉角 | Roll/Pitch/Yaw 三角度 |
| DCM | 方向余弦矩阵 |
| 轴角 | 单位向量 + 旋转角 |

## Kabsch 算法
1. 中心化两组点集 (减去质心)
2. 计算协方差矩阵 H = A^T @ B
3. SVD 分解 H = U S V^T
4. d = sign(det(V U^T)), R = V diag(1, 1, d) U^T
5. 最小化 RMSD 的旋转矩阵

## EXP
```python
import numpy as np
from scipy.spatial.transform import Rotation
import rmsd
from pwn import *

# 读取参考星 dataA_list
def get_dataAlist():
    with open("test.txt", "r") as f:
        data = f.readlines()[:-1]
    return [[float(n) for n in t.split(",")] for t in data]

def cal_matrix(stars):
    v_ref, v_obs = [], []
    for idx, x, y, z in stars:
        v_ref.append([dataAlist[idx][0], dataAlist[idx][1], dataAlist[idx][2]])
        v_obs.append([x, y, z])
    A, B = np.array(v_ref), np.array(v_obs)
    R = rmsd.kabsch(A, B)
    sol = Rotation.from_matrix(R).as_quat()
    return ','.join(str(x) for x in sol)

def recvdata():
    res = p.recvuntil(b"\n\n").split(b"\n")
    lines = []
    for line in res:
        if b'0.' in line:
            id = int(line.split(b" : ")[0].strip())
            r = line.split(b" : ")[1].split(b',t')
            lines.append([id, float(r[0]), float(r[1]), float(r[2])])
    return lines

p = remote("172.17.0.1", 31312)
for i in range(20):
    stars = recvdata()
    sol = cal_matrix(stars)
    p.sendline(sol)
```

## 部署
```bash
socat -v tcp-listen:31312,reuseaddr exec:"docker run --rm -i \
  -e SEED=3472657338860861762 -e FLAG=flag{1234} \
  attitude:challenge" > run.log 2>&1
```
