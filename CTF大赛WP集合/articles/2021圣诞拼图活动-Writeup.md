# 2021圣诞拼图活动-Writeup

> 原文: https://www.ctfiot.com/19654.html
> ID: 19654

昵称
使用时间(ms)

f11st
246934

crystal
880427

gorgeousdays
3104518

solazola
3553183

本次圣诞拼图活动每次开始游戏，将随机生成一个图片，并被分割成 n*n 块，出于友好度，设置为 4，也就是分割为 16 块，其中随机一个图块被置于全黑，然后滑动周围的图块 n 次，形成打乱的图呈现给做题者。这里打乱的步数为 64 步，所以理论上只需要 ≤64 步即可顺利还原。

一醒来发现圣诞节还有活动，满满福利！

得出原图块对应还原后图片的序列5, 1, 6, 8, 2, 11, 7, 13, 15, 14, 3, 4, 10, 16, 12, 0

接下来就是路径规划算法，查网上资料一般采用 A* 算法求解。求快直接 CV 一个 A* 算法得出结果。

由于需要在 80 步内完成，算法可能需要多试几张拼图

解题脚本：

首先，找一张好拼的图保存下来

写个脚本，把图裁剪出 16 份：

找一个拼图工具，手动拼起来：

给待解决的图编号：

要拼成的目标的正序编号就是：

1. 把初始化的 list 代入

2. 把终点的 list 代入

3. 结果做一下转换，转成题目要求的格式

想继续优化的话，可以写一个脚本，不断的 reset，直到刷到自己拼好的那张图，然后自动匹配每小块，自动编号，自动生成初始化 list。这样，前面手动匹配编号的步骤就可以减少时间了。

再采用 python 创建一个 4*4 的数字华容道程序，初始化为题目示意，最终状态为 1-16 按顺序，即将题目变为数字华容道的复原。并在每一步后打印出结果。

然后就手动拼了。

2. 沿着黑线剪开，剪成16个小方块

4. 最终完成的图：

技巧：

用的是最原始的方法吧，截出 16 个格子的图，使用 photoshop 摆好原正常的图，编上数字，然后按要解的图案摆好，开始录像，手动把图像拼好，再看着录像把上下左右每一步写下来，得出答案。

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
搜索完成，共用时：2.600806474685669 秒
RRDDRDLULURRULDLDLUURRRDLLDRULDDRULUURDRULLDRRDLLLDRURULLDDRULURRDLDRURU
所需步数为：72
共搜索状态数：3927
# A*代码来自于https://github.com/Alec-lt/Puzzle_Game
# main.py
from State import Node, MinBinHeapq, Step
import time
from copy import deepcopy

