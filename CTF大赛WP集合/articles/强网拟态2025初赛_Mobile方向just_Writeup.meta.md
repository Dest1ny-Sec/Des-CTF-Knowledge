---
title: 强网拟态2025初赛 Mobile方向 just Writeup - Unity il2cpp Frida hook
contest: 强网拟态2025初赛 Mobile方向
year: 2025
difficulty: hard
vuln_type: reverse
tags: [Unity, il2cpp, Frida, hook_clone, Arm64Writer, nop_64, crc_check, global-metadata.dat, dec_global_metadata, XOR解密, Il2CppDumper, Android_Reverse, Mobile]
attack_chain: Frida hook_clone监听子线程栈地址 → 识别libjust.so → nop_64(base+0x119F8)过CRC校验 → Il2CppDumper dump global-metadata.dat → dec_global_metadata函数:XOR解密 (src[2*v2+0x202] ^ src[2*(v9%v2)+0x202])
key_payload: Frida hook_clone + nop_64(0x119F8) CRC + global-metadata.dat XOR解密 + Il2CppDumper
one_liner: 强网拟态2025初赛Mobile just:Unity il2cpp Frida hook_clone NOP CRC+global-metadata.dat XOR解密。
lesson: Unity il2cpp游戏Mobile逆向:Frida hook clone监控子线程栈地址,识别目标so后NOP关键地址过CRC校验;global-metadata.dat需Il2CppDumper解;dec_global_metadata用XOR链式解v9%v2;Arm64Writer.w.putRet()写RET指令。
quality: high
---
