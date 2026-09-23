---
title: H&NCTF RE 部分题解
contest: H&NCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags:
- rev
- enigma-virtual-box
- anti-vm
- anti-av
- shellcode-injection
- kernel32-hash
- ldr-list
attack_chain:
- enigma virtual box 打包exe+多个dll
- 'main函数: 在C盘用户视频目录创建副本svchsst.exe'
- '副本启动: 删除txt+原文件+继续执行'
- '实体机跑: v48=16 走主逻辑'
- 检测VMware tools/VirtualBox Guest Additions
- 进程快照遍历LDR双向链表
- kernel32名字hash比对
- '杀软检测: Process Snapshot遍历'
- sub_140001320 shellcode自解密+注入exp10rer.exe
- shellcode自修改XOR+位运算
key_payload: sub_140001320 解密shellcode → 注入 exp10rer.exe
one_liner: H&NCTF RWhackA：Enigma打包+反VM+反杀软+shellcode注入
lesson: Enigma Virtual Box打包需用动态调试+反VM检测绕过
quality: high
full_path: H&NCTF_RE_部分题解.full.md
meta_path: H&NCTF_RE_部分题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'H&NCTF RE 部分题解。H&NCTF RWhackA：Enigma打包+反VM+反杀软+shellcode注入。关键路径：enigma virtual box 打包exe+多个dll → main函数: 在C盘用户视频目录创建副本svchsst.exe → 副本启动: 删除txt+原文件+继续执行。经验：Enigma Virtual Box打包需用动态调试+反VM检测绕过'
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/183150.html
reasoning_chain:
- RWhackA 题静态分析发现 enigma virtual box 打包 → 触发点：exe+dll 一体打包
- 动作：用解包工具尝试解包 → 观察：解包失败 → 假设：必须动态调试硬分析
- main 函数初始地址下断点 → 观察：函数名恢复 → 假设：mydll1.dll 被一起打包
- 副本启动逻辑：在 C 盘用户视频目录创建 svchsst.exe 并启动 → 假设：副本做恶意操作
- 虚拟机跑 → 观察：v48 < 5 → 假设：system_info 结构体 v48 受 VM 配置影响
- 动作：实体机跑 → 观察：v48=16 → 假设：实体机 v48 进入主逻辑
- 检测 VMWare tools / VirtualBox Guest Additions 进程 → 触发点：6 进程枚举检测
- LDR 双向链表遍历 + kernel32 hash 比对 → 假设：模块名 hash 检测
- 杀软检测：Process Snapshot 遍历杀软进程 → 触发点：sub_140001320 shellcode 自修改
- 动作：shellcode XOR+位运算自解密 → 观察：注入 exp10rer.exe 完成 flag 输出
failed_attempts:
- 试图用解包工具静态解 enigma 打包 → 失败：解包工具不兼容
- 在虚拟机内调试 → 失败：v48 一直 < 5 不进 flag 路径
- 静态分析定位 flag 字符串 → 失败：flag 藏在 shellcode 内
key_observations:
- Enigma Virtual Box 打包必须动态调试硬分析
- system_info 结构体差异可识别 VM/实体机
- LDR 双向链表 + 模块名 hash 是反调试经典手法
- Process Snapshot 遍历是反杀软常见方案
- shellcode 自修改 XOR + 注入是 malware 标志
prerequisites:
- Enigma Virtual Box 打包原理
- Windows LDR 链表结构
- PE 注入与 shellcode 编写
- VMX/anti-VM 检测绕过
---
# H&NCTF RE 部分题解

> 原文: https://www.ctfiot.com/183150.html
> ID: 183150

一

RWhackA

本质上就是一个恶意程序，运行时在别的进程注入shellcode，flag就藏在shellcode里面。

首先用分析工具发现存在enigma virtual box，相当于把多个可执行文件或者链接库给一块打包了，用解包工具尝试解包发现失败，那就只能先硬着分析。

