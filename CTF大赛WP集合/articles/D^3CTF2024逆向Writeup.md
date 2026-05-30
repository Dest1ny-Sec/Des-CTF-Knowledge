# D^3CTF2024逆向Writeup

> 原文: https://www.ctfiot.com/176701.html
> ID: 176701

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
#!/usr/bin/env python

flag = [0x5406CBB1, 0xA4A41EA2, 0x34489AC5, 0x53D68797, 0xB8E0C06F, 0x259F2DB, 0x52E38D82, 0x595D5E1D]

k2 = 0xE8017300
k3 = 0xFF58F981
key = [0x5454, 0x4602, 0x4477, 0x5E5E, 0x33, 0x43, 0x54, 0x46]

for i in range(0, 7, 2):
    v6 = flag[i+1]
    v7 = flag[i]
    a2 = k2
    for _ in range(32)
        a2 = a2 + 0x100000000 - k3
        a2 &= 0xFFFFFFFF
    for _ in range(32):
        a2 += k3
        a2 &= 0xFFFFFFFF
        v6 = v6 + 0x100000000 - (((v7 + ((v7 << 5) ^ (v7 >> 6))) ^ (key[(a2>>11)&3]+a2) ^ 0x33) & 0xFFFFFFFF)
        v6 &= 0xFFFFFFFF
        v7 = v7 + 0x100000000 - (((v6 + ((v6 << 4) ^ (v6 >> 5))) ^ (key[a2&3]+a2) ^ 0x44) & 0xFFFFFFFF)
        v7 &= 0xFFFFFFFF
    flag[i+1] = v6
    flag[i] = v7
    print(hex(v7), hex(v6))

for f in flag:
    print(f.to_bytes(4, "little").decode(), end='')
# fakeflag{Is_there_anywhere_else}
```



```
复制代码 隐藏代码
flag = [0xB6DDB3A9, 0x36162C23, 0x1889FABF, 0x6CE4E73B, 0xA5AF8FC, 0x21FF8415, 0x44859557, 0x2DC227B7]

for i in range(8):
    for _ in range(32):
        v0 = flag[i]
        if ((v0 & 1) == 1):
            v0 ^= 0x84A6972F
            v0 = v0 >> 1
            v0 |= 0x80000000
        else:
            v0 = v0 >> 1
        flag[i] = v0
```



```
复制代码 隐藏代码
import idc
import idaapi

start = 0x717F

funcs = {}
# 递归找函数关系
def recur(addr):
    print(hex(addr))
    if (addr == 0x241A):
        return
    ea = addr
    value_dic = {}
    while (True):
        ins = idc.generate_disasm_line(ea, 0)
        if (ins.startswith("mov")):
            op0 = idc.print_operand(ea, 0)
            op1 = idc.print_operand(ea, 1)
            # 过滤eax rax
            if (op0[0] in "er"):
                op0 = op0[1:]
            if (op1[0] in "er"):
                op1 = op1[1:]
            value_dic[op0] = op1
            value_dic[op0] = op1
            if (op0.startswith("[rbp+var_")):
                if (op1[-1] != 'h'):
                    value_dic[op0] = value_dic[op1]
        # print(hex(ea), ins)
        if (ins == "call    _rand" and len(value_dic) >= 10):
            break
        ins_len = idc.create_insn(ea)
        ea += ins_len
    # xor
    print(value_dic)
    xor_ins = idc.print_operand(ea+0x36, 1)[:-1]
    xor = int(xor_ins, 16)
    nexts = []
    for i in ["60", "58", "50", "48", "40", "38", "30", "28", "20", "18"]:
        next = int(value_dic[f"[rbp+var_{i}]"][:-1], 16)
        next = ((next ^ xor) + addr) & 0xFFFFFFFFFFFFFFFF
        nexts.append(next)
    funcs[addr] = nexts
    for next in nexts:
        if (next not in funcs):
            recur(next)

ea = start
idc.set_name(ea, "main_main")
recur(ea)
print(funcs)

for ea in funcs:
    src = str(idaapi.decompile(ea)).split('n')
    print(f"{hex(ea)}: "{src[5]}",")
