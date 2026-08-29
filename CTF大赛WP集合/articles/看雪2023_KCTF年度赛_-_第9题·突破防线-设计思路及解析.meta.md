---
title: 看雪2023 KCTF年度赛 | 第9题·突破防线-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: hard
vuln_type: kernel
tags: [Go VM, vmfs内核驱动, IOCTL用户态通信, 自定义VM指令, sha512密码学, cgo FFI, http服务+VM执行]
attack_chain: 上传代码到vmfs驱动→IOCTL 0xff00-0xff05(创建/移动/删除/读写/排序文件)→runFile/VM执行上传代码→sha512 blockGeneric+blockAsm→C/S混合VM→custom opcodes
key_payload: "VMFS_CREATE_FILE=0xff00;VMFS_MOVE_TO_TRASH=0xff01;VMFS_DELETE_FROM_TRASH=0xff02;VMFS_WRITE_FILE=0xff03;VMFS_READ_FILE=0xff04;VMFS_SORT_FILE=0xff05;main_machine_0 reg[16]+_pc+code[4096]+data[]"
one_liner: KCTF2023年度赛Q9《突破防线》Go VM+vmfs驱动+IOCTL通信+自定义指令VM+sha512
lesson: Go写的VM+内核驱动组合：cgo调用ioctl传递用户态buffer到内核VM执行
quality: high
---

# 看雪2023 KCTF年度赛 | 第9题·突破防线-设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q9《突破防线》

**难度**：仅1队提交

**题目设计**：
- Go VM + vmfs内核驱动组合
- VM中开启HTTP服务
- 用户上传代码 → 写入/dev/vmfs驱动 → 发送运行指令 → VM执行

**vmfs驱动IOCTL**：
```c
#define VMFS_CREATE_FILE 0xff00       // 创建文件节点
#define VMFS_MOVE_TO_TRASH 0xff01     // 文件节点移动到回收站
#define VMFS_DELETE_FROM_TRASH 0xff02 // 彻底删除文件节点
#define VMFS_WRITE_FILE 0xff03         // 写文件节点
#define VMFS_READ_FILE 0xff04          // 读文件节点
#define VMFS_SORT_FILE 0xff05         // 对文件节点进行排序
```

**main_machine_0结构**：
```c
struct main_machine_0 {
    uint64_t reg[16];          // 16个寄存器
    uint64_t _pc;               // 程序计数器
    uint64_t code[4096];        // 4096指令
    struct _slice_uint64 data;  // 数据
};
```

**用户态runFile函数**：
```go
func runFile(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Access-Control-Allow-Origin", "*")
    
    var req Req
    err := json.NewDecoder(r.Body).Decode(&req)
    
    f, err := os.OpenFile(dev_path, syscall.O_RDONLY, 0600)
    
    var vm machine
    vm.data = make([]uint64, 0x1000)
    
    data := user_argv{
        id: uint64(req.Id),
        addr: uintptr(unsafe.Pointer(&(vm.code))),
        size: uint64(req.Size),
        choose_index: uint64(req.ChooseIndex),
        sort_option: uint64(0),
    }
    _, _, errno := syscall.Syscall(
        syscall.SYS_IOCTL,
        uintptr(f.Fd()),
        uintptr(VMFS_READ_FILE),
        uintptr(unsafe.Pointer(&data)),
    )
    f.Close()
    // ... 运行vm
}
```

**关键组件**：
- crypto_sha512：blockGeneric + blockAsm 两种实现
- runtime._ptr_profBuf.write
- main.runVM：核心VM循环
- cgo FFI（Go ↔ C）

**VM特性**：
- 16个通用寄存器
- 4096条指令
- sha512密码学原语
- 数组array、长度len、容量cap
- 字符串slice

**利用**：
- 上传自定义代码到vmfs
- IOCTL读取 → 装入vm.code
- 启动VM执行
- 返回结果通过HTTP

**核心技术**：
- Go语言写VM（非常规）
- 用户态+内核态混合VM
- cgo FFI做IOCTL通信
- sha512密码学原语
- 自定义VM指令集

**质量评估**：高（IOCTL接口+结构体定义+VM架构）
