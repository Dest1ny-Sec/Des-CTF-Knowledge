# 2025解题领红包之七 Windows高级Writeup

> 原文: https://www.ctfiot.com/227560.html
> ID: 227560

作者论坛账号：Command （排行榜第五名同学）

成果(虽然无法提交):

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
int __fastcall main(int argc, const char **argv, const char **envp)
{
  return ((__int64 (__fastcall *)(int, const char **, const char **))off_140026AD8)(argc, argv, envp);
}
```



```
复制代码 隐藏代码
mov     eax, 0FFFFFFFFh
retn
```



```
复制代码 隐藏代码
__int64 sub_140001190()
{
  __int64 result; // rax
  __int64 (__fastcall *v1)(); // rcx

  result = sub_140001C50(0LL, 0LL);
  v1 = off_140026AD8;
  if ( !result )
    v1 = sub_1400017A0;
  // ......底部省略一堆+16
  return result;
}
```



```
复制代码 隐藏代码
__int64 sub_1400017A0()
{
  __int64 a; // r12
  __int64 Gx; // r14
  __int64 Gy; // r15
  int v4; // r13d
  int FlagLength; // ecx
  _BYTE *v6; // rax
  __int64 v7; // rsi
  char *Flag_1; // rdi
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rdx
  __int64 v12; // rdi
  __int64 v13; // rsi
  __int64 p; // r13
  __int64 v15; // rbx
  __int64 v16; // r8
  __int64 de_p; // r14
  __int64 *v18; // rbx
  __int64 de_a; // r15
  __int64 v20; // r12
  unsigned __int64 x1; // rcx
  __int64 y1; // rax
  __int64 v23; // rbx
  int v24; // eax
  const char *v25; // rcx
  __int64 d; // [rsp+40h] [rbp-C0h]
  __int64 res[2]; // [rsp+48h] [rbp-B8h] BYREF
  __int64 result[2]; // [rsp+58h] [rbp-A8h] BYREF
  char Format[4]; // [rsp+68h] [rbp-98h] BYREF
  char a1[4]; // [rsp+6Ch] [rbp-94h] BYREF
  char v31[4]; // [rsp+70h] [rbp-90h] BYREF
  char v32[4]; // [rsp+74h] [rbp-8Ch] BYREF
  unsigned __int64 UID; // [rsp+78h] [rbp-88h] BYREF
  __int64 IntArray[18]; // [rsp+80h] [rbp-80h] BYREF
  char Str1[32]; // [rsp+110h] [rbp+10h] BYREF
  char Str2[32]; // [rsp+130h] [rbp+30h] BYREF
  _OWORD FlagInput[8]; // [rsp+150h] [rbp+50h] BYREF

  a = ::a;
  Gx = ::Gx;
  Gy = ::Gy;
  d = ::d;
  res[0] = ::p; 
  // 上述值在sub_140001000中被sub_140001520初始化; a, d与时间有关
  printf_0_0(::Format);
  printf_0_0(InputYourUID);
  scanf_s_0(::Format, &UID);
  if ( UID - 1 > 0x5F5E0FE )
  {
    printf_0_0(&Error);
    exit(-1);
  }
  UID ^= 60 * (time(0LL) / 60) / 10;
  sprintf_s<32>((char (*)[32])Str2, ::Format, abs64(UID * UID)); // UID与时间取整之后除以10得到的值进行异或然后平方
  Str2[16] = 0;
  memset(FlagInput, 0, sizeof(FlagInput));
  printf_0_0(InputYourKey);
  if ( scanf_s_0(asc_140026AC4, FlagInput, 128LL) )
  {
    v4 = 0;
    FlagLength = 0;
    v6 = FlagInput;
    do
    {
      ++FlagLength;
      ++v6;
    }
    while ( *v6 );
    if ( FlagLength == 108 * (FlagLength / 108) ) // 判断长度是否为108
    {
LABEL_10:
      v7 = 0LL;
      Flag_1 = (char *)FlagInput + 1;
      a1[2] = 0;
      v31[2] = 0;
      v32[2] = 0;
      do
      {
        a1[0] = *(Flag_1 - 1);
        a1[1] = *Flag_1;
        v31[0] = Flag_1[1];
        v31[1] = Flag_1[2];
        v32[0] = Flag_1[3];
        v32[1] = Flag_1[4];
        v9 = 100 * ParseInt(a1);
        v10 = 100 * (v9 + ParseInt(v31));
        Flag_1 += 6;
        IntArray[v7++] = v10 + ParseInt(v32);
      }
      while ( v7 < 18 );                        // 将输入的Key每六个字符一组, 解析数值, 变成一个长度为18的数组(IntArray)
                                                // (ParseInt是10进制, 解析时遇到非数字停止)
      v11 = d;
      v12 = Gx;
      v13 = Gy;
      if ( d == 1 ) // d will never be 1
      {
        v16 = 0LL;
      }
      else
      {
        p = res[0];
        v15 = d - 1;
        result[0] = d - 1;
        do
        {
          point_add(res, v12, v13, Gx, Gy, a, p);// 椭圆曲线加密(ECC), 问deepseek才知道... 加密的是v12, v13 (初始值为Gx, Gy)
          v12 = res[1];
          v13 = res[0];
          --v15;
        }
        while ( v15 );
        v11 = d;
        v4 = 0;
        v16 = result[0];
      }
      de_p = IntArray[17];                      // 此处从数组中下标为16与17的地方读出a与p, 我们需要控制这两个值与上方加密时的a与p相等
      v18 = IntArray;
      de_a = IntArray[16];
      v20 = 0LL;
      res[0] = (__int64)IntArray;
      Str1[0] = 0;
      *(_DWORD *)Format = 25381; // %c
      do
      {
        x1 = v12;                               // 解密后为Gx
        y1 = v13;                               // 解密后为Gy
        if ( v11 != 1 )
        {
          v23 = v16;
          do
          {
            point_add(result, x1, y1, v12, v13, de_a, de_p);// 根据我们传进来的a与p解密刚才加密的Gx, Gy
            x1 = result[1];
            y1 = result[0];
            --v23;
          }
          while ( v23 );
          v18 = (__int64 *)res[0];
        }
        sprintf_s_0_1(&Str1[v4], 2uLL, Format, (unsigned int)(char)((*v18 + -10 * y1 - v20) / x1));// 从数组中开始读数, 向Str1中追加经过处理后的字符
        v11 = d;
        ++v18;
        ++v4;
        res[0] = (__int64)v18;
        v20 += 10202LL;
        v16 = d - 1;
      }
      while ( v20 < 163232 );                   // 共循环16次 (步长10202)
      Str1[16] = 0;
      v24 = strncmp(Str1, Str2, 0x10uLL);       // 比较是否不一致 (注意, 是不一致)
      v25 = Correct;
      if ( v24 )
        v25 = &Error;
      printf_0_0(v25);
      return 0LL;
    }
  }
  // 几个else省略
}
```



```
复制代码 隐藏代码
a = ::a;
Gx = ::Gx;
Gy = ::Gy;
d = ::d;
res[0] = ::p;
```



```
复制代码 隐藏代码
; 这是上面那段代码对应的汇编
mov     r12, cs:a
mov     r14, cs:Gx
mov     r15, cs:Gy
mov     [rsp+200h+d], rax
mov     rax, cs:p
mov     [rsp+200h+res], rax  ; 我选择在这里Hook, 获取寄存器值, 此时rax为p, r12为a, r14为Gx, r15为Gy, 完美!
```



```
复制代码 隐藏代码
import idaapi
import idc
import time