```



```
复制代码 隐藏代码
ops = {
0x717f: ([0x6bc8, 0x340a, 0x2917, 0x2db3, 0x6233, 0x4f23, 0x16f8, 0x1e22, 0x2f84, 0x2db3], "  array[r0] = 0;"),
0x6bc8: ([0x55a9, 0x604e, 0x3725, 0x2917, 0x1fb5, 0x2425, 0x6d19, 0x7095, 0x16f8, 0x26a4], "  *((_BYTE *)&flag + (unsigned __int8)r1) = ((int)*((unsigned __int8 *)&flag + (unsigned __int8)r1) >> array[r0]) | (*((_BYTE *)&flag + (unsigned __int8)r1) << (8 - array[r0]));"),
0x55a9: ([0x5c94, 0x62f3, 0x3d82, 0x3d82, 0x40cb, 0x3959, 0x5676, 0x40cb, 0x3f0e, 0x6154], "  array[r0] = 0;"),
0x5c94: ([0x1cd0, 0x3308, 0x1a4c, 0x1e22, 0x1cd0, 0x16f8, 0x16f8, 0x1a4c, 0x1a4c, 0x44aa], "  --r0;"),
0x1cd0: ([0x3f0e, 0x41aa, 0x66a4, 0x3a4b, 0x481b, 0x7375, 0x7375, 0x2cd4, 0x51ff, 0x5f5c], "  array[r0] = syscall((char)array[r0], (unsigned int)(char)array[r0 + 1], &array[r0 + 2], (unsigned int)(char)array[r0 + 3]);"),
0x3f0e: ([0x2917, 0x2917, 0x3bf0, 0x5676, 0x55a9, 0x5676, 0x3bf0, 0x3f0e, 0x3959, 0x3f0e], "  ++r0;"),
0x2917: ([0x340a, 0x43c2, 0x3e48, 0x24db, 0x24db, 0x1ee8, 0x55a9, 0x5002, 0x2425, 0x2771], "  *((_BYTE *)&flag + (unsigned __int8)r1) ^= array[r0];"),
0x340a: ([0x3f0e, 0x25b1, 0x42fc, 0x51ff, 0x3f0e, 0x5676, 0x64d3, 0x3058, 0x3f0e, 0x3959], "  array[r0] = syscall((char)array[r0], (unsigned int)(char)array[r0 + 1], &array[r0 + 2], (unsigned int)(char)array[r0 + 3]);"),
0x25b1: ([0x24db, 0x7809, 0x42fc, 0x5baf, 0x1ee8, 0x26a4, 0x4570, 0x5baf, 0x284a, 0x340a], "  *((_BYTE *)&flag + (unsigned __int8)r1) = array[r0];"),
0x24db: ([0x5754, 0x2f84, 0x3f0e, 0x42fc, 0x3d82, 0x7462, 0x3b11, 0x4f23, 0x2db3, 0x7375], "  array[r0] = 0;"),
0x5754: ([0x3876, 0x7809, 0x2261, 0x2261, 0x51ff, 0x6bc8, 0x340a, 0x51ff, 0x2261, 0x51ff], "  --array[r0];"),
0x3876: ([0x2cd4, 0x196d, 0x6ed7, 0x3876, 0x5002, 0x7462, 0x196d, 0x7462, 0x6ed7, 0x4a13], "  ++array[r0];"),
0x2cd4: ([0x63d2, 0x3725, 0x6154, 0x63d2, 0x3058, 0x196d, 0x209a, 0x2182, 0x2cd4, 0x6154], "  ++array[r0];"),
0x63d2: ([0x1b12, 0x5c94, 0x63d2, 0x472e, 0x1bf1, 0x43c2, 0x679b, 0x196d, 0x63d2, 0x7462], "  ++array[r0];"),
0x1b12: ([0x6154, 0x7462, 0x1b12, 0x6ed7, 0x2f84, 0x2e92, 0x3137, 0x4a13, 0x4a13, 0x1bf1], "  ++array[r0];"),
0x6154: ([0x6ed7, 0x65c5, 0x4a13, 0x6ed7, 0x5aa9, 0x5aa9, 0x43c2, 0x63d2, 0x679b, 0x3137], "  ++array[r0];"),
0x6ed7: ([0x209a, 0x2337, 0x209a, 0x6ed7, 0x3fd4, 0x6a77, 0x68a6, 0x209a, 0x3876, 0x6ed7], "  ++array[r0];"),
0x209a: ([0x5002, 0x3b11, 0x3058, 0x3216, 0x5103, 0x209a, 0x1b12, 0x4570, 0x5002, 0x5aa9], "  ++array[r0];"),
0x5002: ([0x5f5c, 0x604e, 0x209a, 0x3058, 0x6154, 0x2182, 0x196d, 0x4570, 0x4570, 0x3876], "  ++array[r0];"),
0x5f5c: ([0x7462, 0x2182, 0x5e5b, 0x5e5b, 0x1bf1, 0x2182, 0x2cd4, 0x6a77, 0x7541, 0x5f5c], "  ++array[r0];"),
0x7462: ([0x4570, 0x188f, 0x5e5b, 0x4f23, 0x5002, 0x7462, 0x196d, 0x2cd4, 0x3876, 0x4570], "  ++array[r0];"),
0x4570: ([0x65c5, 0x52ed, 0x5002, 0x4570, 0x3876, 0x209a, 0x604e, 0x16f8, 0x1a4c, 0x5f5c], "  ++array[r0];"),
0x65c5: ([0x2337, 0x52ed, 0x5002, 0x6ed7, 0x5e5b, 0x2337, 0x7462, 0x5c94, 0x52ed, 0x196d], "  ++array[r0];"),
0x2337: ([0x2337, 0x4f23, 0x196d, 0x5f5c, 0x196d, 0x3725, 0x1a4c, 0x604e, 0x4f23, 0x5f5c], "  ++array[r0];"),
0x4f23: ([0x16f8, 0x2db3, 0x3058, 0x62f3, 0x3b11, 0x3b11, 0x65c5, 0x62f3, 0x188f, 0x604e], "  ++array[r0];"),
0x16f8: ([0x6fb6, 0x6fb6, 0x340a, 0x1a4c, 0x5c94, 0x6233, 0x5c94, 0x1cd0, 0x5c94, 0x6a77], "  --r0;"),
0x6fb6: ([0x4f23, 0x40cb, 0x5e5b, 0x66a4, 0x604e, 0x2db3, 0x2db3, 0x6fb6, 0x6df8, 0x66a4], "  ++array[r0];"),
0x40cb: ([0x3725, 0x3725, 0x6233, 0x40cb, 0x464f, 0x6d19, 0x7375, 0x66a4, 0x464f, 0x40cb], "  ++array[r0];"),
0x3725: ([0x55a9, 0x2917, 0x5e5b, 0x48fe, 0x2425, 0x2b07, 0x136e, 0x2337, 0x724c, 0x66a4], "  *((_BYTE *)&flag + (unsigned __int8)r1) = ((int)*((unsigned __int8 *)&flag + (unsigned __int8)r1) >> array[r0]) | (*((_BYTE *)&flag + (unsigned __int8)r1) << (8 - array[r0]));"),
0x5e5b: ([0x5002, 0x5f5c, 0x63d2, 0x2337, 0x5f5c, 0x196d, 0x1b12, 0x2182, 0x1bf1, 0x5e5b], "  ++array[r0];"),
0x196d: ([0x5f5c, 0x604e, 0x2cd4, 0x63d2, 0x3876, 0x3876, 0x5e5b, 0x6154, 0x65c5, 0x5e5b], "  ++array[r0];"),
0x604e: ([0x2182, 0x66a4, 0x3876, 0x52ed, 0x188f, 0x62f3, 0x62f3, 0x4f23, 0x2337, 0x4570], "  ++array[r0];"),
0x2182: ([0x65c5, 0x52ed, 0x3876, 0x2182, 0x2337, 0x65c5, 0x2182, 0x5927, 0x3725, 0x5e5b], "  ++array[r0];"),
0x52ed: ([0x3b11, 0x52ed, 0x2182, 0x188f, 0x6fb6, 0x52ed, 0x65c5, 0x3b11, 0x188f, 0x52ed], "  ++array[r0];"),
0x3b11: ([0x2337, 0x6d19, 0x7462, 0x188f, 0x62f3, 0x3b11, 0x62f3, 0x6fb6, 0x66a4, 0x7462], "  ++array[r0];"),
0x6d19: ([0x6df8, 0x6df8, 0x188f, 0x66a4, 0x6fb6, 0x40cb, 0x66a4, 0x2db3, 0x464f, 0x2db3], "  ++array[r0];"),
0x6df8: ([0x464f, 0x40cb, 0x6d19, 0x6fb6, 0x6df8, 0x464f, 0x6fb6, 0x66a4, 0x6233, 0x464f], "  ++array[r0];"),
0x464f: ([0x40cb, 0x40cb, 0x6d19, 0x5927, 0x6df8, 0x464f, 0x188f, 0x6d19, 0x6bc8, 0x6233], "  ++array[r0];"),
0x5927: ([0x55a9, 0x1cd0, 0x16f8, 0x2b07, 0x64d3, 0x6a77, 0x3a4b, 0x41aa, 0x2261, 0x3e48], "  *((_BYTE *)&flag + (unsigned __int8)r1) = ((int)*((unsigned __int8 *)&flag + (unsigned __int8)r1) >> array[r0]) | (*((_BYTE *)&flag + (unsigned __int8)r1) << (8 - array[r0]));"),
0x2b07: ([0x3d82, 0x7809, 0x5e5b, 0x5676, 0x3a4b, 0x3e48, 0x5676, 0x3959, 0x6df8, 0x17be], "  array[r0] = 0;"),
0x3d82: ([0x2b07, 0x3f0e, 0x3959, 0x3d82, 0x7375, 0x3308, 0x48fe, 0x55a9, 0x5676, 0x3bf0], "  ++r0;"),
0x3959: ([0x53cc, 0x153a, 0x284a, 0x2917, 0x3bf0, 0x136e, 0x2b07, 0x2f84, 0x26a4, 0x55a9], "  ++r0;"),
0x53cc: ([0x472e, 0x2bdd, 0x2771, 0x4e18, 0x3137, 0x2182, 0x5baf, 0x7462, 0x43c2, 0x3959], "  array[r0] = 0;"),
0x472e: ([0x4e18, 0x6154, 0x5aa9, 0x63d2, 0x7541, 0x65c5, 0x3725, 0x43c2, 0x4e18, 0x66a4], "  ++array[r0];"),
0x4e18: ([0x679b, 0x5002, 0x472e, 0x2a19, 0x153a, 0x63d2, 0x2182, 0x2cd4, 0x3137, 0x42fc], "  ++array[r0];"),
0x679b: ([0x4e18, 0x1bf1, 0x3137, 0x679b, 0x7375, 0x3cbc, 0x62f3, 0x6ed7, 0x43c2, 0x55a9], "  ++array[r0];"),
0x1bf1: ([0x3137, 0x65c5, 0x1bf1, 0x209a, 0x3058, 0x63d2, 0x5aa9, 0x5f5c, 0x4e18, 0x3058], "  ++array[r0];"),
0x3137: ([0x1610, 0x3a4b, 0x3137, 0x3216, 0x3959, 0x4a13, 0x1b12, 0x1bf1, 0x68a6, 0x3876], "  ++array[r0];"),
0x1610: ([0x3725, 0x2e92, 0x340a, 0x6233, 0x481b, 0x44aa, 0x4d52, 0x2f84, 0x7375, 0x16f8], "  ++array[r0];"),
0x2e92: ([0x188f, 0x43c2, 0x6233, 0x3876, 0x65c5, 0x464f, 0x196d, 0x679b, 0x4b0f, 0x7375], "  ++array[r0];"),
0x188f: ([0x62f3, 0x6df8, 0x6bc8, 0x52ed, 0x6fb6, 0x6fb6, 0x188f, 0x2182, 0x6d19, 0x52ed], "  ++array[r0];"),
0x62f3: ([0x604e, 0x6d19, 0x604e, 0x66a4, 0x4f23, 0x4570, 0x4f23, 0x2337, 0x3b11, 0x6fb6], "  ++array[r0];"),
0x66a4: ([0x6fb6, 0x2db3, 0x3b11, 0x188f, 0x4f23, 0x464f, 0x2db3, 0x66a4, 0x6d19, 0x2db3], "  ++array[r0];"),
0x2db3: ([0x3b11, 0x6df8, 0x604e, 0x464f, 0x62f3, 0x6d19, 0x62f3, 0x2db3, 0x6df8, 0x6d19], "  ++array[r0];"),
0x43c2: ([0x3137, 0x5002, 0x1b12, 0x4a13, 0x1b12, 0x1bf1, 0x7809, 0x7809, 0x4a13, 0x679b], "  ++array[r0];"),
0x4a13: ([0x63d2, 0x65c5, 0x1b12, 0x3058, 0x68a6, 0x3058, 0x472e, 0x3876, 0x2cd4, 0x4a13], "  ++array[r0];"),
0x3058: ([0x2cd4, 0x5f5c, 0x1bf1, 0x472e, 0x5aa9, 0x6154, 0x43c2, 0x209a, 0x2cd4, 0x4e18], "  ++array[r0];"),
0x5aa9: ([0x1bf1, 0x2cd4, 0x6154, 0x43c2, 0x6df8, 0x3216, 0x2e92, 0x6154, 0x54ca, 0x5676], "  ++array[r0];"),
0x3216: ([0x7375, 0x3058, 0x5aa9, 0x5c94, 0x12a8, 0x78f1, 0x65c5, 0x11c9, 0x5103, 0x78f1], "  ++array[r0];"),
0x7375: ([0x26a4, 0x153a, 0x7095, 0x64d3, 0x7375, 0x3959, 0x284a, 0x7095, 0x78f1, 0x3bf0], "  ++r0;"),
0x26a4: ([0x5002, 0x3725, 0x2f84, 0x5676, 0x604e, 0x62f3, 0x2f84, 0x5754, 0x2bdd, 0x3876], "  array[r0] = 0;"),
0x2f84: ([0x136e, 0x1ee8, 0x48fe, 0x3959, 0x5833, 0x3565, 0x3bf0, 0x2f84, 0x3959, 0x724c], "  ++r0;"),
0x136e: ([0x2a19, 0x5f5c, 0x17be, 0x42fc, 0x3959, 0x78f1, 0x3e48, 0x3bf0, 0x2771, 0x3725], "  *((_BYTE *)&flag + (unsigned __int8)r1) ^= array[r0];"),
0x2a19: ([0x3bf0, 0x209a, 0x65c5, 0x3bf0, 0x3bf0, 0x24db, 0x7095, 0x78f1, 0x17be, 0x7095], "  *((_BYTE *)&flag + (unsigned __int8)r1) = array[r0];"),
0x3bf0: ([0x5754, 0x3d82, 0x3d82, 0x40cb, 0x464f, 0x3959, 0x6df8, 0x3d82, 0x5754, 0x481b], "  array[r0] = 0;"),
0x481b: ([0x48fe, 0x340a, 0x5676, 0x5754, 0x6ed7, 0x5d6d, 0x153a, 0x3cbc, 0x6df8, 0x2f84], "  ++r0;"),
0x48fe: ([0x1fb5, 0x2771, 0x241a, 0x44aa, 0x1fb5, 0x12a8, 0x5d6d, 0x5d6d, 0x5d6d, 0x5baf], "  *((_BYTE *)&flag + (unsigned __int8)r1) ^= array[r0];"),
0x1fb5: ([0x65c5, 0x2425, 0x69b1, 0x6d19, 0x464f, 0x241a, 0x5676, 0x153a, 0x2425, 0x3e48], "  array[r0] = *((_BYTE *)&flag + (unsigned __int8)r1);"),
0x2425: ([0x2cd4, 0x2f84, 0x3308, 0x3308, 0x48fe, 0x2a19, 0x48fe, 0x2a19, 0x3308, 0x2a19], "  ++r1;"),
0x3308: ([0x62f3, 0x724c, 0x5d6d, 0x5676, 0x3e48, 0x3e48, 0x5d6d, 0x6154, 0x1fb5, 0x5d6d], "  *((_BYTE *)&flag + (unsigned __int8)r1) ^= array[r0];"),
0x724c: ([0x16f8, 0x64d3, 0x2425, 0x7717, 0x2bdd, 0x3959, 0x4d52, 0x78f1, 0x2425, 0x2b07], "  *((_BYTE *)&flag + (unsigned __int8)r1) ^= array[r0];"),
0x64d3: ([0x3308, 0x5d6d, 0x3d82, 0x26a4, 0x724c, 0x209a, 0x51ff, 0x5002, 0x5676, 0x724c], "  ++r0;"),
0x5d6d: ([0x2425, 0x3e48, 0x3e48, 0x55a9, 0x5676, 0x3e48, 0x2a19, 0x3e48, 0x2425, 0x3e48], "  array[r0] = *((_BYTE *)&flag + (unsigned __int8)r1);"),
0x3e48: ([0x25b1, 0x2a19, 0x48fe, 0x48fe, 0x48fe, 0x2a19, 0x48fe, 0x2a19, 0x3308, 0x48fe], "  ++r1;"),
0x5676: ([0x2b07, 0x1ee8, 0x24db, 0x3d82, 0x7095, 0x5833, 0x24db, 0x7095, 0x7375, 0x3308], "  ++r0;"),
0x1ee8: ([0x2337, 0x6a77, 0x7375, 0x196d, 0x3a4b, 0x65c5, 0x679b, 0x63d2, 0x7717, 0x7462], "  array[r0] = 0;"),
0x6a77: ([0x24db, 0x5aa9, 0x51ff, 0x284a, 0x5927, 0x481b, 0x241a, 0x5baf, 0x6154, 0x40cb], "  *((_BYTE *)&flag + (unsigned __int8)r1) = ((int)*((unsigned __int8 *)&flag + (unsigned __int8)r1) >> array[r0]) | (*((_BYTE *)&flag + (unsigned __int8)r1) << (8 - array[r0]));"),
0x51ff: ([0x26a4, 0x55a9, 0x53cc, 0x5e5b, 0x51ff, 0x24db, 0x26a4, 0x4e18, 0x5d6d, 0x2b07], "  if ( (char)array[r0] < 0 ) rand();"),
0x284a: ([0x5676, 0x5e5b, 0x7375, 0x464f, 0x4570, 0x69b1, 0x7717, 0x1b12, 0x3f0e, 0x2337], "  array[r0] = 0;"),
0x69b1: ([0x78f1, 0x153a, 0x3d82, 0x6ed7, 0x42fc, 0x44aa, 0x7809, 0x2cd4, 0x51ff, 0x44aa], "  --r1;"),
0x78f1: ([0x7638, 0x5002, 0x41aa, 0x3876, 0x1a4c, 0x51ff, 0x3cbc, 0x7717, 0x2f84, 0x26a4], "  array[r0] = 0;"),
0x7638: ([0x5aa9, 0x44aa, 0x464f, 0x3876, 0x2a19, 0x3137, 0x3d82, 0x2337, 0x2261, 0x48fe], "  --array[r0];"),
0x44aa: ([0x44aa, 0x44aa, 0x44aa, 0x5c94, 0x69b1, 0x5d6d, 0x44aa, 0x69b1, 0x44aa, 0x44aa], "  --r1;"),
0x2261: ([0x7095, 0x17be, 0x7095, 0x26a4, 0x284a, 0x3bf0, 0x24db, 0x55a9, 0x6bc8, 0x24db], "  if ( (char)array[r0] < 0 ) rand();"),
0x7095: ([0x4570, 0x7717, 0x7375, 0x7717, 0x63d2, 0x4f23, 0x65c5, 0x5754, 0x7717, 0x3959], "  array[r0] = 0;"),
0x7717: ([0x17be, 0x1cd0, 0x3565, 0x2261, 0x3565, 0x5c94, 0x43c2, 0x2261, 0x2261, 0x3565], "  --array[r0];"),
0x17be: ([0x7717, 0x2425, 0x64d3, 0x284a, 0x2db3, 0x5002, 0x1ee8, 0x6df8, 0x6ed7, 0x2db3], "  array[r0] = 0;"),
0x3565: ([0x55a9, 0x16f8, 0x6df8, 0x48fe, 0x62f3, 0x6bc8, 0x55a9, 0x2f84, 0x17be, 0x363b], "  if ( (char)array[r0] < 0 ) rand();"),
0x363b: ([0x2771, 0x209a, 0x2917, 0x3565, 0x1b12, 0x1b12, 0x5676, 0x6fb6, 0x5754, 0x41aa], "  array[r0] = 0;"),
0x2771: ([0x4f23, 0x24db, 0x6a77, 0x25b1, 0x40cb, 0x25b1, 0x2a19, 0x2db3, 0x679b, 0x12a8], "  ++r1;"),
0x12a8: ([0x1cd0, 0x3725, 0x65c5, 0x17be, 0x7375, 0x2db3, 0x2a19, 0x604e, 0x1b12, 0x2425], "  ++r1;"),
0x41aa: ([0x1cd0, 0x3565, 0x6d19, 0x2f84, 0x3137, 0x2261, 0x1cd0, 0x481b, 0x66a4, 0x3137], "  array[r0] = syscall((char)array[r0], (unsigned int)(char)array[r0 + 1], &array[r0 + 2], (unsigned int)(char)array[r0 + 3]);"),
0x1a4c: ([0x1e22, 0x41aa, 0x6233, 0x1e22, 0x340a, 0x16f8, 0x1a4c, 0x6233, 0x6233, 0x16f8], "  --r0;"),
0x1e22: ([0x1a4c, 0x4a13, 0x24db, 0x24db, 0x1cd0, 0x1a4c, 0x340a, 0x340a, 0x5c94, 0x42fc], "  --r0;"),
0x42fc: ([0x3058, 0x7717, 0x7095, 0x7095, 0x6a77, 0x1cd0, 0x3e48, 0x5927, 0x63d2, 0x64d3], "  ++r0;"),
0x6233: ([0x340a, 0x1cd0, 0x6233, 0x340a, 0x6233, 0x6233, 0x1a4c, 0x340a, 0x340a, 0x1a4c], "  --r0;"),
0x3cbc: ([0x7375, 0x5754, 0x464f, 0x3bf0, 0x1a4c, 0x3cbc, 0x241a, 0x4a13, 0x1470, 0x55a9], "  --r0;"),
0x1470: ([0x5e5b, 0x340a, 0x3725, 0x40cb, 0x41aa, 0x2771, 0x3959, 0x1a4c, 0x5e5b, 0x188f], "  --r0;"),
0x153a: ([0x3a4b, 0x2f84, 0x1b12, 0x2337, 0x52ed, 0x209a, 0x4d52, 0x41aa, 0x43c2, 0x2182], "  array[r0] = 0;"),
0x3a4b: ([0x4c8c, 0x6bc8, 0x284a, 0x26a4, 0x24db, 0x26a4, 0x3f0e, 0x4d52, 0x6a77, 0x2f84], "  ++r0;"),
0x4c8c: ([0x340a, 0x3f0e, 0x1ee8, 0x1ee8, 0x3a4b, 0x4a13, 0x2bdd, 0x42fc, 0x7541, 0x41aa], "  ++r0;"),
0x2bdd: ([0x78f1, 0x63d2, 0x2a19, 0x136e, 0x284a, 0x724c, 0x5676, 0x2261, 0x2261, 0x3058], "  --array[r0];"),
0x7541: ([0x16f8, 0x62f3, 0x2b07, 0x2a19, 0x6154, 0x44aa, 0x42fc, 0x2cd4, 0x16f8, 0x51ff], "  ++r0;"),
0x4d52: ([0x7375, 0x7095, 0x51ff, 0x2f84, 0x5f5c, 0x604e, 0x25b1, 0x64d3, 0x3b11, 0x7375], "  ++r1;"),
0x7809: ([0x5002, 0x3959, 0x4d52, 0x241a, 0x1e22, 0x3cbc, 0x1e22, 0x7809, 0x7809, 0x5d6d], "  --r0;"),
0x5baf: ([0x3058, 0x66a4, 0x5754, 0x604e, 0x40cb, 0x241a, 0x196d, 0x3959, 0x5833, 0x2425], "  array[r0] = *((_BYTE *)&flag + (unsigned __int8)r1);"),
0x5833: ([0x5c94, 0x43c2, 0x7717, 0x51ff, 0x4f23, 0x5f5c, 0x2771, 0x42fc, 0x3959, 0x7375], "  array[r0] = 0;"),
0x11c9: ([0x62f3, 0x5aa9, 0x2182, 0x2cd4, 0x6154, 0x5f5c, 0x4a13, 0x241a, 0x3d82, 0x1fb5], "  ++array[r0];"),
0x5103: ([0x1a4c, 0x1b12, 0x5927, 0x64d3, 0x25b1, 0x2771, 0x5f5c, 0x4a13, 0x6233, 0x5f5c], "  ++array[r0];"),
0x54ca: ([0x209a, 0x1b12, 0x724c, 0x5baf, 0x209a, 0x5f5c, 0x2bdd, 0x3058, 0x3058, 0x3bf0], "  ++array[r0];"),
0x68a6: ([0x3565, 0x209a, 0x3308, 0x42fc, 0x6fb6, 0x42fc, 0x3725, 0x3058, 0x5aa9, 0x1bf1], "  ++array[r0];"),
0x4b0f: ([0x2917, 0x48fe, 0x3137, 0x5baf, 0x2bdd, 0x2425, 0x62f3, 0x2771, 0x136e, 0x5754], "  *((_BYTE *)&flag + (unsigned __int8)r1) = ((int)*((unsigned __int8 *)&flag + (unsigned __int8)r1) >> array[r0]) | (*((_BYTE *)&flag + (unsigned __int8)r1) << (8 - array[r0]));"),
0x3fd4: ([0x3bf0, 0x4a13, 0x209a, 0x6a77, 0x17be, 0x1cd0, 0x63d2, 0x5002, 0x63d2, 0x64d3], "  ++array[r0];")
}
```



```
复制代码 隐藏代码
"""
array[r0] = 0
array[r0] += 1
array[r0] -= 1
r0 += 1
r0 -= 1
r1 += 1
r1 -= 1
flag[r1] = (flag[r1] >> array[r0]) | (flag[r1] << (8 - array[r0]))
array[r0] = syscall(array[r0], array[r0+1], &array[r0+2], array[r0+3])
flag[r1] ^= array[r0]
flag[r1] = array[r0]
array[r0] = flag[r1]
if (array[r0] < 0) rand();
"""
```



```
复制代码 隐藏代码
pc = 0x717F
i = 0
skips = [18, 22, 48, 168, 172, 312, 340, 370, 397, 449, 478, 595, 599, 623, 627, 675]
while (pc != 0x241A):
    print(i, hex(pc), ops[pc][1])
    if (i in skips):
        i += 1
    r = rands[i]
    i += 1
    pc = ops[pc][0][r]