静态分析发现有很多內存访问异常点，均出自函数调用上，可能是程序重定位时产生的错误，没办法只能动态调试了。

在main函数的初始地址处下断点，发现函数名正常恢复了：

题目附件里没有给出mydll1.dll文件，侧面也验证了这个链接库被一起打包进了这个exe里面。

这个函数的逻辑就是在c盘的用户目录下的视频文件夹中创建了一个和源程序一模一样的副本并启动它，具体的逻辑如下：

◆原程序打开txt文件失败，复制其本身到视频文件夹下的svchsst.exe副本中，并启动它，完成后将自身路径写入txt文件中并结束自身运行。

◆副本启动后检测到了txt文件，删除掉了txt文件和原文件，并继续后面的执行过程。

一开始我在虚拟机里面跑这个程序，发现调用完后v5一直小于5，这里面v47存储的是system_info结构体的内容，我怀疑v48和虚拟机配置有关，因为sub_140001070函数就是结束函数了（后面会分析），并没有flag的逻辑，最后考虑在实体机里面跑一下，发现实体机里面v48的值等于16。

这部分代码就是在枚举当前计算机运行的进程，看有没有上面6个进程存在，有的话就进入结束函数，这部分功能实际上就是在检测VMWare tools和virtualbox Guests Additions的运行情况，如果在运行该进程就会退出。

程序加载的模块链表（LDR）本质上是一个双向链表，因此一直索引下一个结点一定会定位到链表头，这里的v17[6].Flink索引到的是模块名，每一个字符占两个字节，另外一个补0，如下图：

最后检测到的程序名的形式如上图，根据v22的值就是程序名生成的对应hash值的结果，最后可以确定是kernel32。

基本方式也是调用kernel32库里面的函数，检测杀毒软件的原理和检测虚拟机服务的原理一致，也是打进程快照然后再遍历。

主逻辑在sub_140001320函数中，基本思路是将shellcode自解密然后注入另外一个进程中。

这里待注入的进程名是exp10rer.exe，但是我看这个程序本身并没有启动过名为exp10rer.exe的进程，这个地方最开始以为自己哪个地方的代码分析出错了，只能先尝试分析一下shellcode本身。

v4 = &unk_140003450;
 v5 = 7i64;
 do
 {
 v3 += 32;
 v6 = *v4;
 v7 = v4[1];
 v4 += 8;
 *(v3 - 8) = v6;
 v8 = *(v4 - 6);
 *(v3 - 7) = v7;
 v9 = *(v4 - 5);
 *(v3 - 6) = v8;
 v10 = *(v4 - 4);
 *(v3 - 5) = v9;
 v11 = *(v4 - 3);
 *(v3 - 4) = v10;
 v12 = *(v4 - 2);
 *(v3 - 3) = v11;
 v13 = *(v4 - 1);
 *(v3 - 2) = v12;
 *(v3 - 1) = v13;
 --v5;
 }
 while ( v5 );
 v14 = *(v4 + 4);
 v15 = 6;
 v16 = -1162190778i64;
 v17 = 1i64;
 *v3 = *v4;
 v3[4] = v14;
 do
 {
 v18 = 227i64;
 v19 = &v45;
 v20 = 227;
 v21 = &v44;
 do
 {
 v22 = *v21;
 v21 -= 4;
 v19 -= 4;
 v23 = *(&v41 + (v20 + 1) % 0xBu);
 v24 = v17 ^ v18-- & 3;
 *(v19 + 1) -= ((v23 ^ v16) + (si128.m128i_i32[v24] ^ v22)) ^ (((v22 >> 6) ^ (4 * v23)) + ((16 * v22) ^ (v23 >> 3)));
 --v20;
 }
 while ( v20 );
 v25 = v42 ^ v16;
 v16 -= 1953785185i64;
 v41 -= (v25 + (si128.m128i_i32[v17] ^ v43)) ^ (((v43 >> 6) ^ (4 * v42)) + ((16 * v43) ^ (v42 >> 3)));
 v17 = (v16 >> 2) & 3;
 --v15;
 }
 while ( v15 );
 v26 = &v41;
 for ( i = 0; i < 0x393; ++i )
 sub_140001010("%c ", *v26++);

