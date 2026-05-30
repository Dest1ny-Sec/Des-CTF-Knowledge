# 官方WP | 侧信道攻击赛题Power Trajectory Diagram解析

> 原文: https://www.ctfiot.com/187746.html
> ID: 187746

编者荐语：

本文分享了大鲲智联在第十七届全国大学生信息安全竞赛—创新实践能力赛初赛中设计的侧信道攻击赛题的深入分析。同时，也分享了成功解出这道题目的队伍所采用的方法和技巧。

“Power Trajectory Diagram”赛题均已部署在伽玛实验场，欢迎前去挑战。

三种思路解题

本次的侧信道功耗分析题属于入门级，难度系数较低。

首先下载npz文件，然后通过python的numpy库进行加载，同时打印相关属性（获取键值名）。

执行后返回4个键值，分别是index、input、output、trace，我们再统计各个数据组的长度。

通过返回结果，可以发现除了output组以外其它每组数据长度都是520。

我们再依次打印index、input、trace数据，看看数据样式。

通过键值名和打印的数据可以推断，index是输入字符的序号（从下标0开始），共计输入密码字符串的长度是13，input是每次输入的字符，输入的顺序是a…z0…9_!@#共40个字符，trace是功耗轨迹数据，至此数据已经加载和分析完毕，接下来看看解题思路。

通过绘制功耗轨迹图做对比，判断哪个字符是正确的密码，因为每一位密码输入了40次，而只有1次是正确的，那么正确的功耗轨迹和错误的功耗轨迹肯定会存在差异。

可以发现通过观察每组功耗轨迹绘制图能准确判断出正确密码字符，需要注意的是第13位密码的功耗轨迹绘制图基本一致，所以密码长度实际是12位，通过观察可以得出正确密码是_ciscn_2024_，flag值为flag{_ciscn_2024_}。

该方式是思路1的升级版本，因为通过功耗轨迹图可以发现正确密码的低峰X坐标大于错误密码的低峰，然后我们可以通过编程的方式实现自动判断。

先看第1位密码的处理方式：

再看看全自动的判断方式：

但是通过返回结果可以看出，该方式不能准确判断出最后一位密码是无效的。这里需要使用第3种思路。

通过计算每条功耗轨迹和当前组功耗平均值的相关系数值来判断正确密码字符。这里我们使用python中numpy库中的corrcoef()函数，它是用于获取任意两个数组之间的皮尔逊（Pearson）相关系数矩阵，前提是两个数组的形状相同（即长度一样）。

我们先了解一个概念，相关系数是用来衡量2个变量之间关系程度的统计指标，用来描述两个变量之间的线性关系强弱，它的取值范围从-1到+1，当相关系数接近+1时，表示两个变量呈正相关；当相关系数接近-1时，表示两个变量呈负相关；当相关系数接近0时，表示两个变量之间没有线性关系。

通过上图我们可以发现输入正确的密码字符功耗轨迹数据与平均功耗轨迹的相关系数远远低于其它字符的相关系数值，利用这个依据可以准确判断哪个字符是正确密码。

当所有输入的密码字符都是错误时，计算出来的相关系数均大于0.99，看示例代码：

最后我们实现自动化破解，代码如下：

思路1的优点在于简单，但是缺点是需要人工识别判断结果。

思路2和3的优点在于能进行自动化破解，但前提也需要人工参与判断，同时思路2无法准确判断密码位数，而思路3需要人工先分析出阈值。

关于大鲲智联
大鲲智联(北京)科技有限公司是专业提供智能网联汽车、智能交通、自动驾驶领域相关信息安全的技术保障，为客户提供从技术支持到整体解决方案的全周期平台化解决方案，塑造安全可信的新一代智能网联汽车、移动互联网和物联网生态环境。

选手解法

下载附件，发现是一个npz文件（基于NumPy库的二进制文件格式），于是用python看看里面有什么数据,是什么结构：

了解了数据格式，index考虑是每一轮的标号，标识这一轮在flag中的位置，每40个input为一轮，每一轮index+1。

由题目描述和题目名称考虑（功耗轨迹）要对trace作图。

一开始考虑是要对比同一个input在不同轮次（index）中的图像，寻找有不同图像的index。也就是对比[index:0,input:a] 、[index:40,input:a] 、[index:80,input:a]……. 找到其中不一样的那个图形。仔细找了一下，虽然有小不同（有的记录的上限、下限不太一样），但是没有什么决定性的不同。

然后发现不对，应该是对比同一轮次（index）中不同input的图像，于是作图：

于是发现确实是对比同一轮次（index）中不同input的图像，找出其中波谷位置独特的input（比如上图中的42号input：c），于是遍历一下index，进行寻找。

找出每一轮的不同：_ciscn_2024_

最后一轮40个数找不出不一样的了，考虑没有？

试着提交一下，最后一轮果然是没有的，结果就是：flag{_ciscn_2024_}


