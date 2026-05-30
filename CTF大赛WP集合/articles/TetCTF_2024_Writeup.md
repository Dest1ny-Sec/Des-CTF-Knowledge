# TetCTF 2024 Writeup

> 原文: https://www.ctfiot.com/160243.html
> ID: 160243


```
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>baby-asm</title>
 
</head>

 
 

 <script>

 code = [ 0,97,115,109,1,0,0,0,1,56,9,80,0,95,1,127,1,80,0,94,99,0,1,96,0,0,96,1,127,1,100,1,96,3,99,1,127,127,0,96,2,99,1,127,1,127,96,4,99,1,127,127,127,0,96,1,99,1,1,127,96,1,99,1,1,127,3,8,7,2,3,4,5,6,7,8,6,118,20,127,1,65,224,0,11,127,1,65,229,0,11,127,1,65,20,11,127,1,65,177,1,11,127,1,65,155,1,11,127,1,65,244,0,11,127,1,65,236,0,11,127,1,65,197,0,11,127,1,65,212,0,11,127,1,65,237,0,11,127,1,65,231,0,11,127,1,65,238,0,11,127,1,65,239,0,11,127,1,65,223,0,11,127,1,65,244,0,11,127,1,65,231,0,11,127,1,65,225,0,11,127,1,65,200,0,11,127,1,65,20,11,127,1,65,59,11,7,45,7,1,49,0,0,4,105,110,105,116,0,1,10,97,114,114,97,121,95,102,105,108,108,0,2,1,51,0,3,1,52,0,4,1,53,0,5,5,99,104,101,99,107,0,6,10,184,8,7,142,1,0,35,0,65,19,115,36,0,35,1,65,55,115,36,1,35,2,65,32,115,36,2,35,3,65,36,115,36,3,35,4,65,19,115,36,4,35,5,65,55,115,36,5,35,6,65,32,115,36,6,35,7,65,36,115,36,7,35,8,65,19,115,36,8,35,9,65,55,115,36,9,35,10,65,32,115,36,10,35,11,65,36,115,36,11,35,12,65,19,115,36,12,35,13,65,55,115,36,13,35,14,65,32,115,36,14,35,15,65,36,115,36,15,35,16,65,19,115,36,16,35,17,65,55,115,36,17,35,18,65,32,115,36,18,35,19,65,36,115,36,19,11,9,0,32,0,251,7,1,16,0,11,22,0,32,0,32,1,32,2,65,19,106,65,64,107,251,0,0,65,1,251,16,1,11,13,0,32,0,32,1,251,11,1,251,2,0,0,11,109,0,32,1,65,0,70,4,64,32,0,32,2,32,0,32,2,16,3,32,3,106,65,32,115,16,2,5,32,1,65,1,70,4,64,32,0,32,2,32,0,32,2,16,3,32,3,106,65,36,115,16,2,5,32,1,65,2,70,4,64,32,0,32,2,32,0,32,2,16,3,32,3,106,65,19,115,16,2,5,32,1,65,3,70,4,64,32,0,32,2,32,0,32,2,16,3,32,3,106,65,55,115,16,2,11,11,11,11,11,172,3,1,1,127,32,0,65,0,16,3,65,137,175,2,70,4,64,32,1,65,1,106,33,1,5,11,32,0,65,1,16,3,65,200,4,70,4,64,32,1,65,1,106,33,1,11,32,0,65,2,16,3,65,226,5,70,4,64,32,1,65,1,106,33,1,11,32,0,65,3,16,3,65,194,173,2,70,4,64,32,1,65,1,106,33,1,11,32,0,65,4,16,3,65,193,242,3,70,4,64,32,1,65,1,106,33,1,11,32,0,65,5,16,3,65,135,5,70,4,64,32,1,65,1,106,33,1,11,32,0,65,6,16,3,65,193,6,70,4,64,32,1,65,1,106,33,1,11,32,0,65,7,16,3,65,242,240,3,70,4,64,32,1,65,1,106,33,1,11,32,0,65,8,16,3,65,166,243,2,70,4,64,32,1,65,1,106,33,1,11,32,0,65,9,16,3,65,238,3,70,4,64,32,1,65,1,106,33,1,11,32,0,65,10,16,3,65,151,5,70,4,64,32,1,65,1,106,33,1,11,32,0,65,11,16,3,65,229,241,2,70,4,64,32,1,65,1,106,33,1,11,32,0,65,12,16,3,65,225,139,4,70,4,64,32,1,65,1,106,33,1,11,32,0,65,13,16,3,65,129,5,70,4,64,32,1,65,1,106,33,1,11,32,0,65,14,16,3,65,151,6,70,4,64,32,1,65,1,106,33,1,11,32,0,65,15,16,3,65,174,137,4,70,4,64,32,1,65,1,106,33,1,11,32,0,65,16,16,3,65,225,149,2,70,4,64,32,1,65,1,106,33,1,11,32,0,65,17,16,3,65,177,4,70,4,64,32,1,65,1,106,33,1,11,32,0,65,18,16,3,65,161,5,70,4,64,32,1,65,1,106,33,1,11,32,0,65,19,16,3,65,234,147,2,70,4,64,32,1,65,1,106,33,1,11,32,1,65,20,70,4,127,65,1,5,65,0,11,11,218,2,0,32,0,65,0,65,1,32,0,65,0,16,3,35,0,106,16,4,32,0,65,1,65,2,32,0,65,1,16,3,35,1,107,16,4,32,0,65,2,65,3,32,0,65,2,16,3,35,2,108,16,4,32,0,65,3,65,0,32,0,65,3,16,3,35,3,115,16,4,32,0,65,0,65,5,32,0,65,4,16,3,35,4,106,16,4,32,0,65,1,65,6,32,0,65,5,16,3,35,5,107,16,4,32,0,65,2,65,7,32,0,65,6,16,3,35,6,108,16,4,32,0,65,3,65,4,32,0,65,7,16,3,35,7,115,16,4,32,0,65,0,65,9,32,0,65,8,16,3,35,8,106,16,4,32,0,65,1,65,10,32,0,65,9,16,3,35,9,107,16,4,32,0,65,2,65,11,32,0,65,10,16,3,35,10,108,16,4,32,0,65,3,65,8,32,0,65,11,16,3,35,11,115,16,4,32,0,65,0,65,13,32,0,65,12,16,3,35,12,106,16,4,32,0,65,1,65,14,32,0,65,13,16,3,35,13,107,16,4,32,0,65,2,65,15,32,0,65,14,16,3,35,14,108,16,4,32,0,65,3,65,12,32,0,65,15,16,3,35,15,115,16,4,32,0,65,0,65,17,32,0,65,16,16,3,35,16,106,16,4,32,0,65,1,65,18,32,0,65,17,16,3,35,17,107,16,4,32,0,65,2,65,19,32,0,65,18,16,3,35,18,108,16,4,32,0,65,3,65,16,32,0,65,19,16,3,35,19,115,16,4,32,0,16,5,11,0,45,4,110,97,109,101,1,38,7,0,1,49,1,4,105,110,105,116,2,10,97,114,114,97,121,95,102,105,108,108,3,1,51,4,1,52,5,1,53,6,5,99,104,101,99,107 ]; const byte_code = new Uint8Array(code);

 const wasmModule = new WebAssembly.Module(byte_code);
 const wasmInstance = new WebAssembly.Instance(wasmModule, {});
 const wasm = wasmInstance.exports;

 const consoleDiv = document.getElementById('console');
 const inputField = document.getElementById('input');

 inputField.addEventListener('keydown', function (event) {
 if (event.key === 'Enter') {
 const inputText = inputField.value;
 processInput(inputText);
 inputField.value = '';
 }
 });

 function processInput(text) {
 const p = document.createElement('p');
 if (text.startsWith('TetCTF{') && text.endsWith('}') && text.length === 27) {

 let array_size= 20;
 let array_obj = wasm.init(array_size);

 for (var i = 0; i < array_size; i++) {
 wasm.array_fill(array_obj, i, text.charCodeAt(i+7));
 }
 if (wasm.check(array_obj )){
 p.textContent = '> Correct!';
 } else {
 p.textContent = '> Incorrect!';
 }
 } else {
 p.textContent = '> Incorrect!';
 }
 consoleDiv.appendChild(p);
 consoleDiv.scrollTop = consoleDiv.scrollHeight;
 }
 </script>

</html>
function processInput(text) {
 const p = document.createElement('p');
 if (text.startsWith('TetCTF{') && text.endsWith('}') && text.length === 27) {

 let array_size= 20;
 let array_obj = wasm.init(array_size);

 for (var i = 0; i < array_size; i++) {
 wasm.array_fill(array_obj, i, text.charCodeAt(i+7));
 }
 if (wasm.check(array_obj )){
 p.textContent = '> Correct!';
 } else {
 p.textContent = '> Incorrect!';
 }
 } else {
 p.textContent = '> Incorrect!';
 }
 consoleDiv.appendChild(p);
 consoleDiv.scrollTop = consoleDiv.scrollHeight;
}
# array_fill
def array_fill(arr,i,c):
 arr[i] = c + 83
 return arr
(func $check (;6;) (export "check") (param $var0 (ref null $type1)) (result i32)
 local.get $var0
 i32.const 0
 i32.const 1
 local.get $var0
 i32.const 0
 call $3
 global.get $global0
 i32.add
 call $4
 local.get $var0
 i32.const 1
 i32.const 2
 local.get $var0
 i32.const 1
 call $3
 global.get $global1
 i32.sub
 call $4
 local.get $var0
 i32.const 2
 i32.const 3
 local.get $var0
 i32.const 2
 call $3
 global.get $global2
 i32.mul
 call $4
 local.get $var0
 i32.const 3
 i32.const 0
 local.get $var0
 i32.const 3
 call $3
 global.get $global3
 i32.xor
 call $4
 local.get $var0
 i32.const 0
 i32.const 5
 local.get $var0
 i32.const 4
 call $3
 global.get $global4
 i32.add
 call $4
 local.get $var0
 i32.const 1
 i32.const 6
 local.get $var0
 i32.const 5
 call $3
 global.get $global5
 i32.sub
 call $4
 local.get $var0
 i32.const 2
 i32.const 7
 local.get $var0
 i32.const 6
 call $3
 global.get $global6
 i32.mul
 call $4
 local.get $var0
 i32.const 3
 i32.const 4
 local.get $var0
 i32.const 7
 call $3
 global.get $global7
 i32.xor
 call $4
 local.get $var0
 i32.const 0
 i32.const 9
 local.get $var0
 i32.const 8
 call $3
 global.get $global8
 i32.add
 call $4
 local.get $var0
 i32.const 1
 i32.const 10
 local.get $var0
 i32.const 9
 call $3
 global.get $global9
 i32.sub
 call $4
 local.get $var0
 i32.const 2
 i32.const 11
 local.get $var0
 i32.const 10
 call $3
 global.get $global10
 i32.mul
 call $4
 local.get $var0
 i32.const 3
 i32.const 8
 local.get $var0
 i32.const 11
 call $3
 global.get $global11
 i32.xor
 call $4
 local.get $var0
 i32.const 0
 i32.const 13
 local.get $var0
 i32.const 12
 call $3
 global.get $global12
 i32.add
 call $4
 local.get $var0
 i32.const 1
 i32.const 14
 local.get $var0
 i32.const 13
 call $3
 global.get $global13
 i32.sub
 call $4
 local.get $var0
 i32.const 2
 i32.const 15
 local.get $var0
 i32.const 14
 call $3
 global.get $global14
 i32.mul
 call $4
 local.get $var0
 i32.const 3
 i32.const 12
 local.get $var0
 i32.const 15
 call $3
 global.get $global15
 i32.xor
 call $4
 local.get $var0
 i32.const 0
 i32.const 17
 local.get $var0
 i32.const 16
 call $3
 global.get $global16
 i32.add
 call $4
 local.get $var0
 i32.const 1
 i32.const 18
 local.get $var0
 i32.const 17
 call $3
 global.get $global17
 i32.sub
 call $4
 local.get $var0
 i32.const 2
 i32.const 19
 local.get $var0
 i32.const 18
 call $3
 global.get $global18
 i32.mul
 call $4
 local.get $var0
 i32.const 3
 i32.const 16
 local.get $var0
 i32.const 19
 call $3
 global.get $global19
 i32.xor
 call $4
 local.get $var0
 call $5
 )
)
from z3 import *
from math import *

flag = [BitVec(f"flag[{i}]", 8) for i in range(27)]
s = Solver()

# TetCTF{AAAAAAAAAAAAAAAAAAA}
s.add(flag[0] == ord("T"))
s.add(flag[1] == ord("e"))
s.add(flag[2] == ord("t"))
s.add(flag[3] == ord("C"))
s.add(flag[4] == ord("T"))
s.add(flag[5] == ord("F"))
s.add(flag[6] == ord("{"))
s.add(flag[26] == ord("}"))
for i in range(7,26):
 s.add(And(
 (flag[i] >= 0x21),
 (flag[i] <= 0x7e)
 ))

# flag = list("TetCTF{") + [ord("A") for i in range(20)] + ["}"]

globals = [115,82,52,149,136,67,76,97,71,90,71,74,124,104,84,67,114,127,52,31]

# array_fill
def array_fill(arr,i,c):
 arr[i] = c + 83
 return arr

def f4(arr,type_num,index,value):
 tmp = arr[index] + value

 if type_num == 0:
 tmp = tmp ^ 32
 if type_num == 1:
 tmp = tmp ^ 36
 if type_num == 2:
 tmp = tmp ^ 19
 if type_num == 3:
 tmp = tmp ^ 55

 arr = array_fill(arr,index,tmp)
 return arr

arr = [0 for i in range(20)]
for i in range(20):
 arr = array_fill(arr,i,flag[i+7])

# print(arr)
next = [1,2,3,0,5,6,7,4,9,10,11,8,13,14,15,12,17,18,19,16]

for i in range(20):
 type_num = i % 4
 index = next[i]
 val = arr[i]
 g_val = globals[i]

 if type_num == 0:
 val = val + g_val
 if type_num == 1:
 val = val - g_val
 if type_num == 2:
 val = val * g_val
 if type_num == 3:
 val = val ^ g_val

 # print(type_num,index,val)
 arr = f4(arr,type_num,index,val)

# print(arr)

ans = [38793,584,738,38594,63809,647,833,63602,47526,494,663,47333,67041,641,791,66734,35553,561,673,35306]
for i in range(20):
 s.add(ans[i] == arr[i])

assert s.check() == sat
while s.check() == sat:
 m = s.model()
 for c in flag:
 print(chr(m[c].as_long()),end="")
 print("")
 break
undefined8 check_key(char *param_1)
{
 long lVar1;
 int iVar2;
 size_t len_flag;
 undefined8 uVar3;
 long in_FS_OFFSET;
 uint k;
 uint m;
 uint l;
 uint a;
 uint b;
 uint i;
 long mem1 [22];
 long mem2 [22];
 long unk [22];
 undefined8 local_38;
 undefined8 local_30;
 undefined4 local_28;
 undefined2 local_24;
 long local_20;

 local_20 = *(long *)(in_FS_OFFSET + 0x28);
 len_flag = strlen(param_1);
 if (len_flag == 0x54) {
 local_38 = 0x6766656463615f21;
 local_30 = 0x72706f6e6d6c6968;
 local_28 = 0x77757473;
 local_24 = 0x79;
 for (k = 0; k < 0x54; k = k + 1) {
 for (m = 0; (m < 0x15 && (*(char *)((long)&local_38 + (ulong)m) != param_1[k])); m = m + 1) {
 if (m == 0x14) {
 uVar3 = 0;
 goto LAB_00101603;
 }
 }
 }
 memset(mem1,0,0xa8);
 for (l = 0; l < 0x15; l = l + 1) {
 iVar2 = hash_64_fnv1a(param_1 + (l << 2),4);
 mem1[l] = (long)iVar2;
 }
 x = 0x75bcd15;
 y = 0x159a55e5;
 z = 0x1f123bb5;
 w = 0xdeadbeef;
 memset(mem2,0,0xa8);
 for (a = 0; a < 0x15; a = a + 1) {
 for (b = 0; b < 0x15; b = b + 1) {
 lVar1 = mem1[b];
 iVar2 = xorshift128();
 mem2[a] = lVar1 * (iVar2 % 0x400) + mem2[a];
 }
 }
 unk[0] = -0x90ee47fcb5;
 unk[1] = 0x673420daf2;
 unk[2] = 0x45eb817f02c;
 unk[3] = 0xfffffe3099503945;
 unk[4] = 0x18f8dce1227;
 unk[5] = 0x26050ea6875;
 unk[6] = 0x298599c4bf0;
 unk[7] = 0xfffff8a356ce9e58;
 unk[8] = 0xfffffed3c712cf36;
 unk[9] = 0xfffffe96846d630f;
 unk[10] = 0x58cb1ce3ff3;
 unk[11] = 0xfffffccf182c2a63;
 unk[12] = 0xfffffe57fdf3f1de;
 unk[13] = 0xfffffa603f35f962;
 unk[14] = 0xffffff7884570b57;
 unk[15] = 0x4897c4d9c1;
 unk[16] = 0xfffffeb9355e5cb4;
 unk[17] = 0xdcedf7d094;
 unk[18] = 0x3602e9cac47;
 unk[19] = 0xfffffee3667219d6;
 unk[20] = 0xfffffdc326c9b063;
 for (i = 0; i < 0x15; i = i + 1) {
 if (unk[i] != mem2[i]) {
 uVar3 = 0;
 goto LAB_00101603;
 }
 }
 uVar3 = 1;
 }
 else {
 uVar3 = 0;
 }
LAB_00101603:
 if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
 return uVar3;
 }
 /* WARNING: Subroutine does not return */
 __stack_chk_fail();
}
len_flag = strlen(param_1);
 if (len_flag == 0x54) {
 # 0x21,0x5F,0x61,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6C,0x6D,0x6E,0x6F,0x70,0x72,0x73,0x74,0x75,0x77,0x79
 # !_acdefghilmnoprstuwy
 local_38 = 0x6766656463615f21;
 local_30 = 0x72706f6e6d6c6968;
 local_28 = 0x77757473;
 local_24 = 0x79;
 for (k = 0; k < 0x54; k = k + 1) {
 for (m = 0; (m < 0x15 && (*(char *)((long)&local_38 + (ulong)m) != param_1[k])); m = m + 1) {
 if (m == 0x14) {
 uVar3 = 0;
 goto LAB_00101603;
 }
 }
 }
memset(mem1,0,0xa8);
for (l = 0; l < 0x15; l = l + 1) {
 iVar2 = hash_64_fnv1a(param_1 + (l << 2),4);
 mem1[l] = (long)iVar2;
}
x = 0x75bcd15;
y = 0x159a55e5;
z = 0x1f123bb5;
w = 0xdeadbeef;
memset(mem2,0,0xa8);
for (a = 0; a < 0x15; a = a + 1) {
 for (b = 0; b < 0x15; b = b + 1) {
 lVar1 = mem1[b];
 iVar2 = xorshift128();
 mem2[a] = lVar1 * (iVar2 % 0x400) + mem2[a];
 }
}
for (i = 0; i < 0x15; i = i + 1) {
 if (unk[i] != mem2[i]) {
 uVar3 = 0;
 goto LAB_00101603;
 }
}
uVar3 = 1;
uint xorshift128(void)
{
 uint uVar1;

 uVar1 = x ^ x << 0xb;
 x = y;
 y = z;
 z = w;
 w = w ^ w >> 0x13 ^ uVar1 ^ uVar1 >> 8;
 return w;
}
from ctypes import *
import numpy as np
import math
from itertools import permutations,product

ans = [0 for i in range(0x15)]
ans[0] = 0xffffff6f11b8034b
ans[1] = 0x673420daf2
ans[2] = 0x45eb817f02c
ans[3] = 0xfffffe3099503945
ans[4] = 0x18f8dce1227
ans[5] = 0x26050ea6875
ans[6] = 0x298599c4bf0
ans[7] = 0xfffff8a356ce9e58
ans[8] = 0xfffffed3c712cf36
ans[9] = 0xfffffe96846d630f
ans[10] = 0x58cb1ce3ff3
ans[11] = 0xfffffccf182c2a63
ans[12] = 0xfffffe57fdf3f1de
ans[13] = 0xfffffa603f35f962
ans[14] = 0xffffff7884570b57
ans[15] = 0x4897c4d9c1
ans[16] = 0xfffffeb9355e5cb4
ans[17] = 0xdcedf7d094
ans[18] = 0x3602e9cac47
ans[19] = 0xfffffee3667219d6
ans[20] = 0xfffffdc326c9b063

def hash_64_fnv1a(data):
 fnv_prime = 0x100000001b3
 hash = 0xcbf29ce484222325
 for byte in data:
 hash = c_int32((hash ^ byte) * fnv_prime).value
 return hash

x = 0x75bcd15
y = 0x159a55e5
z = 0x1f123bb5
w = 0xdeadbeef

def xorshift128():
 global x, y, z, w
 v1 = ((c_uint32(x<<11).value ^ c_uint32(x).value) >> 8)
 v1 ^= c_uint32(x<<11).value ^ x
 v1 = c_uint32(v1).value
 x = y
 y = z
 z = w
 w ^= c_uint32(w).value >> 19
 w ^= v1
 w = c_int32(w).value
 return w

hashes = {}
words = "!_acdefghilmnoprstuwy"
for chars in product(words,repeat=4):
 A = ''.join(chars)
 hashes[hash_64_fnv1a(A.encode())] = A

X = []
for i in range(0x15):
 X.append([int(math.fmod(xorshift128(), 1024)) for n in range(0x15)])

# N1 = val[0]*X[i*0x15+0] + 0
# N2 = val[1]*X[i*0x15+1] + N1
# N3 = val[2]*X[i*0x15+2] + N2
# N4 = val[3]*X[i*0x15+3] + N3
# N5 = val[4]*X[i*0x15+4] + N4
# N6 = val[5]*X[i*0x15+5] + N5
# N7 = val[6]*X[i*0x15+6] + N6
# N8 = val[7]*X[i*0x15+7] + N7
# N9 = val[8]*X[i*0x15+8] + N8
# N10 = val[9]*X[i*0x15+9] + N9
# N11 = val[10]*X[i*0x15+10] + N10
# N12 = val[11]*X[i*0x15+11] + N11
# N13 = val[12]*X[i*0x15+12] + N12
# N14 = val[13]*X[i*0x15+13] + N13
# N15 = val[14]*X[i*0x15+14] + N14
# N16 = val[15]*X[i*0x15+15] + N15
# N17 = val[16]*X[i*0x15+16] + N16
# N18 = val[17]*X[i*0x15+17] + N17
# N19 = val[18]*X[i*0x15+18] + N18
# N20 = val[19]*X[i*0x15+19] + N19
# N21 = val[20]*X[i*0x15+20] + N20
# ans が右辺ベクトル、X[i*0x15+j] が係数行列になるので上記の連立方程式を解く

A = np.array(X)
B = np.array([c_int64(n).value for n in ans])
solution = np.linalg.solve(A, B)

for s in solution:
 v = c_int64(round(s)).value
 print(hashes[v],end="")
```
