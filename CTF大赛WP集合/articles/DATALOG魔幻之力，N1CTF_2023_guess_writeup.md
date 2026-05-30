# DATALOG魔幻之力，N1CTF 2023 guess writeup

> 原文: https://www.ctfiot.com/141277.html
> ID: 141277

对于一道静态分析相关的CTF题目，如何兼顾题目与静态分析的相关性和选手做题时的体验感是出题时面临的最大困难。若在实战方向命题，例如要求使用静态分析进行漏洞挖掘或利用静态分析算法本身的漏洞，题目本身就具有较高的门槛，选手几乎无法通过临场学习完成题目。若在纯理论方向命题，例如开发分析算法并评估指标，往往会使题目丧失趣味性，且容易使0基础选手直接放弃题目。

本题在设计时采用了Soufflé作为背景，Soufflé是一个与datalog类似的逻辑编程语言执行引擎，在静态分析领域有广泛应用。题目要求选手阅读Soufflé的文档并理解部分执行原理，从而用技巧获得flag。由于规避了静态分析理论体系的学习，0基础选手也可能在48小时的比赛内完成题目，提高了题目的参与度和体验感，也希望本题能引发选手对于静态分析领域的学习兴趣。

cscat

寻臻科技初创核心，Nu1L Team比赛负责人

cyberutopian

题目信息

题目给出了一个Soufflé源文件：

.functor hash1(x:symbol):number
.functor hash2(x:symbol):number
.functor GETFLAG():symbol

.decl SALT(x:symbol)
//SALTS
.output SALT

.decl FLAG(x:symbol)
FLAG(@GETFLAG()).
.decl HINT(x:symbol)
HINT(substr(x,0,4)) :- FLAG(x).

.decl HASH(x:number)
HASH(@hash1(x)) :- FLAG(x).

.decl SALT_HASH1(h:number,s:symbol)
SALT_HASH1(h,s) :- h=@hash1(cat(flg,s)),FLAG(flg),SALT(s).

.decl SALT_HASH2(h:number,s:symbol)
SALT_HASH2(h,s) :- h=@hash2(cat(flg,s)),FLAG(flg),SALT(s).

.decl GUESS(x:symbol)
//GUESS
.output GUESS(attributeNames="ans")

题目服务器chal.py（部分代码省略）：
# Enjoy the music :)
SALT_DICT=base64.b64decode(b'aHR0cHM6Ly95LnFxLmNvbS9uL3J5cXEvc29uZ0RldGFpbC8wMDAyOTJXNjJvODd3Rg==')

def generate_salts():
    num_salts=random.randint(1,16)
    return [bytes(random.choices(SALT_DICT,k=random.randint(16,32))) for _ in range(num_salts)]

def generate_tmpflag():
    return os.urandom(32).hex().encode()

# ...

# compile and write dl file using given salts and your guess rules
def generate_dl(salts,guesser):
    G=f'GUESS(x) :- {guesser}.'
    S='n'.join([f'SALT("{i.decode()}").' for i in salts])
    compiled_chal=chal_template.replace('//GUESS',G).replace("//SALTS",S)
    os.truncate(chal_fd,0)
    os.pwrite(chal_fd,compiled_chal.encode(),0)

# run souffle and check your answer
def run_chal(TMPFLAG):
    cmdline=f"timeout -s KILL 1s ./souffle -D- -lhash --no-preprocessor -w {chal_path}"
    proc=subprocess.Popen(args=cmdline,shell=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={"TMPFLAG":TMPFLAG})
    proc.wait()
    out=proc.stdout.read()
    prefix=b'---------------nGUESSnansn===============n'
    if not out.startswith(prefix):
        raise RuntimeError(f'Souffle error? {out}')
    out=out.removeprefix(prefix)[:64]
    if out!=TMPFLAG:
        raise RuntimeError(f"Wrong guess")

# check user guess rules
def check_user_rules(r:str):
    if len(r) > 300:
        raise RuntimeError("rule too looong")
    e=r.encode()
    ban_chars=b'Ff.'
    for i in e:
        if i>0x7f or i<0x20 or i in ban_chars:
            raise RuntimeError("illegal char in rule")

# how many rounds will you guess
DIFFICULTY=36