```



```
复制代码 隐藏代码
"""
16 0x284a   array[r0] = 0;
17 0x7717   --array[r0];
18 0x3565   if ( (char)array[r0] < 0 ) rand();
"""
```



```
复制代码 隐藏代码
"""
array[0] = 0
array[1] = 0
array[3] = 1
10    array[2] = getchar()
flag[0] ^= array[2]
flag[1] = array[2]
array[2] = 3
flag[1] = (flag[1] >> 3 | (flag[1] << 5)
flag[1] ^= 3
"""
```



```
复制代码 隐藏代码
"""
array[4] = 101
array[5] = 0
array[6] = 0
array[7] = 0
array[8] = 0
array[4] = syscall(101, 0, 0, 0) # ptrace反调试, 0
"""
```



```
复制代码 隐藏代码
"""
array[0] = 0
array[1] = 0
array[3] = 1
10    array[2] = getchar()
flag[0] ^= array[2]
flag[1] = array[2]
array[2] = 3
flag[1] = (flag[1] >> 3 | (flag[1] << 5)
flag[1] ^= 3

array[2] = 0
array[3] = 0
array[5] = 1
40      array[4] = getchar()
flag[1] ^= array[4]
flag[2] = array[4]

array[4] = 101
array[5] = 0
array[6] = 0
array[7] = 0
array[8] = 0
array[4] = syscall(101, 0, 0, 0) # ptrace反调试, 0

array[4] = 5
flag[2] = (flag[2] >> 5 | (flag[2] << 3)

array[4] = 0
array[5] = 0
array[7] = 1
191     array[6] = getchar()    # array[4] = 1
flag[2] ^= array[6]
flag[3] = array[6]

array[6] = 101
array[7] = 0
array[8] = 0
array[9] = 0
array[10] = 0
array[6] = syscall(101, 0, 0, 0) # ptrace反调试, -1

array[6] = 6
flag[3] = (flag[3] >> 6 | (flag[3] << 2)

array[6] = 0
array[7] = 0
array[9] = 1
332     array[8] = getchar()    # array[6] = 1
flag[3] ^= array[8]
falg[4] = array[8]

array[8] = 7
flag[4] = (flag[4] >> 7 | (flag[4] << 1)
flag[4] ^= 7

array[8] = 0
arry[9] = 0
array[11] = 1
362     array[10] = getchar()   # array[8] = 1
flag[4] ^= array[10]
flag[5] = array[10]

array[10] = 4
flag[5] = (flag[5] >> 4 | (flag[5] << 4)
flag[5] ^= 4

array[10] = 0
array[11] = 0
array[13] = 1
389     array[12] = getchar()   # array[10] = 1
flag[5] ^= array[12]
flag[6] = array[12]

array[12] = 4
flag[6] = (flag[6] >> 4 | (flag[6] << 4)

array[12] = 0
array[13] = 0
array[15] = 1
415     array[14] = getchar()   # array[12] = 1
flag[6] ^= array[14]
flag[7] = array[14]

array[14] = 7
flag[7] = (flag[7] >> 7 | (flag[7] << 1)
flag[7] ^= 7

array[14] = 0
array[15] = 0
array[17] = 1
441     array[16] = getchar()   # array[14] = 1
flag[7] ^= array[16]
flag[8] = array[16]

array[16] = 7
flag[8] = (flag[8] >> 7 | (flag[8] << 1)

array[16] = 0
array[17] = 0
array[19] = 1
470    array[18] = getchar()   # array[16] = 1
flag[8] ^= array[18]
flag[9] = array[18]

flag[9] = (flag[9] >> 2 | (flag[9] << 6)

615     c = getchar()
flag[9] ^= c
flag[10] = c

flag[10] = (flag[10] >> 4) | (flag[10] << 4)

645     c = getchar()
flag[10] ^= c
flag[11] = c

flag[11] = (flag[11] >> 4) | (flag[11] << 4)

667     c = getchar()
flag[11] ^= c
flag[12] = c

flag[12] = (flag[12] >> 7) | (flag[12] << 1)
flag[12] ^= 7

flag[2] ^= flag[1]
.
.
.
flag[12] ^= flag[11]
"""
```



```
复制代码 隐藏代码
flag = [0, 0x9D, 0x6B, 0xA1, 0x02, 0xD7, 0xED, 0x40, 0xF6, 0x0E, 0xAE, 0x84, 0x19]
for i in range(12, 1, -1):
    flag[i] ^= flag[i-1]

