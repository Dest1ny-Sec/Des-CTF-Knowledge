---
title: 看雪2023 KCTF年度赛 | 第8题·AI核心地带-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: medium
vuln_type: reverse
tags:
- AI出题
- CrackMe
- JS注册码生成
- signed char BUG
- 字符型处理
- S8左移保号
attack_chain: 修复signed char*BUG→S8左移保号修复→JS代码生成500位序列→奇偶交替填入e[9]位→k+12-d(i))%0xA计算每步code→join得到5826...序列号
key_payload: odd+k&1判断奇偶;d(i)=(0xFFFEC610>>i%0x1f)%0xA;e=[1,0,1,0,1,0,0,0,1]位图;JS算法生成582606981190746395118531851185249089744027265368693769576937697816165851808443150195011501950410798490871663488927792799277958360668112074539521851185318514909974002766535869476937695769681626582180144305010501950115040079949037162348792789277927995826067811907483951185218511853490897410272653986937694769376988161658318084433501950105019504207984904716634829277927892779584606681100745395418511852185149009740027365358697769376947696816365821809443050125019501050400790490371673487927
one_liner: KCTF2023年度赛Q8《AI核心地带》AI出题+JS注册码生成+CrackMe signed char BUG修复
lesson: 出题人故意留signed char BUG：S8左移保号使if多次成立，应用S8显式转换
quality: high
full_path: 看雪2023_KCTF年度赛_-_第8题·AI核心地带-设计思路及解析.full.md
meta_path: 看雪2023_KCTF年度赛_-_第8题·AI核心地带-设计思路及解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 看雪2023 KCTF年度赛 | 第8题·AI核心地带-设计思路及解析。KCTF2023年度赛Q8《AI核心地带》AI出题+JS注册码生成+CrackMe signed char BUG修复。经验：出题人故意留signed char BUG：S8左移保号使if多次成立，应用S8显式转换
category: reverse
subcategory: reverse
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/136265.html
reasoning_chain:
- 题目给JS算法生成注册码 → 触发点：500位长序列码，要复现生成器
- 假设：JS位图e=[1,0,1,0,1,0,0,0,1]控制k值在f()中循环选位 → 动作：逐i模拟算法跑500步
- 观察：(odd+i)&1 决定奇偶步，偶数步k=首个1位索引 → 下一步：关注奇偶分支
- d(i)=(0xFFFEC610>>>i)%0xA作为步长因子 → 假设：常数表驱动每步code生成
- m=(k+12-d(i))%0xA push入code → 动作：用Node复现JS输出5826...序列
- C端step()函数里(*p)<<3符号扩展BUG → 触发点：signed char左移保号if多次成立
- 假设：必须显式转换S8才能正确还原check流程 → 动作：patch S8转换绕过BUG
- 观察：bug修复后所有500位code都参与校验 → 下一步：500位字符串输入即成功
failed_attempts:
- 试图直接绕过JS算法手算500位 → 失败：位图翻转+奇偶交替分支太多不可手算
- 试图忽略S8 signed char BUG → 失败：IF多次成立后check会提前退出
- 把(*p)<<3当作unsigned char处理 → 失败：高位保号导致check顺序错乱
key_observations:
- JS位图+奇偶交替循环生成器是CTF出题AI常见套路
- signed char 左移保号是C语言经典BUG，VS编译器会自动扩展符号位
- 显式(S8)转换是规避平台相关行为的最佳实践
- 500位长码作为注册码 = 输入长度上限 + 验证逻辑全在客户端
- AI生成注册码类题目 = 出题人用LLM快速生成JS算法，逆向等价于JS复现
prerequisites:
- JS位图/状态机模拟能力
- signed char vs unsigned char 行为差异
- C语言类型转换 (S8) 显式转换语义
- VS编译器对char扩展规则的了解
---
# 看雪2023 KCTF年度赛 | 第8题·AI核心地带-设计思路及解析

> 原文: https://www.ctfiot.com/136265.html
> ID: 136265

这是一场人类与超智能AI的“生死”较量

请立刻集结，搭乘SpaceX，前往AI控制空间站

智慧博弈  谁能问鼎

看雪·2023 KCTF 年度赛于9月1日中午12点正式开赛！比赛基本延续往届模式，设置了难度值、火力值和精致度积分。由此来引导竞赛的难度和趣味度，使其更具挑战性和吸引力，同时也为参赛选手提供了更加公平、有趣的竞赛平台。

