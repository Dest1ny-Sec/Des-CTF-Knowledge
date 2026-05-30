# [SUCTF2025] SU_APP、SU_Harmony 出题小记

> 原文: https://www.ctfiot.com/226563.html
> ID: 226563

一

SU_APP

function hook_memcmp_addr() {
 var memcmp_addr = Module.findExportByName("libc.so", "fread");
 if (memcmp_addr !== null) {
 console.log("fread address: ", memcmp_addr);
 Interceptor.attach(memcmp_addr, {
 onEnter: function (args) {
 this.buffer = args[0];
 this.size = args[1];
 this.count = args[2];
 this.stream = args[3];
 },
 onLeave: function (retval) {
 if (this.count.toInt32() == 8) {
 Memory.writeByteArray(this.buffer, [0x50, 0x00, 0x00, 0x58, 0x00, 0x02, 0x1f, 0xd6]);
 retval.replace(8);
 }
 }
 });
 } else {

 }
}

function Hookdlopenext() {
 hook_memcmp_addr()

 var dlopen = Module.findExportByName(null, "android_dlopen_ext");
 Interceptor.attach(dlopen, {
 onEnter: function (args) {
 var filePath = args[0].readCString();

 if (filePath.indexOf("suapp") != -1) {
 this.isCanHook = true;

 }
 }, onLeave: function (retValue) {
 if (this.isCanHook) {
 this.isCanHook = false;
 NativeHook();

 }
 }
 })
}

setImmediate(Hookdlopenext);

function dump_so(so_name) {
 var libso = Process.getModuleByName(so_name);
 console.log("[name]:", libso.name);
 console.log("[base]:", libso.base);
 console.log("[size]:", ptr(libso.size));
 console.log("[path]:", libso.path);
 var file_path = "/sdcard/Download/" + libso.name + "_" + libso.base + "_" + ptr(libso.size) + ".so";
 var file_handle = new File(file_path, "wb");
 if (file_handle && file_handle != null) {
 Memory.protect(ptr(libso.base), libso.size, 'rwx');
 var libso_buffer = ptr(libso.base).readByteArray(libso.size);
 file_handle.write(libso_buffer);
 file_handle.flush();
 file_handle.close();
 console.log("[dump]:", file_path);
 }

}

addr = 0x4D2D0
for i in range(addr,addr + 0x40):
 print(hex(get_wide_byte(i)^0x3c),end=" ")

addr = 0x4D0D0
for i in range(addr,addr + 0x40):
 print(hex(get_wide_byte(i)),end=" ")

.SoFixer-Windows-64.exe -s .libsuapp.so_0x7d248e7000_0x25000.so -o libsuapp.sofix -m 0x7d248e7000 -d

typedef int (*Func1)(int, int, int);
typedef int (*Func2)(int, int, int, int);
typedef int (*Func3)(int, int, int, int, int);

typedef struct {
 union {
 Func1 func1; // Function with 1 parameter
 Func2 func2; // Function with 2 parameters
 Func3 func3; // Function with 3 parameters
 } func;
 int param_count; // Number of parameters
} OperationFunction;

function NativeHook() {
 var base = Module.getBaseAddress("libsuapp.so");
 console.log("[Base]->", base);
 Interceptor.attach(base.add("0xA158"), {
 onEnter: function (args) {

 },
 onLeave: function (retval) {
 randcode.push(retval.toInt32())
 }
 });
 Interceptor.attach(base.add("0x9FA8"), {
 onEnter: function (args) {
 console.log(randcode);

 console.log(randcode.length);
 while (randcode.length) {
 randcode.pop();
 }
 },
 onLeave: function (retval) {


 }
 });
}

function hook_memcmp_addr() {
 var memcmp_addr = Module.findExportByName("libc.so", "fread");
 if (memcmp_addr !== null) {
 console.log("fread address: ", memcmp_addr);
 Interceptor.attach(memcmp_addr, {
 onEnter: function (args) {
 this.buffer = args[0];
 this.size = args[1];
 this.count = args[2];
 this.stream = args[3];
 },
 onLeave: function (retval) {
 if (this.count.toInt32() == 8) {
 Memory.writeByteArray(this.buffer, [0x50, 0x00, 0x00, 0x58, 0x00, 0x02, 0x1f, 0xd6]);
 retval.replace(8);
 }
 }
 });
 } else {

 }
}

var randcode = [];
function dump_so(so_name) {
 var libso = Process.getModuleByName(so_name);
 console.log("[name]:", libso.name);
 console.log("[base]:", libso.base);
 console.log("[size]:", ptr(libso.size));
 console.log("[path]:", libso.path);
 var file_path = "/sdcard/Download/" + libso.name + "_" + libso.base + "_" + ptr(libso.size) + ".so";
 var file_handle = new File(file_path, "wb");
 if (file_handle && file_handle != null) {
 Memory.protect(ptr(libso.base), libso.size, 'rwx');
 var libso_buffer = ptr(libso.base).readByteArray(libso.size);
 file_handle.write(libso_buffer);
 file_handle.flush();
 file_handle.close();
 console.log("[dump]:", file_path);
 }

}

function NativeHook() {
 var base = Module.getBaseAddress("libsuapp.so");
 console.log("[Base]->", base);
 Interceptor.attach(base.add("0xA158"), {
 onEnter: function (args) {

 },
 onLeave: function (retval) {
 randcode.push(retval.toInt32())
 }
 });
 Interceptor.attach(base.add("0x9FA8"), {
 onEnter: function (args) {
 console.log(randcode);

 console.log(randcode.length);
 while (randcode.length) {
 randcode.pop();
 }
 },
 onLeave: function (retval) {


 }
 });



}

function Hookdlopenext() {
 hook_memcmp_addr()

 var dlopen = Module.findExportByName(null, "android_dlopen_ext");
 Interceptor.attach(dlopen, {
 onEnter: function (args) {
 var filePath = args[0].readCString();

 if (filePath.indexOf("suapp") != -1) {
 this.isCanHook = true;

 }
 }, onLeave: function (retValue) {
 if (this.isCanHook) {
 this.isCanHook = false;
 NativeHook();

 }
 }
 })
}

setImmediate(Hookdlopenext);

import idautils
import idc
import idaapi

def rename_functions(start_name, num_funcs, prefix='func_'):
 """
 从指定函数开始，批量重命名后续函数。

 Args:
 start_name (str): 起始函数的名称。
 num_funcs (int): 要重命名的函数数量。
 prefix (str): 新函数名称的前缀。
 """
 # 获取起始函数的地址
 start_ea = idc.get_name_ea_simple(start_name)
 if start_ea == idc.BADADDR:
 print("错误: 未找到名称为 '{}' 的函数。".format(start_name))
 return

 # 获取所有函数地址并排序
 functions = list(idautils.Functions())
 functions = sorted(functions)

 # 查找起始函数在函数列表中的索引
 try:
 start_index = functions.index(start_ea)
 
except ValueError:
 print("错误: 起始函数地址未在函数列表中找到。")
 return

 # 检查是否有足够的函数进行重命名
 if start_index + num_funcs > len(functions):
 print("警告: 函数数量不足，最多只能重命名 {} 个函数。".format(len(functions) - start_index))
 num_funcs = len(functions) - start_index

 # 执行批量重命名
 for i in range(num_funcs):
 func_ea = functions[start_index + i]
 old_name = idc.get_func_name(func_ea)
 new_name = "{}{}".format(prefix, i)

 # 尝试重命名函数
 success = idc.set_name(func_ea, new_name, idc.SN_NOWARN)
 if success:
 print("成功: 将函数 0x{:X} ('{}') 重命名为 '{}'。".format(func_ea, old_name, new_name))
 else:
 print("失败: 无法将函数 0x{:X} ('{}') 重命名为 '{}'。".format(func_ea, old_name, new_name))

def main():
 start_func_name = "sub_A224" # 起始函数名称，根据需要修改
 number_of_functions = 256 # 要重命名的函数数量
 prefix = "func_" # 新函数名称的前缀

 rename_functions(start_func_name, number_of_functions, prefix)

if __name__ == "__main__":
 main()

import idaapi
import idautils
import hashlib
import re # 导入正则表达式模块

# 获取函数的字节码（字节序列）
def get_function_bytes(func_start):
 func = idaapi.get_func(func_start)
 func_end = func.end_ea # 使用 end_ea 获取函数结束地址
 func_bytes = bytearray()
 for addr in range(func_start, func_end):
 func_bytes.append(idaapi.get_byte(addr)) # 使用 idaapi.get_byte 获取字节
 return func_bytes

# 计算字节码的哈希值作为相似度的度量
def get_function_hash(func_start):
 func_bytes = get_function_bytes(func_start)
 return hashlib.md5(func_bytes).hexdigest()

# 获取所有符合条件（__Z8func_*）函数的哈希值，并提取数字
def get_all_functions():
 functions = {}
 func_pattern = re.compile(r'func_(d+)') # 修改正则表达式，匹配 __Z8func_ 后面跟数字
 for func_start in idautils.Functions():
 func_name = idaapi.get_func_name(func_start)
 # 检查函数名是否符合 "__Z8func_*" 格式
 match = func_pattern.search(func_name)
 if match:
 func_number = int(match.group(1)) # 提取函数名中的数字部分
 func_hash = get_function_hash(func_start) # 计算哈希值
 if func_hash not in functions:
 functions[func_hash] = [] # 如果没有该哈希的组，则创建一个新组
 functions[func_hash].append(func_number) # 将函数的数字加入对应哈希的组中
 return functions

# 输出相同哈希的函数数字组

def print_functions_by_hash(functions):
 count = 1
 for func_hash, func_numbers in functions.items():
 # 输出哈希值和对应的数字数组3
 print(f"type{count}: {sorted(func_numbers)}")
 count += 1

# 主函数
def main():
 functions = get_all_functions() # 获取所有函数并按哈希分组
 print_functions_by_hash(functions) # 输出按哈希分组的数字数组

# 运行主函数
if __name__ == "__main__":
 main()

#include 
using namespace std;

// 各种类型的操作函数
void type1(int a1, int a2, int a3, int a4) {
 // a4 + a3 + a1 + a2;
 printf("a[%d] = a[%d] + a[%d] + %d + %d;n", a3, a4, a3, a1, a2);
}

void type2(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ (a3 + a1 + a4)) + a2
 printf("a[%d] = (a[%d] ^ (%d + %d + a[%d])) + %d;n", a4, a5, a3, a1, a4, a2);
}

void type3(int a1, int a2, int a3, int a4, int a5) {
 // a5 + a4 + a3 + a1 + a2
 printf("a[%d] = a[%d] + a[%d] + %d + %d + %d;n", a4, a5, a4, a3, a2, a1);
}

void type4(int a1, int a2, int a3) {
 // (a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ %d) + a[%d];n", a2, a3, a1, a2);
}

void type5(int a1, int a2, int a3, int a4) {
 // (a1 ^ (a3 + a4)) + a2
 printf("a[%d] = (%d ^ (a[%d] + a[%d])) + %d;n", a3, a1, a3, a4, a2);
}

void type6(int a1, int a2, int a3, int a4) {
 // (a4 ^ a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ %d) + %d;n", a3, a4, a3, a1, a2);
}

void type7(int a1, int a2, int a3, int a4) {
 // (a4 ^ (a1 + a3)) + a2;
 printf("a[%d] = (a[%d] ^ (%d + a[%d])) + %d;n", a3, a4, a1, a3, a2);
}

void type8(int a1, int a2, int a3) {
 // a3 + a1 + a2;
 printf("a[%d] = a[%d] + %d + a[%d];n", a2, a3, a1, a2);
}

void type9(int a1, int a2, int a3, int a4, int a5) {
 // (a3 ^ a1 ^ (a4 + a5)) + a2
 printf("a[%d] = (%d ^ %d ^ (a[%d] + a[%d])) + %d;n", a4, a3, a1, a4, a5, a2);
}

void type10(int a1, int a2, int a3, int a4, int a5) {
 // (a1 ^ (a4 + a3 + a5)) + a2;
 printf("a[%d] = (%d ^ (a[%d] + %d + a[%d])) + %d;n", a4, a1, a4, a3, a5, a2);
}

void type11(int a1, int a2, int a3, int a4, int a5) {
 // ((a4 + a5) ^ (a1 + a3)) + a2;
 printf("a[%d] = ((a[%d] + a[%d]) ^ (%d + %d)) + %d;n", a4, a4, a5, a1, a3, a2);
}

void type12(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a4 ^ a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ %d ^ %d) + %d;n", a4, a5, a4, a3, a1, a2);
}

