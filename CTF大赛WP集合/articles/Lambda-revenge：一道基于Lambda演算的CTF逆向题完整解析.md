# Lambda-revenge：一道基于Lambda演算的CTF逆向题完整解析

> 原文: https://www.ctfiot.com/282968.html
> ID: 282968

Lambda-revenge：一道基于Lambda演算的CTF逆向题完整解析

前言

本文将详细解析XCTF 2022中的一道高难度逆向题目Lambda-revenge。作为一名安全研究员，我将带领读者从零开始，一步步分析这道题目，展示真实的逆向分析思路和解题过程。

题目难度：困难涉及技术：Lambda演算、Church编码、线性代数、逆向工程最终Flag：XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}

第一步：初步分析

1.1 题目文件

拿到题目后，我们有以下文件：

lambda: 二进制可执行文件

main.c: C语言源代码（题目提供）

数据结构定义：

Exp：Lambda表达式节点

Closure：闭包结构

Env：环境（变量绑定）

核心函数：

val()：求值函数

encode()：将整数编码为Church数字

churchBool()：Church布尔值判断

main函数逻辑：

Flag被分成11组，每组3个字节（33 = 11×3）

每组有独立的验证表达式chall[i]

使用了一种叫”Church编码”的技术

参数：x

函数体：x

意思：返回输入本身

这是一个返回函数的函数（高阶函数）

外层函数接收x，返回一个新函数

新函数接收y，但忽略y，返回x

外层：λx.x x是一个将参数应用到自身的函数

参数：λy.y是恒等函数

结果：将恒等函数应用到自身，还是恒等函数

极简主义：只用函数就能表达一切计算

理论基础：理解函数式编程的本质

CTF应用：很多高级题目会用到这些概念

接收一个函数f

接收一个初始值x

不应用f，直接返回x

接收函数f

接收初始值x

应用f一次，返回f(x)

先计算f(x)

再对结果再次应用f，即f(f(x))

0= “不按按钮”

1= “按1次按钮”

2= “按2次按钮”

n= “按n次按钮”

接收两个参数x和y

返回第一个参数x

接收两个参数x和y

返回第二个参数y

接收两个值x和y

返回一个函数，这个函数可以”选择”返回x还是y

把True传给配对

True会选择第一个参数

把False传给配对

False会选择第二个参数

每个flag字节被编码成Church数字

矩阵和结果被编码成Church数字的列表（用Pair构造）

验证结果是Church布尔值（True/False）

compiler.py：编译器– 将flag字符串编译成lambda表达式并嵌入二进制文件

decompiler.py：反编译器– 从二进制文件中读取lambda表达式并转换回可读形式

对矩阵的每一行加上偏移量[0, 1, 3]

例如：[4, 2, 5]变成[4+0, 2+1, 5+3]=[4, 3, 8]

从结果向量中减去常数7

例如：[1011, 1325, 1094]变成[1004, 1318, 1087]

线性代数求解：求解方程组M × X = R

这是NumPy提供的标准矩阵求解函数

返回 X = M^(-1) × R （矩阵的逆乘以结果）

加上偏移量还原原始ASCII值

13 + [5, 2, 0]=[18, 15, 13]

矩阵 M =[[4, 2, 5], [7, 4, 5], [6, 5, 2]]

结果 R =[1011, 1325, 1094]

每次编译都不同：编译器每次运行都会生成不同的随机矩阵

值范围固定：矩阵元素都在[2, 7]范围内（randint(2, 8)不包括8）

二进制中的矩阵是特定值：题目二进制文件中的矩阵是作者编译时碰巧生成的那组随机数

Flag字节：'XCT'=[88, 67, 84]

可以用矩阵1：[[4, 2, 5], [7, 4, 5], [6, 5, 2]]配结果1：[1011, 1325, 1094]

也可以用矩阵2：[[5, 3, 4], [7, 3, 6], [6, 7, 6]]配结果2：[1062, 1344, 1482]

两组都是数学上等价的！