*注意：签到题持续开放，整个比赛期间均可提交答案获得积分

昨日中午12:
00第八题《AI核心地带》已截止答题，该题共有7支战队成功提交flag，一起来看下该题的设计思路和解析吧。

出题团队简介

设计思路

// 使用 JS 计算注册码

var odd=0;
var code=[];
var e=[1,0,1,0,1,0,0,0,1];
var d=function(i){i%=0x1f;
return (0xFFFEC610>>>i)%0xA;}
var f=function(){for(var i=0;i<9;i++)if(e[i])return +i+1;
return -1;}
var k,m;
for(var i=0;i<500;i++){
 if((odd+i)&1)k=0;
 else k=f();
 if(k>=0) e[k]=(e[k]+1)&1;
 m=(k+12-d(i))%0xA;
 console.log(m,i,e);
 code.push(m);
 if(f()<0)break;
}
code.join('');

// 本题答案
// 582606981190746395118531851185249089744027265368693769576937697816165851808443150195011501950410798490871663488927792799277958360668112074539521851185318514909974002766535869476937695769681626582180144305010501950115040079949037162348792789277927995826067811907483951185218511853490897410272653986937694769376988161658318084433501950105019504207984904716634829277927892779584606681100745395418511852185149009740027365358697769376947696816365821809443050125019501050400790490371673487927

/**
 * pos = [0,1,2,...,9]
 */
void step(S32* L, S32* S, int pos){
//  S8* p; // signed char* 修复为 char*，修复如下
    char* p;
    int i;
    for(i=0;i<LOCKS32;i++)
        L[i]^=S[pos];
    if(pos>8){
//      p=((S8*)(S+9))+1; // signed char* 修复为 char*，修复如下
        p=((char*)(S+9))+1;
//      if(((*p)<<3)>=0) *p=(~*p)&0x7F;
//      BUG: signed char 左移会保号导致IF多次成立，应为首次成立，修复如下
        if((S8)((*p)<<3)>=0) *p=(~*p)&0x7F;
    }
}

赛题解析

本题解析由看雪大牛 奔跑的阿狸 提供：

1.IDA加载，发现如下字符串

//称为flag[10]，看做10个int数
00402100 66 6C 61 67 7B 42 7A 63 5A 44 6E 66 4E 49 71 6D flag{BzcZDnfNIqm
00402110 51 43 74 6B 54 47 6C 77 4C 79 44 59 65 69 48 49 QCtkTGlwLyDYeiHI
00402120 6A 78 53 58 77 6B 52 4B 7A 70 46 50 76 7D 00 00 jxSXwkRKzpFPv}..
//称为check[5]，取20字节，看做5个int
00402130 43 61 6E 20 79 6F 75 20 63 72 61 63 6B 20 6D 65 Can you crack me
00402140 3F 5E 6F 6C 6F 5E 00 00 ?^olo^.

2.输入最多1000位

if ( input_len <= 0 || (input_len_1 = input_len - 1, input[input_len - 1] != 'n') )
 {
 v3 = 1; // 错误
 v27 = 1;
 }

3.输入只能是数字

input_num = input[v8];
 if ( (unsigned int)(input_num - '0') <= 9 )// 只能输入数字
 break;
 v3 = 1; //这个数不能等于1
 v27 = 1; //这个数也不能等于1

4.然后后面的代码很乱，看不懂在干啥，一度不想做这道题了

5.分析关键代码

//根据下标和对应的数字，转换出一个0-9的数
v12 = (input_num + (0xFFFEC610 >> input_id % 31)) % 0xA;
//奇数位，v12==0；偶数位，v12!=0
if ( (input_id & 1) != v12 < 1 )
 v27 = 1;
