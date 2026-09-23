---
title: '[CTF] ECW CTF 2022 – Reverse challenges writeup'
contest: ECW CTF 2022
year: 2022
difficulty: hard
vuln_type: esoteric
tags:
- minifilter_driver
- flt_registration
- xor_rand_bytes_encrypt
- efi_decompress_protocol
- opengl_ld_preload_hook
- glsl_330_core
- gl_fragcoord_uniform
- glteximage2d_data_extract
- ctf_re_3chals
attack_chain: '1) Minifilter 驱动 FLT_REGISTRATION 结构 + encrypt(buf, len, value) ^ rand_bytes[i%4] + file.txt.lock → key=[\xff,\xfe,E,0] + off+value 1+2+... 累加 XOR → utf-16 输出 flag / 2) EFI Decompress Protocol + cipher utf-16 切片 + off 0x200+2*24 chr(cipher[off]+4) / 3) HotShotGL OpenGL hook.so LD_PRELOAD + glCreateShader + glTexImage2D data 提取 + #version 330 core + gl_FragCoord.x*0xF117+0xA380 % 256 + uniform AN225 / uniform int X15[63] + gl_FragCoord.x+13 + ~(a^b) 还原 flag'
key_payload: key = [data[0] ^ 1 ^ 0xff, data[1] ^ 1 ^ 0xfe, data[2] ^ 1 ^ 0x45, data[3] ^ 1 ^ 0] / cipher = "x0cV$2ekF2Q..." 切片 [0x200:0x200+2*24] / glTexImage2D width=164 height=1 data <izmlvpq...> / flag[i] = ~((i*0xF117+0xA380)%256 ^ X15[i+13])
one_liner: ECW CTF 2022 三道逆向：Minifilter 驱动文件加密 + EFI Decompress Protocol UTF-16 + OpenGL hook.so LD_PRELOAD 提取 GLSL Fragment Shader uniform 计算。
lesson: OpenGL hook LD_PRELOAD glTexImage2D 是提取 Fragment Shader 输入的经典方法；Minifilter 驱动用 FLT_REGISTRATION 结构定位 PreOperation 回调是 Win 驱动逆向起点。
quality: high
full_path: '[CTF]_ECW_CTF_2022_–_Reverse_challenges_writeup.full.md'
meta_path: '[CTF]_ECW_CTF_2022_–_Reverse_challenges_writeup.meta.md'
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '[CTF] ECW CTF 2022 – Reverse challenges writeup。ECW CTF 2022 三道逆向：Minifilter 驱动文件加密 + EFI Decompress Protocol UTF-16 + OpenGL hook.so LD_PRELOAD 提取 GLSL Fragment Shader uniform 计算。。经验：OpenGL hook L...'
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/60146.html
reasoning_chain:
- 触发点:第一题是 Minifilter 驱动 .sys → 假设:有 FLT_REGISTRATION 结构 + PreOperation 回调 → 动作:IDA 静态分析 DriverEntry
- 观察:encrypt(buf, len, value) ^ rand_bytes[i%4] + 写入 file.txt.lock → 假设:key=[0xff,0xfe,E,0] 可爆破
- 动作:data[0] ^ 1 ^ 0xff, data[1] ^ 1 ^ 0xfe, data[2] ^ 1 ^ 0x45, data[3] ^ 1 ^ 0 → 观察:还原 key
- 动作:off+value 1+2+... 累加 XOR → utf-16 输出 flag → 完成第一题
- 触发点:第二题 EFI Decompress Protocol → 假设:cipher utf-16 切片 → 动作:off 0x200+2*24 chr(cipher[off]+4)
- 观察:还原 flag 第二题
- 触发点:第三题 HotShotGL OpenGL hook.so LD_PRELOAD → 假设:glTexImage2D data 可提取 → 动作:hook.so LD_PRELOAD
- 动作:hook glCreateShader + glTexImage2D → 观察:width=164 height=1 data=<izmlvpq...> → 假设:fragment shader 计算 flag
- 动作:flag[i] = ~((i*0xF117+0xA380)%256 ^ X15[i+13]) → 观察:还原 flag → 完成
failed_attempts:
- 试图直接 IDA F5 Minifilter → 失败:驱动代码需先看 FLT_REGISTRATION 结构
- 试图不解 EFI Decompress → 失败:off+value 累加 XOR 必走
- 试图不解 OpenGL hook → 失败:fragment shader uniform X15 必须 hook glTexImage2D 取
key_observations:
- OpenGL hook LD_PRELOAD glTexImage2D 是提取 Fragment Shader 输入的经典方法
- Minifilter 驱动用 FLT_REGISTRATION 结构定位 PreOperation 回调是 Win 驱动逆向起点
- EFI Decompress Protocol + cipher utf-16 切片是 UEFI 逆向通用思路
- fragment shader 计算公式 flag[i] = ~((i*0xF117+0xA380)%256 ^ X15[i+13]) 是固定套路
- GL_PRELOAD hook 比 Frida hook OpenGL 更轻量,适合 CTF 时限
prerequisites:
- Windows Minifilter 驱动开发基础 (FLT_REGISTRATION / PreOperation)
- UEFI / EFI Decompress Protocol 协议基础
- OpenGL hook.so LD_PRELOAD + GLSL Fragment Shader
- IDA 驱动逆向 (PDB 符号 / DriverEntry)
---
# [CTF] ECW CTF 2022 – Reverse challenges writeup

