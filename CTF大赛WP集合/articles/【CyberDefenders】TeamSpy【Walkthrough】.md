# 【CyberDefenders】TeamSpy【Walkthrough】

> 原文: https://www.ctfiot.com/151190.html
> ID: 151190


```
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem imageinfo
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
INFO : volatility.debug : Determining profile based on KDBG search...
 Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418
 AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
 AS Layer2 : FileAddressSpace (/home/remnux/Downloads/ecorpoffice/win7ecorpoffice2010-36b02ed3.vmem)
 PAE type : No PAE
 DTB : 0x187000L
 KDBG : 0xf800029ed070L
 Number of Processors : 2
 Image Type (Service Pack) : 0
 KPCR for CPU 0 : 0xfffff800029eed00L
 KPCR for CPU 1 : 0xfffff880009ee000L
 KUSER_SHARED_DATA : 0xfffff78000000000L
 Image date and time : 2016-10-05 03:05:11 UTC+0000
 Image local date and time : 2016-10-04 21:05:11 -0600

remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem imageinfo
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
INFO : volatility.debug : Determining profile based on KDBG search...
 Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418
 AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
 AS Layer2 : FileAddressSpace (/home/remnux/Downloads/ecorpwin7/ecorpwin7-e73257c4.vmem)
 PAE type : No PAE
 DTB : 0x187000L
 KDBG : 0xf80002bf70a0L
 Number of Processors : 1
 Image Type (Service Pack) : 1
 KPCR for CPU 0 : 0xfffff80002bf8d00L
 KUSER_SHARED_DATA : 0xfffff78000000000L
 Image date and time : 2016-10-05 03:39:07 UTC+0000
 Image local date and time : 2016-10-04 21:39:07 -0600
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 malfind
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
Process: svchost.exe Pid: 2232 Address: 0x5c40000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 128, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x0000000005c40000 20 00 00 00 e0 ff 07 00 0c 00 00 00 01 00 07 00 ................
0x0000000005c40010 00 42 00 30 00 70 00 60 00 50 00 c0 00 d0 00 00 .B.0.p.`.P......
0x0000000005c40020 08 00 42 00 00 00 00 05 48 8b 45 20 48 89 c2 48 ..B.....H.E.H..H
0x0000000005c40030 8b 45 18 48 8b 00 48 89 02 48 8b 45 20 81 00 a0 .E.H..H..H.E....

0x0000000005c40000 2000 AND [EAX], AL
0x0000000005c40002 0000 ADD [EAX], AL
0x0000000005c40004 e0ff LOOPNZ 0x5c40005
0x0000000005c40006 07 POP ES
0x0000000005c40007 000c00 ADD [EAX+EAX], CL
0x0000000005c4000a 0000 ADD [EAX], AL
0x0000000005c4000c 0100 ADD [EAX], EAX
0x0000000005c4000e 07 POP ES
0x0000000005c4000f 0000 ADD [EAX], AL
0x0000000005c40011 42 INC EDX
0x0000000005c40012 0030 ADD [EAX], DH
0x0000000005c40014 007000 ADD [EAX+0x0], DH
0x0000000005c40017 60 PUSHA
0x0000000005c40018 005000 ADD [EAX+0x0], DL
0x0000000005c4001b c000d0 ROL BYTE [EAX], 0xd0
0x0000000005c4001e 0000 ADD [EAX], AL
0x0000000005c40020 0800 OR [EAX], AL
0x0000000005c40022 42 INC EDX
0x0000000005c40023 0000 ADD [EAX], AL
0x0000000005c40025 0000 ADD [EAX], AL
0x0000000005c40027 05488b4520 ADD EAX, 0x20458b48
0x0000000005c4002c 48 DEC EAX
0x0000000005c4002d 89c2 MOV EDX, EAX
0x0000000005c4002f 48 DEC EAX
0x0000000005c40030 8b4518 MOV EAX, [EBP+0x18]
0x0000000005c40033 48 DEC EAX
0x0000000005c40034 8b00 MOV EAX, [EAX]
0x0000000005c40036 48 DEC EAX
0x0000000005c40037 8902 MOV [EDX], EAX
0x0000000005c40039 48 DEC EAX
0x0000000005c4003a 8b4520 MOV EAX, [EBP+0x20]
0x0000000005c4003d 81 DB 0x81
0x0000000005c4003e 00 DB 0x0
0x0000000005c4003f a0 DB 0xa0

...省略

