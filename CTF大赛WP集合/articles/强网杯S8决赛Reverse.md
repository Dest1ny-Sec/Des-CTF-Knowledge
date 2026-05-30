# 强网杯S8决赛Reverse

> 原文: https://www.ctfiot.com/220846.html
> ID: 220846

一

S1mpleVM

__int64 __fastcall vmrun(char *input, char *vmcode)
{
 //some defs for local variable
 v2 = 0LL;
 v3 = *vmcode - 16;
 v5 = v48;
 v6 = vmcode + 1;
 while ( 2 )
 {
 switch ( v3 )
 {
 case 0u:
 if ( v2 )
 {
 v9 = v2;
 v2 = (signed int *)*((_QWORD *)v2 + 1);
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = v2;
 v2 = (signed int *)*((_QWORD *)v2 + 1);
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
 }
 else
 {
 v7 = 0x80000000;
 v8 = 0x80000000;
 }
 v11 = (signed int *)j__malloc_base(0x10uLL);
 *v11 = v7 % v8;
 goto LABEL_53;
 case 1u:
 //...
LABEL_53:
 *((_QWORD *)v11 + 1) = v2;
 v2 = v11;
 }
 }
}

struct LinkEntry{
 signed val;
 LinkEntry * next;
}

case 0u:
if ( v2 )
{
 v9 = &v2->val;
 v2 = v2->next;
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = &v2->val;
 v2 = v2->next;
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
}
else
{
 v7 = 0x80000000;
 v8 = 0x80000000;
}
v11 = (LinkEntry *)j__malloc_base(0x10uLL);
v11->val = v7 % v8;
goto LABEL_53;