def game():
    user_rules=input("your rules?n")
    check_user_rules(user_rules)
    for i in range(DIFFICULTY):
        generate_dl(generate_salts(),user_rules)
        run_chal(generate_tmpflag())
        print(f"guess {i} is correct")
    print("Congratulations! Here is your flag:")
    os.system("/readflag")

cyberutopian

题目分析

分析chal.py的交互代码，可以发现选手的任务是填写关系GUESS的推理规则，使得x始终为外部随机flag。Soufflé源文件共运行36次，如果GUESS的推理结果都正确，则输出题目flag。

Soufflé源文件中@GETFLAG、@hash1、@hash2为外部库函数。@GETFLAG用来获取每轮执行时的外部临时flag，@hash1和@hash2是字符串哈希函数。

一种比较显然的推理规则是FLAG(x)或x=@GETFLAG()，但chal.py要求推理规则中不能出现Ff.三个字符，所以选手无法直接获取flag。

另一个思路是通过关系HINT获取flag的前4字符，SALT_HASH1和SALT_HASH2获取hash(flag+salt)和salt，通过数学运算倒推flag。但flag过长，hash函数保留信息有限，容易证明无法通过hash和salt的组合恢复flag。

此时需要选手阅读文档，使用Soufflé引擎的特性获得flag。

在Soufflé中，所有的字符串（symbol）都存储于一个全局的symbol table中，字符串在关系数据中的表示形式是symbol table的序号（ordinal number）。当推理过程产生一个新字符串时，会尝试插入到symbol table中，获得其序号表示。需要猜测的flag是functor GETFLAG产生的字符串，会被插入到symbol table中。我们无法直接访问flag，但可以猜测其在symbol table中的序号。而souffle也提供了序号和字符串相互转换的功能，x=as(<序号>,symbol)即可推理出正确的flag，ord(@GETFLAG())可得到flag字符串的序号。

由于chal.py在每轮猜测会生成个数不同的salt，flag字符串的序号也会变化。如果将flag序号写成常数，无法通过36轮的猜测。选手的解法包括通过其他字符串的序号计算flag的序号（两者差值固定）、通过GUESS规则所在的行数（__LINE__）计算salt个数，从而算出flag的序号。

读者在自行尝试编写规则时，可能遇到两点问题，笔者也在这里进行分析。

1-用ord(@GETFLAG())得到了flag的序号和__LINE__的关系，但直接填写x=as(__LINE-…,symbol)无法得到flag。

这与Soufflé的计算优化有关。Soufflé在实际运行用户程序前，会进行一定程度的优化。其中一步优化为“移除多余关系”。如果关系GUESS的推理规则为x=as(__LINE__-...,symbol)，那么得到程序输出需要求解的关系只有GUESS和SALT。关系FLAG并没有被任何输出直接或间接地引用，因而被删除了。而Soufflé将外部functor返回的symbol插入symbol table的过程发生在用户程序运行时，关系FLAG被删除后，flag不再存在于symbol table。此时需要选手添加GUESS对FLAG的依赖关系，例如HINT(_)。

2-如果规则用到了SALT，会导致Soufflé先输出SALT，再输出GUESS，导致chal.py报错。

这是Soufflé的求解策略决定的。如果规则用到了SALT，那么SALT的推理顺序要早于GUESS，由于SALT是一个需要输出的关系，所以SALT的求解过程也包括SALT的输出过程。呈现出来的结果就是先输出SALT的内容，再输出GUESS的内容。

cyberutopian

题目解法

点击关注公众号，回复n1ctf2023获取题目wp

cyberutopian 新一代开放式程序分析的引领者

从Datalog到开放式代码分析

在对目标程序进行静态分析时，通常需要静态分析工具的开发者将相应的做法进行实现，编码过程完成后，该工具所针对的场景、能分析的问题也基本随之确定。用户通过工具开发者提供的使用方法将源程序传入，经过工具分析并输出对应的扫描结果。在这个过程，使用者通常不会对工具分析的主要逻辑进行二次修改，但如果一旦使用者有了无法被满足的需求，或者发现了现有方案的问题，此时便需要对工具进行二次开发。对静态分析工具进行二次开发的成本是十分高昂的，无论是理解原有项目，又或是新增新的分析能力，都对开发者在静态分析领域的能力有很高的要求。