Process: explorer.exe Pid: 2492 Address: 0x49f0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 16, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00000000049f0000 41 ba 80 00 00 00 48 b8 f8 7c 2d ff fe 07 00 00 A.....H..|-.....
0x00000000049f0010 48 ff 20 90 41 ba 81 00 00 00 48 b8 f8 7c 2d ff H...A.....H..|-.
0x00000000049f0020 fe 07 00 00 48 ff 20 90 41 ba 82 00 00 00 48 b8 ....H...A.....H.
0x00000000049f0030 f8 7c 2d ff fe 07 00 00 48 ff 20 90 41 ba 83 00 .|-.....H...A...

0x00000000049f0000 41 INC ECX
0x00000000049f0001 ba80000000 MOV EDX, 0x80
0x00000000049f0006 48 DEC EAX
0x00000000049f0007 b8f87c2dff MOV EAX, 0xff2d7cf8
0x00000000049f000c fe07 INC BYTE [EDI]
0x00000000049f000e 0000 ADD [EAX], AL
0x00000000049f0010 48 DEC EAX
0x00000000049f0011 ff20 JMP DWORD [EAX]
0x00000000049f0013 90 NOP
0x00000000049f0014 41 INC ECX
0x00000000049f0015 ba81000000 MOV EDX, 0x81
0x00000000049f001a 48 DEC EAX
0x00000000049f001b b8f87c2dff MOV EAX, 0xff2d7cf8
0x00000000049f0020 fe07 INC BYTE [EDI]
0x00000000049f0022 0000 ADD [EAX], AL
0x00000000049f0024 48 DEC EAX
0x00000000049f0025 ff20 JMP DWORD [EAX]
0x00000000049f0027 90 NOP
0x00000000049f0028 41 INC ECX
0x00000000049f0029 ba82000000 MOV EDX, 0x82
0x00000000049f002e 48 DEC EAX
0x00000000049f002f b8f87c2dff MOV EAX, 0xff2d7cf8
0x00000000049f0034 fe07 INC BYTE [EDI]
0x00000000049f0036 0000 ADD [EAX], AL
0x00000000049f0038 48 DEC EAX
0x00000000049f0039 ff20 JMP DWORD [EAX]
0x00000000049f003b 90 NOP
0x00000000049f003c 41 INC ECX
0x00000000049f003d ba DB 0xba
0x00000000049f003e 83 DB 0x83
0x00000000049f003f 00 DB 0x0

Process: SkypeC2AutoUpd Pid: 1364 Address: 0x310000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 1, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x0000000000310000 00 00 00 00 40 0d 31 00 15 00 00 00 00 00 00 00 ....@.1.........
0x0000000000310010 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0000000000310020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0000000000310030 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................

0x0000000000310000 0000 ADD [EAX], AL
0x0000000000310002 0000 ADD [EAX], AL
0x0000000000310004 40 INC EAX
0x0000000000310005 0d31001500 OR EAX, 0x150031
0x000000000031000a 0000 ADD [EAX], AL
0x000000000031000c 0000 ADD [EAX], AL
0x000000000031000e 0000 ADD [EAX], AL
0x0000000000310010 0000 ADD [EAX], AL
0x0000000000310012 0000 ADD [EAX], AL
0x0000000000310014 0000 ADD [EAX], AL
0x0000000000310016 0000 ADD [EAX], AL
0x0000000000310018 0000 ADD [EAX], AL
0x000000000031001a 0000 ADD [EAX], AL
0x000000000031001c 0000 ADD [EAX], AL
0x000000000031001e 0000 ADD [EAX], AL
0x0000000000310020 0000 ADD [EAX], AL
0x0000000000310022 0000 ADD [EAX], AL
0x0000000000310024 0000 ADD [EAX], AL
0x0000000000310026 0000 ADD [EAX], AL
0x0000000000310028 0000 ADD [EAX], AL
0x000000000031002a 0000 ADD [EAX], AL
0x000000000031002c 0000 ADD [EAX], AL
0x000000000031002e 0000 ADD [EAX], AL
0x0000000000310030 0000 ADD [EAX], AL
0x0000000000310032 0000 ADD [EAX], AL
0x0000000000310034 0000 ADD [EAX], AL
0x0000000000310036 0000 ADD [EAX], AL
0x0000000000310038 0000 ADD [EAX], AL
0x000000000031003a 0000 ADD [EAX], AL
0x000000000031003c 0000 ADD [EAX], AL
0x000000000031003e 0000 ADD [EAX], AL

Process: SkypeC2AutoUpd Pid: 1364 Address: 0xe00000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 1, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x0000000000e00000 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0000000000e00010 00 00 e0 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0000000000e00020 10 00 e0 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0000000000e00030 20 00 e0 00 00 00 00 00 00 00 00 00 00 00 00 00 ................