//将check数组中5个int做xor，得到4字节=v28
v28 = v38 ^ HIDWORD(v37) ^ v37 ^ HIDWORD(v36) ^ v36;
if ( v25 ) //如果是input最后一位，就进行校验
{
//v28的 (((bit0 ^ bit2) & 0x1F) == 0)
//v28的 (((bit1 ^ bit3) & 0x1F) == 0)
 if ( ((unsigned __int8)v28 ^ (unsigned __int8)(BYTE2(v38) ^ BYTE6(v37) ^ BYTE2(v37) ^ BYTE6(v36) ^ BYTE2(v36))) & 0x1F// 也就是说这个条件，必须成立
 || (HIBYTE(v28) ^ BYTE1(v28)) & 0x1F )
 {
 v13 = -1; //v13等于-1是成功状态
 }
 goto LABEL_27;
}
//根据v12取出flag中的4字节，分别跟check的5个数xor
v17 = v31[v12];
LODWORD(v36) = v17 ^ v36; // 那20字节，跟选定的数字xor
HIDWORD(v36) ^= v17;
LODWORD(v37) = v17 ^ v37;
HIDWORD(v37) ^= v17;
//xor后的数据要满足
if ( v12 >= 6 )
{
 if ( ((unsigned __int8)v28 ^ BYTE2(v28)) & 0x1F )
 {
LABEL_26:
 v13 = 9; //将当前v12重置为9
 goto LABEL_27;
 }
 v15 = 13 - v12;
}
else
{
 v15 = 8 - v12;
 v16 = v28; // =0
}
if ( (v16 << v15) + -128 == v14 << v15 ) //需要成立
 goto LABEL_27;

6.然后整理下大概逻辑：
check数组有初始状态
flag数组是始终不变的
根据input的每一位，计算出一个下标id，选取flag[id]
将check数组5个数，分别跟flag[id] xor，最终会进行一个校验

7.因为xor具有偶数次消除的性质，所以先编写脚本，跑出最终结果需要flag中的[0] [2] [4] [8]

//标记10层，每层选取的元素是谁
unsigned int id08[10] = { -1,-1,-1,-1,-1,-1,-1,-1,-1,-1 };

//判断数组是否合规 1=合规 0=错误
int judge08(unsigned int *flag, unsigned int *check)
{
 unsigned int final[5] = { 0 };
 for (int i = 0; i < 5; i++)
 final[i] = check[i];

 for (int i = 0; i < 10; i++)	//flag用10次
 {
 if (id08[i] == -1)	//不跟这个数参与xor
 continue;

 for (int j = 0; j < 5; j++)	//check中是5个4位数
 {
 final[j] ^= flag[i];
 }
 }

 final[0] = final[0] ^ final[1] ^ final[2] ^ final[3] ^ final[4];
 int bit0 = (final[0] & 0xFF000000) >> 24;
 int bit1 = (final[0] & 0xFF0000) >> 16;
 int bit2 = (final[0] & 0xFF00) >> 8;
 int bit3 = final[0] & 0xFF;
 printf("%xn", final[0]);

 int e = bit0 ^ bit2;
 int f = bit1 ^ bit3;
 printf("%x %xn", e, f);

 if (((e & 0x1F) == 0) && ((f & 0x1F) == 0))
 {
 printf("%x %xn", (e & 0x1F), (f & 0x1F));
 return 1;
 }
 return 0;
}

//depth表示当前层级，一共遍历39层
void search08(unsigned int *flag, unsigned int *check, int depth)
{
 if (depth == 10)
 {
 //printArr(id08, 10);

 if (judge08(flag, check))
 {
 printf("heihein");
 printArr(id08, 10);
 exit(0);
 }
 return;
 }

 for (int i = 0; i < 2; i++)
 {
 if (i == 0)
 id08[depth] = 1;
 else
 id08[depth] = -1;
 search08(flag, check, depth + 1);
 }
 return;
}

8.但是结果只选4位，分别对应0248，那样又不行，因为还有其他限制

8.1 奇数位，v12必须等于0；偶数位，v12不能等于0

8.2 若成立，flag下标就设定位为9
((unsigned __int8)v28 ^ BYTE2(v28)) & 0x1F

8.3 若成立，就能跳过flag设定为9
if ( (v16 << v15) + -128 == v14 << v15 )
goto LABEL_27;

9.又因为 0248必须是奇数个数，4个奇数=偶数。135679都是偶数，所以input是偶数位。

然后就编码跑数据

int judge08_2(unsigned int *flag, unsigned int *check, int index)
{
 for (int j = 0; j < 5; j++)	//check中是5个4位数
 {
 check[j] ^= flag[index];
 }

 int num = check[0] ^ check[1] ^ check[2] ^ check[3] ^ check[4];
 int bit0 = (num & 0xFF000000) >> 24;
 int bit1 = (num & 0xFF0000) >> 16;
 int bit2 = (num & 0xFF00) >> 8;
 int bit3 = num & 0xFF;
 //printf("%xn", num);

 int e = bit0 ^ bit2;
 int f = bit1 ^ bit3;
 //printf("%x %xn", e, f);

 if (((e & 0x1F) == 0) && ((f & 0x1F) == 0))
 {
 //printf("%x %xn", (e & 0x1F), (f & 0x1F));
 return 1;
 }
 return 0;
}

