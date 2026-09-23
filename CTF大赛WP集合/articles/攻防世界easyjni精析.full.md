---
title: 攻防世界 easyjni 精析
contest: 攻防世界 (xctf)
year: 2023
difficulty: medium
vuln_type:
- reverse
- crypto_oracle
tags:
- APK
- JNI
- native
- base64
- 自定义编码表
- swap
- 字符交换
- 看雪
- xianxiong
attack_chain:
- APK 反编译定位 JNI native 方法
- JADX/Ghidra 打开 .so 看 JNI_OnLoad 注册函数
- 识别自定义 base64 编码表 'i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN
- 用 str.maketrans 映射回标准 base64 字母表
- base64 解码得 flag 字符串
- 看 so 函数：先做 16 字节字符表置换 (s1[i] = t_str[i+16])
- 再做 32 字节相邻 swap 还原
key_payload: str1.translate(str.maketrans(string1, string2)) → base64.b64decode
one_liner: 自定义 base64 字母表 + JNI 字符串置换还原
lesson: native 层 base64 经常换字母表防识别；JNI_OnLoad 里 StringUTFChars 读入后做字符表 swap
quality: high
full_path: 攻防世界easyjni精析.full.md
meta_path: 攻防世界easyjni精析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 攻防世界 easyjni 精析。自定义 base64 字母表 + JNI 字符串置换还原。关键路径：APK 反编译定位 JNI native 方法 → JADX/Ghidra 打开 .so 看 JNI_OnLoad 注册函数 → 识别自定义 base64 编码表 'i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN...
category: reverse
subcategory: reverse
subcategories:
- reverse
- oracle
tools_used:
- Ghidra
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/97303.html
reasoning_chain:
- 题目是 Android APK + JNI native 层加密 → 触发点：JADX/Ghidra 打开 .so 看 JNI_OnLoad 注册函数
- 假设：native 层做了字符串置换 → 观察：自定义 base64 编码表 'i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN'
- 假设：用 str.maketrans(string1, string2) 把自定义表映射回标准表 → 动作：str1.translate(str.maketrans(string1, string2)) → base64.b64decode
- 观察：得到 flag 字符串
- 触发点：看 so 函数先做 16 字节字符表置换 (s1[i] = t_str[i+16]) → 假设：32 字节相邻 swap 还原
- 动作：写 Python 还原脚本 → 观察：得 flag
failed_attempts:
- 试图不解字符串表直接 base64 解 → 失败：自定义表解码乱码
- 试图只看 Java 层逻辑 → 失败：native 层才是真实算法
- 试图不解 so 函数还原 → 失败：字符串表置换必须在 native 层做
key_observations:
- native 层 base64 经常换字母表防识别
- JNI_OnLoad 里 StringUTFChars 读入后做字符表 swap
- 16 字节字符表置换 + 32 字节相邻 swap 是两层变换
- str.maketrans 是 Python 处理自定义编码表的标准工具
- Android JNI 题必须看 .so 而不能只看 Java 层
prerequisites:
- Android JNI 编程基础（Java + native）
- Ghidra/JADX 反编译工具
- base64 编码原理
- Python str.translate + maketrans
---
# 攻防世界easyjni精析

> 原文: https://www.ctfiot.com/97303.html
> ID: 97303

一

考察apk

0、待编码字符串按照3个一组分组

1、字符转ascii码值

2、ascii码值转换为8bit二进制表示

3、按照6bit一组重新组合

4、6bit数转10进制

5、查表

=LOOKUP(1,0/EXACT(改写后的编码表!B:B,A2),改写后的编码表!C:C)=LOOKUP(1,0/EXACT(Base64编码表!A:A,B2),Base64编码表!B:B)

import base64import stringstr1 = "QAoOQMPFks1BsB7cbM3TQsXg30i9g3=="string1 = 'i'+'5'+'j'+'L'+'W'+'7'+'S'+'0'+'G'+'X'+'6'+'u'+'f'+'1'+'c'+'v'+'3'+'n'+'y'+'4'+'q'+'8'+'e'+'s'+'2'+'Q'+'+'+'b'+'d'+'k'+'Y'+'g'+'K'+'O'+'I'+'T'+'/'+'t'+'A'+'x'+'U'+'r'+'F'+'l'+'V'+'P'+'z'+'h'+'m'+'o'+'w'+'9'+'B'+'H'+'C'+'M'+'D'+'p'+'E'+'a'+'J'+'R'+'Z'+'N' string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"print (str1)print (string1)print (string2)print (str1.translate(str.maketrans(string1,string2)))print (base64.b64decode(str1.translate(str.maketrans(string1,string2))))

二

考察so

do { v8 = &s1[i]; s1[i] = t_str[i + 16]; v9 = t_str[i++]; v8[16] = v9; } while ( i != 16 );

do { v12 = __OFSUB__(v10, 30); v11 = v10 - 30 < 0; v16 = s1[v10]; s1[v10] = s1[v10 + 1]; s1[v10 + 1] = v16; v10 += 2; } while ( v11 ^ v12 );