0x0000000000e00000 0000 ADD [EAX], AL
0x0000000000e00002 0000 ADD [EAX], AL
0x0000000000e00004 0000 ADD [EAX], AL
0x0000000000e00006 0000 ADD [EAX], AL
0x0000000000e00008 0000 ADD [EAX], AL
0x0000000000e0000a 0000 ADD [EAX], AL
0x0000000000e0000c 0000 ADD [EAX], AL
0x0000000000e0000e 0000 ADD [EAX], AL
0x0000000000e00010 0000 ADD [EAX], AL
0x0000000000e00012 e000 LOOPNZ 0xe00014
0x0000000000e00014 0000 ADD [EAX], AL
0x0000000000e00016 0000 ADD [EAX], AL
0x0000000000e00018 0000 ADD [EAX], AL
0x0000000000e0001a 0000 ADD [EAX], AL
0x0000000000e0001c 0000 ADD [EAX], AL
0x0000000000e0001e 0000 ADD [EAX], AL
0x0000000000e00020 1000 ADC [EAX], AL
0x0000000000e00022 e000 LOOPNZ 0xe00024
0x0000000000e00024 0000 ADD [EAX], AL
0x0000000000e00026 0000 ADD [EAX], AL
0x0000000000e00028 0000 ADD [EAX], AL
0x0000000000e0002a 0000 ADD [EAX], AL
0x0000000000e0002c 0000 ADD [EAX], AL
0x0000000000e0002e 0000 ADD [EAX], AL
0x0000000000e00030 2000 AND [EAX], AL
0x0000000000e00032 e000 LOOPNZ 0xe00034
0x0000000000e00034 0000 ADD [EAX], AL
0x0000000000e00036 0000 ADD [EAX], AL
0x0000000000e00038 0000 ADD [EAX], AL
0x0000000000e0003a 0000 ADD [EAX], AL
0x0000000000e0003c 0000 ADD [EAX], AL
0x0000000000e0003e 0000 ADD [EAX], AL

...省略
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 procdump -p 1364 -D out
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
Process(V) ImageBase Name Result
------------------ ------------------ -------------------- ------
0xfffffa8003ec7a70 0x0000000000400000 SkypeC2AutoUpd OK: executable.1364.exe
remnux@remnux:~/Downloads/ecorpoffice$
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 memdump -p 1364 -D out
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
************************************************************************
Writing SkypeC2AutoUpd [ 1364] to 1364.dmp
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 editbox
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : 0xf07848
nChars : 43
selStart : 0
selEnd : 0
isPwdControl : False
undoPos : 0
undoLen : 0
address-of undoBuf: 0x0
undoBuf :
-------------------------
Передайте свои ID 528 812 561 и пароль 8218
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : 0xf07518
nChars : 13
selStart : 0
selEnd : 0
isPwdControl : False
undoPos : 0
undoLen : 0
address-of undoBuf: 0x0
undoBuf :
-------------------------
phillip.price
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : -
-------------------------
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : 0xf06a08
nChars : 8
selStart : 0
selEnd : 0
isPwdControl : False
undoPos : 0
undoLen : 0
address-of undoBuf: 0x0
undoBuf :
-------------------------
P59fS93m
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : 0xf06858
nChars : 11
selStart : 0
selEnd : 0
isPwdControl : False
undoPos : 0
undoLen : 0
address-of undoBuf: 0x0
undoBuf :
-------------------------
528 812 561
******************************
Wnd Context : 1\WinSta0\Default
Process ID : 1364
ImageFileName : SkypeC2AutoUpd
IsWow64 : Yes
atom_class : 6.0.7600.16385!Edit
value-of WndExtra : 0xf05f70
nChars : 0
selStart : 0
selEnd : 0
isPwdControl : False
undoPos : 0
undoLen : 0
address-of undoBuf: 0x0
undoBuf :
-------------------------

******************************
Wnd Context : 1\WinSta0\Default
Process ID : 2692
ImageFileName : OUTLOOK.EXE
IsWow64 : Yes
atom_class : 6.0.7600.16385!Listbox
value-of WndExtra : 0x746f28
firstVisibleRow : 0
caretPos : -1
rowsVisible : 1
itemCount : 0
stringsStart : 0x72aa40
stringsLength : 0
-------------------------

