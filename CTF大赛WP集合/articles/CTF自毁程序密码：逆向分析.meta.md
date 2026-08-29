---
title: CTF 自毁程序密码 Android 逆向
contest: Android Crackme
year: 2024
difficulty: medium
vuln_type: reverse
tags: [Android, libcrackme.so, AndroidNativeEmu, Frida hook, unidbg, JNI]
attack_chain: |
  1. 目标: libcrackme.so 的 Java_com_yaotong_crackme_MainActivity_securityCheck(JNIEnv*, jclass, jstring password) 验证输入 password
  2. 自毁机制: 失败 N 次后程序自动擦除敏感数据
  3. 解法 1 - AndroidNativeEmu 模拟: 装 unicorn + androidemu 模拟器 + load_library libc/libcrackme + memory hook 0x4450+0xa009b000 字符串变量
  4. emulator.call_symbol(lib_module, 'Java_com_yaotong_crackme_MainActivity_securityCheck', jni_env_ptr, 0, "wojiushidaan", is_return_jobject=False)
  5. 解法 2 - Frida hook: Module.findBaseAddress("libcrackme.so") + v1 = addr.add(0x4450) + v1.readCString() 直接读 0x4450 处 C 字符串
  6. 解法 3 - unidbg 模拟: com.github.unidbg.AndroidEmulatorBuilder + AndroidResolver + DynarmicFactory 后端模拟
key_payload: |
  // 解法 1 AndroidNativeEmu:
  emulator = Emulator(vfp_inst_set=True)
  emulator.load_library("../example_binaries/32/libc.so", do_init=False)
  lib_module = emulator.load_library("libcrackme.so", do_init=False)
  target_address = 0x4450+0xa009b000
  emulator.uc.hook_add(UC_HOOK_MEM_READ, memory_read_hook, None, target_address, target_address+100)
  emulator.uc.hook_add(UC_HOOK_MEM_WRITE, memory_write_hook, None, target_address, target_address+100)
  result1 = emulator.call_symbol(lib_module, 'Java_com_yaotong_crackme_MainActivity_securityCheck', emulator.java_vm.jni_env.address_ptr, 0, "wojiushidaan", is_return_jobject=False)
  
  // 解法 2 Frida:
  function hook_so() {
    var addr = Module.findBaseAddress("libcrackme.so");
    var v1 = addr.add(0x4450);
    console.log(v1.readCString());
  }
one_liner: 自毁机制 Android crackme，3 种解法 (AndroidNativeEmu 模拟 / Frida hook / unidbg) 都不需要碰真实设备。
lesson: |
  - JNI 函数的符号名固定为 Java_<package_class_method> 格式
  - AndroidNativeEmu 适合静态分析带 .so 的 Android 应用
  - Frida hook 找 .so 加载基址 + 偏移即可读 C 字符串变量
  - unidbg 比 AndroidNativeEmu 更完整，支持 ARM64 + ARM32 + Dynarmic 后端
quality: medium
---

# CTF 自毁程序密码 Android 逆向

> 来源: ctfiot.com 223659

## 背景

`libcrackme.so` 内有 `Java_com_yaotong_crackme_MainActivity_securityCheck(JNIEnv*, jclass, jstring password)` 函数，验证 password 失败若干次后程序自动擦除敏感数据（自毁机制）。要绕过自毁，三种"不碰真机"解法。

## 解法 1: AndroidNativeEmu 模拟

```python
from androidemu.emulator import Emulator
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

emulator = Emulator(vfp_inst_set=True)
emulator.load_library("../example_binaries/32/libc.so", do_init=False)
lib_module = emulator.load_library("libcrackme.so", do_init=False)

target_address = 0x4450 + 0xa009b000  # 关键字符串变量地址
string_length = 100

def memory_read_hook(uc, access, address, size, value, user_data):
    if address == target_address:
        current_value = uc.mem_read(address, string_length).split(b'\x00', 1)[0].decode('ascii', errors='ignore')
        print(f"【READ】 Address: 0x{address:X}, Current Value: {current_value}")

def memory_write_hook(uc, access, address, size, value, user_data):
    if address == target_address:
        new_value = uc.mem_read(address, string_length).split(b'\x00', 1)[0].decode('ascii', errors='ignore')
        print(f"【WRITE】 Address: 0x{address:X}, New Value: {new_value}")

emulator.uc.hook_add(UC_HOOK_MEM_READ, memory_read_hook, None, target_address, target_address + string_length)
emulator.uc.hook_add(UC_HOOK_MEM_WRITE, memory_write_hook, None, target_address, target_address + string_length)

result1 = emulator.call_symbol(
    lib_module, 'Java_com_yaotong_crackme_MainActivity_securityCheck',
    emulator.java_vm.jni_env.address_ptr, 0, "wojiushidaan",  # 测试密码
    is_return_jobject=False
)
```

## 解法 2: Frida hook 读 C 字符串

```javascript
function hook_so() {
    Java.perform(function(){
        var addr = Module.findBaseAddress("libcrackme.so");
        var v1 = addr.add(0x4450);
        console.log(v1.readCString());
    });
}
function main() { hook_so() }
setTimeout(main, 4000);
```

## 解法 3: unidbg 模拟

```java
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.arm.backend.DynarmicFactory;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;

AndroidEmulator emulator = AndroidEmulatorBuilder
    .for32Bit()
    .setProcessName("com.yaotong.crackme")
    .build();
```

## 评价

题目自毁机制让"试错"路线堵死，但用 unicorn 模拟 / Frida hook / unidbg 都可以无副作用拿到答案。三种解法并列展示，对 AndroidNativeEmu 与 unidbg 的 API 入门很友好。