三

思考题

do { v12 = __OFSUB__(v10, 30); v11 = v10 - 30 < 0; v16 = s1[v10]; s1[v10] = s1[v10 + 1]; s1[v10 + 1] = v16; v10 += 2; } while ( v11 ^ v12 );

四

附件

#include <stdio.h> int main(){ int i=0; int j=0; char *v8; char v9; char s1[33]="s1:
abcdefghijklmnopqrstuvwxyz123"; char t_str[33]="t_str:
ABCDEFGHIJKLMNOPQRSTUVWXYZ"; do { v8 = &s1[i]; s1[i] = t_str[i + 16]; v9 = t_str[i++]; v8[16] = v9; } while ( i != 16 ); for(j=0;j<33;j++) printf("%c",t_str[j]); printf("n"); printf("n"); printf("n"); for(j=0;j<33;j++) printf("%c",s1[j]); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); i = 0; /* do { v12 = __OFSUB__(i, 30); v11 = (i - 30) < 0; v16 = s1[i]; s1[i] = s1[i + 1]; s1[i + 1] = v16; i += 2; } while ( v11 ^ v12 ); */ do { v9 = s1[i]; s1[i] = s1[i + 1]; s1[i + 1] = v9; i += 2; } while ( i != 32 ); for(j=0;j<33;j++) printf("%c",s1[j]); return 0; }

五一

心灵鸡汤

六

参考

七

鸣谢

看雪ID：xianxiong

https://bbs.kanxue.com/user-home-846161.htm

*本文由看雪论坛 xianxiong 原创，转载请注明来自看雪社区

# 往期推荐

1、地图浏览器-vip分析

2、车服务平台-ios版本分析

3、STL容器逆向与实战

4、RCTF2022-MyCarsShowSpeed 题目分析

5、MRCTF2022 stuuuuub 题解

6、CS-exe木马分析

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
考察apk
=LOOKUP(1,0/EXACT(改写后的编码表!B:B,A2),改写后的编码表!C:C)=LOOKUP(1,0/EXACT(Base64编码表!A:A,B2),Base64编码表!B:B)
import base64import stringstr1 = "QAoOQMPFks1BsB7cbM3TQsXg30i9g3=="string1 = 'i'+'5'+'j'+'L'+'W'+'7'+'S'+'0'+'G'+'X'+'6'+'u'+'f'+'1'+'c'+'v'+'3'+'n'+'y'+'4'+'q'+'8'+'e'+'s'+'2'+'Q'+'+'+'b'+'d'+'k'+'Y'+'g'+'K'+'O'+'I'+'T'+'/'+'t'+'A'+'x'+'U'+'r'+'F'+'l'+'V'+'P'+'z'+'h'+'m'+'o'+'w'+'9'+'B'+'H'+'C'+'M'+'D'+'p'+'E'+'a'+'J'+'R'+'Z'+'N' string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"print (str1)print (string1)print (string2)print (str1.translate(str.maketrans(string1,string2)))print (base64.b64decode(str1.translate(str.maketrans(string1,string2))))
二
考察so
do { v8 = &s1[i]; s1[i] = t_str[i + 16]; v9 = t_str[i++]; v8[16] = v9; } while ( i != 16 );
do { v12 = __OFSUB__(v10, 30); v11 = v10 - 30 < 0; v16 = s1[v10]; s1[v10] = s1[v10 + 1]; s1[v10 + 1] = v16; v10 += 2; } while ( v11 ^ v12 );
三
思考题
do { v12 = __OFSUB__(v10, 30); v11 = v10 - 30 < 0; v16 = s1[v10]; s1[v10] = s1[v10 + 1]; s1[v10 + 1] = v16; v10 += 2; } while ( v11 ^ v12 );
四
附件
    #include <stdio.h> int main(){ int i=0; int j=0; char *v8; char v9; char s1[33]="s1:
abcdefghijklmnopqrstuvwxyz123"; char t_str[33]="t_str:
ABCDEFGHIJKLMNOPQRSTUVWXYZ"; do { v8 = &s1[i]; s1[i] = t_str[i + 16]; v9 = t_str[i++]; v8[16] = v9; } while ( i != 16 ); for(j=0;j<33;j++) printf("%c",t_str[j]); printf("n"); printf("n"); printf("n"); for(j=0;j<33;j++) printf("%c",s1[j]); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); printf("n"); i = 0; /* do { v12 = __OFSUB__(i, 30); v11 = (i - 30) < 0; v16 = s1[i]; s1[i] = s1[i + 1]; s1[i + 1] = v16; i += 2; } while ( v11 ^ v12 ); */ do { v9 = s1[i]; s1[i] = s1[i + 1]; s1[i + 1] = v9; i += 2; } while ( i != 32 ); for(j=0;j<33;j++) printf("%c",s1[j]); return 0; }
五一
心灵鸡汤
六
参考
七
鸣谢
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