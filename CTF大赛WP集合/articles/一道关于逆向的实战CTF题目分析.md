# 一道关于逆向的实战CTF题目分析

> 原文: https://www.ctfiot.com/193276.html
> ID: 193276


```
push ebx
.....
pop ebx
```



```
int __cdecl sub_401040(char a1, int a2)
{
  return ((a2 ^ a1) << 8) - a2;
}
```



```
int __cdecl sub_401080(char a1, int a2)
{
  
  return a2 ^ (a1 << 8);
}
```



```
left
xor
xor
left
xor
left
left
xor
left
left
xor
xor
xor
left
left
left
xor
xor
xor
left
xor
xor
left
xor
left
left
left
left
xor
xor
xor
left
```



```
int temp[32] = { 1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1 };
```



```
dword_402120 数组
unsignedint dword_402120[32]={
0x00004408,0x000068D8,0x00007AD8,0x00004308,0x00007BD8,0x00004608,0x00007B08,0x000070D8,
0x00003308,0x00007308,0x000076D8,0x00005CD8,0x000076D8,0x00006608,0x00006908,0x00006E08,
0x00004BD8,0x000076D8,0x00003FD8,0x00006F08,0x00005ED8,0x000076D8,0x00007408,0x000046D8,
0x00005F08,0x00006308,0x00003408,0x00007408,0x000076D8,0x000044D8,0x00004CD8,0x00007D08
};
```



```
#include <stdio.h>

void left(unsigned int a1, unsigned int a2) {
//  (a1>>8)^a2
printf("%c",((a1 ^ a2)>>8));
}
void xors(unsigned int a1, unsigned int a2) {
//(((a1+a2)>>8)^a2)
printf("%c",(((a1 + a2)>>8)^ a2));
}
int main()
{
unsignedint dword_402120[32]={
0x00004408,0x000068D8,0x00007AD8,0x00004308,0x00007BD8,0x00004608,0x00007B08,0x000070D8,
0x00003308,0x00007308,0x000076D8,0x00005CD8,0x000076D8,0x00006608,0x00006908,0x00006E08,
0x00004BD8,0x000076D8,0x00003FD8,0x00006F08,0x00005ED8,0x000076D8,0x00007408,0x000046D8,
0x00005F08,0x00006308,0x00003408,0x00007408,0x000076D8,0x000044D8,0x00004CD8,0x00007D08
};
int temp[32]={1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1};
for(size_t i =0; i <32; i++)
{
if(temp[i]){
//left
left(dword_402120[i],8);
}
else{
//xor
xors(dword_402120[i],40);

}
}

}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1720861753.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1720861757.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1720861757.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1720861758.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1720861758.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1720861759.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1720861759.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1720861759.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1720861760.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1720861760.jpeg)