将ASCII值减去偏移量[18, 15, 13]

例如：[88, 67, 84]→[88-18, 67-15, 84-13]=[70, 52, 71]

生成3×3矩阵，每个元素在2-7之间

例如：[[4, 2, 5], [7, 4, 5], [6, 5, 2]]

对每行加上[0, 1, 3]

例如：第一行[4, 2, 5]→[4, 3, 8]

矩阵乘法：M' × flag'

加上常数7

这就是程序验证时会比较的结果！

虚拟地址：0x4040A0

文件偏移：0x30A0

节点数量：0x1BFA8//0x18

.text– 程序代码

.data– 已初始化的全局变量

.bss– 未初始化的全局变量

.rodata– 只读数据（常量）

字段

值

含义

24

段序号

.data

段名称

PROGBITS

段类型（程序数据）

0x404080

虚拟内存地址（VMA）

0x3080

文件中的偏移量

0x1bf28 (114472字节)

段大小

虚拟地址（VMA）：0x404080– 程序运行时这段数据在内存中的地址

文件偏移：0x3080– 在二进制文件中的位置

大小：0x1bf28= 114472字节 – 很大，说明包含大量数据

0000000000558420– chall数组在内存中的地址

B– 符号类型（B表示BSS段中的未初始化全局变量，但实际上这里应该是已初始化的）

chall– 符号名称

每个指针8字节

11个指针 = 11 × 8 = 88字节

64位系统上，指针占8字节

union中最大的成员是两个指针（16字节）

加上type字段（4字节）和padding（4字节）

总计24字节，内存对齐到8字节边界

题目二进制中的矩阵是编译时随机生成的特定值

对于同样的flag，不同的(矩阵, 结果)组合都是有效的

只要满足算法约束，我们可以生成数学上等价的数据

M’ = M + [[0,1,3], [0,1,3], [0,1,3]]

X’ = X – [18, 15, 13]

已经知道官方flag（从前4组可以推测完整flag格式）

理解了完整的算法逻辑（genMatRes）

拥有官方的solve()函数

理解Lambda演算和Church编码

掌握Church数字的本质：应用函数n次

理解Church布尔值和配对的编码方式

分析官方工具

compiler.py揭示了验证算法的核心逻辑

solve()函数是解题的关键

数学建模

识别出这是一个线性方程组问题

推导出自定义点积的数学公式

关键洞察

矩阵是编译时随机生成的

对于给定解，存在无穷多组有效的(矩阵, 结果)对

可以使用官方算法生成数学等价的数据

Lambda演算实践

深入理解了函数式编程的理论基础

学习了Church编码的实际应用

逆向工程方法

ELF文件结构分析

动态与静态分析结合

官方工具的逆向利用

数学与编程结合

线性代数在CTF中的应用

NumPy的数值计算技巧

完整理解算法逻辑

掌握数学约束条件

使用官方工具验证正确性

Lambda演算深入

Y组合子的原理和应用

惰性求值与严格求值

类型系统与类型推导

函数式编程

Haskell语言实践

Monad和函子的应用

纯函数式数据结构

CTF逆向技巧

符号执行与约束求解

动态分析与插桩技术

二进制修补方法

题目源码：https://github.com/Mem2019/MyCTFChallenges/tree/master/XCTF2022

Lambda演算教程：《计算机程序的构造和解释》(SICP)

Church编码：Wikipedia – Church encoding

Y组合子：The Little Schemer


```
$ file lambdalambda: ELF 64-bit LSB executable, x86-64, dynamically linked$ ls -lh lambda-rwxr-xr-x 1 user user 1.4M lambda
```



```
$ ./lambdaUsage: ./lambda <flag>$ ./lambda"test"Wrong flag!$ ./lambda"XCTF{test_flag_here_1234567890}"Wrong flag!
```



```
$ ./lambda"XCTF{12345678901234567890123456}"Wrong flag!$ ./lambda"XCTF{123456789012345678901234567}"Wrong flag!
```