void ctf08()
{
 unsigned int check[] = { 0x43616e20, 0x796f7520, 0x63726163, 0x6b206d65, 0x3f5e6f6c };
 unsigned int flag[] = {
 0x427a635a,
 0x446e664e,
 0x49716d51,
 0x43746b54,
 0x476c774c,
 0x79445965,
 0x6948496a,
 0x78535877,
 0x6b524b7a,
 0x70465076
 };

 for (int i = 0; i < 1000; i++)
 {
 int j = 0;
 for (; j < 10; j++)	//从0-9遍历
 {
 int v12 = ((0xFFFEC610 >> i % 31) + (0x30 + j)) % 0xA;
 if ((i & 1) != v12 < 1)	//过滤掉不符合的数字
 continue;

 if (v12 == 0)	//i是奇数位
 {
 for (int k = 0; k < 5; k++)	//check中是5个4位数
 {
 check[k] ^= flag[v12];	//其实也就是0位
 }
 printf("id=%d num=%d v12=%dn", i, j, v12);
 break;
 }

 int num = check[0] ^ check[1] ^ check[2] ^ check[3] ^ check[4];

 //75 73 1D 00=0x001d7375
 int al = (num & 0xFF00) >> 8;	//73
 int dl = (num & 0xFF000000) >> 24;

 int v15;
 if (v12 >= 6)
 {
 int e = al ^ dl;
 if ((e & 0x1F) != 0)
 continue;

 v15 = 13 - v12;
 al = num & 0xFF;
 dl = (num & 0xFF0000) >> 16;
 }
 else
 v15 = 8 - v12;

 int a = (al << v15) & 0xff;
 int b = (dl << v15) & 0xff;
 if (a == ((128 + b) & 0xff))
 {
 printf("id=%d num=%d v12=%dn", i, j, v12);

 if (judge08_2(flag, check, v12))
 {
 printf("hahaha");
 exit(0);
 }

 break;
 }
 }

 if (j == 10)	//没找到数字的话
 {
 for (int k = 0; k < 5; k++)	//check中是5个4位数
 {
 check[j] ^= flag[9];	//其实也就是0位
 }
 printf("id=%d [9]n", i);
 }
 }
 //search08(flag, check, 0);
}

10.跑出来的数据，再手动根据0248原则筛选，最后发现从486位截断不要9就行了。
5826069811907463951185318511852490897440272653686937695769376978161658518084
4315019501150195041079849087166348892779279927795836066811207453952185118531
8514909974002766535869476937695769681626582180144305010501950115040079949037
1623487927892779279958260678119074839511852185118534908974102726539869376947
6937698816165831808443350195010501950420798490471663482927792789277958460668
1100745395418511852185149009740027365358697769376947696816365821809443050125
019501050400790490371673487927

昨日中午12：00

第九题《突破防线》已开赛！

在这个充满变数的赛场上，没有人能够预料到最终的结局。有时，优势的领先可能只是一时的，一瞬间的失误就足以颠覆一切。而那些一直默默努力、不断突破自我的人，往往会在最后关头迎头赶上，成为最耀眼的存在。

谁能保持领先优势？谁能迎头赶上？谁又能突出重围成为黑马？

球分享

球点赞

球在看

点击阅读原文进入比赛


