---
title: 强网拟态2025初赛 Mobile方向 just Writeup - Unity il2cpp Frida hook
contest: 强网拟态2025初赛 Mobile方向
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- Unity
- il2cpp
- Frida
- hook_clone
- Arm64Writer
- nop_64
- crc_check
- global-metadata.dat
- dec_global_metadata
- XOR解密
- Il2CppDumper
- Android_Reverse
- Mobile
attack_chain: Frida hook_clone监听子线程栈地址 → 识别libjust.so → nop_64(base+0x119F8)过CRC校验 → Il2CppDumper dump global-metadata.dat → dec_global_metadata函数:XOR解密 (src[2*v2+0x202] ^ src[2*(v9%v2)+0x202])
key_payload: Frida hook_clone + nop_64(0x119F8) CRC + global-metadata.dat XOR解密 + Il2CppDumper
one_liner: 强网拟态2025初赛Mobile just:Unity il2cpp Frida hook_clone NOP CRC+global-metadata.dat XOR解密。
lesson: Unity il2cpp游戏Mobile逆向:Frida hook clone监控子线程栈地址,识别目标so后NOP关键地址过CRC校验;global-metadata.dat需Il2CppDumper解;dec_global_metadata用XOR链式解v9%v2;Arm64Writer.w.putRet()写RET指令。
quality: high
full_path: 强网拟态2025初赛_Mobile方向just_Writeup.full.md
meta_path: 强网拟态2025初赛_Mobile方向just_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 强网拟态2025初赛 Mobile方向 just Writeup - Unity il2cpp Frida hook。强网拟态2025初赛Mobile just:Unity il2cpp Frida hook_clone NOP CRC+global-metadata.dat XOR解密。。经验：Unity il2cpp游戏Mobile逆向:Frida hook clone监控子线程栈地址,...
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/275655.html
reasoning_chain:
- Unity il2cpp Mobile 逆向 just：Frida hook_clone + nop CRC + Il2CppDumper + XOR 解密 → 触发点：Unity il2cpp 标准逆向流程
- Frida hook clone 监听子线程栈地址 → 假设：clone 调用栈可识别目标 so → 动作：function hook_clone(soname) 用 Interceptor.attach clone
- 观察：识别 libjust.so
- nop_64(base+0x119F8) CRC 校验 → 函数 nop_64 用 Arm64Writer putRet() → 假设：CRC 校验可跳过
- Il2CppDumper dump global-metadata.dat → 假设：metadata 是 il2cpp 元数据 → 动作：启动 Il2CppDumper 选 metadata 生成 dump.cs
- dec_global_metadata 函数 XOR 解密 (src[2*v2+0x202] ^ src[2*(v9%v2)+0x202]) → 假设：XOR 链式解密
- 观察：得完整字符串表 + Il2CppDumper 信息 → flag
failed_attempts:
- 试图静态反汇编 libjust.so → 失败：il2cpp 必须 Il2CppDumper 还原函数名
- Frida 直接 attach 入口 → 失败：CRC 校验在 init 早执行
- XOR 用单 key stream → 失败：链式 XOR 涉及 v9%v2 索引
key_observations:
- Unity il2cpp 游戏 Mobile 逆向：Frida hook clone 监控子线程栈地址识别目标 so
- NOP 关键地址过 CRC 校验 = Arm64Writer.putRet() 写 RET 指令
- global-metadata.dat 需 Il2CppDumper 解，生成函数列表
- dec_global_metadata 用 XOR 链式解 v9%v2
- Mobile 逆向 base+offset 是 il2cpp 标准定位
prerequisites:
- Frida 动态 hook 与 NativeFunction 调用
- Arm64 指令 (putRet, nop_64) 写入
- Unity il2cpp 架构（global-metadata.dat + libil2cpp.so）
- Il2CppDumper 工具使用
---
# 强网拟态2025初赛 Mobile方向just Writeup

> 原文: https://www.ctfiot.com/275655.html
> ID: 275655