当程序执行到上面最后两行代码位置时即是打印最后生成好的shellcode，首先使用idapython去dump这段內存，然后需要手写一个加载器去模拟执行它。

对应加载器的代码如下(dump.bin是对应的shellcode)：

#include <windows.h>
#include <stdio.h>

// 从文件加载shellcode的函数声明
BOOL LoadShellcodeFromFile(const char* filename, PBYTE* shellcode, DWORD* size);

// shellcode执行函数声明
void ExecuteShellcode(PBYTE shellcode);

int main() {
 PBYTE shellcode;
 DWORD size;

 // 从文件加载shellcode
 if (!LoadShellcodeFromFile("dump.bin", &shellcode, &size)) {
 printf("Failed to load shellcode from file.n");
 return 1;
 }

 // 执行shellcode
 ExecuteShellcode(shellcode);

 // 清理资源
 VirtualFree(shellcode, 0, MEM_RELEASE);

 return 0;
}

// 从文件加载shellcode到内存的函数实现
BOOL LoadShellcodeFromFile(const char* filename, PBYTE* shellcode, DWORD* size) {
 HANDLE file;
 DWORD bytesRead;

 // 打开文件
 file = CreateFileA(filename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
 if (file == INVALID_HANDLE_VALUE) {
 return FALSE;
 }

 // 获取文件大小
 *size = GetFileSize(file, NULL);
 if (*size == INVALID_FILE_SIZE) {
 CloseHandle(file);
 return FALSE;
 }

 // 分配内存
 *shellcode = (PBYTE)VirtualAlloc(NULL, *size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
 if (*shellcode == NULL) {
 CloseHandle(file);
 return FALSE;
 }

 // 读取文件内容到内存
 if (!ReadFile(file, *shellcode, *size, &bytesRead, NULL) || bytesRead != *size) {
 VirtualFree(*shellcode, 0, MEM_RELEASE);
 CloseHandle(file);
 return FALSE;
 }

 // 关闭文件
 CloseHandle(file);

 return TRUE;
}

// 执行shellcode的函数实现
void ExecuteShellcode(PBYTE shellcode) {
 // 将shellcode地址转换为函数指针
 void (*func)() = (void(*)())shellcode;

 // 调用函数指针，执行shellcode
 func();
}

其实在shellcode末尾就能看到flag，但是还是想继续分析一下。

这段shellcode本身的逻辑就是不断更新r10寄存器的值，然后去各个模块中找对应的函数名算哈希，如果找到了某个函数的hash值和r10的值相等就调用对应的函数，在这期间shellcode还会设置好rcx,rdx,r8,r9等寄存器的值作为参数。

计算hash的汇编代码如下：

debug029:
000001C1E53B002D xor rax, rax
debug029:
000001C1E53B0030 lodsb
debug029:
000001C1E53B0031 cmp al, 61h ; 'a'
debug029:
000001C1E53B0033 jl short loc_1C1E53B0037
debug029:
000001C1E53B0035 sub al, 20h ; ' '
debug029:
000001C1E53B0037
debug029:
000001C1E53B0037 loc_1C1E53B0037: ; CODE XREF: sub_1C1E53B0000+33↑j
debug029:
000001C1E53B0037 ror r9d, 0Dh
debug029:
000001C1E53B003B add r9d, eax
debug029:
000001C1E53B003E loop loc_1C1E53B002D

主体逻辑就是小写变大写，其余不变，然后累计循环右移13位做加法，

下面给出每一次调用的函数名和作用：

加载wininet.dll

调用InternetOpenA函数

调用InternetConnectA，这个函数的参数包含了待连接的服务器ip或者域名，由第二次参数给出，而第二个参数rdx刚好指向shellcode的內存，我们去对应地址看看，则发现了flag。

二

ezshopping

安卓逆向，程序解包后没有lib库，考虑代码逻辑仅在java层

作者实现了一个类似于购买商品的客户端，要先注册账号，才能进一步去购买flag，但是好像没有充值或者赚钱的逻辑，也没有flag的标价。

浏览了一下shopactivity的逻辑，发现两处比较关键的代码。

private void verifyPurchase(final String str, final double d, final String str2) {
 Volley.newRequestQueue(this).add(new StringRequest(1, URL.purchaseURL, new Response.Listener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda2
 @Override // com.android.volley.Response.Listener
 public final void onResponse(Object obj) {
 shopActivity.this.m95lambda$verifyPurchase$0$comswddezshopingshopActivity((String) obj);
 }
 }, new Response.ErrorListener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda3
 @Override // com.android.volley.Response.ErrorListener
 public final void onErrorResponse(VolleyError volleyError) {
 shopActivity.this.m96lambda$verifyPurchase$2$comswddezshopingshopActivity(volleyError);
 }
 }) { // from class: com.swdd.ezshoping.shopActivity.1
 @Override // com.android.volley.Request
 protected Map<String, String> getParams() {
 HashMap hashMap = new HashMap();
 hashMap.put("username", str);
 hashMap.put("Money", String.format("%.2f", Double.valueOf(d)));
 hashMap.put("signature", str2);
 return hashMap;
 }
 });
 }

 /* JADX INFO: Access modifiers changed from: package-private */
 /* renamed from: lambda$verifyPurchase$2$com-swdd-ezshoping-shopActivity reason: not valid java name */
 public /* synthetic */ void m96lambda$verifyPurchase$2$comswddezshopingshopActivity(VolleyError volleyError) {
 if (volleyError.networkResponse != null) {
 switch (volleyError.networkResponse.statusCode) {
 case TypedValues.CycleType.TYPE_VISIBILITY /* 402 */:
 Toast.makeText(this, "Insufficient funds to complete the purchase.", 1).show();
 return;
 case TypedValues.CycleType.TYPE_ALPHA /* 403 */:
 AlertDialog.Builder builder = new AlertDialog.Builder(this);
 builder.setTitle("ERROR!");
 builder.setMessage("小伙子别想改我代码!");
 builder.setPositiveButton("OK", new DialogInterface.OnClickListener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda0
 @Override // android.content.DialogInterface.OnClickListener
 public final void onClick(DialogInterface dialogInterface, int i) {
 dialogInterface.dismiss();
 }
 });
 builder.show();
 return;
 case 404:
 Toast.makeText(this, "User not found.", 1).show();
 return;
 default:
 Toast.makeText(this, "An error occurred: " + volleyError.toString(), 1).show();
 return;
 }
 }
 Toast.makeText(this, "Network error, no response received.", 1).show();
 }

