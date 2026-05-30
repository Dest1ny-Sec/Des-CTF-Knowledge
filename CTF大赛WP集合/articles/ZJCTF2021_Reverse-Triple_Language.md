# ZJCTF2021 Reverse-Triple Language

> 原文: https://www.ctfiot.com/36904.html
> ID: 36904

比赛的时候由于各种原因没有做出来，由于这道题需要unicorn的知识，对我本身而言是一个很好的学习机会，所以赛后进行了复现。为了写代码方便，本文使用python调用unicorn。

拿到题目，发现附近中存在unicorn.dll，猜测这个程序用到了unicorn的一些函数。

先查壳：

无壳，直接拖入IDA找到main函数分析：

初步分析，该程序需要输入两次，分别对应两个验证函数sub_7FF634B112B0和sub_7FF634B11A90，先看看第一个验证函数干了啥：

首先进行规定输入字符串的长度为22，然后有几个等式，这几个等式中的数据可以看出是跟我们输入数据的后16位有关，最终v11的结果要等于0x3EBB0EFAF301FC，猜测后续要进行解方程求解。往下看：

下面就使用了unicorn的函数，uc_open就是c调用unicorn时初始化unicorn的环境，然后第一个参数就是具体环境，第二个参数为具体的模式，我们查一下3和4具体代表啥：

说明初始化的是mips环境，且是x86模式。继续往下看：

从uc_mem_write可以看出mips的代码是从unk_7FF634B13340中提取出来的，大小为272。然后0x11000，0x12000，0x13000地址处填入的应该是mips代码中所需要的数据。其中byte_7FF634B15656和byte_7FF634B1565E是我们所输入的数据中的后16位。

这里有个uc_hook_add的函数，这个是unicorn的hook机制，第三个参数为4，代表unicorn每执行一次模拟的代码，就会触发一次hook机制，第四个参数是回调函数。接下来的操作就是初始化一些寄存器环境，然后进行模拟代码的执行，最后执行完，读取各个寄存器的值，进行验证。sub_7FF634B11000为回调函数，我们跟进去看下：

__int64 __fastcall sub_7FF634B11000(__int64 a1, __int64 a2){ __int64 result; // rax int v5; // [rsp+20h] [rbp-28h] BYREF int v6; // [rsp+24h] [rbp-24h] BYREF int v7; // [rsp+28h] [rbp-20h] BYREF int v8; // [rsp+2Ch] [rbp-1Ch] BYREF int v9[6]; // [rsp+30h] [rbp-18h] BYREF int v10; // [rsp+58h] [rbp+10h] BYREF uc_reg_read(a1, 11i64, &v10); uc_reg_read(a1, 12i64, &v5); uc_reg_read(a1, 13i64, &v6); uc_reg_read(a1, 14i64, &v7); uc_reg_read(a1, 15i64, &v8); result = uc_reg_read(a1, 16i64, v9); switch ( a2 ) // a2是地址 { case 0x10010i64: result = uc_reg_read(a1, 11i64, &v10); if ( v10 != 0x2F2E ) { printf("You died before you killed anyone.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10020i64: result = uc_reg_read(a1, 12i64, &v5); if ( v5 != 0x282A ) { printf("You died when you killed only one.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10030i64: result = uc_reg_read(a1, 13i64, &v6); if ( v6 != 0x2C42 ) { printf("Nice! Double kill, but died.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10040i64: result = uc_reg_read(a1, 14i64, &v7); if ( v7 != 0x2A8A ) { printf("Awesome! Triple Kill, but interrupted.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10050i64: result = uc_reg_read(a1, 15i64, &v8); if ( v8 != 0x13E0 ) { printf("Unimaginable! Quadra Kill, but emm...You know what I want to say.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10060i64: result = uc_reg_read(a1, 16i64, v9); if ( v9[0] != 0x36D4 ) { printf("Incredible! Penta Kill, but frankly, you still died.n"); uc_emu_stop(a1); exit(-1); } return result; default: return result; } return result;}

暂时不清楚是用来干啥的。由于不知道mips的具体代码是啥，所以我们先得拿到mips的代码，将mips的二进制码从unk_7FF634B13340提取出来。直接放入ida：

看着难受，而且不能F5看算法，索性我们自己写一个unicorn调试一下这个代码：

from unicorn import *from unicorn.x86_const import *from unicorn.arm_const import *from unicorn.mips_const import *from capstone import *with open('mips', 'rb') as file: #读代码段 MIPS_CODE = file.read() # 读取代码
class UnidbgMips: def __init__(self): # x32程序 mu = Uc(UC_ARCH_MIPS, UC_MODE_32) mu.mem_map(0x10000, 0x200000) mu.mem_write(0x10000,MIPS_CODE) mu.mem_write(0x11000,b"zjgcjyx00") mu.mem_write(0x12000,b"xFCx01xF3xFAx0ExBBx3Ex00") #输入假的值 mu.mem_write(0x13000,b"x00x00x00x00x00x00x00x00") mu.reg_write(UC_MIPS_REG_T1, 0x30)#输入假的值 mu.reg_write(UC_MIPS_REG_T2, 0x31) mu.reg_write(UC_MIPS_REG_T3, 0x32) mu.reg_write(UC_MIPS_REG_T4, 0x33) mu.reg_write(UC_MIPS_REG_T5, 0x34) mu.reg_write(UC_MIPS_REG_T6, 0x35) mu.hook_add(UC_HOOK_CODE, self.hook_code) self.mu=mu # 反汇编引擎 self.md = Cs(CS_ARCH_MIPS, CS_MODE_32) def hook_code(self, mu, address, size, data): disasm = self.md.disasm(mu.mem_read(address, size), address) for i in disasm: print("0x%x:t%st%s" %(i.address,i.mnemonic,i.op_str)) def start(self): try: self.mu.emu_start(0x10000,0x10110) 
except: passif __name__ == '__main__': UnidbgMips().start()

这里使用了下capstone反汇编引擎来识别一下mips的代码。结果：

仔细观察可以发现，这些指令有这重复的操作，四句指令为一组：

将t0寄存器的值进行一个输出，可以发现这四句指令具体的操作就是将0x11000地址处的zjgcjy这串字符，一个个取出，然后跟我们输入值的前6个字符一个个取出进行相乘。得到一个结果，然后我们回去看hook的回调函数：

可以发现0x10010就是我们完成第一组指令后的地址 他这里将t1的值取出判断是不是等于0x2f2e，说明我们输入值的第一个字符*z=0x2F2E，后面可以因此类推，得到前6个字符：

#includeusing namespace std;
unsigned char flag[50] = { 0 };
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } printf("%srn", flag); }int main(){ getFirstHalfFlag(); return 0; }

得到结果：
cann0t

继续分析后续的代码：

