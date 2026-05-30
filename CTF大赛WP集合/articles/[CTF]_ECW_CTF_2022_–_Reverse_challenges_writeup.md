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
```



```
typedef struct _FLT_OPERATION_REGISTRATION {
 UCHAR MajorFunction;
 FLT_OPERATION_REGISTRATION_FLAGS Flags;
 PFLT_PRE_OPERATION_CALLBACK PreOperation;
 PFLT_POST_OPERATION_CALLBACK PostOperation;
 PVOID Reserved1;
} FLT_OPERATION_REGISTRATION, *PFLT_OPERATION_REGISTRATION;
```



```
typedef FLT_PREOP_CALLBACK_STATUS
 (FLTAPI *PFLT_PRE_OPERATION_CALLBACK)(
 PFLT_CALLBACK_DATA Data,
 PCFLT_RELATED_OBJECTS FltObjects,
 PVOID *CompletionContext);
```



```
void encrypt(char *buf, uint32_t lenght, uint32_t value)
{
	uint32_t i;
 
 for (i = 0; i < lenght; i++)
 {
 *(buf + i) ^= value ^ rand_bytes[i % 4];
 }
 
	return;
}
```



```
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
```



```
typedef struct _EFI_DECOMPRESS_PROTOCOL {
	EFI_DECOMPRESS_GET_INFO GetInfo;
	EFI_DECOMPRESS_DECOMPRESS Decompress;
} EFI_DECOMPRESS_PROTOCOL;
```



```
cipher = "x0cV$2ekF2Qizv6^oyq^pUHKUgFj1Jd__V4LKW45H3R3__QvN3@sMwGeWw0VKBYFzRbviq6u#7RA9ArnM8XDIEEvHQ&HGT@Sv&LUZdb4BF6%2_4dci33595^VZQeoji^z^ucPVhc#&cT6#NH0^97O$7WqofM3pHpyMsY4WeTtS&eeNwq466kV6__GHG7e&S&ReuO353pv^UppLd5*$5!TD__nipgduZdxzv#oDWd&DFNzVWAmO_7jEH38DGb%dkAA?SwABE[>up/[_,`/[nqh/vy4PrhsulP%wMNpg&4cRY7S8x^!Veptn9kK__P8D3j41V%qktB7i_L&ViJdr1%#P&Dhy4C3H"
cipher = cipher.encode("utf-16")[2:]

flag = ""
for off in range(0x200, 0x200 + (2 * 24), 2):
	flag += chr(cipher[off] + 4)

print("Flag :", flag)
```



```
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
#include <unistd.h>
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
```



```
void glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const void * data)
{
 void (*func)(GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, const void *);
 func = dlsym(RTLD_NEXT, "glTexImage2D");
 func(target, level, internalformat, width, height, border, format, type, data);
 printf("[glTexImage2D] width : %d, height : %d, format : 0x%x, type : 0x%x, data content : %s\n", width, height, format, type, (char *)data);
 return;
}
```



```
[glTexImage2D] width : 164, height : 1, format : 0x1903, type : 0x1401, data content : <izmlvpq?,,/?|pmzs~fpjk7sp|~kvpq?"?/6?pjk?ysp~k?pI~sjz$ipv{?r~vq76d????pI~sjz?"?ysp~k77jvqk7xs@Ym~x\ppm{1g6?5?jvqk7/gY..(6?4?jvqk7/g^,'/66?:?-*)J6?0?-**1$b
```



```
#version 330 core

layout(location = 0) out float oValue;

uniform uint AN225;

void main()
{
 oValue = float(AN225 % 256U) / 255.;
}
```



```
for i in {000..999};do echo -ne "$i " ; ./HotShotGL ECW\{"$i"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\};done
```



```
#version 330 core

layout(location = 0) out float oValue;

void main(){
 oValue = float((uint(gl_FragCoord.x) * uint(0xF117) + uint(0xA380)) % 256U) / 255.;
}
```



```
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
```



```
#version 330 core

layout(location = 0) out float oValue;

uniform int X15[63];

void main()
{
 int jet = int(gl_FragCoord.x) + 13;
 oValue = float(X15[jet]) / 255.;
}
```



```
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
```



```
for (int i = 0; i < sizeof(flag); i++)
{
 X15[i + 13] ^= flag[i];
}
```



```
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
```



```
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