void type13(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a1 ^ (a3 + a4)) + a2;
 printf("a[%d] = (a[%d] ^ %d ^ (%d + a[%d])) + %d;n", a4, a5, a1, a3, a4, a2);
}

void type14(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a4 ^ (a1 + a3)) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ (%d + %d)) + %d;n", a4, a5, a4, a1, a3, a2);
}

vector type1e = {0, 2, 11, 12, 15, 21, 26, 28, 39, 44, 53, 57, 62, 63, 72, 74, 77, 81, 90, 94, 97, 108, 113, 118, 121, 122, 125, 142, 144, 145, 151, 161, 162, 166, 181, 183, 185, 192, 199, 203, 215, 226, 230, 238, 242, 244, 247};
vector type21 = {1, 5, 34, 49, 84, 93, 130, 152, 154, 155, 207, 216, 217};
vector type31 = {3, 20, 24, 38, 42, 64, 70, 71, 73, 82, 124, 132, 176, 189, 196, 209, 220, 223, 224, 225, 237, 255};
vector type41 = {4, 9, 10, 14, 22, 23, 25, 31, 32, 33, 45, 69, 92, 99, 103, 111, 115, 117, 129, 147, 149, 150, 156, 164, 165, 172, 175, 241, 250, 254};
vector type51 = {6, 7, 29, 46, 47, 51, 60, 65, 76, 80, 85, 88, 98, 177, 182, 193, 208, 210, 221, 222, 236};
vector type61 = {8, 50, 54, 89, 126, 133, 198, 219, 240};
vector type71 = {13, 48, 55, 106, 119, 120, 127, 148, 170, 171, 197, 218, 233, 248, 252, 253};
vector type81 = {16, 17, 19, 30, 35, 36, 37, 43, 56, 59, 67, 68, 78, 79, 96, 100, 101, 107, 112, 114, 116, 123, 131, 135, 138, 139, 143, 158, 159, 160, 163, 167, 168, 169, 173, 178, 180, 188, 191, 194, 195, 204, 205, 211, 212, 227, 228, 229, 234, 235, 245, 249, 251};
vector type91 = {18, 134, 136, 140, 174, 213, 232};
vector type101 = {27, 58, 86, 104, 110, 146, 157, 179, 184, 202, 239, 243, 246};
vector type111 = {40, 52, 66, 95, 109, 128, 141, 153, 206, 231};
vector type121 = {41, 87, 200, 201};
vector type131 = {61, 91, 102, 137, 186, 187, 190, 214};
vector type141 = {75, 83, 105};

// 类型查找函数，根据opcode选择对应的类型
int getType(int opcode) {
 if (find(type1e.begin(), type1e.end(), opcode) != type1e.end()) return 1;
 if (find(type21.begin(), type21.end(), opcode) != type21.end()) return 2;
 if (find(type31.begin(), type31.end(), opcode) != type31.end()) return 3;
 if (find(type41.begin(), type41.end(), opcode) != type41.end()) return 4;
 if (find(type51.begin(), type51.end(), opcode) != type51.end()) return 5;
 if (find(type61.begin(), type61.end(), opcode) != type61.end()) return 6;
 if (find(type71.begin(), type71.end(), opcode) != type71.end()) return 7;
 if (find(type81.begin(), type81.end(), opcode) != type81.end()) return 8;
 if (find(type91.begin(), type91.end(), opcode) != type91.end()) return 9;
 if (find(type101.begin(), type101.end(), opcode) != type101.end()) return 10;
 if (find(type111.begin(), type111.end(), opcode) != type111.end()) return 11;
 if (find(type121.begin(), type121.end(), opcode) != type121.end()) return 12;
 if (find(type131.begin(), type131.end(), opcode) != type131.end()) return 13;
 if (find(type141.begin(), type141.end(), opcode) != type141.end()) return 14;
 return -1; // 未找到类型
}

unsigned char opcode[9999] = {

 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168, 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168, 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168

};

int main() {

 for (int i = 0; i < 1536; i += 6) {
 int a = opcode[i], b = opcode[i + 1], c = opcode[i + 2];
 int indexA = opcode[i + 3] % 32;
 int indexB = opcode[i + 4] % 32;
 int logic = opcode[i + 5];
 switch (getType(logic)) {
 case 1:
 type1(a, b, indexA, indexB);
 break;
 case 2:
 type2(a, b, c, indexA, indexB);
 break;
 case 3:
 type3(a, b, c, indexA, indexB);
 break;
 case 4:
 type4(a, indexA, indexB);
 break;
 case 5:
 type5(a, b, indexA, indexB);
 break;
 case 6:
 type6(a, b, indexA, indexB);
 break;
 case 7:
 type7(a, b, indexA, indexB);
 break;
 case 8:
 type8(a, indexA, indexB);
 break;
 case 9:
 type9(a, b, c, indexA, indexB);
 break;
 case 10:
 type10(a, b, c, indexA, indexB);
 break;
 case 11:
 type11(a, b, c, indexA, indexB);
 break;
 case 12:
 type12(a, b, c, indexA, indexB);
 break;
 case 13:
 type13(a, b, c, indexA, indexB);
 break;
 case 14:
 type14(a, b, c, indexA, indexB);
 break;
 default:
 cout << "Unknown logic type: " << logic << endl;
 }
 }
}

import re
from z3 import *

def translate_transformation(line):
 """
 Translates a single C++ transformation line into a Python Z3 constraint.

 Args:
 line (str): A line of C++ code representing a transformation.

 Returns:
 str: A line of Python code formatted for Z3.
 """
 # Remove any trailing semicolon and whitespace
 line = line.strip().rstrip(';')

 # Match the pattern a[index] = expression
 match = re.match(r'a[(d+)]s*=s*(.+)', line)
 if not match:
 raise ValueError(f"Invalid transformation line: {line}")

 index = match.group(1)
 expression = match.group(2)

 # Function to replace integers with BitVecVal(x, 32), excluding indices in a[index]
 def replace_int_literals(match):
 num = match.group(0)
 # If the number is part of 'a[number]', return as is
 if match.group(1):
 return num
 else:
 return f'BitVecVal({num}, 32)'

 # Regular expression to find integer literals not preceded by 'a['
 # This uses a negative lookbehind to ensure numbers inside a[...] are not matched
 int_literal_pattern = re.compile(r'(?<!a[)b(0x[0-9a-fA-F]+|d+)b')

 # Replace all integer literals not inside a[...] with BitVecVal(x, 32)
 processed_expression = int_literal_pattern.sub(replace_int_literals, expression)

 # Construct the Python assignment statement
 python_line = f'a[{index}] = {processed_expression}'

 return python_line

def translate_transformations(cpp_transformations):
 """
 Translates multiple C++ transformation lines into Python Z3 constraints.

 Args:
 cpp_transformations (str): Multiline string of C++ transformation lines.

 Returns:
 list: List of Python Z3 constraint lines.
 """
 python_constraints = []
 for line in cpp_transformations.strip().split('n'):
 # Remove comments
 line = line.split('//')[0]
 # Skip empty lines or lines that do not contain transformations
 if not line.strip() or not line.strip().startswith('a['):
 continue
 python_line = translate_transformation(line)
 python_constraints.append(python_line)
 return python_constraints

def generate_z3_script(transformation_constraints, results, input_size=32):
 """
 Generates the complete Z3 Python script with the given constraints.

 Args:
 transformation_constraints (list): List of Python Z3 constraint lines.
 results (list): List of expected result values.
 input_size (int): Size of the input array.

 Returns:
 str: The complete Python Z3 script as a string.
 """
 script_lines = [
 "from z3 import *",
 "",
 "# Initialize Z3 solver",
 "s = Solver()",
 "",
 "# Define input characters as 8-bit BitVec variables",
 f"input_vars = [BitVec(f'c{{i}}', 8) for i in range({input_size})]",
 "",
 "# Initialize array 'a' with {0} elements, initially set to input characters".format(input_size),
 f"a = [ZeroExt(24, input_vars[i]) for i in range({input_size})]",
 "",
 "# Translated Python Z3 Constraints"
 ]

 # Add transformation constraints
 for constraint in transformation_constraints:
 script_lines.append(constraint)

 # Define the results array
 script_lines.extend([
 "",
 "# Define the results array",
 "results = [",
 ])
 # Format results as hex for readability
 for res in results:
 script_lines.append(f" 0x{res:x},")
 script_lines.append("]")

 # Add constraints that a[i] == results[i]
 script_lines.append("")
 script_lines.append("# After all transformations, set constraints that a[i] == results[i]")
 script_lines.append("for i in range({0}):".format(input_size))
 script_lines.append(" s.add(a[i] == results[i])")

 # Add constraints for input characters to be printable ASCII (optional)
 script_lines.append("")
 script_lines.append("# Add constraints for input characters to be printable ASCII (optional)")
 script_lines.append("for c in input_vars:")
 script_lines.append(" s.add(c >= 32, c <= 126) # Printable ASCII range")

 # Add the solver check and model extraction
 script_lines.extend([
 "",
 "# Check if the constraints are satisfiable",
 "if s.check() == sat:",
 " model = s.model()",
 " # Extract the input string",
 " input_string = ''.join([chr(model[c].as_long()) for c in input_vars])",
 " print(f"Found input: {input_string}")",
 "else:",
 " print("No solution found.")",
 ""
 ])

 return 'n'.join(script_lines)

