# 2024阿里CTF  WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/170629.html
> ID: 170629

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

数据集https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment/data

准确率不高，反正试了几次也出了


```
    #malloc 0x20 &show(ptr)
n1[0] = 0   
n1[15] = 4
n1[0] = 0   
n1[15] = 4
__int64 sub_20F7()
{
  int i; // [rsp+8h] [rbp-118h]
  int v2; // [rsp+Ch] [rbp-114h]
  char v3[264]; // [rsp+10h] [rbp-110h] BYREF overflow
  unsigned __int64 v4; // [rsp+118h] [rbp-8h]
    #mid edit & stack overflow
n1[0] = 0   
n1[15] = 4
    #writen by flyyy
from pwn import *
from ctypes import *
import warnings
warnings.filterwarnings("ignore", category=BytesWarning)
import copy
flag = [0 for i in range(19)]
flag[0] = -1 # 数组从下标1开始，flag[0]不使用
flag[15] = 7
flag[18] = 4
import hashlib
import itertools
######################训练模型##############################################
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1711767221.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711767223.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711767224.webp)