发现也是以组为单位的，分别取出0x12000地址中的值和0x13000地址中的值进行一个相加得到结果，然后这两个地址+1取下一个,以此类推得到t1,t2,t3,t4,t5,t6,t7,t8寄存器的值。再回过头来看unicorn执行结束后的判断：

t1,t2,t3,t4,t5,t6,t7,t8寄存器的值进行验证。

再根据这些等式，得到一组方程两元一次方程，这里只写一个举个例子：
x1-y1=0xFC
x1+y1=0xC2
解出x1,y1，以此类推，直接写脚本，由于这里存在溢出问题，所以我采用爆破的方式，准确一点。

#includeusing namespace std;
unsigned char flag[50] = { 0 };
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } unsigned char key1[] = { 0xFC,0x1,0xF3,0xFA,0xE,0xBB,0x3E,0x0 }; unsigned char key2[] = { 0xC2,0xC3,0xD7,0xC4,0xDA,0xA5,0xA0,0xBE }; for (int i = 0; i < 8; i++) { for (unsigned char a = 32; a <= 126; a++) { for (unsigned char b = 32; b <= 126; b++) { unsigned char res1 = a - b; unsigned char res2 = a + b; if (res1 == key1[i] && res2 == key2[i]) { flag[6 + i] = a; flag[14 + i] = b; break; } } } } printf("%srn", flag); }int main(){ getFirstHalfFlag(); return 0; }

得到前半个flag：
cann0t_be_t0ocarefu1

查看第二个验证函数sub_7FF634B11A90：

先验证输入的长度为20，再公共sub_7FF634B119F0验证输入的前四个字符。查看一波sub_7FF634B119F0：

发现有一个表，然后有一个异或操作，由于这里有一个移位操作，存在丢失数据，而且就验证四个字符，所以我们直接爆破他。

#include#include<Windows.h>using namespace std;
unsigned int key[] = { 0x0,0xf26b8303,0xe13b70f7,0x1350f3f4,0xc79a971f,0x35f1141c,0x26a1e7e8,0xd4ca64eb, 0x8ad958cf,0x78b2dbcc,0x6be22838,0x9989ab3b,0x4d43cfd0,0xbf284cd3,0xac78bf27,0x5e133c24, 0x105ec76f,0xe235446c,0xf165b798,0x30e349b,0xd7c45070,0x25afd373,0x36ff2087,0xc494a384, 0x9a879fa0,0x68ec1ca3,0x7bbcef57,0x89d76c54,0x5d1d08bf,0xaf768bbc,0xbc267848,0x4e4dfb4b, 0x20bd8ede,0xd2d60ddd,0xc186fe29,0x33ed7d2a,0xe72719c1,0x154c9ac2,0x61c6936,0xf477ea35, 0xaa64d611,0x580f5512,0x4b5fa6e6,0xb93425e5,0x6dfe410e,0x9f95c20d,0x8cc531f9,0x7eaeb2fa, 0x30e349b1,0xc288cab2,0xd1d83946,0x23b3ba45,0xf779deae,0x5125dad,0x1642ae59,0xe4292d5a, 0xba3a117e,0x4851927d,0x5b016189,0xa96ae28a,0x7da08661,0x8fcb0562,0x9c9bf696,0x6ef07595, 0x417b1dbc,0xb3109ebf,0xa0406d4b,0x522bee48,0x86e18aa3,0x748a09a0,0x67dafa54,0x95b17957, 0xcba24573,0x39c9c670,0x2a993584,0xd8f2b687,0xc38d26c,0xfe53516f,0xed03a29b,0x1f682198, 0x5125dad3,0xa34e59d0,0xb01eaa24,0x42752927,0x96bf4dcc,0x64d4cecf,0x77843d3b,0x85efbe38, 0xdbfc821c,0x2997011f,0x3ac7f2eb,0xc8ac71e8,0x1c661503,0xee0d9600,0xfd5d65f4,0xf36e6f7, 0x61c69362,0x93ad1061,0x80fde395,0x72966096,0xa65c047d,0x5437877e,0x4767748a,0xb50cf789, 0xeb1fcbad,0x197448ae,0xa24bb5a,0xf84f3859,0x2c855cb2,0xdeeedfb1,0xcdbe2c45,0x3fd5af46, 0x7198540d,0x83f3d70e,0x90a324fa,0x62c8a7f9,0xb602c312,0x44694011,0x5739b3e5,0xa55230e6, 0xfb410cc2,0x92a8fc1,0x1a7a7c35,0xe811ff36,0x3cdb9bdd,0xceb018de,0xdde0eb2a,0x2f8b6829, 0x82f63b78,0x709db87b,0x63cd4b8f,0x91a6c88c,0x456cac67,0xb7072f64,0xa457dc90,0x563c5f93, 0x82f63b7,0xfa44e0b4,0xe9141340,0x1b7f9043,0xcfb5f4a8,0x3dde77ab,0x2e8e845f,0xdce5075c, 0x92a8fc17,0x60c37f14,0x73938ce0,0x81f80fe3,0x55326b08,0xa759e80b,0xb4091bff,0x466298fc, 0x1871a4d8,0xea1a27db,0xf94ad42f,0xb21572c,0xdfeb33c7,0x2d80b0c4,0x3ed04330,0xccbbc033, 0xa24bb5a6,0x502036a5,0x4370c551,0xb11b4652,0x65d122b9,0x97baa1ba,0x84ea524e,0x7681d14d, 0x2892ed69,0xdaf96e6a,0xc9a99d9e,0x3bc21e9d,0xef087a76,0x1d63f975,0xe330a81,0xfc588982, 0xb21572c9,0x407ef1ca,0x532e023e,0xa145813d,0x758fe5d6,0x87e466d5,0x94b49521,0x66df1622, 0x38cc2a06,0xcaa7a905,0xd9f75af1,0x2b9cd9f2,0xff56bd19,0xd3d3e1a,0x1e6dcdee,0xec064eed, 0xc38d26c4,0x31e6a5c7,0x22b65633,0xd0ddd530,0x417b1db,0xf67c32d8,0xe52cc12c,0x1747422f, 0x49547e0b,0xbb3ffd08,0xa86f0efc,0x5a048dff,0x8ecee914,0x7ca56a17,0x6ff599e3,0x9d9e1ae0, 0xd3d3e1ab,0x21b862a8,0x32e8915c,0xc083125f,0x144976b4,0xe622f5b7,0xf5720643,0x7198540, 0x590ab964,0xab613a67,0xb831c993,0x4a5a4a90,0x9e902e7b,0x6cfbad78,0x7fab5e8c,0x8dc0dd8f, 0xe330a81a,0x115b2b19,0x20bd8ed,0xf0605bee,0x24aa3f05,0xd6c1bc06,0xc5914ff2,0x37faccf1, 0x69e9f0d5,0x9b8273d6,0x88d28022,0x7ab90321,0xae7367ca,0x5c18e4c9,0x4f48173d,0xbd23943e, 0xf36e6f75,0x105ec76,0x12551f82,0xe03e9c81,0x34f4f86a,0xc69f7b69,0xd5cf889d,0x27a40b9e, 0x79b737ba,0x8bdcb4b9,0x988c474d,0x6ae7c44e,0xbe2da0a5,0x4c4623a6,0x5f16d052,0xad7d5351};
void getLastHalfFlag(){ unsigned int v1; DWORD res = 0xCAFABCBC; res = ~res; for (DWORD i = 0x32323232; i <= 0x7E7E7E7E; i++) { v1 = -1; unsigned char *cRes = (unsigned char*)&i; for (int j = 0; j < 4; j++) { unsigned char value = cRes[j] ^ v1; v1 = ((v1 >> 8) ^ key[value]); } if (res == v1) { printf("%xrn", i); break; } }}int main(){ getLastHalfFlag(); return 0; }