# Example usage
if __name__ == "__main__":
 cpp_transformations = """
 a[11] = a[15] + a[11] + 197 + 209;
 a[25] = (a[4] ^ (86 + a[25])) + 73;
 a[6] = (a[12] ^ 148 ^ (131 + a[6])) + 158;
 a[19] = a[23] + a[19] + 144 + 225;
 a[10] = a[23] + a[10] + 179 + 62;
 a[23] = (a[16] ^ a[23] ^ 121 ^ 187) + 180;
 a[12] = (58 ^ (a[12] + 213 + a[23])) + 174;
 a[21] = a[8] + 95 + a[21];
 a[1] = a[19] + 126 + a[1];
 a[4] = (a[17] ^ a[4] ^ (219 + 9)) + 109;
 a[22] = a[18] + 60 + a[22];
 a[14] = a[30] + a[14] + 109 + 238;
 a[18] = (a[20] ^ 72) + a[18];
 a[15] = a[24] + a[15] + 146 + 45 + 10;
 a[19] = (a[14] ^ a[19] ^ 23) + 51;
 a[14] = (140 ^ (a[14] + a[20])) + 155;
 a[21] = (a[13] ^ a[21] ^ 89) + 209;
 a[21] = a[19] + a[21] + 187 + 168;
 a[8] = a[22] + a[8] + 47 + 229;
 a[4] = (159 ^ (a[4] + a[12])) + 248;
 a[29] = (27 ^ (a[29] + 255 + a[19])) + 137;
 a[7] = a[16] + 93 + a[7];
 a[4] = (a[12] ^ 206 ^ (188 + a[4])) + 11;
 a[8] = (a[7] ^ (33 + a[8])) + 141;
 a[24] = a[11] + 178 + a[24];
 a[13] = a[8] + 35 + a[13];
 a[19] = a[23] + a[19] + 230 + 169 + 215;
 a[5] = a[27] + 201 + a[5];
 a[28] = a[19] + 107 + a[28];
 a[26] = (a[28] ^ a[26] ^ (111 + 48)) + 196;
 a[12] = (a[28] ^ 132) + a[12];
 a[0] = (a[3] ^ 163) + a[0];
 a[16] = a[3] + 117 + a[16];
 a[0] = (a[24] ^ a[0] ^ 84) + 217;
 a[19] = (a[29] ^ 211 ^ (68 + a[19])) + 217;
 a[24] = a[13] + 29 + a[24];
 a[14] = a[28] + a[14] + 117 + 37 + 228;
 a[9] = (a[22] ^ (141 + 208 + a[9])) + 62;
 a[30] = a[27] + a[30] + 202 + 90;
 a[20] = (a[8] ^ 0) + a[20];
 a[28] = (57 ^ (a[28] + a[1])) + 129;
 a[15] = a[28] + 210 + a[15];
 a[14] = (a[10] ^ (85 + 79 + a[14])) + 177;
 a[17] = a[23] + 123 + a[17];
 a[30] = a[18] + a[30] + 146 + 255;
 a[25] = a[1] + a[25] + 84 + 120;
 a[20] = (a[15] ^ (1 + 55 + a[20])) + 102;
 a[6] = (a[23] ^ (154 + a[6])) + 169;
 a[5] = (15 ^ (a[5] + a[31])) + 104;
 a[1] = (a[4] ^ 250) + a[1];
 a[18] = a[8] + a[18] + 255 + 177;
 a[15] = a[21] + a[15] + 101 + 168 + 249;
 a[0] = ((a[0] + a[30]) ^ (218 + 152)) + 128;
 a[5] = a[18] + 94 + a[5];
 a[9] = (a[0] ^ 98) + a[9];
 a[15] = (166 ^ (a[15] + 65 + a[5])) + 46;
 a[26] = a[8] + 206 + a[26];
 a[20] = a[4] + 104 + a[20];
 a[23] = a[4] + 144 + a[23];
 a[31] = a[23] + 202 + a[31];
 a[28] = a[20] + 160 + a[28];
 a[5] = a[23] + a[5] + 60 + 235 + 94;
 a[26] = a[3] + a[26] + 50 + 253;
 a[6] = (a[17] ^ (149 + a[6])) + 19;
 a[31] = a[7] + a[31] + 34 + 198;
 a[18] = (a[20] ^ a[18] ^ 35) + 249;
 a[26] = a[17] + 65 + a[26];
 a[10] = a[11] + a[10] + 237 + 142;
 a[25] = a[24] + a[25] + 247 + 167 + 7;
 a[3] = (a[17] ^ a[3] ^ 22) + 190;
 a[16] = a[25] + 234 + a[16];
 a[29] = a[7] + a[29] + 172 + 9 + 231;
 a[1] = (a[5] ^ 230) + a[1];
 a[2] = a[4] + a[2] + 152 + 55 + 51;
 a[17] = a[3] + a[17] + 252 + 161;
 a[17] = (a[11] ^ (119 + a[17])) + 212;
 a[30] = (a[9] ^ a[30] ^ 88) + 72;
 a[8] = a[10] + a[8] + 30 + 38;
 a[19] = (a[14] ^ (229 + a[19])) + 3;
 a[5] = ((a[5] + a[18]) ^ (45 + 241)) + 60;
 a[25] = a[14] + a[25] + 197 + 244;
 a[30] = a[18] + a[30] + 241 + 231;
 a[8] = (a[31] ^ a[8] ^ 226 ^ 138) + 185;
 a[18] = (a[9] ^ (7 + 154 + a[18])) + 183;
 a[2] = (a[17] ^ 138) + a[2];
 a[17] = a[12] + 173 + a[17];
 a[9] = (a[26] ^ (86 + 111 + a[9])) + 151;
 a[30] = a[3] + a[30] + 148 + 170 + 100;
 a[1] = (a[19] ^ 12) + a[1];
 a[30] = a[12] + 215 + a[30];
 a[20] = (a[25] ^ 151) + a[20];
 a[14] = a[21] + a[14] + 144 + 41;
 a[24] = (23 ^ (a[24] + a[12])) + 86;
 a[0] = (a[29] ^ 168) + a[0];
 a[13] = a[9] + 83 + a[13];
 a[7] = (177 ^ (a[7] + a[4])) + 83;
 a[14] = (146 ^ (a[14] + a[9])) + 173;
 a[27] = (30 ^ (a[27] + 72 + a[8])) + 2;
 a[13] = a[18] + 148 + a[13];
 a[19] = a[9] + 152 + a[19];
 a[27] = (238 ^ (a[27] + 140 + a[14])) + 50;
 a[17] = (a[25] ^ 148) + a[17];
 a[8] = (a[20] ^ 77) + a[8];
 a[5] = (19 ^ (a[5] + 47 + a[17])) + 238;
 a[24] = a[14] + 182 + a[24];
 a[9] = (a[31] ^ 172 ^ (27 + a[9])) + 210;
 a[6] = (a[2] ^ 211) + a[6];
 a[11] = (a[28] ^ 80) + a[11];
 a[13] = (33 ^ 12 ^ (a[13] + a[5])) + 61;
 a[22] = (231 ^ (a[22] + 178 + a[8])) + 197;
 a[1] = a[13] + 203 + a[1];
 a[9] = (72 ^ (a[9] + 215 + a[6])) + 116;
 a[30] = a[14] + 183 + a[30];
 a[25] = a[4] + a[25] + 107 + 100 + 27;
 a[4] = (a[16] ^ 19 ^ (111 + a[4])) + 235;
 a[5] = (a[15] ^ 220) + a[5];
 a[24] = ((a[24] + a[0]) ^ (60 + 163)) + 164;
 a[27] = (a[7] ^ (99 + a[27])) + 25;
 a[25] = a[28] + 163 + a[25];
 a[25] = (24 ^ (a[25] + a[4])) + 54;
 a[10] = (a[16] ^ (29 + 189 + a[10])) + 214;
 a[5] = a[21] + a[5] + 13 + 160;
 a[30] = (a[13] ^ 92 ^ (208 + a[30])) + 189;
 a[26] = (a[15] ^ a[26] ^ 246) + 93;
 a[30] = (a[7] ^ (0 + 59 + a[30])) + 72;
 a[1] = (136 ^ (a[1] + a[9])) + 111;
 a[25] = (65 ^ (a[25] + a[0])) + 98;
 a[17] = a[21] + 92 + a[17];
 a[15] = (42 ^ (a[15] + a[17])) + 1;
 a[31] = (a[4] ^ 183) + a[31];
 a[24] = a[18] + a[24] + 242 + 28;
 a[6] = a[1] + 1 + a[6];
 a[9] = (154 ^ 15 ^ (a[9] + a[10])) + 152;
 a[8] = (a[2] ^ 55) + a[8];
 a[29] = a[23] + a[29] + 250 + 46 + 255;
 a[17] = (68 ^ (a[17] + a[22])) + 165;
 a[8] = (a[5] ^ (249 + 104 + a[8])) + 0;
 a[0] = a[24] + a[0] + 53 + 224;
 a[17] = (a[1] ^ 222) + a[17];
 a[10] = (a[2] ^ a[10] ^ (82 + 98)) + 180;
 a[14] = (128 ^ (a[14] + 166 + a[1])) + 25;
 a[0] = (a[29] ^ 165) + a[0];
 a[13] = a[15] + 72 + a[13];
 a[19] = a[30] + a[19] + 36 + 59;
 a[17] = a[9] + 196 + a[17];
 a[17] = a[4] + a[17] + 160 + 96 + 183;
 a[11] = a[28] + 244 + a[11];
 a[29] = a[30] + a[29] + 87 + 189;
 a[19] = a[0] + a[19] + 149 + 162 + 99;
 a[6] = a[3] + 177 + a[6];
 a[25] = (103 ^ (a[25] + a[30])) + 162;
 a[29] = a[13] + a[29] + 148 + 8;
 a[14] = (a[15] ^ (241 + a[14])) + 17;
 a[7] = a[23] + 139 + a[7];
 a[30] = a[9] + 152 + a[30];
 a[23] = a[4] + a[23] + 113 + 54;
 a[9] = (a[12] ^ (89 + a[9])) + 79;
 a[19] = a[27] + a[19] + 230 + 189 + 39;
 a[23] = (a[24] ^ (51 + 37 + a[23])) + 147;
 a[1] = a[4] + a[1] + 252 + 224 + 196;
 a[20] = a[2] + 67 + a[20];
 a[8] = (a[13] ^ 43) + a[8];
 a[6] = (30 ^ 137 ^ (a[6] + a[7])) + 54;
 a[3] = (a[22] ^ 74) + a[3];
 a[28] = a[17] + 110 + a[28];
 a[20] = (a[9] ^ (197 + 178 + a[20])) + 141;
 a[7] = (142 ^ (a[7] + a[10])) + 230;
 a[25] = (a[2] ^ a[25] ^ 82) + 242;
 a[23] = (a[7] ^ a[23] ^ 191) + 201;
 a[11] = a[18] + a[11] + 137 + 34;
 a[8] = a[5] + a[8] + 173 + 117 + 49;
 a[23] = a[22] + a[23] + 111 + 235 + 172;
 a[10] = a[20] + 250 + a[10];
 a[27] = a[16] + a[27] + 12 + 38 + 131;
 a[28] = a[19] + a[28] + 179 + 115;
 a[23] = a[27] + 108 + a[23];
 a[9] = (144 ^ 121 ^ (a[9] + a[26])) + 23;
 a[22] = (a[31] ^ (23 + 213 + a[22])) + 108;
 a[0] = ((a[0] + a[30]) ^ (140 + 168)) + 85;
 a[19] = ((a[19] + a[27]) ^ (125 + 83)) + 129;
 a[19] = a[28] + 9 + a[19];
 a[13] = a[13] + a[13] + 228 + 182;
 a[2] = a[8] + 105 + a[2];
 a[30] = (a[10] ^ 40) + a[30];
 a[28] = (146 ^ (a[28] + a[23])) + 143;
 a[18] = (a[12] ^ (238 + 201 + a[18])) + 211;
 a[19] = a[25] + a[19] + 148 + 110 + 78;
 a[18] = a[27] + 57 + a[18];
 a[14] = a[15] + 180 + a[14];
 a[25] = (a[31] ^ (177 + a[25])) + 104;
 a[18] = (a[27] ^ 46 ^ (172 + a[18])) + 100;
 a[14] = (a[29] ^ a[14] ^ 255) + 61;
 a[8] = a[14] + a[8] + 226 + 103;
 a[29] = ((a[29] + a[1]) ^ (188 + 12)) + 164;
 a[5] = (a[18] ^ 229) + a[5];
 a[2] = a[3] + a[2] + 8 + 184;
 a[20] = a[23] + 45 + a[20];
 a[6] = (a[9] ^ a[6] ^ 230) + 243;
 a[4] = a[11] + a[4] + 174 + 101;
 a[11] = a[15] + a[11] + 19 + 124 + 68;
 a[11] = a[4] + 48 + a[11];
 a[4] = (a[3] ^ (60 + 111 + a[4])) + 172;
 a[25] = (192 ^ (a[25] + 99 + a[21])) + 128;
 a[3] = (a[20] ^ (163 + 167 + a[3])) + 48;
 a[22] = (a[19] ^ (24 + 28 + a[22])) + 160;
 a[22] = a[29] + a[22] + 189 + 51 + 68;
 a[0] = a[4] + 80 + a[0];
 a[29] = a[16] + a[29] + 117 + 142;
 a[29] = a[10] + a[29] + 141 + 137;
 a[8] = (a[0] ^ a[8] ^ 175) + 126;
 a[15] = (a[25] ^ 7) + a[15];
 a[2] = (a[18] ^ (65 + 105 + a[2])) + 60;
 a[4] = (96 ^ (a[4] + a[15])) + 47;
 a[1] = (a[27] ^ 85) + a[1];
 a[11] = a[18] + a[11] + 183 + 177 + 81;
 a[28] = (a[20] ^ (228 + a[28])) + 254;
 a[23] = (a[23] ^ 50 ^ (1 + a[23])) + 57;
 a[24] = a[26] + 1 + a[24];
 a[28] = (10 ^ (a[28] + 55 + a[15])) + 134;
 a[14] = a[26] + a[14] + 98 + 165;
 a[5] = (215 ^ (a[5] + a[31])) + 225;
 a[0] = a[25] + 86 + a[0];
 a[0] = ((a[0] + a[26]) ^ (101 + 53)) + 207;
 a[31] = (a[30] ^ 152) + a[31];
 a[20] = (a[2] ^ (65 + a[20])) + 69;
 a[25] = (194 ^ (a[25] + a[6])) + 105;
 a[19] = (a[14] ^ 65) + a[19];
 a[11] = (a[8] ^ 29) + a[11];
 a[27] = (a[16] ^ 175) + a[27];
 a[8] = a[10] + a[8] + 254 + 215;
 a[0] = (a[0] ^ 201) + a[0];
 a[18] = a[30] + 68 + a[18];
 a[29] = (a[18] ^ (60 + a[29])) + 101;
 a[2] = a[21] + 190 + a[2];
 a[11] = (a[2] ^ a[11] ^ 128) + 38;
 a[2] = a[3] + 195 + a[2];
 a[8] = (a[1] ^ (222 + a[8])) + 210;
 a[17] = a[13] + a[17] + 109 + 90;
 a[28] = a[7] + 143 + a[28];
 a[4] = (a[22] ^ 247 ^ (152 + a[4])) + 249;
 a[22] = (a[10] ^ (233 + a[22])) + 163;
 a[15] = (a[7] ^ 132) + a[15];
 a[29] = a[6] + 172 + a[29];
 a[19] = (a[19] ^ (123 + a[19])) + 225;
 a[0] = a[28] + a[0] + 152 + 34;
 a[10] = a[23] + 68 + a[10];
 a[23] = a[24] + a[23] + 130 + 17;
 a[22] = a[30] + a[22] + 137 + 254 + 141;
 a[8] = a[5] + a[8] + 74 + 232 + 71;
 a[9] = (118 ^ (a[9] + a[13])) + 115;
 a[13] = a[5] + a[13] + 241 + 101;
 a[6] = ((a[6] + a[17]) ^ (73 + 142)) + 217;
 a[18] = a[10] + a[18] + 202 + 222;
 a[9] = a[26] + a[9] + 226 + 8;
 a[2] = a[10] + 7 + a[2];
 a[21] = a[13] + 114 + a[21];
 """

 results = [
 0xd7765, 0x11ebd, 0x32d12, 0x13778, 0x8a428,
 0xb592, 0x3fa57, 0x1616, 0x3659e, 0x2483a,
 0x2882, 0x508f4, 0xbad, 0x27920, 0xf821,
 0x19f83, 0xf97, 0x33904, 0x170d5, 0x16c,
 0xcf5d, 0x280d2, 0xa8ade, 0x9eaa, 0x9dab,
 0x1f45e, 0x3214, 0x52fa, 0x6d57a, 0x460ed,
 0x124ff, 0x13936
 ]
 translated_constraints = translate_transformations(cpp_transformations)

 z3_script = generate_z3_script(translated_constraints, results, input_size=32)

 with open('z3_solver.py', 'w') as f:
 f.write(z3_script)

 print("Z3 solver script 'z3_solver.py' has been generated.")