class Solution():
    def __init__(self, puzzle):
        # 列表元素总数，分块总数
        self.number = 16
        # 图的数组保存形式
        self.map = puzzle
        # 白块的位置
        self.white = -1

        # 方向
        # 0  1  2  3
        # 上 下 左 右
        self.direction = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.step_direction = [0, 1, 2, 3]

        # 分割维度
        self.dim = 4

        # A_star算法相关变量
        self.fac = []
        self.step_dict = {}
        self.hash_visited = {}
        self.steps = []
        self.ai_fac()

        # 计数君
        self.hhhh = 0

    def ai_manhattan(self, map_list=[]):
        """
        曼哈顿距离计算
        :
return: distance
        """
        distance = 0
        for i in range(self.dim*self.dim):
            if map_list[i] == 0:
                continue
            cx = int(i / self.dim)
            cy = int(i % self.dim)
            gx = int((map_list[i]-1) / self.dim)
            gy = int((map_list[i]-1) % self.dim)
            distance += (abs(cx-gx) + abs(cy-gy))

        return 10 * distance

    def ai_fac(self):
        """
        计算阶乘数列
        :
return: None
        """
        self.fac.append(1)
        for i in range(1, 26):
            self.fac.append(i*self.fac[i-1])

    def ai_to_hash(self, state=[]):
        """
        哈希化
        :
param state: 状态数组
        :
return: 哈希值
        """
        result = 0
        length = len(state)

        for i in range(length):
            k = 0
            for j in range(i+1, length):
                if state[i] > state[j]:
                    k += 1
            result = result + k*self.fac[length-i-1]

        return result

    def ai_step_print(self, hash_node):
        k = self.step_dict.get(hash_node)
        if k.pre == -1:
            return
        self.ai_step_print(k.pre)
        self.steps.append(k.ch)

    def ai_a_star(self):
        """
        执行A_star算法
        :
return: None
        """

        q = MinBinHeapq()
        sta = Node(self.map)
        old_hash = self.ai_to_hash(sta.map)
        new_step = Step(-1, -1)
        self.step_dict.setdefault(old_hash, deepcopy(new_step))
        self.hash_visited.setdefault(old_hash, 1)

        q.push(deepcopy(sta))

        while not q.empty():
            self.hhhh += 1
            sta = deepcopy(q.pop())

            if sta.man_distance == -1:
                sta.man_distance = self.ai_manhattan(sta.map)

            if sta.man_distance == 0:
                self.ai_step_print(self.ai_to_hash(sta.map))
                break

            s = sta.map.index(0)
            sx = int(s / self.dim)
            sy = int(s % self.dim)
            old_man_distance = sta.man_distance
            old_g_value = sta.g_value
            old_hash = self.ai_to_hash(sta.map)

            for i in range(4):

                mi = sx + self.direction[i][0]
                mj = sy + self.direction[i][1]

                if mi < 0 or mi >= self.dim or mj < 0 or mj >= self.dim:
                    continue

                m = mi * self.dim + mj

                sta.map[s], sta.map[m] = sta.map[m], sta.map[s]

                # 通过字典 查看哈希值(状态)是否被访问过
                new_hash = self.ai_to_hash(sta.map)

                if self.hash_visited.get(new_hash) is None:
                    self.hash_visited.setdefault(new_hash, 1)

                    sta.man_distance = self.ai_manhattan(sta.map)
                    sta.g_value = old_g_value + 1

                    new_step.pre, new_step.ch = old_hash, i
                    self.step_dict.setdefault(new_hash, deepcopy(new_step))

                    q.push(deepcopy(sta))

                    sta.man_distance = old_man_distance
                    sta.g_value = old_g_value

                sta.map[s], sta.map[m] = sta.map[m], sta.map[s]

            del sta

        self.hash_visited.clear()
        del q

    def ai_work(self):
        """
        自动还原展示
        步数依据：self.steps = [...]
        :
return: None
        """

        # 步数的相关数据清空
        self.step_dict.clear()
        self.steps.clear()

        self.white = self.map.index(0)

        start = time.time()
        self.ai_a_star()
        end = time.time()
        print('搜索完成，共用时：', (end - start), '秒')
        # print(self.steps)
        desc = ''
        for i in self.steps:
            if i == 0:
                desc += 'D'
            elif i == 1:
                desc += 'U'
            elif i == 2:
                desc += 'R'
            elif i == 3:
                desc += 'L'
        print(desc)
        print('所需步数为：', len(self.steps))
        print('共搜索状态数：', self.hhhh)
        self.hhhh = 0

if __name__ == '__main__':
    s = Solution([5, 1, 6, 8, 2, 11, 7, 13, 15, 14, 3, 4, 10, 16, 12, 0])
    s.ai_work()
# State.py
import gc

class Node(object):
    def __init__(self, map_list=[], man_distance=-1, g_value=0):
        """
        结点类  (i, j)为白块的位置
        :
param map_list: 存取状态
        :
param man_distance: 曼哈顿距离
        """
        self.map = map_list[:]
        self.man_distance = man_distance
        self.g_value = g_value

class Step(object):
    def __init__(self, pre=-1, ch=-1):
        """
        步类
        :
param pre: 上一个步类结点
        :
param ch: 方向
        """
        self.pre = pre
        self.ch = ch