flag[12] ^= 7
flag[12] = (flag[12] << 7) | (flag[12] >> 1)
flag[12] &= 0xFF

flag[11] ^= flag[12]
flag[11] = (flag[11] << 4) | (flag[11] >> 4)
flag[11] &= 0xFF

flag[10] ^= flag[11]
flag[10] = (flag[10] << 4) | (flag[10] >> 4)
flag[10] &= 0xFF

flag[9] ^= flag[10]
flag[9] = (flag[9] << 2) | (flag[9] >> 6)
flag[9] &= 0xFF

flag[8] ^= flag[9]
flag[8] = (flag[8] << 7) | (flag[8] >> 1)
flag[8] &= 0xFF

flag[7] ^= flag[8]
flag[7] ^= 7
flag[7] = (flag[7] << 7) | (flag[7] >> 1)
flag[7] &= 0xFF

flag[6] ^= flag[7]
flag[6] = (flag[6] << 4) | (flag[6] >> 4)
flag[6] &= 0xFF

flag[5] ^= flag[6]
flag[5] ^= 4
flag[5] = (flag[5] << 4) | (flag[5] >> 4)
flag[5] &= 0xFF

flag[4] ^= flag[5]
flag[4] ^= 7
flag[4] = (flag[4] << 7) | (flag[4] >> 1)
flag[4] &= 0xFF