构造的数据包中有用户名，签名和钱，服务器响应中有钱款不够，代码被修改等字样，考虑到客户端有计算程序hash值的步骤，会在发送的数据包中体现，因此如果服务端比对程序hash值改变说明有人恶意修改了代码，会直接返回错误，这说明我们不能通过修改程序逻辑的方式增加钱款数量。

既然本地逻辑不能修改，那就修改客户端发送的数据包，先抓包获得发送钱款为0时的数据包为底板，再用python写脚本。

构造脚本如下：

import socket

# 指定服务器地址和端口
server_address = ('hnctf.imxbt.cn', 20528)

# 指定表单数据
form_data = {
 # 这里应该填入POST请求的具体数据
 "Money": "114514.00",
 "signature": "376c4fe518240bc513f67bf477d5d950d757d51bb58db594fa4551e248364413",
 "username": "" #填自己的用户名即可
}

# 将表单数据转换为application/x-www-form-urlencoded格式
form_data_encoded = "&".join("{}={}".format(key, val) for key, val in form_data.items())

# 准备HTTP请求头
http_request = """POST /purchase HTTP/1.1r
Host: hnctf.imxbt.cn:
20528r
If-None-Match: W/"12-hfcD7BKoo9fJ4GgYnq9Rj3aNpD8"r
Content-Type: application/x-www-form-urlencoded; charset=UTF-8r
User-Agent: Dalvik/2.1.0 (Linux; U; Android 9; PCRT00 Build/PQ3A.190605.01231654)r
Connection: Keep-Aliver
Accept-Encoding: gzipr
Content-Length: {}r
r
""".format(len(form_data_encoded))

