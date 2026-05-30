# 【卫星安全系列五】attitude 赛题复现

> 原文: https://www.ctfiot.com/153356.html
> ID: 153356

题目介绍
题目名：attitude

给出一个附件：test.txt，共2500行记录，每行记录有4个值，分别表示天球参考系中指向某颗恒星的单位向量X、Y、Z坐标值和其星等值。

nc指定地址后，需要给出4个浮点数，如下所示：

题目源码链接：

https://github.com/cromulencellc/hackasat-qualifier-2020

文件如下：

由于网络问题，我们需要配置国内源

1）新建一个sources.list文件

添加如下内容：

添加

如果你用的是wsl的docker，那就在windows下编译

编译generator-base

由于需要编译generator模块而generator依赖generator-base，所以先要编译generator-base

make build

打开终端，cd到attitude目录，执行make build即可，如下：

make test

输入make test 可以查看解题效果

至此环境搭建完成。

根据题目数据，我们要以四个浮点数组成的四元数来描述卫星跟踪器的姿态，所以我们要了解卫星姿态和描述方式。

卫星姿态是指卫星星体在轨道上运行所处的空间指向状态。直角坐标系的原点置于星体上，指向地面的Z轴反映偏航方向，Y轴反映俯仰方向，X轴反映滚动方向。卫星星体可由其星体坐标系来代替，所以卫星姿态实际上描述的是星体坐标系Ob xb yb zb相当于参考坐标系Or xr yr zr的转动关系，如下图所示：

旋转矩阵（Rotation Matrix）： 旋转矩阵是一个3×3的正交矩阵，用来表示姿态的旋转。对于卫星，通常用一个从卫星系到惯性系的旋转矩阵来描述姿态。

四元数（Quaternion）： 四元数是一种数学工具，可以用来表示三维空间中的旋转。它是一个包含四个实数的向量，通常表示为 q = [w, x, y, z]，其中w是标量部分，(x, y, z)是向量部分。四元数常用于在旋转中避免万向锁问题。

欧拉角（Euler Angles）： 欧拉角是一组三个角度，通常用来描述三维空间中的旋转。这三个角度通常是绕固定坐标轴（通常是x、y、z轴）旋转的角度，可以是滚转角（Roll）、俯仰角（Pitch）、偏航角（Yaw）等。

方向余弦矩阵（Direction Cosine Matrix，DCM）： 方向余弦矩阵是一个3×3的正交矩阵，用于描述两个坐标系之间的方向关系。在卫星姿态中，它可以用于描述卫星坐标系相对于惯性坐标系的方向。

轴角表示法（Axis-Angle Representation）： 轴角表示法使用一个单位向量表示旋转轴，再加上一个旋转角度来描述旋转。这种表示方式简单且直观。

下面看一下数学上的说明

旋转矩阵

旋转矩阵是一种用于描述旋转变换的数学工具，通常用于将一个坐标系中的向量旋转到另一个坐标系中。在三维空间中，旋转矩阵是一个3×3的正交矩阵，满足以下条件：

正交性（Orthogonality）： 矩阵的行向量和列向量是单位向量，且互相垂直，即

，其中

是矩阵 
的转置，
 是单位矩阵。

行列式为1（Determinant = 1）： 矩阵的行列式等于1，即 

。

其中，

 是矩阵的元素。这个矩阵描述了一个坐标系从原始方向经过旋转后的方向。

对于绕某个坐标轴的旋转，可以使用以下的旋转矩阵：

绕X轴的旋转矩阵（Roll）：

绕Y轴的旋转矩阵（Pitch）：

绕Z轴的旋转矩阵（Yaw）：

其中，θ 是旋转角度。这些基础的旋转矩阵可以组合使用，通过矩阵相乘实现任意轴的旋转。例如，绕固定轴顺序执行旋转，可以用

，其中 α、β、γ 分别是绕X、Y、Z轴的旋转角度。

方向余弦矩阵

方向余弦矩阵的表示 ：

方向余弦矩阵 
 是一个3×3的矩阵，表示为：

其中，

 表示两个坐标系之间第 
 轴在第 
 轴上的余弦值。

正交性质：

方向余弦矩阵具有正交性质，即它的转置与其逆相等：

这里，

 表示矩阵 
 的转置，
 是单位矩阵。

方向性质:

方向余弦矩阵的列向量表示了一个坐标系的基向量在另一个坐标系中的表示。例如，矩阵的第一列表示卫星坐标系中X轴在地球坐标系中的表示。

旋转变换:

方向余弦矩阵可以用于进行坐标系之间的旋转变换。如果有一个向量 
 在一个坐标系中的表示为 

，则在另一个坐标系中的表示为：

四元数