得到结果为(要等个几秒钟)：
0x6e65687转化为字符串”when”

然后继续往下分析：

后面的逻辑主要是验证输入的后16个字符，这里uc_open的第一个参数代码的是ARM架构，然后ARM的代码是从unk_7FF634B139B0开始的，大小为0x400，我们保存下来。偷个懒，用IDA的F5识别出算法。

void __noreturn sub_0(){ char *v0; // r2 char *v1; // r2 char *v2; // r2 char *v3; // r2 char *v4; // r2 char *v5; // r2 char *v6; // r3 char *v7; // r2 char *v8; // r3 char *v9; // r3 char v10[100]; // [sp+0h] [bp-8Ch] BYREF char v11[28]; // [sp+64h] [bp-28h] BYREF int i; // [sp+80h] [bp-Ch] char *v13; // [sp+84h] [bp-8h] qmemcpy(v11, ")8FP>6^B=G6@>X*P<G=B)1 ", 24); v13 = v10; for ( i = 0; i <= 13; i += 3 ) // 四个为一组 { v0 = v13++; *v0 = (*(_BYTE *)(i + 0x21024) >> 2) + 33; // 通过这个得到第i个字符的高6位 v1 = v13++; *v1 = ((16 * *(_BYTE *)(i + 135204)) & 0x30 | (*(_BYTE *)(i + 135205) >> 4)) + 33;// 这个结果包含了第i个字符的低2位和第i+1个字符的高4位 v2 = v13++; *v2 = ((4 * *(_BYTE *)(i + 135205)) & 0x3C | (*(_BYTE *)(i + 135206) >> 6)) + 33;// 这个结果包含了第i+1个字符的低4位和第i+2个字符的高两位 v3 = v13++; *v3 = (*(_BYTE *)(i + 135206) & 0x3F) + 33; // 这个结果包含了第i+2个字符的低6位 } if ( i <= 15 ) { v4 = v13++; *v4 = (*(_BYTE *)(i + 135204) >> 2) + 33; // 通过这个得出一个字符中高6位的值 v5 = v13++; if ( i == 15 ) { *v5 = ((16 * MEMORY[0x21033]) & 0x30) + 33;// ((16**(byte*)(i+0x21024))&0x30)+0x21 通过这个计算一个字符中最低两位的值 v6 = v13++; *v6 = 32; } else { *v5 = ((16 * *(_BYTE *)(i + 135204)) & 0x30 | (*(_BYTE *)(i + 135205) >> 4)) + 33; v7 = v13++; *v7 = ((4 * *(_BYTE *)(i + 135205)) & 0x3C) + 33; } v8 = v13++; *v8 = 32; } v9 = v13++; *v9 = 0; for ( i = 0; i <= 23 && v10[i] == v11[i]; ++i ) ; JUMPOUT(0x400);}

算法的大题逻辑能看，但是还是有些东西看不清楚，我们跟前面一样，自己用unicorn写一个调试一下。

from unicorn import *from unicorn.x86_const import *from unicorn.arm_const import *from unicorn.mips_const import *from capstone import *with open('Arm', 'rb') as file: ARM_CODE=file.read()class UnidbgArm: def __init__(self): # x32程序 mu = Uc(UC_ARCH_ARM, UC_MODE_ARM) mu.mem_map(0x200000, 0x200000) mu.mem_map(0x10000,0x1000) mu.mem_write(0x200000,ARM_CODE) mu.mem_map(0x20000,0x10000) mu.mem_write(0x21024,b"1234567891234567x00x00x00x00x00x00x00x00x00x00x00x00x00") #输入假的数据 mu.reg_write(UC_ARM_REG_SP,0x11000) mu.hook_add(UC_HOOK_CODE, self.hook_code) self.mu=mu # 反汇编引擎 self.md = Cs(CS_ARCH_ARM,UC_MODE_ARM) def hook_code(self, mu,address, size, data): if address==0x200010 or address==0x200058: v5=mu.reg_read(UC_ARM_REG_R3) v5+=15 mu.reg_write(UC_ARM_REG_R3,v5) elif address==0x200018: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x6F mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200020 or address==0x200040: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=12 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200028: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x12 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200030 or address==0x200070: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=5 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200038: v5 = mu.reg_read(UC_ARM_REG_R3) v5 += 33 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200048: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0xD mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200050: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=3 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200060: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x68 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200068: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0xA mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200078: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -= 33 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200080: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=48 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200088: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x18 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200090: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=2 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200098: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=16 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000A0: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x1B mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000A8: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=6 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000B0: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x13 mu.reg_write(UC_ARM_REG_R3, v5) # if(mu.reg_read(UC_ARM_REG_R3)>=32 and mu.reg_read(UC_ARM_REG_R3)<=126): # print(chr(mu.reg_read(UC_ARM_REG_R3))) # else: print("r3:0x%x r2:0x%x r1:0x%x r0:0x%x"%(mu.reg_read(UC_ARM_REG_R3),mu.reg_read(UC_ARM_REG_R2),mu.reg_read(UC_ARM_REG_R1),mu.reg_read(UC_ARM_REG_R0))) disasm = self.md.disasm(mu.mem_read(address, size), address) for i in disasm: print("0x%x:t%st%s" %(i.address,i.mnemonic,i.op_str)) def start(self): try: self.mu.emu_start(0x200000, 0x200400) print(self.mu.reg_read(66)) 
except: passif __name__ == '__main__': #UnidbgMips().start() UnidbgArm().start()

发现这里有一些常量存到了一个连续的地址中，对应IDA就是以下一些字符：

但是他在程序中注册了一个hook回调，我们看一下回调里干了啥：

对v5进行了一些操作，而v5对应的就是代码里的r3寄存器，说明该hook代码将IDA中识别的字符串进行了改变，手动提取得到：

unsigned char res[] = { 0x38,0x57,0x3A,0x42,0x39,0x57,0x52,0x4F,0x3A,0x56,0x5E,0x4A,0x39,0x37,0x5A,0x48,0x3E,0x37,0x26,0x48,0x3A,0x31 };

接下来就是对下面算法的逆向求解：

他将我们输入的字符进行了一些拆分，然后存起来。通过自己写的unicorn调试输出一些寄存器的值，得到函数最后将拆分得到的结果值和上面的那串res里的值进行比对，直接写脚本求解：

#include#include<Windows.h>using namespace std;
unsigned char flag[50] = { 0 };
unsigned int key[] = { 0x0,0xf26b8303,0xe13b70f7,0x1350f3f4,0xc79a971f,0x35f1141c,0x26a1e7e8,0xd4ca64eb, 0x8ad958cf,0x78b2dbcc,0x6be22838,0x9989ab3b,0x4d43cfd0,0xbf284cd3,0xac78bf27,0x5e133c24, 0x105ec76f,0xe235446c,0xf165b798,0x30e349b,0xd7c45070,0x25afd373,0x36ff2087,0xc494a384, 0x9a879fa0,0x68ec1ca3,0x7bbcef57,0x89d76c54,0x5d1d08bf,0xaf768bbc,0xbc267848,0x4e4dfb4b, 0x20bd8ede,0xd2d60ddd,0xc186fe29,0x33ed7d2a,0xe72719c1,0x154c9ac2,0x61c6936,0xf477ea35, 0xaa64d611,0x580f5512,0x4b5fa6e6,0xb93425e5,0x6dfe410e,0x9f95c20d,0x8cc531f9,0x7eaeb2fa, 0x30e349b1,0xc288cab2,0xd1d83946,0x23b3ba45,0xf779deae,0x5125dad,0x1642ae59,0xe4292d5a, 0xba3a117e,0x4851927d,0x5b016189,0xa96ae28a,0x7da08661,0x8fcb0562,0x9c9bf696,0x6ef07595, 0x417b1dbc,0xb3109ebf,0xa0406d4b,0x522bee48,0x86e18aa3,0x748a09a0,0x67dafa54,0x95b17957, 0xcba24573,0x39c9c670,0x2a993584,0xd8f2b687,0xc38d26c,0xfe53516f,0xed03a29b,0x1f682198, 0x5125dad3,0xa34e59d0,0xb01eaa24,0x42752927,0x96bf4dcc,0x64d4cecf,0x77843d3b,0x85efbe38, 0xdbfc821c,0x2997011f,0x3ac7f2eb,0xc8ac71e8,0x1c661503,0xee0d9600,0xfd5d65f4,0xf36e6f7, 0x61c69362,0x93ad1061,0x80fde395,0x72966096,0xa65c047d,0x5437877e,0x4767748a,0xb50cf789, 0xeb1fcbad,0x197448ae,0xa24bb5a,0xf84f3859,0x2c855cb2,0xdeeedfb1,0xcdbe2c45,0x3fd5af46, 0x7198540d,0x83f3d70e,0x90a324fa,0x62c8a7f9,0xb602c312,0x44694011,0x5739b3e5,0xa55230e6, 0xfb410cc2,0x92a8fc1,0x1a7a7c35,0xe811ff36,0x3cdb9bdd,0xceb018de,0xdde0eb2a,0x2f8b6829, 0x82f63b78,0x709db87b,0x63cd4b8f,0x91a6c88c,0x456cac67,0xb7072f64,0xa457dc90,0x563c5f93, 0x82f63b7,0xfa44e0b4,0xe9141340,0x1b7f9043,0xcfb5f4a8,0x3dde77ab,0x2e8e845f,0xdce5075c, 0x92a8fc17,0x60c37f14,0x73938ce0,0x81f80fe3,0x55326b08,0xa759e80b,0xb4091bff,0x466298fc, 0x1871a4d8,0xea1a27db,0xf94ad42f,0xb21572c,0xdfeb33c7,0x2d80b0c4,0x3ed04330,0xccbbc033, 0xa24bb5a6,0x502036a5,0x4370c551,0xb11b4652,0x65d122b9,0x97baa1ba,0x84ea524e,0x7681d14d, 0x2892ed69,0xdaf96e6a,0xc9a99d9e,0x3bc21e9d,0xef087a76,0x1d63f975,0xe330a81,0xfc588982, 0xb21572c9,0x407ef1ca,0x532e023e,0xa145813d,0x758fe5d6,0x87e466d5,0x94b49521,0x66df1622, 0x38cc2a06,0xcaa7a905,0xd9f75af1,0x2b9cd9f2,0xff56bd19,0xd3d3e1a,0x1e6dcdee,0xec064eed, 0xc38d26c4,0x31e6a5c7,0x22b65633,0xd0ddd530,0x417b1db,0xf67c32d8,0xe52cc12c,0x1747422f, 0x49547e0b,0xbb3ffd08,0xa86f0efc,0x5a048dff,0x8ecee914,0x7ca56a17,0x6ff599e3,0x9d9e1ae0, 0xd3d3e1ab,0x21b862a8,0x32e8915c,0xc083125f,0x144976b4,0xe622f5b7,0xf5720643,0x7198540, 0x590ab964,0xab613a67,0xb831c993,0x4a5a4a90,0x9e902e7b,0x6cfbad78,0x7fab5e8c,0x8dc0dd8f, 0xe330a81a,0x115b2b19,0x20bd8ed,0xf0605bee,0x24aa3f05,0xd6c1bc06,0xc5914ff2,0x37faccf1, 0x69e9f0d5,0x9b8273d6,0x88d28022,0x7ab90321,0xae7367ca,0x5c18e4c9,0x4f48173d,0xbd23943e, 0xf36e6f75,0x105ec76,0x12551f82,0xe03e9c81,0x34f4f86a,0xc69f7b69,0xd5cf889d,0x27a40b9e, 0x79b737ba,0x8bdcb4b9,0x988c474d,0x6ae7c44e,0xbe2da0a5,0x4c4623a6,0x5f16d052,0xad7d5351};
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } printf("%srn", flag); unsigned char key1[] = { 0xFC,0x1,0xF3,0xFA,0xE,0xBB,0x3E,0x0 }; unsigned char key2[] = { 0xC2,0xC3,0xD7,0xC4,0xDA,0xA5,0xA0,0xBE }; for (int i = 0; i < 8; i++) { for (unsigned char a = 32; a <= 126; a++) { for (unsigned char b = 32; b <= 126; b++) { unsigned char res1 = a - b; unsigned char res2 = a + b; if (res1 == key1[i] && res2 == key2[i]) { flag[6 + i] = a; flag[14 + i] = b; break; } } } } printf("%srn", flag);} void getLastHalfFlag(){ //直接爆破 爆出来是 when /* unsigned int v1; DWORD res = 0xCAFABCBC; res = ~res; for (DWORD i = 0x32323232; i <= 0x7E7E7E7E; i++) { v1 = -1; unsigned char *cRes = (unsigned char*)&i; for (int j = 0; j < 4; j++) { unsigned char value = cRes[j] ^ v1; v1 = ((v1 >> 8) ^ key[value]); } if (res == v1) { printf("%xrn", i); break; } } */ memcpy(&flag[22], "when", 4); printf("%srn", flag); unsigned char res[] = { 0x38,0x57,0x3A,0x42,0x39,0x57,0x52,0x4F,0x3A,0x56,0x5E,0x4A,0x39,0x37,0x5A, 0x48,0x3E,0x37,0x26,0x48,0x3A,0x31 }; unsigned char chr1 = 0; unsigned char chr2 = 0; unsigned char chr3 = 0; int total = 26; for (int i = 0; i < 18; i += 4) { chr1 = (res[i] - 0x21) << 2; chr1 = ((res[i + 1] - 0x21) >> 4) | chr1; chr2 = ((res[i + 1] - 0x21) << 4); chr2 = ((res[i + 2] - 0x21) >>2) | chr2; chr3 = res[i + 3] - 0x21; chr3 = ((res[i + 2] - 0x21) << 6) | chr3; flag[total++] = chr1; flag[total++] = chr2; flag[total++] = chr3; } chr1= (res[20] - 0x21) << 2; chr1 = chr1 | ((res[21] - 0x21) >> 4); flag[total] = chr1; printf("%srn", flag); } int main(){ getFirstHalfFlag(); getLastHalfFlag(); return 0; }

得到完整flag：
cann0t_be_t0o_carefu1_when_faclng_ianguage

‍‍‍

看雪ID：榆一

https://bbs.pediy.com/user-home-923269.htm

*本文由看雪论坛 榆一 原创，转载请注明来自看雪社区

# 往期推荐

1.Docker-remoter-api渗透

2.Writeup-ROP Emporium fluff

3.Windows内核-句柄

4.APT28样本超详细分析

5.CVE-2016-0095提权漏洞学习笔记

6.java序列化与反序列化

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
__int64 __fastcall sub_7FF634B11000(__int64 a1, __int64 a2){ __int64 result; // rax int v5; // [rsp+20h] [rbp-28h] BYREF int v6; // [rsp+24h] [rbp-24h] BYREF int v7; // [rsp+28h] [rbp-20h] BYREF int v8; // [rsp+2Ch] [rbp-1Ch] BYREF int v9[6]; // [rsp+30h] [rbp-18h] BYREF int v10; // [rsp+58h] [rbp+10h] BYREF uc_reg_read(a1, 11i64, &v10); uc_reg_read(a1, 12i64, &v5); uc_reg_read(a1, 13i64, &v6); uc_reg_read(a1, 14i64, &v7); uc_reg_read(a1, 15i64, &v8); result = uc_reg_read(a1, 16i64, v9); switch ( a2 ) // a2是地址 { case 0x10010i64: result = uc_reg_read(a1, 11i64, &v10); if ( v10 != 0x2F2E ) { printf("You died before you killed anyone.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10020i64: result = uc_reg_read(a1, 12i64, &v5); if ( v5 != 0x282A ) { printf("You died when you killed only one.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10030i64: result = uc_reg_read(a1, 13i64, &v6); if ( v6 != 0x2C42 ) { printf("Nice! Double kill, but died.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10040i64: result = uc_reg_read(a1, 14i64, &v7); if ( v7 != 0x2A8A ) { printf("Awesome! Triple Kill, but interrupted.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10050i64: result = uc_reg_read(a1, 15i64, &v8); if ( v8 != 0x13E0 ) { printf("Unimaginable! Quadra Kill, but emm...You know what I want to say.n"); uc_emu_stop(a1); exit(-1); } return result; case 0x10060i64: result = uc_reg_read(a1, 16i64, v9); if ( v9[0] != 0x36D4 ) { printf("Incredible! Penta Kill, but frankly, you still died.n"); uc_emu_stop(a1); exit(-1); } return result; default: return result; } return result;}
from unicorn import *from unicorn.x86_const import *from unicorn.arm_const import *from unicorn.mips_const import *from capstone import *with open('mips', 'rb') as file: #读代码段 MIPS_CODE = file.read() # 读取代码
class UnidbgMips: def __init__(self): # x32程序 mu = Uc(UC_ARCH_MIPS, UC_MODE_32) mu.mem_map(0x10000, 0x200000) mu.mem_write(0x10000,MIPS_CODE) mu.mem_write(0x11000,b"zjgcjyx00") mu.mem_write(0x12000,b"xFCx01xF3xFAx0ExBBx3Ex00") #输入假的值 mu.mem_write(0x13000,b"x00x00x00x00x00x00x00x00") mu.reg_write(UC_MIPS_REG_T1, 0x30)#输入假的值 mu.reg_write(UC_MIPS_REG_T2, 0x31) mu.reg_write(UC_MIPS_REG_T3, 0x32) mu.reg_write(UC_MIPS_REG_T4, 0x33) mu.reg_write(UC_MIPS_REG_T5, 0x34) mu.reg_write(UC_MIPS_REG_T6, 0x35) mu.hook_add(UC_HOOK_CODE, self.hook_code) self.mu=mu # 反汇编引擎 self.md = Cs(CS_ARCH_MIPS, CS_MODE_32) def hook_code(self, mu, address, size, data): disasm = self.md.disasm(mu.mem_read(address, size), address) for i in disasm: print("0x%x:t%st%s" %(i.address,i.mnemonic,i.op_str)) def start(self): try: self.mu.emu_start(0x10000,0x10110) 
except: passif __name__ == '__main__': UnidbgMips().start()
    #includeusing namespace std;
unsigned char flag[50] = { 0 };
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } printf("%srn", flag); }int main(){ getFirstHalfFlag(); return 0; }
    #includeusing namespace std;