二

SU_Harmony

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 定义最大位数，根据需要调整
#define MAX_DIGITS 5000

// 反转字符串
void reverse_str(char *str) {
 int len = strlen(str);
 for(int i=0; i<len/2; i++) {
 char temp = str[i];
 str[i] = str[len-1-i];
 str[len-1-i] = temp;
 }
}

// 大整数加法：result = num1 + num2
void add(char *num1, char *num2, char *result) {
 char a[MAX_DIGITS] = {0};
 char b[MAX_DIGITS] = {0};
 strcpy(a, num1);
 strcpy(b, num2);

 reverse_str(a);
 reverse_str(b);

 int len1 = strlen(a);
 int len2 = strlen(b);
 int maxlen = len1 > len2 ? len1 : len2;
 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<maxlen; i++) {
 int digit1 = i < len1 ? a[i] - '0' : 0;
 int digit2 = i < len2 ? b[i] - '0' : 0;
 int sum = digit1 + digit2 + carry;
 carry = sum / 10;
 sum = sum % 10;
 char temp = sum + '0';
 strncat(result, &temp, 1);
 }
 if(carry) {
 char temp = carry + '0';
 strncat(result, &temp, 1);
 }


 reverse_str(result);

 // 去除前导零
 int start = 0;
 while(result[start] == '0' && start < strlen(result)-1) {
 start++;
 }
 if(start > 0) {
 memmove(result, result + start, strlen(result) - start + 1);
 }
}

// 大整数减法：result = num1 - num2 (假设 num1 >= num2)
void subtract(char *num1, char *num2, char *result) {
 char a[MAX_DIGITS] = {0};
 char b[MAX_DIGITS] = {0};
 strcpy(a, num1);
 strcpy(b, num2);

 reverse_str(a);
 reverse_str(b);

 int len1 = strlen(a);
 int len2 = strlen(b);
 int borrow = 0;
 result[0] = ' ';

 for(int i=0; i<len1; i++) {
 int digit1 = a[i] - '0';
 int digit2 = i < len2 ? (b[i] - '0') : 0;
 int sub = digit1 - digit2 - borrow;
 if(sub < 0) {
 sub += 10;
 borrow = 1;
 }
 else {
 borrow = 0;
 }
 char temp = sub + '0';
 strncat(result, &temp, 1);
 }

 // 去除多余的0
 while(strlen(result) > 1 && result[strlen(result)-1] == '0') {
 result[strlen(result)-1] = ' ';
 }

 reverse_str(result);
}

// 大整数乘法：result = num1 * num2
void multiply(char *num1, char *num2, char *result) {
 int len1 = strlen(num1);
 int len2 = strlen(num2);
 int total_len = len1 + len2;
 int temp_result[MAX_DIGITS] = {0};

 // 从右到左计算每一位的乘积
 for(int i=len1-1; i>=0; i--) {
 for(int j=len2-1; j>=0; j--) {
 int p1 = i + j;
 int p2 = i + j + 1;
 int mul = (num1[i] - '0') * (num2[j] - '0') + temp_result[p2];
 temp_result[p2] = mul % 10;
 temp_result[p1] += mul / 10;
 }
 }

 // 构建结果字符串
 int i = 0;
 while(i < total_len && temp_result[i] == 0) i++;
 if(i == total_len) {
 strcpy(result, "0");
 return;
 }
 result[0] = ' ';
 for(; i < total_len; i++) {
 char digit = temp_result[i] + '0';
 strncat(result, &digit, 1);
 }
}

// 大整数乘以单个数字：result = num * digit
void multiply_single_digit(char *num, int digit, char *result) {
 if(digit < 0 || digit > 9) {
 strcpy(result, "0");
 return;
 }
 char a[MAX_DIGITS] = {0};
 strcpy(a, num);
 reverse_str(a);

 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<strlen(a); i++) {
 int prod = (a[i] - '0') * digit + carry;
 carry = prod / 10;
 int sum = prod % 10;
 char temp = sum + '0';
 strncat(result, &temp, 1);
 }
 if(carry) {
 char temp = carry + '0';
 strncat(result, &temp, 1);
 }

 reverse_str(result);

 // 去除前导零
 int start = 0;
 while(result[start] == '0' && start < strlen(result)-1) {
 start++;
 }
 if(start > 0) {
 memmove(result, result + start, strlen(result) - start + 1);
 }
}

// 大整数除以2：result = num / 2
void divide_by_two(char *num, char *result) {
 int len = strlen(num);
 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<len; i++) {
 int current = carry * 10 + (num[i] - '0');
 int quotient = current / 2;
 carry = current % 2;
 char temp = quotient + '0';
 // 处理前导零
 if(!(i == 0 && quotient == 0)) {
 strncat(result, &temp, 1);
 }
 }
 if(strlen(result) == 0) {
 strcpy(result, "0");
 }
}

void uint_to_dec_str(unsigned int num, char *str) {
 int i = 0;

 // 特殊情况处理：num == 0
 if(num == 0) {
 str[i++] = '0';
 str[i] = ' ';
 return;
 }

 // 逐位提取数字并存入字符串（逆序）
 while(num > 0) {
 int digit = num % 10;
 str[i++] = digit + '0';
 num /= 10;
 }

 // 添加字符串终止符
 str[i] = ' ';

 // 反转字符串以得到正确的顺序
 reverse_str(str);
 printf("input : %s",str);
}

// 检查字符串是否为有效的非负整数
int is_valid_number(char *num) {
 if(strlen(num) == 0) return 0;
 for(int i=0; i<strlen(num); i++) {
 if(num[i] < '0' || num[i] > '9') return 0;
 }
 return 1;
}

int main() {
 /*

 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[0] = 54435553
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[1] = 614d7b46
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[2] = 575f6837
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[3] = 646c726f
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[4] = 535f7349
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[5] = 33425f30
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[6] = 31747561
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[7] = 7d6c7566

 */
 char b[MAX_DIGITS];
 char b_squared[MAX_DIGITS] = {0};
 char two_b[MAX_DIGITS] = {0};
 char sum[MAX_DIGITS] = {0};
 char numerator[MAX_DIGITS] = {0};
 char final_result[MAX_DIGITS] = {0};
 unsigned int x;
 // 提示用户输入
 printf("请输入上限值 b：");
 if(scanf("%x", &x) != 1) {
 printf("输入无效，请输入一个整数。n");
 return 1;
 }
 uint_to_dec_str(x,b);

//	gets(b);
 // 输入验证
 if(!is_valid_number(b)) {
 printf("输入无效，请输入一个非负整数。n");
 return 1;
 }

 // 计算 b^2
 multiply(b, b, b_squared);
 // printf("b^2 = %sn", b_squared); // 调试用

 // 计算 2 * b
 multiply_single_digit(b, 2, two_b);
 // printf("2*b = %sn", two_b); // 调试用

 // 计算 b^2 + 2*b
 add(b_squared, two_b, sum);
 // printf("b^2 + 2*b = %sn", sum); // 调试用

 // 计算 b^2 + 2*b - 3
 subtract(sum, "3", numerator);
 // printf("b^2 + 2*b - 3 = %sn", numerator); // 调试用

 // 计算 (b^2 + 2*b - 3) / 2
 divide_by_two(numerator, final_result);

 // 输出结果
 printf("函数 f(x) = x + 1 在区间 [1, %s] 上的定积分结果为：%sn", b, final_result);

 return 0;
}

import struct
import math

# 定义加密列表（假设为十进制字符串）
encList = [
 "999272289930604998",
 "1332475531266467542",
 "1074388003071116830",
 "1419324015697459326",
 "978270870200633520",
 "369789474534896558",
 "344214162681978048",
 "2213954953857181622"
]

def solve_x(enc_num):
 """
 根据公式 f(x) = (x^2 + 2x - 3) / 2 = enc_num 反向计算 x
 """
 # 计算 8 * enc_num + 16
 val = 8 * enc_num + 16
 # 计算整数平方根
 sqrt_val = math.isqrt(val)
 # 初步计算 x_i
 x_i = (sqrt_val - 2) // 2
 # 验证 x_i 是否满足方程
 if (x_i ** 2 + 2 * x_i - 3) // 2 == enc_num:
 return x_i
 # 如果不满足，尝试 x_i + 1
 x_i += 1
 if (x_i ** 2 + 2 * x_i - 3) // 2 == enc_num:
 return x_i
 # 如果仍不满足，抛出异常
 raise ValueError(f"无法找到满足方程的 x_i 对于 enc_num={enc_num}")

# 计算所有 x_i
x_list = []
for idx, enc in enumerate(encList):
 enc_num = int(enc)
 try:
 x = solve_x(enc_num)
 x_list.append(x)
 print(f"encList[{idx}]: {enc_num}, x[{idx}]: {x}")
 
except ValueError as e:
 print(f"Error for encList[{idx}]: {e}")
 exit(1)

