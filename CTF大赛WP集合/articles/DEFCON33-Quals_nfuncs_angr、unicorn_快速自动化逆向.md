# DEFCON33-Quals nfuncs angr、unicorn 快速自动化逆向

> 原文: https://www.ctfiot.com/253727.html
> ID: 253727

read(0, DstBuf, 1u);  read(0, &DstBuf[1], 1u);read(0, &DstBuf[2], 1u);read(0, &DstBuf[3], 1u);read(0, &DstBuf[4], 1u);read(0, &DstBuf[5], 1u);read(0, &DstBuf[6], 1u);read(0, &DstBuf[7], 1u);v0 = 32 * (DstBuf[0] & 1);if ( (DstBuf[0] & 2) != 0 )v0 = (32 * (DstBuf[0] & 1)) | 0x40;if ( (DstBuf[0] & 4) != 0 )v0 |= 0x80u;if ( (DstBuf[0] & 8) != 0 )v0 |= 0x10u;if ( (DstBuf[0] & 0x10) != 0 )v0 |= 1u;if ( (DstBuf[0] & 0x20) != 0 )v0 |= 2u;if ( (DstBuf[0] & 0x40) != 0 )v0 |= 8u;if ( DstBuf[0] < 0 )v0 |= 4u;v1 = v0 & 0xDF;if ( (DstBuf[1] & 1) != 0 )v1 = v0 | 0x20;v2 = v1 | 0x40;v3 = v1 & 0xBF;if ( (DstBuf[1] & 2) != 0 )v3 = v2;v4 = v3 | 0x80;v5 = v3 & 0x7F;if ( (DstBuf[1] & 4) != 0 )v5 = v4;v6 = v5 | 0x10;v7 = v5 & 0xEF;if ( (DstBuf[1] & 8) != 0 )v7 = v6;v8 = v7 | 1;v9 = v7 & 0xFE;if ( (DstBuf[1] & 0x10) != 0 )v9 = v8;v10 = v9 | 2;v11 = v9 & 0xFD;if ( (DstBuf[1] & 0x20) != 0 )v11 = v10;v12 = v11 | 8;v13 = v11 & 0xF7;if ( (DstBuf[1] & 0x40) != 0 )v13 = v12;v14 = v13 | 4;v15 = v13 & 0xFB;if ( DstBuf[1] < 0 )v15 = v14;v16 = v15 & 0xDF;if ( (DstBuf[2] & 1) != 0 )v16 = v15 | 0x20;v17 = v16 | 0x40;v18 = v16 & 0xBF;if ( (DstBuf[2] & 2) != 0 )v18 = v17;v19 = v18 | 0x80;v20 = v18 & 0x7F;if ( (DstBuf[2] & 4) != 0 )v20 = v19;v21 = v20 | 0x10;v22 = v20 & 0xEF;if ( (DstBuf[2] & 8) != 0 )v22 = v21;v23 = v22 | 1;v24 = v22 & 0xFE;if ( (DstBuf[2] & 0x10) != 0 )v24 = v23;v25 = v24 | 2;v26 = v24 & 0xFD;if ( (DstBuf[2] & 0x20) != 0 )v26 = v25;v27 = v26 | 8;v28 = v26 & 0xF7;if ( (DstBuf[2] & 0x40) != 0 )v28 = v27;v29 = v28 | 4;v30 = v28 & 0xFB;if ( DstBuf[2] < 0 )v30 = v29;v31 = v30 & 0xDF;if ( (DstBuf[3] & 1) != 0 )v31 = v30 | 0x20;v32 = v31 | 0x40;v33 = v31 & 0xBF;if ( (DstBuf[3] & 2) != 0 )v33 = v32;v34 = v33 | 0x80;v35 = v33 & 0x7F;if ( (DstBuf[3] & 4) != 0 )v35 = v34;v36 = v35 | 0x10;v37 = v35 & 0xEF;if ( (DstBuf[3] & 8) != 0 )v37 = v36;v38 = v37 | 1;v39 = v37 & 0xFE;if ( (DstBuf[3] & 0x10) != 0 )v39 = v38;v40 = v39 | 2;v41 = v39 & 0xFD;if ( (DstBuf[3] & 0x20) != 0 )v41 = v40;v42 = v41 | 8;v43 = v41 & 0xF7;if ( (DstBuf[3] & 0x40) != 0 )v43 = v42;v44 = v43 | 4;v45 = v43 & 0xFB;if ( DstBuf[3] < 0 )v45 = v44;v46 = v45 & 0xDF;if ( (DstBuf[4] & 1) != 0 )v46 = v45 | 0x20;v47 = v46 | 0x40;v48 = v46 & 0xBF;if ( (DstBuf[4] & 2) != 0 )v48 = v47;v49 = v48 | 0x80;v50 = v48 & 0x7F;if ( (DstBuf[4] & 4) != 0 )v50 = v49;v51 = v50 | 0x10;v52 = v50 & 0xEF;if ( (DstBuf[4] & 8) != 0 )v52 = v51;v53 = v52 | 1;v54 = v52 & 0xFE;if ( (DstBuf[4] & 0x10) != 0 )v54 = v53;v55 = v54 | 2;v56 = v54 & 0xFD;if ( (DstBuf[4] & 0x20) != 0 )v56 = v55;v57 = v56 | 8;v58 = v56 & 0xF7;if ( (DstBuf[4] & 0x40) != 0 )v58 = v57;v59 = v58 | 4;v60 = v58 & 0xFB;if ( DstBuf[4] < 0 )v60 = v59;v61 = v60 & 0xDF;if ( (DstBuf[5] & 1) != 0 )v61 = v60 | 0x20;v62 = v61 | 0x40;v63 = v61 & 0xBF;if ( (DstBuf[5] & 2) != 0 )v63 = v62;v64 = v63 | 0x80;v65 = v63 & 0x7F;if ( (DstBuf[5] & 4) != 0 )v65 = v64;v66 = v65 | 0x10;v67 = v65 & 0xEF;if ( (DstBuf[5] & 8) != 0 )v67 = v66;v68 = v67 | 1;v69 = v67 & 0xFE;if ( (DstBuf[5] & 0x10) != 0 )v69 = v68;v70 = v69 | 2;v71 = v69 & 0xFD;if ( (DstBuf[5] & 0x20) != 0 )v71 = v70;v72 = v71 | 8;v73 = v71 & 0xF7;if ( (DstBuf[5] & 0x40) != 0 )v73 = v72;v74 = v73 | 4;v75 = v73 & 0xFB;if ( DstBuf[5] < 0 )v75 = v74;v76 = v75 & 0xDF;if ( (DstBuf[6] & 1) != 0 )v76 = v75 | 0x20;v77 = v76 | 0x40;v78 = v76 & 0xBF;if ( (DstBuf[6] & 2) != 0 )v78 = v77;v79 = v78 | 0x80;v80 = v78 & 0x7F;if ( (DstBuf[6] & 4) != 0 )v80 = v79;v81 = v80 | 0x10;v82 = v80 & 0xEF;if ( (DstBuf[6] & 8) != 0 )v82 = v81;v83 = v82 | 1;v84 = v82 & 0xFE;if ( (DstBuf[6] & 0x10) != 0 )v84 = v83;v85 = v84 | 2;v86 = v84 & 0xFD;if ( (DstBuf[6] & 0x20) != 0 )v86 = v85;v87 = v86 | 8;v88 = v86 & 0xF7;if ( (DstBuf[6] & 0x40) != 0 )v88 = v87;v89 = v88 | 4;v90 = v88 & 0xFB;if ( DstBuf[6] < 0 )v90 = v89;v91 = v90 & 0xDF;if ( (DstBuf[7] & 1) != 0 )v91 = v90 | 0x20;v92 = v91 | 0x40;v93 = v91 & 0xBF;if ( (DstBuf[7] & 2) != 0 )v93 = v92;v94 = v93 | 0x80;v95 = v93 & 0x7F;if ( (DstBuf[7] & 4) != 0 )v95 = v94;v96 = v95 | 0x10;v97 = v95 & 0xEF;if ( (DstBuf[7] & 8) != 0 )v97 = v96;v98 = v97 | 1;v99 = v97 & 0xFE;if ( (DstBuf[7] & 0x10) != 0 )v99 = v98;v100 = v99 | 2;v101 = v99 & 0xFD;if ( (DstBuf[7] & 0x20) != 0 )v101 = v100;v102 = v101 | 8;v103 = v101 & 0xF7;if ( (DstBuf[7] & 0x40) != 0 )v103 = v102;v104 = v103 | 4;v105 = v103 & 0xFB;if ( DstBuf[7] < 0 )v105 = v104;if ( v0 == -77 && !(v45 | (unsigned __int8)(v30 | v15)) && v60 == 32 && v75 == 107 && v90 == 73 && v105 == -24 ){strcpy(v108, ":)");puts(v108);v110[0] = 0LL;v110[1] = 0LL;sub_14003A1C0(v110, *(_QWORD *)DstBuf + 2815032436LL);VirtualProtect(sub_140055A50, 0x17960uLL, 0x40u, &v109);for ( i = 0LL; i != 96608; ++i )*(_BYTE *)(i + 0x140055A50LL) ^= *((_BYTE *)v110 + (i & 0xF));VirtualProtect(sub_140055A50, 0x17960uLL, v109, 0LL);
return sub_140055A50();}else{strcpy(Buffer, ":(");
return puts(Buffer);}}

