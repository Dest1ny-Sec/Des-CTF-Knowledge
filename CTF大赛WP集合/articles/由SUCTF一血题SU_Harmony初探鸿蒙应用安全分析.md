# 由SUCTF一血题SU_Harmony初探鸿蒙应用安全分析

> 原文: https://www.ctfiot.com/224542.html
> ID: 224542

前言

周末SUCTF偶遇SU_Harmony，拼尽全力拿下一血就跑，没想到被官方提到了：

于是借编写此题wp的机会，梳理一下鸿蒙的应用程序（主要是其中的HAP包）的逆向方法。本文内容仅供学习交流之用，请勿将其用于任何非法用途。

HAP包介绍

此处摘录一段官方文档中对HAP包的介绍：

HAP（Harmony Ability Package）是应用安装和运行的基本单元。HAP包是由代码、资源、第三方库、配置文件等打包生成的模块包，其主要分为两种类型：entry和feature。

entry：应用的主模块，作为应用的入口，提供了应用的基础功能。

feature：应用的动态特性模块，作为应用能力的扩展，可以根据用户的需求和设备类型进行选择性安装。

应用程序包可以只包含一个基础的entry包，也可以包含一个基础的entry包和多个功能性的feature包。

本题只提供了名为entry-default-unsigned.hap的HAP包，从命名可以看出这是其对应的应用程序的entry包，并且以default模式进行编译。

file可见其实为Zip，用unzip解压：

其目录结构如下：

如需逆向该包的主要代码逻辑（如本题），我们需要关注其 ./ets/modules.abc（ArkTS源码的编译结果）和 ./libs目录（动态库）。目录中的其余文件如配置文件、资源文件等，不涉及代码逻辑的实现。

modules.abc逆向

目前modules.abc的反编译工具中比较好用的是abc-decompiler（https://github.com/ohos-decompiler/abc-decompiler）。由于其基于jadx开发，使用方法与jadx相似，减少了入门新工具的学习成本。

 使用abc-decompiler打开modules.abc后可见源代码结构如下：

分析过程中一般需要关注的是源代码中main包的pages目录，这里包含了该程序中的所有的页面，这里只有一个Index页面。

类编译后的入口函数为func_main_0，用于进行初始化。

由于flag一般需要输入框，直接找TextInput：

这里设置了TextInput的一些属性和事件，其中有一个onSubmit事件，键盘回车时会触发，所以去跟踪onSubmit找处理函数：

这个handleInput是我们上面初始化是赋值过的#~@0>#handleInput，继续跟踪：

可以看到是调用了libentry.so中的check函数来对输入进行检查，并根据检查结果判断对错，这里我们需要让check函数的返回值为“right”。

动态库逆向

在模块注册函数中找到entry函数：

进而在entry函数中找到前文中调用的check函数：

这两个函数中都有许多垃圾代码，形如：

这里我们需要让v149 == 0.0，即napi_get_value_string_utf8的结果为0（napi_ok），否则退出。于是通过排除这些垃圾代码可以将check函数整理成：

v180 = 2LL;memset(s, 0, sizeof(s));memset(input2uintArray, 0, sizeof(input2uintArray));napi_get_cb_info(a1, a2, &v180, s, 0LL);napi_typeof(a1, *(_QWORD *)s, v178);memset(input, 0, sizeof(input));value_string_utf8 = napi_get_value_string_utf8(a1, *(_QWORD *)s, input, 256LL, &v177);if (value_string_utf8) { OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input error"); napi_create_string_utf8(a1, "error", 5LL, &v179); return v179;}OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "Your input : %{public}s nlen:%{public}d", input, input_len);// 输入长度为32if ( input_len != 32 ) { OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input length error"); napi_create_string_utf8(a1, "error", 5LL, &v179); return v179;}// 将输入由32个char转为8个uintfor ( j = 0; j < 8; ++j ) { input2uintArray[j] = input[j]; LODWORD(v5) = input2uintArray[j]; OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input2uintArray[%{public}d] = %{public}x", (unsigned int)j, v5);}// 对输入的8个uint依次进行检查，array为已知数组（其中均为大数字符串）for ( m = 0; m < 8; ++m ) { if (sub_57B0(input2uintArray[m], array[(__int64)m])) { napi_create_string_utf8(a1, "error", 5LL, &v179); return v179; }}napi_create_string_utf8(a1, "right", 5LL, &v179);return v179;