# 将 x_i 打包为小端字节序的4字节无符号整数
input_bytes = b''.join([struct.pack(' Bytes: {packed.hex()} -> ASCII: {ascii_chars}")

看雪ID：Shangwendada

https://bbs.kanxue.com/user-home-979679.htm

*本文为看雪论坛精华文章，由 Shangwendada 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
SU_APP
function hook_memcmp_addr() {
 var memcmp_addr = Module.findExportByName("libc.so", "fread");
 if (memcmp_addr !== null) {
 console.log("fread address: ", memcmp_addr);
 Interceptor.attach(memcmp_addr, {
 onEnter: function (args) {
 this.buffer = args[0];
 this.size = args[1];
 this.count = args[2];
 this.stream = args[3];
 },
 onLeave: function (retval) {
 if (this.count.toInt32() == 8) {
 Memory.writeByteArray(this.buffer, [0x50, 0x00, 0x00, 0x58, 0x00, 0x02, 0x1f, 0xd6]);
 retval.replace(8);
 }
 }
 });
 } else {

 }
}
function Hookdlopenext() {
 hook_memcmp_addr()

 var dlopen = Module.findExportByName(null, "android_dlopen_ext");
 Interceptor.attach(dlopen, {
 onEnter: function (args) {
 var filePath = args[0].readCString();

 if (filePath.indexOf("suapp") != -1) {
 this.isCanHook = true;

 }
 }, onLeave: function (retValue) {
 if (this.isCanHook) {
 this.isCanHook = false;
 NativeHook();

 }
 }
 })
}

setImmediate(Hookdlopenext);
function dump_so(so_name) {
 var libso = Process.getModuleByName(so_name);
 console.log("[name]:", libso.name);
 console.log("[base]:", libso.base);
 console.log("[size]:", ptr(libso.size));
 console.log("[path]:", libso.path);
 var file_path = "/sdcard/Download/" + libso.name + "_" + libso.base + "_" + ptr(libso.size) + ".so";
 var file_handle = new File(file_path, "wb");
 if (file_handle && file_handle != null) {
 Memory.protect(ptr(libso.base), libso.size, 'rwx');
 var libso_buffer = ptr(libso.base).readByteArray(libso.size);
 file_handle.write(libso_buffer);
 file_handle.flush();
 file_handle.close();
 console.log("[dump]:", file_path);
 }

}
addr = 0x4D2D0
for i in range(addr,addr + 0x40):
 print(hex(get_wide_byte(i)^0x3c),end=" ")
addr = 0x4D0D0
for i in range(addr,addr + 0x40):
 print(hex(get_wide_byte(i)),end=" ")
.SoFixer-Windows-64.exe -s .libsuapp.so_0x7d248e7000_0x25000.so -o libsuapp.sofix -m 0x7d248e7000 -d
typedef int (*Func1)(int, int, int);
typedef int (*Func2)(int, int, int, int);
typedef int (*Func3)(int, int, int, int, int);

typedef struct {
 union {
 Func1 func1; // Function with 1 parameter
 Func2 func2; // Function with 2 parameters
 Func3 func3; // Function with 3 parameters
 } func;
 int param_count; // Number of parameters
} OperationFunction;
function NativeHook() {
 var base = Module.getBaseAddress("libsuapp.so");
 console.log("[Base]->", base);
 Interceptor.attach(base.add("0xA158"), {
 onEnter: function (args) {

 },
 onLeave: function (retval) {
 randcode.push(retval.toInt32())
 }
 });
 Interceptor.attach(base.add("0x9FA8"), {
 onEnter: function (args) {
 console.log(randcode);

 console.log(randcode.length);
 while (randcode.length) {
 randcode.pop();
 }
 },
 onLeave: function (retval) {


 }
 });
}
function hook_memcmp_addr() {
 var memcmp_addr = Module.findExportByName("libc.so", "fread");
 if (memcmp_addr !== null) {
 console.log("fread address: ", memcmp_addr);
 Interceptor.attach(memcmp_addr, {
 onEnter: function (args) {
 this.buffer = args[0];
 this.size = args[1];
 this.count = args[2];
 this.stream = args[3];
 },
 onLeave: function (retval) {
 if (this.count.toInt32() == 8) {
 Memory.writeByteArray(this.buffer, [0x50, 0x00, 0x00, 0x58, 0x00, 0x02, 0x1f, 0xd6]);
 retval.replace(8);
 }
 }
 });
 } else {

 }
}

var randcode = [];
function dump_so(so_name) {
 var libso = Process.getModuleByName(so_name);
 console.log("[name]:", libso.name);
 console.log("[base]:", libso.base);
 console.log("[size]:", ptr(libso.size));
 console.log("[path]:", libso.path);
 var file_path = "/sdcard/Download/" + libso.name + "_" + libso.base + "_" + ptr(libso.size) + ".so";
 var file_handle = new File(file_path, "wb");
 if (file_handle && file_handle != null) {
 Memory.protect(ptr(libso.base), libso.size, 'rwx');
 var libso_buffer = ptr(libso.base).readByteArray(libso.size);
 file_handle.write(libso_buffer);
 file_handle.flush();
 file_handle.close();
 console.log("[dump]:", file_path);
 }

}

function NativeHook() {
 var base = Module.getBaseAddress("libsuapp.so");
 console.log("[Base]->", base);
 Interceptor.attach(base.add("0xA158"), {
 onEnter: function (args) {

 },
 onLeave: function (retval) {
 randcode.push(retval.toInt32())
 }
 });
 Interceptor.attach(base.add("0x9FA8"), {
 onEnter: function (args) {
 console.log(randcode);

 console.log(randcode.length);
 while (randcode.length) {
 randcode.pop();
 }
 },
 onLeave: function (retval) {


 }
 });



}

function Hookdlopenext() {
 hook_memcmp_addr()

 var dlopen = Module.findExportByName(null, "android_dlopen_ext");
 Interceptor.attach(dlopen, {
 onEnter: function (args) {
 var filePath = args[0].readCString();

 if (filePath.indexOf("suapp") != -1) {
 this.isCanHook = true;

 }
 }, onLeave: function (retValue) {
 if (this.isCanHook) {
 this.isCanHook = false;
 NativeHook();

 }
 }
 })
}

setImmediate(Hookdlopenext);
import idautils
import idc
import idaapi

def rename_functions(start_name, num_funcs, prefix='func_'):
 """
 从指定函数开始，批量重命名后续函数。

 Args:
 start_name (str): 起始函数的名称。
 num_funcs (int): 要重命名的函数数量。
 prefix (str): 新函数名称的前缀。
 """
 # 获取起始函数的地址
 start_ea = idc.get_name_ea_simple(start_name)
 if start_ea == idc.BADADDR:
 print("错误: 未找到名称为 '{}' 的函数。".format(start_name))
 return

 # 获取所有函数地址并排序
 functions = list(idautils.Functions())
 functions = sorted(functions)

 # 查找起始函数在函数列表中的索引
 try:
 start_index = functions.index(start_ea)
 
except ValueError:
 print("错误: 起始函数地址未在函数列表中找到。")
 return

 # 检查是否有足够的函数进行重命名
 if start_index + num_funcs > len(functions):
 print("警告: 函数数量不足，最多只能重命名 {} 个函数。".format(len(functions) - start_index))
 num_funcs = len(functions) - start_index

 # 执行批量重命名
 for i in range(num_funcs):
 func_ea = functions[start_index + i]
 old_name = idc.get_func_name(func_ea)
 new_name = "{}{}".format(prefix, i)

 # 尝试重命名函数
 success = idc.set_name(func_ea, new_name, idc.SN_NOWARN)
 if success:
 print("成功: 将函数 0x{:X} ('{}') 重命名为 '{}'。".format(func_ea, old_name, new_name))
 else:
 print("失败: 无法将函数 0x{:X} ('{}') 重命名为 '{}'。".format(func_ea, old_name, new_name))

def main():
 start_func_name = "sub_A224" # 起始函数名称，根据需要修改
 number_of_functions = 256 # 要重命名的函数数量
 prefix = "func_" # 新函数名称的前缀

 rename_functions(start_func_name, number_of_functions, prefix)

if __name__ == "__main__":
 main()
import idaapi
import idautils
import hashlib
import re # 导入正则表达式模块

# 获取函数的字节码（字节序列）
def get_function_bytes(func_start):
 func = idaapi.get_func(func_start)
 func_end = func.end_ea # 使用 end_ea 获取函数结束地址
 func_bytes = bytearray()
 for addr in range(func_start, func_end):
 func_bytes.append(idaapi.get_byte(addr)) # 使用 idaapi.get_byte 获取字节
 return func_bytes

# 计算字节码的哈希值作为相似度的度量
def get_function_hash(func_start):
 func_bytes = get_function_bytes(func_start)
 return hashlib.md5(func_bytes).hexdigest()

# 获取所有符合条件（__Z8func_*）函数的哈希值，并提取数字
def get_all_functions():
 functions = {}
 func_pattern = re.compile(r'func_(d+)') # 修改正则表达式，匹配 __Z8func_ 后面跟数字
 for func_start in idautils.Functions():
 func_name = idaapi.get_func_name(func_start)
 # 检查函数名是否符合 "__Z8func_*" 格式
 match = func_pattern.search(func_name)
 if match:
 func_number = int(match.group(1)) # 提取函数名中的数字部分
 func_hash = get_function_hash(func_start) # 计算哈希值
 if func_hash not in functions:
 functions[func_hash] = [] # 如果没有该哈希的组，则创建一个新组
 functions[func_hash].append(func_number) # 将函数的数字加入对应哈希的组中
 return functions

# 输出相同哈希的函数数字组

def print_functions_by_hash(functions):
 count = 1
 for func_hash, func_numbers in functions.items():
 # 输出哈希值和对应的数字数组3
 print(f"type{count}: {sorted(func_numbers)}")
 count += 1

# 主函数
def main():
 functions = get_all_functions() # 获取所有函数并按哈希分组
 print_functions_by_hash(functions) # 输出按哈希分组的数字数组

# 运行主函数
if __name__ == "__main__":
 main()
    #include 
using namespace std;

// 各种类型的操作函数
void type1(int a1, int a2, int a3, int a4) {
 // a4 + a3 + a1 + a2;
 printf("a[%d] = a[%d] + a[%d] + %d + %d;n", a3, a4, a3, a1, a2);
}

void type2(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ (a3 + a1 + a4)) + a2
 printf("a[%d] = (a[%d] ^ (%d + %d + a[%d])) + %d;n", a4, a5, a3, a1, a4, a2);
}

void type3(int a1, int a2, int a3, int a4, int a5) {
 // a5 + a4 + a3 + a1 + a2
 printf("a[%d] = a[%d] + a[%d] + %d + %d + %d;n", a4, a5, a4, a3, a2, a1);
}

void type4(int a1, int a2, int a3) {
 // (a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ %d) + a[%d];n", a2, a3, a1, a2);
}

void type5(int a1, int a2, int a3, int a4) {
 // (a1 ^ (a3 + a4)) + a2
 printf("a[%d] = (%d ^ (a[%d] + a[%d])) + %d;n", a3, a1, a3, a4, a2);
}

void type6(int a1, int a2, int a3, int a4) {
 // (a4 ^ a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ %d) + %d;n", a3, a4, a3, a1, a2);
}

void type7(int a1, int a2, int a3, int a4) {
 // (a4 ^ (a1 + a3)) + a2;
 printf("a[%d] = (a[%d] ^ (%d + a[%d])) + %d;n", a3, a4, a1, a3, a2);
}

void type8(int a1, int a2, int a3) {
 // a3 + a1 + a2;
 printf("a[%d] = a[%d] + %d + a[%d];n", a2, a3, a1, a2);
}

void type9(int a1, int a2, int a3, int a4, int a5) {
 // (a3 ^ a1 ^ (a4 + a5)) + a2
 printf("a[%d] = (%d ^ %d ^ (a[%d] + a[%d])) + %d;n", a4, a3, a1, a4, a5, a2);
}

void type10(int a1, int a2, int a3, int a4, int a5) {
 // (a1 ^ (a4 + a3 + a5)) + a2;
 printf("a[%d] = (%d ^ (a[%d] + %d + a[%d])) + %d;n", a4, a1, a4, a3, a5, a2);
}

void type11(int a1, int a2, int a3, int a4, int a5) {
 // ((a4 + a5) ^ (a1 + a3)) + a2;
 printf("a[%d] = ((a[%d] + a[%d]) ^ (%d + %d)) + %d;n", a4, a4, a5, a1, a3, a2);
}

void type12(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a4 ^ a3 ^ a1) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ %d ^ %d) + %d;n", a4, a5, a4, a3, a1, a2);
}

void type13(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a1 ^ (a3 + a4)) + a2;
 printf("a[%d] = (a[%d] ^ %d ^ (%d + a[%d])) + %d;n", a4, a5, a1, a3, a4, a2);
}

void type14(int a1, int a2, int a3, int a4, int a5) {
 // (a5 ^ a4 ^ (a1 + a3)) + a2;
 printf("a[%d] = (a[%d] ^ a[%d] ^ (%d + %d)) + %d;n", a4, a5, a4, a1, a3, a2);
}

vector type1e = {0, 2, 11, 12, 15, 21, 26, 28, 39, 44, 53, 57, 62, 63, 72, 74, 77, 81, 90, 94, 97, 108, 113, 118, 121, 122, 125, 142, 144, 145, 151, 161, 162, 166, 181, 183, 185, 192, 199, 203, 215, 226, 230, 238, 242, 244, 247};
vector type21 = {1, 5, 34, 49, 84, 93, 130, 152, 154, 155, 207, 216, 217};
vector type31 = {3, 20, 24, 38, 42, 64, 70, 71, 73, 82, 124, 132, 176, 189, 196, 209, 220, 223, 224, 225, 237, 255};
vector type41 = {4, 9, 10, 14, 22, 23, 25, 31, 32, 33, 45, 69, 92, 99, 103, 111, 115, 117, 129, 147, 149, 150, 156, 164, 165, 172, 175, 241, 250, 254};
vector type51 = {6, 7, 29, 46, 47, 51, 60, 65, 76, 80, 85, 88, 98, 177, 182, 193, 208, 210, 221, 222, 236};
vector type61 = {8, 50, 54, 89, 126, 133, 198, 219, 240};
vector type71 = {13, 48, 55, 106, 119, 120, 127, 148, 170, 171, 197, 218, 233, 248, 252, 253};
vector type81 = {16, 17, 19, 30, 35, 36, 37, 43, 56, 59, 67, 68, 78, 79, 96, 100, 101, 107, 112, 114, 116, 123, 131, 135, 138, 139, 143, 158, 159, 160, 163, 167, 168, 169, 173, 178, 180, 188, 191, 194, 195, 204, 205, 211, 212, 227, 228, 229, 234, 235, 245, 249, 251};
vector type91 = {18, 134, 136, 140, 174, 213, 232};
vector type101 = {27, 58, 86, 104, 110, 146, 157, 179, 184, 202, 239, 243, 246};
vector type111 = {40, 52, 66, 95, 109, 128, 141, 153, 206, 231};
vector type121 = {41, 87, 200, 201};
vector type131 = {61, 91, 102, 137, 186, 187, 190, 214};
vector type141 = {75, 83, 105};