```
function nop_64(addr) {
    Memory.protect(addr, 4 , 'rwx');
    var w = new Arm64Writer(addr);
    w.putRet();
    w.flush();
    w.dispose();
}

function hook_clone(soname)
{
    var clone = Module.findExportByName('libc.so', 'clone');
    Interceptor.attach(clone, {
        onEnter: function(args) {
            // args[3] 子线程的栈地址。如果这个值为 0，可能意味着没有指定栈地址
            if(args[3] != 0){
                var addr = args[3].add(96).readPointer()
                var so_name = Process.findModuleByAddress(addr).name;
                var so_base = Module.getBaseAddress(so_name);
                var offset = (addr - so_base);
                //console.log("===============>", so_name, addr,offset, offset.toString(16));
                if(so_name.indexOf(soname) >= 0) {
                    //console.log("nop ===============>", so_name, addr,offset, offset.toString(16));
                    nop_64(addr)
                    main()
                }
                
            }
        },
        onLeave: function(retval) {
            
        }
    });
     
}

function main()
{
    var base =  Module.findBaseAddress("libjust.so")
    //获取目标进程的基地址
    //console.log("inject success!!!")
    //console.log("base:",base)
    if(base){
        nop_64(base.add(0x119F8))  //crc check
        //nop_64(base.add(0x123E4))
       
    }
}

setImmediate(hook_clone, "libjust.so")

//frida -U -f "com.DefaultCompany.just" -l hook_clone.js
    #include 
    #include <fstream>
    #include <vector>
    #include <cstdint>
    #include <Windows.h>

usingnamespacestd;

char* __fastcall dec_global_metadata(unsigned __int16* src, __int64 a2)
{
    __int64 v2; // x21
    __int64 v4; // x8
    __int64 i_2; // x22
    char* dest; // x19
    __int64 i; // x8
    __int64 i_1; // x13
    __int64 v9; // x12

    v2 = src[0x200];
    v4 = a2 - 4 * v2;
    i_2 = v4 - 0x404;
    dest = (char*)malloc(v4 - 4);
    memcpy(dest, src, 0x400u);
    if (i_2 >= 1)
    {
        for (i = 0; i < i_2; i += 4)
        {
            i_1 = i + 3;
            v9 = i + i / v2;
            if (i >= 0)
                i_1 = i;
            *(DWORD*)&dest[(i_1 & 0xFFFFFFFFFFFFFFFCLL) + 0x400] = *(DWORD*)((char*)&src[2 * v2 + 0x202]
                + (i_1 & 0xFFFFFFFFFFFFFFFCLL))
                ^ *(DWORD*)&src[2 * (v9 % v2) + 0x202];
        }
    }
    return dest;
}
int main()
{
    string inputFilePath = "D:\CTF\qwnt_2025\Mobile\just\Il2CppDumper-win-v6.7.46\input\global-metadata.dat";

    // 2. Open the file in binary mode
    ifstream inputFile(inputFilePath, ios::
binary | ios::
ate);
    if (!inputFile.is_open())
    {
        cerr << "Error: Could not open file " << inputFilePath << endl;
        return1;
    }

    // 3. Get the size of the file
    streamsize fileSize = inputFile.tellg();
    inputFile.seekg(0, ios::
beg);

    // 4. Read the file into a buffer (using std::
vector for automatic memory management)
    vector buffer(fileSize / sizeof(unsigned __int16));
    if (!inputFile.read(reinterpret_cast<char*>(buffer.data()), fileSize))
    {
        cerr << "Error: Could not read file " << inputFilePath << endl;
        inputFile.close();
        return1;
    }

    inputFile.close();

    // 5. Call the decryption function

    char* decryptedData = dec_global_metadata(buffer.data(), fileSize);

    if (decryptedData)
    {
        // 6. Ask the user for an output file path and save the decrypted data
        string outputFilePath = "D:\CTF\qwnt_2025\Mobile\just\Il2CppDumper-win-v6.7.46\input\global-metadata.dat.dec";

        ofstream outputFile(outputFilePath, ios::
binary);
        if (!outputFile.is_open())
        {
            cerr << "Error: Could not create output file " << outputFilePath << endl;
            free(decryptedData); // Free the memory allocated by the decryption function
            return1;
        }

        // The size of the decrypted data is determined by the logic inside dec_global_metadata
        // v4 = a2 - 4 * v2; dest = (char*)malloc(v4 - 4);
        // We need to calculate this size to write the correct amount of data.
        unsigned __int16 v2 = buffer[0x200];
        __int64 decryptedSize = fileSize - 4 * v2 - 4;

        outputFile.write(decryptedData, decryptedSize);
        outputFile.close();

        cout << "File decrypted successfully and saved to " << outputFilePath << endl;

        // 7. Clean up the memory allocated by dec_global_metadata
        free(decryptedData);
    }
    else
    {
        cerr << "Error: Decryption failed." << endl;
    }

    return0;
}
function hook_il2cpp()
{
    var il2cpp_base =  Module.findBaseAddress("libil2cpp.so")
    if(il2cpp_base){
        console.log("il2cpp_base:",il2cpp_base)

        //hook tea
        Interceptor.attach(il2cpp_base.add(0x41C330), {

            onEnter: function(args) {
                console.log("entering TeaEncrypt", args[0], args[1])
            },
            onLeave: function(retval){
                console.log("leaving TeaEncrypt")
            }

        });

        //hook to uint32_t
        Interceptor.attach(il2cpp_base.add(0x1B5D88), {

            onEnter: function(args) {

            },
            onLeave: function(retval){
                console.log("uint32_t => ", retval)
            }

        });

        //hook ToUInt32LE
        Interceptor.attach(il2cpp_base.add(0x41B8B8), {

            onEnter: function(args) {

            },
            onLeave: function(retval){
                console.log("ToUInt32LE => ", retval)
            }

        });

        //hook cipher
        Interceptor.attach(il2cpp_base.add(0x1B6048), {

            onEnter: function(args) {
                var ReallyCompare_addr = args[0];
                console.log(hexdump(ReallyCompare_addr, {
                    offset: 0,
                    length: 256,
                    header: true,
                    ansi: true,
                }));
            },
            onLeave: function(retval){
                //console.log("uint32_t => ", retval)
            }

        });
    }
}

//frida -U -f "com.DefaultCompany.just" -l hook_clone.js
    #include <stdio.h>
    #include <stdint.h>

//加密函数
void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;     //v0,v1分别为字符串的低字节高字节     
    uint32_t delta=0x61C88647;                    
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; 
    for (i=0; i < 16; i++) {            
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        sum -= delta;
    }                                             
    v[0]=v0; v[1]=v1;
}

//解密函数
void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], i;  
    uint32_t delta=0x61C88647;   
    uint32_t sum = (-16)*delta;                  
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];  
    for (i=0; i<16; i++) {            
                sum += delta;            //解密时将加密算法的顺序倒过来，还有+=变为-=
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        
    }                                              
    v[0]=v0; v[1]=v1;
}

//密文 
unsignedchar cipher[]= {
    0xaf, 0x58, 0x64, 0x40, 0x9d, 0xb9, 0x21, 0x67,
    0xae, 0xb5, 0x29, 0x04, 0x9e, 0x86, 0xc5, 0x43,
    0x23, 0x0f, 0xbf, 0xa6, 0xb2, 0xae, 0x4a, 0xb5,
    0xc5, 0x69, 0xb7, 0xa8, 0x03, 0xd1, 0xae, 0xcf,
    0xc6, 0x2c, 0x5b, 0x7f, 0xa2, 0x86, 0x1e, 0x1a,
};

unsignedchar input[]="flag{uniABCDEFGHIJKLMNOPQRSTUVWXYZabcdef";

int main()
{
        //flag{D0_you_l1ke_th3_m4gic_uN1c0rn_with_A4rch64}
        
        unsignedchar a;
    uint32_t *v = (uint32_t*)input;
        unsignedchar *p = (unsignedchar*)v;
    uint32_t k[4]={0x12345678, 0x09101112, 0x13141516, 0x15161718};
    
    
    encrypt(v, k);
    for(int l = 8; l < 40; l+=8) {
        encrypt(v, k);
        
        p = (unsignedchar*)(input + l);
        for(int i = 0; i < 8; i++) {
                p[i] ^= input[i];
                }
        //printf("%x %x n", v[0], v[1]);
        }
        for(int i=0;i<40;i++)
    {
            printf("%x ", input[i]);
    } 
    printf("n"); 
        
         
        v = (uint32_t*)cipher;
        

        for(int l = 32; l >=8; l-=8) {
        p = (unsignedchar*)(cipher + l);
        for(int i = 0; i < 8; i++) {
                p[i] ^= cipher[i];
                }
                
        decrypt(v, k);
        }
        decrypt(v, k);
    
    for(int i=0;i<40;i++)
    {
            printf("%c", cipher[i]);
    } 
    
    return0;
}
//flag{unitygame_I5S0ooFunny_Isnotit?????}
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