class MinBinHeapq(object):
    """
    最小堆
    """
    def __init__(self):
        self.size = 0
        self.data = []

        node = Node()
        self.data.append(node)

    def pre_up(self, i):
        """
        上升结点
        :
param i: 上升的结点编号
        :
return:  void
        """
        while i // 2 > 0:
            if self.data[i].man_distance + self.data[i].g_value < self.data[i // 2].man_distance + self.data[i // 2].g_value:
                self.data[i // 2], self.data[i] = self.data[i], self.data[i // 2]
            i = i // 2

    def push(self, k):
        """
        插入结点操作
        :
param k: 插入结点类
        :
return: void
        """
        self.data.append(k)
        self.size += 1
        self.pre_up(self.size)

    def pre_down(self, i):
        """
        元素下潜
        :
param i: 当前元素编号
        :
return: void
        """
        while (i*2) <= self.size:
            mc = self.min_child(i)
            if self.data[i].man_distance + self.data[i].g_value > self.data[mc].man_distance + self.data[mc].g_value:
                self.data[i], self.data[mc] = self.data[mc], self.data[i]
            i = mc

    def min_child(self, i):
        """
        寻找最小的子孩子
        :
param i: 当前结点的编号
        :
return: 最小孩子的编号
        """
        if i * 2 + 1 > self.size:
            return i * 2
        else:
            if self.data[i*2].man_distance + self.data[i*2].g_value < self.data[i*2 + 1].man_distance + self.data[i*2 + 1].g_value:
                return i * 2
            else:
                return i * 2 + 1

    def pop(self):
        """
        弹出元素，先把头一个存一下，用最后一个的值赋值
        删除最后一个元素，最后再进行元素下潜
        :
return: 结点类
        """
        value = self.data[1]
        self.data[1] = self.data[self.size]
        self.size = self.size - 1
        self.data.pop()
        # gc.collect()
        return value

    def empty(self):
        """
        判空
        :
return: 空 True 非空 False
        """
        if self.size == 0:
            return True
        return False
[[3,6,9,4],[2,15,7,10],[13,5,16,11],[14,1,12,8]]
[[3,6,9,4],[2,15,7,10],[13,0,5,11],[14,1,12,8]]
[[1, 2, 3, 4], [0, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 5]]
import cv2
import numpy as np
import matplotlib.pyplot as plt
img=cv2.imread("chamd5.png")
img.shape

for i in range(4):
    for j in range(4):
        temp_img = np.zeros([125, 125, 3], np.uint8)
        temp_img=img[125*i:
125*(i+1),125*j:
125*(j+1)]
        cv2.imwrite("imgs/img"+str(i)+str(j)+".jpg",temp_img)

index=[]
left=[]
right=[]
up=[]
down=[]
for i in range(4):
    for j in range(4):
        temp_img=cv2.imread("imgs/img"+str(i)+str(j)+".jpg")
        index.append(i*4+j+1)
        left.append(temp_img[63][0])
        right.append(temp_img[63][124])
        up.append(temp_img[0][63])
        down.append(temp_img[124][63])
 
temp_img=cv2.imread("imgs/img"+str(0)+str(0)+".jpg")
plt.imshow(temp_img)

def diff(pixel1,pixel2):
    return (int(pixel1[0])-int(pixel2[0]))**2+(int(pixel1[1])-int(pixel2[1]))**2+(int(pixel1[2])-int(pixel2[2]))**2

ban=11
def getleft(index,left,right):
    min_value=1e5
    right_index=-1
    for i in range(16):
        if(i==index or i==ban):
            continue
        if(diff(left[index],right[i])<min_value):
            min_value=diff(left[index],right[i])
            right_index=i
    print("pic "+str(index)+" 's' left is pic "+str(right_index)+" and the diff value is "+str(min_value))
    return (right_index,min_value)
def getright(index,left,right):
    min_value=1e5
    left_index=-1
    for i in range(16):
        if(i==index or i==ban):
            continue
        if(diff(right[index],left[i])<min_value):
            min_value=diff(right[index],left[i])
            left_index=i
    print("pic "+str(index)+" 's' right is pic "+str(left_index)+" and the diff value is "+str(min_value))
    return (left_index,min_value)
def getup(index,up,down):
    min_value=1e5
    up_index=-1
    for i in range(16):
        if(i==index or i==ban):
            continue
        if(diff(up[index],down[i])<min_value):
            min_value=diff(up[index],down[i])
            up_index=i
    print("pic "+str(index)+" 's' up is pic "+str(up_index)+" and the diff value is "+str(min_value))
    return (up_index,min_value)
def getdown(index,up,down):
    min_value=1e5
    down_index=-1
    for i in range(16):
        if(i==index or i==ban):
            continue
        if(diff(down[index],up[i])<min_value):
            min_value=diff(down[index],up[i])
            down_index=i
    print("pic "+str(index)+" 's' down is pic "+str(down_index)+" and the diff value is "+str(min_value))
    return (down_index,min_value)

ans_left=[]
ans_right=[]
ans_up=[]
ans_down=[]
for i in range(16):
    if(i==ban):
        ans_left.append((-1,0))
        continue
    ans_left.append(getleft(i,left,right))
for i in range(16):
    if(i==ban):
        ans_right.append((-1,0))
        continue
    ans_right.append(getright(i,left,right))
for i in range(16):
    if(i==ban):
        ans_up.append((-1,0))
        continue
    ans_up.append(getup(i,up,down))
for i in range(16):
    if(i==ban):
        ans_down.append((-1,0))
        continue
    ans_down.append(getdown(i,up,down))
    
for i in range(16):    
    flag=0
    if(ans_down[i][1]>1000):
        flag+=1
    if(ans_down[i][1]>1000):
        flag+=1
    if(ans_down[i][1]>1000):
        flag+=1
    if(ans_down[i][1]>1000):
        flag+=1
    if(flag>2):
        print(i)
import numpy as np
import cv2
import matplotlib.pyplot as plt
# splicing the images
img = np.zeros([500, 500, 3], np.uint8)
    #true_index=[12,10,7,1,11,5,3,4,6,7,8,9,0,13,14,15,2]
    #true_index=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
true_index=[9,5,1,3,13,11,15,4,2,16,12,6,14,7,10,8]
true_index=[i-1 for i in true_index]
for i in range(4):
    for j in range(4):
        temp_img=cv2.imread("imgsimg"+str(i)+str(j)+".jpg")
        index=true_index[i*4+j]
        true_i=int(index/4)
        true_j=int(index%4)
        print(true_i,true_j)
        img[125*true_i:
125*(true_i+1),125*true_j:
125*(true_j+1)]=temp_img[:,:]
cv2.imwrite("trueimg.jpg",img)
plt.imshow(img)
from random import *   
from tkinter import *   
step_number = 0     #设置步数的变量，初始值为0
def Button_Click_2(x,y):      #按钮点击事件函数
        """声明空白按钮行列号和步数的变量为全局变量"""
        global row_of_space  
        global col_of_space    
        global step_number
        """判断判断点击按钮旁是否为空白按钮，是则交换位置"""
        if abs(x-row_of_space) + abs(y-col_of_space) == 1:  
            step_number += 1    #将步数赋值
            label_step_number['text'] = '步数:' + str(step_number)  #将步数变量导入label控件
            """交换按钮位置"""
            buttons[row_of_space,col_of_space]['text'] = buttons[x,y]['text']
            if(row_of_space>x and col_of_space==y):
                print("D")
            elif(row_of_space<x and col_of_space==y):
                print("U")
            elif(row_of_space==x and col_of_space>y):
                print("R")
            elif(row_of_space==x and col_of_space<y):
                print("L")
            buttons[x,y]['text']  = ' ' 
            row_of_space = x            
            col_of_space = y
            n = 0  
            for row in range(4):
                for col in range(4):
                    """对比所有按钮序列是否正确，不正确则跳出函数"""
                    if buttons[row,col]['text'] != numbers[n]:  
                        return
                    n += 1
            """所有按钮判断完毕赢得游戏胜利"""
            label_welcomes['text'] = '你赢了'
 
"""创建华容道游戏窗口"""
root = Tk()                      #创建图形化用户界面实例
root.title('数字华容道')         #设置窗口标题
root.geometry("400x400")    #将窗口大小设为高400宽400
root.configure(bg = 'black') #将窗口背景设为黑色
root.resizable(width = False,height = False)    #设置窗口为不可拉伸
"""设置欢迎语的label控件"""
label_welcomes = Label(root,text = '欢迎来到数字华容道',bg = 'black',fg = 'red',font = ("Arial",13))    #设置label控件的属性
label_welcomes.place(x = 20,y = 10,width = 250,height = 40)  #设置label控件位置
"""设置显示操作方式的label控件"""
label_operation = Label(root,text = '单击数字',bg = 'black',fg = 'white',font = ("Arial",10))
label_operation.place(x = 3,y = 40,width = 50,height = 30)
label_operation_2 = Label(root,text = '移动方块',bg = 'black',fg = 'white',font = ("Arial",10))
label_operation_2.place(x = 3,y = 60,width = 50,height = 30)
"""设置显示步数的label控件"""
label_step_number = Label(root,text = '步数:' + str(step_number),bg = 'black',fg = 'yellow',font = ("Arial",10))
label_step_number.place(x = 3,y = 20,width = 50,height = 30)
 

root.attributes("-topmost", True)
row_of_space = 0    #存放空白按钮的行号 
col_of_space = 0    #存放空白按钮的列号
buttons = {}      #存放数字按钮的数组
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' '] #所有数字文本的列表 
shuffle(numbers)     #打乱数字列表中的数字顺序

numbers=['8','10','7','14','6','12','16','2','4','15',' ','13','3','1','5','9']
"""制造数字华容道方阵"""

for row in range(4): 
    for col in range(4):
        """创建数字按钮，并将行列号传入该按钮的点击事件函数"""
        button = Button(root,command = lambda x = row,y = col:
Button_Click_2(x,y),bg = 'black',fg = 'green',font = ("Arial",35))
        buttons[row,col] = button   #将按钮导入数组
        button['text'] = numbers.pop()    #设置按钮上的文本
        button.place(x = 60 + col * 60,y = 60 + row * 60,width = 50,height = 50)    #设置数字按钮大小
        if button['text'] == ' ':        #判断是否为空白按钮，如果是，则记录到空白按钮行列号变量
            row_of_space = row
            col_of_space = col
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']   #还原数字列表 
root.mainloop() #显示窗口
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/3-1640773703.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/7-1640773704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/2-1640773704.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/7-1640773705.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/2-1640773705.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1640773705.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/1-1640773705.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/8-1640773706.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1640773706.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1640773706.png)