// 类型查找函数，根据opcode选择对应的类型
int getType(int opcode) {
 if (find(type1e.begin(), type1e.end(), opcode) != type1e.end()) return 1;
 if (find(type21.begin(), type21.end(), opcode) != type21.end()) return 2;
 if (find(type31.begin(), type31.end(), opcode) != type31.end()) return 3;
 if (find(type41.begin(), type41.end(), opcode) != type41.end()) return 4;
 if (find(type51.begin(), type51.end(), opcode) != type51.end()) return 5;
 if (find(type61.begin(), type61.end(), opcode) != type61.end()) return 6;
 if (find(type71.begin(), type71.end(), opcode) != type71.end()) return 7;
 if (find(type81.begin(), type81.end(), opcode) != type81.end()) return 8;
 if (find(type91.begin(), type91.end(), opcode) != type91.end()) return 9;
 if (find(type101.begin(), type101.end(), opcode) != type101.end()) return 10;
 if (find(type111.begin(), type111.end(), opcode) != type111.end()) return 11;
 if (find(type121.begin(), type121.end(), opcode) != type121.end()) return 12;
 if (find(type131.begin(), type131.end(), opcode) != type131.end()) return 13;
 if (find(type141.begin(), type141.end(), opcode) != type141.end()) return 14;
 return -1; // 未找到类型
}

unsigned char opcode[9999] = {

 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168, 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168, 197, 209, 172, 235, 111, 151, 86, 73, 250, 217, 100, 170, 148, 158, 131, 38, 12, 91, 144, 225, 179, 115, 215, 28, 179, 62, 108, 138, 151, 151, 187, 180, 121, 23, 144, 41, 58, 174, 213, 108, 23, 86, 95, 152, 140, 85, 168, 160, 126, 128, 125, 129, 83, 19, 219, 109, 9, 68, 177, 83, 60, 167, 228, 182, 146, 173, 109, 238, 105, 46, 30, 2, 72, 123, 40, 146, 148, 254, 10, 45, 146, 143, 152, 220, 23, 51, 201, 211, 238, 50, 140, 155, 78, 110, 148, 51, 89, 209, 57, 149, 77, 50, 187, 168, 180, 117, 19, 238, 47, 229, 177, 104, 182, 57, 159, 248, 46, 100, 172, 210, 27, 137, 255, 61, 211, 110, 93, 198, 226, 103, 80, 168, 206, 11, 188, 164, 12, 61, 33, 141, 229, 136, 231, 197, 178, 150, 8, 184, 203, 194, 35, 97, 45, 205, 72, 116, 215, 169, 230, 243, 183, 38, 201, 126, 174, 101, 27, 100, 107, 185, 68, 124, 19, 235, 111, 196, 48, 186, 220, 75, 132, 101, 111, 172, 60, 164, 163, 152, 192, 128, 99, 25, 117, 27, 167, 48, 163, 227, 84, 217, 28, 160, 24, 54, 211, 217, 68, 51, 189, 214, 29, 42, 80, 152, 13, 160, 228, 37, 117, 142, 92, 189, 208, 62, 141, 137, 246, 93, 202, 90, 175, 126, 59, 72, 0, 126, 7, 84, 136, 111, 57, 129, 105, 60, 65, 98, 210, 217, 96, 47, 92, 68, 79, 177, 85, 78, 42, 1, 123, 175, 81, 177, 183, 139, 146, 255, 228, 254, 242, 28, 84, 120, 50, 57, 1, 183, 55, 102, 1, 212, 15, 152, 154, 169, 10, 134, 55, 252, 15, 104, 98, 165, 255, 46, 250, 125, 215, 225, 68, 165, 255, 177, 86, 210, 104, 0, 249, 168, 101, 207, 53, 224, 218, 128, 152, 0, 222, 95, 94, 241, 65, 69, 82, 180, 98, 170, 194, 105, 128, 25, 166, 46, 65, 239, 165, 179, 206, 32, 29, 250, 72, 107, 104, 45, 175, 116, 36, 59, 144, 115, 254, 215, 196, 168, 202, 81, 201, 191, 183, 96, 160, 241, 68, 220, 244, 114, 94, 235, 60, 101, 87, 189, 50, 253, 190, 122, 99, 162, 149, 19, 128, 38, 177, 171, 34, 198, 195, 159, 103, 162, 35, 249, 222, 210, 148, 8, 65, 253, 109, 90, 241, 17, 237, 142, 143, 106, 139, 28, 7, 167, 247, 249, 152, 132, 22, 190, 233, 163, 113, 54, 234, 119, 132, 144, 89, 79, 231, 9, 172, 253, 39, 189, 230, 211, 123, 225, 37, 147, 51, 55, 152, 34, 196, 224, 252, 161, 68, 209, 67, 74, 119, 212, 130, 17, 43, 55, 88, 72, 141, 254, 137, 54, 30, 38, 71, 232, 74, 72, 229, 3, 118, 115, 110, 233, 45, 60, 241, 101, 178, 141, 197, 244, 73, 217, 142, 230, 241, 231, 202, 222, 82, 242, 138, 185, 226, 8, 191, 201, 154, 183, 7, 50, 137, 34, 138, 139, 114, 162, 49, 117, 173, 168

};

int main() {

 for (int i = 0; i < 1536; i += 6) {
 int a = opcode[i], b = opcode[i + 1], c = opcode[i + 2];
 int indexA = opcode[i + 3] % 32;
 int indexB = opcode[i + 4] % 32;
 int logic = opcode[i + 5];
 switch (getType(logic)) {
 case 1:
 type1(a, b, indexA, indexB);
 break;
 case 2:
 type2(a, b, c, indexA, indexB);
 break;
 case 3:
 type3(a, b, c, indexA, indexB);
 break;
 case 4:
 type4(a, indexA, indexB);
 break;
 case 5:
 type5(a, b, indexA, indexB);
 break;
 case 6:
 type6(a, b, indexA, indexB);
 break;
 case 7:
 type7(a, b, indexA, indexB);
 break;
 case 8:
 type8(a, indexA, indexB);
 break;
 case 9:
 type9(a, b, c, indexA, indexB);
 break;
 case 10:
 type10(a, b, c, indexA, indexB);
 break;
 case 11:
 type11(a, b, c, indexA, indexB);
 break;
 case 12:
 type12(a, b, c, indexA, indexB);
 break;
 case 13:
 type13(a, b, c, indexA, indexB);
 break;
 case 14:
 type14(a, b, c, indexA, indexB);
 break;
 default:
 cout << "Unknown logic type: " << logic << endl;
 }
 }
}
import re
from z3 import *

def translate_transformation(line):
 """
 Translates a single C++ transformation line into a Python Z3 constraint.

 Args:
 line (str): A line of C++ code representing a transformation.

 Returns:
 str: A line of Python code formatted for Z3.
 """
 # Remove any trailing semicolon and whitespace
 line = line.strip().rstrip(';')

 # Match the pattern a[index] = expression
 match = re.match(r'a[(d+)]s*=s*(.+)', line)
 if not match:
 raise ValueError(f"Invalid transformation line: {line}")

 index = match.group(1)
 expression = match.group(2)

 # Function to replace integers with BitVecVal(x, 32), excluding indices in a[index]
 def replace_int_literals(match):
 num = match.group(0)
 # If the number is part of 'a[number]', return as is
 if match.group(1):
 return num
 else:
 return f'BitVecVal({num}, 32)'

 # Regular expression to find integer literals not preceded by 'a['
 # This uses a negative lookbehind to ensure numbers inside a[...] are not matched
 int_literal_pattern = re.compile(r'(?<!a[)b(0x[0-9a-fA-F]+|d+)b')

 # Replace all integer literals not inside a[...] with BitVecVal(x, 32)
 processed_expression = int_literal_pattern.sub(replace_int_literals, expression)

 # Construct the Python assignment statement
 python_line = f'a[{index}] = {processed_expression}'

 return python_line

def translate_transformations(cpp_transformations):
 """
 Translates multiple C++ transformation lines into Python Z3 constraints.

 Args:
 cpp_transformations (str): Multiline string of C++ transformation lines.

 Returns:
 list: List of Python Z3 constraint lines.
 """
 python_constraints = []
 for line in cpp_transformations.strip().split('n'):
 # Remove comments
 line = line.split('//')[0]
 # Skip empty lines or lines that do not contain transformations
 if not line.strip() or not line.strip().startswith('a['):
 continue
 python_line = translate_transformation(line)
 python_constraints.append(python_line)
 return python_constraints

def generate_z3_script(transformation_constraints, results, input_size=32):
 """
 Generates the complete Z3 Python script with the given constraints.

 Args:
 transformation_constraints (list): List of Python Z3 constraint lines.
 results (list): List of expected result values.
 input_size (int): Size of the input array.

 Returns:
 str: The complete Python Z3 script as a string.
 """
 script_lines = [
 "from z3 import *",
 "",
 "# Initialize Z3 solver",
 "s = Solver()",
 "",
 "# Define input characters as 8-bit BitVec variables",
 f"input_vars = [BitVec(f'c{{i}}', 8) for i in range({input_size})]",
 "",
 "# Initialize array 'a' with {0} elements, initially set to input characters".format(input_size),
 f"a = [ZeroExt(24, input_vars[i]) for i in range({input_size})]",
 "",
 "# Translated Python Z3 Constraints"
 ]

 # Add transformation constraints
 for constraint in transformation_constraints:
 script_lines.append(constraint)

 # Define the results array
 script_lines.extend([
 "",
 "# Define the results array",
 "results = [",
 ])
 # Format results as hex for readability
 for res in results:
 script_lines.append(f" 0x{res:x},")
 script_lines.append("]")

 # Add constraints that a[i] == results[i]
 script_lines.append("")
 script_lines.append("# After all transformations, set constraints that a[i] == results[i]")
 script_lines.append("for i in range({0}):".format(input_size))
 script_lines.append(" s.add(a[i] == results[i])")

 # Add constraints for input characters to be printable ASCII (optional)
 script_lines.append("")
 script_lines.append("# Add constraints for input characters to be printable ASCII (optional)")
 script_lines.append("for c in input_vars:")
 script_lines.append(" s.add(c >= 32, c <= 126) # Printable ASCII range")

 # Add the solver check and model extraction
 script_lines.extend([
 "",
 "# Check if the constraints are satisfiable",
 "if s.check() == sat:",
 " model = s.model()",
 " # Extract the input string",
 " input_string = ''.join([chr(model[c].as_long()) for c in input_vars])",
 " print(f"Found input: {input_string}")",
 "else:",
 " print("No solution found.")",
 ""
 ])

 return 'n'.join(script_lines)