与常见的静态分析做法不同，基于Datalog的程序分析以抽取出来的程序数据为基础形成数据分析平台。结合基于Datalog规范设计的DSL语言，便能够构建出不同的模块，用于实现程序分析不同流程的各个环节，基于Datalog的程序分析实质上变成了以模块相连接的链式行为。在Datalog程序分析方向中，CodeQL、Doop作为较为常见的两个分析框架便能充分体现这个特点。在使用这些框架进行程序分析时，我们实质上是在使用开发者预先已经开发好的模块进行分析。

这些模块足够开放且易于定制化修改，使用者可以在不进行深入理解分析逻辑的前提下，快速构建出满足特定需求的分析逻辑。在这个使用过程中，静态分析能力不再封闭且难以理解，而是足够开放并易于使用。因此，我们以Soufflé为基础设计了这道题目，希望大家能从中对这个领域了解更多一些。

我们也将在不久后发布寻臻科技在开放式代码分析方向上的产品，涵盖了从支持高级语法特性的DSL到更快的推理引擎等多个层面，我们希望它能带给行业更多且更好的变化，敬请期待。


```
.functor hash1(x:symbol):number
.functor hash2(x:symbol):number
.functor GETFLAG():symbol

.decl SALT(x:symbol)
//SALTS
.output SALT

.decl FLAG(x:symbol)
FLAG(@GETFLAG()).
.decl HINT(x:symbol)
HINT(substr(x,0,4)) :- FLAG(x).

.decl HASH(x:number)
HASH(@hash1(x)) :- FLAG(x).

.decl SALT_HASH1(h:number,s:symbol)
SALT_HASH1(h,s) :- h=@hash1(cat(flg,s)),FLAG(flg),SALT(s).

.decl SALT_HASH2(h:number,s:symbol)
SALT_HASH2(h,s) :- h=@hash2(cat(flg,s)),FLAG(flg),SALT(s).

.decl GUESS(x:symbol)
//GUESS
.output GUESS(attributeNames="ans")

题目服务器chal.py（部分代码省略）：
# Enjoy the music :)
SALT_DICT=base64.b64decode(b'aHR0cHM6Ly95LnFxLmNvbS9uL3J5cXEvc29uZ0RldGFpbC8wMDAyOTJXNjJvODd3Rg==')

def generate_salts():
    num_salts=random.randint(1,16)
    return [bytes(random.choices(SALT_DICT,k=random.randint(16,32))) for _ in range(num_salts)]

def generate_tmpflag():
    return os.urandom(32).hex().encode()

# ...

# compile and write dl file using given salts and your guess rules
def generate_dl(salts,guesser):
    G=f'GUESS(x) :- {guesser}.'
    S='n'.join([f'SALT("{i.decode()}").' for i in salts])
    compiled_chal=chal_template.replace('//GUESS',G).replace("//SALTS",S)
    os.truncate(chal_fd,0)
    os.pwrite(chal_fd,compiled_chal.encode(),0)

# run souffle and check your answer
def run_chal(TMPFLAG):
    cmdline=f"timeout -s KILL 1s ./souffle -D- -lhash --no-preprocessor -w {chal_path}"
    proc=subprocess.Popen(args=cmdline,shell=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={"TMPFLAG":TMPFLAG})
    proc.wait()
    out=proc.stdout.read()
    prefix=b'---------------nGUESSnansn===============n'
    if not out.startswith(prefix):
        raise RuntimeError(f'Souffle error? {out}')
    out=out.removeprefix(prefix)[:64]
    if out!=TMPFLAG:
        raise RuntimeError(f"Wrong guess")

# check user guess rules
def check_user_rules(r:str):
    if len(r) > 300:
        raise RuntimeError("rule too looong")
    e=r.encode()
    ban_chars=b'Ff.'
    for i in e:
        if i>0x7f or i<0x20 or i in ban_chars:
            raise RuntimeError("illegal char in rule")

# how many rounds will you guess
DIFFICULTY=36

def game():
    user_rules=input("your rules?n")
    check_user_rules(user_rules)
    for i in range(DIFFICULTY):
        generate_dl(generate_salts(),user_rules)
        run_chal(generate_tmpflag())
        print(f"guess {i} is correct")
    print("Congratulations! Here is your flag:")
    os.system("/readflag")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/2-1698387918.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1698387920.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/6-1698387923.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1698387925.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/6-1698387927.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/8-1698387929.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1698387931.png)