```
// 使用 JS 计算注册码

var odd=0;
var code=[];
var e=[1,0,1,0,1,0,0,0,1];
var d=function(i){i%=0x1f;
return (0xFFFEC610>>>i)%0xA;}
var f=function(){for(var i=0;i<9;i++)if(e[i])return +i+1;
return -1;}
var k,m;
for(var i=0;i<500;i++){
 if((odd+i)&1)k=0;
 else k=f();
 if(k>=0) e[k]=(e[k]+1)&1;
 m=(k+12-d(i))%0xA;
 console.log(m,i,e);
 code.push(m);
 if(f()<0)break;
}
code.join('');

// 本题答案
// 582606981190746395118531851185249089744027265368693769576937697816165851808443150195011501950410798490871663488927792799277958360668112074539521851185318514909974002766535869476937695769681626582180144305010501950115040079949037162348792789277927995826067811907483951185218511853490897410272653986937694769376988161658318084433501950105019504207984904716634829277927892779584606681100745395418511852185149009740027365358697769376947696816365821809443050125019501050400790490371673487927
/**
 * pos = [0,1,2,...,9]
 */
void step(S32* L, S32* S, int pos){
//  S8* p; // signed char* 修复为 char*，修复如下
    char* p;
    int i;
    for(i=0;i<LOCKS32;i++)
        L[i]^=S[pos];
    if(pos>8){
//      p=((S8*)(S+9))+1; // signed char* 修复为 char*，修复如下
        p=((char*)(S+9))+1;
//      if(((*p)<<3)>=0) *p=(~*p)&0x7F;
//      BUG: signed char 左移会保号导致IF多次成立，应为首次成立，修复如下
        if((S8)((*p)<<3)>=0) *p=(~*p)&0x7F;
    }
}
//称为flag[10]，看做10个int数
00402100 66 6C 61 67 7B 42 7A 63 5A 44 6E 66 4E 49 71 6D flag{BzcZDnfNIqm
00402110 51 43 74 6B 54 47 6C 77 4C 79 44 59 65 69 48 49 QCtkTGlwLyDYeiHI
00402120 6A 78 53 58 77 6B 52 4B 7A 70 46 50 76 7D 00 00 jxSXwkRKzpFPv}..
//称为check[5]，取20字节，看做5个int
00402130 43 61 6E 20 79 6F 75 20 63 72 61 63 6B 20 6D 65 Can you crack me
00402140 3F 5E 6F 6C 6F 5E 00 00 ?^olo^.
if ( input_len <= 0 || (input_len_1 = input_len - 1, input[input_len - 1] != 'n') )
 {
 v3 = 1; // 错误
 v27 = 1;
 }
input_num = input[v8];
 if ( (unsigned int)(input_num - '0') <= 9 )// 只能输入数字
 break;
 v3 = 1; //这个数不能等于1
 v27 = 1; //这个数也不能等于1
//根据下标和对应的数字，转换出一个0-9的数
v12 = (input_num + (0xFFFEC610 >> input_id % 31)) % 0xA;
//奇数位，v12==0；偶数位，v12!=0
if ( (input_id & 1) != v12 < 1 )
 v27 = 1;
//将check数组中5个int做xor，得到4字节=v28
v28 = v38 ^ HIDWORD(v37) ^ v37 ^ HIDWORD(v36) ^ v36;
if ( v25 ) //如果是input最后一位，就进行校验
{
//v28的 (((bit0 ^ bit2) & 0x1F) == 0)
//v28的 (((bit1 ^ bit3) & 0x1F) == 0)
 if ( ((unsigned __int8)v28 ^ (unsigned __int8)(BYTE2(v38) ^ BYTE6(v37) ^ BYTE2(v37) ^ BYTE6(v36) ^ BYTE2(v36))) & 0x1F// 也就是说这个条件，必须成立
 || (HIBYTE(v28) ^ BYTE1(v28)) & 0x1F )
 {
 v13 = -1; //v13等于-1是成功状态
 }
 goto LABEL_27;
}
//根据v12取出flag中的4字节，分别跟check的5个数xor
v17 = v31[v12];
LODWORD(v36) = v17 ^ v36; // 那20字节，跟选定的数字xor
HIDWORD(v36) ^= v17;
LODWORD(v37) = v17 ^ v37;
HIDWORD(v37) ^= v17;
//xor后的数据要满足
if ( v12 >= 6 )
{
 if ( ((unsigned __int8)v28 ^ BYTE2(v28)) & 0x1F )
 {
LABEL_26:
 v13 = 9; //将当前v12重置为9
 goto LABEL_27;
 }
 v15 = 13 - v12;
}
else
{
 v15 = 8 - v12;
 v16 = v28; // =0
}
if ( (v16 << v15) + -128 == v14 << v15 ) //需要成立
 goto LABEL_27;
//标记10层，每层选取的元素是谁
unsigned int id08[10] = { -1,-1,-1,-1,-1,-1,-1,-1,-1,-1 };

//判断数组是否合规 1=合规 0=错误
int judge08(unsigned int *flag, unsigned int *check)
{
 unsigned int final[5] = { 0 };
 for (int i = 0; i < 5; i++)
 final[i] = check[i];

 for (int i = 0; i < 10; i++)	//flag用10次
 {
 if (id08[i] == -1)	//不跟这个数参与xor
 continue;

 for (int j = 0; j < 5; j++)	//check中是5个4位数
 {
 final[j] ^= flag[i];
 }
 }

 final[0] = final[0] ^ final[1] ^ final[2] ^ final[3] ^ final[4];
 int bit0 = (final[0] & 0xFF000000) >> 24;
 int bit1 = (final[0] & 0xFF0000) >> 16;
 int bit2 = (final[0] & 0xFF00) >> 8;
 int bit3 = final[0] & 0xFF;
 printf("%xn", final[0]);

 int e = bit0 ^ bit2;
 int f = bit1 ^ bit3;
 printf("%x %xn", e, f);

 if (((e & 0x1F) == 0) && ((f & 0x1F) == 0))
 {
 printf("%x %xn", (e & 0x1F), (f & 0x1F));
 return 1;
 }
 return 0;
}

//depth表示当前层级，一共遍历39层
void search08(unsigned int *flag, unsigned int *check, int depth)
{
 if (depth == 10)
 {
 //printArr(id08, 10);

 if (judge08(flag, check))
 {
 printf("heihein");
 printArr(id08, 10);
 exit(0);
 }
 return;
 }

 for (int i = 0; i < 2; i++)
 {
 if (i == 0)
 id08[depth] = 1;
 else
 id08[depth] = -1;
 search08(flag, check, depth + 1);
 }
 return;
}
int judge08_2(unsigned int *flag, unsigned int *check, int index)
{
 for (int j = 0; j < 5; j++)	//check中是5个4位数
 {
 check[j] ^= flag[index];
 }

 int num = check[0] ^ check[1] ^ check[2] ^ check[3] ^ check[4];
 int bit0 = (num & 0xFF000000) >> 24;
 int bit1 = (num & 0xFF0000) >> 16;
 int bit2 = (num & 0xFF00) >> 8;
 int bit3 = num & 0xFF;
 //printf("%xn", num);

 int e = bit0 ^ bit2;
 int f = bit1 ^ bit3;
 //printf("%x %xn", e, f);

 if (((e & 0x1F) == 0) && ((f & 0x1F) == 0))
 {
 //printf("%x %xn", (e & 0x1F), (f & 0x1F));
 return 1;
 }
 return 0;
}

void ctf08()
{
 unsigned int check[] = { 0x43616e20, 0x796f7520, 0x63726163, 0x6b206d65, 0x3f5e6f6c };
 unsigned int flag[] = {
 0x427a635a,
 0x446e664e,
 0x49716d51,
 0x43746b54,
 0x476c774c,
 0x79445965,
 0x6948496a,
 0x78535877,
 0x6b524b7a,
 0x70465076
 };

 for (int i = 0; i < 1000; i++)
 {
 int j = 0;
 for (; j < 10; j++)	//从0-9遍历
 {
 int v12 = ((0xFFFEC610 >> i % 31) + (0x30 + j)) % 0xA;
 if ((i & 1) != v12 < 1)	//过滤掉不符合的数字
 continue;

 if (v12 == 0)	//i是奇数位
 {
 for (int k = 0; k < 5; k++)	//check中是5个4位数
 {
 check[k] ^= flag[v12];	//其实也就是0位
 }
 printf("id=%d num=%d v12=%dn", i, j, v12);
 break;
 }

 int num = check[0] ^ check[1] ^ check[2] ^ check[3] ^ check[4];

 //75 73 1D 00=0x001d7375
 int al = (num & 0xFF00) >> 8;	//73
 int dl = (num & 0xFF000000) >> 24;

 int v15;
 if (v12 >= 6)
 {
 int e = al ^ dl;
 if ((e & 0x1F) != 0)
 continue;

 v15 = 13 - v12;
 al = num & 0xFF;
 dl = (num & 0xFF0000) >> 16;
 }
 else
 v15 = 8 - v12;

 int a = (al << v15) & 0xff;
 int b = (dl << v15) & 0xff;
 if (a == ((128 + b) & 0xff))
 {
 printf("id=%d num=%d v12=%dn", i, j, v12);

 if (judge08_2(flag, check, v12))
 {
 printf("hahaha");
 exit(0);
 }

 break;
 }
 }

 if (j == 10)	//没找到数字的话
 {
 for (int k = 0; k < 5; k++)	//check中是5个4位数
 {
 check[j] ^= flag[9];	//其实也就是0位
 }
 printf("id=%d [9]n", i);
 }
 }
 //search08(flag, check, 0);
}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]