remnux@remnux:~/Downloads/ecorpoffice$
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 pslist
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
Offset(V) Name PID PPID Thds Hnds Sess Wow64 Start Exit
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa80018af9e0 System 4 0 97 366 ------ 0 2016-10-04 12:05:22 UTC+0000
0xfffffa80027ba470 smss.exe 280 4 2 30 ------ 0 2016-10-04 12:05:22 UTC+0000
0xfffffa800336a060 csrss.exe 360 344 10 469 0 0 2016-10-04 12:05:22 UTC+0000
0xfffffa80036c81b0 wininit.exe 412 344 3 77 0 0 2016-10-04 12:05:23 UTC+0000
0xfffffa8003fb49f0 csrss.exe 428 404 11 363 1 0 2016-10-04 12:05:23 UTC+0000
0xfffffa8003631300 services.exe 460 412 10 238 0 0 2016-10-04 12:05:23 UTC+0000
0xfffffa8003a52910 lsass.exe 476 412 8 666 0 0 2016-10-04 12:05:23 UTC+0000
0xfffffa800383f700 lsm.exe 484 412 10 196 0 0 2016-10-04 12:05:23 UTC+0000
0xfffffa8003a7b060 winlogon.exe 552 404 3 112 1 0 2016-10-04 12:05:23 UTC+0000
0xfffffa800300d7c0 svchost.exe 644 460 11 359 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa80033ac7c0 vmacthlp.exe 708 460 3 57 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003535060 svchost.exe 752 460 9 301 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa80035bb810 svchost.exe 816 460 19 479 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003697290 svchost.exe 900 460 17 414 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa80036e2060 svchost.exe 928 460 39 1031 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003748b30 svchost.exe 372 460 15 639 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa80039cbb30 svchost.exe 924 460 22 575 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003a23b30 spoolsv.exe 1112 460 16 344 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003c2bb30 svchost.exe 1144 460 19 306 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003fc4680 VGAuthService. 1280 460 3 87 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa8003fc9b30 vmtoolsd.exe 1336 460 10 302 0 0 2016-10-04 12:05:24 UTC+0000
0xfffffa80040bf060 WmiPrvSE.exe 1580 644 11 235 0 0 2016-10-04 12:05:59 UTC+0000
0xfffffa8004100060 dllhost.exe 1772 460 14 192 0 0 2016-10-04 12:05:59 UTC+0000
0xfffffa8002a77b30 msdtc.exe 1996 460 12 136 0 0 2016-10-04 12:05:59 UTC+0000
0xfffffa8003cad060 svchost.exe 2232 460 13 354 0 0 2016-10-04 12:06:06 UTC+0000
0xfffffa8003d09140 taskhost.exe 2380 460 10 175 1 0 2016-10-04 12:06:11 UTC+0000
0xfffffa8003d49060 dwm.exe 2460 900 3 72 1 0 2016-10-04 12:06:11 UTC+0000
0xfffffa8003d4cb30 explorer.exe 2492 2436 25 800 1 0 2016-10-04 12:06:11 UTC+0000
0xfffffa8003e06b30 vmtoolsd.exe 2708 2492 7 183 1 0 2016-10-04 12:06:11 UTC+0000
0xfffffa8003e14060 chrome.exe 2896 2492 0 -------- 1 0 2016-10-04 12:06:14 UTC+0000 2016-10-05 02:55:38 UTC+0000
0xfffffa80036eaa60 svchost.exe 2940 460 5 75 0 0 2016-10-04 12:06:14 UTC+0000
0xfffffa8003597060 SearchIndexer. 3180 460 15 786 0 0 2016-10-04 12:06:17 UTC+0000
0xfffffa8004289490 OSPPSVC.EXE 3532 460 4 130 0 0 2016-10-04 12:06:21 UTC+0000
0xfffffa80041726e0 sppsvc.exe 860 460 4 152 0 0 2016-10-04 12:07:51 UTC+0000
0xfffffa8003ec7a70 SkypeC2AutoUpd 1364 2528 15 1951 1 1 2016-10-04 12:07:51 UTC+0000
0xfffffa8003dbc8e0 OUTLOOK.EXE 2692 2492 29 2082 1 1 2016-10-05 03:05:06 UTC+0000
0xfffffa80020b9960 SearchProtocol 3692 3180 13 534 1 1 2016-10-05 03:05:07 UTC+0000
0xfffffa8001b3d060 SearchFilterHo 3924 3180 5 86 0 0 2016-10-05 03:05:07 UTC+0000
0xfffffa80042beb30 cmd.exe 1920 1336 0 -------- 0 0 2016-10-05 03:05:11 UTC+0000 2016-10-05 03:05:11 UTC+0000
0xfffffa800248a750 conhost.exe 1940 360 0 -------- 0 0 2016-10-05 03:05:11 UTC+0000 2016-10-05 03:05:11 UTC+0000
0xfffffa80042e4060 ipconfig.exe 3348 1920 0 -------- 0 0 2016-10-05 03:05:11 UTC+0000 2016-10-05 03:05:11 UTC+0000
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 memdump -p 2692 -D out
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
************************************************************************
Writing OUTLOOK.EXE [ 2692] to 2692.dmp
remnux@remnux:~/Downloads/ecorpoffice$
remnux@remnux:~/Downloads/ecorpoffice$ vol.py -f win7ecorpoffice2010-36b02ed3.vmem --profile=Win7SP1x64 dumpfiles -n -u -r pst$ -D pst
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
DataSectionObject 0xfffffa8001a9ee20 2692 \Device\HarddiskVolume1\Users\phillip.price\Documents\Outlook Files\Outlook.pst
SharedCacheMap 0xfffffa8001a9ee20 2692 \Device\HarddiskVolume1\Users\phillip.price\Documents\Outlook Files\Outlook.pst
DataSectionObject 0xfffffa8003d2b520 2692 \Device\HarddiskVolume1\Users\phillip.price\AppData\Local\Microsoft\Outlook\phillip.price@e-corp.biz.pst
SharedCacheMap 0xfffffa8003d2b520 2692 \Device\HarddiskVolume1\Users\phillip.price\AppData\Local\Microsoft\Outlook\phillip.price@e-corp.biz.pst
remnux@remnux:~/Downloads/ecorpoffice$
$ sudo apt install pff-tools
remnux@remnux:~/Downloads/ecorpoffice/pst$ pffexport file.2692.0xfffffa8003cfe3b0.Outlook.pst.dat
pffexport 20180714

