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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676167307.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676167307.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/9-1676167307.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1676167308.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/8-1676167308.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1676167309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676167309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1676167309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/9-1676167310.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676167310.png)