# Example usage
if __name__ == "__main__":
 cpp_transformations = """
 a[11] = a[15] + a[11] + 197 + 209;
 a[25] = (a[4] ^ (86 + a[25])) + 73;
 a[6] = (a[12] ^ 148 ^ (131 + a[6])) + 158;
 a[19] = a[23] + a[19] + 144 + 225;
 a[10] = a[23] + a[10] + 179 + 62;
 a[23] = (a[16] ^ a[23] ^ 121 ^ 187) + 180;
 a[12] = (58 ^ (a[12] + 213 + a[23])) + 174;
 a[21] = a[8] + 95 + a[21];
 a[1] = a[19] + 126 + a[1];
 a[4] = (a[17] ^ a[4] ^ (219 + 9)) + 109;
 a[22] = a[18] + 60 + a[22];
 a[14] = a[30] + a[14] + 109 + 238;
 a[18] = (a[20] ^ 72) + a[18];
 a[15] = a[24] + a[15] + 146 + 45 + 10;
 a[19] = (a[14] ^ a[19] ^ 23) + 51;
 a[14] = (140 ^ (a[14] + a[20])) + 155;
 a[21] = (a[13] ^ a[21] ^ 89) + 209;
 a[21] = a[19] + a[21] + 187 + 168;
 a[8] = a[22] + a[8] + 47 + 229;
 a[4] = (159 ^ (a[4] + a[12])) + 248;
 a[29] = (27 ^ (a[29] + 255 + a[19])) + 137;
 a[7] = a[16] + 93 + a[7];
 a[4] = (a[12] ^ 206 ^ (188 + a[4])) + 11;
 a[8] = (a[7] ^ (33 + a[8])) + 141;
 a[24] = a[11] + 178 + a[24];
 a[13] = a[8] + 35 + a[13];
 a[19] = a[23] + a[19] + 230 + 169 + 215;
 a[5] = a[27] + 201 + a[5];
 a[28] = a[19] + 107 + a[28];
 a[26] = (a[28] ^ a[26] ^ (111 + 48)) + 196;
 a[12] = (a[28] ^ 132) + a[12];
 a[0] = (a[3] ^ 163) + a[0];
 a[16] = a[3] + 117 + a[16];
 a[0] = (a[24] ^ a[0] ^ 84) + 217;
 a[19] = (a[29] ^ 211 ^ (68 + a[19])) + 217;
 a[24] = a[13] + 29 + a[24];
 a[14] = a[28] + a[14] + 117 + 37 + 228;
 a[9] = (a[22] ^ (141 + 208 + a[9])) + 62;
 a[30] = a[27] + a[30] + 202 + 90;
 a[20] = (a[8] ^ 0) + a[20];
 a[28] = (57 ^ (a[28] + a[1])) + 129;
 a[15] = a[28] + 210 + a[15];
 a[14] = (a[10] ^ (85 + 79 + a[14])) + 177;
 a[17] = a[23] + 123 + a[17];
 a[30] = a[18] + a[30] + 146 + 255;
 a[25] = a[1] + a[25] + 84 + 120;
 a[20] = (a[15] ^ (1 + 55 + a[20])) + 102;
 a[6] = (a[23] ^ (154 + a[6])) + 169;
 a[5] = (15 ^ (a[5] + a[31])) + 104;
 a[1] = (a[4] ^ 250) + a[1];
 a[18] = a[8] + a[18] + 255 + 177;
 a[15] = a[21] + a[15] + 101 + 168 + 249;
 a[0] = ((a[0] + a[30]) ^ (218 + 152)) + 128;
 a[5] = a[18] + 94 + a[5];
 a[9] = (a[0] ^ 98) + a[9];
 a[15] = (166 ^ (a[15] + 65 + a[5])) + 46;
 a[26] = a[8] + 206 + a[26];
 a[20] = a[4] + 104 + a[20];
 a[23] = a[4] + 144 + a[23];
 a[31] = a[23] + 202 + a[31];
 a[28] = a[20] + 160 + a[28];
 a[5] = a[23] + a[5] + 60 + 235 + 94;
 a[26] = a[3] + a[26] + 50 + 253;
 a[6] = (a[17] ^ (149 + a[6])) + 19;
 a[31] = a[7] + a[31] + 34 + 198;
 a[18] = (a[20] ^ a[18] ^ 35) + 249;
 a[26] = a[17] + 65 + a[26];
 a[10] = a[11] + a[10] + 237 + 142;
 a[25] = a[24] + a[25] + 247 + 167 + 7;
 a[3] = (a[17] ^ a[3] ^ 22) + 190;
 a[16] = a[25] + 234 + a[16];
 a[29] = a[7] + a[29] + 172 + 9 + 231;
 a[1] = (a[5] ^ 230) + a[1];
 a[2] = a[4] + a[2] + 152 + 55 + 51;
 a[17] = a[3] + a[17] + 252 + 161;
 a[17] = (a[11] ^ (119 + a[17])) + 212;
 a[30] = (a[9] ^ a[30] ^ 88) + 72;
 a[8] = a[10] + a[8] + 30 + 38;
 a[19] = (a[14] ^ (229 + a[19])) + 3;
 a[5] = ((a[5] + a[18]) ^ (45 + 241)) + 60;
 a[25] = a[14] + a[25] + 197 + 244;
 a[30] = a[18] + a[30] + 241 + 231;
 a[8] = (a[31] ^ a[8] ^ 226 ^ 138) + 185;
 a[18] = (a[9] ^ (7 + 154 + a[18])) + 183;
 a[2] = (a[17] ^ 138) + a[2];
 a[17] = a[12] + 173 + a[17];
 a[9] = (a[26] ^ (86 + 111 + a[9])) + 151;
 a[30] = a[3] + a[30] + 148 + 170 + 100;
 a[1] = (a[19] ^ 12) + a[1];
 a[30] = a[12] + 215 + a[30];
 a[20] = (a[25] ^ 151) + a[20];
 a[14] = a[21] + a[14] + 144 + 41;
 a[24] = (23 ^ (a[24] + a[12])) + 86;
 a[0] = (a[29] ^ 168) + a[0];
 a[13] = a[9] + 83 + a[13];
 a[7] = (177 ^ (a[7] + a[4])) + 83;
 a[14] = (146 ^ (a[14] + a[9])) + 173;
 a[27] = (30 ^ (a[27] + 72 + a[8])) + 2;
 a[13] = a[18] + 148 + a[13];
 a[19] = a[9] + 152 + a[19];
 a[27] = (238 ^ (a[27] + 140 + a[14])) + 50;
 a[17] = (a[25] ^ 148) + a[17];
 a[8] = (a[20] ^ 77) + a[8];
 a[5] = (19 ^ (a[5] + 47 + a[17])) + 238;
 a[24] = a[14] + 182 + a[24];
 a[9] = (a[31] ^ 172 ^ (27 + a[9])) + 210;
 a[6] = (a[2] ^ 211) + a[6];
 a[11] = (a[28] ^ 80) + a[11];
 a[13] = (33 ^ 12 ^ (a[13] + a[5])) + 61;
 a[22] = (231 ^ (a[22] + 178 + a[8])) + 197;
 a[1] = a[13] + 203 + a[1];
 a[9] = (72 ^ (a[9] + 215 + a[6])) + 116;
 a[30] = a[14] + 183 + a[30];
 a[25] = a[4] + a[25] + 107 + 100 + 27;
 a[4] = (a[16] ^ 19 ^ (111 + a[4])) + 235;
 a[5] = (a[15] ^ 220) + a[5];
 a[24] = ((a[24] + a[0]) ^ (60 + 163)) + 164;
 a[27] = (a[7] ^ (99 + a[27])) + 25;
 a[25] = a[28] + 163 + a[25];
 a[25] = (24 ^ (a[25] + a[4])) + 54;
 a[10] = (a[16] ^ (29 + 189 + a[10])) + 214;
 a[5] = a[21] + a[5] + 13 + 160;
 a[30] = (a[13] ^ 92 ^ (208 + a[30])) + 189;
 a[26] = (a[15] ^ a[26] ^ 246) + 93;
 a[30] = (a[7] ^ (0 + 59 + a[30])) + 72;
 a[1] = (136 ^ (a[1] + a[9])) + 111;
 a[25] = (65 ^ (a[25] + a[0])) + 98;
 a[17] = a[21] + 92 + a[17];
 a[15] = (42 ^ (a[15] + a[17])) + 1;
 a[31] = (a[4] ^ 183) + a[31];
 a[24] = a[18] + a[24] + 242 + 28;
 a[6] = a[1] + 1 + a[6];
 a[9] = (154 ^ 15 ^ (a[9] + a[10])) + 152;
 a[8] = (a[2] ^ 55) + a[8];
 a[29] = a[23] + a[29] + 250 + 46 + 255;
 a[17] = (68 ^ (a[17] + a[22])) + 165;
 a[8] = (a[5] ^ (249 + 104 + a[8])) + 0;
 a[0] = a[24] + a[0] + 53 + 224;
 a[17] = (a[1] ^ 222) + a[17];
 a[10] = (a[2] ^ a[10] ^ (82 + 98)) + 180;
 a[14] = (128 ^ (a[14] + 166 + a[1])) + 25;
 a[0] = (a[29] ^ 165) + a[0];
 a[13] = a[15] + 72 + a[13];
 a[19] = a[30] + a[19] + 36 + 59;
 a[17] = a[9] + 196 + a[17];
 a[17] = a[4] + a[17] + 160 + 96 + 183;
 a[11] = a[28] + 244 + a[11];
 a[29] = a[30] + a[29] + 87 + 189;
 a[19] = a[0] + a[19] + 149 + 162 + 99;
 a[6] = a[3] + 177 + a[6];
 a[25] = (103 ^ (a[25] + a[30])) + 162;
 a[29] = a[13] + a[29] + 148 + 8;
 a[14] = (a[15] ^ (241 + a[14])) + 17;
 a[7] = a[23] + 139 + a[7];
 a[30] = a[9] + 152 + a[30];
 a[23] = a[4] + a[23] + 113 + 54;
 a[9] = (a[12] ^ (89 + a[9])) + 79;
 a[19] = a[27] + a[19] + 230 + 189 + 39;
 a[23] = (a[24] ^ (51 + 37 + a[23])) + 147;
 a[1] = a[4] + a[1] + 252 + 224 + 196;
 a[20] = a[2] + 67 + a[20];
 a[8] = (a[13] ^ 43) + a[8];
 a[6] = (30 ^ 137 ^ (a[6] + a[7])) + 54;
 a[3] = (a[22] ^ 74) + a[3];
 a[28] = a[17] + 110 + a[28];
 a[20] = (a[9] ^ (197 + 178 + a[20])) + 141;
 a[7] = (142 ^ (a[7] + a[10])) + 230;
 a[25] = (a[2] ^ a[25] ^ 82) + 242;
 a[23] = (a[7] ^ a[23] ^ 191) + 201;
 a[11] = a[18] + a[11] + 137 + 34;
 a[8] = a[5] + a[8] + 173 + 117 + 49;
 a[23] = a[22] + a[23] + 111 + 235 + 172;
 a[10] = a[20] + 250 + a[10];
 a[27] = a[16] + a[27] + 12 + 38 + 131;
 a[28] = a[19] + a[28] + 179 + 115;
 a[23] = a[27] + 108 + a[23];
 a[9] = (144 ^ 121 ^ (a[9] + a[26])) + 23;
 a[22] = (a[31] ^ (23 + 213 + a[22])) + 108;
 a[0] = ((a[0] + a[30]) ^ (140 + 168)) + 85;
 a[19] = ((a[19] + a[27]) ^ (125 + 83)) + 129;
 a[19] = a[28] + 9 + a[19];
 a[13] = a[13] + a[13] + 228 + 182;
 a[2] = a[8] + 105 + a[2];
 a[30] = (a[10] ^ 40) + a[30];
 a[28] = (146 ^ (a[28] + a[23])) + 143;
 a[18] = (a[12] ^ (238 + 201 + a[18])) + 211;
 a[19] = a[25] + a[19] + 148 + 110 + 78;
 a[18] = a[27] + 57 + a[18];
 a[14] = a[15] + 180 + a[14];
 a[25] = (a[31] ^ (177 + a[25])) + 104;
 a[18] = (a[27] ^ 46 ^ (172 + a[18])) + 100;
 a[14] = (a[29] ^ a[14] ^ 255) + 61;
 a[8] = a[14] + a[8] + 226 + 103;
 a[29] = ((a[29] + a[1]) ^ (188 + 12)) + 164;
 a[5] = (a[18] ^ 229) + a[5];
 a[2] = a[3] + a[2] + 8 + 184;
 a[20] = a[23] + 45 + a[20];
 a[6] = (a[9] ^ a[6] ^ 230) + 243;
 a[4] = a[11] + a[4] + 174 + 101;
 a[11] = a[15] + a[11] + 19 + 124 + 68;
 a[11] = a[4] + 48 + a[11];
 a[4] = (a[3] ^ (60 + 111 + a[4])) + 172;
 a[25] = (192 ^ (a[25] + 99 + a[21])) + 128;
 a[3] = (a[20] ^ (163 + 167 + a[3])) + 48;
 a[22] = (a[19] ^ (24 + 28 + a[22])) + 160;
 a[22] = a[29] + a[22] + 189 + 51 + 68;
 a[0] = a[4] + 80 + a[0];
 a[29] = a[16] + a[29] + 117 + 142;
 a[29] = a[10] + a[29] + 141 + 137;
 a[8] = (a[0] ^ a[8] ^ 175) + 126;
 a[15] = (a[25] ^ 7) + a[15];
 a[2] = (a[18] ^ (65 + 105 + a[2])) + 60;
 a[4] = (96 ^ (a[4] + a[15])) + 47;
 a[1] = (a[27] ^ 85) + a[1];
 a[11] = a[18] + a[11] + 183 + 177 + 81;
 a[28] = (a[20] ^ (228 + a[28])) + 254;
 a[23] = (a[23] ^ 50 ^ (1 + a[23])) + 57;
 a[24] = a[26] + 1 + a[24];
 a[28] = (10 ^ (a[28] + 55 + a[15])) + 134;
 a[14] = a[26] + a[14] + 98 + 165;
 a[5] = (215 ^ (a[5] + a[31])) + 225;
 a[0] = a[25] + 86 + a[0];
 a[0] = ((a[0] + a[26]) ^ (101 + 53)) + 207;
 a[31] = (a[30] ^ 152) + a[31];
 a[20] = (a[2] ^ (65 + a[20])) + 69;
 a[25] = (194 ^ (a[25] + a[6])) + 105;
 a[19] = (a[14] ^ 65) + a[19];
 a[11] = (a[8] ^ 29) + a[11];
 a[27] = (a[16] ^ 175) + a[27];
 a[8] = a[10] + a[8] + 254 + 215;
 a[0] = (a[0] ^ 201) + a[0];
 a[18] = a[30] + 68 + a[18];
 a[29] = (a[18] ^ (60 + a[29])) + 101;
 a[2] = a[21] + 190 + a[2];
 a[11] = (a[2] ^ a[11] ^ 128) + 38;
 a[2] = a[3] + 195 + a[2];
 a[8] = (a[1] ^ (222 + a[8])) + 210;
 a[17] = a[13] + a[17] + 109 + 90;
 a[28] = a[7] + 143 + a[28];
 a[4] = (a[22] ^ 247 ^ (152 + a[4])) + 249;
 a[22] = (a[10] ^ (233 + a[22])) + 163;
 a[15] = (a[7] ^ 132) + a[15];
 a[29] = a[6] + 172 + a[29];
 a[19] = (a[19] ^ (123 + a[19])) + 225;
 a[0] = a[28] + a[0] + 152 + 34;
 a[10] = a[23] + 68 + a[10];
 a[23] = a[24] + a[23] + 130 + 17;
 a[22] = a[30] + a[22] + 137 + 254 + 141;
 a[8] = a[5] + a[8] + 74 + 232 + 71;
 a[9] = (118 ^ (a[9] + a[13])) + 115;
 a[13] = a[5] + a[13] + 241 + 101;
 a[6] = ((a[6] + a[17]) ^ (73 + 142)) + 217;
 a[18] = a[10] + a[18] + 202 + 222;
 a[9] = a[26] + a[9] + 226 + 8;
 a[2] = a[10] + 7 + a[2];
 a[21] = a[13] + 114 + a[21];
 """

 results = [
 0xd7765, 0x11ebd, 0x32d12, 0x13778, 0x8a428,
 0xb592, 0x3fa57, 0x1616, 0x3659e, 0x2483a,
 0x2882, 0x508f4, 0xbad, 0x27920, 0xf821,
 0x19f83, 0xf97, 0x33904, 0x170d5, 0x16c,
 0xcf5d, 0x280d2, 0xa8ade, 0x9eaa, 0x9dab,
 0x1f45e, 0x3214, 0x52fa, 0x6d57a, 0x460ed,
 0x124ff, 0x13936
 ]
 translated_constraints = translate_transformations(cpp_transformations)

 z3_script = generate_z3_script(translated_constraints, results, input_size=32)

 with open('z3_solver.py', 'w') as f:
 f.write(z3_script)

 print("Z3 solver script 'z3_solver.py' has been generated.")
