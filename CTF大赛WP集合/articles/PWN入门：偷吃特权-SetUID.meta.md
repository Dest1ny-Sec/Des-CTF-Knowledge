---
title: PWN入门 - 偷吃特权 SetUID
contest: 看雪论坛 ctfiot 系列
year: 2024
difficulty: medium
vuln_type: auth_bypass
tags: [pwn, 教程, setuid, linux-kernel, cred, inode, S_ISUID, 命令注入]
attack_chain:
  - struct cred 含 uid/gid/suid/sgid/euid/egid/fsuid/fsgid 8 个 ID
  - ls -lh 看 s 位 (rwsr-xr-x) 标识 SetUID 程序
  - do_new_mount → fs_context_for_mount → alloc_fs_context → fs_context->cred
  - sb->s_flags SB_NOSUID = 1 时忽略 suid 位
  - do_execve → do_execveat_common → bprm_execve → prepare_bprm_creds
  - prepare_creds 拷贝 current->cred 作 new
  - search_binary_handler → load_elf_binary → bprm_fill_uid
  - mode & S_ISUID 触发 bprm->cred->euid = uid (i_uid_into_mnt)
  - security_bprm_creds_from_file → cap_bprm_creds_from_file 设 suid/fsuid = euid
  - begin_new_exec → commit_creds 生效
  - 示例程序 vuln_by_user_input: snprintf echo %s → system 注入
  - 注入 "233333 ; /bin/sh" 或 "233333 && /bin/sh"
  - vuln_by_permission_leak: open private_data.bin (root 600) 拿 fd
  - 利用 setuid 拿到的 euid=root 写 0x3 (CCCCC)
key_payload: ./set_uid_example "233333 ; /bin/sh" → root shell
one_liner: 从 Linux VFS/inode/cred 结构体内核视角看 SetUID 工作机制，配合漏洞示例演示 setuid 提权 + 命令注入实战。
lesson: SetUID 加载时把 euid 改成文件属主 uid；snprintf + system 拼接用户输入是经典命令注入；fd 已 open 的文件即使 setuid 失效后仍可写。
quality: high
---
