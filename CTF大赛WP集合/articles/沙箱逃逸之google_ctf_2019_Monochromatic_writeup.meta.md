---
title: 沙箱逃逸之google ctf 2019 Monochromatic writeup
contest: Google CTF 2019
year: 2019
difficulty: expert
vuln_type: rce
tags: [Chromium Mojo IPC, Person/Dog/Cat Interface, BeingCreatorInterface, Blink, content_browser_manifest, MojoJS]
attack_chain: Mojo IDL定义BeingCreatorInterface+PersonInterface+DogInterface+CatInterface→content_browser_manifest暴露blink.mojom.BeingCreatorInterface→renderer调用CreatePerson/CreateDog/CreateCat→Impl侧直接传入blink::mojom::FoodInterface引用计数处理UAF→sandbox逃逸
key_payload: "mojo public/tools/bindings/mojom.gni;interface BeingCreatorInterface CreatePerson CreateDog CreateCat;PersonInterface GetName/SetName/GetAge/SetAge/GetWeight/SetWeight/CookAndEat(blink.mojom.FoodInterface food)"
one_liner: Google CTF 2019 Monochromatic：Chromium Mojo IPC BeingCreatorInterface + 3 Interface UAF沙箱逃逸
lesson: Blink Mojo IPC新增Interface需注册到content_browser_manifest；FoodInterface引用计数UAF是逃逸点
quality: high
---

# 沙箱逃逸之google_ctf_2019_Monochromatic_writeup

**赛事**：Google CTF 2019 Monochromatic（Chromium Mojo沙箱逃逸）

**核心结构**：

**1. mojom接口定义**：
```mojom
module test.echo.mojom;
interface Echo {
  EchoInteger(int32 value) => (int32 result);
};
```

**2. build.gn配置**：
```gn
import("//mojo/public/tools/bindings/mojom.gni")
mojom("interfaces") {
  sources = ["echo.mojom"]
}
```
- 生成: `ninja -C out/r services/echo/public/interfaces:interfaces_js`
- 输出: `out/gen/services/echo/public/interfaces/echo.mojom.js`

**3. 浏览器侧调用**：
```html
<script src="URL/to/mojo_bindings.js"></script>
<script src="URL/to/echo.mojom.js"></script>
<script>
var echoPtr = new test.echo.mojom.EchoPtr();
var echoRequest = mojo.makeRequest(echoPtr);
</script>
```

**4. 服务侧实现**：
```javascript
function EchoImpl() {}
EchoImpl.prototype.echoInteger = function(value) {
  return Promise.resolve({result: value});
};
var echoServicePtr = new test.echo.mojom.EchoPtr();
var echoServiceRequest = mojo.makeRequest(echoServicePtr);
var echoServiceBinding = new mojo.Binding(test.echo.mojom.Echo, new EchoImpl(), echoServiceRequest);
```

**CTF patch改动**：

**1. `content/public/app/content_browser_manifest.cc`**：
```diff
+ "blink.mojom.BeingCreatorInterface",
```
- 暴露BeingCreatorInterface到renderer capability

**2. 新增BeingCreatorInterface**：
```mojom
import "url/mojom/origin.mojom";
import "third_party/blink/public/mojom/CTF/person_interface.mojom";
import "third_party/blink/public/mojom/CTF/dog_interface.mojom";
import "third_party/blink/public/mojom/CTF/cat_interface.mojom";

interface BeingCreatorInterface {
  CreatePerson() => (blink.mojom.PersonInterface? person);
  CreateDog() => (blink.mojom.DogInterface? dog);
  CreateCat() => (blink.mojom.CatInterface? cat);
};

interface PersonInterface {
  GetName() => (string name);
  SetName(string new_name) => ();
  GetAge() => (uint64 age);
  SetAge(uint64 new_age) => ();
  GetWeight() => (uint64 weight);
  SetWeight(uint64 new_weight) => ();
  CookAndEat(blink.mojom.FoodInterface food) => ();
};
```

**3. CatInterfaceImpl**：
- 继承 `blink::mojom::CatInterface`
- 类成员关系导致FoodInterface引用计数处理UAF
- 利用链：renderer → CreateCat → Cat持有Food → Food UAF → sandbox escape

**Docker构建**：
```bash
args = [
  './binary/chrome',
  '--enable-blink-features=MojoJS',
  '--disable-gpu',
  '--headless',
  '--repl',
  'server'
]
```

**质量评估**：高（mojom IDL + patch + 漏洞链清晰）