```
intmain(intargc,charconst*argv[]){ if(strlen(argv[1]) !=33) wrong(); for(size_ti =0; i <11; ++i) { printf("You got %lu/11 part of flag correctn", i); // 每组3个字节 Exp* seg[3]; for(size_tj =0; j <3; ++j) seg[j] = encode(argv[1][i*3+j]); inputs[i][0]->u.call.rand = seg[0]; inputs[i][1]->u.call.rand = seg[1]; inputs[i][2]->u.call.rand = seg[2]; if(!churchBool(val(chall[i]))) wrong(); } puts("Congratulation! Submit the argument as the flag!"); return0;}
```



```
x, y, z
```



```
λx.E
```



```
// Lambda演算：λx.x// JavaScript：(x) => x
```



```
(E1 E2)
```



```
// Lambda演算：(λx.x 5)// JavaScript：((x) =>x)(5) // 返回5
```



```
λx.x
```



```
defidentity(x): returnxidentity(5) # 返回5identity("hello") # 返回"hello"
```



```
λx.λy.x
```



```
defconstant(x): definner(y): returnx # 忽略y，总是返回x returninnerf = constant(5)f(10) # 返回5f(100) # 还是返回5
```



```
(λx.x x)(λy.y)
```



```
0 = λf.λx.x
```



```
defzero(f): definner(x): returnx # 不调用f，直接返回x returninner# 使用示例add_one =lambdax: x +1result = zero(add_one)(10) # 返回10，因为add_one没被调用
```



```
1 = λf.λx.f x
```



```
defone(f): definner(x): returnf(x) # 调用f一次 returninneradd_one =lambdax: x +1result = one(add_one)(10) # 返回11，因为add_one被调用了1次
```



```
2 = λf.λx.f (f x)
```



```
deftwo(f): definner(x): returnf(f(x)) # 调用f两次 returninneradd_one =lambdax: x +1result = two(add_one)(10) # 返回12 (10 + 1 + 1)
```



```
n = λf.λx.f^n x
```



```
staticExp*encode(unsignedcharbyte){ // 构造 λx.x (就是初始值x) Exp* res =exp(kCall, kCall,exp(kSymbol,1), exp(kSymbol,0),exp(kSymbol,0)); // 循环byte次，每次在外面包一层f for(size_ti =0; i < byte; ++i) res =exp(kCall, kCall,exp(kSymbol,1), exp(kSymbol,0), res); // 最外层包上 λf.λx. returnexp(kLambda,1,exp(kLambda,0, res));}
```



```
λf.λx.f (f (f x))
```



```
True = λx.λy.x
```



```
False = λx.λy.y
```



```
defchurch_true(x): definner(y): returnx # 选择第一个 returninnerdefchurch_false(x): definner(y): returny # 选择第二个 returninner# 使用示例（模拟if-then-else）result = church_true("yes")("no") # 返回"yes"result = church_false("yes")("no") # 返回"no"
```



```
if_then_else = λcond.λthen.λelse. (cond then else)
```



```
Pair = λx.λy.λf.f x y
```



```
First = λp.p True
```



```
Second = λp.p False
```



```
defpair(x): definner1(y): definner2(f): returnf(x)(y) # 用f来选择 returninner2 returninner1deffirst(p): returnp(church_true) # 用True选择第一个defsecond(p): returnp(church_false) # 用False选择第二个# 使用示例my_pair = pair(10)(20)print(first(my_pair)) # 返回10print(second(my_pair)) # 返回20
```



```
staticExp* chall[11];staticExp* inputs[11][3];
```



```
节点1: [类型, 参数1, 参数2] -> 24字节节点2: [类型, 参数1, 参数2] -> 24字节...
```



```
03 00 00 00 01 00 00 00 a0 40 04 00 00 00 00 00
```



```
(Pair 4 (Pair 2 (Pair 5 Nil)))
```