Opening file.
Exporting items.
Exporting folder item 1 out of 10.
Exporting folder item 2 out of 10.
Exporting appointment item 1 out of 1.
Exporting contact item 1 out of 2.
Exporting contact item 2 out of 2.
Exporting folder item 3 out of 10.
Exporting folder item 4 out of 10.
Exporting folder item 5 out of 10.
Exporting folder item 6 out of 10.
Skipped item 1 out of 1 of type: IPM.Microsoft.ScheduleData.FreeBusy.
Exporting folder item 7 out of 10.
Exporting folder item 8 out of 10.
Exporting folder item 9 out of 10.
Exporting folder item 10 out of 10.

Export completed.
remnux@remnux:~/Downloads/ecorpoffice/pst$

remnux@remnux:~/Downloads/ecorpoffice/pst$ pffexport file.2692.0xfffffa80042dcf10.phillip.price@e-corp.biz.pst.dat
pffexport 20180714

Opening file.
Exporting items.
Exporting folder item 1 out of 7.
Exporting folder item 2 out of 7.
Exporting email item 1 out of 4.
Exporting recipient.
Exporting email item 2 out of 4.
Exporting recipient.
Exporting email item 3 out of 4.
Exporting recipient.
Exporting email item 4 out of 4.
Exporting recipient.
Exporting email item 1 out of 11.
Exporting recipient.
Exporting email item 2 out of 11.
Exporting recipient.
Exporting email item 3 out of 11.
Exporting recipient.
Exporting email item 4 out of 11.
Exporting recipient.
Exporting email item 5 out of 11.
Exporting recipient.
Exporting email item 6 out of 11.
Exporting recipient.
Exporting email item 7 out of 11.
Exporting recipient.
Exporting email item 8 out of 11.
Exporting recipient.
Exporting email item 9 out of 11.
Exporting recipient.
Exporting email item 10 out of 11.
Exporting recipient.
Exporting email item 11 out of 11.
Exporting recipient.
Exporting attachment 1 out of 1.
Exporting folder item 3 out of 7.
Exporting folder item 4 out of 7.
Exporting folder item 5 out of 7.
Exporting folder item 6 out of 7.
Exporting folder item 7 out of 7.

Export completed.
remnux@remnux:~/Downloads/ecorpoffice/pst$
remnux@remnux:~/Downloads/ecorpoffice/pst$ find file.2692.0xfffffa80042dcf10.phillip.price@e-corp.biz.pst.dat.export -name "*.doc*"
file.2692.0xfffffa80042dcf10.phillip.price@e-corp.biz.pst.dat.export/Top of Outlook data file/Inbox/Message00011/Attachments/1_bank_statement_088452.doc
remnux@remnux:~/Downloads/ecorpoffice/pst$
remnux@remnux:~/Downloads/ecorpoffice/pst/file.2692.0xfffffa80042dcf10.phillip.price@e-corp.biz.pst.dat.export/Top of Outlook data file/Inbox/Message00011/Attachments$ sha256sum 1_bank_statement_088452.doc
66ba9807f532505a7a6a4efe9a1e2ea630e51ec51dddfa581ee1b2ee04933b88 1_bank_statement_088452.do
$ olevba --deobf 1_bank_statement_088452.doc
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 filescan | grep "pst$"
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
0x000000007de17f20 6 6 RW-r-- \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlscott.knowles@e-corp.biz-00000004.pst
0x000000007e267f20 27 6 RW-r-- \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlook.pst
0x000000007e2e75a0 26 0 RW-r-- \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlscott.knowles@e-corp.biz-00000004.pst
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 dumpfiles -n -r pst$ -D pst
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
DataSectionObject 0xfffffa8003467f20 2496 \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlook.pst
SharedCacheMap 0xfffffa8003467f20 2496 \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlook.pst
DataSectionObject 0xfffffa8003817f20 2496 \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlscott.knowles@e-corp.biz-00000004.pst
SharedCacheMap 0xfffffa8003817f20 2496 \Device\HarddiskVolume1\Users\scott.knowles\AppData\Local\Microsoft\Outlook\Outlscott.knowles@e-corp.biz-00000004.pst
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpwin7/pst$ pffexport file.2496.0xfffffa80034e9850.Outlscott.knowles@e-corp.biz-00000004.pst.dat
pffexport 20180714