```
import numpy as np
dataset = np.load('./ctf_ciscn_2024.npz', allow_pickle=True)
print(dataset.files)
print("{}".format(dataset['index']))
print("{}".format(dataset['input']))
print("{}".format(dataset['trace']))
import matplotlib.pyplot as plt

trace = dataset['trace'] # 获取trace
num = len(dataset['trace']) # 数量
i = 0 # 第几位密码
for x in range(num):
    index = dataset['index'][x] # 读取下标
    # 根据下标值来绘制图
    if index == i:
        print("当前第{}位密码，输入的字符为'{}'".format(index+1, dataset['input'][x]))
        # 绘制功率轨迹图
        plt.figure(figsize=(20, 2))
        plt.grid(True)
        plt.plot(trace[x][:
1000]) # 绘制
        plt.show()
import numpy as np

index_array = dataset['index']
input_array = dataset['input']
trace_array = dataset['trace']

t = []
for i in range(40):
    x_loc = np.argmin(trace_array[i]) # 求最低峰的X坐标位置
    print("{} 最低峰位置 {}".format(input_array[i], x_loc))
    t.append(x_loc)
max_index = np.argmax(t) # 返回最大值的索引
print("n第1位正确密码字符 '{}'".format(input_array[max_index]))
import numpy as np

index_array = dataset['index']
input_array = dataset['input']
trace_array = dataset['trace']

pwdrange_len = len("abcdefghijklmnopqrstuvwxyz0123456789_!@#") # 密码字符范围长度
pass_len = len(trace_array) / pwdrange_len # 猜测的密码长度

password = ""
for x in range(int(pass_len)):
    t = []
    for i in range(40):
        x_loc = np.argmin(trace_array[x*40 + i])
        t.append(x_loc)
    max_index = np.argmax(t) # # 返回最大值的索引
    password = password + input_array[max_index] # 拼接密码

print("n正确密码 - '{}'".format(password)) # 打印结果
# 导入必要的库
import numpy as np
from numpy import corrcoef

index_array = []
input_array = []
trace_array = []
index_array = dataset['index']
input_array = dataset['input']
trace_array = dataset['trace']
pwdrange_len = len("abcdefghijklmnopqrstuvwxyz0123456789_!@#") # 密码字符范围长度

# 计算第1位密码所有字符功耗轨迹平均值
block_trace = trace_array[0:39] # 0-39是第1位密码所有字符功耗轨迹范围
avg_trace = np.mean(block_trace, axis=0) # 求第1组的平均值
# 开始计算每次输入和当前组的平均值的相关系数值
for i in range(pwdrange_len):
    corr = corrcoef(avg_trace, trace_array[i])[0][1]
    print("当前输入字符{}, 与平均值的相关系数 - {}".format(input_array[i], corr))
# 导入必要的库
import numpy as np
from numpy import corrcoef

index_array = []
input_array = []
trace_array = []
index_array = dataset['index']
input_array = dataset['input']
trace_array = dataset['trace']
pwdrange_len = len("abcdefghijklmnopqrstuvwxyz0123456789_!@#") # 密码字符范围长度

# 计算最后1位密码所有字符功耗轨迹平均值
block_trace = trace_array[480:
519] # 480-519是最后1位密码所有字符功耗轨迹范围
avg_trace = np.mean(block_trace, axis=0) # 求最后1组的平均值
# 开始计算每次输入和当前组的平均值的相关系数值
for i in range(480, 520):
    corr = corrcoef(avg_trace, trace_array[i])[0][1]
    print("当前输入字符{}, 与平均值的相关系数 - {}".format(input_array[i], corr))
# 导入必要的库
import numpy as np
from numpy import corrcoef

index_array = []
input_array = []
trace_array = []
index_array = dataset['index']
input_array = dataset['input']
trace_array = dataset['trace']

pwdrange_len = len("abcdefghijklmnopqrstuvwxyz0123456789_!@#") # 密码字符范围长度
pass_len = len(trace_array) / pwdrange_len # 猜测的密码长度
threshold = 0.90 # 设定阈值，用于判断密码字符是否正确

flag = "" # 
for block in range(int(pass_len)):
    block_trace = trace_array[(block * pwdrange_len) : ((block+1) * pwdrange_len)] # 分批取每组能耗轨迹
    avg = np.mean(block_trace, axis=0) # 求每组的平均值
    for i in range(pwdrange_len):
        # 开始计算每次输入和当前组的平均值的相关系数值
        corr = corrcoef(avg, trace_array[i+pwdrange_len*block])[0][1]
        # 设置判断阈值，然后打印满足条件的输入字符
        if corr < threshold:
            flag += input_array[i+pwdrange_len*block]

# 最后打印结果
print("flag{}{}{}".format("{", flag, "}"))
i=1
# 提取 trace 数据
trace = npz_file['trace']
for x in range(40*i,40*(i+1)):
    print(f"x:{x},{input_data[x]}")
    # 绘制第一个 trace 的功率轨迹图
    plt.figure(figsize=(100, 6))
    plt.plot(trace[x], label='Trace 0')  # 绘制第一个 trace 数据

    plt.title('Power Trace')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1718327924.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/10-1718327925.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/8-1718327925.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1718327926.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1718327926.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1718327927.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1718327927.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1718327928.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/9-1718327929.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/2-1718327929.png)