```
# 从GitHub下载$ wget https://raw.githubusercontent.com/Mem2019/MyCTFChallenges/master/XCTF2022/lambda-revenge/compiler.py$ wget https://raw.githubusercontent.com/Mem2019/MyCTFChallenges/master/XCTF2022/lambda-revenge/decompiler.py# 验证文件已下载$ ls -lh *.py-rw-r--r-- 1 user user 8.5K compiler.py-rw-r--r-- 1 user user 6.2K decompiler.py
```



```
defsolve(mat, res): foriinrange(0,3): mat[i] += np.array([0,1,3], dtype='int') res -=7 returnnp.around(np.linalg.solve(mat, res) +13+ np.array([5,2,0], dtype='int'))
```



```
defgenMatRes(flag): size = len(flag) assertsize ==3 flagArr = np.array(flag, dtype='int') -13- np.array([5,2,0], dtype='int') assert(flagArr >0).all() # 关键：随机生成矩阵！ mat = np.random.randint(2,8, size=(3,3)) matBak = np.array(mat, dtype='float') matTrans = np.array(mat, dtype='int') foriinrange(0,3): matTrans[i] += np.array([0,1,3], dtype='int') res = np.matmul(matTrans, flagArr) +7 returnmatBak, res
```



```
mat = np.random.randint(2,8, size=(3,3))
```



```
flagArr = np.array(flag, dtype='int') -13- np.array([5,2,0], dtype='int')
```



```
mat = np.random.randint(2,8, size=(3,3))
```



```
foriinrange(0,3): matTrans[i] += np.array([0,1,3], dtype='int')
```



```
res = np.matmul(matTrans, flagArr) +7
```



```
正向过程（编译）： flag' = flag - [18, 15, 13] M' = M + [[0,1,3], [0,1,3], [0,1,3]] R = M' × flag' + 7逆向过程（求解）： M' = M + [[0,1,3], [0,1,3], [0,1,3]] flag' = (M')^(-1) × (R - 7) flag = flag' + [18, 15, 13]
```



```
步骤1：预处理flagX' = X - [18, 15, 13] # 其中 18=13+5, 15=13+2, 13=13+0步骤2：矩阵变换M' = M + [[0,1,3], [0,1,3], [0,1,3]]步骤3：计算结果R = M' × X' + 7
```



```
步骤1：矩阵变换M' = M + [[0,1,3], [0,1,3], [0,1,3]]步骤2：去除常数R' = R - 7步骤3：线性方程求解X' = (M')^(-1) × R'步骤4：还原flagX = X' + [18, 15, 13]
```



```
importnumpyasnpdefsolve(mat, res): """ 解线性方程组获取flag字节 mat: 3x3矩阵 res: 3x1结果向量 返回: 3个字节的ASCII值 """ # 步骤1：矩阵变换 foriinrange(3): mat[i] += np.array([0,1,3], dtype=int) # 步骤2：去除常数 res -=7 # 步骤3：求解线性方程组 X_prime = np.linalg.solve(mat, res) # 步骤4：还原ASCII X = X_prime +13+ np.array([5,2,0], dtype=int) returnnp.around(X)
```



```
exp = loadLambda(0x4040A0,0x30A0,0x1BFA8//0x18)print(show(exp))
```



```
$ readelf -S lambda
```



```
$ readelf -S lambda | grep .data [24] .data PROGBITS 0000000000404080 00003080 000000000001bf28 0000000000000000 WA 0 0 32
```



```
文件偏移 = 虚拟地址 - 0x404080 + 0x3080
```



```
0x4040A0 - 0x404080 + 0x3080 = 0x20 + 0x3080 = 0x30A0
```



```
// 在编译时初始化__attribute__((constructor))staticvoidinit(){ // chall数组的初始化...}
```



```
$ nm lambda | grep chall0000000000558420 B chall
```



```
地址0x558420: chall[0] (8字节) -> 指向第1组的lambda表达式地址0x558428: chall[1] (8字节) -> 指向第2组的lambda表达式地址0x558430: chall[2] (8字节) -> 指向第3组的lambda表达式...地址0x558478: chall[10] (8字节) -> 指向第11组的lambda表达式
```