# 完整的HTTP请求数据
http_request += form_data_encoded

# 创建TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
sock.connect(server_address)

# 发送HTTP请求
sock.sendall(http_request.encode())

# 接收响应数据
response = sock.recv(4096)
print(response.decode())

# 关闭socket连接
sock.close()

发送过去后会有两种回显。

一个是Not enough money!!，另一个是Did you cheat with this much money?!，然后出题人给了钱款的上限，其实也可以专门对金额写一个二分，但是没必要，可以手动试出来，最后金额设定为114514.00时返回flag。

HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 61
ETag: W/"3d-lbjcXjt9Oql9sd2OEm6pVRILsSE"
Date: Thu, 16 May 2024 01:31:23 GMT
Connection: keep-alive
Keep-Alive: timeout=5

H&NCTF{Congratulati0ns!_3cad3260-0c7e-4d98-afbc-814cc5221fcc}

这题没有过多的钱款验证逻辑，其实还可以对username，money一起做一个hash，然后写入数据包，服务端可以采取相同的逻辑进行运算，然后对比hash结果，这样构造数据包时不能只修改钱款，也要还原正常哈希的逻辑补充hash值，会更像逆向题一些。

看雪ID：ccccl1180

https://bbs.kanxue.com/user-home-975140.htm

*本文为看雪论坛优秀文章，由 ccccl1180 原创，转载请注明来自看雪社区

# 往期推荐

1、Windows主机入侵检测与防御内核技术深入解析

2、BFS Ekoparty 2022 Linux Kernel Exploitation Challenge

3、银狐样本分析

4、使用pysqlcipher3操作Windows微信数据库

5、XYCTF两道Unity IL2CPP题的出题思路与题解

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
RWhackA
v4 = &unk_140003450;
 v5 = 7i64;
 do
 {
 v3 += 32;
 v6 = *v4;
 v7 = v4[1];
 v4 += 8;
 *(v3 - 8) = v6;
 v8 = *(v4 - 6);
 *(v3 - 7) = v7;
 v9 = *(v4 - 5);
 *(v3 - 6) = v8;
 v10 = *(v4 - 4);
 *(v3 - 5) = v9;
 v11 = *(v4 - 3);
 *(v3 - 4) = v10;
 v12 = *(v4 - 2);
 *(v3 - 3) = v11;
 v13 = *(v4 - 1);
 *(v3 - 2) = v12;
 *(v3 - 1) = v13;
 --v5;
 }
 while ( v5 );
 v14 = *(v4 + 4);
 v15 = 6;
 v16 = -1162190778i64;
 v17 = 1i64;
 *v3 = *v4;
 v3[4] = v14;
 do
 {
 v18 = 227i64;
 v19 = &v45;
 v20 = 227;
 v21 = &v44;
 do
 {
 v22 = *v21;
 v21 -= 4;
 v19 -= 4;
 v23 = *(&v41 + (v20 + 1) % 0xBu);
 v24 = v17 ^ v18-- & 3;
 *(v19 + 1) -= ((v23 ^ v16) + (si128.m128i_i32[v24] ^ v22)) ^ (((v22 >> 6) ^ (4 * v23)) + ((16 * v22) ^ (v23 >> 3)));
 --v20;
 }
 while ( v20 );
 v25 = v42 ^ v16;
 v16 -= 1953785185i64;
 v41 -= (v25 + (si128.m128i_i32[v17] ^ v43)) ^ (((v43 >> 6) ^ (4 * v42)) + ((16 * v43) ^ (v42 >> 3)));
 v17 = (v16 >> 2) & 3;
 --v15;
 }
 while ( v15 );
 v26 = &v41;
 for ( i = 0; i < 0x393; ++i )
 sub_140001010("%c ", *v26++);
    #include <windows.h>
    #include <stdio.h>