flag[3] ^= flag[4]
flag[3] = (flag[3] << 6) | (flag[3] >> 2)
flag[3] &= 0xFF

flag[2] ^= flag[3]
flag[2] = (flag[2] << 5) | (flag[2] >> 3)
flag[2] &= 0xFF

flag[1] ^= flag[2]
flag[1] ^= 3
flag[1] = (flag[1] << 3) | (flag[1] >> 5)
flag[1] &= 0xFF

# flag[0] ^= flag[1]
print(bytes(flag))
```



```
复制代码 隐藏代码
unsigned int __thiscall execption_handle(unsigned int **this)
{
  unsigned int result; // eax
  unsigned int *v3; // ecx
  unsigned int *v4; // eax
  _DWORD *v5; // eax
  int v6; // ecx
  unsigned int v7; // edx
  void **v8; // ecx
  int v9; // esi
  int i; // ecx
  int v11; // edx
  int v12; // eax
  int v13; // esi
  int v14; // edx
  void **v15; // eax
  int v16; // [esp+10h] [ebp-2Ch]
  int v17; // [esp+14h] [ebp-28h]
  _DWORD *v18; // [esp+18h] [ebp-24h]

  GetCurrentThreadId();
  result = **this;
  if ( result <= 0xC0000005 )
  {
    if ( result != 0xC0000005 )
    {
      if ( result != 0x80000003 )
      {
        if ( result != 0x80000004 )
          return result;
        v3 = this[1];
        if ( ((v3[46] - (_DWORD)&code) & 0x3F) == 7 && v3[44] == 1 )
          v3[46] += 0x17;
        v4 = this[1];
        goto LABEL_33;
      }
      if ( byte_CE6028 )
      {
        byte_CE6028 = 0;
        R2 = (int)malloc(4u);
        R1 = (int)malloc(4u);
        v5 = malloc(4u);
        v6 = R1;
        v7 = kk;
        v18 = v5;
        R0 = (int)v5;
        *(_DWORD *)R1 = 0;
        *v5 = 0;
        v17 = v6;
        if ( (unsigned int)len > v7 )
        {
          v8 = &flag;
          if ( HIDWORD(len) >= 0x10 )
            v8 = (void **)flag;
          v16 = R2;
          v9 = 0;
          *(_DWORD *)R2 = *((_BYTE *)v8 + v7) != 0x30;
          kk = v7 + 1;
          for ( i = 0; i < 0x483D; ++i )
          {
            if ( *((_BYTE *)&code + i) == 0xFF
              && *((_BYTE *)&code + i + 1) == 0xFF
              && *((_BYTE *)&code + i + 2) == 0xFF
              && *((_BYTE *)&code + i + 3) == 0xFF )
            {
              v11 = v9 % 5;
              if ( v9 % 5 == 1 || v11 == 3 )
              {
                v12 = v17;                      // R1
              }
              else if ( v11 == 2 || v11 == 4 )
              {
                v12 = (int)v18;                 // R0
              }
              else
              {
                v12 = v16;                      // R2
              }
              *(_DWORD *)((char *)&code + i) = v12;
              ++v9;
              i += 3;
            }
          }
          this[1][46] = (unsigned int)&code;
          this[1][48] |= 0x100u;
          return -1;
        }
LABEL_39:
        sub_CE28B0();
      }
      return(0);
    }
    right();
  }
  if ( result != 0xC0000096 )
    return result;
  v13 = kk;
  v14 = *(_DWORD *)R1 + 17 * *(_DWORD *)R0;
  if ( kk >= (unsigned int)len )
  {
    return(1);
    goto LABEL_39;
  }
  v15 = &flag;
  if ( HIDWORD(len) >= 0x10 )
    v15 = (void **)flag;
  *(_DWORD *)R2 = *((_BYTE *)v15 + kk) != 0x30;
  kk = v13 + 1;
  this[1][46] = (unsigned int)&code + 0x40 * v14;
  v4 = this[1];
LABEL_33:
  v4[48] |= 0x100u;
  return -1;
}
```



```
复制代码 隐藏代码
// ksarm.h
#define STATUS_ACCESS_VIOLATION 0xc0000005
#define STAUSBREAKPOINT 0x80000003
#define STATUS_SINGLE_STEP 0x80000004
#define STATUS_PRIVILEGED_INSTRUCTION 0xc0000096
```



```
复制代码 隐藏代码
if (byte_CE6028)
{
    byte_CE6028 = 0;
    R2 = (int)malloc(4u);
    R1 = (int)malloc(4u);
    v5 = malloc(4u);
    v6 = R1;
    v7 = kk;
    v18 = v5;
    R0 = (int)v5;
    *(_DWORD *)R1 = 0;
    *v5 = 0;
    v17 = v6;
    if ((unsigned int)len > v7)
    {
        v8 = &flag;
        if (HIDWORD(len) >= 0x10)
            v8 = (void **)flag;
        v16 = R2;
        v9 = 0;
        *(_DWORD *)R2 = *((_BYTE *)v8 + v7) != 0x30;
        kk = v7 + 1;
        for (i = 0; i < 0x483D; ++i)
        {
            if (*((_BYTE *)&code + i) == 0xFF && *((_BYTE *)&code + i + 1) == 0xFF && *((_BYTE *)&code + i + 2) == 0xFF && *((_BYTE *)&code + i + 3) == 0xFF)
            {
                v11 = v9 % 5;
                if (v9 % 5 == 1 || v11 == 3)
                {
                    v12 = v17; // R1
                }
                else if (v11 == 2 || v11 == 4)
                {
                    v12 = (int)v18; // R0
                }
                else
                {
                    v12 = v16; // R2
                }
                *(_DWORD *)((char *)&code + i) = v12;
                ++v9;
                i += 3;
            }
        }
        this[1][46] = (unsigned int)&code;
        this[1][48] |= 0x100u;
        return -1;
    }
LABEL_39:
    sub_CE28B0();
}
```



```
复制代码 隐藏代码
v13 = kk;
v14 = *(_DWORD *)R1 + 17 * *(_DWORD *)R0;
if (kk >= (unsigned int)len)
{
    return (1);
    goto LABEL_39;
}
v15 = &flag;
if (HIDWORD(len) >= 0x10)
    v15 = (void **)flag;