def collect_cmp_value(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        cmps = []
        for i in md.disasm(func_code, base_addr):

            if i.mnemonic == 'cmp':
                # print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                op2 =  i.op_str.split(',')[1].strip()
                if i.operands[1].type == X86_OP_IMM :
                    op2 = int(op2, 16)
                    if op2 < 0x100:
                        # print(f"op2: {op2}")
                        cmps.append(op2)
            if i.mnemonic == 'test':
                cmps.append(0)
            if len(cmps) == 8:
                break

import angr 
import claripy
import io
from angr.calling_conventions import SimCCMicrosoftAMD64
from angr.errors import SimProcedureError
from capstone import *
import archinfo
from capstone.x86_const import *

def rva_to_foa(addr):
return addr - 0x140001000 + 0x400

def get_file_slice(file_path, start, size):
    start = rva_to_foa(start)
with open(file_path, 'rb') as f:
        f.seek(start)
return f.read(size)

def store_ans(ans):
with open("all-ans.bin",'a+b') as f1:
# print("write all-ans")
print(ans)
        f1.write(ans)
        f1.flush()
with open('last-ans.bin','wb') as f:
        f.write(ans) 

# last_read_return_address = None

is_lut = False

def find_ans(FUN_VA, file_path='nfuncs1.exe'):
global is_lut
    input_bytes = []
class ReadHook(angr.SimProcedure):
def run(self, fd, buf, cnt):
global last_read_return_address
            fd = self.state.solver.eval(fd)
            cnt = self.state.solver.eval(cnt)
            target_addr = self.state.solver.eval(buf)   
if fd != 0 or cnt != 1:
print(f'[!] Unexpected read: fd {fd}, count {cnt}')

# if len(input_bytes) == 0:
#      for i in range(256):
#         self.state.memory.store(target_addr-0x108 + i , (i+13) % 256, 8, endness=archinfo.Endness.LE)

            sym =  claripy.BVS(f"input_{len(input_bytes)}", 8)
            input_bytes.append(sym)

            self.state.memory.store(target_addr, sym)
# print(f"[+] Hooked: wrote symbolic byte to {hex(target_addr)}")
# rip = self.state.solver.eval(self.state.memory.load(self.state.regs.rsp,8,endness=archinfo.Endness.LE))
# last_read_return_address = rip
# print(f"[+] Hooked: rip {hex(rip)}")
            value  = self.state.solver.eval(self.state.memory.load(target_addr-0x108, 1),cast_to=int)
if value == 13 + len(input_bytes) - 1:
                is_lut = True
else:
                is_lut = False

# print(f"[+] Hooked: value {hex(value)}")
if len(input_bytes) == 8 and is_lut:
# print("is_lut")
                cmps = collect_cmp_value(FUN_VA)
if len(cmps) == 8: # nothing i can do
for i, target in enumerate(cmps):
# v12_expr = (index + 13) % 256
# print(hex(target))
                        self.state.solver.add(input_bytes[i] == target - 13)
# state.solver.add((input_bytes[i] + 13) % 256 == target)

class VirtualProtectHook(angr.SimProcedure):
def run(self, lpAddress, dwSize, flNewProtect, lpflOldProtect):
            addr = self.state.solver.eval(lpAddress)
            size = self.state.solver.eval(dwSize)
            prot = self.state.solver.eval(flNewProtect)

print(f"[+] Hooked VirtualProtect:")
print(f"    -> Address: {hex(addr)}")
print(f"    -> Size   : {hex(size)}")
print(f"    -> NewProt: {hex(prot)}")

return claripy.BVV(1, self.state.arch.bits)

class PutsHook(angr.SimProcedure):
def run(self,buf):
            str_address = self.state.solver.eval(buf)
            s = self.state.solver.eval(self.state.memory.load(str_address,3),cast_to=bytes)
print("input:",s) # b':)x00' or b':(x00'
if s == b':(x00':
print("[!] Detected bad output ':(', killing path.")
return claripy.BVV(1, self.state.arch.bits)

# FUN_VA =  0x14000F000
    func_code = get_file_slice(file_path, FUN_VA, 0x1000)

def find_avoid_address(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        find_address = None
        avoid_address = None
for i in md.disasm(func_code, base_addr):

# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
if i.mnemonic == 'mov' and  '0x283a' in i.op_str:
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                avoid_address = i.address
if i.mnemonic == 'mov' and  '0x293a' in i.op_str:
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                find_address = i.address
if find_address and avoid_address:
break
return (find_address,avoid_address)

def collect_cmp_value(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        cmps = []
for i in md.disasm(func_code, base_addr):

if i.mnemonic == 'cmp':
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                op2 =  i.op_str.split(',')[1].strip()
if i.operands[1].type == X86_OP_IMM :
                    op2 = int(op2, 16)
if op2 < 0x100:
# print(f"op2: {op2}")
                        cmps.append(op2)
if i.mnemonic == 'test':
                cmps.append(0)
if len(cmps) == 8:
break
# assert len(cmps) == 8, f"[-] cmps length is not 8!"
return cmps
# exit()

# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
    find_address,avoid_address = find_avoid_address(FUN_VA)
# assert avoid_address != None, f"[-] Can't find avoid address!"

    proj = angr.Project(io.BytesIO(func_code), auto_load_libs=False, main_opts={
'base_addr': FUN_VA,
'backend': 'blob',
'arch': 'X86_64',
'entry_point': 0, # just avoid warnings
    }, )

#handle IAT 
    cc = SimCCMicrosoftAMD64(proj.arch)
    proj.hook(0x1A703AA78, ReadHook(cc=cc))
    proj.hook(0xDEADBEFF00, VirtualProtectHook(cc=cc))
    proj.hook(0x1A703AA50, angr.SIM_PROCEDURES['libc']['puts']())

    state = proj.factory.blank_state(addr=FUN_VA, add_options={
            angr.options.UNICORN,
            angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
            angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
        }) # faster

#manually process relocations
#read(0)

    state.regs.rsp = claripy.BVV(0x7fffffffffe000, 64)  # 设个高地址

    state.regs.rdx = claripy.BVV(0x7fffffffffdfe8, 64)
# state.memory.store(0x7fffffffffdfe8 - 0x108, claripy.BVV(0, 64))

# 手动在栈顶写入一个“假的返回地址”，防止后面ret或call出问题
    state.memory.store(0x7fffffffffe000, claripy.BVV(0xdeadbeefdeadbeef, 64))

    state.memory.store(0x1A707D330, int.to_bytes(0x1A703AA78, 16, 'little'))
#put()
    state.memory.store(0x1A707D320, int.to_bytes(0x1A703AA50, 16, 'little'))
#virtualprotect()
    state.memory.store(0x1A71B2210, int.to_bytes(0xDEADBEFF00, 16, 'little'))

    simgr = proj.factory.simulation_manager(state)
# simgr.use_technique(angr.exploration_techniques.Veritesting())
    simgr.explore(find=find_address,avoid_address=avoid_address)
# print("start explore")
# print(simgr)
# print(simgr.errored)
if simgr.found:
        found = simgr.found[0]
# print("[+] Found a solution!")
        ans = found.solver.eval(claripy.Concat(*input_bytes),cast_to=bytes)
print(ans)
# print(found.step().regs.rip)
# store_ans(ans)
return ans

# find_ans(0x140001510, file_path='nfuncs_fast.exe')

import pefile
from unicorn import *
from unicorn.x86_const import *
from my_angr import find_ans, store_ans
import time
from capstone import *

# actually not so fast

# with open('last-ans.bin', 'rb') as f:
#     ANS = f.read()

# ans = bytearray(reversed(ANS))

PE_PATH = "nfuncs_fast.exe"

with open("checkpoint.txt", 'r') as f:
    FUN_VA = int(f.read(), 16)
    # print("FUN_VA:", hex(FUN_VA))

# FUN_VA = 0x140001510
STACK_ADDR = 0xDEADBEEF000
STACK_SIZE = 0x10000
CODE_EXEC_LIMIT = 0x10000
SMC_LIMIT = 0x40000

def store_checkpoint(addr):
     with open("checkpoint.txt",'w') as f:
            f.write(hex(addr))

def hook_instruction(uc, address, size, user_data):
            if address == 0xDEADBEEF100:
                addr = uc.reg_read(UC_X86_REG_RCX)
                size = uc.reg_read(UC_X86_REG_RDX)
print(f"[+] Hooked VirtualProtect:")
print(f"    -> Address: {hex(addr)}")
print(f"    -> Size   : {hex(size)}")
                # print("before read")
                smcs[addr] = uc.mem_read(addr, size)
                # print("after read")

                uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
            elif address == 0x1A703AA78:
                # print("read() called")

                assert uc.reg_read(UC_X86_REG_RCX) == 0 and uc.reg_read(UC_X86_REG_R8) == 1
                if ans:
                    byte = ans.pop()
                    uc.mem_write(uc.reg_read(UC_X86_REG_RDX), bytes([byte]))
                    uc.reg_write(UC_X86_REG_RAX, 1)
                    uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                    uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
                else:
print("input drained")
                    uc.emu_stop()
            elif address == 0x1A703AA50: 
                # print("puts() called")
                uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)

# print(len(pe.sections))
mu = Uc(UC_ARCH_X86,UC_MODE_64)

mu.mem_map(STACK_ADDR, STACK_SIZE)
mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE // 2)
pe = pefile.PE(PE_PATH, fast_load=True)
base_address = pe.OPTIONAL_HEADER.ImageBase
for section in pe.sections:
    sectionName = section.Name.strip(b' ')
    # if(sectionName == b'.text'):
    #     start = base_address + section.VirtualAddress
    #     size = section.Misc_VirtualSize
    #     mu.mem_map(FUN_VA &~ 0xfff,SMC_LIMIT*2)
    #     mu.mem_write(FUN_VA,section.get_data()[FUN_VA-start:
FUN_VA-start+SMC_LIMIT])
    #     print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
    # else:
    start = base_address + section.VirtualAddress
    size = section.Misc_VirtualSize
    mu.mem_map(start,(size + 0xfff) &~ 0xfff)
    mu.mem_write(start,section.get_data())