由上可见sub_57B0函数为核心检查函数，所以继续分析sub_57B0函数：

__int64 sub_57B0(unsigned int input_uint, const char *array) { memset(rslt1, 0, 0x1388uLL); memset(rslt2, 0, 0x1388uLL); memset(rslt3, 0, 0x1388uLL); memset(rslt4, 0, 0x1388uLL); memset(rslt5, 0, 0x1388uLL); sub_62F0(input_uint, rslt0); sub_6D20(rslt0, rslt0, rslt1); sub_8270(rslt0, 2LL, rslt2); sub_9890(rslt1, rslt2, rslt3); sub_A8F0(rslt3, "3", rslt4); sub_C160(rslt4, rslt5); if (!strcmp(rslt5, array)) { return 0; } else { return 1; }}

因此我们只需要让输入的当前uint经过一系列函数处理后与array相同即可。

以下对处理函数进行逐个分析：

__int64 sub_62F0(unsigned int a1, _BYTE *a2) { if (!a1) { *a2 = 48; a2[1] = 0; return 0; } uint = a1; idx = 0; // 从低位开始逐位转为十进制大整数字符串 while (1) { if (!uint) return; _idx = idx++; a2[_idx] = uint % 0xA + 48; uint /= 0xAu; } a2[idx] = 0; return sub_CC10(a2);}__int64 sub_CC10(const char *a1) { v20 = strlen(a1); // 反转大整数字符串 for ( j = 0; j < v20 / 2; ++j ) { v17 = a1[j]; a1[j] = a1[v20 - 1 - j]; a1[v20 - 1 - j] = v17; } return 0;}unsigned __int64 sub_6D20(const char *a1, const char *a2, char *a3) { v109 = strlen(a1); v108 = strlen(a2); v107 = v108 + v109; memset(v124, 0, 0x4E20uLL); // 大整数乘法，a3 = a1 * a2 for ( j = v109 - 1; j >= 0; --j ) { for ( m = v108 - 1; m >= 0; --m ) { v102 = m + j + 1; v101 = v124[v102] + (a2[m] - 48) * (a1[j] - 48); v124[v102] = v101 % 10; v124[m + j] += v101 / 10; } } for ( n = 0; n < v107; ++n ) { // 忽略前导0 if (v124[n] != 0) break; } strcpy(a3, "0"); while ( n < v107 ) { src = v124[n] + 48; strncat(a3, &src, 1uLL); ++n; } return 0;}unsigned __int64 sub_8270(const char *a1, int a2, char *a3) { if (a2 > 9) { strcpy(a3, "0"); return 0; } memset(s, 0, sizeof(s)); strcpy(s, a1); sub_CC10(s); // 反转大整数字符串 // 从低位开始逐位与a2相乘 for ( j = 0; j < strlen(s); ++j ) { v108 = v111 + a2 * (s[j] - 48); v111 = v108 / 10; v126 = v108 % 10 + 48; strncat(a3, &v126, 1uLL); } v125 = v111 + 48; strncat(a3, &v125, 1uLL); sub_CC10(a3); // 反转大整数字符串a3 for ( k = 0; k < strlen(a3) - 1; ++k ) { // 忽略前导0 if ( a3[k] != 48 ) break; } v3 = strlen(a3); memmove(a3, &a3[k], v3 - k + 1); return 0;}unsigned __int64 sub_9890(const char *a1, const char *a2, char *a3) { memset(s, 0, sizeof(s)); memset(dest, 0, 0x1388uLL); strcpy(s, a1); strcpy(dest, a2); sub_CC10(s); // 反转大整数字符串a1 sub_CC10(dest); // 反转大整数字符串a2 v82 = strlen(s); v81 = strlen(dest); if ( v82 <= v81 ) // v75 = max(strlen(a1), strlen(a2)) v75 = v81; else v75 = v82; // 大整数加法，a3 = a1 + a2 for ( j = 0; j < v75; ++j ) { if ( j >= v82 ) v59 = 0; else v59 = s[j] - 48; if ( j >= v81 ) v58 = 0; else v58 = dest[j] - 48; v77 = v80 + v58 + v59; v80 = v77 / 10; v93 = v77 % 10 + 48; strncat(a3, &v93, 1uLL); } v92 = v80 + 48; strncat(a3, &v92, 1uLL); sub_CC10(a3); // 反转大整数字符串a3 for ( k = 0; k < strlen(a3) - 1; ++k ) { // 忽略前导0 if ( a3[k] != 48 ) break; } v3 = strlen(a3); memmove(a3, &a3[k], v3 - k + 1); return 0;}unsigned __int64 sub_A8F0(const char *a1, const char *a2, char *a3) { memset(s, 0, sizeof(s)); memset(dest, 0, 0x1388uLL); strcpy(s, a1); strcpy(dest, a2); sub_CC10(s); // 反转大整数字符串a1 sub_CC10(dest); // 反转大整数字符串a2 v120 = strlen(s); v119 = strlen(dest); v118 = 0; *a3 = 0; // 大整数减法，a3 = a1 - a2 for ( j = 0; j < v120; ++j ) { if ( j >= v119 ) v99 = 0; else v99 = dest[j] - 48; v115 = s[j] - 48 - v99 - v118; if (v115 < 0) { LOBYTE(v115) = v115 + 10; v118 = 1; } else { v118 = 0; } v132 = v115 + 48; strncat(a3, &v132, 1uLL); } while ( strlen(a3) > 1 ) { // 忽略前导0 if (a3[strlen(a3) - 1] != 48) { break; } a3[strlen(a3) - 1] = 0; } sub_CC10(a3); // 反转大整数字符串a3 return 0;}unsigned __int64 sub_C160(const char *a1, char *a2) { v60 = strlen(a1); v59 = 0; *a2 = 0; // 将大整数a1整除2并存入a2中 for ( j = 0; j < v60; ++j ) { v56 = a1[j] - 48 + 10 * v59; v59 = v56 % 2; src = v56 / 2 + 48; if (j == 0 && v56 / 2 == 0) continue; strncat(a2, &src, 1uLL); } if ( strlen(a2) == 0 ) strcpy(a2, "0"); return 0;}

由上述函数分析可以整理出以下函数功能：

sub_62F0：将uint转为大整数字符串；

sub_CC10：将大整数字符串反转；

sub_6D20：大整数乘法，a3 = a1 * a2；

sub_8270：大整数与整数相乘，a3 = a1 * a2（其中a2为int）；

sub_9890：大整数加法，a3 = a1 + a2；

sub_A8F0：大整数减法，a3 = a1 – a2；

sub_C160：将大整数a1整除2，并存入a2中，即a2 = a1 // 2。

从而整理出sub_57B0的检查逻辑：

// rslt0为input_uint的大整数字符串形式sub_62F0(input_uint, rslt0);// rslt1 = rslt0 * rslt0sub_6D20(rslt0, rslt0, rslt1);// rslt2 = rslt0 * 2sub_8270(rslt0, 2LL, rslt2);// rslt3 = rslt1 + rslt2sub_9890(rslt1, rslt2, rslt3);// rslt4 = rslt3 - 3sub_A8F0(rslt3, "3", rslt4);// rslt5 = rslt4 // 2sub_C160(rslt4, rslt5);

即 (input_uint ** 2 + input_uint * 2 – 3) // 2 == array。

用z3解方程即可，需要注意这里的除法为整除，如rslt4为奇数那么rslt5为其减一后的一半。

from z3 import *
array = [b'999272289930604998', b'1332475531266467542', b'1074388003071116830', b'1419324015697459326', b'978270870200633520', b'369789474534896558', b'344214162681978048', b'2213954953857181622']s = Solver()v = [Int(f"v{i}") for i in range(8)]for i in range(8):    get = ToInt(v[i]**2 + 2*v[i] - 3)    s.add(v[i] > 0)    s.add(Or(        And(get % 2 == 1, (get - 1) / 2 == int(array[i])), # 为奇数        And(get % 2 == 0,  get      / 2 == int(array[i]))  # 为偶数    ))flag = b''if s.check() == sat:    m = s.model()    for i in range(8):        flag += m[v[i]].as_long().to_bytes(4, 'little')print(flag)# b'SUCTF{Ma7h_WorldIs_S0_B3aut1ful}'

结语

简单鸿蒙应用的静态分析与安卓应用的分析方法类似，而结构和源语言的差异会导致在逆向分析时使用的方式有所不同。本题的难点主要在动态库中被额外添加的junk code会影响我们对函数的逆向分析以及细节的处理，但由于代码量不大所以可以手动反混淆并提取出关键的代码逻辑，逆向过程中还不需要动态分析。


```
v180 = 2LL;memset(s, 0, sizeof(s));memset(input2uintArray, 0, sizeof(input2uintArray));napi_get_cb_info(a1, a2, &v180, s, 0LL);napi_typeof(a1, *(_QWORD *)s, v178);memset(input, 0, sizeof(input));value_string_utf8 = napi_get_value_string_utf8(a1, *(_QWORD *)s, input, 256LL, &v177);if (value_string_utf8) { OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input error"); napi_create_string_utf8(a1, "error", 5LL, &v179); return v179;}OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "Your input : %{public}s nlen:%{public}d", input, input_len);// 输入长度为32if ( input_len != 32 ) { OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input length error"); napi_create_string_utf8(a1, "error", 5LL, &v179); return v179;}// 将输入由32个char转为8个uintfor ( j = 0; j < 8; ++j ) { input2uintArray[j] = input[j]; LODWORD(v5) = input2uintArray[j]; OH_LOG_Print(0LL, 4LL, 12800LL, "Native Log", "input2uintArray[%{public}d] = %{public}x", (unsigned int)j, v5);}// 对输入的8个uint依次进行检查，array为已知数组（其中均为大数字符串）for ( m = 0; m < 8; ++m ) { if (sub_57B0(input2uintArray[m], array[(__int64)m])) { napi_create_string_utf8(a1, "error", 5LL, &v179); return v179; }}napi_create_string_utf8(a1, "right", 5LL, &v179);return v179;
```



```
__int64 sub_57B0(unsigned int input_uint, const char *array) { memset(rslt1, 0, 0x1388uLL); memset(rslt2, 0, 0x1388uLL); memset(rslt3, 0, 0x1388uLL); memset(rslt4, 0, 0x1388uLL); memset(rslt5, 0, 0x1388uLL); sub_62F0(input_uint, rslt0); sub_6D20(rslt0, rslt0, rslt1); sub_8270(rslt0, 2LL, rslt2); sub_9890(rslt1, rslt2, rslt3); sub_A8F0(rslt3, "3", rslt4); sub_C160(rslt4, rslt5); if (!strcmp(rslt5, array)) { return 0; } else { return 1; }}
```



```
__int64 sub_62F0(unsigned int a1, _BYTE *a2) { if (!a1) { *a2 = 48; a2[1] = 0; return 0; } uint = a1; idx = 0; // 从低位开始逐位转为十进制大整数字符串 while (1) { if (!uint) return; _idx = idx++; a2[_idx] = uint % 0xA + 48; uint /= 0xAu; } a2[idx] = 0; return sub_CC10(a2);}__int64 sub_CC10(const char *a1) { v20 = strlen(a1); // 反转大整数字符串 for ( j = 0; j < v20 / 2; ++j ) { v17 = a1[j]; a1[j] = a1[v20 - 1 - j]; a1[v20 - 1 - j] = v17; } return 0;}unsigned __int64 sub_6D20(const char *a1, const char *a2, char *a3) { v109 = strlen(a1); v108 = strlen(a2); v107 = v108 + v109; memset(v124, 0, 0x4E20uLL); // 大整数乘法，a3 = a1 * a2 for ( j = v109 - 1; j >= 0; --j ) { for ( m = v108 - 1; m >= 0; --m ) { v102 = m + j + 1; v101 = v124[v102] + (a2[m] - 48) * (a1[j] - 48); v124[v102] = v101 % 10; v124[m + j] += v101 / 10; } } for ( n = 0; n < v107; ++n ) { // 忽略前导0 if (v124[n] != 0) break; } strcpy(a3, "0"); while ( n < v107 ) { src = v124[n] + 48; strncat(a3, &src, 1uLL); ++n; } return 0;}unsigned __int64 sub_8270(const char *a1, int a2, char *a3) { if (a2 > 9) { strcpy(a3, "0"); return 0; } memset(s, 0, sizeof(s)); strcpy(s, a1); sub_CC10(s); // 反转大整数字符串 // 从低位开始逐位与a2相乘 for ( j = 0; j < strlen(s); ++j ) { v108 = v111 + a2 * (s[j] - 48); v111 = v108 / 10; v126 = v108 % 10 + 48; strncat(a3, &v126, 1uLL); } v125 = v111 + 48; strncat(a3, &v125, 1uLL); sub_CC10(a3); // 反转大整数字符串a3 for ( k = 0; k < strlen(a3) - 1; ++k ) { // 忽略前导0 if ( a3[k] != 48 ) break; } v3 = strlen(a3); memmove(a3, &a3[k], v3 - k + 1); return 0;}unsigned __int64 sub_9890(const char *a1, const char *a2, char *a3) { memset(s, 0, sizeof(s)); memset(dest, 0, 0x1388uLL); strcpy(s, a1); strcpy(dest, a2); sub_CC10(s); // 反转大整数字符串a1 sub_CC10(dest); // 反转大整数字符串a2 v82 = strlen(s); v81 = strlen(dest); if ( v82 <= v81 ) // v75 = max(strlen(a1), strlen(a2)) v75 = v81; else v75 = v82; // 大整数加法，a3 = a1 + a2 for ( j = 0; j < v75; ++j ) { if ( j >= v82 ) v59 = 0; else v59 = s[j] - 48; if ( j >= v81 ) v58 = 0; else v58 = dest[j] - 48; v77 = v80 + v58 + v59; v80 = v77 / 10; v93 = v77 % 10 + 48; strncat(a3, &v93, 1uLL); } v92 = v80 + 48; strncat(a3, &v92, 1uLL); sub_CC10(a3); // 反转大整数字符串a3 for ( k = 0; k < strlen(a3) - 1; ++k ) { // 忽略前导0 if ( a3[k] != 48 ) break; } v3 = strlen(a3); memmove(a3, &a3[k], v3 - k + 1); return 0;}unsigned __int64 sub_A8F0(const char *a1, const char *a2, char *a3) { memset(s, 0, sizeof(s)); memset(dest, 0, 0x1388uLL); strcpy(s, a1); strcpy(dest, a2); sub_CC10(s); // 反转大整数字符串a1 sub_CC10(dest); // 反转大整数字符串a2 v120 = strlen(s); v119 = strlen(dest); v118 = 0; *a3 = 0; // 大整数减法，a3 = a1 - a2 for ( j = 0; j < v120; ++j ) { if ( j >= v119 ) v99 = 0; else v99 = dest[j] - 48; v115 = s[j] - 48 - v99 - v118; if (v115 < 0) { LOBYTE(v115) = v115 + 10; v118 = 1; } else { v118 = 0; } v132 = v115 + 48; strncat(a3, &v132, 1uLL); } while ( strlen(a3) > 1 ) { // 忽略前导0 if (a3[strlen(a3) - 1] != 48) { break; } a3[strlen(a3) - 1] = 0; } sub_CC10(a3); // 反转大整数字符串a3 return 0;}unsigned __int64 sub_C160(const char *a1, char *a2) { v60 = strlen(a1); v59 = 0; *a2 = 0; // 将大整数a1整除2并存入a2中 for ( j = 0; j < v60; ++j ) { v56 = a1[j] - 48 + 10 * v59; v59 = v56 % 2; src = v56 / 2 + 48; if (j == 0 && v56 / 2 == 0) continue; strncat(a2, &src, 1uLL); } if ( strlen(a2) == 0 ) strcpy(a2, "0"); return 0;}
```



```
// rslt0为input_uint的大整数字符串形式sub_62F0(input_uint, rslt0);// rslt1 = rslt0 * rslt0sub_6D20(rslt0, rslt0, rslt1);// rslt2 = rslt0 * 2sub_8270(rslt0, 2LL, rslt2);// rslt3 = rslt1 + rslt2sub_9890(rslt1, rslt2, rslt3);// rslt4 = rslt3 - 3sub_A8F0(rslt3, "3", rslt4);// rslt5 = rslt4 // 2sub_C160(rslt4, rslt5);
```



```
from z3 import *
array = [b'999272289930604998', b'1332475531266467542', b'1074388003071116830', b'1419324015697459326', b'978270870200633520', b'369789474534896558', b'344214162681978048', b'2213954953857181622']s = Solver()v = [Int(f"v{i}") for i in range(8)]for i in range(8):    get = ToInt(v[i]**2 + 2*v[i] - 3)    s.add(v[i] > 0)    s.add(Or(        And(get % 2 == 1, (get - 1) / 2 == int(array[i])), # 为奇数        And(get % 2 == 0,  get      / 2 == int(array[i]))  # 为偶数    ))flag = b''if s.check() == sat:    m = s.model()    for i in range(8):        flag += m[v[i]].as_long().to_bytes(4, 'little')print(flag)# b'SUCTF{Ma7h_WorldIs_S0_B3aut1ful}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736944042.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736944043.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736944046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736944046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736944048.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736944050.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736944051.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736944052.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736944053.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736944054.png)