> 原文: https://www.ctfiot.com/60146.html
> ID: 60146


```
typedef struct _FLT_REGISTRATION {
 USHORT Size;
 USHORT Version;
 FLT_REGISTRATION_FLAGS Flags;
 const FLT_CONTEXT_REGISTRATION *ContextRegistration;
 const FLT_OPERATION_REGISTRATION *OperationRegistration;
 PFLT_FILTER_UNLOAD_CALLBACK FilterUnloadCallback;
 PFLT_INSTANCE_SETUP_CALLBACK InstanceSetupCallback;
 PFLT_INSTANCE_QUERY_TEARDOWN_CALLBACK InstanceQueryTeardownCallback;
 PFLT_INSTANCE_TEARDOWN_CALLBACK InstanceTeardownStartCallback;
 PFLT_INSTANCE_TEARDOWN_CALLBACK InstanceTeardownCompleteCallback;
 PFLT_GENERATE_FILE_NAME GenerateFileNameCallback;
 PFLT_NORMALIZE_NAME_COMPONENT NormalizeNameComponentCallback;
 PFLT_NORMALIZE_CONTEXT_CLEANUP NormalizeContextCleanupCallback;
 PFLT_TRANSACTION_NOTIFICATION_CALLBACK TransactionNotificationCallback;
 PFLT_NORMALIZE_NAME_COMPONENT_EX NormalizeNameComponentExCallback;
 PFLT_SECTION_CONFLICT_NOTIFICATION_CALLBACK SectionNotificationCallback;
} FLT_REGISTRATION, *PFLT_REGISTRATION;
typedef struct _FLT_OPERATION_REGISTRATION {
 UCHAR MajorFunction;
 FLT_OPERATION_REGISTRATION_FLAGS Flags;
 PFLT_PRE_OPERATION_CALLBACK PreOperation;
 PFLT_POST_OPERATION_CALLBACK PostOperation;
 PVOID Reserved1;
} FLT_OPERATION_REGISTRATION, *PFLT_OPERATION_REGISTRATION;
typedef FLT_PREOP_CALLBACK_STATUS
 (FLTAPI *PFLT_PRE_OPERATION_CALLBACK)(
 PFLT_CALLBACK_DATA Data,
 PCFLT_RELATED_OBJECTS FltObjects,
 PVOID *CompletionContext);
void encrypt(char *buf, uint32_t lenght, uint32_t value)
{
	uint32_t i;

 for (i = 0; i < lenght; i++)
 {
 *(buf + i) ^= value ^ rand_bytes[i % 4];
 }

	return;
}
#!/usr/bin/python3

with open("file.txt.lock", "rb") as file:
 data = file.read()
 file.close()

key = [
 data[0] ^ 1 ^ 0xff,	# \xff
 data[1] ^ 1 ^ 0xfe,	# \xfe
 data[2] ^ 1 ^ 0x45,	# E
 data[3] ^ 1 ^ 0x0 # \0
 ]

off, value = 0, 1
lock = False

flag = b""

while (lock == False):
 for idx in range(0x7):
 flag += bytes([data[off] ^ value ^ key[idx % 4]])
 off += 1
 if off == len(data):
 lock = True
 break
 value += 1

print(flag[2:].decode('utf-16'))
typedef struct _EFI_DECOMPRESS_PROTOCOL {
	EFI_DECOMPRESS_GET_INFO GetInfo;
	EFI_DECOMPRESS_DECOMPRESS Decompress;
} EFI_DECOMPRESS_PROTOCOL;
cipher = "x0cV$2ekF2Qizv6^oyq^pUHKUgFj1Jd__V4LKW45H3R3__QvN3@sMwGeWw0VKBYFzRbviq6u#7RA9ArnM8XDIEEvHQ&HGT@Sv&LUZdb4BF6%2_4dci33595^VZQeoji^z^ucPVhc#&cT6#NH0^97O$7WqofM3pHpyMsY4WeTtS&eeNwq466kV6__GHG7e&S&ReuO353pv^UppLd5*$5!TD__nipgduZdxzv#oDWd&DFNzVWAmO_7jEH38DGb%dkAA?SwABE[>up/[_,`/[nqh/vy4PrhsulP%wMNpg&4cRY7S8x^!Veptn9kK__P8D3j41V%qktB7i_L&ViJdr1%#P&Dhy4C3H"
cipher = cipher.encode("utf-16")[2:]

flag = ""
for off in range(0x200, 0x200 + (2 * 24), 2):
	flag += chr(cipher[off] + 4)

print("Flag :", flag)
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdint.h>
    #include <dlfcn.h>
    #include <stdlib.h>
    #include <X11/X.h>
    #include <X11/Xlib.h>
    #include <GL/gl.h>
    #include <GL/glx.h>
    #include <GL/glu.h>
    #include 
    #include <string.h>

// gcc -fPIC -shared hook.c -o hook.so

GLuint glCreateShader(GLenum shaderType)
{
 GLuint (*func)(GLenum);
 func = dlsym(RTLD_NEXT, "glCreateShader");
 printf("[glCreateShader] shader type : 0x%x\n", shaderType);
 return func(shaderType);
}

void (*glXGetProcAddress(const GLubyte *procName))(void)
{
 void * (*func)(const GLubyte *);
 func = dlsym(RTLD_NEXT, "glXGetProcAddress");

 if (!strcmp(procName, "glCreateShader"))
 {
 return glCreateShader;
 }

 return func(procName);
}
void glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const void * data)
{
 void (*func)(GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, const void *);
 func = dlsym(RTLD_NEXT, "glTexImage2D");
 func(target, level, internalformat, width, height, border, format, type, data);
 printf("[glTexImage2D] width : %d, height : %d, format : 0x%x, type : 0x%x, data content : %s\n", width, height, format, type, (char *)data);
 return;
}
[glTexImage2D] width : 164, height : 1, format : 0x1903, type : 0x1401, data content : <izmlvpq?,,/?|pmzs~fpjk7sp|~kvpq?"?/6?pjk?ysp~k?pI~sjz$ipv{?r~vq76d????pI~sjz?"?ysp~k77jvqk7xs@Ym~x\ppm{1g6?5?jvqk7/gY..(6?4?jvqk7/g^,'/66?:?-*)J6?0?-**1$b
    #version 330 core

layout(location = 0) out float oValue;

uniform uint AN225;

void main()
{
 oValue = float(AN225 % 256U) / 255.;
}
for i in {000..999};do echo -ne "$i " ; ./HotShotGL ECW\{"$i"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\};done
    #version 330 core

layout(location = 0) out float oValue;

void main(){
 oValue = float((uint(gl_FragCoord.x) * uint(0xF117) + uint(0xA380)) % 256U) / 255.;
}
int main(void)
{
 uint8_t a, b;
 unsigned char flag[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";

 for (int i = 0; i < sizeof(flag); i++)
 {
 a = (i * 0xF117 + 0xA380) % 256;
 b = flag[i];
 flag[i] = ~(a ^ b);
 printf("flag[%d] : 0x%x\n", i, flag[i]);
 }
}
    #version 330 core

layout(location = 0) out float oValue;

uniform int X15[63];

void main()
{
 int jet = int(gl_FragCoord.x) + 13;
 oValue = float(X15[jet]) / 255.;
}
int X15[63] = {
 0x32, 0x43, 0x58, 0x97, 0xf3, 0x31, 0x87, 0x32,
 0xa4, 0xbe, 0xfa, 0x01, 0xaa, 0x28, 0x0d, 0x3d,
 0x59, 0x4c, 0x61, 0x90, 0x81, 0xa8, 0xde, 0xc6,
 0xc0, 0x04, 0x35, 0x4f, 0x42, 0x23, 0xa7, 0xb5,
 0xa2, 0xda, 0xef, 0xda, 0x07, 0x24, 0x1f, 0x70,
 0x7d, 0x8e, 0x96, 0x92, 0xf5, 0xfe, 0xf8, 0x05,
 0x3b, 0x2a, 0x42, 0x4a, 0xad, 0x97, 0xb5, 0xd8,
 0xc9, 0xe2, 0x1a, 0x3a, 0x19, 0x14, 0x31
};
for (int i = 0; i < sizeof(flag); i++)
{
 X15[i + 13] ^= flag[i];
}
    #version 330 core

layout(location = 0) out float oValue;

uniform sampler2D Input;

void main()
{
 ivec2 p = 2 * ivec2(gl_FragCoord.xy);
 oValue = texelFetch(Input, p, 0).r;

 if((p.x + 1) < textureSize(Input, 0).x) {
 oValue += texelFetch(Input, p + ivec2(1, 0), 0).r;
 }
}
void main(void)
{
 uint8_t a, b;
 int X15[63] = {
 0x32, 0x43, 0x58, 0x97, 0xf3, 0x31, 0x87, 0x32,
 0xa4, 0xbe, 0xfa, 0x01, 0xaa, 0x28, 0x0d, 0x3d,
 0x59, 0x4c, 0x61, 0x90, 0x81, 0xa8, 0xde, 0xc6,
 0xc0, 0x04, 0x35, 0x4f, 0x42, 0x23, 0xa7, 0xb5,
 0xa2, 0xda, 0xef, 0xda, 0x07, 0x24, 0x1f, 0x70,
 0x7d, 0x8e, 0x96, 0x92, 0xf5, 0xfe, 0xf8, 0x05,
 0x3b, 0x2a, 0x42, 0x4a, 0xad, 0x97, 0xb5, 0xd8,
 0xc9, 0xe2, 0x1a, 0x3a, 0x19, 0x14, 0x31
 };

 unsigned char flag[50] = {0};

 for (int i = 0; i < sizeof(flag); i++)
 {
 a = (i * 0xF117 + 0xA380) % 256;
 b = X15[i + 13];
 flag[i] = ~(a ^ b);
 }

 printf("flag : %s\n", flag);
}
```
