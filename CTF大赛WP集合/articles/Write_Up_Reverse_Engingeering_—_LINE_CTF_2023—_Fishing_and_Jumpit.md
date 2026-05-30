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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428219dcfb22.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_642821ef1a985.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_642821f64e2e2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_642821ff7f3a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_642822084584b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428221376b9a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428221cbbe29.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428222594a31.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428223576e9c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/img_6428223d04f35.png)