二
SU_Harmony
    #include <stdio.h>
    #include <string.h>
    #include <stdlib.h>

// 定义最大位数，根据需要调整
    #define MAX_DIGITS 5000

// 反转字符串
void reverse_str(char *str) {
 int len = strlen(str);
 for(int i=0; i<len/2; i++) {
 char temp = str[i];
 str[i] = str[len-1-i];
 str[len-1-i] = temp;
 }
}

// 大整数加法：result = num1 + num2
void add(char *num1, char *num2, char *result) {
 char a[MAX_DIGITS] = {0};
 char b[MAX_DIGITS] = {0};
 strcpy(a, num1);
 strcpy(b, num2);

 reverse_str(a);
 reverse_str(b);

 int len1 = strlen(a);
 int len2 = strlen(b);
 int maxlen = len1 > len2 ? len1 : len2;
 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<maxlen; i++) {
 int digit1 = i < len1 ? a[i] - '0' : 0;
 int digit2 = i < len2 ? b[i] - '0' : 0;
 int sum = digit1 + digit2 + carry;
 carry = sum / 10;
 sum = sum % 10;
 char temp = sum + '0';
 strncat(result, &temp, 1);
 }
 if(carry) {
 char temp = carry + '0';
 strncat(result, &temp, 1);
 }


 reverse_str(result);

 // 去除前导零
 int start = 0;
 while(result[start] == '0' && start < strlen(result)-1) {
 start++;
 }
 if(start > 0) {
 memmove(result, result + start, strlen(result) - start + 1);
 }
}

// 大整数减法：result = num1 - num2 (假设 num1 >= num2)
void subtract(char *num1, char *num2, char *result) {
 char a[MAX_DIGITS] = {0};
 char b[MAX_DIGITS] = {0};
 strcpy(a, num1);
 strcpy(b, num2);

 reverse_str(a);
 reverse_str(b);

 int len1 = strlen(a);
 int len2 = strlen(b);
 int borrow = 0;
 result[0] = ' ';

 for(int i=0; i<len1; i++) {
 int digit1 = a[i] - '0';
 int digit2 = i < len2 ? (b[i] - '0') : 0;
 int sub = digit1 - digit2 - borrow;
 if(sub < 0) {
 sub += 10;
 borrow = 1;
 }
 else {
 borrow = 0;
 }
 char temp = sub + '0';
 strncat(result, &temp, 1);
 }

 // 去除多余的0
 while(strlen(result) > 1 && result[strlen(result)-1] == '0') {
 result[strlen(result)-1] = ' ';
 }

 reverse_str(result);
}

// 大整数乘法：result = num1 * num2
void multiply(char *num1, char *num2, char *result) {
 int len1 = strlen(num1);
 int len2 = strlen(num2);
 int total_len = len1 + len2;
 int temp_result[MAX_DIGITS] = {0};

 // 从右到左计算每一位的乘积
 for(int i=len1-1; i>=0; i--) {
 for(int j=len2-1; j>=0; j--) {
 int p1 = i + j;
 int p2 = i + j + 1;
 int mul = (num1[i] - '0') * (num2[j] - '0') + temp_result[p2];
 temp_result[p2] = mul % 10;
 temp_result[p1] += mul / 10;
 }
 }

 // 构建结果字符串
 int i = 0;
 while(i < total_len && temp_result[i] == 0) i++;
 if(i == total_len) {
 strcpy(result, "0");
 return;
 }
 result[0] = ' ';
 for(; i < total_len; i++) {
 char digit = temp_result[i] + '0';
 strncat(result, &digit, 1);
 }
}

// 大整数乘以单个数字：result = num * digit
void multiply_single_digit(char *num, int digit, char *result) {
 if(digit < 0 || digit > 9) {
 strcpy(result, "0");
 return;
 }
 char a[MAX_DIGITS] = {0};
 strcpy(a, num);
 reverse_str(a);

 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<strlen(a); i++) {
 int prod = (a[i] - '0') * digit + carry;
 carry = prod / 10;
 int sum = prod % 10;
 char temp = sum + '0';
 strncat(result, &temp, 1);
 }
 if(carry) {
 char temp = carry + '0';
 strncat(result, &temp, 1);
 }

 reverse_str(result);

 // 去除前导零
 int start = 0;
 while(result[start] == '0' && start < strlen(result)-1) {
 start++;
 }
 if(start > 0) {
 memmove(result, result + start, strlen(result) - start + 1);
 }
}

// 大整数除以2：result = num / 2
void divide_by_two(char *num, char *result) {
 int len = strlen(num);
 int carry = 0;
 result[0] = ' ';

 for(int i=0; i<len; i++) {
 int current = carry * 10 + (num[i] - '0');
 int quotient = current / 2;
 carry = current % 2;
 char temp = quotient + '0';
 // 处理前导零
 if(!(i == 0 && quotient == 0)) {
 strncat(result, &temp, 1);
 }
 }
 if(strlen(result) == 0) {
 strcpy(result, "0");
 }
}

void uint_to_dec_str(unsigned int num, char *str) {
 int i = 0;

 // 特殊情况处理：num == 0
 if(num == 0) {
 str[i++] = '0';
 str[i] = ' ';
 return;
 }

 // 逐位提取数字并存入字符串（逆序）
 while(num > 0) {
 int digit = num % 10;
 str[i++] = digit + '0';
 num /= 10;
 }

 // 添加字符串终止符
 str[i] = ' ';

 // 反转字符串以得到正确的顺序
 reverse_str(str);
 printf("input : %s",str);
}

// 检查字符串是否为有效的非负整数
int is_valid_number(char *num) {
 if(strlen(num) == 0) return 0;
 for(int i=0; i<strlen(num); i++) {
 if(num[i] < '0' || num[i] > '9') return 0;
 }
 return 1;
}

int main() {
 /*

 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[0] = 54435553
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[1] = 614d7b46
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[2] = 575f6837
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[3] = 646c726f
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[4] = 535f7349
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[5] = 33425f30
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[6] = 31747561
 12-28 00:51:55.741 16594-16594 A03200/Native Log com.swdd.suapp2 I input2uintArray[7] = 7d6c7566

 */
 char b[MAX_DIGITS];
 char b_squared[MAX_DIGITS] = {0};
 char two_b[MAX_DIGITS] = {0};
 char sum[MAX_DIGITS] = {0};
 char numerator[MAX_DIGITS] = {0};
 char final_result[MAX_DIGITS] = {0};
 unsigned int x;
 // 提示用户输入
 printf("请输入上限值 b：");
 if(scanf("%x", &x) != 1) {
 printf("输入无效，请输入一个整数。n");
 return 1;
 }
 uint_to_dec_str(x,b);

//	gets(b);
 // 输入验证
 if(!is_valid_number(b)) {
 printf("输入无效，请输入一个非负整数。n");
 return 1;
 }

 // 计算 b^2
 multiply(b, b, b_squared);
 // printf("b^2 = %sn", b_squared); // 调试用

 // 计算 2 * b
 multiply_single_digit(b, 2, two_b);
 // printf("2*b = %sn", two_b); // 调试用

 // 计算 b^2 + 2*b
 add(b_squared, two_b, sum);
 // printf("b^2 + 2*b = %sn", sum); // 调试用

 // 计算 b^2 + 2*b - 3
 subtract(sum, "3", numerator);
 // printf("b^2 + 2*b - 3 = %sn", numerator); // 调试用

 // 计算 (b^2 + 2*b - 3) / 2
 divide_by_two(numerator, final_result);

 // 输出结果
 printf("函数 f(x) = x + 1 在区间 [1, %s] 上的定积分结果为：%sn", b, final_result);

 return 0;
}
import struct
import math

# 定义加密列表（假设为十进制字符串）
encList = [
 "999272289930604998",
 "1332475531266467542",
 "1074388003071116830",
 "1419324015697459326",
 "978270870200633520",
 "369789474534896558",
 "344214162681978048",
 "2213954953857181622"
]

def solve_x(enc_num):
 """
 根据公式 f(x) = (x^2 + 2x - 3) / 2 = enc_num 反向计算 x
 """
 # 计算 8 * enc_num + 16
 val = 8 * enc_num + 16
 # 计算整数平方根
 sqrt_val = math.isqrt(val)
 # 初步计算 x_i
 x_i = (sqrt_val - 2) // 2
 # 验证 x_i 是否满足方程
 if (x_i ** 2 + 2 * x_i - 3) // 2 == enc_num:
 return x_i
 # 如果不满足，尝试 x_i + 1
 x_i += 1
 if (x_i ** 2 + 2 * x_i - 3) // 2 == enc_num:
 return x_i
 # 如果仍不满足，抛出异常
 raise ValueError(f"无法找到满足方程的 x_i 对于 enc_num={enc_num}")

# 计算所有 x_i
x_list = []
for idx, enc in enumerate(encList):
 enc_num = int(enc)
 try:
 x = solve_x(enc_num)
 x_list.append(x)
 print(f"encList[{idx}]: {enc_num}, x[{idx}]: {x}")
 
except ValueError as e:
 print(f"Error for encList[{idx}]: {e}")
 exit(1)

# 将 x_i 打包为小端字节序的4字节无符号整数
input_bytes = b''.join([struct.pack(' Bytes: {packed.hex()} -> ASCII: {ascii_chars}")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1738640265.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/3-1738640265.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1738640265.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1738640266.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/1-1738640266.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/5-1738640267.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1738640267.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1738640267.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1738640268.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/5-1738640268.png)