// 从文件加载shellcode的函数声明
BOOL LoadShellcodeFromFile(const char* filename, PBYTE* shellcode, DWORD* size);

// shellcode执行函数声明
void ExecuteShellcode(PBYTE shellcode);

int main() {
 PBYTE shellcode;
 DWORD size;

 // 从文件加载shellcode
 if (!LoadShellcodeFromFile("dump.bin", &shellcode, &size)) {
 printf("Failed to load shellcode from file.n");
 return 1;
 }

 // 执行shellcode
 ExecuteShellcode(shellcode);

 // 清理资源
 VirtualFree(shellcode, 0, MEM_RELEASE);

 return 0;
}

// 从文件加载shellcode到内存的函数实现
BOOL LoadShellcodeFromFile(const char* filename, PBYTE* shellcode, DWORD* size) {
 HANDLE file;
 DWORD bytesRead;

 // 打开文件
 file = CreateFileA(filename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
 if (file == INVALID_HANDLE_VALUE) {
 return FALSE;
 }

 // 获取文件大小
 *size = GetFileSize(file, NULL);
 if (*size == INVALID_FILE_SIZE) {
 CloseHandle(file);
 return FALSE;
 }

 // 分配内存
 *shellcode = (PBYTE)VirtualAlloc(NULL, *size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
 if (*shellcode == NULL) {
 CloseHandle(file);
 return FALSE;
 }

 // 读取文件内容到内存
 if (!ReadFile(file, *shellcode, *size, &bytesRead, NULL) || bytesRead != *size) {
 VirtualFree(*shellcode, 0, MEM_RELEASE);
 CloseHandle(file);
 return FALSE;
 }

 // 关闭文件
 CloseHandle(file);

 return TRUE;
}

// 执行shellcode的函数实现
void ExecuteShellcode(PBYTE shellcode) {
 // 将shellcode地址转换为函数指针
 void (*func)() = (void(*)())shellcode;

 // 调用函数指针，执行shellcode
 func();
}
debug029:
000001C1E53B002D xor rax, rax
debug029:
000001C1E53B0030 lodsb
debug029:
000001C1E53B0031 cmp al, 61h ; 'a'
debug029:
000001C1E53B0033 jl short loc_1C1E53B0037
debug029:
000001C1E53B0035 sub al, 20h ; ' '
debug029:
000001C1E53B0037
debug029:
000001C1E53B0037 loc_1C1E53B0037: ; CODE XREF: sub_1C1E53B0000+33↑j
debug029:
000001C1E53B0037 ror r9d, 0Dh
debug029:
000001C1E53B003B add r9d, eax
debug029:
000001C1E53B003E loop loc_1C1E53B002D
二
ezshopping
private void verifyPurchase(final String str, final double d, final String str2) {
 Volley.newRequestQueue(this).add(new StringRequest(1, URL.purchaseURL, new Response.Listener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda2
 @Override // com.android.volley.Response.Listener
 public final void onResponse(Object obj) {
 shopActivity.this.m95lambda$verifyPurchase$0$comswddezshopingshopActivity((String) obj);
 }
 }, new Response.ErrorListener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda3
 @Override // com.android.volley.Response.ErrorListener
 public final void onErrorResponse(VolleyError volleyError) {
 shopActivity.this.m96lambda$verifyPurchase$2$comswddezshopingshopActivity(volleyError);
 }
 }) { // from class: com.swdd.ezshoping.shopActivity.1
 @Override // com.android.volley.Request
 protected Map<String, String> getParams() {
 HashMap hashMap = new HashMap();
 hashMap.put("username", str);
 hashMap.put("Money", String.format("%.2f", Double.valueOf(d)));
 hashMap.put("signature", str2);
 return hashMap;
 }
 });
 }

 /* JADX INFO: Access modifiers changed from: package-private */
 /* renamed from: lambda$verifyPurchase$2$com-swdd-ezshoping-shopActivity reason: not valid java name */
 public /* synthetic */ void m96lambda$verifyPurchase$2$comswddezshopingshopActivity(VolleyError volleyError) {
 if (volleyError.networkResponse != null) {
 switch (volleyError.networkResponse.statusCode) {
 case TypedValues.CycleType.TYPE_VISIBILITY /* 402 */:
 Toast.makeText(this, "Insufficient funds to complete the purchase.", 1).show();
 return;
 case TypedValues.CycleType.TYPE_ALPHA /* 403 */:
 AlertDialog.Builder builder = new AlertDialog.Builder(this);
 builder.setTitle("ERROR!");
 builder.setMessage("小伙子别想改我代码!");
 builder.setPositiveButton("OK", new DialogInterface.OnClickListener() { // from class: com.swdd.ezshoping.shopActivity$$ExternalSyntheticLambda0
 @Override // android.content.DialogInterface.OnClickListener
 public final void onClick(DialogInterface dialogInterface, int i) {
 dialogInterface.dismiss();
 }
 });
 builder.show();
 return;
 case 404:
 Toast.makeText(this, "User not found.", 1).show();
 return;
 default:
 Toast.makeText(this, "An error occurred: " + volleyError.toString(), 1).show();
 return;
 }
 }
 Toast.makeText(this, "Network error, no response received.", 1).show();
 }
