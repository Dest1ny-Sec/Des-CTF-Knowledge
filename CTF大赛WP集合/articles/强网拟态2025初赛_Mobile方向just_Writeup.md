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
```



```
#include <iostream>
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
    ifstream inputFile(inputFilePath, ios::binary | ios::ate);
    if (!inputFile.is_open())
    {
        cerr << "Error: Could not open file " << inputFilePath << endl;
        return1;
    }

    // 3. Get the size of the file
    streamsize fileSize = inputFile.tellg();
    inputFile.seekg(0, ios::beg);

    // 4. Read the file into a buffer (using std::vector for automatic memory management)
    vector<unsigned __int16> buffer(fileSize / sizeof(unsigned __int16));
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

        ofstream outputFile(outputFilePath, ios::binary);
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
```



```
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
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707506-wxsync-2025-10-63db80d193db2f6f917929c6c36386fa.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707508-wxsync-2025-10-36784332b6e98a1dda25dc4033b36328.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707510-wxsync-2025-10-6ecfc805a7d2e902387a96c0b7ebddd1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707511-wxsync-2025-10-ee25caa062f8740224757db696d083a0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707513-wxsync-2025-10-2770c3d08d90f00718d600838c013dd1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707515-wxsync-2025-10-894f8cf5967c2c182966c9dfdbed48ca.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707517-wxsync-2025-10-d28c6eee49a8253edb813bcd6e91c779.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707519-wxsync-2025-10-feb36a568fa280acb231d9378da4e518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707521-wxsync-2025-10-93860090c1be47c86eb9270b8eed9f62.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707523-wxsync-2025-10-deb167d0d2b1887485cdbc95a3b239b5.png)