四元数（Quaternion）是一种数学工具，用于表示三维空间中的旋转。它可以看作是复数的扩展，由一个实部和三个虚部组成。通常，四元数用符号 

 表示，其中：

是实部（标量部分），

是虚部，分别对应 

 轴的系数。

四元数的形式为 

，其中 

 是虚部的向量。

在四元数中，乘法和加法的定义如下：

加法：

乘法：

其中，
 表示向量的点积，
 表示向量的叉积。

四元数的模长（或范数）定义为：

单位四元数（模长为1）常用于表示旋转，因为它们可以用来避免万向锁问题。为了实现旋转，可以通过将一个向量用四元数表示，然后用另一个四元数来表示旋转，最后将它们相乘。

欧拉角

欧拉角（Z-Y-X顺序）：

欧拉角的表示形式为 

α
β
γ
。

旋转矩阵的Z-Y-X欧拉角表示为：

其中：

Kabsch算法是一种用于计算两组点集之间的最佳旋转矩阵的算法。它通常用于结构生物学和计算机图形学中的分子对齐等领域。该算法的目标是找到最小平方偏差的旋转矩阵，使得一个点集能够最好地匹配到另一个点集。

以下是Kabsch算法的基本步骤：

中心化数据： 对两组点集进行平移，将它们的质心移动到原点，以消除平移的影响。

计算协方差矩阵： 计算两组点集的协方差矩阵。协方差矩阵描述了数据的分散和方向。

计算奇异值分解（SVD）： 对协方差矩阵进行奇异值分解，得到左奇异向量、右奇异向量和奇异值。SVD是一种矩阵分解方法，将矩阵分解为三个矩阵的乘积。

计算旋转矩阵： 利用SVD结果，通过构造旋转矩阵，使其从一个点集到另一个点集的映射最优。这通常涉及选择左奇异向量和右奇异向量构造旋转矩阵。

Kabsch算法的输出是一个旋转矩阵，该矩阵描述了如何将一个点集旋转和平移以最小化两个点集之间的均方根偏差。python的第三方库rmsd实现了Kabsch算法，可以用其来求解旋转矩阵。

直接使用 pip install rmsd 安装即可

首先用下图说明解题流程

参考向量组A的数据，需要按四元组表示，用python的列表来存储比较合适。

test.txt：

这段代码将参考星数据存储到了dataA_list里，那么获取服务器给的追踪器采集的数据再结合kabsch就得到了旋转矩阵，再将旋转矩阵转为四元数，发送给服务器进行验证，20次即可完成。

Exp如下：

运行challenge

攻击结果：


```
deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb http://mirrors.aliyun.com/debian-security bullseye-security main
deb-src http://mirrors.aliyun.com/debian-security bullseye-security main
deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
ADD sources.list /etc/apt/sources.list
with open("test.txt","r") as f:
    data = f.readlines()

dataA_list = []
data = data[:-1]
for t in data:
    tmp = [float(num) for num in t.split(",")]
    dataA_list.append(tmp)
import numpy as np
from scipy.spatial.transform import Rotation
import rmsd
from pwn import *
context.log_level = "debug"
def cal_matrix(stars):
    dataAlist = get_dataAlist()
    v_ref, v_obs = [], []
    for idx,x,y,z in stars:
        v_ref.append([dataAlist[idx][0],dataAlist[idx][1],dataAlist[idx][2]])
        v_obs.append([x, y, z])
    A = np.array(v_ref)
    B = np.array(v_obs)

    # 通过Kabsch算法获得旋转矩阵
    R = rmsd.kabsch(A, B)
    sol = Rotation.from_matrix(R).as_quat()

    return ','.join(str(x) for x in sol)

def recvdata():
    res = p.recvuntil(b"nn").split(b"n")
    lines = []
    for line in res:
        if b'0.' in line:
            id = int(line.split(b" : ")[0].strip())
            r = line.split(b" : ")[1].split(b',t')
            x = float(r[0])
            y = float(r[1])
            z = float(r[2])
            lines.append([id, x, y, z])
    return lines

def get_dataAlist():
    with open("test.txt", "r") as f:
        data = f.readlines()

    dataA_list = []
    data = data[:-1]
    for t in data:
        tmp = [float(num) for num in t.split(",")]
        dataA_list.append(tmp)
    return dataA_list

p = remote("172.17.0.1",31312)

for i in range(20):
    stars = recvdata()
    sol = cal_matrix(stars)
    p.sendline(sol)
    data = p.recvuntil('n')

# p.interactive()
socat -v tcp-listen:
31312,reuseaddr exec:"docker run --rm -i -e SEED=3472657338860861762  -e FLAG=flag{1234}  attitude:
challenge" > run.log 2>&1
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1703508656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1703508657.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703508657.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1703508658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1703508659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703508660.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1703508660.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1703508661.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1703508662.png)