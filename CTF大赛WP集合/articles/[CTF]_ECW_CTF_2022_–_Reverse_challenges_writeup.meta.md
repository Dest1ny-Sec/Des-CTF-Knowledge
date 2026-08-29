---
title: [CTF] ECW CTF 2022 – Reverse challenges writeup
contest: ECW CTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [minifilter_driver, flt_registration, xor_rand_bytes_encrypt, efi_decompress_protocol, opengl_ld_preload_hook, glsl_330_core, gl_fragcoord_uniform, glteximage2d_data_extract, ctf_re_3chals]
attack_chain: 1) Minifilter 驱动 FLT_REGISTRATION 结构 + encrypt(buf, len, value) ^ rand_bytes[i%4] + file.txt.lock → key=[\xff,\xfe,E,0] + off+value 1+2+... 累加 XOR → utf-16 输出 flag / 2) EFI Decompress Protocol + cipher utf-16 切片 + off 0x200+2*24 chr(cipher[off]+4) / 3) HotShotGL OpenGL hook.so LD_PRELOAD + glCreateShader + glTexImage2D data 提取 + #version 330 core + gl_FragCoord.x*0xF117+0xA380 % 256 + uniform AN225 / uniform int X15[63] + gl_FragCoord.x+13 + ~(a^b) 还原 flag
key_payload: key = [data[0] ^ 1 ^ 0xff, data[1] ^ 1 ^ 0xfe, data[2] ^ 1 ^ 0x45, data[3] ^ 1 ^ 0] / cipher = "x0cV$2ekF2Q..." 切片 [0x200:0x200+2*24] / glTexImage2D width=164 height=1 data <izmlvpq...> / flag[i] = ~((i*0xF117+0xA380)%256 ^ X15[i+13])
one_liner: ECW CTF 2022 三道逆向：Minifilter 驱动文件加密 + EFI Decompress Protocol UTF-16 + OpenGL hook.so LD_PRELOAD 提取 GLSL Fragment Shader uniform 计算。
lesson: OpenGL hook LD_PRELOAD glTexImage2D 是提取 Fragment Shader 输入的经典方法；Minifilter 驱动用 FLT_REGISTRATION 结构定位 PreOperation 回调是 Win 驱动逆向起点。
quality: high
---