unsigned char flag[50] = { 0 };
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } unsigned char key1[] = { 0xFC,0x1,0xF3,0xFA,0xE,0xBB,0x3E,0x0 }; unsigned char key2[] = { 0xC2,0xC3,0xD7,0xC4,0xDA,0xA5,0xA0,0xBE }; for (int i = 0; i < 8; i++) { for (unsigned char a = 32; a <= 126; a++) { for (unsigned char b = 32; b <= 126; b++) { unsigned char res1 = a - b; unsigned char res2 = a + b; if (res1 == key1[i] && res2 == key2[i]) { flag[6 + i] = a; flag[14 + i] = b; break; } } } } printf("%srn", flag); }int main(){ getFirstHalfFlag(); return 0; }
    #include#include<Windows.h>using namespace std;
unsigned int key[] = { 0x0,0xf26b8303,0xe13b70f7,0x1350f3f4,0xc79a971f,0x35f1141c,0x26a1e7e8,0xd4ca64eb, 0x8ad958cf,0x78b2dbcc,0x6be22838,0x9989ab3b,0x4d43cfd0,0xbf284cd3,0xac78bf27,0x5e133c24, 0x105ec76f,0xe235446c,0xf165b798,0x30e349b,0xd7c45070,0x25afd373,0x36ff2087,0xc494a384, 0x9a879fa0,0x68ec1ca3,0x7bbcef57,0x89d76c54,0x5d1d08bf,0xaf768bbc,0xbc267848,0x4e4dfb4b, 0x20bd8ede,0xd2d60ddd,0xc186fe29,0x33ed7d2a,0xe72719c1,0x154c9ac2,0x61c6936,0xf477ea35, 0xaa64d611,0x580f5512,0x4b5fa6e6,0xb93425e5,0x6dfe410e,0x9f95c20d,0x8cc531f9,0x7eaeb2fa, 0x30e349b1,0xc288cab2,0xd1d83946,0x23b3ba45,0xf779deae,0x5125dad,0x1642ae59,0xe4292d5a, 0xba3a117e,0x4851927d,0x5b016189,0xa96ae28a,0x7da08661,0x8fcb0562,0x9c9bf696,0x6ef07595, 0x417b1dbc,0xb3109ebf,0xa0406d4b,0x522bee48,0x86e18aa3,0x748a09a0,0x67dafa54,0x95b17957, 0xcba24573,0x39c9c670,0x2a993584,0xd8f2b687,0xc38d26c,0xfe53516f,0xed03a29b,0x1f682198, 0x5125dad3,0xa34e59d0,0xb01eaa24,0x42752927,0x96bf4dcc,0x64d4cecf,0x77843d3b,0x85efbe38, 0xdbfc821c,0x2997011f,0x3ac7f2eb,0xc8ac71e8,0x1c661503,0xee0d9600,0xfd5d65f4,0xf36e6f7, 0x61c69362,0x93ad1061,0x80fde395,0x72966096,0xa65c047d,0x5437877e,0x4767748a,0xb50cf789, 0xeb1fcbad,0x197448ae,0xa24bb5a,0xf84f3859,0x2c855cb2,0xdeeedfb1,0xcdbe2c45,0x3fd5af46, 0x7198540d,0x83f3d70e,0x90a324fa,0x62c8a7f9,0xb602c312,0x44694011,0x5739b3e5,0xa55230e6, 0xfb410cc2,0x92a8fc1,0x1a7a7c35,0xe811ff36,0x3cdb9bdd,0xceb018de,0xdde0eb2a,0x2f8b6829, 0x82f63b78,0x709db87b,0x63cd4b8f,0x91a6c88c,0x456cac67,0xb7072f64,0xa457dc90,0x563c5f93, 0x82f63b7,0xfa44e0b4,0xe9141340,0x1b7f9043,0xcfb5f4a8,0x3dde77ab,0x2e8e845f,0xdce5075c, 0x92a8fc17,0x60c37f14,0x73938ce0,0x81f80fe3,0x55326b08,0xa759e80b,0xb4091bff,0x466298fc, 0x1871a4d8,0xea1a27db,0xf94ad42f,0xb21572c,0xdfeb33c7,0x2d80b0c4,0x3ed04330,0xccbbc033, 0xa24bb5a6,0x502036a5,0x4370c551,0xb11b4652,0x65d122b9,0x97baa1ba,0x84ea524e,0x7681d14d, 0x2892ed69,0xdaf96e6a,0xc9a99d9e,0x3bc21e9d,0xef087a76,0x1d63f975,0xe330a81,0xfc588982, 0xb21572c9,0x407ef1ca,0x532e023e,0xa145813d,0x758fe5d6,0x87e466d5,0x94b49521,0x66df1622, 0x38cc2a06,0xcaa7a905,0xd9f75af1,0x2b9cd9f2,0xff56bd19,0xd3d3e1a,0x1e6dcdee,0xec064eed, 0xc38d26c4,0x31e6a5c7,0x22b65633,0xd0ddd530,0x417b1db,0xf67c32d8,0xe52cc12c,0x1747422f, 0x49547e0b,0xbb3ffd08,0xa86f0efc,0x5a048dff,0x8ecee914,0x7ca56a17,0x6ff599e3,0x9d9e1ae0, 0xd3d3e1ab,0x21b862a8,0x32e8915c,0xc083125f,0x144976b4,0xe622f5b7,0xf5720643,0x7198540, 0x590ab964,0xab613a67,0xb831c993,0x4a5a4a90,0x9e902e7b,0x6cfbad78,0x7fab5e8c,0x8dc0dd8f, 0xe330a81a,0x115b2b19,0x20bd8ed,0xf0605bee,0x24aa3f05,0xd6c1bc06,0xc5914ff2,0x37faccf1, 0x69e9f0d5,0x9b8273d6,0x88d28022,0x7ab90321,0xae7367ca,0x5c18e4c9,0x4f48173d,0xbd23943e, 0xf36e6f75,0x105ec76,0x12551f82,0xe03e9c81,0x34f4f86a,0xc69f7b69,0xd5cf889d,0x27a40b9e, 0x79b737ba,0x8bdcb4b9,0x988c474d,0x6ae7c44e,0xbe2da0a5,0x4c4623a6,0x5f16d052,0xad7d5351};
void getLastHalfFlag(){ unsigned int v1; DWORD res = 0xCAFABCBC; res = ~res; for (DWORD i = 0x32323232; i <= 0x7E7E7E7E; i++) { v1 = -1; unsigned char *cRes = (unsigned char*)&i; for (int j = 0; j < 4; j++) { unsigned char value = cRes[j] ^ v1; v1 = ((v1 >> 8) ^ key[value]); } if (res == v1) { printf("%xrn", i); break; } }}int main(){ getLastHalfFlag(); return 0; }
void __noreturn sub_0(){ char *v0; // r2 char *v1; // r2 char *v2; // r2 char *v3; // r2 char *v4; // r2 char *v5; // r2 char *v6; // r3 char *v7; // r2 char *v8; // r3 char *v9; // r3 char v10[100]; // [sp+0h] [bp-8Ch] BYREF char v11[28]; // [sp+64h] [bp-28h] BYREF int i; // [sp+80h] [bp-Ch] char *v13; // [sp+84h] [bp-8h] qmemcpy(v11, ")8FP>6^B=G6@>X*P<G=B)1 ", 24); v13 = v10; for ( i = 0; i <= 13; i += 3 ) // 四个为一组 { v0 = v13++; *v0 = (*(_BYTE *)(i + 0x21024) >> 2) + 33; // 通过这个得到第i个字符的高6位 v1 = v13++; *v1 = ((16 * *(_BYTE *)(i + 135204)) & 0x30 | (*(_BYTE *)(i + 135205) >> 4)) + 33;// 这个结果包含了第i个字符的低2位和第i+1个字符的高4位 v2 = v13++; *v2 = ((4 * *(_BYTE *)(i + 135205)) & 0x3C | (*(_BYTE *)(i + 135206) >> 6)) + 33;// 这个结果包含了第i+1个字符的低4位和第i+2个字符的高两位 v3 = v13++; *v3 = (*(_BYTE *)(i + 135206) & 0x3F) + 33; // 这个结果包含了第i+2个字符的低6位 } if ( i <= 15 ) { v4 = v13++; *v4 = (*(_BYTE *)(i + 135204) >> 2) + 33; // 通过这个得出一个字符中高6位的值 v5 = v13++; if ( i == 15 ) { *v5 = ((16 * MEMORY[0x21033]) & 0x30) + 33;// ((16**(byte*)(i+0x21024))&0x30)+0x21 通过这个计算一个字符中最低两位的值 v6 = v13++; *v6 = 32; } else { *v5 = ((16 * *(_BYTE *)(i + 135204)) & 0x30 | (*(_BYTE *)(i + 135205) >> 4)) + 33; v7 = v13++; *v7 = ((4 * *(_BYTE *)(i + 135205)) & 0x3C) + 33; } v8 = v13++; *v8 = 32; } v9 = v13++; *v9 = 0; for ( i = 0; i <= 23 && v10[i] == v11[i]; ++i ) ; JUMPOUT(0x400);}
from unicorn import *from unicorn.x86_const import *from unicorn.arm_const import *from unicorn.mips_const import *from capstone import *with open('Arm', 'rb') as file: ARM_CODE=file.read()class UnidbgArm: def __init__(self): # x32程序 mu = Uc(UC_ARCH_ARM, UC_MODE_ARM) mu.mem_map(0x200000, 0x200000) mu.mem_map(0x10000,0x1000) mu.mem_write(0x200000,ARM_CODE) mu.mem_map(0x20000,0x10000) mu.mem_write(0x21024,b"1234567891234567x00x00x00x00x00x00x00x00x00x00x00x00x00") #输入假的数据 mu.reg_write(UC_ARM_REG_SP,0x11000) mu.hook_add(UC_HOOK_CODE, self.hook_code) self.mu=mu # 反汇编引擎 self.md = Cs(CS_ARCH_ARM,UC_MODE_ARM) def hook_code(self, mu,address, size, data): if address==0x200010 or address==0x200058: v5=mu.reg_read(UC_ARM_REG_R3) v5+=15 mu.reg_write(UC_ARM_REG_R3,v5) elif address==0x200018: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x6F mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200020 or address==0x200040: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=12 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200028: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x12 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200030 or address==0x200070: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=5 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200038: v5 = mu.reg_read(UC_ARM_REG_R3) v5 += 33 mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200048: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0xD mu.reg_write(UC_ARM_REG_R3, v5) elif address==0x200050: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=3 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200060: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0x68 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200068: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^= 0xA mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200078: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -= 33 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200080: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=48 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200088: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x18 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200090: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=2 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x200098: v5 = mu.reg_read(UC_ARM_REG_R3) v5 -=16 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000A0: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x1B mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000A8: v5 = mu.reg_read(UC_ARM_REG_R3) v5 +=6 mu.reg_write(UC_ARM_REG_R3, v5) elif address == 0x2000B0: v5 = mu.reg_read(UC_ARM_REG_R3) v5 ^=0x13 mu.reg_write(UC_ARM_REG_R3, v5) # if(mu.reg_read(UC_ARM_REG_R3)>=32 and mu.reg_read(UC_ARM_REG_R3)<=126): # print(chr(mu.reg_read(UC_ARM_REG_R3))) # else: print("r3:0x%x r2:0x%x r1:0x%x r0:0x%x"%(mu.reg_read(UC_ARM_REG_R3),mu.reg_read(UC_ARM_REG_R2),mu.reg_read(UC_ARM_REG_R1),mu.reg_read(UC_ARM_REG_R0))) disasm = self.md.disasm(mu.mem_read(address, size), address) for i in disasm: print("0x%x:t%st%s" %(i.address,i.mnemonic,i.op_str)) def start(self): try: self.mu.emu_start(0x200000, 0x200400) print(self.mu.reg_read(66)) 
except: passif __name__ == '__main__': #UnidbgMips().start() UnidbgArm().start()
unsigned char res[] = { 0x38,0x57,0x3A,0x42,0x39,0x57,0x52,0x4F,0x3A,0x56,0x5E,0x4A,0x39,0x37,0x5A,0x48,0x3E,0x37,0x26,0x48,0x3A,0x31 };
    #include#include<Windows.h>using namespace std;
unsigned char flag[50] = { 0 };
unsigned int key[] = { 0x0,0xf26b8303,0xe13b70f7,0x1350f3f4,0xc79a971f,0x35f1141c,0x26a1e7e8,0xd4ca64eb, 0x8ad958cf,0x78b2dbcc,0x6be22838,0x9989ab3b,0x4d43cfd0,0xbf284cd3,0xac78bf27,0x5e133c24, 0x105ec76f,0xe235446c,0xf165b798,0x30e349b,0xd7c45070,0x25afd373,0x36ff2087,0xc494a384, 0x9a879fa0,0x68ec1ca3,0x7bbcef57,0x89d76c54,0x5d1d08bf,0xaf768bbc,0xbc267848,0x4e4dfb4b, 0x20bd8ede,0xd2d60ddd,0xc186fe29,0x33ed7d2a,0xe72719c1,0x154c9ac2,0x61c6936,0xf477ea35, 0xaa64d611,0x580f5512,0x4b5fa6e6,0xb93425e5,0x6dfe410e,0x9f95c20d,0x8cc531f9,0x7eaeb2fa, 0x30e349b1,0xc288cab2,0xd1d83946,0x23b3ba45,0xf779deae,0x5125dad,0x1642ae59,0xe4292d5a, 0xba3a117e,0x4851927d,0x5b016189,0xa96ae28a,0x7da08661,0x8fcb0562,0x9c9bf696,0x6ef07595, 0x417b1dbc,0xb3109ebf,0xa0406d4b,0x522bee48,0x86e18aa3,0x748a09a0,0x67dafa54,0x95b17957, 0xcba24573,0x39c9c670,0x2a993584,0xd8f2b687,0xc38d26c,0xfe53516f,0xed03a29b,0x1f682198, 0x5125dad3,0xa34e59d0,0xb01eaa24,0x42752927,0x96bf4dcc,0x64d4cecf,0x77843d3b,0x85efbe38, 0xdbfc821c,0x2997011f,0x3ac7f2eb,0xc8ac71e8,0x1c661503,0xee0d9600,0xfd5d65f4,0xf36e6f7, 0x61c69362,0x93ad1061,0x80fde395,0x72966096,0xa65c047d,0x5437877e,0x4767748a,0xb50cf789, 0xeb1fcbad,0x197448ae,0xa24bb5a,0xf84f3859,0x2c855cb2,0xdeeedfb1,0xcdbe2c45,0x3fd5af46, 0x7198540d,0x83f3d70e,0x90a324fa,0x62c8a7f9,0xb602c312,0x44694011,0x5739b3e5,0xa55230e6, 0xfb410cc2,0x92a8fc1,0x1a7a7c35,0xe811ff36,0x3cdb9bdd,0xceb018de,0xdde0eb2a,0x2f8b6829, 0x82f63b78,0x709db87b,0x63cd4b8f,0x91a6c88c,0x456cac67,0xb7072f64,0xa457dc90,0x563c5f93, 0x82f63b7,0xfa44e0b4,0xe9141340,0x1b7f9043,0xcfb5f4a8,0x3dde77ab,0x2e8e845f,0xdce5075c, 0x92a8fc17,0x60c37f14,0x73938ce0,0x81f80fe3,0x55326b08,0xa759e80b,0xb4091bff,0x466298fc, 0x1871a4d8,0xea1a27db,0xf94ad42f,0xb21572c,0xdfeb33c7,0x2d80b0c4,0x3ed04330,0xccbbc033, 0xa24bb5a6,0x502036a5,0x4370c551,0xb11b4652,0x65d122b9,0x97baa1ba,0x84ea524e,0x7681d14d, 0x2892ed69,0xdaf96e6a,0xc9a99d9e,0x3bc21e9d,0xef087a76,0x1d63f975,0xe330a81,0xfc588982, 0xb21572c9,0x407ef1ca,0x532e023e,0xa145813d,0x758fe5d6,0x87e466d5,0x94b49521,0x66df1622, 0x38cc2a06,0xcaa7a905,0xd9f75af1,0x2b9cd9f2,0xff56bd19,0xd3d3e1a,0x1e6dcdee,0xec064eed, 0xc38d26c4,0x31e6a5c7,0x22b65633,0xd0ddd530,0x417b1db,0xf67c32d8,0xe52cc12c,0x1747422f, 0x49547e0b,0xbb3ffd08,0xa86f0efc,0x5a048dff,0x8ecee914,0x7ca56a17,0x6ff599e3,0x9d9e1ae0, 0xd3d3e1ab,0x21b862a8,0x32e8915c,0xc083125f,0x144976b4,0xe622f5b7,0xf5720643,0x7198540, 0x590ab964,0xab613a67,0xb831c993,0x4a5a4a90,0x9e902e7b,0x6cfbad78,0x7fab5e8c,0x8dc0dd8f, 0xe330a81a,0x115b2b19,0x20bd8ed,0xf0605bee,0x24aa3f05,0xd6c1bc06,0xc5914ff2,0x37faccf1, 0x69e9f0d5,0x9b8273d6,0x88d28022,0x7ab90321,0xae7367ca,0x5c18e4c9,0x4f48173d,0xbd23943e, 0xf36e6f75,0x105ec76,0x12551f82,0xe03e9c81,0x34f4f86a,0xc69f7b69,0xd5cf889d,0x27a40b9e, 0x79b737ba,0x8bdcb4b9,0x988c474d,0x6ae7c44e,0xbe2da0a5,0x4c4623a6,0x5f16d052,0xad7d5351};
void getFirstHalfFlag(){ memset(flag, 0, 50); unsigned int res[] = { 0x2F2E,0x282A,0x2C42,0x2A8A,0x13E0,0x36D4 }; unsigned char key[] = "zjgcjy"; for (int i = 0; i < 6; i++) { flag[i] = res[i] / key[i]; } printf("%srn", flag); unsigned char key1[] = { 0xFC,0x1,0xF3,0xFA,0xE,0xBB,0x3E,0x0 }; unsigned char key2[] = { 0xC2,0xC3,0xD7,0xC4,0xDA,0xA5,0xA0,0xBE }; for (int i = 0; i < 8; i++) { for (unsigned char a = 32; a <= 126; a++) { for (unsigned char b = 32; b <= 126; b++) { unsigned char res1 = a - b; unsigned char res2 = a + b; if (res1 == key1[i] && res2 == key2[i]) { flag[6 + i] = a; flag[14 + i] = b; break; } } } } printf("%srn", flag);} void getLastHalfFlag(){ //直接爆破 爆出来是 when /* unsigned int v1; DWORD res = 0xCAFABCBC; res = ~res; for (DWORD i = 0x32323232; i <= 0x7E7E7E7E; i++) { v1 = -1; unsigned char *cRes = (unsigned char*)&i; for (int j = 0; j < 4; j++) { unsigned char value = cRes[j] ^ v1; v1 = ((v1 >> 8) ^ key[value]); } if (res == v1) { printf("%xrn", i); break; } } */ memcpy(&flag[22], "when", 4); printf("%srn", flag); unsigned char res[] = { 0x38,0x57,0x3A,0x42,0x39,0x57,0x52,0x4F,0x3A,0x56,0x5E,0x4A,0x39,0x37,0x5A, 0x48,0x3E,0x37,0x26,0x48,0x3A,0x31 }; unsigned char chr1 = 0; unsigned char chr2 = 0; unsigned char chr3 = 0; int total = 26; for (int i = 0; i < 18; i += 4) { chr1 = (res[i] - 0x21) << 2; chr1 = ((res[i + 1] - 0x21) >> 4) | chr1; chr2 = ((res[i + 1] - 0x21) << 4); chr2 = ((res[i + 2] - 0x21) >>2) | chr2; chr3 = res[i + 3] - 0x21; chr3 = ((res[i + 2] - 0x21) << 6) | chr3; flag[total++] = chr1; flag[total++] = chr2; flag[total++] = chr3; } chr1= (res[20] - 0x21) << 2; chr1 = chr1 | ((res[21] - 0x21) >> 4); flag[total] = chr1; printf("%srn", flag); } int main(){ getFirstHalfFlag(); getLastHalfFlag(); return 0; }
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/2-1650381400.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/0-1650381400.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/7-1650381400.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/4-1650381401.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/4-1650381401.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/9-1650381402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/5-1650381402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/1-1650381402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/8-1650381402.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/04/6-1650381403.png)