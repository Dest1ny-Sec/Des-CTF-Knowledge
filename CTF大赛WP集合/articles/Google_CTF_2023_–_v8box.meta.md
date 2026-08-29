---
title: Google CTF 2023 – v8box
contest: Google CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [v8, javascript-engine, jitless, sandbox, code-pointer, memory-corruption-api, maglev]
attack_chain:
  - fetch v8: git switch -d d90d4533b05301e2be813a5f90223f4c6c1bf63d
  - gclient sync
  - git apply v8.patch + 0001-Protect-chunk-headers-on-the-heap.patch
  - ./tools/dev/v8gen.py x64.release
  - v8_enable_sandbox=true + v8_code_pointer_sandboxing=true
  - v8_jitless=true (无JIT)
  - v8_enable_maglev=false + v8_enable_turbofan=false
  - v8_expose_memory_corruption_api=true
  - gn gen out.gn/x64.release
  - ninja -C out.gn/x64.release -j 12 d8
  - V8_EXPOSE_MEMORY_CORRUPTION_API 暴露漏洞
key_payload: v8_enable_sandbox=true + v8_code_pointer_sandboxing=true
one_liner: Google CTF 2023 v8box：V8 sandbox+code pointer sandbox+JITless
lesson: V8 sandbox模式开启后内存破坏API需特殊配置
quality: high
---

# Google CTF 2023 – v8box

## 题目信息
- 比赛：Google CTF 2023
- 题目：v8box（V8 沙箱）
- 类别：V8 引擎漏洞利用

## 关键攻击链
### 1. 环境搭建
```bash
fetch v8
git switch -d d90d4533b05301e2be813a5f90223f4c6c1bf63d
gclient sync
git apply < ./v8.patch
git apply < ./0001-Protect-chunk-headers-on-the-heap.patch
./tools/dev/v8gen.py x64.release
```

### 2. V8 配置
```python
is_component_build = false
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true                # 沙箱模式
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
dcheck_always_on = false
v8_jitless = true                        # 无 JIT
v8_enable_maglev = false                 # 关闭 Maglev
v8_enable_turbofan = false               # 关闭 TurboFan
v8_enable_webassembly = false
v8_expose_memory_corruption_api = true   # 暴露内存破坏 API
use_goma = false
v8_code_pointer_sandboxing = true        # 代码指针沙箱

gn gen out.gn/x64.release
ninja -C out.gn/x64.release -j 12 d8
```

### 3. 内存破坏 API
```cpp
#ifdef V8_EXPOSE_MEMORY_CORRUPTION_API
namespace {
// Sandbox.byteLength
void SandboxGetByteLength(const v8::FunctionCallbackInfo<v8::Value>& args) {
    ...
}
#endif
```

## 关键技术点
- V8 Sandbox（v8_enable_sandbox）
- Code Pointer Sandboxing
- JITless 模式（无优化编译器）
- Maglev 关闭
- 内存破坏 API 暴露

## 评分
- quality: high（V8 引擎配置 + 沙箱模式 + 代码指针沙箱完整）