print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
    #register hook
mu.hook_add(UC_HOOK_CODE, hook_instruction)

mu.mem_write(0x1A71B2210, int.to_bytes(0xDEADBEEF100, 16, 'little'))

with open(PE_PATH, 'r+b') as f:
    while True:
        # try:

            # code = mu.mem_read(FUN_VA,SMC_LIMIT)
            # print(hex(len(code)))
            # md = Cs(CS_ARCH_X86, CS_MODE_64)
            # for i in md.disasm(code, FUN_VA):
            #     print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")

print("FUN_VA:", hex(FUN_VA))
            ANS = find_ans(FUN_VA,file_path=PE_PATH)
            ans = bytearray(reversed(ANS))
            smcs = {}

#emulation start
            mu.emu_start(FUN_VA, FUN_VA + CODE_EXEC_LIMIT)

            for addr, data in smcs.items():
print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
                for section in pe.sections:
                    sectionName = section.Name.strip(b' ')
if(sectionName == b'.text'):
                        start = base_address + section.VirtualAddress
                        size = section.Misc_VirtualSize
                        # if addr >= start and addr < start + size:
                        #     print(f'Committing code changes at {addr:#x}')
                            # print(section.PointerToRawData)

                        f.seek(section.PointerToRawData + addr - start)
                        f.write(data)
                        # next_code = section.get_data()[addr-start:
addr-start+SMC_LIMIT]
                        # mu.mem_unmap(FUN_VA &~ 0xfff, SMC_LIMIT*4)
                        # mu.mem_map(addr &~ 0xfff, SMC_LIMIT*2)
                        # mu.mem_write(addr, next_code)
                        # len_data = len(data)
                        # next_addr = addr + len_data
                        # print(hex(next_addr),  hex(len_data))
                        # mu.mem_write(next_addr,section.get_data()[next_addr-start:
SMC_LIMIT * 2 - len_data])
                        # mu.mem_write(start,section.get_data())
                        break
                FUN_VA = addr
store_ans(ANS)
store_checkpoint(addr)

    # 
except Exception as e:
    #     end_time = time.time()
    #     print(f"总耗时：{end_time - start_time:.2f} 秒")
    #     print(f'[!] Unicorn error: {e}')
    #     break

import pefilefrom unicorn import *from unicorn.x86_const import *from my_angr_2 import get_file_slice, find_ans, store_ansfrom capstone import *from capstone.x86_const import *from decrypted import decrypt
# with open('last-ans.bin', 'rb') as f:#     ANS = f.read()
# ans = bytearray(reversed(ANS))PE_PATH = "nfuncs_fast.exe"# #0x193c22610 #0x17dcd166e
# FUN_VA = 0x153022570 #0x149C8CA50 #140001510with open("checkpoint.txt", 'r') as f:
FUN_VA = int(f.read(), 16)#0x146e3f760STACK_ADDR = 0xDEADBEEF000STACK_SIZE = 0x10000CODE_EXEC_LIMIT = 0x1000ans_address = NoneANS = Nonedef store_checkpoint(addr):
with open("checkpoint.txt",'w') as f:f.write(hex(addr))def find_key_enc(FUN_VA, file_path):md = Cs(CS_ARCH_X86, CS_MODE_64)md.detail = Truefunc_code = get_file_slice(file_path, FUN_VA, 0x1000)for i in md.disasm(func_code, FUN_VA):# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
# find key mov rax, keyif i.mnemonic == 'movabs' and 'rax' in i.op_str and '0x' in i.op_str:
key = i.op_str.split(',')[1].strip()key = int(key, 16)
# print(key)return keydef hook_instruction(uc, address, size, user_data):
global ans_addressglobal ANSif address == 0xDEADBEEF100:
addr = uc.reg_read(UC_X86_REG_RCX)size = uc.reg_read(UC_X86_REG_RDX)print(f"[+] Hooked VirtualProtect:")print(f"    -> Address: {hex(addr)}")print(f"    -> Size   : {hex(size)}")smcs[addr] = uc.mem_read(addr, size)
# for addr, data in smcs.items():#     # print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
#     print(data[:8])uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)elif address == 0x1A703AA78:# print("read() called")assert uc.reg_read(UC_X86_REG_RCX) == 0 and uc.reg_read(UC_X86_REG_R8) == 1if ans:
byte = ans.pop()ans_address = uc.reg_read(UC_X86_REG_RDX)
# print(f"ans_address: {hex(ans_address)}")uc.mem_write(uc.reg_read(UC_X86_REG_RDX), bytes([byte]))uc.reg_write(UC_X86_REG_RAX, 1)uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)else:
print("input drained")uc.emu_stop()elif address == 0x1A703AA50:# print("puts() called")ss =  uc.mem_read(uc.reg_read(UC_X86_REG_RCX),4)
# print(f"ss: {ss}")uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)elif address == 0x1A703AA40:# print("memcmp() called")enc_text = uc.mem_read(uc.reg_read(UC_X86_REG_RDX), 8)
# print(enc_text)dec_text = decrypt(key, enc_text)
# print(dec_text)uc.mem_write(ans_address-7, dec_text)ANS = dec_text
# print(f"ans_address: {hex(ans_address - 7)}")uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)uc.reg_write(UC_X86_REG_RAX, 0)mu = Uc(UC_ARCH_X86,UC_MODE_64)mu.mem_map(STACK_ADDR, STACK_SIZE)mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE // 2)pe = pefile.PE(PE_PATH, fast_load=True)base_address = pe.OPTIONAL_HEADER.ImageBasefor section in pe.sections:
sectionName = section.Name.strip(b' ')
# if(sectionName == b'.text'):
start = base_address + section.VirtualAddresssize = section.Misc_VirtualSizemu.mem_map(start,(size + 0xfff) &~ 0xfff)mu.mem_write(start,section.get_data())print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
# #register hookmu.hook_add(UC_HOOK_CODE, hook_instruction)mu.mem_write(0x1A71B2210, int.to_bytes(0xDEADBEEF100, 16, 'little'))with open(PE_PATH, 'r+b') as f:
while True:# try:
print("FUN_VA:", hex(FUN_VA))ANS = find_ans(FUN_VA,file_path=PE_PATH)ans = bytearray(8)if ANS != None:
ans = bytearray(reversed(ANS))else:
key = find_key_enc(FUN_VA, file_path=PE_PATH)smcs = {}ans_address = None      #emulation startmu.emu_start(FUN_VA, FUN_VA + CODE_EXEC_LIMIT)for addr, data in smcs.items():
print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
# print(data[:8])
# mu.mem_write(addr, bytes(data))code = datafor section in pe.sections:
sectionName = section.Name.strip(b' ')if(sectionName == b'.text'):
start = base_address + section.VirtualAddresssize = section.Misc_VirtualSize
# if addr >= start and addr < start + size:#     print(f'Committing code changes at {addr:#x}')
# print(section.PointerToRawData)f.seek(section.PointerToRawData + addr - start)f.write(data)breakFUN_VA = addrstore_ans(ANS)store_checkpoint(addr)
# 
except Exception as e:#     end_time = time.time()
#     print(f"总耗时：{end_time - start_time:.2f} 秒")
#     print(f'[!] Unicorn error: {e}')    #     break

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-950548.htm

*本文为看雪论坛优秀文章，由 SleepAlone 原创，转载请注明来自看雪社区

# 往期推荐

miniL2025 mmapheap 题解

Redis漏洞分析，ACL篇

VMProtect3.5.1脱壳临床指南

2025长城杯决赛应急响应木马分析

APP 常见的 libmsaoaidsec.so 绕过姿势

球分享

球点赞

球在看

点击阅读原文查看更多


