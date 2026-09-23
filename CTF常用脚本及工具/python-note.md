# python-note
> 记录CTF-python常用的函数

- [常用内置函数](#常用内置函数)
    - [进制转换](#进制转换)
        - [转ascii](#转ascii)
    - [常用编码](#常用编码)
    - [文件操作](#文件操作)
    - [切片操作](#切片操作)
    - [其它操作](#其它操作)
        - [zfill](#zfill)
        - [index](#index)

- [常用模块](#常用模块)
    - [python-requests模块](#python-reuqests模块)
    - [python-urllib模块](#python-urllib模块)
    - [python-os模块](#python-os模块)
    - [python-re模块](#python-re模块)
    - [python-sys模块](#python-sys模块)
    - [python-time模块](#python-time模块)
    - [python-string模块](#python-string模块)
    - [python-zipfile模块](#python-zipfile模块)


## 常用内置函数

### 进制转换
```py
hex(16)     # 10进制转16进制
oct(8)      # 10进制转8进制
bin(8)      # 10进制转2进制



例子：
int('10')       # 字符串转换成10进制整数
int('10',16)    # 字符串转换成16进制整数
int('0x10',16)  # 字符串转换成16进制整数
int('10',8)     # 字符串转换成8进制整数
int('010',8)    # 字符串转换成8进制整数
int('10',2)     # 字符串转换成2进制整数
```

#### 转ascii

```py
chr(int(x,2)) # 二进制转字符
.join([chr(int(i,2)) for i in c.split('0b')[1:]]) # 批量
```


### 常用编码


encode(),decode()

str通过encode()方法可以编码为指定的bytes
反过来，如果我们从网络或磁盘上读取了字节流，那么读到的数据就是bytes。要把bytes变为str，就需要用decode()方法：


- chr()  十进制->基础字符
- ord()  字符->十进制符
- bin() 十进制->二进制

二进制转十六进制

 hex(int('0000010010001101', 2))



例子：
```py
chr(65)  # 输出 : 'A'
ord('A') # 输出 : 65
bin(10)  # 输出 ：0b1010
```
### 文件操作

**写入文件**
with open('1.txt','r'):
    f.write(line)

**逐行读取文件**
with open('1.txt','r'):
    line = f.readline()

read()，一次读取全部内容到内存
readline()
readlines() 逐行读取

**文件模式**
r rb w wb 区别
r：Python 将会按照编码格式进行解析，read() 操作返回的是str
rb：也即 binary mode，read()操作返回的是bytes

### 切片操作

- 切片
    ```
    a=[1,2,3.4,5]
    [-1]    -> [5]
    [:-1]   -> [1,2,3,4]
    [::-1]  -> [5,4,3,2,1]
    [2::-1] -> [3,2,1]
    ```

### 其它操作

#### zfill

**介绍**
zfill()
str.zfill(width)
width -- 指定字符串的长度。原字符串右对齐，前面填充0。

**语法**
```py
#!/usr/bin/python
str = "this is string example....wow!!!";
print str.zfill(40);
print str.zfill(50);

## 输出结果
## 00000000this is string example....wow!!!
## 000000000000000000this is string example....wow!!!
```

#### index

index() 函数用于从列表中找出某个值第一个匹配项的索引位置。

```py
aList = [123, 'xyz', 'runoob', 'abc']

print "xyz 索引位置: ", aList.index( 'xyz' )
print "runoob 索引位置 : ", aList.index( 'runoob', 1, 3 )

# xyz 索引位置:  1
# runoob 索引位置 :  2
```

## 常用模块


### python-requests模块
- import requests
    ```py
    # GET请求
     r = requests.get(url=url)
    # POST请求
     r = requests.post(url=url,data={xxx:xxx})
    ```

### python-urllib模块
```py
# url编码与解码
from urllib import parse
parse.unquote(str1) # url解码
parse.quote(str2) # url编码
```

### python-os模块
- os.listdir(path)
 > 返回指定路径下的文件和文件夹列表
- for i in os.scandir(path) 遍历文件
    ```
    i.name  文件名
    i.path 文件路径
    i.is_dir() 是否为文件夹 否为false
    i.is_file() 是否为文件 是为True
    ```
### python-re模块


- re.findall
    ```py
    import re
    kk = re.compile(r'\d+')
    kk.findall('one1two2three3four4')
    # 输出['1','2','3','4']
    re.findall(kk,"one123")
    # 输出 [123]
    ```

- re.compile
```
compile(pattern[,flags] )
pattern : 一个字符串形式的正则表达式
flags : 可选，表示匹配模式，比如忽略大小写，多行模式等，具体参数为：

1).re.I(re.IGNORECASE): 忽略大小写
2).re.M(MULTILINE): 多行模式，改变'^'和'$'的行为
3).re.S(DOTALL): 点任意匹配模式，改变'.'的行为
4).re.L(LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
5).re.U(UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
6).re.X(VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释
```

```
re.compile('<td class="Big"><span class="big3">(.*?)</span>'(.*?)</span>)
```
### python-sys模块

```py
sys.argv[0] # 表示当前所执行的脚本
sys.argv[1] # 表示脚本第一个参数
sys.argv[2] # 表示脚本第二个参数

len(sys.argv) == 4 # 表示当前脚本含有3个参数
len(sys.argv) == 1 # 表示没有参数

https://www.cnblogs.com/cherishry/p/5725184.html
```

### python-time模块

### python-string模块

string.ascii_letters 生成所有的字母 a-z和A-Z

string.digits 所有数字0-9

### python-zipfile模块

zipfile.ZipFile 用于读写 ZIP 文件的类。

getinfo



### python-try捕获异常

样例1:(捕获所有异常)
```py
try:
    r_check = requests.get(url , timeout =2 )
    except: #捕获所有异常不中止程序
        print(f"{url} can not connect ")
        continue
```

样例2:(捕获单一异常)
```py
try:
    r_check = requests.get(url , timeout =2 )
except requests.exceptions.SSLError as e:
    print(f"{url} can not connect SSL")
    continue
```