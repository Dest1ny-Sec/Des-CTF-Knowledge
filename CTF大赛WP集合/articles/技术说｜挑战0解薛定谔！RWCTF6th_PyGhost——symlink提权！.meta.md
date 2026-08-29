---
title: RWCTF6th PyGhost - Windows LPE symlink提权(0解薛定谔题)
contest: RealWorldCTF 6th(0解薛定谔赛题)
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [LPE, Local_Privilege_Escalation, Windows, PyInstaller, symlink, named_pipe, matplotlib, os.scandir, _rmtree_unsafe, is_symlink, 0解, 薛定谔题, RWCTF, ctf低权限, nt_authority_system, 服务权限]
attack_chain: Windows服务以ctf低权限运行(RWCTFService+SMWinservice+named pipe) → 接收png/jpg/svg/pdf指令生成matplotlib图存C:\Windows\Temp\res.X.png → 0解赛题利用matplotlib临时文件可预测目录+PyInstaller的_rmtree_unsafe已知漏洞:scandir+is_dir但is_symlink被catch后continue → TOCTOU+symlink替换 → 提权
key_payload: PyInstaller _rmtree_unsafe+symlink TOCTOU + matplotlib C:\Windows\Temp + named pipe + os.scandir
one_liner: RWCTF6th PyGhost 0解薛定谔题:Windows服务matplotlib+PyInstaller _rmtree_unsafe symlink TOCTOU LPE。
lesson: 0解薛定谔题特点:必须有历史漏洞背景知识+Windows特性;PyInstaller的_rmtree_unsafe:os.scandir+entry.is_dir(follow_symlinks=False)但is_symlink被catch后continue是race;matplotlib写C:\Windows\Temp可预测目录+Windows named pipe ACL;Windows service低权限运行需提权;挑战时间3分钟+只3次机会。
quality: high
---