```
read(0, DstBuf, 1u);  read(0, &DstBuf[1], 1u);read(0, &DstBuf[2], 1u);read(0, &DstBuf[3], 1u);read(0, &DstBuf[4], 1u);read(0, &DstBuf[5], 1u);read(0, &DstBuf[6], 1u);read(0, &DstBuf[7], 1u);v0 = 32 * (DstBuf[0] & 1);if ( (DstBuf[0] & 2) != 0 )v0 = (32 * (DstBuf[0] & 1)) | 0x40;if ( (DstBuf[0] & 4) != 0 )v0 |= 0x80u;if ( (DstBuf[0] & 8) != 0 )v0 |= 0x10u;if ( (DstBuf[0] & 0x10) != 0 )v0 |= 1u;if ( (DstBuf[0] & 0x20) != 0 )v0 |= 2u;if ( (DstBuf[0] & 0x40) != 0 )v0 |= 8u;if ( DstBuf[0] < 0 )v0 |= 4u;v1 = v0 & 0xDF;if ( (DstBuf[1] & 1) != 0 )v1 = v0 | 0x20;v2 = v1 | 0x40;v3 = v1 & 0xBF;if ( (DstBuf[1] & 2) != 0 )v3 = v2;v4 = v3 | 0x80;v5 = v3 & 0x7F;if ( (DstBuf[1] & 4) != 0 )v5 = v4;v6 = v5 | 0x10;v7 = v5 & 0xEF;if ( (DstBuf[1] & 8) != 0 )v7 = v6;v8 = v7 | 1;v9 = v7 & 0xFE;if ( (DstBuf[1] & 0x10) != 0 )v9 = v8;v10 = v9 | 2;v11 = v9 & 0xFD;if ( (DstBuf[1] & 0x20) != 0 )v11 = v10;v12 = v11 | 8;v13 = v11 & 0xF7;if ( (DstBuf[1] & 0x40) != 0 )v13 = v12;v14 = v13 | 4;v15 = v13 & 0xFB;if ( DstBuf[1] < 0 )v15 = v14;v16 = v15 & 0xDF;if ( (DstBuf[2] & 1) != 0 )v16 = v15 | 0x20;v17 = v16 | 0x40;v18 = v16 & 0xBF;if ( (DstBuf[2] & 2) != 0 )v18 = v17;v19 = v18 | 0x80;v20 = v18 & 0x7F;if ( (DstBuf[2] & 4) != 0 )v20 = v19;v21 = v20 | 0x10;v22 = v20 & 0xEF;if ( (DstBuf[2] & 8) != 0 )v22 = v21;v23 = v22 | 1;v24 = v22 & 0xFE;if ( (DstBuf[2] & 0x10) != 0 )v24 = v23;v25 = v24 | 2;v26 = v24 & 0xFD;if ( (DstBuf[2] & 0x20) != 0 )v26 = v25;v27 = v26 | 8;v28 = v26 & 0xF7;if ( (DstBuf[2] & 0x40) != 0 )v28 = v27;v29 = v28 | 4;v30 = v28 & 0xFB;if ( DstBuf[2] < 0 )v30 = v29;v31 = v30 & 0xDF;if ( (DstBuf[3] & 1) != 0 )v31 = v30 | 0x20;v32 = v31 | 0x40;v33 = v31 & 0xBF;if ( (DstBuf[3] & 2) != 0 )v33 = v32;v34 = v33 | 0x80;v35 = v33 & 0x7F;if ( (DstBuf[3] & 4) != 0 )v35 = v34;v36 = v35 | 0x10;v37 = v35 & 0xEF;if ( (DstBuf[3] & 8) != 0 )v37 = v36;v38 = v37 | 1;v39 = v37 & 0xFE;if ( (DstBuf[3] & 0x10) != 0 )v39 = v38;v40 = v39 | 2;v41 = v39 & 0xFD;if ( (DstBuf[3] & 0x20) != 0 )v41 = v40;v42 = v41 | 8;v43 = v41 & 0xF7;if ( (DstBuf[3] & 0x40) != 0 )v43 = v42;v44 = v43 | 4;v45 = v43 & 0xFB;if ( DstBuf[3] < 0 )v45 = v44;v46 = v45 & 0xDF;if ( (DstBuf[4] & 1) != 0 )v46 = v45 | 0x20;v47 = v46 | 0x40;v48 = v46 & 0xBF;if ( (DstBuf[4] & 2) != 0 )v48 = v47;v49 = v48 | 0x80;v50 = v48 & 0x7F;if ( (DstBuf[4] & 4) != 0 )v50 = v49;v51 = v50 | 0x10;v52 = v50 & 0xEF;if ( (DstBuf[4] & 8) != 0 )v52 = v51;v53 = v52 | 1;v54 = v52 & 0xFE;if ( (DstBuf[4] & 0x10) != 0 )v54 = v53;v55 = v54 | 2;v56 = v54 & 0xFD;if ( (DstBuf[4] & 0x20) != 0 )v56 = v55;v57 = v56 | 8;v58 = v56 & 0xF7;if ( (DstBuf[4] & 0x40) != 0 )v58 = v57;v59 = v58 | 4;v60 = v58 & 0xFB;if ( DstBuf[4] < 0 )v60 = v59;v61 = v60 & 0xDF;if ( (DstBuf[5] & 1) != 0 )v61 = v60 | 0x20;v62 = v61 | 0x40;v63 = v61 & 0xBF;if ( (DstBuf[5] & 2) != 0 )v63 = v62;v64 = v63 | 0x80;v65 = v63 & 0x7F;if ( (DstBuf[5] & 4) != 0 )v65 = v64;v66 = v65 | 0x10;v67 = v65 & 0xEF;if ( (DstBuf[5] & 8) != 0 )v67 = v66;v68 = v67 | 1;v69 = v67 & 0xFE;if ( (DstBuf[5] & 0x10) != 0 )v69 = v68;v70 = v69 | 2;v71 = v69 & 0xFD;if ( (DstBuf[5] & 0x20) != 0 )v71 = v70;v72 = v71 | 8;v73 = v71 & 0xF7;if ( (DstBuf[5] & 0x40) != 0 )v73 = v72;v74 = v73 | 4;v75 = v73 & 0xFB;if ( DstBuf[5] < 0 )v75 = v74;v76 = v75 & 0xDF;if ( (DstBuf[6] & 1) != 0 )v76 = v75 | 0x20;v77 = v76 | 0x40;v78 = v76 & 0xBF;if ( (DstBuf[6] & 2) != 0 )v78 = v77;v79 = v78 | 0x80;v80 = v78 & 0x7F;if ( (DstBuf[6] & 4) != 0 )v80 = v79;v81 = v80 | 0x10;v82 = v80 & 0xEF;if ( (DstBuf[6] & 8) != 0 )v82 = v81;v83 = v82 | 1;v84 = v82 & 0xFE;if ( (DstBuf[6] & 0x10) != 0 )v84 = v83;v85 = v84 | 2;v86 = v84 & 0xFD;if ( (DstBuf[6] & 0x20) != 0 )v86 = v85;v87 = v86 | 8;v88 = v86 & 0xF7;if ( (DstBuf[6] & 0x40) != 0 )v88 = v87;v89 = v88 | 4;v90 = v88 & 0xFB;if ( DstBuf[6] < 0 )v90 = v89;v91 = v90 & 0xDF;if ( (DstBuf[7] & 1) != 0 )v91 = v90 | 0x20;v92 = v91 | 0x40;v93 = v91 & 0xBF;if ( (DstBuf[7] & 2) != 0 )v93 = v92;v94 = v93 | 0x80;v95 = v93 & 0x7F;if ( (DstBuf[7] & 4) != 0 )v95 = v94;v96 = v95 | 0x10;v97 = v95 & 0xEF;if ( (DstBuf[7] & 8) != 0 )v97 = v96;v98 = v97 | 1;v99 = v97 & 0xFE;if ( (DstBuf[7] & 0x10) != 0 )v99 = v98;v100 = v99 | 2;v101 = v99 & 0xFD;if ( (DstBuf[7] & 0x20) != 0 )v101 = v100;v102 = v101 | 8;v103 = v101 & 0xF7;if ( (DstBuf[7] & 0x40) != 0 )v103 = v102;v104 = v103 | 4;v105 = v103 & 0xFB;if ( DstBuf[7] < 0 )v105 = v104;if ( v0 == -77 && !(v45 | (unsigned __int8)(v30 | v15)) && v60 == 32 && v75 == 107 && v90 == 73 && v105 == -24 ){strcpy(v108, ":)");puts(v108);v110[0] = 0LL;v110[1] = 0LL;sub_14003A1C0(v110, *(_QWORD *)DstBuf + 2815032436LL);VirtualProtect(sub_140055A50, 0x17960uLL, 0x40u, &v109);for ( i = 0LL; i != 96608; ++i )*(_BYTE *)(i + 0x140055A50LL) ^= *((_BYTE *)v110 + (i & 0xF));VirtualProtect(sub_140055A50, 0x17960uLL, v109, 0LL);
return sub_140055A50();}else{strcpy(Buffer, ":(");
return puts(Buffer);}}
def collect_cmp_value(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        cmps = []
        for i in md.disasm(func_code, base_addr):

            if i.mnemonic == 'cmp':
                # print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                op2 =  i.op_str.split(',')[1].strip()
                if i.operands[1].type == X86_OP_IMM :
                    op2 = int(op2, 16)
                    if op2 < 0x100:
                        # print(f"op2: {op2}")
                        cmps.append(op2)
            if i.mnemonic == 'test':
                cmps.append(0)
            if len(cmps) == 8:
                break
import angr 
import claripy
import io
from angr.calling_conventions import SimCCMicrosoftAMD64
from angr.errors import SimProcedureError
from capstone import *
import archinfo
from capstone.x86_const import *

def rva_to_foa(addr):
return addr - 0x140001000 + 0x400

def get_file_slice(file_path, start, size):
    start = rva_to_foa(start)
with open(file_path, 'rb') as f:
        f.seek(start)
return f.read(size)

def store_ans(ans):
with open("all-ans.bin",'a+b') as f1:
# print("write all-ans")
print(ans)
        f1.write(ans)
        f1.flush()
with open('last-ans.bin','wb') as f:
        f.write(ans) 

# last_read_return_address = None

is_lut = False

def find_ans(FUN_VA, file_path='nfuncs1.exe'):
global is_lut
    input_bytes = []
class ReadHook(angr.SimProcedure):
def run(self, fd, buf, cnt):
global last_read_return_address
            fd = self.state.solver.eval(fd)
            cnt = self.state.solver.eval(cnt)
            target_addr = self.state.solver.eval(buf)   
if fd != 0 or cnt != 1:
print(f'[!] Unexpected read: fd {fd}, count {cnt}')

# if len(input_bytes) == 0:
#      for i in range(256):
#         self.state.memory.store(target_addr-0x108 + i , (i+13) % 256, 8, endness=archinfo.Endness.LE)

            sym =  claripy.BVS(f"input_{len(input_bytes)}", 8)
            input_bytes.append(sym)

            self.state.memory.store(target_addr, sym)
# print(f"[+] Hooked: wrote symbolic byte to {hex(target_addr)}")
# rip = self.state.solver.eval(self.state.memory.load(self.state.regs.rsp,8,endness=archinfo.Endness.LE))
# last_read_return_address = rip
# print(f"[+] Hooked: rip {hex(rip)}")
            value  = self.state.solver.eval(self.state.memory.load(target_addr-0x108, 1),cast_to=int)
if value == 13 + len(input_bytes) - 1:
                is_lut = True
else:
                is_lut = False

# print(f"[+] Hooked: value {hex(value)}")
if len(input_bytes) == 8 and is_lut:
# print("is_lut")
                cmps = collect_cmp_value(FUN_VA)
if len(cmps) == 8: # nothing i can do
for i, target in enumerate(cmps):
# v12_expr = (index + 13) % 256
# print(hex(target))
                        self.state.solver.add(input_bytes[i] == target - 13)
# state.solver.add((input_bytes[i] + 13) % 256 == target)

class VirtualProtectHook(angr.SimProcedure):
def run(self, lpAddress, dwSize, flNewProtect, lpflOldProtect):
            addr = self.state.solver.eval(lpAddress)
            size = self.state.solver.eval(dwSize)
            prot = self.state.solver.eval(flNewProtect)

print(f"[+] Hooked VirtualProtect:")
print(f"    -> Address: {hex(addr)}")
print(f"    -> Size   : {hex(size)}")
print(f"    -> NewProt: {hex(prot)}")

return claripy.BVV(1, self.state.arch.bits)

class PutsHook(angr.SimProcedure):
def run(self,buf):
            str_address = self.state.solver.eval(buf)
            s = self.state.solver.eval(self.state.memory.load(str_address,3),cast_to=bytes)
print("input:",s) # b':)x00' or b':(x00'
if s == b':(x00':
print("[!] Detected bad output ':(', killing path.")
return claripy.BVV(1, self.state.arch.bits)

# FUN_VA =  0x14000F000
    func_code = get_file_slice(file_path, FUN_VA, 0x1000)

def find_avoid_address(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        find_address = None
        avoid_address = None
for i in md.disasm(func_code, base_addr):

# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
if i.mnemonic == 'mov' and  '0x283a' in i.op_str:
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                avoid_address = i.address
if i.mnemonic == 'mov' and  '0x293a' in i.op_str:
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                find_address = i.address
if find_address and avoid_address:
break
return (find_address,avoid_address)

def collect_cmp_value(base_addr):
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        cmps = []
for i in md.disasm(func_code, base_addr):

if i.mnemonic == 'cmp':
# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
                op2 =  i.op_str.split(',')[1].strip()
if i.operands[1].type == X86_OP_IMM :
                    op2 = int(op2, 16)
if op2 < 0x100:
# print(f"op2: {op2}")
                        cmps.append(op2)
if i.mnemonic == 'test':
                cmps.append(0)
if len(cmps) == 8:
break
# assert len(cmps) == 8, f"[-] cmps length is not 8!"
return cmps
# exit()

# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
    find_address,avoid_address = find_avoid_address(FUN_VA)
# assert avoid_address != None, f"[-] Can't find avoid address!"

    proj = angr.Project(io.BytesIO(func_code), auto_load_libs=False, main_opts={
'base_addr': FUN_VA,
'backend': 'blob',
'arch': 'X86_64',
'entry_point': 0, # just avoid warnings
    }, )

    #handle IAT 
    cc = SimCCMicrosoftAMD64(proj.arch)
    proj.hook(0x1A703AA78, ReadHook(cc=cc))
    proj.hook(0xDEADBEFF00, VirtualProtectHook(cc=cc))
    proj.hook(0x1A703AA50, angr.SIM_PROCEDURES['libc']['puts']())

    state = proj.factory.blank_state(addr=FUN_VA, add_options={
            angr.options.UNICORN,
            angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
            angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
        }) # faster

    #manually process relocations
    #read(0)

    state.regs.rsp = claripy.BVV(0x7fffffffffe000, 64)  # 设个高地址

    state.regs.rdx = claripy.BVV(0x7fffffffffdfe8, 64)
# state.memory.store(0x7fffffffffdfe8 - 0x108, claripy.BVV(0, 64))

# 手动在栈顶写入一个“假的返回地址”，防止后面ret或call出问题
    state.memory.store(0x7fffffffffe000, claripy.BVV(0xdeadbeefdeadbeef, 64))

    state.memory.store(0x1A707D330, int.to_bytes(0x1A703AA78, 16, 'little'))
    #put()
    state.memory.store(0x1A707D320, int.to_bytes(0x1A703AA50, 16, 'little'))
    #virtualprotect()
    state.memory.store(0x1A71B2210, int.to_bytes(0xDEADBEFF00, 16, 'little'))

    simgr = proj.factory.simulation_manager(state)
# simgr.use_technique(angr.exploration_techniques.Veritesting())
    simgr.explore(find=find_address,avoid_address=avoid_address)
# print("start explore")
# print(simgr)
# print(simgr.errored)
if simgr.found:
        found = simgr.found[0]
# print("[+] Found a solution!")
        ans = found.solver.eval(claripy.Concat(*input_bytes),cast_to=bytes)
print(ans)
# print(found.step().regs.rip)
# store_ans(ans)
return ans

# find_ans(0x140001510, file_path='nfuncs_fast.exe')
import pefile
from unicorn import *
from unicorn.x86_const import *
from my_angr import find_ans, store_ans
import time
from capstone import *

# actually not so fast

# with open('last-ans.bin', 'rb') as f:
#     ANS = f.read()

# ans = bytearray(reversed(ANS))

PE_PATH = "nfuncs_fast.exe"

with open("checkpoint.txt", 'r') as f:
    FUN_VA = int(f.read(), 16)
    # print("FUN_VA:", hex(FUN_VA))

# FUN_VA = 0x140001510
STACK_ADDR = 0xDEADBEEF000
STACK_SIZE = 0x10000
CODE_EXEC_LIMIT = 0x10000
SMC_LIMIT = 0x40000

def store_checkpoint(addr):
     with open("checkpoint.txt",'w') as f:
            f.write(hex(addr))

def hook_instruction(uc, address, size, user_data):
            if address == 0xDEADBEEF100:
                addr = uc.reg_read(UC_X86_REG_RCX)
                size = uc.reg_read(UC_X86_REG_RDX)
print(f"[+] Hooked VirtualProtect:")
print(f"    -> Address: {hex(addr)}")
print(f"    -> Size   : {hex(size)}")
                # print("before read")
                smcs[addr] = uc.mem_read(addr, size)
                # print("after read")

                uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
            elif address == 0x1A703AA78:
                # print("read() called")

                assert uc.reg_read(UC_X86_REG_RCX) == 0 and uc.reg_read(UC_X86_REG_R8) == 1
                if ans:
                    byte = ans.pop()
                    uc.mem_write(uc.reg_read(UC_X86_REG_RDX), bytes([byte]))
                    uc.reg_write(UC_X86_REG_RAX, 1)
                    uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                    uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
                else:
print("input drained")
                    uc.emu_stop()
            elif address == 0x1A703AA50: 
                # print("puts() called")
                uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))
                uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)

# print(len(pe.sections))
mu = Uc(UC_ARCH_X86,UC_MODE_64)

mu.mem_map(STACK_ADDR, STACK_SIZE)
mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE // 2)
pe = pefile.PE(PE_PATH, fast_load=True)
base_address = pe.OPTIONAL_HEADER.ImageBase
for section in pe.sections:
    sectionName = section.Name.strip(b' ')
    # if(sectionName == b'.text'):
    #     start = base_address + section.VirtualAddress
    #     size = section.Misc_VirtualSize
    #     mu.mem_map(FUN_VA &~ 0xfff,SMC_LIMIT*2)
    #     mu.mem_write(FUN_VA,section.get_data()[FUN_VA-start:
FUN_VA-start+SMC_LIMIT])
    #     print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
    # else:
    start = base_address + section.VirtualAddress
    size = section.Misc_VirtualSize
    mu.mem_map(start,(size + 0xfff) &~ 0xfff)
    mu.mem_write(start,section.get_data())
print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
    #register hook
mu.hook_add(UC_HOOK_CODE, hook_instruction)

mu.mem_write(0x1A71B2210, int.to_bytes(0xDEADBEEF100, 16, 'little'))

with open(PE_PATH, 'r+b') as f:
    while True:
        # try:

            # code = mu.mem_read(FUN_VA,SMC_LIMIT)
            # print(hex(len(code)))
            # md = Cs(CS_ARCH_X86, CS_MODE_64)
            # for i in md.disasm(code, FUN_VA):
            #     print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")

print("FUN_VA:", hex(FUN_VA))
            ANS = find_ans(FUN_VA,file_path=PE_PATH)
            ans = bytearray(reversed(ANS))
            smcs = {}

    #emulation start
            mu.emu_start(FUN_VA, FUN_VA + CODE_EXEC_LIMIT)

            for addr, data in smcs.items():
print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
                for section in pe.sections:
                    sectionName = section.Name.strip(b' ')
if(sectionName == b'.text'):
                        start = base_address + section.VirtualAddress
                        size = section.Misc_VirtualSize
                        # if addr >= start and addr < start + size:
                        #     print(f'Committing code changes at {addr:#x}')
                            # print(section.PointerToRawData)

                        f.seek(section.PointerToRawData + addr - start)
                        f.write(data)
                        # next_code = section.get_data()[addr-start:
addr-start+SMC_LIMIT]
                        # mu.mem_unmap(FUN_VA &~ 0xfff, SMC_LIMIT*4)
                        # mu.mem_map(addr &~ 0xfff, SMC_LIMIT*2)
                        # mu.mem_write(addr, next_code)
                        # len_data = len(data)
                        # next_addr = addr + len_data
                        # print(hex(next_addr),  hex(len_data))
                        # mu.mem_write(next_addr,section.get_data()[next_addr-start:
SMC_LIMIT * 2 - len_data])
                        # mu.mem_write(start,section.get_data())
                        break
                FUN_VA = addr
store_ans(ANS)
store_checkpoint(addr)

    # 
except Exception as e:
    #     end_time = time.time()
    #     print(f"总耗时：{end_time - start_time:.2f} 秒")
    #     print(f'[!] Unicorn error: {e}')
    #     break
import pefilefrom unicorn import *from unicorn.x86_const import *from my_angr_2 import get_file_slice, find_ans, store_ansfrom capstone import *from capstone.x86_const import *from decrypted import decrypt
# with open('last-ans.bin', 'rb') as f:#     ANS = f.read()
# ans = bytearray(reversed(ANS))PE_PATH = "nfuncs_fast.exe"# #0x193c22610 #0x17dcd166e
# FUN_VA = 0x153022570 #0x149C8CA50 #140001510with open("checkpoint.txt", 'r') as f:
FUN_VA = int(f.read(), 16)#0x146e3f760STACK_ADDR = 0xDEADBEEF000STACK_SIZE = 0x10000CODE_EXEC_LIMIT = 0x1000ans_address = NoneANS = Nonedef store_checkpoint(addr):
with open("checkpoint.txt",'w') as f:f.write(hex(addr))def find_key_enc(FUN_VA, file_path):md = Cs(CS_ARCH_X86, CS_MODE_64)md.detail = Truefunc_code = get_file_slice(file_path, FUN_VA, 0x1000)for i in md.disasm(func_code, FUN_VA):# print(f"0x{i.address:x}:t{i.mnemonic}t{i.op_str}")
# find key mov rax, keyif i.mnemonic == 'movabs' and 'rax' in i.op_str and '0x' in i.op_str:
key = i.op_str.split(',')[1].strip()key = int(key, 16)
# print(key)return keydef hook_instruction(uc, address, size, user_data):
global ans_addressglobal ANSif address == 0xDEADBEEF100:
addr = uc.reg_read(UC_X86_REG_RCX)size = uc.reg_read(UC_X86_REG_RDX)print(f"[+] Hooked VirtualProtect:")print(f"    -> Address: {hex(addr)}")print(f"    -> Size   : {hex(size)}")smcs[addr] = uc.mem_read(addr, size)
# for addr, data in smcs.items():#     # print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
#     print(data[:8])uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)elif address == 0x1A703AA78:# print("read() called")assert uc.reg_read(UC_X86_REG_RCX) == 0 and uc.reg_read(UC_X86_REG_R8) == 1if ans:
byte = ans.pop()ans_address = uc.reg_read(UC_X86_REG_RDX)
# print(f"ans_address: {hex(ans_address)}")uc.mem_write(uc.reg_read(UC_X86_REG_RDX), bytes([byte]))uc.reg_write(UC_X86_REG_RAX, 1)uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)else:
print("input drained")uc.emu_stop()elif address == 0x1A703AA50:# print("puts() called")ss =  uc.mem_read(uc.reg_read(UC_X86_REG_RCX),4)
# print(f"ss: {ss}")uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)elif address == 0x1A703AA40:# print("memcmp() called")enc_text = uc.mem_read(uc.reg_read(UC_X86_REG_RDX), 8)
# print(enc_text)dec_text = decrypt(key, enc_text)
# print(dec_text)uc.mem_write(ans_address-7, dec_text)ANS = dec_text
# print(f"ans_address: {hex(ans_address - 7)}")uc.reg_write(UC_X86_REG_RIP, int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP),8),"little"))uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)uc.reg_write(UC_X86_REG_RAX, 0)mu = Uc(UC_ARCH_X86,UC_MODE_64)mu.mem_map(STACK_ADDR, STACK_SIZE)mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE // 2)pe = pefile.PE(PE_PATH, fast_load=True)base_address = pe.OPTIONAL_HEADER.ImageBasefor section in pe.sections:
sectionName = section.Name.strip(b' ')
# if(sectionName == b'.text'):
start = base_address + section.VirtualAddresssize = section.Misc_VirtualSizemu.mem_map(start,(size + 0xfff) &~ 0xfff)mu.mem_write(start,section.get_data())print(f"[+] Mapped {sectionName} at {hex(start)} ({hex(size)})")
# #register hookmu.hook_add(UC_HOOK_CODE, hook_instruction)mu.mem_write(0x1A71B2210, int.to_bytes(0xDEADBEEF100, 16, 'little'))with open(PE_PATH, 'r+b') as f:
while True:# try:
print("FUN_VA:", hex(FUN_VA))ANS = find_ans(FUN_VA,file_path=PE_PATH)ans = bytearray(8)if ANS != None:
ans = bytearray(reversed(ANS))else:
key = find_key_enc(FUN_VA, file_path=PE_PATH)smcs = {}ans_address = None      #emulation startmu.emu_start(FUN_VA, FUN_VA + CODE_EXEC_LIMIT)for addr, data in smcs.items():
print(f"[+] Committing changes to {hex(addr)} ({hex(len(data))})")
# print(data[:8])
# mu.mem_write(addr, bytes(data))code = datafor section in pe.sections:
sectionName = section.Name.strip(b' ')if(sectionName == b'.text'):
start = base_address + section.VirtualAddresssize = section.Misc_VirtualSize
# if addr >= start and addr < start + size:#     print(f'Committing code changes at {addr:#x}')
# print(section.PointerToRawData)f.seek(section.PointerToRawData + addr - start)f.write(data)breakFUN_VA = addrstore_ans(ANS)store_checkpoint(addr)
# 
except Exception as e:#     end_time = time.time()
#     print(f"总耗时：{end_time - start_time:.2f} 秒")
#     print(f'[!] Unicorn error: {e}')    #     break
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467260-wxsync-2025-06-c9e816614142944a7c29a060c1825af8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467264-wxsync-2025-06-376d9cf5487e7757e11f072ba55cf918.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467266-wxsync-2025-06-c980f6c32495145a1cc97be0a03dbf69.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467270-wxsync-2025-06-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467272-wxsync-2025-06-de64945aa0b604040631e8be49b0fa8e.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467273-wxsync-2025-06-de64945aa0b604040631e8be49b0fa8e.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467275-wxsync-2025-06-de64945aa0b604040631e8be49b0fa8e.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749467278-wxsync-2025-06-ff2718abd400f3bb9d1926e6f7ac8e37.gif)