*(_DWORD *)R2 = *((_BYTE *)v15 + kk) != 0x30;
kk = v13 + 1;
this[1][46] = (unsigned int)&code + 0x40 * v14;
v4 = this[1];
v4[48] |= 0x100u;
```



```
复制代码 隐藏代码
if (result != 0x80000004)
    return result;
v3 = this[1];
if (((v3[46] - (_DWORD)&code) & 0x3F) == 7 && v3[44] == 1)
    v3[46] += 0x17;
v4 = this[1];
v4[48] |= 0x100u;
```



```
复制代码 隐藏代码
import idc
import idaapi

image_base = idaapi.get_imagebase()
code_off = 0x6030
code_size = 0x4840

start = image_base + code_off
end = image_base + code_off + code_size

op_ls = [(-1, -1) for _ in range(0x121)]
for idx in range(0x121):
    ea = start + idx * 0x40
    print(f"[{hex(ea)}]: ")
    ins = idc.generate_disasm_line(ea, 0)
    if (ins.startswith("mov     eax, 0FFFFFFFFh")):
        op1 = idc.print_operand(ea+0x0C, 1)
        if (op1[-1] == 'h'):
            op1 = int(op1[:-1], 16)
        else:
            op1 = int(op1)
        op2 = idc.print_operand(ea+0x17, 1)
        if (op2[-1] == 'h'):
            op2 = int(op2[:-1], 16)
        else:
            op2 = int(op2)
        op3 = idc.print_operand(ea+0x23, 1)
        if (op3[-1] == 'h'):
            op3 = int(op3[:-1], 16)
        else:
            op3 = int(op3)
        op4 = idc.print_operand(ea+0x2E, 1)
        if (op4[-1] == 'h'):
            op4 = int(op4[:-1], 16)
        else:
            op4 = int(op4)
        ins = (op1+17*op2, op3+17*op4)
    elif (ins.startswith("int     3")):
        ins = (-1, -1)
    print(ins)
    op_ls[idx] = ins