import socket

# 指定服务器地址和端口
server_address = ('hnctf.imxbt.cn', 20528)

# 指定表单数据
form_data = {
 # 这里应该填入POST请求的具体数据
 "Money": "114514.00",
 "signature": "376c4fe518240bc513f67bf477d5d950d757d51bb58db594fa4551e248364413",
 "username": "" #填自己的用户名即可
}

# 将表单数据转换为application/x-www-form-urlencoded格式
form_data_encoded = "&".join("{}={}".format(key, val) for key, val in form_data.items())

# 准备HTTP请求头
http_request = """POST /purchase HTTP/1.1r
Host: hnctf.imxbt.cn:
20528r
If-None-Match: W/"12-hfcD7BKoo9fJ4GgYnq9Rj3aNpD8"r
Content-Type: application/x-www-form-urlencoded; charset=UTF-8r
User-Agent: Dalvik/2.1.0 (Linux; U; Android 9; PCRT00 Build/PQ3A.190605.01231654)r
Connection: Keep-Aliver
Accept-Encoding: gzipr
Content-Length: {}r
r
""".format(len(form_data_encoded))

# 完整的HTTP请求数据
http_request += form_data_encoded

# 创建TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
sock.connect(server_address)

# 发送HTTP请求
sock.sendall(http_request.encode())

# 接收响应数据
response = sock.recv(4096)
print(response.decode())

# 关闭socket连接
sock.close()
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 61
ETag: W/"3d-lbjcXjt9Oql9sd2OEm6pVRILsSE"
Date: Thu, 16 May 2024 01:31:23 GMT
Connection: keep-alive
Keep-Alive: timeout=5

H&NCTF{Congratulati0ns!_3cad3260-0c7e-4d98-afbc-814cc5221fcc}
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