__int64 __fastcall vmrun(char *input, char *vmcode)
{
 LinkEntry *v2; // rdi
 unsigned int opcode; // eax
 unsigned int v5; // r14d
 char *PC; // rbp
 signed int v7; // esi
 signed int v8; // ebx
 signed int *v9; // rcx
 signed int *v10; // rcx
 LinkEntry *v11; // rcx
 int v12; // ebx
 LinkEntry *v13; // rax
 unsigned int *v14; // rcx
 unsigned int v15; // esi
 unsigned int v16; // ebx
 unsigned int *v17; // rcx
 unsigned int *v18; // rcx
 LinkEntry *v19; // rax
 unsigned int v20; // esi
 unsigned int v21; // ebx
 unsigned int *v22; // rcx
 unsigned int *v23; // rcx
 int v24; // eax
 int v25; // ebx
 LinkEntry *v26; // rax
 int v27; // esi
 int v28; // ebx
 signed int *v29; // rcx
 int *v30; // rcx
 LinkEntry *v31; // rax
 unsigned int v32; // esi
 unsigned int v33; // ebx
 unsigned int *v34; // rcx
 unsigned int *v35; // rcx
 LinkEntry *v36; // rax
 unsigned int v37; // ebx
 unsigned int v38; // esi
 unsigned int *v39; // rcx
 unsigned int *v40; // rcx
 LinkEntry *v41; // rax
 signed int v42; // esi
 signed int v43; // ebx
 signed int *v44; // rcx
 signed int *v45; // rcx
 int v46; // eax
 unsigned int v48; // [rsp+58h] [rbp+10h]

 v2 = 0LL;
 opcode = *vmcode - 16;
 v5 = v48;
 PC = vmcode + 1;
 while ( 2 )
 {
 switch ( opcode )
 {
 case 0u:
 if ( v2 )
 {
 v9 = &v2->val;
 v2 = v2->next;
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = &v2->val;
 v2 = v2->next;
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
 }
 else
 {
 v7 = 0x80000000;
 v8 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v11->val = v7 % v8;
 goto LABEL_53;
 case 1u:
 v12 = *PC;
 v13 = (LinkEntry *)j__malloc_base(0x10uLL);
 ++PC;
 v13->next = v2;
 v2 = v13;
 v13->val = v12;
 goto LABEL_54;
 case 2u:
 if ( v2 )
 {
 v14 = (unsigned int *)v2;
 v2 = v2->next;
 v5 = *v14;
 free(v14);
 }
 else
 {
 v5 = 0x80000000;
 }
 goto LABEL_54;
 case 3u:
 if ( v2 )
 {
 v17 = (unsigned int *)v2;
 v2 = v2->next;
 v15 = *v17;
 free(v17);
 if ( v2 )
 {
 v18 = (unsigned int *)v2;
 v2 = v2->next;
 v16 = *v18;
 free(v18);
 }
 else
 {
 v16 = 0x80000000;
 }
 }
 else
 {
 v15 = 0x80000000;
 v16 = 0x80000000;
 }
 v19 = (LinkEntry *)j__malloc_base(0x10uLL);
 v19->next = v2;
 v2 = v19;
 v19->val = v15 * v16;
 goto LABEL_54;
 case 4u:
 if ( v2 )
 {
 v22 = (unsigned int *)v2;
 v2 = v2->next;
 v20 = *v22;
 free(v22);
 if ( v2 )
 {
 v23 = (unsigned int *)v2;
 v2 = v2->next;
 v21 = *v23;
 free(v23);
 }
 else
 {
 v21 = 0x80000000;
 }
 }
 else
 {
 v20 = 0x80000000;
 v21 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v24 = v21 + v20;
 goto LABEL_52;
 case 5u:
 sub_1400011B0("%c", v5);
 goto LABEL_54;
 case 6u:
 v25 = *input;
 v26 = (LinkEntry *)j__malloc_base(0x10uLL);
 v26->next = v2;
 v2 = v26;
 v26->val = v25;
 goto LABEL_54;
 case 7u:
 if ( v2 )
 {
 v29 = &v2->val;
 v2 = v2->next;
 v27 = *v29;
 free(v29);
 if ( v2 )
 {
 v30 = &v2->val;
 v2 = v2->next;
 v28 = *v30;
 free(v30);
 }
 else
 {
 v28 = 0x80000000;
 }
 }
 else
 {
 LOBYTE(v27) = 0;
 v28 = 0x80000000;
 }
 v31 = (LinkEntry *)j__malloc_base(0x10uLL);
 v31->next = v2;
 v2 = v31;
 v31->val = (v28 >> v27) & 1;
 goto LABEL_54;
 case 8u:
 if ( v2 )
 {
 v34 = (unsigned int *)v2;
 v2 = v2->next;
 v32 = *v34;
 free(v34);
 if ( v2 )
 {
 v35 = (unsigned int *)v2;
 v2 = v2->next;
 v33 = *v35;
 free(v35);
 }
 else
 {
 v33 = 0x80000000;
 }
 }
 else
 {
 v32 = 0x80000000;
 v33 = 0x80000000;
 }
 v36 = (LinkEntry *)j__malloc_base(0x10uLL);
 v36->next = v2;
 v2 = v36;
 v36->val = v32 ^ v33;
 goto LABEL_54;
 case 9u:
 ++input;
 goto LABEL_54;
 case 0xAu:
 return v5;
 case 0xBu:
 if ( v2 )
 {
 v39 = (unsigned int *)v2;
 v2 = v2->next;
 v37 = *v39;
 free(v39);
 if ( v2 )
 {
 v40 = (unsigned int *)v2;
 v2 = v2->next;
 v38 = *v40;
 free(v40);
 }
 else
 {
 v38 = 0x80000000;
 }
 }
 else
 {
 v37 = 0x80000000;
 v38 = 0x80000000;
 }
 v41 = (LinkEntry *)j__malloc_base(0x10uLL);
 v41->next = v2;
 v2 = v41;
 v41->val = v37 - v38;
 goto LABEL_54;
 case 0xCu:
 if ( v2 )
 {
 v44 = &v2->val;
 v2 = v2->next;
 v42 = *v44;
 free(v44);
 if ( v2 )
 {
 v45 = &v2->val;
 v2 = v2->next;
 v43 = *v45;
 free(v45);
 }
 else
 {
 v43 = 0x80000000;
 }
 }
 else
 {
 v42 = 0x80000000;
 v43 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v24 = v42 / v43;
LABEL_52:
 v11->val = v24;
LABEL_53:
 v11->next = v2;
 v2 = v11;
LABEL_54:
 v46 = *PC++;
 opcode = v46 - 16;
 if ( opcode <= 0xC )
 continue;
 goto LABEL_57;
 default:
LABEL_57:
 sub_1400011B0("WTF are u doinggg...");
 exit(1);
 }
 }
}

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/fcntl.h>
#include<stack>
std::stack<int>s;
char buffer[0x10000];
int getstackval(){
 int val=0x80000000;
 if(s.size()){
 val=s.top();
 s.pop();
 }
 return val;
}
void pushstackval(int val){
 printf("push val %dn",val);
 s.push(val);
}
int main(){
 
 int fd=open("./quest",0);
 size_t ret=read(fd,buffer,0x10000);
 char *PC=buffer;
 int reg1,reg2,reg3;
 char input[]="flag{aaaaaaaaaaaaaaaaaaaaaaaaaa}";
 char *p=input;
 while(1){
 char opcode=*PC-0x10;
 char operand;
 PC++;
 
 switch (opcode) {
 case 0:
 reg2=getstackval();
 reg3=getstackval();
 pushstackval(reg2%reg3);
 printf("calc %d %% %d=%d",reg2,reg3,reg2%reg3);
 break;
 case 1:
 operand=*PC++;
 pushstackval(operand);
 break;
 case 2:
 reg1=getstackval();
 printf("pop %d to reg1n",reg1);
 break;
 case 3:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d*%d=%dn",reg2,reg3,reg2*reg3);
 pushstackval(reg2*reg3);
 break;
 case 4:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d+%d=%dn",reg2,reg3,reg2+reg3);
 pushstackval(reg2+reg3);
 break;
 case 5:
 printf("output a char %cn",reg1);
 break;
 case 6:
 printf("get %d inputn",p-input+1,*p);
 pushstackval(*p);
 break;
 case 7:
 reg3=getstackval();
 reg2=getstackval();
 printf("calc (%d>>%d)&1=%dn",reg2,reg3,(reg2>>reg3)&1);
 pushstackval((reg2>>reg3)&1);
 
 break;
 case 8:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d^%d=%dn",reg2,reg3,reg2^reg3);
 pushstackval(reg2^reg3);
 break;
 case 9:
 p++;
 break;
 case 10:
 printf("retval=%dn",reg1);
 return reg1;
 case 11:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d-%d=%dn",reg2,reg3,reg2-reg3);
 pushstackval(reg2-reg3);
 break;
 case 12:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d/%d=%fn",reg2,reg3,reg2/reg3);
 pushstackval(reg2/reg3);
 break;
 default:
 printf("invalid op");
 exit(0);
 break;
 } 
 }
}

get 1 input
push val 102
push val 0
calc (102>>0)&1=0
push val 0
push val 2
calc 2*0=0
push val 0
get 1 input
push val 102
push val 1
calc (102>>1)&1=1
push val 1
push val 3
calc 3*1=3
push val 3
get 1 input
push val 102
push val 2
calc (102>>2)&1=1
push val 1
push val 67
calc 67*1=67
push val 67
get 1 input
push val 102
push val 3
calc (102>>3)&1=0
push val 0
push val 37
calc 37*0=0
push val 0
get 1 input
push val 102
push val 4
calc (102>>4)&1=0
push val 0
push val 41
calc 41*0=0
push val 0
get 1 input
push val 102
push val 5
calc (102>>5)&1=1
push val 1
push val 11
calc 11*1=11
push val 11
get 1 input
push val 102
push val 6
calc (102>>6)&1=1
push val 1
push val 13
calc 13*1=13
push val 13
get 1 input
push val 102
push val 7
calc (102>>7)&1=0
push val 0
push val 89
calc 89*0=0
push val 0
calc 0+13=13
push val 13
calc 13+11=24
push val 24
calc 24+0=24
push val 24
calc 24+0=24
push val 24
calc 24+67=91
push val 91
calc 91+3=94
push val 94
calc 94+0=94
push val 94
push val 70
calc 70^94=24
push val 24
get 2 input
push val 108
push val 0
calc (108>>0)&1=0

2 3 67 37 41 11 13 89

calc 137+71=208
push val 208
calc 208+39=247
push val 247
calc 247+120=367
push val 367
calc 367+22=389
push val 389
calc 389+119=508
push val 508
calc 508+89=597
push val 597
calc 597+22=619
push val 619
calc 619+218=837
push val 837
calc 837+203=1040
push val 1040
calc 1040+125=1165
push val 1165
calc 1165+125=1290
push val 1290
calc 1290+5=1295
push val 1295
calc 1295+118=1413
push val 1413
calc 1413+30=1443
push val 1443
calc 1443+59=1502
push val 1502
calc 1502+89=1591
push val 1591
calc 1591+213=1804
push val 1804
calc 1804+114=1918
push val 1918
calc 1918+35=1953
push val 1953
calc 1953+18=1971
push val 1971
calc 1971+18=1989
push val 1989
calc 1989+121=2110
push val 2110
calc 2110+65=2175
push val 2175
calc 2175+32=2207
push val 2207
calc 2207+221=2428
push val 2428
calc 2428+253=2681
push val 2681
calc 2681+348=3029
push val 3029
calc 3029+130=3159
push val 3159
calc 3159+92=3251
push val 3251
calc 3251+140=3391
push val 3391
calc 3391+24=3415
push val 3415
pop 3415 to reg1
retval=3415

#include<stdio.h>
char v[]={
2,3,67,37,41,11,13,89,2,3,67,5,7,47,61,29,2,67,37,7,43,11,13,31,97,3,41,73,11,13,53,29,97,67,3,11,43,13,47,83,67,5,37,71,7,11,89,29,2,3,5,11,13,83,53,61,2,3,7,71,43,83,29,31,7,73,11,13,53,89,29,31,2,3,5,37,7,43,13,61,2,5,7,43,11,13,53,89,5,7,73,43,11,13,59,31,3,5,73,41,43,13,83,89,2,7,71,11,43,13,29,61,2,5,7,11,13,79,47,83,3,67,37,5,73,11,13,61,2,67,5,7,71,11,13,61,67,3,5,37,43,11,13,61,2,3,37,7,71,41,11,29,3,5,41,11,43,47,53,29,2,3,7,71,43,13,47,79,2,3,5,37,11,43,13,79,97,67,5,37,7,41,11,61,3,71,7,43,11,79,53,61,2,3,71,73,11,13,61,31,97,2,3,67,5,11,13,83,2,3,5,37,7,41,11,53,2,3,73,43,11,13,53,61,2,67,3,37,7,11,47,59,2,37,5,73,13,47,53,59,2,67,71,73,41,11,13,89,2,3,67,37,73,11,43,59,};
char target[]={70,56,70,77,74,90,87,82,60,67,86,95,64,94,85,66,33,69,64,98,67,71,94,93,90,32,65,82,68,65,93,96,};
int checkval(int i,int pos){
 int sum=0;
 for(int j=0;j<8;j++){
 sum+=((i>>j)&1)*v[j+pos*8];
 }
 return sum;
}
int main(){
 for(size_t i=0;i<sizeof(target);i++){
 for(int j=0x20;j<127;j++){
 if(target[i]==checkval(j,i)){
 putchar(j);
 break;
 }
 }
 }
}
//s1mpl3_VM_us3s_link3d_l1st_st4ck

二

UnsafeFile

#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
int main(){
 while(1){
 Sleep(1000);
 }
}

#include<stdio.h>

int main(){
 unsigned char key[]="xcdx8bx95xe3x1fx16xd9x21x6bx3cx3cx24xb2x6ex98xe7";
 for(int i=0;i<16;i++){
 unsigned char t=key[i]&0xf;
 key[i]>>=4;
 key[i]|=t<<4;
 key[i]^=0x5A;
 printf("%02x ",key[i]);
 }
}

看雪ID：xi@0ji233

https://bbs.kanxue.com/user-home-919002.htm

*本文为看雪论坛精华文章，由 xi@0ji233 原创，转载请注明来自看雪社区

# 往期推荐

1、Frida 逆向一个 APP

2、强网杯S8 Rust Pwn chat-with-me出题思路分享

3、浅析libc2.38版本及以前tcache安全机制演进过程与绕过手法

4、购物APP设备风控SDK-mtop简单分析

5、PWN入门：偷吃特权-SetUID

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
S1mpleVM
```



```
__int64 __fastcall vmrun(char *input, char *vmcode)
{
 //some defs for local variable
 v2 = 0LL;
 v3 = *vmcode - 16;
 v5 = v48;
 v6 = vmcode + 1;
 while ( 2 )
 {
 switch ( v3 )
 {
 case 0u:
 if ( v2 )
 {
 v9 = v2;
 v2 = (signed int *)*((_QWORD *)v2 + 1);
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = v2;
 v2 = (signed int *)*((_QWORD *)v2 + 1);
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
 }
 else
 {
 v7 = 0x80000000;
 v8 = 0x80000000;
 }
 v11 = (signed int *)j__malloc_base(0x10uLL);
 *v11 = v7 % v8;
 goto LABEL_53;
 case 1u:
 //...
LABEL_53:
 *((_QWORD *)v11 + 1) = v2;
 v2 = v11;
 }
 }
}
```



```
struct LinkEntry{
 signed val;
 LinkEntry * next;
}
```



```
case 0u:
if ( v2 )
{
 v9 = &v2->val;
 v2 = v2->next;
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = &v2->val;
 v2 = v2->next;
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
}
else
{
 v7 = 0x80000000;
 v8 = 0x80000000;
}
v11 = (LinkEntry *)j__malloc_base(0x10uLL);
v11->val = v7 % v8;
goto LABEL_53;
```



```
__int64 __fastcall vmrun(char *input, char *vmcode)
{
 LinkEntry *v2; // rdi
 unsigned int opcode; // eax
 unsigned int v5; // r14d
 char *PC; // rbp
 signed int v7; // esi
 signed int v8; // ebx
 signed int *v9; // rcx
 signed int *v10; // rcx
 LinkEntry *v11; // rcx
 int v12; // ebx
 LinkEntry *v13; // rax
 unsigned int *v14; // rcx
 unsigned int v15; // esi
 unsigned int v16; // ebx
 unsigned int *v17; // rcx
 unsigned int *v18; // rcx
 LinkEntry *v19; // rax
 unsigned int v20; // esi
 unsigned int v21; // ebx
 unsigned int *v22; // rcx
 unsigned int *v23; // rcx
 int v24; // eax
 int v25; // ebx
 LinkEntry *v26; // rax
 int v27; // esi
 int v28; // ebx
 signed int *v29; // rcx
 int *v30; // rcx
 LinkEntry *v31; // rax
 unsigned int v32; // esi
 unsigned int v33; // ebx
 unsigned int *v34; // rcx
 unsigned int *v35; // rcx
 LinkEntry *v36; // rax
 unsigned int v37; // ebx
 unsigned int v38; // esi
 unsigned int *v39; // rcx
 unsigned int *v40; // rcx
 LinkEntry *v41; // rax
 signed int v42; // esi
 signed int v43; // ebx
 signed int *v44; // rcx
 signed int *v45; // rcx
 int v46; // eax
 unsigned int v48; // [rsp+58h] [rbp+10h]

 v2 = 0LL;
 opcode = *vmcode - 16;
 v5 = v48;
 PC = vmcode + 1;
 while ( 2 )
 {
 switch ( opcode )
 {
 case 0u:
 if ( v2 )
 {
 v9 = &v2->val;
 v2 = v2->next;
 v7 = *v9;
 free(v9);
 if ( v2 )
 {
 v10 = &v2->val;
 v2 = v2->next;
 v8 = *v10;
 free(v10);
 }
 else
 {
 v8 = 0x80000000;
 }
 }
 else
 {
 v7 = 0x80000000;
 v8 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v11->val = v7 % v8;
 goto LABEL_53;
 case 1u:
 v12 = *PC;
 v13 = (LinkEntry *)j__malloc_base(0x10uLL);
 ++PC;
 v13->next = v2;
 v2 = v13;
 v13->val = v12;
 goto LABEL_54;
 case 2u:
 if ( v2 )
 {
 v14 = (unsigned int *)v2;
 v2 = v2->next;
 v5 = *v14;
 free(v14);
 }
 else
 {
 v5 = 0x80000000;
 }
 goto LABEL_54;
 case 3u:
 if ( v2 )
 {
 v17 = (unsigned int *)v2;
 v2 = v2->next;
 v15 = *v17;
 free(v17);
 if ( v2 )
 {
 v18 = (unsigned int *)v2;
 v2 = v2->next;
 v16 = *v18;
 free(v18);
 }
 else
 {
 v16 = 0x80000000;
 }
 }
 else
 {
 v15 = 0x80000000;
 v16 = 0x80000000;
 }
 v19 = (LinkEntry *)j__malloc_base(0x10uLL);
 v19->next = v2;
 v2 = v19;
 v19->val = v15 * v16;
 goto LABEL_54;
 case 4u:
 if ( v2 )
 {
 v22 = (unsigned int *)v2;
 v2 = v2->next;
 v20 = *v22;
 free(v22);
 if ( v2 )
 {
 v23 = (unsigned int *)v2;
 v2 = v2->next;
 v21 = *v23;
 free(v23);
 }
 else
 {
 v21 = 0x80000000;
 }
 }
 else
 {
 v20 = 0x80000000;
 v21 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v24 = v21 + v20;
 goto LABEL_52;
 case 5u:
 sub_1400011B0("%c", v5);
 goto LABEL_54;
 case 6u:
 v25 = *input;
 v26 = (LinkEntry *)j__malloc_base(0x10uLL);
 v26->next = v2;
 v2 = v26;
 v26->val = v25;
 goto LABEL_54;
 case 7u:
 if ( v2 )
 {
 v29 = &v2->val;
 v2 = v2->next;
 v27 = *v29;
 free(v29);
 if ( v2 )
 {
 v30 = &v2->val;
 v2 = v2->next;
 v28 = *v30;
 free(v30);
 }
 else
 {
 v28 = 0x80000000;
 }
 }
 else
 {
 LOBYTE(v27) = 0;
 v28 = 0x80000000;
 }
 v31 = (LinkEntry *)j__malloc_base(0x10uLL);
 v31->next = v2;
 v2 = v31;
 v31->val = (v28 >> v27) & 1;
 goto LABEL_54;
 case 8u:
 if ( v2 )
 {
 v34 = (unsigned int *)v2;
 v2 = v2->next;
 v32 = *v34;
 free(v34);
 if ( v2 )
 {
 v35 = (unsigned int *)v2;
 v2 = v2->next;
 v33 = *v35;
 free(v35);
 }
 else
 {
 v33 = 0x80000000;
 }
 }
 else
 {
 v32 = 0x80000000;
 v33 = 0x80000000;
 }
 v36 = (LinkEntry *)j__malloc_base(0x10uLL);
 v36->next = v2;
 v2 = v36;
 v36->val = v32 ^ v33;
 goto LABEL_54;
 case 9u:
 ++input;
 goto LABEL_54;
 case 0xAu:
 return v5;
 case 0xBu:
 if ( v2 )
 {
 v39 = (unsigned int *)v2;
 v2 = v2->next;
 v37 = *v39;
 free(v39);
 if ( v2 )
 {
 v40 = (unsigned int *)v2;
 v2 = v2->next;
 v38 = *v40;
 free(v40);
 }
 else
 {
 v38 = 0x80000000;
 }
 }
 else
 {
 v37 = 0x80000000;
 v38 = 0x80000000;
 }
 v41 = (LinkEntry *)j__malloc_base(0x10uLL);
 v41->next = v2;
 v2 = v41;
 v41->val = v37 - v38;
 goto LABEL_54;
 case 0xCu:
 if ( v2 )
 {
 v44 = &v2->val;
 v2 = v2->next;
 v42 = *v44;
 free(v44);
 if ( v2 )
 {
 v45 = &v2->val;
 v2 = v2->next;
 v43 = *v45;
 free(v45);
 }
 else
 {
 v43 = 0x80000000;
 }
 }
 else
 {
 v42 = 0x80000000;
 v43 = 0x80000000;
 }
 v11 = (LinkEntry *)j__malloc_base(0x10uLL);
 v24 = v42 / v43;
LABEL_52:
 v11->val = v24;
LABEL_53:
 v11->next = v2;
 v2 = v11;
LABEL_54:
 v46 = *PC++;
 opcode = v46 - 16;
 if ( opcode <= 0xC )
 continue;
 goto LABEL_57;
 default:
LABEL_57:
 sub_1400011B0("WTF are u doinggg...");
 exit(1);
 }
 }
}
```



```
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/fcntl.h>
#include<stack>
std::stack<int>s;
char buffer[0x10000];
int getstackval(){
 int val=0x80000000;
 if(s.size()){
 val=s.top();
 s.pop();
 }
 return val;
}
void pushstackval(int val){
 printf("push val %dn",val);
 s.push(val);
}
int main(){
 
 int fd=open("./quest",0);
 size_t ret=read(fd,buffer,0x10000);
 char *PC=buffer;
 int reg1,reg2,reg3;
 char input[]="flag{aaaaaaaaaaaaaaaaaaaaaaaaaa}";
 char *p=input;
 while(1){
 char opcode=*PC-0x10;
 char operand;
 PC++;
 
 switch (opcode) {
 case 0:
 reg2=getstackval();
 reg3=getstackval();
 pushstackval(reg2%reg3);
 printf("calc %d %% %d=%d",reg2,reg3,reg2%reg3);
 break;
 case 1:
 operand=*PC++;
 pushstackval(operand);
 break;
 case 2:
 reg1=getstackval();
 printf("pop %d to reg1n",reg1);
 break;
 case 3:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d*%d=%dn",reg2,reg3,reg2*reg3);
 pushstackval(reg2*reg3);
 break;
 case 4:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d+%d=%dn",reg2,reg3,reg2+reg3);
 pushstackval(reg2+reg3);
 break;
 case 5:
 printf("output a char %cn",reg1);
 break;
 case 6:
 printf("get %d inputn",p-input+1,*p);
 pushstackval(*p);
 break;
 case 7:
 reg3=getstackval();
 reg2=getstackval();
 printf("calc (%d>>%d)&1=%dn",reg2,reg3,(reg2>>reg3)&1);
 pushstackval((reg2>>reg3)&1);
 
 break;
 case 8:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d^%d=%dn",reg2,reg3,reg2^reg3);
 pushstackval(reg2^reg3);
 break;
 case 9:
 p++;
 break;
 case 10:
 printf("retval=%dn",reg1);
 return reg1;
 case 11:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d-%d=%dn",reg2,reg3,reg2-reg3);
 pushstackval(reg2-reg3);
 break;
 case 12:
 reg2=getstackval();
 reg3=getstackval();
 printf("calc %d/%d=%fn",reg2,reg3,reg2/reg3);
 pushstackval(reg2/reg3);
 break;
 default:
 printf("invalid op");
 exit(0);
 break;
 } 
 }
}
```



```
get 1 input
push val 102
push val 0
calc (102>>0)&1=0
push val 0
push val 2
calc 2*0=0
push val 0
get 1 input
push val 102
push val 1
calc (102>>1)&1=1
push val 1
push val 3
calc 3*1=3
push val 3
get 1 input
push val 102
push val 2
calc (102>>2)&1=1
push val 1
push val 67
calc 67*1=67
push val 67
get 1 input
push val 102
push val 3
calc (102>>3)&1=0
push val 0
push val 37
calc 37*0=0
push val 0
get 1 input
push val 102
push val 4
calc (102>>4)&1=0
push val 0
push val 41
calc 41*0=0
push val 0
get 1 input
push val 102
push val 5
calc (102>>5)&1=1
push val 1
push val 11
calc 11*1=11
push val 11
get 1 input
push val 102
push val 6
calc (102>>6)&1=1
push val 1
push val 13
calc 13*1=13
push val 13
get 1 input
push val 102
push val 7
calc (102>>7)&1=0
push val 0
push val 89
calc 89*0=0
push val 0
calc 0+13=13
push val 13
calc 13+11=24
push val 24
calc 24+0=24
push val 24
calc 24+0=24
push val 24
calc 24+67=91
push val 91
calc 91+3=94
push val 94
calc 94+0=94
push val 94
push val 70
calc 70^94=24
push val 24
get 2 input
push val 108
push val 0
calc (108>>0)&1=0
```



```
2 3 67 37 41 11 13 89
```



```
calc 137+71=208
push val 208
calc 208+39=247
push val 247
calc 247+120=367
push val 367
calc 367+22=389
push val 389
calc 389+119=508
push val 508
calc 508+89=597
push val 597
calc 597+22=619
push val 619
calc 619+218=837
push val 837
calc 837+203=1040
push val 1040
calc 1040+125=1165
push val 1165
calc 1165+125=1290
push val 1290
calc 1290+5=1295
push val 1295
calc 1295+118=1413
push val 1413
calc 1413+30=1443
push val 1443
calc 1443+59=1502
push val 1502
calc 1502+89=1591
push val 1591
calc 1591+213=1804
push val 1804
calc 1804+114=1918
push val 1918
calc 1918+35=1953
push val 1953
calc 1953+18=1971
push val 1971
calc 1971+18=1989
push val 1989
calc 1989+121=2110
push val 2110
calc 2110+65=2175
push val 2175
calc 2175+32=2207
push val 2207
calc 2207+221=2428
push val 2428
calc 2428+253=2681
push val 2681
calc 2681+348=3029
push val 3029
calc 3029+130=3159
push val 3159
calc 3159+92=3251
push val 3251
calc 3251+140=3391
push val 3391
calc 3391+24=3415
push val 3415
pop 3415 to reg1
retval=3415
```



```
#include<stdio.h>
char v[]={
2,3,67,37,41,11,13,89,2,3,67,5,7,47,61,29,2,67,37,7,43,11,13,31,97,3,41,73,11,13,53,29,97,67,3,11,43,13,47,83,67,5,37,71,7,11,89,29,2,3,5,11,13,83,53,61,2,3,7,71,43,83,29,31,7,73,11,13,53,89,29,31,2,3,5,37,7,43,13,61,2,5,7,43,11,13,53,89,5,7,73,43,11,13,59,31,3,5,73,41,43,13,83,89,2,7,71,11,43,13,29,61,2,5,7,11,13,79,47,83,3,67,37,5,73,11,13,61,2,67,5,7,71,11,13,61,67,3,5,37,43,11,13,61,2,3,37,7,71,41,11,29,3,5,41,11,43,47,53,29,2,3,7,71,43,13,47,79,2,3,5,37,11,43,13,79,97,67,5,37,7,41,11,61,3,71,7,43,11,79,53,61,2,3,71,73,11,13,61,31,97,2,3,67,5,11,13,83,2,3,5,37,7,41,11,53,2,3,73,43,11,13,53,61,2,67,3,37,7,11,47,59,2,37,5,73,13,47,53,59,2,67,71,73,41,11,13,89,2,3,67,37,73,11,43,59,};
char target[]={70,56,70,77,74,90,87,82,60,67,86,95,64,94,85,66,33,69,64,98,67,71,94,93,90,32,65,82,68,65,93,96,};
int checkval(int i,int pos){
 int sum=0;
 for(int j=0;j<8;j++){
 sum+=((i>>j)&1)*v[j+pos*8];
 }
 return sum;
}
int main(){
 for(size_t i=0;i<sizeof(target);i++){
 for(int j=0x20;j<127;j++){
 if(target[i]==checkval(j,i)){
 putchar(j);
 break;
 }
 }
 }
}
//s1mpl3_VM_us3s_link3d_l1st_st4ck
```



```
二
UnsafeFile
```



```
#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
int main(){
 while(1){
 Sleep(1000);
 }
}
```



```
#include<stdio.h>

int main(){
 unsigned char key[]="xcdx8bx95xe3x1fx16xd9x21x6bx3cx3cx24xb2x6ex98xe7";
 for(int i=0;i<16;i++){
 unsigned char t=key[i]&0xf;
 key[i]>>=4;
 key[i]|=t<<4;
 key[i]^=0x5A;
 printf("%02x ",key[i]);
 }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734874299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1734874300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1734874301.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1734874301.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1734874303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1734874304.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734874305.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1734874305.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734874306.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1734874307.png)