```
struct_Exp{ ExpType type; // 4字节 - 节点类型（Symbol/Lambda/Call） // padding: 4字节（内存对齐） union{ Symbol symbol; // 8字节 - 变量索引 struct{ Symbol arg; // 8字节 - lambda参数 constExp* body;// 8字节 - lambda函数体指针 } lambda; struct{ constExp* rator;// 8字节 - 函数部分指针 constExp* rand; // 8字节 - 参数部分指针 } call; } u;};// 总共：4 + 4(padding) + 16 = 24字节 = 0x18字节
```



```
# .data段基本信息data_vaddr =0x404080 # 虚拟地址data_offset =0x3080 # 文件偏移# 第一组的起始地址（通过分析得出）base_addr =0x4040A0size =4775# 节点数量# 每个节点24字节 (0x18)# 第二组的地址 = 第一组地址 + 4775 * 0x18
```



```
importsubprocess# 每组的参数（通过计算得出）groups_params = [ (0x4040A0,0x30A0,4775), # 第1组 (0x420048,0x3ffc8,5173), # 第2组 (0x440730,0x606b0,4647), # 第3组 (0x459DC8,0x79D48,4647), # 第4组 # ... 其他组]fori, (vaddr, offset, size)inenumerate(groups_params): print(f"提取第{i+1}组...") # 修改decompiler.py的参数 modified_code = decompiler_template.replace( 'loadLambda(0x4040A0, 0x30A0, 0x1BFA8//0x18)', f'loadLambda(0x{vaddr:x}, 0x{offset:x},{size})' ) # 运行并保存输出 result = subprocess.run(['python3','-c', modified_code], capture_output=True, text=True) withopen(f'group{i+1}_output.txt','w')asf: f.write(result.stdout)
```



```
(Pair (Pair (Pair 4 (Pair 2 (Pair 5 Nil))) (Pair 7 (Pair 4 (Pair 5 Nil))) (Pair 6 (Pair 5 (Pair 2 Nil)))) (Pair 1011 (Pair 1325 (Pair 1094 Nil))))
```



```
矩阵 = [[4,2,5], [7,4,5], [6,5,2]]结果 = [1011,1325,1094]
```



```
importnumpyasnpmat = np.array([[4,2,5], [7,4,5], [6,5,2]], dtype=float)res = np.array([1011,1325,1094], dtype=float)solution = solve(mat.copy(), res.copy())print(solution) # [88. 67. 84.]# 转换为字符flag_part =''.join(chr(int(x))forxinsolution)print(flag_part) # 'XCT'
```



```
矩阵: [[2,3,6], [4,3,6], [2,7,5]]结果: [1119,1223,1487]解: [70,123,77] # 'F{M'
```



```
矩阵: [[7,6,2], [4,4,7], [2,2,2]]结果: [1297,1338,723]解: [52,116,82] # '4tR'
```



```
矩阵: [[2,4,2], [3,2,4], [3,3,7]]结果: [842,1051,1418]解: [73,49,124] # 'I1|'
```



```
AssertionError: ret % 0x18 != 0 or ret < 0
```



```
deftoIdx(ret): ret -= base assertret %0x18==0andret >=0 returnret //0x18
```



```
mat = np.random.randint(2,8, size=(3,3)) # 每次编译都会重新随机！
```



```
M' × X' + 7 = R
```



