---
title: AVSS 2023 Writeup
contest: AVSS
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [Parcel LaunchAnywhere, broadcast GET_FLAG, am broadcast, kernel栈溢出, prepare_kernel_cred, commit_creds, ret_to_user, Android 7/8/9/10 arm64, canary泄漏, mmap共享内存, cross-slab funcptr, msg_msg UAF, kStackOverflow, kHeapUserCopy, kSysUAF]
attack_chain:
  - APP-VulnParcel: Parcel.writeInt + Bundle appendFrom 构造 Bundle[-1]=4c444e42 + VulnParcelable + Intent → LaunchAnywhere
  - APP-expReceiver: am broadcast -a com.avss.testreceiver.GET_FLAG + --es sms_body '1' + logcat -d | grep flag
  - Kernel-kStackOverflow: __NR_stackof 601 触发 my_ctu 栈溢出
  - 0x61 (pop rdi 错) + prepare_kernel_cred (0xFFFFFFC0000C1354) + 0x63 (ret) + commit_creds
  - 0x65 (skip) + ret_to_user + 0x67 (skip) + buf + get_root
  - Android 10: 先 leak canary (syscall len=0x108^0xdeadbeef 读 buf+0x100)
  - mmap 0xabcd00000 共享内存传 flag
  - Kernel-kHeapUserCopy: __NR_easyof 602 申请 slab + dmesg 读地址 + 改 funcptr
  - Kernel-kSysUAF: kfree 不置 NULL → msg_msg 复用 → UAF
key_payload: 'Parcel Bundle 4c444e42 VulnParcelable LaunchAnywhere / am broadcast --es sms_body / 0x61 0x63 0x65 0x67 ROP / prepare_kernel_cred+commit_creds+ret_to_user / canary leak 0x100 / cross-slab funcptr / msg_msg UAF'
one_liner: AVSS 2023 移动安全+内核 — Parcel LaunchAnywhere + broadcast 触发 + Android 7/8/9/10 内核栈溢出 ROP + canary 泄漏 + mmap 共享内存 + cross-slab funcptr + msg_msg UAF。
lesson: Parcel 数据可构造恶意 Bundle 触发 LaunchAnywhere;内核栈溢出 4 个字节 0x61/0x63/0x65/0x67 是 gadgets 占位;canary 在 Android 10 起必查,先 leak;UAF 经典走 msg_msg cross-cache。
quality: high
---

# AVSS 2023 Writeup

## 速读
Polaris 战队第 5 — APP + Kernel 双向覆盖。

## APP-VulnParcel
- Parcel 构造 Bundle: `4c444E42` magic + `VulnParcelable` payload
- `appendFrom(obtain3, 0, obtain3.dataSize())` 注入嵌套 Intent
- 触发 LaunchAnywhere

## APP-expReceiver
```bash
am broadcast -a com.avss.testreceiver.GET_FLAG -n com.avss.testreceiver/.IntentReceiver
logcat -d | grep flag
```

## Kernel-kStackOverflow (`__NR_stackof=601`)
- 4 个 Android 版本 (7/8/9/10) arm64 + x86
- ROP 链:
  - `0x61` 错位 pop + `prepare_kernel_cred`
  - `0x63` + `commit_creds`
  - `0x65` + `ret_to_user`
  - `0x67` + `buf` + `get_root`
- Android 10: 先 leak canary (`leak()` syscall `0x108 ^ 0xdeadbeefdeadbeef`, 读 `buf+0x100`)
- `mmap 0xabcd00000` 共享内存传 flag

## Kernel-kHeapUserCopy
- `__NR_easyof=602` 申请 2 个 slab (0x0101 + 0x0201)
- `dmesg | grep p1` 读地址
- 跨 slab 改 funcptr → onestep gadget → root

## Kernel-kSysUAF
- `del_buffer` 不置 NULL
- `msg_msg` 复用释放块 → UAF
