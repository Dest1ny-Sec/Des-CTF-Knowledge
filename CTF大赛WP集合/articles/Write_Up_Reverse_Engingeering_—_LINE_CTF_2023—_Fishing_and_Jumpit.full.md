---
title: Write Up Reverse Engineering — LINE CTF 2023— Fishing and Jumpit
contest: LINE CTF 2023
year: 2023
difficulty: hard
vuln_type: reverse
tags:
- anti_decompiler_ebff
- nop_patch
- thread_modification_debug
- custom_rc4_iv
- frida_hook_brute_force
- unity_il2cpp
- il2cppdumper
- ghidra_python_script
- aes_ecb_score_concat
- anti_debug_int2c
attack_chain: Fishing:EB FF XX 反反编译字节码 → Python 脚本扫描全文件改 0x90 NOP → 重 IDA 反编译成功 → 发现 sub_140001DDB 段选混淆 + 线程修改 (key 调试器=m4g1KaRp_ON_7H3_Hook 实际) → XOR+sub 输入加密 + 自定义 RC4 加密 + memcmp 比 encryptedFlag → Frida hook 0x3f48 fscanf + 0x2310 encrypt + 0x3ff0 memcmp → 多线程 8 池爆破 41 字节 flag / Jumpit:Unity Android libil2cpp.so + global-metadata.dat → IL2CPPDumper → Ghidra + Python ghidra_with_struct.py 恢复符号 → GameManager$$ScoreUp 拼接 11 段 score StringLiteral → "Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx" 作 AES-128 ECB 密钥 → base64 解 cWGTmeDlFsYEFI9E5mH/eCnQ1SNlWJlXj+klPLbWS/c/1vI7UPrO4dp41u2tTGM2
key_payload: ebff_nop_patch = b'\xeb\xff\xXX' → b'\x90\x90\x90' / Frida hook 0x3f48 + 0x2310 + 0x3ff0 / key = 'Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx' / AES.MODE_ECB / score literal concat
one_liner: LINE CTF 2023 两道 RE：Fishing (EB FF XX 反 IDA + 线程修改 + Frida hook 41 字节爆破) + Jumpit (Unity IL2CPP 还原 + GameManager 11 段 score 拼接 AES-128 ECB 密钥解密)。
lesson: '"EB FF XX" 是 IDA 反编译杀手；现代 CTF RE 必备三件套：Frida 自动化 + IL2CPPDumper Unity 反编译 + Ghidra Python 脚本恢复符号表。'
quality: high
full_path: Write_Up_Reverse_Engingeering_—_LINE_CTF_2023—_Fishing_and_Jumpit.full.md
meta_path: Write_Up_Reverse_Engingeering_—_LINE_CTF_2023—_Fishing_and_Jumpit.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Write Up Reverse Engineering — LINE CTF 2023— Fishing and Jumpit。LINE CTF 2023 两道 RE：Fishing (EB FF XX 反 IDA + 线程修改 + Frida hook 41 字节爆破) + Jumpit (Unity IL2CPP 还原 + GameManager 11 段 score 拼接 AES-1...
category: misc
subcategory: misc_other
tools_used:
- Ghidra
- IDA
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/107081.html
wp_author: some
reasoning_chain:
- Fishing 触发点：EB FF XX 反反编译字节码 → 假设：直接 IDA 反编译卡死
- 动作：Python 脚本扫描全文件改 0x90 NOP → 重 IDA 反编译成功
- 观察：sub_140001DDB 段选混淆 + 线程修改（key 调试器=m4g1KaRp_ON_7H3_Hook 实际）→ 假设：线程会改 input
- XOR+sub 输入加密 + 自定义 RC4 加密 + memcmp 比 encryptedFlag → Frida hook 0x3f48 fscanf + 0x2310 encrypt + 0x3ff0 memcmp
- 假设：多线程 8 池爆破 41 字节 flag → 假设：必须并行 hook
- Jumpit 触发点：Unity Android libil2cpp.so + global-metadata.dat → 假设：IL2CPP 编译 Unity
- 动作：IL2CPPDumper 还原 → Ghidra + Python ghidra_with_struct.py 恢复符号
- 观察：GameManager$$ScoreUp 拼接 11 段 score StringLiteral → 'Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx' 作 AES-128 ECB 密钥
- 动作：base64 解 cWGTmeDlFsYEFI9E5mH/eCnQ1SNlWJlXj+klPLbWS/c/1vI7UPrO4dp41u2tTGM2 → AES.MODE_ECB 解密
- 观察：flag 解出 → 完成
failed_attempts:
- Fishing 试图静态分析 → 失败：EB FF XX 是 IDA 反编译杀手，必须 NOP patch
- Jumpit 试图 IDA 反编译 libil2cpp.so → 失败：必须用 IL2CPPDumper 还原符号
- Fishing 试图爆破 41 字节单线程 → 失败：必须 Frida hook 多线程并行
key_observations:
- '''EB FF XX'' 是 IDA 反编译杀手；现代 CTF RE 必备三件套：Frida 自动化 + IL2CPPDumper Unity 反编译 + Ghidra Python 脚本恢复符号表'
- 自定义 RC4 + 线程修改 input 是 RE 高阶题常见组合
- AES-128 ECB 密钥藏于 StringLiteral 拼接是 Unity RE 经典
- Unity Android libil2cpp.so + global-metadata.dat 是 Unity RE 标配
- Frida hook 多线程并行爆破是 Frida 高阶用法
prerequisites:
- IDA 反编译 + EB FF XX 字节码理解
- Frida hook 基础（fscanf / encrypt / memcmp）
- IL2CPPDumper + Ghidra 符号恢复
- AES-128 ECB 解密（PyCryptodome）
- 多线程 Frida 并行爆破
---
# Write Up Reverse Engingeering — LINE CTF 2023— Fishing and Jumpit

> 原文: https://www.ctfiot.com/107081.html
> ID: 107081

Introduction

A week ago, I participated in LINE CTF as part of team TCP1P, with the username mahoushoujo. I managed to solve two reverse engineering challenges named Fishing and Jumpit, and our team secured 16th place out of 477 teams.

Today, I want to share a write-up for these two challenges.

All files can be downloaded here

Table of Content

· Introduction

· Table of Content

· Fishing

· Jumpit

· Epilogue

Fishing

In this challenge, there is a binary called fishing.exe. Running the binary prompts the user to input the correct flag.

Now, let’s view the program in the decompiler

In the decompiler, there are a few strings defined that are printed on the prompt.

However, if we look at the references, these strings are not used from any address.

If we examine the function code, we can see that the program fails at the decompiled code. This can be proven by some of the code below.

This occurs because the program has anti-decompiler instructions that break the analysis. Now we need to investigate how the anti-decompiler works in this program.

For this analysis, I used the function sub_140001DDB.

If we look at the disassembly view, we can see the program jumps to location 140001E15+1.

Now, let’s view the code at 140001E16 by undefining the code at 140001E15 and defining the code again at 140001E16.

After doing this, we should see the following instruction

The program increases and decreases the eax value, which does not affect the execution flow.

Now we know that the bytecode EB FF XX, with XX as any byte, serves as an anti-decompiler. To patch this, I created a Python script to find this pattern in the binary and replace it with a nop instruction.

data = open(“fishing.exe”, “rb”).read()

databyte = list(data)

for i in range(len(data)):

if(data[i:i+2] == “ebff”.decode(‘hex’)):

print(databyte[i:i+3])

for j in range(3):

databyte[i+j] = chr(0x90)

print(databyte[i:i+3])

newdata = ”.join(databyte)

open(‘fishing-patch.exe’, ‘wb’).write(newdata)

Running the program and reopening the new file fishing-patch.exe in the decompiler.

After patching, the string is already referenced, and the program should now decompile successfully.

Before inspecting the main code, we should check for any anti-debugger code within the program.

If we examine the program’s functions, we can see the code below:

This function would disrupt the program’s execution when attached to a debugger. To fix this, the function needs to be patched.

After patching, we should see the program prompting for input.

Now, let’s analyze the program. Below is the main function that has been renamed based on its functionality:

In the startAddress function, the program encrypts our input using a combination of XOR and subtraction processes. The program also performs XOR and addition processes on our key. After modifying the key and input, the program executes a custom RC4 encryption and compares the results using memcmp with the encryptedFlag variable that has already been set.

However, this function is straightforward; I discovered strange behavior during the analysis.

Below is the value of the key when the program is being debugged:

The program should run fine, performing the encryption XOR and using the key below:

However, when my team debugged the program in Frida, we observed a different result. When executing this in Frida, my team found that the key used in the custom RC4 is “m4g1KaRp_ON_7H3_Hook”

This strange behavior also exists in the input variable.

Below is another behavior of the program modifying the input:

I tried inputting BBBBBBB into the program. The program correctly displayed the result as 63 63 63 63 in hex. But before entering sub34, the variable changed to 1b 1b 1b 1b in hex.

If we examine the code, the program does not perform any other processes between these functions.

This behavior also exists in the key encryption. Before entering xor11, the key is not processed with any function.

This code applies normally to the debugger.

However, this behavior changes when entering xor11, as the key has already been altered to a different value, indicating that there is another process before entering the xor11 function.

This can happen because the program calls this function.

In this function, the program sets up some kind of thread modification, causing the process in the debugger and the real-time process to exhibit different behavior.

I tried to analyze this process and attempted to duplicate the code in C, but still failed

However, I had another approach to solve this. If we look at the code, the program compares encryptedFlag with outputRc4 in the function. We can obtain the value of this argument using Frida.

The outputRc4 encryption used by the program also has a linear encryption, meaning if we modify the first byte input, only the first byte output is modified. Why not use Frida to brute force?

After coming up with this idea, I tried to create a Frida script to hook the function address after input, replace our fake input with our brute-force input, and then hook the memcmp function to get the value of encryptedFlag and outputRc4.

I combined this Frida script with a Python script to wrap the automation, and we should be able to automate hooking in Windows (with a hacky script, I guess hehe).

Below is the Python script that I used to automate this process:

from subprocess import check_output as co

from os import system

from multiprocessing.dummy import Pool as ThreadPool

# read base frida script

hook = open(‘hook2.js’).read()

def execute_process(args):

# defined var

ch, j, pload = args

pload_copy = pload[:]

# append null byte as end string

pload_copy.append(“\x00”)

pload_copy[j] = chr(ch)

ploadconv = map(ord, list(pload_copy))

conv = (str(ploadconv))

# replace hex value with brute input

hook2 = hook.replace(“REPLACER”, conv)

hook2fp = open(‘tmp/hook_{}_{}p.js’.format(ch, j), ‘w’)

hook2fp.write(hook2)

hook2fp.close()

# fake input

hook2fp = open(‘tmp/test_{}_{}.txt’.format(ch, j), ‘w’)

hook2fp.write(“test”)

hook2fp.close()

# execute frida script

print(‘loop’)

print(“frida -f .\\fishing.exe -l .\\tmp\\hook_{}_{}p.js –no-pause < tmp\\test_{}_{}.txt > tmp\\a_{}_{}”.format(ch, j,ch, j,ch, j))

data = system(“frida -f .\\fishing.exe -l .\\tmp\\hook_{}_{}p.js –no-pause < tmp\\test_{}_{}.txt > tmp\\a_{}_{}”.format(ch, j,ch, j,ch, j))

print(data)

# parsing frida output

a = open(‘tmp\\a_{}_{}’.format(ch, j), ‘r’)

data = a.read()

a.close()

kotak = data.split(“So: fishing.exe Method: cmp: 0x3ff0”)[1].split(“0123456789ABCDEF”)[2].split(“\n”)[1 + (j / 16)].split(” “)[1].split(” “)[0]

print(j, 1 + (j % 16), kotak)

kotak = kotak.strip()

kotak = kotak.replace(” “, “”)

kotak = kotak.decode(‘hex’)

flag = “d0be9f5abdf034b5d06ffbe299baaed736d52dc22245b0039d636653c728cc2a2b14bb099be360463a”.decode(‘hex’)

print(flag[j].encode(‘hex’), kotak[j % 16].encode(‘hex’))

# if encrypted input == encrypted flag, return value

if(flag[j] == kotak[j % 16]):

return pload_copy, chr(ch)

return None, None

# init input bruteforce

pload = [“A” for i in range(41)]

flag = “”

for i in range(len(flag)):

pload[i] = flag[i]

import string

# brute space

flagchr = string.letters + “{_}” + string.digits

# loop flag character

for j in range(len(flag), 41):

pool = ThreadPool(8)

results = pool.map(execute_process, [(ord(chx), j, pload) for chx in flagchr])

pool.close()

pool.join()

for payload_result, chr_result in results:

# if brute found solution append to flag character

if payload_result and chr_result:

pload = payload_result

flag += chr_result

print(flag)

print(flag)

print(pload)

print(chr_result)

break

Below is frida script that I used to implement my ideas

// init frida script

(function () {

// @ts-ignore

function print_arg(addr) {

try {

var module = Process.findRangeByAddress(addr);

if (module != null) return “\n”+hexdump(addr) + “\n”;

return ptr(addr) + “\n”;

} catch (e) {

return addr + “\n”;

}

}

// @ts-ignore

function hook_native_addr(funcPtr, paramsNum, method,mod=0) {

var module = Process.findModuleByAddress(funcPtr);

try {

Interceptor.attach(funcPtr, {

onEnter: function (args) {

this.logs = “”;

this.params = [];

// @ts-ignore

this.logs=this.logs.concat(“So: ” + module.name + ” Method: “+method+”: ” + ptr(funcPtr).sub(module.base) + “\n”);

for (let i = 0; i < paramsNum; i++) {

this.params.push(args[i]);

this.logs=this.logs.concat(“this.args” + i + ” onEnter: ” + print_arg(args[i]));

}

}, onLeave: function (retval) {

for (let i = 0; i < paramsNum; i++) {

this.logs=this.logs.concat(“this.args” + i + ” onLeave: ” + print_arg(this.params[i]));

}

this.logs=this.logs.concat(“retval onLeave: ” + print_arg(retval) + “\n”);

console.log(this.logs);

// if mod == 1, which means scanf called. Modify memory and to replace with brute input

if(mod == 1){

var point = this.params[4].readPointer()

console.log(point)

const newData = REPLACER;

Memory.writeByteArray(point, newData);

console.log(point.readByteArray(32))

}

}

});

} catch (e) {

console.log(e);

}

}

// @ts-ignore

// this hook used to modify memory after read data, I did not found any graceful way to input to frida 🙁

hook_native_addr(Module.findBaseAddress(“fishing.exe”).add(0x3f48), 0x5, “fscan after”, 1);

// this hook used to debug program

hook_native_addr(Module.findBaseAddress(“fishing.exe”).add(0x2310), 0x5, “encrypt”);

// our encrypted flag and encrypted input would compared on this address

hook_native_addr(Module.findBaseAddress(“fishing.exe”).add(0x3ff0), 3, “cmp”);

})();

Before running the script, don’t forget to create a tmp folder as a directory to store temporary thread outputs

mkdir tmp

Run the script and wait for a while until all flags can be guessed

python2 mt3.py

Notes:

Another intended solution that analysis threading handler can be viewed here: https://blog.snwo.kr/posts/(ctf)-line-ctf-2023/

Jumpit

In this challenge, a folder containing the Android distribution folder is provided.

However, only this folder is provided, without an APK build.

I checked the program in the native library and found libil2cpp.so and libunity.so, indicating that this project was built on the Unity framework.

In the program, I also found global-metadata files for Unity.

If metadata files exist, we should be able to view the program logic and discover the structure of libil2cpp.so using Ill2cppDumper

Run IL2CPPDumper and provide global-metadata.dat and libil2cpp.so.

After IL2CPPDumper is completed, these files will be generated:

This file can be used to resolve the structure and literal strings in the library. Now, using Ghidra (you can use IDA too for doing this), load the libil2cpp.so.

After the file is loaded, open the Window tab and open Script Manager.

Now, create a new script.

Choose Python and select a script name.

Now, open the file ghidra_with_struct.py in the IL2CPPDumper directory and copy all the code to the new script that we just created.

After copying the code content, click Run.

The program will ask for the script.json file that was generated by the IL2CPPDumper executable.

Now, we should be able to view the Unity logic in the library.

Now, the function can be resolved, and the logic code can be analyzed. Below is the code for getFlag:

In the getFlag method, the program executes DecryptECB with several parameters. Parameter _StringLiteral_2608 has a base64 value:

cWGTmeDlFsYEFI9E5mH/eCnQ1SNlWJlXj+klPLbWS/c/1vI7UPrO4dp41u2tTGM2

This value is an encrypted string that will be decrypted by AES ECB.

Another parameter, *(param_1 + 0x50), points to another value.

If we look at the GameManager$$ScoreUp method, this pointer is used and concatenated with another StringLiteral when the score reaches a certain point.

Below is the logic code for GameManager$$ScoreUp:

If we combine all score comparisons from the lowest to the highest and concatenate all StringLiterals for every score, the pointer will have the string value “Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx”.

I then created a Python script to decrypt “cWGTmeDlFsYEFI9E5mH/eCnQ1SNlWJlXj+klPLbWS/c/1vI7UPrO4dp41u2tTGM2” using the key “Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx”, and the flag was acquired in the output.

import base64

from Crypto.Cipher import AES

from Crypto.Util.Padding import pad,unpad

#AES ECB mode without IV

key = ‘Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx’ #Must Be 16 char for AES128

def encrypt(raw):

raw = pad(raw.encode(),16)

cipher = AES.new(key.encode(‘utf-8’), AES.MODE_ECB)

return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc):

enc = base64.b64decode(enc)

cipher = AES.new(key.encode(‘utf-8’), AES.MODE_ECB)

print(cipher.decrypt(enc))

# return unpad(cipher.decrypt(enc),16)

decrypted = decrypt(“cWGTmeDlFsYEFI9E5mH/eCnQ1SNlWJlXj+klPLbWS/c/1vI7UPrO4dp41u2tTGM2”)

print(‘data: ‘,decrypted)

Epilogue

I learned a lot while doing this CTF. Automating debugging and brute-forcing on Windows is always challenging because the environment is not as robust as GDB scripts running on Linux. Unity reverse engineering is also something rare that I’ve encountered in CTFs.

I hope this write-up helps people learn about Unity reverse engineering and Windows brute-forcing.

原文始发于Maulvi Alfansuri：Write Up Reverse Engingeering — LINE CTF 2023— Fishing and Jumpit

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