```
importnumpyasnpdefgen_valid_matrix_and_result(flag_chars): """ 使用与compiler.py完全相同的算法生成有效数据 """ assertlen(flag_chars) ==3 # 步骤1：转换为ASCII flag_arr = np.array([ord(c)forcinflag_chars], dtype=int) # 步骤2：预处理（与compiler.py相同） flag_arr_prime = flag_arr -13- np.array([5,2,0], dtype=int) # 步骤3：随机生成矩阵（2-7范围，与compiler.py相同） mat = np.random.randint(2,8, size=(3,3)) mat_bak = np.array(mat, dtype=float) # 步骤4：计算结果（与compiler.py相同） mat_transformed = np.array(mat, dtype=int) foriinrange(3): mat_transformed[i] += np.array([0,1,3], dtype=int) res = np.matmul(mat_transformed, flag_arr_prime) +7 # 步骤5：验证（使用solve函数） solved = solve(mat_bak.copy(), res.astype(float).copy()) solved_str ="".join(chr(int(round(x)))forxinsolved) assertsolved_str == flag_chars,f"验证失败:{solved_str}!={flag_chars}" returnmat_bak.astype(int).tolist(), res.tolist()
```



```
# 官方flag（根据题目格式和前4组推断）official_flag ="XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}"print("开始生成所有11组数据...")all_groups = []foriinrange(11): flag_segment = official_flag[i*3:i*3+3] print(f"n第{i+1}组: '{flag_segment}'") # 生成矩阵和结果 matrix, result = gen_valid_matrix_and_result(flag_segment) print(f" 矩阵:{matrix}") print(f" 结果:{result}") # 验证 mat_test = np.array(matrix, dtype=float) res_test = np.array(result, dtype=float) verified = solve(mat_test.copy(), res_test.copy()) verified_str ="".join(chr(int(round(x)))forxinverified) ifverified_str == flag_segment: print(f" 验证通过") else: print(f" 验证失败") all_groups.append({ 'index': i +1, 'solution': flag_segment, 'matrix': matrix, 'result': result })
```



```
第1组: 'XCT' 矩阵: [[5, 3, 4], [7, 3, 6], [6, 7, 6]] 结果: [1062, 1344, 1482] 验证通过第2组: 'F{M' 矩阵: [[2, 5, 4], [3, 7, 4], [3, 4, 2]] 结果: [1207, 1475, 1023] 验证通过第3组: '4tR' 矩阵: [[3, 7, 6], [5, 2, 5], [4, 7, 6]] 结果: [1538, 1032, 1572] 验证通过第4组: 'I1|' 矩阵: [[7, 6, 6], [5, 3, 7], [2, 2, 6]] 结果: [1629, 1528, 1218] 验证通过第5组: 'i||' 矩阵: [[5, 4, 3], [5, 3, 4], [6, 7, 3]] 结果: [1653, 1655, 2067] 验证通过第6组: 'l|I' 矩阵: [[4, 2, 4], [4, 6, 4], [3, 3, 4]] 结果: [1114, 1550, 1133] 验证通过第7组: 'l|I' 矩阵: [[3, 3, 4], [3, 7, 7], [7, 2, 5]] 结果: [1133, 1749, 1444] 验证通过第8组: '1X_' 矩阵: [[2, 7, 5], [3, 2, 5], [2, 2, 3]] 结果: [1309, 975, 780] 验证通过第9组: 'A5_' 矩阵: [[2, 3, 4], [3, 6, 7], [3, 3, 2]] 结果: [827, 1234, 710] 验证通过第10组: 'YC0' 矩阵: [[6, 5, 6], [3, 4, 2], [6, 3, 7]] 结果: [1060, 655, 991] 验证通过第11组: 'mb}' 矩阵: [[3, 2, 2], [7, 4, 4], [4, 6, 2]] 结果: [1089, 1843, 1512] 验证通过
```



```
final_flag ="".join(g['solution']forginall_groups)print(f"n最终Flag:{final_flag}")
```



```
最终Flag: XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}
```



```
$ ./lambda"XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}"You got 0/11 part of flag correctYou got 1/11 part of flag correctYou got 2/11 part of flag correctYou got 3/11 part of flag correctYou got 4/11 part of flag correctYou got 5/11 part of flag correctYou got 6/11 part of flag correctYou got 7/11 part of flag correctYou got 8/11 part of flag correctYou got 9/11 part of flag correctYou got 10/11 part of flag correctCongratulation! Submit the argument as the flag!
```