# s是最后需要在解密时得到的字符串
def build_str(s: str, Gx: int, Gy: int) -> str:
    res = ''
    for i, v20 in zip(s, range(0, 163232, 10202)): # 步长10202模拟代码中v20 += 10202LL
        res += str(ord(i) * Gx + v20 + 10 * Gy).zfill(6) # 补齐6位
    return res

class MyDbgHook(idaapi.DBG_Hooks):
    def dbg_bpt(self, tid, ea):
        if ea == 0x1400017F8:
            UID = 1354181  # 此处写UID
            UID ^= int(60 * (int(time.time()) // 60 / 10))
            # r14: Gx, r15: Gy, r12: a, rax: p
            print(build_str(str(UID * UID)[:-1] if len(str(UID * UID)) == 17 else str(UID * UID), idc.get_reg_value("r14"), idc.get_reg_value("r15")) + str(idc.get_reg_value("r12")).zfill(6) + str(idc.get_reg_value("rax")).zfill(6))
        return 0

hook = MyDbgHook()
hook.hook()
idc.add_bpt(0x1400017F8)  # 刚才那行汇编的地址
```



```
复制代码 隐藏代码
de_p = IntArray[17];                      // 此处从数组中下标为16与17的地方读出a与p
v18 = IntArray;
de_a = IntArray[16];
v20 = 0LL;
res[0] = (__int64)IntArray;
Str1[0] = 0;
*(_DWORD *)Format = 25381; // %c
do
{
  x1 = v12;                               // 解密后甭管是啥, 总之10s内, 输入相同a, p的话这个值不会变 (rcx)
  y1 = v13;                               // 解密后甭管是啥, 总之10s内, 输入相同a, p的话这个值不会变 (rax)
  if ( v11 != 1 )
  {
    v23 = v16;
    do
    {
            point_add(result, x1, y1, v12, v13, de_a, de_p); // 根据我们传进来的a与p解密刚才加密的Gx, Gy; 解出来的对不对? 不关我事
            x1 = result[1];
            y1 = result[0];
            --v23;
    }
    while ( v23 );
    v18 = (__int64 *)res[0];
  }
  // 虽然解出的x1, y1和题中Gx, Gy不一样, 但是在10s内依旧是个定值
  sprintf_s_0_1(&Str1[v4], 2uLL, Format, (unsigned int)(char)((*v18 + -10 * y1 - v20) / x1)); // 从数组中开始读数, 向Str1中追加经过处理后的字符; 我当时选择在这里进行Hook
}
```



```
复制代码 隐藏代码
imul    rax, -0Ah  ; 我选择hook这一条指令, 获取寄存器值
xor     edx, edx
lea     r8, [rsp+200h+Format] ; Format
sub     rax, r12
add     rax, [rbx]
div     rcx
; ......call在底下
```



```
复制代码 隐藏代码
import idaapi
import idc
import time

def build_str(s: str, v21: int, v22: int) -> str:
    res = ''
    for i, v20 in zip(s, range(0, 163232, 10202)):
        res += str(ord(i) * v21 + v20 + 10 * v22).zfill(6)
    return res

class MyDbgHook(idaapi.DBG_Hooks):
    def dbg_bpt(self, tid, ea):
        if ea == 0x140001B37:
            UID = 1354181
            print(int(time.time()))
            UID ^= int(60 * (int(time.time()) // 60 / 10))
            print(str(UID * UID))
            # rcx: x1, rax: y1  最后加上的后12个字符可以是其他的, 但是要求必须与你在程序中输入的Key一致
            print(build_str(str(UID * UID)[:-1], idc.get_reg_value("rcx"), idc.get_reg_value("rax")) + 'aaaa11aaaa11')
        return 0

hook = MyDbgHook()
hook.hook()
idc.add_bpt(0x140001B37)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/7-1739711042.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/7-1739711042.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1739711043.webp)