print(op_ls)
```



```
复制代码 隐藏代码
"""
int     3
add     [ecx-51h], ebx
mov     eax, 1; mov     dword ptr [eax], 39393939h
add     [ebp+28D5560Ah], ecx
"""
```



```
复制代码 隐藏代码
op_ls = [(11, 41), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (193, 52), (7, 7), (216, 43), (116, 13), (120, 189), (82, 244), (12, 12), (8, 15), (-1, -1), (-1, -1), (72, 95), (233, 272), (211, 194), (-1, -1), (59, 230), (237, 89), (60, 190), (23, 23), (243, 232), 'add     [ecx-51h], ebx', (207, 224), 'mov     eax, 1', (31, 61), (151, 179), (12, 180), (-1, -1), (76, 147), (-1, -1), (153, 196), (279, 271), (-1, -1), (276, 7), (38, 38), (39, 39), (48, 171), (-1, -1), (236, 251), (16, 192), (-1, -1), (125, 165), (46, 46), (260, 27), (45, 3), (174, 190), (219, 92), (51, 51), (-1, -1), 'add     [ebp+28D5560Ah], ecx', (54, 54), (280, 204), (20, 135), (57, 57), (58, 58), (59, 59), (60, 60), (223, 235), (113, 265), (55, 278), (87, 6), (19, 214), (100, 36), (-1, -1), (68, 68), (69, 69), (70, 70), (130, 24), (258, 44), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (122, 240), (79, 79), (80, 80), (-1, -1), (67, 26), (83, 83), (117, 118), (85, 85), (-1, -1), (-1, -1), (106, 73), (89, 89), (-1, -1), (-1, -1), (119, 129), (93, 93), (85, 167), (-1, -1), (96, 96), (97, 97), (123, 225), (259, 173), (229, 226), (101, 101), (269, 68), (169, 182), (104, 104), (105, 105), (154, 50), (-1, -1), (108, 108), (23, 112), (140, 99), (111, 111), (210, 202), (113, 113), (274, 56), (-1, -1), (-1, -1), (261, 42), (118, 118), (32, 115), (267, 209), (121, 121), (122, 122), (123, 123), (231, 256), (125, 125), (126, 126), (57, 206), (145, 245), (129, 129), (130, 130), (131, 131), (-1, -1), (133, 133), (155, 162), (135, 135), (136, 136), (-1, -1), (-1, -1), (-1, -1), (140, 140), (78, 197), (134, 163), (200, 103), (71, 218), (185, 283), (-1, -1), (139, 34), (188, 104), (-1, -1), (150, 150), (151, 151), (102, 253), (246, 157), (154, 154), (155, 155), 'add     [ebp+57h], ebp', (93, 255), (158, 158), (38, 144), (281, 286), (28, 146), (186, 285), (163, 163), (138, 174), (69, 37), (166, 166), (241, 111), (168, 168), (169, 169), (-1, -1), (171, 171), (58, 148), (173, 173), (205, 64), (175, 175), (176, 176), (177, 177), 'add     ds:0F215EE7Ch[edi*8], ecx', (181, 75), (128, 264), (257, 270), (160, 176), (221, 175), (101, 141), (220, 47), (88, 91), (195, 114), (158, 247), (189, 189), (80, 142), (287, 133), (-1, -1), (14, 161), (242, 166), (195, 195), (196, 196), (197, 197), 'add     [edx], edi', (131, 65), (200, 200), (190, 130), (199, 96), (183, 105), (204, 204), (-1, -1), (35, 74), (-1, -1), (168, 109), (209, 209), (210, 210), (-1, -1), (-1, -1), (213, 213), (239, 108), (215, 215), (-1, -1), (217, 217), (218, 218), (219, 219), (220, 220), (136, 10), (222, 222), (107, 266), (66, 273), (1, 21), (-1, -1), (227, 227), (228, 228), (263, 170), (5, 191), (62, 46), (232, 232), (-1, -1), (103, 36), (-1, -1), (236, 236), (184, 2), (-1, -1), (98, 137), (126, 277), (217, 250), (172, 228), (102, 70), (-1, -1), (245, 245), (246, 246), (17, 86), (248, 248), (104, 38), (83, 268), (39, 187), (270, 128), (253, 253), (22, 149), (4, 94), (256, 256), (257, 257), (222, 84), (215, 288), (260, 260), (-1, -1), (254, 248), (164, 132), (264, 264), (54, 262), (33, 9), (253, 18), (213, 203), (30, 97), (40, 227), (271, 271), (79, 127), (-1, -1), (274, 274), (131, 241), (212, 63), (77, 143), (-1, -1), (121, 110), (124, 150), (281, 281), (282, 282), (-1, -1), 'add     edi, esp', (285, 285), (51, 29), (282, 208), (159, 177)]