Opening file.
Exporting items.
Exporting folder item 1 out of 7.
Exporting folder item 2 out of 7.
Exporting email item 1 out of 1.
Exporting recipient.
Exporting email item 1 out of 5.
Exporting recipient.
Exporting email item 2 out of 5.
Exporting recipient.
Exporting email item 3 out of 5.
Exporting recipient.
Exporting email item 4 out of 5.
Exporting recipient.
Exporting email item 5 out of 5.
Exporting recipient.
Exporting attachment 1 out of 1.
Exporting folder item 3 out of 7.
Exporting folder item 4 out of 7.
Exporting folder item 5 out of 7.
Exporting folder item 6 out of 7.
Exporting folder item 7 out of 7.

Export completed.
remnux@remnux:~/Downloads/ecorpwin7/pst$
remnux@remnux:~/Downloads/ecorpwin7/pst/file.2496.0xfffffa80034e9850.Outlscott.knowles@e-corp.biz-00000004.pst.dat.export$ find .
.
./Top of Personal Folders
./Top of Personal Folders/Inbox
./Top of Personal Folders/Inbox/Junk
./Top of Personal Folders/Inbox/Message00003
./Top of Personal Folders/Inbox/Message00003/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Message00003/Recipients.txt
./Top of Personal Folders/Inbox/Message00003/ConversationIndex.txt
./Top of Personal Folders/Inbox/Message00003/InternetHeaders.txt
./Top of Personal Folders/Inbox/Message00003/Message.txt
./Top of Personal Folders/Inbox/Message00001
./Top of Personal Folders/Inbox/Message00001/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Message00001/Recipients.txt
./Top of Personal Folders/Inbox/Message00001/ConversationIndex.txt
./Top of Personal Folders/Inbox/Message00001/InternetHeaders.txt
./Top of Personal Folders/Inbox/Message00001/Message.txt
./Top of Personal Folders/Inbox/Message00002
./Top of Personal Folders/Inbox/Message00002/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Message00002/Recipients.txt
./Top of Personal Folders/Inbox/Message00002/ConversationIndex.txt
./Top of Personal Folders/Inbox/Message00002/InternetHeaders.txt
./Top of Personal Folders/Inbox/Message00002/Message.txt
./Top of Personal Folders/Inbox/Drafts
./Top of Personal Folders/Inbox/Outbox
./Top of Personal Folders/Inbox/Outbox/Message00001
./Top of Personal Folders/Inbox/Outbox/Message00001/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Outbox/Message00001/Recipients.txt
./Top of Personal Folders/Inbox/Outbox/Message00001/ConversationIndex.txt
./Top of Personal Folders/Inbox/Outbox/Message00001/Message.txt
./Top of Personal Folders/Inbox/Message00004
./Top of Personal Folders/Inbox/Message00004/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Message00004/Recipients.txt
./Top of Personal Folders/Inbox/Message00004/ConversationIndex.txt
./Top of Personal Folders/Inbox/Message00004/InternetHeaders.txt
./Top of Personal Folders/Inbox/Message00004/Message.txt
./Top of Personal Folders/Inbox/Message00005
./Top of Personal Folders/Inbox/Message00005/OutlookHeaders.txt
./Top of Personal Folders/Inbox/Message00005/Recipients.txt
./Top of Personal Folders/Inbox/Message00005/ConversationIndex.txt
./Top of Personal Folders/Inbox/Message00005/Attachments
./Top of Personal Folders/Inbox/Message00005/Attachments/1_Important_ECORP_Lawsuit_Washington_Leak.rtf
./Top of Personal Folders/Inbox/Message00005/InternetHeaders.txt
./Top of Personal Folders/Inbox/Message00005/Message.txt
./Top of Personal Folders/Inbox/Trash
./Top of Personal Folders/Inbox/Sent
./Tracked Mail Processing
./SPAM Search Folder 2
./Search Root
./Search Root/All Messages
./Reminders
./ItemProcSearch
./To-Do Search
remnux@remnux:~/Downloads/ecorpwin7/pst/file.2496.0xfffffa80034e9850.Outlscott.knowles@e-corp.biz-00000004.pst.dat.export$ md5sum "./Top of Personal Folders/Inbox/Message00005/Attachments/1_Important_ECORP_Lawsuit_Washington_Leak.rtf"
d41d8cd98f00b204e9800998ecf8427e ./Top of Personal Folders/Inbox/Message00005/Attachments/1_Important_ECORP_Lawsuit_Washington_Leak.rtf
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 filescan | grep "rtf$"
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
0x000000007d6b33c0 1 0 R--r-- \Device\HarddiskVolume1\Users\scott.knowles\Documents\~$portant_ECORP_Lawsuit_Washington_Leak.rtf
0x000000007d6b3850 1 0 R--r-- \Device\HarddiskVolume1\Users\scott.knowles\Documents\Important_ECORP_Lawsuit_Washington_Leak.rtf
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 dumpfiles -Q 0x000000007d6b33c0,0x000000007d6b3850 -u -n -D rtf
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
DataSectionObject 0x7d6b33c0 None \Device\HarddiskVolume1\Users\scott.knowles\Documents\~$portant_ECORP_Lawsuit_Washington_Leak.rtf
DataSectionObject 0x7d6b3850 None \Device\HarddiskVolume1\Users\scott.knowles\Documents\Important_ECORP_Lawsuit_Washington_Leak.rtf
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 pstree
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
Name Pid PPid Thds Hnds Time
-------------------------------------------------- ------ ------ ------ ------ ----
 0xfffffa8003573b30:
explorer.exe 2172 2120 27 843 2016-10-04 14:36:24 UTC+0000
. 0xfffffa80035f2060:
vmtoolsd.exe 2304 2172 6 191 2016-10-04 14:36:25 UTC+0000
. 0xfffffa8003481790:
chrome.exe 1896 2172 35 1070 2016-10-05 03:35:25 UTC+0000
.. 0xfffffa80032bf930:
chrome.exe 3100 1896 5 174 2016-10-05 03:35:26 UTC+0000
.. 0xfffffa80036f3060:
chrome.exe 316 1896 11 156 2016-10-05 03:35:27 UTC+0000
... 0xfffffa8002e69910:
wininit.exe 384 316 3 75 2016-10-04 14:35:03 UTC+0000
.... 0xfffffa8002efdb30:
services.exe 484 384 7 207 2016-10-04 14:35:03 UTC+0000
..... 0xfffffa80030251b0:
svchost.exe 812 484 19 443 2016-10-04 14:35:04 UTC+0000
..... 0xfffffa80031e1b30:
armsvc.exe 1172 484 4 69 2016-10-04 14:35:05 UTC+0000
..... 0xfffffa800312d1d0:
spoolsv.exe 1052 484 13 322 2016-10-04 14:35:05 UTC+0000
..... 0xfffffa800353cb30:
taskhost.exe 2080 484 10 186 2016-10-04 14:36:24 UTC+0000
..... 0xfffffa8002f9a970:
svchost.exe 624 484 9 351 2016-10-04 14:35:03 UTC+0000
...... 0xfffffa800335b060:
WmiPrvSE.exe 1672 624 10 273 2016-10-04 14:36:08 UTC+0000
..... 0xfffffa8002fcbb30:
vmacthlp.exe 684 484 3 54 2016-10-04 14:35:04 UTC+0000
..... 0xfffffa8003686b30:
SearchIndexer. 2608 484 15 834 2016-10-04 14:36:31 UTC+0000
...... 0xfffffa800412cb30:
SearchProtocol 3244 2608 8 321 2016-10-05 03:38:00 UTC+0000
...... 0xfffffa8003782060:
SearchFilterHo 2464 2608 5 93 2016-10-05 03:38:00 UTC+0000
..... 0xfffffa8003060060:
svchost.exe 904 484 43 1128 2016-10-04 14:35:04 UTC+0000
..... 0xfffffa80033ddb30:
msdtc.exe 1928 484 12 131 2016-10-04 14:36:11 UTC+0000
..... 0xfffffa80032893c0:
vmtoolsd.exe 1332 484 9 298 2016-10-04 14:35:06 UTC+0000
...... 0xfffffa8004057060:
cmd.exe 4084 1332 0 ------ 2016-10-05 03:39:07 UTC+0000
..... 0xfffffa8003157b30:
svchost.exe 1080 484 18 306 2016-10-04 14:35:05 UTC+0000
..... 0xfffffa800353ab30:
svchost.exe 288 484 8 169 2016-10-04 14:36:55 UTC+0000
...... 0xfffffa8003645370:
rundll32.exe 2432 288 7 858 2016-10-04 14:36:57 UTC+0000
...... 0xfffffa80037e4780:
rundll32.exe 2404 288 2 66 2016-10-04 14:36:57 UTC+0000
..... 0xfffffa8003962b30:
sppsvc.exe 3656 484 4 149 2016-10-04 14:38:08 UTC+0000
..... 0xfffffa8002ff54a0:
svchost.exe 728 484 8 301 2016-10-04 14:35:04 UTC+0000
..... 0xfffffa800323b740:
dllhost.exe 1764 484 13 191 2016-10-04 14:36:09 UTC+0000
..... 0xfffffa800304fb30:
svchost.exe 860 484 15 364 2016-10-04 14:35:04 UTC+0000
...... 0xfffffa8003556670:
dwm.exe 2132 860 5 132 2016-10-04 14:36:24 UTC+0000
..... 0xfffffa8002653630:
svchost.exe 1256 484 5 102 2016-10-05 02:02:12 UTC+0000
..... 0xfffffa80030e9550:
svchost.exe 744 484 22 548 2016-10-04 14:35:05 UTC+0000
..... 0xfffffa8003250b30:
VGAuthService. 1264 484 3 84 2016-10-04 14:35:05 UTC+0000
..... 0xfffffa80036a9b30:
svchost.exe 2772 484 11 137 2016-10-04 14:37:23 UTC+0000
..... 0xfffffa80030ae360:
svchost.exe 264 484 14 622 2016-10-04 14:35:04 UTC+0000
.... 0xfffffa8002f11b30:
lsm.exe 508 384 10 197 2016-10-04 14:35:03 UTC+0000
.... 0xfffffa8002f05b30:
lsass.exe 500 384 7 628 2016-10-04 14:35:03 UTC+0000
... 0xfffffa8002c3e740:
csrss.exe 332 316 9 509 2016-10-04 14:35:03 UTC+0000
.... 0xfffffa800264a6d0:
conhost.exe 3056 332 2 33 2016-10-05 02:12:43 UTC+0000
.. 0xfffffa80037b5b30:
chrome.exe 1788 1896 7 77 2016-10-05 03:35:25 UTC+0000
.. 0xfffffa800388b060:
chrome.exe 2812 1896 12 338 2016-10-05 03:35:32 UTC+0000
.. 0xfffffa800397d060:
chrome.exe 3000 1896 12 190 2016-10-05 03:35:27 UTC+0000
. 0xfffffa80037a7060:
OUTLOOK.EXE 2496 2172 20 2125 2016-10-04 14:37:22 UTC+0000
 0xfffffa80018ad890:
System 4 0 84 387 2016-10-04 14:35:02 UTC+0000
. 0xfffffa8002019b30:
smss.exe 252 4 2 29 2016-10-04 14:35:02 UTC+0000
 0xfffffa8002e8e950:
csrss.exe 392 376 11 390 2016-10-04 14:35:03 UTC+0000
 0xfffffa8002eba060:
winlogon.exe 428 376 3 111 2016-10-04 14:35:03 UTC+0000
 0xfffffa8003e46060:sc.exe 3580 3112 1 25 2016-10-05 02:46:00 UTC+0000
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 cmdline -p 2432,2404
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
************************************************************************
rundll32.exe pid: 2432
Command line : RUNDLL32.EXE "C:\ProgramData\test.DLL" GnrkQr 2
************************************************************************
rundll32.exe pid: 2404
Command line : RUNDLL32.EXE "C:\ProgramData\test.DLL" GnrkQr 2
remnux@remnux:~/Downloads/ecorpwin7$
remnux@remnux:~/Downloads/ecorpwin7/out$ md5sum file.None.0xfffffa8003791f10.test.DLL.dat
e297538fd11e88f35c51d59361579625 file.None.0xfffffa8003791f10.test.DLL.dat
remnux@remnux:~/Downloads/ecorpwin7/out$ md5sum file.None.0xfffffa80035ef010.test.DLL.img
2769761a23f793d93bbad3ded28e8ebd file.None.0xfffffa80035ef010.test.DLL.img
remnux@remnux:~/Downloads/ecorpwin7/out$
remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 memdump -p 288 -D out
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
************************************************************************
Writing svchost.exe [ 288] to 288.dmp

remnux@remnux:~/Downloads/ecorpwin7$ vol.py -f ecorpwin7-e73257c4.vmem --profile=Win7SP1x64 memdump -p 2432,2404 -D out
Volatility Foundation Volatility Framework 2.6.1
/usr/local/lib/python2.7/dist-packages/volatility/plugins/community/YingLi/ssh_agent_key.py:12: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
 from cryptography.hazmat.backends.openssl import backend
************************************************************************
Writing rundll32.exe [ 2432] to 2432.dmp
************************************************************************
Writing rundll32.exe [ 2404] to 2404.dmp
remnux@remnux:~/Downloads/ecorpwin7$
```
