---
title: 强网拟态@2025 writeup - AI/Pwn/Web/Misc/Crypto全方向
contest: 强网拟态@2025
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [smolagents, prompt_injection, ROP, ret2libc, libc_environ, AArch64_pwn, mprotect, ORW_shellcode, Spring_Gateway_Actuator, SpEL注入, file://, Refresh_header_SSRF, Jinja2_SSTI, lipsum, LCG_LLL, AES_MD5]
attack_chain: AI small_injection:smolagents系统提示词欺骗+Python子类Popen反弹shell → Pwn babystack:栈溢出+覆盖n180097847为0x1337ABC → Pwn pin_note:tcache堆编辑+environ泄露+heap交叉指针 → Pwn printf+ORW:ROP+openat+read+puts → Pwn aarch64:qemu模拟aarch64+tcache poison+environ栈迁移 → Web Spring:Actuator routes SpEL执行restrictive-property-accessor=false+resourceHandlerMapping locationValues=file:// + file:///flag → Web fetch+SSRF:Flask Refresh头+meta跳转+X-Next头7步跳到127.0.0.1:5000/_internal/secret → SSTI:Jinja2 {{set lipsum[sget('g')].os.popen(sget('p'))}} → Crypto LCG:LLL恢复s33+反推s1+生成admin_pass+AES MD5(ts) ECB+Ciallo～(∠・ω<)编码
key_payload: smolagents注入 + Actuator SpEL + Jinja2 lipsum os.popen + LCG LLL + 7步SSRF Refresh
one_liner: 强网拟态2025全方向10+题:smolagents提示词注入+ROP+heap+AArch64+Spring Gateway Actuator SpEL+Flask SSRF链+Jinja2 lipsum+RCE+LCG LLL恢复。
lesson: smolagents system prompt可被用户消息覆盖;Spring Cloud Gateway Actuator routes配置filter SpEL可执行任意SpEL + property accessor解禁;Flask Refresh header+meta refresh+X-Next串联7步跳转绕过同源+SSRF;Jinja2 lipsum全局函数os.popen SSTI;LCG高字节通过LLL格密码恢复;AArch64 libc-2.27 environ栈迁移;openat+read+puts orw链。
quality: high
---