for i in range(0x121):
    if (type(op_ls[i]) != str):
        continue
    for j in range(0x121):
        if (type(op_ls[j]) == str):
            continue
        if (i in op_ls[j]):
            print(f"[{i}]: {op_ls[i]}")
            break
```



```
复制代码 隐藏代码
def dfs(cur, path=[]):
    # print(cur, path)
    if (cur == 27):
        print(path)
        return
    elif (type(op_ls[cur]) == str):
        return
    l = op_ls[cur][0]
    if (l != -1 and l not in path):
        new_path = path.copy()
        new_path.append(cur)
        dfs(l, new_path)
    r = op_ls[cur][1]
    if (r != -1 and r not in path):
        new_path = path.copy()
        new_path.append(cur)
        dfs(r, new_path)

dfs(0, [])
```



```
复制代码 隐藏代码
path = [11, 82, 26, 224, 66, 100, 229, 263, 164, 174, 64, 6, 193, 161, 28, 61, 223, 266, 9, 13, 8, 43, 16, 72, 258, 84, 117, 42, 251, 187, 114, 56, 20, 230, 191, 287, 208, 109, 112, 202, 199, 65, 214, 239, 98, 225, 21, 237, 184, 141, 78, 240, 277, 143, 103, 182, 160, 286, 29, 179, 181, 270, 40, 48, 45, 165, 37, 276, 63, 55, 280, 124, 231, 62, 265, 262, 254, 22, 190, 142, 134, 162, 186, 88, 106, 50, 92, 119, 32, 147, 34, 153, 157, 255, 94, 167, 241, 250, 268, 203, 183, 221, 10, 120, 267, 18, 194, 242, 172, 148, 188, 247, 17, 272, 127, 206, 35, 279, 110, 99, 259, 288, 159, 144, 71, 24, 243, 102, 269, 30, 180, 128, 145, 185, 47, 27]

last = 0
flag = ""
for cur in path:
    if (cur == op_ls[last][0]):
        flag += "0"
    else:
        flag += "1"
    last = cur
print(int(flag, 2).to_bytes(17))
# d3ctf{0ut_of_th3ForesT#}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1714377089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1714377089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714377090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1714377090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1714377091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714377091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1714377091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714377092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1714377092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714377092.webp)